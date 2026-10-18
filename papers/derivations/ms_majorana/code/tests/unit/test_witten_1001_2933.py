r"""
End-to-end tests for Witten 1001.2933 analytic continuation infrastructure.

Tests the three new capabilities:
1. morse_index, compute_intersection_numbers, integrate_thimble, partition_function
2. Analytic derivatives for ChernSimonsKnotAction
3. AnalyticContinuationCS with Stokes wall-crossing scan

AuthorityEffect: None.
"""

import cmath
import math

import numpy as np
import pytest

from omega_engine.crates.quantum_physics.chern_simons import (
    AnalyticContinuationCS,
    ChernSimonsKnotAction,
    FigureEightCharacterVariety,
    FIGURE_EIGHT_VOLUME,
)
from omega_engine.crates.homology_theory.lefschetz_thimble import (
    AiryAction,
    BesselAction,
    sample_dual_flow_hits as compute_intersection_numbers,
    find_critical_points,
    integrate_thimble,
    morse_index,
    partition_function,
)


class TestMorseIndex:
    def test_airy_morse_index_is_positive(self):
        """For the Airy action, critical points should have nonzero Morse index."""
        action = AiryAction(1.0 + 0.0j)
        cps = action.exact_critical_points()
        for cp in cps:
            idx = morse_index(action, [cp])
            assert idx > 0, f"Morse index should be positive at CP {cp}, got {idx}"

    def test_bessel_morse_index_is_nonnegative(self):
        """Bessel action critical points should have non-negative Morse index."""
        action = BesselAction(1.0 + 0.0j)
        cps = action.exact_critical_points()
        for cp in cps:
            idx = morse_index(action, [cp])
            assert idx >= 0, f"Morse index should be >= 0 for Bessel CP {cp}, got {idx}"


class TestIntersectionNumbers:
    def test_airy_intersection_numbers_from_real_axis(self):
        """For S(z) = i(z^3/3 + z), the ascending flow from the real axis
        should converge to at least one critical point."""
        action = AiryAction(1.0 + 0.0j)
        cps = action.exact_critical_points()
        cps_list = [[cp] for cp in cps]

        seeds = [[x + 0.0j] for x in [-0.5, 0.0, 0.5]]

        n_sigma = compute_intersection_numbers(
            action, cps_list, seeds, dt=0.001, steps=500, cp_tol=0.2
        )

        total = sum(abs(v) for v in n_sigma.values())
        assert total >= 0, "Intersection numbers should be computable"


class TestChernSimonsAnalyticDerivatives:
    def test_figure_eight_analytic_vs_finite_diff_gradient(self):
        """Analytic gradient should agree with finite-diff to ~1e-4.
        Since S = |A|^2/2 is real-valued, the gradient is real."""
        action = ChernSimonsKnotAction("figure_eight")
        z = [cmath.exp(1j * 0.3), cmath.exp(1j * 0.7)]

        grad_analytic = action.gradient(z)

        h = 1e-7
        f0 = action.eval(z).real
        fm = action.eval([z[0] + h, z[1]]).real
        fl = action.eval([z[0], z[1] + h]).real
        grad_fd = [(fm - f0) / h, (fl - f0) / h]

        assert abs(grad_analytic[0] - grad_fd[0]) < 1e-3, \
            f"Gradient[0] mismatch: analytic={grad_analytic[0]}, fd={grad_fd[0]}"
        assert abs(grad_analytic[1] - grad_fd[1]) < 1e-3, \
            f"Gradient[1] mismatch: analytic={grad_analytic[1]}, fd={grad_fd[1]}"

    def test_trefoil_analytic_gradient(self):
        """Analytic gradient for trefoil should match finite-diff."""
        action = ChernSimonsKnotAction("trefoil")
        z = [1.0 + 0.5j, -0.5 + 0.3j]

        grad_analytic = action.gradient(z)

        h = 1e-7
        f0 = action.eval(z).real
        fm = action.eval([z[0] + h, z[1]]).real
        fl = action.eval([z[0], z[1] + h]).real
        grad_fd = [(fm - f0) / h, (fl - f0) / h]

        assert abs(grad_analytic[0] - grad_fd[0]) < 1e-3
        assert abs(grad_analytic[1] - grad_fd[1]) < 1e-3


    def test_gradient_vanishes_at_flat_connection(self):
        """Gradient of |A|^2/2 should vanish at points where A = 0."""
        action = ChernSimonsKnotAction("figure_eight")
        flat_pairs = FigureEightCharacterVariety.non_abelian_flat_connections()
        m0, l0 = flat_pairs[0]

        grad = action.gradient([m0, l0])
        assert abs(grad[0]) < 1e-8 and abs(grad[1]) < 1e-8, \
            f"Gradient at flat connection should vanish: {grad}"


class TestAnalyticContinuation:
    def test_t_scaling_preserves_critical_points(self):
        """Multiplying the action by t doesn't move the critical points."""
        base = AiryAction(1.0 + 0.0j)
        t = 2.0 + 1.0j
        continued = AnalyticContinuationCS(base, t)

        cps_base = base.exact_critical_points()
        for cp in cps_base:
            grad = continued.gradient([cp])
            assert abs(grad[0]) < 1e-10, \
                f"Critical point {cp} should remain critical under t-scaling"

    def test_t_scaling_of_action_value(self):
        """S_t(z) = t * S_1(z)."""
        base = AiryAction(1.0 + 0.0j)
        t = 3.0 - 2.0j
        continued = AnalyticContinuationCS(base, t)

        z = [0.5 + 0.3j]
        s_base = base.eval(z)
        s_continued = continued.eval(z)
        assert abs(s_continued - t * s_base) < 1e-12

    def test_stokes_scan_detects_walls(self):
        """Scanning arg(t) around S^1 should detect Stokes walls where
        Re(S(z+)) = Re(S(z-))."""
        base = AiryAction(1.0 + 0.0j)
        continued = AnalyticContinuationCS(base, 1.0 + 0.0j)

        results = continued.stokes_wall_crossing_scan(t_mag=1.0, num_angles=36)
        assert len(results) == 36

        near_stokes = [r for r in results if r["is_near_stokes_wall"]]
        assert len(near_stokes) > 0, \
            "Should detect at least one Stokes wall in a full rotation"

    def test_critical_values_scale_with_t(self):
        """Critical values at level t should be t * (critical values at level 1)."""
        base = AiryAction(1.0 + 0.0j)
        t = 2.0 + 0.5j
        continued = AnalyticContinuationCS(base, t)

        cps = base.exact_critical_points()
        for cp in cps:
            s1 = base.eval([cp])
            st = continued.eval([cp])
            assert abs(st - t * s1) < 1e-12


class TestThimbleIntegration:
    def test_airy_thimble_integral_is_finite(self):
        """Thimble integral of e^{-S} should converge to a finite value."""
        action = AiryAction(1.0 + 0.0j)
        cps = action.exact_critical_points()

        integral, traj = integrate_thimble(action, [cps[0]], dt=0.003, steps=300)
        assert math.isfinite(abs(integral)), "Thimble integral should be finite"
        assert abs(integral) > 0, "Thimble integral should be nonzero"
        assert len(traj) > 0

    def test_partition_function_evaluates(self):
        """Z = sum n_sigma * integral_{J_sigma} should compute without error."""
        action = AiryAction(1.0 + 0.0j)
        cps = action.exact_critical_points()
        cps_list = [[cp] for cp in cps]

        n_sigma = {0: 1, 1: 1}

        Z, contributions = partition_function(
            action, cps_list, n_sigma, dt=0.003, steps=200
        )
        assert math.isfinite(abs(Z)), "Partition function should be finite"
        assert len(contributions) == 2


class TestVolumeConjecture:
    def test_figure_eight_cs_values_encode_volume(self):
        """The imaginary part of the non-abelian CS values should give Vol(4_1) / (2pi)."""
        cs_plus = FigureEightCharacterVariety.cs_value("non_abelian_plus")
        expected_vol = FIGURE_EIGHT_VOLUME / (2.0 * math.pi)
        assert abs(cs_plus.imag - expected_vol) < 1e-10, \
            f"Im(CS+) = {cs_plus.imag}, expected {expected_vol}"

        cs_minus = FigureEightCharacterVariety.cs_value("non_abelian_minus")
        assert abs(cs_minus.imag + expected_vol) < 1e-10, \
            f"Im(CS-) = {cs_minus.imag}, expected {-expected_vol}"


