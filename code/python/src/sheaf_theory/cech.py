"""Finite Čech coboundary and the square-zero identity.

Origin: lean4/CellGrammar.lean theorem boundarySquare_implies_cochain
(d1(d0 alpha) is zero whenever the chain boundary squares to zero).
Claim: urn:omega:fqm:cech:coboundary-square-witness:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/sheaf_theory/test_cech_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: cech_square_witness checks delta(delta omega) = 0 for one
rational 0-cochain on a 3-set cover. Constant H^0 and the 1-cocycle test
are the same coboundary. This file does not prove the general dualization
theorem in CellGrammar.lean.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import combinations
from typing import Mapping, Sequence


class CechError(ValueError):
    """One violated Čech invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CechError:
    return CechError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the Čech boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the Čech boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


@dataclass(frozen=True)
class OpenSet:
    """Finite open set represented by point indices."""

    points: frozenset[int]

    @classmethod
    def from_iterable(cls, items: object) -> OpenSet:
        if isinstance(items, (str, bytes)) or not isinstance(items, (list, tuple, set, frozenset)):
            raise _fail("open set is not a collection of points", received=type(items).__name__)
        return cls(frozenset(_require_int(item, "point") for item in items))

    def intersection(self, other: OpenSet) -> OpenSet:
        partner = _require_open(other)
        return OpenSet(self.points.intersection(partner.points))

    def is_empty(self) -> bool:
        return len(self.points) == 0

    def contains(self, point: object) -> bool:
        return _require_int(point, "point") in self.points


def _require_open(value: object) -> OpenSet:
    if isinstance(value, OpenSet):
        return value
    raise _fail("value is not an open set", received=type(value).__name__)


@dataclass
class CechCochain:
    """Čech p-cochain with rational values on ordered index tuples."""

    degree: int
    data: dict[tuple[int, ...], Fraction] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.degree = _require_int(self.degree, "degree")
        if self.degree < 0:
            raise _fail("Čech degree is negative", degree=self.degree)
        self.data = _parse_cochain_data(self.data)

    def get(self, indices: object) -> Fraction:
        key = _sorted_indices(indices)
        return self.data.get(key, Fraction(0))

    def is_zero(self) -> bool:
        for value in self.data.values():
            if value != 0:
                return False
        return True


def _parse_cochain_data(data: object) -> dict[tuple[int, ...], Fraction]:
    if not isinstance(data, dict):
        raise _fail("cochain data is not a dictionary", received=type(data).__name__)
    parsed: dict[tuple[int, ...], Fraction] = {}
    for key, value in data.items():
        parsed[_sorted_indices(key)] = _require_fraction(value, "cochain value")
    return parsed


def _sorted_indices(indices: object) -> tuple[int, ...]:
    if isinstance(indices, (str, bytes)) or not isinstance(indices, tuple):
        raise _fail("cochain index is not a tuple", received=type(indices).__name__)
    return tuple(sorted(_require_int(item, "index") for item in indices))


def cech_coboundary_rational(cochain: object, cover: Sequence[object]) -> CechCochain:
    """Return delta omega on the nonempty intersections of the cover."""
    source = _require_cochain(cochain)
    opens = _require_cover(cover)
    degree = source.degree + 1
    data: dict[tuple[int, ...], Fraction] = {}
    for indices in combinations(range(len(opens)), degree + 1):
        _write_simplex(data, source, opens, indices)
    return CechCochain(degree, data)


def _require_cochain(value: object) -> CechCochain:
    if isinstance(value, CechCochain):
        return value
    raise _fail("value is not a Čech cochain", received=type(value).__name__)


def _require_cover(cover: Sequence[object]) -> tuple[OpenSet, ...]:
    if isinstance(cover, (str, bytes)) or not isinstance(cover, (list, tuple)):
        raise _fail("cover is not a sequence", received=type(cover).__name__)
    return tuple(_require_open(item) for item in cover)


def _write_simplex(
    data: dict[tuple[int, ...], Fraction],
    cochain: CechCochain,
    cover: tuple[OpenSet, ...],
    indices: tuple[int, ...],
) -> None:
    if _intersection_empty(cover, indices):
        return
    data[indices] = _alternating_sum(cochain, indices)


def _intersection_empty(cover: tuple[OpenSet, ...], indices: tuple[int, ...]) -> bool:
    points = cover[indices[0]].points
    for index in indices[1:]:
        points = points.intersection(cover[index].points)
    return len(points) == 0


def _alternating_sum(cochain: CechCochain, indices: tuple[int, ...]) -> Fraction:
    total = Fraction(0)
    for omitted in range(len(indices)):
        total += _signed_face(cochain, indices, omitted)
    return total


def _signed_face(cochain: CechCochain, indices: tuple[int, ...], omitted: int) -> Fraction:
    face = tuple(indices[index] for index in range(len(indices)) if index != omitted)
    value = cochain.get(face)
    if omitted % 2 == 1:
        return -value
    return value


def compute_cech_h0(cover: Sequence[object], constant_val: object) -> CechCochain | None:
    """Return the constant 0-cochain when it is closed."""
    opens = _require_cover(cover)
    value = _require_fraction(constant_val, "constant")
    data = {(index,): value for index in range(len(opens))}
    cochain = CechCochain(0, data)
    if cech_coboundary_rational(cochain, opens).is_zero():
        return cochain
    return None


def is_1_cocycle(cochain: object, cover: Sequence[object]) -> bool:
    """Return whether a degree-1 cochain is closed."""
    source = _require_cochain(cochain)
    if source.degree != 1:
        return False
    return cech_coboundary_rational(source, cover).is_zero()


def cech_square_witness() -> int:
    """Return 0 when delta squared vanishes on the sample 0-cochain."""
    cover = (
        OpenSet.from_iterable((0, 1, 2)),
        OpenSet.from_iterable((1, 2, 3)),
        OpenSet.from_iterable((2, 3, 0)),
    )
    cochain = CechCochain(0, {(0,): Fraction(1), (1,): Fraction(2), (2,): Fraction(5)})
    once = cech_coboundary_rational(cochain, cover)
    twice = cech_coboundary_rational(once, cover)
    if not twice.is_zero():
        raise _fail("Čech coboundary does not square to zero")
    if not is_1_cocycle(once, cover):
        raise _fail("Čech coboundary is not a 1-cocycle")
    return 0


def main() -> int:
    """Print the Čech square certificate."""
    try:
        print(cech_square_witness())
    except CechError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
