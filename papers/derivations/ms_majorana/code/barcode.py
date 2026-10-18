"""Exact barcode read off a finite persistence diagram.

Origin: papers/derivations/ms_majorana/code/persistence_diagram.py
Claim: urn:omega:fqm:ms-majorana:barcode:finite-bars:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: Bar length is death minus birth. It is not a physical lifetime.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping

from .persistence_diagram import PersistenceDiagram, PersistencePoint


class BarcodeError(ValueError):
    """One violated barcode invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> BarcodeError:
    return BarcodeError(invariant, parameters)


@dataclass(frozen=True)
class Bar:
    """One finite bar copied from a persistence point."""

    birth: Fraction
    death: Fraction
    dimension: int

    def length(self) -> Fraction:
        return self.death - self.birth


@dataclass(frozen=True)
class Barcode:
    """The multiset of finite bars of one diagram."""

    bars: tuple[Bar, ...]


def _bar(point: PersistencePoint) -> Bar:
    if point.death <= point.birth:
        raise _fail("bar death is not strictly after birth", birth=str(point.birth), death=str(point.death))
    return Bar(point.birth, point.death, point.dimension)


def from_diagram(diagram: object) -> Barcode:
    """Copy each finite point into a bar and recheck its length."""
    if not isinstance(diagram, PersistenceDiagram):
        raise _fail("barcode requires a persistence diagram", received=type(diagram).__name__)
    bars = tuple(_bar(point) for point in diagram.points)
    return Barcode(bars)


def total_length(barcode: Barcode) -> Fraction:
    """Sum the exact lengths of the bars."""
    if not isinstance(barcode, Barcode):
        raise _fail("total length requires a barcode", received=type(barcode).__name__)
    total = Fraction(0)
    for bar in barcode.bars:
        total += bar.length()
    return total


__all__ = ["Bar", "Barcode", "BarcodeError", "from_diagram", "total_length"]
