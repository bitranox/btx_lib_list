"""Shared pytest fixtures and OS marker configuration.

Purpose:
    Centralizes test configuration, fixture definitions, and platform markers
    so the test suite adapts cleanly to each execution environment.

Fixture Philosophy:
    Fixtures shared across multiple test modules belong here.
    Module-specific fixtures stay within their respective test files.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from dataclasses import fields
from typing import TYPE_CHECKING

import pytest
from click.testing import CliRunner

import lib_cli_exit_tools

if TYPE_CHECKING:
    from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ANSI_ESCAPE_PATTERN = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
CONFIG_FIELDS: tuple[str, ...] = tuple(field.name for field in fields(type(lib_cli_exit_tools.config)))


# ---------------------------------------------------------------------------
# Marker Registration
# ---------------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """Register OS-specific markers for test categorization."""
    config.addinivalue_line("markers", "os_agnostic: test runs on every supported OS")
    config.addinivalue_line("markers", "os_windows: test exercises Windows-only behavior")
    config.addinivalue_line("markers", "os_macos: test exercises macOS-only behavior")
    config.addinivalue_line("markers", "os_posix: test exercises POSIX-only behavior")
    config.addinivalue_line("markers", "os_linux: test exercises Linux-only behavior")


# ---------------------------------------------------------------------------
# Text Processing Helpers
# ---------------------------------------------------------------------------


def _remove_ansi_codes(text: str) -> str:
    """Strip ANSI escape sequences from text for stable assertions."""
    return ANSI_ESCAPE_PATTERN.sub("", text)


# ---------------------------------------------------------------------------
# CLI Configuration Helpers
# ---------------------------------------------------------------------------


def _snapshot_cli_config() -> dict[str, Any]:
    """Capture every attribute from lib_cli_exit_tools.config."""
    return {name: getattr(lib_cli_exit_tools.config, name) for name in CONFIG_FIELDS}


def _restore_cli_config(snapshot: dict[str, Any]) -> None:
    """Reapply a previously captured CLI configuration."""
    for name, value in snapshot.items():
        setattr(lib_cli_exit_tools.config, name, value)


# ---------------------------------------------------------------------------
# CLI Runner Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a fresh CliRunner for each test.

    Each test receives an isolated runner to prevent state leakage
    between CLI invocations.
    """
    return CliRunner()


# ---------------------------------------------------------------------------
# Output Cleaning Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def strip_ansi() -> Callable[[str], str]:
    """Return a helper that strips ANSI escape sequences.

    Use this when asserting on CLI output that may contain
    color codes from rich-click.
    """
    return _remove_ansi_codes


# ---------------------------------------------------------------------------
# Traceback State Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def preserve_traceback_state() -> Iterator[None]:
    """Snapshot and restore lib_cli_exit_tools configuration.

    Use this fixture when tests modify traceback settings and must
    restore them afterward to avoid polluting other tests.
    """
    snapshot = _snapshot_cli_config()
    try:
        yield
    finally:
        _restore_cli_config(snapshot)


@pytest.fixture
def isolated_traceback_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reset traceback flags to a known disabled baseline.

    Use this fixture to ensure tests start with traceback disabled,
    preventing accidental state leakage from previous tests.
    """
    lib_cli_exit_tools.reset_config()
    monkeypatch.setattr(lib_cli_exit_tools.config, "traceback", False, raising=False)
    monkeypatch.setattr(lib_cli_exit_tools.config, "traceback_force_color", False, raising=False)
