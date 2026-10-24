#!/usr/bin/env python3
"""Independent exact rational and number-theoretic verifier for TFQ-0119 (CONTINUUM_INTERFACE).

Verifies with Python Fractions and exact integer arithmetic (no Lean dependency):
1. Lean keeps the dyadic direct-system invariance and the level-k Haar sum of one.
   This script does not recheck Fraction cancellation of those identities.
2. Non-surjectivity of the dyadic direct limit onto the circle (1/3 not in Z[1/2]):
   - For k = 0..19, (2^k) % 3 is 1 or 2.
   - For k = 0..8 and m = 0..2^k, m / 2^k is not 1/3.
   - For p in {3, 5, 7, 11, 13} and k = 0..11, 2^k is not divisible by p.
3. Dyadic Cauchy sequence approximating 1/3 without converging in the uncompleted direct limit:
   - For n = 1..20, (4^n - 1) % 3 == 0, so a_n = (4^n - 1) // 3 is an exact integer numerator
     over 4^n = 2^(2n), with residual 1/3 - a_n / 4^n == 1 / (3 * 4^n) > 0 contracting by 1/4 per step.
"""

from __future__ import annotations

from fractions import Fraction
import sys


def dyadic_rat_val(k: int, m: int) -> Fraction:
    return Fraction(m, 2**k)


def main() -> int:
    checks = 0
    obstruction_checks = 0
    cauchy_checks = 0
    failures = 0

    def check(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, obstruction_checks, cauchy_checks, failures
        checks += 1
        if bucket == "obstruction":
            obstruction_checks += 1
        elif bucket == "cauchy":
            cauchy_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [{bucket}]: {msg}", file=sys.stderr)

    # Lean keeps the direct-system invariance and the Haar sum of one.
    # Fraction cancellation of those identities is not rechecked here.

    # 1/3 (and 1/p for the recorded odd primes) is never a checked dyadic.
    for k in range(20):
        rem = (2**k) % 3
        check(rem in (1, 2) and rem != 0, "obstruction", f"(2^{k}) % 3 != 0")
    for k in range(9):
        for m in range(2**k + 1):
            check(
                dyadic_rat_val(k, m) != Fraction(1, 3),
                "obstruction",
                f"{m}/2^{k} != 1/3",
            )
    for p in (3, 5, 7, 11, 13):
        for k in range(12):
            check((2**k) % p != 0, "obstruction", f"2^{k} not divisible by odd prime {p}")

    # 3. Dyadic Cauchy sequence s_n = ((4^n - 1)/3) / 4^n approaching 1/3
    for n in range(1, 21):
        num_raw = 4**n - 1
        check(num_raw % 3 == 0, "cauchy", f"(4^{n} - 1) divisible by 3")
        a_n = num_raw // 3
        approx = dyadic_rat_val(2 * n, a_n)
        res = Fraction(1, 3) - approx
        expected_res = Fraction(1, 3 * (4**n))
        check(
            res == expected_res and res > Fraction(0) and approx < Fraction(1, 3),
            "cauchy",
            f"Cauchy residual at n={n}",
        )
        if n < 20:
            next_res = Fraction(1, 3) - dyadic_rat_val(2 * (n + 1), (4 ** (n + 1) - 1) // 3)
            check(
                next_res == Fraction(1, 4) * res,
                "cauchy",
                f"quarter contraction at n={n}",
            )

    print(
        f"checks={checks} obstruction={obstruction_checks} "
        f"cauchy={cauchy_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
