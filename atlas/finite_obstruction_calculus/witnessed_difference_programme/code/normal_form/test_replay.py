"""Independent SQLite control and negative inputs for the retained normal form."""
import pytest

from .replay import replay


def test_original_source_set_is_recovered_including_empty_relation():
    rows = (("a", "b", "c"), ("a", "b", "d"), ("x", "y", "c"))
    assert replay(rows)["rows"] == tuple(sorted(rows))
    assert replay(())["rows"] == ()


def test_duplicate_rows_and_false_dependency_are_refused():
    with pytest.raises(ValueError, match="duplicate"):
        replay((("a", "b", "c"), ("a", "b", "c")))
    with pytest.raises(ValueError, match="dependency"):
        replay((("a", "b", "c"), ("a", "x", "d")))
