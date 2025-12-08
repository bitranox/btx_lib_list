# Changelog

All notable changes to this project will be documented in this file following
the [Keep a Changelog](https://keepachangelog.com/) format.

## [1.0.2] - 2025-12-08

### Changed
- Refactored test suite to clean architecture principles with improved clarity and real behavior testing.
- Organized tests into focused classes where each test verifies exactly one behavior.
- Added OS-specific markers (`os_agnostic`, `os_windows`, `os_macos`, `os_posix`, `os_linux`) for environment-aware test execution.
- Centralized shared fixtures in `conftest.py` for better discoverability and reduced duplication.
- Replaced stub-heavy tests with real behavior tests in `test_module_entry.py`.
- Simplified `test_metadata.py` to use direct imports instead of file parsing.

## [1.0.1] - 2025-10-15

- enhance Readme examples

## [1.0.0] - 2025-10-15

### Added
- - Scaffolded the `btx_lib_list` Python package with CLI entry points (`btx_lib_list`, `btx-lib-list`, and `python -m btx_lib_list`) and rich-click powered help output.
- Shipped the greeting and failure behaviour helpers (`emit_greeting`, `raise_intentional_failure`, `print_info`) with unit-tested coverage.
- Provisioned the automation suite under `scripts/` supporting build, release, version bumping, and metadata inspection tasks.
- Established the pytest-based test suite for behaviours, CLI commands, scripts, and module metadata.
- Authored the initial documentation set including README, INSTALL, architecture concept overview, and the system design module reference.
- Introduced the `btx_lib_list.lib_list` module with a full suite of list-processing helpers (deduplication, pattern filters, string stripping, chunking) and exported them from the package root.
- Added `tests/test_lib_list.py` covering the new helpers across positive, negative, and edge-path behaviours.

### Changed
- Updated the README and module reference to document the list utilities and their CLI usage examples.
- Trimmed and reorganised `AGENTS.md` to reflect the narrower pre-release scope for contributors.
