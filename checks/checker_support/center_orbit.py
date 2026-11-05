"""Bounded three-color boundary polynomial and C3 sum. AuthorityEffect: None.

Coefficients lie in Q(i), degrees -3..3. Evaluation at the three declared
center roots lies in Q(i,sqrt(3)); no gauge measure or continuation is implied.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Any
import sympy as sp

from .boundary import Violation, evaluate
from .domains import integer, rational, sequence
from .gaussian_expression import _decode, _encode
from .gaussian_matrix import GaussianMatrix as M
from .gaussian_rational import GaussianRational as G
from .outcome import Outcome

_T = sp.Symbol("t", nonzero=True)
_OMEGA = (-1+sp.sqrt(3)*sp.I)/2
_FIELD = sp.QQ.algebraic_field(sp.I, sp.sqrt(3))
_ROOT = _FIELD.from_sympy(_OMEGA)
_IMAGINARY = _FIELD.from_sympy(sp.I)
_PHASES = tuple(tuple(_ROOT**(((i-3)*k) % 3) for i in range(7)) for k in range(3))


def _field_admit(value: Any) -> Any:
    """Admit coordinates of the trusted four-dimensional exact algebraic field."""
    for coefficient in value.to_list():
        rational(int(coefficient.numerator), "center-field numerator")
        rational(int(coefficient.denominator), "center-field denominator")
    return value


def _coefficient(value: G) -> Any:
    """Embed the owned Q(i) value directly; the imaginary basis is already known."""
    real = _FIELD.convert(value.re.numerator)/_FIELD.convert(value.re.denominator)
    imaginary = _FIELD.convert(value.im.numerator)/_FIELD.convert(value.im.denominator)
    return _field_admit(real+imaginary*_IMAGINARY)


def _one() -> LaurentCenterPolynomial:
    return LaurentCenterPolynomial((0, 0, 0, 1, 0, 0, 0))


def _entry(link: M, adjoint: M, i: int, j: int) -> LaurentCenterPolynomial:
    return LaurentCenterPolynomial((0, 0, adjoint.rows[i][j].div(G(4)),
                                    G(3).div(G(2)) if i == j else G(0),
                                    link.rows[i][j].div(G(4)), 0, 0))


@dataclass(frozen=True, slots=True, init=False)
class LaurentCenterPolynomial:
    """Owns seven Gaussian coefficients, ordered by exponents -3 through 3."""
    coefficients: tuple[G, ...]

    def __init__(self, coefficients: object) -> None:
        entries = sequence(coefficients, "center coefficients", 7, 7)
        owned = tuple(_decode(entry) for entry in entries)
        object.__setattr__(self, "coefficients", owned)

    def add(self, other: object) -> LaurentCenterPolynomial:
        if type(other) is not LaurentCenterPolynomial:
            raise Violation("input", "center addition requires an owned polynomial")
        return LaurentCenterPolynomial(tuple(a+b for a, b in zip(self.coefficients, other.coefficients)))

    def scale(self, scalar: object) -> LaurentCenterPolynomial:
        factor = _decode(scalar)
        return LaurentCenterPolynomial(tuple(value.mul(factor) for value in self.coefficients))

    def mul(self, other: object) -> LaurentCenterPolynomial:
        if type(other) is not LaurentCenterPolynomial:
            raise Violation("input", "center multiplication requires an owned polynomial")
        result = [G(0) for _ in range(7)]
        for i, left in enumerate(self.coefficients):
            for j, right in enumerate(other.coefficients):
                product = left.mul(right)
                if product == G(0):
                    continue
                index = i+j-3
                if not 0 <= index < 7:
                    raise Violation("resource", "center product exceeds degrees -3..3")
                result[index] = result[index]+product
        return LaurentCenterPolynomial(result)

    def expression(self) -> sp.Expr:
        return sp.expand(sum(_encode(value)*_T**(i-3) for i, value in enumerate(self.coefficients)))

    def _evaluate(self, center_index: object) -> sp.Expr:
        index = integer(center_index, "center index", 0, 2)
        total = _FIELD.zero
        for i, coefficient in enumerate(self.coefficients):
            scalar = _coefficient(coefficient)
            phase = _PHASES[index][i]
            term = _field_admit(scalar*phase)
            total = _field_admit(total+term)
        return _FIELD.to_sympy(total)

    def evaluate(self, center_index: object) -> Outcome[sp.Expr]:
        return evaluate(self._evaluate, center_index)

    def _center(self) -> LaurentCenterPolynomial:
        return LaurentCenterPolynomial(tuple(value.mul(G(3)) if (i-3) % 3 == 0 else G(0)
                                              for i, value in enumerate(self.coefficients)))

    def center(self) -> Outcome[LaurentCenterPolynomial]:
        """Unnormalized finite C3 orbit sum: retain only degree multiples of three."""
        return evaluate(self._center)

    @classmethod
    def _from_boundary(cls, link: object) -> LaurentCenterPolynomial:
        if type(link) is not M:
            raise Violation("input", "boundary requires an owned GaussianMatrix")
        link.require_shape(3, 3)
        adjoint = link.adjoint()
        if adjoint.mul(link) != M.eye(3) or link.determinant() != G(1):
            raise Violation("input", "boundary link requires SU(3)")
        entries = tuple(tuple(_entry(link, adjoint, i, j) for j in range(3)) for i in range(3))
        result = cls((0,)*7)
        for order in permutations(range(3)):
            inversions = sum(order[i] > order[j] for i in range(3) for j in range(i+1, 3))
            term = _one()
            for i, column in enumerate(order):
                term = term.mul(entries[i][column])
            result = result.add(term.scale((-1)**inversions))
        return result

    @classmethod
    def from_boundary(cls, link: object) -> Outcome[LaurentCenterPolynomial]:
        """det(I6+(F-Fback)/2) = det(3I3/2+(tL+L*/t)/4) for a unitary L."""
        return evaluate(cls._from_boundary, link)
