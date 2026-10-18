"""Finite persistence points with exact rational birth and death.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/persistence_diagram.py
Claim: urn:omega:fqm:ms-majorana:persistence:finite-bars:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: Infinite bars are refused. This file does not compute a persistence module.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class PersistenceError(ValueError):
    """One violated persistence invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> PersistenceError:
    return PersistenceError(invariant, parameters)


def _rational(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _dimension(value: object) -> int:
    if isinstance(value, bool) or type(value) is not int or value < 0:
        raise _fail("dimension is not a nonnegative integer", received=type(value).__name__)
    return value


@dataclass(frozen=True)
class PersistencePoint:
    """One finite bar. Death is strictly later than birth."""

    birth: Fraction
    death: Fraction
    dimension: int

    def persistence(self) -> Fraction:
        return self.death - self.birth


@dataclass(frozen=True)
class PersistenceDiagram:
    """A finite set of finite bars."""

    points: tuple[PersistencePoint, ...]

    def finite_only(self) -> tuple[PersistencePoint, ...]:
        return self.points


def finite(birth: object, death: object, dimension: object) -> PersistencePoint:
    """Admit one finite bar."""
    born = _rational(birth, "birth")
    died = _rational(death, "death")
    if died <= born:
        raise _fail("death is not strictly after birth", birth=str(born), death=str(died))
    return PersistencePoint(born, died, _dimension(dimension))


def certify_diagram(records: object) -> PersistenceDiagram:
    """Admit a sequence of (birth, death, dimension) triples."""
    if isinstance(records, (str, bytes)) or not isinstance(records, Sequence):
        raise _fail("diagram records must be a sequence", received=type(records).__name__)
    points: list[PersistencePoint] = []
    for index, record in enumerate(records):
        if isinstance(record, (str, bytes)) or not isinstance(record, Sequence) or len(record) != 3:
            raise _fail("diagram record must be a triple", role=f"records[{index}]", received=type(record).__name__)
        points.append(finite(record[0], record[1], record[2]))
    return PersistenceDiagram(tuple(points))


__all__ = ["PersistenceDiagram", "PersistenceError", "PersistencePoint", "certify_diagram", "finite"]
