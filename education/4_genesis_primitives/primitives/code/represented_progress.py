"""Genesis Primitives Category 18: Represented Progress, Retractions & Proposal Records.

Selected educational models related to 19L57G1 (lean4/Derivation/Represented.lean, Completion.lean, code/derivation/represented.py).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

The represented-progress kernel World, satisfaction and violation predicates,
down-map retractions, and represented extension proposals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from .canonical import FrozenMap, validate_typed_fields

View = tuple[int, ...]
Req = tuple[int, int]
Event = tuple[Any, ...]


@dataclass(frozen=True)
class World:
    """Represented-progress kernel state: explicit data, observation views, requirements,
    refusal logs, and execution budget. No unrepresented state reaches transitions."""

    data: tuple[int, ...] = ()
    views: tuple[View, ...] = ()
    reqs: tuple[Req, ...] = ()
    refusals: tuple[Req, ...] = ()
    budget: int = 0
    aug_licensed: bool = True
    notes: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        validate_typed_fields(self)


GENESIS_WORLD = World()


def sep(c: View, i: int, j: int) -> bool:
    """View separation: element i is in view c XOR element j is in view c."""
    return (i in c) != (j in c)


def sat(w: World, r: Req) -> bool:
    """Satisfaction: at least one view in the world separates the required pair."""
    return any(sep(c, r[0], r[1]) for c in w.views)


def viol(w: World, r: Req) -> bool:
    """Violation: requirement is asserted in reqs but unseparated by all views."""
    return r in w.reqs and not sat(w, r)


def quiescent(w: World) -> bool:
    """Quiescence: all imposed requirements are satisfied."""
    return all(sat(w, r) for r in w.reqs)


@dataclass(frozen=True)
class ProposalRecord:
    """Represented extension proposal equipped with an explicit retraction down-map."""

    name: str
    target_pair: Req
    down_map: dict[int, int]  # Retraction r: Extended -> Base satisfying r(i) = i on Base
    cost: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "down_map", FrozenMap(self.down_map))
        validate_typed_fields(self)

    def is_valid_retraction(self, base_data: Sequence[int]) -> bool:
        """Verifies that the down-map acts as the identity on the base carrier."""
        if any(type(point) is not int or point < 0 for point in base_data):
            return False
        return all(self.down_map.get(x) == x for x in base_data)
