"""Create missing locale files for every UI language.

This script intentionally preserves existing locale files. Newly created locale
files inherit English Colab-facing copy and set only the default source language.
"""

from __future__ import annotations

import json
from pathlib import Path

from languages import UI_LANGUAGE_ORDER


ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "locales"


def build_minimal_locale(code: str, language_name: str, display_name: str) -> dict:
    return {
        "language": code,
        "display_name": display_name,
        "native_name": display_name,
        "direction": "ltr",
        "placeholders": {
            "settings.source_language_default": language_name,
        },
        "readme": {
            "title": "Whisper Colab",
            "subtitle": (
                "Google Colab notebook for Whisper transcription. "
                f"Default source language: {display_name}."
            ),
        },
    }


def sync() -> list[Path]:
    LOCALES_DIR.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for language in UI_LANGUAGE_ORDER:
        path = LOCALES_DIR / f"{language.code}.json"
        if path.exists():
            continue
        data = build_minimal_locale(
            language.code,
            language.name,
            language.display_name,
        )
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        written.append(path)
    return written


if __name__ == "__main__":
    for path in sync():
        print(path.relative_to(ROOT).as_posix())
