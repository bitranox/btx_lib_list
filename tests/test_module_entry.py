"""Module entry stories ensuring `python -m` mirrors the console script."""

from __future__ import annotations

import importlib
import runpy
import sys
from typing import TYPE_CHECKING

import lib_cli_exit_tools
import pytest

from btx_lib_list import cli as cli_mod

if TYPE_CHECKING:
    from collections.abc import Callable


def _run_module_entry(monkeypatch: pytest.MonkeyPatch, argv: list[str]) -> int:
    """Run ``python -m btx_lib_list`` with ``argv`` and return its exit code."""
    monkeypatch.setattr(sys, "argv", ["btx_lib_list", *argv])
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("btx_lib_list.__main__", run_name="__main__")
    code = exc.value.code
    assert isinstance(code, int)
    return code


@pytest.mark.os_agnostic
def test_hello_via_module_entry_exits_zero_and_greets(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    assert _run_module_entry(monkeypatch, ["hello"]) == 0
    assert "Hello World" in capsys.readouterr().out


@pytest.mark.os_agnostic
def test_info_via_module_entry_exits_zero_and_names_the_package(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    assert _run_module_entry(monkeypatch, ["info"]) == 0
    assert "btx_lib_list" in capsys.readouterr().out


@pytest.mark.os_agnostic
@pytest.mark.parametrize("argv", [["--bad-flag"], ["no-such-command"], ["fail"], ["hello"], ["--help"]])
def test_module_entry_exits_with_the_code_the_console_script_gives(monkeypatch: pytest.MonkeyPatch, isolated_traceback_config: None, argv: list[str]) -> None:
    script_code = cli_mod.main(argv)

    assert _run_module_entry(monkeypatch, argv) == script_code


@pytest.mark.os_agnostic
@pytest.mark.parametrize("argv", [["--bad-flag"], ["no-such-command"]])
def test_a_usage_error_via_module_entry_exits_two(monkeypatch: pytest.MonkeyPatch, isolated_traceback_config: None, argv: list[str]) -> None:
    assert _run_module_entry(monkeypatch, argv) == 2


@pytest.mark.os_agnostic
def test_traceback_flag_via_module_entry_prints_the_full_traceback(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    strip_ansi: Callable[[str], str],
    isolated_traceback_config: None,
) -> None:
    code = _run_module_entry(monkeypatch, ["--traceback", "fail"])

    plain_err = strip_ansi(capsys.readouterr().err)
    assert code != 0
    assert "Traceback (most recent call last)" in plain_err
    assert "RuntimeError: I should fail" in plain_err
    assert "[TRUNCATED" not in plain_err
    assert lib_cli_exit_tools.config.traceback is False
    assert lib_cli_exit_tools.config.traceback_force_color is False


@pytest.mark.os_agnostic
def test_when_the_module_is_imported_it_runs_nothing() -> None:
    # Left imported, every later runpy of btx_lib_list.__main__ warns that it is already loaded.
    previous = sys.modules.pop("btx_lib_list.__main__", None)
    try:
        module = importlib.import_module("btx_lib_list.__main__")

        assert module.cli is cli_mod
    finally:
        sys.modules.pop("btx_lib_list.__main__", None)
        if previous is not None:
            sys.modules["btx_lib_list.__main__"] = previous
