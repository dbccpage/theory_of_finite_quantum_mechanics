"""Exact rational filtration. Birth values are Fractions and must be nondecreasing.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/filtration.py
Claim: urn:omega:fqm:ms-majorana:filtration:nondecreasing-rationals:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: This file does not compute persistent homology and does not admit binary-float birth times.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class FiltrationError(ValueError):
    """One violated filtration invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> FiltrationError:
    return FiltrationError(invariant, parameters)


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


def _vertices(values: object, role: str) -> tuple[int, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or len(values) == 0:
        raise _fail("simplex vertices must be a nonempty sequence", role=role, received=type(values).__name__)
    parsed: list[int] = []
    for index, item in enumerate(values):
        if isinstance(item, bool) or type(item) is not int:
            raise _fail("vertex is not an exact index", role=f"{role}[{index}]", received=type(item).__name__)
        parsed.append(item)
    return tuple(parsed)


@dataclass(frozen=True)
class FilteredSimplex:
    """One simplex admitted at an exact rational filtration value."""

    vertices: tuple[int, ...]
    value: Fraction
    dimension: int


@dataclass(frozen=True)
class Filtration:
    """A finite filtration whose values are rechecked to be nondecreasing."""

    simplices: tuple[FilteredSimplex, ...]
    max_dimension: int

    def __len__(self) -> int:
        return len(self.simplices)

    def values_nondecreasing(self) -> bool:
        previous = self.simplices[0].value if len(self.simplices) else Fraction(0)
        for simplex in self.simplices:
            if simplex.value < previous:
                return False
            previous = simplex.value
        return True


def _simplex(vertices: object, value: object, dimension: object) -> FilteredSimplex:
    if isinstance(dimension, bool) or type(dimension) is not int or dimension < 0:
        raise _fail("dimension is not a nonnegative integer", received=type(dimension).__name__)
    parsed = FilteredSimplex(_vertices(vertices, "vertices"), _rational(value, "value"), dimension)
    if len(parsed.vertices) != dimension + 1:
        raise _fail("vertex count does not match the dimension", vertices=len(parsed.vertices), dimension=dimension)
    return parsed


def certify_filtration(records: object) -> Filtration:
    """Admit simplices and refuse a decrease in the rational filtration value."""
    if isinstance(records, (str, bytes)) or not isinstance(records, Sequence):
        raise _fail("filtration records must be a sequence", received=type(records).__name__)
    simplices: list[FilteredSimplex] = []
    max_dimension = 0
    for index, record in enumerate(records):
        if isinstance(record, (str, bytes)) or not isinstance(record, Sequence) or len(record) != 3:
            raise _fail("filtration record must be a triple", role=f"records[{index}]", received=type(record).__name__)
        simplex = _simplex(record[0], record[1], record[2])
        simplices.append(simplex)
        if simplex.dimension > max_dimension:
            max_dimension = simplex.dimension
    filtration = Filtration(tuple(simplices), max_dimension)
    if not filtration.values_nondecreasing():
        raise _fail("filtration values are not nondecreasing")
    return filtration


__all__ = ["FilteredSimplex", "Filtration", "FiltrationError", "certify_filtration"]
