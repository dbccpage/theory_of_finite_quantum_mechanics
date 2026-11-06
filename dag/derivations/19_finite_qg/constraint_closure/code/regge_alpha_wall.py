"""Regge wall sums and an explicitly post-hoc 248 → 137 comparison.

AuthorityEffect: None. Stdlib only (math).

A perfect infinite equilateral triangulation has k=6 inside, so
interior deficits vanish. α cannot be the raw sum of those zeros.

What you can compute:

1. Finite hexagonal disk of radius R, with every missing boundary
   wedge charged as vertex deficit: the sum in units of π/3 is
   18R+6, i.e. 6πR + 2π radians.  That boundary-inclusive sum
   diverges and is not the boundary-corrected Gauss–Bonnet integral.

2. (2π)^3 = 8π³ ≈ 248.05. That is the “1/245” memory (also easy
   to mix with the 246 GeV VEV). Three full rotations.

3. The hand-selected polynomial
   4π³ + π² + π ≈ 137.036304 sits 3e-4 from QED α^{-1}.
   This arithmetic coincidence is not selected by the wall model and
   is not a derivation of QED. The 4π/D ≈ 142.62 ansatz also remains.

The wall series that would actually sum to 137 without a polynomial
ansatz is still a hunt (observer weights w(n)).
"""

from __future__ import annotations

import math
from typing import Any

PI = math.pi
QED_ALPHA_INV = 137.035999177
QED_ALPHA_INV_SOURCE = "https://physics.nist.gov/cuu/pdf/wallet_2022.pdf"


def deficit_units(k: int) -> int:
    """ε in units of π/3: (6-k). Flat interior k=6 ⇒ 0."""
    return 6 - k


def eight_pi_cubed() -> float:
    """(2π)^3 = 8π³. The ~248 number."""
    return 8.0 * PI**3


def four_pi_cubed() -> float:
    return 4.0 * PI**3


def alpha_inv_pi_poly() -> float:
    """Hand-selected arithmetic expression 4π³ + π² + π."""
    return 4.0 * PI**3 + PI**2 + PI


def three_cycle_D() -> float:
    return 1.0 - 9.0 / (PI**2)


def alpha_inv_4pi_over_D() -> float:
    return (4.0 * PI) / three_cycle_D()


_HEX_STEPS: tuple[tuple[int, int], ...] = (
    (1, 0),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (0, -1),
    (1, -1),
)


def _hex_norm(q: int, r: int) -> int:
    return max(abs(q), abs(r), abs(q + r))


def hex_vertices(radius: int) -> frozenset[tuple[int, int]]:
    pts: set[tuple[int, int]] = set()
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            if _hex_norm(q, r) <= radius:
                pts.add((q, r))
    return frozenset(pts)


def triangles_at(q: int, r: int, wall: frozenset[tuple[int, int]]) -> int:
    """How many of the six equilateral wedges at (q,r) are filled."""
    nbs = [(q + dq, r + dr) for dq, dr in _HEX_STEPS]
    k = 0
    for i in range(6):
        if nbs[i] in wall and nbs[(i + 1) % 6] in wall:
            k += 1
    return k


def hex_wall_deficit_units(radius: int) -> int:
    """Sum of (6-k_v) over a hexagonal disk. Interior k=6 contributes 0."""
    if radius < 0:
        raise ValueError("radius")
    wall = hex_vertices(radius)
    return sum(6 - triangles_at(q, r, wall) for q, r in wall)


def hex_wall_deficit_radians(radius: int) -> float:
    return hex_wall_deficit_units(radius) * (PI / 3.0)


def hex_wall_report(max_r: int = 8) -> dict[str, Any]:
    rows = []
    for r in range(max_r + 1):
        units = hex_wall_deficit_units(r)
        rad = hex_wall_deficit_radians(r)
        rows.append(
            {
                "R": r,
                "deficit_units": units,
                "deficit_radians": rad,
                "per_R": rad / r if r else None,
                "over_two_pi": rad / (2.0 * PI),
            }
        )
    return {
        "rows": rows,
        "units_formula": "6+18R",
        "per_R_limit": 6.0 * PI,
        "gauss_bonnet_disk_constant": 2.0 * PI,
        "diverges": True,
        "interior_k6_deficit": 0,
    }


def transform_248_to_137() -> dict[str, Any]:
    raw = eight_pi_cubed()
    half = four_pi_cubed()
    triangle = PI**2 + PI
    out = half + triangle
    return {
        "two_pi_cubed": raw,
        "remembered_as": 245,
        "half": half,
        "triangle_pi_sq_plus_pi": triangle,
        "alpha_inv_poly": out,
        "qed_alpha_inv": QED_ALPHA_INV,
        "qed_alpha_inv_source": QED_ALPHA_INV_SOURCE,
        "poly_minus_qed": out - QED_ALPHA_INV,
        "old_4pi_over_D": alpha_inv_4pi_over_D(),
        "is_qed_theorem": False,
        "formula_selected_post_hoc": True,
        "wall_selects_formula": False,
    }


def observer_series_D_over_n_nplus1(n_max: int = 200) -> dict[str, Any]:
    """g_n = D / (n(n+1)), sums to D ≈ 0.0881, not α."""
    d = three_cycle_D()
    partial = 0.0
    for n in range(1, n_max + 1):
        partial += d / (n * (n + 1))
    return {
        "partial": partial,
        "limit_D": d,
        "equals_alpha": False,
    }


def w_obstruction_removal(n: int) -> float:
    """Telescoping weight from the declared capacity ansatz c_n = 1/n.

    A radius-one propagation bound says only when shell n can first be
    reached; it does not derive the capacity ansatz.  Once c_n = 1/n
    is supplied, the removed slice telescopes:
    1/n - 1/(n+1) = 1/(n(n+1)).
    """
    if n < 1:
        raise ValueError("n")
    return 1.0 / (n * (n + 1))


def l1_unity(n_max: int = 10_000) -> dict[str, Any]:
    """The declared telescoping weights have sum one.

    This proves an elementary series identity after the 1/n capacity
    ansatz is supplied.  It does not derive a Born rule; the separate
    series sum 1/n² = π²/6 is reported only for comparison.
    """
    s_l1 = 0.0
    s_born = 0.0
    for n in range(1, n_max + 1):
        s_l1 += w_obstruction_removal(n)
        s_born += 1.0 / (n * n)
    d = three_cycle_D()
    return {
        "sum_w_l1": s_l1,
        "sum_w_l1_limit": 1.0,
        "sum_born_1_over_n2": s_born,
        "sum_born_limit": PI**2 / 6.0,
        "leak_after_l1_unity": d * 1.0,
        "leak_after_born": d * (PI**2 / 6.0),
        "alpha_inv_if_4pi_on_l1": (4.0 * PI) / d,
        "c_lr": 1,
        "is_qed": False,
        "capacity_ansatz": "1/n",
        "capacity_ansatz_derived": False,
        "born_rule_derived": False,
    }
