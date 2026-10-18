"""Centralizer of one rational matrix, as the kernel of X |-> XA − AX.

Origin: code/rust/src/linear_algebra/commutant.rs, which builds centralizers
from row-major commutation equations, and lean4/CommutingObservables.lean,
which records that in M_2 a non-scalar matrix has commutant span{I, A}.
Claim: urn:omega:fqm:linear-algebra:commutant:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_commutant.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: commutant_dimension checks the rational matrix it is given. Each
returned basis matrix is rechecked by multiplication, and the count is the
nullity of the row-major commutator map. On a 2 by 2 non-scalar witness the
dimension is 2. This file does not prove the integral dependence in
masa_of_commuting_symmetric, does not classify a matrix algebra, and does not
admit floats or Q(i).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Sequence

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class CommutantError(MatrixError):
    """One violated commutant invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CommutantError:
    return CommutantError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; commutant in this module is over Q", role=role)
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


def _rational_square(matrix: object) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail("commutant input is not an ExactMatrix", received=type(matrix).__name__)
    rows = _require_dimension(matrix.rows, "rows")
    cols = _require_dimension(matrix.cols, "cols")
    if rows != cols:
        raise _fail("commutant requires a square matrix", rows=rows, cols=cols)
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _matrix_unit(size: int, row: int, col: int) -> ExactMatrix:
    data = [Fraction(0)] * (size * size)
    data[row * size + col] = Fraction(1)
    return ExactMatrix(size, size, data)


def _commutator(left: ExactMatrix, right: ExactMatrix) -> ExactMatrix:
    return left * right - right * left


def _vector(matrix: ExactMatrix) -> list[Fraction]:
    return [_require_entry(value, "commutator-entry") for value in matrix.data]


def _commutator_columns(source: ExactMatrix) -> list[list[Fraction]]:
    size = source.rows
    columns: list[list[Fraction]] = []
    for index in range(size * size):
        probe = _matrix_unit(size, index // size, index % size)
        columns.append(_vector(_commutator(probe, source)))
    return columns


def _stack(columns: Sequence[Sequence[Fraction]]) -> ExactMatrix:
    height = len(columns[0])
    width = len(columns)
    data: list[Fraction] = []
    for row in range(height):
        for column in columns:
            data.append(column[row])
    return ExactMatrix(height, width, data)


def _basis_matrix(size: int, vector: Sequence[object]) -> ExactMatrix:
    data = [_require_entry(entry, "kernel-entry") for entry in vector]
    if len(data) != size * size:
        raise _fail("kernel vector length is not n squared", length=len(data), n=size)
    return ExactMatrix(size, size, data)


def commutant_basis(matrix: object) -> list[ExactMatrix]:
    """Return a rational basis of {X : XA = AX}, in row-major coordinates."""
    source = _rational_square(matrix)
    size = source.rows
    if size == 0:
        return []
    kernel = _stack(_commutator_columns(source)).kernel_basis()
    return [_basis_matrix(size, vector) for vector in kernel]


def _commutes(element: ExactMatrix, source: ExactMatrix) -> bool:
    defect = _commutator(element, source)
    for entry in defect.data:
        if _require_entry(entry, "recheck-entry") != 0:
            return False
    return True


def _require_commuting(element: ExactMatrix, source: ExactMatrix) -> None:
    if not _commutes(element, source):
        raise _fail("commutant basis element does not commute", rows=source.rows)


def commutant_dimension(matrix: object) -> int:
    """Dimension of the commutant. Each basis element is rechecked by multiplication."""
    source = _rational_square(matrix)
    basis = commutant_basis(source)
    for element in basis:
        _require_commuting(element, source)
    return len(basis)


__all__ = [
    "CommutantError",
    "ExactMatrix",
    "commutant_basis",
    "commutant_dimension",
]
