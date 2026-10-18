"""Contracted obstruction runtime engine.

Candidate generation, scoring, evaluation, and reduction remain in their
component crates. This module advances runtime state only.
"""

from __future__ import annotations

from typing import Any, Final, Optional

from omega_engine.crates.evaluator.eval_obstruction import validate_score_weights
from omega_engine.crates.functional.fn_obstruction import obstruction_score
from omega_engine.crates.operator.lambda_op.lamb_obstruction_candidates import BestScoreSelector, CandidateSelector
from omega_engine.crates.type.obstruction_runtime import EvaluatedCandidate, ScoreWeights, StepOutcome

CONTRACT_ID: Final[str] = "urn:omega:engine:obstruction_runtime_engine:file:v1.0.0"


from omega_engine.crates.engine.base.eng_base import Engine


class ObstructionRuntime(Engine):
    authority_effect: Final[str] = "None"
    implements: Final[tuple[str, ...]] = (CONTRACT_ID,)

    def __init__(self, seed_state: Any, functional: Any, evaluator: Any, generator: Any, weights: Optional[ScoreWeights] = None, selector: Optional[CandidateSelector] = None):
        self.weights = weights or ScoreWeights.default()
        validate_score_weights(self.weights)
        self.seed = seed_state
        self.functional = functional
        self.evaluator = evaluator
        self.generator = generator
        self.selector = selector or BestScoreSelector()
        self.current_state = seed_state
        self.step_index = 0
        self.trace: list[StepOutcome] = []

    @classmethod
    def try_new(cls, *args: Any, **kwargs: Any) -> "ObstructionRuntime":
        return cls(*args, **kwargs)

    def step(self) -> StepOutcome:
        evaluated = []
        for index, candidate in enumerate(self.generator.generate(self.current_state)):
            if hasattr(self.functional, "compute"):
                metrics = self.functional.compute(candidate.state)
            elif hasattr(self.functional, "evaluate"):
                metrics = self.functional.evaluate(candidate.state)
            else:
                metrics = getattr(candidate.state, "metrics", None)
            parent_metrics = getattr(self.current_state, "metrics", self.current_state)
            verdict = self.evaluator.decide(parent_metrics, metrics)
            evaluated.append(EvaluatedCandidate(index, candidate, metrics, verdict, obstruction_score(metrics, self.weights)))
        selected = self.selector.select(evaluated)
        if selected is not None:
            self.current_state = selected.candidate.state
        outcome = StepOutcome(self.step_index, evaluated, selected)
        self.trace.append(outcome)
        self.step_index += 1
        return outcome


__all__ = ["CONTRACT_ID", "ObstructionRuntime"]
