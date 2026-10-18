from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CochainState:
    values: tuple[tuple[tuple[int, int], float], ...]

    def __post_init__(self) -> None:
        edges = tuple(edge for edge, _ in self.values)
        if len(set(edges)) != len(edges):
            raise ValueError("cochain state contains duplicate edges")
        if any(not math.isfinite(float(value)) for _, value in self.values):
            raise ValueError("cochain values must be finite")

    @classmethod
    def from_mapping(cls, values: dict[tuple[int, int], float]) -> "CochainState":
        return cls(
            tuple(sorted(((edge, float(value)) for edge, value in values.items())))
        )

    def as_mapping(self) -> dict[tuple[int, int], float]:
        return dict(self.values)

    @property
    def raw_l1_mass(self) -> float:
        return float(sum(abs(value) for _, value in self.values))
