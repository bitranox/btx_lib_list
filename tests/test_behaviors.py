"""Behavior layer tests: each helper tells a single story.

Each test reads like plain English describing one specific behavior.
No test verifies more than one truth.
Real behavior is tested, not mocked interfaces.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import StringIO

import pytest

from btx_lib_list import behaviors


# ---------------------------------------------------------------------------
# Greeting Emission: Writing to Streams
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestGreetingWritesToStream:
    """emit_greeting writes the canonical message to the target stream."""

    def test_greeting_appears_in_buffer(self) -> None:
        """The greeting text appears in the provided buffer."""
        buffer = StringIO()

        behaviors.emit_greeting(stream=buffer)

        assert buffer.getvalue() == "Hello World\n"

    def test_greeting_ends_with_newline(self) -> None:
        """The greeting text ends with exactly one newline."""
        buffer = StringIO()

        behaviors.emit_greeting(stream=buffer)

        assert buffer.getvalue().endswith("\n")
        assert buffer.getvalue().count("\n") == 1


@pytest.mark.os_agnostic
class TestGreetingDefaultsToStdout:
    """emit_greeting uses stdout when no stream is given."""

    def test_greeting_appears_on_stdout(self, capsys: pytest.CaptureFixture[str]) -> None:
        """The greeting appears on stdout when no stream is provided."""
        behaviors.emit_greeting()

        assert capsys.readouterr().out == "Hello World\n"

    def test_stderr_remains_silent(self, capsys: pytest.CaptureFixture[str]) -> None:
        """The greeting never writes to stderr."""
        behaviors.emit_greeting()

        assert capsys.readouterr().err == ""


@pytest.mark.os_agnostic
class TestGreetingFlushBehavior:
    """emit_greeting flushes streams that support flushing."""

    def test_flushable_stream_is_flushed(self) -> None:
        """Streams with a flush method are flushed after writing."""

        @dataclass
        class FlushableStream:
            content: list[str]
            flushed: bool = False

            def write(self, text: str) -> None:
                self.content.append(text)

            def flush(self) -> None:
                self.flushed = True

        stream = FlushableStream([])

        behaviors.emit_greeting(stream=stream)  # type: ignore[arg-type]

        assert stream.flushed is True

    def test_stream_without_flush_works(self) -> None:
        """Streams lacking flush do not cause errors."""

        class MinimalStream:
            def __init__(self) -> None:
                self.written = ""

            def write(self, text: str) -> None:
                self.written = text

        stream = MinimalStream()

        behaviors.emit_greeting(stream=stream)  # type: ignore[arg-type]

        assert stream.written == "Hello World\n"


# ---------------------------------------------------------------------------
# Intentional Failure: The Error Path
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestIntentionalFailure:
    """raise_intentional_failure raises a clear RuntimeError."""

    def test_raises_runtime_error(self) -> None:
        """Calling raise_intentional_failure raises RuntimeError."""
        with pytest.raises(RuntimeError):
            behaviors.raise_intentional_failure()

    def test_error_message_says_i_should_fail(self) -> None:
        """The error message states 'I should fail'."""
        with pytest.raises(RuntimeError, match="I should fail"):
            behaviors.raise_intentional_failure()


# ---------------------------------------------------------------------------
# Placeholder Main: The Noop Path
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestNoopMain:
    """noop_main does nothing and returns None."""

    def test_returns_none(self) -> None:
        """noop_main returns None."""
        assert behaviors.noop_main() is None

    def test_produces_no_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        """noop_main produces no stdout or stderr output."""
        behaviors.noop_main()

        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""


# ---------------------------------------------------------------------------
# Canonical Greeting Constant
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestCanonicalGreetingConstant:
    """CANONICAL_GREETING holds the expected greeting value."""

    def test_value_is_hello_world(self) -> None:
        """The constant equals 'Hello World'."""
        assert behaviors.CANONICAL_GREETING == "Hello World"

    def test_is_a_string(self) -> None:
        """The constant is a string type."""
        assert isinstance(behaviors.CANONICAL_GREETING, str)


# ---------------------------------------------------------------------------
# Module Exports
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestModuleExports:
    """The module exports all documented public symbols."""

    def test_all_includes_expected_symbols(self) -> None:
        """__all__ includes all documented public symbols."""
        expected = {"CANONICAL_GREETING", "emit_greeting", "raise_intentional_failure", "noop_main"}

        assert set(behaviors.__all__) == expected

    def test_exported_symbols_are_accessible(self) -> None:
        """All exported symbols are accessible from the module."""
        for name in behaviors.__all__:
            assert hasattr(behaviors, name)
