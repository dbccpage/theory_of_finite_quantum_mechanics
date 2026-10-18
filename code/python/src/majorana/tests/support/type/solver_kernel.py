"""Narrow frozen SolverKernel v1.2 substrate and structural protocol.

These types carry no authority. Solver results, diagnostics, and proof-shaped
artifacts remain unverified EvidenceOnly material until a separate boundary
checks them. This module intentionally mirrors the adopted Python substrate;
it is not the complete managed packet and hashing implementation described by
the machine contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Generic, Mapping, Optional, Protocol, Tuple, TypeVar, runtime_checkable


ProblemT = TypeVar("ProblemT", contravariant=True)
PayloadT = TypeVar("PayloadT", covariant=True)

SOLVER_KERNEL_CONTRACT_REF = "urn:omega:execution:solver_kernel:v1.2.0"
EVIDENCE_ONLY = "EvidenceOnly"
AUTHORITY_EFFECT_NONE = "None"
UNVERIFIED = "Unverified"
NORMAL_COMPLETION_STATES = frozenset(
    {
        "completed_with_output",
        "budget_exhausted_with_candidate",
        "tolerance_exit_with_candidate",
    }
)


@dataclass(frozen=True)
class SolverDescriptor:
    solver_id: str
    version: str
    implementation_hash: str
    algorithm_ref: str
    contract_ref: str = SOLVER_KERNEL_CONTRACT_REF
    authority_effect: str = field(default=AUTHORITY_EFFECT_NONE, init=False)


@runtime_checkable
class SolverKernel(Protocol[ProblemT, PayloadT]):
    """Operation-scoped structural protocol; inheritance is not conformance."""

    def solve(self, problem: ProblemT) -> "SolverResult[PayloadT]":
        ...


@dataclass(frozen=True)
class ProofArtifactCandidate:
    """Proof-shaped output that is explicitly not a verified certificate."""

    artifact_kind: str
    claim_predicate_ref: str
    payload_hash: str
    generation_algorithm_ref: str
    verification_status: str = field(default=UNVERIFIED, init=False)
    evidence_class: str = field(default=EVIDENCE_ONLY, init=False)
    authority_effect: str = field(default=AUTHORITY_EFFECT_NONE, init=False)

    def __post_init__(self) -> None:
        for name in (
            "artifact_kind",
            "claim_predicate_ref",
            "payload_hash",
            "generation_algorithm_ref",
        ):
            if not getattr(self, name):
                raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True)
class SolverResult(Generic[PayloadT]):
    payload: PayloadT
    residual: Optional[Any] = None
    diagnostics: Optional[Mapping[str, Any]] = None
    proof_artifact_candidates: Tuple[ProofArtifactCandidate, ...] = ()
    evidence_class: str = field(default=EVIDENCE_ONLY, init=False)
    authority_effect: str = field(default=AUTHORITY_EFFECT_NONE, init=False)

    def __post_init__(self) -> None:
        if self.diagnostics is not None:
            object.__setattr__(
                self,
                "diagnostics",
                MappingProxyType(dict(self.diagnostics)),
            )
        candidates = tuple(self.proof_artifact_candidates)
        if not all(isinstance(item, ProofArtifactCandidate) for item in candidates):
            raise TypeError(
                "proof_artifact_candidates must contain ProofArtifactCandidate records"
            )
        object.__setattr__(self, "proof_artifact_candidates", candidates)


@dataclass(frozen=True)
class ManagedSolverRequest(Generic[ProblemT]):
    invocation_id: str
    descriptor: SolverDescriptor
    problem: ProblemT
    problem_hash: str
    configuration_hash: str
    request_hash: str
    arithmetic_profile: str


@dataclass(frozen=True)
class ManagedSolverOutput(Generic[PayloadT]):
    invocation_id: str
    request_hash: str
    completion_state: str
    output: SolverResult[PayloadT]
    evidence_class: str = field(default=EVIDENCE_ONLY, init=False)
    authority_effect: str = field(default=AUTHORITY_EFFECT_NONE, init=False)

    def __post_init__(self) -> None:
        if self.completion_state not in NORMAL_COMPLETION_STATES:
            raise ValueError(
                "ManagedSolverOutput requires a normal lifecycle completion state"
            )


__all__ = [
    "AUTHORITY_EFFECT_NONE",
    "EVIDENCE_ONLY",
    "ManagedSolverOutput",
    "ManagedSolverRequest",
    "NORMAL_COMPLETION_STATES",
    "PayloadT",
    "ProblemT",
    "ProofArtifactCandidate",
    "SOLVER_KERNEL_CONTRACT_REF",
    "SolverDescriptor",
    "SolverKernel",
    "SolverResult",
    "UNVERIFIED",
]
