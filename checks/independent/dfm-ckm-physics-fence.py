"""Independent check for DFM-CKM-PHYSICS-FENCE.

Rational counting expressions and two Gaussian-rational quartets are
recomputed with fractions.Fraction. This file imports no repository code.
"""

from fractions import Fraction


def cycle_count(n):
    n = Fraction(n)
    return (n - 1) * (n - 1)


def constraint_count(n):
    n = Fraction(n)
    return n * (n - 1) / 2


def cp_count(n):
    n = Fraction(n)
    return (n - 1) * (n - 2) / 2


class GR:
    def __init__(self, re, im=0):
        self.re = Fraction(re)
        self.im = Fraction(im)

    def conj(self):
        return GR(self.re, -self.im)

    def mul(self, other):
        return GR(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def __eq__(self, other):
        return self.re == other.re and self.im == other.im

    def __repr__(self):
        return f"{self.re}+{self.im}i"


def quartet(a, b, c, d):
    return a.mul(b).mul(c.conj().mul(d.conj()))


def main():
    samples = (
        Fraction(0),
        Fraction(1),
        Fraction(2),
        Fraction(3),
        Fraction(4),
        Fraction(5),
        Fraction(-1),
        Fraction(3, 2),
        Fraction(7, 5),
    )
    for n in samples:
        if cycle_count(n) - constraint_count(n) != cp_count(n):
            raise SystemExit(f"difference failed at {n}")
        if cp_count(n) + (n - 1) != constraint_count(n):
            raise SystemExit(f"constraint sum failed at {n}")
    table = {
        1: (0, 0),
        2: (1, 0),
        3: (4, 1),
        4: (9, 3),
    }
    for n, (cyc, cp) in table.items():
        if cycle_count(n) != cyc or cp_count(n) != cp:
            raise SystemExit(f"table failed at {n}")
    if cycle_count(1) != cp_count(1):
        raise SystemExit("n=1 should agree")
    for n in (2, 3, 4):
        if cycle_count(n) == cp_count(n):
            raise SystemExit(f"n={n} should differ")
    if constraint_count(3) != 3:
        raise SystemExit("constraint count at 3")
    if cycle_count(3) - constraint_count(3) != 1:
        raise SystemExit("4 - 3")
    one = GR(1, 0)
    eye = GR(0, 1)
    q_real = quartet(one, one, one, one)
    q_imag = quartet(one, eye, one, one)
    if q_real != GR(1, 0) or q_imag != GR(0, 1):
        raise SystemExit(f"quartets {q_real} {q_imag}")
    if q_real.im == cp_count(3) or q_imag.im != cp_count(3):
        raise SystemExit("count match")
    if q_real == q_imag:
        raise SystemExit("quartets should differ")
    print("difference identity on 9 rational samples")
    print("table cycle/cp: n=1 -> 0,0; n=2 -> 1,0; n=3 -> 4,1; n=4 -> 9,3")
    print("n=3 split: cycle 4, constraint 3, cp 1")
    print("quartet imag parts 0 and 1; cp 3 matches only the second")
    print("checked: counting identities, four-point table, quartet split")


if __name__ == "__main__":
    main()
