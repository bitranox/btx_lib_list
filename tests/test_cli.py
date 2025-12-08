"""CLI tests: every invocation tells a single story.

Tests exercise real CLI behavior through Click's CliRunner.
Each test verifies exactly one behavior.
Real behavior is preferred over stubs.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest
from click.testing import CliRunner

import lib_cli_exit_tools

from btx_lib_list import __init__conf__
from btx_lib_list import cli as cli_mod


# ---------------------------------------------------------------------------
# Traceback State: Snapshot Captures State
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestTracebackSnapshot:
    """snapshot_traceback_state captures the current traceback configuration."""

    def test_captures_traceback_disabled(self, isolated_traceback_config: None) -> None:
        """When traceback is disabled, snapshot reflects that."""
        snapshot = cli_mod.snapshot_traceback_state()

        assert snapshot.traceback_enabled is False

    def test_captures_force_color_disabled(self, isolated_traceback_config: None) -> None:
        """When force_color is disabled, snapshot reflects that."""
        snapshot = cli_mod.snapshot_traceback_state()

        assert snapshot.force_color is False

    def test_captures_traceback_enabled(self, isolated_traceback_config: None) -> None:
        """When traceback is enabled, snapshot reflects that."""
        cli_mod.apply_traceback_preferences(True)

        snapshot = cli_mod.snapshot_traceback_state()

        assert snapshot.traceback_enabled is True

    def test_captures_force_color_enabled(self, isolated_traceback_config: None) -> None:
        """When force_color is enabled, snapshot reflects that."""
        cli_mod.apply_traceback_preferences(True)

        snapshot = cli_mod.snapshot_traceback_state()

        assert snapshot.force_color is True


# ---------------------------------------------------------------------------
# Traceback State: Apply Changes Configuration
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestApplyTracebackPreferences:
    """apply_traceback_preferences sets global traceback configuration."""

    def test_enabling_sets_traceback_flag(self, isolated_traceback_config: None) -> None:
        """Enabling traceback sets the traceback flag to True."""
        cli_mod.apply_traceback_preferences(True)

        assert lib_cli_exit_tools.config.traceback is True

    def test_enabling_sets_force_color_flag(self, isolated_traceback_config: None) -> None:
        """Enabling traceback sets force_color to True."""
        cli_mod.apply_traceback_preferences(True)

        assert lib_cli_exit_tools.config.traceback_force_color is True

    def test_disabling_clears_traceback_flag(self, isolated_traceback_config: None) -> None:
        """Disabling traceback sets the traceback flag to False."""
        cli_mod.apply_traceback_preferences(True)
        cli_mod.apply_traceback_preferences(False)

        assert lib_cli_exit_tools.config.traceback is False

    def test_disabling_clears_force_color_flag(self, isolated_traceback_config: None) -> None:
        """Disabling traceback sets force_color to False."""
        cli_mod.apply_traceback_preferences(True)
        cli_mod.apply_traceback_preferences(False)

        assert lib_cli_exit_tools.config.traceback_force_color is False


# ---------------------------------------------------------------------------
# Traceback State: Restore Reverts Changes
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestRestoreTracebackState:
    """restore_traceback_state reverts to a previously captured state."""

    def test_restores_traceback_flag(self, isolated_traceback_config: None) -> None:
        """Restoring reverts the traceback flag to its snapshot value."""
        previous = cli_mod.snapshot_traceback_state()
        cli_mod.apply_traceback_preferences(True)

        cli_mod.restore_traceback_state(previous)

        assert lib_cli_exit_tools.config.traceback is False

    def test_restores_force_color_flag(self, isolated_traceback_config: None) -> None:
        """Restoring reverts the force_color flag to its snapshot value."""
        previous = cli_mod.snapshot_traceback_state()
        cli_mod.apply_traceback_preferences(True)

        cli_mod.restore_traceback_state(previous)

        assert lib_cli_exit_tools.config.traceback_force_color is False


# ---------------------------------------------------------------------------
# CLI Without Arguments: Shows Help
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestCliWithoutArguments:
    """Invoking CLI with no arguments shows help and exits successfully."""

    def test_exits_with_zero(self, cli_runner: CliRunner) -> None:
        """CLI with no arguments exits with code 0."""
        result = cli_runner.invoke(cli_mod.cli, [])

        assert result.exit_code == 0

    def test_shows_usage_information(self, cli_runner: CliRunner) -> None:
        """CLI with no arguments displays usage information."""
        result = cli_runner.invoke(cli_mod.cli, [])

        assert "Usage:" in result.output


# ---------------------------------------------------------------------------
# Hello Command: Emits Greeting
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestHelloCommand:
    """The hello command emits the canonical greeting."""

    def test_exits_successfully(self, cli_runner: CliRunner) -> None:
        """The hello command exits with code 0."""
        result = cli_runner.invoke(cli_mod.cli, ["hello"])

        assert result.exit_code == 0

    def test_outputs_hello_world(self, cli_runner: CliRunner) -> None:
        """The hello command outputs 'Hello World'."""
        result = cli_runner.invoke(cli_mod.cli, ["hello"])

        assert result.output == "Hello World\n"


# ---------------------------------------------------------------------------
# Info Command: Shows Package Information
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestInfoCommand:
    """The info command displays package metadata."""

    def test_exits_successfully(self, cli_runner: CliRunner) -> None:
        """The info command exits with code 0."""
        result = cli_runner.invoke(cli_mod.cli, ["info"])

        assert result.exit_code == 0

    def test_shows_package_name(self, cli_runner: CliRunner) -> None:
        """The info command displays the package name."""
        result = cli_runner.invoke(cli_mod.cli, ["info"])

        assert f"Info for {__init__conf__.name}:" in result.output

    def test_shows_version(self, cli_runner: CliRunner) -> None:
        """The info command displays the package version."""
        result = cli_runner.invoke(cli_mod.cli, ["info"])

        assert __init__conf__.version in result.output


# ---------------------------------------------------------------------------
# Fail Command: Triggers Error
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestFailCommand:
    """The fail command deliberately triggers an error."""

    def test_exits_with_nonzero(self, cli_runner: CliRunner) -> None:
        """The fail command exits with a non-zero exit code."""
        result = cli_runner.invoke(cli_mod.cli, ["fail"])

        assert result.exit_code != 0

    def test_raises_runtime_error(self, cli_runner: CliRunner) -> None:
        """The fail command raises RuntimeError."""
        result = cli_runner.invoke(cli_mod.cli, ["fail"])

        assert isinstance(result.exception, RuntimeError)


# ---------------------------------------------------------------------------
# Unknown Command: Shows Error
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestUnknownCommand:
    """An unknown command shows an error message."""

    def test_exits_with_error(self, cli_runner: CliRunner) -> None:
        """An unknown command exits with a non-zero code."""
        result = cli_runner.invoke(cli_mod.cli, ["does-not-exist"])

        assert result.exit_code != 0

    def test_shows_no_such_command(self, cli_runner: CliRunner) -> None:
        """An unknown command shows 'No such command' message."""
        result = cli_runner.invoke(cli_mod.cli, ["does-not-exist"])

        assert "No such command" in result.output


# ---------------------------------------------------------------------------
# Traceback Flag Without Subcommand
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestTracebackFlagWithoutSubcommand:
    """Using --traceback without a subcommand runs noop_main."""

    def test_exits_successfully(self, cli_runner: CliRunner) -> None:
        """--traceback without a subcommand exits with code 0."""
        result = cli_runner.invoke(cli_mod.cli, ["--traceback"])

        assert result.exit_code == 0

    def test_does_not_show_help(self, cli_runner: CliRunner) -> None:
        """--traceback without a subcommand does not display help."""
        result = cli_runner.invoke(cli_mod.cli, ["--traceback"])

        assert "Usage:" not in result.output


# ---------------------------------------------------------------------------
# Traceback Flag: Error Formatting
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestTracebackErrorFormatting:
    """The --traceback flag shows full tracebacks on errors."""

    def test_shows_traceback_header(
        self,
        isolated_traceback_config: None,
        capsys: pytest.CaptureFixture[str],
        strip_ansi: Callable[[str], str],
    ) -> None:
        """The --traceback flag shows 'Traceback (most recent call last)'."""
        cli_mod.main(["--traceback", "fail"])

        plain_err = strip_ansi(capsys.readouterr().err)

        assert "Traceback (most recent call last)" in plain_err

    def test_shows_exception_details(
        self,
        isolated_traceback_config: None,
        capsys: pytest.CaptureFixture[str],
        strip_ansi: Callable[[str], str],
    ) -> None:
        """The --traceback flag shows 'RuntimeError: I should fail'."""
        cli_mod.main(["--traceback", "fail"])

        plain_err = strip_ansi(capsys.readouterr().err)

        assert "RuntimeError: I should fail" in plain_err

    def test_output_is_not_truncated(
        self,
        isolated_traceback_config: None,
        capsys: pytest.CaptureFixture[str],
        strip_ansi: Callable[[str], str],
    ) -> None:
        """The --traceback output is not truncated."""
        cli_mod.main(["--traceback", "fail"])

        plain_err = strip_ansi(capsys.readouterr().err)

        assert "[TRUNCATED" not in plain_err


# ---------------------------------------------------------------------------
# Traceback Flag: State Restoration
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestTracebackStateRestoration:
    """The traceback configuration is restored after execution."""

    def test_traceback_flag_restored(self, isolated_traceback_config: None) -> None:
        """After execution, the traceback flag is restored to disabled."""
        cli_mod.main(["--traceback", "fail"])

        assert lib_cli_exit_tools.config.traceback is False

    def test_force_color_flag_restored(self, isolated_traceback_config: None) -> None:
        """After execution, the force_color flag is restored to disabled."""
        cli_mod.main(["--traceback", "fail"])

        assert lib_cli_exit_tools.config.traceback_force_color is False


# ---------------------------------------------------------------------------
# Main Function: Exit Codes
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestMainExitCodes:
    """main() returns appropriate exit codes for each command."""

    def test_hello_returns_zero(self, isolated_traceback_config: None) -> None:
        """main returns 0 for the hello command."""
        exit_code = cli_mod.main(["hello"])

        assert exit_code == 0

    def test_fail_returns_nonzero(self, isolated_traceback_config: None) -> None:
        """main returns non-zero for the fail command."""
        exit_code = cli_mod.main(["fail"])

        assert exit_code != 0

    def test_info_returns_zero(self, isolated_traceback_config: None) -> None:
        """main returns 0 for the info command."""
        exit_code = cli_mod.main(["info"])

        assert exit_code == 0


# ---------------------------------------------------------------------------
# Restore Traceback Option
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestRestoreTracebackOption:
    """main(restore_traceback=False) preserves traceback state."""

    def test_keeps_traceback_enabled(
        self,
        isolated_traceback_config: None,
        preserve_traceback_state: None,
    ) -> None:
        """When restore_traceback=False, traceback stays enabled."""
        cli_mod.apply_traceback_preferences(False)

        cli_mod.main(["--traceback", "hello"], restore_traceback=False)

        assert lib_cli_exit_tools.config.traceback is True

    def test_keeps_force_color_enabled(
        self,
        isolated_traceback_config: None,
        preserve_traceback_state: None,
    ) -> None:
        """When restore_traceback=False, force_color stays enabled."""
        cli_mod.apply_traceback_preferences(False)

        cli_mod.main(["--traceback", "hello"], restore_traceback=False)

        assert lib_cli_exit_tools.config.traceback_force_color is True


# ---------------------------------------------------------------------------
# Info Command With Traceback Flag
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestInfoWithTracebackFlag:
    """Info command works correctly with --traceback flag."""

    def test_returns_zero(
        self,
        isolated_traceback_config: None,
        preserve_traceback_state: None,
    ) -> None:
        """Info command with --traceback returns 0."""
        exit_code = cli_mod.main(["--traceback", "info"])

        assert exit_code == 0

    def test_restores_traceback_flag(
        self,
        isolated_traceback_config: None,
        preserve_traceback_state: None,
    ) -> None:
        """Info command with --traceback restores the traceback flag."""
        cli_mod.main(["--traceback", "info"])

        assert lib_cli_exit_tools.config.traceback is False

    def test_restores_force_color_flag(
        self,
        isolated_traceback_config: None,
        preserve_traceback_state: None,
    ) -> None:
        """Info command with --traceback restores the force_color flag."""
        cli_mod.main(["--traceback", "info"])

        assert lib_cli_exit_tools.config.traceback_force_color is False


# ---------------------------------------------------------------------------
# Version Option
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestVersionOption:
    """The --version option shows version information."""

    def test_shows_version(self, cli_runner: CliRunner) -> None:
        """The --version option displays the package version."""
        result = cli_runner.invoke(cli_mod.cli, ["--version"])

        assert __init__conf__.version in result.output

    def test_exits_successfully(self, cli_runner: CliRunner) -> None:
        """The --version option exits with code 0."""
        result = cli_runner.invoke(cli_mod.cli, ["--version"])

        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# Help Options
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestHelpOptions:
    """The --help and -h options show help text."""

    def test_long_help_shows_usage(self, cli_runner: CliRunner) -> None:
        """The --help option displays help text."""
        result = cli_runner.invoke(cli_mod.cli, ["--help"])

        assert "Usage:" in result.output

    def test_short_help_shows_usage(self, cli_runner: CliRunner) -> None:
        """The -h option displays help text."""
        result = cli_runner.invoke(cli_mod.cli, ["-h"])

        assert "Usage:" in result.output

    def test_help_exits_successfully(self, cli_runner: CliRunner) -> None:
        """The --help option exits with code 0."""
        result = cli_runner.invoke(cli_mod.cli, ["--help"])

        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# CLI Constants
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestCliConstants:
    """CLI constants have expected values."""

    def test_context_settings_includes_help_options(self) -> None:
        """CLI context settings include -h and --help."""
        expected = ["-h", "--help"]

        assert cli_mod.CLICK_CONTEXT_SETTINGS["help_option_names"] == expected

    def test_summary_limit_is_positive(self) -> None:
        """The traceback summary limit is a positive integer."""
        assert cli_mod.TRACEBACK_SUMMARY_LIMIT > 0

    def test_verbose_limit_exceeds_summary_limit(self) -> None:
        """The verbose limit is larger than the summary limit."""
        assert cli_mod.TRACEBACK_VERBOSE_LIMIT > cli_mod.TRACEBACK_SUMMARY_LIMIT


# ---------------------------------------------------------------------------
# TracebackState Dataclass
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestTracebackStateDataclass:
    """TracebackState dataclass stores traceback configuration."""

    def test_stores_traceback_enabled(self) -> None:
        """TracebackState stores the traceback_enabled field."""
        state = cli_mod.TracebackState(traceback_enabled=True, force_color=False)

        assert state.traceback_enabled is True

    def test_stores_force_color(self) -> None:
        """TracebackState stores the force_color field."""
        state = cli_mod.TracebackState(traceback_enabled=False, force_color=True)

        assert state.force_color is True


# ---------------------------------------------------------------------------
# CliContext Dataclass
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestCliContextDataclass:
    """CliContext dataclass stores CLI context options."""

    def test_default_traceback_is_false(self) -> None:
        """CliContext defaults traceback to False."""
        ctx = cli_mod.CliContext()

        assert ctx.traceback is False

    def test_accepts_traceback_parameter(self) -> None:
        """CliContext can be initialized with traceback=True."""
        ctx = cli_mod.CliContext(traceback=True)

        assert ctx.traceback is True
