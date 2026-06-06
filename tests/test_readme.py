import unittest
from pathlib import Path

README_PATH = Path(__file__).resolve().parents[1] / "README.md"


class ReadmeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = README_PATH.read_text(encoding="utf-8")

    def test_readme_does_not_duplicate_notebook_usage(self):
        self.assertNotIn("## Colab usage", self.readme)
        self.assertIn("Usage instructions are included in `Whisper_v3.ipynb`.", self.readme)
        self.assertIn("Runtime > Run all", self.readme)
        self.assertIn("Keep the Colab notebook open", self.readme)

    def test_readme_has_colab_badge_and_clear_headline(self):
        self.assertIn("# Free Whisper Transcription on Google Colab", self.readme)
        self.assertIn("colab-badge.svg", self.readme)
        self.assertIn("Without Per-Minute Limits", self.readme)

    def test_readme_has_no_license_section(self):
        self.assertNotIn("## License", self.readme)


if __name__ == "__main__":
    unittest.main()
