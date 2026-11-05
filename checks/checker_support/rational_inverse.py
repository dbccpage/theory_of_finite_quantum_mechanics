"""Bounded exact inverse search with independent two-sided certificate replay.

AuthorityEffect: None. Owns matrices through RationalMatrix; dimensions1..64,
4096-bit rational intermediates, O(n^3) operations and O(n^2) workspace.
"""
from fractions import Fraction as Q

from .boundary import Violation, evaluate, require
from .domains import rational
from .outcome import Outcome
from .rational_matrix import RationalMatrix


def _square(value: object) -> RationalMatrix:
    if type(value) is not RationalMatrix:
        raise Violation("input", "inverse requires an owned RationalMatrix")
    value.require_shape(value.shape[0], value.shape[0])
    return value


def _verify(matrix: object, candidate: object) -> RationalMatrix:
    original = _square(matrix)
    inverse = _square(candidate).require_shape(*original.shape)
    identity = RationalMatrix.eye(original.shape[0])
    require(original.mul(inverse) == identity, "right inverse identity failed")
    require(inverse.mul(original) == identity, "left inverse identity failed")
    return inverse


def verify_inverse(matrix: object, candidate: object) -> Outcome[RationalMatrix]:
    """Admit and replay a proposed inverse without trusting its producer."""
    return evaluate(_verify, matrix, candidate)


def _eliminate(row: list[Q], pivot: list[Q], column: int) -> list[Q]:
    factor = row[column]
    return [rational(value-rational(factor*entry, "inverse elimination product"), "inverse elimination difference")
            for value, entry in zip(row, pivot)]


def _candidate(matrix: RationalMatrix) -> RationalMatrix:
    size = matrix.shape[0]
    rows = [list(row)+[Q(int(i == j)) for j in range(size)] for i, row in enumerate(matrix.rows)]
    for column in range(size):
        pivot = next((index for index in range(column, size) if rows[index][column] != 0), None)
        if pivot is None:
            raise Violation("input", "singular matrix has no inverse")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        divisor = rows[column][column]
        normalized = [rational(value/divisor, "inverse pivot quotient") for value in rows[column]]
        rows = [_eliminate(row, normalized, column) if index != column else normalized
                for index, row in enumerate(rows)]
    return RationalMatrix(tuple(tuple(row[size:]) for row in rows))


def _inverse(matrix: object) -> RationalMatrix:
    original = _square(matrix)
    return _verify(original, _candidate(original))


def inverse(matrix: object) -> Outcome[RationalMatrix]:
    """Search and certify; singular input and resource refusal remain distinct."""
    return evaluate(_inverse, matrix)
