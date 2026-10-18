"""Fin 2 identity fails to preserve observer zero-relatedness.

Origin: lean4/WorldObserverFunctoriality.lean theorem fin2_source_zero
(constant observation identifies Fin 2 points 0 and 1), theorem
fin2_target_nonzero (separating observation distinguishes them: false at 0
and true otherwise), and theorem fin2_failure_coordinatewise_minimal
(those two source points and their identity images are distinct).
Claim: urn:omega:fqm:observer:fin2-identity-failure:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_observer_functor.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 5; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: identity_failure(0, 1) returns 1 when that witness holds.
Other integers use the same observe definitions and are not further Fin 2
theorems. composition_defect returns the trace of the rational product
[[1, 0], [1/3, 1]] [[1, 1/2], [0, 1]], which is 13/6. That trace is not
any of the cited theorems. This file does not prove quotient-factor
uniqueness or that every subsingleton carrier preserves zero-relatedness.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_SOURCE_AGREE = False


class ObserverFunctorError(Exception):
    """One violated observer invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ObserverFunctorError:
    return ObserverFunctorError(invariant, parameters)


def _require_point(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the point boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer point was required", role=role)
    if type(value) is not int:
        raise _fail("point is not an integer", role=role, received=type(value).__name__)
    return value


def _constant(_point: int) -> bool:
    return _SOURCE_AGREE


def _separating(point: int) -> bool:
    return point != 0


def _named_failure(source: int, target: int) -> int:
    if _constant(source) is not False or _constant(target) is not False:
        raise _fail("constant observations separated the source", left=source, right=target)
    if _separating(source) is not False or _separating(target) is not True:
        raise _fail("separating observations left false/true", left=source, right=target)
    if source == target:
        raise _fail("identity images coincided", left=source, right=target)
    return 1


def identity_failure(left: object = 0, right: object = 1) -> int:
    """Return 1 when the Fin 2 identity witness holds for these points."""
    source = _require_point(left, "left")
    target = _require_point(right, "right")
    if source == 0 and target == 1:
        return _named_failure(source, target)
    if _separating(source) != _separating(target) and source != target:
        return 1
    return 0


def _product_entry(row: tuple[Fraction, Fraction], left: Fraction, right: Fraction) -> Fraction:
    return row[0] * left + row[1] * right


def composition_defect() -> Fraction:
    """Return the trace of the fenced rational matrix product, 13/6."""
    arrow_f = ((Fraction(1), Fraction(1, 2)), (Fraction(0), Fraction(1)))
    arrow_g = ((Fraction(1), Fraction(0)), (Fraction(1, 3), Fraction(1)))
    trace = _product_entry(arrow_g[0], arrow_f[0][0], arrow_f[1][0])
    trace += _product_entry(arrow_g[1], arrow_f[0][1], arrow_f[1][1])
    if trace != Fraction(13, 6):
        raise _fail("matrix trace left 13/6", trace=str(trace))
    return trace


def main() -> int:
    value = identity_failure()
    print(value)
    if value == 1 and composition_defect() == Fraction(13, 6):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
