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
                    # Whisper Colab App

                    Use this notebook to launch the Whisper Colab App.

                    ## Steps

                    1. Click `Runtime > Run all`. Change the flags in the launch cell first if needed.
                    2. Wait for the setup to finish. This can take a few minutes. If Colab asks for confirmation, such as Google Drive access, approve it.
                    3. When an address like `https://xxxxxxxxx.gradio.live` appears below, click it to open the app.

                    Keep this Colab notebook open while using the app. Closing or disconnecting the notebook stops the app.

                    ## Launch Flags

                    - `INSTALL_PACKAGES`: install or update packages and `ffmpeg` in the Colab runtime.
                    - `REQUIRE_GPU`: stop early if no CUDA GPU is available. Recommended for Whisper large models.
                    - `MOUNT_GOOGLE_DRIVE`: mount Google Drive and enable Drive picker/path modes. Turn this off for upload-only use.
                    """
                ),
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {"cellView": "form"},
                "outputs": [],
                "source": _source_lines(
                    """
                    #@title Launch Whisper Colab App

                    # Install Python packages and ffmpeg in the Colab runtime when needed.
                    INSTALL_PACKAGES = True #@param {type:"boolean"}

                    # Exit before launching the app if this runtime has no CUDA GPU.
                    REQUIRE_GPU = True #@param {type:"boolean"}

                    # Mount Google Drive and enable Drive picker/path inputs.
                    MOUNT_GOOGLE_DRIVE = True #@param {type:"boolean"}

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
                        require_gpu=REQUIRE_GPU,
                        mount_google_drive=MOUNT_GOOGLE_DRIVE,
                    )

                    app = launch_gradio_app(config, share=True, inline=False)
                    """
                ),
            },
        ],
        "metadata": {
            "accelerator": "GPU",
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
