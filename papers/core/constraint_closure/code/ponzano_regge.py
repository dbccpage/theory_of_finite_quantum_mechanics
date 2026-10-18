"""Ponzano-Regge semiclassical asymptotics and L1 phase envelope bounds.

Connects the exact Wigner 6j symbol to the Regge action phase:
    {k j_e} ~ 1 / sqrt(12 * pi * V(j)) * k^(-3/2) * cos(k * S_Regge + pi/4)
where S_Regge = sum_{e=1}^6 (j_e + 1/(2k)) * theta_e and V(j) is the volume of the unscaled tetrahedron
(Roberts 1999). Note that general 6j symbols involve algebraic radicals from Racah triangle factors
(e.g., {1,1,1; 1,2,2} = -1/sqrt(20)).

Establishes L1 phase stability:
    Fixed-angle bound: |Delta S_theta| <= ||Delta j||_1 * ||theta||_inf
    Schläfli geometric path bound: |S(J') - S(J)| <= ||J' - J||_1 * sup_{t in [0,1]} ||theta(J(t))||_inf <= pi * ||J' - J||_1.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
import numpy as np

from ponzano_regge_6j import wigner_6j_exact
from simplex import regular_simplex_dihedral_angle


@dataclass(frozen=True)
class PonzanoReggeAsymptotics:
    """Asymptotic evaluation data for a tetrahedron 6j symbol.

    exact_6j may be Fraction (for rational values like 1/6 for all spins 1)
    or float/str when Racah triangle square roots produce algebraic radicals (e.g. -1/sqrt(20)).
    """

    spins: Tuple[int, int, int, int, int, int]
    exact_6j: Union[Fraction, float, str]
    semiclassical_phase: float
    l1_spin_norm: int
    l1_phase_envelope: float
    tetrahedron_volume: float
    authority_effect: str = "None"


def evaluate_semiclassical_regge_phase(
    spins: Sequence[int | float],
    dihedral_angles: Optional[Sequence[float]] = None,
    require_geometric_angles: bool = False,
) -> float:
    """Evaluate discrete Regge action phase S_Regge = sum_{e=1}^6 (j_e + 1/2) * theta_e.

    For regular tetrahedron spins, theta_e = arccos(1/3).
    For non-regular configurations where dihedral angles vary with geometry, explicit
    dihedral angles must be provided when require_geometric_angles=True to prevent
    conflating fixed-angle bounds with dynamical geometry.
    """
    if len(spins) != 6:
        raise ValueError(f"Tetrahedron requires 6 edge spins, got {len(spins)}")

    if dihedral_angles is None:
        if require_geometric_angles and len(set(spins)) > 1:
            raise ValueError(
                "Non-regular spins require explicit geometric dihedral angles when require_geometric_angles=True."
            )
        theta = regular_simplex_dihedral_angle(3)
        angles = [theta] * 6
    else:
        if len(dihedral_angles) != 6:
            raise ValueError("Must provide 6 dihedral angles")
        angles = list(dihedral_angles)

    phase = sum((float(j) + 0.5) * th for j, th in zip(spins, angles))
    return float(phase)


def compute_l1_phase_envelope(
    spins: Sequence[int | float],
    max_dihedral_angle: Optional[float] = None,
    include_shift: bool = True,
) -> float:
    """Compute upper bound on Regge phase via L1 norm.

    If include_shift is True (default), bounds the semiclassical phase:
        |sum (j_e + 1/2) theta_e| <= ||j + 1/2||_1 * ||theta||_inf
    If include_shift is False, bounds the unshifted sum:
        |sum j_e theta_e| <= ||j||_1 * ||theta||_inf
    """
    if max_dihedral_angle is None:
        max_dihedral_angle = regular_simplex_dihedral_angle(3)
    if include_shift:
        l1_norm = sum(abs(float(j) + 0.5) for j in spins)
    else:
        l1_norm = sum(abs(float(j)) for j in spins)
    return float(l1_norm * max_dihedral_angle)


def verify_regge_action_lipschitz_bound(
    spins1: Sequence[int],
    spins2: Sequence[int],
    dihedral_angles: Optional[Sequence[float]] = None,
) -> Dict[str, Any]:
    """Verify that |S(j1) - S(j2)| <= ||j1 - j2||_1 * ||theta||_inf."""
    if len(spins1) != 6 or len(spins2) != 6:
        raise ValueError("Both configurations must have 6 edge spins")

    if dihedral_angles is None:
        theta_val = regular_simplex_dihedral_angle(3)
        angles = [theta_val] * 6
    else:
        angles = list(dihedral_angles)

    phase1 = evaluate_semiclassical_regge_phase(spins1, angles)
    phase2 = evaluate_semiclassical_regge_phase(spins2, angles)

    actual_diff = abs(phase1 - phase2)
    l1_diff = sum(abs(j1 - j2) for j1, j2 in zip(spins1, spins2))
    max_theta = max(abs(th) for th in angles)
    upper_bound = l1_diff * max_theta

    bound_holds = (actual_diff <= upper_bound + 1e-12)

    return {
        "bound_holds": bound_holds,
        "actual_difference": actual_diff,
        "l1_spin_difference": l1_diff,
        "max_dihedral_angle": max_theta,
        "lipschitz_upper_bound": upper_bound,
        "authority_effect": "None",
    }


def evaluate_schlafli_path_bound(
    lengths1: Sequence[float],
    lengths2: Sequence[float],
    sup_dihedral_angle: float,
) -> Dict[str, Any]:
    """Evaluate the geometric Schläfli path bound between two tetrahedron edge length configurations:

        |S(J') - S(J)| <= ||J' - J||_1 * sup_{t in [0, 1]} ||theta(J(t))||_inf <= pi * ||J' - J||_1.

    Under the Schläfli identity dS = sum theta_e dJ_e, integrating along any smooth curve of
    nondegenerate geometries yields |Delta S| <= int_0^1 sum |theta_e| |dJ_e/dt| dt <= ||Delta J||_1 sup ||theta||_inf.
    """
    if len(lengths1) != 6 or len(lengths2) != 6:
        raise ValueError("Both configurations must have 6 edge lengths")

    l1_diff = float(sum(abs(j1 - j2) for j1, j2 in zip(lengths1, lengths2)))
    path_bound = l1_diff * sup_dihedral_angle
    pi_bound = l1_diff * math.pi

    return {
        "l1_length_difference": l1_diff,
        "sup_dihedral_angle": sup_dihedral_angle,
        "path_bound": path_bound,
        "pi_universal_bound": pi_bound,
        "authority_effect": "None",
    }
