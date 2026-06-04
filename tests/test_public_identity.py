from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_LITERALS = [
    "Aki" + "hiko",
    "Kita" + "da",
    "kitada" + "hiko",
    "YOUR_GITHUB" + "_USERNAME",
]


class PublicIdentityTests(unittest.TestCase):
    def test_tracked_text_does_not_contain_private_identity_strings(self):
        text = "\n".join(_read_public_text_files())
        for literal in FORBIDDEN_LITERALS:
            self.assertNotIn(literal, text)
        self.assertIsNone(re.search(r"\bpic" + r"cori\b", text))


def _read_public_text_files():
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix in {".pyc", ".wav", ".mp3", ".mp4", ".xlsx"}:
            continue
        yield path.read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
