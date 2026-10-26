"""Finite 2 by 4 coset-weight count. Imports no repository code.

AuthorityEffect: None. One parity-check matrix and two syndromes.
This is not a reduction and not a hardness result.
"""

from __future__ import annotations

import sys


def bit(n: int, i: int) -> int:
    return (n // 2**i) % 2


def row1(n: int) -> int:
    return (bit(n, 0) + bit(n, 1)) % 2


def row2(n: int) -> int:
    return (bit(n, 1) + bit(n, 2) + bit(n, 3)) % 2


def dot4(a: int, b: int, c: int, d: int, n: int) -> int:
    return (a * bit(n, 0) + b * bit(n, 1) + c * bit(n, 2) + d * bit(n, 3)) % 2


def wt(n: int) -> int:
    return bit(n, 0) + bit(n, 1) + bit(n, 2) + bit(n, 3)


def main() -> int:
    labels = list(range(16))
    if len(labels) != 16:
        print("FAILURE length")
        return 1
    for n in labels:
        if row1(n) != dot4(1, 1, 0, 0, n) or row2(n) != dot4(0, 1, 1, 1, n):
            print("FAILURE matrix row", n)
            return 1
    coset = [n for n in labels if row1(n) == 1 and row2(n) == 0]
    kernel = [n for n in labels if row1(n) == 0 and row2(n) == 0]
    weights = [wt(n) for n in coset]
    weight_one = [n for n in coset if wt(n) == 1]
    minimum = min(weights)
    coords = (bit(1, 0), bit(1, 1), bit(1, 2), bit(1, 3))
    expected_coset = [1, 6, 10, 13]
    expected_weights = [1, 2, 2, 3]
    expected_kernel = [0, 7, 11, 12]
    checks = [
        ("coset", coset, expected_coset),
        ("weights", weights, expected_weights),
        ("minimum", minimum, 1),
        ("weight_one", weight_one, [1]),
        ("coords", coords, (1, 0, 0, 0)),
        ("kernel", kernel, expected_kernel),
    ]
    for name, got, expected in checks:
        if got != expected:
            print(f"FAILURE {name}: {got} != {expected}")
            return 1
        print(f"CHECK {name} {got}")
    print("CHECKS", len(checks) + 16)
    print("FAILURES 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
