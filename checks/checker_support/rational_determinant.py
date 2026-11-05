"""Bounded exact determinant of an owned square matrix. AuthorityEffect: None."""
from fractions import Fraction as Q

from .boundary import Violation, evaluate
from .domains import rational
from .outcome import Outcome
from .rational_matrix import RationalMatrix


def _reduce(row: list[Q], pivot: list[Q], column: int) -> list[Q]:
    factor = rational(row[column] / pivot[column], "determinant elimination factor")
    return row[:column] + [rational(value-rational(factor*entry, "determinant product"),
                                  "determinant difference")
                           for value, entry in zip(row[column:], pivot[column:])]


def _determinant(matrix: object) -> Q:
    if type(matrix) is not RationalMatrix:
        raise Violation("input", "determinant requires an owned RationalMatrix")
    matrix.require_shape(matrix.shape[0], matrix.shape[0])
    rows = [list(row) for row in matrix.rows]
    determinant = Q(1)
    size = len(rows)
    for column in range(size):
        pivot = next((i for i in range(column, size) if rows[i][column] != 0), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            determinant = -determinant
        determinant = rational(determinant*rows[column][column], "determinant pivot product")
        rows[column+1:] = [_reduce(row, rows[column], column) for row in rows[column+1:]]
    return determinant


def determinant(matrix: object) -> Outcome[Q]:
    """O(n^3) rational operations, O(n^2) workspace; 1..64 square dimensions."""
    return evaluate(_determinant, matrix)
