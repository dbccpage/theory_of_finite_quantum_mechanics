"""AuthorizationBoundary: a report cannot certify what it erased.

AuthorityEffect: None.

If p(x) = p(y) but independently defined valid(x) != valid(y), no
function of the report alone recovers valid. If valid is constant on
p-fibers (or p is the identity), a report-level decider exists.

External authorization is an added input, not a magical knower.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class BoundaryResult:
    factors: bool
    reason: str


def factors_through(
    xs: tuple[object, ...],
    p: Callable[[object], object],
    valid: Callable[[object], bool],
    decide: Callable[[object], bool],
) -> bool:
    return all(decide(p(x)) == valid(x) for x in xs)


def fiber_splits_valid(
    xs: tuple[object, ...],
    p: Callable[[object], object],
    valid: Callable[[object], bool],
) -> bool:
    reports: dict[object, bool] = {}
    for x in xs:
        r = p(x)
        v = valid(x)
        if r in reports and reports[r] != v:
            return True
        reports[r] = v
    return False


def no_report_decision(
    xs: tuple[object, ...],
    p: Callable[[object], object],
    valid: Callable[[object], bool],
) -> BoundaryResult:
    if not fiber_splits_valid(xs, p, valid):
        return BoundaryResult(True, "fiber does not split valid; report-level decider exists")
    # Exhaust the two constant deciders on a singleton report space,
    # and more generally check that every decide on the image fails.
    image = {p(x) for x in xs}
    for bits in _bool_assignments(sorted(image, key=repr)):
        decide = bits.__getitem__
        if factors_through(xs, p, valid, decide):
            return BoundaryResult(True, "unexpected decider")
    return BoundaryResult(False, "no report-only decider")


def _bool_assignments(keys: list[object]) -> list[dict[object, bool]]:
    if not keys:
        return [{}]
    rest = _bool_assignments(keys[1:])
    return [{keys[0]: False, **r} for r in rest] + [
        {keys[0]: True, **r} for r in rest
    ]


def p_neg(x: object) -> object:
    return ()


def valid_neg(x: object) -> bool:
    return bool(x)


def p_pos(x: object) -> object:
    return x


def valid_pos(x: object) -> bool:
    return bool(x)


def with_extra(
    p: Callable[[object], object],
    extra: Callable[[object], object],
    k: Callable[[object, object], bool],
    x: object,
) -> bool:
    return k(p(x), extra(x))
