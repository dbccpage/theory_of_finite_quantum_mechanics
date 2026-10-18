"""Value types for the provisional CODA engine contract."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SimplicialCarrier:
    vertices: List[Any]
    edges: List[Tuple[Any, Any]]
    faces: List[Tuple[Any, Any, Any]] = field(default_factory=list)

    def validate(self) -> bool:
        if len(self.vertices) != len(set(self.vertices)):
            return False
        vertex_set = set(self.vertices)
        seen_edges = set()
        for left, right in self.edges:
            if left not in vertex_set or right not in vertex_set or left == right or (left, right) in seen_edges:
                return False
            seen_edges.add((left, right))
        edge_set = set(self.edges)
        for face in self.faces:
            if len(face) != 3 or len(set(face)) != 3 or any(vertex not in vertex_set for vertex in face):
                return False
            left, middle, right = face
            for edge in ((left, middle), (middle, right), (left, right)):
                if edge not in edge_set and tuple(reversed(edge)) not in edge_set:
                    return False
        return True


@dataclass
class ObserverPacket:
    observer_id: str
    gauge_name: str
    resolution: float = 1e-6
    authority_effect: str = "None"

    def probe_vertex_state(self, vertex_data: Dict[Any, float]) -> Dict[Any, float]:
        return {vertex: float(value) for vertex, value in vertex_data.items()}


@dataclass
class ObstructionSignature:
    phi_1: float
    gamma_2: float
    r_cl: float
    status_label: str
    residual_vector: List[float] = field(default_factory=list)
    input_cochain: List[float] = field(default_factory=list)


@dataclass
class StepRecord:
    step_index: int
    letter: str
    receipt_hash: str
    residual_digest: str
    prev_hash: str
    authority_effect: str = "None"

    def compute_step_hash(self) -> str:
        payload = f"{self.step_index}:{self.letter}:{self.receipt_hash}:{self.residual_digest}:{self.prev_hash}:{self.authority_effect}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass
class CandidatePacket:
    artifact_id: str
    locus_id: str
    problem_family: str
    primitive_difference_proposal: str
    carrier_proposal: str
    zero_rel_proposal: str
    observer_proposal: str
    witness_available: bool = True
    quotient_or_refusal: str = "E"
    adapter_confidence: str = "high"
    authority_effect: str = "None"
    status: str = "proposed_only"


@dataclass
class IntakeTrace:
    raw_artifact_hash: str
    candidate_locus: str
    candidate_packet: CandidatePacket
    intake_adapter_status: str = "ADMITTED"
    enters_dda_trace: bool = False


@dataclass
class LocalDeclarationOrder:
    step0_grounding_hash: str
    step1_carrier: SimplicialCarrier
    step2_observer: ObserverPacket
    step3_primitive_difference: Dict[Tuple[Any, Any], float]
    step4_zero_rel_rule: str
    step5_witness_certificate: Optional[str]
    step6_quotient_policy: str = "Q1_SEPARATED"

    def validate_declaration_order(self) -> Tuple[bool, str]:
        if not self.step0_grounding_hash:
            return False, "REFUSE_MISSING_GROUNDING"
        if not self.step1_carrier or not self.step1_carrier.validate():
            return False, "REFUSE_MISSING_CARRIER"
        if not self.step2_observer or not self.step2_observer.observer_id:
            return False, "REFUSE_MISSING_OBSERVER"
        if self.step3_primitive_difference is None:
            return False, "REFUSE_MISSING_PRIMITIVE_DIFFERENCE"
        if not self.step4_zero_rel_rule:
            return False, "REFUSE_MISSING_ZERO_REL"
        if not self.step5_witness_certificate:
            return False, "REFUSE_MISSING_WITNESS"
        return True, "ACCEPT_DECLARATION"


__all__ = ["CandidatePacket", "IntakeTrace", "LocalDeclarationOrder", "ObserverPacket", "ObstructionSignature", "SimplicialCarrier", "StepRecord"]
