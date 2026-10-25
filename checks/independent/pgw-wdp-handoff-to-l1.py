"""Independent check for the one-triangle boundary of PGW-WDP-HANDOFF-TO-L1.

Integer arithmetic only. No repository imports. The finite box recomputes
concrete values and samples the residual inequality. It does not discharge
the Lean statements quantified over every integer.
"""
from __future__ import annotations


def iabs(n: int) -> int:
    return -n if n < 0 else n


def d0(f0: int, f1: int, f2: int) -> tuple[int, int, int]:
    return (f1 - f0, f2 - f1, f2 - f0)


def face(x01: int, x12: int, x02: int) -> int:
    return x01 + x12 - x02


def l1(x01: int, x12: int, x02: int) -> int:
    return iabs(x01) + iabs(x12) + iabs(x02)


def leakage(f0: int, f1: int, f2: int) -> int:
    a, b, c = d0(f0, f1, f2)
    return l1(a, b, c)


def repair(h01: int, h12: int, h02: int) -> tuple[int, int, int]:
    value = face(h01, h12, h02)
    if value < 0:
        return (0, h01, h01 + h12)
    return (0, h01 - value, h02)


def verdict(phi: int, gamma: int) -> int:
    if phi > 0:
        return 0
    if gamma > 0:
        return 0
    return 1


def fibre_constant(a0: int, a1: int) -> bool:
    return a0 == a1


def residual(h: tuple[int, int, int], f: tuple[int, int, int]) -> tuple[int, int, int]:
    cob = d0(*f)
    return (h[0] - cob[0], h[1] - cob[1], h[2] - cob[2])


def main() -> int:
    failures = 0
    checked = 0

    def expect(condition: bool) -> None:
        nonlocal failures, checked
        checked += 1
        if not condition:
            failures += 1

    expect(leakage(0, 1, 0) == 2)
    expect(d0(0, 1, 0) == (1, -1, 0))
    expect(l1(1 - 1, -1 - (-1), 0 - 0) == 0)
    expect(leakage(0, 1, 0) != 0)
    expect(face(1, 0, 0) == 1)
    expect(verdict(1, 1) == 0)
    expect(verdict(0, 0) == 1)
    expect(fibre_constant(1, 1))
    expect(not fibre_constant(0, 1))

    box = range(-2, 3)
    for f0 in box:
        for f1 in box:
            for f2 in box:
                cob = d0(f0, f1, f2)
                expect(face(*cob) == 0)
                for h01 in box:
                    for h12 in box:
                        for h02 in box:
                            value = face(h01, h12, h02)
                            gap = residual((h01, h12, h02), (f0, f1, f2))
                            expect(iabs(value) <= l1(*gap))

    for h01 in box:
        for h12 in box:
            for h02 in box:
                value = face(h01, h12, h02)
                neg = d0(0, h01, h01 + h12)
                expect(h01 - neg[0] == 0)
                expect(h12 - neg[1] == 0)
                expect(h02 - neg[2] == -value)
                nonneg = d0(0, h01 - value, h02)
                expect(h01 - nonneg[0] == value)
                expect(h12 - nonneg[1] == 0)
                expect(h02 - nonneg[2] == 0)
                picked = repair(h01, h12, h02)
                if value < 0:
                    expect(picked == (0, h01, h01 + h12))
                    expect(l1(0, 0, -value) == iabs(value))
                else:
                    expect(picked == (0, h01 - value, h02))
                    expect(l1(value, 0, 0) == iabs(value))
                if value == 0:
                    expect((h01, h12, h02) == nonneg)

    print(f"checked {checked} conditions, {failures} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
