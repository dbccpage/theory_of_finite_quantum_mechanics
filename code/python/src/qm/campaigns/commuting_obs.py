"""Commutator mass of rational observables.

Origin: lean4/CommutingObservables.lean definitions pauliX and pauliZ.
X = [[0, 1], [1, 0]] and Z = [[1, 0], [0, -1]] are not scalar, and the
computed mass of [X, Z] is 4. Two diagonal matrices contribute mass 0.
Claim: urn:omega:fqm:qm:pauli-commutator-mass:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 7; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: This file measures the entrywise absolute mass of one commutator.
It does not classify maximal abelian subalgebras.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_MASS = Fraction(4)


class CommutatorError(Exception):
    """One violated observable invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CommutatorError:
    return CommutatorError(invariant, parameters)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _parse_row(row: object, role: str) -> tuple[Fraction, ...]:
    if isinstance(row, (str, bytes)) or not isinstance(row, tuple) or len(row) == 0:
        raise _fail("observable row is not a nonempty tuple", role=role, received=type(row).__name__)
    return tuple(_require_fraction(entry, role) for entry in row)


def _parse_matrix(matrix: object, role: str) -> tuple[tuple[Fraction, ...], ...]:
    if isinstance(matrix, (str, bytes)) or not isinstance(matrix, tuple) or len(matrix) == 0:
        raise _fail("observable is not a nonempty tuple", role=role, received=type(matrix).__name__)
    rows = tuple(_parse_row(row, f"{role}-row") for row in matrix)
    width = len(rows[0])
    index = 0
    while index < len(rows):
        if len(rows[index]) != width:
            raise _fail("observable rows differ in width", role=role, width=width, actual=len(rows[index]))
        index += 1
    return rows


def _dot(left: tuple[Fraction, ...], right: tuple[tuple[Fraction, ...], ...], column: int) -> Fraction:
    total = Fraction(0)
    index = 0
    while index < len(left):
        total += left[index] * right[index][column]
        index += 1
    return total


def _mul_row(left: tuple[Fraction, ...], right: tuple[tuple[Fraction, ...], ...]) -> tuple[Fraction, ...]:
    values: list[Fraction] = []
    column = 0
    while column < len(right[0]):
        values.append(_dot(left, right, column))
        column += 1
    return tuple(values)


def _mul(left: tuple[tuple[Fraction, ...], ...], right: tuple[tuple[Fraction, ...], ...]) -> tuple[tuple[Fraction, ...], ...]:
    if len(left[0]) != len(right):
        raise _fail("observable shapes do not match", left=len(left[0]), right=len(right))
    rows: list[tuple[Fraction, ...]] = []
    index = 0
    while index < len(left):
        rows.append(_mul_row(left[index], right))
        index += 1
    return tuple(rows)


def _mass(left: tuple[tuple[Fraction, ...], ...], right: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    product = _mul(left, right)
    reverse = _mul(right, left)
    total = Fraction(0)
    row = 0
    while row < len(product):
        column = 0
        while column < len(product[0]):
            total += abs(product[row][column] - reverse[row][column])
            column += 1
        row += 1
    return total


def commutator_mass(left: object, right: object) -> Fraction:
    """Sum of absolute entries of XY − YX."""
    return _mass(_parse_matrix(left, "left"), _parse_matrix(right, "right"))


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def pauli_commutator_mass() -> Fraction:
    """Mass of [X, Z]. The diagonal pair is checked to contribute 0."""
    diagonal_mass = commutator_mass(((1, 0), (0, 2)), ((3, 0), (0, -1)))
    if diagonal_mass != 0:
        raise _fail("diagonal observables failed to commute", mass=str(diagonal_mass))
    mass = commutator_mass(((0, 1), (1, 0)), ((1, 0), (0, -1)))
    return _locked(mass, _MASS, "Pauli commutator mass drifted")


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the Pauli commutator mass 4."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return pauli_commutator_mass()


def main() -> int:
    value = pauli_commutator_mass()
    print(value)
    if value == _MASS:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
