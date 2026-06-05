"""Widget-based Colab UI for Whisper transcription."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import asdict
from typing import Any

from .colab_runner import (
    INPUT_MODE_DRIVE_FILE_PATHS,
    INPUT_MODE_DRIVE_FILE_PICKER,
    INPUT_MODE_DRIVE_FOLDER_PATH,
    INPUT_MODE_DRIVE_FOLDER_PICKER,
    INPUT_MODE_UPLOAD,
    LANGUAGE_OPTIONS,
    MODEL_OPTIONS,
    ColabTranscriptionConfig,
    run_colab_transcription,
)

INPUT_MODE_LABELS = {
    INPUT_MODE_UPLOAD: "Upload local files",
    INPUT_MODE_DRIVE_FILE_PATHS: "Google Drive file paths",
    INPUT_MODE_DRIVE_FOLDER_PATH: "Google Drive folder path",
    INPUT_MODE_DRIVE_FILE_PICKER: "Pick a Drive file",
    INPUT_MODE_DRIVE_FOLDER_PICKER: "Pick a Drive folder",
}


def launch_colab_ui(
    initial_config: ColabTranscriptionConfig | None = None,
) -> dict[str, Any]:
    """Display an ipywidgets UI and run transcription when the user clicks the button."""

    config = initial_config or ColabTranscriptionConfig()
    widgets, display = _import_widget_modules(install_packages=config.install_packages)
    form = _build_form(widgets, config)
    status = widgets.HTML(value="")
    output = widgets.Output()
    run_button = widgets.Button(
        description="Run transcription",
        button_style="primary",
        icon="play",
        layout=widgets.Layout(width="220px"),
    )
    state: dict[str, Any] = {
        "config": config,
        "results": None,
    }

    def on_run(_button) -> None:
        status.value = "<b>Running transcription...</b>"
        run_button.disabled = True
        with output:
            output.clear_output()
            try:
                next_config = config_from_ui_values(_read_form_values(form))
                state["config"] = next_config
                state["results"] = run_colab_transcription(next_config)
                status.value = "<b>Done.</b>"
            except Exception as exc:  # noqa: BLE001
                status.value = f"<b>Error:</b> {exc}"
                raise
            finally:
                run_button.disabled = False

    run_button.on_click(on_run)
    display(
        widgets.VBox(
            [
                _header(widgets),
                _section(widgets, "Input", form["input_box"]),
                _section(widgets, "Model and language", form["model_box"]),
                _section(widgets, "Outputs", form["output_box"]),
                _section(widgets, "Runtime", form["runtime_box"]),
                widgets.HBox([run_button, status]),
                output,
            ],
            layout=widgets.Layout(width="100%", max_width="880px"),
        )
    )
    return state


def _import_widget_modules(*, install_packages: bool):
    try:
        import ipywidgets as widgets
        from IPython.display import display

        return widgets, display
    except ImportError as exc:
        if not install_packages:
            raise RuntimeError("The widget UI requires ipywidgets and IPython.") from exc

    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "ipywidgets"], check=True)
    try:
        import ipywidgets as widgets
        from IPython.display import display
    except ImportError as exc:
        raise RuntimeError("The widget UI requires ipywidgets and IPython.") from exc
    return widgets, display


def config_from_ui_values(values: dict[str, Any]) -> ColabTranscriptionConfig:
    """Build a transcription config from raw widget values."""

    return ColabTranscriptionConfig(
        input_mode=str(values["input_mode"]),
        meeting_file_paths=_parse_meeting_file_paths(str(values["meeting_file_paths"])),
        drive_folder_path=str(values["drive_folder_path"]),
        drive_recursive=bool(values["drive_recursive"]),
        model_id=str(values["model_id"]),
        language=str(values["language"]),
        custom_language=str(values["custom_language"]),
        translate_to_english=bool(values["translate_to_english"]),
        include_timestamps=bool(values["include_timestamps"]),
        export_excel=bool(values["export_excel"]),
        audio_output_dir=str(values["audio_output_dir"]),
        output_dir=str(values["output_dir"]),
        export_zip=bool(values["export_zip"]),
        download_individual_files=bool(values["download_individual_files"]),
        zip_file_name=str(values["zip_file_name"]),
        max_segment_seconds=int(values["max_segment_seconds"]),
        install_packages=bool(values["install_packages"]),
    )


def ui_values_from_config(config: ColabTranscriptionConfig) -> dict[str, Any]:
    """Return serializable UI values for a config."""

    values = asdict(config)
    values["meeting_file_paths"] = "\n".join(config.meeting_file_paths)
    return values


def _parse_meeting_file_paths(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def _build_form(widgets, config: ColabTranscriptionConfig) -> dict[str, Any]:
    values = ui_values_from_config(config)
    input_mode = widgets.Dropdown(
        options=[(INPUT_MODE_LABELS[mode], mode) for mode in _ordered_input_modes()],
        value=values["input_mode"],
        description="Input mode",
        layout=widgets.Layout(width="100%"),
    )
    meeting_file_paths = widgets.Textarea(
        value=values["meeting_file_paths"],
        description="Drive files",
        placeholder="/content/drive/MyDrive/path/to/meeting.mp4",
        rows=4,
        layout=widgets.Layout(width="100%"),
    )
    drive_folder_path = widgets.Text(
        value=values["drive_folder_path"],
        description="Drive folder",
        layout=widgets.Layout(width="100%"),
    )
    drive_recursive = widgets.Checkbox(
        value=values["drive_recursive"],
        description="Search folder recursively",
    )

    model_id = widgets.Dropdown(
        options=MODEL_OPTIONS,
        value=values["model_id"],
        description="Model",
        layout=widgets.Layout(width="100%"),
    )
    language = widgets.Dropdown(
        options=LANGUAGE_OPTIONS,
        value=values["language"],
        description="Language",
        layout=widgets.Layout(width="100%"),
    )
    custom_language = widgets.Text(
        value=values["custom_language"],
        description="Custom",
        placeholder="Example: welsh",
        layout=widgets.Layout(width="100%"),
    )
    translate_to_english = widgets.Checkbox(
        value=values["translate_to_english"],
        description="Translate to English",
    )
    max_segment_seconds = widgets.BoundedIntText(
        value=values["max_segment_seconds"],
        min=0,
        max=24 * 60 * 60,
        step=60,
        description="Split seconds",
        layout=widgets.Layout(width="320px"),
    )

    include_timestamps = widgets.Checkbox(
        value=values["include_timestamps"],
        description="Include timestamps",
    )
    export_excel = widgets.Checkbox(
        value=values["export_excel"],
        description="Export Excel",
    )
    output_dir = widgets.Text(
        value=values["output_dir"],
        description="Output dir",
        layout=widgets.Layout(width="100%"),
    )
    export_zip = widgets.Checkbox(
        value=values["export_zip"],
        description="Download ZIP archive",
    )
    download_individual_files = widgets.Checkbox(
        value=values["download_individual_files"],
        description="Download individual files",
    )
    zip_file_name = widgets.Text(
        value=values["zip_file_name"],
        description="ZIP name",
        layout=widgets.Layout(width="100%"),
    )

    audio_output_dir = widgets.Text(
        value=values["audio_output_dir"],
        description="Audio dir",
        layout=widgets.Layout(width="100%"),
    )
    install_packages = widgets.Checkbox(
        value=values["install_packages"],
        description="Install packages when needed",
    )

    controls = {
        "input_mode": input_mode,
        "meeting_file_paths": meeting_file_paths,
        "drive_folder_path": drive_folder_path,
        "drive_recursive": drive_recursive,
        "model_id": model_id,
        "language": language,
        "custom_language": custom_language,
        "translate_to_english": translate_to_english,
        "max_segment_seconds": max_segment_seconds,
        "include_timestamps": include_timestamps,
        "export_excel": export_excel,
        "output_dir": output_dir,
        "export_zip": export_zip,
        "download_individual_files": download_individual_files,
        "zip_file_name": zip_file_name,
        "audio_output_dir": audio_output_dir,
        "install_packages": install_packages,
    }
    return {
        **controls,
        "input_box": widgets.VBox(
            [
                input_mode,
                meeting_file_paths,
                drive_folder_path,
                drive_recursive,
            ]
        ),
        "model_box": widgets.VBox(
            [
                model_id,
                language,
                custom_language,
                translate_to_english,
                max_segment_seconds,
            ]
        ),
        "output_box": widgets.VBox(
            [
                include_timestamps,
                export_excel,
                output_dir,
                export_zip,
                download_individual_files,
                zip_file_name,
            ]
        ),
        "runtime_box": widgets.VBox(
            [
                audio_output_dir,
                install_packages,
            ]
        ),
    }


def _read_form_values(form: dict[str, Any]) -> dict[str, Any]:
    value_keys = [
        "input_mode",
        "meeting_file_paths",
        "drive_folder_path",
        "drive_recursive",
        "model_id",
        "language",
        "custom_language",
        "translate_to_english",
        "max_segment_seconds",
        "include_timestamps",
        "export_excel",
        "output_dir",
        "export_zip",
        "download_individual_files",
        "zip_file_name",
        "audio_output_dir",
        "install_packages",
    ]
    return {key: form[key].value for key in value_keys}


def _ordered_input_modes() -> list[str]:
    return [
        INPUT_MODE_UPLOAD,
        INPUT_MODE_DRIVE_FILE_PATHS,
        INPUT_MODE_DRIVE_FOLDER_PATH,
        INPUT_MODE_DRIVE_FILE_PICKER,
        INPUT_MODE_DRIVE_FOLDER_PICKER,
    ]


def _header(widgets):
    return widgets.HTML(
        """
        <div style="padding: 16px 18px; border: 1px solid #dadce0; border-radius: 8px;">
          <h2 style="margin: 0 0 6px 0;">Whisper Colab Transcription</h2>
          <p style="margin: 0; color: #5f6368;">
            Configure the run, then click <b>Run transcription</b>. The parameter cell remains available as a fallback.
          </p>
        </div>
        """
    )


def _section(widgets, title: str, body):
    return widgets.VBox(
        [
            widgets.HTML(f"<h3 style='margin: 18px 0 8px 0;'>{title}</h3>"),
            body,
        ],
        layout=widgets.Layout(width="100%"),
    )
