"""Immutable value storage and exact canonical snapshots of educational primitives.

AuthorityEffect: None. A snapshot is data custody, not a source proof.
Numerical realizations and executable callbacks cannot enter this exact codec.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass, fields, is_dataclass
from fractions import Fraction
from functools import lru_cache
from types import UnionType
from typing import Any, Generic, TypeVar, Union, get_args, get_origin, get_type_hints

K = TypeVar("K")
V = TypeVar("V")


@dataclass(frozen=True, init=False, eq=False)
class FrozenMap(Mapping[K, V], Generic[K, V]):
    """Copied immutable mapping with order-independent equality and hashing."""

    _items: tuple[tuple[K, V], ...]

    def __init__(self, source: Mapping[K, V]) -> None:
        if not isinstance(source, Mapping):
            raise TypeError("REFUSED_SHAPE: expected mapping")
        items = tuple(source.items())
        for key, value in items:
            _immutable(key)
            _immutable(value)
        object.__setattr__(self, "_items", items)

    def __getitem__(self, key: K) -> V:
        for current, value in self._items:
            if exact_equal(current, key):
                return value
        raise KeyError(key)

    def __iter__(self) -> Iterator[K]:
        return (key for key, _ in self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other) or len(self) != len(other):
            return False
        return all(
            any(
                exact_equal(key, other_key) and exact_equal(value, other_value)
                for other_key, other_value in other._items
            )
            for key, value in self._items
        )

    def __hash__(self) -> int:
        return hash(frozenset(self._items))


def exact_equal(left: object, right: object) -> bool:
    """Compare immutable payloads recursively without Python's bool/int aliases."""
    if type(left) is not type(right):
        return False
    if left is right:
        return True
    if type(left) is tuple:
        return len(left) == len(right) and all(exact_equal(a, b) for a, b in zip(left, right))
    if type(left) is frozenset:
        return len(left) == len(right) and all(any(exact_equal(a, b) for b in right) for a in left)
    if isinstance(left, FrozenMap):
        return left == right
    if is_dataclass(left) and left.__dataclass_params__.frozen:
        return left == right and all(
            exact_equal(getattr(left, field.name), getattr(right, field.name))
            for field in fields(left)
        )
    return left == right


def _immutable(value: object) -> None:
    if type(value) in (type(None), bool, int, str, float, Fraction):
        return
    if type(value) in (tuple, frozenset):
        for entry in value:
            _immutable(entry)
        return
    if isinstance(value, FrozenMap):
        return
    if is_dataclass(value) and value.__dataclass_params__.frozen:
        for field in fields(value):
            _immutable(getattr(value, field.name))
        _require_hash(value)
        return
    if callable(value):
        _require_hash(value)
        return
    raise TypeError("REFUSED_SHAPE: mutable or unsupported value in immutable primitive")


def _require_hash(value: object) -> None:
    try:
        hash(value)
    except TypeError as error:
        raise TypeError("REFUSED_SHAPE: immutable primitive payload must be hashable") from error


@lru_cache(maxsize=None)
def _field_types(record_type: type) -> dict[str, object]:
    return get_type_hints(record_type)


def _typed(value: object, annotation: object) -> bool:
    origin, arguments = get_origin(annotation), get_args(annotation)
    if annotation in (Any, object) or isinstance(annotation, TypeVar):
        _immutable(value)
        return True
    if origin in (Union, UnionType):
        return any(_typed(value, option) for option in arguments)
    if origin is tuple:
        if type(value) is not tuple:
            return False
        if len(arguments) == 2 and arguments[1] is Ellipsis:
            return all(_typed(entry, arguments[0]) for entry in value)
        return len(value) == len(arguments) and all(
            _typed(entry, expected) for entry, expected in zip(value, arguments)
        )
    if origin is frozenset:
        return type(value) is frozenset and all(_typed(entry, arguments[0]) for entry in value)
    if origin in (dict, Mapping):
        return type(value) is FrozenMap and all(
            _typed(key, arguments[0]) and _typed(entry, arguments[1])
            for key, entry in value.items()
        )
    if origin is Sequence:
        return type(value) is tuple and all(_typed(entry, arguments[0]) for entry in value)
    if origin is Callable:
        if not callable(value):
            return False
        _immutable(value)
        return True
    if annotation is type(None):
        return value is None
    if isinstance(annotation, type):
        return type(value) is annotation
    return False


def validate_typed_fields(record: object) -> None:
    """Reject bool/int confusion and mutable payloads without coercing witnesses."""
    for name, annotation in _field_types(type(record)).items():
        if not _typed(getattr(record, name), annotation):
            raise TypeError(f"REFUSED_SHAPE: {type(record).__name__}.{name} has wrong exact type")


def canonical_data(value: object) -> object:
    """Type-preserving JSON tree; no float rounding or callable name stand-ins."""
    if value is None or type(value) in (bool, int, str):
        return value
    if type(value) is Fraction:
        return f"{value.numerator}/{value.denominator}"
    if type(value) is float:
        raise TypeError("REFUSED_FLOAT: numerical realization cannot enter exact snapshot")
    if callable(value):
        raise TypeError("REFUSED_UNSERIALIZABLE: executable payload cannot enter exact snapshot")
    if isinstance(value, FrozenMap):
        return canonical_data(dict(value.items()))
    if is_dataclass(value):
        if not value.__dataclass_params__.frozen:
            raise TypeError("REFUSED_UNVERIFIED_RECORD: mutable runtime metadata")
        _immutable(value)
        validate_typed_fields(value)
        validator = getattr(value, "validate_boundary", None)
        if validator is not None:
            validator()
        verify = getattr(value, "is_well_formed", None)
        if verify is not None and not verify():
            raise ValueError("REFUSED_UNVERIFIED_RECORD: transition does not replay")
        return {
            "$type": f"{type(value).__module__.rsplit('.', 1)[-1]}.{type(value).__qualname__}",
            **{field.name: canonical_data(getattr(value, field.name)) for field in fields(value)},
        }
    if isinstance(value, Mapping):
        if all(type(key) is str for key in value):
            return {key: canonical_data(entry) for key, entry in value.items()}
        entries = [[canonical_data(key), canonical_data(entry)] for key, entry in value.items()]
        return {"$map": sorted(entries, key=lambda pair: _json(pair[0]))}
    if type(value) is tuple:
        return {"$tuple": [canonical_data(entry) for entry in value]}
    if type(value) is frozenset:
        return {"$set": sorted((canonical_data(entry) for entry in value), key=_json)}
    if type(value) is list:
        return [canonical_data(entry) for entry in value]
    raise TypeError("REFUSED_UNSERIALIZABLE: executable or unsupported payload")


def _json(value: object) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    )


def canonical_json(value: object) -> bytes:
    """Sorted compact UTF-8 JSON, no BOM, exactly one trailing LF."""
    return (_json(canonical_data(value)) + "\n").encode("utf-8")
