"""Exact finite norms and typed induced operator norms for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Callable, Sequence
import numpy as np

Gauge = Callable[[np.ndarray], float]


def l1(x: np.ndarray) -> float:
    """Standard l1 norm on R^n."""
    if np.iscomplexobj(x):
        raise TypeError("Real vector space inputs required")
    arr = np.asarray(x, dtype=float)
    return float(np.sum(np.abs(arr.ravel())))


def l2(x: np.ndarray) -> float:
    """Standard l2 (Euclidean) norm on R^n."""
    if np.iscomplexobj(x):
        raise TypeError("Real vector space inputs required")
    arr = np.asarray(x, dtype=float)
    return float(np.linalg.norm(arr.ravel(), 2))


def linf(x: np.ndarray) -> float:
    """Standard max (l_infinity) norm on R^n."""
    if np.iscomplexobj(x):
        raise TypeError("Real vector space inputs required")
    arr = np.asarray(x, dtype=float)
    return float(np.max(np.abs(arr.ravel())))


def anisotropic_gauge(x: np.ndarray, a: Sequence[float] = (1.0, 2.0)) -> float:
    """Anisotropic l1 gauge j(x) = sum a_i |x_i| on R^n."""
    if np.iscomplexobj(x):
        raise TypeError("Real vector space inputs required")
    v = np.asarray(x, dtype=float).ravel()
    if v.shape[0] != len(a):
        raise ValueError(
            f"Dimension mismatch: vector dim {v.shape[0]} != weight count {len(a)}"
        )
    if any(w <= 0 for w in a):
        raise ValueError("Anisotropic weights must be strictly positive")
    return float(sum(ai * abs(vi) for ai, vi in zip(a, v)))


def exact_induced_operator_norm(
    T: np.ndarray, domain_norm: str = "l2", codomain_norm: str = "l2"
) -> float:
    """Compute exact induced operator norm ||T||_{domain -> codomain} for standard norms.

    - l1 -> l1: max column sum
    - linf -> linf: max row sum
    - l2 -> l2: spectral norm (max singular value)
    - l1 -> linf: max absolute entry
    - linf -> l1: exact evaluation over 2^n extreme vertices of [-1, 1]^n
    """
    arr = np.asarray(T, dtype=float)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError("T must be a square real matrix")

    domain = domain_norm.lower()
    codomain = codomain_norm.lower()

    if domain == "l1" and codomain == "l1":
        return float(np.max(np.sum(np.abs(arr), axis=0)))
    elif domain == "linf" and codomain == "linf":
        return float(np.max(np.sum(np.abs(arr), axis=1)))
    elif domain == "l2" and codomain == "l2":
        return float(np.linalg.norm(arr, 2))
    elif domain == "l1" and codomain == "linf":
        return float(np.max(np.abs(arr)))
    elif domain == "linf" and codomain == "l1":
        n = arr.shape[1]
        if n > 12:
            raise ValueError(
                "Exact linf -> l1 norm evaluation limited to dimension <= 12"
            )
        from itertools import product

        max_val = 0.0
        for vertex in product([-1.0, 1.0], repeat=n):
            v = np.array(vertex)
            val = float(np.sum(np.abs(arr @ v)))
            if val > max_val:
                max_val = val
        return max_val
    else:
        raise ValueError(f"Unsupported norm pair: {domain} -> {codomain}")


def sample_lower_bound_induced_norm(
    T: np.ndarray, gauge: Gauge, n_samples: int = 1000, seed: int = 42
) -> tuple[float, np.ndarray]:
    """Sample-based lower bound estimate for induced operator norm ||T||_{j -> j}.

    Includes basis vectors and random vectors. Returns (lower_bound_estimate, worst_witness_vector).
    """
    arr = np.asarray(T, dtype=float)
    n = arr.shape[0]
    rng = np.random.default_rng(seed)

    # Standard basis vectors e_i
    basis_vectors = [np.eye(n)[i] for i in range(n)]
    raw_samples = list(basis_vectors) + list(rng.normal(size=(n_samples, n)))

    max_ratio = 0.0
    best_witness = raw_samples[0]

    for v in raw_samples:
        j_v = gauge(v)
        if j_v <= 1e-15:
            continue
        j_Tv = gauge(arr @ v)
        ratio = j_Tv / j_v
        if ratio > max_ratio:
            max_ratio = ratio
            best_witness = v

    return float(max_ratio), best_witness
