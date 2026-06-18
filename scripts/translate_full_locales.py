"""Machine-translate locale files from the English source locale.

This maintenance helper follows the same model as vibevoice-asr-colab: preserve
code tokens and notebook form markers, then translate user-facing prose.
Review generated translations before a formal release.
"""

from __future__ import annotations

import json
import re
import time
from html import unescape
import sys
from collections.abc import Iterable
from pathlib import Path

import requests
from deep_translator import GoogleTranslator, MyMemoryTranslator

from languages import UI_LANGUAGE_ORDER


ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "locales"

GOOGLE_TARGET_OVERRIDES = {
    "chinese": "zh-CN",
    "hebrew": "iw",
    "haitian creole": "ht",
    "javanese": "jw",
    "myanmar": "my",
    "nynorsk": "no",
    "cantonese": "zh-TW",
    "tagalog": "tl",
}

CODE_TARGET_OVERRIDES = {
    "zh-CN": ("google", "zh-CN"),
    "zh-TW": ("google", "zh-TW"),
}

DIRECT_GOOGLE_TARGETS = {
    "bashkir": "ba",
    "breton": "br",
    "faroese": "fo",
    "occitan": "oc",
    "tibetan": "bo",
}

MYMEMORY_TARGETS = {}

SKIP_TRANSLATION_KEYS = {
    "intro_markdown",
    "settings.source_language_default",
}

PROTECT_PATTERNS = [
    re.compile(r"\[[^\]]+\]\([^)]+\)"),
    re.compile(r"`[^`]+`"),
    re.compile(r"https?://\S+"),
    re.compile(r'"[^"]+"'),
    re.compile(r"\bGoogle Colab\b"),
    re.compile(r"\bGoogle Drive\b"),
    re.compile(r"\bHugging Face\b"),
    re.compile(r"\bTransformers\b"),
    re.compile(r"\bOpenAI\b"),
    re.compile(r"\bWhisper\b"),
    re.compile(r"\blarge-v3-turbo\b"),
    re.compile(r"\blarge-v3\b"),
    re.compile(r"\bCUDA\b"),
    re.compile(r"\bGPU\b"),
    re.compile(r"\bJSON\b"),
    re.compile(r"\bTXT\b"),
    re.compile(r"\bMD\b"),
    re.compile(r"\bCSV\b"),
    re.compile(r"\bExcel\b"),
    re.compile(r"\bSRT\b"),
    re.compile(r"\bZIP\b"),
    re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b"),
    re.compile(r"\b[a-z]+_[a-z0-9_]+\b"),
]
PROTECT_RE = re.compile("|".join(f"(?:{pattern.pattern})" for pattern in PROTECT_PATTERNS))

COMMENT_PREFIX_PATTERNS = [
    re.compile(r"^(# @title \d+\. )(.*)$", re.S),
    re.compile(r"^(# \d+\. )(.*)$", re.S),
    re.compile(r"^(# @markdown #{2,3} )(.*)$", re.S),
    re.compile(r"^(# @markdown - )(.*)$", re.S),
    re.compile(r"^(# @markdown )(.*)$", re.S),
    re.compile(r"^(# ## )(.*)$", re.S),
    re.compile(r"^(# - )(.*)$", re.S),
    re.compile(r"^(# )(.*)$", re.S),
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def language_targets() -> dict[str, tuple[str, str]]:
    supported = GoogleTranslator().get_supported_languages(as_dict=True)
    targets: dict[str, tuple[str, str]] = {}
    for language in UI_LANGUAGE_ORDER:
        if language.name == "english":
            continue
        if language.code in CODE_TARGET_OVERRIDES:
            targets[language.code] = CODE_TARGET_OVERRIDES[language.code]
            continue
        if language.name in DIRECT_GOOGLE_TARGETS:
            targets[language.code] = ("direct_google", DIRECT_GOOGLE_TARGETS[language.name])
            continue
        if language.name in MYMEMORY_TARGETS:
            targets[language.code] = ("mymemory", MYMEMORY_TARGETS[language.name])
            continue
        target = (
            GOOGLE_TARGET_OVERRIDES.get(language.name)
            or supported.get(language.name)
        )
        if not target:
            raise KeyError(f"No translation target for {language.code}: {language.name}")
        targets[language.code] = ("google", target)
    return targets


def protect(text: str) -> tuple[str, dict[str, str]]:
    tokens: dict[str, str] = {}

    def add_token(match: re.Match[str]) -> str:
        token = f"@@P{len(tokens):04d}@@"
        tokens[token] = match.group(0)
        return token

    return PROTECT_RE.sub(add_token, text), tokens


def restore(text: str, tokens: dict[str, str]) -> str:
    restored = text
    for token, value in tokens.items():
        index = int(token.removeprefix("@@P").removesuffix("@@"))
        restored = fuzzy_token_pattern(index).sub(value, restored)
        restored = restored.replace(token, value)
    return unescape(restored)


def fuzzy_token_pattern(index: int) -> re.Pattern[str]:
    digits = f"{index:04d}"
    loose_digits = r"\s*".join(digits)
    return re.compile(rf"@+\s*(?:@+\s*)*P\s*{loose_digits}\s*(?:@\s*)+P?", re.I)


def split_comment_prefix(text: str) -> tuple[str, str]:
    for pattern in COMMENT_PREFIX_PATTERNS:
        match = pattern.match(text)
        if match:
            return match.group(1), match.group(2)
    return "", text


class Translator:
    def __init__(self, provider: str, target: str) -> None:
        self.provider = provider
        self.target = target
        if provider == "google":
            self.translator = GoogleTranslator(source="en", target=target)
        elif provider == "mymemory":
            self.translator = MyMemoryTranslator(source="en-US", target=target)
        elif provider == "direct_google":
            self.translator = None
        else:
            raise ValueError(provider)

    def translate(self, text: str) -> str:
        if self.provider == "mymemory" and len(text) > 480:
            return self.translate_long_mymemory(text)
        if self.provider == "direct_google":
            return self.translate_direct_google(text)
        for attempt in range(4):
            try:
                return self.translator.translate(text)
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(2 * (attempt + 1))
        raise RuntimeError("unreachable")

    def translate_direct_google(self, text: str) -> str:
        for attempt in range(4):
            try:
                response = requests.get(
                    "https://translate.googleapis.com/translate_a/single",
                    params={
                        "client": "gtx",
                        "sl": "en",
                        "tl": self.target,
                        "dt": "t",
                        "q": text,
                    },
                    timeout=30,
                )
                response.raise_for_status()
                payload = response.json()
                return "".join(part[0] for part in payload[0] if part and part[0])
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(2 * (attempt + 1))
        raise RuntimeError("unreachable")

    def translate_long_mymemory(self, text: str) -> str:
        translated_lines: list[str] = []
        for line in text.splitlines():
            if not line.strip():
                translated_lines.append(line)
                continue
            translated_lines.append(" ".join(self.translate_piece(piece) for piece in split_text(line)))
        return "\n".join(translated_lines)

    def translate_piece(self, text: str) -> str:
        if len(text) <= 480:
            return self.translate(text)
        midpoint = len(text) // 2
        split_at = max(text.rfind(" ", 0, midpoint), text.rfind(".", 0, midpoint))
        if split_at <= 0:
            split_at = midpoint
        return self.translate_piece(text[:split_at].strip()) + " " + self.translate_piece(
            text[split_at:].strip()
        )


def split_text(text: str) -> list[str]:
    pieces: list[str] = []
    current = ""
    for part in re.split(r"(?<=[.!?。！？])\s+", text):
        if not part:
            continue
        if current and len(current) + len(part) + 1 > 450:
            pieces.append(current)
            current = part
        else:
            current = f"{current} {part}".strip()
    if current:
        pieces.append(current)
    return pieces or [text]


def translate_block(translator: Translator, items: list[str]) -> list[str]:
    if translator.provider == "mymemory":
        return [translator.translate(item) for item in items]

    block = "\n".join(f"@@ITEM{i:03d}@@\n{item}" for i, item in enumerate(items))
    translated = translator.translate(block)
    matches = list(re.finditer(r"@@ITEM(\d{3})@@\s*(.*?)(?=\n?@@ITEM\d{3}@@|$)", translated, re.S))
    if len(matches) != len(items):
        return [translator.translate(item) for item in items]
    result: list[str] = [""] * len(items)
    for match in matches:
        result[int(match.group(1))] = match.group(2).strip()
    return result


def chunk_items(items: list[tuple[str, str, str, dict[str, str]]], limit: int = 3000):
    chunk: list[tuple[str, str, str, dict[str, str]]] = []
    size = 0
    for item in items:
        item_size = len(item[2]) + 20
        if chunk and size + item_size > limit:
            yield chunk
            chunk = []
            size = 0
        chunk.append(item)
        size += item_size
    if chunk:
        yield chunk


def prepare_string(key: str, value: str) -> tuple[str, str, str, dict[str, str]]:
    if key in SKIP_TRANSLATION_KEYS:
        return key, "", value, {}
    prefix, body = split_comment_prefix(value)
    protected, tokens = protect(body)
    return key, prefix, protected, tokens


def translate_string_map(values: dict[str, str], translator: Translator) -> dict[str, str]:
    output: dict[str, str] = {}
    passthrough: dict[str, str] = {}
    prepared: list[tuple[str, str, str, dict[str, str]]] = []
    for key, value in values.items():
        if key in SKIP_TRANSLATION_KEYS:
            passthrough[key] = value
        else:
            prepared.append(prepare_string(key, value))

    for chunk in chunk_items(prepared):
        translated_texts = translate_block(translator, [item[2] for item in chunk])
        for (key, prefix, _protected, tokens), translated_text in zip(chunk, translated_texts):
            output[key] = normalize_translated_value(
                key,
                prefix + restore(translated_text, tokens),
            )
        time.sleep(0.2)

    output.update(passthrough)
    return output


def normalize_translated_value(key: str, value: str) -> str:
    if key == "intro_markdown":
        return value
    return re.sub(r"\s*\n\s*", " ", value).strip()


def flatten_readme(readme: dict) -> dict[str, str]:
    flat: dict[str, str] = {}
    for key, value in readme.items():
        if isinstance(value, str):
            flat[key] = value
        elif isinstance(value, list):
            for index, item in enumerate(value):
                flat[f"{key}.{index}"] = str(item)
    return flat


def unflatten_readme(flat: dict[str, str], original: dict) -> dict:
    output: dict = {}
    for key, value in original.items():
        if isinstance(value, str):
            output[key] = flat[key]
        elif isinstance(value, list):
            output[key] = [flat[f"{key}.{index}"] for index, _item in enumerate(value)]
    return output


def clean_markdown(text: str) -> str:
    return re.sub(r"\*\*\s*(.*?)\s*\*\*", r"**\1**", text)


def render_intro_markdown(notebook: dict) -> str:
    labels = notebook.get("feature_labels")
    bodies = notebook.get("feature_bodies")
    if labels and bodies:
        features = "\n".join(
            f"- **{clean_markdown(label.strip())}:** {clean_markdown(body.strip())}"
            for label, body in zip(labels, bodies)
        )
    else:
        features = "\n".join(f"- {clean_markdown(item)}" for item in notebook.get("features", []))
    steps = "\n".join(
        f"{index}. {clean_markdown(item)}"
        for index, item in enumerate(notebook.get("how_to_use_steps", []), start=1)
    )
    notes = "\n".join(f"- {clean_markdown(item)}" for item in notebook.get("notes", []))
    return "\n\n".join(
        [
            f"# {notebook['title']}",
            notebook["description"],
            f"## {notebook['features_heading']}\n\n{features}",
            f"## {notebook['how_to_use_heading']}\n\n{steps}",
            f"## {notebook['notes_heading']}\n\n{notes}",
        ]
    )


def translate_locale(code: str, provider: str, target: str, base: dict, existing: dict) -> dict:
    translator = Translator(provider, target)
    translated = dict(existing)
    translated["placeholders"] = translate_string_map(base["placeholders"], translator)
    if "settings.source_language_default" in existing.get("placeholders", {}):
        translated["placeholders"]["settings.source_language_default"] = existing["placeholders"][
            "settings.source_language_default"
        ]
    translated["labels"] = translate_string_map(base["labels"], translator)
    readme_flat = translate_string_map(flatten_readme(base["readme"]), translator)
    translated["readme"] = unflatten_readme(readme_flat, base["readme"])
    notebook_flat = translate_string_map(flatten_readme(base["notebook"]), translator)
    translated["notebook"] = unflatten_readme(notebook_flat, base["notebook"])
    translated["placeholders"]["intro_markdown"] = render_intro_markdown(translated["notebook"])
    translated["translation_source"] = f"{provider}:{target}; machine-translated from en"
    return translated


def main(codes: Iterable[str] | None = None) -> None:
    base = load_json(LOCALES_DIR / "en.json")
    targets = language_targets()
    selected = set(codes or targets)
    for code in UI_LANGUAGE_ORDER:
        if code.code == "en" or code.code not in selected:
            continue
        provider, target = targets[code.code]
        path = LOCALES_DIR / f"{code.code}.json"
        existing = load_json(path)
        print(f"Translating {code.code} ({code.name}) via {provider}:{target} ...", flush=True)
        write_json(path, translate_locale(code.code, provider, target, base, existing))


if __name__ == "__main__":
    main(sys.argv[1:] or None)
