"""Automated test validating simplex pivot scaling on dense complete graphs Kn (n >= 8).

# Executable finite evidence; AuthorityEffect: None.
"""

from fractions import Fraction
import pytest

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import (
    DEFAULT_PIVOT_BUDGET,
    d0_matrix,
    solve_standard_lp,
    verify_standard_lp,
)
from witnessed_difference.outcomes import Accepted


@pytest.mark.parametrize("n", [8, 9, 10])
def test_kn_simplex_pivot_scaling_within_budget(n: int):
    """Verify that dense complete graphs Kn execute far below the 10,000 pivot budget limit."""
    vertices = tuple(f"v{i}" for i in range(n))
    edges = tuple((f"v{i}", f"v{j}") for i in range(n) for j in range(i + 1, n))
    comp = FiniteComplex(vertices, edges)
    edge_pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]

    # Frustrated spin configuration
    cochain = [
        Fraction(1) if (i * 3 + j * 7) % 5 >= 2 else Fraction(-1)
        for i, j in edge_pairs
    ]

    d = d0_matrix(comp)
    m = len(d)
    width = len(comp.vertices)
    w = (Fraction(1),) * m

    rows = [
        list(row) + [-entry for entry in row] + [Fraction(int(i == k)) for k in range(m)]
        + [-Fraction(int(i == k)) for k in range(m)]
        for i, row in enumerate(d)
    ]
    costs = [Fraction(0)] * (2 * width) + list(w) + list(w)

    solved = solve_standard_lp(costs, rows, cochain, max_pivots=DEFAULT_PIVOT_BUDGET)
    assert isinstance(solved, Accepted)
    sol = solved.value

    # Verify primal and dual optimality
    assert verify_standard_lp(costs, rows, cochain, sol)

    # Budget assertion: pivots must be strictly less than 10% of DEFAULT_PIVOT_BUDGET (1,000)
    assert sol.pivots < 1000
    assert sol.pivots < DEFAULT_PIVOT_BUDGET

    # Empirical linear factor: pivots / m must remain bounded (empirical ratio < 5.0)
    ratio = sol.pivots / m
    assert ratio < 5.0
