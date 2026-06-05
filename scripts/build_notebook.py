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
sys.path.insert(0, str(REPO_ROOT / "src"))

from whisper_colab.colab_runner import (  # noqa: E402
    DEFAULT_AUDIO_OUTPUT_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_ZIP_FILE_NAME,
    LANGUAGE_OPTIONS,
    MODEL_OPTIONS,
)


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

                    ## Usage

                    1. Keep `USE_WIDGET_UI` enabled for the guided form, or disable it to run directly from the parameter values.
                    2. Run the bootstrap/run cell.
                    3. In widget mode, review the form and click `Run transcription`.
                    4. Upload files, or provide Google Drive paths.
                    5. Download the generated transcript files.

                    ## Input Modes

                    - `upload`: upload local files to the Colab runtime.
                    - `drive_file_paths`: enter one or more Google Drive file paths manually.
                    - `drive_folder_path`: enter a Google Drive folder path and process supported media files in that folder.
                    - `drive_file_picker`: pick one file from mounted Google Drive with a small notebook widget.
                    - `drive_folder_picker`: pick one folder from mounted Google Drive with a small notebook widget.

                    ## Settings Notes

                    - Leave `LANGUAGE` as `auto` unless you want to force a source language.
                    - Select `custom` and set `CUSTOM_LANGUAGE` only when the language you need is not in the list.
                    - Enable `TRANSLATE_TO_ENGLISH` only when you want Whisper's translation task. Whisper translates speech to English, not to an arbitrary target language.
                    - Keep `MAX_SEGMENT_SECONDS` at `0` for normal runs. Set it to a positive value, such as `1800`, only when a long recording needs to be split before transcription.
                    - Use `OUTPUT_DIR`, `EXPORT_ZIP`, and `DOWNLOAD_INDIVIDUAL_FILES` to control where transcript files are saved and how they are downloaded.

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
                    #@title 1. Settings

                    # Keep enabled for the guided widget UI. Disable to run directly from these parameters.
                    USE_WIDGET_UI = True #@param {type:"boolean"}

                    # Input mode.
                    INPUT_MODE = "upload" #@param ["upload", "drive_file_paths", "drive_folder_path", "drive_file_picker", "drive_folder_picker"]

                    # Used only when INPUT_MODE is "drive_file_paths".
                    MEETING_FILE_PATHS = [
                        "/content/drive/MyDrive/path/to/meeting.mp4",
                    ]

                    # Used only when INPUT_MODE is "drive_folder_path".
                    DRIVE_FOLDER_PATH = "/content/drive/MyDrive/whisper-input" #@param {type:"string"}
                    DRIVE_RECURSIVE = False #@param {type:"boolean"}

                    # Whisper model and generation settings.
                    MODEL_ID = "openai/whisper-large-v3-turbo" #@param __MODEL_CHOICES__
                    LANGUAGE = "auto" #@param __LANGUAGE_CHOICES__
                    CUSTOM_LANGUAGE = "" #@param {type:"string"}
                    TRANSLATE_TO_ENGLISH = False #@param {type:"boolean"}
                    MAX_SEGMENT_SECONDS = 0 #@param {type:"integer"}

                    # Output settings.
                    INCLUDE_TIMESTAMPS = True #@param {type:"boolean"}
                    EXPORT_EXCEL = True #@param {type:"boolean"}
                    AUDIO_OUTPUT_DIR = "__DEFAULT_AUDIO_OUTPUT_DIR__" #@param {type:"string"}
                    OUTPUT_DIR = "__DEFAULT_OUTPUT_DIR__" #@param {type:"string"}
                    EXPORT_ZIP = True #@param {type:"boolean"}
                    DOWNLOAD_INDIVIDUAL_FILES = False #@param {type:"boolean"}
                    ZIP_FILE_NAME = "__DEFAULT_ZIP_FILE_NAME__" #@param {type:"string"}

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
                    #@title 2. Clone repository and launch

                    import subprocess
                    import sys
                    from pathlib import Path

                    REPO_URL = "https://github.com/piccoripico/whisper-colab.git"
                    REPO_DIR = Path("/content/whisper-colab")

                    if not REPO_DIR.exists():
                        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, str(REPO_DIR)], check=True)

                    sys.path.insert(0, str(REPO_DIR / "src"))

                    from whisper_colab import ColabTranscriptionConfig, launch_colab_ui, run_colab_transcription  # noqa: E402

                    config = ColabTranscriptionConfig(
                        input_mode=INPUT_MODE,
                        meeting_file_paths=MEETING_FILE_PATHS,
                        drive_folder_path=DRIVE_FOLDER_PATH,
                        drive_recursive=DRIVE_RECURSIVE,
                        model_id=MODEL_ID,
                        language=LANGUAGE,
                        custom_language=CUSTOM_LANGUAGE,
                        translate_to_english=TRANSLATE_TO_ENGLISH,
                        include_timestamps=INCLUDE_TIMESTAMPS,
                        export_excel=EXPORT_EXCEL,
                        audio_output_dir=AUDIO_OUTPUT_DIR,
                        output_dir=OUTPUT_DIR,
                        export_zip=EXPORT_ZIP,
                        download_individual_files=DOWNLOAD_INDIVIDUAL_FILES,
                        zip_file_name=ZIP_FILE_NAME,
                        max_segment_seconds=MAX_SEGMENT_SECONDS,
                        install_packages=INSTALL_PACKAGES,
                    )

                    if USE_WIDGET_UI:
                        ui_state = launch_colab_ui(config)
                        results = ui_state
                    else:
                        results = run_colab_transcription(config)
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
    replacements = {
        "__MODEL_CHOICES__": _colab_param_choices(MODEL_OPTIONS),
        "__LANGUAGE_CHOICES__": _colab_param_choices(LANGUAGE_OPTIONS),
        "__DEFAULT_AUDIO_OUTPUT_DIR__": DEFAULT_AUDIO_OUTPUT_DIR,
        "__DEFAULT_OUTPUT_DIR__": DEFAULT_OUTPUT_DIR,
        "__DEFAULT_ZIP_FILE_NAME__": DEFAULT_ZIP_FILE_NAME,
    }
    source = dedent(text).lstrip("\n")
    for placeholder, value in replacements.items():
        source = source.replace(placeholder, value)
    return source.splitlines(keepends=True)


def _colab_param_choices(values: list[str]) -> str:
    return json.dumps(values)


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
