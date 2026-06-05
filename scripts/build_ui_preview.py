"""Build a static preview of the guided Colab UI."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "output" / "playwright" / "colab_ui_preview.html"
sys.path.insert(0, str(REPO_ROOT / "src"))

from whisper_colab.colab_ui import build_ui_preview_html  # noqa: E402


def write_preview(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_ui_preview_html(), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="HTML preview output path.",
    )
    args = parser.parse_args()

    write_preview(args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
