"""Exact H^1 = ker d1 / im d0 (A3). Diagnostic, exact-rational."""

import pytest

from omega_engine.crates.homology_theory.cohomology_h1 import CohomologyH1
from omega_engine.crates.homology_theory.errors import DimensionMismatch, CoboundaryLawViolation


def _triangle():
    d0 = [
        [-1, 1, 0],
        [0, -1, 1],
        [1, 0, -1],
    ]
    d1 = [[1, 1, 1]]
    return d0, d1


def test_filled_triangle_with_face_h1_dimension_is_zero():
    d0, d1 = _triangle()
    coh = CohomologyH1.from_dims(d0, d1)
    r = coh.result()
    assert r.dim_z1 == 2
    assert r.dim_b1 == 2
    assert r.dim_h1 == 0


def test_triangle_no_face_h1_dimension_is_one():
    d0 = [
        [-1, 1, 0],
        [0, -1, 1],
        [1, 0, -1],
    ]
    coh = CohomologyH1(d0, [], num_edges=3, num_vertices=3, num_faces=0)
    r = coh.result()
    assert r.num_edges == 3
    assert r.rank_d1 == 0
    assert r.dim_z1 == 3
    assert r.dim_b1 == 2
    assert r.dim_h1 == 1


def test_tree_h1_dimension_is_zero():
    d0 = [
        [-1, 1, 0],
        [0, -1, 1],
    ]
    coh = CohomologyH1(d0, [], num_edges=2, num_vertices=3, num_faces=0)
    r = coh.result()
    assert r.dim_z1 == 2
    assert r.dim_b1 == 2
    assert r.dim_h1 == 0


def test_membership_exact_vs_closed_nonexact():
    d0 = [
        [-1, 1, 0],
        [0, -1, 1],
        [1, 0, -1],
    ]
    coh = CohomologyH1(d0, [], num_edges=3, num_vertices=3, num_faces=0)
    x_exact = [3, 2, -5]
    assert coh.is_closed(x_exact)
    assert coh.is_exact(x_exact)
    assert coh.class_dimension_contribution(x_exact) == "exact"
    x_cycle = [1, 1, 1]
    assert coh.is_closed(x_cycle)
    assert not coh.is_exact(x_cycle)
    assert coh.class_dimension_contribution(x_cycle) == "closed_nonexact"


def test_refuse_shape_mismatch():
    d0 = [[-1, 1, 0], [0, -1, 1]]
    d1 = [[1, 1, 1]]
    with pytest.raises(DimensionMismatch):
        CohomologyH1.from_dims(d0, d1)


def test_refuse_d1d0_nonzero():
    d0 = [
        [-1, 1, 0],
        [0, -1, 1],
        [1, 0, -1],
    ]
    d1_bad = [[1, 0, 0]]
    with pytest.raises(CoboundaryLawViolation):
        CohomologyH1.from_dims(d0, d1_bad)


def test_h1_dimension_helper_exact_fraction_input():
    from fractions import Fraction

    d0 = [
        [Fraction(-1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(-1), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(-1)],
    ]
    coh = CohomologyH1(d0, [], num_edges=3, num_vertices=3, num_faces=0)
    assert coh.dim_h1() == 1


