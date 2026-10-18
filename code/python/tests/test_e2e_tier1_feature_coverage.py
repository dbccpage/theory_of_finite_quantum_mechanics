"""Tier 1: Feature Coverage E2E Tests (30 Tests).

AuthorityEffect: None.
Verifies the functional correctness and mathematical compliance of all primary quantum capabilities.
"""

from __future__ import annotations

from fractions import Fraction
import numpy as np
import pytest

from finite_qm.domain.primitives import (
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    HADAMARD_2,
    dagger,
)
from finite_qm.use_cases.born_normalization import (
    l1_to_l2_amplitude_lift,
    verify_born_normalization,
)
from finite_qm.use_cases.cptp_channel import (
    amplitude_damping_kraus,
    apply_channel,
    apply_depolarizing_channel,
    choi_matrix,
    construct_dual_witness,
    dephasing_kraus,
    hadamard_kraus,
    is_completely_positive,
    is_trace_preserving,
    solve_covariant_wigner_yanase_monotonicity,
    trace_distance_contraction,
    verify_dual_witness_bound,
    wigner_yanase_skew_information,
)
from finite_qm.use_cases.stabilizer_codes import (
    build_four_qubit_css_surface_code,
    build_steane_seven_qubit_code,
    build_three_qubit_bitflip_code,
)
from finite_qm.use_cases.composition_tensor_mub import (
    build_exact_composite_mub_d6,
    check_bilinearity,
    check_local_unitary_covariance,
    projection_report_dump,
    tensor_product,
    verify_mub_d6_unbiasedness,
)
from finite_qm.use_cases.contextuality_f2 import (
    context_products,
    enumerate_all_assignments,
    parity_obstruction,
)
from finite_qm.use_cases.contextuality_thresholds import ContextualityThresholds
from finite_qm.use_cases.quantum_protocols import (
    evaluate_clifford_pauli_conjugations,
    evaluate_discrete_pythagorean_bell_chsh,
    evaluate_pell_pythagorean_tsirelson_convergence,
    evaluate_qutrit_discrete_wigner,
    evaluate_t_gate_orbit_departure,
    simulate_discrete_quantum_teleportation,
    simulate_discrete_superdense_coding,
)


def test_tier1_born_normalization_basic():
    """1. L1 probability distribution lift to normalized Hilbert amplitude vector."""
    rho = np.array([0.2, 0.3, 0.5])
    psi = l1_to_l2_amplitude_lift(rho)
    assert verify_born_normalization(psi) is True
    assert np.isclose(np.sum(np.abs(psi) ** 2), 1.0, atol=1e-12)


def test_tier1_born_normalization_complex_phases():
    """2. Born amplitude lift with declared relative complex phases."""
    rho = [0.25, 0.75]
    phases = [0.0, np.pi / 2.0]
    psi = l1_to_l2_amplitude_lift(rho, phases=phases)
    assert verify_born_normalization(psi) is True
    assert np.isclose(psi[0].imag, 0.0, atol=1e-9)
    assert np.isclose(psi[1].real, 0.0, atol=1e-9)
    assert np.isclose(np.abs(psi[1]) ** 2, 0.75, atol=1e-9)


def test_tier1_cptp_dephasing_channel():
    """3. Single-qubit dephasing channel trace-preservation and complete positivity."""
    kraus = dephasing_kraus(0.3)
    assert is_trace_preserving(kraus) is True
    assert is_completely_positive(kraus) is True


def test_tier1_cptp_amplitude_damping_channel():
    """4. Amplitude damping channel trace-preservation and complete positivity."""
    kraus = amplitude_damping_kraus(0.25)
    assert is_trace_preserving(kraus) is True
    assert is_completely_positive(kraus) is True


def test_tier1_cptp_depolarizing_channel():
    """5. Depolarizing channel action on pure ground state."""
    rho0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_out = apply_depolarizing_channel(rho0, 0.4)
    assert np.isclose(rho_out[0, 0].real, 0.8, atol=1e-9)
    assert np.isclose(rho_out[1, 1].real, 0.2, atol=1e-9)
    assert np.isclose(np.trace(rho_out).real, 1.0, atol=1e-12)
    assert np.isclose(abs(rho_out[0, 1]), 0.0, atol=1e-12)


def test_tier1_cptp_choi_matrix_isomorphism():
    """6. Choi matrix isomorphism for single-qubit Hadamard channel."""
    kraus = hadamard_kraus()
    choi = choi_matrix(kraus)
    assert np.allclose(choi, choi.conj().T, atol=1e-12)
    assert np.isclose(np.trace(choi).real, 2.0, atol=1e-12)


def test_tier1_cptp_trace_distance_contraction():
    """7. Trace distance contraction under dephasing channel."""
    rho1 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho2 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)
    kraus = dephasing_kraus(0.2)
    res = trace_distance_contraction(rho1, rho2, kraus)
    assert res["is_contractive"] is True
    assert res["contraction_factor"] <= 1.0 + 1e-9


def test_tier1_wigner_yanase_skew_information():
    """8. Wigner-Yanase skew information for pure state and Pauli-Z observable."""
    psi = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho = np.outer(psi, psi.conj())
    val = wigner_yanase_skew_information(rho, SIGMA_Z)
    assert np.isclose(val, 1.0, atol=1e-9)


def test_tier1_covariant_wigner_yanase_monotonicity():
    """9. Covariant Wigner-Yanase skew information monotonicity under dephasing channel."""
    rho = np.diag([0.7, 0.3]).astype(complex)
    kraus = dephasing_kraus(0.2)
    res = solve_covariant_wigner_yanase_monotonicity(rho, kraus, SIGMA_Z)
    assert res["status"] == "COVARIANT_WIGNER_YANASE_MONOTONICITY_VERIFIED"
    assert res["delta_i"] >= -1e-9


def test_tier1_cptp_dual_witness_exact_norm():
    """10. Dual witness operator attaining exact trace distance norm."""
    rho1 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    psi_plus = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho2 = np.outer(psi_plus, psi_plus.conj())
    assert verify_dual_witness_bound(rho1, rho2) is True


def test_tier1_three_qubit_bitflip_code_stabilizers():
    """11. Three-qubit bitflip stabilizer code algebra and commutation."""
    res = build_three_qubit_bitflip_code()
    assert res["stabilizers_commute"] is True
    assert res["logical_ops_anticommute"] is True


def test_tier1_three_qubit_bitflip_error_recovery():
    """12. Three-qubit bitflip single-error syndrome distinctness and recovery."""
    res = build_three_qubit_bitflip_code()
    assert res["all_syndromes_distinct"] is True
    assert res["recovered_correctly"] is True


def test_tier1_four_qubit_css_surface_code():
    """13. Four-qubit [[4, 2, 2]] CSS surface code distance-2 error detection."""
    res = build_four_qubit_css_surface_code()
    assert res["all_single_errors_detected"] is True
    assert res["detected_error_count"] == 12


def test_tier1_steane_seven_qubit_code():
    """14. Steane [[7, 1, 3]] CSS code single-qubit error correction on Fano plane."""
    res = build_steane_seven_qubit_code()
    assert res["all_single_qubit_errors_correctable"] is True
    assert res["unique_error_syndromes_count"] == 21


def test_tier1_steane_code_transversal_hadamard():
    """15. Steane [[7, 1, 3]] code transversal Hadamard stability."""
    res = build_steane_seven_qubit_code()
    assert res["hadamard_preserves_stabilizers"] is True
    assert res["hadamard_implements_logical_h"] is True


def test_tier1_mub_dimension_6_three_bases():
    """16. Dimension d=6 composite MUB bases with exact mutual unbiasedness."""
    bases = build_exact_composite_mub_d6()
    assert len(bases) == 3
    res = verify_mub_d6_unbiasedness(bases)
    assert res["unbiasedness_verified"] is True
    assert res["basis_count"] == 3


def test_tier1_mub_tensor_axioms_bilinearity():
    """17. Tensor product bilinearity axiom verification."""
    assert check_bilinearity(tensor_product) is True


def test_tier1_mub_tensor_axioms_local_covariance():
    """18. Tensor product local unitary covariance and rival failure."""
    assert check_local_unitary_covariance(tensor_product) is True
    assert check_local_unitary_covariance(projection_report_dump) is False


def test_tier1_contextuality_peres_mermin_square():
    """19. Mermin-Peres 9-observable square context products and parity."""
    res = context_products()
    assert res["all_contexts_commute"] is True
    assert res["n_negative_contexts"] == 1
    assert res["parity_of_signs"] == -1


def test_tier1_contextuality_f2_parity_obstruction():
    """20. F_2 linear constraint rank inconsistency in Mermin-Peres square."""
    res = parity_obstruction()
    assert res["system_inconsistent"] is True
    assert res["rank_A"] == 5
    assert res["rank_augmented"] == 6


def test_tier1_contextuality_exhaustive_enumeration():
    """21. Exhaustive valuation search over 2^9 assignments confirming uncolorability."""
    res = enumerate_all_assignments()
    assert res["n_fully_consistent"] == 0
    assert res["max_contexts_satisfiable"] == 5


def test_tier1_contextuality_thresholds_peres_33():
    """22. Peres 33 rays in Z[sqrt(2)]^3 Kochen-Specker uncolorability."""
    res = ContextualityThresholds.evaluate_peres_33_rays()
    assert res["ray_count"] == 33
    assert res["uncolorability_confirmed"] is True


def test_tier1_contextuality_cabello_18_rays():
    """23. Cabello 18 rational rays in dimension 4 Kochen-Specker uncolorability."""
    res = ContextualityThresholds.evaluate_cabello_18_rays()
    assert res["ray_count"] == 18
    assert res["uncolorability_confirmed"] is True
    assert res["all_rays_degree_2"] is True


def test_tier1_bell_chsh_pythagorean_exact_violation():
    """24. Discrete Pythagorean (3, 4, 5) Bell-CHSH violation S = 14/5 = 2.8 > 2.0."""
    res = evaluate_discrete_pythagorean_bell_chsh()
    assert res["s_chsh_fraction"] == Fraction(14, 5)
    assert res["violates_local_realism"] is True


def test_tier1_pell_tsirelson_rational_deficit():
    """25. Pell-Pythagorean triple (119, 120, 169) Tsirelson convergence deficit."""
    res = evaluate_pell_pythagorean_tsirelson_convergence()
    assert res["s_chsh_fraction"] == Fraction(478, 169)
    assert res["squared_tsirelson_deficit"] == Fraction(4, 28561)


def test_tier1_clifford_pauli_conjugations():
    """26. Clifford normalizer action on single-qubit Pauli group."""
    res = evaluate_clifford_pauli_conjugations()
    assert res["is_clifford_normalizer"] is True
    assert res["h_squared_is_eye"] is True


def test_tier1_t_gate_orbit_departure():
    """27. Non-Clifford T-gate departure from Pauli group normalizer."""
    res = evaluate_t_gate_orbit_departure()
    assert res["is_equal_superposition"] is True
    assert res["non_clifford_certified"] is True


def test_tier1_qutrit_discrete_wigner_magic_negativity():
    """28. Qutrit discrete Wigner distribution magic state negativity W(0,0) = -1/3."""
    res = evaluate_qutrit_discrete_wigner("magic")
    assert res["has_negativity"] is True
    assert np.isclose(res["w00"], -1.0 / 3.0, atol=1e-9)


def test_tier1_discrete_quantum_teleportation_fidelity():
    """29. Discrete 3-qubit quantum teleportation protocol unit fidelity."""
    res = simulate_discrete_quantum_teleportation()
    assert res["all_branches_fidelity_one"] is True
    assert len(res["branch_fidelities"]) == 4


def test_tier1_discrete_superdense_coding_capacity():
    """30. Discrete superdense coding channel capacity ratio 2.0."""
    res = simulate_discrete_superdense_coding(1, 0)
    assert res["success"] is True
    assert res["channel_capacity_ratio"] == 2.0
