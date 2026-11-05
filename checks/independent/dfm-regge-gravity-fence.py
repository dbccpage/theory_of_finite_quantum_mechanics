"""Bounded exact cosine-law formulas and an independently supplied rational block.

AuthorityEffect: None. No deficit angle, hinge holonomy,4-simplex or continuum
gravity equation is constructed. The block parameter is not inferred from lengths.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
import json
from pathlib import Path as _Path
import sys as _sys

import sympy as sp

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import rational
from checker_support.outcome import Outcome
from checker_support.rational_matrix import RationalMatrix


def exact(value: object) -> Q:
    return rational(value)


def _numerator(a: Q, b: Q, c: Q) -> Q:
    aa, bb, cc = rational(a*a, "a square"), rational(b*b, "b square"), rational(c*c, "c square")
    return rational(rational(bb+cc, "square sum")-aa, "cosine numerator")


def cos_num(a: object, b: object, c: object) -> Q:
    first, second, third = exact(a), exact(b), exact(c)
    return _numerator(first, second, third)


def cos_law(a: object, b: object, c: object) -> Q:
    """Algebraic formula on signed rationals with bc!=0; no triangle admission."""
    first, second, third = exact(a), exact(b), exact(c)
    denominator = rational(2*rational(second*third, "side product"), "cosine denominator")
    if denominator == 0:
        raise Violation("input", "cosine-law denominator must be nonzero")
    return rational(_numerator(first, second, third)/denominator, "cosine-law value")


@dataclass(frozen=True, slots=True, init=False)
class CayleyBlock:
    """Owned rational parameter beta!=+-1; it is not a physical velocity input."""
    parameter: Q
    square: Q
    denominator: Q

    def __init__(self, beta: object) -> None:
        parameter = exact(beta)
        square = rational(parameter*parameter, "parameter square")
        denominator = rational(1-square, "block denominator")
        if denominator == 0:
            raise Violation("input", "block parameter must differ from plus/minus1")
        object.__setattr__(self, "parameter", parameter)
        object.__setattr__(self, "square", square)
        object.__setattr__(self, "denominator", denominator)

    def _gamma(self) -> Q:
        return rational(rational(1+self.square, "diagonal numerator")/self.denominator, "block diagonal")

    def _off_diagonal(self) -> Q:
        return rational(rational(2*self.parameter, "off-diagonal numerator")/self.denominator, "off-diagonal entry")

    def _matrix(self) -> RationalMatrix:
        diagonal, off = self._gamma(), self._off_diagonal()
        return RationalMatrix(((diagonal, off, 0, 0), (off, diagonal, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))

    def matrix(self) -> Outcome[RationalMatrix]:
        return evaluate(self._matrix)

    def _trace(self) -> Q:
        matrix = self._matrix()
        total = Q(0)
        for index in range(4):
            total = rational(total+matrix.rows[index][index], "block trace accumulation")
        return total

    def trace(self) -> Outcome[Q]:
        return evaluate(self._trace)


def gamma(beta: object) -> Q:
    return CayleyBlock(beta)._gamma()


def block_trace(beta: object) -> Q:
    return CayleyBlock(beta)._trace()


def _cases(cases: object) -> Cases:
    if type(cases) is not Cases:
        raise Violation("input", "Cases recorder required")
    return cases


def check_numerator_identity(cases: Cases) -> None:
    run = _cases(cases)
    a, b, c = sp.symbols("a b c")
    residual = ((b*b+c*c-a*a)+(a*a+c*c-b*b)+(a*a+b*b-c*c)-(a*a+b*b+c*c))
    run.require(sp.expand(residual) == 0, "symbolic numerator identity")
    samples = ((Q(3), Q(4), Q(5)), (Q(0), Q(0), Q(0)),
               (Q(-2), Q(7), Q(1, 3)), (Q(1, 2), Q(-3, 5), Q(8)))
    for first, second, third in samples:
        run.require(cos_num(first, second, third)+cos_num(second, first, third)+cos_num(third, first, second)
                    == first*first+second*second+third*third, "rational numerator sum")


def check_lengths(cases: Cases) -> Q:
    run = _cases(cases)
    triples = ((5, 3, 4), (3, 4, 5), (4, 3, 5))
    numerators = tuple(cos_num(*sides) for sides in triples)
    for actual, expected in zip(numerators, (0, 32, 18)):
        run.require(actual == expected, "3-4-5 numerator")
    run.require(sum(numerators) == 50, "numerator total")
    cosines = tuple(cos_law(*sides) for sides in triples)
    for actual_cosine, expected_cosine in zip(cosines, (Q(0), Q(4, 5), Q(3, 5))):
        run.require(actual_cosine == expected_cosine, "3-4-5 cosine")
    total = sum(cosines, Q(0))
    run.require(total == Q(7, 5), "cosine sum")
    return total


def check_block(cosine_sum: object, cases: Cases) -> None:
    run = _cases(cases)
    comparison = exact(cosine_sum)
    block = CayleyBlock(Q(1, 2))
    run.require(block.denominator == Q(3, 4), "block denominator")
    run.require(block._gamma() == Q(5, 3), "block diagonal")
    run.require(block._off_diagonal() == Q(4, 3), "block off-diagonal")
    trace = block._trace()
    run.require(trace == Q(16, 3), "block trace")
    run.require(trace != 4, "block trace differs from identity trace")
    run.require(trace != comparison, "block trace differs from cosine sum")


def main() -> None:
    run = Cases()
    check_numerator_identity(run)
    cosine_sum = check_lengths(run)
    check_block(cosine_sum, run)
    print(json.dumps({"status": "passed", "checks": run.checks,
                      "scope": "exact rational formulas and supplied block; no Regge complex or continuum equation"}))


if __name__ == "__main__":
    raise SystemExit(cli(main))
