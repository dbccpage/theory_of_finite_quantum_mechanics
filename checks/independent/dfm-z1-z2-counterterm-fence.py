"""Bounded exact Dirac kernels and the supplied lowered vertex contraction.

AuthorityEffect: None. Minkowski signature(+---), immutable Gaussian entries.
No loop integral, regularization prescription or counterterm ratio is computed.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path as _Path
import sys as _sys

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import integer, rational, sequence
from checker_support.gaussian_rational import GaussianRational as G
from checker_support.outcome import Outcome

Matrix = tuple[tuple[G, ...], ...]
Momentum = tuple[Q, Q, Q, Q]
ETA = (Q(1), Q(-1), Q(-1), Q(-1))


def _matrix(value: object) -> Matrix:
    rows = tuple(sequence(row, "Dirac row", 4) for row in sequence(value, "Dirac matrix", 4))
    return tuple(tuple(_entry(entry) for entry in row) for row in rows)


def _entry(value: object) -> G:
    if type(value) is not G:
        raise Violation("input", "Dirac entries require GaussianRational")
    return value


def _momentum(value: object) -> Momentum:
    t, x, y, z = sequence(value, "four-momentum", 4)
    return rational(t), rational(x), rational(y), rational(z)


def _index(value: object) -> int:
    direction = integer(value, "Lorentz index", 0)
    if direction > 3:
        raise Violation("input", "Lorentz index must be0..3")
    return direction


def zero_matrix() -> Matrix:
    return tuple(tuple(G(0) for _ in range(4)) for _ in range(4))


def eye() -> Matrix:
    return tuple(tuple(G(int(row == column)) for column in range(4)) for row in range(4))


def _gamma(direction: int) -> Matrix:
    if direction == 0:
        return tuple(tuple(G((1 if row < 2 else -1) if row == column else 0) for column in range(4)) for row in range(4))
    pauli = (((G(0), G(1)), (G(1), G(0))), ((G(0), G(0, -1)), (G(0, 1), G(0))),
             ((G(1), G(0)), (G(0), G(-1))))[direction-1]
    rows = [[G(0) for _ in range(4)] for _ in range(4)]
    for row, column in product(range(2), repeat=2):
        rows[row][column+2] = pauli[row][column]
        rows[row+2][column] = G(-1)*pauli[row][column]
    return tuple(tuple(row) for row in rows)


GAMMAS = tuple(_gamma(direction) for direction in range(4))


def _combine(left: Matrix, right: Matrix, sign: int) -> Matrix:
    factor = G(sign)
    return tuple(tuple(a+factor*b for a, b in zip(row, other)) for row, other in zip(left, right))


def madd(left: object, right: object) -> Matrix:
    return _combine(_matrix(left), _matrix(right), 1)


def msub(left: object, right: object) -> Matrix:
    return _combine(_matrix(left), _matrix(right), -1)


def _scale(scalar: Q, matrix: Matrix) -> Matrix:
    factor = G(scalar)
    return tuple(tuple(factor*entry for entry in row) for row in matrix)


def mscale(scalar: object, matrix: object) -> Matrix:
    return _scale(rational(scalar), _matrix(matrix))


def _dot(row: tuple[G, ...], column: tuple[G, ...]) -> G:
    value = G(0)
    for first, second in zip(row, column):
        value = value+first*second
    return value


def _multiply(left: Matrix, right: Matrix) -> Matrix:
    columns = tuple(zip(*right))
    return tuple(tuple(_dot(row, column) for column in columns) for row in left)


def mmul(left: object, right: object) -> Matrix:
    return _multiply(_matrix(left), _matrix(right))


def _slash(momentum: Momentum) -> Matrix:
    value = zero_matrix()
    for component, metric, gamma in zip(momentum, ETA, GAMMAS):
        value = _combine(value, _scale(component*metric, gamma), 1)
    return value


def slash(momentum: object) -> Matrix:
    return _slash(_momentum(momentum))


@dataclass(frozen=True, slots=True, init=False)
class DiracKernel:
    """Owns exact momentum and mass; a propagator additionally requires off-shell data."""
    momentum: Momentum
    mass: Q

    def __init__(self, momentum: object, mass: object) -> None:
        owned = _momentum(momentum)
        admitted_mass = rational(mass, "mass")
        object.__setattr__(self, "momentum", owned)
        object.__setattr__(self, "mass", admitted_mass)

    def _inverse_operator(self) -> Matrix:
        return _combine(_slash(self.momentum), _scale(self.mass, eye()), -1)

    def inverse_operator(self) -> Outcome[Matrix]:
        return evaluate(self._inverse_operator)

    def _denominator(self) -> Q:
        value = Q(0)
        for component, sign in zip(self.momentum+(self.mass,), ETA+(Q(-1),)):
            square = rational(component*component, "mass-shell square")
            value = rational(value+sign*square, "mass-shell prefix")
        if value == 0:
            raise Violation("input", "singular propagator")
        return value

    def _propagator(self) -> Matrix:
        denominator = self._denominator()
        numerator = _combine(_slash(self.momentum), _scale(self.mass, eye()), 1)
        return _scale(Q(1)/denominator, numerator)

    def propagator(self) -> Outcome[Matrix]:
        return evaluate(self._propagator)


def prop_inv(momentum: object, mass: object) -> Matrix:
    return DiracKernel(momentum, mass)._inverse_operator()


def prop(momentum: object, mass: object) -> Matrix:
    return DiracKernel(momentum, mass)._propagator()


def _dirac(matrix: Matrix) -> Matrix:
    total = zero_matrix()
    for sign, gamma in zip(ETA, GAMMAS):
        total = _combine(total, _multiply(gamma, _multiply(matrix, _scale(sign, gamma))), 1)
    return total


def dirac(matrix: object) -> Matrix:
    return _dirac(_matrix(matrix))


def _vertex(direction: int, left: Matrix, right: Matrix) -> Matrix:
    return _dirac(_multiply(left, _multiply(GAMMAS[direction], right)))


def vertex(direction: object, left: object, right: object) -> Matrix:
    return _vertex(_index(direction), _matrix(left), _matrix(right))


def contract(momentum: object, left: object, right: object) -> Matrix:
    vector, first, second = _momentum(momentum), _matrix(left), _matrix(right)
    total = zero_matrix()
    for direction, (component, sign) in enumerate(zip(vector, ETA)):
        total = _combine(total, _scale(component*sign, _vertex(direction, first, second)), 1)
    return total


def _basis_controls(cases: Cases) -> None:
    for mu, nu in product(range(4), repeat=2):
        actual = madd(mmul(GAMMAS[mu], GAMMAS[nu]), mmul(GAMMAS[nu], GAMMAS[mu]))
        expected = mscale(2*ETA[mu] if mu == nu else 0, eye())
        cases.require(actual == expected, "Minkowski Clifford pair")


def _inverse_difference(p: Momentum, q: Momentum, mass: Q, cases: Cases) -> None:
    shifted = tuple(rational(a+b) for a, b in zip(p, q))
    cases.require(msub(prop_inv(shifted, mass), prop_inv(p, mass)) == slash(q), "inverse difference")


def verify(cases: Cases) -> None:
    if type(cases) is not Cases:
        raise Violation("input", "Cases recorder required")
    _basis_controls(cases)
    p, q, mass = _momentum((2, 0, 0, 0)), _momentum((1, 0, 0, 1)), Q(1)
    _inverse_difference(p, q, mass, cases)
    _inverse_difference(_momentum((4, -1, 2, 3)), _momentum((-2, 5, 0, 1)), Q(6), cases)
    shifted = tuple(a+b for a, b in zip(p, q))
    first, second = prop(p, mass), prop(shifted, mass)
    for momentum, propagator in ((p, first), (shifted, second)):
        inverse = prop_inv(momentum, mass)
        cases.require(mmul(inverse, propagator) == eye(), "left inverse")
        cases.require(mmul(propagator, inverse) == eye(), "right inverse")
    cases.require(mmul(second, mmul(slash(q), first)) == msub(first, second), "sandwich")
    contracted = contract(q, second, first)
    cases.require(contracted == msub(dirac(first), dirac(second)), "lowered contraction")
    expected = ((Q(2, 7), 0, Q(-2, 7), 0), (0, Q(2, 7), 0, Q(2, 7)),
                (Q(2, 7), 0, Q(26, 21), 0), (0, Q(-2, 7), 0, Q(26, 21)))
    cases.require(contracted == tuple(tuple(G(value) for value in row) for row in expected), "witness entries")


def main() -> None:
    cases = Cases()
    verify(cases)
    print(json.dumps({"status": "passed", "checks": cases.checks,
                      "scope": "exact finite Dirac contraction; Z1/Z2 not computed"}))


if __name__ == "__main__":
    raise SystemExit(cli(main))
