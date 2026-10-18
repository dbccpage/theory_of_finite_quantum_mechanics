"""Kronecker product over Q and the mixed-product law.

Origin: code/rust/src/linear_algebra/matrix.rs function kronecker, whose
comment states that entry (i·p + k, j·q + l) of a ⊗ b is a[i][j]·b[k][l],
and the test comment "the mixed-product law `(A ⊗ B)(C ⊗ D) = AC ⊗ BD`"
together with "tr(A ⊗ B) = tr(A) tr(B)".
Claim: urn:omega:fqm:linear-algebra:kronecker-mixed-product:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_complex_tensor.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: mixed_product_defect and trace_product_defect check the rational
matrices they are given. This file does not implement the doubled-module
balance map, does not bound allocation fuel, does not admit Q(i), and does
not admit floats.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class TensorError(MatrixError):
    """One violated Kronecker invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> TensorError:
    return TensorError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; the Kronecker product in this module is over Q", role=role)
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
        raise _fail("Kronecker input is not an ExactMatrix", received=type(matrix).__name__)
    rows = _require_dimension(matrix.rows, "rows")
    cols = _require_dimension(matrix.cols, "cols")
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _require_product(left_cols: int, right_rows: int, role: str) -> None:
    if left_cols != right_rows:
        raise _fail("cannot multiply shapes", role=role, left_cols=left_cols, right_rows=right_rows)


def _require_square(matrix: ExactMatrix, role: str) -> None:
    if matrix.rows != matrix.cols:
        raise _fail("trace factor is not square", role=role, rows=matrix.rows, cols=matrix.cols)


def _trace(matrix: ExactMatrix) -> Fraction:
    total = Fraction(0)
    index = 0
    while index < matrix.rows:
        total += _require_entry(matrix.get(index, index), f"diagonal[{index}]")
        index += 1
    return total


def _block_entry(left: ExactMatrix, right: ExactMatrix, row: int, col: int) -> Fraction:
    right_rows = right.rows
    right_cols = right.cols
    i = row // right_rows
    k = row % right_rows
    j = col // right_cols
    ell = col % right_cols
    left_entry = _require_entry(left.get(i, j), "left-block")
    right_entry = _require_entry(right.get(k, ell), "right-block")
    return left_entry * right_entry


def kronecker(left: object, right: object) -> ExactMatrix:
    """Return a ⊗ b with entry (i·p + k, j·q + l) equal to a[i][j]·b[k][l]."""
    left_m = _rational_matrix(left)
    right_m = _rational_matrix(right)
    rows = left_m.rows * right_m.rows
    cols = left_m.cols * right_m.cols
    data = [_block_entry(left_m, right_m, row, col) for row in range(rows) for col in range(cols)]
    return ExactMatrix(rows, cols, data)


def _gap_mass(matrix: ExactMatrix) -> Fraction:
    total = Fraction(0)
    for value in matrix.data:
        total += abs(_require_entry(value, "gap-entry"))
    return total


def mixed_product_defect(a: object, b: object, c: object, d: object) -> Fraction:
    """Sum of absolute entries of (A ⊗ B)(C ⊗ D) − (AC) ⊗ (BD)."""
    a_m = _rational_matrix(a)
    b_m = _rational_matrix(b)
    c_m = _rational_matrix(c)
    d_m = _rational_matrix(d)
    _require_product(a_m.cols, c_m.rows, "mixed-left")
    _require_product(b_m.cols, d_m.rows, "mixed-right")
    left_side = kronecker(a_m, b_m) * kronecker(c_m, d_m)
    right_side = kronecker(a_m * c_m, b_m * d_m)
    return _gap_mass(left_side - right_side)


def trace_product_defect(left: object, right: object) -> Fraction:
    """Absolute value of tr(A ⊗ B) − tr(A) tr(B)."""
    left_m = _rational_matrix(left)
    right_m = _rational_matrix(right)
    _require_square(left_m, "left")
    _require_square(right_m, "right")
    product = kronecker(left_m, right_m)
    left_trace = _trace(left_m)
    right_trace = _trace(right_m)
    return abs(_trace(product) - left_trace * right_trace)


def _require_zero_defect(defect: Fraction, role: str) -> None:
    if defect != 0:
        raise _fail("Kronecker defect is nonzero", role=role, defect=str(defect))


def _block_factors() -> tuple[ExactMatrix, ExactMatrix]:
    left = ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(2), Fraction(0)],
            [Fraction(0), Fraction(1), Fraction(3)],
        ]
    )
    right = ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(0)],
            [Fraction(4), Fraction(5)],
            [Fraction(0), Fraction(1)],
        ]
    )
    return left, right


def _mixed_factors() -> tuple[ExactMatrix, ExactMatrix, ExactMatrix, ExactMatrix]:
    first = ExactMatrix.from_rows([[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]])
    second = ExactMatrix.from_rows([[Fraction(2), Fraction(0)], [Fraction(0), Fraction(3)]])
    third = ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(1), Fraction(1)]])
    fourth = ExactMatrix.from_rows([[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]])
    return first, second, third, fourth


def _trace_factors() -> tuple[ExactMatrix, ExactMatrix]:
    left = ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]])
    right = ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1, 3)]])
    return left, right


def witness_block_entry() -> Fraction:
    """Entry (2, 1) of the fixed 2×3 ⊗ 3×2 block. It is computed, not stored."""
    first, second, third, fourth = _mixed_factors()
    _require_zero_defect(mixed_product_defect(first, second, third, fourth), "mixed")
    trace_left, trace_right = _trace_factors()
    _require_zero_defect(trace_product_defect(trace_left, trace_right), "trace")
    left, right = _block_factors()
    product = kronecker(left, right)
    return _require_entry(product.get(2, 1), "witness")


__all__ = [
    "ExactMatrix",
    "TensorError",
    "kronecker",
    "mixed_product_defect",
    "trace_product_defect",
    "witness_block_entry",
]
