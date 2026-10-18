"""Canonical Evaluator Base Contract & Implementation (evaluator_base.py).

Doctrine:
- Evaluator applies declared policy to already-computed facts.
- Evaluator DOES NOT measure, discover, mutate, terminalize, certify, or execute.
- Missing required facts MUST yield fail-closed Escalate / MissingRequiredEvidence (NEVER default to 0.0).
- EvaluationResult contains complete provenance and hash trail.
- AuthorityEffect: EvidenceOnly.
"""

from __future__ import annotations
import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Final, List, Optional, Tuple

CONTRACT_ID: Final[str] = "urn:omega:judgment:evaluator:v1.0.0"


class EvaluationVerdict(str, Enum):
    """Normative evaluation verdicts."""
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    ESCALATE = "Escalate"
    INCONCLUSIVE = "Inconclusive"


@dataclass(frozen=True, slots=True)
class ClauseResult:
    """Result of an individual EvaluationClause evaluation."""
    clause_name: str
    verdict: EvaluationVerdict
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class EvaluationClause(ABC):
    """Abstract clause evaluated by EvaluatorBase."""

    def __init__(self, clause_name: str, required_fact_keys: Tuple[str, ...] = ()) -> None:
        self.clause_name = clause_name
        self.required_fact_keys = required_fact_keys

    @abstractmethod
    def evaluate(
        self, facts: Dict[str, Any], policy_params: Dict[str, Any]
    ) -> ClauseResult:
        """Internal clause evaluation logic."""


@dataclass(frozen=True, slots=True)
class EvaluationPolicy:
    """Immutable declared evaluation policy."""

    policy_id: str
    clauses: Tuple[EvaluationClause, ...] = ()
    policy_params: Dict[str, Any] = field(default_factory=dict)
    policy_hash: str = field(default_factory=str)

    def __post_init__(self) -> None:
        if not self.policy_hash:
            raw = json.dumps(
                {
                    "policy_id": self.policy_id,
                    "clause_names": [c.clause_name for c in self.clauses],
                    "policy_params": self.policy_params,
                },
                sort_keys=True,
            ).encode("utf-8")
            object.__setattr__(
                self, "policy_hash", f"sha256:{hashlib.sha256(raw).hexdigest()}"
            )


@dataclass(frozen=True, slots=True)
class EvaluationInput:
    """Immutable input envelope containing facts and evidence references."""

    candidate_id: str
    facts: Dict[str, Any]
    evidence_refs: Tuple[str, ...] = ()
    policy_ref: str = "default_policy"

    def compute_hash(self) -> str:
        raw = json.dumps(
            {
                "candidate_id": self.candidate_id,
                "facts": self.facts,
                "evidence_refs": list(self.evidence_refs),
                "policy_ref": self.policy_ref,
            },
            sort_keys=True,
        ).encode("utf-8")
        return f"sha256:{hashlib.sha256(raw).hexdigest()}"


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    """Complete provenance record of an evaluation judgment."""

    verdict: EvaluationVerdict
    policy_id: str
    clauses_fired: Tuple[ClauseResult, ...]
    evidence_used: Tuple[str, ...]
    evaluator_id: str
    evaluator_version: str
    input_hash: str
    output_hash: str = ""
    policy_hash: str = ""
    rejection_reasons: Tuple[str, ...] = ()
    authority_effect: str = "EvidenceOnly"

    def compute_hash(self) -> str:
        raw = json.dumps(
            {
                "verdict": self.verdict.value,
                "policy_id": self.policy_id,
                "evaluator_id": self.evaluator_id,
                "evaluator_version": self.evaluator_version,
                "input_hash": self.input_hash,
                "policy_hash": self.policy_hash,
                "rejection_reasons": list(self.rejection_reasons),
                "authority_effect": self.authority_effect,
            },
            sort_keys=True,
        ).encode("utf-8")
        return f"sha256:{hashlib.sha256(raw).hexdigest()}"


class EvaluatorBase:
    """Canonical fail-closed Evaluator applying declared policy to facts."""

    contract_id: Final[str] = CONTRACT_ID
    authority_effect: Final[str] = "EvidenceOnly"

    def __init__(
        self,
        evaluator_id: str = "evaluator_001",
        evaluator_version: str = "v1.0.0",
    ) -> None:
        self.evaluator_id = evaluator_id
        self.evaluator_version = evaluator_version

    def evaluate(
        self, input_data: EvaluationInput, policy: EvaluationPolicy
    ) -> EvaluationResult:
        """Fail-closed evaluation envelope."""
        input_hash = input_data.compute_hash()

        for clause in policy.clauses:
            missing = [k for k in clause.required_fact_keys if k not in input_data.facts]
            if missing:
                escalate_clause = ClauseResult(
                    clause_name=clause.clause_name,
                    verdict=EvaluationVerdict.ESCALATE,
                    message=f"Missing required fact keys: {missing}",
                )
                res = EvaluationResult(
                    verdict=EvaluationVerdict.ESCALATE,
                    policy_id=policy.policy_id,
                    clauses_fired=(escalate_clause,),
                    evidence_used=input_data.evidence_refs,
                    evaluator_id=self.evaluator_id,
                    evaluator_version=self.evaluator_version,
                    input_hash=input_hash,
                    policy_hash=policy.policy_hash,
                    rejection_reasons=(f"MissingRequiredEvidence: {missing}",),
                )
                return EvaluationResult(
                    verdict=res.verdict,
                    policy_id=res.policy_id,
                    clauses_fired=res.clauses_fired,
                    evidence_used=res.evidence_used,
                    evaluator_id=res.evaluator_id,
                    evaluator_version=res.evaluator_version,
                    input_hash=res.input_hash,
                    output_hash=res.compute_hash(),
                    policy_hash=res.policy_hash,
                    rejection_reasons=res.rejection_reasons,
                )

        results: List[ClauseResult] = []
        rejections: List[str] = []
        final_verdict = EvaluationVerdict.ACCEPTED

        for clause in policy.clauses:
            clause_res = clause.evaluate(input_data.facts, policy.policy_params)
            results.append(clause_res)
            if clause_res.verdict == EvaluationVerdict.REJECTED:
                final_verdict = EvaluationVerdict.REJECTED
                rejections.append(f"{clause.clause_name}: {clause_res.message}")
            elif clause_res.verdict == EvaluationVerdict.ESCALATE and final_verdict != EvaluationVerdict.REJECTED:
                final_verdict = EvaluationVerdict.ESCALATE

        unhashed = EvaluationResult(
            verdict=final_verdict,
            policy_id=policy.policy_id,
            clauses_fired=tuple(results),
            evidence_used=input_data.evidence_refs,
            evaluator_id=self.evaluator_id,
            evaluator_version=self.evaluator_version,
            input_hash=input_hash,
            policy_hash=policy.policy_hash,
            rejection_reasons=tuple(rejections),
        )

        return EvaluationResult(
            verdict=unhashed.verdict,
            policy_id=unhashed.policy_id,
            clauses_fired=unhashed.clauses_fired,
            evidence_used=unhashed.evidence_used,
            evaluator_id=unhashed.evaluator_id,
            evaluator_version=unhashed.evaluator_version,
            input_hash=unhashed.input_hash,
            output_hash=unhashed.compute_hash(),
            policy_hash=unhashed.policy_hash,
            rejection_reasons=unhashed.rejection_reasons,
        )


__all__ = [
    "EvaluatorBase",
    "EvaluationClause",
    "EvaluationVerdict",
    "ClauseResult",
    "EvaluationPolicy",
    "EvaluationInput",
    "EvaluationResult",
    "CONTRACT_ID",
]
