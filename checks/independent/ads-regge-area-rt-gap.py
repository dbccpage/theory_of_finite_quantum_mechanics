#!/usr/bin/env python3
"""Independent verification for ADS-REGGE-AREA-RT-GAP (TFQ-2211).

AuthorityEffect: None.

Checks finite arithmetic conditional on supplied hinge and triangulation counts;
does not construct the simplicial incidence or derive a tensor-network model.
Related formal statements are in
lean4/AdsReggeAreaRtGap.lean:
1. Simplicial Regge hinge carrier (10 hinges = 6 right + 4 equilateral on orthogonal_pentatope,
   240 Kuhn pentatopes on closed_s4_cube_boundary) vs. 6-pentagon HaPPY {5,4} network (6 tensors,
   5 internal bonds, 20 boundary legs, 380 proper contiguous boundary intervals with mincut
   distribution (50, 90, 110, 100, 30) across values {1, 2, 3, 4, 5}), and absence of a single
   rational constant alpha mapping both hinge squared-area classes (1/4, 3/4) to unit bond weight 1.
2. Subdivision collapse of squared hinge areas (m * (A / m)^2 = A^2 / m, defect ((m - 1)/m) * A^2 > 0
   for m > 1, A != 0) vs. subdivision invariance of linear areas (m * (A / m) = A).
3. Holonomy-defect weighting (kappa_h) decoupling from topological bond cuts (ReggePachnerWdw
   flat vs. curved vertex dichotomy, linear scaling (9/2) * kappa on orthogonal_pentatope, and
   subregion mincut variation across {1, 2, 3, 4, 5} on the fixed flat-background HaPPY network).
"""

from __future__ import annotations

from fractions import Fraction
import math

# Shared checker infrastructure only; no production implementation is imported.
from pathlib import Path as _Path
import sys as _sys
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli
from checker_support.cases import Cases
from checker_support.domains import MAX_RATIONAL_BITS, integer, rational


from checker_support.happy_boundary import interval_mincut


def linear_area_subdivision_sum(area: Fraction, m: int) -> Fraction:
    area = rational(area, "area", minimum=0)
    integer(m, "subdivision count", 1, (1 << MAX_RATIONAL_BITS) - 1)
    return m * (area / m)


def sq_area_subdivision_sum(area: Fraction, m: int) -> Fraction:
    area = rational(area, "area", minimum=0)
    integer(m, "subdivision count", 1, (1 << MAX_RATIONAL_BITS) - 1)
    return m * (area / m) ** 2


def sq_area_subdivision_defect(area: Fraction, m: int) -> Fraction:
    area = rational(area, "area", minimum=0)
    integer(m, "subdivision count", 1, (1 << MAX_RATIONAL_BITS) - 1)
    return area * area - sq_area_subdivision_sum(area, m)


def uniform_defect_regge_action(total_area_sq: Fraction, kappa: Fraction) -> Fraction:
    # Algebraic polynomial on Q, as in Lean; signed curvature is admitted.
    total_area_sq = rational(total_area_sq, "total squared area")
    kappa = rational(kappa, "curvature defect")
    return total_area_sq * kappa


def check_supplied_carrier_counts(run: Cases) -> Fraction:
    v_cnt, e_cnt, h_cnt, f_cnt = (
        math.comb(5, 1),
        math.comb(5, 2),
        math.comb(5, 3),
        math.comb(5, 4),
    )
    run.require(
        (v_cnt, e_cnt, h_cnt, f_cnt) == (5, 10, 10, 5),
        "pentatope incidence counts",
    )
    run.require(
        v_cnt - e_cnt + h_cnt - f_cnt == 0,
        "boundary Euler characteristic",
    )
    run.require(
        10 * math.factorial(4) == 240,
        "Kuhn count",
    )


    counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for start in range(20):
        for length in range(1, 20):
            mc = interval_mincut(start, length)
            run.require(mc in counts, "mincut belongs to 1..5")
            counts[mc] += 1


    run.require(
        (counts[1], counts[2], counts[3], counts[4], counts[5]) == (50, 90, 110, 100, 30),
        "mincut distribution",
    )
    run.require(
        sum(counts.values()) == 380,
        "380 intervals",
    )


    # Check no rational alpha maps both 1/4 and 3/4 to 1
    right_sq = Fraction(1, 4)
    equil_sq = Fraction(3, 4)
    total_sq = 6 * right_sq + 4 * equil_sq
    run.require(
        total_sq == Fraction(9, 2),
        "total squared hinge area",
    )
    run.require(
        4 * right_sq == 1 and 4 * equil_sq == 3 and (4 * total_sq == 18),
        "no common unit normalization",
    )


    return total_sq


def check_subdivisions(run: Cases) -> None:
    areas = [Fraction(1, 2), Fraction(1, 1), Fraction(3, 2), Fraction(5, 3), Fraction(7, 4)]
    mults = [2, 3, 4, 6, 8, 12, 16, 24, 64]
    for area in areas:
        for m in mults:
            lin_sum = linear_area_subdivision_sum(area, m)
            sq_sum = sq_area_subdivision_sum(area, m)
            defect = sq_area_subdivision_defect(area, m)
            run.require(
                lin_sum == area,
                "linear subdivision invariance",
            )
            run.require(
                sq_sum == area * area / m,
                "squared subdivision collapse",
            )
            run.require(
                defect == Fraction(m - 1, m) * (area * area) and defect > 0,
                "positive squared-area defect",
            )


def check_defect_weighting(total_sq: Fraction, run: Cases) -> None:
    total_sq = rational(total_sq, "total squared area")
    for k1 in [Fraction(0), Fraction(1, 3), Fraction(1), Fraction(2), Fraction(7, 2)]:
        for k2 in [Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3), Fraction(5, 2)]:
            act1 = uniform_defect_regge_action(total_sq, k1)
            act2 = uniform_defect_regge_action(total_sq, k2)
            run.require(
                act2 - act1 == Fraction(9, 2) * (k2 - k1),
                "recorded subregion cut",
            )


    expected_subregion_cuts = [(2, 1, 1), (2, 2, 2), (2, 3, 3), (2, 4, 4), (2, 8, 5), (0, 4, 1)]
    for start, length, exp_cut in expected_subregion_cuts:
        run.require(
            interval_mincut(start, length) == exp_cut,
            "curvature action difference",
        )


def main() -> int:
    carrier, subdivision, decoupling = Cases(), Cases(), Cases()
    total_sq = check_supplied_carrier_counts(carrier)
    check_subdivisions(subdivision)
    check_defect_weighting(total_sq, decoupling)
    checks = carrier.checks + subdivision.checks + decoupling.checks
    print(f"checks={checks} carrier={carrier.checks} subdiv={subdivision.checks} "
          f"decoupling={decoupling.checks} failures=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
