# Changelog

All notable changes to this project will be documented in this file following
the [Keep a Changelog](https://keepachangelog.com/) format.

## [Unreleased]

## [1.0.5] 2026-07-24 16:18:31

### Fixed
- Latest ruff (0.16.0, floating dev pin) newly defaults to ~920 rules on a repo with no explicit `[tool.ruff.lint].select`; pinned the curated bitranox rule set instead so CI stopped reddening on unrelated rule families.
- `T201` (print): swapped `print()` for `sys.stdout.write()` in `__init__conf__.print_info`.
- `PLR2004` (magic value): named the quote-stripping length threshold in `lib_list.ls_strip_afz`.
- `UP035` (deprecated import): replaced `typing.ContextManager` with `contextlib.AbstractContextManager` in `__main__.py`.
- `RUF002` (ambiguous en dash): replaced en dashes with ASCII hyphens in module docstrings.
- `ERA001` false positives on two test section-header comments that happened to parse as valid Python; reworded them.
- `PERF401`: replaced a manual test loop with a list comprehension in `test_lib_list.py`.

### Changed
- Added `[tool.ruff.lint].select` (the bitranox curated rule set) plus `pydocstyle` google convention and per-file-ignores for `tests/*.py` and `src/btx_lib_list/cli.py` (Click's boolean option flags).
- Ran the mechanical import-sort/dunder-all-sort autofixes (`I001`, `RUF022`, `TC003`) across `src` and `tests`.

## [1.0.4] 2026-06-14

### Changed
- Added a `typed_click.py` facade wrapping rich-click's `option` / `argument` decorators behind explicit, fully-known signatures, keeping the CLI strict-clean under pyright 1.1.410 (`reportUnknownMemberType`) without disabling the rule (ignore isolated to the facade).
- Migrated build automation from the in-repo `scripts/` package to the external `bmk` tooling (`uvx bmk`); removed the obsolete `scripts/` directory and `[tool.scripts.test]` config; added `[tool.bashate]` settings.
- Bumped `lib_cli_exit_tools` floor to `>=2.3.2`.

## [1.0.3] - 2026-04-26

### Changed
- Pruned stale entries from the `pip-audit` ignore list and documented the two remaining accepted-risk advisories inline.

### Fixed
- Unblocked CI by ignoring `CVE-2026-3219` in `pip-audit`; the runner-bundled `pip 26.0.1` is affected and no upstream fix is available yet.

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
