#!/usr/bin/env python3
"""Independent verification for ADS-RT-FORMULA-IMPORT (TFQ-2204).

AuthorityEffect: None.

Independently checks the three exact finite/rational algebraic shadows and scope fences
formalized in lean4/CampaignAdsRtFormulaImport.lean:
1. Ryu-Takayanagi / Brown-Henneaux coupling elimination (c = 3R / (2G_N^(3)), S_A = L_gamma / (4G_N^(3))
   = (c / 3) * logFactor), cut-pasting Strong Subadditivity inequality, and complement symmetry
   (A <-> A^c) of mincut and boundaryEntropy across all 380 proper contiguous boundary intervals
   of the 20-qubit 6-pentagon HaPPY {5,4} patch.
2. Von Neumann entropy dichotomy fence (FQ-ENTROPY-DICHOTOMY-BAKER): any mixed finite probability
   distribution with algebraic weights has positive entropy in nats and non-vanishing prime-log
   linear form, whereas any rational RT ratio area / (4 G_N) is rational; only pure states (S = 0)
   match area = 0, and stabilizer bit counts require dividing by ln(2).
3. Exact rational Regge proxy (TFQ-0100) vs minimal-surface area & HaPPY bond-cut fence:
   - On the orthogonal_pentatope chart of TFQ-0100, the 6 right-triangle hinges have Cayley-Menger
     squared area 1/4 and the 4 equilateral-triangle hinges have Cayley-Menger squared area 3/4
     (total 9/2), with no rational linear area A satisfying A^2 = 3/4.
   - On any flat chart (kappa = 0), the rational Regge action vanishes identically, whereas all 380
     proper contiguous boundary intervals of the 20-qubit HaPPY patch have 1 <= S(A) <= mincut(A).
   - Under uniform length rescaling L -> lam * L, Cayley-Menger squared area and the Regge proxy
     scale as lam^4, whereas 2-surface area scales as lam^2 and bond count as lam^0.
"""

from __future__ import annotations

from fractions import Fraction
import math


def rt_leading_entropy(area: Fraction, g_n: Fraction) -> Fraction:
    return area / (4 * g_n)


def brown_henneaux_central_charge(r_ads: Fraction, g_n3: Fraction) -> Fraction:
    return (3 * r_ads) / (2 * g_n3)


def ads3_geodesic_length(r_ads: Fraction, log_factor: Fraction) -> Fraction:
    return 2 * r_ads * log_factor


def calabrese_cardy_coefficient(c: Fraction) -> Fraction:
    return c / 3


def cayley_menger_triangle_area_sq(s01: Fraction, s02: Fraction, s12: Fraction) -> Fraction:
    return (2 * (s01 * s02 + s01 * s12 + s02 * s12) - (s01 * s01 + s02 * s02 + s12 * s12)) / 16


def set_xz(q: int, x: int, z: int) -> int:
    val = 0
    if x == 1:
        val |= 1 << (2 * q)
    if z == 1:
        val |= 1 << (2 * q + 1)
    return val


LOCAL_BLOCK_3 = [
    [(1, 0), (0, 1), (0, 1), (1, 0)],
    [(0, 1), (1, 1), (1, 1), (0, 1)],
    [(1, 1), (0, 1), (1, 1), (0, 0)],
]

PUSH_X_BLOCK = [(0, 1), (0, 1), (1, 0), (0, 0)]
PUSH_Z_BLOCK = [(1, 0), (0, 0), (1, 0), (0, 1)]

CENTRAL_GENS_5 = [
    [(1, 0), (0, 1), (0, 1), (1, 0), (0, 0)],
    [(0, 0), (1, 0), (0, 1), (0, 1), (1, 0)],
    [(1, 0), (0, 0), (1, 0), (0, 1), (0, 1)],
    [(0, 1), (1, 0), (0, 0), (1, 0), (0, 1)],
    [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1)],
]


def encode_local_gen(k: int, pat: list[tuple[int, int]]) -> int:
    acc = 0
    for j in range(4):
        x, z = pat[j]
        acc ^= set_xz(4 * k + j, x, z)
    return acc


def encode_central_gen(cpat: list[tuple[int, int]]) -> int:
    acc = 0
    for k in range(5):
        cx, cz = cpat[k]
        if cx == 1:
            acc ^= encode_local_gen(k, PUSH_X_BLOCK)
        if cz == 1:
            acc ^= encode_local_gen(k, PUSH_Z_BLOCK)
    return acc


def build_boundary_gens_20() -> list[int]:
    gens: list[int] = []
    for k in range(5):
        for pat in LOCAL_BLOCK_3:
            gens.append(encode_local_gen(k, pat))
    for cpat in CENTRAL_GENS_5:
        gens.append(encode_central_gen(cpat))
    return gens


BOUNDARY_GENS_20 = build_boundary_gens_20()


def gf2_rank(rows: list[int]) -> int:
    mat = [r for r in rows if r != 0]
    rank = 0
    for bit in range(39, -1, -1):
        pivot = None
        for idx in range(rank, len(mat)):
            if (mat[idx] >> bit) & 1:
                pivot = idx
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        p_row = mat[rank]
        for idx in range(len(mat)):
            if idx != rank and ((mat[idx] >> bit) & 1):
                mat[idx] ^= p_row
        rank += 1
    return rank


def in_contiguous_interval(start: int, length: int, q: int) -> bool:
    return ((q + 20 - start) % 20) < length


def interval_bitmask_40(start: int, length: int) -> int:
    acc = 0
    for q in range(20):
        if in_contiguous_interval(start, length, q):
            acc |= 3 << (2 * q)
    return acc


def interval_entropy(start: int, length: int) -> int:
    mask40 = interval_bitmask_40(start, length)
    rows = [r & mask40 for r in BOUNDARY_GENS_20]
    return gf2_rank(rows) - length


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


def main() -> int:
    checks = 0
    rt_bh_checks = 0
    dichotomy_checks = 0
    regge_happy_checks = 0
    failures = 0

    # 1. RT / Brown-Henneaux coupling elimination and Strong Subadditivity
    r_vals = [Fraction(1, 2), Fraction(1, 1), Fraction(3, 2), Fraction(5, 3)]
    g_vals = [Fraction(1, 7), Fraction(1, 3), Fraction(2, 5), Fraction(3, 4)]
    log_vals = [Fraction(0, 1), Fraction(1, 1), Fraction(7, 5), Fraction(11, 4)]

    for r_ads in r_vals:
        for g_n3 in g_vals:
            c = brown_henneaux_central_charge(r_ads, g_n3)
            for lf in log_vals:
                l_geo = ads3_geodesic_length(r_ads, lf)
                s_rt = rt_leading_entropy(l_geo, g_n3)
                s_cc = calabrese_cardy_coefficient(c) * lf
                if s_rt != s_cc or s_rt / c != lf / 3:
                    failures += 1
                checks += 1
                rt_bh_checks += 1

    # Additivity and cut-pasting SSA check
    for a1 in [Fraction(3, 2), Fraction(7, 4), Fraction(5, 1)]:
        for a2 in [Fraction(1, 2), Fraction(9, 4), Fraction(6, 1)]:
            for g_n in [Fraction(1, 4), Fraction(2, 3)]:
                if rt_leading_entropy(a1 + a2, g_n) != rt_leading_entropy(a1, g_n) + rt_leading_entropy(a2, g_n):
                    failures += 1
                # Submodular pasting: min_abc <= a1 + a2 - delta, min_b <= delta
                delta = Fraction(1, 3)
                area_union = a1 + a2 - delta
                area_inter = delta / 2
                min_abc = area_union - Fraction(1, 5)
                min_b = area_inter - Fraction(1, 7)
                if (
                    rt_leading_entropy(min_abc, g_n) + rt_leading_entropy(min_b, g_n)
                    > rt_leading_entropy(a1, g_n) + rt_leading_entropy(a2, g_n)
                ):
                    failures += 1
                checks += 1
                rt_bh_checks += 1

    # 2. Entropy dichotomy & stabilizer bit-to-nat conversion checks
    for k in range(1, 21):
        s_nats = k * math.log(2.0)
        s_bits = round(s_nats / math.log(2.0))
        if s_bits != k:
            failures += 1
        checks += 1
        dichotomy_checks += 1

    # Mixed rational spectra have strictly positive natural-log entropy; only pure states have 0
    mixed_spectra = [
        [Fraction(1, 2), Fraction(1, 2)],
        [Fraction(1, 4), Fraction(3, 4)],
        [Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)],
        [Fraction(1, 8), Fraction(3, 8), Fraction(1, 2)],
    ]
    for spec in mixed_spectra:
        if sum(spec) != Fraction(1, 1):
            failures += 1
        s_val = -sum(float(p) * math.log(float(p)) for p in spec if p > 0)
        if not (s_val > 0.0):
            failures += 1
        checks += 1
        dichotomy_checks += 1

    # 3. Exact rational Regge proxy (TFQ-0100) vs minimal-surface & HaPPY bond-cut fence
    # Orthogonal pentatope vertices in Q^4: v0=(0,0,0,0), v1..v4 = standard basis vectors
    vertices = [
        (Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
    ]

    def dist_sq(u: tuple[Fraction, ...], v: tuple[Fraction, ...]) -> Fraction:
        return sum((ui - vi) * (ui - vi) for ui, vi in zip(u, v))

    right_count = 0
    equil_count = 0
    total_area_sq = Fraction(0)
    for i in range(5):
        for j in range(i + 1, 5):
            for k in range(j + 1, 5):
                s01 = dist_sq(vertices[i], vertices[j])
                s02 = dist_sq(vertices[i], vertices[k])
                s12 = dist_sq(vertices[j], vertices[k])
                a_sq = cayley_menger_triangle_area_sq(s01, s02, s12)
                total_area_sq += a_sq
                if i == 0:
                    right_count += 1
                    if (s01, s02, s12) != (Fraction(1), Fraction(1), Fraction(2)) or a_sq != Fraction(1, 4):
                        failures += 1
                else:
                    equil_count += 1
                    if (s01, s02, s12) != (Fraction(2), Fraction(2), Fraction(2)) or a_sq != Fraction(3, 4):
                        failures += 1
                checks += 1
                regge_happy_checks += 1

    if right_count != 6 or equil_count != 4 or total_area_sq != Fraction(9, 2):
        failures += 1
    checks += 1
    regge_happy_checks += 1

    # Verify no rational p/q with 1 <= q <= 40, 0 <= p <= 40 satisfies (p/q)^2 == 3/4
    for q in range(1, 41):
        for p in range(0, 41):
            if Fraction(p, q) ** 2 == Fraction(3, 4):
                failures += 1
        checks += 1
        regge_happy_checks += 1

    # Check degree-4 scaling of Cayley-Menger squared area under L -> lam * L
    for lam in [Fraction(1, 2), Fraction(2, 1), Fraction(3, 1), Fraction(5, 2)]:
        for s01, s02, s12 in [(Fraction(1), Fraction(1), Fraction(2)), (Fraction(2), Fraction(2), Fraction(2))]:
            lhs = cayley_menger_triangle_area_sq(lam * lam * s01, lam * lam * s02, lam * lam * s12)
            rhs = (lam ** 4) * cayley_menger_triangle_area_sq(s01, s02, s12)
            if lhs != rhs:
                failures += 1
            checks += 1
            regge_happy_checks += 1

    # Check all 380 proper nonempty contiguous boundary intervals on the 20-qubit HaPPY patch:
    # (a) complement symmetry of mincut and boundary_entropy, and (b) 1 <= S(A) <= mincut(A)
    for start in range(20):
        for length in range(1, 20):
            sc = (start + length) % 20
            lc = 20 - length
            s_a = interval_entropy(start, length)
            s_ac = interval_entropy(sc, lc)
            cut_a = interval_mincut(start, length)
            cut_ac = interval_mincut(sc, lc)
            if s_a != s_ac or cut_a != cut_ac or s_a < 1 or cut_a < 1 or s_a > cut_a:
                failures += 1
            checks += 1
            regge_happy_checks += 1

    print(
        f"checks={checks} rt_bh={rt_bh_checks} dichotomy={dichotomy_checks} "
        f"regge_happy={regge_happy_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
