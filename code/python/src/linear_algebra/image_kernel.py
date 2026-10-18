"""Rank-nullity certificate for one rational matrix.

Origin: research/lean4/qm_superposition_h1_rank.md theorem finrank_H1_eq_one,
which applies LinearMap.finrank_range_add_finrank_ker, and
research/lean4/qm_superposition_cochain.md definition d0
(d0 φ x = φ (x + 1) - φ x).
Claim: urn:omega:fqm:linear-algebra:image-kernel-rank-nullity:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_image_kernel.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: rank_nullity_certificate checks the matrix it is given. The pivot
columns rebuild that matrix, each kernel vector is sent to zero, the kernel is
independent on the free columns, and rank + nullity equals the column count.
On the n = 3 cycle coboundary this nullity is 1. This file does not prove
finrank_H1_eq_one for every n, does not compute H¹, and does not admit floats
or Q(i).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class ImageKernelError(MatrixError):
    """One violated image-kernel invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


@dataclass(frozen=True)
class RankNullityCertificate:
    """Checked rank, nullity, image basis, and kernel basis over Q."""

    rank: int
    nullity: int
    columns: int
    image: tuple[tuple[Fraction, ...], ...]
    kernel: tuple[tuple[Fraction, ...], ...]


def _fail(invariant: str, **parameters: object) -> ImageKernelError:
    return ImageKernelError(invariant, parameters)


def _require_entry(value: object, role: str) -> Fraction:
    if type(value) is float:
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; image-kernel certificate is over Q", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("matrix entry is not an exact rational", role=role, received=type(value).__name__)


def _require_dimension(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a matrix dimension was required", role=role)
    if type(value) is int:
        if value < 0:
            raise _fail("matrix shape is negative", role=role, received=value)
        return value
    raise _fail("matrix shape is not an integer", role=role, received=type(value).__name__)


def _require_shape(rows: object, cols: object) -> tuple[int, int]:
    return _require_dimension(rows, "rows"), _require_dimension(cols, "cols")


def _require_data_length(matrix: ExactMatrix, rows: int, cols: int) -> None:
    length = len(matrix.data)
    if length != rows * cols:
        raise _fail("matrix data length does not match the shape", length=length, rows=rows, cols=cols)


def _rational_matrix(matrix: object) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail("image-kernel input is not an ExactMatrix", received=type(matrix).__name__)
    rows, cols = _require_shape(matrix.rows, matrix.cols)
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _stored_fraction(value: object, role: str) -> Fraction:
    if type(value) is float:
        raise _fail("float refused on a stored matrix entry", role=role, received="float")
    if isinstance(value, Fraction):
        return value
    raise _fail("stored entry left the rational carrier", role=role, received=type(value).__name__)


def _image_factor(source: ExactMatrix, pivots: Sequence[int]) -> ExactMatrix:
    data: list[Fraction] = []
    for row in range(source.rows):
        for pivot in pivots:
            data.append(_stored_fraction(source.get(row, pivot), "pivot-column"))
    return ExactMatrix(source.rows, len(pivots), data)


def _coordinate_rows(reduced: ExactMatrix, rank: int) -> ExactMatrix:
    data: list[Fraction] = []
    for row in range(rank):
        for col in range(reduced.cols):
            data.append(_stored_fraction(reduced.get(row, col), "coordinate"))
    return ExactMatrix(rank, reduced.cols, data)


def _require_pivot_identity(reduced: ExactMatrix, pivots: Sequence[int]) -> None:
    for row, pivot in enumerate(pivots):
        entry = _stored_fraction(reduced.get(row, pivot), "pivot")
        if entry != Fraction(1):
            raise _fail("pivot entry is not one", row=row, pivot=pivot, entry=str(entry))


def _require_factorization(source: ExactMatrix, image: ExactMatrix, coordinates: ExactMatrix) -> None:
    if image * coordinates != source:
        raise _fail(
            "pivot columns do not rebuild the matrix",
            rows=source.rows,
            cols=source.cols,
            rank=image.cols,
        )


def _free_columns(width: int, pivots: Sequence[int]) -> list[int]:
    occupied = set(pivots)
    return [col for col in range(width) if col not in occupied]


def _kernel_vector(coordinates: ExactMatrix, pivots: Sequence[int], free_col: int) -> list[Fraction]:
    vector = [Fraction(0)] * coordinates.cols
    vector[free_col] = Fraction(1)
    for row, pivot in enumerate(pivots):
        entry = _stored_fraction(coordinates.get(row, free_col), "kernel-coordinate")
        vector[pivot] = -entry
    return vector


def _kernel_vectors(coordinates: ExactMatrix, pivots: Sequence[int]) -> list[list[Fraction]]:
    return [_kernel_vector(coordinates, pivots, free_col) for free_col in _free_columns(coordinates.cols, pivots)]


def _is_zero_image(values: list[object]) -> bool:
    for value in values:
        if _stored_fraction(value, "annihilated") != Fraction(0):
            return False
    return True


def _require_annihilator(source: ExactMatrix, vector: list[Fraction], free_col: int) -> None:
    if not _is_zero_image(source.mul_vec(vector)):
        raise _fail("kernel vector is not annihilated", free_col=free_col, rows=source.rows)


def _require_free_slot(vector: list[Fraction], free_col: int, other: int) -> None:
    if other == free_col:
        if vector[free_col] != Fraction(1):
            raise _fail("kernel free coordinate is not one", free_col=free_col)
        return
    if vector[other] != Fraction(0):
        raise _fail("kernel vectors are not independent", free_col=free_col, other=other)


def _require_one_vector(vector: list[Fraction], free_cols: Sequence[int], free_col: int) -> None:
    for other in free_cols:
        _require_free_slot(vector, free_col, other)


def _require_kernel(source: ExactMatrix, kernel: list[list[Fraction]], pivots: Sequence[int]) -> None:
    free_cols = _free_columns(source.cols, pivots)
    if len(kernel) != len(free_cols):
        raise _fail("kernel count is not the nullity", kernel=len(kernel), nullity=len(free_cols))
    for index, free_col in enumerate(free_cols):
        vector = kernel[index]
        _require_annihilator(source, vector, free_col)
        _require_one_vector(vector, free_cols, free_col)


def _require_rank_nullity(rank: int, nullity: int, columns: int) -> None:
    if rank + nullity != columns:
        raise _fail("rank plus nullity is not the column count", rank=rank, nullity=nullity, columns=columns)


def _one_column(image: ExactMatrix, col: int) -> tuple[Fraction, ...]:
    values: list[Fraction] = []
    for row in range(image.rows):
        values.append(_stored_fraction(image.get(row, col), "image"))
    return tuple(values)


def _column_tuples(image: ExactMatrix) -> tuple[tuple[Fraction, ...], ...]:
    columns: list[tuple[Fraction, ...]] = []
    for col in range(image.cols):
        columns.append(_one_column(image, col))
    return tuple(columns)


def rank_nullity_certificate(matrix: ExactMatrix) -> RankNullityCertificate:
    """Check image, kernel, and rank + nullity = columns for one rational matrix."""
    source = _rational_matrix(matrix)
    reduced, pivots = source.rref()
    _require_pivot_identity(reduced, pivots)
    image = _image_factor(source, pivots)
    coordinates = _coordinate_rows(reduced, len(pivots))
    _require_factorization(source, image, coordinates)
    kernel = _kernel_vectors(coordinates, pivots)
    _require_kernel(source, kernel, pivots)
    rank = len(pivots)
    nullity = len(kernel)
    _require_rank_nullity(rank, nullity, source.cols)
    return RankNullityCertificate(
        rank=rank,
        nullity=nullity,
        columns=source.cols,
        image=_column_tuples(image),
        kernel=tuple(tuple(vector) for vector in kernel),
    )


def image_basis(matrix: ExactMatrix) -> list[list[Fraction]]:
    """Return the checked pivot-column basis of the column space."""
    certificate = rank_nullity_certificate(matrix)
    return [list(column) for column in certificate.image]


def kernel_basis(matrix: ExactMatrix) -> list[list[Fraction]]:
    """Return the checked kernel basis, one vector per free column."""
    certificate = rank_nullity_certificate(matrix)
    return [list(vector) for vector in certificate.kernel]


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "ImageKernelError",
    "MatrixError",
    "RankNullityCertificate",
    "image_basis",
    "kernel_basis",
    "rank_nullity_certificate",
]
