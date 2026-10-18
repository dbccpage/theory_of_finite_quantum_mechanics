"""Exact degree, basis label, and nonempty provenance identifiers.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/ids.py
Claim: urn:omega:fqm:ms-majorana:ids:exact-identifiers:v1
AuthorityEffect: None
Mutation-Kills: 5 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: A nonempty provenance string is not a proof audit and does not raise AuthorityEffect.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, cast

from .errors import InvalidProvenance


class IdentifierError(ValueError):
    """One violated identifier invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> IdentifierError:
    return IdentifierError(invariant, parameters)


@dataclass(frozen=True)
class Degree:
    """An exact integer cohomological degree. Bool is not a degree."""

    value: int

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or type(self.value) is not int:
            raise _fail("degree is not an exact integer", received=type(self.value).__name__)

    @staticmethod
    def new(value: object) -> Degree:
        if isinstance(value, float):
            raise _fail("float refused at the public boundary", role="degree", received="float")
        return Degree(cast(int, value))


@dataclass(frozen=True)
class BasisId:
    """A nonempty basis label."""

    label: str

    def __post_init__(self) -> None:
        if not isinstance(self.label, str) or self.label == "":
            raise _fail("basis label must be a nonempty string", received=type(self.label).__name__)

    @staticmethod
    def new(label: object) -> BasisId:
        if isinstance(label, float):
            raise _fail("float refused at the public boundary", role="label", received="float")
        if not isinstance(label, str):
            raise _fail("basis label must be a nonempty string", received=type(label).__name__)
        return BasisId(label)


@dataclass(frozen=True)
class TheoremProvenance:
    """A nonempty verification-source string. AuthorityEffect remains None."""

    verification_source: str

    def __post_init__(self) -> None:
        if not isinstance(self.verification_source, str) or self.verification_source == "":
            raise InvalidProvenance("provenance verification_source must be non-empty")

    @staticmethod
    def new(verification_source: object) -> TheoremProvenance:
        if isinstance(verification_source, float):
            raise _fail("float refused at the public boundary", role="verification_source", received="float")
        if not isinstance(verification_source, str):
            raise InvalidProvenance("provenance verification_source must be non-empty")
        return TheoremProvenance(verification_source)


@dataclass(frozen=True)
class IdentifierCertificate:
    """Witness that a degree and a provenance source were admitted together."""

    degree: Degree
    provenance: TheoremProvenance


def certify_identifiers(degree: object, verification_source: object) -> IdentifierCertificate:
    """Admit one exact degree and one nonempty provenance source."""
    return IdentifierCertificate(Degree.new(degree), TheoremProvenance.new(verification_source))


__all__ = [
    "BasisId",
    "Degree",
    "IdentifierCertificate",
    "IdentifierError",
    "TheoremProvenance",
    "certify_identifiers",
]
