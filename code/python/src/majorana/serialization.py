"""Canonical reduced encoding of exact rationals. Decimal text and floats are refused.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/serialization.py
Claim: urn:omega:fqm:ms-majorana:serialization:reduced-rational:v1
AuthorityEffect: None
Mutation-Kills: 5 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: The encoding is a commitment to a reduced fraction. It is not a cryptographic signature and not a physics receipt.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class SerializationError(ValueError):
    """One violated serialization invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SerializationError:
    return SerializationError(invariant, parameters)


def _rational(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str):
        return _from_text(value, role)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _from_text(value: str, role: str) -> Fraction:
    if value == "" or "." in value or "e" in value or "E" in value:
        raise _fail("decimal or empty text refused", role=role)
    try:
        parsed = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise _fail("text is not an exact rational", role=role) from error
    return parsed


def canonical_rational(value: object) -> str:
    """Return numerator/denominator in lowest terms with a positive denominator."""
    parsed = _rational(value, "value")
    return f"{parsed.numerator}/{parsed.denominator}"


@dataclass(frozen=True)
class EncodingCertificate:
    """Witness that a value and its canonical text decode to the same reduced fraction."""

    value: Fraction
    text: str


def certify_encoding(value: object) -> EncodingCertificate:
    """Encode, decode, and recheck reduced equality."""
    parsed = _rational(value, "value")
    text = canonical_rational(parsed)
    decoded = _rational(text, "text")
    if decoded != parsed:
        raise _fail("canonical text did not decode to the same rational", text=text)
    if parsed.denominator <= 0:
        raise _fail("reduced denominator is not positive", denominator=parsed.denominator)
    return EncodingCertificate(parsed, text)


def canonical_vector(values: object) -> tuple[str, ...]:
    """Encode a sequence of exact rationals."""
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("vector must be a sequence", received=type(values).__name__)
    return tuple(canonical_rational(item) for item in values)


__all__ = [
    "EncodingCertificate",
    "SerializationError",
    "canonical_rational",
    "canonical_vector",
    "certify_encoding",
]
