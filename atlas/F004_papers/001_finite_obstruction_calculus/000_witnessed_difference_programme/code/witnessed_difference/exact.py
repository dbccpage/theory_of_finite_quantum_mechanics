"""Small exact-arithmetic and canonicalization helpers."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import fields, is_dataclass
from enum import Enum
from fractions import Fraction
from math import isfinite
from typing import Any, Iterable


def as_fraction(value: int | str | Fraction) -> Fraction:
    """Convert admitted exact scalars; floats are deliberately refused."""

    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError("exact values must not be bool or float")
    if isinstance(value, (int, str, Fraction)):
        return Fraction(value)
    raise TypeError(f"unsupported exact scalar: {type(value).__name__}")


def exact_row(values: object) -> tuple[Fraction, ...]:
    """A sequence of exact scalars; a string is not read as a sequence of digits."""

    if isinstance(values, (str, bytes, Mapping)) or not isinstance(values, Sequence):
        raise TypeError("expected a sequence of exact scalars, not a string or mapping")
    return tuple(as_fraction(value) for value in values)  # type: ignore[arg-type]


def l1(values: Iterable[Fraction]) -> Fraction:
    from .native_functionals import representative_mass

    return representative_mass(values)


def canonical_data(value: Any) -> Any:
    """Convert supported objects into typed deterministic JSON data.

    Every non-primitive shape has an explicit type envelope.  In particular,
    a user mapping can never collide with the internal representation of a
    fraction, byte string, complex number, enum, dataclass, or container.
    """

    if is_dataclass(value) and not isinstance(value, type):
        return {
            "__wdp_type__": "dataclass",
            "class": f"{type(value).__module__}.{type(value).__qualname__}",
            "fields": [
                [field.name, canonical_data(getattr(value, field.name))]
                for field in fields(value)
            ],
        }
    if isinstance(value, Enum):
        return {
            "__wdp_type__": "enum",
            "class": f"{type(value).__module__}.{type(value).__qualname__}",
            "value": canonical_data(value.value),
        }
    if isinstance(value, Fraction):
        return {
            "__wdp_type__": "fraction",
            "denominator": value.denominator,
            "numerator": value.numerator,
        }
    if isinstance(value, complex):
        if not isfinite(value.real) or not isfinite(value.imag):
            raise TypeError("canonical complex values must have finite components")
        real = 0.0 if value.real == 0 else value.real
        imag = 0.0 if value.imag == 0 else value.imag
        return {
            "__wdp_type__": "complex",
            "imag_hex": imag.hex(),
            "real_hex": real.hex(),
        }
    if isinstance(value, bytes):
        return {"__wdp_type__": "bytes", "hex": value.hex()}
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise TypeError("canonical mappings require string keys; keys are never coerced")
        return {
            "__wdp_type__": "mapping",
            "items": [
                [key, canonical_data(item)]
                for key, item in sorted(value.items())
            ],
        }
    if isinstance(value, (set, frozenset)):
        converted = [canonical_data(item) for item in value]
        converted.sort(
            key=lambda item: json.dumps(
                item, ensure_ascii=True, separators=(",", ":"), sort_keys=True
            )
        )
        return {
            "__wdp_type__": "frozenset" if isinstance(value, frozenset) else "set",
            "items": converted,
        }
    if isinstance(value, list):
        return {"__wdp_type__": "list", "items": [canonical_data(item) for item in value]}
    if isinstance(value, tuple):
        return {"__wdp_type__": "tuple", "items": [canonical_data(item) for item in value]}
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise TypeError(f"unsupported canonical value: {type(value).__name__}")
# Executable finite evidence; AuthorityEffect: None.
