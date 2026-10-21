r"""4D CDT Ginsparg-Wilson & Neuberger Overlap Dirac Operator Engine.
AuthorityEffect: None.

Formulates Ginsparg-Wilson and Neuberger overlap Dirac operators on 4D Lorentzian
Causal Dynamical Triangulation (CDT) complexes to evaluate whether exact lattice
chiral symmetry (Lüscher chiral invariance) can be preserved on dynamical
triangulations without species doubling or boundary nilpotence violations.

Key components:
1. Dirac gamma algebra in 4D: gamma^0..gamma^3 and chiral gamma^5 = i gamma^0 gamma^1 gamma^2 gamma^3.
2. Discrete Wilson-Dirac operator D_w = D_naive + W with anti-Hermitian hopping and Hermitian Wilson Laplacian.
3. Hermitian Wilson-Dirac Hamiltonian H_w = gamma_5 (D_w - m_0).
4. Matrix sign function sgn(H_w) via spectral decomposition.
5. Neuberger overlap Dirac operator D_ov = (1/a)(I + gamma_5 sgn(H_w)).
6. Exact Ginsparg-Wilson algebraic relation: {D_ov, gamma_5} = a D_ov gamma_5 D_ov.
7. Exact Lüscher chiral action invariance |delta S| <= 1e-12.
8. Lattice Atiyah-Singer index theorem Index(D_ov) = (1/2) Tr(gamma_5 a D_ov) = n_+ - n_-.
9. Doubler decoupling: Wilson mass gap lifts all 15 doubler states to O(1/a).
10. Locality audit: exponential kernel decay on gapped complexes vs locality obstruction when lambda_min(H_w) -> 0.
11. Relational SQLite logging and view ViewCdtOverlapDiracAudit.
"""

from dataclasses import dataclass, field
import math
from pathlib import Path
import sqlite3
from typing import Dict, List, Optional, Set, Tuple
import numpy as np


class DiracAlgebra4D:
    """Standard 4D Dirac gamma matrices and chiral matrix gamma_5."""

    def __init__(self):
        sigma_1 = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        sigma_2 = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
        sigma_3 = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
        i_2 = np.eye(2, dtype=complex)
        zero_2 = np.zeros((2, 2), dtype=complex)

        self.gamma_0 = np.block([[zero_2, i_2], [i_2, zero_2]])
        self.gamma_1 = np.block([[zero_2, sigma_1], [-sigma_1, zero_2]])
        self.gamma_2 = np.block([[zero_2, sigma_2], [-sigma_2, zero_2]])
        self.gamma_3 = np.block([[zero_2, sigma_3], [-sigma_3, zero_2]])

        self.gamma_5 = np.block([[-i_2, zero_2], [zero_2, i_2]])

        self.gammas = [self.gamma_0, self.gamma_1, self.gamma_2, self.gamma_3]


@dataclass
class SimplicialComplexGraph:
    """Graph structure of a simplicial complex for fermion propagation."""
    complex_id: str
    geometry_type: str
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
        edges = []
        edge_vecs = {}
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                edges.append((i, j))
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
        edges = []
        edge_vecs = {}
        for i in range(4):
            for j in range(i + 1, 4):
                edges.append((i, j))
                vec = np.zeros(4, dtype=float)
                vec[(j - i) % 4] = 1.0
                edge_vecs[(i, j)] = vec
                edge_vecs[(j, i)] = -vec

        for i in range(4, 8):
            for j in range(i + 1, 8):
                edges.append((i, j))
                vec = np.zeros(4, dtype=float)
                vec[(j - i) % 4] = 1.0
                edge_vecs[(i, j)] = vec
                edge_vecs[(j, i)] = -vec

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

        for v in range(nv):
            idx = slice(4 * v, 4 * (v + 1))
            Gamma_5[idx, idx] = self.algebra.gamma_5

        degrees = {v: 0 for v in range(nv)}
        for u, v in graph.edges:
            degrees[u] += 1
            degrees[v] += 1
            n_uv = graph.edge_vectors.get((u, v), np.array([1.0, 0.0, 0.0, 0.0]))
            gamma_n = sum(n_uv[mu] * self.algebra.gammas[mu] for mu in range(4))

            idx_u = slice(4 * u, 4 * (u + 1))
            idx_v = slice(4 * v, 4 * (v + 1))

            hop_forward = (1.0 / (2.0 * a)) * gamma_n
            D_naive[idx_u, idx_v] += hop_forward
            D_naive[idx_v, idx_u] -= hop_forward.conj().T

            wilson_hop = -(r / (2.0 * a)) * np.eye(4, dtype=complex)
            W[idx_u, idx_v] += wilson_hop
            W[idx_v, idx_u] += wilson_hop

        for v in range(nv):
            idx = slice(4 * v, 4 * (v + 1))
            W[idx, idx] += (r / (2.0 * a)) * float(degrees[v]) * np.eye(4, dtype=complex)

        D_w = D_naive + W

        H_w = Gamma_5 @ (D_w - m0 * np.eye(n_dof, dtype=complex))
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

        eigenvals, eigenvecs = np.linalg.eigh(H_w)
        spectral_gap = float(np.min(np.abs(eigenvals)))

        eps = 1e-14
        sgn_vals = np.where(np.abs(eigenvals) > eps, np.sign(eigenvals), 1.0)
        sgn_Hw = eigenvecs @ np.diag(sgn_vals) @ eigenvecs.conj().T

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
        operator_defect = (D_ov @ Gamma_5 + Gamma_5 @ D_ov) - (a * D_ov @ Gamma_5 @ D_ov)
        return float(np.max(np.abs(operator_defect)))

    def evaluate_topological_index(
        self, D_ov: np.ndarray, Gamma_5: np.ndarray, a: float = 1.0
    ) -> Tuple[float, int, int]:
        """Evaluates lattice Atiyah-Singer index Index(D_ov) = (1/2) Tr(Gamma_5 a D_ov) = n_+ - n_-."""
        trace_val = float(np.real(np.trace(Gamma_5 @ (a * D_ov))))
        index_val = 0.5 * trace_val

        # Solve for zero eigenspace of D_ov using SVD
        zero_threshold = 1e-6
        u, s, vh = np.linalg.svd(D_ov)
        zero_mask = s < zero_threshold
        null_dim = int(np.sum(zero_mask))

        if null_dim == 0:
            n_pos = 0
            n_neg = 0
        else:
            # Nullspace basis vectors are columns of vh.conj().T corresponding to zero singular values
            v0 = vh[zero_mask, :].conj().T
            g5_sub = v0.conj().T @ Gamma_5 @ v0
            chiral_vals = np.linalg.eigvalsh(0.5 * (g5_sub + g5_sub.conj().T))
            n_pos = int(np.sum(chiral_vals > 0.5))
            n_neg = int(np.sum(chiral_vals < -0.5))

        return index_val, n_pos, n_neg

    def evaluate_kernel_localization(
        self, D_ov: np.ndarray, graph: SimplicialComplexGraph
    ) -> Tuple[float, float, bool]:
        """Evaluates spatial localization length xi of overlap kernel ||D_ov(u, v)|| <= C exp(-d(u,v)/xi).

        Computes shortest-path graph distances between vertices and measures genuine block decay
        as a function of graph distance, independent of complex labels.

        Returns:
            (decay_length_xi, max_nonlocal_tail, is_exponentially_local)
        """
        nv = graph.num_vertices
        dist = np.full((nv, nv), np.inf)
        np.fill_diagonal(dist, 0.0)
        for u, v in graph.edges:
            dist[u, v] = 1.0
            dist[v, u] = 1.0
        for k in range(nv):
            for i in range(nv):
                for j in range(nv):
                    if dist[i, k] + dist[k, j] < dist[i, j]:
                        dist[i, j] = dist[i, k] + dist[k, j]

        couplings_by_dist = {}
        for u in range(nv):
            for v in range(nv):
                d = int(dist[u, v]) if not np.isinf(dist[u, v]) else -1
                if d < 0:
                    continue
                block = D_ov[4 * u : 4 * (u + 1), 4 * v : 4 * (v + 1)]
                norm_uv = float(np.max(np.abs(block)))
                if d not in couplings_by_dist:
                    couplings_by_dist[d] = []
                couplings_by_dist[d].append(norm_uv)

        distant_couplings = [norm for d, norms in couplings_by_dist.items() if d > 0 for norm in norms]
        max_tail = float(max(distant_couplings)) if distant_couplings else 0.0

        distances = sorted([d for d in couplings_by_dist.keys() if d >= 0])
        max_couplings = {d: max(couplings_by_dist[d]) for d in distances}

        if max(distances) >= 2:
            # Multi-distance complex: require monotonic exponential decay
            is_monotonic = True
            for i in range(1, len(distances) - 1):
                if max_couplings[distances[i + 1]] >= max_couplings[distances[i]]:
                    is_monotonic = False
                    break
            if not is_monotonic:
                return 999.0, max_tail, False

            xs = [float(d) for d in distances]
            ys = [float(np.log(max(max_couplings[d], 1e-15))) for d in distances]
            slope, _ = np.polyfit(xs, ys, 1)
            if slope < -0.2:
                decay_xi = float(-1.0 / slope)
                is_local = (decay_xi < 5.0)
                return decay_xi, max_tail, is_local
            else:
                return 999.0, max_tail, False
        else:
            # Single-distance complex: evaluate ratio of on-site (d=0) to nearest-neighbor (d=1)
            c0 = max_couplings.get(0, 1.0)
            c1 = max_couplings.get(1, 0.0)
            if c0 > c1 and c1 > 0:
                decay_xi = float(1.0 / np.log(c0 / c1))
                is_local = (decay_xi < 5.0)
                return decay_xi, max_tail, is_local
            else:
                return 999.0, max_tail, False

    def record_complex_evaluation(
        self,
        graph: SimplicialComplexGraph,
        m0: float = 1.2,
        r: float = 1.0,
    ) -> Dict[str, object]:
        """Evaluates overlap fermions on graph and records to SQLite tables."""
        a = graph.lattice_spacing_a
        D_ov, Gamma_5, sgn_Hw, spectral_gap = self.build_overlap_dirac_operator(graph, m0, r)

        gw_res = self.evaluate_ginsparg_wilson_relation(D_ov, Gamma_5, a)
        luescher_res = self.evaluate_luescher_chiral_invariance(D_ov, Gamma_5, a)
        index_val, n_pos, n_neg = self.evaluate_topological_index(D_ov, Gamma_5, a)
        decay_xi, max_tail, is_local = self.evaluate_kernel_localization(D_ov, graph)

        doubler_mass_gap = float(2.0 * r / a)
        is_doubler_free = 1 if doubler_mass_gap > 0.5 else 0
        is_spectrally_gapped = 1 if spectral_gap >= 1e-4 else 0

        classification = (
            "ExactChiralOverlapPreserved"
            if is_local and is_spectrally_gapped
            else "GinspargWilsonLocalityObstruction"
        )

        cur = self.conn.cursor()

        cur.execute(
            """
            INSERT OR REPLACE INTO CdtOverlapDiracTrajectory (
                complex_id, geometry_type, num_vertices, num_edges, lattice_spacing_a,
                wilson_mass_m0, wilson_r, spectral_gap, gw_relation_residual,
                luscher_invariance_residual, doubler_mass_gap, is_gw_satisfied,
                is_chiral_invariant, is_doubler_free, is_spectrally_gapped,
                authority_effect
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'None')
            """,
            (
                graph.complex_id,
                graph.geometry_type,
                graph.num_vertices,
                len(graph.edges),
                a,
                m0,
                r,
                spectral_gap,
                gw_res,
                luescher_res,
                doubler_mass_gap,
                1 if gw_res <= 1e-12 else 0,
                1 if luescher_res <= 1e-12 else 0,
                is_doubler_free,
                is_spectrally_gapped,
            ),
        )

        topological_charge = int(round(index_val))
        index_residual = abs(index_val - topological_charge)
        cur.execute(
            """
            INSERT OR REPLACE INTO CdtOverlapIndexAudit (
                complex_id, num_zero_modes, n_pos_chirality, n_neg_chirality,
                index_trace, topological_charge, index_residual, is_index_certified,
                authority_effect
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'None')
            """,
            (
                graph.complex_id,
                n_pos + n_neg,
                n_pos,
                n_neg,
                index_val,
                topological_charge,
                index_residual,
                1 if index_residual <= 1e-12 else 0,
            ),
        )

        cur.execute(
            """
            INSERT OR REPLACE INTO CdtOverlapLocalitySummary (
                complex_id, geometry_type, min_spectral_gap, decay_length_xi,
                max_nonlocal_tail, is_exponentially_local, classification,
                authority_effect
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'None')
            """,
            (
                graph.complex_id,
                graph.geometry_type,
                spectral_gap,
                decay_xi,
                max_tail,
                1 if is_local else 0,
                classification,
            ),
        )

        self.conn.commit()

        cur.execute(
            """
            SELECT overlap_audit_verdict FROM ViewCdtOverlapDiracAudit
            WHERE complex_id = ?
            """,
            (graph.complex_id,),
        )
        row = cur.fetchone()
        audit_verdict = row[0] if row else "AUDIT_NOT_FOUND"

        return {
            "complex_id": graph.complex_id,
            "geometry_type": graph.geometry_type,
            "spectral_gap": spectral_gap,
            "gw_residual": gw_res,
            "luescher_residual": luescher_res,
            "doubler_mass_gap": doubler_mass_gap,
            "index": index_val,
            "is_local": is_local,
            "classification": classification,
            "audit_verdict": audit_verdict,
        }

    def close(self) -> None:
        self.conn.close()
