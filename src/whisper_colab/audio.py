"""Audio conversion helpers for Whisper transcription."""

from __future__ import annotations

import subprocess
from collections.abc import Sequence
from pathlib import Path

MIN_AUDIO_BYTES = 1_000


class AudioExtractionError(RuntimeError):
    """Raised when ffmpeg cannot create a usable Whisper audio file."""


class AudioStreamNotFoundError(AudioExtractionError):
    """Raised when the input file has no first audio stream."""


def extract_audio_for_whisper(
    src_path: str | Path,
    output_dir: str | Path = "/content/whisper_audio",
    sample_rate: int = 16_000,
    channels: int = 1,
    overwrite: bool = True,
) -> str:
    """Extract the first audio stream as mono PCM WAV for Whisper.

    Args:
        src_path: Source audio or video file.
        output_dir: Directory for the generated ``*.whisper.wav`` file.
        sample_rate: Target sampling rate. Whisper expects 16000 Hz.
        channels: Target channel count. Whisper works well with mono audio.
        overwrite: Recreate the output when it already exists.

    Returns:
        The generated WAV path as a string.
    """

    src = Path(src_path).expanduser()
    if not src.exists():
        raise FileNotFoundError(f"Input file does not exist: {src}")
    if sample_rate <= 0:
        raise ValueError("sample_rate must be a positive integer")
    if channels <= 0:
        raise ValueError("channels must be a positive integer")

    output = _output_path(src, Path(output_dir).expanduser())
    output.parent.mkdir(parents=True, exist_ok=True)

    if output.exists() and not overwrite:
        _validate_output(output)
        return str(output)

    command = _build_ffmpeg_command(
        src=src,
        output=output,
        sample_rate=sample_rate,
        channels=channels,
        overwrite=overwrite,
    )
    _run_ffmpeg(command)
    _validate_output(output)
    return str(output)


def _output_path(src: Path, output_dir: Path) -> Path:
    return output_dir / f"{src.stem}.whisper.wav"


def _build_ffmpeg_command(
    *,
    src: Path,
    output: Path,
    sample_rate: int,
    channels: int,
    overwrite: bool,
) -> list[str]:
    return [
        "ffmpeg",
        "-y" if overwrite else "-n",
        "-hide_banner",
        "-loglevel",
        "error",
        "-nostdin",
        "-i",
        str(src),
        "-map",
        "0:a:0",
        "-vn",
        "-ac",
        str(channels),
        "-ar",
        str(sample_rate),
        "-c:a",
        "pcm_s16le",
        str(output),
    ]


def _run_ffmpeg(command: Sequence[str]) -> None:
    try:
        completed = subprocess.run(
            list(command),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise AudioExtractionError(
            "ffmpeg was not found. Install ffmpeg before extracting audio."
        ) from exc

    if completed.returncode == 0:
        return

    stderr = (completed.stderr or "").strip()
    stdout = (completed.stdout or "").strip()
    detail = stderr or stdout or f"ffmpeg exited with code {completed.returncode}"
    if _looks_like_missing_audio_stream(detail):
        raise AudioStreamNotFoundError(f"No audio stream was found: {detail}")
    raise AudioExtractionError(f"ffmpeg failed to extract audio: {detail}")


def _looks_like_missing_audio_stream(message: str) -> bool:
    lowered = message.lower()
    return (
        "matches no streams" in lowered
        or "stream map" in lowered
        and "no streams" in lowered
        or "audio:0" in lowered
        and "not found" in lowered
    )


def _validate_output(output: Path) -> None:
    if not output.exists():
        raise AudioExtractionError(f"ffmpeg did not create an output file: {output}")
    if output.stat().st_size < MIN_AUDIO_BYTES:
        raise AudioExtractionError(
            f"Extracted audio is too small to be usable: {output} ({output.stat().st_size} bytes)"
        )
