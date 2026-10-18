"""Paper Alpha primitive difference operator."""

import math
from typing import Dict, List, Tuple


class PrimitiveDifference:
    """Primitive scalar difference and raw L1 inconsistency."""

    @staticmethod
    def validate(section: Dict[str, float]) -> None:
        for k, v in section.items():
            assert math.isfinite(v), f"Invalid scalar at {k}: {v}"

    @staticmethod
    def phi_raw(section: Dict[str, float], edges: List[Tuple[str, str]]) -> float:
        """Phi_raw = sum_e |x_b - x_a|."""
        PrimitiveDifference.validate(section)
        return sum(abs(section[b] - section[a]) for a, b in edges)

    @staticmethod
    def support(
        section: Dict[str, float],
        edges: List[Tuple[str, str]],
        tol: float = 1e-10,
    ) -> int:
        """Number of edges with nonzero defect."""
        return sum(1 for a, b in edges if abs(section[b] - section[a]) > tol)

    @staticmethod
    def delta_phi(
        old: Dict[str, float],
        new: Dict[str, float],
        edges: List[Tuple[str, str]],
        changed: List[str],
    ) -> float:
        """Incremental Phi change over edges incident to changed nodes."""
        PrimitiveDifference.validate(old)
        PrimitiveDifference.validate(new)
        changed_set = set(changed)
        total = 0.0
        for a, b in edges:
            if a in changed_set or b in changed_set:
                total += abs(new[b] - new[a]) - abs(old[b] - old[a])
        return total

