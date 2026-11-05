"""Bounded finite forests and supplied commuting rational-projector reductions.

AuthorityEffect: None. No Feynman integrand, positive-degree subtraction or
continuum convergence is constructed. Expected failures use the Railway boundary.
"""
from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import chain, combinations, product
import json
from pathlib import Path as _Path
import sys as _sys

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import integer, rational, sequence
from checker_support.outcome import Outcome
from checker_support.rational_matrix import RationalMatrix, Flat2

Matrix = Flat2
IDENTITY: Matrix = (Q(1), Q(0), Q(0), Q(1))
ZERO: Matrix = (Q(0), Q(0), Q(0), Q(0))
OVERLAP = {"L": frozenset({0, 1, 2}), "R": frozenset({2, 3, 4}), "G": frozenset(range(5))}
NEST = {"inner": frozenset({0, 1}), "outer": frozenset(range(4))}


def _label(value: object) -> str:
    if type(value) is not str or not value.strip():
        raise Violation("input", "forest labels must be nonempty strings")
    integer(len(value), "label characters", 1, 64)
    return value


def _names(value: object) -> tuple[str, ...]:
    names = tuple(_label(item) for item in sequence(value, "forest labels", maximum=12))
    if len(set(names)) != len(names):
        raise Violation("input", "forest labels must be distinct")
    return names


def _edge_map(value: object) -> dict[str, frozenset[int]]:
    if type(value) is not dict:
        raise Violation("input", "forest edges must be a dict")
    integer(len(value), "edge-set labels", 0, 12)
    owned: dict[str, frozenset[int]] = {}
    for key, carrier in value.items():
        name = _label(key)
        if type(carrier) is not frozenset:
            raise Violation("input", "edge carriers must be frozensets")
        integer(len(carrier), "edge carrier size", 0, 64)
        owned[name] = frozenset(integer(edge, "edge index", 0, 4095) for edge in carrier)
    return owned


def powerset(items: object) -> Iterator[tuple[str, ...]]:
    pool = _names(items)
    return chain.from_iterable(combinations(pool, size) for size in range(len(pool)+1))


def compatible(edges: object) -> Callable[[object, object], bool]:
    """Own the entire bounded mapping, including entries unused by a later query."""
    owned = _edge_map(edges)
    def ok(left: object, right: object) -> bool:
        a, b = _label(left), _label(right)
        if a not in owned or b not in owned:
            raise Violation("input", "unknown forest label")
        ea, eb = owned[a], owned[b]
        return ea <= eb or eb <= ea or ea.isdisjoint(eb)
    return ok


def forests(names: object, edges: object) -> list[tuple[str, ...]]:
    labels = _names(names)
    ok = compatible(edges)
    for label in labels:
        ok(label, label)
    return [subset for subset in powerset(labels)
            if all(ok(a, b) for a, b in combinations(subset, 2))]


def exact(value: object) -> Q:
    return rational(value, "scalar")


def N(x: object, y: object) -> Q:
    a, b = exact(x), exact(y)
    return exact(2 + 3*a + 5*b + 7*a*b)


def six(x: object, y: object) -> Q:
    a, b = exact(x), exact(y)
    return exact(N(a, b) - N(0, b) - N(a, 0) - N(0, 0) + N(0, 0) + N(0, 0))


def inclusion(x: object, y: object) -> Q:
    a, b = exact(x), exact(y)
    return exact(N(a, b) - N(0, b) - N(a, 0) + N(0, 0))


def sector_k(z: object, lam: object) -> Q:
    z, lam = exact(z), exact(lam)
    if lam in (0, -1):
        raise Violation("input", "sector denominator vanishes")
    return exact((1 + z*lam)/(lam*(1+lam)))


def multiply(a: object, b: object) -> Matrix:
    return RationalMatrix.from_flat2(a).mul(RationalMatrix.from_flat2(b)).flat2()


def residual(p: object) -> Matrix:
    return RationalMatrix.eye(2).add(RationalMatrix.from_flat2(p).neg()).flat2()


def _projector(value: object) -> RationalMatrix:
    entries = sequence(value, "2x2 projector", 4)
    if any(type(x) is not Q for x in entries):
        raise Violation("input", "projectors require exact Fraction entries")
    result = RationalMatrix.from_flat2(entries)
    if result.mul(result) != result:
        raise Violation("input", "non-idempotent projector")
    return result


@dataclass(frozen=True, slots=True, init=False)
class CommutingProjectorFamily:
    """Aggregate owning <=64 rational2x2 idempotents and their commutation invariant."""
    projectors: tuple[RationalMatrix, ...]

    def __init__(self, projectors: object) -> None:
        owned = tuple(_projector(p) for p in sequence(projectors, "projector family", maximum=64))
        for p, q in combinations(owned, 2):
            if p.mul(q) != q.mul(p):
                raise Violation("input", "noncommuting projectors")
        object.__setattr__(self, "projectors", owned)

    def _reduction(self) -> RationalMatrix:
        result = RationalMatrix.eye(2)
        for projector in reversed(self.projectors):
            result = RationalMatrix.eye(2).add(projector.neg()).mul(result)
        return result

    def reduction(self) -> Outcome[RationalMatrix]:
        return evaluate(self._reduction)

    def _apply(self, vector: object) -> tuple[Q, Q]:
        x, y = sequence(vector, "rational two-vector", 2)
        result = self._reduction().mul(RationalMatrix(((x,), (y,))))
        return result.rows[0][0], result.rows[1][0]

    def apply(self, vector: object) -> Outcome[tuple[Q, Q]]:
        return evaluate(self._apply, vector)


def checked_reduce(projectors: object) -> Matrix:
    return CommutingProjectorFamily(projectors)._reduction().flat2()


def _cases(cases: Cases | None) -> Cases:
    if cases is None:
        return Cases()
    if type(cases) is not Cases:
        raise Violation("input", "a Cases recorder is required")
    return cases


def check_family(family: object, cases: Cases | None = None) -> None:
    cases = _cases(cases)
    aggregate = CommutingProjectorFamily(family)
    result = aggregate._reduction().flat2()
    cases.require(multiply(result, result) == result, "reduction is idempotent")
    for projector in aggregate.projectors:
        p = projector.flat2()
        cases.require(multiply(p, result) == ZERO, "reduction lies in supplied kernel")
        cases.require(multiply(residual(p), result) == result, "subfamily absorbs reduction")
    if not aggregate.projectors:
        cases.require(result == IDENTITY, "empty subtraction is identity")


def check_projector_api(cases: Cases | None = None) -> None:
    cases = _cases(cases)
    matrices: list[Matrix] = [(Q(a), Q(b), Q(c), Q(d)) for a, b, c, d in product((-1, 0, 1), repeat=4)]
    projectors = [p for p in matrices if multiply(p, p) == p]
    checked = 0
    for size in range(3):
        for family in product(projectors, repeat=size):
            if all(multiply(p, q) == multiply(q, p) for p, q in combinations(family, 2)):
                check_family(family, cases)
                cases.require(checked_reduce(family+family) == checked_reduce(family), "repeated family changes no reduction")
                checked += 1
    bad: Matrix = (Q(2), Q(0), Q(0), Q(0))
    p: Matrix = (Q(1), Q(0), Q(0), Q(0))
    q: Matrix = (Q(1), Q(1), Q(0), Q(0))
    for family in ((bad,), (p, q)):
        cases.require(not evaluate(checked_reduce, family).ok, "invalid projector family refused")
    print(f"projectors: {len(projectors)} exact idempotents; {checked} compatible lists; two invalid families refused")


def check_invalid_scalars(cases: Cases | None = None) -> None:
    cases = _cases(cases)
    for value in (True, 0.5, "1"):
        cases.require(not evaluate(exact, value).ok, "inexact scalar refused")
    for pole in (Q(0), Q(-1)):
        cases.require(not evaluate(sector_k, 1, pole).ok, "sector pole refused")


def check_forest_carriers(cases: Cases | None=None) -> None:
    cases = _cases(cases)
    overlap = forests(('L', 'R', 'G'), OVERLAP)
    nest = forests(('inner', 'outer'), NEST)
    cases.require(not len(overlap) != 6, 'overlap forest count')
    cases.require(not (('L', 'R') in overlap or ('L', 'R', 'G') in overlap), 'overlapping pair was admitted')
    cases.require(not {('L', 'G'), ('R', 'G'), ('G',), ('L',), ('R',), ()} != set(overlap), 'overlap forest list')
    cases.require(not len(nest) != 4, 'nested forest count')
    cases.require(not 2 not in OVERLAP['L'] & OVERLAP['R'] & OVERLAP['G'], 'shared edge')


def check_numerator_examples(cases: Cases | None=None) -> None:
    cases = _cases(cases)
    constant = N(0, 0)
    x_coefficient = N(1, 0) - constant
    y_coefficient = N(0, 1) - constant
    mixed_coefficient = N(1, 1) - N(1, 0) - N(0, 1) + constant
    cases.require((constant, x_coefficient, y_coefficient, mixed_coefficient) == (Q(2), Q(3), Q(5), Q(7)), 'numerator finite-difference coefficients')
    samples = [Q(0), Q(1, 2), Q(-3), Q(4, 7), Q(5), Q(-2, 9)]
    for x in samples:
        for y in samples:
            cases.require(not (six(x, y) != 7 * x * y or inclusion(x, y) != 7 * x * y), f'identity failed at {x}, {y}')
            three = N(x, y) - N(0, y) - N(x, 0)
            cases.require(not three != 7 * x * y - 2, f'three-sum failed at {x}, {y}')
            if x * y != 0:
                cases.require(not six(x, y) / (x * y) != 7, f'quotient failed at {x}, {y}')
                cases.require(not three / (x * y) != 7 - 2 / (x * y), f'remainder failed at {x}, {y}')
    x, y = (Q(1, 2), Q(1, 3))
    cases.require(not six(x, y) != Q(7, 6), 'witness numerator')
    cases.require(not six(x, y) / (x * y) != 7, 'witness quotient')
    cases.require(not (N(x, y) - N(0, y) - N(x, 0)) / (x * y) != -5, 'witness remainder')


def check_sector_example(cases: Cases | None=None) -> None:
    cases = _cases(cases)
    z, lam1, lam2 = (Q(3, 5), Q(1, 2), Q(1, 3))
    sector = (sector_k(z, lam1) - sector_k(0, lam1)) * (sector_k(z, lam2) - sector_k(0, lam2))
    cases.require(not sector != Q(9, 50), 'sector value')
    cases.require(not (sector == 7 or z * z != Q(9, 25) or z * z == 7), 'sector comparison')


def main() -> None:
    cases = Cases()
    for check in (check_forest_carriers, check_numerator_examples, check_sector_example,
                  check_projector_api, check_invalid_scalars):
        check(cases)
    print(json.dumps({"AuthorityEffect": "None", "status": "passed", "checks": cases.checks,
                      "scope": "Finite forests, declared numerator and supplied commuting projectors only."}, indent=2))


if __name__ == "__main__":
    raise SystemExit(cli(main))
