"""Exact scalar and shaped-matrix codecs for the paper's native adapters.

These are value and shape contracts. Mathematical operations run in Rust.
"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction

from sympy import Matrix, Rational
from sympy.matrices.matrixbase import MatrixBase

ExactInput = int | str | Fraction | Rational


def as_rational(value: ExactInput) -> Rational:
    """Reject approximate and symbolic values before crossing the native seam."""
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction, Rational)):
        raise TypeError("exact scalar must be int, str, Fraction, or SymPy Rational")
    try:
        return Rational(value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise ValueError("expected a finite exact rational") from error


def exact_vector(value: Sequence[ExactInput] | MatrixBase, *, label: str) -> Matrix:
    if isinstance(value, MatrixBase):
        if value.shape in ((0, 0), (0, 1), (1, 0)):
            return Matrix(0, 1, [])
        if value.cols != 1:
            raise ValueError(f"{label} must be a column vector")
        return Matrix(value.rows, 1, [as_rational(item) for item in value])
    entries = [as_rational(item) for item in value]
    return Matrix(len(entries), 1, entries)


def matrix_wire(value: MatrixBase) -> dict:
    if not isinstance(value, MatrixBase):
        raise TypeError("expected an exact SymPy matrix")
    return {
        "rows": value.rows,
        "cols": value.cols,
        "data": [
            [str(as_rational(value[row, col])) for col in range(value.cols)]
            for row in range(value.rows)
        ],
    }
