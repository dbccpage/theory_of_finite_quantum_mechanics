"""
Canonical l1-to-density lift and Ξ functional (Paper 006 §3, §5).

rho_l1: EdgeCochain -> density matrix (rank-1 projector)
compute_xi: (h1, phi_star) -> trace distance between density lifts
"""

import numbers
from typing import Optional

import numpy as np


def _as_valid_real_vector(v: np.ndarray, name: str = "v") -> np.ndarray:
    if isinstance(v, (list, tuple, np.ndarray)):
        items = v.tolist() if isinstance(v, np.ndarray) else list(v)
        for item in items:
            if isinstance(item, bool) or not isinstance(item, numbers.Real):
                raise TypeError(
                    f"{name} must contain only real scalars, got {type(item).__name__}"
                )

    arr = np.asarray(v, dtype=float)

    if arr.ndim != 1:
        raise ValueError(f"{name} must be a 1D vector.")

    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values.")

    return arr


def rho_l1(v: np.ndarray) -> Optional[np.ndarray]:
    """
    Lift a nonzero real signed L1 vector to a rank-1 normalized outer product.

    Returns None for the zero vector.
    """
    v = _as_valid_real_vector(v)

    if np.allclose(v, 0):
        return None

    mass = float(np.sum(np.abs(v)))
    psi = np.sign(v) * np.sqrt(np.abs(v) / mass)

    return np.outer(psi, np.conjugate(psi))


def trace_norm(A: np.ndarray) -> float:
    """Schatten-1 (trace) norm computed from singular values."""
    return float(np.sum(np.linalg.svd(A, compute_uv=False)))


def compute_xi(h_raw: np.ndarray, h_can: np.ndarray) -> Optional[float]:
    """Xi = ||rho(h_raw) - rho(h_can)||_1 with zero-residual convention.

    Conventions:
        - compute_xi(v, v) == 0.0   (identical residuals).
        - compute_xi(0, 0) == 0.0   (both sides carry no density; defined as 0).
        - Exactly one side zero (one density-lift None, the other not): the
          comparison is UNDEFINED, so this returns ``None``. Returning 0.0 here
          would falsely read as "identical".
    """
    h_raw = _as_valid_real_vector(h_raw, "h_raw")
    h_can = _as_valid_real_vector(h_can, "h_can")

    if h_raw.shape != h_can.shape:
        raise ValueError("h_raw and h_can must have the same shape.")

    if np.allclose(h_raw, 0) and np.allclose(h_can, 0):
        return 0.0

    rho_raw = rho_l1(h_raw)
    rho_can = rho_l1(h_can)

    if rho_raw is None or rho_can is None:
        return None

    return 0.5 * trace_norm(rho_raw - rho_can)

