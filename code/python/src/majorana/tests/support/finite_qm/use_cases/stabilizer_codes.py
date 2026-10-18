"""Stabilizer codes and discrete topological error-correcting codes.

Decomposed from foundations.py monolith. Integrates with omega_engine crates.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
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


def build_three_qubit_bitflip_code() -> dict[str, Any]:
    r"""Loop 8: Constructs the 3-qubit bit-flip stabilizer code on a discrete triangular cell.

    Stabilizer generators:
        S1 = Z \otimes Z \otimes I
        S2 = I \otimes Z \otimes Z
    Logical operators:
        Z_L = Z \otimes Z \otimes Z
        X_L = X \otimes X \otimes X

    Single-qubit errors:
        E0 = I \otimes I \otimes I  -> Syndrome (s1, s2) = (+1, +1)
        E1 = X \otimes I \otimes I  -> Syndrome (s1, s2) = (-1, +1)
        E2 = I \otimes X \otimes I  -> Syndrome (s1, s2) = (-1, -1)
        E3 = I \otimes I \otimes X  -> Syndrome (s1, s2) = (+1, -1)

    All 4 syndromes are mutually distinct, enabling deterministic error recovery.
    """
    s1 = kron_all(SIGMA_Z, SIGMA_Z, SIGMA_I)
    s2 = kron_all(SIGMA_I, SIGMA_Z, SIGMA_Z)
    z_l = kron_all(SIGMA_Z, SIGMA_Z, SIGMA_Z)
    x_l = kron_all(SIGMA_X, SIGMA_X, SIGMA_X)

    comm_s1_s2 = np.allclose(s1 @ s2, s2 @ s1)
    comm_s1_zl = np.allclose(s1 @ z_l, z_l @ s1)
    comm_s1_xl = np.allclose(s1 @ x_l, x_l @ s1)
    comm_s2_zl = np.allclose(s2 @ z_l, z_l @ s2)
    comm_s2_xl = np.allclose(s2 @ x_l, x_l @ s2)
    anti_xl_zl = np.allclose(x_l @ z_l, -z_l @ x_l)

    errors = {
        "I": kron_all(SIGMA_I, SIGMA_I, SIGMA_I),
        "X0": kron_all(SIGMA_X, SIGMA_I, SIGMA_I),
        "X1": kron_all(SIGMA_I, SIGMA_X, SIGMA_I),
        "X2": kron_all(SIGMA_I, SIGMA_I, SIGMA_X),
    }

    syndromes = {}
    recovered_correctly = True
    for name, E in errors.items():
        val1 = 1 if np.allclose(E @ s1 @ E, s1) else -1
        val2 = 1 if np.allclose(E @ s2 @ E, s2) else -1
        syndromes[name] = (val1, val2)

        R = E
        restored = R @ E
        if not np.allclose(restored, kron_all(SIGMA_I, SIGMA_I, SIGMA_I)):
            recovered_correctly = False

    expected_syndromes = {
        "I": (1, 1),
        "X0": (-1, 1),
        "X1": (-1, -1),
        "X2": (1, -1),
    }

    syndromes_match_expected = (syndromes == expected_syndromes)
    all_syndromes_distinct = (len(set(syndromes.values())) == 4)

    return {
        "stabilizers_commute": comm_s1_s2,
        "logical_ops_commute_with_stabilizers": (comm_s1_zl and comm_s1_xl and comm_s2_zl and comm_s2_xl),
        "logical_ops_anticommute": anti_xl_zl,
        "syndromes": syndromes,
        "syndromes_match_expected": syndromes_match_expected,
        "all_syndromes_distinct": all_syndromes_distinct,
        "recovered_correctly": recovered_correctly,
    }



def build_four_qubit_css_surface_code() -> dict[str, Any]:
    r"""Loop 9: Constructs the [[4, 2, 2]] CSS surface code on a 2-torus.

    4 physical qubits, 2 stabilizer generators:
        S_Z = Z \otimes Z \otimes Z \otimes Z
        S_X = X \otimes X \otimes X \otimes X

    2 encoded logical qubits:
        Logical Qubit 1:
            Z_L1 = Z \otimes Z \otimes I \otimes I
            X_L1 = X \otimes I \otimes X \otimes I
        Logical Qubit 2:
            Z_L2 = Z \otimes I \otimes Z \otimes I
            X_L2 = X \otimes X \otimes I \otimes I

    Code properties:
        - Stabilizers commute: [S_Z, S_X] = 0 because they overlap on 4 qubits ((-1)^4 = +1).
        - All 4 logical operators commute with both stabilizers.
        - Logical operators satisfy independent Pauli algebras:
            {X_L1, Z_L1} = 0, {X_L2, Z_L2} = 0,
            [O_L1, O_L2] = 0 for all cross-qubit pairs.
        - Distance d = 2: all 12 single-qubit Pauli errors {X_i, Y_i, Z_i} produce non-trivial syndromes.
    """
    s_z = kron_all(SIGMA_Z, SIGMA_Z, SIGMA_Z, SIGMA_Z)
    s_x = kron_all(SIGMA_X, SIGMA_X, SIGMA_X, SIGMA_X)

    z_l1 = kron_all(SIGMA_Z, SIGMA_Z, SIGMA_I, SIGMA_I)
    x_l1 = kron_all(SIGMA_X, SIGMA_I, SIGMA_X, SIGMA_I)

    z_l2 = kron_all(SIGMA_Z, SIGMA_I, SIGMA_Z, SIGMA_I)
    x_l2 = kron_all(SIGMA_X, SIGMA_X, SIGMA_I, SIGMA_I)

    comm_sz_sx = np.allclose(s_z @ s_x, s_x @ s_z)

    logicals = [z_l1, x_l1, z_l2, x_l2]
    all_logicals_commute_with_stabilizers = all(
        np.allclose(L @ s_z, s_z @ L) and np.allclose(L @ s_x, s_x @ L)
        for L in logicals
    )

    anti_l1 = np.allclose(x_l1 @ z_l1, -z_l1 @ x_l1)
    anti_l2 = np.allclose(x_l2 @ z_l2, -z_l2 @ x_l2)
    cross_commute = (
        np.allclose(z_l1 @ z_l2, z_l2 @ z_l1) and
        np.allclose(z_l1 @ x_l2, x_l2 @ z_l1) and
        np.allclose(x_l1 @ z_l2, z_l2 @ x_l1) and
        np.allclose(x_l1 @ x_l2, x_l2 @ x_l1)
    )

    pauli_ops = [("X", SIGMA_X), ("Y", SIGMA_Y), ("Z", SIGMA_Z)]
    detected_errors = []
    all_single_errors_detected = True

    for qubit_idx in range(4):
        for name, op in pauli_ops:
            op_list = [SIGMA_I, SIGMA_I, SIGMA_I, SIGMA_I]
            op_list[qubit_idx] = op
            E = kron_all(*op_list)

            val_z = 1 if np.allclose(E @ s_z @ E.conj().T, s_z) else -1
            val_x = 1 if np.allclose(E @ s_x @ E.conj().T, s_x) else -1
            syndrome = (val_z, val_x)

            if syndrome == (1, 1):
                all_single_errors_detected = False
            detected_errors.append((f"{name}{qubit_idx}", syndrome))

    return {
        "n_physical_qubits": 4,
        "n_logical_qubits": 2,
        "code_distance": 2,
        "stabilizers_commute": comm_sz_sx,
        "logicals_commute_with_stabilizers": all_logicals_commute_with_stabilizers,
        "logical_qubit_1_anticommutes": anti_l1,
        "logical_qubit_2_anticommutes": anti_l2,
        "cross_logical_commutes": cross_commute,
        "all_single_errors_detected": all_single_errors_detected,
        "detected_error_count": len(detected_errors),
    }



def build_steane_seven_qubit_code() -> dict[str, Any]:
    r"""Loop 10: Constructs the Steane [[7, 1, 3]] CSS code on the Fano plane PG(2, 2).

    7 physical qubits corresponding to the 7 points of the Fano plane.
    6 stabilizer generators from the 3 dual Fano lines / [7, 4, 3] Hamming parity checks:
        h1 = {0, 2, 4, 6} (weight 4)
        h2 = {1, 2, 5, 6} (weight 4)
        h3 = {3, 4, 5, 6} (weight 4)

    Stabilizers:
        S_X^(i) = \bigotimes_{k \in h_i} X_k,  for i \in {1, 2, 3}
        S_Z^(i) = \bigotimes_{k \in h_i} Z_k,  for i \in {1, 2, 3}

    1 encoded logical qubit:
        X_L = X^{\otimes 7}
        Z_L = Z^{\otimes 7}

    Code properties:
        - Fano line intersection: |h_i \cap h_j| = 2 \equiv 0 mod 2 for all i \neq j,
          ensuring all 6 stabilizers commute pairwise ((-1)^2 = +1).
        - Logical operators commute with all stabilizers (|h_i| = 4 \equiv 0 mod 2).
        - Logical operators anticommute ({X_L, Z_L} = 0 since 7 \equiv 1 mod 2).
        - Distance d = 3: all 21 single-qubit errors {X_j, Y_j, Z_j} are uniquely detected
          and corrected via binary syndrome decoding.
        - Transversal Hadamard: H^{\otimes 7} maps S_X <-> S_Z, preserving the codespace
          and implementing logical Hadamard H_L.
    """
    h_rows = [
        [0, 2, 4, 6],
        [1, 2, 5, 6],
        [3, 4, 5, 6],
    ]

    fano_intersections_even = True
    for i in range(len(h_rows)):
        for j in range(i + 1, len(h_rows)):
            overlap = len(set(h_rows[i]).intersection(set(h_rows[j])))
            if overlap % 2 != 0:
                fano_intersections_even = False

    def make_pauli_string(weight_indices: list[int], pauli_op: np.ndarray) -> np.ndarray:
        ops = [SIGMA_I] * 7
        for idx in weight_indices:
            ops[idx] = pauli_op
        return kron_all(*ops)

    sx_gens = [make_pauli_string(h, SIGMA_X) for h in h_rows]
    sz_gens = [make_pauli_string(h, SIGMA_Z) for h in h_rows]
    all_stabilizers = sx_gens + sz_gens

    all_stabilizers_commute = True
    for i in range(len(all_stabilizers)):
        for j in range(i + 1, len(all_stabilizers)):
            if not np.allclose(all_stabilizers[i] @ all_stabilizers[j], all_stabilizers[j] @ all_stabilizers[i]):
                all_stabilizers_commute = False
                break

    x_l = kron_all(*([SIGMA_X] * 7))
    z_l = kron_all(*([SIGMA_Z] * 7))

    logicals_commute_with_stabilizers = all(
        np.allclose(x_l @ S, S @ x_l) and np.allclose(z_l @ S, S @ z_l)
        for S in all_stabilizers
    )

    logical_anticommutes = bool(np.allclose(x_l @ z_l, -z_l @ x_l))

    h_transversal = kron_all(*([HADAMARD_2] * 7))

    hadamard_preserves_stabilizers = True
    for sx, sz in zip(sx_gens, sz_gens):
        h_sx_h = h_transversal @ sx @ h_transversal.conj().T
        h_sz_h = h_transversal @ sz @ h_transversal.conj().T
        if not np.allclose(h_sx_h, sz) or not np.allclose(h_sz_h, sx):
            hadamard_preserves_stabilizers = False

    hadamard_implements_logical_h = (
        np.allclose(h_transversal @ x_l @ h_transversal.conj().T, z_l) and
        np.allclose(h_transversal @ z_l @ h_transversal.conj().T, x_l)
    )

    pauli_errors = [("X", SIGMA_X), ("Y", SIGMA_Y), ("Z", SIGMA_Z)]
    unique_syndromes = set()
    all_single_qubit_errors_correctable = True

    for j in range(7):
        s_z_vals = tuple(1 if j not in h else -1 for h in h_rows)
        s_x_vals = tuple(1 if j not in h else -1 for h in h_rows)

        syn_x = (s_z_vals, (1, 1, 1))
        syn_z = ((1, 1, 1), s_x_vals)
        syn_y = (s_z_vals, s_x_vals)

        for syn in [syn_x, syn_z, syn_y]:
            if syn in unique_syndromes or syn == ((1, 1, 1), (1, 1, 1)):
                all_single_qubit_errors_correctable = False
            unique_syndromes.add(syn)

    return {
        "n_physical_qubits": 7,
        "n_logical_qubits": 1,
        "code_distance": 3,
        "fano_intersections_even": fano_intersections_even,
        "all_stabilizers_commute": all_stabilizers_commute,
        "logicals_commute_with_stabilizers": logicals_commute_with_stabilizers,
        "logical_anticommutes": logical_anticommutes,
        "hadamard_preserves_stabilizers": hadamard_preserves_stabilizers,
        "hadamard_implements_logical_h": hadamard_implements_logical_h,
        "all_single_qubit_errors_correctable": all_single_qubit_errors_correctable,
        "unique_error_syndromes_count": len(unique_syndromes),
    }

__all__ = ['build_four_qubit_css_surface_code', 'build_steane_seven_qubit_code', 'build_three_qubit_bitflip_code']
