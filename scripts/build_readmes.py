"""Build README files for all locales."""

from __future__ import annotations

import json
from pathlib import Path

from languages import UI_LANGUAGE_ORDER


ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "locales"
DOCS_README_DIR = ROOT / "docs" / "README"
REPO = "piccoripico/whisper-colab"


LANGUAGES: list[str] = [language.code for language in UI_LANGUAGE_ORDER]


DEFAULT_LABELS = {
    "features": "Features",
    "languages": "Languages",
    "language": "Language",
    "readme": "README",
    "notebook": "Notebook",
    "repository_layout": "Repository Layout",
    "build": "Build",
    "checks": "Checks",
    "what_ci_can_test": "What CI Can Test",
    "license": "License",
}


EN_TEXT = {
    "subtitle": "Multilingual Google Colab notebooks for Whisper transcription.",
    "feature_labels": [
        "Free to use",
        "No fixed notebook-side file size limit",
        "Batch processing",
        "Google Drive support",
        "Fully online",
        "Multiple output formats",
    ],
    "feature_bodies": [
        "This notebook uses [openai/whisper](https://github.com/openai/whisper), which OpenAI open-sourced on January 17, 2023, together with Google Colab's free GPU runtime.",
        "Large audio and video files can be processed.",
        "Multiple audio and video files can be processed in one run.",
        "Files can be uploaded directly, or audio/video files stored in Google Drive can be processed.",
        "Downloads and processing are performed on Google Colab. No local computing resources are used.",
        "The notebook outputs the original JSON transcript and derived TXT, CSV, Markdown, Excel, and SRT subtitle files.",
    ],
    "template_note": (
        "The root README is the English entry point, and docs/README contains generated "
        "localized README files. The template notebook is the source notebook and contains "
        "placeholders such as `{{cell1.title}}`. Locale files provide language-specific "
        "README and Colab-facing copy. Generated notebooks are committed so Colab links "
        "stay stable."
    ),
    "checks_note": (
        "The CI workflow rebuilds README files and notebooks from the template and locale "
        "files, checks notebook JSON, verifies empty outputs, checks Python syntax in code "
        "cells, scans for obvious accidental secrets, and fails when generated files are "
        "not committed."
    ),
    "ci_items": [
        "README generation from locale files",
        "notebook generation from the template and locale files",
        "notebook JSON validity",
        "empty execution outputs",
        "Python syntax in code cells",
        "obvious accidental secrets",
        "committed generated README and notebook files matching the sources",
    ],
    "ci_limit": (
        "The full transcription path requires Colab-specific APIs, model downloads, GPU "
        "availability, and user-provided media files. Treat that path as a manual Colab "
        "smoke test after generated-file checks pass."
    ),
    "license_note": (
        "This repository's README generator, notebook template, locale files, generated "
        "notebooks, and maintenance scripts are released under the MIT License. Whisper "
        "models and third-party dependencies are governed by their respective licenses."
    ),
}


def read_locale(code: str) -> dict:
    return json.loads((LOCALES_DIR / f"{code}.json").read_text(encoding="utf-8"))


def output_path(code: str) -> Path:
    if code == "en":
        return ROOT / "README.md"
    return DOCS_README_DIR / f"README.{code}.md"


def readme_link(code: str, current_code: str) -> str:
    if current_code == "en":
        return "README.md" if code == "en" else f"docs/README/README.{code}.md"
    return "../../README.md" if code == "en" else f"README.{code}.md"


def colab_badge(code: str) -> str:
    notebook = f"notebooks/Whisper_Colab_{code}.ipynb"
    url = f"https://colab.research.google.com/github/{REPO}/blob/main/{notebook}"
    return f"[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"


def locale_text(locale: dict) -> dict:
    return {**DEFAULT_LABELS, **EN_TEXT, **locale.get("readme", {})}


def language_table(current_code: str, labels: dict[str, str]) -> str:
    lines = [
        f"| {labels['language']} | {labels['readme']} | {labels['notebook']} |",
        "| --- | --- | --- |",
    ]
    for code in LANGUAGES:
        locale = read_locale(code)
        name = locale.get("native_name") or locale.get("display_name") or code
        label = "README.md" if code == "en" else f"README.{code}.md"
        lines.append(f"| {name} | [`{label}`]({readme_link(code, current_code)}) | {colab_badge(code)} |")
    return "\n".join(lines)


def repository_sections(text: dict) -> str:
    ci_items = "\n".join(f"- {item}" for item in text["ci_items"])
    return f"""## {text['repository_layout']}

```text
.github/
  workflows/
    ci.yml
docs/
  README/
    README.<language-code>.md
locales/
  *.json
notebook_template/
  Whisper_Colab.template.ipynb
notebooks/
  Whisper_Colab_<language-code>.ipynb
scripts/
  build_notebooks.py
  build_readmes.py
  check_notebooks.py
  languages.py
  repair_translated_locales.py
  sync_locales.py
  translate_full_locales.py
.gitattributes
.gitignore
LICENSE
README.md
```

{text['template_note']}

## {text['build']}

```bash
python scripts/sync_locales.py
python scripts/build_readmes.py
python scripts/build_notebooks.py
```

## {text['checks']}

```bash
python scripts/check_notebooks.py
```

{text['checks_note']}

## {text['what_ci_can_test']}

{ci_items}

{text['ci_limit']}

## {text['license']}

{text['license_note']}
"""


def feature_lines(text: dict) -> str:
    labels = text.get("feature_labels")
    bodies = text.get("feature_bodies")
    if labels and bodies:
        return "\n".join(f"- **{label.strip()}:** {body.strip()}" for label, body in zip(labels, bodies))
    return "\n".join(f"- {item}" for item in text["features"])


def build_readme(code: str) -> str:
    locale = read_locale(code)
    text = locale_text(locale)
    labels = {**DEFAULT_LABELS, **locale.get("labels", {})}
    title = text.get("title", "Whisper Colab")
    subtitle = text["subtitle"]
    features = feature_lines(text)
    markdown = f"""# {title}

{subtitle}

## {labels['features']}

{features}

## {labels['languages']}

{language_table(code, labels)}

{repository_sections({**text, **labels})}
"""
    return markdown.rstrip() + "\n"


def remove_stale_readmes() -> None:
    expected = {"README.md"}
    expected.update(f"README.{code}.md" for code in LANGUAGES if code != "en")
    for path in ROOT.glob("README.*.md"):
        if path.name not in expected:
            path.unlink()
    for path in DOCS_README_DIR.glob("README.*.md"):
        if path.name not in expected:
            try:
                path.unlink()
            except PermissionError:
                pass


def main() -> None:
    DOCS_README_DIR.mkdir(parents=True, exist_ok=True)
    remove_stale_readmes()
    for code in LANGUAGES:
        path = output_path(code)
        path.write_text(build_readme(code), encoding="utf-8", newline="\n")
        print(path.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
