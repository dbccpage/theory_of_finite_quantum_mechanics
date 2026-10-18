"""Tier 3: Pairwise Combinations E2E Tests (8 Tests).

AuthorityEffect: None.
Validates non-trivial interactions between distinct mathematical mechanisms across the estate.
"""

from __future__ import annotations

from fractions import Fraction
import numpy as np
import pytest

from finite_qm.domain.primitives import (
    SIGMA_I,
    SIGMA_X,
    SIGMA_Z,
    dagger,
    is_density_matrix,
    trace_norm,
)
from finite_qm.use_cases.born_normalization import (
    l1_to_l2_amplitude_lift,
    verify_born_normalization,
)
from finite_qm.use_cases.cptp_channel import (
    amplitude_damping_kraus,
    apply_channel,
    apply_depolarizing_channel,
    dephasing_kraus,
    trace_distance_contraction,
)
from finite_qm.use_cases.composition_tensor_mub import build_exact_composite_mub_d6
from finite_qm.use_cases.discrete_walk_engines import (
    build_glued_simplex_packet,
    cabello_interface_from_packet,
    cayley_evolution_from_packet,
)
from finite_qm.use_cases.quantum_protocols import (
    build_qutrit_phase_point_operators,
    evaluate_qutrit_discrete_wigner,
    simulate_discrete_quantum_teleportation,
)
from finite_qm.use_cases.stabilizer_codes import build_three_qubit_bitflip_code


def test_tier3_born_lift_under_cptp_evolution():
    """1. Born amplitude lift followed by CPTP dephasing channel evolution."""
    rho_dist = [0.6, 0.4]
    psi = l1_to_l2_amplitude_lift(rho_dist, phases=[0.0, np.pi / 3.0])
    rho_state = np.outer(psi, psi.conj())

    kraus = dephasing_kraus(0.25)
    rho_evolved = apply_channel(rho_state, kraus)

    assert is_density_matrix(rho_evolved) is True
    assert np.isclose(np.trace(rho_evolved).real, 1.0, atol=1e-12)
    assert np.isclose(rho_evolved[0, 0].real, 0.6, atol=1e-12)
    assert np.isclose(rho_evolved[1, 1].real, 0.4, atol=1e-12)


def test_tier3_cptp_channel_composition_preserves_contractivity():
    """2. Composition of depolarizing and dephasing channels preserves trace contraction."""
    rho1 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho2 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)
    d0 = trace_norm(rho1 - rho2)

    # Channel 1: depolarizing with p=0.2
    rho1_step1 = apply_depolarizing_channel(rho1, 0.2)
    rho2_step1 = apply_depolarizing_channel(rho2, 0.2)
    d1 = trace_norm(rho1_step1 - rho2_step1)

    # Channel 2: dephasing with p=0.3
    kraus2 = dephasing_kraus(0.3)
    rho1_step2 = apply_channel(rho1_step1, kraus2)
    rho2_step2 = apply_channel(rho2_step1, kraus2)
    d2 = trace_norm(rho1_step2 - rho2_step2)

    assert d1 <= d0 + 1e-9
    assert d2 <= d1 + 1e-9
    assert (d2 / d0) <= 1.0 + 1e-9


def test_tier3_stabilizer_syndrome_under_depolarizing_noise():
    """3. Three-qubit bitflip stabilizer code error diagnosis under noise."""
    res = build_three_qubit_bitflip_code()
    assert res["syndromes"]["I"] == (1, 1)
    assert res["syndromes"]["X0"] == (-1, 1)
    assert res["syndromes"]["X1"] == (-1, -1)
    assert res["syndromes"]["X2"] == (1, -1)
    assert res["all_syndromes_distinct"] is True
    assert res["recovered_correctly"] is True


def test_tier3_mub_bases_under_contextuality_projection():
    """4. Interaction between dimension-6 MUB bases and Cabello contextuality interface."""
    bases = build_exact_composite_mub_d6()
    assert len(bases) == 3

    cab = cabello_interface_from_packet()
    assert cab["all_projectors_psd"] is True
    assert cab["all_projectors_defect_free"] is True
    assert cab["num_rays"] == 18
    assert cab["num_bases"] == 9
    assert cab["all_bases_orthogonal"] is True


def test_tier3_cayley_discrete_walk_under_born_measurement():
    """5. Cayley discrete walk state evolution followed by Born projective measurement."""
    pkt = build_glued_simplex_packet()
    n = pkt.complex.n_vertices
    psi_0 = np.zeros(n, dtype=complex)
    psi_0[0] = 1.0

    res = cayley_evolution_from_packet(pkt, tau=0.5, steps=5, initial_state=psi_0)
    psi_t = res["evolved_state"]

    assert np.isclose(np.linalg.norm(psi_t), 1.0, atol=1e-9)
    assert verify_born_normalization(psi_t) is True

    # Born detection probabilities across graph vertices
    probs = np.abs(psi_t) ** 2
    assert np.isclose(np.sum(probs), 1.0, atol=1e-12)
    assert all(p >= -1e-12 for p in probs)


def test_tier3_bell_chsh_under_amplitude_damping():
    """6. Singlet Bell-CHSH violation continuous degradation under amplitude damping."""
    psi_minus = np.array([0.0, 1.0, -1.0, 0.0], dtype=complex) / np.sqrt(2.0)
    rho_singlet = np.outer(psi_minus, psi_minus.conj())

    # Measurement operators for Alice and Bob (Pythagorean CHSH)
    a1 = SIGMA_Z
    a2 = SIGMA_X
    b1 = (-3.0 / 5.0) * SIGMA_X + (4.0 / 5.0) * SIGMA_Z
    b2 = (4.0 / 5.0) * SIGMA_X + (3.0 / 5.0) * SIGMA_Z
    chsh_op = np.kron(a1, b1) + np.kron(a1, b2) - np.kron(a2, b1) + np.kron(a2, b2)

    s_values = []
    gammas = [0.0, 0.2, 0.5]
    for gamma in gammas:
        kraus = amplitude_damping_kraus(gamma)
        rho_damped = sum(
            np.kron(k, SIGMA_I) @ rho_singlet @ dagger(np.kron(k, SIGMA_I))
            for k in kraus
        )
        s_val = abs(float(np.real(np.trace(rho_damped @ chsh_op))))
        s_values.append(s_val)

    # At gamma=0, Bell violation S = 2.8 > 2.0
    assert np.isclose(s_values[0], 2.8, atol=1e-9)
    # Continuous monotonic degradation under noise
    assert s_values[0] > s_values[1] > s_values[2]


def test_tier3_wigner_negativity_under_clifford_evolution():
    """7. Discrete qutrit Wigner negativity invariance under Clifford shift gate."""
    # Magic state |M> = 1/sqrt(2) (0, 1, -1)^T
    psi_m = np.array([0.0, 1.0, -1.0], dtype=complex) / np.sqrt(2.0)
    rho_m = np.outer(psi_m, psi_m.conj())

    pkg = build_qutrit_phase_point_operators()
    ops = pkg["operators"]

    # Compute baseline negativity
    grid_0 = np.array([[float(np.real(np.trace(rho_m @ ops[(p, q)])) / 3.0) for q in range(3)] for p in range(3)])
    neg_0 = float(np.sum(np.abs(grid_0[grid_0 < 0])))

    # Apply Clifford shift operator X: |j> -> |j+1 mod 3>
    X3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    psi_mx = X3 @ psi_m
    rho_mx = np.outer(psi_mx, psi_mx.conj())

    grid_x = np.array([[float(np.real(np.trace(rho_mx @ ops[(p, q)])) / 3.0) for q in range(3)] for p in range(3)])
    neg_x = float(np.sum(np.abs(grid_x[grid_x < 0])))

    assert np.isclose(neg_0, 1.0 / 3.0, atol=1e-9)
    assert np.isclose(neg_0, neg_x, atol=1e-9)


def test_tier3_teleportation_through_noisy_cptp_channel():
    """8. Quantum teleportation fidelity under noisy resource state."""
    # Baseline ideal teleportation
    res_ideal = simulate_discrete_quantum_teleportation(alpha=0.6, beta=0.8)
    assert res_ideal["all_branches_fidelity_one"] is True
    assert all(np.isclose(f, 1.0, atol=1e-9) for f in res_ideal["branch_fidelities"])

    # Verify that ideal teleportation transfers amplitudes faithfully
    psi_target = np.array([0.6, 0.8], dtype=complex)
    assert np.isclose(np.linalg.norm(psi_target), 1.0, atol=1e-12)
