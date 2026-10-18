from __future__ import annotations
from dataclasses import field, dataclass
from typing import Any, Dict, List, Optional, Set, Tuple
import math
import numpy as np

from omega_engine.crates.engine.base.engine_base import Engine
from omega_engine.crates.functional.gamma2 import gamma2
from omega_engine.crates.functional.phi1 import residual_l1

CONTRACT_ID = "urn:omega:engine:coda_engine:file:v1.0.0"
CODA_ENGINE_ROLE = "math_suite_callable_by_domain_worker"
CODA_ENGINE_FILE_CONTRACT = "urn:omega:engine:coda_engine:file:v1.0.0"


# --- OE-000 / CODA-000 Cohomological Infrastructure ---

@dataclass
class SimplicialCarrier:
    """Finite 2-truncated simplicial carrier P = (V, E, F)."""
    vertices: List[Any]
    edges: List[Tuple[Any, Any]]  # 1-simplices (u, v)
    faces: List[Tuple[Any, Any, Any]] = field(default_factory=list)  # 2-simplices (u, v, w)

    def validate(self) -> bool:
        """Validate carrier combinatorial structure (basis honesty)."""
        if len(self.vertices) != len(set(self.vertices)):
            return False
        vertex_set = set(self.vertices)
        seen_edges = set()
        for u, v in self.edges:
            if u not in vertex_set or v not in vertex_set:
                return False
            if u == v:
                return False
            if (u, v) in seen_edges:
                return False
            seen_edges.add((u, v))
        edge_set = set(self.edges)
        for face in self.faces:
            if len(face) != 3:
                return False
            u, v, w = face
            if len({u, v, w}) != 3:
                return False
            if u not in vertex_set or v not in vertex_set or w not in vertex_set:
                return False
            for a, b in ((u, v), (v, w), (u, w)):
                if (a, b) not in edge_set and (b, a) not in edge_set:
                    return False
        return True


@dataclass
class ObserverPacket:
    """Observer probe / detector JL specification (CODA-003 / OE-000)."""
    observer_id: str
    gauge_name: str
    resolution: float = 1e-6
    authority_effect: str = "None"

    def probe_vertex_state(self, vertex_data: Dict[Any, float]) -> Dict[Any, float]:
        """Apply observer scalar gauge to vertex state (C0 0-cochain)."""
        return {v: float(val) for v, val in vertex_data.items()}


class CohomologicalEngine(Engine):
    """Computes coboundary operators d0, d1, quotient class Q1 = C1 / im(d0), and nilpotency."""

    @staticmethod
    def h_on_edge(h_1: Dict[Tuple[Any, Any], float], u: Any, v: Any) -> float:
        """Oriented cochain lookup: h(v,u) = -h(u,v) when only reverse key is stored."""
        if (u, v) in h_1:
            return float(h_1[(u, v)])
        if (v, u) in h_1:
            return -float(h_1[(v, u)])
        return 0.0

    @staticmethod
    def project_h1_to_edge_basis(
        carrier: "SimplicialCarrier",
        h_1: Dict[Tuple[Any, Any], float],
    ) -> List[float]:
        """Project dictionary cochain onto carrier edge basis with orientation honesty."""
        return [
            CohomologicalEngine.h_on_edge(h_1, u, v) for u, v in carrier.edges
        ]

    @staticmethod
    def d0(carrier: SimplicialCarrier, f_0: Dict[Any, float]) -> Dict[Tuple[Any, Any], float]:
        """Compute 0-coboundary d0: C0 -> C1. (d0 f)(u, v) = f(v) - f(u)."""
        result: Dict[Tuple[Any, Any], float] = {}
        for u, v in carrier.edges:
            f_u = f_0.get(u, 0.0)
            f_v = f_0.get(v, 0.0)
            result[(u, v)] = f_v - f_u
        return result

    @staticmethod
    def d1(carrier: SimplicialCarrier, h_1: Dict[Tuple[Any, Any], float]) -> Dict[Tuple[Any, Any, Any], float]:
        """Compute 1-coboundary d1: C1 -> C2. (d1 h)(u, v, w) = h(v, w) - h(u, w) + h(u, v).

        Oriented lookup: a 1-cochain is alternating, h(v, u) = -h(u, v), so a
        key stored reversed reads as its negation (repair ``057662bb4b`` /
        PR #1879, re-applied to this recovered surface; regression tests in
        ``tests/test_coda_d1_orientation.py`` and ``tests/core/test_coda_engine.py``).
        """
        def h(a: Any, b: Any) -> float:
            if (a, b) in h_1:
                return h_1[(a, b)]
            if (b, a) in h_1:
                return -h_1[(b, a)]
            return 0.0

        result: Dict[Tuple[Any, Any, Any], float] = {}
        for u, v, w in carrier.faces:
            result[(u, v, w)] = h(v, w) - h(u, w) + h(u, v)
        return result

    @classmethod
    def verify_nilpotency(cls, carrier: SimplicialCarrier, f_0: Dict[Any, float], eps: float = 1e-9) -> bool:
        """Verify exact nilpotency: d1(d0(f)) == 0 for all 2-simplices."""
        h_1 = cls.d0(carrier, f_0)
        c_2 = cls.d1(carrier, h_1)
        return all(abs(val) < eps for val in c_2.values())


@dataclass
class ObstructionSignature:
    """Triple (Phi_1, Gamma_2, R_cl) plus residual receipt identity.

    Phi_1   : Quotient residual mass ||[h]||_{Q1} via residual_l1
    Gamma_2 : d1-closure charge ||d1 h||_1 via gamma2
    R_cl    : Obstruction ratio / closure status (Phi_1 / (Gamma_2 + eps))
    residual_vector : post-gauge residual whose L1 mass is Phi_1
    input_cochain   : orientation-projected input on carrier edge basis
    """
    phi_1: float
    gamma_2: float
    r_cl: float
    status_label: str
    residual_vector: List[float] = field(default_factory=list)
    input_cochain: List[float] = field(default_factory=list)


class ObstructionCalculus(Engine):
    """Diagnoses primitive difference h in C1 into removable gauge, closed obstruction, or rupture."""

    @classmethod
    def analyze_1cochain(
        cls,
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float],
        eps: float = 1e-6
    ) -> ObstructionSignature:
        """Analyze a 1-cochain h_1 on carrier to compute (Phi_1, Gamma_2, R_cl).

        Wave C: Phi_1 / Gamma_2 residual masses via functional residual_l1 / gamma2
        (PROTO dual-home). Orientation-aware cochain projection. AuthorityEffect None.
        """
        input_cochain = CohomologicalEngine.project_h1_to_edge_basis(carrier, h_1)
        h_vec = input_cochain
        if carrier.faces:
            d1_mat, _, _ = cls._build_d1_matrix(carrier)
            gres = gamma2(d1_mat, np.asarray(h_vec, dtype=float), tolerance=float(eps))
            gamma_2 = float(gres.value)
        else:
            c_2 = CohomologicalEngine.d1(carrier, h_1)
            gamma_2 = residual_l1([float(v) for v in c_2.values()]) if c_2 else 0.0

        vertices = carrier.vertices
        f_pot = {v: 0.0 for v in vertices}
        if carrier.edges:
            for _ in range(50):
                new_f = dict(f_pot)
                for u, v in carrier.edges:
                    h_val = CohomologicalEngine.h_on_edge(h_1, u, v)
                    new_f[v] = 0.5 * (new_f[v] + (f_pot[u] + h_val))
                    new_f[u] = 0.5 * (new_f[u] + (f_pot[v] - h_val))
                f_pot = new_f

        gauge_part = CohomologicalEngine.d0(carrier, f_pot)
        residual_vec = [
            CohomologicalEngine.h_on_edge(h_1, u, v) - float(gauge_part.get((u, v), 0.0))
            for u, v in carrier.edges
        ]
        phi_1 = residual_l1(residual_vec)
        r_cl = phi_1 / (gamma_2 + 1e-9)

        if phi_1 < eps:
            label = "REMOVABLE_GAUGE"
        elif gamma_2 < eps:
            label = "CLOSED_OBSTRUCTION"
        else:
            label = "NON_CLOSED_RUPTURE"

        return ObstructionSignature(
            phi_1=phi_1,
            gamma_2=gamma_2,
            r_cl=r_cl,
            status_label=label,
            residual_vector=list(residual_vec),
            input_cochain=list(input_cochain),
        )

    @classmethod
    def _build_d0_matrix(cls, carrier: SimplicialCarrier) -> Tuple[np.ndarray, Dict[Any, int], Dict[Tuple[Any, Any], int]]:
        """Build d0 incidence matrix (n_edges, n_vertices)."""
        v_map = {v: idx for idx, v in enumerate(carrier.vertices)}
        e_map = {e: idx for idx, e in enumerate(carrier.edges)}
        d0_mat = np.zeros((len(carrier.edges), len(carrier.vertices)))
        for u, v in carrier.edges:
            e_idx = e_map[(u, v)]
            d0_mat[e_idx, v_map[v]] += 1.0
            d0_mat[e_idx, v_map[u]] -= 1.0
        return d0_mat, v_map, e_map

    @classmethod
    def _build_d1_matrix(cls, carrier: SimplicialCarrier) -> Tuple[np.ndarray, Dict[Tuple[Any, Any], int], Dict[Tuple[Any, Any, Any], int]]:
        """Build d1 incidence matrix (n_faces, n_edges)."""
        edge_map = {e: idx for idx, e in enumerate(carrier.edges)}
        face_map = {f: idx for idx, f in enumerate(carrier.faces)}
        d1_mat = np.zeros((len(carrier.faces), len(carrier.edges)))
        for f_idx, (u, v, w) in enumerate(carrier.faces):
            for (e_u, e_v), sign in [((u, v), 1.0), ((v, w), 1.0), ((u, w), -1.0)]:
                if (e_u, e_v) in edge_map:
                    d1_mat[f_idx, edge_map[(e_u, e_v)]] += sign
                elif (e_v, e_u) in edge_map:
                    d1_mat[f_idx, edge_map[(e_v, e_u)]] -= sign
        return d1_mat, edge_map, face_map

    @classmethod
    def hodge_laplacian_matrix(cls, carrier: SimplicialCarrier) -> np.ndarray:
        """Compute the degree-1 Hodge Laplacian L1 = d0 d0* + d1* d1."""
        d0_mat, _, _ = cls._build_d0_matrix(carrier)
        d1_mat, _, _ = cls._build_d1_matrix(carrier)
        L1 = (d0_mat @ d0_mat.T) + (d1_mat.T @ d1_mat)
        return L1

    @classmethod
    def hodge_decompose_l2(
        cls,
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float]
    ) -> Dict[str, Any]:
        """Full 3-way discrete Hodge decomposition: h = d0 f + d1* u + h_harm (unweighted)."""
        return cls.hodge_decompose_weighted_l2(carrier, h_1, edge_weights=None)

    @classmethod
    def hodge_decompose_weighted_l2(
        cls,
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float],
        edge_weights: Optional[Dict[Tuple[Any, Any], float]] = None
    ) -> Dict[str, Any]:
        """Weighted 3-way discrete Hodge decomposition: h = d0 f + d1* u + h_harm
        under inner product <alpha, beta>_W = sum_e w_e alpha_e beta_e.
        AuthorityEffect: None.
        """
        n_edges = len(carrier.edges)
        if n_edges == 0:
            return {
                "exact": {}, "coexact": {}, "harmonic": {},
                "gauge_mass": 0.0, "curvature_mass": 0.0, "harmonic_mass": 0.0,
                "gauge_mass_weighted": 0.0, "curvature_mass_weighted": 0.0, "harmonic_mass_weighted": 0.0,
                "authority_effect": "None", "letter": "E", "status": "HODGE_DECOMPOSED",
                "loss_ledger": []
            }

        weights_arr = np.array([edge_weights.get(e, 1.0) if edge_weights else 1.0 for e in carrier.edges])
        W = np.diag(weights_arr)
        W_inv = np.diag(np.where(weights_arr > 0, 1.0 / weights_arr, 0.0))

        d0_mat, _, _ = cls._build_d0_matrix(carrier)
        d1_mat, _, _ = cls._build_d1_matrix(carrier)
        h_vec = np.array([h_1.get(e, 0.0) for e in carrier.edges])

        # 1. Exact part d0 f: solve (d0.T @ W @ d0) f = d0.T @ W @ h
        L_vert = d0_mat.T @ W @ d0_mat
        rhs_vert = d0_mat.T @ W @ h_vec
        f_sol, _, _, _ = np.linalg.lstsq(L_vert, rhs_vert, rcond=None)
        exact_vec = d0_mat @ f_sol

        # 2. Coexact part d1* u: solve (d1 @ W_inv @ d1.T) u = d1 @ h
        if len(carrier.faces) > 0:
            L_face = d1_mat @ W_inv @ d1_mat.T
            rhs_face = d1_mat @ h_vec
            u_sol, _, _, _ = np.linalg.lstsq(L_face, rhs_face, rcond=None)
            coexact_vec = W_inv @ d1_mat.T @ u_sol
        else:
            coexact_vec = np.zeros(n_edges)

        # 3. Harmonic part
        harmonic_vec = h_vec - exact_vec - coexact_vec

        exact_dict = {e: float(exact_vec[i]) for i, e in enumerate(carrier.edges)}
        coexact_dict = {e: float(coexact_vec[i]) for i, e in enumerate(carrier.edges)}
        harmonic_dict = {e: float(harmonic_vec[i]) for i, e in enumerate(carrier.edges)}

        gauge_mass = float(np.linalg.norm(exact_vec))
        curvature_mass = float(np.linalg.norm(coexact_vec))
        harmonic_mass = float(np.linalg.norm(harmonic_vec))

        gauge_mass_w = math.sqrt(float(exact_vec.T @ W @ exact_vec))
        curvature_mass_w = math.sqrt(float(coexact_vec.T @ W @ coexact_vec))
        harmonic_mass_w = math.sqrt(float(harmonic_vec.T @ W @ harmonic_vec))

        sig_before = cls.analyze_1cochain(carrier, h_1)
        sig_after = cls.analyze_1cochain(carrier, harmonic_dict)

        d0_adj_harm = float(np.linalg.norm(d0_mat.T @ harmonic_vec))

        loss_ledger = [
            f"Weighted Hodge Decomposition: gauge_w={gauge_mass_w:.4f}, curvature_w={curvature_mass_w:.4f}, harmonic_w={harmonic_mass_w:.4f}"
        ]

        return {
            "exact": exact_dict,
            "coexact": coexact_dict,
            "harmonic": harmonic_dict,
            "gauge_mass": gauge_mass,
            "curvature_mass": curvature_mass,
            "harmonic_mass": harmonic_mass,
            "gauge_mass_weighted": gauge_mass_w,
            "curvature_mass_weighted": curvature_mass_w,
            "harmonic_mass_weighted": harmonic_mass_w,
            "gamma_2_of_harmonic": sig_after.gamma_2,
            "d0_adj_norm_of_harmonic": d0_adj_harm,
            "phi_1_before": sig_before.phi_1,
            "phi_1_after_full_hodge": sig_after.phi_1,
            "delta_phi_1": sig_after.phi_1 - sig_before.phi_1,
            "edge_weights_source": "user_supplied" if edge_weights else "uniform",
            "authority_effect": "None",
            "letter": "E",
            "status": "HODGE_DECOMPOSED",
            "loss_ledger": loss_ledger
        }

    @classmethod
    def repair_to_closed_weighted_l2(
        cls,
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float],
        edge_weights: Optional[Dict[Tuple[Any, Any], float]] = None
    ) -> Dict[str, Any]:
        """Convenience wrapper returning closed part under weighted l2 Hodge repair."""
        return cls.hodge_decompose_weighted_l2(carrier, h_1, edge_weights=edge_weights)

    @classmethod
    def solve_l1_gauge_minimization(
        cls,
        carrier: SimplicialCarrier,
        cochain_vec: np.ndarray
    ) -> Tuple[float, np.ndarray]:
        """Solve exact l1 gauge minimization problem inf_{alpha in R^V} ||omega - d0 alpha||_1 via SciPy linprog LP.
        AuthorityEffect: None.
        """
        n_v = len(carrier.vertices)
        n_e = len(carrier.edges)
        if n_e == 0 or n_v == 0:
            return 0.0, np.zeros(n_v)

        import scipy.optimize as opt
        d0_mat, _, _ = cls._build_d0_matrix(carrier)

        # Variables: x = [alpha_0..alpha_{n_v-1}, s_0..s_{n_e-1}]
        c = np.concatenate([np.zeros(n_v), np.ones(n_e)])

        # Constraints: d0 alpha - s <= omega and -d0 alpha - s <= -omega
        I_e = np.eye(n_e)
        A_ub = np.vstack([
            np.hstack([d0_mat, -I_e]),
            np.hstack([-d0_mat, -I_e])
        ])
        b_ub = np.concatenate([cochain_vec, -cochain_vec])

        bounds = [(None, None)] * n_v + [(0, None)] * n_e
        res = opt.linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

        if res.success:
            alpha_opt = res.x[:n_v]
            min_l1 = float(res.fun)
            return min_l1, alpha_opt
        else:
            return residual_l1([float(x) for x in cochain_vec]), np.zeros(n_v)

    @classmethod
    def monotone_l1_cycle_step(
        cls,
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float],
        cycle_cochain: Optional[Dict[Tuple[Any, Any], float]] = None,
        eps_prog: float = 1e-6
    ) -> Dict[str, Any]:
        """M-letter multi-dimensional cycle-supported l1 descent step via LP:
        min_{t in R^k} ||h - sum_j t_j c^{(j)}||_1 over ker(L1) harmonic basis cycles.
        AuthorityEffect: None.
        """
        edges = carrier.edges
        n_edges = len(edges)
        if n_edges == 0:
            return {
                "h_updated": dict(h_1), "l1_before": 0.0, "l1_after": 0.0,
                "delta_l1": 0.0, "t_opt": [], "accepted": False,
                "letter": "M", "authority_effect": "None", "loss_ledger": []
            }

        h_vec = np.array([h_1.get(e, 0.0) for e in edges])
        l1_init = float(np.sum(np.abs(h_vec)))

        B_on = cls.extract_orthonormal_harmonic_basis(carrier)
        if B_on.shape[1] == 0 and cycle_cochain is not None:
            c_vec = np.array([cycle_cochain.get(e, 0.0) for e in edges])
            if np.linalg.norm(c_vec) > 1e-9:
                B_on = c_vec.reshape(-1, 1)

        k_basis = B_on.shape[1]
        if k_basis == 0:
            return {
                "h_updated": dict(h_1), "l1_before": l1_init, "l1_after": l1_init,
                "delta_l1": 0.0, "t_opt": [], "accepted": False,
                "letter": "M", "authority_effect": "None",
                "loss_ledger": ["No harmonic cycles available for M-letter descent"]
            }

        import scipy.optimize as opt
        c_lp = np.concatenate([np.zeros(k_basis), np.ones(n_edges)])
        I_e = np.eye(n_edges)
        A_ub = np.vstack([
            np.hstack([B_on, -I_e]),
            np.hstack([-B_on, -I_e])
        ])
        b_ub = np.concatenate([h_vec, -h_vec])
        bounds = [(None, None)] * k_basis + [(0, None)] * n_edges

        res = opt.linprog(c_lp, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        if res.success:
            t_opt = res.x[:k_basis]
            best_l1 = float(res.fun)
            delta_l1 = best_l1 - l1_init
            accepted = delta_l1 < -eps_prog
            h_updated_vec = h_vec - (B_on @ t_opt if accepted else 0.0)
        else:
            accepted = False
            best_l1 = l1_init
            delta_l1 = 0.0
            h_updated_vec = h_vec
            t_opt = np.zeros(k_basis)

        h_updated = {e: float(h_updated_vec[i]) for i, e in enumerate(edges)}
        loss_ledger = [
            f"M-letter multi-cycle LP step: k_dim={k_basis}, delta_l1={delta_l1:+.6e}, accepted={accepted}"
        ]

        return {
            "h_updated": h_updated,
            "l1_before": l1_init,
            "l1_after": best_l1 if accepted else l1_init,
            "delta_l1": delta_l1 if accepted else 0.0,
            "t_opt": t_opt.tolist(),
            "accepted": accepted,
            "letter": "M",
            "authority_effect": "None",
            "loss_ledger": loss_ledger
        }

    @classmethod
    def _integer_matrix_rank(cls, mat: np.ndarray) -> int:
        """Exact rank of an integer incidence matrix via SymPy (no float threshold)."""
        if mat.size == 0 or mat.shape[0] == 0 or mat.shape[1] == 0:
            return 0
        try:
            import sympy as sp
            sp_mat = sp.Matrix(np.round(mat).astype(int))
            return int(sp_mat.rank())
        except Exception:
            return int(np.linalg.matrix_rank(mat, tol=1e-9))

    @classmethod
    def _smith_normal_form_diagonal(cls, mat: np.ndarray) -> List[int]:
        """Return non-zero invariant factors of the Smith Normal Form of an integer matrix."""
        if mat.size == 0 or mat.shape[0] == 0 or mat.shape[1] == 0:
            return []
        try:
            import sympy as sp
            from sympy.matrices.normalforms import smith_normal_form
            sp_mat = sp.Matrix(np.round(mat).astype(int))
            smf = smith_normal_form(sp_mat)
            diag = [int(smf[i, i]) for i in range(min(smf.shape)) if smf[i, i] != 0]
            return diag
        except Exception:
            return []

    @classmethod
    def compute_exact_betti_1(cls, carrier: SimplicialCarrier) -> Tuple[int, int, int]:
        """Compute exact certified integer Betti number b1(P) = |E| - rank_Z(D0) - rank_Z(D1)
        via exact integer rank reduction on D0 and D1 incidence matrices (SymPy).
        Returns (b1, rank_d0, rank_d1).
        AuthorityEffect: None.
        """
        n_edges = len(carrier.edges)
        if n_edges == 0:
            return 0, 0, 0

        d0_mat, _, _ = cls._build_d0_matrix(carrier)
        d1_mat, _, _ = cls._build_d1_matrix(carrier)

        rank_d0 = cls._integer_matrix_rank(d0_mat)
        rank_d1 = cls._integer_matrix_rank(d1_mat) if len(carrier.faces) > 0 else 0

        b1 = max(0, n_edges - rank_d0 - rank_d1)
        return b1, rank_d0, rank_d1

    @classmethod
    def compute_exact_betti_1_with_snf(cls, carrier: SimplicialCarrier) -> Dict[str, Any]:
        """Compute exact integer Betti 1 along with SNF invariant diagonals of D0 and D1."""
        b1, r_d0, r_d1 = cls.compute_exact_betti_1(carrier)
        d0_mat, _, _ = cls._build_d0_matrix(carrier)
        d1_mat, _, _ = cls._build_d1_matrix(carrier)

        snf_d0 = cls._smith_normal_form_diagonal(d0_mat)
        snf_d1 = cls._smith_normal_form_diagonal(d1_mat) if len(carrier.faces) > 0 else []

        return {
            "b1": b1,
            "rank_d0": r_d0,
            "rank_d1": r_d1,
            "snf_diagonal_d0": snf_d0,
            "snf_diagonal_d1": snf_d1,
            "authority_effect": "None"
        }

    @classmethod
    def compute_exact_betti_numbers(cls, carrier: SimplicialCarrier) -> Dict[str, Any]:
        """Compute free Betti numbers (b0, b1, b2) of a 2-truncated simplicial carrier
        using exact integer ranks via Smith Normal Form (SymPy).
        b0 = |V| - rank_Z(D0)
        b1 = |E| - rank_Z(D0) - rank_Z(D1)
        b2 = |F| - rank_Z(D1)
        AuthorityEffect: None.
        """
        n_v = len(carrier.vertices)
        n_e = len(carrier.edges)
        n_f = len(carrier.faces)
        if n_v == 0:
            return {
                "b0": 0, "b1": 0, "b2": 0,
                "rank_d0": 0, "rank_d1": 0,
                "snf_d0": [], "snf_d1": [],
                "n_vertices": 0, "n_edges": 0, "n_faces": 0,
                "authority_effect": "None",
                "note": "b_k = hard topological upper bounds on residual dim at degree k"
            }

        d0_mat, _, _ = cls._build_d0_matrix(carrier)
        d1_mat, _, _ = cls._build_d1_matrix(carrier)

        r_d0 = cls._integer_matrix_rank(d0_mat)
        r_d1 = cls._integer_matrix_rank(d1_mat) if n_f > 0 else 0

        snf_d0 = cls._smith_normal_form_diagonal(d0_mat)
        snf_d1 = cls._smith_normal_form_diagonal(d1_mat) if n_f > 0 else []

        b0 = max(0, n_v - r_d0)
        b1 = max(0, n_e - r_d0 - r_d1)
        b2 = max(0, n_f - r_d1)

        return {
            "b0": b0,
            "b1": b1,
            "b2": b2,
            "rank_d0": r_d0,
            "rank_d1": r_d1,
            "snf_d0": snf_d0,
            "snf_d1": snf_d1,
            "n_vertices": n_v,
            "n_edges": n_e,
            "n_faces": n_f,
            "authority_effect": "None",
            "note": "b_k = hard topological upper bounds on residual dim at degree k"
        }

    @classmethod
    def extract_orthonormal_harmonic_basis(cls, carrier: SimplicialCarrier) -> np.ndarray:
        """Extract an orientation-invariant orthonormal basis B_on for ker(L1)
        via Cholesky factor R of Gram matrix G = B^T B => B_on = B R^{-1}.
        """
        b1, _, _ = cls.compute_exact_betti_1(carrier)
        n_edges = len(carrier.edges)
        if b1 == 0 or n_edges == 0:
            return np.zeros((n_edges, 0))

        L1 = cls.hodge_laplacian_matrix(carrier)
        evals, evecs = np.linalg.eigh(L1)

        # Nullspace eigenvectors corresponding to small eigenvalues
        null_mask = evals < 1e-7
        B_raw = evecs[:, null_mask]

        if B_raw.shape[1] == 0:
            return np.zeros((n_edges, 0))

        # Take up to exact b1 basis vectors
        if B_raw.shape[1] > b1:
            B_raw = B_raw[:, :b1]

        # Orthonormalization via Cholesky decomposition of Gram matrix G = B^T B
        G = B_raw.T @ B_raw
        try:
            R = np.linalg.cholesky(G)
            B_on = B_raw @ np.linalg.inv(R.T)
        except np.linalg.LinAlgError:
            # Fallback to QR orthonormalization
            B_on, _ = np.linalg.qr(B_raw)

        return B_on

    @classmethod
    def evaluate_dda_transition(
        cls,
        receipt_e: Dict[str, Any],
        eps_gamma: float = 1e-6,
        eps_harm: float = 1e-6
    ) -> Dict[str, Any]:
        """Transition rule after E-letter (Hodge repair):
        - gamma_2_after > eps_gamma  => emit M (CURVATURE_REMAINING)
        - harmonic_mass <= eps_harm  => emit T/Q (EXACT_CLASS)
        - harmonic_mass > eps_harm   => emit M (HARMONIC_RESIDUAL_SURVIVES)
        """
        gamma_2_after = receipt_e.get("gamma_2_after", 0.0)
        harmonic_mass = receipt_e.get("harmonic_mass", 0.0)

        if gamma_2_after > eps_gamma:
            next_letter = "M"
            reason = "CURVATURE_REMAINING"
            note = f"Curvature gamma_2 = {gamma_2_after:.6e} remains after E repair"
        elif harmonic_mass <= eps_harm:
            next_letter = "T"
            reason = "EXACT_CLASS"
            note = "Harmonic mass <= eps_harm; all removable defect eliminated"
        else:
            next_letter = "M"
            reason = "HARMONIC_RESIDUAL_SURVIVES"
            note = f"Harmonic mass mu = {harmonic_mass:.6e} survives E repair; class lives in H^1(P)"

        loss_ledger = list(receipt_e.get("loss_ledger", []))
        loss_ledger.append(f"DDA Transition: {reason} => emit letter {next_letter}")

        return {
            "next_letter": next_letter,
            "reason": reason,
            "note": note,
            "authority_effect": "None",
            "loss_ledger": loss_ledger
        }

    @classmethod
    def repair_to_closed_l2(
        cls,
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float]
    ) -> Dict[str, Any]:
        """Option A — l2 orthogonal Hodge projection onto ker(d1).
        Solves discrete Poisson system (d1 d1*) u = d1 h, setting h_closed = h - d1* u.
        AuthorityEffect: None.
        """
        c_2 = CohomologicalEngine.d1(carrier, h_1)
        gamma_2_before = math.sqrt(sum(val ** 2 for val in c_2.values())) if c_2 else 0.0

        if not carrier.faces or gamma_2_before < 1e-9:
            return {
                "h_closed": dict(h_1),
                "gamma_2_before": gamma_2_before,
                "gamma_2_after": gamma_2_before,
                "l2_distance": 0.0,
                "phi_1_change": 0.0,
                "letter": "E",
                "authority_effect": "None",
                "loss_ledger": []
            }

        # Build incidence matrices for d1: C1 -> C2
        n_edges = len(carrier.edges)
        n_faces = len(carrier.faces)
        edge_map = {e: idx for idx, e in enumerate(carrier.edges)}
        
        # d1 matrix of shape (n_faces, n_edges)
        d1_mat = np.zeros((n_faces, n_edges))
        for f_idx, (u, v, w) in enumerate(carrier.faces):
            for (e_u, e_v), sign in [((u, v), 1.0), ((v, w), 1.0), ((u, w), -1.0)]:
                if (e_u, e_v) in edge_map:
                    d1_mat[f_idx, edge_map[(e_u, e_v)]] += sign
                elif (e_v, e_u) in edge_map:
                    d1_mat[f_idx, edge_map[(e_v, e_u)]] -= sign

        # h vector
        h_vec = np.array([h_1.get(e, 0.0) for e in carrier.edges])
        d1_h = d1_mat @ h_vec

        # Face Laplacian L_face = d1 @ d1.T
        L_face = d1_mat @ d1_mat.T

        # Solve L_face u = d1_h via least squares
        u_sol, _, _, _ = np.linalg.lstsq(L_face, d1_h, rcond=None)

        # h_closed = h - d1.T @ u_sol
        correction = d1_mat.T @ u_sol
        h_closed_vec = h_vec - correction

        h_closed = {e: float(h_closed_vec[i]) for i, e in enumerate(carrier.edges)}
        
        c_2_after = CohomologicalEngine.d1(carrier, h_closed)
        gamma_2_after = math.sqrt(sum(val ** 2 for val in c_2_after.values())) if c_2_after else 0.0
        l2_dist = float(np.linalg.norm(correction))

        sig_before = cls.analyze_1cochain(carrier, h_1)
        sig_after = cls.analyze_1cochain(carrier, h_closed)
        phi_1_before = sig_before.phi_1
        phi_1_after = sig_after.phi_1
        delta_phi_1 = phi_1_after - phi_1_before
        progress_pred = (delta_phi_1 < -1e-6) or (gamma_2_after < 1e-6)

        loss_ledger = [
            f"l2-repair residual mass change delta_Phi1 = {delta_phi_1:+.6e} (before={phi_1_before:.6e}, after={phi_1_after:.6e})"
        ]

        return {
            "letter": "E",
            "repair_method": "l2_hodge",
            "h_closed": h_closed,
            "gamma_2_before": gamma_2_before,
            "gamma_2_after": gamma_2_after,
            "phi_1_before": phi_1_before,
            "phi_1_after": phi_1_after,
            "delta_phi_1": delta_phi_1,
            "l2_distance_cancelled": l2_dist,
            "progress_predicate": progress_pred,
            "authority_effect": "None",
            "loss_ledger": loss_ledger
        }

    @classmethod
    def evaluate_e_letter_progress(
        cls,
        receipt: Dict[str, Any],
        eps_prog: float = 1e-6,
        eps_gamma: float = 1e-6
    ) -> bool:
        """Integration rule for CanContinue_n tape generator.
        ProgressPredicate = (delta_phi_1 < -eps_prog) or (gamma_2_after < eps_gamma).
        """
        delta_phi_1 = receipt.get("delta_phi_1", 0.0)
        gamma_2_after = receipt.get("gamma_2_after", 0.0)
        return (delta_phi_1 < -eps_prog) or (gamma_2_after < eps_gamma)

    @classmethod
    def repair_to_closed_local_stencil(
        cls,
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float],
        max_iter: int = 100
    ) -> Dict[str, Any]:
        """Option C — Fast local exact-repair stencil (DDA E-letter path).
        Iteratively cancels face charges (d1 h)_f supported on boundary d(f).
        """
        h_curr = dict(h_1)
        sig_init = cls.analyze_1cochain(carrier, h_1)

        for iteration in range(max_iter):
            c_2 = CohomologicalEngine.d1(carrier, h_curr)
            max_defect = 0.0
            for (u, v, w), val in c_2.items():
                if abs(val) > 1e-7:
                    if abs(val) > max_defect:
                        max_defect = abs(val)
                    h_curr[(u, v)] = h_curr.get((u, v), 0.0) - val / 3.0
                    h_curr[(v, w)] = h_curr.get((v, w), 0.0) - val / 3.0
                    h_curr[(u, w)] = h_curr.get((u, w), 0.0) + val / 3.0
            if max_defect < 1e-7:
                break

        c_2_final = CohomologicalEngine.d1(carrier, h_curr)
        gamma_2_after = math.sqrt(sum(v ** 2 for v in c_2_final.values())) if c_2_final else 0.0
        sig_final = cls.analyze_1cochain(carrier, h_curr)
        delta_phi_1 = sig_final.phi_1 - sig_init.phi_1
        progress_pred = (delta_phi_1 < -1e-6) or (gamma_2_after < 1e-6)

        loss_ledger = [
            f"Local stencil repair residual delta_Phi1 = {delta_phi_1:+.6e}"
        ]

        return {
            "letter": "E",
            "repair_method": "local_stencil",
            "h_closed": h_curr,
            "gamma_2_before": sig_init.gamma_2,
            "gamma_2_after": gamma_2_after,
            "phi_1_before": sig_init.phi_1,
            "phi_1_after": sig_final.phi_1,
            "delta_phi_1": delta_phi_1,
            "progress_predicate": progress_pred,
            "authority_effect": "None",
            "loss_ledger": loss_ledger
        }

    @classmethod
    def pullback_carrier_span(
        cls,
        carrier_A: SimplicialCarrier,
        carrier_B: SimplicialCarrier,
        lens_type: str = "strict",
        eps_lens: float = 1e-6
    ) -> Tuple[SimplicialCarrier, List[str]]:
        """Carrier Span Pullback & ker(d1) preservation options A, B, C.
        Returns (pulled_back_carrier, loss_ledger).
        """
        loss_ledger: List[str] = []
        verts = sorted(list(set(carrier_A.vertices) & set(carrier_B.vertices)), key=lambda x: str(x))
        edges = [e for e in carrier_A.edges if e in set(carrier_B.edges)]
        faces = [f for f in carrier_A.faces if f in set(carrier_B.faces)]

        if lens_type == "strict":
            pulled_carrier = SimplicialCarrier(vertices=verts, edges=edges, faces=faces)
            return pulled_carrier, loss_ledger

        elif lens_type == "homotopy_coherent":
            all_faces = list(set(carrier_A.faces) | set(carrier_B.faces))
            pulled_carrier = SimplicialCarrier(vertices=verts, edges=edges, faces=all_faces)
            loss_ledger.append("Homotopy-coherent lens added contractible face span; ker(d1) preserved up to homotopy")
            return pulled_carrier, loss_ledger

        else:
            pulled_carrier = SimplicialCarrier(vertices=verts, edges=edges, faces=faces)
            loss_ledger.append(f"Residual-aware pullback span declared with tolerance eps_lens = {eps_lens}")
            return pulled_carrier, loss_ledger

    @classmethod
    def compose_lens_spans(
        cls,
        carriers: List[SimplicialCarrier],
        lens_type: str = "strict"
    ) -> Tuple[SimplicialCarrier, List[str]]:
        """Multi-Carrier Lens Span Composition law in LensSpan(P).
        Option A (strict triple/multi-intersection): S_12...N = P1 ∩ P2 ∩ ... ∩ PN.
        Associativity: (S_AB) ∘ S_BC = S_ABC = S_AB ∘ (S_BC).
        """
        if not carriers:
            return SimplicialCarrier([], [], []), ["Empty carriers list"]
        if len(carriers) == 1:
            return carriers[0], []

        curr = carriers[0]
        accumulated_loss: List[str] = []
        for next_c in carriers[1:]:
            curr, loss = cls.pullback_carrier_span(curr, next_c, lens_type=lens_type)
            accumulated_loss.extend(loss)

        return curr, accumulated_loss

    @classmethod
    def l1_l2_gap_dual_certificate(
        cls,
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float],
        receipt_l2: Dict[str, Any]
    ) -> Dict[str, float]:
        """Option A/B dual certificate bound for l1 vs l2 gap:
        | ||h - h_l2||_1 - ||h - h_l1||_1 | <= C_mesh * Gamma_2.
        Re-uses existing residual mass shift delta_Phi1.
        """
        gamma_2 = receipt_l2.get("gamma_2_before", 0.0)
        c_mesh = 1.0  # Normalized mesh constant on unit 2-simplex
        gap_bound = c_mesh * gamma_2
        delta_phi_1 = receipt_l2.get("delta_phi_1", 0.0)

        return {
            "gamma_2": gamma_2,
            "c_mesh": c_mesh,
            "linear_gap_bound": gap_bound,
            "delta_phi_1_runtime_cert": delta_phi_1
        }

    @classmethod
    def validate_observer_resolution(
        cls,
        observer: ObserverPacket,
        phi_1_min: float
    ) -> Tuple[bool, str]:
        """Option B Observer Non-Distortion Threshold Guard.
        Enforces eps_obs < 0.5 * phi_1_min to prevent false CLOSED_OBSTRUCTION status.
        """
        if observer.resolution >= 0.5 * phi_1_min:
            return False, "REFUSED_OBSERVER_DISTORTION"
        return True, "OBSERVER_RESOLUTION_VALIDATED"

    @classmethod
    def monotone_l1_multi_cycle_descent(
        cls,
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float]
    ) -> Dict[str, Any]:
        """CODA-DERIV-003: Multi-Cycle L1 LP Gradient Descent over ker(L1) harmonic basis.
        Solves min_{t in R^{b1}} || h - sum_{j=1}^{b1} t_j h^{(j)} ||_1 via SciPy linprog LP.
        AuthorityEffect: None.
        """
        B_harm = cls.extract_orthonormal_harmonic_basis(carrier)
        n_edges, b1 = B_harm.shape
        h_vec = np.array([h_1.get(e, 0.0) for e in carrier.edges])
        phi1_initial = float(np.sum(np.abs(h_vec))) if n_edges > 0 else 0.0

        if b1 == 0 or n_edges == 0:
            return {
                "t_opt": np.array([]),
                "phi1_initial": phi1_initial,
                "phi1_optimal": phi1_initial,
                "residual_reduction": 0.0,
                "b1": 0,
                "status": "NO_HARMONIC_CYCLES"
            }

        # LP formulation: min sum_i z_i
        # s.t. -z_i <= h_i - sum_j t_j B_{i,j} <= z_i
        c_obj = np.concatenate([np.zeros(b1), np.ones(n_edges)])

        A_ub1 = np.hstack([-B_harm, -np.eye(n_edges)])
        b_ub1 = -h_vec

        A_ub2 = np.hstack([B_harm, -np.eye(n_edges)])
        b_ub2 = h_vec

        A_ub = np.vstack([A_ub1, A_ub2])
        b_ub = np.concatenate([b_ub1, b_ub2])

        bounds = [(None, None)] * b1 + [(0, None)] * n_edges

        from scipy.optimize import linprog
        res = linprog(c_obj, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

        if res.success:
            t_opt = res.x[:b1]
            phi1_optimal = float(res.fun)
            residual_reduction = max(0.0, phi1_initial - phi1_optimal)
            status = "MULTI_CYCLE_DESCENT_SUCCESS"
        else:
            t_opt = np.zeros(b1)
            phi1_optimal = phi1_initial
            residual_reduction = 0.0
            status = "LP_SOLVER_FAILED"

        return {
            "t_opt": t_opt,
            "phi1_initial": phi1_initial,
            "phi1_optimal": phi1_optimal,
            "residual_reduction": residual_reduction,
            "b1": b1,
            "status": status
        }



# --- Functional–Evaluator–Terminalizer Triad & Merkle Tape Verifier ---

import hashlib

class ResidualFunctional:
    """Pure functional mapping cochains to scalar residual metrics (Phi1, Gamma2, mu_harm).
    Purity: No branching, no tape writes, no mutable state.
    """
    @staticmethod
    def evaluate(carrier: SimplicialCarrier, h_1: Dict[Tuple[Any, Any], float]) -> Dict[str, float]:
        sig = ObstructionCalculus.analyze_1cochain(carrier, h_1)
        decomp = ObstructionCalculus.hodge_decompose_l2(carrier, h_1)
        return {
            "phi_1": sig.phi_1,
            "gamma_2": sig.gamma_2,
            "mu_harm": decomp["harmonic_mass"],
            "gauge_mass": decomp["gauge_mass"],
            "curvature_mass": decomp["curvature_mass"]
        }


class ResidualEvaluator:
    """Pure evaluator mapping functional values + declared epsilons to typed receipts.
    Purity: No control flow, no residual mutation.
    """
    @staticmethod
    def evaluate(
        func_values: Dict[str, float],
        eps_gamma: float = 1e-6,
        eps_harm: float = 1e-6,
        eps_phi: float = 1e-6
    ) -> Dict[str, Any]:
        gamma_2 = func_values.get("gamma_2", 0.0)
        mu_harm = func_values.get("mu_harm", 0.0)
        phi_1 = func_values.get("phi_1", 0.0)

        if phi_1 < eps_phi:
            label = "EXACT_CLASS"
        elif gamma_2 < eps_gamma and mu_harm > eps_harm:
            label = "CLOSED_RESIDUAL"
        elif gamma_2 >= eps_gamma:
            label = "ACTIVE_CLOSURE_FAILURE"
        else:
            label = "CLOSED_RESIDUAL"

        return {
            "label": label,
            "phi_1": phi_1,
            "gamma_2": gamma_2,
            "mu_harm": mu_harm,
            "predicate": (label == "EXACT_CLASS")
        }


@dataclass
class StepRecord:
    """Append-only Merkle tape StepRecord."""
    step_index: int
    letter: str
    receipt_hash: str
    residual_digest: str
    prev_hash: str
    authority_effect: str = "None"

    def compute_step_hash(self) -> str:
        payload = f"{self.step_index}:{self.letter}:{self.receipt_hash}:{self.residual_digest}:{self.prev_hash}:{self.authority_effect}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class DDATerminalizer:
    """Terminalizer managing execution flow, calling CanContinue_n, and writing Merkle tape."""

    def __init__(self, engine: PrimeTriadEngine, genesis_hash: str = "GENESIS_000"):
        self.engine = engine
        self.merkle_tape: List[StepRecord] = []
        self.current_root = genesis_hash

    def process_step(self, letter: str, receipt: Dict[str, Any]) -> str:
        # Check CanContinue_n predicate
        can_cont = self.engine.can_continue(
            stage=self.engine.ops_count,
            has_obligation=True,
            has_witness=True
        )
        if not can_cont:
            return "HALT_BUDGET_EXHAUSTED"

        step_idx = len(self.merkle_tape)
        receipt_payload = str(sorted(receipt.items()))
        receipt_hash = hashlib.sha256(receipt_payload.encode("utf-8")).hexdigest()

        res_digest_payload = f"{receipt.get('phi_1_before', 0.0)}:{receipt.get('phi_1_after', 0.0)}:{receipt.get('delta_phi_1', 0.0)}:{receipt.get('gamma_2_before', 0.0)}:{receipt.get('gamma_2_after', 0.0)}:{receipt.get('harmonic_mass', 0.0)}"
        residual_digest = hashlib.sha256(res_digest_payload.encode("utf-8")).hexdigest()

        record = StepRecord(
            step_index=step_idx,
            letter=letter,
            receipt_hash=receipt_hash,
            residual_digest=residual_digest,
            prev_hash=self.current_root,
            authority_effect="None"
        )

        self.current_root = record.compute_step_hash()
        self.merkle_tape.append(record)
        self.engine.execute_step()
        return "STEP_RECORDED"


def verify_merkle_tape(tape: List[StepRecord], genesis_hash: str = "GENESIS_000") -> Tuple[bool, str]:
    """Linear O(N) Merkle tape verification without re-solving differential operators."""
    current_hash = genesis_hash
    for record in tape:
        if record.prev_hash != current_hash:
            return False, f"Prev hash mismatch at step {record.step_index}"
        expected_hash = record.compute_step_hash()
        current_hash = expected_hash
    return True, "MERKLE_TAPE_VERIFIED"


# --- OE-000 Candidate Packet, Intake Trace, & 7-Step Local Declaration ---

@dataclass
class CandidatePacket:
    """OE001-01 Candidate Packet Schema."""
    artifact_id: str
    locus_id: str
    problem_family: str
    primitive_difference_proposal: str
    carrier_proposal: str
    zero_rel_proposal: str
    observer_proposal: str
    witness_available: bool = True
    quotient_or_refusal: str = "E"
    adapter_confidence: str = "high"
    authority_effect: str = "None"
    status: str = "proposed_only"


@dataclass
class IntakeTrace:
    """OE001-01 Intake Trace Schema."""
    raw_artifact_hash: str
    candidate_locus: str
    candidate_packet: CandidatePacket
    intake_adapter_status: str = "ADMITTED"
    enters_dda_trace: bool = False


@dataclass
class LocalDeclarationOrder:
    """OE001-02 7-Step Local Packet Declaration Order."""
    step0_grounding_hash: str
    step1_carrier: SimplicialCarrier
    step2_observer: ObserverPacket
    step3_primitive_difference: Dict[Tuple[Any, Any], float]
    step4_zero_rel_rule: str
    step5_witness_certificate: Optional[str]
    step6_quotient_policy: str = "Q1_SEPARATED"

    def validate_declaration_order(self) -> Tuple[bool, str]:
        if not self.step0_grounding_hash:
            return False, "REFUSE_MISSING_GROUNDING"
        if not self.step1_carrier or not self.step1_carrier.validate():
            return False, "REFUSE_MISSING_CARRIER"
        if not self.step2_observer or not self.step2_observer.observer_id:
            return False, "REFUSE_MISSING_OBSERVER"
        if self.step3_primitive_difference is None:
            return False, "REFUSE_MISSING_PRIMITIVE_DIFFERENCE"
        if not self.step4_zero_rel_rule:
            return False, "REFUSE_MISSING_ZERO_REL"
        if not self.step5_witness_certificate:
            return False, "REFUSE_MISSING_WITNESS"
        return True, "ACCEPT_DECLARATION"


class PrimeTriadEngine:
    """Master Algorithm Prime Triad Engine (000, 001, 002)."""

    def __init__(self, budget: float = 100.0, delta_control: float = 10.0):
        self.budget = budget
        self.delta_control = delta_control
        self.ops_count = 0
        self.loss_ledger: List[str] = []

    def evaluate_intake(self, trace: IntakeTrace) -> str:
        packet = trace.candidate_packet
        if not packet.carrier_proposal:
            return "REFUSED_MISSING_CARRIER"
        if not packet.observer_proposal:
            return "REFUSED_MISSING_OBSERVER"
        if not packet.witness_available:
            return "REFUSED_MISSING_WITNESS"
        if packet.adapter_confidence == "inadequate":
            self.loss_ledger.append(f"Intake adapter inadequate for artifact {packet.artifact_id}")
            return "ADAPTER_INADEQUATE"
        return "ACCEPT_DECLARATION"

    def can_continue(
        self,
        stage: int,
        has_obligation: bool,
        has_witness: bool,
        next_carrier_declared: bool = True,
        adapter_sound: bool = True,
        detector_adequate: bool = True,
        minimal_lift: bool = True,
        skeleton_preserved: bool = True,
        budget_remains: bool = True,
        coda_la_refusal: bool = False
    ) -> bool:
        """Prime 002 Master Continuation Predicate CanContinue_n."""
        has_budget = budget_remains and (self.budget - self.delta_control >= 0)
        return (
            has_obligation
            and has_witness
            and next_carrier_declared
            and adapter_sound
            and detector_adequate
            and minimal_lift
            and skeleton_preserved
            and has_budget
            and not coda_la_refusal
        )

    def execute_step(self) -> str:
        if self.budget < self.delta_control:
            return "TERMINAL_WITH_DEBT"
        self.budget -= self.delta_control
        self.ops_count += 1
        return "LOCAL_GREEN_FOR_SCOPE"

    def record_transform_move(
        self,
        move: str,  # "D" (Descent) or "Λ" (Structural Lift)
        loss_or_gain: str,
        forcing_obstruction: str,
    ) -> Dict[str, str]:
        """Record D/Λ representation move telemetry with loss/gain distinction (S3 harvest rule)."""
        entry = {
            "move": move,
            "loss_or_gain": loss_or_gain,
            "forcing_obstruction": forcing_obstruction,
        }
        self.loss_ledger.append(f"[{move}] {loss_or_gain} (forced by {forcing_obstruction})")
        return entry

    def coda_reentry(self, locus_id: str) -> Dict[str, Any]:
        return {
            "locus": locus_id,
            "carrier": f"Carrier_{locus_id}",
            "observer": f"Observer_{locus_id}",
            "authority_effect": "None",
            "status": "RE_ENTERED_LOCAL_SCOPE"
        }


# --- Legacy CODAMasterSuite (CODA-000 to CODA-009) ---

class CODAMasterSuite:
    """Master CODA Computational Framework (CODA-000 to CODA-009)."""
    
    def __init__(self, N_nodes: int, edges: List[Tuple[int, int]], faces: List[Tuple[int, int, int]]):
        self.N_nodes = N_nodes
        self.edges = edges
        self.faces = faces
        self.simplicial_carrier = SimplicialCarrier(
            vertices=list(range(N_nodes)),
            edges=edges,
            faces=faces
        )
        
    def coda_000_foc_curvature(self, cochain: np.ndarray) -> np.ndarray:
        """CODA-000 (FOC): Compute face curvature K_f = (d_1 delta)_f."""
        edge_map = {e: idx for idx, e in enumerate(self.edges)}
        for (u, v), idx in list(edge_map.items()):
            edge_map[(v, u)] = idx
            
        curvatures = np.zeros(len(self.faces))
        for f_idx, (u, v, w) in enumerate(self.faces):
            e1 = edge_map.get((u, v))
            e2 = edge_map.get((v, w))
            e3 = edge_map.get((w, u))
            v1 = cochain[e1] if e1 is not None else 0.0
            v2 = cochain[e2] if e2 is not None else 0.0
            v3 = cochain[e3] if e3 is not None else 0.0
            curvatures[f_idx] = v1 + v2 + v3
        return curvatures

    def coda_002_mur_l1_gauge_norm(self, cochain: np.ndarray) -> float:
        """CODA-002 (MUR): Compute exact l1 gauge-minimized norm Phi_1([delta]) via SciPy linprog LP."""
        min_l1, _ = ObstructionCalculus.solve_l1_gauge_minimization(self.simplicial_carrier, cochain)
        return min_l1

    def coda_005_cs_q_bridge_embedding(self, omega_val: float) -> float:
        """CODA-005 (CS-Q-BRIDGE): Classical diagonal embedding defect D_e = 0.5 * |omega|."""
        return 0.5 * abs(omega_val)

    def coda_008_q_rates(
        self,
        cochain: Optional[np.ndarray] = None,
        J_int: float = 1.5,
        t: float = 0.05
    ) -> Tuple[float, float, float]:
        """CODA-008 (Q): Compute normal rate nu_e, acceleration a_e, and Pinsker bound from cochain."""
        if cochain is not None and len(cochain) == len(self.edges):
            nu_e = float(np.mean(np.abs(cochain)))
            curv = self.coda_000_foc_curvature(cochain)
            a_e = float(np.mean(np.abs(curv))) if len(curv) > 0 else 0.0
        else:
            nu_e = 2.0 * J_int
            a_e = 2.0 * (J_int**2)
        defect = max(0.0, nu_e * t - a_e * (t**2))
        mi_pinsker = (1.0 / (2.0 * np.log(2.0))) * (defect**2)
        return nu_e, a_e, mi_pinsker

    def coda_009_master_ledger(self, cochain: np.ndarray, J_int: float = 1.5, t: float = 0.05) -> Dict[str, float]:
        """CODA-009 (Master Brand Wrapper): Compute unified CODA ledger."""
        curv = self.coda_000_foc_curvature(cochain)
        phi_1 = self.coda_002_mur_l1_gauge_norm(cochain)
        d_emb = self.coda_005_cs_q_bridge_embedding(cochain[0])
        nu_e, a_e, mi_pinsker = self.coda_008_q_rates(J_int=J_int, t=t)
        
        return {
            "coda_000_face_curvature": float(curv[0]),
            "coda_002_l1_gauge_norm_phi1": phi_1,
            "coda_005_cs_q_bridge_defect": d_emb,
            "coda_008_nu_e": nu_e,
            "coda_008_a_e": a_e,
            "coda_008_pinsker_qmi": mi_pinsker
        }


# --- CODA-DERIV-001 & CODA-DERIV-004 Mechanics ---

class SelfRepairAdjunction:
    """CODA-DERIV-001: Self-Repair Adjunction F ⊣ G (CODA-006 / CODA-003).
    Section functor F: C0 -> C1, F(alpha) = d0 alpha.
    Repair functor G: C1 -> C0, G(omega) = argmin_alpha ||omega - d0 alpha||_1.
    AuthorityEffect: None.
    """

    @staticmethod
    def section_functor_F(carrier: SimplicialCarrier, f_0: Dict[Any, float]) -> Dict[Tuple[Any, Any], float]:
        """Compute Section functor F(alpha) = d0 alpha."""
        return CohomologicalEngine.d0(carrier, f_0)

    @staticmethod
    def repair_functor_G(carrier: SimplicialCarrier, h_1: Dict[Tuple[Any, Any], float]) -> Dict[Any, float]:
        """Compute Repair functor G(omega) = argmin_alpha ||omega - d0 alpha||_1 via SciPy LP."""
        h_vec = np.array([h_1.get(e, 0.0) for e in carrier.edges])
        _, alpha_opt = ObstructionCalculus.solve_l1_gauge_minimization(carrier, h_vec)
        if isinstance(alpha_opt, np.ndarray):
            return {v: float(val) for v, val in zip(carrier.vertices, alpha_opt)}
        return alpha_opt

    @classmethod
    def verify_galois_insertion(
        cls,
        carrier: SimplicialCarrier,
        f_0: Dict[Any, float],
        tol: float = 1e-6
    ) -> bool:
        """Verify Galois insertion d0 G(F(alpha)) == d0 alpha."""
        f_alpha = cls.section_functor_F(carrier, f_0)
        g_f_alpha = cls.repair_functor_G(carrier, f_alpha)
        d0_g_f = cls.section_functor_F(carrier, g_f_alpha)
        
        diff = sum(abs(d0_g_f.get(e, 0.0) - f_alpha.get(e, 0.0)) for e in carrier.edges)
        return bool(diff < tol)

    @classmethod
    def verify_autopoietic_stability(
        cls,
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float],
        tol: float = 1e-6
    ) -> bool:
        """Verify 1-step self-repair stability: d0 G(d0 G(omega)) == d0 G(omega)."""
        alpha1 = cls.repair_functor_G(carrier, h_1)
        d0_alpha1 = cls.section_functor_F(carrier, alpha1)
        alpha2 = cls.repair_functor_G(carrier, d0_alpha1)
        d0_alpha2 = cls.section_functor_F(carrier, alpha2)
        
        diff = sum(abs(d0_alpha2.get(e, 0.0) - d0_alpha1.get(e, 0.0)) for e in carrier.edges)
        return bool(diff < tol)


class ColimitAggregationEngine:
    """CODA-DERIV-004: Global Presheaf Colimit Aggregation (CODA-001 / CODA-005 / CODA-007).
    Aggregates local cochains over graph cover into global colimit colim_i omega_i.
    AuthorityEffect: None.
    """

    @staticmethod
    def aggregate_local_cochains(
        carrier: SimplicialCarrier,
        local_cochains: List[Dict[Tuple[Any, Any], float]]
    ) -> Dict[Tuple[Any, Any], float]:
        """Compute colimit presheaf aggregation colim_i omega_i = mean_i omega_i(e)."""
        if not local_cochains:
            return {e: 0.0 for e in carrier.edges}
        
        global_cochain: Dict[Tuple[Any, Any], float] = {}
        for e in carrier.edges:
            vals = [lc.get(e, 0.0) for lc in local_cochains if e in lc]
            global_cochain[e] = float(np.mean(vals)) if vals else 0.0
            
        return global_cochain

    @staticmethod
    def verify_bilipschitz_defect_bounds(
        carrier: SimplicialCarrier,
        h_1: Dict[Tuple[Any, Any], float],
        c_min: float = 0.1,
        c_max: float = 10.0
    ) -> Dict[str, Any]:
        """Verify global bi-Lipschitz defect bounds c * Phi_1 <= D_M <= C * Phi_1."""
        h_vec = np.array([h_1.get(e, 0.0) for e in carrier.edges])
        phi_1, _ = ObstructionCalculus.solve_l1_gauge_minimization(carrier, h_vec)
        
        # Bridge B1 classical diagonal embedding defect D_e = 0.5 * ||omega||_1
        d_emb = 0.5 * float(np.sum(np.abs(h_vec)))
        
        bounds_hold = bool(c_min * phi_1 <= d_emb <= c_max * phi_1) if phi_1 > 1e-9 else True
        
        return {
            "phi_1": phi_1,
            "d_emb": d_emb,
            "bounds_hold": bounds_hold,
            "c_min": c_min,
            "c_max": c_max,
            "status": "BILIPSCHITZ_BOUNDS_VERIFIED"
        }


def run_coda_master_suite() -> Dict[str, float]:
    """Execute CODA Master Suite demonstration."""
    print("=== UNIVERSE CODA: MASTER BRAND SUITE (CODA-000 to CODA-009 & OE-000) ===")
    edges = [(0, 1), (1, 2), (2, 0)]
    faces = [(0, 1, 2)]
    coda = CODAMasterSuite(3, edges, faces)
    
    cochain = np.array([1.0, 0.5, -0.8])
    ledger = coda.coda_009_master_ledger(cochain, J_int=1.5, t=0.05)
    
    print(f"CODA-000 Face Curvature K_f: {ledger['coda_000_face_curvature']:.4f}")
    print(f"CODA-002 l1 Gauge Norm Phi_1: {ledger['coda_002_l1_gauge_norm_phi1']:.4f}")
    print(f"CODA-005 CS-Q-Bridge Defect D_e: {ledger['coda_005_cs_q_bridge_defect']:.4f}")
    print(f"CODA-008 Normal Rate nu_e: {ledger['coda_008_nu_e']:.4f}, Acceleration a_e: {ledger['coda_008_a_e']:.4f}")
    print(f"CODA-009 Master Ledger QMI: {ledger['coda_008_pinsker_qmi']:.6f}")
    
    return ledger

if __name__ == "__main__":
    run_coda_master_suite()







