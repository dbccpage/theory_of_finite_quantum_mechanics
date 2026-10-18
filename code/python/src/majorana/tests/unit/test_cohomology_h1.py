"""Exact H^1 = ker d1 / im d0 (A3). Diagnostic, exact-rational."""

import pytest

from omega_engine.crates.homology_theory.cohomology_h1 import CohomologyH1
from omega_engine.crates.homology_theory.errors import DimensionMismatch, CoboundaryLawViolation


def _triangle():
    # 3 vertices, 3 edges (0->1, 1->2, 2->0), one face (the cycle).
    # d0 : (E=3, V=3) incidence (tail -1, head +1).
    d0 = [
        [-1, 1, 0],  # edge 0: 0->1
        [0, -1, 1],  # edge 1: 1->2
        [1, 0, -1],  # edge 2: 2->0
    ]
    # d1 : (F=1, E=3) the cycle 0+1+2.
    d1 = [[1, 1, 1]]
    return d0, d1


def test_filled_triangle_with_face_h1_dimension_is_zero():
    # Triangle WITH its 2-cell (the face fills the single cycle), so H^1 = 0:
    # the cycle is now a coboundary-complement killed by the face in ker d1.
    d0, d1 = _triangle()
    coh = CohomologyH1.from_dims(d0, d1)
    r = coh.result()
    # rank d1 = 1, so Z^1 = ker d1 has dim 3-1 = 2; im d0 dim = 2 => H^1 = 0.
    assert r.dim_z1 == 2
    assert r.dim_b1 == 2
    assert r.dim_h1 == 0


def test_triangle_no_face_h1_dimension_is_one():
    # Triangle graph with NO 2-cell: d1 is the empty (0 faces) map => ker d1 = all of C^1.
    d0 = [
        [-1, 1, 0],
        [0, -1, 1],
        [1, 0, -1],
    ]
    # from_dims needs to infer (F=0, E=3); supply an explicit zero-row matrix.
    coh = CohomologyH1(d0, [], num_edges=3, num_vertices=3, num_faces=0)
    r = coh.result()
    assert r.num_edges == 3
    assert r.rank_d1 == 0
    assert r.dim_z1 == 3  # everything is closed (no faces)
    assert r.dim_b1 == 2  # tree rank of incidence
    assert r.dim_h1 == 1  # one independent cycle survives


def test_tree_h1_dimension_is_zero():
    # Path 0->1->2 (a tree): 3 vertices, 2 edges, no cycles.
    d0 = [
        [-1, 1, 0],  # 0->1
        [0, -1, 1],  # 1->2
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
    # x = d0 alpha for alpha = [0,3,5]: edge0=3, edge1=2, edge2=-5 -> exact.
    x_exact = [3, 2, -5]
    assert coh.is_closed(x_exact)
    assert coh.is_exact(x_exact)
    assert coh.class_dimension_contribution(x_exact) == "exact"
    # x = [1,1,1] the cycle: closed (no faces) but NOT a coboundary.
    x_cycle = [1, 1, 1]
    assert coh.is_closed(x_cycle)
    assert not coh.is_exact(x_cycle)
    assert coh.class_dimension_contribution(x_cycle) == "closed_nonexact"


def test_refuse_shape_mismatch():
    d0 = [[-1, 1, 0], [0, -1, 1]]  # (E=2, V=3)
    d1 = [[1, 1, 1]]  # (F=1, E=3) -- E mismatch (2 vs 3)
    with pytest.raises(DimensionMismatch):
        CohomologyH1.from_dims(d0, d1)


def test_refuse_d1d0_nonzero():
    # d1 d0 != 0 : pick d1 that does not annihilate im d0.
    d0 = [
        [-1, 1, 0],
        [0, -1, 1],
        [1, 0, -1],
    ]
    d1_bad = [[1, 0, 0]]  # picks out edge 0 only; d1 d0 = row [-1,1,0] != 0
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


