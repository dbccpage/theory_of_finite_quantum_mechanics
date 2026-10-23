"""Numerical norms and finite-Hamiltonian bound formulas.

The lower bound assumes product initial data and ||H||_op <= g for the
entire closed-system Hamiltonian, not a per-site interaction budget.
AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

from ._validation import integer, matrix, nonnegative
from .k_cell_retraction import k_cell_product_retraction


def schatten_1_norm(matrix_: np.ndarray) -> float:
    """Numerically evaluate the sum of singular values."""
    return float(np.sum(np.linalg.svd(matrix(matrix_, "operator"), compute_uv=False)))


def operator_norm(matrix_: np.ndarray) -> float:
    """Numerically evaluate the largest singular value."""
    return float(np.max(np.linalg.svd(matrix(matrix_, "operator"), compute_uv=False)))


def evaluate_k_party_trace_defect(rho_state: np.ndarray, dims: Sequence[int]) -> float:
    """Distance to the product of marginals; not a separability test."""
    return schatten_1_norm(np.asarray(rho_state) - k_cell_product_retraction(rho_state, dims))


def short_time_k_party_defect_lower_bound(
    nu_sigma: float, k: int, g: float, t: float
) -> tuple[float, float, bool]:
    """Return (nu*t-6*k^2*g^2*t^2, half-slope window, in_window).

    The caller must establish the Hamiltonian norm and product-state
    hypotheses. Zero speed has no positive half-slope window.
    """
    nu = nonnegative(nu_sigma, "nu_sigma")
    count = integer(k, "k", 2)
    bound_g = nonnegative(g, "g")
    time = nonnegative(t, "t")
    if bound_g == 0:
        if nu != 0:
            raise ValueError("g=0 implies nu_sigma=0")
        return 0.0, 0.0, False
    try:
        coefficient = 6 * count**2 * bound_g**2
        if not np.isfinite(coefficient) or coefficient == 0:
            raise ValueError("bound coefficient overflows or underflows")
        t_star = nu / (2 * coefficient)
        value = nu * time - coefficient * time**2
    except OverflowError as error:
        raise ValueError("bound calculation overflows") from error
    if not np.isfinite(value) or not np.isfinite(t_star):
        raise ValueError("bound calculation overflows")
    return float(value), float(t_star), bool(nu > 0 and time <= t_star)


def schatten1_dual_witness(
    residual: np.ndarray, tol: float = 0.0
) -> tuple[np.ndarray, float, float]:
    """Polar partial isometry, operator norm, full complex pairing error.

    tol is an absolute singular-value cutoff; discarded values contribute
    to alignment error. No tangent-annihilator claim is made.
    """
    z = matrix(residual, "residual")
    cutoff = nonnegative(tol, "tol")
    u, singular, vh = np.linalg.svd(z, full_matrices=False)
    active = singular > cutoff
    w = u[:, active] @ vh[active, :]
    error = abs(np.vdot(w, z) - np.sum(singular))
    return w, operator_norm(w), float(error)


def duhamel_observable_certificate(observable: np.ndarray, residuals_integrated: float) -> float:
    """Evaluate ||O||_op times a known Duhamel residual integral.

    Requires unitary exact propagation and an approximate-trajectory
    residual integral. Sampling the initial speed alone is insufficient.
    """
    return operator_norm(observable) * nonnegative(residuals_integrated, "residuals_integrated")
