from __future__ import annotations
"""
basic_matrix.py

Numeric realization substrate (row-major dense matrix).

WARNING
-------
This module is a pure numeric backend. It must remain free of:
- mathematical meaning or invariants
- basis choices or identity semantics
- topology, category, or homological concepts

All semantics enter strictly above this module via realization, basis choice,
change-of-basis, packet compilation, verification, terminalization, etc.

The class below is intentionally boring: shape checks, row-major storage,
bounds checks, allocation limits, and arithmetic replay.
"""


from dataclasses import dataclass
from typing import Any, Callable, Generic, Iterable, Iterator, Optional, Protocol, Sequence, TypeVar, cast, runtime_checkable
import sys

T = TypeVar("T")
U = TypeVar("U")

MAX_USIZE = sys.maxsize



class MatrixError(Exception):
    """Base class for numeric matrix storage errors."""


@dataclass(frozen=True)
class NegativeDimension(MatrixError):
    rows: int
    cols: int

    def __str__(self) -> str:
        return f"Matrix dimensions must be nonnegative, got {self.rows}x{self.cols}"


@dataclass(frozen=True)
class DimensionOverflow(MatrixError):
    rows: int
    cols: int

    def __str__(self) -> str:
        return f"Matrix dimension {self.rows}x{self.cols} overflowed usize"


@dataclass(frozen=True)
class IndexOverflow(MatrixError):
    row: int
    col: int
    cols: int

    def __str__(self) -> str:
        return f"Matrix index ({self.row}, {self.col}) with {self.cols} columns overflowed"


@dataclass(frozen=True)
class ShapeMismatch(MatrixError):
    rows: int
    cols: int
    length: int

    def __str__(self) -> str:
        return f"Data length {self.length} does not match matrix shape {self.rows}x{self.cols}"


@dataclass(frozen=True)
class DimensionMismatch(MatrixError):
    left: tuple[int, int]
    right: tuple[int, int]

    def __str__(self) -> str:
        return f"Dimension mismatch: {self.left} vs {self.right}"


@dataclass(frozen=True)
class IndexOutOfBounds(MatrixError):
    row: int
    col: int
    rows: int
    cols: int

    def __str__(self) -> str:
        return f"Index ({self.row}, {self.col}) is out of bounds for {self.rows}x{self.cols} matrix"


@dataclass(frozen=True)
class AllocationLimitExceeded(MatrixError):
    requested: int
    limit: int

    def __str__(self) -> str:
        return f"Allocation limit exceeded: requested {self.requested}, limit {self.limit}"


@dataclass(frozen=True)
class InvalidOperation(MatrixError):
    message: str

    def __str__(self) -> str:
        return f"Invalid operation: {self.message}"


class CheckedMatrixError(Exception):
    """Base class for checked matrix operation failures."""


@dataclass(frozen=True)
class CheckedMatrixStructureError(CheckedMatrixError):
    error: MatrixError

    def __str__(self) -> str:
        return f"Matrix error: {self.error}"


@dataclass(frozen=True)
class CheckedMatrixScalarError(CheckedMatrixError):
    error: BaseException

    def __str__(self) -> str:
        return f"Scalar arithmetic error: {self.error}"



@runtime_checkable
class CheckedNumeric(Protocol):
    """Protocol for audit-grade scalar arithmetic.

    Scalars implementing this protocol provide fallible arithmetic methods.
    Python's built-in ``int`` is arbitrary precision, so ordinary ``add``/``mul``
    is usually sufficient for integer audit work. This protocol is for wrappers
    that want bounded or domain-specific scalar failures.
    """

    @classmethod
    def zero(cls) -> Any: ...

    def checked_add(self, rhs: Any) -> Any: ...
    def checked_sub(self, rhs: Any) -> Any: ...
    def checked_mul(self, rhs: Any) -> Any: ...


@dataclass(frozen=True)
class FlatIndex:
    """Opaque flat index. Prevents accidental coordinate semantics."""

    value: int



def checked_len(rows: int, cols: int) -> int:
    """Return rows * cols with usize-like validation."""
    if rows < 0 or cols < 0:
        raise NegativeDimension(rows, cols)
    total = rows * cols
    if total > MAX_USIZE:
        raise DimensionOverflow(rows, cols)
    return total


def _ensure_limit(requested: int, limit: int) -> None:
    if limit < 0:
        raise AllocationLimitExceeded(requested=requested, limit=limit)
    if requested > limit:
        raise AllocationLimitExceeded(requested=requested, limit=limit)


def _default_zero_like(example: Any = None) -> Any:
    """Default zero scalar.

    This deliberately returns ``0`` rather than inferring algebraic structure.
    Callers needing rationals, decimals, or wrappers should pass an explicit
    ``zero`` value or ``zero_factory``.
    """
    return 0



@dataclass(eq=True)
class BasicMatrix(Generic[T]):
    """Dense row-major numeric matrix.

    No mathematical meaning is implied. This is storage plus numeric replay.
    """

    rows: int
    cols: int
    data: list[T]

    def __post_init__(self) -> None:
        expected = checked_len(self.rows, self.cols)
        if len(self.data) != expected:
            raise ShapeMismatch(self.rows, self.cols, len(self.data))
        self.data = list(self.data)


    @classmethod
    def from_row_major(cls, rows: int, cols: int, data: Iterable[T]) -> "BasicMatrix[T]":
        values = list(data)
        expected = checked_len(rows, cols)
        if len(values) != expected:
            raise ShapeMismatch(rows, cols, len(values))
        return cls(rows, cols, values)

    @classmethod
    def from_row_major_with_limit(
        cls,
        rows: int,
        cols: int,
        data: Iterable[T],
        limit: int,
    ) -> "BasicMatrix[T]":
        expected = checked_len(rows, cols)
        _ensure_limit(expected, limit)
        return cls.from_row_major(rows, cols, data)

    @classmethod
    def from_fn(cls, rows: int, cols: int, f: Callable[[int, int], T]) -> "BasicMatrix[T]":
        checked_len(rows, cols)
        return cls(rows, cols, [f(r, c) for r in range(rows) for c in range(cols)])

    @classmethod
    def from_fn_with_limit(
        cls,
        rows: int,
        cols: int,
        limit: int,
        f: Callable[[int, int], T],
    ) -> "BasicMatrix[T]":
        length = checked_len(rows, cols)
        _ensure_limit(length, limit)
        return cls.from_fn(rows, cols, f)

    @classmethod
    def zero(
        cls,
        rows: int,
        cols: int,
        *,
        zero: Optional[T] = None,
        zero_factory: Optional[Callable[[], T]] = None,
    ) -> "BasicMatrix[T]":
        """Create a zero matrix of the specified shape.

        WARNING: If a mutable scalar object is passed as `zero`, the same object reference
        will be duplicated across all entries. For mutable scalar objects, provide a
        `zero_factory` instead to generate a unique instance for each entry.
        """
        length = checked_len(rows, cols)
        if zero_factory is not None:
            data = [zero_factory() for _ in range(length)]
        else:
            z = _default_zero_like() if zero is None else zero
            data = [z for _ in range(length)]
        return cls(rows, cols, data)


    def shape(self) -> tuple[int, int]:
        return (self.rows, self.cols)

    def nrows(self) -> int:
        return self.rows

    def ncols(self) -> int:
        return self.cols

    def as_list(self) -> list[T]:
        """Return a copy of the row-major data."""
        return list(self.data)

    def as_tuple(self) -> tuple[T, ...]:
        return tuple(self.data)

    def iter_row_major(self) -> Iterator[T]:
        return iter(self.data)

    def to_nested(self) -> list[list[T]]:
        return [self.data[r * self.cols : (r + 1) * self.cols] for r in range(self.rows)]

    @classmethod
    def from_nested(cls, rows_data: Sequence[Sequence[T]]) -> "BasicMatrix[T]":
        rows = len(rows_data)
        cols = len(rows_data[0]) if rows else 0
        flat: list[T] = []
        for row in rows_data:
            if len(row) != cols:
                raise ShapeMismatch(rows, cols, sum(len(x) for x in rows_data))
            flat.extend(row)
        return cls.from_row_major(rows, cols, flat)

    def to_numpy(self, *, dtype: Any = None):
        import numpy as np
        return np.array(self.data, dtype=dtype).reshape((self.rows, self.cols))

    @classmethod
    def from_numpy(cls, array: Any) -> "BasicMatrix[Any]":
        arr = array
        if getattr(arr, "ndim", None) != 2:
            raise InvalidOperation(f"from_numpy expects a 2D array, got ndim={getattr(arr, 'ndim', None)}")
        rows, cols = int(arr.shape[0]), int(arr.shape[1])
        flat_data: list[Any] = []
        for r in range(rows):
            for c in range(cols):
                item = arr[r, c]
                flat_data.append(cast(Any, item.item()) if hasattr(item, "item") else cast(Any, item))
        return cls.from_row_major(rows, cols, flat_data)


    def _index(self, row: int, col: int) -> FlatIndex:
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            raise IndexOutOfBounds(row, col, self.rows, self.cols)
        base = row * self.cols
        idx = base + col
        if idx > MAX_USIZE:
            raise IndexOverflow(row, col, self.cols)
        return FlatIndex(idx)

    def get(self, row: int, col: int) -> T:
        return self.data[self._index(row, col).value]

    def set(self, row: int, col: int, value: T) -> None:
        self.data[self._index(row, col).value] = value

    def __getitem__(self, key: tuple[int, int]) -> T:
        row, col = key
        return self.get(row, col)

    def __setitem__(self, key: tuple[int, int], value: T) -> None:
        row, col = key
        self.set(row, col, value)


    def transpose(self) -> "BasicMatrix[T]":
        return BasicMatrix.from_fn(self.cols, self.rows, lambda r, c: self.get(c, r))

    def map(self, f: Callable[[T], U]) -> "BasicMatrix[U]":
        return BasicMatrix(self.rows, self.cols, [f(v) for v in self.data])

    def map_with_index(self, f: Callable[[int, int, T], U]) -> "BasicMatrix[U]":
        return BasicMatrix.from_fn(self.rows, self.cols, lambda r, c: f(r, c, self.get(r, c)))


    def add(self, rhs: "BasicMatrix[T]") -> "BasicMatrix[Any]":
        if self.shape() != rhs.shape():
            raise DimensionMismatch(self.shape(), rhs.shape())
        return BasicMatrix(self.rows, self.cols, [cast(Any, a + b) for a, b in zip(self.data, rhs.data)])

    def sub(self, rhs: "BasicMatrix[T]") -> "BasicMatrix[Any]":
        if self.shape() != rhs.shape():
            raise DimensionMismatch(self.shape(), rhs.shape())
        return BasicMatrix(self.rows, self.cols, [cast(Any, a - b) for a, b in zip(self.data, rhs.data)])

    def mul(self, rhs: "BasicMatrix[T]", *, zero: Any = 0) -> "BasicMatrix[Any]":
        if self.cols != rhs.rows:
            raise DimensionMismatch(self.shape(), rhs.shape())

        def entry(r: int, c: int) -> Any:
            acc: Any = zero
            for k in range(self.cols):
                prod: Any = self.get(r, k) * rhs.get(k, c)
                acc = acc + prod
            return acc

        return BasicMatrix.from_fn(self.rows, rhs.cols, entry)

    def mul_vec(self, vector: Sequence[T], *, zero: Any = 0) -> list[Any]:
        if self.cols != len(vector):
            raise DimensionMismatch(self.shape(), (len(vector), 1))
        out: list[Any] = []
        for r in range(self.rows):
            acc: Any = zero
            for c in range(self.cols):
                prod: Any = self.get(r, c) * vector[c]
                acc = acc + prod
            out.append(acc)
        return out

    def __add__(self, rhs: "BasicMatrix[T]") -> "BasicMatrix[Any]":
        return self.add(rhs)

    def __sub__(self, rhs: "BasicMatrix[T]") -> "BasicMatrix[Any]":
        return self.sub(rhs)

    def __matmul__(self, rhs: "BasicMatrix[T]") -> "BasicMatrix[Any]":
        return self.mul(rhs)


    @staticmethod
    def _checked_add_scalar(a: Any, b: Any) -> Any:
        try:
            return a.checked_add(b)
        except AttributeError:
            return a + b
        except Exception as exc:
            raise CheckedMatrixScalarError(exc) from exc

    @staticmethod
    def _checked_sub_scalar(a: Any, b: Any) -> Any:
        try:
            return a.checked_sub(b)
        except AttributeError:
            return a - b
        except Exception as exc:
            raise CheckedMatrixScalarError(exc) from exc

    @staticmethod
    def _checked_mul_scalar(a: Any, b: Any) -> Any:
        try:
            return a.checked_mul(b)
        except AttributeError:
            return a * b
        except Exception as exc:
            raise CheckedMatrixScalarError(exc) from exc

    @staticmethod
    def _zero_for_checked(example: Any = None, zero: Any = None) -> Any:
        if zero is not None:
            return zero
        if example is not None:
            example_type: type[Any] = type(example)
            if hasattr(example_type, "zero"):
                return example_type.zero()
        return 0

    def checked_add(self, rhs: "BasicMatrix[T]", *, limit: int = MAX_USIZE) -> "BasicMatrix[Any]":
        if self.shape() != rhs.shape():
            raise CheckedMatrixStructureError(DimensionMismatch(self.shape(), rhs.shape()))
        _ensure_limit(len(self.data), limit)
        try:
            return BasicMatrix(self.rows, self.cols, [self._checked_add_scalar(a, b) for a, b in zip(self.data, rhs.data)])
        except MatrixError as exc:
            raise CheckedMatrixStructureError(exc) from exc

    def checked_sub(self, rhs: "BasicMatrix[T]", *, limit: int = MAX_USIZE) -> "BasicMatrix[Any]":
        if self.shape() != rhs.shape():
            raise CheckedMatrixStructureError(DimensionMismatch(self.shape(), rhs.shape()))
        _ensure_limit(len(self.data), limit)
        try:
            return BasicMatrix(self.rows, self.cols, [self._checked_sub_scalar(a, b) for a, b in zip(self.data, rhs.data)])
        except MatrixError as exc:
            raise CheckedMatrixStructureError(exc) from exc

    def checked_mul(
        self,
        rhs: "BasicMatrix[T]",
        *,
        limit: int = MAX_USIZE,
        zero: Any = None,
    ) -> "BasicMatrix[Any]":
        if self.cols != rhs.rows:
            raise CheckedMatrixStructureError(DimensionMismatch(self.shape(), rhs.shape()))
        requested = checked_len(self.rows, rhs.cols)
        _ensure_limit(requested, limit)

        example = self.data[0] if self.data else (rhs.data[0] if rhs.data else None)

        def entry(r: int, c: int) -> Any:
            acc = self._zero_for_checked(example, zero)
            for k in range(self.cols):
                prod = self._checked_mul_scalar(self.get(r, k), rhs.get(k, c))
                acc = self._checked_add_scalar(acc, prod)
            return acc

        try:
            return BasicMatrix.from_fn(self.rows, rhs.cols, entry)
        except MatrixError as exc:
            raise CheckedMatrixStructureError(exc) from exc

    def checked_mul_vec(
        self,
        vector: Sequence[T],
        *,
        limit: int = MAX_USIZE,
        zero: Any = None,
    ) -> list[Any]:
        if self.cols != len(vector):
            raise CheckedMatrixStructureError(DimensionMismatch(self.shape(), (len(vector), 1)))
        _ensure_limit(self.rows, limit)
        example = self.data[0] if self.data else (vector[0] if vector else None)
        out: list[Any] = []
        for r in range(self.rows):
            acc = self._zero_for_checked(example, zero)
            for c in range(self.cols):
                prod = self._checked_mul_scalar(self.get(r, c), vector[c])
                acc = self._checked_add_scalar(acc, prod)
            out.append(acc)
        return out


__all__ = [
    "BasicMatrix",
    "MatrixError",
    "NegativeDimension",
    "DimensionOverflow",
    "IndexOverflow",
    "ShapeMismatch",
    "DimensionMismatch",
    "IndexOutOfBounds",
    "AllocationLimitExceeded",
    "InvalidOperation",
    "CheckedNumeric",
    "CheckedMatrixError",
    "CheckedMatrixStructureError",
    "CheckedMatrixScalarError",
    "FlatIndex",
    "checked_len",
]


