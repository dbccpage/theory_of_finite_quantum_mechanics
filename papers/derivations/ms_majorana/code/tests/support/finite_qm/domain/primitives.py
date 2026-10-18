r"""
Finite matrix primitives for quantum physics.

AuthorityEffect: None.

Canonical Implementation: omega_engine_projects.ms_majorana.code.tests.support.finite_qm.domain.primitives
"""

from __future__ import annotations
from typing import Tuple

import numpy as np

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


def is_density_matrix(rho: np.ndarray, atol: float = 1e-9) -> bool:
    r"""True iff ``rho`` is Hermitian, positive semidefinite, and has unit trace."""
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
        return False
    if not np.allclose(rho, dagger(rho), atol=atol):
        return False
    if not np.isclose(float(np.real(np.trace(rho))), 1.0, atol=atol):
        return False
    evals = np.linalg.eigvalsh(rho)
    return bool(np.all(evals >= -atol))


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
]
