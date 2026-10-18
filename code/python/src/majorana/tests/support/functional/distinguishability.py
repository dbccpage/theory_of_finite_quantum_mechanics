import numpy as np
from typing import Dict, List

from omega_engine.crates.linear_algebra_theory.schatten import SchattenExtension


class DistinguishabilityBound:
    """Pathwise trace-distance bound checker.

    For an ordered path of matrices, computes endpoint trace distance and
    the sum of adjacent trace distances. The reported bound is a metric
    TRIANGLE-INEQUALITY check on ``SchattenExtension.trace_distance``; it is
    NOT a physical distinguishability certificate. The inequality holds for
    any metric on the supplied matrices regardless of whether they are valid
    quantum states. Treat the result as a numerical metric check only.

    ``half_I`` convention: ``half_I`` is already the half-summed edge mass,
    i.e. it equals ``(1/2) * I(s)`` because each ``trace_distance`` edge term
    is itself ``(1/2)||rho_u - rho_v||_1``. The endpoint ``T_ab`` carries the
    same ``1/2`` factor, so the comparison ``T_ab <= half_I`` is consistent.
    """

    @staticmethod
    def evaluate_path_triangle_bound(
        states: Dict[str, np.ndarray],
        path: List[str],
    ) -> Dict:
        """
        Verify T(rho_a, rho_b) <= 1/2 * I(s) along a path.

        For identity restriction maps:
            I(s) = sum_e ||rho_{e+1} - rho_e||_1
            T(a,b) = 1/2 ||rho_a - rho_b||_1
        """
        if len(path) < 2:
            raise ValueError("path must contain at least two nodes")

        missing = [p for p in path if p not in states]
        if missing:
            raise KeyError(f"missing states for path nodes: {missing}")

        for p in path:
            arr = np.asarray(states[p])
            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError(f"state '{p}' must be a square 2D matrix")
            if not np.all(np.isfinite(arr)):
                raise ValueError(f"state '{p}' must contain only finite values")

        shapes = {states[p].shape for p in path}
        if len(shapes) != 1:
            raise ValueError("all states on path must have same shape")

        half_I = 0.0
        edge_distances = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            t_e = SchattenExtension.trace_distance(states[u], states[v])
            half_I += t_e
            edge_distances.append((u, v, t_e))

        T_ab = SchattenExtension.trace_distance(states[path[0]], states[path[-1]])

        return {
            "T_endpoint": T_ab,
            "half_I": half_I,
            "bound_holds": T_ab <= half_I + 1e-10,
            "edge_distances": edge_distances,
        }



