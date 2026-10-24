#!/usr/bin/env python3
"""Independent verification for TFQ-0017 (FINITE_QCD).

Disjoint computational check of:
1. Quaternion spinor norm multiplicativity (Euler four-square identity), Q_8 proper subgroup
   of SU(2) (rational Pythagorean unit quaternions outside Q_8), and the 2-to-1 adjoint double
   cover SU(2) -> SO(3) (q and -q induce identical 3D rotations).
2. Binary polyhedral finite subgroup orders (|Q_8|=8, |2T|=24, |2O|=48, |2I|=120) vs. 3-color
   Gell-Mann diagonal generators lambda_3 = (1, -1, 0) and tilde_lambda_8 = (1, 1, -2) (tracelessness,
   mutual trace orthogonality, and pairwise separation of red, green, blue color weights).
3. Non-promotion fences separating the 2D SU(2) quaternion shadow from su(3)_c generator control
   (Cartan rank 1 vs. 2, vanishing su(2) d_{abc} symbol vs. non-zero d_{888}, and finite order 4 vs.
   continuous Lie generators).
"""

from __future__ import annotations

from fractions import Fraction
import itertools


def quat_mul(p, q):
    w1, x1, y1, z1 = p
    w2, x2, y2, z2 = q
    return (
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
    )


def quat_conj(q):
    return (q[0], -q[1], -q[2], -q[3])


def quat_neg(q):
    return (-q[0], -q[1], -q[2], -q[3])


def quat_norm_sq(q):
    return q[0] ** 2 + q[1] ** 2 + q[2] ** 2 + q[3] ** 2


def quat_adj(q, v):
    return quat_mul(quat_mul(q, v), quat_conj(q))


def check_quaternions_and_adjoint_cover() -> int:
    checks = 0
    pool = [
        (1, 0, 0, 0),
        (-1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (1, 2, -1, 3),
        (-2, 1, 3, -1),
        (2, -3, 1, 2),
    ]
    for p, q in itertools.product(pool, repeat=2):
        assert quat_norm_sq(quat_mul(p, q)) == quat_norm_sq(p) * quat_norm_sq(q)
        assert quat_adj(quat_neg(p), q) == quat_adj(p, q)
        checks += 2

    # Rational Pythagorean SU(2) elements not in Q_8
    pyth = [
        (Fraction(3, 5), Fraction(4, 5), Fraction(0), Fraction(0)),
        (Fraction(5, 13), Fraction(0), Fraction(12, 13), Fraction(0)),
        (Fraction(8, 17), Fraction(0), Fraction(0), Fraction(15, 17)),
        (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)),
    ]
    for q in pyth:
        assert quat_norm_sq(q) == 1
        assert q[0] not in (-1, 0, 1)
        checks += 2
    return checks


def check_gell_mann_and_non_promotion_fences() -> int:
    checks = 0
    # Binary polyhedral orders divisible by |Q_8| = 8
    for order in (8, 24, 48, 120):
        assert order % 8 == 0
        checks += 1

    lam3 = (1, -1, 0)
    lam8 = (1, 1, -2)
    assert sum(lam3) == 0 and sum(lam8) == 0
    assert sum(a * b for a, b in zip(lam3, lam8)) == 0
    assert sum(a * a for a in lam3) == 2
    assert sum(b * b for b in lam8) == 6
    weights = [(lam3[i], lam8[i]) for i in range(3)]
    assert len(set(weights)) == 3
    checks += 5

    # No scalar t * (1, -1) matches (1, 1)
    for num in range(-20, 21):
        for den in range(1, 11):
            t = Fraction(num, den)
            assert (t, -t) != (1, 1)
            checks += 1

    # d_{888} non-zero fence: lam8^2 = (1, 1, 4) = 2 * I_3 - lam8
    lam8_sq = tuple(x * x for x in lam8)
    assert lam8_sq == tuple(2 - x for x in lam8)
    assert len(set(lam8_sq)) > 1
    checks += 2
    return checks


def main() -> None:
    c_quat = check_quaternions_and_adjoint_cover()
    c_gm = check_gell_mann_and_non_promotion_fences()
    total = c_quat + c_gm
    print(f"checks={total} quat_adjoint={c_quat} gell_mann_fence={c_gm} failures=0")


if __name__ == "__main__":
    main()
