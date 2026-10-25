"""Independent check for the dimension-2 boundary of MUB-PRIME-POWER-CONSTRUCTION.

Gaussian-integer arithmetic only. No repository imports. The six vectors and
the two-element character do not discharge a construction for every prime power.
"""
from __future__ import annotations


def gadd(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])


def gmul(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gconj(a: tuple[int, int]) -> tuple[int, int]:
    return (a[0], -a[1])


def gnorm(a: tuple[int, int]) -> int:
    return a[0] * a[0] + a[1] * a[1]


def ip(u: tuple[tuple[int, int], tuple[int, int]], v: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, int]:
    return gadd(gmul(gconj(u[0]), v[0]), gmul(gconj(u[1]), v[1]))


def vnorm(u: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return gnorm(u[0]) + gnorm(u[1])


def chi(bit: int) -> int:
    return -1 if bit else 1


def xor(a: int, b: int) -> int:
    return 0 if a == b else 1


def main() -> int:
    failures = 0
    checked = 0

    def expect(condition: bool) -> None:
        nonlocal failures, checked
        checked += 1
        if not condition:
            failures += 1

    z0 = ((1, 0), (0, 0))
    z1 = ((0, 0), (1, 0))
    x0 = ((1, 0), (1, 0))
    x1 = ((1, 0), (-1, 0))
    y0 = ((1, 0), (0, 1))
    y1 = ((1, 0), (0, -1))
    expect(gmul((0, 1), (0, 1)) == (-1, 0))
    norms = {z0: 1, z1: 1, x0: 2, x1: 2, y0: 2, y1: 2}
    for vector, value in norms.items():
        expect(vnorm(vector) == value)
        expect(ip(vector, vector) == (value, 0))
    for left, right in ((z0, z1), (x0, x1), (y0, y1)):
        expect(ip(left, right) == (0, 0))
    for left in (z0, z1):
        for right in (x0, x1, y0, y1):
            expect(gnorm(ip(left, right)) * 2 == vnorm(left) * vnorm(right))
    for left in (x0, x1):
        for right in (y0, y1):
            expect(gnorm(ip(left, right)) * 2 == vnorm(left) * vnorm(right))
    expect(chi(0) == 1)
    expect(chi(1) == -1)
    expect(xor(0, 0) == 0)
    expect(xor(1, 1) == 0)
    expect(chi(xor(0, 0)) == 1)
    expect(chi(xor(1, 1)) == 1)
    print(f"checked {checked} conditions, {failures} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
