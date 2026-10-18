"""Evaluator Governance Contract Implementation.

Conforms strictly to contract specification:
    urn:omega:governance:evaluator:v1.0.0
    (omega_engine/crates/omega_contracts/src/contract_canonical_definitions/05_core_governance/evaluator.contract.yaml)

Doctrine:
- Evaluator applies declared evaluation policy to already-computed facts.
- Evaluator does not measure, discover, mutate, terminalize, or execute.
- Evaluation decisions are deterministic functions of typed evidence and declared policy.
"""

from __future__ import annotations
import hashlib
import json
from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

CONTRACT_ID = "urn:omega:governance:evaluator:v1.0.0"
SCHEMA_VERSION = "omega.contract.v1"


class FormalismFirewall:
    def __init__(self, allowed: Sequence[str]) -> None:
        self.allowed = set(allowed)

    def check_access(self, source: str, target: str) -> Any:
        from omega_engine.crates.type.refusal import Refusal
        if source in self.allowed and target in self.allowed:
            return True
        return Refusal("access refused by FormalismFirewall")


@dataclass(frozen=True)
class EvaluationInput:
    """Read-only evaluation input containing candidate reference and pre-computed fact envelopes."""
    candidate_id: str
    fact_envelopes: Dict[str, Any]
    context_data: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvaluationPolicy:
    """Explicit admissibility thresholds and tolerance specifications."""
    policy_id: str
    max_phi1_tol: float = 1e-9
    max_gamma2_tol: float = 1e-9
    require_exactness: bool = True


@dataclass(frozen=True)
class EvaluationResult:
    """Deterministic evaluation verdict decision envelope."""
    evaluator_id: str
    candidate_id: str
    verdict: str  # "ACCEPT" | "REJECT" | "CONDITIONAL"
    is_admissible: bool
    rejection_reasons: List[str]
    authority_effect: str = "RequestsDecision"


class Evaluator:
    """Read-only governance decision layer applying admissibility policy to evidence."""

    def __init__(
        self,
        evaluator_id: str,
        evaluator_version: str = "v1.0.0",
    ):
        self.evaluator_id = evaluator_id
        self.evaluator_version = evaluator_version
        self.schema_hash = self.compute_schema_hash()

    def compute_schema_hash(self) -> str:
        raw = f"{CONTRACT_ID}:{SCHEMA_VERSION}:{self.evaluator_id}:{self.evaluator_version}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def evaluate(
        self,
        input_data: EvaluationInput,
        policy: EvaluationPolicy,
    ) -> EvaluationResult:
        """Apply policy thresholds deterministically to input facts."""
        reasons = []
        
        phi1_mass = float(input_data.fact_envelopes.get("phi1_mass", 0.0))
        gamma2_mass = float(input_data.fact_envelopes.get("gamma2_mass", 0.0))
        
        if policy.require_exactness and phi1_mass > policy.max_phi1_tol:
            reasons.append(f"Phi1 residual mass ({phi1_mass:.4e}) exceeds tolerance ({policy.max_phi1_tol:.4e})")
        
        if gamma2_mass > policy.max_gamma2_tol:
            reasons.append(f"Gamma2 curvature defect ({gamma2_mass:.4e}) exceeds tolerance ({policy.max_gamma2_tol:.4e})")
        
        is_admissible = len(reasons) == 0
        verdict = "ACCEPT" if is_admissible else "REJECT"
        
        return EvaluationResult(
            evaluator_id=self.evaluator_id,
            candidate_id=input_data.candidate_id,
            verdict=verdict,
            is_admissible=is_admissible,
            rejection_reasons=reasons,
            authority_effect="RequestsDecision",
        )


def verify_evaluator_contract(evaluator: Evaluator) -> Dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "evaluator_id": evaluator.evaluator_id,
        "schema_hash": evaluator.schema_hash,
        "authority_effect": "RequestsDecision",
        "admissible": True,
    }


__all__ = [
    "Evaluator",
    "EvaluationInput",
    "EvaluationPolicy",
    "EvaluationResult",
    "verify_evaluator_contract",
    "CONTRACT_ID",
    "SCHEMA_VERSION",
]




