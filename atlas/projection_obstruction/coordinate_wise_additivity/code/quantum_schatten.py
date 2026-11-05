"""Non-Commutative Quantum Operator Additivity & Schatten Norms for GS-000 Extension.

AuthorityEffect: None. Operator-algebraic generalization of coordinate additivity to B(H).
"""

from __future__ import annotations

from typing import Callable

import numpy as np
from coord_additivity import _dimension, _nonnegative_scalar

OperatorSeminorm = Callable[[np.ndarray], float]


def _finite_matrix(a: np.ndarray) -> np.ndarray:
    m = np.asarray(a, dtype=complex)
    if m.ndim != 2 or not np.all(np.isfinite(m)):
        raise ValueError("operator must be a finite two-dimensional matrix")
    return m


def _density_matrix(a: np.ndarray) -> np.ndarray:
    m = _finite_matrix(a)
    if not m.shape[0] or m.shape[0] != m.shape[1]:
        raise ValueError("density matrix must be nonempty and square")
    if not np.allclose(m, m.conj().T, rtol=0, atol=1e-9):
        raise ValueError("density matrix must be Hermitian")
    if not np.isclose(np.trace(m), 1, rtol=0, atol=1e-9):
        raise ValueError("density matrix must have trace one")
    if np.linalg.eigvalsh(m).min() < -1e-9:
        raise ValueError("density matrix must be positive semidefinite")
    return m


def singular_values(a: np.ndarray) -> np.ndarray:
    """Compute singular values of matrix A in descending order."""
    m = _finite_matrix(a)
    if m.size == 0:
        return np.array([], dtype=float)
    s = np.linalg.svd(m, compute_uv=False)
    return np.asarray(s, dtype=float)


def schatten_norm(a: np.ndarray, p: float | str = 1) -> float:
    """Compute Schatten p-norm ||A||_p = (sum sigma_i^p)^{1/p}.

    p=1: Trace norm (Schatten 1-norm).
    p=2: Frobenius norm (Schatten 2-norm / Hilbert-Schmidt norm).
    p=inf / 'inf': Operator / spectral norm.
    0 < p < 1: Schatten quasi-norm, not a norm.
    """
    p_val = float(p)
    if np.isnan(p_val) or p_val <= 0:
        raise ValueError("p must be > 0 and finite, or positive infinity")
    s = singular_values(a)
    if s.size == 0:
        return 0.0
    if p == 1 or p == 1.0:
        return float(np.sum(s))
    elif p == 2 or p == 2.0:
        return float(np.sqrt(np.sum(s**2)))
    elif p == np.inf or p == "inf":
        return float(np.max(s))
    else:
        return float(np.sum(s**p_val) ** (1.0 / p_val))


def trace_norm(a: np.ndarray) -> float:
    """Compute trace norm ||A||_1 = Tr(sqrt(A^dagger A))."""
    return schatten_norm(a, p=1)


def are_mutually_orthogonal_support(a: np.ndarray, b: np.ndarray, tol: float = 1e-9) -> bool:
    """Check if operators A and B have mutually orthogonal support:

    A B^dagger = 0 and A^dagger B = 0.
    This is the non-commutative analogue of disjoint coordinate support.
    """
    tol = _nonnegative_scalar(tol, "tolerance")
    ma = _finite_matrix(a)
    mb = _finite_matrix(b)
    if ma.shape != mb.shape:
        raise ValueError("Matrix dimensions must match")

    ab_dagger = ma @ mb.conj().T
    a_dagger_b = ma.conj().T @ mb

    norm_1 = np.linalg.norm(ab_dagger)
    norm_2 = np.linalg.norm(a_dagger_b)
    return bool(norm_1 <= tol and norm_2 <= tol)


def is_unitarily_invariant(
    nu: OperatorSeminorm,
    a: np.ndarray,
    num_trials: int = 5,
    seed: int = 42,
    tol: float = 1e-9,
) -> bool:
    """Probe ν(U A V) = ν(A) on listed random trials, not universally."""
    num_trials = _dimension(num_trials, positive=True)
    tol = _nonnegative_scalar(tol, "tolerance")
    m = _finite_matrix(a)
    n_rows, n_cols = m.shape
    base_val = _nonnegative_scalar(nu(m), "diagnostic output")

    rng = np.random.default_rng(seed)
    for _ in range(num_trials):
        # Generate Haar-random unitary via QR of random Gaussian matrix
        q_u, _ = np.linalg.qr((rng.normal(size=(n_rows, n_rows)) + 1j * rng.normal(size=(n_rows, n_rows))))
        q_v, _ = np.linalg.qr((rng.normal(size=(n_cols, n_cols)) + 1j * rng.normal(size=(n_cols, n_cols))))

        transformed = q_u @ m @ q_v
        if abs(_nonnegative_scalar(nu(transformed), "diagnostic output") - base_val) > tol:
            return False
    return True


def is_orthogonal_operator_additive(
    nu: OperatorSeminorm,
    dim: int,
    num_trials: int = 5,
    seed: int = 42,
    tol: float = 1e-9,
) -> bool:
    """Probe orthogonal additivity on finite rank-one trials, not universally."""
    dim = _dimension(dim, positive=True)
    if dim < 2:
        raise ValueError("dimension must be at least two for two orthogonal probes")
    num_trials = _dimension(num_trials, positive=True)
    tol = _nonnegative_scalar(tol, "tolerance")
    rng = np.random.default_rng(seed)
    for _ in range(num_trials):
        # Generate random orthonormal vectors u1, u2 and v1, v2
        q_u, _ = np.linalg.qr(rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim)))
        q_v, _ = np.linalg.qr(rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim)))

        u1, u2 = q_u[:, 0:1], q_u[:, 1:2]
        v1, v2 = q_v[:, 0:1], q_v[:, 1:2]

        # Rank-1 operators with orthogonal left and right support
        s1, s2 = abs(rng.normal()), abs(rng.normal())
        a = s1 * (u1 @ v1.conj().T)
        b = s2 * (u2 @ v2.conj().T)

        assert are_mutually_orthogonal_support(a, b, tol=tol)

        val_sum = _nonnegative_scalar(nu(a + b), "diagnostic output")
        val_add = (_nonnegative_scalar(nu(a), "diagnostic output")
                   + _nonnegative_scalar(nu(b), "diagnostic output"))
        if abs(val_sum - val_add) > tol:
            return False
    return True


def quantum_state_trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    """Compute trace distance D(rho, sigma) = 1/2 ||rho - sigma||_1 between density matrices."""
    r = _density_matrix(rho)
    s = _density_matrix(sigma)
    if r.shape != s.shape:
        raise ValueError("density matrix dimensions must match")
    diff = r - s
    return 0.5 * trace_norm(diff)


def cptp_depolarizing_channel(rho: np.ndarray, p: float) -> np.ndarray:
    """Convex depolarizing model for a density matrix and mixing weight 0 <= p <= 1.

    This deliberately exposes the convex-mixture range, not every admissible
    parameterization of the depolarizing channel.
    """
    p = _nonnegative_scalar(p, "mixing weight")
    if p > 1:
        raise ValueError("mixing weight must be at most one")
    r = _density_matrix(rho)
    d = r.shape[0]
    eye = np.eye(d, dtype=complex)
    tr_r = np.trace(r)
    return (1.0 - p) * r + p * (eye / d) * tr_r
