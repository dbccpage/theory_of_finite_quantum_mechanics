"""Finite graph and overlap-matrix numerical examples.
AuthorityEffect: None.
Legacy CDT names denote graph fixtures, not causal triangulations. Dense NumPy
calculations check finite operator identities within tolerance. They establish no
spacetime model, doubler-removal theorem, or uniform localization bound.
"""

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np


class DiracAlgebra4D:
    """Standard 4D Dirac gamma matrices and chiral matrix gamma_5."""

    def __init__(self):
        # Pauli matrices
        sigma_1 = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        sigma_2 = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
        sigma_3 = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
        i_2 = np.eye(2, dtype=complex)
        zero_2 = np.zeros((2, 2), dtype=complex)

        # Chiral (Weyl) basis:
        # gamma^0 = [[0, I], [I, 0]]
        # gamma^k = [[0, sigma_k], [-sigma_k, 0]]
        self.gamma_0 = np.block([[zero_2, i_2], [i_2, zero_2]])
        self.gamma_1 = np.block([[zero_2, sigma_1], [-sigma_1, zero_2]])
        self.gamma_2 = np.block([[zero_2, sigma_2], [-sigma_2, zero_2]])
        self.gamma_3 = np.block([[zero_2, sigma_3], [-sigma_3, zero_2]])

        # gamma_5 = i gamma^0 gamma^1 gamma^2 gamma^3 = [[-I, 0], [0, I]]
        self.gamma_5 = np.block([[-i_2, zero_2], [zero_2, i_2]])

        self.gammas = [self.gamma_0, self.gamma_1, self.gamma_2, self.gamma_3]


@dataclass
class SimplicialComplexGraph:
    """Graph structure of a simplicial complex for fermion propagation."""

    complex_id: str
    geometry_type: str  # 'REGULAR_GAPPED' or 'SINGULAR_GAPLESS'
    num_vertices: int
    edges: List[Tuple[int, int]]
    edge_vectors: Dict[Tuple[int, int], np.ndarray] = field(default_factory=dict)
    lattice_spacing_a: float = 1.0


class CdtOverlapDiracEvaluator:
    """Evaluates overlap Dirac operators and Ginsparg-Wilson chiral symmetry on CDT."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or ":memory:"
        self.conn = sqlite3.connect(self.db_path)
        self.algebra = DiracAlgebra4D()
        self._init_db()

    def _init_db(self) -> None:
        """Initializes database schema from regge_wdw_schema.sql."""
        schema_path = Path(__file__).resolve().parent.parent / "databases" / "regge_wdw_schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                self.conn.executescript(f.read())
        self.conn.commit()

    def build_regular_gapped_complex(
        self, complex_id: str = "cdt_gapped_01", num_vertices: int = 6
    ) -> SimplicialComplexGraph:
        """Constructs a regular, highly connected CDT sandwich complex with open spectral gap."""
        # Hexagonal prism / regular 4D cross-polytope sub-complex
        edges = []
        edge_vecs = {}
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                edges.append((i, j))
                # Normalized directional unit vector in 4D
                vec = np.zeros(4, dtype=float)
                vec[(j - i) % 4] = 1.0
                edge_vecs[(i, j)] = vec
                edge_vecs[(j, i)] = -vec

        return SimplicialComplexGraph(
            complex_id=complex_id,
            geometry_type="REGULAR_GAPPED",
            num_vertices=num_vertices,
            edges=edges,
            edge_vectors=edge_vecs,
            lattice_spacing_a=1.0,
        )

    def build_singular_gapless_complex(
        self, complex_id: str = "cdt_singular_01", num_vertices: int = 8
    ) -> SimplicialComplexGraph:
        """Constructs a singular CDT complex with bottleneck geometry causing spectral gap closing."""
        # Two clusters connected by a single bottleneck link
        edges = []
        edge_vecs = {}
        # Cluster A: 0..3
        for i in range(4):
            for j in range(i + 1, 4):
                edges.append((i, j))
                vec = np.zeros(4, dtype=float)
                vec[(j - i) % 4] = 1.0
                edge_vecs[(i, j)] = vec
                edge_vecs[(j, i)] = -vec

        # Cluster B: 4..7
        for i in range(4, 8):
            for j in range(i + 1, 8):
                edges.append((i, j))
                vec = np.zeros(4, dtype=float)
                vec[(j - i) % 4] = 1.0
                edge_vecs[(i, j)] = vec
                edge_vecs[(j, i)] = -vec

        # Weak bottleneck connection between vertex 3 and vertex 4
        edges.append((3, 4))
        vec_neck = np.array([0.0, 0.0, 0.0, 1.0], dtype=float)
        edge_vecs[(3, 4)] = vec_neck
        edge_vecs[(4, 3)] = -vec_neck

        return SimplicialComplexGraph(
            complex_id=complex_id,
            geometry_type="SINGULAR_GAPLESS",
            num_vertices=num_vertices,
            edges=edges,
            edge_vectors=edge_vecs,
            lattice_spacing_a=1.0,
        )

    def build_wilson_dirac_operator(
        self,
        graph: SimplicialComplexGraph,
        m0: float = 1.2,
        r: float = 1.0,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Constructs discrete Wilson-Dirac operator D_w and global Gamma_5.

        Returns:
            (D_w, Gamma_5, H_w)
        """
        nv = graph.num_vertices
        n_dof = 4 * nv
        a = graph.lattice_spacing_a

        D_naive = np.zeros((n_dof, n_dof), dtype=complex)
        W = np.zeros((n_dof, n_dof), dtype=complex)
        Gamma_5 = np.zeros((n_dof, n_dof), dtype=complex)

        # Global Gamma_5 = I_nv \otimes gamma_5
        for v in range(nv):
            idx = slice(4 * v, 4 * (v + 1))
            Gamma_5[idx, idx] = self.algebra.gamma_5

        # Build D_naive and Wilson term W
        degrees = {v: 0 for v in range(nv)}
        for u, v in graph.edges:
            degrees[u] += 1
            degrees[v] += 1
            n_uv = graph.edge_vectors.get((u, v), np.array([1.0, 0.0, 0.0, 0.0]))
            # sum_mu n_uv^mu gamma^mu
            gamma_n = sum(n_uv[mu] * self.algebra.gammas[mu] for mu in range(4))

            idx_u = slice(4 * u, 4 * (u + 1))
            idx_v = slice(4 * v, 4 * (v + 1))

            # Anti-Hermitian naive hopping
            hop_forward = (1.0 / (2.0 * a)) * gamma_n
            D_naive[idx_u, idx_v] += hop_forward
            D_naive[idx_v, idx_u] -= hop_forward.conj().T

            # Wilson laplacian hopping: -(r / 2a) I_4
            wilson_hop = -(r / (2.0 * a)) * np.eye(4, dtype=complex)
            W[idx_u, idx_v] += wilson_hop
            W[idx_v, idx_u] += wilson_hop

        # Wilson diagonal: (r / 2a) deg(v) I_4
        for v in range(nv):
            idx = slice(4 * v, 4 * (v + 1))
            W[idx, idx] += (r / (2.0 * a)) * float(degrees[v]) * np.eye(4, dtype=complex)

        D_w = D_naive + W

        # Hermitian Wilson Hamiltonian: H_w = Gamma_5 (D_w - m0 * I)
        H_w = Gamma_5 @ (D_w - m0 * np.eye(n_dof, dtype=complex))
        # Enforce exact Hermiticity against floating-point roundoff
        H_w = 0.5 * (H_w + H_w.conj().T)

        return D_w, Gamma_5, H_w

    def build_overlap_dirac_operator(
        self,
        graph: SimplicialComplexGraph,
        m0: float = 1.2,
        r: float = 1.0,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
        """Constructs Neuberger overlap Dirac operator D_ov = (1/a)(I + Gamma_5 sgn(H_w)).

        Returns:
            (D_ov, Gamma_5, sgn_Hw, spectral_gap)
        """
        D_w, Gamma_5, H_w = self.build_wilson_dirac_operator(graph, m0, r)
        a = graph.lattice_spacing_a

        # Spectral decomposition of H_w
        eigenvals, eigenvecs = np.linalg.eigh(H_w)
        spectral_gap = float(np.min(np.abs(eigenvals)))

        # Matrix sign function sgn(H_w)
        # Avoid division by zero if gap is tiny
        eps = 1e-14
        sgn_vals = np.where(np.abs(eigenvals) > eps, np.sign(eigenvals), 1.0)
        sgn_Hw = eigenvecs @ np.diag(sgn_vals) @ eigenvecs.conj().T

        # Overlap Dirac operator: D_ov = (1/a) * (I + Gamma_5 @ sgn(H_w))
        n_dof = 4 * graph.num_vertices
        D_ov = (1.0 / a) * (np.eye(n_dof, dtype=complex) + Gamma_5 @ sgn_Hw)

        return D_ov, Gamma_5, sgn_Hw, spectral_gap

    def evaluate_ginsparg_wilson_relation(
        self, D_ov: np.ndarray, Gamma_5: np.ndarray, a: float = 1.0
    ) -> float:
        """Evaluates residual ||{D_ov, Gamma_5} - a D_ov Gamma_5 D_ov||_inf."""
        anticomm = D_ov @ Gamma_5 + Gamma_5 @ D_ov
        quad = a * D_ov @ Gamma_5 @ D_ov
        diff = np.max(np.abs(anticomm - quad))
        return float(diff)

    def evaluate_luescher_chiral_invariance(
        self, D_ov: np.ndarray, Gamma_5: np.ndarray, a: float = 1.0
    ) -> float:
        """Evaluates exact invariance of fermion bilinear under Lüscher chiral variation."""
        # For arbitrary test spinor psi, delta S = psi^dagger (Gamma_5 D_ov + D_ov Gamma_5 - a D_ov Gamma_5 D_ov) psi
        operator_defect = (D_ov @ Gamma_5 + Gamma_5 @ D_ov) - (a * D_ov @ Gamma_5 @ D_ov)
        return float(np.max(np.abs(operator_defect)))

    def evaluate_topological_index(self, D_ov, Gamma_5, a=1.0):
        """Numerical index and chirality on the computed nullspace; n_plus - n_minus."""
        d = np.asarray(D_ov, dtype=complex)
        g = np.asarray(Gamma_5, dtype=complex)
        if d.ndim != 2 or d.shape[0] != d.shape[1] or g.shape != d.shape or not len(d):
            raise ValueError("Expected nonempty square operators of equal shape")
        if not np.isfinite(d).all() or not np.isfinite(g).all() or not np.isfinite(a) or a <= 0:
            raise ValueError("Operators and positive lattice scale must be finite")
        identity = np.eye(len(d))
        if not np.allclose(g, g.conj().T) or not np.allclose(g @ g, identity):
            raise ValueError("Chirality must be a Hermitian involution")
        if not np.allclose(d @ g + g @ d, a * d @ g @ d, atol=1e-8):
            raise ValueError("Ginsparg-Wilson identity not satisfied within tolerance")
        index = float(np.trace(g @ (identity - a * d / 2)).real)
        _, singular_values, vh = np.linalg.svd(d)
        basis = vh.conj().T[:, singular_values <= 1e-8]
        if not basis.shape[1]:
            return index, 0, 0
        restricted = basis.conj().T @ g @ basis
        chiralities = np.linalg.eigvalsh((restricted + restricted.conj().T) / 2)
        if not np.allclose(np.abs(chiralities), 1, atol=1e-7):
            raise ValueError("Nullspace is not invariant under chirality")
        return index, int(np.sum(chiralities > 0)), int(np.sum(chiralities < 0))



    def close(self) -> None:
        self.conn.close()
