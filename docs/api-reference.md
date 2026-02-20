# API Reference

## Routes
- `GET /` Home
- `GET /projects` Projects
- `GET /projects/case-study` Case study
- `GET /contact` Contact
- `GET /resume` Resume

All routes accept `?lang=<code>`.

## Core Template Helpers
Injected globally from `app/views.py`:
- `t(key, **kwargs)` -> translation lookup with English fallback
- `lang_url(endpoint, **values)` -> URL with current language retained
- `site` -> localized config object loaded from `config/site_config.json`
- `supported_languages` -> dropdown source

## Content Module (`app/content.py`)
- `load_site_config()`
- `load_translations()`
- `normalize_language(language_code)`
- `translate(key, language_code, **kwargs)`
- `get_localized_site_config(language_code)`
