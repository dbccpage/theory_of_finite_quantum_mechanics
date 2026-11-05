"""Owned nonzero integer polynomials of degree at most two.

AuthorityEffect: None. Exact rational and integer roots use the discriminant,
with coefficient, result and arithmetic budgets enforced at 4096 bits. This
algebraic service does not select a scalar field or a continuum completion.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt

from .boundary import Violation, evaluate, require
from .domains import integer, rational, sequence
from .outcome import Outcome


def _integer(value: object) -> int:
    admitted = integer(value, 'polynomial integer')
    if admitted.bit_length() > 4096:
        raise Violation('resource', 'polynomial integer exceeds 4096 bits')
    return admitted


def _square_root(value: object) -> int | None:
    number = _integer(value)
    if number < 0:
        return None
    root = isqrt(number)
    return root if root*root == number else None


@dataclass(frozen=True, slots=True, init=False)
class IntegerQuadraticEquation:
    """Invariant: three owned bounded integer coefficients, not all zero.

    The coefficients represent a*x²+b*x+c, or the homogeneous form
    a*x²+b*x*y+c*y². Root queries return sorted distinct finite solutions;
    the zero polynomial is refused because it has an infinite solution set.
    """
    quadratic: int
    linear: int
    constant: int

    def __init__(self, coefficients: object) -> None:
        a, b, c = (_integer(x) for x in sequence(coefficients, 'three coefficients', 3))
        if a == b == c == 0:
            raise Violation('input', 'the zero polynomial has no finite root list')
        object.__setattr__(self, 'quadratic', a)
        object.__setattr__(self, 'linear', b)
        object.__setattr__(self, 'constant', c)

    @property
    def coefficients(self) -> tuple[int, int, int]:
        return self.quadratic, self.linear, self.constant

    def _evaluate(self, value: object) -> Q:
        x = rational(value, 'polynomial argument')
        first = rational(rational(self.quadratic*x, 'Horner product')+self.linear, 'Horner prefix')
        return rational(rational(first*x, 'Horner product')+self.constant, 'polynomial value')

    def evaluate(self, value: object) -> Outcome[Q]:
        return evaluate(self._evaluate, value)

    def _homogeneous_value(self, values: object) -> int:
        x, y = (_integer(v) for v in sequence(values, 'homogeneous pair', 2))
        square_x, cross, square_y = _integer(x*x), _integer(x*y), _integer(y*y)
        terms = (_integer(self.quadratic*square_x), _integer(self.linear*cross), _integer(self.constant*square_y))
        return _integer(_integer(terms[0]+terms[1])+terms[2])

    def homogeneous_value(self, values: object) -> Outcome[int]:
        return evaluate(self._homogeneous_value, values)

    def _discriminant(self) -> int:
        square = _integer(self.linear*self.linear)
        product = _integer(_integer(4*self.quadratic)*self.constant)
        return _integer(square-product)

    def discriminant(self) -> Outcome[int]:
        return evaluate(self._discriminant)

    @staticmethod
    def square_root(value: object) -> Outcome[int | None]:
        """Return the nonnegative integer root, or None for a nonsquare."""
        return evaluate(_square_root, value)

    def _rational_roots(self) -> tuple[Q, ...]:
        roots: tuple[Q, ...]
        if self.quadratic == 0:
            if self.linear == 0:
                return ()
            roots = (rational(Q(-self.constant, self.linear), 'linear root'),)
        else:
            square_root = _square_root(self._discriminant())
            if square_root is None:
                return ()
            denominator = _integer(2*self.quadratic)
            roots = tuple(sorted({rational(Q(_integer(-self.linear+sign*square_root), denominator), 'quadratic root')
                                  for sign in (-1, 1)}))
        require(all(self._evaluate(root) == 0 for root in roots), 'calculated root fails exact substitution')
        return roots

    def rational_roots(self) -> Outcome[tuple[Q, ...]]:
        return evaluate(self._rational_roots)

    def _integer_roots(self) -> tuple[int, ...]:
        return tuple(root.numerator for root in self._rational_roots() if root.denominator == 1)

    def integer_roots(self) -> Outcome[tuple[int, ...]]:
        return evaluate(self._integer_roots)
