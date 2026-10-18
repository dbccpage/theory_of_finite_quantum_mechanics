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


def _rational_weights(amplitudes: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (amplitudes[0] ** 2, amplitudes[1] ** 2)


def _rational_interfered(amplitudes: tuple[Fraction, Fraction]) -> Fraction:
    total = amplitudes[0] + amplitudes[1]
    return total * total


def theorem_a1_separation() -> Dict[str, Any]:
    """Diagonal Born weights of (1, 1) and (1, -1) agree; the interfered weights do not."""
    from fractions import Fraction

    witness_a = (Fraction(1), Fraction(1))
    witness_b = (Fraction(1), Fraction(-1))
    diagonal_a = _rational_weights(witness_a)
    diagonal_b = _rational_weights(witness_b)
    interfered_a = _rational_interfered(witness_a)
    interfered_b = _rational_interfered(witness_b)
    cross_a = interfered_a - sum(diagonal_a, Fraction(0))
    cross_b = interfered_b - sum(diagonal_b, Fraction(0))
    same_diagonal = diagonal_a == diagonal_b
    differs = interfered_a != interfered_b
    return {
        "witness_a": witness_a,
        "witness_b": witness_b,
        "diagonal_data_a": diagonal_a,
        "diagonal_data_b": diagonal_b,
        "diagonal_data_identical": same_diagonal,
        "interfered_a": interfered_a,
        "interfered_b": interfered_b,
        "interfered_differs": differs,
        "cross_a": cross_a,
        "cross_b": cross_b,
        "separation_holds": same_diagonal and differs and cross_a == -cross_b and cross_a != 0,
        "claim": "no function of the diagonal Born data determines the interfered weight",
        "status": "SEPARATION_WITNESSED" if same_diagonal and differs else "SEPARATION_FAILED",
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
