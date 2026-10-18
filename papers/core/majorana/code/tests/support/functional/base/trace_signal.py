"""TraceSignal Contract Primitive (ephemeral occurrence description).

Doctrine:
- No domain component owns a trace.
- Components produce structured TraceSignals describing what they just did.
- A TraceSignal is an ephemeral, non-canonical local occurrence description.
- A TraceSignal MUST NEVER trigger execution or affect control flow.
- A TraceSignal does NOT contain trace_id, sequence, parent_trace_refs, or artifact_hash.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Final, Tuple, Union

CONTRACT_ID: Final[str] = "urn:omega:evidence:trace_signal:v1.0.0"


class TraceSignalKind(str, Enum):
    """Normative kinds of trace signals produced by domain components."""
    OPERATOR_EXECUTED = "operator_executed"
    ENGINE_COMMITTED = "engine_committed"
    META_SELECTED_OPERATOR = "meta_selected_operator"
    META_PROPOSED_LIFT = "meta_proposed_lift"
    META_REFUSED_CONTINUATION = "meta_refused_continuation"
    FUNCTIONAL_MEASURED = "functional_measured"
    CERTIFIER_VERIFIED = "certifier_verified"
    EVALUATOR_JUDGED = "evaluator_judged"
    POLICY_EVALUATED = "policy_evaluated"
    LICENSE_MINTED = "license_minted"
    CONSTRUCTION_ADMITTED = "construction_admitted"


@dataclass(frozen=True, slots=True)
class TraceSignal:
    """Ephemeral, non-canonical local occurrence signal produced by a domain component."""

    source_ref: str
    source_contract_ref: str
    event_kind: Union[TraceSignalKind, str]
    input_boundary_refs: Tuple[str, ...] = ()
    output_boundary_refs: Tuple[str, ...] = ()
    correlation_ref: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    authority_effect: Union[str, Any] = "None"


__all__ = [
    "TraceSignal",
    "TraceSignalKind",
    "CONTRACT_ID",
]
