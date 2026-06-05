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
        self.assertIn(
            "click the play button on the `Launch Whisper Colab App` cell",
            self.readme,
        )
        self.assertIn("temporary Gradio URL", self.readme)
        self.assertIn("/content/drive/MyDrive", self.readme)

    def test_readme_has_no_license_section(self):
        self.assertNotIn("## License", self.readme)


if __name__ == "__main__":
    unittest.main()
