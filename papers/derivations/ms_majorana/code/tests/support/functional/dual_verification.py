"""
Verify a candidate L∞ dual witness for an L1 residual problem.

This assumes the solver convention where B.T @ phi_star = 0,
||phi_star||∞ <= 1, and <phi_star, h> = Phi.

verify_dual_witness: explicit post-solve certification of φ*
accept: Φ₁-Ξ acceptance law enforcement
"""

from typing import Dict

import numpy as np


def verify_dual_witness(
    B: np.ndarray,
    phi_star: np.ndarray,
    h: np.ndarray,
    Phi: float,
    tol: float = 1e-8,
) -> Dict:
    """
    Explicitly verify that φ* is a valid dual certificate.

    Checks:
        1. B^T φ* = 0       (divergence-free)
        2. ||φ*||∞ ≤ 1      (bounded)
        3. ⟨φ*, h₁⟩ = Φ₁   (tight duality)

    Returns dict with individual checks and overall certified flag.

    Note: this is a post-solve utility; missing keys raise KeyError at the
    caller boundary by design (no defensive key handling here).
    """
    B = np.asarray(B, dtype=float)
    phi_star = np.asarray(phi_star, dtype=float)
    h = np.asarray(h, dtype=float)

    if B.ndim != 2:
        raise ValueError("B must be a 2D array")
    if not np.all(np.isfinite(B)):
        raise ValueError("B must contain only finite values")
    if not np.all(np.isfinite(phi_star)):
        raise ValueError("phi_star must contain only finite values")
    if not np.all(np.isfinite(h)):
        raise ValueError("h must contain only finite values")
    if not np.isfinite(Phi):
        raise ValueError("Phi must be finite")
    if Phi < 0:
        raise ValueError("Phi must be non-negative")

    if B.shape[0] != phi_star.shape[0]:
        raise ValueError("phi_star length must match number of edges")
    if h.shape != phi_star.shape:
        raise ValueError("h and phi_star must have same shape")

    div = B.T @ phi_star
    div_ok = bool(np.allclose(div, 0, atol=tol))

    linf = float(np.max(np.abs(phi_star)))
    linf_ok = linf <= 1.0 + tol

    pairing = float(np.vdot(phi_star, h))
    tight = abs(pairing - Phi) <= tol

    return {
        "divergence_free": div_ok,
        "divergence_norm": float(np.max(np.abs(div))),
        "linf_ok": linf_ok,
        "linf_value": linf,
        "duality_tight": tight,
        "tightness_error": float(abs(pairing - Phi)),
        "dual_pairing": pairing,
        "tol": tol,
        "certified": bool(div_ok and linf_ok and tight),
    }


from omega_engine.crates.evaluator.dual_acceptance import accept as accept




