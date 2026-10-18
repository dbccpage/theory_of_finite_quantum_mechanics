"""Cycle-aware traversal value types."""

from __future__ import annotations

import math


class XiWitness:
    def __init__(self, edge_distortions: list, xi_value: float, top_k: int):
        self.edge_distortions = [float(x) for x in edge_distortions]
        self.xi_value = float(xi_value)
        k = len(self.edge_distortions) if top_k == 0 or top_k > len(self.edge_distortions) else top_k
        indexed = sorted(enumerate(self.edge_distortions), key=lambda item: item[1], reverse=True)
        self.worst_edges = [index for index, _ in indexed[:k]]

    def is_valid(self) -> bool:
        return (
            math.isfinite(self.xi_value)
            and 0.0 <= self.xi_value <= 1.0
            and all(math.isfinite(value) and value >= 0.0 for value in self.edge_distortions)
            and all(index < len(self.edge_distortions) for index in self.worst_edges)
        )

    def is_coherent(self, tolerance: float) -> bool:
        return math.isfinite(tolerance) and tolerance >= 0.0 and all(
            value < tolerance for value in self.edge_distortions
        )

    def max_distortion(self) -> float:
        return max(self.edge_distortions) if self.edge_distortions else 0.0


class XiDiagnostic:
    def __init__(self, harmonic_projection: list, xi_value: float, witness: XiWitness):
        self.harmonic_projection = [float(x) for x in harmonic_projection]
        self.xi_value = float(xi_value)
        self.witness = witness


class CorrectionStrategy:
    HarmonicSnap = "HarmonicSnap"

    @staticmethod
    def is_valid(strategy: object) -> bool:
        if strategy == CorrectionStrategy.HarmonicSnap:
            return True
        if isinstance(strategy, dict) and strategy.get("type") == "GradientStep":
            alpha = strategy.get("alpha")
            return isinstance(alpha, (int, float)) and math.isfinite(alpha) and 0.0 <= alpha <= 1.0
        return False


class CycleAwareConfig:
    def __init__(self, xi_activation_threshold: float = 0.5, top_k_edges: int = 3, strategy=None):
        self.xi_activation_threshold = xi_activation_threshold
        self.top_k_edges = top_k_edges
        self.strategy = strategy or {"type": "GradientStep", "alpha": 0.5}

    @classmethod
    def default(cls) -> "CycleAwareConfig":
        return cls()


__all__ = ["CorrectionStrategy", "CycleAwareConfig", "XiDiagnostic", "XiWitness"]
