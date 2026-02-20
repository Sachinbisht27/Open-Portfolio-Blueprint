from app.content import get_localized_site_config, normalize_language, translate


def test_normalize_language_returns_default_for_invalid_value() -> None:
    assert normalize_language("unknown") == "en"


def test_localized_site_config_resolves_language_fallback() -> None:
    hindi_site = get_localized_site_config("hi")
    assert hindi_site["hero"]["roles"][0] == "फुल स्टैक डेवलपर"


def test_translation_fallbacks_to_key_when_missing() -> None:
    assert translate("does.not.exist", "en") == "does.not.exist"


def test_translation_returns_localized_value() -> None:
    assert translate("home.projects.filters.all", "es") == "Todos los proyectos"
