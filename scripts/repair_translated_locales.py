"""Repair protected tokens and HTML entities in translated locale files."""

from __future__ import annotations

import json
import re
from pathlib import Path

from translate_full_locales import (
    LOCALES_DIR,
    SKIP_TRANSLATION_KEYS,
    flatten_readme,
    normalize_translated_value,
    protect,
    render_intro_markdown,
    restore,
    unflatten_readme,
)

BAD_TRANSLATION_RE = re.compile(
    r"@@|@\s+P|P\d{3,}|\d{4}\s*@@|&#\d+;|&quot;|&amp;|窶|ﾃ|譌|縺|繝|�|\?{3,}"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def repair_map(base: dict[str, str], values: dict[str, str]) -> dict[str, str]:
    repaired = dict(values)
    for key, base_value in base.items():
        if key in SKIP_TRANSLATION_KEYS or key not in repaired:
            continue
        _protected, tokens = protect(base_value)
        repaired[key] = normalize_translated_value(key, restore(str(repaired[key]), tokens))
        if BAD_TRANSLATION_RE.search(repaired[key]):
            repaired[key] = base_value
    return repaired


def main() -> None:
    base = load_json(LOCALES_DIR / "en.json")
    base_readme_flat = flatten_readme(base["readme"])
    for path in sorted(LOCALES_DIR.glob("*.json")):
        if path.stem == "en":
            continue
        data = load_json(path)
        data["placeholders"] = repair_map(base["placeholders"], data.get("placeholders", {}))
        data["labels"] = repair_map(base["labels"], data.get("labels", {}))
        readme_flat = repair_map(base_readme_flat, flatten_readme(data.get("readme", {})))
        data["readme"] = unflatten_readme(readme_flat, base["readme"])
        notebook_flat = repair_map(
            flatten_readme(base["notebook"]),
            flatten_readme(data.get("notebook", {})),
        )
        data["notebook"] = unflatten_readme(notebook_flat, base["notebook"])
        data["placeholders"]["intro_markdown"] = render_intro_markdown(data["notebook"])
        write_json(path, data)
        print(path.relative_to(LOCALES_DIR.parent).as_posix())


if __name__ == "__main__":
    main()
