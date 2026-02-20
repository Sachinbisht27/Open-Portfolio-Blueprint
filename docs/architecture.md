# Architecture Overview

## High-Level Design
- **Presentation layer:** Flask + Jinja templates (`app/templates`)
- **Content layer:** Config + translations (`config/`)
- **Behavior layer:** Frontend interactions and theming (`app/static`)

## Modular Structure
- `app/content.py`: isolated content loading/localization logic
- `app/views.py`: routing + context wiring
- `tests/`: unit + integration tests

## Data Flow
1. Request arrives with optional `lang` query param.
2. Language normalized and stored in request context.
3. Config is localized with fallback to English.
4. Templates render using `site` + `t(...)`.

## Testability
- Content logic tested separately (`tests/test_content.py`)
- Route rendering tested via Flask test client (`tests/test_routes.py`)
