"""SP3a: Regge Deficit Angles and Hexagonal Wall Divergence.

2D equilateral triangulation deficit: ε_v = (π/3)(6 - k_v)
Hexagonal disk of radius R: Σε_v = 2π + 6πR (diverges linearly)
Gauss-Bonnet turning angles: Σκ_v = 2π (invariant)

AuthorityEffect: None.
"""

from __future__ import annotations

import math


def deficit_angle_2d(k: int) -> float:
    """Deficit angle at a vertex with k incident triangles in a 2D equilateral mesh."""
    return (math.pi / 3.0) * (6 - k)


def turning_angle_2d(k: int) -> float:
    """Geodesic turning angle at a boundary vertex with k incident triangles."""
    return math.pi - k * (math.pi / 3.0)


def hexagonal_disk_deficit(R: int) -> dict:
    """Compute exact deficit sum on a regular hexagonal disk of radius R.

    Boundary structure:
      - 6 corner vertices: k = 2, deficit = 4π/3 each
      - 6(R-1) straight edge vertices: k = 3, deficit = π each
      - Interior vertices: k = 6, deficit = 0

    Total: 6 * 4π/3 + 6(R-1) * π = 8π + 6(R-1)π = 2π + 6πR
    In units of π/3: 6*4 + 6(R-1)*3 = 24 + 18(R-1) = 6 + 18R
    """
    assert R >= 1, "Radius must be >= 1"

    n_corners = 6
    k_corner = 2
    deficit_per_corner = deficit_angle_2d(k_corner)

    n_edge_vertices = 6 * (R - 1)
    k_edge = 3
    deficit_per_edge = deficit_angle_2d(k_edge)

    total_deficit_radians = (
        n_corners * deficit_per_corner + n_edge_vertices * deficit_per_edge
    )
    expected_radians = 2 * math.pi + 6 * math.pi * R

    total_units = round(total_deficit_radians / (math.pi / 3))
    expected_units = 6 + 18 * R

    turning_corner = turning_angle_2d(k_corner)
    turning_edge = turning_angle_2d(k_edge)
    total_turning = n_corners * turning_corner + n_edge_vertices * turning_edge

    return {
        "R": R,
        "n_corners": n_corners,
        "n_edge_vertices": n_edge_vertices,
        "total_deficit_radians": total_deficit_radians,
        "expected_deficit_radians": expected_radians,
        "deficit_match": abs(total_deficit_radians - expected_radians) < 1e-10,
        "total_deficit_units": total_units,
        "expected_deficit_units": expected_units,
        "units_match": total_units == expected_units,
        "gauss_bonnet_turning": total_turning,
        "gauss_bonnet_is_2pi": abs(total_turning - 2 * math.pi) < 1e-10,
    }


def verify_linear_divergence(R_values: list[int] | None = None) -> dict:
    """Confirm total deficit grows linearly with R."""
    if R_values is None:
        R_values = [1, 2, 3, 4, 5, 10, 20, 50, 100]

    deficits = []
    for R in R_values:
        result = hexagonal_disk_deficit(R)
        deficits.append(result["total_deficit_radians"])

    slopes = []
    for i in range(1, len(R_values)):
        dR = R_values[i] - R_values[i - 1]
        d_deficit = deficits[i] - deficits[i - 1]
        slopes.append(d_deficit / dR)

    expected_slope = 6 * math.pi
    all_slopes_correct = all(abs(s - expected_slope) < 1e-10 for s in slopes)

    return {
        "R_values": R_values,
        "deficits": deficits,
        "slopes": slopes,
        "expected_slope_6pi": expected_slope,
        "all_slopes_correct": all_slopes_correct,
        "diverges": deficits[-1] > 50 * deficits[0],
    }
