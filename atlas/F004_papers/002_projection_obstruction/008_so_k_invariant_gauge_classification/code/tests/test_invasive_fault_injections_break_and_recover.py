"""
Invasive Fault-Injection, Resilience, and Break-and-Recover Test Suite.
Paper: GS-002 (008_so_k_invariant_gauge_classification)
Bulgakov Council Quality & Adversarial Robustness Gate.
"""

from __future__ import annotations
import math
import numpy as np
import pytest

from carrier import GraphComplex, Cochain, SlaterViolationError
from gauges import (
    make_so2_rotation,
)
from socp_exact_certifier import ExactSOCPCertifier
from falsification import InvasiveAdversary
from cycle_analytics import (
    compute_holonomy,
    single_cycle_quotient_analytical,
)


def create_triangle_complex() -> GraphComplex:
    """Standard normalized triangle complex."""
    edges = [(0, 1), (1, 2), (2, 0)]
    weights = [1.0, 1.0, 1.0]
    return GraphComplex(edges=edges, num_vertices=3, edge_weights=weights, stalk_dim=2)


class TestInvasiveFaultInjections:
    """Adversarial stress-testing suite asserting break-and-recover dynamics."""

    def test_divergence_break_and_recover(self) -> None:
        """Invasive non-divergence injection into dual certificate and Laplacian recovery."""
        gc = create_triangle_complex()
        adv = InvasiveAdversary(gc)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]), degree=1)

        res = adv.test_divergence_injection_and_recovery(
            omega, perturbation_magnitude=0.75
        )
        assert res.detected_failure, (
            "Adversarial non-divergence injection was not detected!"
        )
        assert res.recovery_successful, (
            "Laplacian recovery projection failed to restore divergence-free status!"
        )
        assert res.metrics["max_divergence_corrupted"] > 0.1
        assert res.metrics["max_divergence_recovered"] <= 1e-5

    def test_gauge_anisotropy_break_and_recover(self) -> None:
        """Invasive elliptical anisotropy injection into local gauge and restoration."""
        gc = create_triangle_complex()
        adv = InvasiveAdversary(gc)

        res = adv.test_gauge_anisotropy_injection(epsilon=0.35)
        assert res.detected_failure, "Anisotropic gauge distortion went undetected!"
        assert res.recovery_successful, "Euclidean gauge restoration failed!"
        assert res.metrics["corrupted_max_deviation"] > 0.1
        assert res.metrics["restored_max_deviation"] < 1e-6

    def test_dual_norm_bound_violation_break_and_recover(self) -> None:
        """Invasive dual norm inflation beyond edge weight c_e and metric ball projection."""
        gc = create_triangle_complex()
        adv = InvasiveAdversary(gc)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]), degree=1)

        res = adv.test_dual_norm_bound_violation_and_recovery(
            omega, overshoot_factor=3.0
        )
        assert res.detected_failure, "Dual norm violation went undetected!"
        assert res.recovery_successful, (
            "Metric ball projection failed to recover dual feasibility!"
        )
        assert res.metrics["max_violation_corrupted"] > 0.5
        assert res.metrics["max_violation_recovered"] <= 1e-7

    def test_connection_corruption_and_direct_repair(self) -> None:
        """Invasive SO(2) rotation injection breaking flat holonomy and direct repair."""
        gc = create_triangle_complex()
        adv = InvasiveAdversary(gc)

        res = adv.test_connection_corruption_and_direct_repair(theta_angle=0.45)
        assert res.detected_failure, "Holonomy curvature defect went undetected!"
        assert res.recovery_successful, (
            "Direct connection restoration failed to repair flat connection!"
        )
        assert res.metrics["holonomy_deviation_corrupted"] > 0.1
        assert res.metrics["holonomy_deviation_recovered"] <= 1e-7

    def test_vertex_gauge_transformation_conjugacy(self) -> None:
        """Genuine vertex gauge transformation conjugating holonomy and preserving curvature."""
        gc = create_triangle_complex()
        adv = InvasiveAdversary(gc)

        res = adv.test_vertex_gauge_transformation_conjugacy(theta_angle=0.5)
        assert res.detected_failure, "Curvature should not disappear under gauge transformation!"
        assert res.recovery_successful, "Holonomy conjugacy identity failed under vertex gauge!"
        assert res.metrics["trace_error"] < 1e-6
        assert res.metrics["conjugacy_error"] < 1e-6
        assert res.metrics["holonomy_deviation_transformed"] > 0.1

    def test_holonomy_computation_validation(self) -> None:
        """Verify holonomy matrix multiplication and orientation inversion."""
        theta = 0.5
        rot = make_so2_rotation(theta)
        r_list = [rot, np.eye(2), np.eye(2)]
        h = compute_holonomy(r_list)
        assert np.linalg.norm(h - np.eye(2)) > 0.1
        # Inverse orientation produces transpose
        h_inv = compute_holonomy([rot], orientations=[-1])
        np.testing.assert_allclose(h_inv, rot.T)

        with pytest.raises(ValueError, match="Must provide at least one"):
            compute_holonomy([])
        with pytest.raises(ValueError, match="Orientations count"):
            compute_holonomy([rot], orientations=[1, -1])

    def test_single_cycle_bottleneck_saturation(self) -> None:
        """Verify that single-cycle quotient saturates at min_e w_e * j(S(omega))."""
        from gauges import EuclideanGauge
        euc = EuclideanGauge(1.0)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]), degree=1)
        weights = [2.0, 5.0, 10.0]
        val = single_cycle_quotient_analytical(omega, euc, edge_weights=weights)
        # S(omega) = (1, 1), ||S||_2 = sqrt(2), w_min = 2.0
        assert val == pytest.approx(2.0 * math.sqrt(2.0))

    def test_slater_condition_break_and_recover(self) -> None:
        """Invasive negative-weight injection violating Slater condition and recovery."""
        edges = [(0, 1), (1, 2), (2, 0)]
        corrupt_weights = [1.0, -0.5, 1.0]

        # Break: Slater condition violation
        with pytest.raises(SlaterViolationError, match="strictly positive"):
            GraphComplex(
                edges=edges, num_vertices=3, edge_weights=corrupt_weights, stalk_dim=2
            )

        # Recover: Positive weights restored
        repaired_weights = [1.0, 0.5, 1.0]
        gc = GraphComplex(
            edges=edges, num_vertices=3, edge_weights=repaired_weights, stalk_dim=2
        )
        assert np.all(gc.edge_weights > 0)
        certifier = ExactSOCPCertifier(gc)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]), degree=1)
        cert = certifier.certify(omega)
        assert cert.is_zero_gap
        assert cert.duality_gap < 1e-7

    def test_lipschitz_adversary(self) -> None:
        """Invasive noise perturbation asserting Lipschitz contractivity."""
        gc = create_triangle_complex()
        adv = InvasiveAdversary(gc)
        omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]), degree=1)
        res = adv.test_lipschitz_noise_resilience(omega, noise_level=0.1)
        assert res.recovery_successful, (
            "Lipschitz bound violated under adversarial noise!"
        )
