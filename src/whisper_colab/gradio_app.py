"""Gradio app launcher for the Whisper Colab workflow."""

from __future__ import annotations

import queue
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from dataclasses import asdict
from html import escape
from pathlib import Path, PurePosixPath
from tempfile import gettempdir
from typing import Any
from urllib.parse import unquote

from .colab_runner import (
    DEFAULT_DOWNLOAD_DIR,
    DEFAULT_OUTPUT_DIR,
    DRIVE_ROOT,
    INPUT_MODE_DRIVE_FILE_PATHS,
    INPUT_MODE_DRIVE_FILE_PICKER,
    INPUT_MODE_DRIVE_FOLDER_PATH,
    INPUT_MODE_DRIVE_FOLDER_PICKER,
    INPUT_MODE_UPLOAD,
    LANGUAGE_OPTIONS,
    MODEL_OPTIONS,
    SUPPORTED_MEDIA_EXTENSIONS,
    ColabTranscriptionConfig,
    _collect_drive_folder_paths,
    _collect_manual_drive_file_paths,
    _find_media_files,
    _validate_media_files,
    install_colab_dependencies,
    require_gpu_available,
    run_transcription_for_paths,
)

INPUT_MODE_LABELS = {
    INPUT_MODE_DRIVE_FOLDER_PICKER: "Pick Drive folders",
    INPUT_MODE_DRIVE_FILE_PICKER: "Pick Google Drive files",
    INPUT_MODE_DRIVE_FOLDER_PATH: "Enter Drive folder paths",
    INPUT_MODE_DRIVE_FILE_PATHS: "Enter Drive file paths",
    INPUT_MODE_UPLOAD: "Upload local files",
}

INPUT_MODE_OPTIONS = [
    (INPUT_MODE_LABELS[INPUT_MODE_DRIVE_FILE_PICKER], INPUT_MODE_DRIVE_FILE_PICKER),
    (INPUT_MODE_LABELS[INPUT_MODE_UPLOAD], INPUT_MODE_UPLOAD),
]

UPLOAD_ONLY_INPUT_MODE_OPTIONS = [
    (INPUT_MODE_LABELS[INPUT_MODE_UPLOAD], INPUT_MODE_UPLOAD),
]

OPTIONAL_BOOL_CHOICES = [
    ("Use model default", ""),
    ("True", "true"),
    ("False", "false"),
]

ATTENTION_IMPLEMENTATION_OPTIONS = [
    ("Use model default", ""),
    ("sdpa", "sdpa"),
    ("flash_attention_2", "flash_attention_2"),
    ("eager", "eager"),
]


def _language_label(language: str) -> str:
    if language == "auto":
        return "Auto"
    if language == "custom":
        return "Custom"
    return language.title()


LANGUAGE_CHOICES = [(_language_label(language), language) for language in LANGUAGE_OPTIONS]


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
    if config.require_gpu:
        require_gpu_available()
    if config.mount_google_drive:
        _mount_drive_for_picker()
    gr = _import_gradio(install_packages=config.install_packages)
    demo = _build_gradio_blocks(gr, config)
    demo.queue(default_concurrency_limit=1)
    allowed_paths = [
        str(Path(DEFAULT_DOWNLOAD_DIR).expanduser()),
        str(Path(DEFAULT_OUTPUT_DIR).expanduser()),
        str(Path(config.output_dir).expanduser()),
    ]
    if _is_drive_picker_available(config.mount_google_drive):
        allowed_paths.append(str(DRIVE_ROOT))
    else:
        allowed_paths.append(str(_drive_picker_root(False)))
    return demo.launch(
        share=share,
        inline=inline,
        allowed_paths=allowed_paths,
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
        export_zip=False,
        download_individual_files=False,
        zip_file_name=str(values["zip_file_name"]),
        max_segment_seconds=int(values["max_segment_seconds"]),
        install_packages=False,
        require_gpu=bool(values.get("require_gpu", True)),
        mount_google_drive=bool(values.get("mount_google_drive", True)),
        use_custom_output_dir=bool(values.get("use_custom_output_dir", False)),
        download_zip_on_completion=bool(values.get("download_zip_on_completion", True)),
        pipeline_chunk_length_s=int(values.get("pipeline_chunk_length_s", 0) or 0),
        pipeline_batch_size=int(values.get("pipeline_batch_size", 0) or 0),
        generate_num_beams=int(values.get("generate_num_beams", 0) or 0),
        generate_temperature=str(values.get("generate_temperature", "")),
        generate_condition_on_prev_tokens=str(values.get("generate_condition_on_prev_tokens", "")),
        generate_compression_ratio_threshold=str(
            values.get("generate_compression_ratio_threshold", "")
        ),
        generate_logprob_threshold=str(values.get("generate_logprob_threshold", "")),
        generate_no_speech_threshold=str(values.get("generate_no_speech_threshold", "")),
        model_attn_implementation=str(values.get("model_attn_implementation", "")),
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
    drive_file_picker_paths: str = "",
    drive_folder_picker_paths: str = "",
    mount_google_drive: bool = True,
    drive_root: Path = DRIVE_ROOT,
) -> list[Path]:
    """Resolve Gradio input controls into validated media file paths."""

    if input_mode != INPUT_MODE_UPLOAD and not mount_google_drive:
        raise ValueError("Google Drive input modes require Mount Google Drive to be enabled.")
    if input_mode == INPUT_MODE_DRIVE_FOLDER_PICKER:
        return _paths_from_drive_folder_picker(
            drive_folder_picker,
            fallback_folder_paths=drive_folder_picker_paths,
            recursive=drive_recursive,
            drive_root=drive_root,
        )
    if input_mode == INPUT_MODE_DRIVE_FILE_PICKER:
        return _paths_from_drive_mixed_picker(
            drive_file_picker,
            fallback_file_paths=drive_file_picker_paths,
            recursive=drive_recursive,
            drive_root=drive_root,
        )
    if input_mode == INPUT_MODE_DRIVE_FOLDER_PATH:
        return _collect_drive_folder_paths(drive_folder_path, recursive=drive_recursive)
    if input_mode == INPUT_MODE_DRIVE_FILE_PATHS:
        return _collect_manual_drive_file_paths(_parse_drive_file_paths(drive_file_paths))
    if input_mode == INPUT_MODE_UPLOAD:
        return _paths_from_uploaded_files(uploaded_files)

    raise ValueError(f"Unsupported input_mode: {input_mode!r}")


def _build_gradio_blocks(gr, config: ColabTranscriptionConfig):
    values = ui_values_from_config(config)
    drive_enabled = _is_drive_picker_available(bool(values["mount_google_drive"]))
    drive_picker_root = _drive_picker_root(drive_enabled)
    input_mode_choices = input_mode_options(drive_enabled)
    selected_input_mode = initial_input_mode(values["input_mode"], drive_enabled)
    values["input_mode"] = selected_input_mode
    (
        drive_folder_picker_interactive,
        drive_file_picker_interactive,
        drive_folder_path_interactive,
        drive_file_paths_interactive,
    ) = drive_input_interactivity(drive_enabled)
    with gr.Blocks(title="Whisper Colab App") as demo:

        def drive_browser_refresh(current_dir, selected_paths):
            return _drive_browser_refresh(current_dir, selected_paths)

        def drive_browser_go_up(current_dir, selected_paths):
            return _drive_browser_go_up(current_dir, selected_paths)

        def drive_browser_open_focused(current_dir, focused_path, selected_paths):
            return _drive_browser_open_focused(current_dir, focused_path, selected_paths)

        def drive_browser_select(rows, current_dir, selected_paths, evt: gr.SelectData):
            return _drive_browser_select(rows, current_dir, selected_paths, evt)

        drive_browser_select.__annotations__["evt"] = gr.SelectData

        gr.Markdown(
            """
# Whisper Colab App

1. Keep the Colab notebook open while using this app.
2. Pick recordings from Google Drive or upload local files.
3. Choose recognition and output settings, then run transcription.

As a rough guide, a one-hour recording may take around 10 minutes on a GPU runtime.
The exact time depends on file length, model choice, GPU availability, and Colab load.
"""
        )
        gr.Markdown(_drive_mount_message(drive_enabled))

        with gr.Tab("Input"):
            mount_google_drive = gr.Checkbox(
                value=values["mount_google_drive"],
                visible=False,
            )
            input_mode = gr.Dropdown(
                choices=input_mode_choices,
                value=selected_input_mode,
                label="Input mode",
                info=(
                    "Choose how to provide input files. Drive modes require Drive to be "
                    "mounted from the launch notebook."
                ),
            )
            language = gr.Dropdown(
                choices=LANGUAGE_CHOICES,
                value=values["language"],
                label="Source language",
                info=(
                    "For better transcription accuracy, select the language being spoken "
                    "when you know it. Use Auto only when the source language is unknown."
                ),
            )
            with gr.Group(visible=values["language"] == "custom") as custom_language_group:
                custom_language = gr.Textbox(
                    value=values["custom_language"],
                    label="Custom source language",
                    placeholder="Example: welsh",
                    info="Use this only when the language is not listed above.",
                )
            drive_recursive = gr.Checkbox(
                value=values["drive_recursive"],
                label="Search Drive folders recursively",
                info=(
                    "When enabled, selected folders also scan subfolders. "
                    "When disabled, only files directly inside selected folders are used."
                ),
                interactive=drive_enabled,
            )
            drive_folder_picker = gr.State(None)
            drive_file_picker = gr.State(None)
            drive_folder_picker_paths = gr.State("")
            with gr.Group(visible=False) as drive_folder_picker_group:
                gr.Markdown("")
            with gr.Group(
                visible=_is_input_section_visible(
                    values["input_mode"], INPUT_MODE_DRIVE_FILE_PICKER
                )
            ) as drive_file_picker_group:
                gr.Markdown(
                    "Pick Google Drive files or folders. Click a row to add it to or remove it from "
                    "the selected paths below. If you select a folder, the app transcribes supported "
                    "media files inside that folder; recursive folder scanning follows the checkbox above."
                )
                drive_browser_dir = gr.Textbox(
                    value=str(drive_picker_root),
                    label="Current Google Drive folder",
                    info="Paste a Drive folder path here, then click Refresh.",
                    interactive=drive_file_paths_interactive,
                )
                with gr.Row():
                    drive_browser_refresh_button = gr.Button("Refresh")
                    drive_browser_up_button = gr.Button("Up one folder")
                    drive_browser_open_button = gr.Button("Open selected folder")
                initial_browser_rows = _drive_browser_rows(drive_picker_root, [])
                drive_browser_table = gr.Dataframe(
                    value=initial_browser_rows,
                    headers=["Selected", "Type", "Name", "Path"],
                    datatype=["str", "str", "str", "str"],
                    interactive=False,
                    label="Google Drive picker",
                    row_count=(0, "dynamic"),
                    col_count=(4, "fixed"),
                )
                drive_file_picker_paths = gr.Textbox(
                    label="Selected Google Drive paths",
                    lines=4,
                    placeholder="/content/drive/MyDrive/path/to/meeting.mp4\n/content/drive/MyDrive/path/to/folder",
                    info=(
                        "These paths are passed to Run transcription. "
                        "You can also paste files or folders here, one per line."
                    ),
                    interactive=drive_file_paths_interactive,
                )
                drive_file_picker_paths_state = gr.State([])
                drive_browser_focused_path = gr.State("")
            with gr.Group(
                visible=_is_input_section_visible(
                    values["input_mode"], INPUT_MODE_DRIVE_FOLDER_PATH
                )
            ) as drive_folder_path_group:
                drive_folder_path = gr.Textbox(
                    value=values["drive_folder_path"],
                    label="Drive folder paths",
                    lines=5,
                    placeholder="/content/drive/MyDrive/whisper-input\n/content/drive/MyDrive/another-folder",
                    info="Enter one or more Drive folder paths, one per line.",
                    interactive=drive_folder_path_interactive,
                )
            with gr.Group(
                visible=_is_input_section_visible(values["input_mode"], INPUT_MODE_DRIVE_FILE_PATHS)
            ) as drive_file_paths_group:
                drive_file_paths = gr.Textbox(
                    value=values["drive_file_paths"],
                    label="Drive file paths",
                    lines=5,
                    placeholder="/content/drive/MyDrive/path/to/meeting.mp4",
                    info="Enter one or more Drive file paths, one per line.",
                    interactive=drive_file_paths_interactive,
                )
            with gr.Group(
                visible=_is_input_section_visible(values["input_mode"], INPUT_MODE_UPLOAD)
            ) as uploaded_files_group:
                gr.Markdown(
                    "Upload local files to the temporary Colab runtime. "
                    "Transcription starts automatically after upload completes."
                )
                uploaded_files = gr.File(
                    file_count="multiple",
                    type="filepath",
                    label="Upload local files",
                )
                upload_details = gr.Textbox(
                    label="Upload details",
                    lines=4,
                    interactive=False,
                )

        with gr.Tab("Recognition"):
            model_id = gr.Dropdown(
                choices=MODEL_OPTIONS,
                value=values["model_id"],
                label="Whisper model",
                info=(
                    "Turbo is faster and is the default. Large v3 is available when you "
                    "prefer the non-Turbo model."
                ),
            )
            translate_to_english = gr.Checkbox(
                value=values["translate_to_english"],
                label="Translate to English",
                info=(
                    "Whisper translate mode translates recognized speech to English. "
                    "It does not translate to arbitrary target languages."
                ),
            )
            with gr.Accordion("Optional Whisper parameters", open=False):
                gr.Markdown(
                    """
These settings are optional. Leave each field blank or at zero to use the model default.
"""
                )
                max_segment_seconds = gr.Number(
                    value=values["max_segment_seconds"],
                    label="Split seconds",
                    info=(
                        "Set a positive number to split extracted audio into fixed-length "
                        "segments before transcription. 0 disables this repository-level split."
                    ),
                    precision=0,
                    minimum=0,
                )
                pipeline_chunk_length_s = gr.Number(
                    value=values["pipeline_chunk_length_s"],
                    label="Pipeline chunk_length_s",
                    info=(
                        "Splits long audio inside the Transformers pipeline. "
                        "0 leaves it unset; the separate Split seconds option is usually safer."
                    ),
                    precision=0,
                    minimum=0,
                )
                pipeline_batch_size = gr.Number(
                    value=values["pipeline_batch_size"],
                    label="Pipeline batch_size",
                    info="Batch size used by the ASR pipeline. 0 leaves it unset.",
                    precision=0,
                    minimum=0,
                )
                generate_num_beams = gr.Number(
                    value=values["generate_num_beams"],
                    label="Generate num_beams",
                    info="Beam-search width. 0 leaves it unset.",
                    precision=0,
                    minimum=0,
                )
                generate_temperature = gr.Textbox(
                    value=values["generate_temperature"],
                    label="Generate temperature",
                    info="Sampling temperature. Blank leaves it unset.",
                    placeholder="Example: 0.0",
                )
                generate_condition_on_prev_tokens = gr.Dropdown(
                    choices=OPTIONAL_BOOL_CHOICES,
                    value=values["generate_condition_on_prev_tokens"],
                    label="Generate condition_on_prev_tokens",
                    info=(
                        "Whether each generation conditions on previous text. "
                        "Model default is usually best."
                    ),
                )
                generate_compression_ratio_threshold = gr.Textbox(
                    value=values["generate_compression_ratio_threshold"],
                    label="Generate compression_ratio_threshold",
                    info="Fallback threshold for repeated/compressed text. Blank leaves it unset.",
                )
                generate_logprob_threshold = gr.Textbox(
                    value=values["generate_logprob_threshold"],
                    label="Generate logprob_threshold",
                    info="Fallback threshold for low-confidence text. Blank leaves it unset.",
                )
                generate_no_speech_threshold = gr.Textbox(
                    value=values["generate_no_speech_threshold"],
                    label="Generate no_speech_threshold",
                    info="Threshold for no-speech detection. Blank leaves it unset.",
                )
                model_attn_implementation = gr.Dropdown(
                    choices=ATTENTION_IMPLEMENTATION_OPTIONS,
                    value=values["model_attn_implementation"],
                    label="Model attn_implementation",
                    info="Optional attention backend passed to model loading.",
                )

        with gr.Tab("Outputs"):
            include_timestamps = gr.Checkbox(
                value=values["include_timestamps"],
                label="Include timestamps",
                info="Add approximate segment timestamps to text and Excel outputs.",
            )
            export_excel = gr.Checkbox(
                value=values["export_excel"],
                label="Export Excel",
                info="Also save an `.xlsx` file with timestamp and text columns.",
            )
            use_custom_output_dir = gr.Checkbox(
                value=values["use_custom_output_dir"],
                label="Save all outputs to a custom folder instead of each source folder",
                info=(
                    "Off: save outputs next to each input file. "
                    "On: save all outputs to the custom folder below."
                ),
            )
            with gr.Group(visible=values["use_custom_output_dir"]) as output_dir_group:
                output_dir = gr.Textbox(
                    value=values["output_dir"],
                    label="Custom output directory",
                    info="Used only when custom output folder is enabled.",
                )
            download_zip_on_completion = gr.Checkbox(
                value=values["download_zip_on_completion"],
                label="Download a ZIP when transcription finishes (outputs are also saved in folders)",
                info=(
                    "When enabled, the app prepares one temporary ZIP after processing. "
                    "The original `.txt` and `.xlsx` outputs remain in their output folders."
                ),
            )
            with gr.Group(visible=values["download_zip_on_completion"]) as zip_file_name_group:
                zip_file_name = gr.Textbox(
                    value=values["zip_file_name"],
                    label="ZIP file name",
                    info="Name of the temporary ZIP download file.",
                )
            audio_output_dir = gr.Textbox(
                value=values["audio_output_dir"],
                label="Temporary audio directory",
                info="Temporary location for normalized WAV files and optional split segments.",
            )
            require_gpu = gr.Checkbox(
                value=values["require_gpu"],
                label="Require GPU",
                visible=False,
            )

        run_button = gr.Button(
            "Run transcription",
            variant="primary",
            interactive=selected_input_mode != INPUT_MODE_UPLOAD,
        )
        status = gr.Textbox(label="Status", lines=8)
        output_locations = gr.HTML(label="Output folders")
        auto_download = gr.HTML(label="ZIP download instructions", visible=False)
        output_files = gr.File(label="ZIP download", file_count="multiple", visible=False)
        zip_download_visible = gr.State(False)

        run_button.click(
            fn=_run_from_gradio_stream,
            inputs=[
                input_mode,
                drive_folder_picker,
                drive_file_picker,
                drive_folder_picker_paths,
                drive_file_picker_paths,
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
                mount_google_drive,
                use_custom_output_dir,
                output_dir,
                download_zip_on_completion,
                zip_file_name,
                audio_output_dir,
                require_gpu,
                pipeline_chunk_length_s,
                pipeline_batch_size,
                generate_num_beams,
                generate_temperature,
                generate_condition_on_prev_tokens,
                generate_compression_ratio_threshold,
                generate_logprob_threshold,
                generate_no_speech_threshold,
                model_attn_implementation,
                zip_download_visible,
            ],
            outputs=[status, output_locations, auto_download, output_files, zip_download_visible],
        )
        uploaded_files.upload(
            fn=_upload_details,
            inputs=uploaded_files,
            outputs=upload_details,
        )
        uploaded_files.upload(
            fn=_run_from_gradio_stream,
            inputs=[
                input_mode,
                drive_folder_picker,
                drive_file_picker,
                drive_folder_picker_paths,
                drive_file_picker_paths,
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
                mount_google_drive,
                use_custom_output_dir,
                output_dir,
                download_zip_on_completion,
                zip_file_name,
                audio_output_dir,
                require_gpu,
                pipeline_chunk_length_s,
                pipeline_batch_size,
                generate_num_beams,
                generate_temperature,
                generate_condition_on_prev_tokens,
                generate_compression_ratio_threshold,
                generate_logprob_threshold,
                generate_no_speech_threshold,
                model_attn_implementation,
                zip_download_visible,
            ],
            outputs=[status, output_locations, auto_download, output_files, zip_download_visible],
        )
        input_mode.change(
            fn=_input_visibility_updates,
            inputs=input_mode,
            outputs=[
                drive_folder_picker_group,
                drive_file_picker_group,
                drive_folder_path_group,
                drive_file_paths_group,
                uploaded_files_group,
                run_button,
            ],
        )
        use_custom_output_dir.change(
            fn=_single_visibility_update,
            inputs=use_custom_output_dir,
            outputs=output_dir_group,
        )
        download_zip_on_completion.change(
            fn=_single_visibility_update,
            inputs=download_zip_on_completion,
            outputs=zip_file_name_group,
        )
        language.change(
            fn=_custom_language_visibility_update,
            inputs=language,
            outputs=custom_language_group,
        )
        drive_browser_refresh_button.click(
            fn=drive_browser_refresh,
            inputs=[drive_browser_dir, drive_file_picker_paths_state],
            outputs=[drive_browser_table, drive_browser_dir],
        )
        drive_browser_up_button.click(
            fn=drive_browser_go_up,
            inputs=[drive_browser_dir, drive_file_picker_paths_state],
            outputs=[drive_browser_table, drive_browser_dir],
        )
        drive_browser_open_button.click(
            fn=drive_browser_open_focused,
            inputs=[drive_browser_dir, drive_browser_focused_path, drive_file_picker_paths_state],
            outputs=[drive_browser_table, drive_browser_dir],
        )
        drive_browser_table.select(
            fn=drive_browser_select,
            inputs=[drive_browser_table, drive_browser_dir, drive_file_picker_paths_state],
            outputs=[
                drive_browser_table,
                drive_file_picker_paths,
                drive_file_picker_paths_state,
                drive_browser_focused_path,
            ],
        )
        drive_file_picker_paths.change(
            fn=_manual_path_lines_to_state,
            inputs=[drive_file_picker_paths, drive_browser_dir],
            outputs=[drive_file_picker_paths_state, drive_browser_table],
        )
    return demo


def input_mode_options(drive_available: bool) -> list[tuple[str, str]]:
    if drive_available:
        return INPUT_MODE_OPTIONS
    return UPLOAD_ONLY_INPUT_MODE_OPTIONS


def initial_input_mode(input_mode: str, drive_available: bool) -> str:
    if drive_available and input_mode != INPUT_MODE_UPLOAD:
        return INPUT_MODE_DRIVE_FILE_PICKER
    if drive_available:
        return input_mode
    return INPUT_MODE_UPLOAD


def _drive_mount_message(mount_google_drive: bool) -> str:
    if mount_google_drive:
        return "Google Drive mount is enabled. Drive picker and path inputs are available."
    return "Google Drive mount is disabled or unavailable. Only upload input is available."


def drive_input_interactivity(mount_google_drive: bool) -> tuple[bool, bool, bool, bool]:
    """Return interactive states for Drive folder/file picker and path controls."""

    enabled = bool(mount_google_drive)
    return (enabled, enabled, enabled, enabled)


def _is_drive_picker_available(mount_google_drive: bool, drive_root: Path = DRIVE_ROOT) -> bool:
    return bool(mount_google_drive and drive_root.exists())


def _drive_picker_root(drive_picker_available: bool, drive_root: Path = DRIVE_ROOT) -> Path:
    if drive_picker_available:
        return drive_root
    disabled_root = Path(gettempdir()) / "whisper_colab_disabled_drive_picker"
    disabled_root.mkdir(parents=True, exist_ok=True)
    return disabled_root


def _drive_browser_rows(
    current_dir: str | Path,
    selected_paths: Any,
    *,
    drive_root: Path = DRIVE_ROOT,
) -> list[list[str]]:
    current_path = _normalize_drive_browser_dir(current_dir, drive_root=drive_root)
    selected = set(_deduplicate_path_strings(selected_paths, drop_descendants=True))
    rows = []
    for child in sorted(
        current_path.iterdir(), key=lambda path: (path.is_file(), path.name.lower())
    ):
        if child.is_dir():
            row_type = "folder"
        elif child.is_file() and child.suffix.lower() in SUPPORTED_MEDIA_EXTENSIONS:
            row_type = "file"
        else:
            continue
        display_path = _drive_display_path(child, drive_root=drive_root)
        rows.append(
            [
                "selected" if display_path in selected else "",
                row_type,
                child.name,
                display_path,
            ]
        )
    return rows


def _drive_browser_refresh(current_dir: str, selected_paths: Any) -> tuple[list[list[str]], str]:
    current_path = _normalize_drive_browser_dir(current_dir)
    return _drive_browser_rows(current_path, selected_paths), str(current_path)


def _drive_browser_go_up(current_dir: str, selected_paths: Any) -> tuple[list[list[str]], str]:
    current_path = _normalize_drive_browser_dir(current_dir)
    drive_root = DRIVE_ROOT.expanduser().resolve()
    next_dir = current_path if current_path == drive_root else current_path.parent
    if not _is_relative_to(next_dir, drive_root):
        next_dir = drive_root
    return _drive_browser_rows(next_dir, selected_paths), str(next_dir)


def _drive_browser_open_focused(
    current_dir: str,
    focused_path: str,
    selected_paths: Any,
) -> tuple[list[list[str]], str]:
    if not str(focused_path).strip():
        return _drive_browser_refresh(current_dir, selected_paths)
    next_dir = _normalize_drive_picker_path(focused_path)
    if not next_dir.is_dir():
        return _drive_browser_refresh(current_dir, selected_paths)
    return _drive_browser_rows(next_dir, selected_paths), str(next_dir)


def _drive_browser_select(
    rows: Any,
    current_dir: str,
    selected_paths: Any,
    event_data: Any,
) -> tuple[list[list[str]], str, list[str], str]:
    row = _drive_browser_selected_row(rows, event_data)
    if row is None:
        selected = _deduplicate_path_strings(selected_paths, drop_descendants=True)
        return _drive_browser_rows(current_dir, selected), "\n".join(selected), selected, ""

    row_type = str(row[1])
    path = str(row[3])
    selected = _toggle_path_selection(selected_paths, path)
    focused_path = path if row_type == "folder" else ""
    return _drive_browser_rows(current_dir, selected), "\n".join(selected), selected, focused_path


def _drive_browser_selected_row(rows: Any, event_data: Any) -> list[Any] | None:
    row_index = _drive_browser_selected_row_index(event_data)
    table_rows = _dataframe_rows(rows)
    if row_index is None or row_index < 0 or row_index >= len(table_rows):
        return None
    row = table_rows[row_index]
    if len(row) < 4:
        return None
    return row


def _drive_browser_selected_row_index(event_data: Any) -> int | None:
    index = getattr(event_data, "index", None)
    if isinstance(index, (list, tuple)):
        if not index:
            return None
        return int(index[0])
    if index is None:
        return None
    return int(index)


def _dataframe_rows(rows: Any) -> list[list[Any]]:
    if rows is None:
        return []
    if hasattr(rows, "values"):
        return rows.values.tolist()
    if isinstance(rows, dict):
        data = rows.get("data")
        return data if isinstance(data, list) else []
    return list(rows)


def _toggle_path_selection(selected_paths: Any, path: str) -> list[str]:
    selected = _deduplicate_path_strings(selected_paths, drop_descendants=True)
    if path in selected:
        selected = [selected_path for selected_path in selected if selected_path != path]
    else:
        selected = _deduplicate_path_strings([*selected, path], drop_descendants=True)
    return selected


def _manual_path_lines_to_state(
    path_lines: str, current_dir: str
) -> tuple[list[str], list[list[str]]]:
    selected = _deduplicate_path_strings(_parse_drive_file_paths(path_lines), drop_descendants=True)
    return selected, _drive_browser_rows(current_dir, selected)


def _normalize_drive_browser_dir(current_dir: str | Path, *, drive_root: Path = DRIVE_ROOT) -> Path:
    path = _normalize_drive_picker_path(str(current_dir), drive_root=drive_root)
    if not path.exists():
        raise FileNotFoundError(f"Drive folder does not exist: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Drive browser path is not a folder: {path}")
    return path


def _drive_display_path(path: Path, *, drive_root: Path = DRIVE_ROOT) -> str:
    root = drive_root.expanduser().resolve()
    resolved = path.expanduser().resolve()
    if _is_relative_to(resolved, root):
        return resolved.relative_to(root).as_posix()
    return resolved.as_posix()


def _run_from_gradio(
    input_mode: str,
    drive_folder_picker: Any,
    drive_file_picker: Any,
    drive_folder_picker_paths: str,
    drive_file_picker_paths: str,
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
    mount_google_drive: bool,
    use_custom_output_dir: bool,
    output_dir: str,
    download_zip_on_completion: bool,
    zip_file_name: str,
    audio_output_dir: str,
    require_gpu: bool,
    pipeline_chunk_length_s: int,
    pipeline_batch_size: int,
    generate_num_beams: int,
    generate_temperature: str,
    generate_condition_on_prev_tokens: str,
    generate_compression_ratio_threshold: str,
    generate_logprob_threshold: str,
    generate_no_speech_threshold: str,
    model_attn_implementation: str,
    progress_callback: Callable[[str], None] | None = None,
) -> tuple[str, str, list[str]]:
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
        "mount_google_drive": mount_google_drive,
        "use_custom_output_dir": use_custom_output_dir,
        "audio_output_dir": audio_output_dir,
        "output_dir": output_dir,
        "download_zip_on_completion": download_zip_on_completion,
        "zip_file_name": zip_file_name,
        "max_segment_seconds": int(max_segment_seconds),
        "require_gpu": require_gpu,
        "pipeline_chunk_length_s": int(pipeline_chunk_length_s),
        "pipeline_batch_size": int(pipeline_batch_size),
        "generate_num_beams": int(generate_num_beams),
        "generate_temperature": generate_temperature,
        "generate_condition_on_prev_tokens": generate_condition_on_prev_tokens,
        "generate_compression_ratio_threshold": generate_compression_ratio_threshold,
        "generate_logprob_threshold": generate_logprob_threshold,
        "generate_no_speech_threshold": generate_no_speech_threshold,
        "model_attn_implementation": model_attn_implementation,
    }
    config = config_from_gradio_values(values)
    input_paths = collect_gradio_input_paths(
        input_mode=input_mode,
        drive_file_picker=drive_file_picker,
        drive_folder_picker=drive_folder_picker,
        drive_file_picker_paths=drive_file_picker_paths,
        drive_folder_picker_paths=drive_folder_picker_paths,
        drive_file_paths=drive_file_paths,
        drive_folder_path=drive_folder_path,
        uploaded_files=uploaded_files,
        drive_recursive=drive_recursive,
        mount_google_drive=mount_google_drive,
    )
    results = run_transcription_for_paths(
        config,
        input_paths,
        download_outputs=False,
        progress_callback=progress_callback,
    )
    downloadable_files = _downloadable_files_from_results(results)
    status = _build_status_message(results, downloadable_files)
    output_locations = _build_output_locations_html(results)
    return status, output_locations, downloadable_files


def _run_from_gradio_stream(*args):
    import gradio as gr

    zip_download_visible = bool(args[-1])
    run_args = args[:-1]
    progress_messages: queue.Queue[str] = queue.Queue()
    result_queue: queue.Queue[tuple[str, Any]] = queue.Queue()
    status_lines = _initial_status_lines(run_args)
    current_locations = ""
    current_auto_download = gr.update(visible=zip_download_visible)
    current_files_update = gr.update(visible=zip_download_visible)

    def progress_callback(message: str) -> None:
        progress_messages.put(message)

    def worker() -> None:
        try:
            result_queue.put(
                (
                    "ok",
                    _run_from_gradio(*run_args, progress_callback=progress_callback),
                )
            )
        except Exception as exc:  # noqa: BLE001
            result_queue.put(("error", exc))

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    yield (
        "\n".join(status_lines),
        current_locations,
        current_auto_download,
        current_files_update,
        zip_download_visible,
    )

    while thread.is_alive() or not progress_messages.empty():
        changed = _drain_progress_messages(progress_messages, status_lines)
        if changed:
            yield (
                "\n".join(status_lines),
                current_locations,
                current_auto_download,
                current_files_update,
                zip_download_visible,
            )
        time.sleep(0.5)

    status, payload = result_queue.get()
    if status == "error":
        status_lines.append(f"Error: {payload}")
        yield (
            "\n".join(status_lines),
            current_locations,
            current_auto_download,
            current_files_update,
            zip_download_visible,
        )
        return

    final_status, current_locations, downloadable_files = payload
    status_lines.append("")
    status_lines.append(final_status)
    next_zip_visible = zip_download_visible or bool(downloadable_files)
    current_auto_download = gr.update(
        value=_build_auto_download_html(downloadable_files),
        visible=next_zip_visible,
    )
    current_files_update = gr.update(value=downloadable_files or None, visible=next_zip_visible)
    yield (
        "\n".join(status_lines),
        current_locations,
        current_auto_download,
        current_files_update,
        next_zip_visible,
    )


def _initial_status_lines(run_args: tuple[Any, ...]) -> list[str]:
    input_mode = str(run_args[0])
    uploaded_files = run_args[5]
    lines = ["Starting transcription."]
    if input_mode == INPUT_MODE_UPLOAD:
        lines.append(_upload_details(uploaded_files))
    return [line for line in lines if line]


def _drain_progress_messages(
    progress_messages: queue.Queue[str],
    status_lines: list[str],
) -> bool:
    changed = False
    while True:
        try:
            message = progress_messages.get_nowait()
        except queue.Empty:
            break
        status_lines.append(message)
        changed = True
    return changed


def input_section_visibility(input_mode: str) -> tuple[bool, bool, bool, bool, bool]:
    """Return visible states for input groups in UI output order."""

    return (
        _is_input_section_visible(input_mode, INPUT_MODE_DRIVE_FOLDER_PICKER),
        _is_input_section_visible(input_mode, INPUT_MODE_DRIVE_FILE_PICKER),
        _is_input_section_visible(input_mode, INPUT_MODE_DRIVE_FOLDER_PATH),
        _is_input_section_visible(input_mode, INPUT_MODE_DRIVE_FILE_PATHS),
        _is_input_section_visible(input_mode, INPUT_MODE_UPLOAD),
    )


def _input_visibility_updates(input_mode: str):
    import gradio as gr

    updates = [gr.update(visible=visible) for visible in input_section_visibility(input_mode)]
    updates.append(gr.update(interactive=input_mode != INPUT_MODE_UPLOAD))
    return tuple(updates)


def _single_visibility_update(visible: bool):
    import gradio as gr

    return gr.update(visible=bool(visible))


def _custom_language_visibility_update(language: str):
    import gradio as gr

    return gr.update(visible=language == "custom")


def _is_input_section_visible(input_mode: str, target_mode: str) -> bool:
    return input_mode == target_mode


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


def _build_output_locations_html(results: list[dict[str, Any]]) -> str:
    output_dirs = []
    for result in results:
        output_dir = result.get("output_dir")
        if output_dir and output_dir not in output_dirs:
            output_dirs.append(output_dir)

    if not output_dirs:
        return "<p>No output folder was created.</p>"

    items = []
    for output_dir in output_dirs:
        escaped_path = escape(str(output_dir))
        items.append(f"<li><code>{escaped_path}</code></li>")
    return (
        "<p>Outputs were saved in the folder path(s) below. "
        "Gradio cannot browse folders through a `/file=` link; use Drive or the ZIP panel to retrieve files.</p>"
        "<ul>" + "".join(items) + "</ul>"
    )


def _build_auto_download_html(downloadable_files: list[str]) -> str:
    if not downloadable_files:
        return ""

    zip_path = downloadable_files[0]
    escaped_path = escape(str(zip_path))
    return f"""
<p>
  ZIP download is ready. Use the ZIP download panel below.
  Gradio creates a browser-safe download URL for the ZIP there.
</p>
<p><code>{escaped_path}</code></p>
"""


def _upload_details(uploaded_files: Any) -> str:
    paths = [
        _uploaded_file_to_path(file)
        for file in _flatten_selection(uploaded_files)
        if file is not None
    ]
    if not paths:
        return "No upload has completed yet."

    total_size = 0
    lines = ["Upload complete: 100%"]
    for path in paths:
        size = path.stat().st_size if path.exists() else 0
        total_size += size
        lines.append(f"- {path.name}: {_format_file_size(size)}")
    lines.append(f"Total: {_format_file_size(total_size)}")
    return "\n".join(lines)


def _format_file_size(size_bytes: int) -> str:
    size = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size_bytes} B"


def _selection_to_path_lines(selection: Any) -> str:
    return "\n".join(_deduplicate_path_strings(_flatten_selection(selection)))


def _selection_to_path_lines_and_state(
    selection: Any,
    current_paths: Any,
    *,
    drop_descendants: bool = False,
) -> tuple[str, list[str]]:
    selected_values = _flatten_selection(selection)
    if selected_values:
        next_paths = _deduplicate_path_strings(
            selected_values,
            drop_descendants=drop_descendants,
        )
    else:
        next_paths = _deduplicate_path_strings(
            _flatten_selection(current_paths),
            drop_descendants=drop_descendants,
        )
    return "\n".join(next_paths), next_paths


def _selection_event_to_path_lines_and_state(
    current_paths: Any,
    selection: Any,
    event_data: Any,
    *,
    ignored_values: set[str] | None = None,
    drop_descendants: bool = False,
) -> tuple[str, list[str]]:
    current = _deduplicate_path_strings(
        _flatten_selection(current_paths),
        drop_descendants=drop_descendants,
    )
    ignored_values = ignored_values or set()
    selected_values = [
        value for value in _flatten_selection(selection) if str(value) not in ignored_values
    ]
    event_value = getattr(event_data, "value", None)
    event_values = [
        value for value in _flatten_selection(event_value) if str(value) not in ignored_values
    ]
    if len(selected_values) > 1:
        next_paths = _deduplicate_path_strings(
            selected_values,
            drop_descendants=drop_descendants,
        )
        return "\n".join(next_paths), next_paths

    changed_values = event_values or selected_values
    if getattr(event_data, "selected", True) is False:
        next_paths = [
            path for path in current if path not in set(_deduplicate_path_strings(changed_values))
        ]
    else:
        next_paths = _deduplicate_path_strings(
            [*current, *changed_values],
            drop_descendants=drop_descendants,
        )
    return "\n".join(next_paths), next_paths


def _deduplicate_path_strings(
    values: Any,
    *,
    drop_descendants: bool = False,
) -> list[str]:
    deduplicated = []
    seen = set()
    for value in _flatten_selection(values):
        path = str(value).strip()
        if not path or path in seen:
            continue
        seen.add(path)
        deduplicated.append(path)
    if drop_descendants:
        return _drop_descendant_path_strings(deduplicated)
    return deduplicated


def _drop_descendant_path_strings(values: list[str]) -> list[str]:
    kept = []
    for candidate in values:
        candidate_path = PurePosixPath(candidate)
        if any(_is_posix_descendant(candidate_path, PurePosixPath(parent)) for parent in values):
            continue
        kept.append(candidate)
    return kept


def _is_posix_descendant(candidate: PurePosixPath, parent: PurePosixPath) -> bool:
    if candidate == parent:
        return False
    try:
        candidate.relative_to(parent)
        return True
    except ValueError:
        return False


def _paths_from_drive_file_picker(
    selection: Any,
    *,
    fallback_file_paths: str = "",
    drive_root: Path = DRIVE_ROOT,
) -> list[Path]:
    selected_values = _flatten_selection(selection)
    paths = [
        _normalize_drive_picker_path(value, drive_root=drive_root) for value in selected_values
    ]
    if not paths and fallback_file_paths.strip():
        paths = [
            _normalize_drive_picker_path(value, drive_root=drive_root)
            for value in _parse_drive_file_paths(fallback_file_paths)
        ]
    if not paths:
        raise ValueError(
            "Select one or more Drive files in the picker, or paste file paths into "
            "'Selected Drive file paths'. Opening or previewing a file is not enough; "
            "it must appear as selected."
        )
    for path in paths:
        if path.is_dir():
            raise IsADirectoryError(f"Drive file picker selection is a folder: {path}")
    return _validate_media_files(paths)


def _paths_from_drive_mixed_picker(
    selection: Any,
    *,
    fallback_file_paths: str = "",
    recursive: bool,
    drive_root: Path = DRIVE_ROOT,
) -> list[Path]:
    selected_values = _flatten_selection(selection)
    if fallback_file_paths.strip():
        selected_values = _parse_drive_file_paths(fallback_file_paths)
    paths = [
        _normalize_drive_picker_path(value, drive_root=drive_root) for value in selected_values
    ]
    if not paths:
        raise ValueError(
            "Pick one or more Google Drive files or folders, or paste paths into "
            "'Selected Google Drive paths'."
        )

    file_paths = []
    folder_paths = []
    for path in paths:
        if path.is_dir():
            folder_paths.append(path)
        else:
            file_paths.append(path)

    media_files = _validate_media_files(file_paths)
    for folder in _drop_descendant_paths(folder_paths):
        media_files.extend(_find_media_files(folder, recursive=recursive))
    return _deduplicate_paths(media_files)


def _paths_from_drive_folder_picker(
    selection: Any,
    *,
    fallback_folder_paths: str = "",
    recursive: bool,
    drive_root: Path = DRIVE_ROOT,
) -> list[Path]:
    selected_values = _flatten_selection(selection)
    paths = [
        _normalize_drive_picker_path(value, drive_root=drive_root) for value in selected_values
    ]
    if not paths and fallback_folder_paths.strip():
        paths = [
            _normalize_drive_picker_path(value, drive_root=drive_root)
            for value in _parse_drive_file_paths(fallback_folder_paths)
        ]
    if not paths:
        raise ValueError(
            "Select one or more Drive folders in the picker, or paste folder paths into "
            "'Selected Drive folder paths'. Opening a folder is not enough; it must appear as selected."
        )
    paths = _drop_descendant_paths(paths)
    media_files = []
    for folder in paths:
        if not folder.is_dir():
            raise NotADirectoryError(f"Drive folder picker selection is not a folder: {folder}")
        media_files.extend(_find_media_files(folder, recursive=recursive))
    return _deduplicate_paths(media_files)


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
    raw_value = str(value)
    normalized_value = _clean_picker_path_value(raw_value, root)
    path = Path(normalized_value)
    if not path.is_absolute():
        path = root / path
    path = path.expanduser().resolve()
    if not path.exists() and not _is_relative_to(path, root):
        root_relative_path = root / str(normalized_value).lstrip("/")
        root_relative_path = root_relative_path.expanduser().resolve()
        if _is_relative_to(root_relative_path, root):
            path = root_relative_path
    if not _is_relative_to(path, root):
        raise ValueError(f"Drive picker path is outside the allowed Drive root: {path}")
    return path


def _clean_picker_path_value(value: str, drive_root: Path) -> str:
    cleaned = unquote(str(value).strip())
    if cleaned.startswith("file="):
        cleaned = cleaned.removeprefix("file=")
    if "/file=" in cleaned:
        cleaned = cleaned.split("/file=", 1)[1]
    drive_root_text = drive_root.as_posix()
    drive_root_without_slash = drive_root_text.lstrip("/")
    if cleaned.startswith(drive_root_without_slash):
        cleaned = "/" + cleaned
    return cleaned


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
    if isinstance(selection, dict):
        return _flatten_mapping_selection(selection)
    if hasattr(selection, "model_dump"):
        return _flatten_selection(selection.model_dump())
    if hasattr(selection, "dict"):
        return _flatten_selection(selection.dict())
    if hasattr(selection, "root"):
        return _flatten_selection(selection.root)
    if hasattr(selection, "value"):
        return _flatten_selection(selection.value)
    if hasattr(selection, "selected"):
        return _flatten_selection(selection.selected)
    if hasattr(selection, "files"):
        return _flatten_selection(selection.files)
    if hasattr(selection, "folders"):
        return _flatten_selection(selection.folders)
    if hasattr(selection, "path"):
        return [selection.path]
    if hasattr(selection, "name"):
        return [selection.name]
    values = []
    for item in selection:
        values.extend(_flatten_selection(item))
    return values


def _flatten_mapping_selection(selection: dict[str, Any]) -> list[Any]:
    for key in ("path", "name", "value", "selected", "files", "folders", "root"):
        value = selection.get(key)
        if value:
            return _flatten_selection(value)
    data = selection.get("data")
    if data:
        return _flatten_selection(data)
    return []


def _parse_drive_file_paths(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def _media_file_glob() -> str:
    return "**/*.*"


def _deduplicate_paths(paths: list[Path]) -> list[Path]:
    deduplicated = []
    seen = set()
    for path in paths:
        if path not in seen:
            seen.add(path)
            deduplicated.append(path)
    return deduplicated


def _drop_descendant_paths(paths: list[Path]) -> list[Path]:
    kept = []
    for candidate in paths:
        if any(candidate != parent and _is_relative_to(candidate, parent) for parent in paths):
            continue
        kept.append(candidate)
    return kept


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
