"""Exact rational constructor. Float, bool, and decimal text are refused.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/scalar.py
Claim: urn:omega:fqm:ms-majorana:scalar:exact-rational:v1
AuthorityEffect: None
Mutation-Kills: 5 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: Q is the field of rationals. This file does not construct Q(i) or a real completion.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence

Q = Fraction


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
    if value == "" or "." in value or "e" in value or "E" in value:
        raise _fail("decimal or empty text refused", role=role)
    try:
        parsed = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise _fail("text is not an exact rational", role=role) from error
    return parsed


def q(value: object) -> Fraction:
    """Construct an exact rational from an int, Fraction, or reduced text token."""
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role="value", received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role="value")
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str):
        return _from_text(value, "value")
    raise _fail("value is not an exact rational", role="value", received=type(value).__name__)


def hash_rational(numer: object, denom: object) -> str:
    """Return the reduced numerator/denominator text of numer/denom."""
    numerator = q(numer)
    denominator = q(denom)
    if denominator == 0:
        raise _fail("rational denominator is zero", role="denom")
    reduced = numerator / denominator
    return f"{reduced.numerator}/{reduced.denominator}"


def hash_rational_vec(values: object) -> str:
    """Join reduced encodings of a rational sequence."""
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("rational vector must be a sequence", received=type(values).__name__)
    return ",".join(hash_rational(item, 1) for item in values)


@dataclass(frozen=True)
class ScalarCertificate:
    """Witness that two constructor paths agree on one reduced rational."""

    value: Fraction
    text: str


def certify_scalar(value: object) -> ScalarCertificate:
    """Recheck that the canonical text rebuilds the same fraction."""
    parsed = q(value)
    text = hash_rational(parsed.numerator, parsed.denominator)
    rebuilt = q(text)
    if rebuilt != parsed:
        raise _fail("scalar text did not rebuild the same rational", text=text)
    return ScalarCertificate(parsed, text)


__all__ = ["Q", "ScalarCertificate", "ScalarError", "certify_scalar", "hash_rational", "hash_rational_vec", "q"]
