"""Colab-facing workflow for the Whisper transcription notebook."""

from __future__ import annotations

import shutil
import subprocess
import zipfile
from collections.abc import Callable, Iterable
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
REPO_ROOT = Path(__file__).resolve().parents[2]
COLAB_REQUIREMENTS_PATH = REPO_ROOT / "requirements-colab.txt"
COLAB_REQUIREMENTS = [
    "transformers",
    "accelerate",
    "datasets[audio]",
    "pandas",
    "openpyxl",
    "gradio",
]
DEFAULT_AUDIO_OUTPUT_DIR = "/content/whisper_audio"
DEFAULT_OUTPUT_DIR = "/content/whisper_outputs"
DEFAULT_DOWNLOAD_DIR = "/content/whisper_downloads"
DEFAULT_ZIP_FILE_NAME = "whisper_outputs.zip"

MODEL_OPTIONS = [
    "openai/whisper-large-v3-turbo",
    "openai/whisper-large-v3",
]

LANGUAGE_AUTO = "auto"
LANGUAGE_CUSTOM = "custom"
LANGUAGE_OPTIONS = [
    LANGUAGE_AUTO,
    LANGUAGE_CUSTOM,
    "afrikaans",
    "arabic",
    "armenian",
    "azerbaijani",
    "belarusian",
    "bosnian",
    "bulgarian",
    "catalan",
    "chinese",
    "croatian",
    "czech",
    "danish",
    "dutch",
    "english",
    "estonian",
    "finnish",
    "french",
    "galician",
    "german",
    "greek",
    "hebrew",
    "hindi",
    "hungarian",
    "icelandic",
    "indonesian",
    "italian",
    "japanese",
    "kannada",
    "kazakh",
    "korean",
    "latvian",
    "lithuanian",
    "macedonian",
    "malay",
    "marathi",
    "maori",
    "nepali",
    "norwegian",
    "persian",
    "polish",
    "portuguese",
    "romanian",
    "russian",
    "serbian",
    "slovak",
    "slovenian",
    "spanish",
    "swahili",
    "swedish",
    "tagalog",
    "tamil",
    "thai",
    "turkish",
    "ukrainian",
    "urdu",
    "vietnamese",
    "welsh",
]


@dataclass(frozen=True)
class ColabTranscriptionConfig:
    """User-facing settings passed from the thin Colab notebook."""

    input_mode: str = INPUT_MODE_DRIVE_FOLDER_PICKER
    use_google_drive_files: bool = False
    meeting_file_paths: list[str] = field(default_factory=list)
    drive_folder_path: str = "/content/drive/MyDrive/whisper-input"
    drive_recursive: bool = False
    model_id: str = "openai/whisper-large-v3-turbo"
    language: str = LANGUAGE_AUTO
    custom_language: str = ""
    translate_to_english: bool = False
    is_japanese_language: bool = False
    translate_into_english: bool = False
    include_timestamps: bool = True
    export_excel: bool = True
    audio_output_dir: str = DEFAULT_AUDIO_OUTPUT_DIR
    output_dir: str = DEFAULT_OUTPUT_DIR
    export_zip: bool = True
    download_individual_files: bool = False
    zip_file_name: str = DEFAULT_ZIP_FILE_NAME
    max_segment_seconds: int = 0
    install_packages: bool = True
    require_gpu: bool = True
    mount_google_drive: bool = True
    use_custom_output_dir: bool = False
    download_zip_on_completion: bool = True
    pipeline_chunk_length_s: int = 0
    pipeline_batch_size: int = 0
    generate_num_beams: int = 0
    generate_temperature: str = ""
    generate_condition_on_prev_tokens: str = ""
    generate_compression_ratio_threshold: str = ""
    generate_logprob_threshold: str = ""
    generate_no_speech_threshold: str = ""
    model_attn_implementation: str = ""


def run_colab_transcription(config: ColabTranscriptionConfig) -> list[dict[str, Any]]:
    """Run the full Colab transcription workflow."""

    _validate_config(config)
    _require_colab()
    if config.install_packages:
        install_colab_dependencies()

    files_module = _import_colab_files()
    input_paths = _collect_input_paths(config, files_module)
    return _run_transcription_pipeline(
        config=config,
        input_paths=input_paths,
        files_module=files_module,
        download_outputs=True,
    )


def run_transcription_for_paths(
    config: ColabTranscriptionConfig,
    input_paths: Iterable[str | Path],
    *,
    download_outputs: bool = False,
    files_module=None,
    progress_callback: Callable[[str], None] | None = None,
) -> list[dict[str, Any]]:
    """Run transcription for explicit input paths."""

    _validate_config(config)
    if config.install_packages:
        install_colab_dependencies()
    paths = _validate_media_files(Path(path) for path in input_paths)
    return _run_transcription_pipeline(
        config=config,
        input_paths=paths,
        files_module=files_module,
        download_outputs=download_outputs,
        progress_callback=progress_callback,
    )


def _run_transcription_pipeline(
    *,
    config: ColabTranscriptionConfig,
    input_paths: list[Path],
    files_module=None,
    download_outputs: bool,
    progress_callback: Callable[[str], None] | None = None,
) -> list[dict[str, Any]]:
    if not input_paths:
        raise ValueError("At least one input file is required.")

    _report_progress(progress_callback, "Loading Whisper model.")
    pipe = _load_whisper_pipeline(
        config.model_id,
        require_gpu=config.require_gpu,
        model_attn_implementation=config.model_attn_implementation,
        pipeline_chunk_length_s=config.pipeline_chunk_length_s,
        pipeline_batch_size=config.pipeline_batch_size,
    )
    generate_kwargs = _build_generate_kwargs(config)
    max_segment_seconds = _normalize_max_segment_seconds(config.max_segment_seconds)

    results: list[dict[str, Any]] = []
    all_saved_files: list[Path] = []
    used_output_paths: set[Path] = set()
    total_files = len(input_paths)
    for file_index, source_path in enumerate(input_paths, start=1):
        progress_prefix = f"[{file_index}/{total_files}]"
        _report_progress(progress_callback, f"{progress_prefix} Extracting audio: {source_path}")
        audio_path = extract_audio_for_whisper(
            source_path,
            output_dir=config.audio_output_dir,
        )

        _report_progress(progress_callback, f"{progress_prefix} Preparing audio segments.")
        segment_paths = _split_audio_for_transcription(
            audio_path,
            output_dir=config.audio_output_dir,
            max_segment_seconds=max_segment_seconds,
            progress_callback=progress_callback,
        )
        transcription = _transcribe_audio_segments(
            pipe=pipe,
            segment_paths=segment_paths,
            generate_kwargs=generate_kwargs,
            progress_prefix=progress_prefix,
            max_segment_seconds=max_segment_seconds,
            progress_callback=progress_callback,
        )

        output_dir = _output_dir_for_source(config, source_path)
        _report_progress(progress_callback, f"{progress_prefix} Saving outputs to {output_dir}.")
        saved_files = _save_outputs(
            source_path=source_path,
            transcription=transcription,
            include_timestamps=config.include_timestamps,
            export_excel=config.export_excel,
            output_dir=output_dir,
            used_output_paths=used_output_paths,
        )
        all_saved_files.extend(saved_files)
        results.append(
            {
                "source_path": str(source_path),
                "audio_path": audio_path,
                "segment_paths": [str(path) for path in segment_paths],
                "transcription": transcription,
                "saved_files": [str(path) for path in saved_files],
                "output_dir": str(output_dir),
            }
        )
        _report_progress(progress_callback, f"{progress_prefix} Finished: {source_path.name}")

    fallback_output_dir = Path(config.output_dir).expanduser()
    if download_outputs:
        if files_module is None:
            files_module = _import_colab_files()
        _download_outputs(
            output_paths=all_saved_files,
            config=config,
            output_dir=fallback_output_dir,
            files_module=files_module,
        )
    else:
        downloadable_files = _prepare_downloadable_outputs(
            output_paths=all_saved_files,
            config=config,
            output_dir=fallback_output_dir,
            progress_callback=progress_callback,
        )
        for result in results:
            result["downloadable_files"] = [str(path) for path in downloadable_files]

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
    if COLAB_REQUIREMENTS_PATH.exists():
        subprocess.run(
            [
                "python",
                "-m",
                "pip",
                "install",
                "--upgrade",
                "-r",
                str(COLAB_REQUIREMENTS_PATH),
            ],
            check=True,
        )
    else:
        subprocess.run(
            ["python", "-m", "pip", "install", "--upgrade", *COLAB_REQUIREMENTS],
            check=True,
        )
    flag_path.write_text("Upgrades done", encoding="utf-8")


def _validate_config(config: ColabTranscriptionConfig) -> None:
    _normalize_input_mode(config)
    if not str(config.model_id).strip():
        raise ValueError("model_id must not be empty.")
    _normalize_language(config.language, config.custom_language)
    if not str(config.audio_output_dir).strip():
        raise ValueError("audio_output_dir must not be empty.")
    if config.use_custom_output_dir and not str(config.output_dir).strip():
        raise ValueError("output_dir must not be empty.")
    if (config.export_zip or config.download_zip_on_completion) and not str(
        config.zip_file_name
    ).strip():
        raise ValueError("zip_file_name must not be empty when export_zip is enabled.")
    _normalize_max_segment_seconds(config.max_segment_seconds)


def _normalize_max_segment_seconds(value: int) -> int:
    try:
        normalized = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("max_segment_seconds must be 0 or a positive integer.") from exc
    if normalized < 0:
        raise ValueError("max_segment_seconds must be 0 or a positive integer.")
    return normalized


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

    if not config.mount_google_drive:
        raise ValueError("Google Drive input modes require mount_google_drive=True.")
    _mount_drive()

    if input_mode == INPUT_MODE_DRIVE_FILE_PATHS:
        return _collect_manual_drive_file_paths(config.meeting_file_paths)
    if input_mode == INPUT_MODE_DRIVE_FOLDER_PATH:
        return _collect_drive_folder_paths(
            config.drive_folder_path,
            recursive=config.drive_recursive,
        )
    if input_mode == INPUT_MODE_DRIVE_FILE_PICKER:
        return _collect_manual_drive_file_paths(config.meeting_file_paths)
    if input_mode == INPUT_MODE_DRIVE_FOLDER_PICKER:
        return _collect_drive_folder_paths(
            config.drive_folder_path,
            recursive=config.drive_recursive,
        )

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
    folder_paths = [Path(path) for path in _parse_path_lines(folder_path)]
    if not folder_paths:
        raise ValueError("drive_folder_path must contain at least one folder path.")

    media_files: list[Path] = []
    for folder in folder_paths:
        if not folder.exists():
            raise FileNotFoundError(f"Drive folder does not exist: {folder}")
        if not folder.is_dir():
            raise NotADirectoryError(f"Drive folder path is not a directory: {folder}")
        media_files.extend(_find_media_files(folder, recursive=recursive))
    return _deduplicate_paths(media_files)


def _parse_path_lines(value: str) -> list[str]:
    return [line.strip() for line in str(value).splitlines() if line.strip()]


def _deduplicate_paths(paths: Iterable[Path]) -> list[Path]:
    deduplicated = []
    seen = set()
    for path in paths:
        if path not in seen:
            seen.add(path)
            deduplicated.append(path)
    return deduplicated


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


def require_gpu_available() -> None:
    """Fail early when the runtime is not backed by a CUDA GPU."""

    import torch

    _resolve_torch_device(torch, require_gpu=True)


def _load_whisper_pipeline(
    model_id: str,
    *,
    require_gpu: bool = True,
    model_attn_implementation: str = "",
    pipeline_chunk_length_s: int = 0,
    pipeline_batch_size: int = 0,
):
    import torch
    from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

    device, torch_dtype = _resolve_torch_device(torch, require_gpu=require_gpu)
    model_load_kwargs = {
        "low_cpu_mem_usage": True,
        "use_safetensors": True,
    }
    attn_implementation = _normalize_optional_text(model_attn_implementation)
    if attn_implementation is not None:
        model_load_kwargs["attn_implementation"] = attn_implementation

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
    chunk_length_s = _normalize_optional_positive_int(
        pipeline_chunk_length_s,
        field_name="pipeline_chunk_length_s",
    )
    batch_size = _normalize_optional_positive_int(
        pipeline_batch_size,
        field_name="pipeline_batch_size",
    )
    if chunk_length_s is not None:
        pipeline_kwargs["chunk_length_s"] = chunk_length_s
    if batch_size is not None:
        pipeline_kwargs["batch_size"] = batch_size

    try:
        return pipeline(**pipeline_kwargs, dtype=torch_dtype)
    except TypeError:
        return pipeline(**pipeline_kwargs, torch_dtype=torch_dtype)


def _resolve_torch_device(torch_module, *, require_gpu: bool):
    if torch_module.cuda.is_available():
        return "cuda:0", torch_module.float16
    if require_gpu:
        raise RuntimeError(
            "A CUDA GPU is required for this notebook. In Colab, choose "
            "Runtime > Change runtime type > Hardware accelerator > GPU, then rerun."
        )
    return "cpu", torch_module.float32


def _split_audio_for_transcription(
    audio_path: str | Path,
    *,
    output_dir: str | Path,
    max_segment_seconds: int,
    progress_callback: Callable[[str], None] | None = None,
) -> list[Path]:
    audio = Path(audio_path)
    if max_segment_seconds == 0:
        return [audio]

    segment_dir = Path(output_dir).expanduser() / "segments" / audio.stem
    segment_dir.mkdir(parents=True, exist_ok=True)
    for stale_segment in segment_dir.glob("part*.wav"):
        stale_segment.unlink()

    output_pattern = segment_dir / "part%03d.wav"
    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-nostdin",
        "-i",
        str(audio),
        "-f",
        "segment",
        "-segment_time",
        str(max_segment_seconds),
        "-reset_timestamps",
        "1",
        "-c",
        "copy",
        str(output_pattern),
    ]
    _run_segment_command(command)

    segments = sorted(segment_dir.glob("part*.wav"))
    if not segments:
        raise RuntimeError(f"ffmpeg did not create audio segments in {segment_dir}.")
    _report_progress(progress_callback, f"Created {len(segments)} audio segment(s).")
    return segments


def _run_segment_command(command: list[str]) -> None:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("ffmpeg was not found. Install ffmpeg before segmenting audio.") from exc

    if completed.returncode == 0:
        return

    stderr = (completed.stderr or "").strip()
    stdout = (completed.stdout or "").strip()
    detail = stderr or stdout or f"ffmpeg exited with code {completed.returncode}"
    raise RuntimeError(f"ffmpeg failed to segment audio: {detail}")


def _transcribe_audio_segments(
    *,
    pipe,
    segment_paths: list[Path],
    generate_kwargs: dict[str, Any],
    progress_prefix: str,
    max_segment_seconds: int,
    progress_callback: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    transcriptions = []
    total_segments = len(segment_paths)
    for segment_index, segment_path in enumerate(segment_paths, start=1):
        if total_segments == 1:
            _report_progress(progress_callback, f"{progress_prefix} Transcribing: {segment_path}")
        else:
            _report_progress(
                progress_callback,
                f"{progress_prefix} Transcribing segment {segment_index}/{total_segments}: {segment_path}",
            )

        transcription = pipe(
            str(segment_path),
            return_timestamps=True,
            generate_kwargs=generate_kwargs,
        )
        offset_seconds = (segment_index - 1) * max_segment_seconds if total_segments > 1 else 0
        transcriptions.append(_offset_transcription(transcription, offset_seconds))

    return _merge_transcriptions(transcriptions)


def _offset_transcription(transcription: dict[str, Any], offset_seconds: int) -> dict[str, Any]:
    if offset_seconds == 0:
        return transcription

    shifted = dict(transcription)
    shifted_chunks = []
    for chunk in transcription.get("chunks") or []:
        shifted_chunk = dict(chunk)
        timestamp = shifted_chunk.get("timestamp")
        if isinstance(timestamp, (list, tuple)):
            shifted_chunk["timestamp"] = tuple(
                _offset_timestamp_value(value, offset_seconds) for value in timestamp
            )
        shifted_chunks.append(shifted_chunk)
    shifted["chunks"] = shifted_chunks
    return shifted


def _offset_timestamp_value(value: Any, offset_seconds: int) -> Any:
    if value is None:
        return None
    try:
        return float(value) + offset_seconds
    except (TypeError, ValueError):
        return value


def _merge_transcriptions(transcriptions: list[dict[str, Any]]) -> dict[str, Any]:
    if len(transcriptions) == 1:
        return transcriptions[0]

    chunks = []
    texts = []
    for transcription in transcriptions:
        text = str(transcription.get("text", "")).strip()
        if text:
            texts.append(text)
        chunks.extend(transcription.get("chunks") or [])
    return {
        "text": " ".join(texts),
        "chunks": chunks,
    }


def _build_generate_kwargs(config: ColabTranscriptionConfig) -> dict[str, Any]:
    language = _normalize_language(config.language, config.custom_language)
    if language is None and config.is_japanese_language:
        language = "japanese"

    kwargs: dict[str, Any] = {
        "task": "translate" if _should_translate_to_english(config) else "transcribe"
    }
    if language is not None:
        kwargs["language"] = language
    num_beams = _normalize_optional_positive_int(
        config.generate_num_beams,
        field_name="generate_num_beams",
    )
    if num_beams is not None:
        kwargs["num_beams"] = num_beams
    temperature = _normalize_optional_float(
        config.generate_temperature,
        field_name="generate_temperature",
    )
    if temperature is not None:
        kwargs["temperature"] = temperature
    condition_on_prev_tokens = _normalize_optional_bool(config.generate_condition_on_prev_tokens)
    if condition_on_prev_tokens is not None:
        kwargs["condition_on_prev_tokens"] = condition_on_prev_tokens
    compression_ratio_threshold = _normalize_optional_float(
        config.generate_compression_ratio_threshold,
        field_name="generate_compression_ratio_threshold",
    )
    if compression_ratio_threshold is not None:
        kwargs["compression_ratio_threshold"] = compression_ratio_threshold
    logprob_threshold = _normalize_optional_float(
        config.generate_logprob_threshold,
        field_name="generate_logprob_threshold",
    )
    if logprob_threshold is not None:
        kwargs["logprob_threshold"] = logprob_threshold
    no_speech_threshold = _normalize_optional_float(
        config.generate_no_speech_threshold,
        field_name="generate_no_speech_threshold",
    )
    if no_speech_threshold is not None:
        kwargs["no_speech_threshold"] = no_speech_threshold
    return kwargs


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    if not normalized or normalized.lower() in {"default", "auto", "none"}:
        return None
    return normalized


def _normalize_optional_positive_int(value: int | str | None, *, field_name: str) -> int | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        normalized = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be blank or a positive integer.") from exc
    if normalized <= 0:
        return None
    return normalized


def _normalize_optional_float(value: str | float | int | None, *, field_name: str) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be blank or a number.") from exc


def _normalize_optional_bool(value: str | bool | None) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"", "default", "auto", "none"}:
        return None
    if normalized in {"true", "yes", "1", "on"}:
        return True
    if normalized in {"false", "no", "0", "off"}:
        return False
    raise ValueError(f"Optional boolean must be blank, true, or false. Got {value!r}.")


def _normalize_language(language: str | None, custom_language: str = "") -> str | None:
    if language is None:
        return None
    normalized = language.strip().lower()
    if normalized in {"", LANGUAGE_AUTO, "none"}:
        return None
    if normalized == LANGUAGE_CUSTOM:
        custom = custom_language.strip().lower()
        if not custom:
            raise ValueError("custom_language must be set when language is custom.")
        return custom
    return normalized


def _should_translate_to_english(config: ColabTranscriptionConfig) -> bool:
    return config.translate_to_english or config.translate_into_english


def _save_outputs(
    *,
    source_path: Path,
    transcription: dict[str, Any],
    include_timestamps: bool,
    export_excel: bool,
    output_dir: Path,
    used_output_paths: set[Path],
) -> list[Path]:
    saved_files: list[Path] = []

    text_path = _unique_output_path(
        output_dir / f"{source_path.name}.txt",
        used_output_paths,
    )
    text_path.write_text(
        _build_transcript(transcription, include_timestamps=include_timestamps),
        encoding="utf-8",
    )
    saved_files.append(text_path)
    print(f"Saved: {text_path}")

    if export_excel:
        excel_path = _unique_output_path(
            output_dir / f"{source_path.name}.xlsx",
            used_output_paths,
        )
        _write_excel(transcription, excel_path)
        saved_files.append(excel_path)
        print(f"Saved: {excel_path}")

    return saved_files


def _output_dir_for_source(config: ColabTranscriptionConfig, source_path: Path) -> Path:
    if config.use_custom_output_dir:
        output_dir = Path(config.output_dir).expanduser()
    elif config.input_mode == INPUT_MODE_UPLOAD:
        output_dir = Path(DEFAULT_OUTPUT_DIR)
    else:
        output_dir = source_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _unique_output_path(path: Path, used_output_paths: set[Path]) -> Path:
    candidate = path
    counter = 2
    while candidate in used_output_paths:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        counter += 1
    used_output_paths.add(candidate)
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate


def _download_outputs(
    *,
    output_paths: list[Path],
    config: ColabTranscriptionConfig,
    output_dir: Path,
    files_module,
) -> None:
    if not output_paths:
        return

    if config.download_individual_files:
        for output_path in output_paths:
            files_module.download(str(output_path))

    if config.export_zip:
        zip_path = output_dir / config.zip_file_name
        _create_zip_archive(output_paths, zip_path)
        files_module.download(str(zip_path))
        print(f"Downloaded ZIP archive: {zip_path}")


def _prepare_downloadable_outputs(
    *,
    output_paths: list[Path],
    config: ColabTranscriptionConfig,
    output_dir: Path,
    progress_callback: Callable[[str], None] | None = None,
) -> list[Path]:
    if not output_paths:
        return []

    if not config.download_zip_on_completion:
        return []

    zip_path = _download_zip_path(config, output_dir)
    _report_progress(progress_callback, f"Creating ZIP download: {zip_path}")
    return [_create_zip_archive(output_paths, zip_path)]


def _report_progress(callback: Callable[[str], None] | None, message: str) -> None:
    print(message)
    if callback is not None:
        callback(message)


def _download_zip_path(config: ColabTranscriptionConfig, output_dir: Path) -> Path:
    if _is_colab_path(output_dir):
        base_dir = Path(DEFAULT_DOWNLOAD_DIR)
    else:
        base_dir = output_dir.parent / "whisper_downloads"
    return base_dir / config.zip_file_name


def _is_colab_path(path: Path) -> bool:
    return path.as_posix().startswith("/content/")


def _create_zip_archive(output_paths: list[Path], zip_path: Path) -> Path:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for output_path in output_paths:
            archive.write(output_path, arcname=output_path.name)
    return zip_path


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
