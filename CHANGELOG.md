# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning.

## [Unreleased]
### Added
- Config-driven portfolio data model via `config/site_config.json`
- Multilingual support with eight languages and global language switcher
- RTL support for Arabic
- Open-source governance files (`CONTRIBUTING`, `CODE_OF_CONDUCT`, `Roadmap`, docs set)
- Example config and test suite scaffold
- CI workflow for linting and tests

### Changed
- Reworked Flask context layer for localization and shared template helpers
- Refactored templates to consume config + translation keys
- Improved dark-mode contrast and readability across cards, forms, navigation, and page background

### Fixed
- Theme consistency issues caused by hardcoded light-only colors in dark mode

## [0.1.0] - 2026-02-20
### Added
- Initial open-source baseline release
