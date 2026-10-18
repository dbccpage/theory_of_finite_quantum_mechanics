"""Tier 3 exact pairings: interference against a rational channel and a walk."""
from fractions import Fraction

from src.qm.campaigns.finite_qm_engine import exact_ladder_cross_term
from src.qm.campaigns.interference import theorem_a1_separation
from src.qm.campaigns.quantum_correlation import rational_correlation_defect
from src.qm.campaigns.quantum_walk import cycle_return


def test_tier3_interference_separates_equal_diagonals():
    report = theorem_a1_separation()
    assert report["diagonal_data_identical"] is True
    assert report["separation_holds"] is True
    assert report["cross_a"] == Fraction(2)
    assert report["cross_b"] == Fraction(-2)


def test_tier3_correlation_defect_pairs_with_the_walk_return():
    assert rational_correlation_defect() == Fraction(1)
    assert cycle_return() == Fraction(1, 2)


def test_tier3_ladder_cross_term_is_the_destructive_value():
    assert exact_ladder_cross_term() == Fraction(-2)
