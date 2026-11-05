"""
Graph and 2-cell Complex Carrier with Vector Stalks.
Paper: GS-002 (so_k_invariant_gauge_classification)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Union, Sequence, Any
import numpy as np


class SlaterViolationError(ValueError):
    """Raised when weights violate the strict interior Slater condition (w_e <= 0)."""

    pass


class TopologicalDefectError(ValueError):
    """Raised when boundary operator composition fails nilpotency (d1 @ d0 != 0)."""

    pass


@dataclass(frozen=True)
class Cochain:
    """Vector-valued cochain in C^0(G; R^k), C^1(G; R^k), or C^2(G; R^k)."""

    data: np.ndarray
    degree: int = 1

    def __init__(self, data: Union[np.ndarray, Sequence[Any]], degree: int = 1) -> None:
        if degree not in (0, 1, 2):
            raise ValueError(f"Degree must be 0, 1, or 2 (got {degree}).")

        arr = np.asarray(data, dtype=float)
        if arr.ndim == 0:
            raise ValueError("Cochain data must be 1D or 2D (got scalar / rank 0).")
        elif arr.ndim == 1:
            arr = arr.reshape(-1, 1)
        elif arr.ndim > 2:
            raise ValueError(f"Cochain data must be 1D or 2D (got rank {arr.ndim}).")

        if not np.all(np.isfinite(arr)):
            raise ValueError("Cochain data must contain finite real numbers.")

        object.__setattr__(self, "data", arr)
        object.__setattr__(self, "degree", int(degree))

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.data.shape

    @property
    def num_cells(self) -> int:
        return self.data.shape[0]

    @property
    def stalk_dim(self) -> int:
        return self.data.shape[1] if self.data.ndim > 1 else 1

    def mixed_l1_l2_norm(self, weights: Optional[np.ndarray | List[float]] = None) -> float:
        """Compute ||data||_{1,2,w} = sum_i w_i ||data_i||_2."""
        stalk_l2 = np.linalg.norm(self.data, axis=1)
        if weights is None:
            return float(np.sum(stalk_l2))
        w = np.asarray(weights, dtype=float)
        if w.ndim != 1 or w.shape != (len(stalk_l2),):
            raise ValueError(
                f"Weights length {len(w)} does not match cochain cells {len(stalk_l2)}: must have exact 1D shape ({len(stalk_l2)},), got {w.shape}."
            )
        if not np.all(np.isfinite(w)):
            raise ValueError("Weights must contain finite real numbers.")
        if np.any(w <= 0):
            raise ValueError("Weights must be strictly positive.")
        return float(np.sum(w * stalk_l2))

    def coordinate_l1_l1_norm(self, weights: Optional[np.ndarray | List[float]] = None) -> float:
        """Compute ||data||_{1,1,w} = sum_i w_i sum_j |data_{i,j}|."""
        stalk_l1 = np.sum(np.abs(self.data), axis=1)
        if weights is None:
            return float(np.sum(stalk_l1))
        w = np.asarray(weights, dtype=float)
        if w.ndim != 1 or w.shape != (len(stalk_l1),):
            raise ValueError(
                f"Weights length {len(w)} does not match cochain cells {len(stalk_l1)}: must have exact 1D shape ({len(stalk_l1)},), got {w.shape}."
            )
        if not np.all(np.isfinite(w)):
            raise ValueError("Weights must contain finite real numbers.")
        if np.any(w <= 0):
            raise ValueError("Weights must be strictly positive.")
        return float(np.sum(w * stalk_l1))

    def __add__(self, other: Cochain) -> Cochain:
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        return Cochain(self.data + other.data, degree=self.degree)

    def __sub__(self, other: Cochain) -> Cochain:
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        return Cochain(self.data - other.data, degree=self.degree)

    def __neg__(self) -> Cochain:
        return Cochain(-self.data, degree=self.degree)

    def __rmul__(self, scalar: float) -> Cochain:
        return Cochain(scalar * self.data, degree=self.degree)


class GraphComplex:
    """
    Finite 2-complex C^0 -d0-> C^1 -d1-> C^2 with R^k vector stalks.
    d0: 0-cells (vertices) -> 1-cells (directed edges)
    d1: 1-cells (directed edges) -> 2-cells (faces)
    d1 @ d0 = 0.
    """

    def __init__(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int]],
        faces: Optional[List[List[Tuple[int, int]]]] = None,
        stalk_dim: int = 2,
        edge_weights: Optional[List[float] | np.ndarray] = None,
        face_weights: Optional[List[float] | np.ndarray] = None,
    ) -> None:
        if isinstance(num_vertices, bool) or not isinstance(num_vertices, (int, np.integer)) or num_vertices < 1:
            raise ValueError(f"num_vertices must be integer >= 1 (got {num_vertices}).")
        if isinstance(stalk_dim, bool) or not isinstance(stalk_dim, (int, np.integer)) or stalk_dim < 1:
            raise ValueError(f"stalk_dim must be integer >= 1 (got {stalk_dim}).")

        self.num_vertices = int(num_vertices)
        self.edges = list(edges)
        self.num_edges = len(self.edges)
        if self.num_edges < 1:
            raise ValueError("GraphComplex must have at least one edge (num_edges >= 1).")
        self.stalk_dim = int(stalk_dim)

        # Validate edge endpoints
        for e_idx, edge in enumerate(self.edges):
            if not (isinstance(edge, (tuple, list)) and len(edge) == 2):
                raise ValueError(f"Edge {e_idx} must be a 2-tuple (u, v).")
            u, v = edge
            if isinstance(u, bool) or isinstance(v, bool) or not (
                isinstance(u, (int, np.integer)) and isinstance(v, (int, np.integer))
            ):
                raise ValueError(f"Edge {e_idx} endpoints must be integers (non-boolean).")
            if not (0 <= u < self.num_vertices and 0 <= v < self.num_vertices):
                raise ValueError(
                    f"Edge {e_idx} endpoints ({u}, {v}) out of bounds for num_vertices={self.num_vertices}."
                )
            if u == v:
                raise ValueError(f"Edge {e_idx} is a self-loop ({u}, {v}), which is disallowed.")

        # Edge weights c_e > 0
        if edge_weights is None:
            self.edge_weights = np.ones(self.num_edges, dtype=float)
        else:
            self.edge_weights = np.asarray(edge_weights, dtype=float)
            if self.edge_weights.ndim != 1 or self.edge_weights.shape != (self.num_edges,):
                raise ValueError(
                    f"Edge weights must match number of edges ({self.num_edges}) with exact 1D shape ({self.num_edges},), got {self.edge_weights.shape}."
                )
            if not np.all(np.isfinite(self.edge_weights)):
                raise ValueError("Edge weights must be finite.")
            if np.any(self.edge_weights <= 0):
                raise SlaterViolationError(
                    "Edge weights must be strictly positive (Slater condition violated: w_e <= 0)."
                )

        # Faces: each face is a signed boundary of edges [(edge_idx, orientation_sign), ...]
        self.faces = faces if faces is not None else []
        self.num_faces = len(self.faces)

        # Validate face boundaries
        for f_idx, face in enumerate(self.faces):
            if not isinstance(face, (list, tuple)):
                raise ValueError(f"Face {f_idx} must be a sequence of (edge_idx, sign) pairs.")
            for term in face:
                if not (isinstance(term, (tuple, list)) and len(term) == 2):
                    raise ValueError(f"Face {f_idx} term must be a pair (edge_idx, sign).")
                e_idx, sign = term
                if not (isinstance(e_idx, (int, np.integer)) and not isinstance(e_idx, bool)):
                    raise ValueError(
                        f"Face {f_idx} edge index must be an integer (got {type(e_idx).__name__}: {e_idx})."
                    )
                if not (0 <= e_idx < self.num_edges):
                    raise ValueError(
                        f"Face {f_idx} refers to out-of-bounds edge index {e_idx} (num_edges={self.num_edges})."
                    )
                if not (isinstance(sign, (int, np.integer)) and not isinstance(sign, bool) and sign in (+1, -1)):
                    raise ValueError(
                        f"Face {f_idx} orientation sign must be +1 or -1 (got {sign})."
                    )

        # Face weights u_f > 0
        if face_weights is None:
            self.face_weights = np.ones(self.num_faces, dtype=float)
        else:
            self.face_weights = np.asarray(face_weights, dtype=float)
            if self.face_weights.ndim != 1 or self.face_weights.shape != (self.num_faces,):
                raise ValueError(
                    f"Face weights must match number of faces ({self.num_faces}) with exact 1D shape ({self.num_faces},), got {self.face_weights.shape}."
                )
            if not np.all(np.isfinite(self.face_weights)):
                raise ValueError("Face weights must be finite.")
            if np.any(self.face_weights <= 0):
                raise SlaterViolationError(
                    "Face weights must be strictly positive (Slater condition violated: u_f <= 0)."
                )

        self._d0_matrix: Optional[np.ndarray] = None
        self._d1_matrix: Optional[np.ndarray] = None

    @property
    def d0(self) -> np.ndarray:
        """Incidence matrix d0 (m edges x n vertices). For e=(u->v), (d0 alpha)_e = alpha(v) - alpha(u)."""
        if self._d0_matrix is None:
            mat = np.zeros((self.num_edges, self.num_vertices), dtype=float)
            for e_idx, (u, v) in enumerate(self.edges):
                mat[e_idx, u] = -1.0
                mat[e_idx, v] = 1.0
            self._d0_matrix = mat
        return self._d0_matrix

    @property
    def d1(self) -> np.ndarray:
        """Coboundary matrix d1 (F faces x m edges)."""
        if self._d1_matrix is None:
            mat = np.zeros((self.num_faces, self.num_edges), dtype=float)
            for f_idx, edge_terms in enumerate(self.faces):
                for e_idx, sign in edge_terms:
                    mat[f_idx, e_idx] += float(sign)
            self._d1_matrix = mat
        return self._d1_matrix

    def verify_complex(self, tol: float = 1e-12) -> bool:
        """Check d1 @ d0 == 0."""
        if self.num_faces == 0:
            return True
        prod = self.d1 @ self.d0
        return bool(np.all(np.abs(prod) < tol))

    def verify_complex_strict(self, tol: float = 1e-12) -> None:
        """Check d1 @ d0 == 0 strictly, raising TopologicalDefectError on perturbation."""
        if self.num_faces == 0:
            return
        prod = self.d1 @ self.d0
        max_err = float(np.max(np.abs(prod)))
        if max_err >= tol:
            raise TopologicalDefectError(
                f"Boundary operator perturbation detected: d1 @ d0 != 0 (max norm = {max_err:.4e} >= {tol:.4e})"
            )

    def coboundary_d0(self, alpha: np.ndarray) -> Cochain:
        """Apply d0 to 0-cochain alpha of shape (n, k), returning 1-cochain of shape (m, k)."""
        alpha_arr = np.asarray(alpha, dtype=float)
        if alpha_arr.shape != (self.num_vertices, self.stalk_dim):
            raise ValueError(
                f"Alpha shape {alpha_arr.shape} must be ({self.num_vertices}, {self.stalk_dim})"
            )
        return Cochain(self.d0 @ alpha_arr, degree=1)

    def coboundary_d1(self, omega: Cochain) -> Cochain:
        """Apply d1 to 1-cochain omega of shape (m, k), returning 2-cochain of shape (F, k)."""
        if omega.shape != (self.num_edges, self.stalk_dim):
            raise ValueError(
                f"Omega shape {omega.shape} must be ({self.num_edges}, {self.stalk_dim})"
            )
        return Cochain(self.d1 @ omega.data, degree=2)

    def dual_coboundary_d0_star(self, phi: Cochain) -> np.ndarray:
        """Apply d0^* to 1-cochain phi of shape (m, k), returning divergence of shape (n, k)."""
        if phi.shape != (self.num_edges, self.stalk_dim):
            raise ValueError(
                f"Phi shape {phi.shape} must be ({self.num_edges}, {self.stalk_dim})"
            )
        return self.d0.T @ phi.data

    @classmethod
    def create_cycle_graph(
        cls,
        cycle_len: int,
        stalk_dim: int = 2,
        edge_weights: Optional[List[float] | np.ndarray] = None,
        with_face: bool = True,
        orientations: Optional[List[int] | np.ndarray] = None,
    ) -> GraphComplex:
        """Factory for directed n-cycle 0 -> 1 -> ... -> (n-1) -> 0 with optional signed orientations."""
        if cycle_len < 3:
            raise ValueError(f"cycle_len must be >= 3 (got {cycle_len}).")

        if orientations is None:
            edges = [(i, (i + 1) % cycle_len) for i in range(cycle_len)]
            faces = [[(i, 1) for i in range(cycle_len)]] if with_face else None
        else:
            ori_list = list(orientations)
            if len(ori_list) != cycle_len:
                raise ValueError("Orientations length must match cycle_len.")
            edges = []
            face_terms = []
            for i, sign in enumerate(ori_list):
                if not (isinstance(sign, (int, np.integer)) and not isinstance(sign, bool) and sign in (+1, -1)):
                    raise ValueError(f"Orientation sign must be exactly +1 or -1 (got {sign}).")
                u, v = i, (i + 1) % cycle_len
                if sign == 1:
                    edges.append((u, v))
                    face_terms.append((i, 1))
                else:
                    edges.append((v, u))
                    face_terms.append((i, -1))
            faces = [face_terms] if with_face else None
        return cls(
            num_vertices=cycle_len,
            edges=edges,
            faces=faces,
            stalk_dim=stalk_dim,
            edge_weights=edge_weights,
            face_weights=[1.0] if with_face else None,
        )

    @classmethod
    def create_theta_graph(
        cls, stalk_dim: int = 2, edge_weights: Optional[List[float] | np.ndarray] = None
    ) -> GraphComplex:
        """
        Theta graph: two vertices (0, 1) connected by 3 parallel directed edges e0, e1, e2.
        Faces: 2 cycles:
          f0 = e0 - e1
          f1 = e1 - e2
        d1 @ d0 = 0 automatically holds.
        """
        edges = [(0, 1), (0, 1), (0, 1)]
        faces = [[(0, 1), (1, -1)], [(1, 1), (2, -1)]]
        return cls(
            num_vertices=2,
            edges=edges,
            faces=faces,
            stalk_dim=stalk_dim,
            edge_weights=edge_weights,
        )
