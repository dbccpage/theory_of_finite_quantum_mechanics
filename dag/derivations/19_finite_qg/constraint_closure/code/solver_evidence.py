"""Solver evidence records for Paper 002 local test support.

Self-contained local module replacing legacy omega_engine.crates.type.solver_evidence.
Carries AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Generic, Optional, Protocol, Sequence, TypeVar

AUTHORITY_EFFECT_NONE = "None"
EVIDENCE_ONLY = "EvidenceOnly"

InputT = TypeVar("InputT", contravariant=True)
OutputT = TypeVar("OutputT", covariant=True)


class SolverError(Exception):
    NON_FINITE_INPUT = "NonFiniteInput"
    INFEASIBLE = "Infeasible"
    NUMERICAL_FAILURE = "NumericalFailure"

    def __init__(self, kind: str, message: str = "") -> None:
        self.kind = kind
        self.message = message
        super().__init__(f"{kind}: {message}" if message else kind)

    @classmethod
    def non_finite_input(cls) -> "SolverError":
        return cls(cls.NON_FINITE_INPUT)

    @classmethod
    def infeasible(cls) -> "SolverError":
        return cls(cls.INFEASIBLE)

    @classmethod
    def numerical_failure(cls, message: str) -> "SolverError":
        return cls(cls.NUMERICAL_FAILURE, message)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, SolverError)
            and self.kind == other.kind
            and self.message == other.message
        )

    def __hash__(self) -> int:
        return hash((self.kind, self.message))


class CertificateKind(Enum):
    UnsatCore = auto()
    DualWitness = auto()
    PrimalWitness = auto()
    Eigenpair = auto()
    FlowCut = auto()


@dataclass(frozen=True)
class Certificate:
    kind: CertificateKind
    payload: bytes = b""
    verification_status: str = field(default="Unverified", init=False)
    evidence_class: str = field(default=EVIDENCE_ONLY, init=False)
    authority_effect: str = field(default=AUTHORITY_EFFECT_NONE, init=False)

    def as_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind.name,
            "payload_len": len(self.payload),
            "verification_status": self.verification_status,
        }


@dataclass(frozen=True)
class SolverDiagnostics:
    converged: bool
    primal_residual: Optional[float] = None
    dual_residual: Optional[float] = None
    primal_dual_gap: Optional[float] = None
    iteration_count: Optional[int] = None
    tolerance: Optional[float] = None
    certificates: tuple[Certificate, ...] = ()
    evidence_class: str = field(default=EVIDENCE_ONLY, init=False)
    authority_effect: str = field(default=AUTHORITY_EFFECT_NONE, init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "certificates", tuple(self.certificates))


@dataclass(frozen=True)
class SolverResult(Generic[OutputT]):
    value: OutputT
    diagnostics: SolverDiagnostics
    evidence_class: str = field(default=EVIDENCE_ONLY, init=False)
    authority_effect: str = field(default=AUTHORITY_EFFECT_NONE, init=False)

    @classmethod
    def new_with_diagnostics(
        cls,
        value: OutputT,
        diagnostics: SolverDiagnostics,
    ) -> "SolverResult[OutputT]":
        return cls(value=value, diagnostics=diagnostics)

    @classmethod
    def new_certified(
        cls,
        value: OutputT,
        diagnostics: SolverDiagnostics,
    ) -> "SolverResult[OutputT]":
        return cls.new_with_diagnostics(value, diagnostics)

    @classmethod
    def new_untrusted(cls, value: OutputT) -> "SolverResult[OutputT]":
        return cls(value=value, diagnostics=SolverDiagnostics(converged=False))


class Solver(Protocol[InputT, OutputT]):
    def solve(self, problem: InputT) -> SolverResult[OutputT]:
        ...


__all__ = [
    "AUTHORITY_EFFECT_NONE",
    "Certificate",
    "CertificateKind",
    "EVIDENCE_ONLY",
    "Solver",
    "SolverDiagnostics",
    "SolverError",
    "SolverResult",
]
