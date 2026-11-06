"""Finite graph diffusion and logarithmic return-probability slopes.
AuthorityEffect: None.
The graph constructors are declared combinatorial fixtures. No physical length,
declared scale, CDT path integral, or AJL reproduction is inferred from them.
"""

from __future__ import annotations

import math
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple


@dataclass(frozen=True)
class DiffusionStepReceipt:
    tau: int
    return_prob: float
    log_tau: float
    log_return_prob: float
    spectral_dimension: float
    regime: str


@dataclass(frozen=True)
class SpectralDimensionReceipt:
    num_nodes: int
    steps: Sequence[DiffusionStepReceipt]
    d_short: float  # Spectral dimension at short/early-step diffusion scales (tau ~ 1-3)
    d_macro: float  # Spectral dimension at later-step diffusion scales
    has_slope_crossover: bool
    saturation_reached: bool


class CdtDualGraph:
    """Constructs finite periodic graph fixtures; no simplex incidence is represented."""

    @staticmethod
    def construct_flat_4d_grid(L: int = 5) -> Tuple[int, List[List[int]]]:
        """Constructs a four-dimensional periodic grid graph of size L^4."""
        num_nodes = L**4
        adj: List[List[int]] = [[] for _ in range(num_nodes)]

        def idx(x: int, y: int, z: int, w: int) -> int:
            return (((x % L) * L + (y % L)) * L + (z % L)) * L + (w % L)

        for x in range(L):
            for y in range(L):
                for z in range(L):
                    for w in range(L):
                        curr = idx(x, y, z, w)
                        neighbors = [
                            idx(x + 1, y, z, w),
                            idx(x - 1, y, z, w),
                            idx(x, y + 1, z, w),
                            idx(x, y - 1, z, w),
                            idx(x, y, z + 1, w),
                            idx(x, y, z - 1, w),
                            idx(x, y, z, w + 1),
                            idx(x, y, z, w - 1),
                        ]
                        adj[curr] = list(set(neighbors))
        return num_nodes, adj

    @staticmethod
    def construct_cdt_sandwich_dual(
        num_layers: int = 8, spatial_size: int = 6
    ) -> Tuple[int, List[List[int]]]:
        """Constructs a periodic layered grid graph.

        No simplicial incidence, light-cone metric or causal foliation is represented.
        """
        num_spatial = spatial_size**3
        num_nodes = num_layers * num_spatial
        adj: List[List[int]] = [[] for _ in range(num_nodes)]

        def s_idx(x: int, y: int, z: int) -> int:
            return ((x % spatial_size) * spatial_size + (y % spatial_size)) * spatial_size + (
                z % spatial_size
            )

        def node_idx(t: int, s: int) -> int:
            return (t % num_layers) * num_spatial + s

        for t in range(num_layers):
            for x in range(spatial_size):
                for y in range(spatial_size):
                    for z in range(spatial_size):
                        s = s_idx(x, y, z)
                        u = node_idx(t, s)

                        # Neighbors within each three-dimensional grid layer
                        s_neighbors = [
                            s_idx(x + 1, y, z),
                            s_idx(x - 1, y, z),
                            s_idx(x, y + 1, z),
                            s_idx(x, y - 1, z),
                            s_idx(x, y, z + 1),
                            s_idx(x, y, z - 1),
                        ]
                        # Timelike causal neighbors (forward and backward in foliation)
                        t_forward = node_idx(t + 1, s)
                        t_backward = node_idx(t - 1, s)

                        # In CDT, causal light-cone connectivity:
                        neighbors = [node_idx(t, sn) for sn in s_neighbors]
                        neighbors.extend([t_forward, t_backward])
                        adj[u] = list(set(neighbors))

        return num_nodes, adj


class DiscreteHeatDiffusionEngine:
    """Computes discrete diffusion return probabilities and spectral dimensions."""

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "cdt_diffusion.db")
        self.cur = self.conn.cursor()
        self._init_schema()

    def _init_schema(self) -> None:
        schema_path = Path(__file__).resolve().parent.parent / "databases" / "regge_wdw_schema.sql"
        if not schema_path.exists():
            schema_path = Path(__file__).resolve().parent / "regge_wdw_schema.sql"
        if schema_path.exists():
            self.cur.executescript(schema_path.read_text(encoding="utf-8"))
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    @staticmethod
    def build_transition_matrix(num_nodes: int, adj: List[List[int]]) -> List[List[float]]:
        """Constructs row-stochastic transition matrix M_ij = A_ij / deg(i)."""
        M = [[0.0 for _ in range(num_nodes)] for _ in range(num_nodes)]
        for i in range(num_nodes):
            deg = len(adj[i])
            if deg == 0:
                M[i][i] = 1.0
            else:
                prob = 1.0 / deg
                for j in adj[i]:
                    M[i][j] = prob
        return M

    @staticmethod
    def compute_return_probability_random_walk(num_nodes, adj, tau_max=40, lazy_prob=0.5):
        """Average all diagonal entries of the lazy graph transition powers."""
        if num_nodes <= 0 or len(adj) != num_nodes or tau_max < 0 or not 0 <= lazy_prob <= 1:
            raise ValueError("Invalid finite graph or diffusion parameters")
        if any(v < 0 or v >= num_nodes for row in adj for v in row):
            raise ValueError("Neighbor outside the declared graph")
        profile = [0.0] * (tau_max + 1)
        for start in range(num_nodes):
            prob = {start: 1.0}
            profile[0] += 1.0
            for t in range(1, tau_max + 1):
                nxt = {}
                for u, mass in prob.items():
                    if not adj[u]:
                        nxt[u] = nxt.get(u, 0.0) + mass
                        continue
                    nxt[u] = nxt.get(u, 0.0) + mass * (1-lazy_prob)
                    for v in adj[u]:
                        nxt[v] = nxt.get(v, 0.0) + mass * lazy_prob / len(adj[u])
                prob = nxt
                profile[t] += prob.get(start, 0.0)
        return [p / num_nodes for p in profile]

    @staticmethod
    def compute_spectral_dimension_curve(
        P_tau: List[float], taus: Sequence[int]
    ) -> List[Tuple[int, float, float, float, float]]:
        """Computes d_s(tau) = -2 * d(log P) / d(log tau) using logarithmic finite differences.

        Returns list of (tau, P(tau), log_tau, log_P, d_s(tau)).
        """
        results = []
        for i, tau in enumerate(taus):
            p = P_tau[tau]
            log_t = math.log(tau)
            log_p = math.log(max(p, 1e-15))

            # Finite difference in log space
            t_prev = max(1, tau - 1)
            t_next = min(len(P_tau) - 1, tau + 1)
            if t_next == t_prev:
                ds = 0.0
            else:
                d_log_p = math.log(max(P_tau[t_next], 1e-15)) - math.log(max(P_tau[t_prev], 1e-15))
                d_log_t = math.log(t_next) - math.log(t_prev)
                ds = -2.0 * (d_log_p / d_log_t) if d_log_t != 0.0 else 0.0

            results.append((tau, p, log_t, log_p, ds))
        return results

    @staticmethod
    def classify_diffusion_regime(tau: int, ds: float, tau_max: int) -> str:
        """Classifies numerical slope ranges; these labels have no physical scale."""
        if tau > tau_max * 0.8 and ds < 1.5:
            return "FINITE_SIZE_SATURATION"
        elif ds < 2.3:
            return "LOW_SLOPE"
        elif ds < 3.3:
            return "MID_SLOPE"
        else:
            return "HIGH_SLOPE"

    def evaluate_cdt_sandwich_diffusion(
        self,
        num_layers: int = 8,
        spatial_size: int = 6,
        tau_max: int = 35,
    ) -> SpectralDimensionReceipt:
        """Evaluates diffusion on a 4D declared layered graph, recording steps in SQLite."""
        num_nodes, adj = CdtDualGraph.construct_cdt_sandwich_dual(num_layers, spatial_size)
        P_tau = self.compute_return_probability_random_walk(num_nodes, adj, tau_max=tau_max)

        taus = list(range(1, tau_max + 1))
        curve = self.compute_spectral_dimension_curve(P_tau, taus)

        steps: Sequence[DiffusionStepReceipt] = []

        for tau, p, log_t, log_p, ds in curve:
            regime = self.classify_diffusion_regime(tau, ds, tau_max)
            step_rc = DiffusionStepReceipt(
                tau=tau,
                return_prob=p,
                log_tau=log_t,
                log_return_prob=log_p,
                spectral_dimension=ds,
                regime=regime,
            )
            steps.append(step_rc)

            # Insert into SQLite CdtDiffusionTrajectory
            self.cur.execute(
                """INSERT INTO CdtDiffusionTrajectory
                   (tau, return_prob, log_tau, log_return_prob, spectral_dimension, regime)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (tau, p, log_t, log_p, ds, regime),
            )
        self.conn.commit()

        # early-step spectral dimension: average over short times tau in [1, 3]
        short_steps = [s.spectral_dimension for s in steps if 1 <= s.tau <= 3]
        d_short = sum(short_steps) / len(short_steps) if short_steps else float("nan")

        # Macroscopic spectral dimension: peak in intermediate scaling regime tau in [4, 10]
        macro_steps = [s.spectral_dimension for s in steps if 4 <= s.tau <= 10]
        d_macro = max(macro_steps) if macro_steps else float("nan")

        has_reduction = d_short < d_macro and d_short < 3.0 and d_macro >= 3.2
        saturation = any(s.regime == "FINITE_SIZE_SATURATION" for s in steps)

        return SpectralDimensionReceipt(
            num_nodes=num_nodes,
            steps=steps,
            d_short=d_short,
            d_macro=d_macro,
            has_slope_crossover=has_reduction,
            saturation_reached=saturation,
        )


    def get_sql_spectral_reduction_audit(self) -> List[Dict[str, Any]]:
        """Queries ViewCdtSpectralDimensionalReduction from SQLite."""
        self.cur.execute(
            """SELECT tau, return_prob, log_tau, log_return_prob, spectral_dimension, regime
               FROM ViewCdtSpectralDimensionalReduction"""
        )
        rows = self.cur.fetchall()
        return [
            {
                "tau": r[0],
                "return_prob": r[1],
                "log_tau": r[2],
                "log_return_prob": r[3],
                "spectral_dimension": r[4],
                "regime": r[5],
            }
            for r in rows
        ]


__all__ = [
    "CdtDualGraph",
    "DiffusionStepReceipt",
    "DiscreteHeatDiffusionEngine",
    "SpectralDimensionReceipt",
]
