# Open Portfolio Blueprint (Flask)
A configurable, multilingual developer portfolio template built for open source.

## 30-Second Overview
- **Problem it solves:** Most portfolio templates are hardcoded, single-language, and difficult to reuse.
- **Who it is for:** Developers, students, freelancers, and small teams who need a production-ready portfolio base.
- **Why choose this:** You can fork it, update a single config file, support multiple languages, and ship with built-in quality checks.

## Features
- Config-driven profile, projects, skills, and case-study content via `config/site_config.json`
- Multilingual UI with global language switcher (English, Hindi, Tamil, Telugu, Marathi, Spanish, Arabic, Portuguese)
- Persistent language preference and RTL support for Arabic
- Improved dark mode contrast and readability
- Reusable Flask architecture with centralized content/translation loading
- Open-source contributor workflow (issues, PR template, docs, tests, CI)

## Quick Start
### 1. Clone and install
```bash
git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run locally
```bash
python run.py
```
Open `http://127.0.0.1:5000`.

### 3. Customize your portfolio
Update your details in:
- `config/site_config.json`

At minimum, change:
- `person.full_name`
- `person.email`
- `social_links`
- `experience`
- `featured_projects`

## Configuration Model
- **Primary customization surface:** `config/site_config.json`
- **UI translation dictionaries:** `config/translations/*.json`
- **Optional localized config values:** any text value can be either:
  - a plain string (`"My text"`) or
  - a per-language object (`{"en": "My text", "hi": "मेरा टेक्स्ट"}`)

## Project Structure
```text
app/
  content.py              # Config + i18n loading and localization helpers
  views.py                # Routes and template context injection
  templates/
  static/
config/
  site_config.json
  translations/
docs/
examples/
.github/
tests/
```

## Documentation
- `docs/installation.md`
- `docs/quick-start.md`
- `docs/advanced-usage.md`
- `docs/api-reference.md`
- `docs/architecture.md`
- `docs/faq.md`
- `docs/troubleshooting.md`

## Open Source Model and Licensing
- Current community distribution: **MIT** (`LICENSE`)
- Planned commercial direction: **Open-core**
  - Core template remains open source
  - Premium add-ons (themes, templates, integrations) can be commercial

## Versioning Strategy
This project follows **Semantic Versioning** (`MAJOR.MINOR.PATCH`).

## Quality Gates
- Unit/integration tests: `pytest`
- Lint/format checks: `flake8`, `black --check`
- GitHub Actions CI runs on pushes and PRs

## Community
- Contribution guide: `CONTRIBUTING.md`
- Code of conduct: `CODE_OF_CONDUCT.md`
- Roadmap: `Roadmap.md`
- Changelog: `CHANGELOG.md`
- Issues and PR templates under `.github/`

## Example Usage
- Sample configuration: `examples/site_config.example.json`

## Security
If you discover a security issue, please open a private report first (see `CONTRIBUTING.md`).
