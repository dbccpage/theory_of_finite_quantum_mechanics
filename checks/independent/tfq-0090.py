#!/usr/bin/env python3
"""Independent exact rational verifier for TFQ-0090 (FINITE_QG, GAP).

Verifies with Python Fractions and exact integer arithmetic (no Lean dependency):
1. Finite tetrahedral comparison complex K_4^(2): exactness d_1(d_0 phi) = 0,
   gauge invariance d_1(omega + d_0 phi) = d_1(omega), linearity d_1(c * omega) = c * d_1(omega),
   and discrete Bianchi identity F012 - F013 + F023 - F123 = 0.
2. OBL-R03 split between cochain curvature and Regge metric deficit:
   - Flat 6-equilateral-triangle hinge (deficit = 0) with arbitrary nonzero cochain curvature q != 0.
   - Tetrahedral k=3 vertex deficit fullTurn / 2 and Gauss-Bonnet sum 2 * fullTurn.
   The Lean module keeps the edge-length rescaling theorem. This script does not recheck a cancelled ratio.
3. OBL-R01 lattice-spacing fence:
   - Reversal of causal character (timelike > 0, null = 0, spacelike < 0) of a fixed combinatorial
     displacement (N_t, N_x) = (2, 3) under spacing choices ax in {1/2, 2/3, 1}.
   - Manhattan (l_1) vs. Euclidean (l_2^2) mismatch across Pythagorean triples.
   The Lean module keeps the spacing-calibration theorems. This script does not recheck ax / at division.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import sys


def d0(p0: Fraction, p1: Fraction, p2: Fraction, p3: Fraction) -> tuple[Fraction, ...]:
    return (p1 - p0, p2 - p0, p3 - p0, p2 - p1, p3 - p1, p3 - p2)


def d1(omega: tuple[Fraction, ...]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    e01, e02, e03, e12, e13, e23 = omega
    return (
        e01 + e12 - e02,
        e01 + e13 - e03,
        e02 + e23 - e03,
        e12 + e23 - e13,
    )


def bianchi_sum(F: tuple[Fraction, Fraction, Fraction, Fraction]) -> Fraction:
    f012, f013, f023, f123 = F
    return f012 - f013 + f023 - f123


def regge_vertex_deficit(full_turn: Fraction, angle_sum: Fraction) -> Fraction:
    return full_turn - angle_sum


def equilateral_vertex_deficit(full_turn: Fraction, k: Fraction) -> Fraction:
    return regge_vertex_deficit(full_turn, k * (full_turn / Fraction(6, 1)))


def main() -> int:
    checks = 0
    cochain_checks = 0
    obl_r03_checks = 0
    obl_r01_checks = 0
    failures = 0

    def check(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, cochain_checks, obl_r03_checks, obl_r01_checks, failures
        checks += 1
        if bucket == "cochain":
            cochain_checks += 1
        elif bucket == "obl_r03":
            obl_r03_checks += 1
        elif bucket == "obl_r01":
            obl_r01_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [{bucket}]: {msg}", file=sys.stderr)

    # 1. Exhaustive rational sweep of d_1(d_0 phi) = 0, gauge invariance, linearity, and Bianchi
    vals = [Fraction(-2, 1), Fraction(-1, 2), Fraction(0, 1), Fraction(1, 3), Fraction(3, 2)]
    for p0, p1, p2, p3 in itertools.product(vals, repeat=4):
        cob = d0(p0, p1, p2, p3)
        curv = d1(cob)
        check(
            curv == (Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
            "cochain",
            "d_1(d_0 phi) == 0",
        )

    omega_samples = [
        (Fraction(1), Fraction(2), Fraction(-1), Fraction(3), Fraction(1, 2), Fraction(-3, 2)),
        (Fraction(0), Fraction(1, 3), Fraction(2, 5), Fraction(-1, 4), Fraction(7, 3), Fraction(1)),
        (Fraction(-5, 2), Fraction(0), Fraction(4, 3), Fraction(1, 6), Fraction(-2, 3), Fraction(5, 4)),
    ]
    c_vals = [Fraction(-3, 1), Fraction(-1, 2), Fraction(0, 1), Fraction(2, 3), Fraction(5, 1)]
    for omega in omega_samples:
        F_omega = d1(omega)
        check(bianchi_sum(F_omega) == Fraction(0), "cochain", "tetrahedral Bianchi sum == 0")
        for c in c_vals:
            c_omega = tuple(c * x for x in omega)
            check(
                d1(c_omega) == tuple(c * f for f in F_omega),
                "cochain",
                "d_1 linearity",
            )
        for p0, p1, p2 in itertools.product(vals[:3], repeat=3):
            cob = d0(p0, p1, p2, Fraction(1, 1))
            gauged = tuple(o + g for o, g in zip(omega, cob))
            check(d1(gauged) == F_omega, "cochain", "d_1 gauge invariance")

    # 2. OBL-R03 split between cochain curvature and Regge metric deficit
    turns = [Fraction(1, 1), Fraction(2, 1), Fraction(44, 7), Fraction(360, 1)]

    for ft in turns:
        # Flat 6-equilateral-triangle hinge has 0 Regge deficit while single-edge cochain has curvature q != 0
        check(
            equilateral_vertex_deficit(ft, Fraction(6, 1)) == Fraction(0),
            "obl_r03",
            "6-equilateral hinge has zero Regge deficit",
        )
        for q in [Fraction(-3, 1), Fraction(-1, 2), Fraction(1, 4), Fraction(7, 2)]:
            single_omega = (Fraction(0), Fraction(0), Fraction(0), q, Fraction(0), Fraction(0))
            F_single = d1(single_omega)
            check(
                F_single[0] == q and F_single[3] == q and F_single[0] != Fraction(0),
                "obl_r03",
                "nonzero cochain curvature on flat metric hinge",
            )

        # Tetrahedral k=3 vertex has positive Regge deficit ft/2 and Gauss-Bonnet sum 2*ft != 0
        def3 = equilateral_vertex_deficit(ft, Fraction(3, 1))
        check(
            def3 == ft / Fraction(2, 1) and def3 > Fraction(0),
            "obl_r03",
            "tetrahedral k=3 vertex has positive Regge deficit ft/2",
        )
        check(
            Fraction(4, 1) * def3 == Fraction(2, 1) * ft and Fraction(4, 1) * def3 != Fraction(0),
            "obl_r03",
            "Gauss-Bonnet sum on tetrahedron equals 2 * fullTurn != 0",
        )

    # Causal character reversal on (N_t, N_x) = (2, 3) under ax in {1/2, 2/3, 1}
    def minkowski_interval(c: Fraction, at_: Fraction, ax: Fraction, nt: int, nx: int) -> Fraction:
        return (c * nt * at_) ** 2 - (nx * ax) ** 2

    i_timelike = minkowski_interval(Fraction(1), Fraction(1), Fraction(1, 2), 2, 3)
    i_null = minkowski_interval(Fraction(1), Fraction(1), Fraction(2, 3), 2, 3)
    i_spacelike = minkowski_interval(Fraction(1), Fraction(1), Fraction(1, 1), 2, 3)
    check(
        i_timelike == Fraction(7, 4) and i_timelike > Fraction(0),
        "obl_r01",
        "ax=1/2 makes (2,3) timelike",
    )
    check(i_null == Fraction(0), "obl_r01", "ax=2/3 makes (2,3) null")
    check(
        i_spacelike == Fraction(-5, 1) and i_spacelike < Fraction(0),
        "obl_r01",
        "ax=1 makes (2,3) spacelike",
    )

    # Manhattan vs Euclidean light-cone anisotropy across Pythagorean triples
    pythagorean_triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
    for dx, dy, r in pythagorean_triples:
        check(
            dx * dx + dy * dy == r * r and (dx + dy) != r,
            "obl_r01",
            f"Pythagorean triple ({dx},{dy}) vs ({r},0) Euclidean vs Manhattan mismatch",
        )

    print(
        f"checks={checks} cochain={cochain_checks} obl_r03={obl_r03_checks} "
        f"obl_r01={obl_r01_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
