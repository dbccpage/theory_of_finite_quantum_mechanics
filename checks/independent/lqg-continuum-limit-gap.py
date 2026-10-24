"""Independent check for LQG-CONTINUUM-LIMIT-GAP.

Recomputes the level-2 admissibility census on {0, 1, 2} and the two
quantum-dimension identities in Q(sqrt 2). Imports no repository code.
"""

from fractions import Fraction

from sympy import sqrt


def admissible(a: int, b: int, c: int) -> bool:
    return (
        a <= 2
        and b <= 2
        and c <= 2
        and a + b >= c
        and a + c >= b
        and b + c >= a
        and (a + b + c) % 2 == 0
        and a + b + c <= 4
    )


class Qsqrt2:
    """Element rat + coeff * sqrt(2), with rational components."""

    def __init__(self, rat: Fraction, coeff: Fraction) -> None:
        self.rat = Fraction(rat)
        self.coeff = Fraction(coeff)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Qsqrt2):
            return NotImplemented
        return self.rat == other.rat and self.coeff == other.coeff

    def __add__(self, other: "Qsqrt2") -> "Qsqrt2":
        return Qsqrt2(self.rat + other.rat, self.coeff + other.coeff)

    def __sub__(self, other: "Qsqrt2") -> "Qsqrt2":
        return Qsqrt2(self.rat - other.rat, self.coeff - other.coeff)

    def __mul__(self, other: "Qsqrt2") -> "Qsqrt2":
        return Qsqrt2(
            self.rat * other.rat + 2 * self.coeff * other.coeff,
            self.rat * other.coeff + self.coeff * other.rat,
        )


def main() -> None:
    labels = (0, 1, 2)
    roster = [
        (a, b, c)
        for a in labels
        for b in labels
        for c in labels
        if admissible(a, b, c)
    ]
    expected = [
        (0, 0, 0),
        (0, 1, 1),
        (0, 2, 2),
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 2),
        (1, 2, 1),
        (2, 0, 2),
        (2, 1, 1),
        (2, 2, 0),
    ]
    if roster != expected:
        raise SystemExit(f"roster {roster}")
    if len(roster) != 10:
        raise SystemExit(f"count {len(roster)}")
    if admissible(0, 0, 1):
        raise SystemExit("witness (0, 0, 1) was accepted")
    if 3**6 != 729 or 3**9 != 19683:
        raise SystemExit("tuple powers")
    one = Qsqrt2(1, 0)
    sqrt2 = Qsqrt2(0, 1)
    zero = Qsqrt2(0, 0)
    d0, d1, d2 = one, sqrt2, one
    if d1 * d1 - d0 != d2:
        raise SystemExit("d1^2 - d0")
    if d1 * d2 - d1 != zero:
        raise SystemExit("d1*d2 - d1")
    # The same identities in sympy, so the radical is not only a pair encoding.
    s = sqrt(2)
    if (s * s - 1) - 1 != 0 or s * 1 - s != 0:
        raise SystemExit("sympy dimensions")
    counts = (Fraction(3), Fraction(729), Fraction(19683))
    if len(set(counts)) != 3:
        raise SystemExit("counts are not pairwise distinct")
    scale = Fraction(1)
    if scale <= 0 or scale in counts:
        raise SystemExit("scale 1 does not separate the counts")
    print("admissible ordered triples: 10")
    print("roster:", roster)
    print("excluded witness: (0, 0, 1)")
    print("six-tuples: 729")
    print("nine-tuples: 19683")
    print("dimension identities: d1^2 - d0 = d2 and d1*d2 - d1 = 0")
    print("counts 3, 729, 19683 pairwise distinct; scale 1 is another positive rational")
    print("continuum limit, semiclassical limit, and physical cosmological constant: not checked")


if __name__ == "__main__":
    main()
