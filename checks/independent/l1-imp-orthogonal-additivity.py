#!/usr/bin/env python3
"""One 2 by 2 integer Gram matrix for L1-IMP-ORTHOGONAL-ADDITIVITY.

The quadratic form is expanded with integer arithmetic.
No repository module is imported. Arbitrary orthogonal frames stay outside.
"""

from __future__ import annotations


def qf(g00: int, g01: int, g10: int, g11: int, a: int, b: int) -> int:
    return g00 * a * a + g01 * a * b + g10 * b * a + g11 * b * b


def main() -> None:
    failures = 0
    checks = 0

    def check(cond: bool, label: str) -> None:
        nonlocal failures, checks
        checks += 1
        if not cond:
            failures += 1
            print("FAIL", label)

    check(1 + (-1) == 0, "pair sum")
    check(1 != 0 and -1 != 0, "entries")
    # Exact cancellation for every integer pair: the cross terms differ by order only.
    # a*b - b*a is 0 because multiplication of integers commutes, so the form is a*a + b*b.
    for a in range(-8, 9):
        for b in range(-8, 9):
            cross = a * b - b * a
            check(cross == 0, f"comm {a} {b}")
            got = qf(1, 1, -1, 1, a, b)
            check(got == a * a + b * b, f"readout {a} {b}")
            check(
                qf(1, 1, -1, 1, a, 0) + qf(1, 1, -1, 1, 0, b) == got,
                f"axis {a} {b}",
            )
    print(
        "matrix=[[1,1],[-1,1]] pair_sum=0 entries_nonzero=true "
        + "census_a=-8..8 census_b=-8..8 failures="
        + str(failures)
    )
    if failures:
        raise SystemExit(1)
    print(
        "L1-IMP-ORTHOGONAL-ADDITIVITY INDEPENDENT CHECKER PASSED: checks="
        + str(checks)
        + " failed=0"
    )


if __name__ == "__main__":
    main()
