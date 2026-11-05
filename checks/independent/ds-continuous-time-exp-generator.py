"""Owned finite maps, order-four matrices and exact finite boundary witnesses.

AuthorityEffect: None. No real time, exponential, logarithm, measure or U(1) fiber is built.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
import json
from pathlib import Path as _Path
import sys as _sys

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import integer, sequence
from checker_support.gaussian_matrix2 import GaussianMatrix2
from checker_support.gaussian_rational import GaussianRational as G
from checker_support.outcome import Outcome
from checker_support.rational_matrix import RationalMatrix

Pair = tuple[int, int]
Flat = tuple[Pair, Pair, Pair, Pair]
SCALED: Flat = ((1, 1), (1, -1), (1, -1), (1, 1))
NEGATIVE: Flat = ((-1, -1), (-1, 1), (-1, 1), (-1, -1))
FOUR_SWAP: Flat = ((0, 0), (4, 0), (4, 0), (0, 0))
RealFlat = tuple[int, int, int, int]
EYE: RealFlat = (1, 0, 0, 1)
JAY: RealFlat = (0, -1, 1, 0)
JAY2: RealFlat = (-1, 0, 0, -1)
JAY3: RealFlat = (0, 1, -1, 0)
REPS: tuple[RealFlat, ...] = (EYE, JAY, JAY2, JAY3)


def _state(value: object, size: int) -> int:
    state = integer(value, "finite state", 0)
    if state >= size:
        raise Violation("input", "state outside finite carrier")
    return state


@dataclass(frozen=True, slots=True, init=False)
class FiniteEndomap:
    """Owned total map of the indexed carrier0..N-1, N=1..4; roots enumerate all N^N maps."""
    images: tuple[int, ...]

    def __init__(self, images: object) -> None:
        values = sequence(images, "endomap images", maximum=4)
        if not values:
            raise Violation("input", "finite carrier must be nonempty")
        owned = tuple(_state(value, len(values)) for value in values)
        object.__setattr__(self, "images", owned)

    def apply(self, state: object) -> Outcome[int]:
        return evaluate(lambda: self.images[_state(state, len(self.images))])

    def _compose(self, other: object) -> FiniteEndomap:
        if type(other) is not FiniteEndomap or len(other.images) != len(self.images):
            raise Violation("input", "composition requires an endomap of the same carrier")
        return FiniteEndomap(tuple(self.images[value] for value in other.images))

    def compose(self, other: object) -> Outcome[FiniteEndomap]:
        return evaluate(self._compose, other)

    def _power(self, exponent: object) -> FiniteEndomap:
        remaining = integer(exponent, "iterate exponent", 0, 4096)
        value, power = FiniteEndomap(tuple(range(len(self.images)))), self
        while remaining:
            if remaining & 1:
                value = power._compose(value)
            remaining >>= 1
            if remaining:
                power = power._compose(power)
        return value

    def power(self, exponent: object) -> Outcome[FiniteEndomap]:
        return evaluate(self._power, exponent)

    def _square_roots(self) -> tuple[FiniteEndomap, ...]:
        roots = []
        for images in product(range(len(self.images)), repeat=len(self.images)):
            candidate = FiniteEndomap(images)
            if candidate._compose(candidate).images == self.images:
                roots.append(candidate)
        return tuple(roots)

    def square_roots(self) -> Outcome[tuple[FiniteEndomap, ...]]:
        return evaluate(self._square_roots)


def toggle(value: object) -> bool:
    if type(value) is not bool:
        raise Violation("input", "Boolean toggle requires bool")
    return not value


def maps() -> tuple[FiniteEndomap, ...]:
    return tuple(FiniteEndomap(images) for images in product(range(2), repeat=2))


def _bounded(value: object) -> int:
    exact = integer(value, "exact integer")
    if exact.bit_length() > 4096:
        raise Violation("resource", "integer exceeds4096 bits")
    return exact


def _gaussian(value: object) -> G:
    real, imaginary = sequence(value, "Gaussian integer pair", 2)
    return G(_bounded(real), _bounded(imaginary))


def _pair(value: G) -> Pair:
    """Internal export: all admitted arithmetic inputs here are Gaussian integers."""
    return value.re.numerator, value.im.numerator


def gadd(left: object, right: object) -> Pair:
    return _pair(_gaussian(left)+_gaussian(right))


def gmul(left: object, right: object) -> Pair:
    return _pair(_gaussian(left)*_gaussian(right))


def _matrix(value: object) -> GaussianMatrix2:
    a, b, c, d = sequence(value, "flat Gaussian matrix", 4)
    return GaussianMatrix2(_gaussian(a), _gaussian(b), _gaussian(c), _gaussian(d))


def mmul(left: object, right: object) -> Flat:
    result = _matrix(left).mul(_matrix(right))
    return _pair(result.a11), _pair(result.a12), _pair(result.a21), _pair(result.a22)


def cayley(parameter: object) -> bool:
    value = _bounded(parameter)
    square = _bounded(value*value)
    minus, plus = _bounded(1-square), _bounded(1+square)
    left = _bounded(_bounded(minus*minus)+_bounded(4*square))
    right = _bounded(plus*plus)
    return left == right


def energy(branch: object) -> int:
    return _bounded(2*_bounded(branch)+1)


def nilpotent(a: object, b: object, c: object, d: object) -> bool:
    value = RationalMatrix(((_bounded(a), _bounded(b)), (_bounded(c), _bounded(d))))
    swap = RationalMatrix(((0, 1), (1, 0)))
    zero = RationalMatrix(((0, 0), (0, 0)))
    return value.add(RationalMatrix.eye(2)).rows == swap.rows and value.mul(value).rows == zero.rows


def _real_matrix(value: object) -> RationalMatrix:
    a, b, c, d = sequence(value, "flat integer matrix", 4)
    return RationalMatrix(((_bounded(a), _bounded(b)), (_bounded(c), _bounded(d))))


def _real_flat(matrix: RationalMatrix) -> RealFlat:
    rows = matrix.require_shape(2, 2).integer_rows()
    return rows[0][0], rows[0][1], rows[1][0], rows[1][1]


def mm(left: object, right: object) -> RealFlat:
    first, second = _real_matrix(left), _real_matrix(right)
    return _real_flat(first.mul(second))


def powj(exponent: object) -> RealFlat:
    """Actual binary matrix multiplication, independent of the residue lookup table."""
    remaining = integer(exponent, "quarter-turn exponent", 0, 4096)
    value, power = RationalMatrix.eye(2), _real_matrix(JAY)
    while remaining:
        if remaining & 1:
            value = value.mul(power)
        remaining >>= 1
        if remaining:
            power = power.mul(power)
    return _real_flat(value)


def verify_residues(cases: Cases) -> None:
    if type(cases) is not Cases:
        raise Violation("input", "Cases recorder required")
    cases.require(mm(JAY, JAY) == JAY2, "quarter-turn square")
    cases.require(mm(JAY2, JAY) == JAY3, "quarter-turn cube")
    cases.require(mm(JAY3, JAY) == EYE, "quarter-turn fourth")
    for representative in REPS[1:]:
        cases.require(representative != EYE, "nonidentity representative")
    cases.require(mm(JAY, JAY)[0] == -1, "square diagonal")
    cases.require(mm(JAY2, JAY2)[0] == 1, "fourth diagonal")
    for exponent, residue in ((0, 0), (1, 1), (2, 2), (3, 3), (4, 0)):
        cases.require(exponent % 4 == residue, "literal residue")
    for exponent, expected in enumerate((JAY, JAY2, JAY3, EYE), 1):
        cases.require(powj(exponent) == expected, "first powers")
    for exponent in range(40):
        residue = exponent % 4
        cases.require((exponent+4) % 4 == residue, "residue period")
        cases.require((exponent+1) % 4 == (residue+1) % 4, "residue successor")
        cases.require(powj(exponent) == REPS[residue], "power representative")
        cases.require((powj(exponent) == EYE) == (residue == 0), "identity iff zero residue")
        cases.require(powj(exponent+4) == powj(exponent), "matrix power period")
        cases.require(mm(REPS[residue], JAY) == REPS[(residue+1) % 4], "representative step")


def _map_controls(cases: Cases) -> None:
    cases.require(toggle(False) is True, "toggle false")
    cases.require(toggle(True) is False, "toggle true")
    cases.require(FiniteEndomap((1, 0))._square_roots() == (), "no Boolean toggle square root")


def _matrix_controls(cases: Cases) -> None:
    cases.require(mmul(SCALED, SCALED) == FOUR_SWAP, "scaled root square")
    cases.require(mmul(NEGATIVE, NEGATIVE) == FOUR_SWAP, "negative root square")
    cases.require(SCALED != NEGATIVE, "distinct roots")
    four_identity = GaussianMatrix2(G(4), G(0), G(0), G(4))
    for value in (SCALED, NEGATIVE):
        matrix = _matrix(value)
        cases.require(matrix.adjoint().mul(matrix) == four_identity, "scaled unitarity")
    cases.require(gadd((2, 3), (5, 7)) == (7, 10), "Gaussian addition")
    cases.require(gmul((1, 1), (1, -1)) == (2, 0), "Gaussian multiplication")


def verify(cases: Cases) -> None:
    if type(cases) is not Cases:
        raise Violation("input", "Cases recorder required")
    _map_controls(cases)
    _matrix_controls(cases)
    for parameter in range(-20, 21):
        cases.require(cayley(parameter), "Cayley polynomial")
    cases.require(energy(0) == 1, "branch zero")
    cases.require(energy(1) == 3, "branch one")
    for first, second in combinations(range(-12, 13), 2):
        cases.require(energy(first) != energy(second), "distinct branch energies")
    candidate = RationalMatrix(((-1, 1), (1, -1)))
    cases.require(candidate.mul(candidate).rows[0][0] == 2, "forced candidate corner")
    cases.require(not nilpotent(-1, 1, 1, -1), "absent square-zero logarithm candidate")


def main() -> None:
    cases = Cases()
    verify(cases)
    first = cases.checks
    verify_residues(cases)
    print(json.dumps({"status": "passed", "checks": cases.checks, "Boolean_maps": len(maps()),
                      "root_and_branch": first, "residues": cases.checks-first,
                      "scope": "finite root, branch and order-four witnesses; no continuous-time generator or U(1) fiber"}))


if __name__ == "__main__":
    raise SystemExit(cli(main))
