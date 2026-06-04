import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.whisper_colab.colab_runner import (
    INPUT_MODE_DRIVE_FILE_PATHS,
    INPUT_MODE_DRIVE_FOLDER_PATH,
    INPUT_MODE_UPLOAD,
    LANGUAGE_AUTO,
    LANGUAGE_OPTIONS,
    MODEL_OPTIONS,
    ColabTranscriptionConfig,
    _build_generate_kwargs,
    _build_transcript,
    _collect_drive_folder_paths,
    _normalize_input_mode,
    _normalize_language,
    _validate_media_files,
)


class ColabRunnerTests(unittest.TestCase):
    def test_model_and_language_options_expose_expected_defaults(self):
        self.assertEqual(MODEL_OPTIONS[0], "openai/whisper-large-v3-turbo")
        self.assertIn("openai/whisper-large-v3", MODEL_OPTIONS)
        self.assertEqual(LANGUAGE_OPTIONS[0], LANGUAGE_AUTO)
        self.assertIn("japanese", LANGUAGE_OPTIONS)
        self.assertIn("english", LANGUAGE_OPTIONS)

    def test_build_generate_kwargs_defaults_to_auto_language_transcription(self):
        config = ColabTranscriptionConfig()

        self.assertEqual(_build_generate_kwargs(config), {"task": "transcribe"})

    def test_build_generate_kwargs_with_source_language(self):
        config = ColabTranscriptionConfig(language="japanese")

        self.assertEqual(
            _build_generate_kwargs(config),
            {"task": "transcribe", "language": "japanese"},
        )

    def test_build_generate_kwargs_for_translation_to_english(self):
        config = ColabTranscriptionConfig(
            language="japanese",
            translate_to_english=True,
        )

        self.assertEqual(
            _build_generate_kwargs(config),
            {"task": "translate", "language": "japanese"},
        )

    def test_build_generate_kwargs_preserves_legacy_japanese_flag(self):
        config = ColabTranscriptionConfig(is_japanese_language=True)

        self.assertEqual(
            _build_generate_kwargs(config),
            {"task": "transcribe", "language": "japanese"},
        )

    def test_normalize_language_treats_auto_as_unspecified(self):
        self.assertIsNone(_normalize_language("auto"))
        self.assertIsNone(_normalize_language(""))
        self.assertEqual(_normalize_language(" English "), "english")

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
