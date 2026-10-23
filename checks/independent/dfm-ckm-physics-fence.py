"""Independent check for DFM-CKM-PHYSICS-FENCE.

Rational counting expressions and two Gaussian-rational quartets are
recomputed with fractions.Fraction. This file imports no repository code.
"""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction
from itertools import product


def exact_rational(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise TypeError("expected an int or Fraction (not bool, float, or text)")


def cycle_count(n: int | Fraction) -> Fraction:
    n = exact_rational(n)
    return (n - 1) * (n - 1)


def constraint_count(n: int | Fraction) -> Fraction:
    n = exact_rational(n)
    return n * (n - 1) / 2


def cp_count(n: int | Fraction) -> Fraction:
    n = exact_rational(n)
    return (n - 1) * (n - 2) / 2


class GR:
    def __init__(self, re: int | Fraction, im: int | Fraction = 0) -> None:
        self.re = exact_rational(re)
        self.im = exact_rational(im)

    def conj(self) -> GR:
        return GR(self.re, -self.im)

    def mul(self, other: GR) -> GR:
        return GR(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def inv(self) -> GR:
        norm = self.re * self.re + self.im * self.im
        if not norm:
            raise ValueError("zero has no multiplicative inverse")
        return GR(self.re / norm, -self.im / norm)

    def div(self, other: GR) -> GR:
        return self.mul(other.inv())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GR):
            return NotImplemented
        return self.re == other.re and self.im == other.im

    def __repr__(self) -> str:
        return f"{self.re}+{self.im}i"


def quartet(a: GR, b: GR, c: GR, d: GR) -> GR:
    return a.mul(b).mul(c.conj().mul(d.conj()))


Table = tuple[tuple[GR, ...], ...]


def shape(matrix: Table) -> tuple[int, int]:
    if not matrix or not matrix[0]:
        raise ValueError("a base row and column are required")
    width = len(matrix[0])
    for row in matrix:
        if len(row) != width:
            raise ValueError("ragged table")
        for entry in row:
            if not isinstance(entry, GR) or entry == GR(0):
                raise ValueError("table labels must be nonzero Gaussian rationals")
    return len(matrix), width


def normalize(matrix: Table) -> Table:
    shape(matrix)
    corner = matrix[0][0]
    return tuple(tuple(entry.mul(corner).div(row[0].mul(matrix[0][j]))
                       for j, entry in enumerate(row)) for row in matrix)


def act(matrix: Table, rows: tuple[GR, ...], cols: tuple[GR, ...]) -> Table:
    height, width = shape(matrix)
    if len(rows) != height or len(cols) != width:
        raise ValueError("gauge dimensions differ from table")
    if any(not isinstance(x, GR) or x == GR(0) for x in rows + cols):
        raise ValueError("gauge labels must be nonzero Gaussian rationals")
    return tuple(tuple(rows[i].mul(x).div(cols[j]) for j, x in enumerate(row))
                 for i, row in enumerate(matrix))


def witness(left: Table, right: Table) -> tuple[tuple[GR, ...], tuple[GR, ...]] | None:
    if shape(left) != shape(right):
        raise ValueError("table shapes differ")
    if normalize(left) != normalize(right):
        return None
    rows = tuple(b[0].div(a[0]) for a, b in zip(left, right, strict=True))
    cols = tuple(a.div(left[0][0]).div(b.div(right[0][0]))
                 for a, b in zip(left[0], right[0], strict=True))
    return rows, cols


def sign_tables(height: int, width: int) -> list[Table]:
    return [tuple(tuple(GR(bits[i * width + j]) for j in range(width))
                  for i in range(height))
            for bits in product((-1, 1), repeat=height * width)]


def check_canonical(table: Table) -> Table:
    norm = normalize(table)
    if normalize(norm) != norm:
        raise SystemExit("normalization is not idempotent")
    if any(x != GR(1) for x in norm[0]) or any(row[0] != GR(1) for row in norm):
        raise SystemExit("canonical boundary is not one")
    return norm


def check_sign_actions(table: Table, height: int, width: int) -> int:
    norm = normalize(table)
    checked = 0
    for scalars in product((-1, 1), repeat=height + width):
        rows = tuple(GR(x) for x in scalars[:height])
        cols = tuple(GR(x) for x in scalars[height:])
        if normalize(act(table, rows, cols)) != norm:
            raise SystemExit("rephasing changed canonical coordinates")
        checked += 1
    return checked


def check_pair(table: Table, other: Table) -> None:
    result = witness(table, other)
    if result is not None and act(table, *result) != other:
        raise SystemExit("computed equivalence witness is unsound")
    if (result is None) == (normalize(table) == normalize(other)):
        raise SystemExit("decision and separating invariant disagree")


def check_nonreal() -> None:
    table = ((GR(1, 1), GR(2, -1)), (GR(Fraction(1, 3), 2), GR(-1, 3)))
    rows, cols = (GR(0, 1), GR(2)), (GR(1, -1), GR(Fraction(2, 3)))
    other = act(table, rows, cols)
    reconstructed = witness(table, other)
    if reconstructed is None or act(table, *reconstructed) != other:
        raise SystemExit("Gaussian-rational reconstruction failed")
    separated = (other[0], (other[1][0], other[1][1].mul(GR(2))))
    if witness(table, separated) is not None:
        raise SystemExit("different cross ratio was accepted")


def check_rephasing() -> None:
    transformations = 0
    comparisons = 0
    orbit_counts = []
    for height, width in ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3)):
        tables = sign_tables(height, width)
        canonical = []
        for table in tables:
            norm = check_canonical(table)
            if norm not in canonical:
                canonical.append(norm)
            transformations += check_sign_actions(table, height, width)
            for other in tables:
                check_pair(table, other)
                comparisons += 1
        expected = 2 ** ((height - 1) * (width - 1))
        if len(canonical) != expected:
            raise SystemExit("independent-coordinate count failed")
        orbit_counts.append(len(canonical))
    check_nonreal()
    print(f"rephasing: {transformations} sign actions, {comparisons} pair decisions; orbits {orbit_counts}")
    print("nonreal rational reconstruction and separated cross-ratio control passed")


def check_invalid_inputs() -> None:
    """Domain refusals use exceptions, including under optimized Python."""
    cases: list[tuple[str, Callable[[], object], type[Exception]]] = [
        ("bool", lambda: exact_rational(True), TypeError),
        ("float", lambda: exact_rational(0.5), TypeError),
        ("text", lambda: exact_rational("1"), TypeError),
        ("zero inverse", lambda: GR(0).inv(), ValueError),
        ("empty table", lambda: shape(()), ValueError),
        ("empty row", lambda: shape(((),)), ValueError),
        ("ragged", lambda: shape(((GR(1),), (GR(1), GR(1)))), ValueError),
        ("zero label", lambda: shape(((GR(0),),)), ValueError),
        ("bad row gauge", lambda: act(((GR(1),),), (), (GR(1),)), ValueError),
        ("zero gauge", lambda: act(((GR(1),),), (GR(0),), (GR(1),)), ValueError),
        ("different shapes", lambda: witness(((GR(1),),), ((GR(1), GR(1)),)), ValueError),
    ]
    for label, action, error in cases:
        try:
            action()
        except error:
            continue
        raise SystemExit("invalid input was admitted: " + label)
    print(f"{len(cases)} invalid-domain cases refused")


def main() -> None:
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
    for sample in samples:
        if cycle_count(sample) - constraint_count(sample) != cp_count(sample):
            raise SystemExit(f"difference failed at {sample}")
        if cp_count(sample) + (sample - 1) != constraint_count(sample):
            raise SystemExit(f"constraint sum failed at {sample}")
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
    print("quartet imag parts 0 and 1; cpCount(3) matches only the second")
    print("checked: counting identities, four-point table, quartet split")
    check_rephasing()
    check_invalid_inputs()


if __name__ == "__main__":
    main()
