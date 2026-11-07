"""Integer audit of 3 * 3 + 4 * 4 = 5 * 5 and of 5 * a * a = 4 * b * b.

The residue tables modulo 5 are exhaustive. The descent step is the same
divisibility reduction used for every natural-number solution. A finite
window is an extra audit of that equation, not a substitute for the
reduction. This script imports no repository code.
"""
from __future__ import annotations


def square_residues() -> dict[int, int]:
    return {r: (r * r) % 5 for r in range(5)}


def descent(a: int, b: int) -> tuple[int, int]:
    if 5 * a * a != 4 * b * b:
        raise SystemExit(f"equation fails at {(a, b)}")
    guard = b + 1
    while b != 0:
        if guard == 0:
            raise SystemExit("descent did not shrink")
        guard -= 1
        if (4 * (b * b)) % 5 != 0 or b % 5 != 0:
            raise SystemExit(f"b not divisible by 5: {b}")
        r = b // 5
        if not r < b:
            raise SystemExit(f"r did not shrink: {r} from {b}")
        if (a * a) % 5 != 0 or a % 5 != 0:
            raise SystemExit(f"a not divisible by 5: {a}")
        s = a // 5
        if 5 * s * s != 4 * r * r:
            raise SystemExit(f"reduced equation fails at {(s, r)}")
        a, b = s, r
    if a != 0 or 5 * a * a != 0:
        raise SystemExit(f"a remained {a}")
    return a, b


def main() -> None:
    residues = square_residues()
    if set(residues.values()) != {0, 1, 4}:
        raise SystemExit(f"residues {residues}")
    if [r for r, sq in residues.items() if sq == 0] != [0]:
        raise SystemExit("square zero class is not residue 0")
    four_zero = [r for r, sq in residues.items() if (4 * sq) % 5 == 0]
    if four_zero != [0]:
        raise SystemExit(f"four-times-square zero class {four_zero}")
    if 3 * 3 + 4 * 4 != 5 * 5 or 5 * 5 != 25:
        raise SystemExit("3-4-5 scale failed")
    if descent(0, 0) != (0, 0):
        raise SystemExit("zero solution failed")
    for s in range(6):
        if 5 * (5 * s) * (5 * s) != 125 * s * s:
            raise SystemExit(f"left scale failed at {s}")
        if 4 * (5 * s) * (5 * s) != 100 * s * s:
            raise SystemExit(f"right scale failed at {s}")
    window = 0
    for a in range(31):
        for b in range(31):
            window += 1
            if 5 * a * a == 4 * b * b and descent(a, b) != (0, 0):
                raise SystemExit(f"window solution {(a, b)}")
    if window != 31 * 31:
        raise SystemExit(f"window count {window}")
    print("checked 3*3 + 4*4 = 25 = 5*5")
    print("checked squares mod 5 on residues 0, 1, 2, 3, 4 are 0, 1, 4, 4, 1")
    print("checked a square is 0 mod 5 only for residue 0")
    print("checked 4 times a square is 0 mod 5 only for residue 0")
    print("checked descent on (0, 0) returns (0, 0)")
    print("checked 5*(5*s)*(5*s) = 125*s*s and 4*(5*s)*(5*s) = 100*s*s for s = 0, 1, 2, 3, 4, 5")
    print("checked the equation on a = 0..30 and b = 0..30 holds only at (0, 0), by the same descent")
    print("failures=0")


if __name__ == "__main__":
    main()
