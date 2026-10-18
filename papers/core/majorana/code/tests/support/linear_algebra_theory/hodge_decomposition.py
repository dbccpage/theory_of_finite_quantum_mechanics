"""Paper 003 L2 Hodge comparison algebra."""

from __future__ import annotations
from typing import Dict

import numpy as np

from omega_engine.crates.homology_theory.discrete_derham import DiscreteDeRham


class HodgeDecomposition:
    """L2 Hodge decomposition on a graph without 2-cells."""

    def __init__(self, graph: DiscreteDeRham):
        self.graph = graph
        self.B = graph.B

    def decompose(self, delta: np.ndarray) -> Dict[str, np.ndarray]:
        """Return delta_ex in im(d_0) and delta_harm in ker(d_0^*)."""
        bt_b = self.B.T @ self.B
        bt_delta = self.B.T @ delta
        f_ls = np.linalg.lstsq(bt_b, bt_delta, rcond=None)[0]

        delta_ex = self.B @ f_ls
        delta_harm = delta - delta_ex

        return {
            "delta_ex": delta_ex,
            "delta_harm": delta_harm,
            "f_ls": f_ls,
        }

    def verify_orthogonality(
        self, delta_ex: np.ndarray, delta_harm: np.ndarray
    ) -> float:
        """Return <delta_ex, delta_harm> in the L2 coordinate system."""
        return float(np.dot(delta_ex, delta_harm))


class L1L2Tension:
    """L1/L2 comparison witnesses from Paper 003 Section 6."""

    @staticmethod
    def inflation_ratio_cycle(n: int) -> float:
        """Return the Paper 003 C_n inflation ratio 3 - 2/n."""
        return 3.0 - 2.0 / n

    @staticmethod
    def compute_inflation(graph: DiscreteDeRham, delta: np.ndarray) -> Dict[str, float]:
        """Compute the L1 inflation induced by the L2 Hodge decomposition."""
        result = HodgeDecomposition(graph).decompose(delta)

        norm_ex = float(np.sum(np.abs(result["delta_ex"])))
        norm_harm = float(np.sum(np.abs(result["delta_harm"])))
        norm_delta = float(np.sum(np.abs(delta)))
        ratio = (norm_ex + norm_harm) / norm_delta if norm_delta > 0 else 0.0

        return {
            "norm_ex_l1": norm_ex,
            "norm_harm_l1": norm_harm,
            "norm_delta_l1": norm_delta,
            "inflation_ratio": ratio,
        }



