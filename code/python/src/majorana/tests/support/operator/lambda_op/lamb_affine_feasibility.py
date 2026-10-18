"""Port of ``omega_solvers/src/continuous/solver_affine_feasibility_projector.rs``.

Projects ``x0`` onto the affine set ``{ x | A x = b }`` via

    x_proj = x0 - A^T (A A^T)^{-1} (A x0 - b)

with an SVD-pseudoinverse fallback when ``A A^T`` is singular (rank-deficient
but consistent). Rejects inconsistent systems when the post-projection residual
exceeds ``sqrt(SVD_EPSILON)``.
"""

from __future__ import annotations
import numpy as np

SVD_EPSILON = 1e-10


def project_onto_affine(a: np.ndarray, b: np.ndarray, x0: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float).reshape(-1)
    x0 = np.asarray(x0, dtype=float).reshape(-1)

    nrows, ncols = a.shape
    if nrows != b.shape[0]:
        raise ValueError(
            f"row/right-hand-side dimension mismatch: {nrows} rows, "
            f"{b.shape[0]} rhs entries"
        )
    if ncols != x0.shape[0]:
        raise ValueError(
            f"column/vector dimension mismatch: {ncols} columns, "
            f"{x0.shape[0]} vector entries"
        )

    residual = a @ x0 - b
    normal = a @ a.T

    multiplier = None
    try:
        cond = np.linalg.cond(normal) if normal.size else 1.0
        if np.isfinite(cond) and cond < 1.0 / np.finfo(float).eps:
            multiplier = np.linalg.solve(normal, residual)
    except np.linalg.LinAlgError:
        multiplier = None

    if multiplier is None:
        try:
            u, s, vt = np.linalg.svd(normal)
            s_inv = np.array([1.0 / sv if sv > SVD_EPSILON else 0.0 for sv in s])
            pinv = (vt.T * s_inv) @ u.T
            multiplier = pinv @ residual
        except np.linalg.LinAlgError as exc:
            raise ValueError("normal system solve failed (both LU and SVD)") from exc

    projected = x0 - a.T @ multiplier

    constraint_residual = float(np.linalg.norm(a @ projected - b))
    if constraint_residual > np.sqrt(SVD_EPSILON):
        raise ValueError(
            f"constraints are inconsistent: post-projection residual = "
            f"{constraint_residual:.2e}"
        )

    return projected
