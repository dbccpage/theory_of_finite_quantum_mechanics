"""Exact bounded inert-prime norm residuals on owned Gaussian three-vectors.

AuthorityEffect: None. The prime is an actual prime3(mod4), at most65535.
Scalar norms are nonnegative exact rationals with4096-bit components. Zero
has valuation0 and unit character0 by explicit computational convention.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt

from .boundary import Violation, evaluate, require
from .domains import integer, rational
from .gaussian_vector3 import GaussianVector3
from .outcome import Outcome


def _prime(value: object) -> int:
    prime = integer(value, 'inert prime', 3, 65535)
    if prime % 4 != 3:
        raise Violation('input', 'inert prime must be3 modulo4')
    if any(prime % divisor == 0 for divisor in range(3, isqrt(prime)+1, 2)):
        raise Violation('input', 'residual parameter must be prime')
    return prime


@dataclass(frozen=True, slots=True, init=False)
class InertPrimeResidual:
    """Owns the admitted prime and evaluates its norm-valuation residual."""
    prime: int

    def __init__(self, prime: object) -> None:
        object.__setattr__(self, 'prime', _prime(prime))

    def _integer_parts(self, value: object) -> tuple[int, int]:
        number = abs(integer(value, 'integer valuation input'))
        if number.bit_length() > 4096:
            raise Violation('resource', 'valuation input exceeds4096bits')
        valuation = 0
        if number == 0:
            return 0, 0
        while number % self.prime == 0:
            number //= self.prime
            valuation += 1
        return valuation, number

    def integer_parts(self, value: object) -> Outcome[tuple[int, int]]:
        return evaluate(self._integer_parts, value)

    def _valuation(self, value: object) -> int:
        norm = rational(value, 'nonnegative norm', minimum=0)
        numerator, _ = self._integer_parts(norm.numerator)
        denominator, _ = self._integer_parts(norm.denominator)
        return numerator-denominator

    def valuation(self, value: object) -> Outcome[int]:
        return evaluate(self._valuation, value)

    def _unit_character(self, value: object) -> Q:
        norm = rational(value, 'nonnegative norm', minimum=0)
        if norm == 0:
            return Q(0)
        _, numerator = self._integer_parts(norm.numerator)
        _, denominator = self._integer_parts(norm.denominator)
        # The quadratic character of a denominator equals that of its inverse.
        residue = ((numerator % self.prime)*(denominator % self.prime)) % self.prime
        sign = pow(residue, (self.prime-1)//2, self.prime)
        require(sign in (1, self.prime-1), 'nonzero prime unit has invalid quadratic character')
        return Q(1 if sign == 1 else -1)

    def unit_character(self, value: object) -> Outcome[Q]:
        return evaluate(self._unit_character, value)

    def _residual(self, value: object) -> Q:
        vector = GaussianVector3._operand(value)
        norm = vector.squared_norm
        total_valuation = self._valuation(norm)
        if total_valuation % 2 == 0:
            return Q(0)
        for component in vector.component_norms:
            if component > 0 and self._valuation(component) < total_valuation:
                return self._unit_character(component)*self._unit_character(norm)
        raise Violation('check', 'odd norm valuation has no leading coordinate')

    def residual(self, value: object) -> Outcome[Q]:
        return evaluate(self._residual, value)

    def _exotic(self, value: object) -> Q:
        return (1+self._residual(value))/3

    def exotic(self, value: object) -> Outcome[Q]:
        return evaluate(self._exotic, value)
