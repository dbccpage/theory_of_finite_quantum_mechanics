"""Bounded integer Gram forms, scalar shares and rotation boundary controls.

AuthorityEffect: None. No channel, environment extension, density operator,
class-operator trace formula or physical normalization is selected.
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
from checker_support.domains import integer, sequence
from checker_support.outcome import Outcome

Rows = tuple[tuple[int, ...], ...]


def _bounded(value: object) -> int:
    number = integer(value, "Gram integer")
    if number.bit_length() > 4096:
        raise Violation("resource", "Gram integer exceeds4096 bits")
    return number


def _nonnegative(value: object) -> int:
    number = _bounded(value)
    if number < 0:
        raise Violation("input", "Gram scale must be nonnegative")
    return number


def _dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    """Internal equally sized admitted integer vectors, with each term/prefix bounded."""
    total = 0
    for first, second in zip(left, right):
        total = _bounded(total+_bounded(first*second))
    return total


def _denominator(value: object) -> int:
    denominator = _bounded(value)
    if denominator <= 0:
        raise Violation("input", "normalization denominator must be positive")
    return _bounded(denominator*denominator)


@dataclass(frozen=True, slots=True, init=False)
class IntegerGramForm:
    """Owns1..16 feature rows over1..16 coordinates; form is scale*A^T*A, scale>=0."""
    features: Rows
    scale: int

    def __init__(self, features: object, scale: object = 1) -> None:
        outer = sequence(features, "feature rows", maximum=16)
        if not outer:
            raise Violation("input", "at least one feature row required")
        first = sequence(outer[0], "feature row", maximum=16)
        if not first:
            raise Violation("input", "at least one coordinate required")
        rows = tuple(sequence(row, "feature row", len(first), 16) for row in outer)
        owned = tuple(tuple(_bounded(value) for value in row) for row in rows)
        admitted_scale = _nonnegative(scale)
        object.__setattr__(self, "features", owned)
        object.__setattr__(self, "scale", admitted_scale)

    @property
    def dimension(self) -> int:
        return len(self.features[0])

    def _vector(self, value: object) -> tuple[int, ...]:
        return tuple(_bounded(entry) for entry in sequence(value, "Gram vector", self.dimension, 16))

    def _coordinates(self, vector: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(_dot(row, vector) for row in self.features)

    def _bilinear(self, left: object, right: object) -> int:
        first, second = self._vector(left), self._vector(right)
        return _bounded(self.scale*_dot(self._coordinates(first), self._coordinates(second)))

    def bilinear(self, left: object, right: object) -> Outcome[int]:
        return evaluate(self._bilinear, left, right)

    def _quadratic(self, vector: object) -> int:
        coordinates = self._coordinates(self._vector(vector))
        return _bounded(self.scale*_dot(coordinates, coordinates))

    def quadratic(self, vector: object) -> Outcome[int]:
        return evaluate(self._quadratic, vector)

    def _gram(self) -> Rows:
        columns = tuple(zip(*self.features))
        return tuple(tuple(_bounded(self.scale*_dot(left, right)) for right in columns) for left in columns)

    def gram(self) -> Outcome[Rows]:
        return evaluate(self._gram)

    def _event(self, value: object) -> tuple[int, ...]:
        indices = tuple(integer(entry, "event index", 0) for entry in sequence(value, "event", maximum=16))
        if any(index >= self.dimension for index in indices):
            raise Violation("input", "event index outside coordinate carrier")
        if len(set(indices)) != len(indices):
            raise Violation("duplicate", "event indices must be distinct")
        return tuple(sorted(indices))

    def _event_weight(self, event: object, denominator: object) -> Q:
        indices = self._event(event)
        divisor = _denominator(denominator)
        selector = tuple(int(index in indices) for index in range(self.dimension))
        return Q(self._quadratic(selector), divisor)

    def event_weight(self, event: object, denominator: object = 1) -> Outcome[Q]:
        return evaluate(self._event_weight, event, denominator)

    def _diagonal_weight(self, denominator: object) -> Q:
        divisor = _denominator(denominator)
        total = 0
        for row in self.features:
            total = _bounded(total+_dot(row, row))
        return Q(_bounded(self.scale*total), divisor)

    def diagonal_weight(self, denominator: object = 1) -> Outcome[Q]:
        return evaluate(self._diagonal_weight, denominator)

    def _partition(self, values: object) -> tuple[tuple[int, ...], ...]:
        groups = tuple(self._event(group) for group in sequence(values, "partition", maximum=16))
        if not groups or any(not group for group in groups):
            raise Violation("input", "partition groups must be nonempty")
        flattened = tuple(index for group in groups for index in group)
        if len(set(flattened)) != len(flattened):
            raise Violation("duplicate", "partition groups overlap")
        if set(flattened) != set(range(self.dimension)):
            raise Violation("input", "partition must cover the coordinate carrier")
        return groups

    def _coarse_grained(self, partition: object) -> IntegerGramForm:
        groups = self._partition(partition)
        rows = tuple(tuple(_dot(tuple(row[index] for index in group), (1,)*len(group)) for group in groups) for row in self.features)
        return IntegerGramForm(rows, self.scale)

    def coarse_grained(self, partition: object) -> Outcome[IntegerGramForm]:
        return evaluate(self._coarse_grained, partition)


def off_diagonal_pairing(scale: object) -> int:
    value = _bounded(scale)
    vector = (1, -1)
    applied = tuple(_dot(row, vector) for row in ((0, value), (value, 0)))
    return _dot(vector, applied)


def nonnegative_product(first: object, second: object) -> int:
    left, right = _nonnegative(first), _nonnegative(second)
    return _bounded(left*right)


def _masses(values: tuple[int, ...], degree: int) -> tuple[int, ...]:
    return tuple(_bounded(value**degree) for value in values)


def _power_shares(amplitudes: object, exponent: object) -> tuple[Q, ...]:
    values = tuple(_bounded(value) for value in sequence(amplitudes, "amplitudes", maximum=16))
    degree = integer(exponent, "mass exponent")
    if degree not in (1, 2, 4):
        raise Violation("input", "mass exponent must be 1, 2 or 4")
    if not values:
        raise Violation("input", "at least one amplitude required")
    masses = _masses(values, degree)
    total = _dot(masses, (1,)*len(masses))
    if total == 0:
        raise Violation("input", "zero total has no normalized shares")
    return tuple(Q(mass, total) for mass in masses)


def power_shares(amplitudes: object, exponent: object) -> Outcome[tuple[Q, ...]]:
    """Explicit linear/quadratic/quartic algebraic shares; linear shares can be signed."""
    return evaluate(_power_shares, amplitudes, exponent)


def _rotation(amplitudes: object, coefficients: object) -> tuple[int, int]:
    a, b = tuple(_bounded(value) for value in sequence(amplitudes, "rotation pair", 2, 2))
    r, s = tuple(_bounded(value) for value in sequence(coefficients, "rotation coefficients", 2, 2))
    return _dot((r, -s), (a, b)), _dot((s, r), (a, b))


def rotation(amplitudes: object, coefficients: object) -> Outcome[tuple[int, int]]:
    """Apply the scaled rotation [[r,-s],[s,r]], without assuming unit norm."""
    return evaluate(_rotation, amplitudes, coefficients)


def _recorder(cases: object) -> Cases:
    if type(cases) is not Cases:
        raise Violation("input", "Cases recorder required")
    return cases


def verify_positivity(cases: Cases) -> None:
    run = _recorder(cases)
    for value in range(-30, 31):
        run.require(IntegerGramForm(((value,),))._quadratic((1,)) >= 0, "integer square")
    for value in range(-20, 21):
        run.require(_dot((-value,), (-value,)) == _dot((value,), (value,)), "negative square")
    for first, second in product(range(9), repeat=2):
        run.require(nonnegative_product(first, second) >= 0, "nonnegative product")
        run.require(nonnegative_product(first, second) == nonnegative_product(second, first), "product symmetry")
    for scale, x, w in product(range(6), range(-3, 4), range(-3, 4)):
        run.require(IntegerGramForm(((1, 1),), scale)._quadratic((x, w)) >= 0, "scaled Bell square")
    run.require(off_diagonal_pairing(1) == -2, "negative pairing")
    for scale in range(-8, 9):
        run.require(off_diagonal_pairing(scale) == -2*scale, "signed scaling")
        run.require(off_diagonal_pairing(scale) == 2*(-scale), "twice negative")
    for scale in range(1, 13):
        run.require(off_diagonal_pairing(scale) < 0, "strict negative pairing")
        run.require(-scale < 0, "negative scale sign")
    run.require(off_diagonal_pairing(0) == 0, "zero pairing")
    run.require(_dot((0, 1, -1, 0), (0, 1, -1, 0)) == 2, "witness norm")


def _normalization_controls(amplitudes: tuple[int, int], denominator: int, cases: Cases) -> None:
    form = IntegerGramForm((amplitudes,))
    diagonal, global_weight = form._diagonal_weight(denominator), form._event_weight((0, 1), denominator)
    expected_diagonal, expected_global = (Q(1, 2), Q(1)) if denominator == 2 else (Q(1), Q(49, 25))
    cases.require(_dot(amplitudes, (1, 1)) == (2 if denominator == 2 else 7), "class sum")
    cases.require(diagonal == expected_diagonal, "diagonal weight")
    cases.require(global_weight == expected_global, "global weight")
    cases.require(diagonal != global_weight, "normalizations differ")
    for index, amplitude in enumerate(amplitudes):
        cases.require(form._event_weight((index,), denominator) == Q(amplitude*amplitude, denominator*denominator), "single event weight")
    cases.require(global_weight-diagonal == (Q(1, 2) if denominator == 2 else Q(24, 25)), "cross contribution")
    coarse = form._coarse_grained(((0, 1),))
    cases.require(coarse._event_weight((0,), denominator) == global_weight, "coarse global weight")


def verify_decoherence(cases: Cases) -> None:
    run = _recorder(cases)
    for a, b in product(range(-6, 7), repeat=2):
        form = IntegerGramForm(((a, b),))
        gram = form._gram()
        run.require(gram[0][0] >= 0, "first diagonal")
        run.require(gram[1][1] >= 0, "second diagonal")
        run.require(gram[0][0]+gram[1][1] >= 0, "diagonal trace")
        run.require(gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0] == 0, "rank-one determinant")
        for x, y in product((-3, -1, 0, 2), (-2, 0, 1, 4)):
            run.require(form._quadratic((x, y)) >= 0, "Gram quadratic")
    _normalization_controls((1, 1), 2, run)
    _normalization_controls((3, 4), 5, run)
    form = IntegerGramForm(((1, 1),))
    gram = form._gram()
    run.require(form._quadratic((1, 1)) == 4, "Gram at ones")
    run.require(gram[0][0]+2*gram[0][1]+gram[1][1] == 4, "expanded Gram at ones")


def verify_selection_witness(cases: Cases) -> None:
    """Retain the eleven original PrimToQmSelection integer obligations."""
    run = _recorder(cases)
    quadratic, quartic = (_masses((1, 2), exponent) for exponent in (2, 4))
    quadratic_total, quartic_total = sum(quadratic), sum(quartic)
    run.require((*quadratic, quadratic_total) == (1, 4, 5), "selection quadratic numerators")
    run.require((*quartic, quartic_total) == (1, 16, 17), "selection quartic numerators")
    run.require(all(value > 0 for value in quadratic+quartic), "selection positivity")
    run.require(sum(quadratic) == quadratic_total and sum(quartic) == quartic_total, "selection normalization sums")
    square_weights, fourth_weights = (_power_shares((1, 2), degree) for degree in (2, 4))
    run.require(square_weights == (Q(1, 5), Q(4, 5)), "selection quadratic weights")
    run.require(fourth_weights == (Q(1, 17), Q(16, 17)), "selection quartic weights")
    left, right = quadratic[0]*quartic_total, quartic[0]*quadratic_total
    run.require(square_weights[0] != fourth_weights[0] and left != right, "selection rules differ")
    run.require((left, right) == (17, 5), "selection cross products")
    symmetric_square, symmetric_fourth = (_masses((1, 1), degree) for degree in (2, 4))
    run.require((*symmetric_square, sum(symmetric_square), *symmetric_fourth, sum(symmetric_fourth)) == (1, 1, 2, 1, 1, 2), "selection symmetric numerators")
    run.require(_power_shares((1, 1), 2)[0] == Q(1, 2), "selection symmetric quadratic")
    run.require(_power_shares((1, 1), 4)[0] == Q(1, 2), "selection symmetric quartic")


def verify_born_boundary(cases: Cases) -> None:
    run = _recorder(cases)
    for a, b in product(range(-5, 6), repeat=2):
        total = _dot((a, b), (1, 1))
        run.require(total == (a+b)*1, "pair sum")
    for a, b, r, s in product(range(-3, 4), repeat=4):
        rotated = _rotation((a, b), (r, s))
        run.require(_dot(rotated, rotated) == (r*r+s*s)*(a*a+b*b), "scaled rotation norm")
    linear, squares, fourths = (_masses((3, 4), exponent) for exponent in (1, 2, 4))
    run.require(sum(linear) == 7 and sum(linear) != 0, "linear denominator")
    run.require(squares == (9, 16) and sum(squares) == 25 and 5*5 == 25, "square masses")
    run.require(fourths == (81, 256) and sum(fourths) == 337, "quartic masses")
    quartic_cross = squares[0]*sum(fourths), fourths[0]*sum(squares)
    linear_cross = linear[0]*sum(squares), squares[0]*sum(linear)
    run.require(quartic_cross == (3033, 2025) and quartic_cross[0] != quartic_cross[1], "quartic separates")
    run.require(linear_cross == (75, 63) and linear_cross[0] != linear_cross[1], "linear separates")
    shares = tuple(_power_shares((3, 4), degree) for degree in (1, 2, 4))
    run.require(shares[0] == (Q(3, 7), Q(4, 7)), "linear shares")
    run.require(shares[1] == (Q(9, 25), Q(16, 25)), "quadratic shares")
    run.require(shares[2] == (Q(81, 337), Q(256, 337)), "quartic shares")
    run.require(all(sum(value) == 1 for value in shares) and len(set(shares)) == 3, "normalization does not select pairing")
    rotated = _rotation((3, 4), (3, 4))
    run.require(rotated == (-7, 24) and _masses(rotated, 2) == (49, 576) and _dot(rotated, rotated) == 625, "rotation witness")
    run.require(sum(squares)*sum(squares) == 625, "scaled norm witness")
    verify_selection_witness(run)


def main() -> None:
    cases = Cases()
    verify_positivity(cases)
    first = cases.checks
    verify_decoherence(cases)
    second = cases.checks
    verify_born_boundary(cases)
    print(json.dumps({"status": "passed", "checks": cases.checks, "positivity": first,
                      "decoherence": second-first, "born_boundary": cases.checks-second,
                      "scope": "finite scalar/Gram controls; no channel, physical history model or Born uniqueness"}))


if __name__ == "__main__":
    raise SystemExit(cli(main))
