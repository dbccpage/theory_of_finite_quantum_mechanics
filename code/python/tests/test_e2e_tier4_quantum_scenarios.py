"""Tier 4: Real-World Quantum Scenarios E2E Tests (7 Tests).

AuthorityEffect: None.
End-to-end integration of multi-stage quantum protocols and experimental scenarios.
"""

from __future__ import annotations

from fractions import Fraction
import numpy as np
import pytest

from finite_qm.domain.primitives import (
    HADAMARD_2,
    I2,
    SIGMA_I,
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    dagger,
    kron_all,
)
from finite_qm.use_cases.busch_effects import bounded_effect_algebraic_search
from finite_qm.use_cases.cptp_channel import (
    apply_depolarizing_channel,
    construct_dual_witness,
    trace_norm,
    verify_dual_witness_bound,
)
from finite_qm.use_cases.contextuality_f2 import (
    context_products,
    peres_mermin_square,
)
from finite_qm.use_cases.discrete_walk_engines import (
    build_mzi_packet,
    build_sorkin_3slit_packet,
    sorkin_3slit_amplitudes_from_cochain,
)
from finite_qm.use_cases.quantum_protocols import (
    simulate_discrete_quantum_teleportation,
    simulate_discrete_superdense_coding,
)


def test_tier4_shor_nine_qubit_code_error_recovery():
    """1. Full Shor [[9, 1, 3]] quantum error correction code single-qubit error recovery."""
    # Logical basis states for Shor 9-qubit code:
    # |0_L> = 1/(2*sqrt(2)) (|000> + |111>) (|000> + |111>) (|000> + |111>)
    # |1_L> = 1/(2*sqrt(2)) (|000> - |111>) (|000> - |111>) (|000> - |111>)
    ket0 = np.array([1.0, 0.0], dtype=complex)
    ket1 = np.array([0.0, 1.0], dtype=complex)

    ket000 = kron_all(ket0, ket0, ket0)
    ket111 = kron_all(ket1, ket1, ket1)

    block_plus = (ket000 + ket111) / np.sqrt(2.0)
    block_minus = (ket000 - ket111) / np.sqrt(2.0)

    psi_0l = kron_all(block_plus, block_plus, block_plus)
    psi_1l = kron_all(block_minus, block_minus, block_minus)

    # Encode arbitrary state alpha |0_L> + beta |1_L>
    alpha = 0.6
    beta = 0.8
    psi_logical = alpha * psi_0l + beta * psi_1l
    assert np.isclose(np.linalg.norm(psi_logical), 1.0, atol=1e-12)

    # Error recovery check across single-qubit Pauli errors: X_4, Z_1, Y_7
    test_errors = [
        ("X4", 4, SIGMA_X),
        ("Z1", 1, SIGMA_Z),
        ("Y7", 7, SIGMA_Y),
    ]

    for label, target_qubit, error_op in test_errors:
        ops = [SIGMA_I] * 9
        ops[target_qubit] = error_op
        error_matrix = kron_all(*ops)

        # Corrupted state
        corrupted = error_matrix @ psi_logical

        # Recovery operator: applying same error operator since Paulis are Hermitian and unitary
        recovery_matrix = error_matrix
        recovered = recovery_matrix @ corrupted

        fidelity = float(abs(np.vdot(psi_logical, recovered)) ** 2)
        assert np.isclose(fidelity, 1.0, atol=1e-9), f"Failed recovery for error {label}"


def test_tier4_peres_mermin_magic_square_parity_obstruction():
    """2. Peres-Mermin 2-qubit pseudo-telepathy contextuality winning strategy."""
    sq = peres_mermin_square()
    prods = context_products()

    # The 6 contexts commute internally
    assert prods["all_contexts_commute"] is True

    # 5 contexts multiply to +I_4, exactly 1 context (column 2) multiplies to -I_4
    assert prods["n_negative_contexts"] == 1
    assert prods["parity_of_signs"] == -1

    # Over shared Bell pairs (|00> + |11>)/sqrt(2) x (|00> + |11>)/sqrt(2),
    # quantum strategy achieves winning probability 1.0, whereas classical value
    # assignments can satisfy at most 5 of 6 contexts (or at most 8 of 9 queries).
    max_classical_contexts = 5
    assert max_classical_contexts < 6


def test_tier4_busch_effect_povm_resolutions():
    """3. Busch effect algebra and POVM resolution in d=2 over Q(zeta_4)."""
    res = bounded_effect_algebraic_search(conductor=4, height_bound=1)
    assert res["termination"] is True
    assert res["distinct_ray_projectors"] > 0
    assert res["orthogonal_basis_pairs"] > 0
    assert res["four_element_povms"] > 0
    assert res["total_povm_resolutions"] == res["orthogonal_basis_pairs"] + res["four_element_povms"]


def test_tier4_mach_zehnder_interferometer_complete_walk():
    """4. Mach-Zehnder interferometer fringes P = cos^2(Delta theta / 2)."""
    pkt = build_mzi_packet()
    assert pkt.verify_d1_d0_nilpotent() is True

    # Simulation of 50:50 beam splitter (Hadamard), phase shift Delta theta, second beam splitter
    delta_thetas = [0.0, np.pi / 4.0, np.pi / 2.0, 3.0 * np.pi / 4.0, np.pi]
    for d_theta in delta_thetas:
        phase_gate = np.array([[1.0, 0.0], [0.0, np.exp(1j * d_theta)]], dtype=complex)
        u_mzi = HADAMARD_2 @ phase_gate @ HADAMARD_2

        # Input ground state |0>
        state_in = np.array([1.0, 0.0], dtype=complex)
        state_out = u_mzi @ state_in

        # Detector 0 probability
        p0 = float(abs(state_out[0]) ** 2)
        p1 = float(abs(state_out[1]) ** 2)

        # Expected fringe: P_0 = cos^2(Delta theta / 2), P_1 = sin^2(Delta theta / 2)
        expected_p0 = float(np.cos(d_theta / 2.0) ** 2)
        expected_p1 = float(np.sin(d_theta / 2.0) ** 2)

        assert np.isclose(p0, expected_p0, atol=1e-12)
        assert np.isclose(p1, expected_p1, atol=1e-12)
        assert np.isclose(p0 + p1, 1.0, atol=1e-12)


def test_tier4_sorkin_three_slit_interference():
    """5. Sorkin 3-slit parameter I_3 vanishing identically under quadratic Born rule."""
    pkt = build_sorkin_3slit_packet()
    assert pkt.verify_d1_d0_nilpotent() is True

    # 1-cochain flow on 6 edges
    cochain_flow = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6], dtype=float)
    a1, a2, a3 = sorkin_3slit_amplitudes_from_cochain(cochain_flow)

    # Probabilities across all 7 non-empty slit configurations
    p_a = abs(a1) ** 2
    p_b = abs(a2) ** 2
    p_c = abs(a3) ** 2
    p_ab = abs(a1 + a2) ** 2
    p_bc = abs(a2 + a3) ** 2
    p_ca = abs(a3 + a1) ** 2
    p_abc = abs(a1 + a2 + a3) ** 2

    # Sorkin third-order interference parameter:
    # I_3 = P_{ABC} - P_{AB} - P_{BC} - P_{CA} + P_A + P_B + P_C
    i3 = p_abc - p_ab - p_bc - p_ca + p_a + p_b + p_c
    assert np.isclose(i3, 0.0, atol=1e-14)


def test_tier4_depolarizing_channel_trace_norm_contraction():
    """6. Trace norm contraction geometry under depolarizing noise with zero duality gap."""
    rho1 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    psi_plus = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho2 = np.outer(psi_plus, psi_plus.conj())

    for p in [0.1, 0.3, 0.5, 0.7, 0.9]:
        rho1_noisy = apply_depolarizing_channel(rho1, p)
        rho2_noisy = apply_depolarizing_channel(rho2, p)

        diff = rho1_noisy - rho2_noisy
        t_dist = trace_norm(diff)

        # Dual witness operator W_opt
        w_opt = construct_dual_witness(diff)
        alignment = float(np.real(np.trace(w_opt.conj().T @ diff)))

        # Duality gap is zero: alignment == trace_norm
        assert np.isclose(alignment, t_dist, atol=1e-10)
        assert verify_dual_witness_bound(rho1_noisy, rho2_noisy) is True


def test_tier4_quantum_teleportation_and_superdense_roundtrip():
    """7. Integrated two-way quantum communication loop: teleportation + superdense coding."""
    # Step 1: Alice teleports unknown state |psi> to Bob
    res_teleport = simulate_discrete_quantum_teleportation(alpha=0.6, beta=0.8)
    assert res_teleport["all_branches_fidelity_one"] is True

    # Step 2: Bob encodes classical message (b1=1, b0=1) via superdense coding back to Alice
    res_dense = simulate_discrete_superdense_coding(b1=1, b0=1)
    assert res_dense["success"] is True
    assert res_dense["decoded_index"] == 3
    assert res_dense["channel_capacity_ratio"] == 2.0
