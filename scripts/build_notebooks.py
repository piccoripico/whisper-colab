"""Build localized Colab notebooks from the template notebook."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

from languages import UI_LANGUAGE_ORDER, source_language_param_options


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "notebook_template" / "Whisper_Colab.template.ipynb"
LOCALES_DIR = ROOT / "locales"
OUTPUT_DIR = ROOT / "notebooks"


def source_to_text(source: object) -> str:
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return str(source or "")


def text_to_source(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def clear_outputs(nb: dict) -> None:
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []


def clean_markdown(text: str) -> str:
    return re.sub(r"\*\*\s*(.*?)\s*\*\*", r"**\1**", text)


def render_intro_markdown(locale: dict, placeholders: dict) -> str:
    intro = locale.get("notebook")
    if not intro:
        return str(placeholders.get("intro_markdown", ""))

    labels = intro.get("feature_labels")
    bodies = intro.get("feature_bodies")
    if labels and bodies:
        features = "\n".join(
            f"- **{clean_markdown(label.strip())}:** {clean_markdown(body.strip())}"
            for label, body in zip(labels, bodies)
        )
    else:
        features = "\n".join(f"- {clean_markdown(item)}" for item in intro.get("features", []))
    steps = "\n".join(
        f"{index}. {clean_markdown(item)}"
        for index, item in enumerate(intro.get("how_to_use_steps", []), start=1)
    )
    notes = "\n".join(f"- {clean_markdown(item)}" for item in intro.get("notes", []))
    return "\n\n".join(
        [
            f"# {intro['title']}",
            intro["description"],
            f"## {intro['features_heading']}\n\n{features}",
            f"## {intro['how_to_use_heading']}\n\n{steps}",
            f"## {intro['notes_heading']}\n\n{notes}",
        ]
    )


def render_locale(template: dict, locale: dict) -> dict:
    nb = copy.deepcopy(template)
    language = locale["language"]
    placeholders = locale.get("placeholders", {})
    placeholders["intro_markdown"] = render_intro_markdown(locale, placeholders)

    for cell in nb.get("cells", []):
        text = source_to_text(cell.get("source", []))
        for key, value in placeholders.items():
            text = text.replace(
                f'"{{{{{key}}}}}"',
                json.dumps(str(value), ensure_ascii=False),
            )
            text = text.replace(f"{{{{{key}}}}}", str(value))
        cell["source"] = text_to_source(text)

    metadata = nb.setdefault("metadata", {})
    metadata["whisper_colab_language"] = language
    metadata["whisper_colab_source_template"] = str(TEMPLATE_PATH.relative_to(ROOT).as_posix())
    metadata.setdefault("colab", {})["name"] = f"Whisper_Colab_{language}.ipynb"
    clear_outputs(nb)
    return nb


def remove_stale_notebooks() -> None:
    for path in OUTPUT_DIR.glob("Whisper_Colab_*.ipynb"):
        path.unlink()


def build() -> list[Path]:
    template = load_json(TEMPLATE_PATH)
    base_locale = load_json(LOCALES_DIR / "en.json")
    base_placeholders = {
        **base_locale.get("placeholders", {}),
        "settings.source_language_options": source_language_param_options(),
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    remove_stale_notebooks()
    written: list[Path] = []

    for language_meta in UI_LANGUAGE_ORDER:
        locale_path = LOCALES_DIR / f"{language_meta.code}.json"
        locale = load_json(locale_path)
        locale["placeholders"] = {
            **base_placeholders,
            "settings.source_language_default": language_meta.name,
            **locale.get("placeholders", {}),
        }
        language = locale["language"]
        nb = render_locale(template, locale)
        output_path = OUTPUT_DIR / f"Whisper_Colab_{language}.ipynb"
        output_path.write_text(
            json.dumps(nb, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        written.append(output_path)

    return written


if __name__ == "__main__":
    for path in build():
        print(path.relative_to(ROOT).as_posix())
