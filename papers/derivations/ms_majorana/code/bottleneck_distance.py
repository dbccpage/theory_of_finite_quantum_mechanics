"""Exact bottleneck distance for diagrams with at most one finite point.

Origin: papers/derivations/ms_majorana/code/persistence_diagram.py
Claim: urn:omega:fqm:ms-majorana:bottleneck:at-most-one-point:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: Diagrams with two or more points are refused. The distance is not a float matching heuristic.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping

from .persistence_diagram import PersistenceDiagram, PersistencePoint


class BottleneckError(ValueError):
    """One violated bottleneck invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> BottleneckError:
    return BottleneckError(invariant, parameters)


def _point(diagram: object, role: str) -> PersistencePoint | None:
    if not isinstance(diagram, PersistenceDiagram):
        raise _fail("bottleneck requires a persistence diagram", role=role, received=type(diagram).__name__)
    if len(diagram.points) > 1:
        raise _fail("bottleneck certificate admits at most one finite point", role=role, count=len(diagram.points))
    if len(diagram.points) == 0:
        return None
    return diagram.points[0]


def diagonal_cost(point: PersistencePoint) -> Fraction:
    """Half the exact persistence of one finite point."""
    if not isinstance(point, PersistencePoint):
        raise _fail("diagonal cost requires a persistence point", received=type(point).__name__)
    if point.death <= point.birth:
        raise _fail("death is not strictly after birth", birth=str(point.birth), death=str(point.death))
    return (point.death - point.birth) / 2


def _pair_cost(left: PersistencePoint, right: PersistencePoint) -> Fraction:
    birth_gap = abs(left.birth - right.birth)
    death_gap = abs(left.death - right.death)
    if birth_gap > death_gap:
        return birth_gap
    return death_gap


@dataclass(frozen=True)
class BottleneckCertificate:
    """Witness of the exact one-point bottleneck distance."""

    distance: Fraction


def _one_empty(point: PersistencePoint | None, other: PersistencePoint | None) -> Fraction | None:
    if point is None and other is None:
        return Fraction(0)
    if point is None and other is not None:
        return diagonal_cost(other)
    if other is None and point is not None:
        return diagonal_cost(point)
    return None


def bottleneck_distance(left: object, right: object) -> Fraction:
    """Return the bottleneck distance of two diagrams of size at most one."""
    first = _point(left, "left")
    second = _point(right, "right")
    partial = _one_empty(first, second)
    if partial is not None:
        return partial
    if first is None or second is None:
        raise _fail("one-point branch was not classified")
    matched = _pair_cost(first, second)
    diagonal = diagonal_cost(first)
    other = diagonal_cost(second)
    cap = diagonal if diagonal > other else other
    if matched < cap:
        return matched
    return cap


def certify_bottleneck(left: object, right: object) -> BottleneckCertificate:
    """Recheck the one-point bottleneck distance."""
    return BottleneckCertificate(bottleneck_distance(left, right))


__all__ = [
    "BottleneckCertificate",
    "BottleneckError",
    "bottleneck_distance",
    "certify_bottleneck",
    "diagonal_cost",
]
