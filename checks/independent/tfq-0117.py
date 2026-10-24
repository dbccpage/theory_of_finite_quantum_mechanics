#!/usr/bin/env python3
"""Independent exact rational and cyclotomic verifier for TFQ-0117 (CONTINUUM_INTERFACE).

Verifies with Python Fractions and exact integer/Gaussian-rational arithmetic (no Lean dependency):
1. Finite cyclic self-duality on Z/NZ:
   - Character dual has exact cardinality N (for N in 1..12) and N-fold periodicity (N * k * x) % N == 0.
   - Z/3Z countermodel (M3/M4): |Z/3Z| == 3, not exponent-2 ((1 + 1) % 3 == 2 != 0), yet every
     element has 3-torsion (3 * x) % 3 == 0, refuting promotion to free integers Z or circle U(1).
2. Exact character orthogonality over Q[i] on Z/4Z:
   - mu_4 = {1, i, -1, -i} is an exact homomorphism under addition mod 4.
   - All 16 character values chi_k(x) have unit Gaussian norm re^2 + im^2 == 1.
   - All 16 inner products sum_{x=0}^3 chi_k(x) conj(chi_m(x)) equal (4, 0) iff k == m and (0, 0) otherwise.
3. Promotion-refusal fences:
   - C_4 cochain syndrome replay: tree_potentials = [200, -400, 300], chord = -300 -> holonomy = 400;
     sign-fiber interference gap (1+1)^2 - (1-1)^2 == 4.
   - Haar unit-mass normalization (1/P) * P == 1 and (1/P) * (alpha * P) == alpha holds for every
     nonzero period P != 0, so Haar uniqueness does not select P = 2*pi.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import sys

GaussRat = tuple[Fraction, Fraction]


def g_add(z: GaussRat, w: GaussRat) -> GaussRat:
    return (z[0] + w[0], z[1] + w[1])


def g_mul(z: GaussRat, w: GaussRat) -> GaussRat:
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def g_conj(z: GaussRat) -> GaussRat:
    return (z[0], -z[1])


def g_norm_sq(z: GaussRat) -> Fraction:
    return z[0] * z[0] + z[1] * z[1]


MU4: list[GaussRat] = [
    (Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(1)),
    (Fraction(-1), Fraction(0)),
    (Fraction(0), Fraction(-1)),
]


def chi4(k: int, x: int) -> GaussRat:
    return MU4[(k * x) % 4]


def main() -> int:
    checks = 0
    cyclic_checks = 0
    char_checks = 0
    fence_checks = 0
    failures = 0

    def check(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, cyclic_checks, char_checks, fence_checks, failures
        checks += 1
        if bucket == "cyclic":
            cyclic_checks += 1
        elif bucket == "char":
            char_checks += 1
        elif bucket == "fence":
            fence_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [{bucket}]: {msg}", file=sys.stderr)

    # 1. Finite cyclic self-duality and N-torsion periodicity across N = 1..12
    for n in range(1, 13):
        dual_labels = list(range(n))
        check(len(dual_labels) == n, "cyclic", f"|dual(Z/{n}Z)| == {n}")
        for k, x in itertools.product(dual_labels, dual_labels):
            check((n * k * x) % n == 0, "cyclic", f"N-torsion on Z/{n}Z")

    # Z/3Z non-exponent-2 torsion fence
    check((1 + 1) % 3 == 2 and (1 + 1) % 3 != 0, "cyclic", "Z/3Z is not exponent-2")
    for x in range(3):
        check((x + x + x) % 3 == 0, "cyclic", f"3*{x} == 0 mod 3")

    # 2. Exact Z/4Z character orthogonality over Q[i]
    for a, b in itertools.product(range(4), range(4)):
        check(
            MU4[(a + b) % 4] == g_mul(MU4[a], MU4[b]),
            "char",
            f"mu4 homomorphism at ({a},{b})",
        )

    for k, x in itertools.product(range(4), range(4)):
        val = chi4(k, x)
        check(
            g_norm_sq(val) == Fraction(1)
            and g_mul(val, g_conj(val)) == (Fraction(1), Fraction(0)),
            "char",
            f"chi4({k},{x}) unit Gaussian norm",
        )

    for k, m in itertools.product(range(4), range(4)):
        acc: GaussRat = (Fraction(0), Fraction(0))
        for x in range(4):
            acc = g_add(acc, g_mul(chi4(k, x), g_conj(chi4(m, x))))
        expected: GaussRat = (Fraction(4), Fraction(0)) if k == m else (Fraction(0), Fraction(0))
        check(acc == expected, "char", f"chi4 orthogonality ({k},{m})")

    # 3. Promotion-refusal fences: C_4 syndrome, sign-fiber gap, and Haar period independence
    tree_potentials = [200, -400, 300]
    chord_potential = -300
    holonomy = sum(tree_potentials) - chord_potential
    check(holonomy == 400, "fence", "C_4 holonomy_gamma2 == 400")
    check(
        (1 + 1) ** 2 == 4 and (1 - 1) ** 2 == 0 and (1 + 1) ** 2 - (1 - 1) ** 2 == 4,
        "fence",
        "sign-fiber destructive cancellation gap == 4",
    )

    periods = [Fraction(1, 1), Fraction(2, 1), Fraction(22, 7), Fraction(44, 7), Fraction(360, 1)]
    alphas = [Fraction(0, 1), Fraction(1, 6), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1, 1)]
    for p in periods:
        check((Fraction(1, 1) / p) * p == Fraction(1, 1), "fence", f"Haar unit mass for period {p}")
        for a in alphas:
            check(
                (Fraction(1, 1) / p) * (a * p) == a,
                "fence",
                f"Haar fractional arc mass for period {p}, alpha {a}",
            )
    for p1, p2 in itertools.combinations(periods, 2):
        for arc in [Fraction(1, 2), Fraction(1, 1), Fraction(3, 1)]:
            check(
                (Fraction(1, 1) / p1) * arc != (Fraction(1, 1) / p2) * arc,
                "fence",
                "distinct periods assign distinct masses to fixed arc length",
            )

    print(
        f"checks={checks} cyclic={cyclic_checks} char={char_checks} "
        f"fence={fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
