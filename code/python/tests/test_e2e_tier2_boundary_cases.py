"""Tier 2 exact boundary cases: constant sections, cocycles, and grid error."""
from fractions import Fraction

from src.qm.campaigns.continuum_lift import cyclotomic_density_approximation
from src.qm.campaigns.rungs import exact_cocycle_defect, triangle_boundary_rank
from src.qm.domain.primitive_difference import (
    PrimitiveDifference,
    evaluate_mu1_tied_classes,
)


def test_tier2_constant_section_has_zero_defect():
    section = {"v0": Fraction(42), "v1": Fraction(42), "v2": Fraction(42)}
    edges = [("v0", "v1"), ("v1", "v2"), ("v2", "v0")]
    assert PrimitiveDifference.phi_raw(section, edges) == Fraction(0)
    assert PrimitiveDifference.support(section, edges) == 0


def test_tier2_float_constant_section_matches_rational_zero():
    section = {"v0": 42.0, "v1": 42.0, "v2": 42.0}
    edges = [("v0", "v1"), ("v1", "v2"), ("v2", "v0")]
    assert PrimitiveDifference.phi_raw(section, edges) == Fraction(0)


def test_tier2_cocycle_defect_and_triangle_rank():
    assert exact_cocycle_defect(Fraction(1, 2), Fraction(2, 3), Fraction(5, 7)) == 0
    assert triangle_boundary_rank() == 2


def test_tier2_separation_classes_are_enumerated():
    assert evaluate_mu1_tied_classes(2, max_arity=1) == 1
    assert evaluate_mu1_tied_classes(2, max_arity=2) == 3
    assert evaluate_mu1_tied_classes(5, max_arity=2) == 5


def test_tier2_gaussian_grid_squared_error_is_inside_the_bound():
    report = cyclotomic_density_approximation(complex(0, 0), grid_resolution=7)
    assert report["error_sq"] <= report["bound_sq"]
    assert isinstance(report["error_sq"], Fraction)
