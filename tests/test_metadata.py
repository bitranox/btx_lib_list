"""Metadata tests: package info lives where it should.

Tests verify real metadata against pyproject.toml.
No mocking - direct comparison of actual values.
Each test checks exactly one piece of information.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, cast

import pytest

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[import-not-found, no-redef]

from btx_lib_list import __init__conf__


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
TARGET_FIELDS = ("name", "title", "version", "homepage", "author", "author_email", "shell_command")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def pyproject_data() -> dict[str, Any]:
    """Load and parse pyproject.toml once per test module."""
    return tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# print_info: Output Verification
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestPrintInfo:
    """print_info outputs the expected metadata."""

    def test_is_callable(self) -> None:
        """print_info is a callable function."""
        assert callable(__init__conf__.print_info)

    def test_outputs_expected_fields(self, capsys: pytest.CaptureFixture[str]) -> None:
        """print_info outputs all documented fields."""
        __init__conf__.print_info()
        output = capsys.readouterr().out

        for field in TARGET_FIELDS:
            assert field in output

    def test_shows_package_name(self, capsys: pytest.CaptureFixture[str]) -> None:
        """print_info shows the package name in the header."""
        __init__conf__.print_info()
        output = capsys.readouterr().out

        assert f"Info for {__init__conf__.name}:" in output


# ---------------------------------------------------------------------------
# Metadata Constants Match pyproject.toml
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestMetadataMatchesPyproject:
    """Module constants match pyproject.toml values."""

    def test_name_matches(self, pyproject_data: dict[str, Any]) -> None:
        """The package name matches pyproject.toml."""
        project_table = cast(dict[str, Any], pyproject_data["project"])
        expected = project_table["name"]

        assert __init__conf__.name == expected

    def test_version_matches(self, pyproject_data: dict[str, Any]) -> None:
        """The package version matches pyproject.toml."""
        project_table = cast(dict[str, Any], pyproject_data["project"])
        expected = project_table["version"]

        assert __init__conf__.version == expected

    def test_title_matches_description(self, pyproject_data: dict[str, Any]) -> None:
        """The title matches pyproject.toml description."""
        project_table = cast(dict[str, Any], pyproject_data["project"])
        expected = project_table["description"]

        assert __init__conf__.title == expected

    def test_homepage_matches(self, pyproject_data: dict[str, Any]) -> None:
        """The homepage URL matches pyproject.toml."""
        project_table = cast(dict[str, Any], pyproject_data["project"])
        urls = cast(dict[str, str], project_table.get("urls", {}))
        expected = urls["Homepage"]

        assert __init__conf__.homepage == expected

    def test_author_matches(self, pyproject_data: dict[str, Any]) -> None:
        """The author name matches pyproject.toml."""
        project_table = cast(dict[str, Any], pyproject_data["project"])
        authors = cast(list[dict[str, str]], project_table.get("authors", []))
        expected = authors[0]["name"]

        assert __init__conf__.author == expected

    def test_author_email_matches(self, pyproject_data: dict[str, Any]) -> None:
        """The author email matches pyproject.toml."""
        project_table = cast(dict[str, Any], pyproject_data["project"])
        authors = cast(list[dict[str, str]], project_table.get("authors", []))
        expected = authors[0]["email"]

        assert __init__conf__.author_email == expected

    def test_shell_command_in_scripts(self, pyproject_data: dict[str, Any]) -> None:
        """The shell command exists in pyproject.toml scripts."""
        project_table = cast(dict[str, Any], pyproject_data["project"])
        scripts = cast(dict[str, Any], project_table.get("scripts", {}))

        assert __init__conf__.shell_command in scripts


# ---------------------------------------------------------------------------
# pyproject.toml Validation
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestPyprojectValidity:
    """pyproject.toml contains valid, well-formed data."""

    def test_has_at_least_one_author(self, pyproject_data: dict[str, Any]) -> None:
        """pyproject.toml defines at least one author."""
        project_table = cast(dict[str, Any], pyproject_data["project"])
        authors = cast(list[dict[str, str]], project_table.get("authors", []))

        assert len(authors) >= 1

    def test_has_homepage_url(self, pyproject_data: dict[str, Any]) -> None:
        """pyproject.toml defines a homepage URL."""
        project_table = cast(dict[str, Any], pyproject_data["project"])
        urls = cast(dict[str, str], project_table.get("urls", {}))
        homepage = urls.get("Homepage")

        assert homepage is not None
        assert len(homepage) > 0

    def test_version_is_semver(self, pyproject_data: dict[str, Any]) -> None:
        """pyproject.toml version follows semantic versioning."""
        project_table = cast(dict[str, Any], pyproject_data["project"])
        version = project_table["version"]
        semver_pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$"

        assert re.match(semver_pattern, version) is not None
