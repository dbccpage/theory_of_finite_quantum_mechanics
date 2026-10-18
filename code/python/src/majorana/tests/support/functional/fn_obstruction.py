"""Pure obstruction metrics and scoring interfaces."""

from omega_engine.crates.type.obstruction_runtime import ObstructionMetrics, ScoreWeights


def obstruction_score(metrics: ObstructionMetrics, weights: ScoreWeights) -> float:
    if metrics is None or not metrics.is_valid():
        return float("-inf")
    return -metrics.phi_1 - weights.lambda_gamma * metrics.gamma_2 + weights.lambda_xi * metrics.xi


class ObstructionFunctional:
    def compute(self, state) -> ObstructionMetrics:
        raise NotImplementedError


__all__ = ["ObstructionFunctional", "obstruction_score"]
