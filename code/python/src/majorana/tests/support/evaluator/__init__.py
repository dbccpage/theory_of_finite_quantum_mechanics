"""Evaluator Package conforming to urn:omega:governance:evaluator:v1.0.0."""

from .evaluator import (
    Evaluator,
    EvaluationInput,
    EvaluationPolicy,
    EvaluationResult,
    FormalismFirewall,
    verify_evaluator_contract,
    CONTRACT_ID,
    SCHEMA_VERSION,
)
from .eval_proposal import (
    EvaluatorConfig,
    KillReason,
    ProposalEvaluationResult,
    ProposalEvaluator,
)
from .dual_acceptance import accept as accept

__all__ = [
    "Evaluator",
    "EvaluationInput",
    "EvaluationPolicy",
    "EvaluationResult",
    "EvaluatorConfig",
    "FormalismFirewall",
    "KillReason",
    "ProposalEvaluationResult",
    "ProposalEvaluator",
    "verify_evaluator_contract",
    "CONTRACT_ID",
    "SCHEMA_VERSION",
    "accept",
]
