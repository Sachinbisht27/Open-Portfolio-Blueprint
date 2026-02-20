# Contributing Guide

## Getting Started
1. Fork the repository and clone your fork.
2. Create and activate a virtual environment.
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the project:
```bash
python run.py
```

## Local Dev Commands
- Run tests:
```bash
pytest
```
- Run lint:
```bash
flake8 app tests run.py
```
- Run format check:
```bash
black --check app tests run.py
```

## Contribution Workflow
1. Create a feature branch from `main`.
2. Make focused changes.
3. Add/update tests when behavior changes.
4. Ensure lint + tests pass locally.
5. Open a Pull Request using the PR template.

## Code Style
- Python style is enforced via `black` and `flake8`.
- Keep functions small and testable.
- Prefer configuration-driven behavior over hardcoded values.
- Keep templates language-aware (`t(...)`, `lang_url(...)`).

## Good First Issues
Look for issues labeled:
- `good first issue`
- `help wanted`
- `documentation`

## Pull Request Expectations
- Explain the problem and proposed fix.
- Reference related issue(s).
- Add screenshots for UI changes.
- Mention migration/config updates if applicable.

## Release Notes
Significant user-facing changes should include a `CHANGELOG.md` update.

## Security Reporting
Please avoid posting security vulnerabilities publicly.
Open a private report with:
- Reproduction details
- Affected files/routes
- Suggested mitigation (if available)
