"""Static checks for generated notebooks and locale files."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "notebook_template"
GENERATED_DIR = ROOT / "notebooks"
LOCALES_DIR = ROOT / "locales"
NOTEBOOK_DIRS = [TEMPLATE_DIR, GENERATED_DIR]
SECRET_PATTERNS = {
    "OpenAI API key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Google API key": re.compile(r"AIza[0-9A-Za-z_-]{25,}"),
}


def source_to_text(source: object) -> str:
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return str(source or "")


def check_notebook(path: Path) -> list[str]:
    errors: list[str] = []
    allow_placeholders = TEMPLATE_DIR in path.parents
    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path}: invalid JSON: {exc}"]

    for index, cell in enumerate(nb.get("cells", []), start=1):
        text = source_to_text(cell.get("source", []))
        if not allow_placeholders and ("{{" in text or "}}" in text):
            errors.append(f"{path}: cell {index} contains an unresolved placeholder")

        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path}: cell {index} contains possible {label}")

        if cell.get("cell_type") == "code":
            if cell.get("execution_count") is not None:
                errors.append(f"{path}: cell {index} has execution_count")
            if cell.get("outputs"):
                errors.append(f"{path}: cell {index} has saved outputs")
            try:
                ast.parse(text or "\n")
            except SyntaxError as exc:
                errors.append(f"{path}: cell {index} has Python syntax error: {exc}")

    return errors


def main() -> int:
    errors: list[str] = []
    for path in sorted(LOCALES_DIR.glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path}: invalid locale JSON: {exc}")

    notebooks = sorted(path for root in NOTEBOOK_DIRS for path in root.glob("*.ipynb"))
    for path in notebooks:
        errors.extend(check_notebook(path))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Checked {len(notebooks)} notebooks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
