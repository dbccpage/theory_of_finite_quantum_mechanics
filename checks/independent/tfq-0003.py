"""Independent integer check for the TFQ-0003 3-cycle signature.

Recomputes holonomy, coboundary, Phi1, and the two classical residuals
without importing repository code.

AuthorityEffect: None
"""

from __future__ import annotations

import sys


def d0(h: tuple[int, int, int]) -> tuple[int, int, int]:
    h0, h1, h2 = h
    return (h1 - h0, h2 - h1, h0 - h2)


def hol(c: tuple[int, int, int]) -> int:
    return c[0] + c[1] + c[2]


def l1(c: tuple[int, int, int]) -> int:
    return abs(c[0]) + abs(c[1]) + abs(c[2])


def sub_co(c: tuple[int, int, int], d: tuple[int, int, int]) -> tuple[int, int, int]:
    return (c[0] - d[0], c[1] - d[1], c[2] - d[2])


def gauge(c: tuple[int, int, int], h: tuple[int, int, int]) -> tuple[int, int, int]:
    return sub_co(c, d0(h))


def preimage(c: tuple[int, int, int]) -> tuple[int, int, int]:
    return (0, c[0], c[0] + c[1])


def edge0(s: int) -> tuple[int, int, int]:
    return (s, 0, 0)


def edge1(s: int) -> tuple[int, int, int]:
    return (0, s, 0)


CHECKS = 0
FAILURES = 0


def check(condition: bool) -> None:
    global CHECKS, FAILURES
    CHECKS += 1
    if not condition:
        FAILURES += 1


def main() -> int:
    sample = (1, -2, 4)
    check(hol(sample) == 3)
    check(abs(hol(sample)) == 3)
    check(l1(sample) == 7)
    check(abs(hol(sample)) < l1(sample))
    check(sample != edge0(hol(sample)))
    zero_example = (1, 2, -3)
    check(hol(zero_example) == 0)
    check(preimage(zero_example) == (0, 1, 3))
    check(d0((0, 1, 3)) == (1, 2, -3))

    values = range(-3, 4)
    cochains = [(a, b, c) for a in values for b in values for c in values]
    for vertex in cochains:
        check(hol(d0(vertex)) == 0)
    for cochain in cochains:
        total = hol(cochain)
        check(l1(cochain) >= abs(total))
        check(hol(edge0(total)) == total)
        check(l1(edge0(total)) == abs(total))
        check(hol(edge1(total)) == total)
        check(l1(edge1(total)) == abs(total))
        if total == 0:
            check(d0(preimage(cochain)) == cochain)
        else:
            check(edge0(total) != edge1(total))
        difference = sub_co(cochain, edge0(total))
        check(hol(difference) == 0)
        check(d0(preimage(difference)) == difference)
        check(gauge(cochain, preimage(difference)) == edge0(total))
        for vertex in cochains:
            shifted = gauge(cochain, vertex)
            check(hol(shifted) == total)
            check(l1(shifted) >= abs(total))

    print(
        f"TFQ-0003 independent check: sample hol=3 phi1=3 l1=7; "
        f"checks={CHECKS} failed={FAILURES}"
    )
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
