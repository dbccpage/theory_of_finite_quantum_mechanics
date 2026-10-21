"""Bounded exact-rational and shaped-matrix codecs for native adapters.

Claim: urn:omega:fqm:majorana:bounded-native-exact-codec:v1
AuthorityEffect: None.
Python performs exact rational normalization and shape admission here; native
owners perform the delegated linear algebra. No native execution is certified by
a successful codec call. Finite decimal/exponent text remains exact rational text.
"""
from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction
from sympy import Matrix, Rational
from sympy.matrices import ImmutableDenseMatrix, MutableDenseMatrix, ImmutableSparseMatrix, MutableSparseMatrix
from sympy.matrices.matrixbase import MatrixBase

ExactInput = int | str | Fraction | Rational
MAX_SCALAR_BITS = 1024
MAX_TEXT_CHARACTERS = 1024
MAX_DECIMAL_EXPONENT = 1024
MAX_WORK_BITS = 8192
MAX_DIMENSION = 1024
MAX_MATRIX_ENTRIES = 65536
MAX_LABEL_CHARACTERS = 256
_RATIONAL_TYPES = frozenset(type(Rational(a, b)) for a, b in [(0, 1), (1, 1), (-1, 1), (2, 1), (1, 2), (2, 3)])
_MATRIX_TYPES = frozenset([ImmutableDenseMatrix, MutableDenseMatrix, ImmutableSparseMatrix, MutableSparseMatrix])


def _bits(value: Fraction, limit: int) -> Fraction:
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > limit:
        raise ValueError("exact rational component bit budget exceeded")
    return value


def _text_atom(text: str) -> Fraction:
    pieces = text.lower().split("e")
    if len(pieces) > 2:
        raise ValueError("expected a finite exact rational")
    if len(pieces) == 2:
        exponent = int(pieces[1])
        if abs(exponent) > MAX_DECIMAL_EXPONENT:
            raise ValueError("exact decimal exponent budget exceeded")
    return _bits(Fraction(text), MAX_WORK_BITS)


def _text_fraction(value: str) -> Fraction:
    if len(value) > MAX_TEXT_CHARACTERS:
        raise ValueError("exact scalar text budget exceeded")
    parts = value.replace(" ", "").split("/")
    if len(parts) not in (1, 2):
        raise ValueError("expected a finite exact rational")
    try:
        result = _text_atom(parts[0])
        if len(parts) == 2:
            result /= _text_atom(parts[1])
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError("expected a finite exact rational within the declared text/exponent/work budgets") from error
    return _bits(result, MAX_SCALAR_BITS)


def as_rational(value: ExactInput) -> Rational:
    """Admit closed built-in/canonical SymPy values; never invoke sympify hooks."""
    kind = type(value)
    if kind is int:
        if value.bit_length() > MAX_SCALAR_BITS:
            raise ValueError("exact rational component bit budget exceeded")
        parsed = Fraction(value)
    elif kind is Fraction:
        parsed = _bits(value, MAX_SCALAR_BITS)
    elif kind is str:
        parsed = _text_fraction(value)
    elif kind in _RATIONAL_TYPES:
        numerator, denominator = value.p, value.q
        if type(numerator) is not int or type(denominator) is not int:
            raise TypeError("canonical SymPy rational must expose built-in integer components")
        if max(numerator.bit_length(), denominator.bit_length()) > MAX_SCALAR_BITS:
            raise ValueError("exact rational component bit budget exceeded")
        parsed = Fraction(numerator, denominator)
    else:
        raise TypeError("exact scalar must be a built-in int/str/Fraction or canonical SymPy Rational")
    return Rational(parsed.numerator, parsed.denominator)


def _label(value: object) -> str:
    if type(value) is not str:
        raise TypeError("diagnostic label must be a built-in string")
    if len(value) > MAX_LABEL_CHARACTERS:
        raise ValueError("diagnostic label budget exceeded")
    return value


def _matrix_shape(value: object) -> tuple[int, int]:
    if type(value) not in _MATRIX_TYPES:
        raise TypeError("expected a canonical exact SymPy dense or sparse matrix")
    rows, cols = value.rows, value.cols
    if type(rows) is not int or type(cols) is not int or rows < 0 or cols < 0:
        raise ValueError("matrix dimensions must be nonnegative integers")
    if max(rows, cols) > MAX_DIMENSION or rows * cols > MAX_MATRIX_ENTRIES:
        raise ValueError("native matrix shape budget exceeded")
    return rows, cols


def _vector_sequence(value: object) -> tuple:
    if type(value) not in (list, tuple, range):
        raise TypeError("exact vector must be a built-in list, tuple, range or canonical SymPy matrix")
    try:
        length = len(value)
    except OverflowError as error:
        raise ValueError("native vector length budget exceeded") from error
    if length > MAX_DIMENSION:
        raise ValueError("native vector length budget exceeded")
    return tuple(value)


def exact_vector(value: Sequence[ExactInput] | MatrixBase, *, label: str) -> Matrix:
    label = _label(label)
    if type(value) in _MATRIX_TYPES:
        rows, cols = _matrix_shape(value)
        if (rows, cols) in ((0, 0), (0, 1), (1, 0)):
            return Matrix(0, 1, [])
        if cols != 1:
            raise ValueError(f"{label} must be a column vector")
        entries = tuple(value)
    else:
        entries = _vector_sequence(value)
    parsed = [as_rational(item) for item in entries]
    return Matrix(len(parsed), 1, parsed)


def matrix_wire(value: MatrixBase) -> dict:
    rows, cols = _matrix_shape(value)
    return {"rows": rows, "cols": 0,
            "data": [[str(as_rational(value[row, col])) for col in range(cols)] for row in range(rows)]}
