import unittest

from src.whisper_colab.colab_runner import (
    ColabTranscriptionConfig,
    _build_generate_kwargs,
    _build_transcript,
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


if __name__ == "__main__":
    unittest.main()
