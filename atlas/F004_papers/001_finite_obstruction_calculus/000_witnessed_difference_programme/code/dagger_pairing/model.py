"""Sparse exact-integer operations for dagger and observer-pairing witnesses."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence


def clean_vector(value: Mapping[str, int]) -> dict[str, int]:
    result: dict[str, int] = {}
    for key, coefficient in value.items():
        if not isinstance(key, str) or not key:
            raise ValueError("coordinate names must be nonempty strings")
        if isinstance(coefficient, bool) or not isinstance(coefficient, int):
            raise ValueError("coefficients must be exact integers")
        if coefficient:
            result[key] = coefficient
    return dict(sorted(result.items()))


def add(left: Mapping[str, int], right: Mapping[str, int]) -> dict[str, int]:
    result = Counter(clean_vector(left))
    result.update(clean_vector(right))
    return clean_vector(result)


def subtract(left: Mapping[str, int], right: Mapping[str, int]) -> dict[str, int]:
    result = Counter(clean_vector(left))
    result.subtract(clean_vector(right))
    return clean_vector(result)


def validate_involution(mapping: Mapping[str, str]) -> dict[str, str]:
    dagger = dict(mapping)
    if any(not isinstance(key, str) or not key for key in dagger):
        raise ValueError("dagger domain names must be nonempty strings")
    if any(not isinstance(value, str) or not value for value in dagger.values()):
        raise ValueError("dagger values must be nonempty strings")
    if set(dagger) != set(dagger.values()):
        raise ValueError("dagger must be a permutation of its declared carrier")
    if any(dagger[dagger[key]] != key for key in dagger):
        raise ValueError("dagger must be involutive")
    return dagger


def apply_dagger(value: Mapping[str, int], mapping: Mapping[str, str]) -> dict[str, int]:
    vector = clean_vector(value)
    dagger = validate_involution(mapping)
    missing = set(vector) - set(dagger)
    if missing:
        raise ValueError(f"dagger is missing coordinates: {sorted(missing)}")
    result: Counter[str] = Counter()
    for key, coefficient in vector.items():
        result[dagger[key]] += coefficient
    return clean_vector(result)


def tensor_product(
    left: Mapping[str, int], right: Mapping[str, int]
) -> dict[str, int]:
    lhs = clean_vector(left)
    rhs = clean_vector(right)
    if any("|" in key for key in (*lhs, *rhs)):
        raise ValueError("the replay pair encoding reserves '|'")
    return clean_vector(
        {
            f"{x}|{y}": a * b
            for x, a in lhs.items()
            for y, b in rhs.items()
            if a * b
        }
    )


def tensor_dagger(
    value: Mapping[str, int],
    left_mapping: Mapping[str, str],
    right_mapping: Mapping[str, str],
) -> dict[str, int]:
    left = validate_involution(left_mapping)
    right = validate_involution(right_mapping)
    result: Counter[str] = Counter()
    for pair, coefficient in clean_vector(value).items():
        parts = pair.split("|")
        if len(parts) != 2 or parts[0] not in left or parts[1] not in right:
            raise ValueError(f"invalid tensor coordinate: {pair}")
        result[f"{left[parts[0]]}|{right[parts[1]]}"] += coefficient
    return clean_vector(result)


def _clean_row(row: Mapping[str, int]) -> dict[str, int]:
    result: dict[str, int] = {}
    for key, coefficient in row.items():
        if not isinstance(key, str) or not key:
            raise ValueError("matrix coordinate names must be nonempty strings")
        if isinstance(coefficient, bool) or not isinstance(coefficient, int):
            raise ValueError("matrix entries must be exact integers")
        result[key] = coefficient
    return result


def observe(
    value: Mapping[str, int], rows: Sequence[Mapping[str, int]]
) -> tuple[int, ...]:
    vector = clean_vector(value)
    matrix = tuple(_clean_row(row) for row in rows)
    covered = set().union(*(row.keys() for row in matrix)) if matrix else set()
    missing = set(vector) - covered
    if missing:
        raise ValueError(f"observer is missing coordinates: {sorted(missing)}")
    return tuple(
        sum(coefficient * row.get(key, 0) for key, coefficient in vector.items())
        for row in matrix
    )


def dot(left: Sequence[int], right: Sequence[int]) -> int:
    if len(left) != len(right):
        raise ValueError("dot-product dimensions differ")
    if any(isinstance(x, bool) or not isinstance(x, int) for x in (*left, *right)):
        raise ValueError("dot-product entries must be exact integers")
    return sum(x * y for x, y in zip(left, right, strict=True))


def gram(
    left: Mapping[str, int],
    right: Mapping[str, int],
    rows: Sequence[Mapping[str, int]],
) -> int:
    return dot(observe(left, rows), observe(right, rows))
