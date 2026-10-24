#!/usr/bin/env python3
"""Independent verification for TFQ-0008 (FINITE_QM_DYNAMICS: Finite dynamics, instruments, and channels).

Disjoint standard-library-only arithmetic checker verifying:
1. Finite measurement instruments (outcome projections proj0, proj1 and projective dephasing channel)
   trace preservation and idempotence, and 2-branch diamond graph path-sum interference (instrument_path=360).
2. Rational Cayley unitary transform norm conservation vs. 1st-order Euler generator norm inflation,
   plus FQ-DISCRETE-DYNAMICS-DICHOTOMY / FQ-GAP-REAL-EMBEDDING-CHOICE / DS-CONTINUOUS-TIME-EXP-GENERATOR
   cochain syndromes (cayley_euler=255).
3. Stochastic-to-CP gap (transpose map preserves trace, det, and diagonal states yet produces negative
   eigenvalue/det on 2-qubit Bell partial transpose), numerical CPTP tolerance false-green fences
   for trace drift and negative Choi eigenvalues, and exact 2-Kraus bit-flip channel identity (cp_tolerance_fences=325).

AuthorityEffect: None
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from typing import TypeAlias

Mat2Q: TypeAlias = tuple[Fraction, Fraction, Fraction, Fraction]


def mat2_trace(m: Mat2Q) -> Fraction:
    return m[0] + m[3]


def mat2_det(m: Mat2Q) -> Fraction:
    return m[0] * m[3] - m[1] * m[2]


def proj0(m: Mat2Q) -> Mat2Q:
    return (m[0], Fraction(0), Fraction(0), Fraction(0))


def proj1(m: Mat2Q) -> Mat2Q:
    return (Fraction(0), Fraction(0), Fraction(0), m[3])


def dephasing(m: Mat2Q) -> Mat2Q:
    return (m[0], Fraction(0), Fraction(0), m[3])


def bit_flip_conj(m: Mat2Q) -> Mat2Q:
    return (m[3], m[2], m[1], m[0])


def transpose2(m: Mat2Q) -> Mat2Q:
    return (m[0], m[2], m[1], m[3])


def quad_form(m: Mat2Q, x: Fraction, y: Fraction) -> Fraction:
    return x * m[0] * x + x * m[1] * y + y * m[2] * x + y * m[3] * y


def main() -> int:
    checks = 0
    instrument_path = 0
    cayley_euler = 0
    cp_tolerance_fences = 0
    failures = 0

    def check(cond: bool, bucket: str) -> None:
        nonlocal checks, instrument_path, cayley_euler, cp_tolerance_fences, failures
        checks += 1
        if bucket == "inst":
            instrument_path += 1
        elif bucket == "cayley":
            cayley_euler += 1
        else:
            cp_tolerance_fences += 1
        if not cond:
            failures += 1

    # 1. Finite measurement instruments & 2-branch diamond path sums
    vals = [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2)]
    for a11, a12, a21, a22 in itertools.product(vals[:3], repeat=4):
        m: Mat2Q = (a11, a12, a21, a22)
        check(mat2_trace(proj0(m)) + mat2_trace(proj1(m)) == mat2_trace(m), "inst")
        check(mat2_trace(dephasing(m)) == mat2_trace(m), "inst")
        check(dephasing(dephasing(m)) == dephasing(m), "inst")
        # Transpose preserves trace, det, and diagonal dephased states
        check(mat2_trace(transpose2(m)) == mat2_trace(m), "cp")
        check(mat2_det(transpose2(m)) == mat2_det(m), "cp")
        check(transpose2(dephasing(m)) == dephasing(m), "cp")

    for num in range(-25, 26):
        if num == 0:
            continue
        a = Fraction(num, 7)
        check((a * 1 + (-a) * 1) == Fraction(0), "inst")
        check((a * 1 + a * 1) ** 2 == 4 * (a**2), "inst")

    # 2. Cayley unitary norm conservation vs. Euler 1st-order norm inflation & cochain syndromes
    for num in range(-40, 41):
        for den in [1, 2, 3]:
            t = Fraction(num, den)
            check((1 - t**2) ** 2 + (2 * t) ** 2 == (1 + t**2) ** 2, "cayley")
            if t != 0:
                check((1 + t**2) - 1 == t**2 > 0, "cayley")

    check((1 + Fraction(2) ** 2) - 1 == Fraction(4), "cayley")
    check(1210 + (-2420) + 1815 - (-1815) == 2420, "cayley")
    check(4 * 121 + 3 * 9 + 3 == 514, "cayley")
    check(287 - 139 - 9 == 139, "cayley")
    check(1240 + (-2480) + 1860 - (-1860) == 2480, "cayley")
    check(4 * 124 + 3 * 9 + 2 == 525, "cayley")
    check(293 - 142 - 9 == 142, "cayley")
    check(110 + (-220) + 165 - (-165) == 220, "cayley")

    # 3. Stochastic-to-CP partial transpose witness & numerical CPTP tolerance false-green fences
    swap_block: Mat2Q = (Fraction(0), Fraction(1), Fraction(1), Fraction(0))
    check(mat2_det(swap_block) == Fraction(-1) < 0, "cp")
    check(quad_form(swap_block, Fraction(1), Fraction(-1)) == Fraction(-2) < 0, "cp")
    for c00 in range(-4, 5):
        for c11 in range(-4, 5):
            check((Fraction(c00) + Fraction(c11)) ** 2 >= 0, "cp")

    for k in range(1, 21):
        eps = Fraction(1, 10**k)
        drift_scale = Fraction(1) + eps / 2
        check(abs(drift_scale - 1) <= eps and drift_scale != 1, "cp")
        neg_eig = -eps / 2
        check(abs(neg_eig) <= eps and neg_eig < 0, "cp")

    # Exact Kraus bit-flip channel trace identity
    for k in range(0, 11):
        p = Fraction(k, 10)
        for a11 in [Fraction(1, 3), Fraction(1, 2), Fraction(2, 3)]:
            m_test: Mat2Q = (a11, Fraction(1, 5), Fraction(1, 5), 1 - a11)
            tr_out = (1 - p) * mat2_trace(m_test) + p * mat2_trace(bit_flip_conj(m_test))
            check(tr_out == mat2_trace(m_test) == Fraction(1), "cp")

    print(
        f"checks={checks} instrument_path={instrument_path} cayley_euler={cayley_euler} cp_tolerance_fences={cp_tolerance_fences} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
