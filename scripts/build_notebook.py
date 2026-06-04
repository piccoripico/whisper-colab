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

                    This notebook is a thin launcher for `piccoripico/whisper-colab`.

                    Only user settings live here. The implementation is cloned from GitHub and imported from `src/whisper_colab`.

                    Steps:

                    1. Edit the settings cell.
                    2. Run the bootstrap/run cell.
                    3. Upload files, or provide Google Drive paths.
                    4. Download the generated transcript files.
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
                    #@title 1. Settings

                    # Input mode.
                    INPUT_MODE = "upload" #@param ["upload", "drive_file_paths", "drive_folder_path", "drive_file_picker", "drive_folder_picker"]

                    # Used only when INPUT_MODE is "drive_file_paths".
                    MEETING_FILE_PATHS = [
                        "/content/drive/MyDrive/path/to/meeting.mp4",
                    ]

                    # Used only when INPUT_MODE is "drive_folder_path".
                    DRIVE_FOLDER_PATH = "/content/drive/MyDrive/whisper-input" #@param {type:"string"}
                    DRIVE_RECURSIVE = False #@param {type:"boolean"}

                    # Whisper model and language settings.
                    MODEL_ID = "openai/whisper-large-v3-turbo" #@param {type:"string"}
                    IS_JAPANESE_LANGUAGE = True #@param {type:"boolean"}
                    TRANSLATE_INTO_ENGLISH = False #@param {type:"boolean"}

                    # Output settings.
                    INCLUDE_TIMESTAMPS = True #@param {type:"boolean"}
                    EXPORT_EXCEL = True #@param {type:"boolean"}
                    AUDIO_OUTPUT_DIR = "/content/whisper_audio" #@param {type:"string"}

                    # Install Python packages and ffmpeg in the Colab runtime when needed.
                    INSTALL_PACKAGES = True #@param {type:"boolean"}
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
                    #@title 2. Clone repository and run transcription

                    import subprocess
                    import sys
                    from pathlib import Path

                    REPO_URL = "https://github.com/piccoripico/whisper-colab.git"
                    REPO_DIR = Path("/content/whisper-colab")

                    if not REPO_DIR.exists():
                        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, str(REPO_DIR)], check=True)

                    sys.path.insert(0, str(REPO_DIR / "src"))

                    from whisper_colab import ColabTranscriptionConfig, run_colab_transcription  # noqa: E402

                    config = ColabTranscriptionConfig(
                        input_mode=INPUT_MODE,
                        meeting_file_paths=MEETING_FILE_PATHS,
                        drive_folder_path=DRIVE_FOLDER_PATH,
                        drive_recursive=DRIVE_RECURSIVE,
                        model_id=MODEL_ID,
                        is_japanese_language=IS_JAPANESE_LANGUAGE,
                        translate_into_english=TRANSLATE_INTO_ENGLISH,
                        include_timestamps=INCLUDE_TIMESTAMPS,
                        export_excel=EXPORT_EXCEL,
                        audio_output_dir=AUDIO_OUTPUT_DIR,
                        install_packages=INSTALL_PACKAGES,
                    )

                    results = run_colab_transcription(config)
                    results
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
    return dedent(text).lstrip("\n").splitlines(keepends=True)


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
