import importlib.util
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = REPO_ROOT / "scripts" / "build_notebook.py"
NOTEBOOK_PATH = REPO_ROOT / "Whisper_v3.ipynb"


class BuildNotebookTests(unittest.TestCase):
    def test_generated_notebook_matches_committed_file(self):
        module = _load_build_notebook_module()
        expected = module.serialize_notebook(module.build_notebook())
        actual = NOTEBOOK_PATH.read_text(encoding="utf-8")

        self.assertEqual(actual, expected)


def _load_build_notebook_module():
    spec = importlib.util.spec_from_file_location("build_notebook", BUILD_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    unittest.main()
