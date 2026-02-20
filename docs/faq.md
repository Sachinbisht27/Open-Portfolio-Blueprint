# FAQ

## Do I need to edit templates to use this project?
No. Most customization is done through `config/site_config.json`.

## How do I change text in specific languages?
Update `config/translations/<language>.json` and/or use localized values in `site_config.json`.

## Why is some content still in English?
If a value in config is a plain string, it is shared across languages. Use language objects for fully localized custom text.

## Does Arabic support RTL layout?
Yes. Arabic automatically sets `dir="rtl"` on the document.

## Can I use this for commercial work?
Yes, under the current MIT license. Planned long-term model is open-core for premium extensions.
