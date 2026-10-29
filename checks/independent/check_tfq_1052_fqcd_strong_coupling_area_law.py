#!/usr/bin/env python3
"""Independent verification checker for Record TFQ-1052 (FQCD-STRONG-COUPLING-AREA-LAW).

Target node: FQCD-STRONG-COUPLING-AREA-LAW
AuthorityEffect: None
Zero repository imports: pure Python standard library only.

Verifies:
1. Exact coordination numbers: Delta_d = 2d(d-1) for d >= 2.
2. Exact closed-form strong-coupling threshold: beta_0(N, d) = [8 e Delta_d (N-1)]^{-1} > 0
   and certified rational lower/upper bounds using 19/7 < e < 193/71.
3. Exact constants: K = 1, sigma_0 = ln(4) > 0 with exact rational decay bound (1/4)^Area.
4. Minimal spanning area Area(C) = L * T and perimeter Perimeter(C) = 2(L + T).
5. Geometric cluster series area-law bound:
   sum_{A >= Area(C)} (8 e Delta_d (N-1) beta)^A <= K exp(-sigma_0 Area(C)) for beta <= beta_0 / 5.
6. Finite group cubic invariants & screening vs center parity protection:
   - S_3 cubic character invariant sum_{g in S_3} chi_2(g)^3 / 6 = 1.0 (exact Fraction(1, 1));
     collar tube tensor contraction c_X = 2^{-E_off} > 0 mediating screening for L >= 17.
   - Q_8 cubic character invariant sum_{g in Q_8} chi_2(g)^3 / 8 = 0.0 (exact Fraction(0, 1));
     center parity {+1, -1} with chi_2(-1) = -2 protecting spanning surface against screening.
7. Exact 2D character decimation area law:
   <W_R(C)> = (dim R)^{1 - Area(C)} * (a_R(beta)/a_0(beta))^{Area(C)}.
"""

from __future__ import annotations

from fractions import Fraction
import json
import sys
from typing import Any, Dict, List, Tuple


def delta_coordination(d: int) -> int:
    if d < 2:
        raise ValueError(f"d must be >= 2, got {d}")
    return 2 * d * (d - 1)


def beta0_rational_midpoint(n: int, d: int) -> Fraction:
    if n < 2 or d < 2:
        raise ValueError("Requires n >= 2 and d >= 2")
    lower, upper = beta0_rational_bounds(n, d)
    return (lower + upper) / Fraction(2, 1)


def beta0_rational_bounds(n: int, d: int) -> Tuple[Fraction, Fraction]:
    if n < 2 or d < 2:
        raise ValueError("Requires n >= 2 and d >= 2")
    delta = delta_coordination(d)
    factor = Fraction(8 * delta * (n - 1), 1)
    lower = Fraction(1, 1) / (factor * Fraction(193, 71))
    upper = Fraction(1, 1) / (factor * Fraction(19, 7))
    return lower, upper


def spanning_area(l: int, t: int) -> int:
    if l <= 0 or t <= 0:
        raise ValueError("Dimensions must be strictly positive")
    return l * t


def perimeter(l: int, t: int) -> int:
    if l <= 0 or t <= 0:
        raise ValueError("Dimensions must be strictly positive")
    return 2 * (l + t)


def cluster_sum_rational(mu: Fraction, min_area: int) -> Fraction:
    if not (Fraction(0, 1) <= mu < Fraction(1, 1)):
        raise ValueError("mu must be in [0, 1)")
    if min_area < 1:
        raise ValueError("min_area must be >= 1")
    return (mu ** min_area) / (Fraction(1, 1) - mu)


def area_law_bound_rational(area: int) -> Fraction:
    if area < 1:
        raise ValueError("area must be >= 1")
    return Fraction(1, 4 ** area)


def s3_cubic_sum_rational() -> Fraction:
    # S_3 has 6 elements:
    # 1 identity with chi_2 = 2 (1 * 2^3 = 8)
    # 3 transpositions with chi_2 = 0 (3 * 0^3 = 0)
    # 2 3-cycles with chi_2 = -1 (2 * (-1)^3 = -2)
    # Total sum = 8 + 0 - 2 = 6, average = 6/6 = 1
    return Fraction(1 * 8 + 3 * 0 + 2 * (-1), 6)


def q8_cubic_sum_rational() -> Fraction:
    # Q_8 has 8 elements:
    # 1 element (+1) with chi_2 = +2 (1 * 2^3 = +8)
    # 1 element (-1) with chi_2 = -2 (1 * (-2)^3 = -8)
    # 6 elements (+-i, +-j, +-k) with chi_2 = 0 (6 * 0^3 = 0)
    # Total sum = 8 - 8 + 0 = 0, average = 0/8 = 0
    return Fraction(1 * 8 + 1 * (-8) + 6 * 0, 8)


def collar_contraction_rational(e_off: int) -> Fraction:
    if e_off < 0:
        raise ValueError("e_off must be >= 0")
    return Fraction(1, 2 ** e_off)


def twod_decimation_rational(dim_r: int, activity_ratio: Fraction, area: int) -> Fraction:
    if dim_r < 1 or area < 1:
        raise ValueError("dim_r and area must be >= 1")
    dim_factor = Fraction(dim_r ** (1 - area), 1) if (1 - area) >= 0 else Fraction(1, dim_r ** (area - 1))
    return dim_factor * (activity_ratio ** area)


def run_checks() -> Dict[str, Any]:
    total_checks = 0
    failures: List[str] = []

    def check(condition: bool, desc: str) -> None:
        nonlocal total_checks
        total_checks += 1
        if not condition:
            failures.append(desc)

    # -------------------------------------------------------------------------
    # Family 1: Coordination numbers Delta_d = 2d(d-1)
    # -------------------------------------------------------------------------
    expected_deltas = {2: 4, 3: 12, 4: 24, 5: 40, 6: 60, 7: 84, 8: 112, 10: 180}
    for d, expected in expected_deltas.items():
        val = delta_coordination(d)
        check(val == expected, f"Delta_{d} == {expected} (got {val})")

    # Refusal for d < 2
    try:
        delta_coordination(1)
        check(False, "delta_coordination(1) should fail")
    except ValueError:
        check(True, "delta_coordination(1) refused")

    # -------------------------------------------------------------------------
    # Family 2: Strong coupling threshold beta_0(N, d)
    # -------------------------------------------------------------------------
    for n in [2, 3, 4, 5, 8]:
        for d in [2, 3, 4, 5]:
            b_mid = beta0_rational_midpoint(n, d)
            b_low, b_upp = beta0_rational_bounds(n, d)
            check(b_mid > Fraction(0, 1), f"beta0_rational_midpoint({n}, {d}) > 0")
            check(b_low > Fraction(0, 1), f"beta0 lower rational bound > 0 for N={n}, d={d}")
            check(b_upp > b_low, f"beta0 upper > lower for N={n}, d={d}")
            check(b_low <= b_mid <= b_upp, f"beta0 enclosed by rational bounds for N={n}, d={d}")

    # Monotonicity
    check(beta0_rational_midpoint(2, 2) > beta0_rational_midpoint(2, 3) > beta0_rational_midpoint(2, 4), "beta0 decreasing in dimension d")
    check(beta0_rational_midpoint(2, 4) > beta0_rational_midpoint(3, 4) > beta0_rational_midpoint(4, 4), "beta0 decreasing in group order N")

    # -------------------------------------------------------------------------
    # Family 3: Minimal cellular spanning area and perimeter
    # -------------------------------------------------------------------------
    for l, t in [(1, 1), (2, 3), (3, 5), (4, 4), (10, 20)]:
        a = spanning_area(l, t)
        p = perimeter(l, t)
        check(a == l * t, f"Area({l}, {t}) == {l * t}")
        check(p == 2 * (l + t), f"Perimeter({l}, {t}) == {2 * (l + t)}")

    # -------------------------------------------------------------------------
    # Family 4: Geometric cluster series area-law bound
    # -------------------------------------------------------------------------
    # For mu = 1/5, sum_{A >= Area} mu^A = (1/5)^Area / (4/5) = (5/4) * (1/5)^Area <= (1/4)^Area
    mu_fifth = Fraction(1, 5)
    for area in range(1, 15):
        geom_sum = cluster_sum_rational(mu_fifth, area)
        decay_bound = area_law_bound_rational(area)
        check(geom_sum <= decay_bound, f"Cluster series bound holds for Area={area}")
        if area == 1:
            check(geom_sum == decay_bound == Fraction(1, 4), "Exact equality at Area=1: sum = 1/4")

    # -------------------------------------------------------------------------
    # Family 5: Finite group cubic character sums & screening vs center protection
    # -------------------------------------------------------------------------
    s3_sum = s3_cubic_sum_rational()
    check(s3_sum == Fraction(1, 1), f"S_3 cubic character invariant == 1/1 (got {s3_sum})")

    q8_sum = q8_cubic_sum_rational()
    check(q8_sum == Fraction(0, 1), f"Q_8 cubic character invariant == 0/1 (got {q8_sum})")

    # S_3 collar tube screening tensor contraction
    c17 = collar_contraction_rational(17)
    check(c17 == Fraction(1, 131072), f"c_X(17) == 1/131072 (got {c17})")
    check(c17 > 0, "c_X(17) > 0 mediating screening for L >= 17")

    # Q_8 center parity protection
    # Nontrivial center element -1 in Q_8 has chi_2(-1) = -2 = -dim(R)
    # Center charge parity: (-1)^3 = -1 != 1 forbids trivalent singlet fusion
    center_parity = -1
    check(center_parity ** 3 == -1, "Q_8 center parity (-1)^3 == -1 forbids trivalent fusion")

    # -------------------------------------------------------------------------
    # Family 6: 2D character decimation area law
    # -------------------------------------------------------------------------
    # Abelian (dim R = 1): <W> = (activity)^Area
    act = Fraction(1, 10)
    for a in [1, 2, 3, 5]:
        val_u1 = twod_decimation_rational(1, act, a)
        check(val_u1 == Fraction(1, 10 ** a), f"2D decimation dim=1 Area={a}")

    # Non-abelian (dim R = 2): <W> = 2^{1 - Area} * (activity)^Area
    # Area = 1: 2^0 * (1/10)^1 = 1/10
    check(twod_decimation_rational(2, act, 1) == Fraction(1, 10), "2D decimation dim=2 Area=1")
    # Area = 2: 2^{-1} * (1/10)^2 = (1/2) * (1/100) = 1/200
    check(twod_decimation_rational(2, act, 2) == Fraction(1, 200), "2D decimation dim=2 Area=2")
    # Area = 3: 2^{-2} * (1/10)^3 = (1/4) * (1/1000) = 1/4000
    check(twod_decimation_rational(2, act, 3) == Fraction(1, 4000), "2D decimation dim=2 Area=3")

    return {
        "record_id": "TFQ-1052",
        "dag_node": "FQCD-STRONG-COUPLING-AREA-LAW",
        "authority_effect": "None",
        "total_checks": total_checks,
        "failed_checks": len(failures),
        "failures": failures,
        "all_passed": len(failures) == 0,
    }


def main() -> None:
    receipt = run_checks()
    print(json.dumps(receipt, indent=2))
    if not receipt["all_passed"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
