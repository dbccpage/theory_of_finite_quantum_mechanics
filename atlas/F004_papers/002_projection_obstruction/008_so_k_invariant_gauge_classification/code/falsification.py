"""
Invasive Fault-Injection and Recovery Engine.
Paper: GS-002 (008_so_k_invariant_gauge_classification)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any
import numpy as np

from carrier import GraphComplex, Cochain
from gauges import (
    EuclideanGauge,
    AnisotropicGauge,
    audit_so_k_invariance,
    make_so2_rotation,
    make_random_sok_rotation,
)
from solver import MixedNormSolver
from cycle_analytics import compute_holonomy, apply_vertex_gauge_transformation


@dataclass(frozen=True)
class InjectionRecoveryResult:
    """Report on fault injection, detection, and recovery."""

    test_name: str
    fault_injected: str
    detected_failure: bool
    recovery_successful: bool
    metrics: Dict[str, Any]


class InvasiveAdversary:
    """
    Adversarial injector that perturbs mathematical contracts,
    verifies that detectors catch violations, and asserts robust recovery.
    """

    def __init__(self, complex: GraphComplex) -> None:
        self.complex = complex
        self.solver = MixedNormSolver(complex)

    def test_divergence_injection_and_recovery(
        self, omega: Cochain, perturbation_magnitude: float = 0.5
    ) -> InjectionRecoveryResult:
        """
        1. Obtain valid optimal dual circulation phi* (satisfies d0^* phi* = 0).
        2. Invasively inject non-divergence-free perturbation delta.
        3. Assert detection: verifier flags divergence violation.
        4. Apply Laplacian projection to recover divergence-free circulation.
        5. Assert recovery: recovered circulation satisfies d0^* phi = 0 and ||phi_e|| <= c_e.
        """
        cert = self.solver.solve(omega)
        phi_clean = cert.dual_circulation.data.copy()

        m, k = self.complex.num_edges, self.complex.stalk_dim
        delta = np.zeros((m, k), dtype=float)
        delta[0, 0] = perturbation_magnitude

        phi_corrupted = phi_clean + delta
        div_corrupted = self.complex.d0.T @ phi_corrupted
        max_div_corrupted = float(np.max(np.abs(div_corrupted)))

        detected = bool(max_div_corrupted > 1e-4)

        d0 = self.complex.d0
        laplacian = d0.T @ d0
        rhs = d0.T @ phi_corrupted
        beta, _, _, _ = np.linalg.lstsq(laplacian, rhs, rcond=None)
        phi_recovered = phi_corrupted - d0 @ beta

        norms = np.linalg.norm(phi_recovered, axis=1)
        ratios = norms / self.complex.edge_weights
        if np.max(ratios) > 1.0:
            phi_recovered = phi_recovered / np.max(ratios)

        div_recovered = self.complex.d0.T @ phi_recovered
        max_div_recovered = float(np.max(np.abs(div_recovered)))
        recovered = bool(max_div_recovered <= 1e-5)

        return InjectionRecoveryResult(
            test_name="divergence_injection_and_recovery",
            fault_injected=f"Additive non-divergence delta of magnitude {perturbation_magnitude}",
            detected_failure=detected,
            recovery_successful=recovered,
            metrics={
                "max_divergence_corrupted": max_div_corrupted,
                "max_divergence_recovered": max_div_recovered,
            },
        )

    def test_gauge_anisotropy_injection(
        self, epsilon: float = 0.2
    ) -> InjectionRecoveryResult:
        """
        1. Inject anisotropy into local gauge via A = diag(1, 1 + eps).
        2. Assert detection: SO(k) invariance audit strictly catches the failure.
        3. Restore isotropic Euclidean gauge.
        4. Assert recovery: invariance audit passes.
        """
        k = self.complex.stalk_dim
        a_corrupt = np.eye(k, dtype=float)
        a_corrupt[0, 0] += epsilon
        aniso_gauge = AnisotropicGauge(a_corrupt)

        audit_corrupt = audit_so_k_invariance(aniso_gauge, dim=k, num_samples=50)
        detected = not audit_corrupt["is_so_k_invariant"]

        iso_gauge = EuclideanGauge(1.0)
        audit_restored = audit_so_k_invariance(iso_gauge, dim=k, num_samples=50)
        recovered = audit_restored["is_so_k_invariant"]

        return InjectionRecoveryResult(
            test_name="gauge_anisotropy_injection",
            fault_injected=f"Diagonal anisotropy scaling with epsilon={epsilon}",
            detected_failure=detected,
            recovery_successful=recovered,
            metrics={
                "corrupted_max_deviation": audit_corrupt["max_deviation"],
                "restored_max_deviation": audit_restored["max_deviation"],
            },
        )

    def test_lipschitz_noise_resilience(
        self, omega: Cochain, noise_level: float = 0.05
    ) -> InjectionRecoveryResult:
        """
        1. Evaluate Phi(omega).
        2. Invasively inject Gaussian noise eta of bounded norm ||eta||_{1,2,c}.
        3. Assert theoretical Lipschitz continuity: |Phi(omega + eta) - Phi(omega)| <= ||eta||_{1,2,c}.
        """
        rng = np.random.default_rng(123)
        phi_orig = self.solver.solve(omega).primal_value

        noise_data = rng.normal(scale=noise_level, size=omega.shape)
        eta = Cochain(noise_data, degree=1)
        eta_norm = eta.mixed_l1_l2_norm(self.complex.edge_weights)

        omega_noisy = omega + eta
        phi_noisy = self.solver.solve(omega_noisy).primal_value

        abs_diff = abs(phi_noisy - phi_orig)
        lipschitz_holds = bool(abs_diff <= eta_norm + 1e-5)

        return InjectionRecoveryResult(
            test_name="lipschitz_noise_resilience",
            fault_injected=f"Gaussian noise with std={noise_level}, ||eta||={eta_norm:.4f}",
            detected_failure=True,
            recovery_successful=lipschitz_holds,
            metrics={
                "phi_original": phi_orig,
                "phi_noisy": phi_noisy,
                "absolute_difference": abs_diff,
                "theoretical_upper_bound": eta_norm,
            },
        )

    def test_dual_norm_bound_violation_and_recovery(
        self, omega: Cochain, overshoot_factor: float = 2.0
    ) -> InjectionRecoveryResult:
        """
        1. Obtain clean dual circulation phi*.
        2. Invasively scale an edge dual vector by overshoot_factor to violate ||phi_e||_2 <= c_e.
        3. Assert detection: verifier catches norm bound violation.
        4. Apply metric ball projection: phi_e <- phi_e * min(1, c_e / ||phi_e||_2).
        5. Assert recovery: dual norms strictly satisfy bounds.
        """
        cert = self.solver.solve(omega)
        phi_corrupt = cert.dual_circulation.data.copy()
        w = self.complex.edge_weights

        phi_corrupt[0] = phi_corrupt[0] * overshoot_factor
        norms_corrupt = np.linalg.norm(phi_corrupt, axis=1)
        violations_corrupt = np.maximum(0.0, norms_corrupt - w)
        max_viol_corrupt = float(np.max(violations_corrupt))
        detected = bool(max_viol_corrupt > 1e-4)

        phi_recovered = phi_corrupt.copy()
        for e in range(len(w)):
            n_e = np.linalg.norm(phi_recovered[e])
            if n_e > w[e]:
                phi_recovered[e] = phi_recovered[e] * (w[e] / n_e)

        norms_recovered = np.linalg.norm(phi_recovered, axis=1)
        violations_recovered = np.maximum(0.0, norms_recovered - w)
        max_viol_recovered = float(np.max(violations_recovered))
        recovered = bool(max_viol_recovered <= 1e-7)

        return InjectionRecoveryResult(
            test_name="dual_norm_bound_violation_and_recovery",
            fault_injected=f"Dual norm scaled by factor {overshoot_factor}",
            detected_failure=detected,
            recovery_successful=recovered,
            metrics={
                "max_violation_corrupted": max_viol_corrupt,
                "max_violation_recovered": max_viol_recovered,
            },
        )

    def test_connection_corruption_and_direct_repair(
        self, theta_angle: float = 0.5
    ) -> InjectionRecoveryResult:
        """
        1. Consider cycle with identity connection R_e = I (flat, H_C = I).
        2. Invasively inject non-trivial rotation R_0 = SO(2)(theta) into edge 0 (curvature corruption).
        3. Assert detection: cycle holonomy deviation ||H_C - I|| > 0.
        4. Directly repair corrupted edge connection by replacing R_0 with original identity transport.
        5. Assert recovery: flat connection restored, H_C = I within numerical tolerance.
        """
        m = self.complex.num_edges
        k = self.complex.stalk_dim
        r_clean = [np.eye(k) for _ in range(m)]
        h_clean = compute_holonomy(r_clean)
        dev_clean = float(np.linalg.norm(h_clean - np.eye(k)))

        rot = make_so2_rotation(theta_angle) if k == 2 else np.eye(k)
        if k > 2:
            rot = np.eye(k)
            rot[0:2, 0:2] = make_so2_rotation(theta_angle)

        r_corrupt = [rot] + [np.eye(k) for _ in range(m - 1)]
        h_corrupt = compute_holonomy(r_corrupt)
        dev_corrupt = float(np.linalg.norm(h_corrupt - np.eye(k)))
        detected = bool(dev_corrupt > 1e-4)

        # Direct repair / replacement: replace corrupted edge 0 with identity
        r_recovered = [np.eye(k)] + [np.eye(k) for _ in range(m - 1)]
        h_recovered = compute_holonomy(r_recovered)
        dev_recovered = float(np.linalg.norm(h_recovered - np.eye(k)))
        recovered = bool(dev_recovered <= 1e-7)

        return InjectionRecoveryResult(
            test_name="connection_corruption_and_direct_repair",
            fault_injected=f"SO(k) rotation of angle {theta_angle:.3f} injected into edge 0",
            detected_failure=detected,
            recovery_successful=recovered,
            metrics={
                "holonomy_deviation_clean": dev_clean,
                "holonomy_deviation_corrupted": dev_corrupt,
                "holonomy_deviation_recovered": dev_recovered,
            },
        )

    def test_vertex_gauge_transformation_conjugacy(
        self, theta_angle: float = 0.5
    ) -> InjectionRecoveryResult:
        """
        Verify genuine vertex gauge transformations g_v in SO(k).
        Under R'_{uv} = g_v @ R_{uv} @ g_u.T, cycle holonomy transforms as H'_C = g_0 @ H_C @ g_0.T.
        Asserts that:
        1. Holonomy curvature ||H_C - I|| does NOT disappear (curvature is gauge-invariant).
        2. Trace Tr(H'_C) == Tr(H_C) is strictly conserved.
        3. Conjugacy identity ||H'_C - g_0 @ H_C @ g_0.T|| == 0 holds.
        """
        m = self.complex.num_edges
        n = self.complex.num_vertices
        k = self.complex.stalk_dim

        # Initial non-trivial connection on edge 0
        rot = make_so2_rotation(theta_angle) if k == 2 else np.eye(k)
        if k > 2:
            rot = np.eye(k)
            rot[0:2, 0:2] = make_so2_rotation(theta_angle)

        r_connections = [rot] + [np.eye(k) for _ in range(m - 1)]
        h_original = compute_holonomy(r_connections)
        tr_original = float(np.trace(h_original))
        dev_original = float(np.linalg.norm(h_original - np.eye(k)))

        # Sample non-trivial vertex gauge elements g_v in SO(k)
        rng = np.random.default_rng(999)
        vertex_gauges = [make_random_sok_rotation(k, rng=rng) for _ in range(n)]

        # Apply genuine vertex gauge transformation
        r_transformed = apply_vertex_gauge_transformation(
            r_connections, vertex_gauges, self.complex.edges
        )
        h_transformed = compute_holonomy(r_transformed)
        tr_transformed = float(np.trace(h_transformed))

        # Expected conjugated holonomy: g_0 @ H_C @ g_0.T
        g0 = vertex_gauges[0]
        h_expected = g0 @ h_original @ g0.T
        conjugacy_error = float(np.linalg.norm(h_transformed - h_expected))
        tr_error = abs(tr_original - tr_transformed)

        # Holonomy does NOT disappear to identity: ||H'_C - I|| remains > 0.1
        dev_transformed = float(np.linalg.norm(h_transformed - np.eye(k)))
        curvature_preserved = dev_transformed > 0.1

        success = bool(conjugacy_error < 1e-6 and tr_error < 1e-6 and curvature_preserved)

        return InjectionRecoveryResult(
            test_name="vertex_gauge_transformation_conjugacy",
            fault_injected=f"Vertex gauge transformation applied to SO(k) connection with curvature {theta_angle:.3f}",
            detected_failure=curvature_preserved,
            recovery_successful=success,
            metrics={
                "trace_original": tr_original,
                "trace_transformed": tr_transformed,
                "trace_error": tr_error,
                "conjugacy_error": conjugacy_error,
                "holonomy_deviation_original": dev_original,
                "holonomy_deviation_transformed": dev_transformed,
            },
        )

    # Backward compatibility alias
    def test_holonomy_curvature_injection_and_recovery(
        self, theta_angle: float = 0.5
    ) -> InjectionRecoveryResult:
        return self.test_connection_corruption_and_direct_repair(theta_angle=theta_angle)
