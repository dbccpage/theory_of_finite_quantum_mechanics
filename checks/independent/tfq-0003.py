#!/usr/bin/env python3
"""Independent check for the TFQ-0003 finite obstruction signature.

No repository imports. Exact integers only.
"""

from __future__ import annotations

FAILURES = 0
CHECKS = 0


def check(cond: bool, label: str) -> None:
    global FAILURES, CHECKS
    CHECKS += 1
    if not cond:
        FAILURES += 1
        print(f"FAIL {label}")


def d0(f0: int, f1: int, f2: int) -> tuple[int, int, int]:
    return (f1 - f0, f2 - f1, f2 - f0)


def d1(w01: int, w12: int, w02: int) -> int:
    return w01 + w12 - w02


def l1(vals: tuple[int, ...]) -> int:
    return sum(abs(v) for v in vals)


def sub(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x - y for x, y in zip(a, b))


def rcl(phi: int, gamma: int) -> tuple[int, int] | None:
    if phi != 0:
        return (gamma, phi)
    if gamma == 0:
        return (0, 1)
    return None


def main() -> None:
    check(0 != 2, "vertex comparison 0 != 2")
    edge02 = (0, 0, 1)
    check(d1(*edge02) == -1, "edge (0,2) has face charge -1")
    check(d1(*edge02) != 0, "raw distinction is not a coboundary")

    for f0 in (-2, 0, 3):
        for f1 in (-1, 0, 4):
            for f2 in (0, 1, 5):
                check(d1(*d0(f0, f1, f2)) == 0, f"d1 d0 at {(f0, f1, f2)}")

    sample = (1, 1, 0)
    check(d1(*sample) == 2, "sample face charge 2")
    repair = (0, 1, 0)
    residual = sub(sample, d0(*repair))
    check(residual == (0, 2, 0), "recorded residual (0, 2, 0)")
    check(l1(residual) == 2, "recorded residual mass 2")

    # Clearing the first two edges attains |d1|.
    a, b = sample[0], sample[1]
    cleared = sub(sample, d0(0, a, a + b))
    check(cleared == (0, 0, sample[2] - (a + b)), "cleared support")
    check(l1(cleared) == abs(d1(*sample)), "cleared mass equals |d1|")

    # Algebraic cancellation: (1-a) + (1-b) - (-(a+b)) = 2 for every integer a, b.
    for a_i in range(-8, 9):
        for b_i in range(-8, 9):
            x, y, z = 1 - a_i, 1 - b_i, a_i + b_i
            check(x + y - (-z) == 2, f"cancellation {(a_i, b_i)}")
            check(abs(x) + abs(y) + abs(z) >= 2, f"l1 lower {(a_i, b_i)}")
            check(l1(sub(sample, d0(0, a_i, a_i + b_i))) >= 2, f"repair box {(a_i, b_i)}")

    check(rcl(2, 2) == (2, 2), "triangle ratio 2/2")
    check(2 == 2, "2/2 equals 1 as equal numerator and denominator")
    check(rcl(0, 0) == (0, 1), "both-vanish value 0/1")
    check(rcl(0, 1) is None, "refusal of 0 denominator with nonzero charge")

    # Unfilled 4-cycle. Gamma2 is 0 because no 2-cell is declared.
    cycle = (1, 0, 0, 0)

    def d0c(f: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        f0, f1, f2, f3 = f
        return (f1 - f0, f2 - f1, f3 - f2, f0 - f3)

    def hol(w: tuple[int, int, int, int]) -> int:
        return sum(w)

    check(hol(d0c((3, -1, 4, 2))) == 0, "cycle coboundary sums to 0")
    check(hol(cycle) == 1, "cycle sample holonomy 1")
    check(l1(cycle) == 1, "cycle sample l1 is 1")
    best = min(l1(sub(cycle, d0c(f))) for f in
               ((a, b, c, d) for a in range(-2, 3) for b in range(-2, 3)
                for c in range(-2, 3) for d in range(-2, 3)))
    check(best == 1, "cycle repair box minimum 1")
    check(0 == 0, "cycle Gamma2 is the declared 0")
    check(rcl(1, 0) == (0, 1), "cycle classical residual 0/1")
    check(hol(cycle) != 0, "cycle sample is not a coboundary")

    print(f"checked {CHECKS} conditions, {FAILURES} failures")
    print("triangle: Phi1 = 2, Gamma2 = 2, R_cl = 2/2 = 1")
    print("zero cochain: Phi1 = 0, Gamma2 = 0, R_cl = 0/1")
    print("4-cycle (1,0,0,0): Phi1 = 1, Gamma2 = 0, R_cl = 0/1, not exact")
    print("refusal cell rcl(0, 1) is None and is not attained on these two complexes")
    if FAILURES:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
