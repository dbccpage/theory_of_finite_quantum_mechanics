"""Value types shared by contracted quantum engine modules."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from omega_engine.crates.linear_algebra_theory.density import NumericalDensityMatrix


class DensityConstruction(Enum):
    PureOuterProduct = "PureOuterProduct"
    SequenceMixture = "SequenceMixture"
    ResponseEnsemble = "ResponseEnsemble"
    WindowedTrajectory = "WindowedTrajectory"
    CovarianceDensity = "CovarianceDensity"
    GraphLaplacian = "GraphLaplacian"
    ProductSpacePartialTrace = "ProductSpacePartialTrace"


@dataclass
class DensityConstructionReport:
    construction: DensityConstruction
    rank: int
    entropy: float
    purity: float
    source_count: int
    top_k: Optional[int]


@dataclass(frozen=True)
class LabIoDim:
    dim_in: int
    dim_out: int

    @classmethod
    def new(cls, dim_in: int, dim_out: int) -> "LabIoDim":
        if dim_in == 0 or dim_out == 0:
            raise ValueError("dimension mismatch: expected 1, got 0")
        return cls(dim_in, dim_out)

    def total_dim(self) -> int:
        return self.dim_in * self.dim_out


class CausalOrder:
    ABeforeB = "ABeforeB"
    BBeforeA = "BBeforeA"


@dataclass(frozen=True)
class CausalMixture:
    a_before_b: float
    b_before_a: float

    @classmethod
    def new(cls, a_before_b: float, b_before_a: float) -> "CausalMixture":
        total = a_before_b + b_before_a
        if a_before_b < 0.0 or b_before_a < 0.0 or abs(total - 1.0) > 1e-9:
            raise ValueError(
                "causal mixture weights must be nonnegative and sum to one, "
                f"got {a_before_b}, {b_before_a}"
            )
        return cls(a_before_b, b_before_a)

    @classmethod
    def fixed(cls, order: str) -> "CausalMixture":
        if order == CausalOrder.ABeforeB:
            return cls(1.0, 0.0)
        return cls(0.0, 1.0)

    def is_fixed_order(self) -> bool:
        return self.a_before_b <= 1e-9 or self.b_before_a <= 1e-9

    @staticmethod
    def violates_causal_bound(score: float, causal_bound: float) -> bool:
        return score > causal_bound + 1e-9


@dataclass
class ReasoningDensityConfig:
    top_k: Optional[int] = None
    timestamps: Optional[List[float]] = None

    @classmethod
    def default(cls) -> "ReasoningDensityConfig":
        return cls()


@dataclass
class ReasoningDensityReport:
    construction: DensityConstruction
    source_count: int
    dim: int
    entropy: float
    purity: float
    l1_coherence: float
    top_k: Optional[int]


@dataclass
class DensityTrajectory:
    states: List[NumericalDensityMatrix]
    timestamps: List[float]
    reports: List[ReasoningDensityReport]


__all__ = [
    "CausalMixture",
    "CausalOrder",
    "DensityConstruction",
    "DensityConstructionReport",
    "DensityTrajectory",
    "LabIoDim",
    "ReasoningDensityConfig",
    "ReasoningDensityReport",
]
