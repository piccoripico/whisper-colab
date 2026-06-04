import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.whisper_colab.colab_runner import (
    INPUT_MODE_DRIVE_FILE_PATHS,
    INPUT_MODE_DRIVE_FOLDER_PATH,
    INPUT_MODE_UPLOAD,
    ColabTranscriptionConfig,
    _build_generate_kwargs,
    _build_transcript,
    _collect_drive_folder_paths,
    _normalize_input_mode,
    _validate_media_files,
)


class ColabRunnerTests(unittest.TestCase):
    def test_build_generate_kwargs_for_japanese_transcription(self):
        config = ColabTranscriptionConfig(
            is_japanese_language=True,
            translate_into_english=False,
        )

        self.assertEqual(
            _build_generate_kwargs(config),
            {"language": "japanese", "task": "transcribe"},
        )

    def test_build_generate_kwargs_for_translation(self):
        config = ColabTranscriptionConfig(
            is_japanese_language=False,
            translate_into_english=True,
        )

        self.assertEqual(_build_generate_kwargs(config), {"task": "translate"})

    def test_build_transcript_with_timestamps(self):
        transcription = {
            "chunks": [
                {"timestamp": (0.0, 2.0), "text": " Hello "},
                {"timestamp": (65.2, 68.0), "text": "world"},
            ]
        }

        self.assertEqual(
            _build_transcript(transcription, include_timestamps=True),
            "[00:00:00] Hello\n[00:01:05] world\n",
        )

    def test_build_transcript_without_chunks(self):
        self.assertEqual(
            _build_transcript({"text": "plain text"}, include_timestamps=True),
            "plain text\n",
        )

    def test_normalize_input_mode_keeps_explicit_mode(self):
        config = ColabTranscriptionConfig(input_mode=INPUT_MODE_DRIVE_FOLDER_PATH)

        self.assertEqual(_normalize_input_mode(config), INPUT_MODE_DRIVE_FOLDER_PATH)

    def test_normalize_input_mode_preserves_legacy_google_drive_flag(self):
        config = ColabTranscriptionConfig(
            input_mode=INPUT_MODE_UPLOAD,
            use_google_drive_files=True,
        )

        self.assertEqual(_normalize_input_mode(config), INPUT_MODE_DRIVE_FILE_PATHS)

    def test_collect_drive_folder_paths_finds_supported_media(self):
        with TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            (folder / "meeting.mp4").write_bytes(b"video")
            (folder / "audio.MP3").write_bytes(b"audio")
            (folder / "notes.txt").write_text("skip", encoding="utf-8")

            paths = _collect_drive_folder_paths(str(folder), recursive=False)

        self.assertEqual([path.name for path in paths], ["audio.MP3", "meeting.mp4"])

    def test_collect_drive_folder_paths_can_recurse(self):
        with TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            nested = folder / "nested"
            nested.mkdir()
            (nested / "meeting.m4a").write_bytes(b"audio")

            paths = _collect_drive_folder_paths(str(folder), recursive=True)

        self.assertEqual([path.name for path in paths], ["meeting.m4a"])

    def test_validate_media_files_rejects_unsupported_extension(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "notes.txt"
            path.write_text("not media", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Unsupported media extension"):
                _validate_media_files([path])


if __name__ == "__main__":
    unittest.main()
