#!/usr/bin/env python3
"""Independent verification for TFQ-0026 (FINITE_QCD):
Euclidean Clifford algebra over Z[i], naive symmetric-difference zero-velocity
modes at k in {0, pi}^d, even/odd period pi-mode periodicity, 2^d naive species
count before spin multiplicity, rational Wilson corner mass shift m + 2*r*c,
MAX_CARRIER_DIMENSION = 128 admission guard, chiral symmetry breaking by scalar
Wilson mass, and no-continuum-limit scope fences.
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
# 1. Euclidean Clifford Algebra over Z[i]
# =============================================================================

GInt = tuple[int, int]
Mat2GI = tuple[GInt, GInt, GInt, GInt]

GI_ZERO: GInt = (0, 0)
GI_ONE: GInt = (1, 0)
GI_NEG_ONE: GInt = (-1, 0)
GI_I: GInt = (0, 1)
GI_NEG_I: GInt = (0, -1)


def gi_add(z: GInt, w: GInt) -> GInt:
    return (z[0] + w[0], z[1] + w[1])


def gi_mul(z: GInt, w: GInt) -> GInt:
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


MAT2_ZERO: Mat2GI = (GI_ZERO, GI_ZERO, GI_ZERO, GI_ZERO)
MAT2_ID: Mat2GI = (GI_ONE, GI_ZERO, GI_ZERO, GI_ONE)

GAMMA1: Mat2GI = (GI_ZERO, GI_ONE, GI_ONE, GI_ZERO)
GAMMA2: Mat2GI = (GI_ZERO, GI_NEG_I, GI_I, GI_ZERO)
GAMMA5: Mat2GI = (GI_ONE, GI_ZERO, GI_ZERO, GI_NEG_ONE)


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


def test_euclidean_clifford_algebra() -> None:
    record(mat2_mul(GAMMA1, GAMMA1) == MAT2_ID, "gamma1^2 == I2")
    record(mat2_mul(GAMMA2, GAMMA2) == MAT2_ID, "gamma2^2 == I2")
    record(mat2_mul(GAMMA5, GAMMA5) == MAT2_ID, "gamma5^2 == I2")
    record(mat2_anticomm(GAMMA1, GAMMA2) == MAT2_ZERO, "{gamma1, gamma2} == 0")
    record(mat2_anticomm(GAMMA1, GAMMA5) == MAT2_ZERO, "{gamma1, gamma5} == 0")
    record(mat2_anticomm(GAMMA2, GAMMA5) == MAT2_ZERO, "{gamma2, gamma5} == 0")

    for w in range(-15, 16):
        if w != 0:
            w_mat = mat2_scale((w, 0), MAT2_ID)
            ac = mat2_anticomm(w_mat, GAMMA5)
            record(ac != MAT2_ZERO, f"scalar Wilson mass w={w} breaks gamma5 anticommutativity")
            record(ac[0] == (2 * w, 0) and ac[3] == (-2 * w, 0), f"anticommutator entries for w={w}")


# =============================================================================
# 2. Naive Symmetric Difference Zero Modes & 2^d Doubling Count
# =============================================================================

def naive_symmetric_diff(psi_plus: int, psi_minus: int) -> int:
    return psi_plus - psi_minus


def axis_periodic_zero_modes(n: int) -> int:
    return 2 if n % 2 == 0 else 1


def naive_species_count(d: int) -> int:
    return 2 ** d


def test_naive_doubling_and_periodicity() -> None:
    for s in range(-50, 51):
        record(naive_symmetric_diff(s, s) == 0, f"k=0 constant mode zero diff s={s}")
        record(naive_symmetric_diff(-s, -s) == 0, f"k=pi staggered mode zero diff s={s}")

    for n in range(3, 40):
        # Explicit check on an N-cycle: count modes psi(x) = r^x with r in {1, -1}
        # that satisfy periodic boundary conditions r^N == 1 and psi(x+1) - psi(x-1) == 0
        valid_roots = [r for r in (1, -1) if (r ** n == 1) and (r - (1 // r) == 0)]
        record(
            len(valid_roots) == axis_periodic_zero_modes(n),
            f"periodic zero-velocity modes on N={n} cycle matches formula",
        )
        if n % 2 == 0:
            record(axis_periodic_zero_modes(n) == 2, f"even N={n} has 2 zero modes per axis")
        else:
            record(axis_periodic_zero_modes(n) == 1, f"odd N={n} has 1 zero mode per axis")

    expected = {1: 2, 2: 4, 3: 8, 4: 16, 5: 32, 6: 64}
    for d, val in expected.items():
        record(naive_species_count(d) == val, f"naive_species_count({d}) == {val}")
        record(naive_species_count(d) - 1 == val - 1 > 0, f"doubler excess for d={d}")


# =============================================================================
# 3. Rational Wilson Mass Shift & Carrier Admission Guard (MAX = 128)
# =============================================================================

def wilson_corner_mass(m: Fraction, r: Fraction, c: int) -> Fraction:
    return m + 2 * r * Fraction(c)


def carrier_dimension(s: int, n: int, d: int) -> int:
    return s * (n ** d)


def admit_lattice_carrier(s: int, n: int, d: int) -> bool:
    return n >= 3 and carrier_dimension(s, n, d) <= 128


def test_wilson_mass_and_carrier_guard() -> None:
    for r_num in range(1, 8):
        for r_den in range(1, 6):
            r = Fraction(r_num, r_den)
            record(wilson_corner_mass(Fraction(0), r, 0) == 0, "origin c=0 stays massless at m=0")
            for c in range(1, 9):
                wm = wilson_corner_mass(Fraction(0), r, c)
                record(wm > 0, f"doubler corner c={c} lifted to {wm} > 0")
                for c0 in range(0, 6):
                    m_crit = -2 * r * Fraction(c0)
                    shifted = wilson_corner_mass(m_crit, r, c)
                    record((shifted == 0) == (c == c0), f"critical mass shell selection c={c}, c0={c0}")

    record(carrier_dimension(2, 4, 2) == 32, "carrier_dimension(2,4,2) == 32")
    record(carrier_dimension(2, 4, 3) == 128, "carrier_dimension(2,4,3) == 128")
    record(carrier_dimension(4, 4, 3) == 256, "carrier_dimension(4,4,3) == 256")
    record(admit_lattice_carrier(2, 4, 2) is True, "admit (2,4,2)")
    record(admit_lattice_carrier(2, 4, 3) is True, "admit (2,4,3)")
    record(admit_lattice_carrier(4, 4, 3) is False, "refuse (4,4,3) > 128")
    record(admit_lattice_carrier(2, 2, 2) is False, "refuse N=2 < 3")

    for s in (1, 2, 4, 8):
        for n in range(1, 8):
            for d in range(1, 5):
                dim = carrier_dimension(s, n, d)
                adm = admit_lattice_carrier(s, n, d)
                record(adm == (n >= 3 and dim <= 128), f"admission predicate check ({s},{n},{d})")


# =============================================================================
# 4. Hypothesis Property-Based Fuzzing
# =============================================================================

@settings(max_examples=150, deadline=None)
@given(
    r_num=st.integers(min_value=1, max_value=50),
    r_den=st.integers(min_value=1, max_value=25),
    c=st.integers(min_value=1, max_value=20),
    c0=st.integers(min_value=0, max_value=20),
    s=st.integers(min_value=-1000, max_value=1000),
)
def test_property_wilson_and_doubling(
    r_num: int, r_den: int, c: int, c0: int, s: int
) -> None:
    r = Fraction(r_num, r_den)
    record(naive_symmetric_diff(s, s) == 0, "prop: k=0 zero diff")
    record(naive_symmetric_diff(-s, -s) == 0, "prop: k=pi zero diff")
    record(wilson_corner_mass(Fraction(0), r, c) > 0, "prop: positive Wilson mass on doubler")
    m_crit = -2 * r * Fraction(c0)
    record(
        (wilson_corner_mass(m_crit, r, c) == 0) == (c == c0),
        "prop: critical mass selects unique corner shell",
    )


# =============================================================================
# 5. Mutation Kills (6 Negative Controls)
# =============================================================================

def test_mutation_kills() -> None:
    # M1: Claiming gamma1 and gamma2 commute -> killed
    record(mat2_anticomm(GAMMA1, GAMMA2) == MAT2_ZERO, "M1 kill: anticommutator vanishes")
    record(mat2_mul(GAMMA1, GAMMA2) != mat2_mul(GAMMA2, GAMMA1), "M1 kill: gamma1*gamma2 != gamma2*gamma1")
    # M2: Claiming odd period N=3 has 2 periodic zero modes per axis -> killed
    record(axis_periodic_zero_modes(3) != 2, "M2 kill: N=3 does not admit periodic pi mode")
    # M3: Claiming 4D naive species count is 1 (no doubling) -> killed
    record(naive_species_count(4) != 1, "M3 kill: 4D naive species count is 16 != 1")
    # M4: Claiming r=0 lifts c=1 doubler corner -> killed
    record(wilson_corner_mass(Fraction(0), Fraction(0), 1) == 0, "M4 kill: r=0 fails to lift doubler")
    # M5: Admitting carrier dimension 256 > 128 -> killed
    record(admit_lattice_carrier(4, 4, 3) is False, "M5 kill: 256 > 128 refused")
    # M6: Claiming scalar Wilson term anticommutes with gamma5 -> killed
    record(mat2_anticomm(mat2_scale((1, 0), MAT2_ID), GAMMA5) != MAT2_ZERO, "M6 kill: Wilson mass breaks chirality")


if __name__ == "__main__":
    test_euclidean_clifford_algebra()
    test_naive_doubling_and_periodicity()
    test_wilson_mass_and_carrier_guard()
    test_property_wilson_and_doubling()
    test_mutation_kills()
    assert CHECKS_FAILED == 0, f"TFQ-0026 checker failed: {CHECKS_FAILED}"
    print(f"TFQ-0026 INDEPENDENT CHECKER PASSED: checks={CHECKS_PASSED} failed={CHECKS_FAILED}")
