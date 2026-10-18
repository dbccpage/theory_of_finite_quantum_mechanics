"""Obstruction evaluator threshold checks."""

import math
from typing import Optional

from omega_engine.crates.type.obstruction_runtime import ObstructionMetrics, ObstructionThresholds, ObstructionVerdict, ScoreWeights


def validate_obstruction_thresholds(thresholds: ObstructionThresholds) -> None:
    for name, value in (
        ("phi_tol", thresholds.phi_tol),
        ("gamma2_threshold", thresholds.gamma2_threshold),
        ("gamma2_delta_threshold", thresholds.gamma2_delta_threshold),
        ("noether_drift_threshold", thresholds.noether_drift_threshold),
    ):
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be finite and nonnegative")
    if not math.isfinite(thresholds.xi_threshold) or not 0.0 <= thresholds.xi_threshold <= 1.0:
        raise ValueError("xi_threshold must be in [0,1]")


def validate_score_weights(weights: ScoreWeights) -> None:
    if not math.isfinite(weights.lambda_gamma) or weights.lambda_gamma < 0.0:
        raise ValueError("lambda_gamma must be finite and nonnegative")
    if not math.isfinite(weights.lambda_xi) or weights.lambda_xi < 0.0:
        raise ValueError("lambda_xi must be finite and nonnegative")


class ObstructionEvaluator:
    def decide(self, parent: ObstructionMetrics, child: ObstructionMetrics) -> str:
        raise NotImplementedError


class DefaultObstructionEvaluator(ObstructionEvaluator):
    def __init__(self, thresholds: Optional[ObstructionThresholds] = None):
        self.thresholds = thresholds or ObstructionThresholds.default()
        validate_obstruction_thresholds(self.thresholds)

    @classmethod
    def try_new(cls, thresholds: ObstructionThresholds) -> "DefaultObstructionEvaluator":
        return cls(thresholds)

    @classmethod
    def new_unchecked(cls, thresholds: ObstructionThresholds) -> "DefaultObstructionEvaluator":
        instance = cls.__new__(cls)
        instance.thresholds = thresholds
        return instance

    def decide(self, parent: ObstructionMetrics, child: ObstructionMetrics) -> str:
        if not parent.is_finite() or not child.is_finite() or not parent.is_valid_range() or not child.is_valid_range():
            return ObstructionVerdict.Invalid
        if child.noether_drift is not None and abs(child.noether_drift) > self.thresholds.noether_drift_threshold:
            return ObstructionVerdict.Invalid
        if child.xi < self.thresholds.xi_threshold:
            return ObstructionVerdict.Incoherent
        if child.gamma_2 > self.thresholds.gamma2_threshold:
            return ObstructionVerdict.Oscillatory
        if child.gamma2_delta is not None and abs(child.gamma2_delta) > self.thresholds.gamma2_delta_threshold:
            return ObstructionVerdict.Oscillatory
        if child.phi_1 <= parent.phi_1 + self.thresholds.phi_tol:
            return ObstructionVerdict.Accept
        return ObstructionVerdict.Reject


__all__ = ["DefaultObstructionEvaluator", "ObstructionEvaluator", "validate_obstruction_thresholds", "validate_score_weights"]
