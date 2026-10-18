"""Algebraic L1 universality checks for Paper 000."""

import math
from typing import Dict, List, Tuple


class L1Universality:
    """Verification helpers for additive universality of the L1 diagnostic."""

    @staticmethod
    def norm_gap(x: List[float]) -> float:
        if not x:
            return 0.0
        l1 = sum(abs(v) for v in x)
        l2 = math.sqrt(sum(v * v for v in x))
        return l1 - l2

    @staticmethod
    def check_disjoint_additivity(p: float) -> Tuple[bool, float]:
        a, b = [1.0, 2.0, 3.0], [4.0, 5.0]
        combined = a + b
        if p == float("inf"):
            na = max(abs(v) for v in a)
            nb = max(abs(v) for v in b)
            nc = max(abs(v) for v in combined)
        else:
            na = sum(abs(v) ** p for v in a) ** (1 / p)
            nb = sum(abs(v) ** p for v in b) ** (1 / p)
            nc = sum(abs(v) ** p for v in combined) ** (1 / p)
        err = abs(nc - (na + nb))
        return (err < 1e-10, err)

    @staticmethod
    def sweep_p_values() -> Dict:
        results = {}
        for p in [1.0, 1.5, 2.0, 3.0, float("inf")]:
            passes, err = L1Universality.check_disjoint_additivity(p)
            results[p] = {"passes": passes, "error": err}
        return results

    @staticmethod
    def dispersion_analysis() -> List[Dict]:
        cases = [
            ("sparse (localized)", [1.0, 0.0, 0.0]),
            ("distributed", [1.0, -1.0, 0.0]),
            ("fully distributed", [1.0, 1.0, 1.0]),
        ]
        results = []
        for name, x in cases:
            l1 = sum(abs(v) for v in x)
            l2 = math.sqrt(sum(v * v for v in x))
            results.append(
                {"name": name, "vector": x, "l1": l1, "l2": l2, "gap": l1 - l2}
            )
        return results

