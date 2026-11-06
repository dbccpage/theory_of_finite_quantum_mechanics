"""Recovered verbatim from ``code/j.py`` at ``be3a3d2f6c`` (the letter file was
deleted without a prose successor; the ``dda_cascade`` conformance vector binds
this class). Only the lazy phi1 import path is adapted. AuthorityEffect: None."""
import numpy as np
from typing import Tuple, List, Dict, Optional


class DdaCascadeRouter:
    """Categorical DDA Cascade Router & Trace Tape Generator.
    Cascades:
      Level 0: d0 Gauge Repair (exact translation)
      Level 1: Fiber Pruning via n_Pi leakage test
      Level 2: Context Extension Inclusion C^\bullet -> C'^\bullet nullifying [omega]
    Records complete DDA trace tape of execution steps.
    """

    def __init__(self, d0: np.ndarray, d1: np.ndarray):
        self.d0 = np.asarray(d0, dtype=float)
        self.d1 = np.asarray(d1, dtype=float)
        self.tape: List[str] = ["C"]

    def compute_hodge_components(self, w: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        w_vec = np.asarray(w, dtype=float)
        u0, s0, _ = np.linalg.svd(self.d0, full_matrices=False)
        rank0 = np.sum(s0 > 1e-10)
        exact = u0[:, :rank0] @ (u0[:, :rank0].T @ w_vec) if rank0 > 0 else np.zeros_like(w_vec)

        delta1 = self.d1.T
        v1, s1, _ = np.linalg.svd(delta1, full_matrices=False)
        rank1 = np.sum(s1 > 1e-10)
        coexact = v1[:, :rank1] @ (v1[:, :rank1].T @ w_vec) if rank1 > 0 else np.zeros_like(w_vec)

        harmonic = w_vec - exact - coexact
        return exact, coexact, harmonic

    def _carrier(self):
        """Recover (vertices, edges) from d0 so the exact LP can be called."""
        edges = []
        for row in self.d0:
            nz = np.flatnonzero(np.abs(row) > 1e-12)
            if len(nz) != 2:
                return None, None
            tail = int(nz[0]) if row[nz[0]] < 0 else int(nz[1])
            head = int(nz[1]) if row[nz[0]] < 0 else int(nz[0])
            edges.append((tail, head))
        return list(range(self.d0.shape[1])), edges

    def phi1_exact(self, w: np.ndarray) -> float:
        r"""Phi_1 by exact linear programming, not the l2-Hodge surrogate.

        This previously returned ||harmonic + coexact||_1 computed from SVD projections.
        That is an l2 object read as an l1 one: the Hodge split is l2-ORTHOGONAL, but the
        l1 norm is not additive across it, so the surrogate can exceed Phi_1 by up to the
        3 - 2/n inflation on cycle graphs (FOC_004 s1.1 item 4). `phi1_comparison` reports
        both so the gap stays visible instead of being folded away.
        """
        vertices, edges = self._carrier()
        if vertices is None:
            return float(np.sum(np.abs(w)))
        from universe_anomalonica.codaq.phi1_lp import phi1_estimate

        return float(phi1_estimate(vertices, edges, np.asarray(w, dtype=float))["min_l1"])

    def phi1_comparison(self, w: np.ndarray) -> Dict[str, float]:
        """Exact Phi_1 against the l2-Hodge surrogate that used to stand in for it."""
        _, coexact, harmonic = self.compute_hodge_components(w)
        surrogate = float(np.sum(np.abs(harmonic + coexact)))
        exact = self.phi1_exact(w)
        return {
            "phi1_exact_lp": exact,
            "phi1_l2_hodge_surrogate": surrogate,
            "inflation_ratio": (surrogate / exact) if exact > 1e-12 else float("nan"),
            "surrogate_overstates": bool(surrogate > exact + 1e-9),
        }

    def route_and_execute(
        self,
        w: np.ndarray,
        d0_ext: Optional[np.ndarray] = None,
        w_ext: Optional[np.ndarray] = None,
        eps: float = 1e-8,
    ) -> Tuple[str, List[str], float]:
        exact, coexact, harmonic = self.compute_hodge_components(w)
        phi1 = self.phi1_exact(w)

        if phi1 <= eps:
            self.tape.extend(["E", "I", "T"])
            return "LEVEL_0_REPAIR", self.tape, 0.0

        self.tape.append("R")

        if np.linalg.norm(harmonic) > eps:
            self.tape.append("M")

        if d0_ext is not None:
            w_target = np.asarray(w_ext if w_ext is not None else w, dtype=float)
            u_ext, s_ext, _ = np.linalg.svd(d0_ext, full_matrices=False)
            rank_ext = np.sum(s_ext > 1e-10)
            proj_ext = u_ext[:, :rank_ext] @ (u_ext[:, :rank_ext].T @ w_target) if rank_ext > 0 else np.zeros_like(w_target)
            phi1_ext = float(np.sum(np.abs(w_target - proj_ext)))

            if phi1_ext <= eps:
                self.tape.extend(["Lambda", "E", "I", "T"])
                return "LEVEL_2_EXTENSION", self.tape, 0.0

        self.tape.append("T")
        return "HALTED_OBSTRUCTION", self.tape, phi1
