"""Base Evaluator crate exposing EvaluatorBase, EvaluationPolicy, and EvaluationClause primitives."""

from omega_engine.crates.evaluator.base.evaluator_base import (
    EvaluatorBase,
    EvaluationClause,
    EvaluationVerdict,
    ClauseResult,
    EvaluationPolicy,
    EvaluationInput,
    EvaluationResult,
)

__all__ = [
    "EvaluatorBase",
    "EvaluationClause",
    "EvaluationVerdict",
    "ClauseResult",
    "EvaluationPolicy",
    "EvaluationInput",
    "EvaluationResult",
]
