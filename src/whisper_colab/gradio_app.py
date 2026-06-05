"""Gradio app launcher for the Whisper Colab workflow."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .colab_runner import (
    DRIVE_ROOT,
    INPUT_MODE_DRIVE_FILE_PATHS,
    INPUT_MODE_DRIVE_FILE_PICKER,
    INPUT_MODE_DRIVE_FOLDER_PATH,
    INPUT_MODE_DRIVE_FOLDER_PICKER,
    INPUT_MODE_UPLOAD,
    LANGUAGE_OPTIONS,
    MODEL_OPTIONS,
    ColabTranscriptionConfig,
    _collect_drive_folder_paths,
    _collect_manual_drive_file_paths,
    _find_media_files,
    _validate_media_files,
    install_colab_dependencies,
    run_transcription_for_paths,
)

INPUT_MODE_LABELS = {
    INPUT_MODE_DRIVE_FOLDER_PICKER: "Pick a Drive folder",
    INPUT_MODE_DRIVE_FILE_PICKER: "Pick Drive files",
    INPUT_MODE_DRIVE_FOLDER_PATH: "Enter a Drive folder path",
    INPUT_MODE_DRIVE_FILE_PATHS: "Enter Drive file paths",
    INPUT_MODE_UPLOAD: "Upload local files",
}

INPUT_MODE_OPTIONS = [
    (INPUT_MODE_LABELS[INPUT_MODE_DRIVE_FOLDER_PICKER], INPUT_MODE_DRIVE_FOLDER_PICKER),
    (INPUT_MODE_LABELS[INPUT_MODE_DRIVE_FILE_PICKER], INPUT_MODE_DRIVE_FILE_PICKER),
    (INPUT_MODE_LABELS[INPUT_MODE_DRIVE_FOLDER_PATH], INPUT_MODE_DRIVE_FOLDER_PATH),
    (INPUT_MODE_LABELS[INPUT_MODE_DRIVE_FILE_PATHS], INPUT_MODE_DRIVE_FILE_PATHS),
    (INPUT_MODE_LABELS[INPUT_MODE_UPLOAD], INPUT_MODE_UPLOAD),
]


def launch_gradio_app(
    initial_config: ColabTranscriptionConfig | None = None,
    *,
    share: bool = True,
    inline: bool = False,
):
    """Launch the browser-based Gradio UI for Colab."""

    config = initial_config or ColabTranscriptionConfig()
    if config.install_packages:
        install_colab_dependencies()
    _mount_drive_for_picker()
    gr = _import_gradio(install_packages=config.install_packages)
    demo = _build_gradio_blocks(gr, config)
    return demo.launch(
        share=share,
        inline=inline,
        allowed_paths=[
            str(DRIVE_ROOT),
            str(Path(config.output_dir).expanduser()),
        ],
    )


def config_from_gradio_values(values: dict[str, Any]) -> ColabTranscriptionConfig:
    """Build a transcription config from Gradio UI values."""

    return ColabTranscriptionConfig(
        input_mode=str(values["input_mode"]),
        meeting_file_paths=_parse_drive_file_paths(str(values["drive_file_paths"])),
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
        install_packages=False,
    )


def ui_values_from_config(config: ColabTranscriptionConfig) -> dict[str, Any]:
    """Return serializable Gradio UI defaults for a config."""

    values = asdict(config)
    values["drive_file_paths"] = "\n".join(config.meeting_file_paths)
    return values


def collect_gradio_input_paths(
    *,
    input_mode: str,
    drive_file_picker: Any,
    drive_folder_picker: Any,
    drive_file_paths: str,
    drive_folder_path: str,
    uploaded_files: Any,
    drive_recursive: bool,
    drive_root: Path = DRIVE_ROOT,
) -> list[Path]:
    """Resolve Gradio input controls into validated media file paths."""

    if input_mode == INPUT_MODE_DRIVE_FOLDER_PICKER:
        return _paths_from_drive_folder_picker(
            drive_folder_picker,
            recursive=drive_recursive,
            drive_root=drive_root,
        )
    if input_mode == INPUT_MODE_DRIVE_FILE_PICKER:
        return _paths_from_drive_file_picker(drive_file_picker, drive_root=drive_root)
    if input_mode == INPUT_MODE_DRIVE_FOLDER_PATH:
        return _collect_drive_folder_paths(drive_folder_path, recursive=drive_recursive)
    if input_mode == INPUT_MODE_DRIVE_FILE_PATHS:
        return _collect_manual_drive_file_paths(_parse_drive_file_paths(drive_file_paths))
    if input_mode == INPUT_MODE_UPLOAD:
        return _paths_from_uploaded_files(uploaded_files)

    raise ValueError(f"Unsupported input_mode: {input_mode!r}")


def _build_gradio_blocks(gr, config: ColabTranscriptionConfig):
    values = ui_values_from_config(config)
    media_glob = _media_file_glob()
    with gr.Blocks(title="Whisper Colab") as demo:
        gr.Markdown(
            """
# Whisper Colab

Pick recordings from Google Drive, choose Whisper settings, and download transcripts.
The Drive picker can see files under `/content/drive/MyDrive` after Drive is mounted.
"""
        )

        with gr.Tab("Input"):
            input_mode = gr.Dropdown(
                choices=INPUT_MODE_OPTIONS,
                value=values["input_mode"],
                label="Input mode",
            )
            drive_recursive = gr.Checkbox(
                value=values["drive_recursive"],
                label="Search Drive folders recursively",
            )
            drive_folder_picker = gr.FileExplorer(
                root_dir=str(DRIVE_ROOT),
                glob="**/*",
                file_count="single",
                label="Drive folder picker",
            )
            drive_file_picker = gr.FileExplorer(
                root_dir=str(DRIVE_ROOT),
                glob=media_glob,
                file_count="multiple",
                label="Drive file picker",
            )
            drive_folder_path = gr.Textbox(
                value=values["drive_folder_path"],
                label="Drive folder path",
                placeholder="/content/drive/MyDrive/whisper-input",
            )
            drive_file_paths = gr.Textbox(
                value=values["drive_file_paths"],
                label="Drive file paths",
                lines=5,
                placeholder="/content/drive/MyDrive/path/to/meeting.mp4",
            )
            uploaded_files = gr.File(
                file_count="multiple",
                type="filepath",
                label="Upload local files",
            )

        with gr.Tab("Recognition"):
            model_id = gr.Dropdown(
                choices=MODEL_OPTIONS,
                value=values["model_id"],
                label="Whisper model",
            )
            language = gr.Dropdown(
                choices=LANGUAGE_OPTIONS,
                value=values["language"],
                label="Source language",
            )
            custom_language = gr.Textbox(
                value=values["custom_language"],
                label="Custom source language",
                placeholder="Example: welsh",
            )
            translate_to_english = gr.Checkbox(
                value=values["translate_to_english"],
                label="Translate to English",
            )
            max_segment_seconds = gr.Number(
                value=values["max_segment_seconds"],
                label="Split seconds",
                precision=0,
                minimum=0,
            )

        with gr.Tab("Outputs"):
            include_timestamps = gr.Checkbox(
                value=values["include_timestamps"],
                label="Include timestamps",
            )
            export_excel = gr.Checkbox(
                value=values["export_excel"],
                label="Export Excel",
            )
            output_dir = gr.Textbox(
                value=values["output_dir"],
                label="Output directory",
            )
            export_zip = gr.Checkbox(
                value=values["export_zip"],
                label="Create ZIP archive",
            )
            download_individual_files = gr.Checkbox(
                value=values["download_individual_files"],
                label="Also expose individual files",
            )
            zip_file_name = gr.Textbox(
                value=values["zip_file_name"],
                label="ZIP file name",
            )
            audio_output_dir = gr.Textbox(
                value=values["audio_output_dir"],
                label="Temporary audio directory",
            )

        run_button = gr.Button("Run transcription", variant="primary")
        status = gr.Textbox(label="Status", lines=8)
        output_files = gr.File(label="Download outputs", file_count="multiple")

        run_button.click(
            fn=_run_from_gradio,
            inputs=[
                input_mode,
                drive_folder_picker,
                drive_file_picker,
                drive_folder_path,
                drive_file_paths,
                uploaded_files,
                drive_recursive,
                model_id,
                language,
                custom_language,
                translate_to_english,
                max_segment_seconds,
                include_timestamps,
                export_excel,
                output_dir,
                export_zip,
                download_individual_files,
                zip_file_name,
                audio_output_dir,
            ],
            outputs=[status, output_files],
        )
    return demo


def _run_from_gradio(
    input_mode: str,
    drive_folder_picker: Any,
    drive_file_picker: Any,
    drive_folder_path: str,
    drive_file_paths: str,
    uploaded_files: Any,
    drive_recursive: bool,
    model_id: str,
    language: str,
    custom_language: str,
    translate_to_english: bool,
    max_segment_seconds: int,
    include_timestamps: bool,
    export_excel: bool,
    output_dir: str,
    export_zip: bool,
    download_individual_files: bool,
    zip_file_name: str,
    audio_output_dir: str,
) -> tuple[str, list[str]]:
    values = {
        "input_mode": input_mode,
        "drive_file_paths": drive_file_paths,
        "drive_folder_path": drive_folder_path,
        "drive_recursive": drive_recursive,
        "model_id": model_id,
        "language": language,
        "custom_language": custom_language,
        "translate_to_english": translate_to_english,
        "include_timestamps": include_timestamps,
        "export_excel": export_excel,
        "audio_output_dir": audio_output_dir,
        "output_dir": output_dir,
        "export_zip": export_zip,
        "download_individual_files": download_individual_files,
        "zip_file_name": zip_file_name,
        "max_segment_seconds": int(max_segment_seconds),
    }
    config = config_from_gradio_values(values)
    input_paths = collect_gradio_input_paths(
        input_mode=input_mode,
        drive_file_picker=drive_file_picker,
        drive_folder_picker=drive_folder_picker,
        drive_file_paths=drive_file_paths,
        drive_folder_path=drive_folder_path,
        uploaded_files=uploaded_files,
        drive_recursive=drive_recursive,
    )
    results = run_transcription_for_paths(config, input_paths, download_outputs=False)
    downloadable_files = _downloadable_files_from_results(results)
    status = _build_status_message(results, downloadable_files)
    return status, downloadable_files


def _downloadable_files_from_results(results: list[dict[str, Any]]) -> list[str]:
    files = []
    for result in results:
        for path in result.get("downloadable_files", []):
            if path not in files:
                files.append(path)
    return files


def _build_status_message(results: list[dict[str, Any]], downloadable_files: list[str]) -> str:
    if not results:
        return "No files were processed."

    lines = [f"Processed {len(results)} file(s)."]
    for result in results:
        lines.append(f"- {Path(result['source_path']).name}")
    if downloadable_files:
        lines.append("")
        lines.append("Download files are ready below.")
    return "\n".join(lines)


def _paths_from_drive_file_picker(selection: Any, *, drive_root: Path = DRIVE_ROOT) -> list[Path]:
    paths = [
        _normalize_drive_picker_path(value, drive_root=drive_root)
        for value in _flatten_selection(selection)
    ]
    if not paths:
        raise ValueError("Select one or more Drive files.")
    return _validate_media_files(paths)


def _paths_from_drive_folder_picker(
    selection: Any,
    *,
    recursive: bool,
    drive_root: Path = DRIVE_ROOT,
) -> list[Path]:
    paths = [
        _normalize_drive_picker_path(value, drive_root=drive_root)
        for value in _flatten_selection(selection)
    ]
    if not paths:
        raise ValueError("Select a Drive folder.")
    if len(paths) > 1:
        raise ValueError("Select only one Drive folder.")
    folder = paths[0]
    if not folder.is_dir():
        raise NotADirectoryError(f"Drive folder picker selection is not a folder: {folder}")
    return _find_media_files(folder, recursive=recursive)


def _paths_from_uploaded_files(uploaded_files: Any) -> list[Path]:
    paths = [
        path
        for path in (_uploaded_file_to_path(file) for file in _flatten_selection(uploaded_files))
    ]
    if not paths:
        raise ValueError("Upload one or more media files.")
    return _validate_media_files(paths)


def _uploaded_file_to_path(file: Any) -> Path:
    if isinstance(file, Path):
        return file
    if isinstance(file, str):
        return Path(file)
    name = getattr(file, "name", None)
    if name:
        return Path(name)
    path = getattr(file, "path", None)
    if path:
        return Path(path)
    raise ValueError(f"Unsupported uploaded file value: {file!r}")


def _normalize_drive_picker_path(value: str | Path, *, drive_root: Path = DRIVE_ROOT) -> Path:
    root = drive_root.expanduser().resolve()
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    path = path.expanduser().resolve()
    if not _is_relative_to(path, root):
        raise ValueError(f"Drive picker path is outside the allowed Drive root: {path}")
    return path


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _flatten_selection(selection: Any) -> list[Any]:
    if selection is None:
        return []
    if isinstance(selection, (str, Path)):
        return [selection]
    return list(selection)


def _parse_drive_file_paths(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def _media_file_glob() -> str:
    return "**/*"


def _mount_drive_for_picker() -> None:
    try:
        from google.colab import drive
    except ImportError:
        return
    drive.mount("/content/drive")


def _import_gradio(*, install_packages: bool):
    try:
        import gradio as gr

        return gr
    except ImportError as exc:
        if not install_packages:
            raise RuntimeError("The Gradio app requires gradio.") from exc

    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "gradio"], check=True)
    try:
        import gradio as gr
    except ImportError as exc:
        raise RuntimeError("The Gradio app requires gradio.") from exc
    return gr
