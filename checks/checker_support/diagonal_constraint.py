"""Owned rational diagonal constraints on three coordinates. AuthorityEffect: None."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q

from .boundary import evaluate
from .domains import rational, sequence
from .outcome import Outcome
from .rational_matrix import RationalMatrix

Vector3 = tuple[Q, Q, Q]


def _vector(value: object) -> Vector3:
    x, y, z = (rational(entry, "constraint coordinate")
               for entry in sequence(value, "three coordinates", 3, 3))
    return x, y, z


def _column(value: object) -> RationalMatrix:
    return RationalMatrix(tuple((entry,) for entry in _vector(value)))


def _entries(column: RationalMatrix) -> Vector3:
    column.require_shape(3, 1)
    return column.rows[0][0], column.rows[1][0], column.rows[2][0]


def _diagonal(values: Vector3) -> RationalMatrix:
    return RationalMatrix(tuple(tuple(values[i] if i == j else Q(0) for j in range(3))
                                for i in range(3)))


@dataclass(frozen=True, slots=True, init=False)
class DiagonalConstraint:
    """Owns exactly three rational coefficients with 4096-bit component bounds."""
    diagonal: Vector3

    def __init__(self, diagonal: object) -> None:
        object.__setattr__(self, "diagonal", _vector(diagonal))

    @property
    def matrix(self) -> RationalMatrix:
        return _diagonal(self.diagonal)

    @property
    def kernel_projector(self) -> RationalMatrix:
        mask = _vector(tuple(int(value == 0) for value in self.diagonal))
        return _diagonal(mask)

    @property
    def kernel_basis(self) -> tuple[Vector3, ...]:
        basis = ((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1)))
        return tuple(basis[i] for i in range(3) if self.diagonal[i] == 0)

    @property
    def rank(self) -> int:
        return sum(value != 0 for value in self.diagonal)

    @property
    def kernel_dimension(self) -> int:
        return 3-self.rank

    @property
    def spectrum(self) -> tuple[tuple[Q, int], ...]:
        return tuple(sorted(Counter(self.diagonal).items()))

    @property
    def is_projector(self) -> bool:
        return all(value in (0, 1) for value in self.diagonal)

    @property
    def is_positive_semidefinite(self) -> bool:
        return all(value >= 0 for value in self.diagonal)

    @property
    def is_indefinite(self) -> bool:
        return any(value > 0 for value in self.diagonal) and any(value < 0 for value in self.diagonal)

    def _apply(self, vector: object) -> Vector3:
        column = _column(vector)
        return _entries(self.matrix.mul(column))

    def apply(self, vector: object) -> Outcome[Vector3]:
        return evaluate(self._apply, vector)

    def _project(self, vector: object) -> Vector3:
        column = _column(vector)
        return _entries(self.kernel_projector.mul(column))

    def project(self, vector: object) -> Outcome[Vector3]:
        return evaluate(self._project, vector)

    def _contains(self, vector: object) -> bool:
        coordinates = _vector(vector)
        return all(coefficient == 0 or coordinate == 0
                   for coefficient, coordinate in zip(self.diagonal, coordinates))

    def contains(self, vector: object) -> Outcome[bool]:
        """Decide kernel membership without multiplying nonzero coefficients."""
        return evaluate(self._contains, vector)

    def _quadratic(self, vector: object) -> Q:
        column = _column(vector)
        weighted = self.matrix.mul(column)
        return column.transpose().mul(weighted).rows[0][0]

    def quadratic(self, vector: object) -> Outcome[Q]:
        return evaluate(self._quadratic, vector)
