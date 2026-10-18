"""Tests for exact finite combinatorics, partitions, finite geometry, and Weyl displacement counts."""

import pytest
from src.combinatorics.finite_combinatorics import (
    CombinatoricsBudgetError,
    binomial_exact,
    enumerate_cartesian_words,
    finite_plane_parameters,
    integer_partitions,
    weyl_heisenberg_displacement_count,
)


def test_binomial_and_partitions() -> None:
    assert binomial_exact(6, 3) == 20
    assert binomial_exact(5, 7) == 0
    parts_4 = integer_partitions(4)
    assert parts_4 == [(4,), (3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)]
    assert len(integer_partitions(5)) == 7


def test_cartesian_words_budget_gate() -> None:
    words = enumerate_cartesian_words(2, 3, budget=8)
    assert len(words) == 8
    with pytest.raises(CombinatoricsBudgetError):
        enumerate_cartesian_words(3, 3, budget=20)


def test_finite_plane_and_weyl_counts() -> None:
    p3 = finite_plane_parameters(3)
    assert p3.pg_points == 13
    assert p3.pg_lines == 13
    assert p3.ag_points == 9
    assert p3.ag_lines == 12
    assert p3.parallel_classes == 4
    assert weyl_heisenberg_displacement_count(6) == (36, 35)
