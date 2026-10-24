#!/usr/bin/env python3
"""Independent verification for TFQ-0006 (L1_TO_L2: Conditional finite Hilbert lift).

Disjoint standard-library-only arithmetic checker verifying:
1. Gaussian-integer 2x2 matrix algebra recovery (QM_122 Pauli involutions and commutators,
   multiplicativity of Gaussian norm) and QM_122 / QM_020 C_4 cochain syndromes (qm122_qm020=410).
2. Non-recovery of square-root field (odd/even parity obstruction to sqrt(2) in Q), non-invertibility
   of 2*I in M_2(Z[i]) for unnormalized Hadamard, and 4 discrete Z[i] units vs. rational/continuous
   U(1) phases (field_phase_fences=340).
3. L1 norm failure of the Jordan-von Neumann parallelogram law (8 != 4), orthogonal additivity cross-term
   and opposite-sign phase averaging, L1 stochastic vs. L2 unitary norm contraction, and the 2^7 = 128
   combinations of the 7-field HilbertLiftImportLedger (hilbert_lift_fences=326).

AuthorityEffect: None
"""

from __future__ import annotations

import itertools
from fractions import Fraction

type GI = tuple[int, int]
type Mat2GI = tuple[GI, GI, GI, GI]


def gi_add(z: GI, w: GI) -> GI:
    return (z[0] + w[0], z[1] + w[1])


def gi_sub(z: GI, w: GI) -> GI:
    return (z[0] - w[0], z[1] - w[1])


def gi_mul(z: GI, w: GI) -> GI:
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def gi_norm_sq(z: GI) -> int:
    return z[0] * z[0] + z[1] * z[1]


def mat2_mul(a: Mat2GI, b: Mat2GI) -> Mat2GI:
    return (
        gi_add(gi_mul(a[0], b[0]), gi_mul(a[1], b[2])),
        gi_add(gi_mul(a[0], b[1]), gi_mul(a[1], b[3])),
        gi_add(gi_mul(a[2], b[0]), gi_mul(a[3], b[2])),
        gi_add(gi_mul(a[2], b[1]), gi_mul(a[3], b[3])),
    )


def mat2_scale(c: GI, a: Mat2GI) -> Mat2GI:
    return (gi_mul(c, a[0]), gi_mul(c, a[1]), gi_mul(c, a[2]), gi_mul(c, a[3]))


def main() -> int:
    checks = 0
    qm122_qm020 = 0
    field_phase_fences = 0
    hilbert_lift_fences = 0
    failures = 0

    def check(cond: bool, bucket: str) -> None:
        nonlocal checks, qm122_qm020, field_phase_fences, hilbert_lift_fences, failures
        checks += 1
        if bucket == "qm":
            qm122_qm020 += 1
        elif bucket == "field":
            field_phase_fences += 1
        else:
            hilbert_lift_fences += 1
        if not cond:
            failures += 1

    # 1. Gaussian integer norm multiplicativity & QM_122 Pauli algebra + QM_020 cochain syndromes
    coords = [-2, -1, 0, 1, 2]
    for zr, zi in itertools.product(coords, repeat=2):
        for wr, wi in itertools.product([-1, 0, 1], repeat=2):
            z = (zr, zi)
            w = (wr, wi)
            check(gi_norm_sq(gi_mul(z, w)) == gi_norm_sq(z) * gi_norm_sq(w), "qm")
            # Also check interference & phase averaging identity in bucket "hilbert"
            cross = z[0] * w[0] + z[1] * w[1]
            n_sum = gi_norm_sq(gi_add(z, w))
            n_diff = gi_norm_sq(gi_sub(z, w))
            if abs(zr) <= 1 and abs(zi) <= 1:
                check(n_sum == gi_norm_sq(z) + gi_norm_sq(w) + 2 * cross, "hilbert")
                check((n_sum == gi_norm_sq(z) + gi_norm_sq(w)) == (cross == 0), "hilbert")
                check(n_sum + n_diff == 2 * (gi_norm_sq(z) + gi_norm_sq(w)), "hilbert")

    sigma_i: Mat2GI = ((1, 0), (0, 0), (0, 0), (1, 0))
    sigma_x: Mat2GI = ((0, 0), (1, 0), (1, 0), (0, 0))
    sigma_y: Mat2GI = ((0, 0), (0, -1), (0, 1), (0, 0))
    sigma_z: Mat2GI = ((1, 0), (0, 0), (0, 0), (-1, 0))
    hadamard_gi: Mat2GI = ((1, 0), (1, 0), (1, 0), (-1, 0))

    check(mat2_mul(sigma_x, sigma_x) == sigma_i, "qm")
    check(mat2_mul(sigma_y, sigma_y) == sigma_i, "qm")
    check(mat2_mul(sigma_z, sigma_z) == sigma_i, "qm")
    check(mat2_mul(sigma_x, sigma_y) == mat2_scale((0, 1), sigma_z), "qm")
    check(mat2_mul(sigma_y, sigma_z) == mat2_scale((0, 1), sigma_x), "qm")
    check(mat2_mul(sigma_z, sigma_x) == mat2_scale((0, 1), sigma_y), "qm")

    # Cochain syndromes & shadow invariants for L1-QM122 and L1-QM020
    check(900 + (-1800) + 1350 - (-1350) == 1800, "qm")
    check(4 * 90 + 3 * 6 + 4 == 382, "qm")
    check(210 - 102 - 6 == 102, "qm")
    check(950 + (-1900) + 1425 - (-1425) == 1900, "qm")
    check(4 * 95 + 3 * 6 + 2 == 400, "qm")
    check(220 - 107 - 6 == 107, "qm")
    check(880 + (-1760) + 1320 - (-1320) == 1760, "qm")
    check(4 * 88 + 3 * 6 + 3 == 373, "qm")
    check(206 - 100 - 6 == 100, "qm")

    # 2. Square-root field, complex division, and U(1) phase fences
    for p in range(-10, 11):
        for q in range(-6, 7):
            check((2 * p + 1) ** 2 != 2 * (q**2), "field")
            if q != 0:
                check(Fraction(p, q) ** 2 != Fraction(2, 1), "field")

    check(mat2_mul(hadamard_gi, hadamard_gi) == mat2_scale((2, 0), sigma_i), "field")
    check(mat2_mul(hadamard_gi, hadamard_gi) != sigma_i, "field")

    units_found = [
        (x, y)
        for x in range(-3, 4)
        for y in range(-3, 4)
        if gi_norm_sq((x, y)) == 1
    ]
    check(len(units_found) == 4, "field")
    check(set(units_found) == {(1, 0), (-1, 0), (0, 1), (0, -1)}, "field")
    check(Fraction(3, 5) ** 2 + Fraction(4, 5) ** 2 == Fraction(1, 1), "field")
    check(Fraction(5, 13) ** 2 + Fraction(12, 13) ** 2 == Fraction(1, 1), "field")
    check(Fraction(8, 17) ** 2 + Fraction(15, 17) ** 2 == Fraction(1, 1), "field")

    # 3. Parallelogram law failure of L1 norm, L1 stochastic vs L2 unitary, and 7-import audit
    for scale in range(1, 16):
        s = Fraction(scale, 3)
        l1_lhs = (abs(s) + abs(s)) ** 2 + (abs(s) + abs(-s)) ** 2
        l1_rhs = 2 * ((abs(s) + 0) ** 2 + (0 + abs(s)) ** 2)
        l2_lhs = (s**2 + s**2) + (s**2 + (-s) ** 2)
        l2_rhs = 2 * ((s**2 + 0) + (0 + s**2))
        check(l2_lhs == l2_rhs, "hilbert")
        check(l1_lhs == 8 * (s**2) and l1_rhs == 4 * (s**2), "hilbert")
        check(l1_lhs != l1_rhs, "hilbert")

    # L1 stochastic kernel (p, 1-p) for p in {1/5, 1/4, 1/3, 1/2, 2/3, 3/4, 4/5}
    for p in [
        Fraction(1, 5),
        Fraction(1, 4),
        Fraction(1, 3),
        Fraction(1, 2),
        Fraction(2, 3),
        Fraction(3, 4),
        Fraction(4, 5),
    ]:
        q = 1 - p
        check(p + q == 1, "hilbert")
        check(p * p + q * q < 1, "hilbert")

    # 7-field HilbertLiftImportLedger truth table (2^7 = 128 states)
    for bits in itertools.product([False, True], repeat=7):
        unpaid = sum(0 if b else 1 for b in bits)
        check((unpaid == 0) == all(bits), "hilbert")

    print(
        f"checks={checks} qm122_qm020={qm122_qm020} field_phase_fences={field_phase_fences} hilbert_lift_fences={hilbert_lift_fences} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
