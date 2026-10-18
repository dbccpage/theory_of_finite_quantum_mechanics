r"""
Interference as the non-:math:`L^1` resource.

AuthorityEffect: None.

Canonical Implementation: finite_qm.use_cases.interference
"""

from __future__ import annotations

from typing import Any, Dict, List, Sequence

import numpy as np


def diagonal_data(c: Sequence[complex] | np.ndarray) -> np.ndarray:
    r""":math:`L_1(c) = (|c_s|^2)_s` --- the sector weights a diagonal readout sees."""
    v = np.asarray(c, dtype=complex)
    return np.abs(v) ** 2


def interfered_weight(c: Sequence[complex] | np.ndarray) -> float:
    r""":math:`\mathcal I(c) = |\sum_s c_s|^2`."""
    v = np.asarray(c, dtype=complex)
    return float(np.abs(np.sum(v)) ** 2)


def cross_term(c: Sequence[complex] | np.ndarray) -> float:
    r""":math:`\mathcal I(c) - \sum_s |c_s|^2 = \sum_{i \neq j} c_i^{*}c_j`."""
    v = np.asarray(c, dtype=complex)
    return interfered_weight(v) - float(np.sum(np.abs(v) ** 2))


def two_path_cross_term(c1: complex, c2: complex) -> float:
    r""":math:`2\operatorname{Re}(c_1^{*}c_2) = 2\sqrt{w_1 w_2}\cos(\phi_1 - \phi_2)`."""
    return float(2.0 * np.real(np.conj(c1) * c2))


def theorem_a1_separation() -> Dict[str, Any]:
    r"""Run the qm_061 Theorem A1 separation instead of restating it."""
    c = np.array([1.0, 1.0], dtype=complex)
    c_prime = np.array([1.0, -1.0], dtype=complex)

    l1_c, l1_cp = diagonal_data(c), diagonal_data(c_prime)
    i_c, i_cp = interfered_weight(c), interfered_weight(c_prime)

    return {
        "witness_a": c,
        "witness_b": c_prime,
        "diagonal_data_a": l1_c,
        "diagonal_data_b": l1_cp,
        "diagonal_data_identical": bool(np.allclose(l1_c, l1_cp, atol=1e-15)),
        "interfered_a": i_c,
        "interfered_b": i_cp,
        "interfered_differs": bool(not np.isclose(i_c, i_cp, atol=1e-12)),
        "cross_a": cross_term(c),
        "cross_b": cross_term(c_prime),
        "separation_holds": bool(
            np.allclose(l1_c, l1_cp, atol=1e-15) and not np.isclose(i_c, i_cp, atol=1e-12)
        ),
        "claim": "no function of the diagonal Born data determines the interfered weight",
        "status": "SEPARATION_WITNESSED",
        "authority_effect": "None",
    }


def phase_sweep(w1: float, w2: float, n: int = 33) -> Dict[str, Any]:
    r"""Sweep the relative phase and locate the interference boundary (qm_208 Thm 2.1)."""
    if w1 < 0 or w2 < 0:
        raise ValueError("phase_sweep: sector weights must be nonnegative")
    phases = np.linspace(0.0, 2.0 * np.pi, n)
    crosses: List[float] = []
    for phi in phases:
        c = np.array([np.sqrt(w1), np.sqrt(w2) * np.exp(1j * phi)], dtype=complex)
        crosses.append(cross_term(c))
    arr = np.asarray(crosses)

    return {
        "phases": phases,
        "cross_terms": arr,
        "max_constructive": float(np.max(arr)),
        "max_destructive": float(np.min(arr)),
        "amplitude": float(2.0 * np.sqrt(w1 * w2)),
        "vanishes_somewhere": bool(np.any(np.abs(arr) < 1e-9)),
        "both_signs_realized": bool(np.max(arr) > 1e-9 and np.min(arr) < -1e-9),
        "authority_effect": "None",
    }


def superposition_quotient_fiber(n_sectors: int) -> Dict[str, Any]:
    r"""qm_060: the phase fiber over fixed sector weights."""
    if n_sectors < 1:
        raise ValueError("superposition_quotient_fiber: need at least one sector")

    base = np.ones(n_sectors, dtype=complex) / np.sqrt(n_sectors)
    global_rotated = base * np.exp(1j * 0.7)

    relative = base.copy()
    if n_sectors >= 2:
        relative[1] *= np.exp(1j * 0.7)

    return {
        "n_sectors": n_sectors,
        "raw_fiber": f"U(1)^{n_sectors}",
        "observable_fiber": f"U(1)^{max(n_sectors - 1, 0)}",
        "global_phase_invisible": bool(
            np.isclose(interfered_weight(base), interfered_weight(global_rotated), atol=1e-12)
        ),
        "relative_phase_visible": bool(
            n_sectors >= 2
            and not np.isclose(
                interfered_weight(base), interfered_weight(relative), atol=1e-12
            )
        ),
        "imports": ["complex amplitudes / U(1) carrier (OB-U1)", "l2 readout (OB-L2-READOUT)"],
        "authority_effect": "None",
    }


__all__ = [
    "diagonal_data",
    "interfered_weight",
    "cross_term",
    "two_path_cross_term",
    "theorem_a1_separation",
    "phase_sweep",
    "superposition_quotient_fiber",
]
