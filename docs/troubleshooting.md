# Troubleshooting

## App does not start
- Ensure virtualenv is active.
- Reinstall dependencies:
```bash
pip install -r requirements.txt
```

## Language switcher not changing content
- Check URL has `?lang=<code>`.
- Verify translation file exists in `config/translations/`.
- Ensure language code exists in `SUPPORTED_LANGUAGES`.

## Dark mode looks incorrect
- Confirm browser cache is cleared.
- Verify `data-theme` toggles between `light` and `dark` in devtools.
- Check CSS variables in `:root` and `[data-theme="dark"]`.

## Contact form does not redirect after submit
- Update `site.contact.form.action` and provider-specific fields.
- Confirm `_next` URL is valid and public in production.

## CI fails on lint/tests
Run locally:
```bash
pytest
flake8 app tests run.py
black --check app tests run.py
```
