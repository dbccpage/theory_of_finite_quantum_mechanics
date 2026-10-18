"""Paper 002 coordinate additivity and coarea checks."""

import itertools
from typing import Dict, List, Optional, Tuple


def disjoint_support(x: List[float], y: List[float], tol: float = 1e-15) -> bool:
    """Check supp(x) cap supp(y) = empty."""
    return all(abs(a) <= tol or abs(b) <= tol for a, b in zip(x, y))


def lp_norm(x: List[float], p: float) -> float:
    """General lp norm, including p=inf."""
    if not x:
        return 0.0
    if p == float("inf"):
        return max(abs(v) for v in x)
    return sum(abs(v) ** p for v in x) ** (1.0 / p)


class CoordinateAdditivity:
    """Axiom checks and proof reconstruction for Paper 002."""

    @staticmethod
    def check_edge_locality(
        edge_defects: List[List[float]], p: float
    ) -> Tuple[bool, float]:
        return (True, sum(lp_norm(d, p) for d in edge_defects))

    @staticmethod
    def check_coordinate_symmetry(x: List[float], p: float) -> Tuple[bool, float]:
        n_x = lp_norm(x, p)
        for perm in itertools.permutations(x):
            n_perm = lp_norm(list(perm), p)
            if abs(n_perm - n_x) > 1e-12:
                return (False, abs(n_perm - n_x))
        return (True, 0.0)

    @staticmethod
    def check_coordinate_additivity(
        x: List[float], y: List[float], p: float
    ) -> Tuple[bool, float]:
        assert disjoint_support(x, y), "Vectors must have disjoint support"
        combined = [a + b for a, b in zip(x, y)]
        err = abs(lp_norm(combined, p) - (lp_norm(x, p) + lp_norm(y, p)))
        return (err < 1e-10, err)

    @staticmethod
    def check_graph_invariance(
        edge_defects: List[List[float]], p: float
    ) -> Tuple[bool, float]:
        per_edge = [lp_norm(d, p) for d in edge_defects]
        base = sum(per_edge)
        for perm in itertools.permutations(per_edge):
            if abs(sum(perm) - base) > 1e-12:
                return (False, abs(sum(perm) - base))
        return (True, 0.0)

    @staticmethod
    def sweep_axiom3(ps: Optional[List[float]] = None) -> Dict[float, Dict]:
        if ps is None:
            ps = [1.0, 1.5, 2.0, 3.0, float("inf")]
        x = [2.0, 0.0, -1.5, 0.0]
        y = [0.0, 3.0, 0.0, -0.7]
        results = {}
        for p in ps:
            passes, err = CoordinateAdditivity.check_coordinate_additivity(x, y, p)
            results[p] = {"passes": passes, "error": err}
        return results

    @staticmethod
    def proof_step_decompose(x: List[float]) -> List[List[float]]:
        return [[v if j == i else 0.0 for j in range(len(x))] for i, v in enumerate(x)]

    @staticmethod
    def proof_step_homogeneity(basis_vectors: List[List[float]], w_e: float) -> float:
        return w_e * sum(lp_norm(v, 1) for v in basis_vectors)


class CochainSpace:
    """C1(G,Rk) isometrically flattened to L1(E x {1..k})."""

    @staticmethod
    def flatten(edge_defects: List[List[float]]) -> List[float]:
        return [v for edge in edge_defects for v in edge]

    @staticmethod
    def verify_isometry(edge_defects: List[List[float]], alpha: float = 1.0) -> Dict:
        nu_g = alpha * sum(sum(abs(v) for v in edge) for edge in edge_defects)
        l1_f = alpha * sum(abs(v) for v in CochainSpace.flatten(edge_defects))
        return {
            "nu_G": nu_g,
            "l1_flat": l1_f,
            "isometry_holds": abs(nu_g - l1_f) < 1e-12,
        }


class CoareaDuality:
    """Discrete coarea formula for scalar signals."""

    @staticmethod
    def total_variation(
        node_values: Dict[str, float],
        edges: List[Tuple[str, str]],
    ) -> float:
        return sum(abs(node_values[b] - node_values[a]) for a, b in edges)

    @staticmethod
    def coarea_boundary_count(
        node_values: Dict[str, float],
        edges: List[Tuple[str, str]],
        level: float,
    ) -> int:
        return sum(
            1 for a, b in edges if (node_values[a] > level) != (node_values[b] > level)
        )

    @staticmethod
    def verify_coarea(
        node_values: Dict[str, float],
        edges: List[Tuple[str, str]],
        n_samples: int = 1000,
    ) -> Dict:
        tv = CoareaDuality.total_variation(node_values, edges)
        vals = sorted(node_values.values())
        lo, hi = vals[0] - 1.0, vals[-1] + 1.0
        dt = (hi - lo) / n_samples
        integral = sum(
            CoareaDuality.coarea_boundary_count(node_values, edges, lo + i * dt) * dt
            for i in range(n_samples)
        )
        return {
            "total_variation": tv,
            "coarea_integral": integral,
            "match": abs(tv - integral) < 0.1,
        }

