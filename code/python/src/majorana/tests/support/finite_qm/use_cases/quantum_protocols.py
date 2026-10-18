"""Discrete quantum information protocols, nonlocality, and Wigner negativity.

Decomposed from foundations.py monolith. Integrates with omega_engine crates.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Any

import numpy as np
import scipy.linalg

from omega_engine_projects.ms_majorana.code.tests.support.finite_qm.domain.primitives import (
    I2,
    SIGMA_I,
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    HADAMARD_2,
    PHASE_S,
    kron_all,
)


def evaluate_discrete_pythagorean_bell_chsh() -> dict[str, Any]:
    """Loop 4: Refutes local realism using exact rational Pythagorean measurement bases.
    
    Singlet state |psi^-> has correlation E(a, b) = - <a, b>.
    Alice measures along standard basis:
        a1 = (0, 1), a2 = (1, 0)
    Bob measures along Pythagorean (3, 4, 5) basis:
        b1 = (-3/5, 4/5), b2 = (4/5, 3/5)
    
    Both bases are strictly orthonormal in Q^2:
        ||a1||^2 = ||a2||^2 = ||b1||^2 = ||b2||^2 = 1,
        <a1, a2> = 0, <b1, b2> = (-12 + 12)/25 = 0.
    
    Correlations:
        E(a1, b1) = -4/5
        E(a1, b2) = -3/5
        E(a2, b1) = +3/5
        E(a2, b2) = -4/5
    
    CHSH Bell operator value:
        S = |E(a1, b1) + E(a1, b2) - E(a2, b1) + E(a2, b2)|
          = |-4/5 - 3/5 - 3/5 - 4/5| = |-14/5| = 14/5 = 2.8.
    
    Since 2.8 > 2.0 (local realism bound), this refutes local realism in exact rational arithmetic.
    """
    a1 = (Fraction(0), Fraction(1))
    a2 = (Fraction(1), Fraction(0))
    b1 = (Fraction(-3, 5), Fraction(4, 5))
    b2 = (Fraction(4, 5), Fraction(3, 5))

    # Check orthonormality
    norm_sq_a1 = a1[0]**2 + a1[1]**2
    norm_sq_a2 = a2[0]**2 + a2[1]**2
    norm_sq_b1 = b1[0]**2 + b1[1]**2
    norm_sq_b2 = b2[0]**2 + b2[1]**2
    dot_a = a1[0] * a2[0] + a1[1] * a2[1]
    dot_b = b1[0] * b2[0] + b1[1] * b2[1]

    assert norm_sq_a1 == norm_sq_a2 == norm_sq_b1 == norm_sq_b2 == 1
    assert dot_a == dot_b == 0

    # Correlations E(a, b) = - dot(a, b)
    e11 = -(a1[0] * b1[0] + a1[1] * b1[1])  # -4/5
    e12 = -(a1[0] * b2[0] + a1[1] * b2[1])  # -3/5
    e21 = -(a2[0] * b1[0] + a2[1] * b1[1])  # +3/5
    e22 = -(a2[0] * b2[0] + a2[1] * b2[1])  # -4/5

    s_frac = abs(e11 + e12 - e21 + e22)
    assert s_frac == Fraction(14, 5)

    # Check all 16 local hidden variable deterministic assignments in {-1, +1}^4
    classical_values = []
    all_classical_bounded = True
    for a1_val in (-1, 1):
        for a2_val in (-1, 1):
            for b1_val in (-1, 1):
                for b2_val in (-1, 1):
                    val = a1_val * b1_val + a1_val * b2_val + a2_val * b1_val - a2_val * b2_val
                    classical_values.append(val)
                    if abs(val) > 2:
                        all_classical_bounded = False

    return {
        "is_orthonormal": True,
        "e11": e11,
        "e12": e12,
        "e21": e21,
        "e22": e22,
        "s_chsh_fraction": s_frac,
        "s_chsh_float": float(s_frac),
        "classical_bound": 2,
        "violates_local_realism": (s_frac > 2),
        "all_classical_bounded_by_2": all_classical_bounded,
        "max_classical_value": max(classical_values),
        "min_classical_value": min(classical_values),
    }


def derive_bell_singlet_correlation(
    u: tuple[float | Fraction, float | Fraction] | np.ndarray,
    v: tuple[float | Fraction, float | Fraction] | np.ndarray,
) -> dict[str, Any]:
    """Loop 4: Derives Bell correlation from singlet state vector and Pauli observables.
    
    Singlet state: |psi^-> = 1/sqrt(2) (|01> - |10>).
    Density matrix: rho = |psi^-> <psi^-|.
    Observables: A(u) = u_x * sigma_x + u_z * sigma_z
                 B(v) = v_x * sigma_x + v_z * sigma_z
    Expectation: <A ⊗ B> = Tr(rho (A(u) ⊗ B(v))) = - (u_x v_x + u_z v_z) = - u · v.
    """
    ux, uz = float(u[0]), float(u[1])
    vx, vz = float(v[0]), float(v[1])

    A_u = ux * SIGMA_X + uz * SIGMA_Z
    B_v = vx * SIGMA_X + vz * SIGMA_Z
    AB = np.kron(A_u, B_v)

    psi_minus = np.array([0.0, 1.0, -1.0, 0.0], dtype=complex) / np.sqrt(2.0)
    rho_singlet = np.outer(psi_minus, psi_minus.conj())

    trace_val = float(np.real(np.trace(rho_singlet @ AB)))
    vector_val = float(np.real(psi_minus.conj().T @ AB @ psi_minus))
    expected_dot = - (ux * vx + uz * vz)

    is_consistent = bool(np.isclose(trace_val, expected_dot) and np.isclose(vector_val, expected_dot))
    return {
        "u": (ux, uz),
        "v": (vx, vz),
        "correlation_trace": trace_val,
        "correlation_vector": vector_val,
        "expected_negative_dot": expected_dot,
        "is_derived_from_singlet": is_consistent,
    }


# --------------------------------------------------------------------------- #
# Loop 5: Pell-Pythagorean Triple Hierarchy & Tsirelson Rational Deficit
# --------------------------------------------------------------------------- #

def evaluate_pell_pythagorean_tsirelson_convergence() -> dict[str, Any]:
    """Loop 5: Evaluates the sequence of primitive Pythagorean triples converging to the Tsirelson bound.
    
    The optimal continuous CHSH angle theta = pi/8 satisfies tan(pi/8) = sqrt(2) - 1.
    Pell number convergent n / m = 5 / 12 yields the primitive Pythagorean triple:
        (m^2 - n^2, 2mn, m^2 + n^2) = (144 - 25, 120, 144 + 25) = (119, 120, 169).
    
    Orthonormal measurement vectors in Q^2 at scale 169:
        b1 = (-119/169, 120/169), b2 = (120/169, 119/169)
        <b1, b2> = (-119*120 + 120*119)/169^2 = 0.
        ||b1||^2 = (119^2 + 120^2)/169^2 = 28561/28561 = 1.
    
    Singlet correlations with standard basis a1 = (0, 1), a2 = (1, 0):
        E(a1, b1) = -120/169
        E(a1, b2) = -119/169
        E(a2, b1) = +119/169
        E(a2, b2) = -120/169
    
    Bell-CHSH value:
        S = |E(a1, b1) + E(a1, b2) - E(a2, b1) + E(a2, b2)|
          = 478 / 169 ~ 2.82840236686.
    
    Comparison with bounds:
      - Classical bound: 2 (exceeded by 478/169 - 2 = 140/169 ~ 0.8284).
      - Tsirelson bound: 2 sqrt(2) ~ 2.82842712475.
      - Exact rational squared deficit:
        8 - (478 / 169)^2 = (8 * 28561 - 228484) / 28561 = 4 / 28561 ~ 0.00014005.
    """
    scale = 169
    a_sq = 119**2
    b_sq = 120**2
    c_sq = scale**2
    assert a_sq + b_sq == c_sq == 28561

    # Exact correlations
    e11 = Fraction(-120, scale)
    e12 = Fraction(-119, scale)
    e21 = Fraction(119, scale)
    e22 = Fraction(-120, scale)

    s_frac = abs(e11 + e12 - e21 + e22)
    assert s_frac == Fraction(478, scale)

    s_squared = s_frac**2
    tsirelson_sq = Fraction(8, 1)
    squared_deficit = tsirelson_sq - s_squared
    assert squared_deficit == Fraction(4, 28561)

    return {
        "scale": scale,
        "triple": (119, 120, 169),
        "is_pythagorean": True,
        "s_chsh_fraction": s_frac,
        "s_chsh_float": float(s_frac),
        "classical_bound": 2,
        "classical_violation": float(s_frac - 2),
        "tsirelson_bound_float": float(2.0 * np.sqrt(2.0)),
        "tsirelson_gap_float": float(2.0 * np.sqrt(2.0) - float(s_frac)),
        "squared_tsirelson_deficit": squared_deficit,
        "strictly_below_tsirelson": (s_squared < 8),
    }


# --------------------------------------------------------------------------- #
# Loop 6: Discrete Clifford Group Normalizer & T-Gate Orbit Departure
# --------------------------------------------------------------------------- #

def evaluate_clifford_pauli_conjugations() -> dict[str, Any]:
    """Loop 6: Verifies exact Clifford group normalizer action on the single-qubit Pauli group.
    
    Generators:
        H = 1/sqrt(2) [[1, 1], [1, -1]]
        S = [[1, 0], [0, i]]
    Pauli operators:
        X = [[0, 1], [1, 0]]
        Y = [[0, -i], [i, 0]]
        Z = [[1, 0], [0, -1]]
    
    Conjugation laws:
        H X H^dagger = Z
        H Z H^dagger = X
        H Y H^dagger = -Y
        S X S^dagger = Y
        S Y S^dagger = -X
        S Z S^dagger = Z
    """
    eye = SIGMA_I
    sigma_x = SIGMA_X
    sigma_y = SIGMA_Y
    sigma_z = SIGMA_Z
    h_mat = HADAMARD_2
    s_mat = PHASE_S

    # Unitary checks
    assert np.allclose(h_mat @ h_mat.conj().T, eye)
    assert np.allclose(s_mat @ s_mat.conj().T, eye)

    # Conjugations by H
    h_x_h = h_mat @ sigma_x @ h_mat.conj().T
    h_z_h = h_mat @ sigma_z @ h_mat.conj().T
    h_y_h = h_mat @ sigma_y @ h_mat.conj().T

    h_preserves = bool(
        np.allclose(h_x_h, sigma_z) and
        np.allclose(h_z_h, sigma_x) and
        np.allclose(h_y_h, -sigma_y)
    )

    # Conjugations by S
    s_x_s = s_mat @ sigma_x @ s_mat.conj().T
    s_y_s = s_mat @ sigma_y @ s_mat.conj().T
    s_z_s = s_mat @ sigma_z @ s_mat.conj().T

    s_preserves = bool(
        np.allclose(s_x_s, sigma_y) and
        np.allclose(s_y_s, -sigma_x) and
        np.allclose(s_z_s, sigma_z)
    )

    # Group orders
    h_squared_is_eye = bool(np.allclose(h_mat @ h_mat, eye))
    s_fourth_is_eye = bool(np.allclose(np.linalg.matrix_power(s_mat, 4), eye))

    return {
        "h_preserves_pauli": h_preserves,
        "s_preserves_pauli": s_preserves,
        "h_squared_is_eye": h_squared_is_eye,
        "s_fourth_is_eye": s_fourth_is_eye,
        "is_clifford_normalizer": (h_preserves and s_preserves),
    }


def evaluate_t_gate_orbit_departure() -> dict[str, Any]:
    """Loop 6: Demonstrates that the non-Clifford T-gate strictly departs from the Pauli group.
    
    T = [[1, 0], [0, e^(i pi / 4)]].
    Conjugating X by T yields:
        T X T^dagger = 1/sqrt(2) (X + Y).
    This linear combination has trace overlap <= 1/sqrt(2) < 1 with all Pauli operators,
    establishing that T is NOT in the Clifford normalizer of the Pauli group.
    """
    sigma_x = SIGMA_X
    sigma_y = SIGMA_Y
    sigma_z = SIGMA_Z
    eye = SIGMA_I

    zeta8 = np.exp(1j * np.pi / 4.0)
    t_mat = np.array([[1.0, 0.0], [0.0, zeta8]], dtype=complex)

    # Conjugate X by T
    t_x_t = t_mat @ sigma_x @ t_mat.conj().T
    expected_superposition = (sigma_x + sigma_y) / np.sqrt(2.0)
    is_equal_superposition = bool(np.allclose(t_x_t, expected_superposition))

    # Test overlap with all 16 generalized single-qubit Pauli elements {+/- I, +/- iI, +/- X, ...}
    pauli_basis = [eye, sigma_x, sigma_y, sigma_z]
    phases = [1.0, -1.0, 1.0j, -1.0j]

    max_overlap = 0.0
    for p in pauli_basis:
        for ph in phases:
            target = ph * p
            overlap = float(np.abs(np.trace(target.conj().T @ t_x_t)) / 2.0)
            if overlap > max_overlap:
                max_overlap = overlap

    is_outside_pauli = bool(max_overlap < 1.0 - 1e-6)

    return {
        "is_equal_superposition": is_equal_superposition,
        "max_pauli_overlap": max_overlap,
        "expected_overlap": float(1.0 / np.sqrt(2.0)),
        "is_outside_pauli_group": is_outside_pauli,
        "non_clifford_certified": (is_equal_superposition and is_outside_pauli),
    }


# --------------------------------------------------------------------------- #
# Loop 7: Qutrit Discrete Wigner Distribution & Magic State Negativity
# --------------------------------------------------------------------------- #

def build_qutrit_phase_point_operators() -> dict[str, Any]:
    """Loop 7: Constructs the 9 discrete Gross phase-point operators on qutrit phase space F_3 x F_3.
    
    Dimension d = 3.
    Shift operator: X |j> = |j + 1 mod 3>.
    Clock operator: Z |j> = omega^j |j> where omega = exp(2 pi i / 3).
    Parity operator: P |j> = |-j mod 3>.
    Phase-point operators:
        A(p, q) = X^p Z^q P Z^(-q) X^(-p).
    
    Properties:
        Tr(A(p, q)) = 1
        Tr(A(p, q) A(p', q')) = 3 delta_{p p'} delta_{q q'}
        sum_{p, q} A(p, q) = 3 I_3
    """
    omega = np.exp(2j * np.pi / 3.0)
    X = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    Z = np.array([[1, 0, 0], [0, omega, 0], [0, 0, omega**2]], dtype=complex)
    P = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    I3 = np.eye(3, dtype=complex)

    ops = {}
    sum_ops = np.zeros((3, 3), dtype=complex)
    for p in range(3):
        for q in range(3):
            xp = np.linalg.matrix_power(X, p)
            zq = np.linalg.matrix_power(Z, q)
            # D(p, q) = tau^(-pq) X^p Z^q, but A(p, q) = X^p Z^q P Z^(-q) X^(-p)
            apq = xp @ zq @ P @ zq.conj().T @ xp.conj().T
            assert np.allclose(apq, apq.conj().T)
            assert np.isclose(np.trace(apq), 1.0)
            ops[(p, q)] = apq
            sum_ops += apq

    assert np.allclose(sum_ops, 3.0 * I3)

    return {
        "dimension": 3,
        "n_points": 9,
        "operators": ops,
        "completeness_verified": True,
    }


def evaluate_qutrit_discrete_wigner(state_type: str = "magic") -> dict[str, Any]:
    """Loop 7: Evaluates the discrete Wigner distribution of a qutrit state.
    
    Supported states:
      - 'stabilizer': |0> = (1, 0, 0)^T.
      - 'magic': |M> = 1/sqrt(2) (0, 1, -1)^T (eigenstate of P with eigenvalue -1).
    
    Wigner formula: W(p, q) = 1/3 Tr(rho A(p, q)).
    For |0>, W(p, q) >= 0 for all (p, q).
    For |M>, W(0, 0) = 1/3 <M| P |M> = 1/3 (-1) = -1/3 < 0,
    witnessing non-classicality and contextuality.
    """
    pkg = build_qutrit_phase_point_operators()
    ops = pkg["operators"]

    if state_type == "stabilizer":
        psi = np.array([1.0, 0.0, 0.0], dtype=complex)
    elif state_type == "magic":
        psi = np.array([0.0, 1.0, -1.0], dtype=complex) / np.sqrt(2.0)
    else:
        raise ValueError(f"Unknown state_type: {state_type}")

    rho = np.outer(psi, psi.conj())
    w_grid = np.zeros((3, 3), dtype=float)

    for p in range(3):
        for q in range(3):
            val = float(np.real(np.trace(rho @ ops[(p, q)])) / 3.0)
            w_grid[p, q] = val

    sum_w = float(np.sum(w_grid))
    min_w = float(np.min(w_grid))
    has_negativity = bool(min_w < -1e-9)
    negativity = float(np.sum(np.abs(w_grid[w_grid < 0])))

    return {
        "state_type": state_type,
        "w_grid": w_grid.tolist(),
        "w00": float(w_grid[0, 0]),
        "sum_w": sum_w,
        "min_w": min_w,
        "has_negativity": has_negativity,
        "negativity": negativity,
    }


def simulate_discrete_quantum_teleportation(
    alpha: complex = 3.0 / 5.0,
    beta: complex = 4.0 / 5.0,
) -> dict[str, Any]:
    r"""Loop 11: Simulates the standard 3-qubit quantum teleportation protocol with exact recovery.
    
    Qubit 0 (Alice): Input state |\psi> = \alpha |0> + \beta |1>.
    Qubits 1 (Alice) & 2 (Bob): Shared Bell pair |\Phi^+> = 1/\sqrt{2} (|00> + |11>).
    
    Protocol:
      1. Entangled resource preparation: CNOT(1 -> 2) (H_1 |0> \otimes |0>).
      2. Alice's Bell measurement: CNOT(0 -> 1) followed by H_0.
      3. Alice measures qubits 0 and 1, obtaining classical bits (m0, m1) \in {0, 1}^2.
      4. Bob receives (m0, m1) via classical communication channel (2 cbits).
      5. Bob applies recovery gate R(m0, m1) = Z^(m0) X^(m1) to qubit 2.
    
    In all 4 measurement branches:
      - Branch (0, 0): Bob has |\psi>, R = I -> |\psi>.
      - Branch (0, 1): Bob has X|\psi>, R = X -> X^2 |\psi> = |\psi>.
      - Branch (1, 0): Bob has Z|\psi>, R = Z -> Z^2 |\psi> = |\psi>.
      - Branch (1, 1): Bob has XZ|\psi>, R = ZX -> ZX(XZ|\psi>) = |\psi>.
    
    All 4 branches achieve exact fidelity F = |\langle\psi|\psi_{rec}\rangle|^2 = 1.0.
    """
    # Normalize input state
    norm = np.sqrt(abs(alpha)**2 + abs(beta)**2)
    a = alpha / norm
    b = beta / norm
    psi_target = np.array([a, b], dtype=complex)

    # Initial state |psi> \otimes |0> \otimes |0> in 3-qubit Hilbert space (dim 8)
    psi_init = np.kron(psi_target, np.array([1.0, 0.0, 0.0, 0.0], dtype=complex))

    # Bell pair preparation on qubits 1 and 2
    # H on qubit 1
    h1 = kron_all(SIGMA_I, HADAMARD_2, SIGMA_I)
    # CNOT on qubits 1 and 2
    cnot12 = np.zeros((8, 8), dtype=complex)
    for q0 in range(2):
        for q1 in range(2):
            for q2 in range(2):
                in_idx = (q0 << 2) | (q1 << 1) | q2
                out_idx = (q0 << 2) | (q1 << 1) | (q2 ^ q1)
                cnot12[out_idx, in_idx] = 1.0

    state_after_bell = cnot12 @ (h1 @ psi_init)

    # Alice's Bell analysis on qubits 0 and 1
    # CNOT(0 -> 1)
    cnot01 = np.zeros((8, 8), dtype=complex)
    for q0 in range(2):
        for q1 in range(2):
            for q2 in range(2):
                in_idx = (q0 << 2) | (q1 << 1) | q2
                out_idx = (q0 << 2) | ((q1 ^ q0) << 1) | q2
                cnot01[out_idx, in_idx] = 1.0

    # H on qubit 0
    h0 = kron_all(HADAMARD_2, SIGMA_I, SIGMA_I)
    state_before_meas = h0 @ (cnot01 @ state_after_bell)

    # Measurement projections on qubits 0 and 1
    branch_results = {}
    all_branches_fid_one = True

    for m0 in (0, 1):
        for m1 in (0, 1):
            # Projector on qubits 0 and 1
            proj_01 = np.zeros((4, 4), dtype=complex)
            proj_idx = (m0 << 1) | m1
            proj_01[proj_idx, proj_idx] = 1.0
            p_full = np.kron(proj_01, SIGMA_I)

            unnorm_post = p_full @ state_before_meas
            prob = float(np.real(np.vdot(unnorm_post, unnorm_post)))
            assert np.isclose(prob, 0.25, atol=1e-9)

            post_state = unnorm_post / np.sqrt(prob)

            idx0 = (m0 << 2) | (m1 << 1) | 0
            idx1 = (m0 << 2) | (m1 << 1) | 1
            bob_unrec = np.array([post_state[idx0], post_state[idx1]], dtype=complex)

            r_mat = np.eye(2, dtype=complex)
            if m1 == 1:
                r_mat = SIGMA_X @ r_mat
            if m0 == 1:
                r_mat = SIGMA_Z @ r_mat

            bob_rec = r_mat @ bob_unrec
            fidelity = float(abs(np.vdot(psi_target, bob_rec))**2)

            if not np.isclose(fidelity, 1.0, atol=1e-9):
                all_branches_fid_one = False

            branch_results[(m0, m1)] = {
                "probability": prob,
                "fidelity": fidelity,
            }

    return {
        "all_branches_fidelity_one": all_branches_fid_one,
        "n_branches": len(branch_results),
        "branch_probabilities": [b["probability"] for b in branch_results.values()],
        "branch_fidelities": [b["fidelity"] for b in branch_results.values()],
        "classical_bit_cost": 2,
    }


# --------------------------------------------------------------------------- #
# Loop 12: Superdense Coding & Dense Channel Capacity over Z[i]
# --------------------------------------------------------------------------- #

def simulate_discrete_superdense_coding(b1: int = 0, b0: int = 0) -> dict[str, Any]:
    r"""Loop 12: Simulates the superdense coding protocol transmitting 2 classical bits via 1 qubit.
    
    Setup:
      - Alice and Bob share Bell pair |\Phi^+> = 1/\sqrt{2} (|00> + |11>).
      - Alice applies local Pauli gate U(b1, b0) = Z^(b1) X^(b0) to qubit 0:
          (0, 0) -> |\Phi^+> = 1/\sqrt{2} (|00> + |11>)
          (0, 1) -> |\Psi^+> = 1/\sqrt{2} (|10> + |01>)
          (1, 0) -> |\Phi^-> = 1/\sqrt{2} (|00> - |11>)
          (1, 1) -> |\Psi^-> = 1/\sqrt{2} (|10> - |01>) (up to global phase)
      - Alice sends qubit 0 to Bob.
      - Bob performs Bell basis measurement (CNOT(0 -> 1) then H_0) and measures in computational basis.
      - Decoded bits (m1, m0) match (b1, b0) with probability 1.0.
    
    Orthogonality:
      The 4 unnormalized Bell state vectors in Z^4 have Gram matrix exactly 2 * I_4.
    """
    if b1 not in (0, 1) or b0 not in (0, 1):
        raise ValueError("Classical bits b1 and b0 must be in {0, 1}")

    # Initial Bell pair |\Phi^+>
    phi_plus = np.array([1.0, 0.0, 0.0, 1.0], dtype=complex) / np.sqrt(2.0)

    # Alice's local encoding U = Z^b1 X^b0 on qubit 0
    u_alice = np.eye(2, dtype=complex)
    if b0 == 1:
        u_alice = SIGMA_X @ u_alice
    if b1 == 1:
        u_alice = SIGMA_Z @ u_alice

    u_full = np.kron(u_alice, SIGMA_I)
    encoded_state = u_full @ phi_plus

    # Bob's decoding circuit: CNOT(0 -> 1) followed by H_0
    cnot01 = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ], dtype=complex)

    h0 = np.kron(HADAMARD_2, SIGMA_I)
    bob_state = h0 @ (cnot01 @ encoded_state)

    # Probabilities in computational basis {|00>, |01>, |10>, |11>}
    probs = [float(abs(bob_state[i])**2) for i in range(4)]
    expected_idx = (b1 << 1) | b0
    success = bool(np.isclose(probs[expected_idx], 1.0, atol=1e-9))

    # All 4 Bell states Gram matrix verification
    bell_vectors = {
        (0, 0): np.kron(SIGMA_I, SIGMA_I) @ phi_plus,
        (0, 1): np.kron(SIGMA_X, SIGMA_I) @ phi_plus,
        (1, 0): np.kron(SIGMA_Z, SIGMA_I) @ phi_plus,
        (1, 1): np.kron(SIGMA_Z @ SIGMA_X, SIGMA_I) @ phi_plus,
    }

    gram = np.zeros((4, 4), dtype=complex)
    states_list = [bell_vectors[(0, 0)], bell_vectors[(0, 1)], bell_vectors[(1, 0)], bell_vectors[(1, 1)]]
    for i in range(4):
        for j in range(4):
            gram[i, j] = np.vdot(states_list[i], states_list[j])

    gram_is_identity = bool(np.allclose(gram, np.eye(4)))

    return {
        "input_bits": (b1, b0),
        "decoded_index": expected_idx,
        "probabilities": probs,
        "success": success,
        "gram_is_identity": gram_is_identity,
        "transmitted_qubits": 1,
        "decoded_cbits": 2,
        "channel_capacity_ratio": 2.0,
    }

__all__ = ['build_qutrit_phase_point_operators', 'derive_bell_singlet_correlation', 'evaluate_clifford_pauli_conjugations', 'evaluate_discrete_pythagorean_bell_chsh', 'evaluate_pell_pythagorean_tsirelson_convergence', 'evaluate_qutrit_discrete_wigner', 'evaluate_t_gate_orbit_departure', 'simulate_discrete_quantum_teleportation', 'simulate_discrete_superdense_coding']
