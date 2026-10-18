"""Obstruction Runtime Type primitives.

Re-exports runtime types for obstruction evaluation.
AuthorityEffect: None.
"""

from __future__ import annotations
from omega_engine.crates.engine.eng_obstruction import (
    Candidate,
    CandidateGenerator,
    CandidateSelector,
    BestScoreSelector,
    EvaluatedCandidate,
    ObstructionMetrics,
    ObstructionThresholds,
    ObstructionVerdict,
    ScoreWeights,
    StepOutcome,
    select_best_accepted,
    OperatorId,
    Provenance,
)

__all__ = [
    "Candidate",
    "CandidateGenerator",
    "CandidateSelector",
    "BestScoreSelector",
    "EvaluatedCandidate",
    "ObstructionMetrics",
    "ObstructionThresholds",
    "ObstructionVerdict",
    "ScoreWeights",
    "StepOutcome",
    "select_best_accepted",
    "OperatorId",
    "Provenance",
]
