#!/usr/bin/env python3
"""Modulo-7 unit circle for L1-U1-SELECTOR-OTHER-SEGMENT.

Recomputes the eight powers of (2, 2) with ordinary integer arithmetic.
No repository module is imported. Other moduli, Gaussian rationals, and
any selection of C or U(1) are not checked.
"""

from __future__ import annotations


MOD = 7
G = (2, 2)
POWERS = (
    (1, 0),
    (2, 2),
    (0, 1),
    (5, 2),
    (6, 0),
    (5, 5),
    (0, 6),
    (2, 5),
)


def mul_int(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return ((a[0] * b[0] - a[1] * b[1]) % MOD, (a[0] * b[1] + a[1] * b[0]) % MOD)


def mul_nat(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    # Same pad as the Lean definition: 252 = 7 * 36.
    return ((a[0] * b[0] + 252 - a[1] * b[1]) % MOD, (a[0] * b[1] + a[1] * b[0]) % MOD)


def main() -> None:
    failures = 0
    checks = 0

    def check(cond: bool, label: str) -> None:
        nonlocal failures, checks
        checks += 1
        if not cond:
            failures += 1
            print("FAIL", label)

    point = (1, 0)
    seen = [point]
    for _ in range(8):
        nxt_i = mul_int(point, G)
        nxt_n = mul_nat(point, G)
        check(nxt_i == nxt_n, f"pad {point}")
        point = nxt_i
        seen.append(point)
    check(seen[:8] == list(POWERS), f"powers {seen[:8]}")
    check(seen[8] == (1, 0), f"eighth {seen[8]}")
    check(all(p != (1, 0) for p in seen[1:8]), "earlier")
    check(len(set(POWERS)) == 8, "distinct")
    check(8 == 7 + 1 and 8 != 4, "count")
    check(G not in ((0, 1), (0, 6), (1, 0), (6, 0)), "axis")
    for x, y in POWERS:
        check((x * x + y * y) % MOD == 1, f"norm {(x, y)}")
    solutions = [
        (x, y)
        for x in range(MOD)
        for y in range(MOD)
        if (x * x + y * y) % MOD == 1
    ]
    check(sorted(solutions) == sorted(POWERS), f"solutions {solutions}")
    # Closure, identity and inverses on this one list.
    check((1, 0) in POWERS, "identity")
    for a in POWERS:
        check(mul_int(a, (a[0], (-a[1]) % MOD)) == (1, 0), f"inverse {a}")
        for b in POWERS:
            check(mul_int(a, b) in POWERS, f"closed {a} {b}")
    print(
        "mod7 powers=8 order=8 eighth=(1, 0) count=8 equals=7+1 not4=true failures="
        + str(failures)
    )
    if failures:
        raise SystemExit(1)
    print(
        "L1-U1-SELECTOR-OTHER-SEGMENT INDEPENDENT CHECKER PASSED: checks="
        + str(checks)
        + " failed=0"
    )


if __name__ == "__main__":
    main()
