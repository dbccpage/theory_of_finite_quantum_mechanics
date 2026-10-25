"""Integer-triangle audit for the weighted residual campaign module.

Recomputes coboundary linearity, the residual shift identity, the closed
pairing, and the absolute residual sum 2 on a finite window. Does not
import repository code. The window is an audit. The general argument is
the Lean module.
"""
from __future__ import annotations

FAILURES = 0


def fail(message: str) -> None:
    global FAILURES
    FAILURES += 1
    print(message)


def d0(f0: int, f1: int, f2: int) -> tuple[int, int, int]:
    return (f1 - f0, f2 - f1, f2 - f0)


def add3(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub3(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def abs_sum(v: tuple[int, int, int]) -> int:
    return abs(v[0]) + abs(v[1]) + abs(v[2])


def pair110(v: tuple[int, int, int]) -> int:
    return v[0] + v[1] - v[2]


def main() -> int:
    delta = (1, 1, 0)
    attained = sub3(delta, d0(0, 1, 0))
    if attained != (0, 2, 0) or abs_sum(attained) != 2:
        fail(f"attained residual {attained}")
    if pair110(attained) != 2:
        fail("attained pairing")
    window = range(-4, 5)
    for f0 in window:
        for f1 in window:
            for f2 in window:
                cob = d0(f0, f1, f2)
                if pair110(cob) != 0:
                    fail(f"pair d0 {(f0, f1, f2)}")
                residual = sub3(delta, cob)
                if pair110(residual) != 2:
                    fail(f"pair residual {(f0, f1, f2)}")
                if abs_sum(residual) < 2:
                    fail(f"lower bound {(f0, f1, f2)}")
                for g0 in window:
                    for g1 in window:
                        for g2 in window:
                            left = d0(f0 + g0, f1 + g1, f2 + g2)
                            right = add3(d0(f0, f1, f2), d0(g0, g1, g2))
                            if left != right:
                                fail(f"linear {(f0, f1, f2)} {(g0, g1, g2)}")
                            shifted = sub3(add3(delta, d0(g0, g1, g2)), left)
                            plain = sub3(delta, d0(f0, f1, f2))
                            if shifted != plain or abs_sum(shifted) != abs_sum(plain):
                                fail(f"shift {(f0, f1, f2)} {(g0, g1, g2)}")
    repair = sub3(add3(delta, d0(3, -2, 5)), d0(0 + 3, 1 + -2, 0 + 5))
    if abs_sum(repair) != 2:
        fail(f"shifted attained {repair}")
    print(f"failures={FAILURES}")
    print("finite window is an audit, not the general argument")
    return FAILURES


if __name__ == "__main__":
    raise SystemExit(main())
