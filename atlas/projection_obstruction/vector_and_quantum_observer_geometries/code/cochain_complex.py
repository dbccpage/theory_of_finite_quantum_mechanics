"""
Cochain Complex and Graph/Cellular Complex Representations.
Paper: GS-003 (vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Union
import numpy as np

from exceptions import DimensionMismatchError, BoundaryConditionError


@dataclass(frozen=True)
class Cochain:
    """
    Cochain in C^0, C^1, or C^2 with vector stalks R^k or operator stalks Herm_0(C^d).
    For vectors, data shape is (num_cells, k) or (num_cells,).
    For operators, data shape is (num_cells, d, d).
    """

    data: np.ndarray
    degree: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.data, np.ndarray):
            object.__setattr__(self, "data", np.asarray(self.data))
        arr = self.data
        if arr.ndim == 1:
            object.__setattr__(self, "data", arr.reshape(-1, 1))

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.data.shape

    @property
    def num_cells(self) -> int:
        return self.data.shape[0]

    @property
    def is_operator(self) -> bool:
        return self.data.ndim == 3 and self.data.shape[1] == self.data.shape[2]

    @property
    def stalk_dim(self) -> int:
        if self.is_operator:
            return self.data.shape[1]
        return self.data.shape[1] if self.data.ndim > 1 else 1

    def mixed_norm(
        self, p: Union[int, float] = 2, weights: Optional[np.ndarray] = None
    ) -> float:
        """
        Mixed norm ||data||_{1,p,w} = sum_e w_e ||data_e||_p for vector stalks.
        Supports p = 1, 2, or np.inf.
        """
        if self.is_operator:
            raise ValueError("Use trace_norm() for operator cochains.")
        if p == 1:
            stalk_norms = np.sum(np.abs(self.data), axis=1)
        elif p == 2:
            stalk_norms = np.linalg.norm(self.data, axis=1)
        elif p == np.inf or p == "inf":
            stalk_norms = np.max(np.abs(self.data), axis=1)
        else:
            stalk_norms = np.power(
                np.sum(np.power(np.abs(self.data), p), axis=1), 1.0 / p
            )

        if weights is None:
            return float(np.sum(stalk_norms))
        w = np.asarray(weights, dtype=float)
        if len(w) != len(stalk_norms):
            raise DimensionMismatchError(
                f"Weights length {len(w)} != cells {len(stalk_norms)}"
            )
        return float(np.sum(w * stalk_norms))

    def trace_norm(self, weights: Optional[np.ndarray] = None) -> float:
        """
        Trace distance gauge J_Q(delta) = sum_e w_e * 0.5 * ||delta_e||_1
        where ||X||_1 = sum_i sigma_i(X) is the Schatten 1-norm.
        """
        if not self.is_operator:
            raise ValueError("trace_norm() requires operator cochain (ndim=3).")
        m = self.num_cells
        vals = np.zeros(m, dtype=float)
        for e in range(m):
            mat = self.data[e]
            s = np.linalg.svdvals(mat)
            vals[e] = 0.5 * float(np.sum(s))
        if weights is None:
            return float(np.sum(vals))
        w = np.asarray(weights, dtype=float)
        if len(w) != m:
            raise DimensionMismatchError(f"Weights length {len(w)} != cells {m}")
        return float(np.sum(w * vals))

    def __add__(self, other: Cochain) -> Cochain:
        if not isinstance(other, Cochain):
            raise TypeError(f"Cannot add Cochain to {type(other)}")
        if self.shape != other.shape or self.degree != other.degree:
            raise DimensionMismatchError(
                f"Shape/degree mismatch: {self.shape},deg={self.degree} vs {other.shape},deg={other.degree}"
            )
        return Cochain(self.data + other.data, degree=self.degree)

    def __sub__(self, other: Cochain) -> Cochain:
        if not isinstance(other, Cochain):
            raise TypeError(f"Cannot subtract {type(other)} from Cochain")
        if self.shape != other.shape or self.degree != other.degree:
            raise DimensionMismatchError(
                f"Shape/degree mismatch: {self.shape},deg={self.degree} vs {other.shape},deg={other.degree}"
            )
        return Cochain(self.data - other.data, degree=self.degree)

    def __neg__(self) -> Cochain:
        return Cochain(-self.data, degree=self.degree)

    def __mul__(self, scalar: Union[int, float, complex]) -> Cochain:
        return Cochain(scalar * self.data, degree=self.degree)

    def __rmul__(self, scalar: Union[int, float, complex]) -> Cochain:
        return Cochain(scalar * self.data, degree=self.degree)

    def __getitem__(self, idx: int) -> np.ndarray:
        return self.data[idx]

    def __len__(self) -> int:
        return self.num_cells


class GraphComplex:
    """
    Finite 2-Cell Complex C^0 -> d0 -> C^1 -> d1 -> C^2.
    Supports vertices, directed edges, and signed 2-cells.
    """

    def __init__(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int]],
        faces: Optional[List[List[Tuple[int, int]]]] = None,
        edge_weights: Optional[List[float]] = None,
    ) -> None:
        self.num_vertices = num_vertices
        self.edges = list(edges)
        self.num_edges = len(self.edges)

        # Edge weights validation
        if edge_weights is None:
            self.edge_weights = np.ones(self.num_edges, dtype=float)
        else:
            self.edge_weights = np.asarray(edge_weights, dtype=float)
            if len(self.edge_weights) != self.num_edges:
                raise DimensionMismatchError(
                    "Edge weights length does not match number of edges."
                )
            if np.any(self.edge_weights <= 0):
                raise ValueError(
                    "Edge weights must be strictly positive (Slater condition)."
                )

        # Incidence matrix d0: (m, n) where row e=(u, v) has -1 at u and +1 at v
        self.d0_matrix = np.zeros((self.num_edges, self.num_vertices), dtype=float)
        for e_idx, (u, v) in enumerate(self.edges):
            if u < 0 or u >= num_vertices or v < 0 or v >= num_vertices:
                raise ValueError(f"Edge ({u}, {v}) references non-existent vertex.")
            self.d0_matrix[e_idx, u] -= 1.0
            self.d0_matrix[e_idx, v] += 1.0

        # 2-cells (faces) and boundary matrix d1: (num_faces, m)
        self.faces = faces or []
        self.num_faces = len(self.faces)
        self.d1_matrix = np.zeros((self.num_faces, self.num_edges), dtype=float)
        for f_idx, face in enumerate(self.faces):
            # face is list of (edge_index, orientation_sign)
            for e_idx, sign in face:
                if e_idx < 0 or e_idx >= self.num_edges:
                    raise ValueError(f"Face references invalid edge {e_idx}")
                self.d1_matrix[f_idx, e_idx] += float(sign)

    def verify_boundary_property(self, tol: float = 1e-12) -> bool:
        """
        Verify that d1 d0 = 0 (boundary of a boundary is zero).
        Raises BoundaryConditionError if violated.
        """
        if self.num_faces == 0:
            return True
        d1_d0 = self.d1_matrix @ self.d0_matrix
        err = float(np.max(np.abs(d1_d0)))
        if err > tol:
            raise BoundaryConditionError(
                f"d1 d0 != 0: max absolute entry is {err} > {tol}"
            )
        return True

    def d0(self, phi: Cochain) -> Cochain:
        """Coboundary map d0: C^0 -> C^1."""
        if phi.degree != 0 or phi.num_cells != self.num_vertices:
            raise DimensionMismatchError(
                f"Cochain not in C^0(V): cells={phi.num_cells}, deg={phi.degree}"
            )

        if phi.is_operator:
            d = phi.stalk_dim
            res = np.zeros((self.num_edges, d, d), dtype=phi.data.dtype)
            for e_idx, (u, v) in enumerate(self.edges):
                res[e_idx] = phi.data[v] - phi.data[u]
            return Cochain(res, degree=1)
        else:
            res = self.d0_matrix @ phi.data
            return Cochain(res, degree=1)

    def d1(self, omega: Cochain) -> Cochain:
        """Coboundary map d1: C^1 -> C^2."""
        if omega.degree != 1 or omega.num_cells != self.num_edges:
            raise DimensionMismatchError(
                f"Cochain not in C^1(E): cells={omega.num_cells}, deg={omega.degree}"
            )
        if self.num_faces == 0:
            raise ValueError("Complex has no 2-cells (faces); d1 is not defined.")

        if omega.is_operator:
            d = omega.stalk_dim
            res = np.zeros((self.num_faces, d, d), dtype=omega.data.dtype)
            for f_idx in range(self.num_faces):
                for e_idx in range(self.num_edges):
                    coeff = self.d1_matrix[f_idx, e_idx]
                    if abs(coeff) > 1e-12:
                        res[f_idx] += coeff * omega.data[e_idx]
            return Cochain(res, degree=2)
        else:
            res = self.d1_matrix @ omega.data
            return Cochain(res, degree=2)

    def d0_adjoint(self, z: Cochain) -> Cochain:
        """
        Divergence map d0^*: C^1 -> C^0.
        (d0^* z)(u) = sum_{e: target(e)=u} z_e - sum_{e: source(e)=u} z_e.
        """
        if z.degree != 1 or z.num_cells != self.num_edges:
            raise DimensionMismatchError(
                f"Cochain not in C^1(E): cells={z.num_cells}, deg={z.degree}"
            )

        if z.is_operator:
            d = z.stalk_dim
            div = np.zeros((self.num_vertices, d, d), dtype=z.data.dtype)
            for e_idx, (u, v) in enumerate(self.edges):
                div[v] += z.data[e_idx]
                div[u] -= z.data[e_idx]
            return Cochain(div, degree=0)
        else:
            div = self.d0_matrix.T @ z.data
            return Cochain(div, degree=0)

    def laplacian_0(self) -> np.ndarray:
        """Sheaf/graph 0-Laplacian L_0 = d0^* d0 on C^0."""
        return self.d0_matrix.T @ self.d0_matrix

    def laplacian_1(self) -> np.ndarray:
        """
        Sheaf/graph 1-Laplacian L_1 = d0 d0^* + d1^* d1 on C^1.
        """
        l1 = self.d0_matrix @ self.d0_matrix.T
        if self.num_faces > 0:
            l1 += self.d1_matrix.T @ self.d1_matrix
        return l1

    @classmethod
    def triangle_complex(
        cls, edge_weights: Optional[List[float]] = None
    ) -> GraphComplex:
        """
        Standard 3-cycle triangle complex:
        Vertices: 0, 1, 2
        Edges: (0, 1), (1, 2), (2, 0)
        Face: 1 counter-clockwise 2-cell with edges [(0, +1), (1, +1), (2, +1)].
        """
        edges = [(0, 1), (1, 2), (2, 0)]
        faces = [[(0, 1), (1, 1), (2, 1)]]
        comp = cls(num_vertices=3, edges=edges, faces=faces, edge_weights=edge_weights)
        comp.verify_boundary_property()
        return comp
