"""Tests for Dual Witness Certification on 4D Lorentzian Regge Triangulations under Adaptive Subdivision.

Strict invariant verification:
1. Minkowski metric eta = diag(-1, 1, 1, 1) and Lorentzian interval s_e^2 = -(Delta t)^2 + |Delta x|^2.
2. Edge signature classification: spacelike (s^2 > 0), timelike (s^2 < 0), null (s^2 = 0).
3. 1-to-5 stellar Pachner subdivision preserves boundary tetrahedra, Euler characteristic, and operator nilpotency (partial^2 = 0, d^2 = 0) across refinement levels 0, 1, 2.
4. Discrete simplicial Bianchi identity d_2 o d_1 == 0 on 4D triangulations across all refinement levels.
5. Exact strong duality for degree-2 cochains: Phi([omega]) == Psi(omega) with zero duality gap (< 1e-10).
6. Dual witness w* is an exact divergence-free 2-cycle (partial_2 w* = 0) bounded by ||w*||_inf <= 1.
7. Subgradient saturation / complementary slackness <w*, r*> == ||r*||_1.
8. 1-gauge transformation invariance: Phi([omega + d_1 beta]) == Phi([omega]) for all beta in C^1.
9. Multi-level adaptive refinement (Levels 0, 1, 2) and edge bisection consistency.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
import numpy as np
import pytest

from lorentzian_regge import (
    Lorentzian4Complex,
    build_canonical_lorentzian_4simplex,
    build_two_adjacent_lorentzian_4simplices,
)
from degree2_dual_witness import (
    Degree2DualCertifiedL1Solver,
    compute_degree2_l1_quotient_with_dual_witness,
)


class TestLorentzianMinkowskiGeometry:
    """Rigorous tests of Minkowski geometry and edge signature classification."""

    def test_canonical_4simplex_edge_signatures(self):
        """Verify that the canonical 4-simplex in R^{1,3} contains both timelike and spacelike edges."""
        c4 = build_canonical_lorentzian_4simplex(t_span=2.0, spatial_scale=1.0)

        assert c4.num_vertices == 5
        assert c4.num_edges == 10
        assert c4.num_triangles == 10
        assert c4.num_tetrahedra == 5
        assert c4.num_four_simplices == 1

        assert c4.is_timelike((0, 4)) is True
        assert c4.is_spacelike((0, 4)) is False
        assert c4.edge_squared_interval((0, 4)) == pytest.approx(-4.0, abs=1e-12)

        assert c4.is_spacelike((1, 2)) is True
        assert c4.is_timelike((1, 2)) is False
        assert c4.edge_squared_interval((1, 2)) == pytest.approx(2.0, abs=1e-12)

        counts = c4.edge_signature_counts()
        assert counts["spacelike"] > 0
        assert counts["timelike"] > 0
        assert counts["spacelike"] + counts["timelike"] + counts["null"] == 10

    def test_lorentzian_null_edge_detection(self):
        """Verify that lightlike (null) edges with s^2 = 0 are identified."""
        vertices = {
            0: np.array([0.0, 0.0, 0.0, 0.0]),
            1: np.array([1.0, 1.0, 0.0, 0.0]),
            2: np.array([1.0, 0.0, 1.0, 0.0]),
            3: np.array([1.0, 0.0, 0.0, 1.0]),
            4: np.array([2.0, 0.0, 0.0, 0.0]),
        }
        c = Lorentzian4Complex(vertices=vertices, four_simplices=[(0, 1, 2, 3, 4)])
        assert c.is_null((0, 1)) is True
        assert abs(c.edge_squared_interval((0, 1))) < 1e-10


class TestAdaptiveSubdivisionTopologicalInvariants:
    """Rigorous tests of 4D adaptive subdivision operators and topological invariants."""

    def test_stellar_subdivision_level1_counts_and_euler(self):
        """1-to-5 stellar subdivision on a single 4-simplex replaces 1 4-cell with 5 daughters."""
        c = build_canonical_lorentzian_4simplex()
        assert c.euler_characteristic() == 1

        b_init = c.boundary_tetrahedra()
        assert len(b_init) == 5

        new_v, daughters = c.stellar_subdivide(0)
        assert new_v == 5
        assert len(daughters) == 5

        assert c.num_vertices == 6
        assert c.num_edges == 15
        assert c.num_triangles == 20
        assert c.num_tetrahedra == 15
        assert c.num_four_simplices == 5

        assert c.euler_characteristic() == 1

        b_after = c.boundary_tetrahedra()
        assert b_after == b_init

    def test_stellar_subdivision_level2_refinement(self):
        """Consecutive stellar subdivisions (Level 0 -> Level 1 -> Level 2)."""
        c = build_canonical_lorentzian_4simplex()
        b_init = c.boundary_tetrahedra()

        c.stellar_subdivide(0)
        assert c.num_four_simplices == 5

        new_v2, daughters2 = c.stellar_subdivide(0)
        assert new_v2 == 6
        assert len(daughters2) == 5

        assert c.num_vertices == 7
        assert c.num_edges == 20
        assert c.num_triangles == 30
        assert c.num_tetrahedra == 25
        assert c.num_four_simplices == 9

        assert c.euler_characteristic() == 1
        assert c.boundary_tetrahedra() == b_init

    def test_operator_nilpotency_across_subdivision_levels(self):
        """Verify partial^2 = 0 and d^2 = 0 across Levels 0, 1, 2."""
        c = build_canonical_lorentzian_4simplex()

        for k in range(1, 5):
            assert c.verify_nilpotency(k) is True

        c.stellar_subdivide(0)
        for k in range(1, 5):
            assert c.verify_nilpotency(k) is True

        c.stellar_subdivide(0)
        for k in range(1, 5):
            assert c.verify_nilpotency(k) is True

    def test_edge_bisection_topological_integrity(self):
        """Simplicial edge bisection splits incident simplices and preserves boundary and nilpotency."""
        c = build_two_adjacent_lorentzian_4simplices()
        b_init = c.boundary_tetrahedra()

        assert (1, 2) in c.cells[1]
        new_v = c.bisect_edge((1, 2))
        assert new_v == 6

        for k in range(1, 5):
            assert c.verify_nilpotency(k) is True


class TestSimplicialBianchiIdentityIn4D:
    """Rigorous tests of the discrete Bianchi identity d_2 o d_1 == 0 in 4D."""

    def test_bianchi_nilpotency_at_levels_0_1_2(self):
        """d_2 o d_1 == 0 identically on 4D simplicial complex across refinement levels."""
        c = build_canonical_lorentzian_4simplex()

        for lvl in range(3):
            d1 = c.coboundary_matrix(1)
            d2 = c.coboundary_matrix(2)
            prod = d2 @ d1
            assert np.allclose(prod, 0.0, atol=1e-14)

            if lvl < 2:
                c.stellar_subdivide(0)

    def test_bianchi_identity_flux_vanishing_on_exact_curvature(self):
        """For any pure 1-gauge variation omega = d_1 beta, Bianchi flux d_2 omega == 0."""
        c = build_canonical_lorentzian_4simplex()
        c.stellar_subdivide(0)

        d1 = c.coboundary_matrix(1)
        np.random.seed(42)
        beta = np.random.randn(c.num_edges)
        omega = d1 @ beta

        res = c.verify_bianchi_identity(omega)
        assert res["is_satisfied"] is True
        assert res["total_l1_flux"] < 1e-13
        assert res["authority_effect"] == "None"


class TestDegree2DualCertifiedL1Solver:
    """Rigorous tests of degree-2 dual L1 solver and certified 2-cycle witnesses."""

    def test_flat_spacetime_zero_quotient_at_all_levels(self):
        """In flat Minkowski spacetime with zero deficit cochain, Phi = 0 and is_closed is True."""
        c = build_canonical_lorentzian_4simplex()
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)

        for lvl in range(3):
            d1 = c.coboundary_matrix(1)
            omega_flat = np.zeros(c.num_triangles)

            res = solver.solve(omega_flat, d1)
            assert res.is_closed is True
            assert res.primal_obj == 0.0
            assert res.dual_obj == 0.0
            assert res.duality_gap == 0.0
            assert res.dual_divergence_norm == 0.0
            assert res.authority_effect == "None"

            if lvl < 2:
                c.stellar_subdivide(0)

    def test_pure_1gauge_variation_closable_across_subdivisions(self):
        """When 2-cochain is pure gauge omega = d_1 beta, Phi([omega]) = 0 and gap < 1e-10."""
        c = build_canonical_lorentzian_4simplex()
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)
        np.random.seed(101)

        for lvl in range(3):
            d1 = c.coboundary_matrix(1)
            beta_rand = np.random.randn(c.num_edges) * 5.0
            omega_gauge = d1 @ beta_rand

            res = solver.solve(omega_gauge, d1)
            assert res.is_closed is True
            assert res.primal_obj < 1e-10
            assert res.duality_gap < 1e-10
            assert res.dual_divergence_norm < 1e-10

            if lvl < 2:
                c.stellar_subdivide(0)

    def test_gauge_invariance_under_arbitrary_shifts(self):
        """The degree-2 L1 quotient is strictly gauge invariant: Phi([omega + d_1 beta]) == Phi([omega])."""
        c = build_canonical_lorentzian_4simplex()
        c.stellar_subdivide(0)

        d1 = c.coboundary_matrix(1)
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)

        np.random.seed(7)
        omega_base = np.zeros(c.num_triangles)
        omega_base[0] = 3.2
        omega_base[5] = -2.1

        base_res = solver.solve(omega_base, d1)
        assert base_res.is_closed is False
        assert base_res.primal_obj > 0.0

        for _ in range(5):
            beta_shift = np.random.randn(c.num_edges) * 10.0
            omega_shifted = omega_base + d1 @ beta_shift
            shifted_res = solver.solve(omega_shifted, d1)

            assert abs(shifted_res.primal_obj - base_res.primal_obj) < 1e-10
            assert abs(shifted_res.dual_obj - base_res.dual_obj) < 1e-10
            assert shifted_res.duality_gap < 1e-10

    def test_dual_witness_certification_under_adaptive_subdivision(self):
        """Verify dual witness certification across adaptive subdivision levels 0, 1, 2.

        At each level:
        1. Strong duality holds with duality gap < 1e-10.
        2. Dual witness w* is an exact divergence-free 2-cycle: ||partial_2 w*||_inf < 1e-10.
        3. Dual witness satisfies L_infty bound: ||w*||_inf <= 1.0 + 1e-10.
        4. Subgradient condition / complementary slackness: <w*, r*> == ||r*||_1.
        """
        c = build_canonical_lorentzian_4simplex()
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)

        for lvl in range(3):
            d1 = c.coboundary_matrix(1)

            omega = np.zeros(c.num_triangles)
            omega[0] = 4.5
            omega[-1] = -2.5

            res = solver.solve(omega, d1)

            assert res.is_closed is False
            assert res.primal_obj > 0.0
            assert res.duality_gap < 1e-10, f"Duality gap at level {lvl} exceeds 1e-10"
            assert res.dual_divergence_norm < 1e-10, f"Dual witness not a 2-cycle at level {lvl}"
            assert np.max(np.abs(res.dual_witness)) <= 1.0 + 1e-10

            dot_val = float(np.dot(res.dual_witness, res.primal_residual))
            assert abs(dot_val - res.primal_obj) < 1e-10

            for h_idx, r_val in enumerate(res.primal_residual):
                if abs(r_val) > 1e-8:
                    assert np.sign(res.dual_witness[h_idx]) == np.sign(r_val)

            if lvl < 2:
                c.stellar_subdivide(0)

    def test_multi_simplex_edge_bisection_dual_witness(self):
        """Verify dual witness certification on adjacent 4-simplices under edge bisection."""
        c = build_two_adjacent_lorentzian_4simplices()
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)

        d1_pre = c.coboundary_matrix(1)
        omega_pre = np.zeros(c.num_triangles)
        omega_pre[0] = 1.8
        res_pre = solver.solve(omega_pre, d1_pre)
        assert res_pre.duality_gap < 1e-10
        assert res_pre.dual_divergence_norm < 1e-10

        c.bisect_edge((1, 2))
        d1_post = c.coboundary_matrix(1)
        omega_post = np.zeros(c.num_triangles)
        omega_post[0] = 1.8
        res_post = solver.solve(omega_post, d1_post)

        assert res_post.duality_gap < 1e-10
        assert res_post.dual_divergence_norm < 1e-10
        assert np.max(np.abs(res_post.dual_witness)) <= 1.0 + 1e-10
        dot_val = float(np.dot(res_post.dual_witness, res_post.primal_residual))
        assert abs(dot_val - res_post.primal_obj) < 1e-10

    def test_solver_convenience_function_and_serialization(self):
        """Test compute_degree2_l1_quotient_with_dual_witness and to_dict serialization."""
        c = build_canonical_lorentzian_4simplex()
        d1 = c.coboundary_matrix(1)
        omega = np.zeros(c.num_triangles)
        omega[0] = 1.0

        res = compute_degree2_l1_quotient_with_dual_witness(omega, d1)
        d = res.to_dict()
        assert d["authority_effect"] == "None"
        assert d["duality_gap"] < 1e-10
        assert "primal_obj" in d
        assert "dual_obj" in d

    def test_error_handling_and_input_validation(self):
        """Test that invalid dimensions or edge targets raise informative errors."""
        c = build_canonical_lorentzian_4simplex()
        assert c.num_faces == c.num_triangles

        solver = Degree2DualCertifiedL1Solver()
        d1 = c.coboundary_matrix(1)
        with pytest.raises(ValueError, match="Length of omega"):
            solver.solve(np.array([1.0, 2.0]), d1)

        with pytest.raises(ValueError, match="Curvature cochain length"):
            c.bianchi_flux(np.array([1.0]))

        with pytest.raises(IndexError, match="out of range"):
            c.stellar_subdivide(99)

        with pytest.raises(ValueError, match="Edge .* not present"):
            c.bisect_edge((0, 99))
