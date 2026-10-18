from typing import Dict, List, Tuple
import numpy as np


class AggregationMonotonicity:
    """Numerical checker for a DECLARED coarse-graining procedure.

    Computes l1 edge defects before and after block coarse-graining and reports
    whether the coarse defect did not exceed the fine defect for the given
    inputs. This is an empirical check on the supplied data for the declared
    procedure, NOT a proof of Theorem 2.1.
    """

    @staticmethod
    def coarse_grain_1d(
        values: List[float], edges: List[Tuple[int, int]], block_size: int = 2
    ) -> Tuple[List[float], List[Tuple[int, int]]]:
        """
        1D coarse-graining: block-average values, collapse internal edges.

        Type (a) edges: pi(a) != pi(b) -- survive into Q.
        Type (b) edges: pi(a) = pi(b) -- collapsed, contribute only to I_P.

        Requires ``block_size > 0`` and ``len(values)`` divisible by
        ``block_size`` (no leftover fine elements are silently dropped).
        """
        if block_size <= 0:
            raise ValueError("block_size must be positive")
        n = len(values)
        if n % block_size != 0:
            raise ValueError(
                f"len(values)={n} is not divisible by block_size={block_size}"
            )
        n_coarse = n // block_size
        coarse_vals = []
        for i in range(n_coarse):
            block = values[i * block_size : (i + 1) * block_size]
            coarse_vals.append(sum(block) / len(block))

        coarse_edges = []
        for i in range(n_coarse - 1):
            coarse_edges.append((i, i + 1))

        return coarse_vals, coarse_edges

    @staticmethod
    def l1_defect(values: List[float], edges: List[Tuple[int, int]]) -> float:
        """I(s) = sum_e |s(b) - s(a)|."""
        return sum(abs(values[b] - values[a]) for a, b in edges)

    @staticmethod
    def verify_monotonicity(
        values: List[float], edges: List[Tuple[int, int]], block_size: int = 2
    ) -> Dict:
        """
        Verify Theorem 2.1: I_Q(pi_* s) <= I_P(s).

        Coarse-graining cannot increase the total defect.
        """
        I_fine = AggregationMonotonicity.l1_defect(values, edges)
        coarse_vals, coarse_edges = AggregationMonotonicity.coarse_grain_1d(
            values, edges, block_size
        )
        I_coarse = AggregationMonotonicity.l1_defect(coarse_vals, coarse_edges)
        return {
            "I_fine": I_fine,
            "I_coarse": I_coarse,
            "monotone": I_coarse <= I_fine + 1e-10,
        }

    @staticmethod
    def coarse_grain_2d(s: np.ndarray, block_size: int = 2) -> np.ndarray:
        """2D block averaging: 2x2 -> 1 (for grid experiments)."""
        s = np.asarray(s)
        if s.ndim != 2:
            raise ValueError("coarse_grain_2d requires a 2D array")
        H, W = s.shape
        if H % block_size != 0 or W % block_size != 0:
            raise ValueError(
                f"COARSE_GRID_LEFTOVER_REFUSED: shape ({H}, {W}) is not divisible by block_size={block_size}"
            )
        new_H = H // block_size
        new_W = W // block_size
        return np.array(
            [
                [
                    np.mean(
                        s[
                            block_size * i : block_size * (i + 1),
                            block_size * j : block_size * (j + 1),
                        ]
                    )
                    for j in range(new_W)
                ]
                for i in range(new_H)
            ]
        )

    @staticmethod
    def l1_energy_2d(s: np.ndarray, periodic: bool = True) -> float:
        """I(s) = sum |dx| + sum |dy| on a 2D grid."""
        s = np.asarray(s)
        if s.ndim != 2:
            raise ValueError("l1_energy_2d requires a 2D array")
        if periodic:
            dx = np.roll(s, -1, axis=0) - s
            dy = np.roll(s, -1, axis=1) - s
        else:
            dx = np.diff(s, axis=0)
            dy = np.diff(s, axis=1)
        return float(np.sum(np.abs(dx)) + np.sum(np.abs(dy)))

    @staticmethod
    def verify_2d_monotonicity(s: np.ndarray) -> Dict:
        """Verify Theorem 2.1 on a 2D grid under block coarse-graining."""
        I_fine = AggregationMonotonicity.l1_energy_2d(s)
        s_coarse = AggregationMonotonicity.coarse_grain_2d(s)
        I_coarse = AggregationMonotonicity.l1_energy_2d(s_coarse)
        return {
            "I_fine": I_fine,
            "I_coarse": I_coarse,
            "monotone": I_coarse <= I_fine + 1e-10,
        }

