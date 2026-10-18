"""Exact checks of the matrix-algebra laws on rational witnesses.

Origin: code/python/src/linear_algebra/matrix.py methods ExactMatrix.__mul__
and ExactMatrix.transpose, which supply the product and the transpose used here.
Claim: urn:omega:fqm:linear-algebra:algebra-laws:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_laws.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: transpose_law_defect and associator_defect check the rational
matrices they are given. The defects are the entrywise absolute masses of
(AB)^T - B^T A^T and (AB)C - A(BC). This file does not schematize the laws
for every ring, does not treat Q(i), and does not admit floats.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class LawError(MatrixError):
    """One violated algebra-law invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> LawError:
    return LawError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; algebra laws in this module are over Q", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("matrix entry is not an exact rational", role=role, received=type(value).__name__)


def _require_dimension(value: object, role: str) -> int:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a matrix dimension was required", role=role)
    if type(value) is int:
        if value < 0:
            raise _fail("matrix shape is negative", role=role, received=value)
        return value
    raise _fail("matrix shape is not an integer", role=role, received=type(value).__name__)


def _require_data_length(matrix: ExactMatrix, rows: int, cols: int) -> None:
    length = len(matrix.data)
    if length != rows * cols:
        raise _fail("matrix data length does not match the shape", length=length, rows=rows, cols=cols)


def _rational_matrix(matrix: object) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail("algebra-law input is not an ExactMatrix", received=type(matrix).__name__)
    rows = _require_dimension(matrix.rows, "rows")
    cols = _require_dimension(matrix.cols, "cols")
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _require_product(left_cols: int, right_rows: int, role: str) -> None:
    if left_cols != right_rows:
        raise _fail(
            "cannot multiply shapes",
            role=role,
            left_cols=left_cols,
            right_rows=right_rows,
        )


def _gap_mass(matrix: ExactMatrix) -> Fraction:
    total = Fraction(0)
    for value in matrix.data:
        total += abs(_require_entry(value, "gap-entry"))
    return total


def transpose_law_defect(left: object, right: object) -> Fraction:
    """Sum of absolute entries of (AB)^T − B^T A^T."""
    left_m = _rational_matrix(left)
    right_m = _rational_matrix(right)
    _require_product(left_m.cols, right_m.rows, "transpose")
    gap = (left_m * right_m).transpose() - (right_m.transpose() * left_m.transpose())
    return _gap_mass(gap)


def associator_defect(left: object, mid: object, right: object) -> Fraction:
    """Sum of absolute entries of (AB)C − A(BC)."""
    left_m = _rational_matrix(left)
    mid_m = _rational_matrix(mid)
    right_m = _rational_matrix(right)
    _require_product(left_m.cols, mid_m.rows, "associator-left")
    _require_product(mid_m.cols, right_m.rows, "associator-right")
    gap = (left_m * mid_m) * right_m - left_m * (mid_m * right_m)
    return _gap_mass(gap)


def _require_zero_defect(defect: Fraction, role: str) -> None:
    if defect != 0:
        raise _fail("algebra-law defect is nonzero", role=role, defect=str(defect))


def witness_product_entry() -> Fraction:
    """(0, 1) entry of (AB)^T for the fixed rational pair. It is computed, not stored."""
    left = ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(0), Fraction(1)]])
    right = ExactMatrix.from_rows([[Fraction(3), Fraction(0)], [Fraction(4), Fraction(5)]])
    _require_zero_defect(transpose_law_defect(left, right), "witness")
    product = (left * right).transpose()
    return _require_entry(product.get(0, 1), "witness")


__all__ = [
    "ExactMatrix",
    "LawError",
    "associator_defect",
    "transpose_law_defect",
    "witness_product_entry",
]
