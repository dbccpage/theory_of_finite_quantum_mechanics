"""Value types for obstruction branch search."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from omega_engine_governance.contracts import AuthorityEffect
from omega_engine.crates.type.qm_density import BranchResidualSearchReport


@dataclass(frozen=True)
class ObstructionSearchPoint:
    phi1: float
    gamma2: float
    xi: Optional[float] = None


@dataclass
class ObstructionBranchCandidate:
    label: str
    after: ObstructionSearchPoint
    provenance: str


@dataclass(frozen=True)
class ObstructionBranchSearchConfig:
    phi_tol: float = 1e-12
    gamma_tol: float = 1e-12
    xi_tol: float = 1e-12

    @classmethod
    def default(cls) -> "ObstructionBranchSearchConfig":
        return cls()


class ObstructionImprovementTier(Enum):
    Phi1 = "Phi1"
    Gamma2 = "Gamma2"
    Xi = "Xi"
    None_ = "None"


class ObstructionBranchVerdict(Enum):
    StrictDescent = "StrictDescent"
    RejectedNoDescent = "RejectedNoDescent"


@dataclass
class ObstructionBranchCandidateReport:
    label: str
    provenance: str
    after: ObstructionSearchPoint
    verdict: ObstructionBranchVerdict
    improvement_tier: ObstructionImprovementTier
    proposal_mass: float
    proposal_probability: float
    rank: int
    authority_effect: AuthorityEffect


@dataclass
class ObstructionBranchSearchReport:
    before: ObstructionSearchPoint
    candidates: List[ObstructionBranchCandidateReport]
    branch_density: Optional[BranchResidualSearchReport]
    best_descent_candidate: Optional[int]
    authority_effect: AuthorityEffect


__all__ = [
    "ObstructionBranchCandidate",
    "ObstructionBranchCandidateReport",
    "ObstructionBranchSearchConfig",
    "ObstructionBranchSearchReport",
    "ObstructionBranchVerdict",
    "ObstructionImprovementTier",
    "ObstructionSearchPoint",
]
