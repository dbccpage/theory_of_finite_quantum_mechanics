"""One-skeleton Vietoris-Rips filtration at an exact rational radius.

Origin: papers/derivations/ms_majorana/code/filtration.py
Claim: urn:omega:fqm:ms-majorana:vietoris-rips:one-skeleton:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: Only vertices and edges are admitted. This file does not build higher simplices or a metric completion.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence

from .filtration import FilteredSimplex, Filtration, certify_filtration


class VietorisError(ValueError):
    """One violated Vietoris-Rips invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> VietorisError:
    return VietorisError(invariant, parameters)


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


@dataclass(frozen=True)
class PointCloud:
    """A finite distance matrix stored row-major as exact rationals."""

    distances: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        count = _count(len(self.distances))
        if count * count != len(self.distances):
            raise _fail("distance table is not square", length=len(self.distances))

    def size(self) -> int:
        return _count(len(self.distances))

    def distance(self, left: int, right: int) -> Fraction:
        width = self.size()
        return self.distances[left * width + right]


def _count(length: int) -> int:
    index = 0
    while index * index < length:
        index += 1
    return index


def cloud(distances: object) -> PointCloud:
    """Admit a square table of exact distances."""
    if isinstance(distances, (str, bytes)) or not isinstance(distances, Sequence):
        raise _fail("distances must be a sequence", received=type(distances).__name__)
    parsed = tuple(_rational(item, f"distances[{index}]") for index, item in enumerate(distances))
    return PointCloud(parsed)


def _edges(table: PointCloud, radius: Fraction) -> list[tuple[tuple[int, ...], Fraction, int]]:
    records: list[tuple[tuple[int, ...], Fraction, int]] = []
    width = table.size()
    for left in range(width):
        records.append(((left,), Fraction(0), 0))
    for left in range(width):
        for right in range(left + 1, width):
            gap = table.distance(left, right)
            if gap <= radius:
                records.append(((left, right), gap, 1))
    return records


def vietoris_rips_filtration(distances: object, radius: object) -> Filtration:
    """Build the 1-skeleton filtration and recheck that its values are nondecreasing."""
    table = cloud(distances)
    limit = _rational(radius, "radius")
    if limit < 0:
        raise _fail("radius is negative", radius=str(limit))
    records = _edges(table, limit)
    ordered = tuple(sorted(records, key=lambda item: (item[1], item[2], item[0])))
    filtration = certify_filtration(ordered)
    for simplex in filtration.simplices:
        if simplex.dimension == 1 and simplex.value > limit:
            raise _fail("edge exceeds the declared radius", value=str(simplex.value), radius=str(limit))
    return filtration


__all__ = ["PointCloud", "VietorisError", "cloud", "vietoris_rips_filtration"]
