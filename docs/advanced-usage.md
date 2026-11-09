# Advanced Usage

## Localized Config Values
Any config text can be either:
```json
"title": "Plain text"
```
or:
```json
"title": {
  "en": "English text",
  "hi": "हिंदी टेक्स्ट"
}
```

## Add a New Language
1. Add language code/name in `app/content.py` (`SUPPORTED_LANGUAGES`).
2. Add `config/translations/<code>.json`.
3. Add localized text values in config where needed.
4. Test route rendering with `?lang=<code>`.

## Replace Contact Form Provider
Current form posts to FormSubmit (`site_config.json`).
You can switch to your own backend by changing form `action` and payload handling.

## Theme Extension
- Update CSS tokens in `:root` and `[data-theme="dark"]`
- Keep contrast-safe values for `--ink`, `--muted`, and `--surface`
