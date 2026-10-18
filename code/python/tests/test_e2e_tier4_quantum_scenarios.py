"""Tier 4 exact scenarios: prices, towers, frames, and the trace obstruction."""
from fractions import Fraction

from src.qm.campaigns.continuum import trace_obstruction
from src.qm.campaigns.continuum_lift import wintner_wielandt_trace_obstruction
from src.qm.campaigns.mub_reports import overlap_gap
from src.qm.causal_prices import cycle_price_defect
from src.qm.tower_walk import tower_degree_product
from src.linear_algebra.smith_form import smith_normal_form
from src.linear_algebra.matrix import ExactMatrix


def test_tier4_price_cycle_and_tower_degree():
    assert cycle_price_defect() == Fraction(0)
    assert tower_degree_product() == 8


def test_tier4_trace_obstruction_is_the_dimension():
    assert trace_obstruction() == Fraction(4)
    report = wintner_wielandt_trace_obstruction(4)
    assert report["trace_commutator"] == 0
    assert report["obstruction_holds"] is True
    assert report["trace_discrepancy"] == Fraction(4)


def test_tier4_mub_gap_and_smith_identity():
    assert overlap_gap() == Fraction(1, 2) - Fraction(16, 25)
    witness = ExactMatrix.from_rows([[2, 4], [2, 6]])
    diagonal, left, right = smith_normal_form(witness)
    assert left * witness * right == diagonal
    assert diagonal.get(0, 0) + diagonal.get(1, 1) == Fraction(4)
