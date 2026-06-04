"""Colab-facing workflow for the Whisper transcription notebook."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .audio import extract_audio_for_whisper


@dataclass(frozen=True)
class ColabTranscriptionConfig:
    """User-facing settings passed from the thin Colab notebook."""

    use_google_drive_files: bool = False
    meeting_file_paths: list[str] = field(default_factory=list)
    model_id: str = "openai/whisper-large-v3-turbo"
    is_japanese_language: bool = True
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
    if config.use_google_drive_files:
        from google.colab import drive

        drive.mount("/content/drive")
        if not config.meeting_file_paths:
            raise ValueError("meeting_file_paths must be set when use_google_drive_files is True.")
        return [Path(path) for path in config.meeting_file_paths]

    uploaded = files_module.upload()
    if not uploaded:
        raise SystemExit("No file was uploaded.")
    return [Path("/content") / name for name in uploaded.keys()]


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
    if config.is_japanese_language and config.translate_into_english:
        return {"language": "japanese", "task": "translate"}
    if config.translate_into_english:
        return {"task": "translate"}
    if config.is_japanese_language:
        return {"language": "japanese", "task": "transcribe"}
    return {"task": "transcribe"}


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
