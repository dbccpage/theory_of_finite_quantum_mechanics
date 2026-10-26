"""
Inline Code Companion for PO-000 (projection_obstruction_paper.md)
=================================================================

This module extracts and packages all inline Python code snippets embedded
in the PO-000 manuscript (projection_obstruction_paper.md) into clean, standalone,
executable functions for automated verification and reviewer evaluation.
"""

from typing import Dict, Tuple
import numpy as np


def run_example_61_bell_state_leakage(theta: float = np.pi / 8) -> Tuple[float, float]:
    """
    Executes the inline code block from Example 6.1 (manuscript lines 885-893).

    Computes the trace norm of the product retraction defect Delta(t) = rho(t) - Pi rho(t)
    for a Bell state evolved under H = J Z_A Z_B.

    Returns:
        Tuple[float, float]: (eigenvalue_sum, analytical_formula_value)
    """
    c, s = np.cos(theta), np.sin(theta)
    a, b = c * c * s * s, c * s
    Delta = np.array([[a, 0, 0, 1j * b],
                      [0, -a, 0, 0],
                      [0, 0, -a, 0],
                      [-1j * b, 0, 0, a]], dtype=complex)
    eig_sum = float(np.sum(np.abs(np.linalg.eigvalsh(Delta))))
    formula_val = float(2 * abs(b) + 2 * a)
    return eig_sum, formula_val


def run_example_62_tfim_normal_rate(J: float = 1.0) -> Tuple[float, float]:
    """
    Executes the inline code block from Example 6.2 (manuscript lines 908-920).

    Computes the raw normal rate nu_e = ||n_e||_1 for the 1D transverse-field
    Ising model under bond term H_e = -J Z_a Z_b with initial state |+><+|.

    Returns:
        Tuple[float, float]: (norm_eigval_sum, nu_e)
    """
    plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
    rp = np.outer(plus, plus)  # |+><+|
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    He = -J * np.kron(Z, Z)  # J bond term
    rab = np.kron(rp, rp)
    rhodot = -1j * (He @ rab - rab @ He)

    def ptr(M: np.ndarray, keep: int) -> np.ndarray:
        M_reshaped = M.reshape(2, 2, 2, 2)
        if keep == 0:
            return np.einsum('ijkj->ik', M_reshaped)
        else:
            return np.einsum('ijil->jl', M_reshaped)

    Ne = rhodot - np.kron(ptr(rhodot, 0), rp) - np.kron(rp, ptr(rhodot, 1))
    eig_sum = float(np.sum(np.abs(np.linalg.eigvalsh(Ne))))
    nu_e = 2.0 * abs(J)
    return eig_sum, nu_e


def run_section_745_tripartite_all_green_diagram() -> Tuple[float, list]:
    """
    Executes the inline code block from Section 7.4.5 (manuscript lines 1105-1116).

    Computes the rawrepresented defect I(s) and observer loss vector J^\alpha(s)
    for a 3-vertex 2-simplex cover diagram with watched edge restrictions.

    Returns:
        Tuple[float, list]: (raw_defect_I, observer_loss_list_J)
    """
    e = np.eye(3)
    s = {
        "u1": e[0], "u2": e[1], "u3": e[2],
        "x12": np.zeros(3), "x23": np.zeros(3), "x31": np.zeros(3)
    }
    edges = [("x12", "u1"), ("x12", "u2"), ("x23", "u2"), ("x23", "u3"), ("x31", "u3"), ("x31", "u1")]
    watcher = {("x12", "u1"): 0, ("x12", "u2"): 1, ("x23", "u2"): 1, ("x23", "u3"): 2, ("x31", "u3"): 2, ("x31", "u1"): 0}

    d = {ed: s[ed[1]] - s[ed[0]] for ed in edges}  # identity restrictions
    I_val = float(sum(np.abs(v).sum() for v in d.values()))
    J_vals = [float(sum(np.abs(np.delete(d[ed], a)).sum() for ed in edges if watcher[ed] == a)) for a in range(3)]
    return I_val, J_vals

