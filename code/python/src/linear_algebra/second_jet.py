"""Second-order jet of a rational polynomial in two variables.

Origin: code/python/src/linear_algebra/second_jet.py
Claim: a polynomial of total degree at most 2 equals its second-order Taylor expansion.
AuthorityEffect: None. Higher-degree remainders are not estimated.
"""
from fractions import Fraction
from typing import Tuple

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class JetError(Exception):
    """A jet coordinate was not rational."""


def _fraction(value) -> Fraction:
    if isinstance(value, GaussianRational):
        raise JetError("the second jet in this module is over Q, not Q(i)")
    try:
        return Fraction(value)
    except (TypeError, ValueError) as exc:
        raise JetError(f"value {value!r} is not rational") from exc


def quadratic_value(x: object, y: object) -> Fraction:
    """f(x, y) = x^2 + 3xy + (1/2) y^2 + 4x − y."""
    xx = _fraction(x)
    yy = _fraction(y)
    return xx * xx + 3 * xx * yy + Fraction(1, 2) * yy * yy + 4 * xx - yy


def second_jet(x: object, y: object) -> Tuple[Fraction, Tuple[Fraction, Fraction], ExactMatrix]:
    """Return f(a), ∇f(a), and the constant Hessian of the quadratic."""
    xx = _fraction(x)
    yy = _fraction(y)
    value = quadratic_value(xx, yy)
    gradient = (2 * xx + 3 * yy + 4, 3 * xx + yy - 1)
    hessian = ExactMatrix.from_rows(
        [
            [Fraction(2), Fraction(3)],
            [Fraction(3), Fraction(1)],
        ]
    )
    return value, gradient, hessian


def taylor_defect(base_x: object, base_y: object, step_x: object, step_y: object) -> Fraction:
    """f(a+h) − (f(a) + ∇f·h + (1/2) h^T H h), which is 0 for this quadratic."""
    hx = _fraction(step_x)
    hy = _fraction(step_y)
    value, gradient, hessian = second_jet(base_x, base_y)
    linear = gradient[0] * hx + gradient[1] * hy
    quad_form = (
        Fraction(hessian.get(0, 0)) * hx * hx
        + Fraction(2) * Fraction(hessian.get(0, 1)) * hx * hy
        + Fraction(hessian.get(1, 1)) * hy * hy
    )
    predicted = value + linear + quad_form / 2
    return quadratic_value(_fraction(base_x) + hx, _fraction(base_y) + hy) - predicted


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "JetError",
    "quadratic_value",
    "second_jet",
    "taylor_defect",
]
