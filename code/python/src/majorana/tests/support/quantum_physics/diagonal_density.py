r"""
Residual weights as a diagonal density: the classical heart of the finite theory.

AuthorityEffect: None.

Canonical Implementation: omega_engine.crates.quantum_physics.diagonal_density
"""

from __future__ import annotations
from typing import Any, Dict, Sequence

import numpy as np

from omega_engine.crates.quantum_physics.primitives import is_density_matrix, purity


def normalize(masses: Sequence[float] | np.ndarray) -> np.ndarray:
    r""":math:`p_s = \mu(s)/W`. Raises when :math:`W = 0` or any mass is negative."""
    mu = np.asarray(masses, dtype=float)
    if np.any(mu < 0.0):
        raise ValueError("normalize: residual masses must be nonnegative")
    total = float(np.sum(mu))
    if total <= 0.0:
        raise ValueError(
            "normalize: total residual mass W = 0 — undefined, there is no state here"
        )
    return mu / total


def diagonal_density(masses: Sequence[float] | np.ndarray) -> np.ndarray:
    r"""The finite diagonal density :math:`\rho = \operatorname{diag}(p)`."""
    return np.diag(normalize(masses)).astype(complex)


def density_report(masses: Sequence[float] | np.ndarray) -> Dict[str, Any]:
    r"""Normalize, embed, and report purity / mixedness with the state checks actually run."""
    p = normalize(masses)
    rho = np.diag(p).astype(complex)
    tr_rho2 = purity(rho)

    return {
        "weights": p,
        "total_mass": float(np.sum(np.asarray(masses, dtype=float))),
        "is_state": is_density_matrix(rho),
        "trace": float(np.real(np.trace(rho))),
        "purity": tr_rho2,
        "mixedness": 1.0 - tr_rho2,
        "is_pure": bool(np.isclose(tr_rho2, 1.0, atol=1e-12)),
        "support_size": int(np.count_nonzero(p > 1e-15)),
        "authority_effect": "None",
    }


def born_readout(rho: np.ndarray, projector: np.ndarray) -> float:
    r""":math:`\operatorname{Tr}(P\rho)` --- the sector-basis measurement probability."""
    return float(np.real(np.trace(projector @ rho)))


def sector_basis_measurement_returns_p(masses: Sequence[float] | np.ndarray) -> bool:
    r"""Check qm_003 RDB-2: measuring :math:`\rho` in the sector basis returns :math:`p`."""
    p = normalize(masses)
    rho = np.diag(p).astype(complex)
    n = len(p)
    for s in range(n):
        proj = np.zeros((n, n), dtype=complex)
        proj[s, s] = 1.0
        if not np.isclose(born_readout(rho, proj), p[s], atol=1e-12):
            return False
    return True


def orientation_collapse(signed_residual: Sequence[float] | np.ndarray) -> Dict[str, Any]:
    r"""Exhibit qm_003 RDB-3b: the diagonal density is orientation-blind."""
    x = np.asarray(signed_residual, dtype=float)
    rho = diagonal_density(np.abs(x))

    flipped = -x
    rho_flipped = diagonal_density(np.abs(flipped))
    identified = bool(np.allclose(rho, rho_flipped, atol=1e-15))

    partial = x.copy()
    nonzero = np.flatnonzero(np.abs(partial) > 1e-15)
    if nonzero.size:
        partial[nonzero[0]] *= -1.0
    rho_partial = diagonal_density(np.abs(partial))

    return {
        "rho": rho,
        "global_flip_identified": identified,
        "partial_flip_identified": bool(np.allclose(rho, rho_partial, atol=1e-15)),
        "distinct_sign_patterns_identified": int(2 ** int(np.count_nonzero(np.abs(x) > 1e-15))),
        "loss_ledger": [
            {
                "discarded": "sign pattern of the signed residual",
                "recovery_requirement": "a declared coherence license (qm_003 RDB-6)",
                "disposition": "PROJECTION_LOSS",
            }
        ],
        "authority_effect": "None",
    }


def coherence_is_not_forced(p: Sequence[float] | np.ndarray) -> Dict[str, Any]:
    r"""qm_012 §6: off-diagonal coherence is a non-forced lift."""
    w = normalize(p)
    n = len(w)
    rho_diag = np.diag(w).astype(complex)

    psi = np.sqrt(w).astype(complex)
    rho_coh = np.outer(psi, psi.conj())

    same_diag = bool(np.allclose(np.real(np.diag(rho_coh)), w, atol=1e-12))
    return {
        "diagonal_purity": purity(rho_diag),
        "coherent_purity": purity(rho_coh),
        "same_sector_statistics": same_diag,
        "purity_differs": bool(
            not np.isclose(purity(rho_diag), purity(rho_coh), atol=1e-12) or n == 1
        ),
        "verdict": "sector weights do not determine the state; coherence is a declared lift",
        "authority_effect": "None",
    }


__all__ = [
    "normalize",
    "diagonal_density",
    "density_report",
    "born_readout",
    "sector_basis_measurement_returns_p",
    "orientation_collapse",
    "coherence_is_not_forced",
]



