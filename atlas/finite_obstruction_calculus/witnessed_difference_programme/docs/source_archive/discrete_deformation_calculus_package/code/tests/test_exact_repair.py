"""
Unit tests for DDC Operation E (Exact Repair).
AuthorityEffect: None.
"""

from fractions import Fraction

import pytest
from exact_repair import ExactRepairSolver


def test_empty_vertex_set_refused():
    """Exact repair has no gauge vertex on an empty complex."""
    with pytest.raises(ValueError, match="non-empty"):
        ExactRepairSolver([], [])


def test_exact_repair_tree_path():
    """Test exact repair along a path graph (curl identically zero)."""
    vertices = ["A", "B", "C"]
    edges = [("A", "B"), ("B", "C")]
    solver = ExactRepairSolver(vertices, edges)

    # Defect: A->B is 2/3, B->C is 5/6
    defect = {
        ("A", "B"): Fraction(2, 3),
        ("B", "C"): Fraction(5, 6),
    }

    receipt = solver.solve(defect, gauge_vertex="A")
    assert receipt.success is True
    assert receipt.residual_norm == Fraction(0)
    assert receipt.potential["A"] == Fraction(0)
    assert receipt.potential["B"] == Fraction(2, 3)
    assert receipt.potential["C"] == Fraction(2, 3) + Fraction(5, 6)


def test_exact_repair_cycle_zero_curl():
    """Test exact repair on a cycle with zero total circulation."""
    vertices = ["A", "B", "C"]
    edges = [("A", "B"), ("B", "C"), ("C", "A")]
    solver = ExactRepairSolver(vertices, edges)

    # Defect: 1 + 2 - 3 = 0
    defect = {
        ("A", "B"): Fraction(1),
        ("B", "C"): Fraction(2),
        ("C", "A"): Fraction(-3),
    }

    receipt = solver.solve(defect, gauge_vertex="A")
    assert receipt.success is True
    assert receipt.residual_norm == Fraction(0)
    assert receipt.error is None


def test_exact_repair_refusal_non_zero_curl():
    """Test refusal on non-zero curl cycle (harmonic / face defect)."""
    vertices = ["A", "B", "C"]
    edges = [("A", "B"), ("B", "C"), ("C", "A")]
    solver = ExactRepairSolver(vertices, edges)

    # Non-zero circulation: 1 + 1 + 1 = 3 != 0
    defect = {
        ("A", "B"): Fraction(1),
        ("B", "C"): Fraction(1),
        ("C", "A"): Fraction(1),
    }

    receipt = solver.solve(defect, gauge_vertex="A")
    assert receipt.success is False
    assert receipt.error == "REFUSED_NON_ZERO_CURL"
    assert receipt.residual_norm == Fraction(3)
