"""Tests for Dual Witness Certification on 3+1 Cauchy Sandwich Triangulations with Lapse & Shift Variations.

Strict invariant verification:
1. 3+1 prism triangulation over spatial Cauchy slice Sigma preserves boundary Sigma_0 U Sigma_1, Euler characteristic, and operator nilpotency (partial^2 = 0, d^2 = 0).
2. Timelike foliation condition: N_v^2 > |N_v|^2 ensures time-track edges are strictly timelike (s^2 < 0).
3. Lapse delta N and shift delta N variations generate exact 1-coboundary gauge shifts delta Omega = d_1 beta in C^2.
4. Pure lapse/shift variations are certified closed: Phi([delta Omega]) = 0, duality gap < 1e-10, dual witness divergence < 1e-10.
5. Exact gauge invariance of the degree-2 L1 quotient norm: Phi([Omega + delta Omega]) == Phi([Omega]).
6. Non-trivial Wheeler-DeWitt constraint violations certified by divergence-free 2-cycle witnesses in Z_2 with zero duality gap (< 1e-10) and complementary slackness.
7. Robustness across foliation thickness Delta t in [0.1, 2.0] and adaptive stellar subdivision.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
import numpy as np
import pytest

from cauchy_sandwich import (
    CauchySandwich4Complex,
    build_canonical_3simplex_sandwich,
)
from degree2_dual_witness import Degree2DualCertifiedL1Solver


class TestCauchySandwichGeometryAndFoliation:
    """Rigorous tests of 3+1 Cauchy sandwich geometry, topology, and foliation conditions."""

    def test_canonical_sandwich_prism_topology(self):
        """Verify simplex counts, Euler characteristic, and boundaries of 3-prism triangulation."""
        sandwich = build_canonical_3simplex_sandwich(dt=1.0, lapse_val=1.0, shift_val=0.0)

        assert sandwich.num_vertices == 8
        assert sandwich.num_four_simplices == 4
        assert sandwich.num_edges == 22
        assert sandwich.num_triangles == 28
        assert sandwich.num_tetrahedra == 17

        assert sandwich.euler_characteristic() == 1

        b_tetras = sandwich.lorentzian_complex.boundary_tetrahedra()
        assert (0, 1, 2, 3) in b_tetras
        assert (4, 5, 6, 7) in b_tetras

    def test_timelike_foliation_condition(self):
        """Verify that N_v^2 > |N_v|^2 yields strictly timelike time-tracks."""
        sandwich_standard = build_canonical_3simplex_sandwich(dt=1.0, lapse_val=1.0, shift_val=0.0)
        assert sandwich_standard.is_timelike_foliation() is True

        s2_04 = sandwich_standard.lorentzian_complex.edge_squared_interval((0, 4))
        assert s2_04 == pytest.approx(-1.0, abs=1e-12)

        sandwich_subluminal = build_canonical_3simplex_sandwich(dt=1.0, lapse_val=1.0, shift_val=0.5)
        assert sandwich_subluminal.is_timelike_foliation() is True
        s2_sub = sandwich_subluminal.lorentzian_complex.edge_squared_interval((0, 4))
        assert s2_sub == pytest.approx(-0.75, abs=1e-12)

        sandwich_super = build_canonical_3simplex_sandwich(dt=1.0, lapse_val=1.0, shift_val=2.0)
        assert sandwich_super.is_timelike_foliation() is False
        s2_super = sandwich_super.lorentzian_complex.edge_squared_interval((0, 4))
        assert s2_super > 0.0

    def test_cauchy_sandwich_operator_nilpotency(self):
        """Verify partial^2 = 0 and d^2 = 0 across dimensions on Cauchy sandwich."""
        sandwich = build_canonical_3simplex_sandwich(dt=0.5, lapse_val=1.2, shift_val=0.1)
        for k in range(1, 5):
            assert sandwich.lorentzian_complex.verify_nilpotency(k) is True


class TestLapseShiftVariationsAndCoboundaryInvariants:
    """Rigorous tests of lapse and shift variations as exact 1-coboundary gauge shifts."""

    def test_pure_lapse_variation_is_exact_coboundary(self):
        """A variation delta N generates delta Omega = d_1 beta in C^2."""
        sandwich = build_canonical_3simplex_sandwich(dt=1.0)
        delta_lapse = {0: 0.2, 1: -0.1, 2: 0.3, 3: 0.0}
        delta_shift = {v: np.zeros(3) for v in range(4)}

        beta, delta_omega = sandwich.apply_lapse_shift_variation(delta_lapse, delta_shift)
        d1 = sandwich.coboundary_matrix(1)

        assert np.allclose(delta_omega, d1 @ beta, atol=1e-14)
        d2 = sandwich.coboundary_matrix(2)
        bianchi_flux = d2 @ delta_omega
        assert np.allclose(bianchi_flux, 0.0, atol=1e-14)

    def test_nonuniform_shift_variation_is_exact_coboundary(self):
        """A spatial shift flow delta N generates delta Omega = d_1 beta in C^2."""
        sandwich = build_canonical_3simplex_sandwich(dt=1.0)
        delta_lapse = {v: 0.0 for v in range(4)}
        delta_shift = {
            0: np.array([0.1, -0.1, 0.0]),
            1: np.array([-0.05, 0.2, 0.1]),
            2: np.array([0.0, 0.0, -0.15]),
            3: np.array([0.05, -0.1, 0.05]),
        }

        beta, delta_omega = sandwich.apply_lapse_shift_variation(delta_lapse, delta_shift)
        d1 = sandwich.coboundary_matrix(1)
        assert np.allclose(delta_omega, d1 @ beta, atol=1e-14)

        d2 = sandwich.coboundary_matrix(2)
        assert np.allclose(d2 @ delta_omega, 0.0, atol=1e-14)


class TestCauchySandwichDualWitnessCertification:
    """Rigorous tests of degree-2 dual L1 solver and certified 2-cycle witnesses on Cauchy sandwich."""

    def test_pure_lapse_shift_variation_exact_closure(self):
        """Pure lapse/shift gauge variations have Phi = 0, zero duality gap, and zero divergence."""
        sandwich = build_canonical_3simplex_sandwich(dt=1.0)
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)

        delta_lapse = {0: 0.15, 1: -0.2, 2: 0.05, 3: 0.1}
        delta_shift = {
            0: np.array([0.05, 0.0, 0.0]),
            1: np.array([0.0, -0.05, 0.0]),
            2: np.array([0.02, 0.02, 0.0]),
            3: np.array([-0.03, 0.01, 0.0]),
        }

        _, delta_omega = sandwich.apply_lapse_shift_variation(delta_lapse, delta_shift)
        d1 = sandwich.coboundary_matrix(1)

        res = solver.solve(delta_omega, d1)
        assert res.is_closed is True
        assert res.primal_obj < 1e-10
        assert res.duality_gap < 1e-10
        assert res.dual_divergence_norm < 1e-10

    def test_gauge_invariance_under_arbitrary_lapse_shift_shifts(self):
        """The L1 quotient norm Phi([Omega + delta_{(N, N)} Omega]) == Phi([Omega])."""
        sandwich = build_canonical_3simplex_sandwich(dt=1.0)
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)
        d1 = sandwich.coboundary_matrix(1)

        omega_base = sandwich.build_sandwich_wdw_constraint_cochain(extrinsic_curvature_pert=1.5)
        base_res = solver.solve(omega_base, d1)
        assert base_res.is_closed is False
        assert base_res.primal_obj > 0.0

        np.random.seed(2026)
        for _ in range(5):
            delta_lapse = {v: float(np.random.randn() * 0.5) for v in range(4)}
            delta_shift = {v: np.random.randn(3) * 0.3 for v in range(4)}

            _, delta_omega = sandwich.apply_lapse_shift_variation(delta_lapse, delta_shift)
            omega_shifted = omega_base + delta_omega

            shifted_res = solver.solve(omega_shifted, d1)
            assert abs(shifted_res.primal_obj - base_res.primal_obj) < 1e-10
            assert abs(shifted_res.dual_obj - base_res.dual_obj) < 1e-10
            assert shifted_res.duality_gap < 1e-10

    def test_non_closable_wdw_violation_certified_dual_witness(self):
        """Verify dual witness certification for genuine Wheeler-DeWitt constraint violations.

        Validates:
        1. Strong duality with duality gap < 1e-10.
        2. Dual witness w* is an exact divergence-free 2-cycle: ||partial_2 w*||_inf < 1e-10.
        3. Dual witness satisfies L_infty bound: ||w*||_inf <= 1.0 + 1e-10.
        4. Subgradient complementary slackness: <w*, r*> == ||r*||_1.
        """
        sandwich = build_canonical_3simplex_sandwich(dt=1.0)
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)
        d1 = sandwich.coboundary_matrix(1)

        omega = sandwich.build_sandwich_wdw_constraint_cochain(extrinsic_curvature_pert=2.8)
        res = solver.solve(omega, d1)

        assert res.is_closed is False
        assert res.primal_obj > 0.0
        assert res.duality_gap < 1e-10
        assert res.dual_divergence_norm < 1e-10
        assert np.max(np.abs(res.dual_witness)) <= 1.0 + 1e-10

        dot_val = float(np.dot(res.dual_witness, res.primal_residual))
        assert abs(dot_val - res.primal_obj) < 1e-10

        for h_idx, r_val in enumerate(res.primal_residual):
            if abs(r_val) > 1e-8:
                assert np.sign(res.dual_witness[h_idx]) == np.sign(r_val)

    def test_foliation_thickness_scaling(self):
        """Verify dual witness certification across foliation intervals Delta t in [0.1, 2.0]."""
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)
        thicknesses = [0.1, 0.5, 1.0, 2.0]

        for dt in thicknesses:
            sandwich = build_canonical_3simplex_sandwich(dt=dt, lapse_val=1.0, shift_val=0.1)
            assert sandwich.is_timelike_foliation() is True
            d1 = sandwich.coboundary_matrix(1)

            omega = sandwich.build_sandwich_wdw_constraint_cochain(extrinsic_curvature_pert=1.0)
            res = solver.solve(omega, d1)

            assert res.duality_gap < 1e-10
            assert res.dual_divergence_norm < 1e-10
            assert np.max(np.abs(res.dual_witness)) <= 1.0 + 1e-10

    def test_sandwich_adaptive_stellar_subdivision(self):
        """Verify that stellar subdivision on a Cauchy sandwich 4-simplex preserves dual witness certification."""
        sandwich = build_canonical_3simplex_sandwich(dt=1.0)
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)

        assert sandwich.num_four_simplices == 4

        new_v, daughters = sandwich.lorentzian_complex.stellar_subdivide(0)
        assert new_v == 8
        assert sandwich.lorentzian_complex.num_four_simplices == 8

        d1_sub = sandwich.lorentzian_complex.coboundary_matrix(1)
        omega_sub = np.zeros(sandwich.lorentzian_complex.num_triangles)
        omega_sub[0] = 2.0

        res_sub = solver.solve(omega_sub, d1_sub)
        assert res_sub.duality_gap < 1e-10
        assert res_sub.dual_divergence_norm < 1e-10
        assert np.max(np.abs(res_sub.dual_witness)) <= 1.0 + 1e-10

    def test_invalid_spatial_slice_raises_error(self):
        """A spatial slice with fewer than 4 vertices raises ValueError."""
        with pytest.raises(ValueError, match="at least 4 vertices"):
            CauchySandwich4Complex(
                spatial_vertices={0: np.zeros(3), 1: np.zeros(3), 2: np.zeros(3)},
                spatial_tetrahedra=[],
            )
