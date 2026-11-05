"""Bounded exact weighted trace forms in the finite Gribov fence.

AuthorityEffect: None. No continuum operator, gauge fixing or Gribov region is
constructed. Shared independent arithmetic is checked by separate matrix oracles.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
import json
from pathlib import Path as _Path
import sys as _sys

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import rational, sequence
from checker_support.outcome import Outcome
from checker_support.rational_matrix import RationalMatrix, Rows


def exact(value: object) -> Q:
    return rational(value)


def _matrix(rows: object) -> RationalMatrix:
    outer = sequence(rows, "3x3 matrix", 3, 3)
    owned = tuple(sequence(row, "3x3 row", 3, 3) for row in outer)
    return RationalMatrix(owned)


def mat(rows: object) -> Rows:
    return _matrix(rows).rows


def mul(a: object, b: object) -> Rows:
    left, right = _matrix(a), _matrix(b)
    return left.mul(right).rows


def _trace(matrix: RationalMatrix) -> Q:
    total = Q(0)
    for index in range(3):
        total = rational(total + matrix.rows[index][index], "trace accumulation")
    return total


def trace(a: object) -> Q:
    return _trace(_matrix(a))


def diag(x: object, y: object, z: object) -> Rows:
    first, second, third = exact(x), exact(y), exact(z)
    return mat(((first, 0, 0), (0, second, 0), (0, 0, third)))


@dataclass(frozen=True, slots=True, init=False)
class TraceQuadraticForm:
    """Owns a rational3x3 weight; Q(H)=Tr(weight*H^2), without positivity claims."""
    weight: RationalMatrix

    def __init__(self, weight: object) -> None:
        object.__setattr__(self, "weight", _matrix(weight))

    def _on(self, generator: RationalMatrix) -> Q:
        return _trace(self.weight.mul(generator.mul(generator)))

    def _value(self, generator: object) -> Q:
        return self._on(_matrix(generator))

    def value(self, generator: object) -> Outcome[Q]:
        return evaluate(self._value, generator)

    def _difference(self, left: object, right: object) -> Q:
        first, second = _matrix(left), _matrix(right)
        return rational(self._on(first) - self._on(second), "form difference")

    def difference(self, left: object, right: object) -> Outcome[Q]:
        return evaluate(self._difference, left, right)


def run_checks(cases: Cases) -> None:
    if type(cases) is not Cases:
        raise Violation("input", "Cases recorder required")
    eye, omega = diag(1, 1, 1), diag(1, -1, -1)
    h23 = mat(((0, 0, 0), (0, 0, 1), (0, 1, 0)))
    h12 = mat(((0, 1, 0), (1, 0, 0), (0, 0, 0)))
    cases.require(mul(h23, h23) == diag(0, 1, 1), "H23 square")
    cases.require(mul(h12, h12) == diag(1, 1, 0), "H12 square")
    cases.require(mul(omega, omega) == eye, "weight involution")
    cases.require(omega[0][0]*omega[1][1]*omega[2][2] == 1, "diagonal determinant")
    cases.require(trace(eye) == 3, "identity trace")
    cases.require(trace(omega) == -1, "weight trace")
    positive, indefinite = TraceQuadraticForm(eye), TraceQuadraticForm(omega)
    cases.require(positive._value(h23) == 2, "identity form")
    cases.require(indefinite._value(h23) == -2, "H23 weighted form")
    cases.require(indefinite._value(h12) == 0, "H12 weighted form")
    cases.require(indefinite._difference(h23, h12) == -2, "forms differ")


def main() -> None:
    cases = Cases()
    run_checks(cases)
    print(json.dumps({"status": "passed", "checks": cases.checks,
                      "scope": "rational3x3 weighted trace forms; no continuum operator"}))


if __name__ == "__main__":
    raise SystemExit(cli(main))
