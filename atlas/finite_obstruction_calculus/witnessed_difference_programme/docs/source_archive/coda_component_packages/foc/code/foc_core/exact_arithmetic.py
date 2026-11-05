"""Exact rational arithmetic, matrix conversions, float firewall, and hash digests.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e).
Self-contained: Zero external monorepo dependencies.
Constraint: Zero floating-point operations in exact algebraic decision paths.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Sequence
from fractions import Fraction
from typing import Any

from sympy import Basic, Matrix, Rational, simplify
from sympy.matrices.matrixbase import MatrixBase


def _as_exact_rational(value: Any) -> Rational:
    """Convert an exact scalar to SymPy Rational, rejecting floats and booleans."""
    if isinstance(value, bool):
        raise TypeError(f"exact arithmetic rejects bool; got {value!r}")
    if isinstance(value, float):
        raise TypeError(f"exact arithmetic rejects float; got {value!r}")
    if isinstance(value, int):
        return Rational(value, 1)
    if isinstance(value, Fraction):
        return Rational(value.numerator, value.denominator)
    if isinstance(value, Rational):
        return value
    if isinstance(value, str):
        return Rational(value)
    if hasattr(value, "is_Float") and value.is_Float:
        raise TypeError(f"exact arithmetic rejects SymPy Float; got {value!r}")
    if isinstance(value, Basic) and value.is_rational:
        return Rational(value)
    raise TypeError(f"exact arithmetic rejects {type(value).__name__}; use an exact scalar")


as_rational = _as_exact_rational


def _check_no_floats(obj: Any, context: str = "certificate") -> None:
    """Recursively verify that an object and all its elements contain zero floating-point values."""
    if obj is None:
        return
    if isinstance(obj, bool):
        raise TypeError(f"{context} rejects bool; got {obj!r}")
    if isinstance(obj, float):
        raise TypeError(
            f"Floating-point inputs are strictly prohibited ({context} got {obj!r}); "
            "use exact integers, fractions.Fraction, or sympy.Rational"
        )
    if hasattr(obj, "is_Float") and obj.is_Float:
        raise TypeError(
            f"Floating-point inputs are strictly prohibited ({context} got SymPy Float {obj!r}); "
            "use exact integers, fractions.Fraction, or sympy.Rational"
        )
    try:
        import numpy as np

        if isinstance(obj, (np.floating, np.complexfloating)):
            raise TypeError(
                f"Floating-point numpy inputs are strictly prohibited ({context} got {obj!r}); "
                "use exact integers, fractions.Fraction, or sympy.Rational"
            )
    except ImportError:
        pass
    if isinstance(obj, complex):
        raise TypeError(
            f"Floating-point complex inputs are strictly prohibited ({context} got {obj!r}); "
            "use exact integers, fractions.Fraction, or sympy.Rational"
        )
    if isinstance(obj, MatrixBase):
        for val in obj:
            _check_no_floats(val, context=f"{context} matrix entry")
        return
    if isinstance(obj, (list, tuple)):
        for item in obj:
            _check_no_floats(item, context=context)
        return
    if isinstance(obj, (int, Fraction, Rational)):
        return
    if isinstance(obj, str):
        return
    if isinstance(obj, Basic):
        for atom in obj.atoms():
            if hasattr(atom, "is_Float") and atom.is_Float:
                raise TypeError(
                    f"Floating-point inputs are strictly prohibited ({context} got SymPy Float atom {atom!r}); "
                    "use exact integers, fractions.Fraction, or sympy.Rational"
                )
            if isinstance(atom, float):
                raise TypeError(
                    f"Floating-point inputs are strictly prohibited ({context} got float atom {atom!r}); "
                    "use exact integers, fractions.Fraction, or sympy.Rational"
                )


def exact_matrix_from_matrix(value: MatrixBase) -> Matrix:
    """Copy a matrix through the exact rational scalar gate."""
    return Matrix(
        value.rows,
        value.cols,
        [_as_exact_rational(value[row, col]) for row in range(value.rows) for col in range(value.cols)],
    )


def exact_equal(left: MatrixBase, right: MatrixBase) -> bool:
    """Check exact mathematical equality between two matrices."""
    _check_no_floats(left, "exact_equal left")
    _check_no_floats(right, "exact_equal right")
    if left.shape != right.shape:
        return False
    diff = left - right
    return all(simplify(diff[r, c]) == 0 for r in range(diff.rows) for c in range(diff.cols))


def _exact_scalar(value: Any) -> Rational:
    _check_no_floats(value, "exact scalar")
    if isinstance(value, bool):
        raise TypeError("exact arithmetic rejects bool; use exact int, Fraction, or Rational")
    import numpy as np

    if isinstance(value, np.integer):
        return Rational(int(value))
    return _as_exact_rational(value)


def _exact_matrix(rows: Any) -> Matrix:
    if isinstance(rows, MatrixBase):
        _check_no_floats(rows, "exact matrix")
        return exact_matrix_from_matrix(rows)
    import numpy as np

    if isinstance(rows, np.ndarray):
        if np.issubdtype(rows.dtype, np.floating) or np.issubdtype(rows.dtype, np.complexfloating):
            raise TypeError("Floating-point numpy arrays are strictly prohibited; use exact scalars")
        if rows.ndim != 2:
            raise ValueError("all repair and defect maps must be matrices")
        r, c = rows.shape
        entries = [_exact_scalar(rows[i, j]) for i in range(r) for j in range(c)]
        return Matrix(r, c, entries)
    if isinstance(rows, (list, tuple)):
        if len(rows) == 0:
            return Matrix.zeros(0, 0)
        if not isinstance(rows[0], (list, tuple, Sequence)):
            raise ValueError("all repair and defect maps must be matrices")
        r = len(rows)
        c = len(rows[0])
        if any(len(row) != c for row in rows):
            raise ValueError("matrix rows must have equal length")
        entries = [_exact_scalar(val) for row in rows for val in row]
        return Matrix(r, c, entries)
    raise TypeError(f"unsupported matrix type: {type(rows)}")


def _exact_vector(values: Any) -> Matrix:
    if isinstance(values, MatrixBase):
        _check_no_floats(values, "exact vector")
        if (values.rows == 0 and values.cols <= 1) or (values.rows <= 1 and values.cols == 0):
            return Matrix.zeros(0, 1)
        if values.cols == 1:
            return exact_matrix_from_matrix(values)
        if values.rows == 1:
            return exact_matrix_from_matrix(values).T
        raise ValueError(f"expected vector, got matrix with shape {values.shape}")
    import numpy as np

    if isinstance(values, np.ndarray):
        if np.issubdtype(values.dtype, np.floating) or np.issubdtype(values.dtype, np.complexfloating):
            raise TypeError("Floating-point numpy arrays are strictly prohibited; use exact scalars")
        if values.ndim == 1:
            n = values.shape[0]
            if n == 0:
                return Matrix.zeros(0, 1)
            entries = [_exact_scalar(values[i]) for i in range(n)]
            return Matrix(n, 1, entries)
        if values.ndim == 2:
            r, c = values.shape
            if (r == 0 and c <= 1) or (r <= 1 and c == 0):
                return Matrix.zeros(0, 1)
            if c == 1:
                entries = [_exact_scalar(values[i, 0]) for i in range(r)]
                return Matrix(r, 1, entries)
            if r == 1:
                entries = [_exact_scalar(values[0, j]) for j in range(c)]
                return Matrix(c, 1, entries)
            raise ValueError(f"expected vector, got 2D array with shape {values.shape}")
        raise ValueError(f"expected 1D vector or explicit row/column vector, got {values.ndim}D array")
    if isinstance(values, (list, tuple)):
        if len(values) == 0:
            return Matrix.zeros(0, 1)
        if isinstance(values[0], (list, tuple)):
            if any(not isinstance(row, (list, tuple)) for row in values):
                raise ValueError("inconsistent nested sequence for vector")
            if all(len(row) == 1 for row in values):
                entries = [_exact_scalar(row[0]) for row in values]
                return Matrix(len(values), 1, entries)
            if len(values) == 1:
                entries = [_exact_scalar(val) for val in values[0]]
                return Matrix(len(values[0]), 1, entries)
            raise ValueError(
                f"expected vector, got 2D nested sequence with shape ({len(values)}, {len(values[0])})"
            )
        entries = [_exact_scalar(v) for v in values]
        return Matrix(len(values), 1, entries)
    if isinstance(values, Iterable):
        items = list(values)
        if len(items) == 0:
            return Matrix.zeros(0, 1)
        return _exact_vector(items)
    raise TypeError(f"unsupported vector type: {type(values)}")


def _digest_exact(label: str, *objects: Any) -> str:
    digest = hashlib.sha256()
    digest.update(label.encode("utf-8"))
    for obj in objects:
        if isinstance(obj, MatrixBase):
            digest.update(f"Matrix({obj.rows},{obj.cols}):".encode("ascii"))
            for val in obj:
                r = as_rational(val)
                digest.update(f"{r.p}/{r.q};".encode("ascii"))
        elif isinstance(obj, (int, Rational, Fraction)):
            r = as_rational(obj)
            digest.update(f"Scalar:{r.p}/{r.q};".encode("ascii"))
        elif isinstance(obj, str):
            digest.update(f"Str:{obj};".encode("utf-8"))
    return digest.hexdigest()


def _digest_strings(label: str, values: Iterable[str]) -> str:
    digest = hashlib.sha256(label.encode("utf-8"))
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)
