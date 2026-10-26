"""Second-order jet of one rational quadratic in two variables.

Origin: papers/core/mub6/documentation/observation_quartic_overlap_secant_failure.md,
which states that the midpoint secant identity holds strictly for quadratic
polynomials and that a degree-4 overlap has a non-vanishing second-order remainder.
Claim: urn:omega:fqm:linear-algebra:second-jet:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_second_jet.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: certify_taylor checks f(x, y) = x^2 + 3xy + (1/2) y^2 + 4x - y
at the rational point and step it is given. The defect is the second-order
Taylor remainder of that one polynomial. This file does not bound the degree-4
Krawczyk remainder, does not add auxiliary bilinear variables, and does not
admit floats or Q(i).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class JetError(MatrixError):
    """One violated jet invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> JetError:
    return JetError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_rational(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational coordinate was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; the second jet in this module is over Q", role=role)
    if type(value) is Fraction:
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("coordinate is not an exact rational", role=role, received=type(value).__name__)


def quadratic_value(x: object, y: object) -> Fraction:
    """f(x, y) = x^2 + 3xy + (1/2) y^2 + 4x - y."""
    xx = _require_rational(x, "x")
    yy = _require_rational(y, "y")
    return xx * xx + 3 * xx * yy + Fraction(1, 2) * yy * yy + 4 * xx - yy


def _gradient(x: Fraction, y: Fraction) -> tuple[Fraction, Fraction]:
    return (2 * x + 3 * y + 4, 3 * x + y - 1)


def _hessian() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(2), Fraction(3)],
            [Fraction(3), Fraction(1)],
        ]
    )


def second_jet(x: object, y: object) -> tuple[Fraction, tuple[Fraction, Fraction], ExactMatrix]:
    """Return f(a), ∇f(a), and the constant Hessian of the quadratic."""
    xx = _require_rational(x, "x")
    yy = _require_rational(y, "y")
    return quadratic_value(xx, yy), _gradient(xx, yy), _hessian()


def _quadratic_form(hessian: ExactMatrix, step_x: Fraction, step_y: Fraction) -> Fraction:
    h00 = _require_rational(hessian.get(0, 0), "h00")
    h01 = _require_rational(hessian.get(0, 1), "h01")
    h11 = _require_rational(hessian.get(1, 1), "h11")
    cross = (h01 + h01) * step_x * step_y
    return h00 * step_x * step_x + cross + h11 * step_y * step_y


def taylor_defect(base_x: object, base_y: object, step_x: object, step_y: object) -> Fraction:
    """f(a+h) - (f(a) + ∇f·h + (1/2) h^T H h)."""
    hx = _require_rational(step_x, "step_x")
    hy = _require_rational(step_y, "step_y")
    value, gradient, hessian = second_jet(base_x, base_y)
    linear = gradient[0] * hx + gradient[1] * hy
    quad_form = _quadratic_form(hessian, hx, hy)
    predicted = value + linear + quad_form / 2
    moved_x = _require_rational(base_x, "base_x") + hx
    moved_y = _require_rational(base_y, "base_y") + hy
    return quadratic_value(moved_x, moved_y) - predicted


def _require_zero_defect(defect: Fraction) -> None:
    if defect != 0:
        raise _fail("Taylor defect is nonzero", defect=str(defect))


def certify_taylor(base_x: object, base_y: object, step_x: object, step_y: object) -> Fraction:
    """Return the Taylor defect after requiring it to be zero."""
    defect = taylor_defect(base_x, base_y, step_x, step_y)
    _require_zero_defect(defect)
    return defect


__all__ = [
    "ExactMatrix",
    "JetError",
    "certify_taylor",
    "quadratic_value",
    "second_jet",
    "taylor_defect",
]
