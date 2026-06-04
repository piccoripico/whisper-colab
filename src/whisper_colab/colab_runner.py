"""Colab-facing workflow for the Whisper transcription notebook."""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .audio import extract_audio_for_whisper

INPUT_MODE_UPLOAD = "upload"
INPUT_MODE_DRIVE_FILE_PATHS = "drive_file_paths"
INPUT_MODE_DRIVE_FOLDER_PATH = "drive_folder_path"
INPUT_MODE_DRIVE_FILE_PICKER = "drive_file_picker"
INPUT_MODE_DRIVE_FOLDER_PICKER = "drive_folder_picker"

INPUT_MODES = {
    INPUT_MODE_UPLOAD,
    INPUT_MODE_DRIVE_FILE_PATHS,
    INPUT_MODE_DRIVE_FOLDER_PATH,
    INPUT_MODE_DRIVE_FILE_PICKER,
    INPUT_MODE_DRIVE_FOLDER_PICKER,
}

SUPPORTED_MEDIA_EXTENSIONS = {
    ".aac",
    ".flac",
    ".m4a",
    ".mov",
    ".mp3",
    ".mp4",
    ".ogg",
    ".wav",
    ".webm",
}
DRIVE_ROOT = Path("/content/drive/MyDrive")

MODEL_OPTIONS = [
    "openai/whisper-large-v3-turbo",
    "openai/whisper-large-v3",
]

LANGUAGE_AUTO = "auto"
LANGUAGE_OPTIONS = [
    LANGUAGE_AUTO,
    "japanese",
    "english",
    "chinese",
    "korean",
    "spanish",
    "french",
    "german",
    "italian",
    "portuguese",
    "russian",
    "arabic",
    "hindi",
    "thai",
    "vietnamese",
    "indonesian",
]


@dataclass(frozen=True)
class ColabTranscriptionConfig:
    """User-facing settings passed from the thin Colab notebook."""

    input_mode: str = INPUT_MODE_UPLOAD
    use_google_drive_files: bool = False
    meeting_file_paths: list[str] = field(default_factory=list)
    drive_folder_path: str = "/content/drive/MyDrive/whisper-input"
    drive_recursive: bool = False
    model_id: str = "openai/whisper-large-v3-turbo"
    language: str = LANGUAGE_AUTO
    translate_to_english: bool = False
    is_japanese_language: bool = False
    translate_into_english: bool = False
    include_timestamps: bool = True
    export_excel: bool = True
    audio_output_dir: str = "/content/whisper_audio"
    install_packages: bool = True


def run_colab_transcription(config: ColabTranscriptionConfig) -> list[dict[str, Any]]:
    """Run the full Colab transcription workflow."""

    _require_colab()
    if config.install_packages:
        install_colab_dependencies()

    files_module = _import_colab_files()
    input_paths = _collect_input_paths(config, files_module)
    pipe = _load_whisper_pipeline(config.model_id)
    generate_kwargs = _build_generate_kwargs(config)

    results: list[dict[str, Any]] = []
    for source_path in input_paths:
        print(f"Extracting audio: {source_path}")
        audio_path = extract_audio_for_whisper(
            source_path,
            output_dir=config.audio_output_dir,
        )

        print(f"Transcribing: {audio_path}")
        transcription = pipe(
            audio_path,
            return_timestamps=True,
            generate_kwargs=generate_kwargs,
        )

        saved_files = _save_and_download_outputs(
            source_path=source_path,
            transcription=transcription,
            include_timestamps=config.include_timestamps,
            export_excel=config.export_excel,
            files_module=files_module,
        )
        results.append(
            {
                "source_path": str(source_path),
                "audio_path": audio_path,
                "transcription": transcription,
                "saved_files": saved_files,
            }
        )
        print(f"Finished: {source_path.name}")

    return results


def install_colab_dependencies() -> None:
    """Install runtime dependencies when needed."""

    if not shutil.which("ffmpeg"):
        subprocess.run(["apt-get", "update", "-qq"], check=True)
        subprocess.run(["apt-get", "install", "-y", "ffmpeg"], check=True)

    flag_path = Path("/content/upgrades_done.flag")
    if flag_path.exists():
        print("Dependency installation already completed in this runtime.")
        return

    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run(
        [
            "python",
            "-m",
            "pip",
            "install",
            "--upgrade",
            "transformers",
            "accelerate",
            "datasets[audio]",
            "pandas",
            "openpyxl",
        ],
        check=True,
    )
    flag_path.write_text("Upgrades done", encoding="utf-8")


def _require_colab() -> None:
    try:
        import google.colab  # noqa: F401
    except ImportError as exc:
        raise RuntimeError("This runner is intended for Google Colab.") from exc


def _import_colab_files():
    from google.colab import files

    return files


def _collect_input_paths(config: ColabTranscriptionConfig, files_module) -> list[Path]:
    input_mode = _normalize_input_mode(config)
    if input_mode == INPUT_MODE_UPLOAD:
        return _collect_uploaded_paths(files_module)

    _mount_drive()

    if input_mode == INPUT_MODE_DRIVE_FILE_PATHS:
        return _collect_manual_drive_file_paths(config.meeting_file_paths)
    if input_mode == INPUT_MODE_DRIVE_FOLDER_PATH:
        return _collect_drive_folder_paths(
            config.drive_folder_path,
            recursive=config.drive_recursive,
        )
    if input_mode == INPUT_MODE_DRIVE_FILE_PICKER:
        return _collect_picker_paths(select_folder=False, recursive=config.drive_recursive)
    if input_mode == INPUT_MODE_DRIVE_FOLDER_PICKER:
        return _collect_picker_paths(select_folder=True, recursive=config.drive_recursive)

    raise ValueError(f"Unsupported input_mode: {config.input_mode!r}")


def _normalize_input_mode(config: ColabTranscriptionConfig) -> str:
    if config.input_mode not in INPUT_MODES:
        raise ValueError(
            f"input_mode must be one of {sorted(INPUT_MODES)}. Got {config.input_mode!r}."
        )
    if config.use_google_drive_files and config.input_mode == INPUT_MODE_UPLOAD:
        return INPUT_MODE_DRIVE_FILE_PATHS
    return config.input_mode


def _collect_uploaded_paths(files_module) -> list[Path]:
    uploaded = files_module.upload()
    if not uploaded:
        raise SystemExit("No file was uploaded.")
    return [Path("/content") / name for name in uploaded.keys()]


def _mount_drive() -> None:
    from google.colab import drive

    drive.mount("/content/drive")


def _collect_manual_drive_file_paths(file_paths: Iterable[str]) -> list[Path]:
    paths = [Path(path) for path in file_paths]
    if not paths:
        raise ValueError("meeting_file_paths must be set when input_mode is drive_file_paths.")
    return _validate_media_files(paths)


def _collect_drive_folder_paths(folder_path: str, *, recursive: bool) -> list[Path]:
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Drive folder does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Drive folder path is not a directory: {folder}")
    return _find_media_files(folder, recursive=recursive)


def _collect_picker_paths(*, select_folder: bool, recursive: bool) -> list[Path]:
    selected_path = _pick_drive_path(select_folder=select_folder)
    if select_folder:
        return _find_media_files(selected_path, recursive=recursive)
    return _validate_media_files([selected_path])


def _find_media_files(folder: Path, *, recursive: bool) -> list[Path]:
    iterator = folder.rglob("*") if recursive else folder.iterdir()
    paths = sorted(
        path
        for path in iterator
        if path.is_file() and path.suffix.lower() in SUPPORTED_MEDIA_EXTENSIONS
    )
    if not paths:
        raise FileNotFoundError(
            f"No supported media files were found in {folder}. "
            f"Supported extensions: {', '.join(sorted(SUPPORTED_MEDIA_EXTENSIONS))}"
        )
    return paths


def _validate_media_files(paths: Iterable[Path]) -> list[Path]:
    valid_paths = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Input file does not exist: {path}")
        if not path.is_file():
            raise ValueError(f"Input path is not a file: {path}")
        if path.suffix.lower() not in SUPPORTED_MEDIA_EXTENSIONS:
            raise ValueError(
                f"Unsupported media extension for {path}. "
                f"Supported extensions: {', '.join(sorted(SUPPORTED_MEDIA_EXTENSIONS))}"
            )
        valid_paths.append(path)
    return valid_paths


def _pick_drive_path(*, select_folder: bool) -> Path:
    try:
        import ipywidgets as widgets
        from IPython.display import clear_output, display
    except ImportError as exc:
        raise RuntimeError("Drive picker mode requires ipywidgets in the Colab runtime.") from exc

    start_path = DRIVE_ROOT if DRIVE_ROOT.exists() else Path("/content/drive")
    state = {"current": start_path, "selected": None}
    output = widgets.Output()
    path_label = widgets.HTML()
    status_label = widgets.HTML()
    items = widgets.Select(rows=14, layout=widgets.Layout(width="100%"))
    open_button = widgets.Button(description="Open")
    parent_button = widgets.Button(description="Parent")
    select_button = widgets.Button(description="Select")

    def refresh() -> None:
        current = state["current"]
        path_label.value = f"<b>Current:</b> {current}"
        entries = ["./"] if select_folder else []
        if current.parent != current:
            entries.append("../")
        children = sorted(current.iterdir(), key=lambda path: (path.is_file(), path.name.lower()))
        for child in children:
            if child.is_dir():
                entries.append(f"{child.name}/")
            elif not select_folder and child.suffix.lower() in SUPPORTED_MEDIA_EXTENSIONS:
                entries.append(child.name)
        items.options = entries
        if entries:
            items.value = entries[0]

    def selected_child() -> Path | None:
        value = items.value
        if not value:
            return None
        if value == "./":
            return state["current"]
        if value == "../":
            return state["current"].parent
        return state["current"] / value.rstrip("/")

    def on_open(_button) -> None:
        child = selected_child()
        if child and child.is_dir():
            state["current"] = child
            refresh()

    def on_parent(_button) -> None:
        if state["current"].parent != state["current"]:
            state["current"] = state["current"].parent
            refresh()

    def on_select(_button) -> None:
        child = selected_child()
        if select_folder:
            selected = child if child and child.is_dir() else state["current"]
        else:
            selected = child
        if selected is None or not selected.exists():
            status_label.value = "<b>No valid path selected.</b>"
            return
        if not select_folder and not selected.is_file():
            status_label.value = "<b>Select a media file.</b>"
            return
        state["selected"] = selected
        status_label.value = f"<b>Selected:</b> {selected}"

    open_button.on_click(on_open)
    parent_button.on_click(on_parent)
    select_button.on_click(on_select)
    refresh()

    with output:
        clear_output()
        display(
            widgets.VBox(
                [
                    path_label,
                    items,
                    widgets.HBox([open_button, parent_button, select_button]),
                    status_label,
                ]
            )
        )
    display(output)

    while state["selected"] is None:
        input("Use the picker above, click Select, then press Enter here to continue.")
    return state["selected"]


def _load_whisper_pipeline(model_id: str):
    import torch
    from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_load_kwargs = {
        "low_cpu_mem_usage": True,
        "use_safetensors": True,
    }

    try:
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id,
            dtype=torch_dtype,
            **model_load_kwargs,
        )
    except TypeError:
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            **model_load_kwargs,
        )

    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    pipeline_kwargs = {
        "task": "automatic-speech-recognition",
        "model": model,
        "tokenizer": processor.tokenizer,
        "feature_extractor": processor.feature_extractor,
        "return_timestamps": True,
        "device": device,
    }

    try:
        return pipeline(**pipeline_kwargs, dtype=torch_dtype)
    except TypeError:
        return pipeline(**pipeline_kwargs, torch_dtype=torch_dtype)


def _build_generate_kwargs(config: ColabTranscriptionConfig) -> dict[str, str]:
    language = _normalize_language(config.language)
    if language is None and config.is_japanese_language:
        language = "japanese"

    kwargs = {"task": "translate" if _should_translate_to_english(config) else "transcribe"}
    if language is not None:
        kwargs["language"] = language
    return kwargs


def _normalize_language(language: str | None) -> str | None:
    if language is None:
        return None
    normalized = language.strip().lower()
    if normalized in {"", LANGUAGE_AUTO, "none"}:
        return None
    return normalized


def _should_translate_to_english(config: ColabTranscriptionConfig) -> bool:
    return config.translate_to_english or config.translate_into_english


def _save_and_download_outputs(
    *,
    source_path: Path,
    transcription: dict[str, Any],
    include_timestamps: bool,
    export_excel: bool,
    files_module,
) -> list[str]:
    saved_files: list[str] = []

    text_path = Path(f"{source_path}.txt")
    text_path.write_text(
        _build_transcript(transcription, include_timestamps=include_timestamps),
        encoding="utf-8",
    )
    files_module.download(str(text_path))
    saved_files.append(str(text_path))
    print(f"Saved: {text_path}")

    if export_excel:
        excel_path = Path(f"{source_path}.xlsx")
        _write_excel(transcription, excel_path)
        files_module.download(str(excel_path))
        saved_files.append(str(excel_path))
        print(f"Saved: {excel_path}")

    return saved_files


def _build_transcript(transcription: dict[str, Any], *, include_timestamps: bool) -> str:
    chunks = transcription.get("chunks") or []
    if not chunks:
        text = transcription.get("text", "")
        return text + ("\n" if text else "")

    lines = []
    for chunk in chunks:
        text = str(chunk.get("text", "")).strip()
        if include_timestamps:
            timestamp = chunk.get("timestamp") or (None, None)
            start_time = timestamp[0] if len(timestamp) >= 1 else None
            lines.append(f"[{_format_timestamp(start_time)}] {text}")
        else:
            lines.append(text)
    return "\n".join(lines) + "\n"


def _format_timestamp(seconds: float | int | None) -> str:
    if seconds is None:
        seconds = 0
    total_seconds = max(0, int(float(seconds)))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def _write_excel(transcription: dict[str, Any], excel_path: Path) -> None:
    import pandas as pd

    chunks = transcription.get("chunks") or []
    if chunks:
        df = pd.DataFrame(chunks)
        if "timestamp" in df.columns:
            timestamps = []
            for value in df["timestamp"]:
                if isinstance(value, (list, tuple)) and len(value) >= 2:
                    timestamps.append((value[0], value[1]))
                else:
                    timestamps.append((None, None))
            df[["start_time", "end_time"]] = pd.DataFrame(timestamps, index=df.index)
            df = df.drop(columns=["timestamp"])
        else:
            df["start_time"] = None
            df["end_time"] = None
        if "text" not in df.columns:
            df["text"] = ""
    else:
        df = pd.DataFrame(
            [
                {
                    "start_time": None,
                    "end_time": None,
                    "text": transcription.get("text", ""),
                }
            ]
        )

    df = df[["start_time", "end_time", "text"]]
    df.to_excel(excel_path, index=False)
