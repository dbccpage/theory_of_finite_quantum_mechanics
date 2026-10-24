#!/usr/bin/env python3
"""Independent verification for TFQ-0032 (FINITE_QCD):
Exact rational SU(N) / SU(3) quark-antiquark channel Casimir coefficients
(-4/3 singlet and +1/6 octet), 3 x 3 = 1 + 8 dimension and weighted trace
cancellation, explicit 3x3 color-trace singlet and octet projectors, declared
finite meson composite carrier dimension 36 * L^d, and non-equivalence fences
showing that channel Casimir rationals do not supply a spatial orbital
wavefunction or meson mass operator.
"""

from __future__ import annotations

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
# 1. Exact Rational SU(N) / SU(3) Quark-Antiquark Channel Casimirs
# =============================================================================

def sun_fund_casimir(n: int) -> Fraction:
    return Fraction(n * n - 1, 2 * n)


def sun_adj_casimir(n: int) -> Fraction:
    return Fraction(n, 1)


def singlet_channel_factor(n: int) -> Fraction:
    return -sun_fund_casimir(n)


def adjoint_channel_factor(n: int) -> Fraction:
    return (sun_adj_casimir(n) - 2 * sun_fund_casimir(n)) / 2


def test_sun_qqbar_casimir_channels() -> None:
    record(sun_fund_casimir(3) == Fraction(4, 3), "SU(3) fundamental Casimir == 4/3")
    record(sun_adj_casimir(3) == Fraction(3, 1), "SU(3) adjoint Casimir == 3")
    record(singlet_channel_factor(3) == Fraction(-4, 3), "SU(3) singlet channel factor == -4/3")
    record(adjoint_channel_factor(3) == Fraction(1, 6), "SU(3) octet channel factor == +1/6")
    record(
        1 * singlet_channel_factor(3) + 8 * adjoint_channel_factor(3) == 0,
        "SU(3) weighted trace sum 1*(-4/3) + 8*(1/6) == 0",
    )
    record(
        singlet_channel_factor(3) / adjoint_channel_factor(3) == -8,
        "SU(3) singlet/octet ratio == -8",
    )

    for n in range(2, 15):
        c1 = singlet_channel_factor(n)
        ca = adjoint_channel_factor(n)
        record(c1 < 0, f"SU({n}) singlet channel attractive (< 0)")
        record(ca == Fraction(1, 2 * n) > 0, f"SU({n}) adjoint channel repulsive (+1/(2N) > 0)")
        record(1 + (n * n - 1) == n * n, f"SU({n}) dimension decomposition 1 + (N^2-1) == N^2")
        record(1 * c1 + (n * n - 1) * ca == 0, f"SU({n}) weighted channel trace == 0")

    record(singlet_channel_factor(2) == Fraction(-3, 4), "SU(2) singlet factor == -3/4")
    record(adjoint_channel_factor(2) == Fraction(1, 4), "SU(2) triplet factor == +1/4")
    record(singlet_channel_factor(2) != singlet_channel_factor(3), "SU(2) != SU(3) singlet factor")


# =============================================================================
# 2. Explicit 3x3 Color Contraction Projectors (singletProj & octetProj)
# =============================================================================

Mat3Q = tuple[
    tuple[Fraction, Fraction, Fraction],
    tuple[Fraction, Fraction, Fraction],
    tuple[Fraction, Fraction, Fraction],
]


def color_trace(m: Mat3Q) -> Fraction:
    return m[0][0] + m[1][1] + m[2][2]


def singlet_proj(m: Mat3Q) -> Mat3Q:
    tr3 = color_trace(m) / 3
    z = Fraction(0)
    return (
        (tr3, z, z),
        (z, tr3, z),
        (z, z, tr3),
    )


def octet_proj(m: Mat3Q) -> Mat3Q:
    s = singlet_proj(m)
    return tuple(
        tuple(m[i][j] - s[i][j] for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


def mat3_add(a: Mat3Q, b: Mat3Q) -> Mat3Q:
    return tuple(
        tuple(a[i][j] + b[i][j] for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


def frobenius_inner(a: Mat3Q, b: Mat3Q) -> Fraction:
    return sum(a[i][j] * b[i][j] for i in range(3) for j in range(3))


def test_color_projectors() -> None:
    zero3: Mat3Q = (
        (Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0)),
    )
    for a in range(-3, 4):
        for b in range(-3, 4):
            for c in range(-3, 4):
                m: Mat3Q = (
                    (Fraction(a), Fraction(a + b, 2), Fraction(c)),
                    (Fraction(b), Fraction(b - c), Fraction(a - c, 3)),
                    (Fraction(-c), Fraction(a), Fraction(c + 1)),
                )
                p1 = singlet_proj(m)
                p8 = octet_proj(m)
                record(color_trace(p1) == color_trace(m), "Tr(P_1(M)) == Tr(M)")
                record(color_trace(p8) == 0, "Tr(P_8(M)) == 0")
                record(mat3_add(p1, p8) == m, "P_1(M) + P_8(M) == M")
                record(singlet_proj(p1) == p1, "P_1(P_1(M)) == P_1(M)")
                record(octet_proj(p8) == p8, "P_8(P_8(M)) == P_8(M)")
                record(singlet_proj(p8) == zero3, "P_1(P_8(M)) == 0")
                record(octet_proj(p1) == zero3, "P_8(P_1(M)) == 0")
                record(frobenius_inner(p1, p8) == 0, "<P_1(M), P_8(M)>_F == 0")


# =============================================================================
# 3. Declared Finite Meson Carrier & Non-Equivalence Fences
# =============================================================================

def meson_carrier_dim(n_c: int, n_s: int, length: int, dim: int) -> int:
    return (n_c * n_c) * (n_s * n_s) * (length ** dim)


def meson_radial_ham_det(m0: Fraction, v0: Fraction, v1: Fraction, t: Fraction) -> Fraction:
    return (2 * m0 + v0) * (2 * m0 + v1) - t * t


def hyperfine_meson_mass(m0: Fraction, delta_ss: Fraction, s_dot_s: Fraction) -> Fraction:
    return m0 + delta_ss * s_dot_s


def test_meson_carrier_and_fences() -> None:
    for length in range(1, 7):
        for dim in range(1, 5):
            total = meson_carrier_dim(3, 2, length, dim)
            record(total == 36 * (length ** dim), f"meson_carrier_dim(3,2,{length},{dim}) == 36*L^d")
            singlet_ps = 1 * 1 * (length ** dim)
            singlet_vec = 1 * 3 * (length ** dim)
            octet_all = 8 * 4 * (length ** dim)
            record(singlet_ps + singlet_vec + octet_all == total, "sector decomposition sums to 36*L^d")

    for t_num in range(1, 15):
        t = Fraction(t_num, 5)
        det_t = meson_radial_ham_det(Fraction(3, 2), Fraction(-4, 3), Fraction(-2, 3), t)
        det_0 = meson_radial_ham_det(Fraction(3, 2), Fraction(-4, 3), Fraction(-2, 3), Fraction(0))
        record(det_t != det_0, f"spatial hopping t={t} changes mass operator det")

    for d_num in range(1, 15):
        dss = Fraction(d_num, 7)
        m_ps = hyperfine_meson_mass(Fraction(2), dss, Fraction(-3, 4))
        m_vec = hyperfine_meson_mass(Fraction(2), dss, Fraction(1, 4))
        record(m_vec - m_ps == dss and m_ps < m_vec, "vector-pseudoscalar hyperfine splitting == delta_SS")


# =============================================================================
# 4. Hypothesis Property-Based Fuzzing & 6 Mutation Kills
# =============================================================================

@settings(max_examples=120, deadline=None)
@given(
    n=st.integers(min_value=2, max_value=30),
    m00=st.integers(min_value=-50, max_value=50),
    m11=st.integers(min_value=-50, max_value=50),
    m22=st.integers(min_value=-50, max_value=50),
    t_num=st.integers(min_value=1, max_value=40),
)
def test_property_tfq0032(n: int, m00: int, m11: int, m22: int, t_num: int) -> None:
    record(
        1 * singlet_channel_factor(n) + (n * n - 1) * adjoint_channel_factor(n) == 0,
        "prop: SU(N) weighted qqbar Casimir sum == 0",
    )
    m: Mat3Q = (
        (Fraction(m00), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(m11), Fraction(-1)),
        (Fraction(2), Fraction(0), Fraction(m22)),
    )
    record(color_trace(octet_proj(m)) == 0, "prop: octet projection traceless")
    t = Fraction(t_num, 3)
    record(
        meson_radial_ham_det(Fraction(1), Fraction(0), Fraction(0), t)
        != meson_radial_ham_det(Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        "prop: non-zero hopping changes radial mass det",
    )


def test_mutation_kills() -> None:
    # M1: Claiming SU(3) octet channel factor is attractive (< 0) -> killed
    record(adjoint_channel_factor(3) > 0, "M1 kill: octet channel is repulsive (+1/6 > 0)")
    # M2: Claiming unweighted sum -4/3 + 1/6 == 0 -> killed
    record(singlet_channel_factor(3) + adjoint_channel_factor(3) != 0, "M2 kill: needs 1 and 8 weights")
    # M3: Claiming octet projection has non-zero color trace -> killed
    sample_m: Mat3Q = (
        (Fraction(3), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(6), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(9)),
    )
    record(color_trace(octet_proj(sample_m)) == 0, "M3 kill: Tr(P_8(M)) == 0")
    # M4: Claiming SU(2) singlet factor equals SU(3) singlet factor -4/3 -> killed
    record(singlet_channel_factor(2) != Fraction(-4, 3), "M4 kill: SU(2) is -3/4 != -4/3")
    # M5: Claiming channel Casimirs distinguish L=2 vs L=3 spatial carriers -> killed
    record(meson_carrier_dim(3, 2, 2, 3) != meson_carrier_dim(3, 2, 3, 3), "M5 kill: 288 != 972")
    # M6: Claiming delta_SS=0 splits pseudoscalar and vector meson masses -> killed
    record(
        hyperfine_meson_mass(Fraction(1), Fraction(0), Fraction(-3, 4))
        == hyperfine_meson_mass(Fraction(1), Fraction(0), Fraction(1, 4)),
        "M6 kill: degenerate without spin-spin operator",
    )


if __name__ == "__main__":
    test_sun_qqbar_casimir_channels()
    test_color_projectors()
    test_meson_carrier_and_fences()
    test_property_tfq0032()
    test_mutation_kills()
    assert CHECKS_FAILED == 0, f"TFQ-0032 checker failed: {CHECKS_FAILED}"
    print(f"TFQ-0032 INDEPENDENT CHECKER PASSED: checks={CHECKS_PASSED} failed={CHECKS_FAILED}")
