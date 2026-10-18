"""Exact Cayley charts over Q(i) and the integer 2x2 Cayley isometry.

Origin: lean4/H019RationalLieSpan.lean theorem cayley_isometry_matrix2x2_rat
and theorem cayley_mat2_off_diagonal_zero. cayleyMat2(p, q) is the integer
matrix with diagonal q^2 - p^2 and off-diagonal entries ∓2pq.
Claim: urn:omega:fqm:lie:cayley-mat2-isometry:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/lie_theory/test_cayley_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: cayley_mat2_isometry_witness checks the four rational samples
(p, q) = (1, 1), (1, 2), (3, 4), (2, 1). The Q(i) chart
U = (I - i tau H)(I + i tau H)^{-1} is exact arithmetic for Hermitian
samples such as Pauli Z. This file does not prove the so(8) isometry.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class CayleyError(ValueError):
    """One violated Cayley invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CayleyError:
    return CayleyError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the Cayley boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, tuple):
        return _pair_fraction(value, role)
    if isinstance(value, float):
        raise _fail("float refused at the Cayley boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _pair_fraction(value: tuple[object, ...], role: str) -> Fraction:
    if len(value) != 2:
        raise _fail("rational pair does not have two entries", role=role, length=len(value))
    numerator = _require_int(value[0], role)
    denominator = _require_int(value[1], role)
    if denominator == 0:
        raise _fail("rational denominator is zero", role=role)
    return Fraction(numerator, denominator)


@dataclass(frozen=True)
class ComplexRational:
    """Exact element a + b i of Q(i)."""

    re: Fraction
    im: Fraction

    def __init__(self, re: object = 0, im: object = 0) -> None:
        object.__setattr__(self, "re", _require_fraction(re, "real part"))
        object.__setattr__(self, "im", _require_fraction(im, "imaginary part"))

    def __add__(self, other: ComplexRational) -> ComplexRational:
        partner = _require_complex(other, "addend")
        return ComplexRational(self.re + partner.re, self.im + partner.im)

    def __sub__(self, other: ComplexRational) -> ComplexRational:
        partner = _require_complex(other, "subtrahend")
        return ComplexRational(self.re - partner.re, self.im - partner.im)

    def __mul__(self, other: ComplexRational) -> ComplexRational:
        partner = _require_complex(other, "factor")
        real = self.re * partner.re - self.im * partner.im
        imag = self.re * partner.im + self.im * partner.re
        return ComplexRational(real, imag)

    def __truediv__(self, other: ComplexRational) -> ComplexRational:
        partner = _require_complex(other, "divisor")
        denom = partner.re * partner.re + partner.im * partner.im
        if denom == 0:
            raise _fail("complex divisor is zero")
        real = (self.re * partner.re + self.im * partner.im) / denom
        imag = (self.im * partner.re - self.re * partner.im) / denom
        return ComplexRational(real, imag)

    def conjugate(self) -> ComplexRational:
        return ComplexRational(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ComplexRational):
            return False
        return self.re == other.re and self.im == other.im

    def __hash__(self) -> int:
        return hash((self.re, self.im))

    @classmethod
    def zero(cls) -> ComplexRational:
        return cls(0, 0)

    @classmethod
    def one(cls) -> ComplexRational:
        return cls(1, 0)

    @classmethod
    def i(cls) -> ComplexRational:
        return cls(0, 1)


def _require_complex(value: object, role: str) -> ComplexRational:
    if isinstance(value, ComplexRational):
        return value
    raise _fail("value is not a complex rational", role=role, received=type(value).__name__)


class ComplexMatrix:
    """Matrix with entries in Q(i)."""

    def __init__(self, rows: object, cols: object, data: Sequence[Sequence[object]]) -> None:
        parsed = _parse_complex_matrix(data)
        self.rows = _require_shape(rows, len(parsed), "rows")
        self.cols = _require_shape(cols, _row_width(parsed), "cols")
        self._data = parsed

    @classmethod
    def identity(cls, dim: object) -> ComplexMatrix:
        width = _require_positive(dim, "dimension")
        return cls(width, width, _complex_identity(width))

    @classmethod
    def zero(cls, rows: object, cols: object) -> ComplexMatrix:
        height = _require_positive(rows, "rows")
        width = _require_positive(cols, "cols")
        return cls(height, width, _complex_zero(height, width))

    def __getitem__(self, index: object) -> list[ComplexRational]:
        row = _require_int(index, "row")
        if row < 0 or row >= self.rows:
            raise _fail("matrix row is outside the matrix", row=row, rows=self.rows)
        return list(self._data[row])

    def add(self, other: ComplexMatrix) -> ComplexMatrix:
        partner = _same_shape(self, other)
        return ComplexMatrix(self.rows, self.cols, _entrywise(self, partner, _add_entry))

    def sub(self, other: ComplexMatrix) -> ComplexMatrix:
        partner = _same_shape(self, other)
        return ComplexMatrix(self.rows, self.cols, _entrywise(self, partner, _sub_entry))

    def scale(self, scalar: object) -> ComplexMatrix:
        factor = _require_complex(scalar, "scalar")
        return ComplexMatrix(self.rows, self.cols, _scale_data(self, factor))

    def multiply(self, other: ComplexMatrix) -> ComplexMatrix:
        partner = _require_complex_matrix(other, "factor")
        if self.cols != partner.rows:
            raise _fail("matrix shapes do not match", left=self.cols, right=partner.rows)
        return ComplexMatrix(self.rows, partner.cols, _multiply_data(self, partner))

    def dagger(self) -> ComplexMatrix:
        return ComplexMatrix(self.cols, self.rows, _conjugate_transpose(self))

    def is_hermitian(self) -> bool:
        if self.rows != self.cols:
            return False
        return _entries_match(self._data, self.dagger()._data)

    def is_unitary(self) -> bool:
        if self.rows != self.cols:
            return False
        return _entries_match(self.multiply(self.dagger())._data, ComplexMatrix.identity(self.rows)._data)

    def inverse(self) -> ComplexMatrix:
        if self.rows != self.cols:
            raise _fail("only a square matrix can be inverted", rows=self.rows, cols=self.cols)
        return ComplexMatrix(self.rows, self.cols, _invert_complex(self._data))


def _require_positive(value: object, role: str) -> int:
    number = _require_int(value, role)
    if number <= 0:
        raise _fail("dimension is not positive", role=role, value=number)
    return number


def _require_shape(declared: object, actual: int, role: str) -> int:
    number = _require_int(declared, role)
    if number != actual:
        raise _fail("declared matrix shape does not match the entries", role=role, declared=number, actual=actual)
    return number


def _row_width(data: tuple[tuple[ComplexRational, ...], ...]) -> int:
    if not data:
        return 0
    return len(data[0])


def _parse_complex_matrix(data: Sequence[Sequence[object]]) -> tuple[tuple[ComplexRational, ...], ...]:
    if isinstance(data, (str, bytes)) or not isinstance(data, (list, tuple)) or len(data) == 0:
        raise _fail("complex matrix is not a nonempty row sequence", received=type(data).__name__)
    rows = tuple(_parse_complex_row(item, index) for index, item in enumerate(data))
    width = len(rows[0])
    for row in rows:
        if len(row) != width:
            raise _fail("complex matrix rows have different widths", expected=width, received=len(row))
    return rows


def _parse_complex_row(item: object, index: int) -> tuple[ComplexRational, ...]:
    if isinstance(item, (str, bytes)) or not isinstance(item, (list, tuple)) or len(item) == 0:
        raise _fail("complex matrix row is empty", index=index)
    parsed: list[ComplexRational] = []
    for column, entry in enumerate(item):
        parsed.append(_as_complex(entry, f"entry[{index},{column}]"))
    return tuple(parsed)


def _as_complex(entry: object, role: str) -> ComplexRational:
    if isinstance(entry, ComplexRational):
        return entry
    return ComplexRational(_require_fraction(entry, role), 0)


def _complex_identity(width: int) -> tuple[tuple[ComplexRational, ...], ...]:
    rows: list[tuple[ComplexRational, ...]] = []
    for row in range(width):
        rows.append(tuple(ComplexRational.one() if row == col else ComplexRational.zero() for col in range(width)))
    return tuple(rows)


def _complex_zero(rows: int, cols: int) -> tuple[tuple[ComplexRational, ...], ...]:
    return tuple(tuple(ComplexRational.zero() for _column in range(cols)) for _row in range(rows))


def _require_complex_matrix(value: object, role: str) -> ComplexMatrix:
    if isinstance(value, ComplexMatrix):
        return value
    raise _fail("value is not a complex matrix", role=role, received=type(value).__name__)


def _same_shape(left: ComplexMatrix, right: object) -> ComplexMatrix:
    partner = _require_complex_matrix(right, "partner")
    if left.rows != partner.rows or left.cols != partner.cols:
        raise _fail("matrix shapes differ", left_rows=left.rows, right_rows=partner.rows)
    return partner


def _add_entry(left: ComplexRational, right: ComplexRational) -> ComplexRational:
    return left + right


def _sub_entry(left: ComplexRational, right: ComplexRational) -> ComplexRational:
    return left - right


def _entrywise(left: ComplexMatrix, right: ComplexMatrix, combine: object) -> tuple[tuple[ComplexRational, ...], ...]:
    if not callable(combine):
        raise _fail("entry combination is not callable")
    rows: list[tuple[ComplexRational, ...]] = []
    for row in range(left.rows):
        rows.append(tuple(combine(left._data[row][col], right._data[row][col]) for col in range(left.cols)))
    return tuple(rows)


def _scale_data(matrix: ComplexMatrix, factor: ComplexRational) -> tuple[tuple[ComplexRational, ...], ...]:
    return tuple(tuple(entry * factor for entry in row) for row in matrix._data)


def _multiply_data(left: ComplexMatrix, right: ComplexMatrix) -> tuple[tuple[ComplexRational, ...], ...]:
    rows: list[tuple[ComplexRational, ...]] = []
    for row in range(left.rows):
        rows.append(_multiply_row(left, right, row))
    return tuple(rows)


def _multiply_row(left: ComplexMatrix, right: ComplexMatrix, row: int) -> tuple[ComplexRational, ...]:
    return tuple(_dot(left, right, row, col) for col in range(right.cols))


def _dot(left: ComplexMatrix, right: ComplexMatrix, row: int, col: int) -> ComplexRational:
    total = ComplexRational.zero()
    for index in range(left.cols):
        total = total + left._data[row][index] * right._data[index][col]
    return total


def _conjugate_transpose(matrix: ComplexMatrix) -> tuple[tuple[ComplexRational, ...], ...]:
    rows: list[tuple[ComplexRational, ...]] = []
    for col in range(matrix.cols):
        rows.append(tuple(matrix._data[row][col].conjugate() for row in range(matrix.rows)))
    return tuple(rows)


def _entries_match(
    left: tuple[tuple[ComplexRational, ...], ...],
    right: tuple[tuple[ComplexRational, ...], ...],
) -> bool:
    return left == right


def _invert_complex(data: tuple[tuple[ComplexRational, ...], ...]) -> tuple[tuple[ComplexRational, ...], ...]:
    width = len(data)
    augmented = _augment(data)
    for col in range(width):
        _eliminate(augmented, col, width)
    return tuple(tuple(row[width:]) for row in augmented)


def _augment(data: tuple[tuple[ComplexRational, ...], ...]) -> list[list[ComplexRational]]:
    return [_augment_row(row, index, len(data)) for index, row in enumerate(data)]


def _augment_row(row: tuple[ComplexRational, ...], index: int, width: int) -> list[ComplexRational]:
    copied = list(row)
    for col in range(width):
        copied.append(ComplexRational.one() if col == index else ComplexRational.zero())
    return copied


def _eliminate(augmented: list[list[ComplexRational]], col: int, width: int) -> None:
    pivot = _pivot(augmented, col, width)
    if pivot < 0:
        raise _fail("complex matrix is singular", column=col)
    augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
    _scale(augmented[col], col, width + width)
    _clear(augmented, col, width)


def _pivot(augmented: list[list[ComplexRational]], col: int, width: int) -> int:
    for row in range(col, width):
        if augmented[row][col] != ComplexRational.zero():
            return row
    return -1


def _scale(row: list[ComplexRational], col: int, span: int) -> None:
    scale = row[col]
    if scale == ComplexRational.zero():
        raise _fail("complex pivot is zero", column=col)
    for index in range(span):
        row[index] = row[index] / scale


def _clear(augmented: list[list[ComplexRational]], col: int, width: int) -> None:
    for row in range(width):
        if row != col:
            _clear_one(augmented[row], augmented[col], col, width + width)


def _clear_one(row: list[ComplexRational], pivot: list[ComplexRational], col: int, span: int) -> None:
    factor = row[col]
    if factor == ComplexRational.zero():
        return
    for index in range(span):
        row[index] = row[index] - factor * pivot[index]


def cayley_unitary(generator: object, tau: object = 1) -> ComplexMatrix:
    """Return U = (I - i tau H) (I + i tau H)^{-1}."""
    hermitian = _require_hermitian(generator)
    step = _require_fraction(tau, "tau")
    scaled = hermitian.scale(ComplexRational(0, step))
    identity = ComplexMatrix.identity(hermitian.rows)
    return identity.sub(scaled).multiply(identity.add(scaled).inverse())


def cayley_generator(unitary: object) -> ComplexMatrix:
    """Return H = i (U - I) (U + I)^{-1}."""
    value = _require_unitary(unitary)
    identity = ComplexMatrix.identity(value.rows)
    return value.sub(identity).multiply(value.add(identity).inverse()).scale(ComplexRational.i())


def _require_hermitian(value: object) -> ComplexMatrix:
    matrix = _require_complex_matrix(value, "generator")
    if not matrix.is_hermitian():
        raise _fail("Cayley generator is not Hermitian")
    return matrix


def _require_unitary(value: object) -> ComplexMatrix:
    matrix = _require_complex_matrix(value, "unitary")
    if not matrix.is_unitary():
        raise _fail("Cayley unitary is not unitary")
    return matrix


def pauli_matrices() -> tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]:
    """Return sigma_x, sigma_y, and sigma_z."""
    sigma_x = ComplexMatrix(2, 2, (
        (ComplexRational(0), ComplexRational(1)),
        (ComplexRational(1), ComplexRational(0)),
    ))
    sigma_y = ComplexMatrix(2, 2, (
        (ComplexRational(0), ComplexRational(0, -1)),
        (ComplexRational(0, 1), ComplexRational(0)),
    ))
    sigma_z = ComplexMatrix(2, 2, (
        (ComplexRational(1), ComplexRational(0)),
        (ComplexRational(0), ComplexRational(-1)),
    ))
    return sigma_x, sigma_y, sigma_z


@dataclass(frozen=True)
class Mat2Int:
    """Integer 2x2 matrix used by the Cayley numerator."""

    m00: int
    m01: int
    m10: int
    m11: int


def cayley_mat2(p_value: object, q_value: object) -> Mat2Int:
    """Return the Lean cayleyMat2 numerator."""
    p = _require_int(p_value, "p")
    q = _require_int(q_value, "q")
    diagonal = q * q - p * p
    off = 2 * p * q
    return Mat2Int(diagonal, -off, off, diagonal)


def cayley_denom(p_value: object, q_value: object) -> int:
    p = _require_int(p_value, "p")
    q = _require_int(q_value, "q")
    return p * p + q * q


def _mat_mul(left: Mat2Int, right: Mat2Int) -> Mat2Int:
    return Mat2Int(
        left.m00 * right.m00 + left.m01 * right.m10,
        left.m00 * right.m01 + left.m01 * right.m11,
        left.m10 * right.m00 + left.m11 * right.m10,
        left.m10 * right.m01 + left.m11 * right.m11,
    )


def _transpose(matrix: Mat2Int) -> Mat2Int:
    return Mat2Int(matrix.m00, matrix.m10, matrix.m01, matrix.m11)


def _smul_id(scale: int) -> Mat2Int:
    return Mat2Int(scale, 0, 0, scale)


def cayley_mat2_defect(p_value: object, q_value: object) -> int:
    """Return 0 when C^T C equals denom(p, q)^2 I and the off-diagonal entries vanish."""
    matrix = cayley_mat2(p_value, q_value)
    product = _mat_mul(_transpose(matrix), matrix)
    scale = cayley_denom(p_value, q_value)
    expected = _smul_id(scale * scale)
    if product != expected:
        raise _fail("Cayley 2x2 isometry failed", p=p_value, q=q_value)
    if product.m01 != 0 or product.m10 != 0:
        raise _fail("Cayley 2x2 off-diagonal is nonzero", m01=product.m01, m10=product.m10)
    return 0


def cayley_mat2_isometry_witness() -> int:
    """Return 0 on the four samples proved in cayley_isometry_matrix2x2_rat."""
    samples = ((1, 1), (1, 2), (3, 4), (2, 1))
    for p_value, q_value in samples:
        cayley_mat2_defect(p_value, q_value)
    return 0


def main() -> int:
    """Print the integer Cayley isometry certificate."""
    try:
        print(cayley_mat2_isometry_witness())
    except CayleyError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
