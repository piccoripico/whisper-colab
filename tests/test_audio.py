import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from whisper_colab.audio import (  # noqa: E402
    AudioExtractionError,
    AudioStreamNotFoundError,
    extract_audio_for_whisper,
)


class ExtractAudioForWhisperTests(unittest.TestCase):
    def test_builds_expected_ffmpeg_command(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source = temp_path / "meeting.mp4"
            source.write_bytes(b"fake mp4")
            output_dir = temp_path / "audio"

            def fake_run(command, **_kwargs):
                Path(command[-1]).write_bytes(b"0" * 2048)
                return subprocess.CompletedProcess(command, 0, "", "")

            with patch("whisper_colab.audio.subprocess.run", side_effect=fake_run) as run:
                result = extract_audio_for_whisper(source, output_dir=output_dir)

            expected_output = output_dir / "meeting.whisper.wav"
            self.assertEqual(result, str(expected_output))
            self.assertEqual(
                run.call_args.args[0],
                [
                    "ffmpeg",
                    "-y",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-nostdin",
                    "-i",
                    str(source),
                    "-map",
                    "0:a:0",
                    "-vn",
                    "-ac",
                    "1",
                    "-ar",
                    "16000",
                    "-c:a",
                    "pcm_s16le",
                    str(expected_output),
                ],
            )

    def test_ffmpeg_failure_includes_stderr(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "broken.mp4"
            source.write_bytes(b"fake mp4")

            with patch(
                "whisper_colab.audio.subprocess.run",
                return_value=subprocess.CompletedProcess(["ffmpeg"], 1, "", "invalid codec data"),
            ):
                with self.assertRaisesRegex(AudioExtractionError, "invalid codec data"):
                    extract_audio_for_whisper(source, output_dir=Path(temp_dir) / "audio")

    def test_missing_audio_stream_has_specific_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "video_only.mp4"
            source.write_bytes(b"fake mp4")

            with patch(
                "whisper_colab.audio.subprocess.run",
                return_value=subprocess.CompletedProcess(
                    ["ffmpeg"],
                    1,
                    "",
                    "Stream map '0:a:0' matches no streams.",
                ),
            ):
                with self.assertRaises(AudioStreamNotFoundError):
                    extract_audio_for_whisper(source, output_dir=Path(temp_dir) / "audio")

    def test_missing_output_file_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "meeting.mp4"
            source.write_bytes(b"fake mp4")

            with patch(
                "whisper_colab.audio.subprocess.run",
                return_value=subprocess.CompletedProcess(["ffmpeg"], 0, "", ""),
            ):
                with self.assertRaisesRegex(AudioExtractionError, "did not create"):
                    extract_audio_for_whisper(source, output_dir=Path(temp_dir) / "audio")


if __name__ == "__main__":
    unittest.main()
