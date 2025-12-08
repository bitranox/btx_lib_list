"""Module entry tests: ensuring `python -m` mirrors the CLI.

Tests verify module entry behavior using the actual CLI commands.
Real behavior tests are preferred; stubs are used only for
testing specific exit code scenarios and library interactions.
"""

from __future__ import annotations

import runpy
import sys
from collections.abc import Callable

import pytest

import lib_cli_exit_tools

from btx_lib_list import __main__ as main_mod
from btx_lib_list import cli as cli_mod


# ---------------------------------------------------------------------------
# Module Entry: Real Behavior Tests
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestModuleEntryRealBehavior:
    """Module entry executes the real CLI commands."""

    def test_hello_command_returns_zero(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Running 'python -m btx_lib_list hello' returns exit code 0."""
        monkeypatch.setattr(sys, "argv", ["btx_lib_list", "hello"])

        with pytest.raises(SystemExit) as exc:
            runpy.run_module("btx_lib_list.__main__", run_name="__main__")

        assert exc.value.code == 0
        assert "Hello World" in capsys.readouterr().out

    def test_info_command_returns_zero(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Running 'python -m btx_lib_list info' returns exit code 0."""
        monkeypatch.setattr(sys, "argv", ["btx_lib_list", "info"])

        with pytest.raises(SystemExit) as exc:
            runpy.run_module("btx_lib_list.__main__", run_name="__main__")

        assert exc.value.code == 0
        assert "btx_lib_list" in capsys.readouterr().out

    def test_fail_command_returns_nonzero(
        self,
        monkeypatch: pytest.MonkeyPatch,
        isolated_traceback_config: None,
    ) -> None:
        """Running 'python -m btx_lib_list fail' returns non-zero exit code."""
        monkeypatch.setattr(sys, "argv", ["btx_lib_list", "fail"])

        with pytest.raises(SystemExit) as exc:
            runpy.run_module("btx_lib_list.__main__", run_name="__main__")

        assert exc.value.code != 0


# ---------------------------------------------------------------------------
# Module Entry: Traceback Flag Behavior
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestModuleEntryTracebackFlag:
    """The --traceback flag affects error output formatting."""

    def test_shows_full_traceback(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
        strip_ansi: Callable[[str], str],
        isolated_traceback_config: None,
    ) -> None:
        """Using --traceback shows 'Traceback (most recent call last)'."""
        monkeypatch.setattr(sys, "argv", ["btx_lib_list", "--traceback", "fail"])

        with pytest.raises(SystemExit):
            runpy.run_module("btx_lib_list.__main__", run_name="__main__")

        plain_err = strip_ansi(capsys.readouterr().err)

        assert "Traceback (most recent call last)" in plain_err

    def test_shows_exception_message(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
        strip_ansi: Callable[[str], str],
        isolated_traceback_config: None,
    ) -> None:
        """Using --traceback shows the exception type and message."""
        monkeypatch.setattr(sys, "argv", ["btx_lib_list", "--traceback", "fail"])

        with pytest.raises(SystemExit):
            runpy.run_module("btx_lib_list.__main__", run_name="__main__")

        plain_err = strip_ansi(capsys.readouterr().err)

        assert "RuntimeError: I should fail" in plain_err

    def test_output_not_truncated(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
        strip_ansi: Callable[[str], str],
        isolated_traceback_config: None,
    ) -> None:
        """Traceback output is not truncated."""
        monkeypatch.setattr(sys, "argv", ["btx_lib_list", "--traceback", "fail"])

        with pytest.raises(SystemExit):
            runpy.run_module("btx_lib_list.__main__", run_name="__main__")

        plain_err = strip_ansi(capsys.readouterr().err)

        assert "[TRUNCATED" not in plain_err

    def test_config_restored_after_execution(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
        strip_ansi: Callable[[str], str],
        isolated_traceback_config: None,
    ) -> None:
        """After execution, traceback config is restored to disabled."""
        monkeypatch.setattr(sys, "argv", ["btx_lib_list", "--traceback", "fail"])

        with pytest.raises(SystemExit):
            runpy.run_module("btx_lib_list.__main__", run_name="__main__")

        # Consume output
        strip_ansi(capsys.readouterr().err)

        assert lib_cli_exit_tools.config.traceback is False
        assert lib_cli_exit_tools.config.traceback_force_color is False


# ---------------------------------------------------------------------------
# Traceback Limits: Constants Verification
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestTracebackLimits:
    """Traceback limits match the CLI module configuration."""

    def test_summary_limit_matches_cli(self) -> None:
        """TRACEBACK_SUMMARY_LIMIT matches the CLI module."""
        assert main_mod.TRACEBACK_SUMMARY_LIMIT == cli_mod.TRACEBACK_SUMMARY_LIMIT

    def test_verbose_limit_matches_cli(self) -> None:
        """TRACEBACK_VERBOSE_LIMIT matches the CLI module."""
        assert main_mod.TRACEBACK_VERBOSE_LIMIT == cli_mod.TRACEBACK_VERBOSE_LIMIT


# ---------------------------------------------------------------------------
# CLI Name Consistency
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestCliNameConsistency:
    """CLI command name is consistently configured."""

    def test_cli_name_is_string(self) -> None:
        """The CLI command has a string name."""
        assert isinstance(cli_mod.cli.name, str)

    def test_cli_name_not_empty(self) -> None:
        """The CLI command name is not empty."""
        assert len(cli_mod.cli.name or "") > 0
