"""Density, channel, residual, and diagnostic value types for QM components."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple

from omega_engine_governance.contracts import AuthorityEffect
from omega_engine.crates.linear_algebra_theory.density import NumericalDensityMatrix


@dataclass(frozen=True)
class StateSpace:
    dim: int


@dataclass
class H1Sector:
    index: int
    edge_indices: List[int]
    weight: float
    probability: float


@dataclass
class SectorMassCertificate:
    phi1: float
    sector_weight_sum: float
    mass_error: float
    prob_error: float


@dataclass
class H1SectorDecomposition:
    sectors: List[H1Sector]
    certificate: SectorMassCertificate


class PhaseWitnessKind(Enum):
    OrientedCycleTransport = "OrientedCycleTransport"
    PathGroupoidRepresentation = "PathGroupoidRepresentation"
    UnitaryRepresentation = "UnitaryRepresentation"


@dataclass
class PhaseWitness:
    kind: PhaseWitnessKind
    phases: List[float]


@dataclass
class H1Density:
    density: NumericalDensityMatrix
    sectors: H1SectorDecomposition
    phase_witness: Optional[PhaseWitness] = None


class ResidualDensityConstruction(Enum):
    EdgeDiagonal = "EdgeDiagonal"
    IncidenceDiagonal = "IncidenceDiagonal"
    CoarseGrainedDiagonal = "CoarseGrainedDiagonal"
    BranchProposalDiagonal = "BranchProposalDiagonal"
    ChannelPushforwardDiagonal = "ChannelPushforwardDiagonal"


@dataclass
class ResidualDensityDiagnostics:
    construction: ResidualDensityConstruction
    source_count: int
    dim: int
    sector_weights: List[float]
    sector_probabilities: List[float]
    raw_l1_mass: float
    mass_error: float
    prob_error: float
    trace: float
    entropy: float
    purity: float
    l1_coherence: float
    dominant_sector: Optional[int]
    residual_concentration: float
    authority_effect: AuthorityEffect


@dataclass
class ResidualDensityReport:
    density: H1Density
    diagnostics: ResidualDensityDiagnostics


@dataclass
class BranchResidualCandidate:
    label: str
    proposal_mass: float


@dataclass
class BranchResidualCandidateDiagnostic:
    label: str
    proposal_mass: float
    proposal_probability: float
    rank: int


@dataclass
class BranchResidualSearchReport:
    density: H1Density
    candidates: List[BranchResidualCandidateDiagnostic]
    total_mass: float
    trace: float
    entropy: float
    purity: float
    dominant_branch: Optional[int]
    authority_effect: AuthorityEffect


@dataclass
class GomcDiagnosticConfig:
    observer_labels: Optional[List[int]] = None
    channel_transition: Optional[List[List[float]]] = None
    branch_candidates: List[BranchResidualCandidate] = field(default_factory=list)
    local_green_purity_threshold: float = 1.0 - 1e-9
    global_red_phi1_threshold: float = 1e-12

    @classmethod
    def default(cls) -> "GomcDiagnosticConfig":
        return cls()


@dataclass
class GomcDiagnosticReport:
    global_report: ResidualDensityReport
    observer: Optional[ResidualDensityReport]
    channel: Optional[ResidualDensityReport]
    branch_search: Optional[BranchResidualSearchReport]
    lggr: Optional[LocalGreenGlobalRedDiagnostic]
    authority_effect: AuthorityEffect


@dataclass
class LocalGreenGlobalRedDiagnostic:
    local_green: bool
    global_red: bool
    detected: bool
    local_purity: float
    global_raw_l1_mass: float
    observer_dim: int
    global_dim: int
    authority_effect: AuthorityEffect


@dataclass
class DensityDiagnostics:
    dim: int
    total_trace: float
    purity: float
    entropy_bits: float
    l1_coherence: float
    diagonal_probs: List[Tuple[str, float]] = field(default_factory=list)
    eigenvalues: List[float] = field(default_factory=list)


__all__ = [
    "BranchResidualCandidate",
    "BranchResidualCandidateDiagnostic",
    "BranchResidualSearchReport",
    "DensityDiagnostics",
    "GomcDiagnosticConfig",
    "GomcDiagnosticReport",
    "H1Density",
    "H1Sector",
    "H1SectorDecomposition",
    "LocalGreenGlobalRedDiagnostic",
    "PhaseWitness",
    "PhaseWitnessKind",
    "ResidualDensityConstruction",
    "ResidualDensityDiagnostics",
    "ResidualDensityReport",
    "SectorMassCertificate",
    "StateSpace",
]
