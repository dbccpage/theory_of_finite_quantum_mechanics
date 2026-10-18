"""Engine and DomainWorker I/O envelopes (type layer).

Moved out of engine/engine.py so value types live under type/.
AuthorityEffect defaults are documentary; callers must not mint higher authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


@dataclass(frozen=True)
class EngineInput:
    """Legacy/playpen input envelope historically used near Engine smoke paths.

    Engine v1 contract input is LicensedTransitionInput. This type remains for
    compatibility envelopes and must not be used to smuggle residual computation
    into Engine v1.
    """

    task_id: str
    carrier_ref: str
    cochain_vector: List[float]
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EngineOutput:
    """Raw engine-adjacent envelope. Default authority is EvidenceOnly, not StateTransition."""

    task_id: str
    status: str
    residual_vector: List[float]
    phi1_mass: float
    output_hash: str
    authority_effect: str = "EvidenceOnly"


@dataclass(frozen=True)
class CheckedEngineOutput:
    output: EngineOutput
    verification_hash: str
    authority_effect: str = "FactOnly"


@dataclass(frozen=True)
class RefusedEngineOutput:
    output: EngineOutput
    refusal_reason: str
    authority_effect: str = "Refused"


@dataclass(frozen=True)
class LicensedTransitionInput:
    """Engine v1 structural input (license required)."""

    license_ref: str
    decision_ref: str
    target_state_ref: str
    precondition_refs: Sequence[str] = ()
    trace_parent_refs: Sequence[str] = ()


@dataclass(frozen=True)
class EngineAction:
    """Engine v1 output: licensed state transition record only."""

    action_id: str
    license_ref: str
    pre_state_hash: str
    post_state_hash: str
    emitted_trace_ref: str
    action_hash: str
    authority_effect: str = "StateTransition"


@dataclass(frozen=True)
class DomainWorkerInput:
    task_id: str
    task_kind: str
    payload: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DomainWorkerOutput:
    task_id: str
    task_kind: str
    status: str
    result: Dict[str, Any]
    residual_vector: List[float]
    residual_l1: float
    math_path: List[str]
    output_hash: str
    authority_effect: str = "EvidenceOnly"
    implements: Sequence[str] = (
        "urn:omega:execution:domain_worker:v1.0.0",
    )


__all__ = [
    "EngineInput",
    "EngineOutput",
    "CheckedEngineOutput",
    "RefusedEngineOutput",
    "LicensedTransitionInput",
    "EngineAction",
    "DomainWorkerInput",
    "DomainWorkerOutput",
]
