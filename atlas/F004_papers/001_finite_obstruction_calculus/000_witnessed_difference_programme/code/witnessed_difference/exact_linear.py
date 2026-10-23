"""Exact linear algebra over Q and Q(i) with declared shapes.

A matrix is a tuple of rows over one declared field: ``Fraction`` entries for
Q and ``GaussianRational`` entries for Q(i).  Every routine receives the column
count, so zero-row and zero-column shapes stay unambiguous.  Hermitian
positivity is decided by exact congruence diagonalization: the certificate is a
basis t_1, ..., t_n and a rational diagonal D with t_j* M t_k = D_j [j = k],
which ``verify_congruence`` recomputes independently.  A negative diagonal
entry is itself a verified vector of negative energy.  Floats and bools are
refused at the boundary; nothing is rounded.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Mapping, Sequence

from .exact import as_fraction
from .outcomes import Accepted, Outcome, RefusalCode, Refused
from .projective import GaussianRational

Scalar = Fraction | GaussianRational
Vector = tuple[Scalar, ...]
Matrix = tuple[Vector, ...]


class ExactField(str, Enum):
    RATIONAL = "Q"
    GAUSSIAN = "Q(i)"


def constant(field: ExactField, value: int | Fraction) -> Scalar:
    """The field element ``value``; Q(i) embeds Q with zero imaginary part."""

    return Fraction(value) if field is ExactField.RATIONAL else GaussianRational(value)


def _scalar(value: object, field: ExactField) -> Scalar:
    if isinstance(value, GaussianRational):
        if field is ExactField.GAUSSIAN:
            return value
        raise TypeError("a Gaussian rational is not an element of Q")
    return constant(field, as_fraction(value))  # type: ignore[arg-type]


def _vector(values: object, field: ExactField) -> Vector:
    if isinstance(values, (str, bytes, Mapping)) or not isinstance(values, Sequence):
        raise TypeError("a vector is a sequence of exact scalars")
    return tuple(_scalar(value, field) for value in values)


def coerce_vector(values: object, length: int | None, field: ExactField) -> Outcome[Vector]:
    """Admit an exact vector of the declared length; floats and bools are refused."""

    try:
        vector = _vector(values, field)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"vector entries must be exact scalars: {error}")
    if length is not None and len(vector) != length:
        return Refused(RefusalCode.INVALID_INPUT, f"expected a vector of length {length}, got {len(vector)}")
    return Accepted(vector)


def coerce_matrix(
    rows: object,
    shape: tuple[int | None, int | None],
    field: ExactField,
) -> Outcome[Matrix]:
    """Admit a rectangular exact matrix whose shape matches every declared extent."""

    try:
        if isinstance(rows, (str, bytes, Mapping)) or not isinstance(rows, Sequence):
            raise TypeError("a matrix is a sequence of rows")
        matrix = tuple(_vector(row, field) for row in rows)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"matrix entries must be exact scalars: {error}")
    expected_rows, expected_columns = shape
    widths = {len(row) for row in matrix} | ({expected_columns} if expected_columns is not None else set())
    if len(widths) > 1 or (expected_rows is not None and len(matrix) != expected_rows):
        return Refused(
            RefusalCode.INVALID_INPUT,
            f"matrix shape does not match the declared {expected_rows} x {expected_columns} extent",
        )
    return Accepted(matrix)


def zero_matrix(rows: int, columns: int, field: ExactField) -> Matrix:
    zero = constant(field, 0)
    return tuple(tuple(zero for _ in range(columns)) for _ in range(rows))


def identity(size: int, field: ExactField) -> Matrix:
    zero, one = constant(field, 0), constant(field, 1)
    return tuple(tuple(one if i == j else zero for j in range(size)) for i in range(size))


def add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(tuple(a + b for a, b in zip(x, y)) for x, y in zip(left, right))


def subtract(left: Matrix, right: Matrix) -> Matrix:
    return tuple(tuple(a + (-b) for a, b in zip(x, y)) for x, y in zip(left, right))


def scale(matrix: Matrix, factor: Scalar) -> Matrix:
    return tuple(tuple(factor * entry for entry in row) for row in matrix)


def matmul(left: Matrix, right: Matrix, columns: int, field: ExactField) -> Matrix:
    """Exact product of a p x q and a q x ``columns`` matrix."""

    zero = constant(field, 0)
    return tuple(
        tuple(sum((entry * right[k][j] for k, entry in enumerate(row)), start=zero) for j in range(columns))
        for row in left
    )


def apply(matrix: Matrix, vector: Vector, field: ExactField) -> Vector:
    zero = constant(field, 0)
    return tuple(sum((a * b for a, b in zip(row, vector)), start=zero) for row in matrix)


def adjoint(matrix: Matrix, columns: int) -> Matrix:
    """Conjugate transpose; the transpose over Q."""

    return tuple(tuple(row[j].conjugate() for row in matrix) for j in range(columns))


def inner(left: Vector, right: Vector, field: ExactField) -> Scalar:
    """<left, right> = sum conj(left_j) right_j."""

    return sum((a.conjugate() * b for a, b in zip(left, right)), start=constant(field, 0))


def is_zero(matrix: Matrix, field: ExactField) -> bool:
    zero = constant(field, 0)
    return all(entry == zero for row in matrix for entry in row)


def row_reduce(matrix: Matrix, columns: int, field: ExactField) -> tuple[Matrix, tuple[int, ...]]:
    """Reduced row echelon form, pivoting only in the first ``columns`` columns."""

    zero = constant(field, 0)
    rows = [list(row) for row in matrix]
    pivots: list[int] = []
    for column in range(columns):
        rank = len(pivots)
        pivot = next((index for index in range(rank, len(rows)) if rows[index][column] != zero), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        lead = rows[rank][column]
        rows[rank] = [entry / lead for entry in rows[rank]]
        for index, row in enumerate(rows):
            factor = row[column]
            if index != rank and factor != zero:
                rows[index] = [a + (-(factor * b)) for a, b in zip(row, rows[rank])]
        pivots.append(column)
    return tuple(tuple(row) for row in rows), tuple(pivots)


def rank(matrix: Matrix, columns: int, field: ExactField) -> int:
    return len(row_reduce(matrix, columns, field)[1])


def kernel_basis(matrix: Matrix, columns: int, field: ExactField) -> tuple[Vector, ...]:
    """A basis of {x : M x = 0}, one vector per free column of the echelon form."""

    reduced, pivots = row_reduce(matrix, columns, field)
    zero, one = constant(field, 0), constant(field, 1)
    basis = []
    for free in (column for column in range(columns) if column not in pivots):
        vector = [zero] * columns
        vector[free] = one
        for row, pivot in zip(reduced, pivots):
            vector[pivot] = -row[free]
        basis.append(tuple(vector))
    return tuple(basis)


def solve(matrix: Matrix, rhs: Vector, columns: int, field: ExactField) -> Vector | None:
    """One exact solution of M x = rhs, or ``None`` when the system is inconsistent."""

    augmented = tuple(row + (value,) for row, value in zip(matrix, rhs))
    reduced, pivots = row_reduce(augmented, columns + 1, field)
    if columns in pivots:
        return None
    solution = [constant(field, 0)] * columns
    for row, pivot in zip(reduced, pivots):
        solution[pivot] = row[columns]
    return tuple(solution)


def inverse(matrix: Matrix, field: ExactField) -> Matrix | None:
    """The exact two-sided inverse of a square matrix, or ``None`` when singular."""

    size = len(matrix)
    augmented = tuple(row + unit for row, unit in zip(matrix, identity(size, field)))
    reduced, pivots = row_reduce(augmented, size, field)
    if len(pivots) < size:
        return None
    return tuple(row[size:] for row in reduced)


@dataclass(frozen=True)
class CongruenceCertificate:
    """``basis[j]`` is t_j; t_j* M t_k equals ``diagonal[j]`` when j = k and 0 otherwise."""

    field: ExactField
    matrix: Matrix
    basis: Matrix
    diagonal: tuple[Fraction, ...]

    @property
    def inertia(self) -> tuple[int, int, int]:
        """(positive, negative, zero) counts, which Sylvester's law makes basis-free."""

        positive = sum(value > 0 for value in self.diagonal)
        negative = sum(value < 0 for value in self.diagonal)
        return positive, negative, len(self.diagonal) - positive - negative

    @property
    def positive_semidefinite(self) -> bool:
        return all(value >= 0 for value in self.diagonal)

    @property
    def positive_definite(self) -> bool:
        return all(value > 0 for value in self.diagonal)

    def negative_vector(self) -> Vector | None:
        """A basis vector t with t* M t < 0, when one exists."""

        return next((vector for vector, value in zip(self.basis, self.diagonal) if value < 0), None)


def _energy(matrix: Matrix, left: Vector, right: Vector, field: ExactField) -> Scalar:
    return inner(left, apply(matrix, right, field), field)


def diagonalize_hermitian(matrix: Matrix, field: ExactField) -> CongruenceCertificate:
    """Congruence-diagonalize a square Hermitian matrix already admitted over ``field``.

    A nonzero diagonal energy is used as a pivot; when every remaining diagonal
    energy vanishes but some off-diagonal energy G_jk does not, t_j + conj(G_jk)
    t_k has energy 2|G_jk|^2 > 0 and becomes the next pivot.
    """

    size = len(matrix)
    zero = constant(field, 0)
    basis = [list(row) for row in identity(size, field)]
    remaining = list(range(size))
    diagonal = [Fraction(0)] * size
    while remaining:
        energies = {j: _energy(matrix, tuple(basis[j]), tuple(basis[j]), field) for j in remaining}
        pivot = next((j for j in remaining if energies[j] != zero), None)
        if pivot is None:
            pair = next(
                (
                    (j, k)
                    for j in remaining
                    for k in remaining
                    if j != k and _energy(matrix, tuple(basis[j]), tuple(basis[k]), field) != zero
                ),
                None,
            )
            if pair is None:
                break
            j, k = pair
            coefficient = _energy(matrix, tuple(basis[k]), tuple(basis[j]), field)
            basis[j] = [a + coefficient * b for a, b in zip(basis[j], basis[k])]
            continue
        remaining.remove(pivot)
        for other in remaining:
            coefficient = _energy(matrix, tuple(basis[pivot]), tuple(basis[other]), field) / energies[pivot]
            basis[other] = [a + (-(coefficient * b)) for a, b in zip(basis[other], basis[pivot])]
        diagonal[pivot] = energies[pivot].real
    return CongruenceCertificate(field, matrix, tuple(tuple(vector) for vector in basis), tuple(diagonal))


def congruence_diagonalize(rows: object, field: ExactField) -> Outcome[CongruenceCertificate]:
    """Admit a square Hermitian matrix and return its verified congruence certificate."""

    if not isinstance(field, ExactField):
        return Refused(RefusalCode.INVALID_INPUT, "the field must be declared as Q or Q(i)")
    admitted = coerce_matrix(rows, (None, None), field)
    if isinstance(admitted, Refused):
        return admitted
    matrix = admitted.value
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        return Refused(RefusalCode.INVALID_INPUT, "a Hermitian form needs a square matrix")
    if adjoint(matrix, size) != matrix:
        return Refused(RefusalCode.NOT_HERMITIAN, "the matrix is not equal to its conjugate transpose")
    return verify_congruence(diagonalize_hermitian(matrix, field))


def verify_congruence(certificate: CongruenceCertificate) -> Outcome[CongruenceCertificate]:
    """Recompute every t_j* M t_k and the rank of the basis; nothing is trusted."""

    if not isinstance(certificate, CongruenceCertificate) or not isinstance(certificate.field, ExactField):
        return Refused(RefusalCode.INVALID_INPUT, "not a congruence certificate")
    field, matrix, basis = certificate.field, certificate.matrix, certificate.basis
    scalar = GaussianRational if field is ExactField.GAUSSIAN else Fraction
    size = len(matrix)
    shaped = (
        type(matrix) is tuple
        and type(basis) is tuple
        and type(certificate.diagonal) is tuple
        and len(basis) == size
        and len(certificate.diagonal) == size
        and all(type(row) is tuple and len(row) == size for row in matrix + basis)
        and all(type(entry) is scalar for row in matrix + basis for entry in row)
        and all(type(value) is Fraction for value in certificate.diagonal)
    )
    if not shaped:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "certificate entries are not exact and square")
    for j in range(size):
        for k in range(size):
            expected = constant(field, certificate.diagonal[j] if j == k else 0)
            if _energy(matrix, basis[j], basis[k], field) != expected:
                return Refused(RefusalCode.CERTIFICATE_MISMATCH, f"t_{j}* M t_{k} differs from the diagonal")
    if rank(basis, size, field) != size:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the congruence basis is singular")
    return Accepted(certificate)


# Executable finite evidence; AuthorityEffect: None.
