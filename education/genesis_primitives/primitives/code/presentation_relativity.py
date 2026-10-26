"""Genesis Primitives Category 13: Presentation Relativity & Gauge Frame Transformations.

Selected educational models related to 19L57G1 (lean4/Derivation/PresentationRelativity.lean, PresentationNaturality.lean).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

Local presentation frames, frame transformations between observers, gauge invariance
of relational observables, and naturality squares across coordinate patches.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence

from .canonical import FrozenMap, validate_typed_fields

Rel = frozenset[tuple[int, int]]


@dataclass(frozen=True)
class PresentationFrame:
    """A localized presentation basis/coordinate system for relational observations."""

    frame_id: str
    carrier_size: int
    local_relations: Rel

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class FrameTransformation:
    """Relational coordinate transformation mapping Frame 1 to Frame 2."""

    source_frame: str
    target_frame: str
    mapping: dict[int, int]

    def __post_init__(self) -> None:
        object.__setattr__(self, "mapping", FrozenMap(self.mapping))
        if len(set(self.mapping.values())) != len(self.mapping):
            raise ValueError(
                "REFUSED_SHAPE: frame coordinate change must be bijective on its image"
            )
        validate_typed_fields(self)

    def transform_pair(self, p: tuple[int, int]) -> tuple[int, int]:
        return (self.mapping[p[0]], self.mapping[p[1]])

    def transform_rel(self, r: Rel) -> Rel:
        return frozenset(self.transform_pair(p) for p in r)


def is_gauge_invariant_observable(
    obs_func: Callable[[Rel], Any],
    r: Rel,
    transforms: Sequence[FrameTransformation],
) -> bool:
    """Verifies that an observable quantity on relation r is invariant across frame transformations."""
    val0 = obs_func(r)
    return all(obs_func(t.transform_rel(r)) == val0 for t in transforms)
