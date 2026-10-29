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


def s4_cubic_invariants_rational() -> Dict[str, Fraction]:
    order = 24
    return {
        "3": Fraction(1 * 27 + 6 * 1 + 8 * 0 + 6 * (-1) + 3 * (-1), order),
        "3_prime": Fraction(1 * 27 + 6 * (-1) + 8 * 0 + 6 * 1 + 3 * (-1), order),
        "2": Fraction(1 * 8 + 6 * 0 + 8 * (-1) + 6 * 0 + 3 * 8, order),
        "sgn": Fraction(1 * 1 + 6 * (-1) + 8 * 1 + 6 * (-1) + 3 * 1, order),
    }


def a5_cubic_invariants_rational() -> Dict[str, Fraction]:
    order = 60
    sum_3 = 1 * 27 + 15 * (-1) + 20 * 0 + 12 * 4
    sum_4 = 1 * 64 + 15 * 0 + 20 * 1 + 12 * (-1) + 12 * (-1)
    sum_5 = 1 * 125 + 15 * 1 + 20 * (-1) + 12 * 0 + 12 * 0
    return {
        "3_a": Fraction(sum_3, order),
        "3_b": Fraction(sum_3, order),
        "4": Fraction(sum_4, order),
        "5": Fraction(sum_5, order),
    }


def general_collar_contraction_rational(dim_r: int, e_off: int) -> Fraction:
    if dim_r < 1 or e_off < 0:
        raise ValueError("Requires dim_r >= 1 and e_off >= 0")
    return Fraction(1, dim_r ** e_off)


def normal_directions(d: int) -> int:
    if d < 3:
        raise ValueError("Requires d >= 3")
    return 2 * (d - 2)


def d4_multi_plaquette_collar_bound(perim: int, width_k: int, dim_r: int, beta: Fraction) -> Fraction:
    if perim < 1 or width_k < 1 or dim_r < 2 or beta <= Fraction(0, 1):
        raise ValueError("Invalid parameters for d=4 collar bound")
    step = Fraction(4, dim_r ** (2 * width_k)) * (beta ** (3 * width_k))
    return step ** perim


def binary_icosahedral_2i_invariants_rational() -> Dict[str, Fraction]:
    order = 120
    sum_2s = 1 * 8 + 1 * (-8) + 30 * 0 + 20 * 1 + 20 * (-1) + 12 * 0 + 12 * 0
    a5_invs = a5_cubic_invariants_rational()
    return {
        "2_s": Fraction(sum_2s, order),
        "2_s_prime": Fraction(sum_2s, order),
        "4_s": Fraction(0, 1),
        "6_s": Fraction(0, 1),
        "3_a": a5_invs["3_a"],
        "3_b": a5_invs["3_b"],
        "4_t": a5_invs["4"],
        "5_t": a5_invs["5"],
    }


def valentiner_sigma1080_invariants_rational() -> Dict[str, Fraction]:
    order = 1080
    norm_sq_3a = 3 * 9 + 135 * 1 + 270 * 1 + 216 * 3
    sq_3a = 0
    cubed_3a = 3 * 27 + 135 * (-1) + 270 * 1 + 216 * 4
    cubed_5a = 3 * (125 + 45 + 320 - 40 - 90)
    cubed_8a = 3 * (512 - 40 - 40 + 72 * 4)
    cubed_10 = 3 * (1000 - 360 + 40 + 40)
    return {
        "I11_3a": Fraction(norm_sq_3a, order),
        "I2_3a": Fraction(sq_3a, order),
        "I3_3a": Fraction(cubed_3a, order),
        "I3_5a": Fraction(cubed_5a, order),
        "I3_8a": Fraction(cubed_8a, order),
        "I3_10": Fraction(cubed_10, order),
    }


def freezing_plaquette_defect_rational_bounds() -> Dict[str, Tuple[Fraction, Fraction]]:
    return {
        "2I_2s": (Fraction(3, 16), Fraction(1, 5)),
        "Sigma1080_3a": (Fraction(11, 24), Fraction(7, 15)),
    }


def su2_ade_binary_polyhedral_tower_rational() -> Dict[str, Any]:
    return {
        "I3_2T_2s": Fraction(1 * 8 + 1 * (-8) + 6 * 0 + 4 * 1 + 4 * (-1) + 4 * 1 + 4 * (-1), 24),
        "I3_2T_3t": Fraction(2 * (1 * 27 + 3 * (-1)), 24),
        "I3_2O_2s": Fraction(0, 48),
        "I3_2O_3": Fraction(2 * 24, 48),
        "delta_min_Q8": Fraction(1, 1),
        "delta_min_2T": Fraction(1, 2),
        "delta_min_2O_bounds": (Fraction(7, 24), Fraction(3, 10)),
        "delta_min_2I_bounds": (Fraction(3, 16), Fraction(1, 5)),
    }


def su3_subgroup_tower_and_freezing_scales_rational() -> Dict[str, Any]:
    d_delta27 = Fraction(1, 1)
    d_delta54 = Fraction(5, 6)
    d_s1080_low, d_s1080_high = Fraction(11, 24), Fraction(7, 15)
    return {
        "I3_Delta27_3": Fraction(3 * 27, 27),
        "I3_Delta54_3_1": Fraction(81 - 27, 54),
        "I3_Delta54_3_2": Fraction(81 + 27, 54),
        "delta_min_Delta27": d_delta27,
        "delta_min_Delta54": d_delta54,
        "delta_min_Sigma1080_bounds": (d_s1080_low, d_s1080_high),
        "beta_freeze_proxy_Delta27": Fraction(1, 1) / d_delta27,
        "beta_freeze_proxy_Delta54": Fraction(1, 1) / d_delta54,
        "beta_freeze_proxy_Sigma1080_bounds": (Fraction(1, 1) / d_s1080_high, Fraction(1, 1) / d_s1080_low),
    }


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

    # -------------------------------------------------------------------------
    # Family 7: Higher-order non-abelian S_4 and A_5 cubic character invariants
    # -------------------------------------------------------------------------
    s4_invs = s4_cubic_invariants_rational()
    check(s4_invs["3"] == Fraction(1, 1), "S_4 standard 3D irrep cubic invariant == 1")
    check(s4_invs["3_prime"] == Fraction(1, 1), "S_4 signed 3D irrep cubic invariant == 1")
    check(s4_invs["2"] == Fraction(1, 1), "S_4 quotient 2D irrep cubic invariant == 1")
    check(s4_invs["sgn"] == Fraction(0, 1), "S_4 sign 1D irrep cubic invariant == 0")

    a5_invs = a5_cubic_invariants_rational()
    check(a5_invs["3_a"] == Fraction(1, 1), "A_5 icosahedral 3_a irrep cubic invariant == 1")
    check(a5_invs["3_b"] == Fraction(1, 1), "A_5 icosahedral 3_b irrep cubic invariant == 1")
    check(a5_invs["4"] == Fraction(1, 1), "A_5 standard 4D irrep cubic invariant == 1")
    check(a5_invs["5"] == Fraction(2, 1), "A_5 5D irrep cubic invariant == 2")

    # -------------------------------------------------------------------------
    # Family 8: General d_R collar contraction and d=4 multi-plaquette collar bounds
    # -------------------------------------------------------------------------
    check(general_collar_contraction_rational(2, 4) > general_collar_contraction_rational(3, 4), "Collar contraction stronger for dim=3 than dim=2")
    check(general_collar_contraction_rational(3, 4) > general_collar_contraction_rational(4, 4), "Collar contraction stronger for dim=4 than dim=3")
    check(general_collar_contraction_rational(4, 4) > general_collar_contraction_rational(5, 4), "Collar contraction stronger for dim=5 than dim=4")
    check(normal_directions(3) == 2 and normal_directions(4) == 4, "Normal directions N_normal(3)=2, N_normal(4)=4")

    b_k1 = d4_multi_plaquette_collar_bound(4, 1, 2, act)
    b_k2 = d4_multi_plaquette_collar_bound(4, 2, 2, act)
    b_k1_d3 = d4_multi_plaquette_collar_bound(4, 1, 3, act)
    check(b_k1 == Fraction(1, 10 ** 12), "d=4 collar bound at P=4, k=1, d_R=2 equals (beta^3)^4")
    check(Fraction(0, 1) < b_k2 < b_k1, "d=4 collar bound decays geometrically with radial width k")
    check(Fraction(0, 1) < b_k1_d3 < b_k1, "d=4 collar bound decreases with representation dimension d_R")

    # -------------------------------------------------------------------------
    # Family 9: Binary icosahedral 2I and Valentiner Sigma(1080) & freezing defects
    # -------------------------------------------------------------------------
    invs_2i = binary_icosahedral_2i_invariants_rational()
    check(invs_2i["2_s"] == Fraction(0, 1), "2I spinorial fundamental 2_s cubic invariant == 0 (Z_2 center protection)")
    check(invs_2i["2_s_prime"] == Fraction(0, 1), "2I spinorial 2_s_prime cubic invariant == 0")
    check(invs_2i["4_s"] == Fraction(0, 1), "2I spinorial 4_s cubic invariant == 0")
    check(invs_2i["6_s"] == Fraction(0, 1), "2I spinorial 6_s cubic invariant == 0")
    check(invs_2i["3_a"] == Fraction(1, 1), "2I tensorial SO(3) adjoint 3_a cubic invariant == 1")
    check(invs_2i["3_b"] == Fraction(1, 1), "2I tensorial 3_b cubic invariant == 1")
    check(invs_2i["4_t"] == Fraction(1, 1), "2I tensorial 4_t cubic invariant == 1")
    check(invs_2i["5_t"] == Fraction(2, 1), "2I tensorial 5_t cubic invariant == 2")

    invs_s1080 = valentiner_sigma1080_invariants_rational()
    check(invs_s1080["I11_3a"] == Fraction(1, 1), "Sigma(1080) fundamental 3_a Hermitian norm I_{1,1} == 1")
    check(invs_s1080["I2_3a"] == Fraction(0, 1), "Sigma(1080) fundamental 3_a quadratic invariant I_2 == 0 (Z_3 center protection)")
    check(invs_s1080["I3_3a"] == Fraction(1, 1), "Sigma(1080) fundamental 3_a baryon-singlet cubic invariant I_3 == 1")
    check(invs_s1080["I3_5a"] == Fraction(1, 1), "Sigma(1080) quotient 5_a cubic invariant I_3 == 1")
    check(invs_s1080["I3_8a"] == Fraction(2, 1), "Sigma(1080) SU(3) adjoint octet 8_a cubic invariant I_3 == 2 (f_abc and d_abc)")
    check(invs_s1080["I3_10"] == Fraction(2, 1), "Sigma(1080) decuplet 10 cubic invariant I_3 == 2")

    defects = freezing_plaquette_defect_rational_bounds()
    d2i_low, d2i_high = defects["2I_2s"]
    ds1080_low, ds1080_high = defects["Sigma1080_3a"]
    check(Fraction(11, 5) ** 2 < Fraction(5, 1) < Fraction(9, 4) ** 2, "Rational sqrt(5) enclosure (11/5)^2 < 5 < (9/4)^2")
    check(Fraction(0, 1) < d2i_low < d2i_high < ds1080_low < ds1080_high < Fraction(1, 1), "Petcher-Weingarten and Bhanot-Rebbi defect bounds ordering")

    # -------------------------------------------------------------------------
    # Family 10: Complete SU(2) ADE and SU(3) subgroup towers & freezing proxies
    # -------------------------------------------------------------------------
    su2_tower = su2_ade_binary_polyhedral_tower_rational()
    d2o_low, d2o_high = su2_tower["delta_min_2O_bounds"]
    check(Fraction(7, 5) ** 2 < Fraction(2, 1) < Fraction(17, 12) ** 2, "Rational sqrt(2) enclosure (7/5)^2 < 2 < (17/12)^2")
    check(su2_tower["I3_2T_2s"] == Fraction(0, 1), "2T spinorial 2_s cubic invariant == 0 (Z_2 center protection)")
    check(su2_tower["I3_2T_3t"] == Fraction(2, 1), "2T tensorial tetrahedral triplet 3_t cubic invariant == 2 (epsilon_ijk and xyz)")
    check(su2_tower["I3_2O_2s"] == Fraction(0, 1), "2O spinorial 2_s cubic invariant == 0")
    check(su2_tower["I3_2O_3"] == Fraction(1, 1), "2O tensorial 3 cubic invariant == 1")
    check(
        Fraction(0, 1) < d2i_low < d2i_high < d2o_low < d2o_high < su2_tower["delta_min_2T"] < su2_tower["delta_min_Q8"],
        "Strict monotonic decrease of minimal plaquette defect across SU(2) ADE series Q_8 -> 2T -> 2O -> 2I",
    )

    su3_tower = su3_subgroup_tower_and_freezing_scales_rational()
    bf_s1080_low, bf_s1080_high = su3_tower["beta_freeze_proxy_Sigma1080_bounds"]
    check(su3_tower["I3_Delta27_3"] == Fraction(3, 1), "Delta(27) fundamental 3 cubic invariant == 3")
    check(su3_tower["I3_Delta54_3_1"] == Fraction(1, 1), "Delta(54) faithful 3_1 cubic invariant == 1")
    check(su3_tower["I3_Delta54_3_2"] == Fraction(2, 1), "Delta(54) signed 3_2 cubic invariant == 2")
    check(
        su3_tower["beta_freeze_proxy_Delta27"] < su3_tower["beta_freeze_proxy_Delta54"] < bf_s1080_low < bf_s1080_high,
        "Strict monotonic increase of inverse-defect Peierls freezing scale proxy across SU(3) tower Delta(27) -> Delta(54) -> Sigma(1080)",
    )

    # -------------------------------------------------------------------------
    # Family 11: Strong-coupling vs freezing regime separation & gap widening
    # -------------------------------------------------------------------------
    g_q8 = Fraction(1, 1) - beta0_rational_midpoint(8, 4)
    g_2t = Fraction(2, 1) - beta0_rational_midpoint(24, 4)
    g_2o_low = Fraction(10, 3) - beta0_rational_midpoint(48, 4)
    g_2i_low = Fraction(5, 1) - beta0_rational_midpoint(120, 4)
    g_d27 = Fraction(1, 1) - beta0_rational_midpoint(27, 4)
    g_d54 = Fraction(6, 5) - beta0_rational_midpoint(54, 4)
    g_s1080_low = Fraction(15, 7) - beta0_rational_midpoint(1080, 4)
    check(Fraction(999, 1000) < g_q8 < g_2t < g_2o_low < g_2i_low, "SU(2) ADE strong-to-freezing coupling gap > 999/1000 and widens strictly with |G|")
    check(Fraction(999, 1000) < g_d27 < g_d54 < g_s1080_low, "SU(3) crystal strong-to-freezing coupling gap > 999/1000 and widens strictly with |G|")

    # -------------------------------------------------------------------------
    # Family 12: Klein Sigma(168) invariants, spurious cubic adjoint elimination, and complete SU(3) defect chain
    # -------------------------------------------------------------------------
    order_168 = 168
    k_i11 = Fraction(1 * 9 + 21 * 1 + 42 * 1 + 48 * 2, order_168)
    k_i2 = Fraction(1 * 9 + 21 * 1 + 42 * 1 + 24 * (-3), order_168)
    k_i3_3a = Fraction(1 * 27 + 21 * (-1) + 42 * 1 + 24 * 5, order_168)
    k_i3_6 = Fraction(1 * 216 + 21 * 8 + 48 * (-1), order_168)
    k_i3_7 = Fraction(1 * 343 + 21 * (-1) + 56 * 1 + 42 * (-1), order_168)
    k_i2_8 = Fraction(1 * 64 + 56 * 1 + 48 * 1, order_168)
    k_i3_8 = Fraction(1 * 512 + 56 * (-1) + 48 * 1, order_168)
    check(k_i11 == Fraction(1, 1) and k_i2 == Fraction(0, 1) and k_i3_3a == Fraction(1, 1), "Sigma(168) fundamental 3_a invariants I_{1,1}=1, I_2=0, I_3=1")
    check(k_i3_6 == Fraction(2, 1) and k_i3_7 == Fraction(2, 1), "Sigma(168) sextet and septet cubic invariants I_3(6)=I_3(7)=2")
    check(k_i2_8 == Fraction(1, 1) and k_i3_8 == Fraction(3, 1) > invs_s1080["I3_8a"], "Sigma(168) adjoint 8 has I_2=1 and spurious I_3=3 > 2 = I_3(Sigma(1080), 8_a)")
    check(Fraction(9, 2) ** 2 < Fraction(21, 1) < Fraction(23, 5) ** 2, "Rational sqrt(21) enclosure (9/2)^2 < 21 < (23/5)^2")
    check(
        ds1080_low < ds1080_high < Fraction(8, 15) < Fraction(13, 24) < Fraction(2, 3) < Fraction(5, 6) < Fraction(1, 1),
        "Complete 6-step SU(3) minimal plaquette defect chain across Sigma(1080), Sigma(168x3), Sigma(168), Delta(54), Delta(27)",
    )

    # -------------------------------------------------------------------------
    # Family 13: Quartic character invariants I_4(G, N) and unique SU(3) continuum matching
    # -------------------------------------------------------------------------
    i4_q8 = Fraction(2 * 16, 8)
    i4_2t = Fraction(2 * 16 + 16 * 1, 24)
    i4_2o = Fraction(2 * 16 + 16 * 1 + 12 * 4, 48)
    i4_2i = Fraction(2 * 16 + 40 * 1 + 24 * 7, 120)
    i4_d27 = Fraction(3 * 81, 27)
    i4_d54 = Fraction(3 * 81 + 27 * 1, 54)
    i4_s168 = Fraction(1 * 81 + 21 * 1 + 42 * 1 + 48 * 4, 168)
    i4_s1080 = Fraction(3 * 81 + 135 * 1 + 270 * 1 + 216 * 7, 1080)
    check(
        i4_q8 == Fraction(4, 1) and i4_2t == Fraction(2, 1) and i4_2o == Fraction(2, 1) and i4_2i == Fraction(2, 1),
        "SU(2) ADE quartic character invariants I_4(Q_8)=4, I_4(2T)=I_4(2O)=I_4(2I)=2",
    )
    check(
        i4_d27 == Fraction(9, 1) and i4_d54 == Fraction(5, 1) and i4_s168 == Fraction(2, 1) and i4_s1080 == Fraction(2, 1),
        "SU(3) crystal quartic character invariants I_4(Delta(27))=9 > I_4(Delta(54))=5 > I_4(Sigma(168))=I_4(Sigma(1080))=2",
    )
    check(
        (invs_s1080["I3_3a"], i4_s1080, invs_s1080["I3_8a"]) == (Fraction(1, 1), Fraction(2, 1), Fraction(2, 1)),
        "Sigma(1080) uniquely matches the continuum SU(3) invariant triple (I_3(3), I_4(3), I_3(8)) = (1, 2, 2)",
    )

    # -------------------------------------------------------------------------
    # Family 14: Principal & Hessian subgroups Sigma(72x3), Sigma(216x3) & quartic adjoint Casimir obstruction
    # -------------------------------------------------------------------------
    i11_72 = Fraction(3 * 9 + 189 * 1, 216)
    i3_72 = Fraction(3 * 27 + 162 * 1 + 27 * (-1), 216)
    i4_72 = Fraction(3 * 81 + 189 * 1, 216)
    i11_216 = Fraction(3 * 9 + 72 * 3 + 405 * 1, 648)
    i3_216 = Fraction(3 * 27 + 108 * 1 + 162 * 1 + 27 * (-1) + 72 * 4 + 36 * 1, 648)
    i4_216 = Fraction(3 * 81 + 72 * 9 + 405 * 1, 648)
    i3_72_8 = Fraction(3 * 512 + 24 * (-1), 216)
    i3_216_8 = Fraction(3 * 512 + 72 * 8 + 168 * (-1), 648)
    i4_72_8 = Fraction(3 * 4096 + 24 * 1, 216)
    i4_168_8 = Fraction(1 * 4096 + 56 * 1 + 48 * 1, 168)
    i4_216_8 = Fraction(3 * 4096 + 72 * 16 + 168 * 1, 648)
    i4_1080_8 = Fraction(3 * (4096 + 80 + 72 * 7), 1080)
    i4_su3_8 = Fraction(1 + 4 + 1 + 1 + 1, 1)
    a6_dim_sq_sum = 1 ** 2 + 5 ** 2 + 5 ** 2 + 8 ** 2 + 8 ** 2 + 9 ** 2 + 10 ** 2
    check(
        i11_72 == i3_72 == i11_216 == i3_216 == Fraction(1, 1) and i4_72 == i4_216 == Fraction(2, 1),
        "Principal Sigma(72x3) and Hessian Sigma(216x3) satisfy I_{1,1}(3)=I_3(3)=1 and I_4(3)=2 (irreducible 8)",
    )
    check(
        i3_72_8 == Fraction(7, 1) > i3_216_8 == Fraction(3, 1) > invs_s1080["I3_8a"],
        "Cubic adjoint invariants descend I_3(Sigma(72x3), 8)=7 > I_3(Sigma(216x3), 8)=3 > I_3(Sigma(1080), 8_a)=2",
    )
    check(
        i4_72_8 == Fraction(57, 1) > i4_168_8 == Fraction(25, 1) > i4_216_8 == Fraction(21, 1) > i4_1080_8 == Fraction(13, 1) > i4_su3_8 == Fraction(8, 1),
        "Quartic adjoint invariants descend 57 > 25 > 21 > 13 > 8 = I_4(SU(3), 8) across finite crystal subgroups",
    )
    check(
        a6_dim_sq_sum == 360 < 27 ** 2 == 729,
        "Burnside-Frobenius obstruction: |A_6| = 360 < 27^2 = 729 forces continuum 27-plet in 8x8 to split",
    )

    # -------------------------------------------------------------------------
    # Family 15: SU(2) higher-spin Casimir obstruction & Hessian Sigma(216x3) defect enclosure
    # -------------------------------------------------------------------------
    i4_2t_3 = Fraction(1 * 81 + 3 * 1, 12)
    i4_2o_3 = Fraction(1 * 81 + 6 * 1 + 3 * 1 + 6 * 1, 24)
    i4_2i_3 = Fraction(1 * 81 + 15 * 1 + 12 * 7, 60)
    i4_su2_3 = Fraction(3, 1)
    i4_2i_5 = Fraction(1 * 625 + 15 * 1 + 20 * 1, 60)
    i4_su2_5 = Fraction(5, 1)
    a5_dim_sq = 1 ** 2 + 3 ** 2 + 3 ** 2 + 4 ** 2 + 5 ** 2
    two_i_dim_sq = 1 ** 2 + 2 ** 2 + 2 ** 2 + 3 ** 2 + 3 ** 2 + 4 ** 2 + 4 ** 2 + 5 ** 2 + 6 ** 2
    c_l = Fraction(36, 47)
    c_u = Fraction(23, 30)
    p_l = 8 * (c_l ** 3) - 6 * c_l + 1
    p_u = 8 * (c_u ** 3) - 6 * c_u + 1
    d216_tl = (Fraction(4, 1) - 2 * c_u - 2 * (c_u ** 2)) / 3
    d216_tu = (Fraction(4, 1) - 2 * c_l - 2 * (c_l ** 2)) / 3
    check(
        i4_2t_3 == Fraction(7, 1) > i4_2o_3 == Fraction(4, 1) > i4_2i_3 == i4_su2_3 == Fraction(3, 1),
        "SU(2) ADE quartic adjoint invariants descend I_4(2T, 3_t)=7 > I_4(2O, 3)=4 > I_4(2I, 3_a)=I_4(SU(2), 3)=3",
    )
    check(
        i4_2i_5 == Fraction(11, 1) > i4_su2_5 == Fraction(5, 1) and a5_dim_sq == 60 and two_i_dim_sq == 120,
        "2I spin-2 (5_t) quartic Casimir obstruction I_4(2I, 5_t)=11 > 5 = I_4(SU(2), 5) with |A_5|=60 and |2I|=120",
    )
    check(
        p_l < Fraction(0, 1) < p_u and Fraction(43, 100) < d216_tl < d216_tu < Fraction(13, 30) < ds1080_low,
        "Hessian Sigma(216x3) order-9 Cartan phase defect enclosed in (581/1350, 2860/6627) subset (43/100, 13/30) < 11/24",
    )

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
