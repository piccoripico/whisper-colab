"""Whisper tokenizer language metadata used by notebooks and README generation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    code: str
    name: str
    native_name: str | None = None

    @property
    def display_name(self) -> str:
        return self.native_name or self.name.title()


TOKENIZER_LANGUAGES: list[Language] = [
    Language("en", "english", "English"),
    Language("zh", "chinese", "Chinese"),
    Language("de", "german", "German"),
    Language("es", "spanish", "Spanish"),
    Language("ru", "russian", "Russian"),
    Language("ko", "korean", "Korean"),
    Language("fr", "french", "French"),
    Language("ja", "japanese", "Japanese"),
    Language("pt", "portuguese", "Portuguese"),
    Language("tr", "turkish", "Turkish"),
    Language("pl", "polish", "Polish"),
    Language("ca", "catalan", "Catalan"),
    Language("nl", "dutch", "Dutch"),
    Language("ar", "arabic", "Arabic"),
    Language("sv", "swedish", "Swedish"),
    Language("it", "italian", "Italian"),
    Language("id", "indonesian", "Indonesian"),
    Language("hi", "hindi", "Hindi"),
    Language("fi", "finnish", "Finnish"),
    Language("vi", "vietnamese", "Vietnamese"),
    Language("he", "hebrew", "Hebrew"),
    Language("uk", "ukrainian", "Ukrainian"),
    Language("el", "greek", "Greek"),
    Language("ms", "malay", "Malay"),
    Language("cs", "czech", "Czech"),
    Language("ro", "romanian", "Romanian"),
    Language("da", "danish", "Danish"),
    Language("hu", "hungarian", "Hungarian"),
    Language("ta", "tamil", "Tamil"),
    Language("no", "norwegian", "Norwegian"),
    Language("th", "thai", "Thai"),
    Language("ur", "urdu", "Urdu"),
    Language("hr", "croatian", "Croatian"),
    Language("bg", "bulgarian", "Bulgarian"),
    Language("lt", "lithuanian", "Lithuanian"),
    Language("la", "latin", "Latin"),
    Language("mi", "maori", "Maori"),
    Language("ml", "malayalam", "Malayalam"),
    Language("cy", "welsh", "Welsh"),
    Language("sk", "slovak", "Slovak"),
    Language("te", "telugu", "Telugu"),
    Language("fa", "persian", "Persian"),
    Language("lv", "latvian", "Latvian"),
    Language("bn", "bengali", "Bengali"),
    Language("sr", "serbian", "Serbian"),
    Language("az", "azerbaijani", "Azerbaijani"),
    Language("sl", "slovenian", "Slovenian"),
    Language("kn", "kannada", "Kannada"),
    Language("et", "estonian", "Estonian"),
    Language("mk", "macedonian", "Macedonian"),
    Language("br", "breton", "Breton"),
    Language("eu", "basque", "Basque"),
    Language("is", "icelandic", "Icelandic"),
    Language("hy", "armenian", "Armenian"),
    Language("ne", "nepali", "Nepali"),
    Language("mn", "mongolian", "Mongolian"),
    Language("bs", "bosnian", "Bosnian"),
    Language("kk", "kazakh", "Kazakh"),
    Language("sq", "albanian", "Albanian"),
    Language("sw", "swahili", "Swahili"),
    Language("gl", "galician", "Galician"),
    Language("mr", "marathi", "Marathi"),
    Language("pa", "punjabi", "Punjabi"),
    Language("si", "sinhala", "Sinhala"),
    Language("km", "khmer", "Khmer"),
    Language("sn", "shona", "Shona"),
    Language("yo", "yoruba", "Yoruba"),
    Language("so", "somali", "Somali"),
    Language("af", "afrikaans", "Afrikaans"),
    Language("oc", "occitan", "Occitan"),
    Language("ka", "georgian", "Georgian"),
    Language("be", "belarusian", "Belarusian"),
    Language("tg", "tajik", "Tajik"),
    Language("sd", "sindhi", "Sindhi"),
    Language("gu", "gujarati", "Gujarati"),
    Language("am", "amharic", "Amharic"),
    Language("yi", "yiddish", "Yiddish"),
    Language("lo", "lao", "Lao"),
    Language("uz", "uzbek", "Uzbek"),
    Language("fo", "faroese", "Faroese"),
    Language("ht", "haitian creole", "Haitian Creole"),
    Language("ps", "pashto", "Pashto"),
    Language("tk", "turkmen", "Turkmen"),
    Language("nn", "nynorsk", "Nynorsk"),
    Language("mt", "maltese", "Maltese"),
    Language("sa", "sanskrit", "Sanskrit"),
    Language("lb", "luxembourgish", "Luxembourgish"),
    Language("my", "myanmar", "Myanmar"),
    Language("bo", "tibetan", "Tibetan"),
    Language("tl", "tagalog", "Tagalog"),
    Language("mg", "malagasy", "Malagasy"),
    Language("as", "assamese", "Assamese"),
    Language("tt", "tatar", "Tatar"),
    Language("haw", "hawaiian", "Hawaiian"),
    Language("ln", "lingala", "Lingala"),
    Language("ha", "hausa", "Hausa"),
    Language("ba", "bashkir", "Bashkir"),
    Language("jw", "javanese", "Javanese"),
    Language("su", "sundanese", "Sundanese"),
    Language("yue", "cantonese", "Cantonese"),
]


SOURCE_LANGUAGE_ORDER: list[Language] = [
    next(language for language in TOKENIZER_LANGUAGES if language.name == "english"),
    next(language for language in TOKENIZER_LANGUAGES if language.name == "japanese"),
    *[
        language
        for language in TOKENIZER_LANGUAGES
        if language.name not in {"english", "japanese"}
    ],
]


UI_LANGUAGE_ORDER: list[Language] = [
    next(language for language in TOKENIZER_LANGUAGES if language.name == "english"),
    next(language for language in TOKENIZER_LANGUAGES if language.name == "japanese"),
    Language("zh-CN", "chinese", "简体中文"),
    Language("zh-TW", "chinese", "繁體中文"),
    *[
        language
        for language in TOKENIZER_LANGUAGES
        if language.name not in {"english", "japanese", "chinese"}
    ],
]


def source_language_values() -> list[str]:
    return ["auto", *(language.name for language in SOURCE_LANGUAGE_ORDER)]


def source_language_param_options() -> str:
    return ", ".join(f'"{language}"' for language in source_language_values())
