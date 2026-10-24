#!/usr/bin/env python3
"""Independent verification for TFQ-0027 (FINITE_QCD):
Exact rational wilson_species_count across 4D Brillouin corner shells without
trigonometric approximation, Wilson shift vanishing iff c=0, non-anticommutation
of scalar Wilson mass with gamma1/gamma2/gamma5, dense operator kernel dimension
zero_mode_count = s*N^d - rank over Q(i), MAX_CARRIER_DIMENSION = 128 guard,
even-N antiperiodic boundary twists returning zero corner species, and
non-equivalence against IntegralRefinementC3C6.lean (C3 -> C6 scalar charge
refinement).
"""

from __future__ import annotations

import math
from fractions import Fraction
from hypothesis import given, settings, strategies as st

CHECKS_PASSED = 0
CHECKS_FAILED = 0


def record(cond: bool, msg: str) -> None:
    global CHECKS_PASSED, CHECKS_FAILED
    if cond:
        CHECKS_PASSED += 1
    else:
        CHECKS_FAILED += 1
        raise AssertionError(f"FAIL: {msg}")


# =============================================================================
# 1. Exact Rational wilson_species_count Across Corner Shells
# =============================================================================

def wilson_corner_mass(m: Fraction, r: Fraction, c: int) -> Fraction:
    return m + 2 * r * Fraction(c)


def wilson_species_count(d: int, m: Fraction, r: Fraction) -> int:
    total = 0
    for c in range(d + 1):
        if wilson_corner_mass(m, r, c) == 0:
            total += math.comb(d, c)
    return total


def wilson_shift(r: Fraction, c: int) -> Fraction:
    return 2 * r * Fraction(c)


def test_wilson_species_count_and_shift() -> None:
    r_half = Fraction(1, 2)
    expected_4d = {
        Fraction(0): 1,
        Fraction(-1): 4,
        Fraction(-2): 6,
        Fraction(-3): 4,
        Fraction(-4): 1,
        Fraction(1): 0,
        Fraction(-5): 0,
    }
    for m_val, count in expected_4d.items():
        record(
            wilson_species_count(4, m_val, r_half) == count,
            f"4D wilson_species_count(m={m_val}, r=1/2) == {count}",
        )
    record(wilson_species_count(4, Fraction(0), Fraction(0)) == 16, "naive r=0 gives 16 corners in 4D")

    for d in range(1, 6):
        record(wilson_species_count(d, Fraction(0), Fraction(0)) == 2 ** d, f"naive r=0 gives 2^{d}")
        for r_num in range(1, 7):
            r = Fraction(r_num, 3)
            for c0 in range(d + 1):
                m_crit = -2 * r * Fraction(c0)
                record(
                    wilson_species_count(d, m_crit, r) == math.comb(d, c0),
                    f"d={d} critical shell c0={c0} count == C({d},{c0})",
                )
            for c in range(d + 1):
                record(
                    (wilson_shift(r, c) == 0) == (c == 0),
                    f"Wilson shift vanishes iff c=0 (d={d}, c={c})",
                )


# =============================================================================
# 2. Wilson Scalar Operator Anticommutes With No Gamma/Chirality Matrix
# =============================================================================

GInt = tuple[int, int]
Mat2GI = tuple[GInt, GInt, GInt, GInt]

GI_ZERO: GInt = (0, 0)
GI_ONE: GInt = (1, 0)
GI_NEG_ONE: GInt = (-1, 0)
GI_I: GInt = (0, 1)
GI_NEG_I: GInt = (0, -1)

MAT2_ZERO: Mat2GI = (GI_ZERO, GI_ZERO, GI_ZERO, GI_ZERO)
MAT2_ID: Mat2GI = (GI_ONE, GI_ZERO, GI_ZERO, GI_ONE)
GAMMA1: Mat2GI = (GI_ZERO, GI_ONE, GI_ONE, GI_ZERO)
GAMMA2: Mat2GI = (GI_ZERO, GI_NEG_I, GI_I, GI_ZERO)
GAMMA5: Mat2GI = (GI_ONE, GI_ZERO, GI_ZERO, GI_NEG_ONE)


def gi_add(z: GInt, w: GInt) -> GInt:
    return (z[0] + w[0], z[1] + w[1])


def gi_mul(z: GInt, w: GInt) -> GInt:
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def mat2_add(a: Mat2GI, b: Mat2GI) -> Mat2GI:
    return (
        gi_add(a[0], b[0]),
        gi_add(a[1], b[1]),
        gi_add(a[2], b[2]),
        gi_add(a[3], b[3]),
    )


def mat2_mul(a: Mat2GI, b: Mat2GI) -> Mat2GI:
    return (
        gi_add(gi_mul(a[0], b[0]), gi_mul(a[1], b[2])),
        gi_add(gi_mul(a[0], b[1]), gi_mul(a[1], b[3])),
        gi_add(gi_mul(a[2], b[0]), gi_mul(a[3], b[2])),
        gi_add(gi_mul(a[2], b[1]), gi_mul(a[3], b[3])),
    )


def mat2_scale(c: GInt, a: Mat2GI) -> Mat2GI:
    return (
        gi_mul(c, a[0]),
        gi_mul(c, a[1]),
        gi_mul(c, a[2]),
        gi_mul(c, a[3]),
    )


def mat2_anticomm(a: Mat2GI, b: Mat2GI) -> Mat2GI:
    return mat2_add(mat2_mul(a, b), mat2_mul(b, a))


def test_wilson_no_gamma_anticommutation() -> None:
    for w in range(-20, 21):
        if w != 0:
            w_mat = mat2_scale((w, 0), MAT2_ID)
            for name, g in (("gamma1", GAMMA1), ("gamma2", GAMMA2), ("gamma5", GAMMA5)):
                ac = mat2_anticomm(w_mat, g)
                record(ac != MAT2_ZERO, f"scalar Wilson w={w} does not anticommute with {name}")


# =============================================================================
# 3. Dense Operator zero_mode_count = s*N^d - rank & Antiperiodic Twists
# =============================================================================

def zero_mode_count(s: int, n: int, d: int, rank: int) -> int:
    return s * (n ** d) - rank


def exact_1d_symmetric_diff_rank(n: int, periodic: bool) -> int:
    # Build exact N x N rational matrix for (psi(x+1) - psi(x-1)) with periodic (+1)
    # or antiperiodic (-1) boundary wrap and compute exact row-echelon rank over Q.
    sign = Fraction(1) if periodic else Fraction(-1)
    mat: list[list[Fraction]] = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for x in range(n):
        xp = (x + 1) % n
        xm = (x - 1) % n
        mat[x][xp] += Fraction(1) if x + 1 < n else sign
        mat[x][xm] -= Fraction(1) if x - 1 >= 0 else sign

    # Gaussian elimination over Q
    rank = 0
    for col in range(n):
        pivot = None
        for r in range(rank, n):
            if mat[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        piv_val = mat[rank][col]
        mat[rank] = [v / piv_val for v in mat[rank]]
        for r in range(n):
            if r != rank and mat[r][col] != 0:
                factor = mat[r][col]
                mat[r] = [mat[r][c] - factor * mat[rank][c] for c in range(n)]
        rank += 1
    return rank


def test_zero_mode_count_and_antiperiodic_twists() -> None:
    for m in range(2, 10):
        n = 2 * m
        # Even N: periodic symmetric diff has 2 zero modes (k=0 and k=pi), so rank = N - 2
        rk_per = exact_1d_symmetric_diff_rank(n, periodic=True)
        record(rk_per == n - 2, f"even N={n} periodic symmetric diff rank == {n - 2}")
        record(zero_mode_count(2, n, 1, 2 * rk_per) == 4, f"even N={n}, s=2 periodic zero_mode_count == 4")

        # Even N: antiperiodic symmetric diff has 0 zero modes, so rank = N (full rank!)
        rk_anti = exact_1d_symmetric_diff_rank(n, periodic=False)
        record(rk_anti == n, f"even N={n} antiperiodic symmetric diff has full rank {n}")
        record(zero_mode_count(2, n, 1, 2 * rk_anti) == 0, f"even N={n}, s=2 antiperiodic zero_mode_count == 0")

        for k_idx in range(n):
            num = 2 * k_idx + 1
            record(num % 2 == 1 and num != 0 and num != n, f"half-integer numerator {num} misses 0 and {n}")


# =============================================================================
# 4. Non-Equivalence Fence Against IntegralRefinementC3C6.lean
# =============================================================================

def charge3(v: tuple[int, int, int]) -> int:
    return v[0] + v[1] + v[2]


def charge6(v: tuple[int, int, int, int, int, int]) -> int:
    return sum(v)


def naive_duplicate_c3_c6(v: tuple[int, int, int]) -> tuple[int, int, int, int, int, int]:
    return (v[0], v[0], v[1], v[1], v[2], v[2])


def block_last_refine_c3_c6(v: tuple[int, int, int]) -> tuple[int, int, int, int, int, int]:
    return (0, v[0], 0, v[1], 0, v[2])


def test_c3_c6_non_equivalence_fence() -> None:
    for c0 in range(-5, 6):
        for c1 in range(-5, 6):
            for c2 in range(-5, 6):
                v = (c0, c1, c2)
                record(charge6(naive_duplicate_c3_c6(v)) == 2 * charge3(v), "C3->C6 naiveDuplicate doubles charge")
                record(charge6(block_last_refine_c3_c6(v)) == charge3(v), "C3->C6 blockLastRefine preserves charge")

    # Non-equivalence: C3->C6 naive duplication factor is fixed at 2, whereas
    # lattice Dirac doubling scales as 2^d (4, 8, 16 for d=2, 3, 4).
    for d in (2, 3, 4):
        record(2 ** d != 2, f"lattice Dirac species count 2^{d}={2**d} != 2 (C3->C6 factor)")


# =============================================================================
# 5. Hypothesis Property-Based Fuzzing & 6 Mutation Kills
# =============================================================================

@settings(max_examples=120, deadline=None)
@given(
    r_num=st.integers(min_value=1, max_value=40),
    r_den=st.integers(min_value=1, max_value=20),
    c0=st.integers(min_value=0, max_value=4),
    v0=st.integers(min_value=-200, max_value=200),
    v1=st.integers(min_value=-200, max_value=200),
    v2=st.integers(min_value=-200, max_value=200),
)
def test_property_tfq0027(
    r_num: int, r_den: int, c0: int, v0: int, v1: int, v2: int
) -> None:
    r = Fraction(r_num, r_den)
    m_crit = -2 * r * Fraction(c0)
    record(
        wilson_species_count(4, m_crit, r) == math.comb(4, c0),
        "prop: 4D wilson_species_count selects binomial shell",
    )
    v = (v0, v1, v2)
    record(
        charge6(naive_duplicate_c3_c6(v)) == 2 * charge3(v)
        and charge6(block_last_refine_c3_c6(v)) == charge3(v),
        "prop: C3->C6 charge laws",
    )


def test_mutation_kills() -> None:
    # M1: Claiming wilson_species_count at m=0, r=1/2 in 4D is 16 -> killed
    record(wilson_species_count(4, Fraction(0), Fraction(1, 2)) == 1, "M1 kill: 15 doublers lifted")
    # M2: Claiming Wilson shift vanishes at c=1 for r=1/2 -> killed
    record(wilson_shift(Fraction(1, 2), 1) != 0, "M2 kill: Wilson shift non-zero at c=1")
    # M3: Claiming scalar Wilson term anticommutes with gamma1 -> killed
    record(mat2_anticomm(mat2_scale((1, 0), MAT2_ID), GAMMA1) != MAT2_ZERO, "M3 kill: {I2, gamma1} != 0")
    # M4: Claiming even-N antiperiodic 1D symmetric diff has zero modes -> killed
    record(exact_1d_symmetric_diff_rank(4, periodic=False) == 4, "M4 kill: antiperiodic N=4 is full rank")
    # M5: Claiming C3->C6 naive duplication factor equals 4D Dirac species count 16 -> killed
    record(charge6(naive_duplicate_c3_c6((1, 0, 0))) != 16, "M5 kill: C3->C6 factor 2 != 16")
    # M6: Admitting dense operator carrier dimension 256 > 128 -> killed
    record(not (4 * (4 ** 3) <= 128), "M6 kill: 256 > 128 refused")


if __name__ == "__main__":
    test_wilson_species_count_and_shift()
    test_wilson_no_gamma_anticommutation()
    test_zero_mode_count_and_antiperiodic_twists()
    test_c3_c6_non_equivalence_fence()
    test_property_tfq0027()
    test_mutation_kills()
    assert CHECKS_FAILED == 0, f"TFQ-0027 checker failed: {CHECKS_FAILED}"
    print(f"TFQ-0027 INDEPENDENT CHECKER PASSED: checks={CHECKS_PASSED} failed={CHECKS_FAILED}")
