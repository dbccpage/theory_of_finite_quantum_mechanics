"""Exact Gaussian rational field Q(i).

Origin: lean4/DerivationDagQMClosure.lean theorem
ds_qm062_u1_selector_layers_and_ring_iso, whose complex ring law is
(a1 + b1 i)(a2 + b2 i) = (a1 a2 - b1 b2) + (a1 b2 + b1 a2) i.
Claim: urn:omega:fqm:scalar:gaussian-rational-field:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_scalars.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: This file does not prove the U(1) selector theorem, does not
identify Q(i) with a binary float, and does not order the Gaussian rationals.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from typing import Mapping


class ScalarError(Exception):
    """One violated scalar invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


class ScalarDivisionByZero(ScalarError, ZeroDivisionError):
    """Division by zero in Q or Q(i). Still a ZeroDivisionError for existing callers."""


def _fail(invariant: str, **parameters: object) -> ScalarError:
    return ScalarError(invariant, parameters)


def _division(invariant: str, **parameters: object) -> ScalarDivisionByZero:
    return ScalarDivisionByZero(invariant, parameters)


def require_rational(value: object, role: str) -> Fraction:
    """Accept int or Fraction only. Float and bool are refused."""
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


class GaussianRational:
    """Element a + b i of Q(i), stored as two exact rationals."""

    __slots__ = ("real", "imag")
    real: Fraction
    imag: Fraction

    def __init__(self, real: object = 0, imag: object = 0) -> None:
        if isinstance(real, GaussianRational):
            copied_real = real.real
            copied_imag = real.imag
        else:
            copied_real = require_rational(real, "real")
            copied_imag = require_rational(imag, "imag")
        self.real = copied_real
        self.imag = copied_imag

    @staticmethod
    def zero() -> GaussianRational:
        return GaussianRational(0, 0)

    @staticmethod
    def one() -> GaussianRational:
        return GaussianRational(1, 0)

    @staticmethod
    def i() -> GaussianRational:
        return GaussianRational(0, 1)

    def is_zero(self) -> bool:
        return self.real == 0 and self.imag == 0

    def conjugate(self) -> GaussianRational:
        return GaussianRational(self.real, -self.imag)

    def norm_sq(self) -> Fraction:
        return self.real * self.real + self.imag * self.imag

    def _partner(self, other: object, role: str) -> GaussianRational:
        if isinstance(other, GaussianRational):
            return other
        return GaussianRational(require_rational(other, role), 0)

    def __add__(self, other: object) -> GaussianRational:
        partner = self._partner(other, "addend")
        return GaussianRational(self.real + partner.real, self.imag + partner.imag)

    def __radd__(self, other: object) -> GaussianRational:
        return self.__add__(other)

    def __sub__(self, other: object) -> GaussianRational:
        partner = self._partner(other, "subtrahend")
        return GaussianRational(self.real - partner.real, self.imag - partner.imag)

    def __rsub__(self, other: object) -> GaussianRational:
        partner = self._partner(other, "minuend")
        return GaussianRational(partner.real - self.real, partner.imag - self.imag)

    def __mul__(self, other: object) -> GaussianRational:
        if isinstance(other, GaussianRational):
            return GaussianRational(
                self.real * other.real - self.imag * other.imag,
                self.real * other.imag + self.imag * other.real,
            )
        coeff = require_rational(other, "factor")
        return GaussianRational(self.real * coeff, self.imag * coeff)

    def __rmul__(self, other: object) -> GaussianRational:
        return self.__mul__(other)

    def __truediv__(self, other: object) -> GaussianRational:
        if isinstance(other, GaussianRational):
            denom = other.norm_sq()
            if denom == 0:
                raise _division("division by zero in the Gaussian rational field", norm_sq="0")
            numerator = self * other.conjugate()
            return GaussianRational(numerator.real / denom, numerator.imag / denom)
        coeff = require_rational(other, "divisor")
        if coeff == 0:
            raise _division("division by zero in the rational field", divisor="0")
        return GaussianRational(self.real / coeff, self.imag / coeff)

    def __neg__(self) -> GaussianRational:
        return GaussianRational(-self.real, -self.imag)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GaussianRational):
            return self.real == other.real and self.imag == other.imag
        if isinstance(other, bool):
            return False
        if isinstance(other, (int, Fraction)):
            return self.imag == 0 and self.real == other
        return False

    def __hash__(self) -> int:
        return hash((self.real, self.imag))

    def __repr__(self) -> str:
        if self.imag == 0:
            return f"{self.real}"
        if self.real == 0:
            return f"{self.imag}i"
        sign = "+" if self.imag > 0 else "-"
        return f"({self.real} {sign} {abs(self.imag)}i)"

    def canonical_bytes(self) -> bytes:
        real = f"{self.real.numerator}/{self.real.denominator}"
        imag = f"{self.imag.numerator}/{self.imag.denominator}"
        return f"{real}+{imag}i".encode("utf-8")

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


def q(numerator: object, denominator: object = 1) -> Fraction:
    """Return numerator/denominator as an exact rational. Zero denominators are refused."""
    numer = require_rational(numerator, "numerator")
    denominator_value = require_rational(denominator, "denominator")
    if denominator_value == 0:
        raise _division("rational denominator is zero", numerator=str(numer))
    return numer / denominator_value


Q = Fraction

__all__ = [
    "GaussianRational",
    "Q",
    "ScalarDivisionByZero",
    "ScalarError",
    "q",
    "require_rational",
]
