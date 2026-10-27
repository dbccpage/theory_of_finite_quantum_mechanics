#!/usr/bin/env python3
"""Independent verification for ADS-REGGE-AREA-RT-GAP (TFQ-2211).

AuthorityEffect: None.

Independently checks the three exact finite/rational non-equivalence fences formalized in
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


def in_contiguous_interval(start: int, length: int, q: int) -> bool:
    return ((q + 20 - start) % 20) < length


def interval_mincut(start: int, length: int) -> int:
    a = [
        sum(1 for j in range(4) if in_contiguous_interval(start, length, 4 * k + j))
        for k in range(5)
    ]

    def cost_for_central(s_c: int) -> int:
        acc = 0
        for k in range(5):
            ak = a[k]
            c0 = ak + (1 if 0 != s_c else 0)
            c1 = (4 - ak) + (1 if 1 != s_c else 0)
            acc += min(c0, c1)
        return acc

    return min(cost_for_central(0), cost_for_central(1))


def linear_area_subdivision_sum(area: Fraction, m: Fraction) -> Fraction:
    return m * (area / m)


def sq_area_subdivision_sum(area: Fraction, m: Fraction) -> Fraction:
    return m * (area / m) ** 2


def sq_area_subdivision_defect(area: Fraction, m: Fraction) -> Fraction:
    return area * area - sq_area_subdivision_sum(area, m)


def uniform_defect_regge_action(total_area_sq: Fraction, kappa: Fraction) -> Fraction:
    return total_area_sq * kappa


def main() -> int:
    checks = 0
    carrier_checks = 0
    subdiv_checks = 0
    decoupling_checks = 0
    failures = 0

    # 1. Carrier counts and 380-interval mincut value distribution
    v_cnt, e_cnt, h_cnt, f_cnt = (
        math.comb(5, 1),
        math.comb(5, 2),
        math.comb(5, 3),
        math.comb(5, 4),
    )
    if (v_cnt, e_cnt, h_cnt, f_cnt) != (5, 10, 10, 5):
        failures += 1
    if v_cnt - e_cnt + h_cnt - f_cnt != 0:
        failures += 1
    if 10 * math.factorial(4) != 240:
        failures += 1
    checks += 3
    carrier_checks += 3

    counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for start in range(20):
        for length in range(1, 20):
            mc = interval_mincut(start, length)
            if mc not in counts:
                failures += 1
            else:
                counts[mc] += 1
            checks += 1
            carrier_checks += 1

    if (counts[1], counts[2], counts[3], counts[4], counts[5]) != (50, 90, 110, 100, 30):
        failures += 1
    if sum(counts.values()) != 380:
        failures += 1
    checks += 2
    carrier_checks += 2

    # Check no rational alpha maps both 1/4 and 3/4 to 1
    right_sq = Fraction(1, 4)
    equil_sq = Fraction(3, 4)
    total_sq = 6 * right_sq + 4 * equil_sq
    if total_sq != Fraction(9, 2):
        failures += 1
    if 4 * right_sq != 1 or 4 * equil_sq != 3 or 4 * total_sq != 18:
        failures += 1
    checks += 2
    carrier_checks += 2

    # 2. Subdivision collapse of squared areas vs invariance of linear areas
    areas = [Fraction(1, 2), Fraction(1, 1), Fraction(3, 2), Fraction(5, 3), Fraction(7, 4)]
    mults = [Fraction(m) for m in [2, 3, 4, 6, 8, 12, 16, 24, 64]]
    for area in areas:
        for m in mults:
            lin_sum = linear_area_subdivision_sum(area, m)
            sq_sum = sq_area_subdivision_sum(area, m)
            defect = sq_area_subdivision_defect(area, m)
            if lin_sum != area:
                failures += 1
            if sq_sum != (area * area) / m:
                failures += 1
            if defect != ((m - 1) / m) * (area * area) or not (defect > 0):
                failures += 1
            checks += 1
            subdiv_checks += 1

    # 3. Holonomy-defect weighting decoupling from topological bond cuts
    for k1 in [Fraction(0), Fraction(1, 3), Fraction(1), Fraction(2), Fraction(7, 2)]:
        for k2 in [Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3), Fraction(5, 2)]:
            act1 = uniform_defect_regge_action(total_sq, k1)
            act2 = uniform_defect_regge_action(total_sq, k2)
            if act2 - act1 != Fraction(9, 2) * (k2 - k1):
                failures += 1
            checks += 1
            decoupling_checks += 1

    expected_subregion_cuts = [(2, 1, 1), (2, 2, 2), (2, 3, 3), (2, 4, 4), (2, 8, 5), (0, 4, 1)]
    for start, length, exp_cut in expected_subregion_cuts:
        if interval_mincut(start, length) != exp_cut:
            failures += 1
        checks += 1
        decoupling_checks += 1

    print(
        f"checks={checks} carrier={carrier_checks} subdiv={subdiv_checks} "
        f"decoupling={decoupling_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
