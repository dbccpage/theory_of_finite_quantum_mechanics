# -*- coding: utf-8 -*-
"""
Value objects for CODA application domain.
Pure immutable objects with strict value equality, fail-closed validation, and zero float tolerance.

Exact scalars are Python ``int`` (not ``bool``), ``fractions.Fraction`` and SymPy
``Rational``/``Integer``. Everything else is refused: Python and NumPy floats,
``sympy.Float`` (a binary expansion, not an exact value), strings (``str(0.1 + 0.2)``
would launder a rounding artefact), ``Decimal``, irrationals and infinities.

AuthorityEffect: None.
"""

from __future__ import annotations

import numbers
import operator
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from math import gcd
from typing import Any, Tuple

from sympy import Matrix, Rational


def validate_exact_rational(value: Any) -> Rational:
    """Fail-closed coercion to an exact sympy Rational; refuses every non-exact input."""
    if isinstance(value, bool):
        raise TypeError(f"CODA exact arithmetic rejects bool value {value!r}")
    if isinstance(value, Rational):  # sympy Rational and Integer; sympy.Float is not a Rational
        return value
    if isinstance(value, Fraction):
        return Rational(value.numerator, value.denominator)
    if isinstance(value, int):
        return Rational(value)
    if isinstance(value, numbers.Integral) and type(value).__name__ not in ("bool_", "bool"):
        # NumPy integers register as Integral but are not int subclasses.
        return Rational(operator.index(value))
    raise TypeError(f"Cannot coerce {value!r} ({type(value).__name__}) to an exact rational")


def _exact_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"ExactRational.{name} must be an int, got {type(value).__name__}")
    return int(value)


@dataclass(frozen=True)
class ExactRational:
    """Exact rational value object in lowest terms with a positive denominator.

    Construction normalises (``ExactRational(2, 4) == ExactRational(1, 2)``, and the
    two hash alike) and refuses float, bool and str fields.
    """

    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        num = _exact_int(self.numerator, "numerator")
        den = _exact_int(self.denominator, "denominator")
        if den == 0:
            raise ZeroDivisionError("Denominator cannot be zero in ExactRational")
        if den < 0:
            num, den = -num, -den
        g = gcd(num, den)
        object.__setattr__(self, "numerator", num // g)
        object.__setattr__(self, "denominator", den // g)

    @classmethod
    def from_rational(cls, r: Any) -> ExactRational:
        q = validate_exact_rational(r)
        return cls(numerator=int(q.p), denominator=int(q.q))

    @property
    def sympy_rational(self) -> Rational:
        return Rational(self.numerator, self.denominator)

    @property
    def fraction(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)

    @property
    def is_zero(self) -> bool:
        return self.numerator == 0

    @property
    def is_positive(self) -> bool:
        return self.numerator > 0  # denominators are positive after normalisation

    def to_tuple(self) -> Tuple[int, int]:
        return (self.numerator, self.denominator)


def _witness_entry(entry: Any) -> Fraction:
    if not isinstance(entry, tuple) or len(entry) != 2:
        raise TypeError(f"DualWitness entries are (p, q) int pairs, got {entry!r}")
    p = _exact_int(entry[0], "p")
    q = _exact_int(entry[1], "q")
    if q == 0:
        raise ZeroDivisionError("DualWitness entry has a zero denominator")
    return Fraction(p, q)


@dataclass(frozen=True)
class DualWitness:
    """
    Exact data for a proposed L1 dual witness.

    Construction validates rational encodings only. The native evaluator checks
    D^T y = 0, ||y||_infty <= 1 and the pairing against the supplied problem
    before the witness can support a checked quotient certificate. This carrier
    neither calculates a norm nor certifies the claimed pairing.
    """

    witness_vector: Tuple[Tuple[int, int], ...]  # Tuple of (p, q) exact rationals
    pairing_value: ExactRational

    def __post_init__(self) -> None:
        if not isinstance(self.witness_vector, tuple):
            raise TypeError("DualWitness.witness_vector must be a tuple of (p, q) pairs")
        if not isinstance(self.pairing_value, ExactRational):
            raise TypeError("DualWitness pairing must be ExactRational")
        for entry in self.witness_vector:
            _witness_entry(entry)

    @property
    def fractions(self) -> Tuple[Fraction, ...]:
        return tuple(Fraction(p, q) for p, q in self.witness_vector)

    def to_matrix(self) -> Matrix:
        return Matrix([Rational(p, q) for p, q in self.witness_vector])

    @classmethod
    def from_fractions(cls, values, pairing: Fraction) -> DualWitness:
        values = tuple(values)
        vec = tuple((v.numerator, v.denominator) for v in values)
        return cls(
            witness_vector=vec,
            pairing_value=ExactRational(pairing.numerator, pairing.denominator),
        )


class FirewallDecision(str, Enum):
    """Authority firewall ternary routing decision."""

    PERMIT_AUTHORIZED = "PERMIT_AUTHORIZED"
    ROUTE_CLOSED_RESIDUAL = "ROUTE_CLOSED_RESIDUAL"
    ROUTE_REFUSED = "ROUTE_REFUSED"


class LayerId(str, Enum):
    """The 9 layers of the CODA stack."""

    FOC = "FOC"      # Layer 1
    MUR = "MUR"      # Layer 2
    CS = "CS"        # Layer 3
    CS_Q = "CS_Q"    # Layer 4
    Q = "Q"          # Layer 5
    A = "A"          # Layer 6
    OR = "OR"        # Layer 7
    FDA = "FDA"      # Layer 8
    GTLA = "GTLA"    # Layer 9
