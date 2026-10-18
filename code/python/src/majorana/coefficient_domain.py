"""Admitted exact coefficient domains. Real and binary-float carriers are refused.

Origin: papers/derivations/ms_majorana/lean4/MajoranaCore.lean theorem f2_weight_l1_l2_coincide
Claim: urn:omega:fqm:ms-majorana:coefficient-domain:exact-admission:v1
AuthorityEffect: None
Mutation-Kills: 5 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: This file does not construct a real vector space and does not admit a float modulus.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class CoefficientDomainError(ValueError):
    """One violated coefficient-domain invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CoefficientDomainError:
    return CoefficientDomainError(invariant, parameters)


class CoefficientDomain(str, Enum):
    """Exact carriers admitted by the Majorana cochain schedule."""

    Integers = "Integers"
    Rational = "Rational"
    FiniteField = "FiniteField"


def as_str(domain: CoefficientDomain) -> str:
    """Return the declared domain name."""
    if not isinstance(domain, CoefficientDomain):
        raise _fail("domain is not an admitted coefficient tag", received=type(domain).__name__)
    return domain.value


@dataclass(frozen=True)
class DomainCertificate:
    """Witness that a name was admitted with an exact modulus constraint."""

    domain: CoefficientDomain
    modulus: int | None


def _modulus(value: object) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role="modulus", received="float")
    if isinstance(value, bool) or type(value) is not int:
        raise _fail("boolean or non-integer modulus refused", received=type(value).__name__)
    return value


def _finite_field(modulus: object) -> DomainCertificate:
    parsed = _modulus(modulus)
    if parsed != 2:
        raise _fail("only the prime field F2 is admitted", modulus=parsed)
    return DomainCertificate(CoefficientDomain.FiniteField, parsed)


def admit_domain(name: object, modulus: object | None = None) -> DomainCertificate:
    """Admit Integers, Rational, or F2. Real, float, and other moduli are refused."""
    if isinstance(name, float):
        raise _fail("float refused at the public boundary", role="name", received="float")
    if name == "Real":
        raise _fail("real coefficient domain refused", name="Real")
    if name == "Integers":
        return DomainCertificate(CoefficientDomain.Integers, None)
    if name == "Rational":
        return DomainCertificate(CoefficientDomain.Rational, None)
    if name == "FiniteField":
        return _finite_field(modulus)
    raise _fail("coefficient domain is not admitted", name=str(name))


__all__ = [
    "CoefficientDomain",
    "CoefficientDomainError",
    "DomainCertificate",
    "admit_domain",
    "as_str",
]
