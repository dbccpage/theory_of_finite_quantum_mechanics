"""Exact witness for the five-triangle metric and deficit-angle carrier in derivation.md."""

from __future__ import annotations

from fractions import Fraction


def _det3(m: list[list[Fraction]]) -> Fraction:
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def cayley_menger_det_2simplex(
    s1: int | Fraction, s2: int | Fraction, b: int | Fraction
) -> Fraction:
    s1_f, s2_f, b_f = Fraction(s1), Fraction(s2), Fraction(b)
    m = [
        [Fraction(0), Fraction(1), Fraction(1), Fraction(1)],
        [Fraction(1), Fraction(0), s1_f, s2_f],
        [Fraction(1), s1_f, Fraction(0), b_f],
        [Fraction(1), s2_f, b_f, Fraction(0)],
    ]
    total = Fraction(0)
    for col in range(4):
        sub = [[m[r][c] for c in range(4) if c != col] for r in range(1, 4)]
        sign = Fraction(1 if col % 2 == 0 else -1)
        total += sign * m[0][col] * _det3(sub)
    return total


def star_edges(n: int) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    if n < 3:
        raise ValueError("a vertex star requires at least 3 boundary vertices")
    return [
        ((0, i), (0, (i % n) + 1), (i, (i % n) + 1))
        for i in range(1, n + 1)
    ]


def witness() -> dict[str, int | Fraction | tuple[Fraction, Fraction]]:
    triangles_k5 = star_edges(5)
    triangles_k6 = star_edges(6)
    cm_det = cayley_menger_det_2simplex(1, 1, 1)
    signed_vol = -cm_det
    if cm_det != -3 or signed_vol != 3:
        raise RuntimeError("unexpected Cayley-Menger determinant for unit equilateral triangle")
    area_sq = Fraction(signed_vol, 16)
    apex_cos = Fraction(1 + 1 - 1, 2)
    apex_sin_sq = 1 - apex_cos * apex_cos
    turn_per_triangle = Fraction(1, 6)
    turn_sum_k5 = len(triangles_k5) * turn_per_triangle
    turn_deficit_k5 = 1 - turn_sum_k5
    turn_deficit_k6 = 1 - len(triangles_k6) * turn_per_triangle
    radian_lo = Fraction(1_047_197_551, 1_000_000_000)
    radian_hi = Fraction(1_047_197_552, 1_000_000_000)
    return {
        "triangles_k5": len(triangles_k5),
        "triangles_k6": len(triangles_k6),
        "cayley_menger_det": int(cm_det),
        "signed_volume_factor": int(signed_vol),
        "triangle_area_sq": area_sq,
        "star_area_sq_k5": len(triangles_k5) ** 2 * area_sq,
        "apex_cosine": apex_cos,
        "apex_sin_sq": apex_sin_sq,
        "turn_sum_k5": turn_sum_k5,
        "turn_deficit_k5": turn_deficit_k5,
        "turn_deficit_k6": turn_deficit_k6,
        "radian_deficit_interval": (radian_lo, radian_hi),
        "radian_deficit_width": radian_hi - radian_lo,
    }


def reject_pinned_cm_determinant(det_value: int | Fraction) -> None:
    if Fraction(det_value) == 3:
        raise ValueError("unit equilateral 2-simplex 4x4 Cayley-Menger determinant is -3, not +3")


def reject_unproved_continuum_bound(claim: str) -> None:
    if "|E(a)| <= (1/6) * a^2" in claim or "Ricci" in claim:
        raise ValueError("a single five-triangle star does not establish a continuum Ricci bound")
