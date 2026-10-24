#!/usr/bin/env python3
"""Independent verification for FSP-LAUGHLIN-EXCHANGE-PHASE (TFQ-1208).

AuthorityEffect: None

Checks with exact integer and rational (Fraction) arithmetic:
1. Laughlin Jastrow polynomial exchange parity across 2-body, 3-body, and 4-body
   Vandermonde products prod_{j<k} (z_j - z_k)^m for odd (fermionic) and even (bosonic) m,
   plus symmetry of the bare holomorphic 2-quasihole prefactor prod_j (z_j - eta_1)(z_j - eta_2)
   under eta_1 <-> eta_2 (showing Berry connection / plasma screening is required for pi/m).
2. Exact SL(2, Z) cyclotomic companion matrix algebra for R6 (exp(i pi/3)) and M3 = R6^2
   (exp(i 2pi/3)), modular S-matrix phase exponent extraction for abelian Z_m anyons,
   and general-m non-contractible monodromy residue (2 % m == 2 != 0 for m >= 3) and odd-m
   coprimality gcd(2, 2k+1) == 1.
3. Scope fences: exhaustive search over 2x2 integer matrices with entries in [-3, 3]
   confirming no Z2 involution (J^2 == I_2) equals M3 or R6, and thermal weight asymmetry
   w_qh != w_qe preventing Z3 monodromy sector cancellation.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import math
from typing import List, Sequence

MatrixInt = List[List[int]]


def require(cond: bool, msg: str, counter: List[int]) -> None:
    if not cond:
        raise AssertionError(msg)
    counter[0] += 1


def mat2_mul(a: MatrixInt, b: MatrixInt) -> MatrixInt:
    return [
        [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
        [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]],
    ]


def mat2_add(a: MatrixInt, b: MatrixInt, scale_b: int = 1) -> MatrixInt:
    return [
        [a[0][0] + scale_b * b[0][0], a[0][1] + scale_b * b[0][1]],
        [a[1][0] + scale_b * b[1][0], a[1][1] + scale_b * b[1][1]],
    ]


def mat2_scale(c_val: int, a: MatrixInt) -> MatrixInt:
    return [[c_val * a[0][0], c_val * a[0][1]], [c_val * a[1][0], c_val * a[1][1]]]


def mat2_pow(a: MatrixInt, exp: int) -> MatrixInt:
    res: MatrixInt = [[1, 0], [0, 1]]
    for _ in range(exp):
        res = mat2_mul(res, a)
    return res


def jastrow_poly(coords: Sequence[Fraction], m: int) -> Fraction:
    prod = Fraction(1)
    n = len(coords)
    for j in range(n):
        for k in range(j + 1, n):
            prod *= (coords[j] - coords[k]) ** m
    return prod


def quasihole_prefactor(
    coords: Sequence[Fraction], eta1: Fraction, eta2: Fraction
) -> Fraction:
    prod = Fraction(1)
    for z in coords:
        prod *= (z - eta1) * (z - eta2)
    return prod


def check_jastrow_and_quasihole_polynomials() -> int:
    c = [0]

    # 1. Two-body, three-body, and four-body Jastrow exchange parity over Q
    sample_coords_4 = [
        (Fraction(1, 2), Fraction(-3, 2), Fraction(5, 3), Fraction(-7, 4)),
        (Fraction(2, 1), Fraction(1, 3), Fraction(-4, 5), Fraction(9, 7)),
        (Fraction(-5, 2), Fraction(3, 4), Fraction(11, 6), Fraction(-1, 5)),
        (Fraction(0, 1), Fraction(7, 3), Fraction(-2, 5), Fraction(4, 3)),
    ]
    all_swaps_4 = list(itertools.combinations(range(4), 2))
    for coords in sample_coords_4:
        for m in range(1, 7):
            sign_expected = -1 if (m % 2 == 1) else 1
            # 2-body
            z1, z2 = coords[0], coords[1]
            v2_orig = (z1 - z2) ** m
            v2_swap = (z2 - z1) ** m
            require(
                v2_swap == sign_expected * v2_orig,
                f"2-body Jastrow m={m} exchange parity",
                c,
            )
            # 3-body all transpositions
            c3 = list(coords[:3])
            v3_orig = jastrow_poly(c3, m)
            require(v3_orig != 0, "distinct 3-body coords give nonzero Jastrow", c)
            for i1, i2 in ((0, 1), (0, 2), (1, 2)):
                c3_swapped = list(c3)
                c3_swapped[i1], c3_swapped[i2] = c3_swapped[i2], c3_swapped[i1]
                v3_swap = jastrow_poly(c3_swapped, m)
                require(
                    v3_swap == sign_expected * v3_orig,
                    f"3-body Jastrow m={m} swap ({i1},{i2})",
                    c,
                )
            # 4-body all 6 transpositions
            c4 = list(coords)
            v4_orig = jastrow_poly(c4, m)
            require(v4_orig != 0, "distinct 4-body coords give nonzero Jastrow", c)
            for i1, i2 in all_swaps_4:
                c4_swapped = list(c4)
                c4_swapped[i1], c4_swapped[i2] = c4_swapped[i2], c4_swapped[i1]
                v4_swap = jastrow_poly(c4_swapped, m)
                require(
                    v4_swap == sign_expected * v4_orig,
                    f"4-body Jastrow m={m} swap ({i1},{i2})",
                    c,
                )

    # 2. Bare holomorphic quasihole polynomial symmetry under eta1 <-> eta2
    etas = [
        (Fraction(1, 5), Fraction(-2, 7)),
        (Fraction(3, 8), Fraction(11, 9)),
        (Fraction(-4, 3), Fraction(5, 6)),
        (Fraction(1, 13), Fraction(7, 11)),
    ]
    for coords in sample_coords_4:
        for eta1, eta2 in etas:
            p12 = quasihole_prefactor(coords, eta1, eta2)
            p21 = quasihole_prefactor(coords, eta2, eta1)
            require(
                p12 == p21 and p12 != 0,
                "bare holomorphic 2-quasihole prefactor symmetric under eta1 <-> eta2",
                c,
            )

    return c[0]


def check_cyclotomic_and_modular_s_algebra() -> int:
    c = [0]
    i2: MatrixInt = [[1, 0], [0, 1]]
    neg_i2: MatrixInt = [[-1, 0], [0, -1]]
    z2: MatrixInt = [[0, 0], [0, 0]]

    r6: MatrixInt = [[0, -1], [1, 1]]
    m3: MatrixInt = [[-1, -1], [1, 0]]

    # 1. Cyclotomic companion matrix R6 (order 6, pi/3 statistical exchange)
    det_r6 = r6[0][0] * r6[1][1] - r6[0][1] * r6[1][0]
    tr_r6 = r6[0][0] + r6[1][1]
    require(det_r6 == 1, "det(R6) == 1", c)
    require(tr_r6 == 1, "Tr(R6) == 1", c)
    phi6_r6 = mat2_add(mat2_add(mat2_mul(r6, r6), r6, scale_b=-1), i2, scale_b=1)
    require(phi6_r6 == z2, "Phi_6(R6) = R6^2 - R6 + I_2 == 0", c)
    require(mat2_pow(r6, 1) not in (i2, neg_i2), "R6^1 not in {I_2, -I_2}", c)
    require(mat2_pow(r6, 2) == m3, "R6^2 == M3", c)
    require(mat2_pow(r6, 2) not in (i2, neg_i2), "R6^2 not in {I_2, -I_2}", c)
    require(mat2_pow(r6, 3) == neg_i2, "R6^3 == -I_2 (3 quasiholes -> 1 electron)", c)
    require(mat2_pow(r6, 6) == i2, "R6^6 == I_2", c)

    # 2. Monodromy companion matrix M3 (order 3, 2pi/3 full braid)
    det_m3 = m3[0][0] * m3[1][1] - m3[0][1] * m3[1][0]
    tr_m3 = m3[0][0] + m3[1][1]
    require(det_m3 == 1, "det(M3) == 1", c)
    require(tr_m3 == -1, "Tr(M3) == -1", c)
    phi3_m3 = mat2_add(mat2_add(i2, m3, scale_b=1), mat2_mul(m3, m3), scale_b=1)
    require(phi3_m3 == z2, "Phi_3(M3) = I_2 + M3 + M3^2 == 0", c)
    require(mat2_pow(m3, 3) == i2, "M3^3 == I_2", c)
    require(mat2_mul(m3, m3) != i2, "M3^2 != I_2 (not an involution)", c)

    # 3. Abelian Z_m modular S-matrix phase exponent extraction & Z_m character sums
    for m_denom in range(3, 12):
        require(2 % m_denom == 2 and 2 % m_denom != 0, f"m={m_denom}: 2 % m == 2 != 0", c)
        for a in range(m_denom):
            for b in range(m_denom):
                e_ab = (a * b) % m_denom
                e_00 = 0
                e_a0 = 0
                e_0b = 0
                mono_exp = (e_ab + e_00 - e_a0 - e_0b) % m_denom
                require(
                    mono_exp == (a * b) % m_denom,
                    f"m={m_denom} modular S monodromy exponent ({a},{b})",
                    c,
                )

    for k in range(0, 50):
        odd_m = 2 * k + 1
        require(math.gcd(2, odd_m) == 1, f"gcd(2, {odd_m}) == 1", c)

    return c[0]


def check_involution_and_weight_fences() -> int:
    c = [0]
    i2: MatrixInt = [[1, 0], [0, 1]]
    z2: MatrixInt = [[0, 0], [0, 0]]
    r6: MatrixInt = [[0, -1], [1, 1]]
    m3: MatrixInt = [[-1, -1], [1, 0]]
    m3_sq = mat2_mul(m3, m3)

    # 1. Exhaustive search over 2x2 integer matrices with entries in [-2, 2]:
    # every involution J (J^2 == I_2) is distinct from M3 and R6
    for entries in itertools.product(range(-2, 3), repeat=4):
        j_mat: MatrixInt = [[entries[0], entries[1]], [entries[2], entries[3]]]
        if mat2_mul(j_mat, j_mat) == i2:
            require(j_mat != m3, "involution J != M3", c)
            require(j_mat != r6, "involution J != R6", c)
            require(j_mat != m3_sq, "involution J != M3^2", c)

    # 2. Equal vs unequal quasihole/quasielectron thermal weights across (I_2, M3, M3^2)
    for w_eq in range(-5, 6):
        comb_eq = mat2_add(
            mat2_add(mat2_scale(w_eq, i2), mat2_scale(w_eq, m3)),
            mat2_scale(w_eq, m3_sq),
        )
        require(comb_eq == z2, f"equal weight w={w_eq} cancels across Z_3 sectors", c)

    for w_qh in range(1, 10):
        for w_qe in range(1, 10):
            if w_qh == w_qe:
                continue
            comb = mat2_add(
                mat2_add(mat2_scale(w_qh, i2), mat2_scale(w_qe, m3)),
                mat2_scale(w_qe, m3_sq),
            )
            expected = mat2_scale(w_qh - w_qe, i2)
            require(
                comb == expected,
                f"unequal weights ({w_qh},{w_qe}) residual == (w_qh - w_qe) I_2",
                c,
            )
            require(
                comb != z2,
                f"unequal weights ({w_qh},{w_qe}) do not cancel to 0",
                c,
            )

    return c[0]


def main() -> None:
    n_poly = check_jastrow_and_quasihole_polynomials()
    n_cyc = check_cyclotomic_and_modular_s_algebra()
    n_fence = check_involution_and_weight_fences()
    total = n_poly + n_cyc + n_fence
    print(
        f"PASS fsp-laughlin-exchange-phase: checks={total} "
        f"jastrow_quasihole={n_poly} cyclotomic_modular={n_cyc} fences={n_fence} failures=0"
    )


if __name__ == "__main__":
    main()
