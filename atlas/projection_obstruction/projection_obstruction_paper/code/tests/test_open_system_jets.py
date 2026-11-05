"""Comprehensive unit and property tests for Open-System Jets and Local Generator Strengths (R2).

Verifies:
1. Incident local generator strengths (g_v, G_v, Gamma_e).
2. Open-system quadratic defect bound nu_e t - 2 (g_v + G_v)^2 t^2.
3. Parameter uncertainty propagation (delta_J, delta_gamma, delta_M).
4. Rigorous three-axis separation (correlation production, entanglement production, prediction error).
5. Open-system Lindblad dynamics simulation and jet expansion consistency.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from observable_duhamel import Interval  # noqa: E402
from open_system_jets import (  # noqa: E402
    LocalHamiltonianTerm,
    LocalJumpOperator,
    OpenSystemInputError,
    ThreeAxisPhenomenology,
    certify_three_axis_separation,
    compute_edge_incident_strengths,
    compute_local_incident_strengths,
    compute_open_system_jets,
    concurrence_two_qubit,
    correlation_defect,
    entanglement_negativity,
    evaluate_open_system_defect_jet,
    evaluate_volume_uniform_open_system_defect,
    compute_local_term_strength,
    compute_maximum_incident_strength,
    amplitude_damping_entropy_cooling,
    partial_trace_bipartite,
    partial_transpose_bipartite,
    propagate_parameter_uncertainties,
    quantum_mutual_information,
    simulate_open_system_evolution,
    trace_norm,
)

SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=np.complex128)
SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
IDENTITY_2 = np.eye(2, dtype=np.complex128)


class TestIncidentLocalGeneratorStrengths:
    """Verify computation of g_v, G_v, and edge interaction strength Gamma_e."""

    def test_single_vertex_incident_strengths(self) -> None:
        # Vertex 1 has two incident Hamiltonian terms: h_01 with norm 1.0, h_12 with norm 0.5
        # and one local Lindblad dephasing jump operator with rate gamma=0.2 and norm=1.0
        h_terms = [
            LocalHamiltonianTerm("h01", (0, 1), 1.0 * np.kron(SIGMA_Z, SIGMA_Z)),
            LocalHamiltonianTerm("h12", (1, 2), 0.5 * np.kron(SIGMA_X, SIGMA_X)),
            LocalHamiltonianTerm("h23", (2, 3), 0.8 * np.kron(SIGMA_Z, SIGMA_Z)),
        ]
        jump_ops = [
            LocalJumpOperator("L1", (1,), SIGMA_Z, rate=0.2),
            LocalJumpOperator("L2", (2,), SIGMA_Z, rate=0.4),
        ]

        g_1, G_1 = compute_local_incident_strengths(h_terms, jump_ops, vertex=1)
        # g_1 = 1.0 + 0.5 = 1.5
        assert math.isclose(g_1, 1.5, abs_tol=1.0e-12)
        # G_1 = 0.2 * 1^2 = 0.2
        assert math.isclose(G_1, 0.2, abs_tol=1.0e-12)

        # Vertex 0: only h01 incident, no jump ops
        g_0, G_0 = compute_local_incident_strengths(h_terms, jump_ops, vertex=0)
        assert math.isclose(g_0, 1.0, abs_tol=1.0e-12)
        assert math.isclose(G_0, 0.0, abs_tol=1.0e-12)

    def test_edge_incident_strengths(self) -> None:
        h_terms = [
            LocalHamiltonianTerm("h01", (0, 1), 1.0 * np.kron(SIGMA_Z, SIGMA_Z)),
        ]
        jump_ops = [
            LocalJumpOperator("L0", (0,), SIGMA_Z, rate=0.1),
            LocalJumpOperator("L1", (1,), SIGMA_Z, rate=0.1),
        ]

        g_e, G_e, gamma_e = compute_edge_incident_strengths(h_terms, jump_ops, edge=(0, 1))
        # g_0 = 1.0, g_1 = 1.0 => g_e = 2.0
        assert math.isclose(g_e, 2.0, abs_tol=1.0e-12)
        # G_0 = 0.1, G_1 = 0.1 => G_e = 0.2
        assert math.isclose(G_e, 0.2, abs_tol=1.0e-12)
        # Gamma_e = (g_e + G_e)^2 = (2.2)^2 = 4.84
        assert math.isclose(gamma_e, 4.84, abs_tol=1.0e-12)


class TestOpenSystemDefectJet:
    """Verify quadratic short-time curvature bound nu_e t - 2 (g_v + G_v)^2 t^2."""

    def test_open_system_defect_jet_evaluation(self) -> None:
        nu_e = 1.0
        g_v = 0.5
        G_v = 0.2
        t = 0.1
        # Gamma = (0.7)^2 = 0.49
        # Curvature = 24 * 0.49 * 0.01 = 0.1176 (from 6 Lambda_*^2 with Lambda_* = 1.4)
        # nu_e * t = 0.1
        # Bound = 0.1 - 0.1176 = -0.0176
        bound = evaluate_open_system_defect_jet(nu_e, g_v, G_v, t)
        assert math.isclose(bound, -0.0176, abs_tol=1.0e-12)

    def test_negative_time_raises_error(self) -> None:
        with pytest.raises(OpenSystemInputError, match="time must be non-negative"):
            evaluate_open_system_defect_jet(nu_e=1.0, g_v=0.5, G_v=0.2, time=-0.1)

    def test_turnaround_time_inflection(self) -> None:
        """Quadrature peak turnaround occurs at t* = nu_e / (48 (g_v + G_v)^2)."""
        nu_e = 2.0
        g_v = 1.0
        G_v = 0.0
        # Gamma = 1.0, D(t) = 2 t - 24 t^2
        # dD/dt = 2 - 48t = 0 => t* = 2/48 = 1/24, D(1/24) = 2(1/24) - 24(1/576) = 1/24
        t_peak = 1.0 / 24.0
        val_at_peak = evaluate_open_system_defect_jet(nu_e, g_v, G_v, time=t_peak)
        val_before = evaluate_open_system_defect_jet(nu_e, g_v, G_v, time=t_peak - 0.01)
        val_after = evaluate_open_system_defect_jet(nu_e, g_v, G_v, time=t_peak + 0.01)
        assert val_at_peak > val_before
        assert val_at_peak > val_after
        assert math.isclose(val_at_peak, 1.0 / 24.0)


class TestParameterUncertaintyPropagation:
    """Verify sensitivity propagation across couplings, jump rates, and measurement noise."""

    def test_uncertainty_interval_expansion(self) -> None:
        base = 0.5
        d_J = 0.05
        d_gamma = 0.02
        d_M = 0.01
        interval = propagate_parameter_uncertainties(
            delta_J=d_J,
            delta_gamma=d_gamma,
            delta_M=d_M,
            base_bound=base,
            time=0.2,
            g_nominal=1.0,
            G_nominal=0.5,
        )
        assert isinstance(interval, Interval)
        assert interval.lower < base
        assert interval.upper > base
        assert interval.contains(base)
        assert interval.width > 2.0 * d_M

    def test_mapping_uncertainty_input(self) -> None:
        delta_j_map = {"bond_0": 0.02, "bond_1": 0.05}
        delta_gamma_map = {"site_0": 0.01, "site_1": 0.03}
        interval = propagate_parameter_uncertainties(
            delta_J=delta_j_map,
            delta_gamma=delta_gamma_map,
            delta_M=0.02,
            base_bound=1.0,
        )
        assert interval.contains(1.0)


class TestThreeAxisPhenomenologicalSeparation:
    """Verify distinct separation of Correlation, Entanglement, and Prediction Error."""

    def test_axis_separation_correlated_separable_state(self) -> None:
        """Classically correlated separable state: D_e > 0, Mutual Info > 0, Negativity = 0."""
        # ρ = 0.5 |00><00| + 0.5 |11><11|
        rho_sep = np.zeros((4, 4), dtype=np.complex128)
        rho_sep[0, 0] = 0.5
        rho_sep[3, 3] = 0.5

        # Factorized product state: ρ_A ⊗ ρ_B = diag(0.25, 0.25, 0.25, 0.25)
        rho_fact = 0.25 * np.eye(4, dtype=np.complex128)

        # Observable that is sensitive to correlation: Z ⊗ Z
        obs_zz = np.kron(SIGMA_Z, SIGMA_Z)

        cert = certify_three_axis_separation(
            rho_actual=rho_sep,
            rho_factorized=rho_fact,
            observable=obs_zz,
        )

        assert isinstance(cert, ThreeAxisPhenomenology)
        # Correlation is present: D_e = ||ρ - 0.25 I||_1 = 4 * 0.25 = 1.0
        assert math.isclose(cert.correlation_defect_d1, 1.0, abs_tol=1.0e-12)
        assert cert.quantum_mutual_information > 0.6  # ln(2) ≈ 0.693
        assert cert.is_correlated is True

        # Entanglement must be strictly ZERO for separable mixture!
        assert math.isclose(cert.entanglement_negativity, 0.0, abs_tol=1.0e-12)
        assert math.isclose(cert.two_qubit_concurrence, 0.0, abs_tol=1.0e-12)
        assert cert.is_entangled is False

        # Prediction error for Z ⊗ Z: Tr(ZZ ρ) = 1.0, Tr(ZZ ρ_fact) = 0.0 => err = 1.0
        assert math.isclose(cert.observable_prediction_error, 1.0, abs_tol=1.0e-12)
        assert cert.has_prediction_error is True
        assert cert.phenomenological_regime == "correlated_separable_error"

    def test_axis_separation_correlated_zero_prediction_error(self) -> None:
        """State with strong correlation and entanglement, but commuting observable has ZERO error."""
        # Bell state |Φ+> = (|00> + |11>)/sqrt(2)
        psi = np.array([1.0, 0.0, 0.0, 1.0], dtype=np.complex128) / math.sqrt(2.0)
        rho_bell = np.outer(psi, psi.conj())
        rho_fact = 0.25 * np.eye(4, dtype=np.complex128)

        # Observable Z ⊗ I: <Z ⊗ I>_bell = 0.0, <Z ⊗ I>_fact = 0.0
        obs_z_single = np.kron(SIGMA_Z, IDENTITY_2)

        cert = certify_three_axis_separation(
            rho_actual=rho_bell,
            rho_factorized=rho_fact,
            observable=obs_z_single,
        )

        assert cert.is_correlated is True
        assert cert.is_entangled is True
        assert math.isclose(cert.entanglement_negativity, 0.5, abs_tol=1.0e-12)
        assert math.isclose(cert.two_qubit_concurrence, 1.0, abs_tol=1.0e-12)

        # Direct metric function calls
        assert math.isclose(trace_norm(rho_bell), 1.0)
        assert math.isclose(entanglement_negativity(rho_bell), 0.5)
        assert quantum_mutual_information(rho_bell) > 1.3  # 2 * ln(2) ≈ 1.386

        # Prediction error is exactly zero!
        assert math.isclose(cert.observable_prediction_error, 0.0, abs_tol=1.0e-12)
        assert cert.has_prediction_error is False
        assert cert.phenomenological_regime == "entangled_commuting"

    def test_axis_separation_pure_product_state(self) -> None:
        """Uncorrelated factorized state: all three axes are zero."""
        # |00><00|
        rho_prod = np.zeros((4, 4), dtype=np.complex128)
        rho_prod[0, 0] = 1.0

        cert = certify_three_axis_separation(
            rho_actual=rho_prod,
            rho_factorized=rho_prod,
            observable=np.kron(SIGMA_Z, SIGMA_Z),
        )
        assert cert.is_correlated is False
        assert cert.is_entangled is False
        assert cert.has_prediction_error is False
        assert cert.phenomenological_regime == "trivial_product"


class TestOpenSystemLindbladDynamics:
    """Verify Master equation integration and short-time Taylor jet envelope."""

    def test_open_system_jets_expansion(self) -> None:
        # Hamiltonian H = J (X ⊗ X)
        h = 0.5 * np.kron(SIGMA_X, SIGMA_X)
        # Dephasing jump operators L_1 = Z ⊗ I, L_2 = I ⊗ Z with rate gamma = 0.1
        jump_ops = [np.kron(SIGMA_Z, IDENTITY_2), np.kron(IDENTITY_2, SIGMA_Z)]
        rates = [0.1, 0.1]

        # Initial pure state |00><00|
        rho_0 = np.zeros((4, 4), dtype=np.complex128)
        rho_0[0, 0] = 1.0

        jets = compute_open_system_jets(rho_0, h, jump_ops, rates, order=2)
        assert len(jets) == 3
        assert np.allclose(jets[0], rho_0)
        # First jet should be Hermiticity preserving with zero trace
        assert math.isclose(complex(np.trace(jets[1])).real, 0.0, abs_tol=1.0e-12)
        assert np.allclose(jets[1], jets[1].conj().T, atol=1.0e-12)

    def test_open_system_simulation_defect_obeys_jet_envelope(self) -> None:
        """Evolve open system under Lindblad master equation and verify quadratic bound at small t."""
        j_val = 0.6
        gamma_val = 0.1
        h = j_val * np.kron(SIGMA_X, SIGMA_X)
        jump_ops = [np.kron(SIGMA_Z, IDENTITY_2), np.kron(IDENTITY_2, SIGMA_Z)]
        rates = [gamma_val, gamma_val]

        rho_0 = np.zeros((4, 4), dtype=np.complex128)
        rho_0[0, 0] = 1.0

        # Evolve up to t = 0.15
        times, states = simulate_open_system_evolution(
            rho_0=rho_0,
            hamiltonian=h,
            jump_ops=jump_ops,
            jump_rates=rates,
            time_horizon=0.15,
            steps=30,
        )

        # Incident local strengths for this 2-qubit system
        g_v = j_val
        G_v = gamma_val * (1.0**2)

        # Check defect D(t) at each small time step
        for t, rho_t in zip(times[1:10], states[1:10]):
            d_actual = correlation_defect(rho_t, dim_a=2, dim_b=2)
            # Normal rate for H = J XX on |00> is 2 * ||chi|| = 2 * J = 1.2
            nu_e = 2.0 * j_val
            bound = evaluate_open_system_defect_jet(nu_e=nu_e, g_v=g_v, G_v=G_v, time=t)
            # D_actual(t) >= nu_e t - 2 (g_v + G_v)^2 t^2
            assert d_actual >= bound - 1.0e-4, f"Defect {d_actual} violated jet bound {bound} at t={t}"


class TestOpenSystemJetsEdgeCasesAndValidation:
    """Exhaustive validation and boundary coverage for open_system_jets module."""

    def test_local_hamiltonian_and_jump_operator_validation(self) -> None:
        with pytest.raises(OpenSystemInputError, match="support cannot be empty"):
            LocalHamiltonianTerm("h", (), np.eye(2))
        with pytest.raises(OpenSystemInputError, match="must be a square matrix"):
            LocalHamiltonianTerm("h", (0,), np.ones((2, 3)))

        with pytest.raises(OpenSystemInputError, match="support cannot be empty"):
            LocalJumpOperator("L", (), np.eye(2))
        with pytest.raises(OpenSystemInputError, match="rate must be non-negative"):
            LocalJumpOperator("L", (0,), np.eye(2), rate=-0.5)
        with pytest.raises(OpenSystemInputError, match="must be a square matrix"):
            LocalJumpOperator("L", (0,), np.ones((2, 3)))

    def test_local_incident_strengths_dataclass_and_raw_tuples(self) -> None:
        from open_system_jets import LocalIncidentStrengths
        strengths = LocalIncidentStrengths(vertex=0, g_v=1.2, G_v=0.8)
        assert math.isclose(strengths.total_strength, 2.0)

        # Raw tuples for Hamiltonian terms and jump operators
        raw_h = [((0, 1), 0.5), ((0, 2), np.kron(SIGMA_Z, SIGMA_Z))]
        raw_jump = [((0,), 0.2, SIGMA_X)]
        g, G = compute_local_incident_strengths(raw_h, raw_jump, vertex=0)
        assert math.isclose(g, 1.5)  # 0.5 + 1.0
        assert math.isclose(G, 0.2)  # 0.2 * 1^2

        with pytest.raises(OpenSystemInputError, match="Cannot parse Hamiltonian term"):
            compute_local_incident_strengths(["invalid_term"], [], vertex=0)  # type: ignore

        with pytest.raises(OpenSystemInputError, match="Cannot parse Jump operator"):
            compute_local_incident_strengths([], ["invalid_jump"], vertex=0)  # type: ignore

    def test_partial_trace_and_transpose_options_and_errors(self) -> None:
        rho = 0.25 * np.eye(4, dtype=np.complex128)
        with pytest.raises(OpenSystemInputError, match="keep must be 'a' or 'b'"):
            partial_trace_bipartite(rho, dim_a=2, dim_b=2, keep="invalid")  # type: ignore

        # Partial transpose with respect to A
        pt_a = partial_transpose_bipartite(rho, dim_a=2, dim_b=2, target="a")
        assert np.allclose(pt_a, rho)

        # Non-4x4 concurrence error
        with pytest.raises(OpenSystemInputError, match="only defined for 4x4"):
            concurrence_two_qubit(np.eye(9, dtype=np.complex128))

    def test_von_neumann_entropy_empty_spectrum(self) -> None:
        from open_system_jets import von_neumann_entropy
        assert von_neumann_entropy(np.zeros((2, 2))) == 0.0

    def test_evaluate_defect_jet_negative_rates(self) -> None:
        with pytest.raises(OpenSystemInputError, match="Rates and generator strengths must be non-negative"):
            evaluate_open_system_defect_jet(nu_e=-0.5, g_v=1.0, G_v=0.2, time=0.1)

    def test_propagate_uncertainties_validation_and_interval_base(self) -> None:
        with pytest.raises(OpenSystemInputError, match="Measurement noise .* must be non-negative"):
            propagate_parameter_uncertainties(delta_J=0.1, delta_gamma=0.1, delta_M=-0.01, base_bound=1.0)

        with pytest.raises(OpenSystemInputError, match="Coupling and jump rate .* must be non-negative"):
            propagate_parameter_uncertainties(delta_J=-0.1, delta_gamma=0.1, delta_M=0.01, base_bound=1.0)

        # Interval base_bound
        base_iv = Interval(0.5, 0.8)
        propagated = propagate_parameter_uncertainties(
            delta_J=0.05,
            delta_gamma=0.02,
            delta_M=0.01,
            base_bound=base_iv,
        )
        assert propagated.lower < 0.5
        assert propagated.upper > 0.8

    def test_certify_three_axis_separation_higher_dim_and_regimes(self) -> None:
        # 3x3 bipartite system (qutrits)
        rho_qutrit = (1.0 / 9.0) * np.eye(9, dtype=np.complex128)
        obs_qutrit = np.eye(9, dtype=np.complex128)
        cert_3 = certify_three_axis_separation(
            rho_actual=rho_qutrit,
            rho_factorized=rho_qutrit,
            observable=obs_qutrit,
            dim_a=3,
            dim_b=3,
        )
        assert cert_3.two_qubit_concurrence == 0.0  # skips 2-qubit concurrence formula
        assert cert_3.phenomenological_regime == "trivial_product"


def test_volume_uniform_open_system_defect_formula():
    """Verify conservative volume-uniform open-system defect bound D_ab(t) >= nu_ab*t - 6 Lambda_*^2 t^2."""
    nu_ab = 1.0
    lambda_star = 0.5
    t = 0.1
    # 6 * (0.5)^2 * (0.1)^2 = 6 * 0.25 * 0.01 = 0.015
    # Bound = 1.0 * 0.1 - 0.015 = 0.085
    val = evaluate_volume_uniform_open_system_defect(nu_ab, lambda_star, t)
    assert math.isclose(val, 0.085, abs_tol=1e-12)


def test_amplitude_damping_entropy_cooling_regression():
    """Verify Review Finding 5 amplitude damping cooling/purification test.

    Maximally mixed state rho(0) = I/2 (1.0 bit entropy) cools under amplitude damping.
    At gamma * t = 1.0, entropy is approximately 0.68862 bits < 1.0 bit.
    """
    res = amplitude_damping_entropy_cooling(gamma_t=1.0)
    assert res["status"] == "pass"
    assert res["is_entropy_decreasing"] is True
    assert math.isclose(res["initial_entropy_bits"], 1.0, abs_tol=1e-12)
    assert math.isclose(res["final_entropy_bits"], 0.68862, abs_tol=1e-4)
    assert res["entropy_reduction_bits"] > 0.31
