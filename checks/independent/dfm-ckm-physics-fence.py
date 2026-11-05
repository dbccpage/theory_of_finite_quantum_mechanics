"""Bounded Gaussian-table rephasing and declared rational counting controls.

AuthorityEffect: None. No unitary mixing matrix, measured phase or Yukawa model
is constructed. Exact table classification concerns supplied nonzero labels.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path as _Path
import sys as _sys

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import integer, rational, sequence
from checker_support.gaussian_rational import GaussianRational as GR
from checker_support.outcome import Outcome

Table = tuple[tuple[GR, ...], ...]
Gauge = tuple[tuple[GR, ...], tuple[GR, ...]]


def exact_rational(value: object) -> Fraction:
    return rational(value, "counting parameter")


def cycle_count(n: object) -> Fraction:
    value = exact_rational(n)
    return rational((value-1)*(value-1), "cycle count")


def constraint_count(n: object) -> Fraction:
    value = exact_rational(n)
    return rational(value*(value-1)/2, "constraint count")


def cp_count(n: object) -> Fraction:
    value = exact_rational(n)
    return rational((value-1)*(value-2)/2, "CP count")


def _gaussian(value: object, nonzero: bool = False) -> GR:
    if type(value) is not GR:
        raise Violation("input", "exact GaussianRational label required")
    if nonzero and value == GR(0):
        raise Violation("input", "rephasing labels must be nonzero")
    return value


def quartet(a: object, b: object, c: object, d: object) -> GR:
    first, second, third, fourth = (_gaussian(value) for value in (a, b, c, d))
    return first.mul(second).mul(third.conj().mul(fourth.conj()))


def _gauges(values: object, length: int) -> tuple[GR, ...]:
    return tuple(_gaussian(value, True) for value in sequence(values, "gauge labels", length, 64))


@dataclass(frozen=True, slots=True, init=False)
class GaussianRephasingTable:
    """Aggregate owning a nonempty rectangular table of nonzero Q(i) values."""
    cells: Table

    def __init__(self, matrix: object) -> None:
        outer = sequence(matrix, "Gaussian table", maximum=64)
        if not outer:
            raise Violation("input", "a base row is required")
        first = sequence(outer[0], "Gaussian row", maximum=64)
        if not first:
            raise Violation("input", "a base column is required")
        owned = tuple(tuple(_gaussian(value, True) for value in sequence(row, "Gaussian row", len(first), 64))
                      for row in outer)
        object.__setattr__(self, "cells", owned)

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.cells), len(self.cells[0])

    def _normalized(self) -> GaussianRephasingTable:
        corner = self.cells[0][0]
        return GaussianRephasingTable(tuple(tuple(entry.mul(corner).div(row[0].mul(self.cells[0][j]))
                                                 for j, entry in enumerate(row)) for row in self.cells))

    def normalized(self) -> Outcome[GaussianRephasingTable]:
        return evaluate(self._normalized)

    def _act(self, rows: object, cols: object) -> GaussianRephasingTable:
        height, width = self.shape
        row_gauge, col_gauge = _gauges(rows, height), _gauges(cols, width)
        return GaussianRephasingTable(tuple(tuple(row_gauge[i].mul(value).div(col_gauge[j])
                                                 for j, value in enumerate(row)) for i, row in enumerate(self.cells)))

    def act(self, rows: object, cols: object) -> Outcome[GaussianRephasingTable]:
        return evaluate(self._act, rows, cols)

    def _witness(self, right: object) -> Gauge | None:
        if type(right) is not GaussianRephasingTable or self.shape != right.shape:
            raise Violation("input", "rephasing requires tables of the same shape")
        if self._normalized() != right._normalized():
            return None
        rows = tuple(b[0].div(a[0]) for a, b in zip(self.cells, right.cells))
        cols = tuple(a.div(self.cells[0][0]).div(b.div(right.cells[0][0]))
                     for a, b in zip(self.cells[0], right.cells[0]))
        return rows, cols

    def witness(self, right: object) -> Outcome[Gauge | None]:
        return evaluate(self._witness, right)


def shape(matrix: object) -> tuple[int, int]:
    return GaussianRephasingTable(matrix).shape


def normalize(matrix: object) -> Table:
    return GaussianRephasingTable(matrix)._normalized().cells


def act(matrix: object, rows: object, cols: object) -> Table:
    return GaussianRephasingTable(matrix)._act(rows, cols).cells


def witness(left: object, right: object) -> Gauge | None:
    return GaussianRephasingTable(left)._witness(GaussianRephasingTable(right))


def _sign_shape(height: object, width: object) -> tuple[int, int]:
    rows = integer(height, "table height", 1, 6)
    cols = integer(width, "table width", 1, 6)
    if rows*cols > 6:
        raise Violation("resource", "sign enumeration is bounded to6 cells")
    return rows, cols


def sign_tables(height: object, width: object) -> list[Table]:
    rows, cols = _sign_shape(height, width)
    return [tuple(tuple(GR(bits[i*cols+j]) for j in range(cols)) for i in range(rows))
            for bits in product((-1, 1), repeat=rows*cols)]


def _cases(cases: Cases | None) -> Cases:
    if cases is None:
        return Cases()
    if type(cases) is not Cases:
        raise Violation("input", "a Cases recorder is required")
    return cases


def check_canonical(table: object, cases: Cases | None = None) -> Table:
    cases = _cases(cases)
    norm = normalize(table)
    cases.require(normalize(norm) == norm, "normalization is idempotent")
    cases.require(all(x == GR(1) for x in norm[0]) and all(row[0] == GR(1) for row in norm), "canonical boundary is one")
    return norm


def check_sign_actions(table: object, height: object, width: object, cases: Cases | None = None) -> int:
    cases = _cases(cases)
    rows, cols = _sign_shape(height, width)
    owned = GaussianRephasingTable(table)
    if owned.shape != (rows, cols):
        raise Violation("input", "enumeration dimensions differ from table")
    norm = owned._normalized()
    checked = 0
    for scalars in product((-1, 1), repeat=rows+cols):
        row_gauge = tuple(GR(x) for x in scalars[:rows])
        col_gauge = tuple(GR(x) for x in scalars[rows:])
        cases.require(owned._act(row_gauge, col_gauge)._normalized() == norm, "rephasing preserves canonical coordinates")
        checked += 1
    return checked


def check_pair(table: object, other: object, cases: Cases | None = None) -> None:
    cases = _cases(cases)
    left, right = GaussianRephasingTable(table), GaussianRephasingTable(other)
    result = left._witness(right)
    cases.require(result is None or left._act(*result) == right, "computed equivalence witness is sound")
    cases.require((result is not None) == (left._normalized() == right._normalized()), "decision and invariant agree")


def check_nonreal(cases: Cases | None = None) -> None:
    cases = _cases(cases)
    table = ((GR(1, 1), GR(2, -1)), (GR(Fraction(1, 3), 2), GR(-1, 3)))
    rows, cols = (GR(0, 1), GR(2)), (GR(1, -1), GR(Fraction(2, 3)))
    other = act(table, rows, cols)
    reconstructed = witness(table, other)
    cases.require(reconstructed is not None and act(table, *reconstructed) == other, "Gaussian-rational reconstruction")
    separated = (other[0], (other[1][0], other[1][1].mul(GR(2))))
    cases.require(witness(table, separated) is None, "different cross ratio is separated")


def check_rephasing(cases: Cases | None = None) -> None:
    cases = _cases(cases)
    transformations = comparisons = 0
    orbit_counts: list[int] = []
    for height, width in ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3)):
        tables = sign_tables(height, width)
        canonical: set[Table] = set()
        for table in tables:
            canonical.add(check_canonical(table, cases))
            transformations += check_sign_actions(table, height, width, cases)
            for other in tables:
                check_pair(table, other, cases)
                comparisons += 1
        cases.require(len(canonical) == 2**((height-1)*(width-1)), "independent-coordinate count")
        orbit_counts.append(len(canonical))
    check_nonreal(cases)
    print(f"rephasing: {transformations} sign actions, {comparisons} pair decisions; orbits {orbit_counts}")


def check_invalid_inputs(cases: Cases | None = None) -> None:
    cases = _cases(cases)
    actions: tuple[Callable[[], object], ...] = (
        lambda: exact_rational(True), lambda: exact_rational(0.5), lambda: exact_rational("1"),
        lambda: GR(0).inv(), lambda: shape(()), lambda: shape(((),)),
        lambda: shape(((GR(1),), (GR(1), GR(1)))), lambda: shape(((GR(0),),)),
        lambda: act(((GR(1),),), (), (GR(1),)),
        lambda: act(((GR(1),),), (GR(0),), (GR(1),)),
        lambda: witness(((GR(1),),), ((GR(1), GR(1)),)))
    for action in actions:
        result = evaluate(action)
        cases.require(result.error is not None and result.error.kind == "input", "invalid-domain input refused")


def check_counting_examples(cases: Cases | None=None) -> None:
    cases = _cases(cases)
    samples = (Fraction(0), Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5), Fraction(-1), Fraction(3, 2), Fraction(7, 5))
    for sample in samples:
        cases.require(not cycle_count(sample) - constraint_count(sample) != cp_count(sample), f'difference failed at {sample}')
        cases.require(not cp_count(sample) + (sample - 1) != constraint_count(sample), f'constraint sum failed at {sample}')
    table = {1: (0, 0), 2: (1, 0), 3: (4, 1), 4: (9, 3)}
    for n, (cyc, cp) in table.items():
        cases.require(not (cycle_count(n) != cyc or cp_count(n) != cp), f'table failed at {n}')
    cases.require(not cycle_count(1) != cp_count(1), 'n=1 should agree')
    for n in (2, 3, 4):
        cases.require(not cycle_count(n) == cp_count(n), f'n={n} should differ')
    cases.require(not constraint_count(3) != 3, 'constraint count at 3')
    cases.require(not cycle_count(3) - constraint_count(3) != 1, '4 - 3')


def check_quartet_examples(cases: Cases | None=None) -> None:
    cases = _cases(cases)
    one = GR(1, 0)
    eye = GR(0, 1)
    q_real = quartet(one, one, one, one)
    q_imag = quartet(one, eye, one, one)
    cases.require(not (q_real != GR(1, 0) or q_imag != GR(0, 1)), f'quartets {q_real} {q_imag}')
    cases.require(not (q_real.im == cp_count(3) or q_imag.im != cp_count(3)), 'count match')
    cases.require(not q_real == q_imag, 'quartets should differ')


def main() -> None:
    cases = Cases()
    for check in (check_counting_examples, check_quartet_examples, check_rephasing, check_invalid_inputs):
        check(cases)
    print(json.dumps({"AuthorityEffect": "None", "status": "passed", "checks": cases.checks,
                      "scope": "Supplied nonzero Gaussian-label rephasing and rational identities only."}, indent=2))


if __name__ == "__main__":
    raise SystemExit(cli(main))
