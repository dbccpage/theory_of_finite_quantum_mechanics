"""Two-site wrong-sign marginal on a normalized rational product reference.

Origin: code/rust/src/linear_algebra/tensor_proj.rs, which states that each
reference factor is square, nonempty, and has exact trace one, and that
id - sum_{proper S} (-1)^(k-|S|) P_S has the wrong sign: on the normalized
product reference it returns twice that reference.
Claim: urn:omega:fqm:linear-algebra:tensor-wrong-sign:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_tensor_proj.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: reference_twice_defect checks two rational factors. This file
does not enumerate subsets for more than two sites, does not charge allocation
fuel, does not claim positivity or Hermiticity, and does not admit Q(i) or floats.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from .complex_tensor import kronecker
from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class ProjectorError(MatrixError):
    """One violated tensor-marginal invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ProjectorError:
    return ProjectorError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; tensor marginals in this module are over Q", role=role)
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
        raise _fail("tensor input is not an ExactMatrix", received=type(matrix).__name__)
    rows = _require_dimension(matrix.rows, "rows")
    cols = _require_dimension(matrix.cols, "cols")
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _trace(matrix: ExactMatrix) -> Fraction:
    total = Fraction(0)
    index = 0
    while index < matrix.rows:
        total += _require_entry(matrix.get(index, index), f"diagonal[{index}]")
        index += 1
    return total


def _require_reference(matrix: object, role: str) -> ExactMatrix:
    parsed = _rational_matrix(matrix)
    if parsed.rows != parsed.cols:
        raise _fail("reference factor is not square", role=role, rows=parsed.rows, cols=parsed.cols)
    if parsed.rows < 1:
        raise _fail("reference factor is empty", role=role, rows=parsed.rows)
    trace = _trace(parsed)
    if trace != 1:
        raise _fail("reference factor does not have trace one", role=role, trace=str(trace))
    return parsed


def _require_operator(operator: object, size: int) -> ExactMatrix:
    parsed = _rational_matrix(operator)
    if parsed.rows != size:
        raise _fail("tensor operator shape does not match the product", rows=parsed.rows, cols=parsed.cols, size=size)
    if parsed.cols != size:
        raise _fail("tensor operator shape does not match the product", rows=parsed.rows, cols=parsed.cols, size=size)
    return parsed


def _trace_right_factor(operator: ExactMatrix, row: int, col: int, right_dim: int) -> Fraction:
    total = Fraction(0)
    site = 0
    while site < right_dim:
        left = row * right_dim + site
        right = col * right_dim + site
        total += _require_entry(operator.get(left, right), "marginal-left")
        site += 1
    return total


def _trace_left_factor(operator: ExactMatrix, row: int, col: int, left_dim: int, right_dim: int) -> Fraction:
    total = Fraction(0)
    site = 0
    while site < left_dim:
        left = site * right_dim + row
        right = site * right_dim + col
        total += _require_entry(operator.get(left, right), "marginal-right")
        site += 1
    return total


def _retain_left(operator: ExactMatrix, left_dim: int, right_dim: int) -> ExactMatrix:
    data: list[Fraction] = []
    slot = 0
    limit = left_dim * left_dim
    while slot < limit:
        row = slot // left_dim
        col = slot % left_dim
        data.append(_trace_right_factor(operator, row, col, right_dim))
        slot += 1
    return ExactMatrix(left_dim, left_dim, data)


def _retain_right(operator: ExactMatrix, left_dim: int, right_dim: int) -> ExactMatrix:
    data: list[Fraction] = []
    slot = 0
    limit = right_dim * right_dim
    while slot < limit:
        row = slot // right_dim
        col = slot % right_dim
        data.append(_trace_left_factor(operator, row, col, left_dim, right_dim))
        slot += 1
    return ExactMatrix(right_dim, right_dim, data)


def _entry_product(left: ExactMatrix, right: ExactMatrix, row: int, col: int, right_dim: int) -> Fraction:
    left_row = row // right_dim
    right_row = row % right_dim
    left_col = col // right_dim
    right_col = col % right_dim
    left_entry = _require_entry(left.get(left_row, left_col), "inject-left")
    right_entry = _require_entry(right.get(right_row, right_col), "inject-right")
    return left_entry * right_entry


def _inject(local: ExactMatrix, factor: ExactMatrix, factor_on_right: bool) -> ExactMatrix:
    factor_dim = factor.rows
    local_dim = local.rows
    size = local_dim * factor_dim
    data: list[Fraction] = []
    index = 0
    limit = size * size
    while index < limit:
        row = index // size
        col = index % size
        if factor_on_right:
            data.append(_entry_product(local, factor, row, col, factor_dim))
        else:
            data.append(_entry_product(factor, local, row, col, local_dim))
        index += 1
    return ExactMatrix(size, size, data)


def _scale(matrix: ExactMatrix, scalar: Fraction) -> ExactMatrix:
    data = [scalar * _require_entry(value, "scale") for value in matrix.data]
    return ExactMatrix(matrix.rows, matrix.cols, data)


def _gap_mass(matrix: ExactMatrix) -> Fraction:
    total = Fraction(0)
    for value in matrix.data:
        total += abs(_require_entry(value, "gap-entry"))
    return total


def _wrong_sign(operator: ExactMatrix, left: ExactMatrix, right: ExactMatrix, product: ExactMatrix) -> ExactMatrix:
    kept_left = _inject(_retain_left(operator, left.rows, right.rows), right, True)
    kept_right = _inject(_retain_right(operator, left.rows, right.rows), left, False)
    empty = _scale(product, _trace(operator))
    return operator - empty + kept_left + kept_right


def reference_twice_defect(left: object, right: object) -> Fraction:
    """Entrywise mass of the wrong-sign image of rho_0 ⊗ rho_1, minus twice that product."""
    left_m = _require_reference(left, "left")
    right_m = _require_reference(right, "right")
    product = kronecker(left_m, right_m)
    wrong = _wrong_sign(product, left_m, right_m, product)
    twice = _scale(product, Fraction(2))
    return _gap_mass(wrong - twice)


def _require_zero_defect(defect: Fraction, role: str) -> None:
    if defect != 0:
        raise _fail("tensor-marginal defect is nonzero", role=role, defect=str(defect))


def _witness_references() -> tuple[ExactMatrix, ExactMatrix]:
    left = ExactMatrix.from_rows([[Fraction(1, 2), Fraction(0)], [Fraction(0), Fraction(1, 2)]])
    right = ExactMatrix.from_rows([[Fraction(1, 3), Fraction(0)], [Fraction(0), Fraction(2, 3)]])
    return left, right


def _basis_shift() -> ExactMatrix:
    data = [Fraction(0)] * 16
    data[1] = Fraction(1)
    return ExactMatrix(4, 4, data)


def witness_basis_entry() -> Fraction:
    """(0, 1) entry of the wrong-sign image of the matrix unit E_01. It is 3/2."""
    left, right = _witness_references()
    _require_zero_defect(reference_twice_defect(left, right), "witness")
    product = kronecker(left, right)
    operator = _require_operator(_basis_shift(), product.rows)
    wrong = _wrong_sign(operator, left, right, product)
    return _require_entry(wrong.get(0, 1), "witness")


__all__ = [
    "ExactMatrix",
    "ProjectorError",
    "reference_twice_defect",
    "witness_basis_entry",
]
