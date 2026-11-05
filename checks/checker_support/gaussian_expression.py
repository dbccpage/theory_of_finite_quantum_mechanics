"""Bounded exact Gaussian expressions without text parsing. AuthorityEffect: None.

Native int/Fraction/GaussianRational and exact SymPy rational/I expressions are
admitted. Expression syntax is Add, Mul and integer powers -16..16, with at
most 64 nodes and depth 8. Every owned Gaussian component has <=4096 bits.
"""
from __future__ import annotations

from fractions import Fraction as Q
from typing import cast
import sympy as sp

from .boundary import Violation, evaluate
from .domains import rational
from .gaussian_rational import GaussianRational as G
from .outcome import Outcome

_RATIONAL_TYPES = frozenset(type(sp.Rational(p, q)) for p, q in
                            ((0, 1), (1, 1), (-1, 1), (2, 1), (1, 2), (2, 3), (-1, 2)))
_IMAGINARY_TYPE = type(sp.I)
_OPERATORS = (sp.Add, sp.Mul, sp.Pow)


def _atom(value: sp.Rational) -> Q:
    numerator = rational(int(value.p), "expression numerator").numerator
    denominator = rational(int(value.q), "expression denominator").numerator
    return Q(numerator, denominator)


def _shape(value: object, depth: int, remaining: int) -> int:
    if depth > 8 or remaining == 0:
        raise Violation("resource", "Gaussian expression exceeds depth 8 or 64 nodes")
    remaining -= 1
    if type(value) in _RATIONAL_TYPES:
        _atom(cast(sp.Rational, value))
        return remaining
    if type(value) is _IMAGINARY_TYPE:
        return remaining
    if type(value) not in _OPERATORS:
        raise Violation("input", "Gaussian expression requires exact atoms, Add, Mul or integer Pow")
    expression = cast(sp.Expr, value)
    for argument in expression.args:
        remaining = _shape(argument, depth+1, remaining)
    if type(value) is sp.Pow:
        if type(expression.args[1]) not in _RATIONAL_TYPES:
            raise Violation("input", "Gaussian expression exponent requires a rational atom")
        exponent = _atom(expression.args[1])
        if exponent.denominator != 1:
            raise Violation("input", "Gaussian expression exponent must be integral")
        if abs(exponent) > 16:
            raise Violation("resource", "Gaussian expression exponent exceeds 16")
    return remaining


def _power(base: G, exponent: int) -> G:
    factor = base.inv() if exponent < 0 else base
    result = G(1)
    for _ in range(abs(exponent)):
        result = result.mul(factor)
    return result


def _value(expression: sp.Expr) -> G:
    if type(expression) in _RATIONAL_TYPES:
        return G(_atom(expression))
    if type(expression) is _IMAGINARY_TYPE:
        return G(0, 1)
    if type(expression) is sp.Pow:
        return _power(_value(expression.args[0]), int(expression.args[1]))
    result = G(0) if type(expression) is sp.Add else G(1)
    for argument in expression.args:
        operand = _value(argument)
        result = result+operand if type(expression) is sp.Add else result.mul(operand)
    return result


def _decode(value: object) -> G:
    if type(value) is G:
        return G(value.re, value.im)
    if type(value) in (int, Q):
        return G(value)
    _shape(value, 0, 64)
    return _value(cast(sp.Expr, value))


def decode(value: object) -> Outcome[G]:
    return evaluate(_decode, value)


def _encode(value: object) -> sp.Expr:
    if type(value) is not G:
        raise Violation("input", "Gaussian encoding requires an owned GaussianRational")
    return (sp.Rational(value.re.numerator, value.re.denominator)
            + sp.I*sp.Rational(value.im.numerator, value.im.denominator))


def encode(value: object) -> Outcome[sp.Expr]:
    return evaluate(_encode, value)
