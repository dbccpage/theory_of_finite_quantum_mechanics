"""Exact finite models of free alternatives, signed completion, and tensors."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping


def _clean(values: Mapping[str, int]) -> dict[str, int]:
    result: dict[str, int] = {}
    for key, value in values.items():
        if not isinstance(key, str) or not key:
            raise ValueError("generator names must be nonempty strings")
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("coefficients must be exact integers")
        if value:
            result[key] = value
    return dict(sorted(result.items()))


def _coefficients(values: Mapping[str, int]) -> dict[str, int]:
    result: dict[str, int] = {}
    for key, value in values.items():
        if not isinstance(key, str) or not key:
            raise ValueError("generator names must be nonempty strings")
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("coefficients must be exact integers")
        result[key] = value
    return dict(sorted(result.items()))


def alternative_counts(word: Iterable[str]) -> dict[str, int]:
    """The free-commutative image of a finite word."""

    items = tuple(word)
    if any(not isinstance(item, str) or not item for item in items):
        raise ValueError("generator names must be nonempty strings")
    return dict(sorted(Counter(items).items()))


def normalize_signed(positive: Iterable[str], negative: Iterable[str]) -> dict[str, int]:
    """Canonical integer coefficients of a positive/negative word pair."""

    result = Counter(alternative_counts(positive))
    result.subtract(alternative_counts(negative))
    return _clean(result)


def add_signed(left: Mapping[str, int], right: Mapping[str, int]) -> dict[str, int]:
    result = Counter(_clean(left))
    result.update(_clean(right))
    return _clean(result)


def negate_signed(value: Mapping[str, int]) -> dict[str, int]:
    return _clean({key: -coefficient for key, coefficient in _clean(value).items()})


def fold_signed(value: Mapping[str, int], generator_values: Mapping[str, int]) -> int:
    vector = _clean(value)
    weights = _coefficients(generator_values)
    missing = set(vector) - set(weights)
    if missing:
        raise ValueError(f"missing generator values: {sorted(missing)}")
    return sum(coefficient * weights[key] for key, coefficient in vector.items())


def tensor_product(
    left: Mapping[str, int], right: Mapping[str, int]
) -> dict[str, int]:
    """Sparse integer coordinates on generator pairs, encoded as `left|right`."""

    lhs = _clean(left)
    rhs = _clean(right)
    if any("|" in key for key in (*left, *right)):
        raise ValueError("tensor generator names must not contain the reserved | separator")
    return _clean(
        {
            f"{x}|{y}": a * b
            for x, a in lhs.items()
            for y, b in rhs.items()
            if a * b
        }
    )


def bilinear_value(
    left: Mapping[str, int],
    right: Mapping[str, int],
    basis_values: Mapping[str, int],
) -> int:
    """Evaluate the unique factor on the tensor coordinates."""

    tensor = tensor_product(left, right)
    coefficients = _coefficients(basis_values)
    missing = set(tensor) - set(coefficients)
    if missing:
        raise ValueError(f"missing pair values: {sorted(missing)}")
    return sum(value * coefficients[pair] for pair, value in tensor.items())


def determinant_2x2(
    value: Mapping[str, int], rows: tuple[str, str], columns: tuple[str, str]
) -> int:
    if len(rows) != 2 or len(columns) != 2 or len(set(rows)) != 2 or len(set(columns)) != 2:
        raise ValueError("two distinct row and column names are required")
    if any(type(key) is not str or not key or "|" in key for key in (*rows, *columns)):
        raise ValueError("invalid tensor generator name")
    matrix = _clean(value)
    a = matrix.get(f"{rows[0]}|{columns[0]}", 0)
    b = matrix.get(f"{rows[0]}|{columns[1]}", 0)
    c = matrix.get(f"{rows[1]}|{columns[0]}", 0)
    d = matrix.get(f"{rows[1]}|{columns[1]}", 0)
    return a * d - b * c
