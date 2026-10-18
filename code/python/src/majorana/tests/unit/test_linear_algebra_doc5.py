"""Regression tests for omega_linear_algebra fixes (py_updates_5)."""

from omega_engine.crates.linear_algebra_theory.basic_matrix import BasicMatrix


def test_try_from_fn_result_populates_data():
    """try_from_fn_result must build data via list.append, not list.push.

    Previously this called data.push(...) which raises AttributeError on a
    Python list. The fix uses data.append(...). Assert the matrix is built
    with the expected shape and contents (no AttributeError).
    """
    m = BasicMatrix.try_from_fn_result(2, 3, lambda r, c: r * 10 + c)

    assert m.shape() == (2, 3)
    assert m.as_slice() == [0, 1, 2, 10, 11, 12]
    assert m.get(1, 2) == 12


