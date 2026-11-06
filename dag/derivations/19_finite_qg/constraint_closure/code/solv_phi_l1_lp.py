"""Pure LP solvers for Paper 000 cohomological L1 witnesses."""

from typing import Optional, Tuple

import numpy as np
from scipy.optimize import linprog


try:
    from .dual_certificate import DivergenceFreeDual, PhiCertificate
    from .l1_seminorm import EdgeCochain
except ImportError:
    from dual_certificate import DivergenceFreeDual, PhiCertificate
    from l1_seminorm import EdgeCochain



def solve_phi(
    B: np.ndarray, omega: np.ndarray, weights: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, np.ndarray, PhiCertificate]:
    """
    Solve the weighted L1 obstruction Phi1 = min_f ||omega - B f||_{1,w}
    = min_f sum_e w_e |omega_e - (B f)_e|.

    ``weights`` (per-edge, length ``B.shape[0]``) defaults to ``None`` == unit
    weights ``w_e = 1``, which is the classical unweighted Phi1 (fully backward
    compatible). The dual of weighted-L1 is weighted-Linf, so the returned dual
    witness satisfies ``|phi_e| <= w_e`` (reducing to ``||phi||_inf <= 1`` at unit
    weights). The certificate is checkable via ``cert.verify()`` -- ``cert.phi1``
    is a float ESTIMATE until verified.

    Returns the primal minimizer, residual h1, and PhiCertificate.
    Note: f_star is one LP minimizer; it is not unique up to kernel(B).
    """
    if B.ndim != 2:
        raise ValueError("B must be a 2D array")
    if omega.ndim != 1:
        raise ValueError("omega must be a 1D array")
    if B.shape[0] != omega.shape[0]:
        raise ValueError(
            f"Shape mismatch: B has {B.shape[0]} rows but omega has {omega.shape[0]} elements"
        )

    m, n = B.shape

    if weights is None:
        w = np.ones(m)
    else:
        w = np.asarray(weights, dtype=float)
        if w.shape != (m,):
            raise ValueError(f"weights length {w.shape} does not match edge count {m}")
        if np.any(w < 0):
            raise ValueError("weights must be non-negative")

    c = np.r_[np.zeros(n), w]
    A_ub = np.vstack([np.c_[-B, -np.eye(m)], np.c_[B, -np.eye(m)]])

    scale = np.max(np.abs(omega))
    if scale > 0:
        omega_scaled = omega / scale
    else:
        omega_scaled = omega

    b_ub = np.r_[-omega_scaled, omega_scaled]
    bounds = [(None, None)] * n + [(0, None)] * m

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not res.success or res.x is None:
        raise RuntimeError(f"LP failed: {res.message}")

    f_star_scaled = res.x[:n]
    h1_scaled = omega_scaled - B @ f_star_scaled
    phi1_val_scaled = float(np.sum(w * np.abs(h1_scaled)))

    marginal_ub = res.ineqlin.marginals
    y1 = -marginal_ub[:m]
    y2 = -marginal_ub[m:]
    phi_vec = y2 - y1

    if (
        not np.allclose(B.T @ phi_vec, 0, atol=1e-7)
        or np.any(np.abs(phi_vec) > w + 1e-7)
        or abs(np.dot(phi_vec, omega_scaled) - phi1_val_scaled) > 1e-6
    ):
        phi_vec = solve_dual(B, h1_scaled, weights=w)

    f_star = f_star_scaled * scale if scale > 0 else f_star_scaled
    h1 = h1_scaled * scale if scale > 0 else h1_scaled
    phi1_val = phi1_val_scaled * scale if scale > 0 else phi1_val_scaled

    try:
        dual = DivergenceFreeDual.create(
            B, phi_vec, weights=None if weights is None else w
        )
    except ValueError:
        dual = DivergenceFreeDual(phi_vec, None if weights is None else w)

    cert = PhiCertificate(
        phi1=phi1_val,
        residual=EdgeCochain(h1),
        dual=dual,
        dual_value=float(np.dot(phi_vec, omega)),
        B=B,
        tol=1e-6,
        weights=None if weights is None else w,
    )

    return f_star, h1, cert


def solve_dual(
    B: np.ndarray, h1: np.ndarray, weights: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    Solve max <phi, h1> subject to |phi_e| <= w_e and B.T phi = 0.

    ``weights`` defaults to unit (``||phi||_inf <= 1``).
    """
    m, n = B.shape
    w = np.ones(m) if weights is None else np.asarray(weights, dtype=float)
    res = linprog(
        -h1,
        A_eq=B.T,
        b_eq=np.zeros(n),
        bounds=[(-w[e], w[e]) for e in range(m)],
        method="highs",
    )
    if not res.success or res.x is None:
        raise RuntimeError(f"Dual LP failed: {res.message}")
    return res.x
