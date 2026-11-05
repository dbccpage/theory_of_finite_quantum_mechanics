"""Schatten p-norms, Ky Fan norms, and unitary invariance classification for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Callable, Sequence
import numpy as np

Gauge = Callable[[np.ndarray], float]


def singular_values(X: np.ndarray) -> np.ndarray:
    """Compute singular values in non-increasing order: s_1 >= s_2 >= ... >= s_n >= 0."""
    arr = np.asarray(X, dtype=complex)
    if arr.ndim != 2:
        raise ValueError("X must be a 2D matrix")
    s = np.linalg.svd(arr, compute_uv=False)
    return np.sort(s)[::-1]


def schatten_norm(X: np.ndarray, p: float = 1.0) -> float:
    """Compute Schatten p-norm ||X||_p = (sum_i s_i^p)^(1/p).

    p = 1: Trace norm (nuclear norm)
    p = 2: Frobenius norm (Hilbert-Schmidt norm)
    p = inf: Operator (spectral) norm
    """
    if p < 1.0:
        raise ValueError(f"Schatten parameter p must be >= 1.0, got {p}")
    s = singular_values(X)
    if np.isinf(p):
        return float(s[0]) if len(s) > 0 else 0.0
    if p == 1.0:
        return float(np.sum(s))
    if p == 2.0:
        return float(np.sqrt(np.sum(s**2)))
    return float(np.sum(s**p) ** (1.0 / p))


def ky_fan_norm(X: np.ndarray, k: int = 1) -> float:
    """Compute Ky Fan k-norm: sum of the k largest singular values.

    k = 1: Operator norm
    k = n: Trace norm
    """
    s = singular_values(X)
    n = len(s)
    if k < 1 or k > n:
        raise ValueError(f"k must be in [1, {n}], got {k}")
    return float(np.sum(s[:k]))


def is_unitarily_invariant(
    gauge: Gauge,
    dimension: int,
    n_probes: int = 20,
    seed: int = 42,
    atol: float = 1e-8,
) -> bool:
    """Test whether a matrix gauge j is unitarily invariant: j(U X V) = j(X).

    Probes random unitary matrices generated via Haar measure (QR of random Gaussian).
    """
    rng = np.random.default_rng(seed)

    def random_unitary(d: int) -> np.ndarray:
        z = (rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))) / np.sqrt(2.0)
        q, r = np.linalg.qr(z)
        d_diag = np.diagonal(r)
        ph = d_diag / np.abs(d_diag)
        return q * ph

    for _ in range(n_probes):
        # Sample random test matrix X
        x = (
            rng.normal(size=(dimension, dimension))
            + 1j * rng.normal(size=(dimension, dimension))
        ) / np.sqrt(2.0)
        j_x = gauge(x)
        if j_x <= 1e-12:
            continue

        u = random_unitary(dimension)
        v = random_unitary(dimension)

        j_uxv = gauge(u @ x @ v)
        if abs(j_uxv - j_x) / j_x > atol:
            return False

    return True


def cptp_schatten_contractivity_audit(
    channel_fn: Callable[[np.ndarray], np.ndarray],
    X: np.ndarray,
    p_values: Sequence[float] = (1.0, 1.5, 2.0, 3.0, np.inf),
) -> dict[float, tuple[float, float, bool]]:
    """Audit whether a CPTP channel contracts Schatten p-norms: ||Lambda(X)||_p <= ||X||_p.

    Returns dict mapping p -> (||X||_p, ||Lambda(X)||_p, is_contractive).
    For trace norm (p=1), contractivity is guaranteed for all CPTP channels.
    For p > 1, contractivity can fail on Hermitian trace-zero differences!
    """
    X_arr = np.asarray(X, dtype=complex)
    Y_arr = channel_fn(X_arr)

    results = {}
    for p in p_values:
        norm_x = schatten_norm(X_arr, p)
        norm_y = schatten_norm(Y_arr, p)
        # Contractive if ||Y||_p <= ||X||_p + tol
        is_cont = bool(norm_y <= norm_x + 1e-8)
        results[p] = (norm_x, norm_y, is_cont)

    return results
