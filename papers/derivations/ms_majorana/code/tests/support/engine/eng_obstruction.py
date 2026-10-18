"""Obstruction evaluation engine components; no iteration runtime ownership."""

import math
from typing import Any, Optional




class ObstructionMetrics:
    def __init__(self, phi_1: float, gamma_2: float, xi: float):
        self.phi_1 = float(phi_1)
        self.gamma_2 = float(gamma_2)
        self.gamma2_delta: Optional[float] = None
        self.noether_drift: Optional[float] = None
        self.xi = float(xi)

    @classmethod
    def new(cls, phi_1: float, gamma_2: float, xi: float):
        return cls(phi_1, gamma_2, xi)

    def with_gamma2_delta(self, gamma2_delta: float):
        self.gamma2_delta = float(gamma2_delta)
        return self

    def with_noether_drift(self, noether_drift: float):
        self.noether_drift = float(noether_drift)
        return self

    def is_finite(self) -> bool:
        vals = [self.phi_1, self.gamma_2, self.xi]
        if self.gamma2_delta is not None:
            vals.append(self.gamma2_delta)
        if self.noether_drift is not None:
            vals.append(self.noether_drift)
        return all(math.isfinite(x) for x in vals)

    def is_valid_range(self) -> bool:
        return self.phi_1 >= 0.0 and self.gamma_2 >= 0.0 and 0.0 <= self.xi <= 1.0

    def is_valid(self) -> bool:
        return self.is_finite() and self.is_valid_range()


class ObstructionVerdict:
    Accept = "Accept"
    Reject = "Reject"
    Oscillatory = "Oscillatory"
    Incoherent = "Incoherent"
    Invalid = "Invalid"

    @staticmethod
    def is_accepted(verdict: str) -> bool:
        return verdict == ObstructionVerdict.Accept


class ObstructionThresholds:
    def __init__(
        self,
        phi_tol: float = 1e-9,
        gamma2_threshold: float = 1.0,
        gamma2_delta_threshold: float = 1.0,
        noether_drift_threshold: float = 1e-6,
        xi_threshold: float = 0.25,
    ):
        self.phi_tol = phi_tol
        self.gamma2_threshold = gamma2_threshold
        self.gamma2_delta_threshold = gamma2_delta_threshold
        self.noether_drift_threshold = noether_drift_threshold
        self.xi_threshold = xi_threshold

    @classmethod
    def default(cls):
        return cls()

    def validate(self):
        if not math.isfinite(self.phi_tol) or self.phi_tol < 0.0:
            raise ValueError("phi_tol must be finite and nonnegative")
        if not math.isfinite(self.gamma2_threshold) or self.gamma2_threshold < 0.0:
            raise ValueError("gamma2_threshold must be finite and nonnegative")
        if (
            not math.isfinite(self.gamma2_delta_threshold)
            or self.gamma2_delta_threshold < 0.0
        ):
            raise ValueError("gamma2_delta_threshold must be finite and nonnegative")
        if (
            not math.isfinite(self.noether_drift_threshold)
            or self.noether_drift_threshold < 0.0
        ):
            raise ValueError("noether_drift_threshold must be finite and nonnegative")
        if (
            not math.isfinite(self.xi_threshold)
            or self.xi_threshold < 0.0
            or self.xi_threshold > 1.0
        ):
            raise ValueError("xi_threshold must be in [0,1]")


class ScoreWeights:
    def __init__(self, lambda_gamma: float = 0.5, lambda_xi: float = 0.25):
        self.lambda_gamma = lambda_gamma
        self.lambda_xi = lambda_xi

    @classmethod
    def default(cls):
        return cls()

    def validate(self):
        if not math.isfinite(self.lambda_gamma) or self.lambda_gamma < 0.0:
            raise ValueError("lambda_gamma must be finite and nonnegative")
        if not math.isfinite(self.lambda_xi) or self.lambda_xi < 0.0:
            raise ValueError("lambda_xi must be finite and nonnegative")


def obstruction_score(metrics: ObstructionMetrics, weights: ScoreWeights) -> float:
    if metrics is None or not metrics.is_valid():
        return float("-inf")
    return (
        -metrics.phi_1
        - weights.lambda_gamma * metrics.gamma_2
        + weights.lambda_xi * metrics.xi
    )




class ObstructionFunctional:
    def compute(self, state) -> ObstructionMetrics:
        raise NotImplementedError


class ObstructionEvaluator:
    def decide(self, parent: ObstructionMetrics, child: ObstructionMetrics) -> str:
        raise NotImplementedError


class DefaultObstructionEvaluator(ObstructionEvaluator):
    def __init__(self, thresholds: Optional[ObstructionThresholds] = None):
        self.thresholds = thresholds or ObstructionThresholds.default()
        self.thresholds.validate()

    @classmethod
    def try_new(cls, thresholds: ObstructionThresholds):
        return cls(thresholds)

    @classmethod
    def new_unchecked(cls, thresholds: ObstructionThresholds):
        self = cls.__new__(cls)
        self.thresholds = thresholds
        return self

    def decide(self, parent: ObstructionMetrics, child: ObstructionMetrics) -> str:
        if not parent.is_finite() or not child.is_finite():
            return ObstructionVerdict.Invalid

        if not parent.is_valid_range() or not child.is_valid_range():
            return ObstructionVerdict.Invalid

        if (
            child.noether_drift is not None
            and abs(child.noether_drift) > self.thresholds.noether_drift_threshold
        ):
            return ObstructionVerdict.Invalid

        if child.xi < self.thresholds.xi_threshold:
            return ObstructionVerdict.Incoherent

        if child.gamma_2 > self.thresholds.gamma2_threshold:
            return ObstructionVerdict.Oscillatory

        if (
            child.gamma2_delta is not None
            and abs(child.gamma2_delta) > self.thresholds.gamma2_delta_threshold
        ):
            return ObstructionVerdict.Oscillatory

        if child.phi_1 <= parent.phi_1 + self.thresholds.phi_tol:
            return ObstructionVerdict.Accept
        else:
            return ObstructionVerdict.Reject


class OperatorId:
    def __init__(self, val: str):
        self.val = str(val)

    def __str__(self):
        return self.val

    def __repr__(self):
        return f"OperatorId('{self.val}')"

    def __eq__(self, other):
        if isinstance(other, OperatorId):
            return self.val == other.val
        return self.val == str(other)

    def __hash__(self):
        return hash(self.val)


class Provenance:
    def __init__(self, val: str):
        self.val = str(val)

    def __str__(self):
        return self.val

    def __repr__(self):
        return f"Provenance('{self.val}')"

    def __eq__(self, other):
        if isinstance(other, Provenance):
            return self.val == other.val
        return self.val == str(other)


class Candidate:
    def __init__(self, state, operator_id, provenance):
        self.state = state
        self.operator_id = (
            OperatorId(operator_id)
            if not isinstance(operator_id, OperatorId)
            else operator_id
        )
        self.provenance = (
            Provenance(provenance)
            if not isinstance(provenance, Provenance)
            else provenance
        )

    @classmethod
    def new(cls, state, operator_id, provenance):
        return cls(state, operator_id, provenance)


class CandidateGenerator:
    def generate(self, state) -> list:
        raise NotImplementedError


class EvaluatedCandidate:
    def __init__(
        self,
        candidate_index: int,
        candidate: Candidate,
        metrics: ObstructionMetrics,
        verdict: str,
        score: float,
    ):
        self.candidate_index = candidate_index
        self.candidate = candidate
        self.metrics = metrics
        self.verdict = verdict
        self.score = score


class CandidateSelector:
    def select(self, evaluated: list) -> Optional[EvaluatedCandidate]:
        raise NotImplementedError


class BestScoreSelector(CandidateSelector):
    def select(self, evaluated: list) -> Optional[EvaluatedCandidate]:
        return select_best_accepted(evaluated)


def select_best_accepted(evaluated: list) -> Optional[EvaluatedCandidate]:
    best = None
    for candidate in evaluated:
        if ObstructionVerdict.is_accepted(candidate.verdict) and math.isfinite(
            candidate.score
        ):
            if best is None or candidate.score > best.score:
                best = candidate
    return best


class StepOutcome:
    def __init__(self, step_index: int, evaluated: list, selected: Optional[EvaluatedCandidate]):
        self.step_index = step_index
        self.evaluated = evaluated
        self.selected = selected


class ObstructionRuntime:
    def __init__(
        self,
        seed: Any,
        functional: Any,
        evaluator: Any,
        generator: Any,
        weights: Optional[ScoreWeights] = None,
        selector: Optional[CandidateSelector] = None,
    ):
        w = weights or ScoreWeights.default()
        if hasattr(w, "validate"):
            w.validate()
        self.seed = seed
        self.functional = functional
        self.evaluator = evaluator
        self.generator = generator
        self.weights = w
        self.selector = selector or BestScoreSelector()
        self.current_state = seed
        self.step_index = 0
        self.trace = []

    @classmethod
    def try_new(
        cls,
        seed: Any,
        functional: Any,
        evaluator: Any,
        generator: Any,
        weights: Optional[ScoreWeights] = None,
        selector: Optional[CandidateSelector] = None,
    ) -> "ObstructionRuntime":
        return cls(seed, functional, evaluator, generator, weights, selector)

    def step(self) -> StepOutcome:
        candidates = self.generator.generate(self.current_state)
        evaluated = []
        for idx, cand in enumerate(candidates):
            if hasattr(self.functional, "compute"):
                metrics = self.functional.compute(cand.state)
            elif hasattr(self.functional, "evaluate"):
                metrics = self.functional.evaluate(cand.state)
            else:
                metrics = getattr(cand.state, "metrics", None)
            parent_metrics = getattr(self.current_state, "metrics", self.current_state)
            verdict = self.evaluator.decide(parent_metrics, metrics)
            score = obstruction_score(metrics, self.weights)
            evaluated.append(EvaluatedCandidate(idx, cand, metrics, verdict, score))
        selected = self.selector.select(evaluated)
        if selected is not None:
            self.current_state = selected.candidate.state
        outcome = StepOutcome(self.step_index, evaluated, selected)
        self.trace.append(outcome)
        self.step_index += 1
        return outcome


__all__ = [
    "BestScoreSelector",
    "Candidate",
    "CandidateGenerator",
    "CandidateSelector",
    "DefaultObstructionEvaluator",
    "EvaluatedCandidate",
    "ObstructionEvaluator",
    "ObstructionFunctional",
    "ObstructionMetrics",
    "ObstructionRuntime",
    "ObstructionThresholds",
    "ObstructionVerdict",
    "OperatorId",
    "Provenance",
    "ScoreWeights",
    "StepOutcome",
    "obstruction_score",
    "select_best_accepted",
]

