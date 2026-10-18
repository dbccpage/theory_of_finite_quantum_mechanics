"""Base Banach presheaf types for Paper 001."""

from typing import Dict, List, Tuple

import numpy as np
from numpy.linalg import norm as np_norm


class BanachStalk:
    """A Banach stalk F(x)=R^d with the standard Euclidean norm."""

    def __init__(self, dim: int, label: str = ""):
        self.dim = dim
        self.label = label

    def norm(self, v: np.ndarray) -> float:
        return float(np_norm(v, ord=2))


class RestrictionMap:
    """Bounded linear restriction map r_{b,a}: F(b) -> F(a)."""

    def __init__(self, matrix: np.ndarray, source_label: str, target_label: str):
        self.matrix = matrix
        self.source_label = source_label
        self.target_label = target_label
        self.op_norm = float(np_norm(matrix, ord=2))

    def apply(self, v: np.ndarray) -> np.ndarray:
        return self.matrix @ v

    def is_contractive(self) -> bool:
        return self.op_norm <= 1.0 + 1e-12


class BanachPresheaf:
    """Finite-dimensional numpy Banach-shadow prototype over an edge poset.

    Prototype carrier: stalks are R^d Euclidean spaces and restriction maps are
    finite matrices. The `validate()` method performs structural numpy checks
    (known endpoints, present restrictions, matrix shape vs stalk dimensions,
    finite entries) but it is opt-in and is NOT called automatically.
    """

    def __init__(
        self,
        stalks: Dict[str, BanachStalk],
        edges: List[Tuple[str, str]],
        restrictions: Dict[Tuple[str, str], RestrictionMap],
    ):
        self.stalks = stalks
        self.edges = edges
        self.restrictions = restrictions

    def validate(self) -> None:
        """Refuse structurally malformed presheaves (opt-in numpy checks).

        Raises:
            ValueError: if an edge references an unknown node, an edge has no
                restriction, a restriction matrix shape mismatches the source/
                target stalk dimensions, or any matrix entry is non-finite.
        """
        for a, b in self.edges:
            if a not in self.stalks:
                raise ValueError(f"edge source {a!r} is not a known stalk")
            if b not in self.stalks:
                raise ValueError(f"edge target {b!r} is not a known stalk")
            r = self.restrictions.get((a, b))
            if r is None:
                raise ValueError(f"edge {(a, b)!r} has no restriction map")
            mat = np.asarray(r.matrix)
            # r: F(b) -> F(a), so matrix is (dim(a) x dim(b)).
            expected = (self.stalks[a].dim, self.stalks[b].dim)
            if mat.shape != expected:
                raise ValueError(
                    f"restriction {(a, b)!r} matrix shape {mat.shape} "
                    f"!= expected {expected}"
                )
            if not np.all(np.isfinite(mat)):
                raise ValueError(
                    f"restriction {(a, b)!r} matrix has non-finite entries"
                )

    def coboundary(
        self, section: Dict[str, np.ndarray]
    ) -> Dict[Tuple[str, str], np.ndarray]:
        delta = {}
        for a, b in self.edges:
            r = self.restrictions[(a, b)]
            delta[(a, b)] = r.apply(section[b]) - section[a]
        return delta

    def l1_coboundary_norm(self, section: Dict[str, np.ndarray]) -> float:
        """Sum of Euclidean stalk norms of the coboundary over all edges.

        This is the sum over edges (a, b) of the Euclidean (L2) norm of the
        coboundary value in stalk F(a). It is a float DIAGNOSTIC only and is
        NOT authority-grade.
        """
        delta = self.coboundary(section)
        return sum(self.stalks[a].norm(d) for (a, _), d in delta.items())
