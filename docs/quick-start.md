# Quick Start

## 1. Update Personal Data
Edit `config/site_config.json`:
- Name and initials
- Email and social links
- Experience, skills, and projects

## 2. Optional Translation Customization
Edit files in `config/translations/` to adjust labels/headings per language.

## 3. Launch
```bash
python run.py
```

## 4. Run checks
```bash
pytest
flake8 app tests run.py
black --check app tests run.py
```
