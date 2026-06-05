import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_LITERALS = [
    "".join(chr(code) for code in [65, 107, 105, 104, 105, 107, 111]),
    "".join(chr(code) for code in [75, 105, 116, 97, 100, 97]),
    "".join(chr(code) for code in [107, 105, 116, 97, 100, 97, 104, 105, 107, 111]),
    "YOUR_GITHUB" + "_USERNAME",
]


class PublicIdentityTests(unittest.TestCase):
    def test_tracked_text_does_not_contain_private_identity_strings(self):
        text = "\n".join(_read_public_text_files())
        for literal in FORBIDDEN_LITERALS:
            self.assertNotIn(literal, text)
        self.assertIsNone(re.search(r"\bpic" + r"cori\b", text))

    def test_tracked_text_does_not_contain_removed_widget_ui_terms(self):
        text = "\n".join(_read_tracked_text_files())
        for literal in ["ipy" + "widgets", "launch_colab" + "_ui"]:
            self.assertNotIn(literal, text)


def _read_public_text_files():
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or ".ruff_cache" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix in {".pyc", ".wav", ".mp3", ".mp4", ".xlsx"}:
            continue
        yield path.read_text(encoding="utf-8")


def _read_tracked_text_files():
    completed = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    for relative_path in completed.stdout.splitlines():
        path = REPO_ROOT / relative_path
        if not path.exists():
            continue
        if path.suffix in {".pyc", ".wav", ".mp3", ".mp4", ".xlsx"}:
            continue
        yield path.read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
