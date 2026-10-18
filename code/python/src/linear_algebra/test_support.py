"""Two-by-two minor and empty determinant, checked against elimination.

Origin: code/python/src/linear_algebra/matrix.py method ExactMatrix.determinant,
and code/rust/src/linear_algebra/elimination.rs, which states that the
determinant of a square matrix is 1 for the empty matrix.
Claim: urn:omega:fqm:linear-algebra:two-by-two-minor:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_support.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: sample_determinant checks ad − bc against ExactMatrix.determinant
for one 2 by 2 rational witness. hilbert_entry builds the rational array
1/(i+j+1) as a second witness and does not cite a Hilbert-space theorem.
This file does not admit floats or Q(i).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class FixtureError(MatrixError):
    """One violated fixture invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> FixtureError:
    return FixtureError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; the two-by-two minor in this module is over Q", role=role)
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
        raise _fail("minor input is not an ExactMatrix", received=type(matrix).__name__)
    rows = _require_dimension(matrix.rows, "rows")
    cols = _require_dimension(matrix.cols, "cols")
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _require_index(value: object, role: str) -> int:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a Hilbert index was required", role=role)
    if type(value) is int:
        if value < 0:
            raise _fail("Hilbert index is negative", role=role, received=value)
        return value
    raise _fail("Hilbert index is not an integer", role=role, received=type(value).__name__)


def _require_size(value: object) -> int:
    _refuse_float(value, "size")
    if type(value) is bool:
        raise _fail("boolean refused where a Hilbert size was required", role="size")
    if type(value) is int:
        if value < 1:
            raise _fail("Hilbert size must be positive", received=value)
        return value
    raise _fail("Hilbert size is not an integer", received=type(value).__name__)


def _require_fraction(value: object, role: str) -> Fraction:
    if type(value) is not Fraction:
        raise _fail("elimination determinant is not rational", role=role, received=type(value).__name__)
    return value


def sample_matrix() -> ExactMatrix:
    """The integer witness [[1, 2], [3, 4]]."""
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(2)],
            [Fraction(3), Fraction(4)],
        ]
    )


def minor_determinant(matrix: object) -> Fraction:
    """Return ad − bc for a rational 2 by 2 matrix."""
    parsed = _rational_matrix(matrix)
    if parsed.rows != 2:
        raise _fail("two-by-two minor requires two rows", rows=parsed.rows, cols=parsed.cols)
    if parsed.cols != 2:
        raise _fail("two-by-two minor requires two columns", rows=parsed.rows, cols=parsed.cols)
    a = _require_entry(parsed.get(0, 0), "a")
    b = _require_entry(parsed.get(0, 1), "b")
    c = _require_entry(parsed.get(1, 0), "c")
    d = _require_entry(parsed.get(1, 1), "d")
    return a * d - b * c


def sample_determinant() -> Fraction:
    """ad − bc for the fixed witness, required to equal ExactMatrix.determinant."""
    matrix = sample_matrix()
    by_minors = minor_determinant(matrix)
    declared = _require_fraction(matrix.determinant(), "sample")
    if by_minors != declared:
        raise _fail(
            "minor determinant disagrees with elimination",
            minor=str(by_minors),
            elimination=str(declared),
        )
    return by_minors


def empty_determinant() -> Fraction:
    """Determinant of the empty matrix. The cited routine returns 1."""
    declared = _require_fraction(ExactMatrix(0, 0, []).determinant(), "empty")
    if declared != 1:
        raise _fail("empty determinant is not 1", elimination=str(declared))
    return declared


def hilbert_entry(row: object, col: object) -> Fraction:
    """Rational entry 1/(i+j+1), indexed from 0."""
    i = _require_index(row, "row")
    j = _require_index(col, "column")
    return Fraction(1, i + j + 1)


def hilbert_matrix(size: object) -> ExactMatrix:
    """The n by n array with entries 1/(i+j+1)."""
    n = _require_size(size)
    data: list[Fraction] = []
    row = 0
    while row < n:
        col = 0
        while col < n:
            data.append(hilbert_entry(row, col))
            col += 1
        row += 1
    return ExactMatrix(n, n, data)


def hilbert_minor_defect() -> Fraction:
    """Absolute gap between the 2 by 2 Hilbert minor and 1/12."""
    minor = ExactMatrix.from_rows(
        [
            [hilbert_entry(0, 0), hilbert_entry(0, 1)],
            [hilbert_entry(1, 0), hilbert_entry(1, 1)],
        ]
    )
    expected = Fraction(1) * Fraction(1, 3) - Fraction(1, 2) * Fraction(1, 2)
    declared = _require_fraction(minor.determinant(), "hilbert")
    if declared != expected:
        raise _fail("Hilbert minor disagrees with elimination", elimination=str(declared))
    return abs(minor_determinant(minor) - expected)


def _require_zero_defect(defect: Fraction, role: str) -> None:
    if defect != 0:
        raise _fail("minor defect is nonzero", role=role, defect=str(defect))


def witness_minor() -> Fraction:
    """The witness determinant −2, after the empty and Hilbert checks."""
    _require_zero_defect(hilbert_minor_defect(), "hilbert")
    if empty_determinant() != 1:
        raise _fail("empty determinant is not 1", elimination="moved")
    return sample_determinant()


__all__ = [
    "ExactMatrix",
    "FixtureError",
    "empty_determinant",
    "hilbert_entry",
    "hilbert_matrix",
    "hilbert_minor_defect",
    "minor_determinant",
    "sample_determinant",
    "sample_matrix",
    "witness_minor",
]
