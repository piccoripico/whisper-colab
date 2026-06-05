"""Build the generated Colab notebook."""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path
from textwrap import dedent
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "Whisper_v3.ipynb"


def build_notebook() -> dict[str, Any]:
    """Return the generated notebook as a Python object."""

    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": _source_lines(
                    """
                    # Whisper v3 Colab Transcription

                    A guided Colab notebook for transcribing audio and video files with Whisper.

                    ## Start Here

                    Click the play button on the cell below: `Launch Whisper Colab App`.

                    After the cell runs, Colab prints a Gradio URL. Open that URL in a new tab, pick files from Google Drive, choose model and output settings, then click `Run transcription` in the app.

                    ## Details

                    This notebook is a thin launcher for `piccoripico/whisper-colab`. The implementation is cloned from GitHub and imported from `src/whisper_colab`.

                    ## Input Modes

                    - `drive_folder_picker`: pick a Google Drive folder from the Gradio app.
                    - `drive_file_picker`: pick one or more Google Drive files from the Gradio app.
                    - `drive_folder_path`: enter a Google Drive folder path manually.
                    - `drive_file_paths`: enter one or more Google Drive file paths manually.
                    - `upload`: upload local files to the Colab runtime.

                    ## Settings Notes

                    - Google Drive is the recommended input source.
                    - The Gradio share URL is temporary and public while the app is running.
                    - The app allows Gradio to serve files under `/content/drive/MyDrive` and the output directory so picker and download features can work.
                    - Avoid using confidential recordings with a public share URL.

                    This notebook clones:

                    `https://github.com/piccoripico/whisper-colab.git`
                    """
                ),
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": _source_lines(
                    """
                    #@title Launch Whisper Colab App

                    # Install Python packages and ffmpeg in the Colab runtime when needed.
                    INSTALL_PACKAGES = True #@param {type:"boolean"}

                    import subprocess
                    import sys
                    from pathlib import Path

                    REPO_URL = "https://github.com/piccoripico/whisper-colab.git"
                    REPO_DIR = Path("/content/whisper-colab")

                    if not REPO_DIR.exists():
                        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, str(REPO_DIR)], check=True)

                    sys.path.insert(0, str(REPO_DIR / "src"))

                    from whisper_colab import ColabTranscriptionConfig, launch_gradio_app  # noqa: E402

                    config = ColabTranscriptionConfig(
                        install_packages=INSTALL_PACKAGES,
                    )

                    app = launch_gradio_app(config, share=True, inline=False)
                    """
                ),
            },
        ],
        "metadata": {
            "colab": {
                "provenance": [],
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }


def serialize_notebook(notebook: dict[str, Any]) -> str:
    """Serialize the notebook deterministically."""

    return json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"


def write_notebook(output_path: Path) -> None:
    output_path.write_text(serialize_notebook(build_notebook()), encoding="utf-8")


def check_notebook(output_path: Path) -> int:
    expected = serialize_notebook(build_notebook())
    actual = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
    if actual == expected:
        print(f"{output_path.name} is up to date.")
        return 0

    diff = difflib.unified_diff(
        actual.splitlines(keepends=True),
        expected.splitlines(keepends=True),
        fromfile=str(output_path),
        tofile="generated notebook",
    )
    sys.stderr.writelines(diff)
    return 1


def _source_lines(text: str) -> list[str]:
    source = dedent(text).lstrip("\n")
    return source.splitlines(keepends=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the generated notebook does not match the committed file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Notebook output path.",
    )
    args = parser.parse_args()

    if args.check:
        return check_notebook(args.output)

    write_notebook(args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
