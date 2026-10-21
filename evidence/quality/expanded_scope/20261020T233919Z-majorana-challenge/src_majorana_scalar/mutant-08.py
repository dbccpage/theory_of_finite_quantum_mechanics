"""Exact rational constructor. Float, bool, and decimal text are refused.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/scalar.py
Claim: urn:omega:fqm:ms-majorana:scalar:exact-rational:v1
AuthorityEffect: None
Mutation-Kills: 5 legacy source faults; current execution evidence is in the companion.
Scope Fence: Q is the field of rationals. This file does not construct Q(i) or a real completion.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping

Q = Fraction
# Q names the representation. q/certificates are the bounded admission APIs.
MAX_SCALAR_BITS = 1024
MAX_TEXT_CHARACTERS = 1024
MAX_VECTOR_LENGTH = 4096


class ScalarError(ValueError):
    """One violated scalar invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ScalarError:
    return ScalarError(invariant, parameters)


def _from_text(value: str, role: str) -> Fraction:
    if len(value) > MAX_TEXT_CHARACTERS:
        raise _fail("scalar text budget exceeded", role=role, limit=MAX_TEXT_CHARACTERS)
    if value == "":
        raise _fail("decimal or empty text refused", role=role)
    try:
        parsed = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise _fail("text is not an exact rational", role=role) from error
    return _bounded(parsed, role)


def _bounded(value: Fraction, role: str) -> Fraction:
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_SCALAR_BITS:
        raise _fail("scalar bit budget exceeded", role=role, limit=MAX_SCALAR_BITS)
    return value


def q(value: object) -> Fraction:
    """Construct an exact rational from an int, Fraction, or reduced text token."""
    if issubclass(type(value), float):
        raise _fail("float refused at the public boundary", role="value", received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role="value")
    if type(value) is Fraction:
        return _bounded(value, "value")
    if type(value) is int:
        if value.bit_length() > MAX_SCALAR_BITS:
            raise _fail("scalar bit budget exceeded", role="value", limit=MAX_SCALAR_BITS)
        return Fraction(value)
    if type(value) is str:
        return _from_text(value, "value")
    raise _fail("value is not an exact rational", role="value", received=type(value).__name__)


def hash_rational(numer: object, denom: object) -> str:
    """Return the reduced numerator/denominator text of numer/denom."""
    numerator = q(numer)
    denominator = q(denom)
    if denominator == 0:
        raise _fail("rational denominator is zero", role="denom")
    reduced = _bounded(numerator / denominator, "quotient")
    return f"{reduced.numerator}/{reduced.denominator}"


def hash_rational_vec(values: object) -> str:
    """Join reduced encodings of a rational sequence."""
    if type(values) not in (list, tuple):
        raise _fail("rational vector must be a sequence", received=type(values).__name__)
    if len(values) > MAX_VECTOR_LENGTH:
        raise _fail("scalar vector budget exceeded", limit=MAX_VECTOR_LENGTH)
    return ",".join(hash_rational(item, 1) for item in values)


@dataclass(frozen=True, slots=True, init=False, eq=False)
class ScalarCertificate:
    """Validated canonical encoding; every public construction checks agreement."""

    value: Fraction
    text: str

    def __init__(self, value: object, text: object) -> None:
        if hasattr(self, "value"):
            raise _fail("scalar certificate already initialized")
        parsed = q(value)
        if type(text) is not str:
            raise _fail("scalar certificate text must be a built-in string")
        if len(text) > MAX_TEXT_CHARACTERS:
            raise _fail("scalar text budget exceeded", role="certificate", limit=MAX_TEXT_CHARACTERS)
        canonical = hash_rational(parsed.numerator, parsed.denominator)
        if text != canonical or q(text) != parsed:
            raise _fail("scalar certificate value and canonical text disagree")
        object.__setattr__(self, "value", parsed)
        object.__setattr__(self, "text", canonical)

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("ScalarCertificate does not admit subclasses")

    def __eq__(self, other: object) -> bool:
        return type(other) is ScalarCertificate and (self.value, self.text) == (other.value, other.text)

    def __hash__(self) -> int:
        return hash((self.value, self.text))


def certify_scalar(value: object) -> ScalarCertificate:
    """Recheck that the canonical text rebuilds the same fraction."""
    parsed = q(value)
    text = hash_rational(parsed.numerator, parsed.denominator)
    rebuilt = q(text)
    if rebuilt != parsed:
        raise _fail("scalar text did not rebuild the same rational", text=text)
    return ScalarCertificate(parsed, text)


__all__ = ["Q", "ScalarCertificate", "ScalarError", "certify_scalar", "hash_rational", "hash_rational_vec", "q"]
