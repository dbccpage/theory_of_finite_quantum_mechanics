r"""
Finite matrix primitives for quantum physics.

AuthorityEffect: None.

"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Sequence, Tuple

import numpy as np

from .gaussian_rational import Gaussian

I2 = np.eye(2, dtype=complex)
SIGMA_I = I2
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)
HADAMARD_2 = (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
PHASE_S = np.array([[1.0, 0.0], [0.0, 1.0j]], dtype=complex)


def kron_all(*matrices: np.ndarray | list[np.ndarray]) -> np.ndarray:
    """Computes Kronecker product of an arbitrary sequence or list of matrices."""
    if len(matrices) == 1 and isinstance(matrices[0], (list, tuple)):
        matrices = tuple(matrices[0])
    if not matrices:
        raise ValueError("kron_all requires at least one matrix.")
    res = matrices[0]
    for m in matrices[1:]:
        res = np.kron(res, m)
    return res


def trace_norm(m: np.ndarray) -> float:
    r"""Schatten 1-norm :math:`\|M\|_1 = \operatorname{Tr}\sqrt{M^\dagger M}`."""
    return float(np.sum(np.linalg.svd(m, compute_uv=False)))


def operator_norm(m: np.ndarray) -> float:
    r"""Schatten :math:`\infty`-norm :math:`\|M\|_\infty`."""
    return float(np.max(np.linalg.svd(m, compute_uv=False)))


def partial_trace_b(m: np.ndarray, da: int = 2, db: int = 2) -> np.ndarray:
    r""":math:`\operatorname{Tr}_b : B(H_a \otimes H_b) \to B(H_a)`."""
    return np.einsum("ikjk->ij", m.reshape(da, db, da, db))


def partial_trace_a(m: np.ndarray, da: int = 2, db: int = 2) -> np.ndarray:
    r""":math:`\operatorname{Tr}_a : B(H_a \otimes H_b) \to B(H_b)`."""
    return np.einsum("kikj->ij", m.reshape(da, db, da, db))


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    r""":math:`[A, B] = AB - BA`."""
    return a @ b - b @ a


def dagger(m: np.ndarray) -> np.ndarray:
    r""":math:`M^\dagger`."""
    return m.conj().T


def to_exact_matrix(m: Any) -> list[list[Gaussian]]:
    """Convert a 2D matrix structure into a square list of lists of Gaussian rationals.

    Accepts lists of lists, tuples, numpy arrays, or objects with an .entries attribute.
    Entries may be of type Fraction, int, str, float, complex, or Gaussian.
    Raises ValueError if input is not a non-empty square matrix.
    """
    if hasattr(m, "entries"):
        rows = [list(r) for r in m.entries]
    elif isinstance(m, np.ndarray):
        rows = m.tolist()
    elif isinstance(m, (list, tuple)):
        rows = []
        for row in m:
            if not isinstance(row, (list, tuple, np.ndarray)):
                raise ValueError("Each matrix row must be a sequence")
            rows.append(list(row))
    else:
        raise ValueError(f"Expected 2D matrix input, got {type(m).__name__}")

    n = len(rows)
    if n == 0 or any(not isinstance(row, list) or len(row) != n for row in rows):
        raise ValueError("Expected a non-empty square matrix")

    try:
        return [[Gaussian.of(val) for val in row] for row in rows]
    except (ValueError, TypeError, OverflowError, ZeroDivisionError) as e:
        raise ValueError(f"Cannot convert matrix entry to Gaussian rational: {e}") from e


def exact_dagger(m: Sequence[Sequence[Any]]) -> list[list[Gaussian]]:
    """Exact conjugate transpose over Q(i): (M^dagger)_{ij} = conj(M_{ji})."""
    mat = to_exact_matrix(m)
    n = len(mat)
    return [[mat[j][i].conjugate() for j in range(n)] for i in range(n)]


def exact_trace(m: Sequence[Sequence[Any]]) -> Gaussian:
    """Exact trace over Q(i): Tr(M) = sum_i M_{ii}."""
    mat = to_exact_matrix(m)
    n = len(mat)
    tr = Gaussian.of(0)
    for i in range(n):
        tr = tr + mat[i][i]
    return tr


def exact_is_psd(m: Sequence[Sequence[Any]]) -> bool:
    """Determine exact positive semidefiniteness (M >= 0) over Q(i).

    Uses exact diagonal congruence reduction with symmetric pivoting over Q(i).
    Returns True iff matrix is Hermitian and all congruence pivots are nonnegative.
    """
    try:
        mat = to_exact_matrix(m)
    except (ValueError, TypeError):
        return False
    n = len(mat)

    for i in range(n):
        if mat[i][i].imag != 0:
            return False
        for j in range(i + 1, n):
            if mat[i][j] != mat[j][i].conjugate():
                return False

    A = [[mat[i][j] for j in range(n)] for i in range(n)]
    for step in range(n):
        for i in range(step, n):
            if A[i][i].real < 0:
                return False

        pivot_idx = -1
        for i in range(step, n):
            if A[i][i].real > 0:
                pivot_idx = i
                break

        if pivot_idx == -1:
            for i in range(step, n):
                for j in range(step, n):
                    if i != j and (A[i][j].real != 0 or A[i][j].imag != 0):
                        return False
            return True

        if pivot_idx != step:
            A[step], A[pivot_idx] = A[pivot_idx], A[step]
            for r in range(n):
                A[r][step], A[r][pivot_idx] = A[r][pivot_idx], A[r][step]

        pivot_val = A[step][step].real
        for i in range(step + 1, n):
            factor = A[i][step] / pivot_val
            if factor.real != 0 or factor.imag != 0:
                for j in range(step + 1, n):
                    A[i][j] = A[i][j] - factor * A[step][j]

    return True


def is_exact_rational_density_matrix(matrix: Any) -> bool:
    """Exact rational density operator predicate.

    Verifies:
      1. Square non-empty dimension d >= 1
      2. Exact Hermiticity: M = M^dagger with strictly real diagonal
      3. Exact unit trace: Tr(M) == Fraction(1, 1) and Im(Tr(M)) == 0
      4. Exact positive semidefiniteness (M >= 0)
    Without floating-point tolerances.
    """
    try:
        mat = to_exact_matrix(matrix)
    except (ValueError, TypeError):
        return False

    tr = exact_trace(mat)
    if tr.imag != 0 or tr.real != Fraction(1, 1):
        return False

    return exact_is_psd(mat)


def exact_purity(rho: Sequence[Sequence[Any]]) -> Fraction:
    """Exact purity Tr(rho^2) in Q for an exact density operator."""
    mat = to_exact_matrix(rho)
    n = len(mat)
    pur = Gaussian.of(0)
    for i in range(n):
        for j in range(n):
            pur = pur + mat[i][j] * mat[j][i]
    if pur.imag != 0:
        raise ValueError("Non-Hermitian purity evaluation")
    return pur.real


def is_density_matrix(rho: Any, atol: float = 1e-9) -> bool:
    r"""True iff ``rho`` is Hermitian, positive semidefinite, and has unit trace.

    Dispatches to exact rational verification when atol == 0.0 or when given an
    exact rational matrix structure.
    """
    if atol == 0.0:
        return is_exact_rational_density_matrix(rho)
    if isinstance(rho, np.ndarray) and np.issubdtype(rho.dtype, np.inexact):
        if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
            return False
        if not np.allclose(rho, dagger(rho), atol=atol):
            return False
        if not np.isclose(float(np.real(np.trace(rho))), 1.0, atol=atol):
            return False
        evals = np.linalg.eigvalsh(rho)
        return bool(np.all(evals >= -atol))
    return is_exact_rational_density_matrix(rho)


def purity(rho: np.ndarray) -> float:
    r""":math:`\operatorname{Tr}(\rho^2) \in (0, 1]`."""
    return float(np.real(np.trace(rho @ rho)))


def von_neumann_entropy(rho: np.ndarray, base: float = 2.0) -> float:
    r""":math:`S(\rho) = -\sum_i \lambda_i \log \lambda_i`."""
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-12]
    if evals.size == 0:
        return 0.0
    return float(-np.sum(evals * np.log(evals) / np.log(base)))


def mutual_information(rho_ab: np.ndarray, da: int = 2, db: int = 2) -> float:
    r""":math:`I(A{:}B) = S(\rho_a) + S(\rho_b) - S(\rho_{ab})`."""
    rho_a = partial_trace_b(rho_ab, da, db)
    rho_b = partial_trace_a(rho_ab, da, db)
    return (
        von_neumann_entropy(rho_a)
        + von_neumann_entropy(rho_b)
        - von_neumann_entropy(rho_ab)
    )


def marginals(rho_ab: np.ndarray, da: int = 2, db: int = 2) -> Tuple[np.ndarray, np.ndarray]:
    r"""``(Tr_b rho, Tr_a rho)``."""
    return partial_trace_b(rho_ab, da, db), partial_trace_a(rho_ab, da, db)


def pure_state(amplitudes: np.ndarray) -> np.ndarray:
    r""":math:`|\psi\rangle\langle\psi|`."""
    psi = np.asarray(amplitudes, dtype=complex)
    nrm = float(np.linalg.norm(psi))
    if nrm == 0.0:
        raise ValueError("pure_state: zero amplitude vector has no ray")
    psi = psi / nrm
    return np.outer(psi, psi.conj())


def ket00(da: int = 2, db: int = 2) -> np.ndarray:
    r"""The product state :math:`|00\rangle\langle 00|`."""
    psi = np.zeros(da * db, dtype=complex)
    psi[0] = 1.0
    return np.outer(psi, psi.conj())


def bell_state() -> np.ndarray:
    r"""The maximally entangled :math:`(|00\rangle + |11\rangle)/\sqrt 2`."""
    psi = np.zeros(4, dtype=complex)
    psi[0] = psi[3] = 1.0 / np.sqrt(2.0)
    return np.outer(psi, psi.conj())


__all__ = [
    "I2",
    "SIGMA_I",
    "SIGMA_X",
    "SIGMA_Y",
    "SIGMA_Z",
    "HADAMARD_2",
    "PHASE_S",
    "kron_all",
    "trace_norm",
    "operator_norm",
    "partial_trace_b",
    "partial_trace_a",
    "commutator",
    "dagger",
    "is_density_matrix",
    "purity",
    "von_neumann_entropy",
    "mutual_information",
    "marginals",
    "pure_state",
    "ket00",
    "bell_state",
    "to_exact_matrix",
    "exact_dagger",
    "exact_trace",
    "exact_is_psd",
    "is_exact_rational_density_matrix",
    "exact_purity",
]
