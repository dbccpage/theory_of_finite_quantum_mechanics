#!/usr/bin/env python3
"""Independent exact rational verifier for TFQ-0118 (CONTINUUM_INTERFACE).

Verifies with Python Fractions and exact integer/Gaussian-rational arithmetic (no Lean dependency):
1. Injective dyadic cyclic inclusion Fin N -> Fin (2*N) (x -> 2*x) for N = 1..12:
   - Strict injectivity of doubling on 0..N-1, and the missed odd residue 1.
   - Lean keeps the modular-addition homomorphism. This script does not recheck that identity.
2. Point-separating character sums on Z/4Z over Q[i]:
   - Dual character projector sum_{k=0}^3 chi_k(x) conj(chi_k(y)) == (4, 0) iff x == y else (0, 0).
   - For every pair x != y in Fin 4, there exists k in Fin 4 with chi_k(x) != chi_k(y).
3. Open continuum obligations fences (cdx2.haar_continuous_density & cdx2.interacting_qft):
   - Exact Riemann sum of t^2 on N uniform subintervals equals (N-1)*(2*N-1)/(6*N^2), and the
     discretization defect 1/3 - S_N(t^2) == (3*N - 1)/(6*N^2) > 0 for all N = 1..64.
   - Quartic interacting EOM m^2*phi + g*phi^3 has superposition defect 3*g*a*b*(a+b), vanishing at
     a = b = 1 iff g == 0.
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
    inclusion_checks = 0
    sep_checks = 0
    fence_checks = 0
    failures = 0

    def check(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, inclusion_checks, sep_checks, fence_checks, failures
        checks += 1
        if bucket == "inclusion":
            inclusion_checks += 1
        elif bucket == "sep":
            sep_checks += 1
        elif bucket == "fence":
            fence_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [{bucket}]: {msg}", file=sys.stderr)

    # Lean keeps dyadicInclude_add_mod_hom. The modular-addition identity is not rechecked here.
    for n in range(1, 13):
        img = [2 * x for x in range(n)]
        check(len(set(img)) == n, "inclusion", f"dyadicInclude injective at N={n}")
        check(1 not in img, "inclusion", f"odd residue 1 missed at N={n}")

    # 2. Point-separating character sums on Z/4Z
    for x, y in itertools.product(range(4), range(4)):
        acc: GaussRat = (Fraction(0), Fraction(0))
        for k in range(4):
            acc = g_add(acc, g_mul(chi4(k, x), g_conj(chi4(k, y))))
        expected: GaussRat = (Fraction(4), Fraction(0)) if x == y else (Fraction(0), Fraction(0))
        check(acc == expected, "sep", f"point projector ({x},{y})")
        if x != y:
            check(
                any(chi4(k, x) != chi4(k, y) for k in range(4)),
                "sep",
                f"characters separate {x} != {y}",
            )

    # 3. Discretization defect and quartic interaction nonlinearity fences
    for n in range(1, 65):
        n_q = Fraction(n, 1)
        riemann_sum = sum((Fraction(j, n) ** 2) * Fraction(1, n) for j in range(n))
        closed_form = (n_q - 1) * (2 * n_q - 1) / (6 * n_q * n_q)
        defect = Fraction(1, 3) - riemann_sum
        defect_closed = (3 * n_q - 1) / (6 * n_q * n_q)
        check(
            riemann_sum == closed_form and defect == defect_closed and defect > Fraction(0),
            "fence",
            f"quadratic discretization defect at N={n}",
        )

    rats = [Fraction(-2, 1), Fraction(-1, 2), Fraction(0, 1), Fraction(1, 3), Fraction(1, 1), Fraction(2, 1)]
    for m_sq, g, a, b in itertools.product(rats[:3], rats, rats[1:], rats[1:]):
        def eom(phi: Fraction) -> Fraction:
            return m_sq * phi + g * (phi**3)

        sup_defect = eom(a + b) - (eom(a) + eom(b))
        check(
            sup_defect == Fraction(3, 1) * g * a * b * (a + b),
            "fence",
            "quartic superposition defect formula",
        )
        if a == Fraction(1) and b == Fraction(1):
            check(
                (sup_defect == Fraction(0)) == (g == Fraction(0)),
                "fence",
                "unit superposition defect vanishes iff g == 0",
            )

    print(
        f"checks={checks} inclusion={inclusion_checks} sep={sep_checks} "
        f"fence={fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
