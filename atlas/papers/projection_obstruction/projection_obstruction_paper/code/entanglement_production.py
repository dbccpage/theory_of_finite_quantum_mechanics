"""Finite NumPy diagnostics for entanglement and product-tangent projections.

These routines evaluate finite-dimensional formulas on supplied states. Their
source hashes and floating-point tests do not establish new publication
propositions or certify general concurrence and Lindblad statements.

AuthorityEffect: None.
"""

from __future__ import annotations

from math import log
from typing import Sequence

import numpy as np
import numpy.typing as npt

ComplexMatrix = npt.NDArray[np.complex128]
ComplexVector = npt.NDArray[np.complex128]

DEFAULT_ATOL = 1.0e-9


def trace_norm(matrix: ComplexMatrix) -> float:
    """Return Schatten-1 (trace) norm of a matrix."""
    return float(np.linalg.svd(matrix, compute_uv=False).sum())


def purity(rho: ComplexMatrix) -> float:
    """Return Tr(rho^2) of a density matrix."""
    return float(np.real(np.trace(rho @ rho)))


def linear_entropy(rho: ComplexMatrix) -> float:
    """Return linear entropy S_L(rho) = 1 - Tr(rho^2)."""
    return float(1.0 - purity(rho))


def renyi_entropy(rho: ComplexMatrix, alpha: float = 2.0) -> float:
    """Return Rényi-alpha entropy S_alpha(rho) = 1/(1-alpha) * ln(Tr(rho^alpha))."""
    if alpha == 2.0:
        p = purity(rho)
        if p <= 0.0:
            return 0.0
        return float(-log(p))
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 0.0]
    return float(1.0 / (1.0 - alpha) * log(np.sum(vals**alpha)))


def von_neumann_entropy(rho: ComplexMatrix) -> float:
    """Return von Neumann entropy S(rho) = -Tr(rho ln rho)."""
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 1.0e-15]
    return float(-np.sum(vals * np.log(vals)))


def partial_trace_bipartite(
    rho_ab: ComplexMatrix, dim_a: int, dim_b: int, keep: str
) -> ComplexMatrix:
    """Compute partial trace of a bipartite matrix, keeping 'a' or 'b'."""
    tensor = rho_ab.reshape(dim_a, dim_b, dim_a, dim_b)
    if keep == "a":
        return np.trace(tensor, axis1=1, axis2=3)
    elif keep == "b":
        return np.trace(tensor, axis1=0, axis2=2)
    raise ValueError("keep must be 'a' or 'b'")


def project_product_tangent(
    x_ab: ComplexMatrix, rho_a: ComplexMatrix, rho_b: ComplexMatrix
) -> ComplexMatrix:
    """Apply the product-retraction differential P_rho to bipartite variation x_ab.

    P_rho(X) = Tr_B(X) (x) rho_B + rho_A (x) Tr_A(X) - Tr(X) * (rho_A (x) rho_B).
    """
    dim_a = rho_a.shape[0]
    dim_b = rho_b.shape[0]
    tr_b = partial_trace_bipartite(x_ab, dim_a, dim_b, keep="a")
    tr_a = partial_trace_bipartite(x_ab, dim_a, dim_b, keep="b")
    tr_total = np.trace(x_ab)
    return np.kron(tr_b, rho_b) + np.kron(rho_a, tr_a) - tr_total * np.kron(rho_a, rho_b)


def project_normal(
    x_ab: ComplexMatrix, rho_a: ComplexMatrix, rho_b: ComplexMatrix
) -> ComplexMatrix:
    """Apply Q_rho = I - P_rho to bipartite variation x_ab."""
    return x_ab - project_product_tangent(x_ab, rho_a, rho_b)


def compute_edge_excitation_vector(
    u_a: ComplexVector, u_b: ComplexVector, h_ab: ComplexMatrix
) -> ComplexVector:
    """Compute the two-site excitation vector chi_e = (Q_a (x) Q_b) h_ab (u_a (x) u_b).

    Here Q_a = I - |u_a><u_a| and Q_b = I - |u_b><u_b|.
    """
    dim_a = len(u_a)
    dim_b = len(u_b)
    p_a = np.outer(u_a, u_a.conj())
    p_b = np.outer(u_b, u_b.conj())
    q_a = np.eye(dim_a, dtype=np.complex128) - p_a
    q_b = np.eye(dim_b, dtype=np.complex128) - p_b
    q_ab = np.kron(q_a, q_b)
    u_ab = np.kron(u_a, u_b)
    return q_ab @ (h_ab @ u_ab)


def compute_edge_normal_rate(u_a: ComplexVector, u_b: ComplexVector, h_ab: ComplexMatrix) -> float:
    """Return nu_e = 2 * ||chi_e||."""
    chi_e = compute_edge_excitation_vector(u_a, u_b, h_ab)
    return 2.0 * float(np.linalg.norm(chi_e))


def two_qubit_concurrence(rho: ComplexMatrix) -> float:
    """Compute Wootters concurrence C(rho) for a two-qubit density matrix."""
    if rho.shape != (4, 4):
        raise ValueError("rho must be 4x4 for two-qubit concurrence")
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    sy_sy = np.kron(sigma_y, sigma_y)
    rho_tilde = sy_sy @ rho.conj() @ sy_sy
    vals = np.linalg.eigvals(rho @ rho_tilde)
    vals_real = np.real(vals)
    vals_nonneg = np.maximum(vals_real, 0.0)
    sqrt_vals = np.sort(np.sqrt(vals_nonneg))[::-1]
    concurrence = sqrt_vals[0] - sqrt_vals[1] - sqrt_vals[2] - sqrt_vals[3]
    return float(max(0.0, concurrence))


def lindblad_dissipator(rho: ComplexMatrix, jump_ops: Sequence[ComplexMatrix]) -> ComplexMatrix:
    """Compute Lindblad dissipator sum_k (L_k rho L_k^dagger - 1/2 {L_k^dagger L_k, rho})."""
    result = np.zeros_like(rho, dtype=np.complex128)
    for l_k in jump_ops:
        l_k_dag = l_k.conj().T
        ldag_l = l_k_dag @ l_k
        result += l_k @ rho @ l_k_dag - 0.5 * (ldag_l @ rho + rho @ ldag_l)
    return result


def verify_lindblad_local_immunity(
    rho_a: ComplexMatrix,
    rho_b: ComplexMatrix,
    jump_ops_a: Sequence[ComplexMatrix],
    jump_ops_b: Sequence[ComplexMatrix],
    atol: float = DEFAULT_ATOL,
) -> tuple[float, float]:
    """Verify that local Lindblad dissipators on site A and B have zero projection under Q_e.

    Returns (||Q_e(D_a(rho_a) (x) rho_b)||_1, ||Q_e(rho_a (x) D_b(rho_b))||_1).
    Zero local normal projections do not imply unchanged concurrence growth
    under Markovian noise. This function checks only the tangent identity.
    """
    d_a = lindblad_dissipator(rho_a, jump_ops_a)
    d_b = lindblad_dissipator(rho_b, jump_ops_b)

    term_a = np.kron(d_a, rho_b)
    term_b = np.kron(rho_a, d_b)

    q_term_a = project_normal(term_a, rho_a, rho_b)
    q_term_b = project_normal(term_b, rho_a, rho_b)

    norm_a = trace_norm(q_term_a)
    norm_b = trace_norm(q_term_b)

    return norm_a, norm_b
