from __future__ import annotations

import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config" / "site_config.json"
TRANSLATIONS_DIR = ROOT_DIR / "config" / "translations"

SUPPORTED_LANGUAGES: dict[str, str] = {
    "en": "English",
    "hi": "हिन्दी",
    "ta": "தமிழ்",
    "te": "తెలుగు",
    "mr": "मराठी",
    "es": "Spanish",
    "ar": "العربية",
    "pt": "Português",
}

RTL_LANGUAGES = {"ar"}


class ContentConfigurationError(RuntimeError):
    """Raised when site configuration files are missing or invalid."""


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ContentConfigurationError(f"Missing configuration file: {path}")
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def load_site_config() -> dict[str, Any]:
    return _load_json(CONFIG_PATH)


@lru_cache(maxsize=1)
def load_translations() -> dict[str, dict[str, Any]]:
    translations: dict[str, dict[str, Any]] = {}
    for language_code in SUPPORTED_LANGUAGES:
        translation_path = TRANSLATIONS_DIR / f"{language_code}.json"
        if translation_path.exists():
            translations[language_code] = _load_json(translation_path)

    if "en" not in translations:
        raise ContentConfigurationError(
            "English translation file is required at config/translations/en.json"
        )

    return translations


def normalize_language(language_code: str | None) -> str:
    if language_code and language_code in SUPPORTED_LANGUAGES:
        return language_code
    return "en"


def _nested_lookup(source: dict[str, Any], dotted_key: str) -> Any:
    current: Any = source
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def translate(key: str, language_code: str, **kwargs: Any) -> str:
    translations = load_translations()
    language_dictionary = translations.get(language_code, translations["en"])
    value = _nested_lookup(language_dictionary, key)

    if value is None:
        value = _nested_lookup(translations["en"], key)

    if value is None:
        return key

    if isinstance(value, str):
        if kwargs:
            try:
                return value.format(**kwargs)
            except KeyError:
                return value
        return value

    return str(value)


def _is_localized_mapping(value: Any) -> bool:
    if not isinstance(value, dict):
        return False

    keys = set(value.keys())
    if not keys:
        return False

    language_keys = set(SUPPORTED_LANGUAGES.keys()) | {"default"}
    return keys.issubset(language_keys) and bool(keys & set(SUPPORTED_LANGUAGES.keys()))


def _resolve_localized_value(value: Any, language_code: str) -> Any:
    if _is_localized_mapping(value):
        return (
            value.get(language_code)
            or value.get("en")
            or value.get("default")
            or next(iter(value.values()))
        )

    if isinstance(value, list):
        return [_resolve_localized_value(item, language_code) for item in value]

    if isinstance(value, dict):
        return {
            key: _resolve_localized_value(nested_value, language_code)
            for key, nested_value in value.items()
        }

    return value


def get_localized_site_config(language_code: str) -> dict[str, Any]:
    config = deepcopy(load_site_config())
    return _resolve_localized_value(config, language_code)
