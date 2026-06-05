import json
import unittest
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).resolve().parents[1] / "Whisper_v3.ipynb"


class NotebookStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
        cls.sources = "\n".join(
            "".join(cell.get("source", [])) for cell in cls.notebook.get("cells", [])
        )

    def test_notebook_is_valid_json(self):
        self.assertEqual(self.notebook["nbformat"], 4)
        self.assertIn("cells", self.notebook)

    def test_notebook_has_no_execution_outputs(self):
        for cell in self.notebook["cells"]:
            self.assertIsNone(cell.get("execution_count"))
            self.assertEqual(cell.get("outputs", []), [])

    def test_notebook_has_no_embedded_base64_image(self):
        self.assertNotIn("data:image/png;base64", self.sources)

    def test_notebook_source_is_ascii(self):
        self.sources.encode("ascii")

    def test_notebook_is_thin_github_launcher(self):
        self.assertIn("https://github.com/piccoripico/whisper-colab.git", self.sources)
        self.assertIn("run_colab_transcription(config)", self.sources)
        self.assertIn("launch_colab_ui(config)", self.sources)
        self.assertIn("USE_WIDGET_UI", self.sources)
        self.assertIn("INPUT_MODE", self.sources)
        self.assertIn("MODEL_ID", self.sources)
        self.assertIn('"openai/whisper-large-v3-turbo"', self.sources)
        self.assertIn('"openai/whisper-large-v3"', self.sources)
        self.assertIn('LANGUAGE = "auto"', self.sources)
        self.assertIn('"japanese"', self.sources)
        self.assertIn('"english"', self.sources)
        self.assertIn('"custom"', self.sources)
        self.assertIn("CUSTOM_LANGUAGE", self.sources)
        self.assertIn("TRANSLATE_TO_ENGLISH", self.sources)
        self.assertIn("MAX_SEGMENT_SECONDS", self.sources)
        self.assertIn("OUTPUT_DIR", self.sources)
        self.assertIn("EXPORT_ZIP", self.sources)
        self.assertIn("DOWNLOAD_INDIVIDUAL_FILES", self.sources)
        self.assertIn("ZIP_FILE_NAME", self.sources)
        for input_mode in [
            "upload",
            "drive_file_paths",
            "drive_folder_path",
            "drive_file_picker",
            "drive_folder_picker",
        ]:
            self.assertIn(input_mode, self.sources)
        self.assertNotIn("pipeline(", self.sources)
        self.assertNotIn("extract_audio_for_whisper(", self.sources)
        self.assertNotIn("chunk_length_s", self.sources)
        self.assertNotIn("IS_JAPANESE_LANGUAGE", self.sources)
        self.assertNotIn("TRANSLATE_INTO_ENGLISH", self.sources)
        self.assertNotIn("YOUR_GITHUB" + "_USERNAME", self.sources)

    def test_notebook_keeps_colab_form_comments(self):
        self.assertIn("#@title", self.sources)
        self.assertIn("#@param", self.sources)
        self.assertNotIn("# @param", self.sources)


if __name__ == "__main__":
    unittest.main()
