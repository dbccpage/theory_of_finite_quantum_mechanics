"""
Unit tests for DDC Operation R (Residual Projection).
AuthorityEffect: None.
"""

from fractions import Fraction

import pytest
from residual_projection import (
    ResidualProjector,
    XiTieBreakCertificate,
    evaluate_xi_tie_break,
)


def test_empty_cycle_edges_refused():
    """Empty cycle has no mean circulation; constructor must fail closed."""
    with pytest.raises(ValueError, match="non-empty"):
        ResidualProjector([])


def test_pure_harmonic_defect():
    """Defect is purely harmonic (uniform circulation around cycle)."""
    cycle = [("A", "B"), ("B", "C"), ("C", "A")]
    projector = ResidualProjector(cycle)

    defect = {("A", "B"): Fraction(1), ("B", "C"): Fraction(1), ("C", "A"): Fraction(1)}
    receipt = projector.project(defect)

    assert receipt.status == "RESIDUAL_RETAINED"
    assert receipt.residual_norm == Fraction(3)
    assert receipt.exact_norm == Fraction(0)
    for e in cycle:
        assert receipt.residual_component[e] == Fraction(1)
        assert receipt.exact_component[e] == Fraction(0)


def test_mixed_harmonic_and_exact_defect():
    """Defect has both exact variation and harmonic circulation."""
    cycle = [("A", "B"), ("B", "C"), ("C", "A")]
    projector = ResidualProjector(cycle)

    # Defect: 3, 0, 0 => sum = 3, mean = 1
    defect = {("A", "B"): Fraction(3), ("B", "C"): Fraction(0), ("C", "A"): Fraction(0)}
    receipt = projector.project(defect)

    assert receipt.status == "RESIDUAL_RETAINED"
    # harmonic part is 1 on each edge
    for e in cycle:
        assert receipt.residual_component[e] == Fraction(1)
    # exact part: 3-1 = 2, 0-1 = -1, 0-1 = -1 (sum = 0, exact!)
    assert receipt.exact_component[("A", "B")] == Fraction(2)
    assert receipt.exact_component[("B", "C")] == Fraction(-1)
    assert receipt.exact_component[("C", "A")] == Fraction(-1)
    # Conservation of defect: exact + residual == original
    for e in cycle:
        assert receipt.exact_component[e] + receipt.residual_component[e] == defect[e]


def test_pure_exact_defect_zero_residual():
    """Defect has zero total circulation around cycle."""
    cycle = [("A", "B"), ("B", "C"), ("C", "A")]
    projector = ResidualProjector(cycle)

    defect = {("A", "B"): Fraction(2), ("B", "C"): Fraction(-1), ("C", "A"): Fraction(-1)}
    receipt = projector.project(defect)

    assert receipt.status == "EXACT_TENSION_ONLY"
    assert receipt.residual_norm == Fraction(0)
    for e in cycle:
        assert receipt.residual_component[e] == Fraction(0)
        assert receipt.exact_component[e] == defect[e]


def test_xi_tie_break_success_and_equality():
    """Verify Xi tie-break works when primary diagnostics (Phi_1, Gamma_2) are strictly equal."""
    # Case 1: candidate_b has lower Xi -> candidate_b wins
    cert_b = evaluate_xi_tie_break(
        candidate_a="cand_A",
        phi1_a=Fraction(2, 3),
        gamma2_a=Fraction(1),
        xi_a=Fraction(5),
        candidate_b="cand_B",
        phi1_b=Fraction(2, 3),
        gamma2_b=Fraction(1),
        xi_b=Fraction(3),
    )
    assert isinstance(cert_b, XiTieBreakCertificate)
    assert cert_b.precondition.is_satisfied() is True
    assert cert_b.tie_broken is True
    assert cert_b.winner == "cand_B"

    # Case 2: candidate_a has lower Xi -> candidate_a wins
    cert_a = evaluate_xi_tie_break(
        candidate_a="cand_A",
        phi1_a=Fraction(2, 3),
        gamma2_a=Fraction(1),
        xi_a=Fraction(2),
        candidate_b="cand_B",
        phi1_b=Fraction(2, 3),
        gamma2_b=Fraction(1),
        xi_b=Fraction(4),
    )
    assert cert_a.tie_broken is True
    assert cert_a.winner == "cand_A"

    # Case 3: Xi is equal -> tie remains unbroken
    cert_eq = evaluate_xi_tie_break(
        candidate_a="cand_A",
        phi1_a=Fraction(1),
        gamma2_a=Fraction(0),
        xi_a=Fraction(7),
        candidate_b="cand_B",
        phi1_b=Fraction(1),
        gamma2_b=Fraction(0),
        xi_b=Fraction(7),
    )
    assert cert_eq.tie_broken is False
    assert cert_eq.winner is None


def test_xi_tie_break_precondition_rejection():
    """Verify fail-closed rejection when primary diagnostics differ (Xi cannot override primary defect)."""
    # Phi_1 differs
    with pytest.raises(ValueError, match="XI_TIE_PRECONDITION_FAILED"):
        evaluate_xi_tie_break(
            candidate_a="cand_A",
            phi1_a=Fraction(2),
            gamma2_a=Fraction(1),
            xi_a=Fraction(1),
            candidate_b="cand_B",
            phi1_b=Fraction(3),
            gamma2_b=Fraction(1),
            xi_b=Fraction(0),  # even if Xi is lower, cannot override Phi_1 worsening
        )

    # Gamma_2 differs
    with pytest.raises(ValueError, match="XI_TIE_PRECONDITION_FAILED"):
        evaluate_xi_tie_break(
            candidate_a="cand_A",
            phi1_a=Fraction(1),
            gamma2_a=Fraction(0),
            xi_a=Fraction(1),
            candidate_b="cand_B",
            phi1_b=Fraction(1),
            gamma2_b=Fraction(1),
            xi_b=Fraction(0),
        )

