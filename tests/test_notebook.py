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
        self.assertNotIn("pipeline(", self.sources)
        self.assertNotIn("extract_audio_for_whisper(", self.sources)
        self.assertNotIn("chunk_length_s", self.sources)
        self.assertNotIn("YOUR_GITHUB" + "_USERNAME", self.sources)

    def test_notebook_keeps_colab_form_comments(self):
        self.assertIn("#@title", self.sources)
        self.assertIn("#@param", self.sources)
        self.assertNotIn("# @param", self.sources)


if __name__ == "__main__":
    unittest.main()
