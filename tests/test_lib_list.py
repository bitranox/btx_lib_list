"""List utility tests: each helper speaks one truth.

Tests verify real behavior of list manipulation functions.
No mocking, only direct function calls and assertions.
Each test checks exactly one behavior.
"""

from __future__ import annotations

from typing import Any

import pytest

import btx_lib_list
from btx_lib_list import lib_list


# ---------------------------------------------------------------------------
# deduplicate: Removing Duplicates
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestDeduplicate:
    """deduplicate removes duplicate elements from a list."""

    def test_removes_duplicates(self) -> None:
        """Duplicate elements are removed from the list."""
        result = lib_list.deduplicate(["b", "a", "b"])

        assert set(result) == {"a", "b"}

    def test_returns_correct_count(self) -> None:
        """The result contains only unique elements."""
        result = lib_list.deduplicate(["b", "a", "b"])

        assert len(result) == 2

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.deduplicate([]) == []

    def test_single_element_unchanged(self) -> None:
        """A single element list returns unchanged."""
        assert lib_list.deduplicate(["x"]) == ["x"]

    def test_all_duplicates_collapse_to_one(self) -> None:
        """A list of identical elements returns one element."""
        result = lib_list.deduplicate(["a", "a", "a"])

        assert result == ["a"]


# ---------------------------------------------------------------------------
# del_elements_containing: Filtering by Substring
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestDelElementsContaining:
    """del_elements_containing removes elements with a given substring."""

    def test_filters_matching_elements(self) -> None:
        """Elements containing the search string are removed."""
        result = lib_list.del_elements_containing(["a", "abba", "c"], "b")

        assert result == ["a", "c"]

    def test_empty_search_returns_original(self) -> None:
        """An empty search string returns the original list."""
        original = ["a", "abba", "c"]

        result = lib_list.del_elements_containing(original, "")

        assert result is original

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.del_elements_containing([], "b") == []

    def test_nonmatching_elements_kept(self) -> None:
        """Elements not containing the search string are kept."""
        result = lib_list.del_elements_containing(["abc", "def", "ghi"], "z")

        assert result == ["abc", "def", "ghi"]

    def test_does_not_mutate_original(self) -> None:
        """The original list is not modified."""
        original = ["a", "abba", "c"]

        lib_list.del_elements_containing(original, "b")

        assert original == ["a", "abba", "c"]


# ---------------------------------------------------------------------------
# filter_contains: Selecting by Substring
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestFilterContains:
    """filter_contains returns elements containing a substring."""

    def test_returns_matching_strings(self) -> None:
        """Only strings containing the search string are returned."""
        result = lib_list.filter_contains(["abcd", "def", 1], "bc")

        assert result == ["abcd"]

    def test_empty_search_returns_all_strings(self) -> None:
        """An empty search returns all string elements."""
        result = lib_list.filter_contains(["abc", 123], "")

        assert result == ["abc"]

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.filter_contains([], "bc") == []

    def test_ignores_non_strings(self) -> None:
        """Non-string elements are filtered out."""
        result = lib_list.filter_contains([1, 2, "abc", None], "a")

        assert result == ["abc"]

    def test_no_matches_returns_empty(self) -> None:
        """When no strings match, an empty list is returned."""
        result = lib_list.filter_contains(["abc", "def"], "xyz")

        assert result == []


# ---------------------------------------------------------------------------
# filter_fnmatch: Shell Pattern Matching
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestFilterFnmatch:
    """filter_fnmatch returns strings matching a shell pattern."""

    def test_returns_matching_strings(self) -> None:
        """Strings matching the fnmatch pattern are returned."""
        result = lib_list.filter_fnmatch(["abc", "def", 1], "a*")

        assert result == ["abc"]

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.filter_fnmatch([], "*") == []

    def test_ignores_non_strings(self) -> None:
        """Non-string elements are not matched."""
        result = lib_list.filter_fnmatch([1, 2, "abc"], "*")

        assert result == ["abc"]

    def test_question_mark_matches_single_char(self) -> None:
        """The ? pattern matches single characters."""
        result = lib_list.filter_fnmatch(["a", "ab", "abc"], "a?")

        assert result == ["ab"]

    def test_bracket_matches_character_set(self) -> None:
        """The [abc] pattern matches character sets."""
        result = lib_list.filter_fnmatch(["ax", "bx", "cx", "dx"], "[ab]x")

        assert result == ["ax", "bx"]


# ---------------------------------------------------------------------------
# is_element_containing: Substring Presence Check
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestIsElementContaining:
    """is_element_containing checks if any element contains a substring."""

    def test_detects_match(self) -> None:
        """Returns True when a string contains the search string."""
        assert lib_list.is_element_containing(["abc", "def"], "bc") is True

    def test_detects_no_match(self) -> None:
        """Returns False when no string contains the search string."""
        assert lib_list.is_element_containing(["abc", "def"], "xy") is False

    def test_empty_list_returns_false(self) -> None:
        """An empty list returns False."""
        assert lib_list.is_element_containing([], "bc") is False

    def test_empty_search_matches_any_string(self) -> None:
        """An empty search string matches any string."""
        assert lib_list.is_element_containing(["a"], "") is True

    def test_ignores_non_strings(self) -> None:
        """Non-string elements are skipped in the search."""
        assert lib_list.is_element_containing([1, 2, 3], "1") is False  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("sequence", "search", "expected"),
        [
            (["alpha", "beta"], "a", True),
            (["alpha", "beta"], "z", False),
            (["hello", "world"], "or", True),
        ],
    )
    def test_parametrized_cases(self, sequence: list[str], search: str, expected: bool) -> None:
        """Parametrized tests for various inputs."""
        assert lib_list.is_element_containing(sequence, search) is expected


# ---------------------------------------------------------------------------
# is_fnmatching: Pattern Presence Check
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestIsFnmatching:
    """is_fnmatching checks if any element matches a pattern."""

    def test_detects_match(self) -> None:
        """Returns True when a string matches the pattern."""
        assert lib_list.is_fnmatching(["abc", "def"], "*bc*") is True

    def test_detects_no_match(self) -> None:
        """Returns False when no string matches the pattern."""
        assert lib_list.is_fnmatching(["abc", "def"], "*zz*") is False

    def test_empty_list_returns_false(self) -> None:
        """An empty list returns False."""
        assert lib_list.is_fnmatching([], "*") is False

    def test_ignores_non_strings(self) -> None:
        """Non-string elements are skipped."""
        assert lib_list.is_fnmatching([1, 2], "*") is False

    @pytest.mark.parametrize(
        ("sequence", "pattern", "expected"),
        [
            (["alpha", "beta"], "*ta", True),
            (["alpha", "beta"], "*zz", False),
            (["file.txt", "image.png"], "*.txt", True),
        ],
    )
    def test_parametrized_cases(self, sequence: list[str], pattern: str, expected: bool) -> None:
        """Parametrized tests for various patterns."""
        assert lib_list.is_fnmatching(sequence, pattern) is expected


# ---------------------------------------------------------------------------
# is_fnmatching_one_pattern: Multiple Pattern Check
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestIsFnmatchingOnePattern:
    """is_fnmatching_one_pattern checks multiple patterns."""

    def test_detects_match(self) -> None:
        """Returns True when any pattern matches any element."""
        assert lib_list.is_fnmatching_one_pattern(["abc"], ["*bc*", "*zz*"]) is True

    def test_detects_no_match(self) -> None:
        """Returns False when no pattern matches any element."""
        assert lib_list.is_fnmatching_one_pattern(["abc"], ["*zz*", "*yy*"]) is False

    def test_empty_patterns_returns_false(self) -> None:
        """An empty pattern list returns False."""
        assert lib_list.is_fnmatching_one_pattern(["abc"], []) is False

    def test_empty_elements_returns_false(self) -> None:
        """An empty element list returns False."""
        assert lib_list.is_fnmatching_one_pattern([], ["*"]) is False

    def test_short_circuits_on_first_match(self) -> None:
        """Matching stops at the first successful pattern."""
        result = lib_list.is_fnmatching_one_pattern(["abc"], ["*a*", "*b*", "*c*"])

        assert result is True


# ---------------------------------------------------------------------------
# substract_all_keep_sorting: In-Place Removal
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestSubstractAllKeepSorting:
    """substract_all_keep_sorting removes elements while preserving order."""

    def test_mutates_and_returns_source(self) -> None:
        """The function returns the same list object."""
        minuend = ["a", "b", "b"]

        result = lib_list.substract_all_keep_sorting(minuend, ["b"])

        assert result is minuend

    def test_removes_all_matching_elements(self) -> None:
        """All occurrences of subtrahend elements are removed."""
        minuend = ["a", "b", "b"]

        lib_list.substract_all_keep_sorting(minuend, ["b"])

        assert minuend == ["a"]

    def test_empty_minuend_returns_empty(self) -> None:
        """An empty minuend returns an empty list."""
        assert lib_list.substract_all_keep_sorting([], ["a"]) == []

    def test_empty_subtrahend_unchanged(self) -> None:
        """An empty subtrahend leaves the minuend unchanged."""
        minuend = ["a", "b"]

        lib_list.substract_all_keep_sorting(minuend, [])

        assert minuend == ["a", "b"]

    def test_preserves_order(self) -> None:
        """Element order is preserved after removal."""
        minuend = ["c", "a", "b", "a"]

        lib_list.substract_all_keep_sorting(minuend, ["a"])

        assert minuend == ["c", "b"]


# ---------------------------------------------------------------------------
# substract_all_unsorted_fast: Set Difference
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestSubstractAllUnsortedFast:
    """substract_all_unsorted_fast performs fast set difference."""

    def test_removes_elements(self) -> None:
        """Elements in subtrahend are removed from result."""
        result = lib_list.substract_all_unsorted_fast(["a", "a", "b"], ["a"])

        assert sorted(result) == ["b"]

    def test_does_not_mutate_source(self) -> None:
        """The source list is not modified."""
        source = ["a", "a", "b"]

        lib_list.substract_all_unsorted_fast(source, ["a"])

        assert source == ["a", "a", "b"]

    def test_empty_minuend_returns_empty(self) -> None:
        """An empty minuend returns an empty list."""
        result = lib_list.substract_all_unsorted_fast([], ["a"])

        assert result == []

    def test_deduplicates_result(self) -> None:
        """The result contains only unique elements."""
        result = lib_list.substract_all_unsorted_fast(["a", "a", "b", "b"], ["c"])

        assert sorted(result) == ["a", "b"]


# ---------------------------------------------------------------------------
# ls_del_empty_elements: Removing Falsey Values
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestLsDelEmptyElements:
    """ls_del_empty_elements removes falsey values from a list."""

    def test_removes_empty_strings(self) -> None:
        """Empty strings are removed."""
        result = lib_list.ls_del_empty_elements(["", "a", ""])

        assert "a" in result
        assert "" not in result

    def test_removes_none(self) -> None:
        """None values are removed."""
        result = lib_list.ls_del_empty_elements(["a", None, "b"])

        assert None not in result

    def test_removes_zero(self) -> None:
        """Zero values are removed."""
        result = lib_list.ls_del_empty_elements(["a", 0, "b"])

        assert 0 not in result

    def test_keeps_whitespace_strings(self) -> None:
        """Whitespace-only strings are kept (they are truthy)."""
        result = lib_list.ls_del_empty_elements(["  ", "a"])

        assert "  " in result

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.ls_del_empty_elements([]) == []


# ---------------------------------------------------------------------------
# ls_double_quote_if_contains_blank: Quoting Spaces
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestLsDoubleQuoteIfContainsBlank:
    """ls_double_quote_if_contains_blank quotes strings with spaces."""

    def test_quotes_strings_with_spaces(self) -> None:
        """Strings with spaces are wrapped in double quotes."""
        result = lib_list.ls_double_quote_if_contains_blank(["has space"])

        assert result == ['"has space"']

    def test_leaves_simple_strings_unchanged(self) -> None:
        """Strings without spaces remain unchanged."""
        result = lib_list.ls_double_quote_if_contains_blank(["simple"])

        assert result == ["simple"]

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.ls_double_quote_if_contains_blank([]) == []

    def test_empty_string_not_quoted(self) -> None:
        """Empty strings are not quoted."""
        result = lib_list.ls_double_quote_if_contains_blank([""])

        assert result == [""]

    def test_multiple_spaces_quoted_once(self) -> None:
        """Strings with multiple spaces are quoted once."""
        result = lib_list.ls_double_quote_if_contains_blank(["a b c"])

        assert result == ['"a b c"']


# ---------------------------------------------------------------------------
# ls_elements_replace_strings: Substring Replacement
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestLsElementsReplaceStrings:
    """ls_elements_replace_strings replaces substrings in elements."""

    def test_replaces_in_strings(self) -> None:
        """Substrings are replaced in string elements."""
        values: list[Any] = ["abc", "xyz"]

        result = lib_list.ls_elements_replace_strings(values, "a", "z")

        assert result == ["zbc", "xyz"]

    def test_ignores_non_strings(self) -> None:
        """Non-string elements are preserved unchanged."""
        values: list[Any] = ["abc", 1]

        result = lib_list.ls_elements_replace_strings(values, "a", "z")

        assert result[1] == 1

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.ls_elements_replace_strings([], "a", "z") == []

    def test_no_match_unchanged(self) -> None:
        """Strings without the search substring remain unchanged."""
        result = lib_list.ls_elements_replace_strings(["xyz"], "a", "b")

        assert result == ["xyz"]

    def test_replaces_all_occurrences(self) -> None:
        """All occurrences within a string are replaced."""
        result = lib_list.ls_elements_replace_strings(["aaa"], "a", "b")

        assert result == ["bbb"]


# ---------------------------------------------------------------------------
# ls_lstrip_list and ls_rstrip_list: Trimming Lists
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestLsLstripList:
    """ls_lstrip_list removes leading sentinel values."""

    def test_removes_leading_empty_strings(self) -> None:
        """Leading empty strings are removed."""
        values = ["", "", "a", "", ""]

        assert lib_list.ls_lstrip_list(values) == ["a", "", ""]

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.ls_lstrip_list([]) == []

    def test_custom_chars_stripped(self) -> None:
        """Custom sentinel values can be stripped from the left."""
        values = ["x", "x", "a", "x"]

        assert lib_list.ls_lstrip_list(values, "x") == ["a", "x"]


@pytest.mark.os_agnostic
class TestLsRstripList:
    """ls_rstrip_list removes trailing sentinel values."""

    def test_removes_trailing_empty_strings(self) -> None:
        """Trailing empty strings are removed."""
        values = ["", "", "a", "", ""]

        assert lib_list.ls_rstrip_list(values) == ["", "", "a"]

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.ls_rstrip_list([]) == []

    def test_custom_chars_stripped(self) -> None:
        """Custom sentinel values can be stripped from the right."""
        values = ["a", "x", "x"]

        assert lib_list.ls_rstrip_list(values, "x") == ["a"]


# ---------------------------------------------------------------------------
# ls_strip_afz: Quote Stripping
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestLsStripAfz:
    """ls_strip_afz removes surrounding quotes from strings."""

    def test_removes_double_quotes(self) -> None:
        """Double quotes are stripped from strings."""
        result = lib_list.ls_strip_afz(['"hello"'])

        assert result == ["hello"]

    def test_removes_single_quotes(self) -> None:
        """Single quotes are stripped from strings."""
        result = lib_list.ls_strip_afz(["'world'"])

        assert result == ["world"]

    def test_none_input_returns_empty(self) -> None:
        """None input returns an empty list."""
        assert lib_list.ls_strip_afz(None) == []

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.ls_strip_afz([]) == []

    def test_preserves_unquoted_strings(self) -> None:
        """Strings without matching quotes remain unchanged."""
        result = lib_list.ls_strip_afz(["hello"])

        assert result == ["hello"]

    def test_strips_whitespace_before_quotes(self) -> None:
        """Whitespace is stripped before removing quotes."""
        result = lib_list.ls_strip_afz(["  'hello'  "])

        assert result == ["hello"]

    def test_mismatched_quotes_preserved(self) -> None:
        """Mismatched quotes are not stripped."""
        result = lib_list.ls_strip_afz(["'hello\""])

        assert result == ["'hello\""]


# ---------------------------------------------------------------------------
# ls_strip_elements and ls_strip_list
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestLsStripElements:
    """ls_strip_elements strips whitespace from elements."""

    def test_strips_whitespace(self) -> None:
        """Whitespace is stripped from each element."""
        result = lib_list.ls_strip_elements(["  a", "b  "])

        assert result == ["a", "b"]

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.ls_strip_elements([]) == []

    def test_custom_chars_stripped(self) -> None:
        """Custom characters can be stripped."""
        result = lib_list.ls_strip_elements(["xxax", "xbx"], "x")

        assert result == ["a", "b"]


@pytest.mark.os_agnostic
class TestLsStripList:
    """ls_strip_list removes leading and trailing markers."""

    def test_removes_both_ends(self) -> None:
        """Both leading and trailing markers are removed."""
        result = lib_list.ls_strip_list(["", "a", ""])

        assert result == ["a"]


# ---------------------------------------------------------------------------
# ls_rstrip_elements: Right-Side Stripping
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestLsRstripElements:
    """ls_rstrip_elements strips trailing characters from elements."""

    def test_strips_trailing_whitespace(self) -> None:
        """Trailing whitespace is stripped from each element."""
        result = lib_list.ls_rstrip_elements(["a  ", "  b"])

        assert result == ["a", "  b"]

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.ls_rstrip_elements([]) == []

    def test_custom_chars_stripped(self) -> None:
        """Custom characters can be stripped from the right."""
        result = lib_list.ls_rstrip_elements(["axx", "bx"], "x")

        assert result == ["a", "b"]


# ---------------------------------------------------------------------------
# ls_substract: Single Occurrence Removal
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestLsSubstract:
    """ls_substract removes single occurrences of elements."""

    def test_removes_single_occurrence(self) -> None:
        """Only the first occurrence of each element is removed."""
        minuend = ["a", "a", "b"]

        lib_list.ls_substract(minuend, ["a"])

        assert minuend == ["a", "b"]

    def test_ignores_nonexistent_elements(self) -> None:
        """Elements not in the minuend are ignored."""
        minuend = ["a", "a", "b"]

        lib_list.ls_substract(minuend, ["z"])

        assert minuend == ["a", "a", "b"]

    def test_returns_mutated_list(self) -> None:
        """The function returns the mutated minuend."""
        minuend = ["a", "b"]

        result = lib_list.ls_substract(minuend, ["a"])

        assert result is minuend

    def test_handles_multiple_removals(self) -> None:
        """Multiple elements can be removed one at a time."""
        minuend = ["a", "b", "c", "a", "b"]

        lib_list.ls_substract(minuend, ["a", "b"])

        assert minuend == ["c", "a", "b"]


# ---------------------------------------------------------------------------
# split_list_into_junks: Chunking
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestSplitListIntoJunks:
    """split_list_into_junks splits lists into chunks."""

    def test_respects_chunk_size(self) -> None:
        """The list is split into chunks of the specified size."""
        data = list(range(7))

        result = lib_list.split_list_into_junks(data, junk_size=3)

        assert result == [[0, 1, 2], [3, 4, 5], [6]]

    def test_small_list_single_chunk(self) -> None:
        """A small list returns a single chunk."""
        data = [1, 2]

        result = lib_list.split_list_into_junks(data, junk_size=5)

        assert result == [[1, 2]]

    def test_returns_reference_for_remainder(self) -> None:
        """The final chunk is a reference to the original list slice."""
        data: list[Any] = []

        parts = lib_list.split_list_into_junks(data)

        assert parts[0] is data

    def test_zero_size_raises_value_error(self) -> None:
        """A chunk size of zero raises ValueError."""
        with pytest.raises(ValueError):
            lib_list.split_list_into_junks([1, 2, 3], junk_size=0)

    def test_negative_size_raises_value_error(self) -> None:
        """A negative chunk size raises ValueError."""
        with pytest.raises(ValueError):
            lib_list.split_list_into_junks([1, 2, 3], junk_size=-1)

    def test_default_size_returns_whole_list(self) -> None:
        """Default chunk size returns the entire list as one chunk."""
        data = [1, 2, 3]

        result = lib_list.split_list_into_junks(data)

        assert result == [[1, 2, 3]]

    @pytest.mark.parametrize("junk_size", [1, 2, 5])
    def test_various_sizes(self, junk_size: int) -> None:
        """Various chunk sizes produce correct results."""
        data = list(range(5))
        expected: list[list[int]] = []
        for index in range(0, len(data), junk_size):
            expected.append(data[index : index + junk_size])

        assert lib_list.split_list_into_junks(data, junk_size=junk_size) == expected


# ---------------------------------------------------------------------------
# str_in_list_lower_and_de_double: Normalize and Dedupe
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestStrInListLowerAndDeDouble:
    """str_in_list_lower_and_de_double normalizes and deduplicates."""

    def test_lowercases_all(self) -> None:
        """All strings are converted to lowercase."""
        result = lib_list.str_in_list_lower_and_de_double(["A", "B"])

        assert all(s.islower() for s in result)

    def test_deduplicates(self) -> None:
        """Duplicate values (after lowercasing) are removed."""
        result = lib_list.str_in_list_lower_and_de_double(["A", "a", "B"])

        assert len(result) == 2

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.str_in_list_lower_and_de_double([]) == []

    def test_preserves_content(self) -> None:
        """The lowercase content is preserved."""
        result = lib_list.str_in_list_lower_and_de_double(["Hello", "WORLD"])

        assert set(result) == {"hello", "world"}


# ---------------------------------------------------------------------------
# str_in_list_non_case_sensitive: Case-Insensitive Check
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestStrInListNonCaseSensitive:
    """str_in_list_non_case_sensitive performs case-insensitive lookup."""

    def test_detects_match(self) -> None:
        """Case-insensitive matching finds the string."""
        assert lib_list.str_in_list_non_case_sensitive("a", ["A", "b"]) is True

    def test_detects_no_match(self) -> None:
        """Returns False when no case-insensitive match exists."""
        assert lib_list.str_in_list_non_case_sensitive("c", ["A", "b"]) is False

    def test_empty_list_returns_false(self) -> None:
        """An empty list returns False."""
        assert lib_list.str_in_list_non_case_sensitive("a", []) is False

    def test_mixed_case_matched(self) -> None:
        """Mixed case strings are matched correctly."""
        assert lib_list.str_in_list_non_case_sensitive("HeLLo", ["HELLO", "world"]) is True


# ---------------------------------------------------------------------------
# str_in_list_to_lower: Lowercase Conversion
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestStrInListToLower:
    """str_in_list_to_lower lowercases all strings."""

    def test_lowercases_all(self) -> None:
        """All strings are converted to lowercase."""
        result = lib_list.str_in_list_to_lower(["A", "B"])

        assert result == ["a", "b"]

    def test_empty_list_returns_empty(self) -> None:
        """An empty list returns an empty list."""
        assert lib_list.str_in_list_to_lower([]) == []

    def test_preserves_already_lowercase(self) -> None:
        """Already lowercase strings remain unchanged."""
        result = lib_list.str_in_list_to_lower(["abc", "def"])

        assert result == ["abc", "def"]


# ---------------------------------------------------------------------------
# strip_and_add_non_empty_args_to_list: Argument Normalization
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestStripAndAddNonEmptyArgsToList:
    """strip_and_add_non_empty_args_to_list normalizes arguments."""

    def test_strips_whitespace(self) -> None:
        """Whitespace is stripped from arguments."""
        result = lib_list.strip_and_add_non_empty_args_to_list(" a ", "  b  ")

        assert result == ["a", "b"]

    def test_filters_empty_strings(self) -> None:
        """Empty strings are filtered out."""
        result = lib_list.strip_and_add_non_empty_args_to_list("a", "", "b")

        assert result == ["a", "b"]

    def test_filters_none_values(self) -> None:
        """None values are filtered out."""
        result = lib_list.strip_and_add_non_empty_args_to_list("a", None, "b")

        assert result == ["a", "b"]

    def test_no_args_returns_empty(self) -> None:
        """No arguments returns an empty list."""
        assert lib_list.strip_and_add_non_empty_args_to_list() == []

    def test_all_empty_args_returns_empty(self) -> None:
        """All empty or None arguments returns an empty list."""
        result = lib_list.strip_and_add_non_empty_args_to_list("", None, "   ")

        assert result == []

    def test_whitespace_only_filtered(self) -> None:
        """Whitespace-only strings become empty after strip and are filtered."""
        result = lib_list.strip_and_add_non_empty_args_to_list("  ", "a")

        assert result == ["a"]


# ---------------------------------------------------------------------------
# Package Exports
# ---------------------------------------------------------------------------


@pytest.mark.os_agnostic
class TestPackageExports:
    """Package exports match module exports."""

    def test_root_exports_match_module(self) -> None:
        """Package root exports match the lib_list module exports."""
        for name in lib_list.__all__:
            assert getattr(btx_lib_list, name) is getattr(lib_list, name)

    def test_all_exports_are_callable(self) -> None:
        """All exported names are callable functions."""
        for name in lib_list.__all__:
            obj = getattr(lib_list, name)
            assert callable(obj), f"{name} should be callable"
