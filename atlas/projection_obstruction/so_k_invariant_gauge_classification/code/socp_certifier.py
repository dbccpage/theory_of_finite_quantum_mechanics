"""
Second-Order Cone Programming (SOCP) Primal-Dual Certifier.
Paper: GS-002 (so_k_invariant_gauge_classification)

Provides:
- Primal-Dual SOCP Zero-Gap Certification:
    Primal: inf_phi sum_e w_e ||delta_e - (d0 phi)_e||_2
    Dual:   sup_z   sum_e <z_e, delta_e> s.t. d0^* z = 0, ||z_e||_2 <= w_e
- Analytical closed-form cycle evaluator for simple cycles with signed orientations:
    CycleClosedFormCertifier
- Numerical tolerance-certified solver for general graph complexes:
    SOCPCertifier (method="auto" | "cycle_closed_form" | "numerical")
- Signed weak-duality gap tracking: signed_duality_gap = primal_value - dual_value.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Tuple, Optional, List
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import svd, null_space

from carrier import GraphComplex, Cochain, SlaterViolationError


def _validate_tolerance(tol: Any) -> float:
    """A numerical acceptance tolerance must be a finite nonnegative real."""
    if (
        isinstance(tol, bool)
        or not isinstance(tol, (int, float, np.integer, np.floating))
        or not np.isfinite(tol)
        or tol < 0
    ):
        raise ValueError(f"Certificate tolerance must be finite and nonnegative (got {tol!r}).")
    return float(tol)


@dataclass(frozen=True)
class DualityCertificate:
    """Certificate of primal and dual optimality for quotient obstruction."""

    primal_value: float
    dual_value: float
    duality_gap: float
    signed_duality_gap: float
    primal_repair: np.ndarray  # shape (n, k)
    residual_cochain: Cochain  # shape (m, k)
    dual_circulation: Cochain  # shape (m, k)
    divergence_norm: float  # ||d0^* phi||_max
    max_dual_norm_violation: float  # max_e max(0, ||phi_e||_2 - c_e)
    is_divergence_free: bool
    is_dual_feasible: bool
    is_optimal: bool
    details: Dict[str, Any]
    is_zero_gap: bool = False  # Explicitly verified based on abs(signed_duality_gap) <= tol
    solver_method: str = "numerical_socp_subspace"  # 'cycle_closed_form', 'zero_circulation', 'numerical_socp_subspace', 'smoothed_lbfgs'


@dataclass(frozen=True)
class SOCPDualityCertificate(DualityCertificate):
    """Certificate of primal and dual optimality for quotient obstruction."""

    pass


class SOCPCertifier:
    """
    Second-order cone primal-dual solver and certifier.
    Routes to exact closed-form on simple cycles, or numerical subspace optimization on general graphs.
    """

    def __init__(self, complex: GraphComplex, tol: float = 1e-7) -> None:
        self.complex = complex
        self.tol = _validate_tolerance(tol)
        # Strict validation of complex and weights
        self.complex.verify_complex_strict()
        if np.any(self.complex.edge_weights <= 0):
            raise SlaterViolationError(
                "Edge weights must be strictly positive (Slater condition violated: w_e <= 0)."
            )

    def _is_simple_directed_cycle(self) -> bool:
        """Check if complex is a connected simple cycle graph (m == n, all degree 2)."""
        m = self.complex.num_edges
        n = self.complex.num_vertices
        if m != n or m < 3:
            return False
        # Check degrees
        in_deg = np.zeros(n, dtype=int)
        out_deg = np.zeros(n, dtype=int)
        for u, v in self.complex.edges:
            out_deg[u] += 1
            in_deg[v] += 1
        # Connected cycle: every vertex has deg=2 in underlying graph
        undir_deg = in_deg + out_deg
        if not np.all(undir_deg == 2):
            return False
        # Check rank of d0 is n - 1 (single connected component)
        d0 = self.complex.d0
        s = svd(d0, compute_uv=False)
        rank = int(np.sum(s > 1e-10))
        return rank == n - 1

    def _simple_cycle_orientation_signs(
        self, orientations: Optional[List[int] | np.ndarray] = None
    ) -> np.ndarray:
        """Signed cycle traversal vs stored edge direction."""
        m = self.complex.num_edges
        if orientations is not None:
            ori_list = list(orientations)
            if len(ori_list) != m:
                raise ValueError("Orientations length must match number of edges.")
            for x in ori_list:
                if not (isinstance(x, (int, np.integer)) and not isinstance(x, bool) and x in (+1, -1)):
                    raise ValueError(
                        f"Orientation sign must be +1 or -1 (got {x}); Orientations must be in {{+1, -1}}."
                    )
            eps = np.array(ori_list, dtype=float)
            if not np.allclose(self.complex.d0.T @ eps, 0.0, atol=1e-6):
                raise ValueError(
                    f"Orientations {orientations} do not represent a closed cycle circulation of the graph (d0^T @ eps != 0)."
                )
            return eps
        # A valid 2-cell boundary may cancel repeated terms; it need not be
        # the graph's cycle traversal. Derive the traversal from the graph.
        return self._walk_simple_cycle_orientation_signs()

    def _walk_simple_cycle_orientation_signs(self) -> np.ndarray:
        """Walk the unique 2-regular cycle; sign is stored-edge agreement."""
        m = self.complex.num_edges
        n = self.complex.num_vertices
        adj: List[List[Tuple[int, int, int]]] = [[] for _ in range(n)]
        for e_idx, (u, v) in enumerate(self.complex.edges):
            adj[u].append((v, e_idx, +1))
            adj[v].append((u, e_idx, -1))
        eps = np.ones(m, dtype=float)
        used = [False] * m
        u = 0
        for _ in range(m):
            nxt = None
            for v, e_idx, direction in adj[u]:
                if not used[e_idx]:
                    nxt = (v, e_idx, direction)
                    break
            if nxt is None:
                break
            v, e_idx, direction = nxt
            used[e_idx] = True
            eps[e_idx] = float(direction)
            u = v
        return eps

    @staticmethod
    def _solve_tree_gauge(
        edges: List[Tuple[int, int]],
        n: int,
        k: int,
        w_data: np.ndarray,
        root: int = 0,
        excluded_edge: Optional[int] = None,
    ) -> np.ndarray:
        """Floating-point gauge potential along spanning tree via forward graph traversal."""
        from collections import deque

        phi = np.zeros((n, k), dtype=float)
        visited = [False] * n
        visited[root] = True
        queue = deque([root])

        adj: List[List[Tuple[int, int, int]]] = [[] for _ in range(n)]
        for e_idx, (u, v) in enumerate(edges):
            if e_idx == excluded_edge:
                continue
            adj[u].append((v, e_idx, +1))
            adj[v].append((u, e_idx, -1))

        while queue:
            u = queue.popleft()
            for v, e_idx, direction in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    if direction == +1:
                        phi[v] = phi[u] + w_data[e_idx]
                    else:
                        phi[v] = phi[u] - w_data[e_idx]
                    queue.append(v)
        return phi

    def _solve_cycle_closed_form(
        self, omega: Cochain, orientations: Optional[List[int] | np.ndarray] = None
    ) -> SOCPDualityCertificate:
        r"""
        Exact closed-form solution on simple cycle:
            Phi_{j,w}(omega) = (min_e w_e) * ||S(omega)||_2.
            Dual z_e = eps_e * w_min * S(omega) / ||S(omega)||_2.
            Primal phi solved on spanning tree E \ {e_min}.
        """
        n = self.complex.num_vertices
        k = self.complex.stalk_dim
        w = self.complex.edge_weights
        w_data = omega.data

        eps = self._simple_cycle_orientation_signs(orientations)
        circ = np.sum(eps[:, None] * w_data, axis=0)  # S(omega)
        circ_norm = float(np.hypot.reduce(circ))

        if circ_norm == 0.0:
            return self._solve_zero_circulation(omega)

        w_min = float(np.min(w))
        min_idx = int(np.argmin(w))

        # Exact dual variable: z_e = eps_e * w_min * (circ / circ_norm)
        unit_circ = circ / circ_norm
        z_data = eps[:, None] * (w_min * unit_circ)

        dual_val = float(np.sum(z_data * w_data))
        # Mathematically, dual_val = w_min * circ_norm

        # Primal repair: solve (d0 phi)_e = w_data_e for all edges except min_idx
        u_min, v_min = self.complex.edges[min_idx]
        phi_tree = self._solve_tree_gauge(
            self.complex.edges, n, k, w_data, root=v_min, excluded_edge=min_idx
        )
        phi_tree -= np.mean(phi_tree, axis=0, keepdims=True)

        res_data = w_data - self.complex.d0 @ phi_tree
        exact_norms = np.hypot.reduce(res_data, axis=1)
        primal_val = float(np.sum(w * exact_norms))

        div = self.complex.d0.T @ z_data
        div_norm = float(np.max(np.abs(div)))
        z_norms = np.hypot.reduce(z_data, axis=1)
        max_ball_viol = float(np.max(np.maximum(0.0, z_norms - w)))
        signed_gap = primal_val - dual_val
        gap = abs(signed_gap)

        is_div = div_norm <= self.tol
        is_feas = max_ball_viol <= self.tol
        is_zg = gap <= self.tol
        is_opt = is_div and is_feas and is_zg

        return SOCPDualityCertificate(
            primal_value=primal_val,
            dual_value=dual_val,
            duality_gap=gap,
            signed_duality_gap=signed_gap,
            primal_repair=phi_tree,
            residual_cochain=Cochain(res_data, degree=1),
            dual_circulation=Cochain(z_data, degree=1),
            divergence_norm=div_norm,
            max_dual_norm_violation=max_ball_viol,
            is_divergence_free=is_div,
            is_dual_feasible=is_feas,
            is_zero_gap=is_zg,
            is_optimal=is_opt,
            solver_method="cycle_closed_form",
            details={
                "w_min": w_min,
                "circulation": circ.tolist(),
                "circulation_norm": circ_norm,
                "bottleneck_edge": min_idx,
            },
        )

    def _solve_zero_circulation(self, omega: Cochain) -> SOCPDualityCertificate:
        """Try a zero dual witness; accept only the weighted numerical gap.

        This is a tolerance-qualified residual check, not a proof that the
        input lies exactly in im(d0).
        """
        m = self.complex.num_edges
        k = self.complex.stalk_dim
        w = self.complex.edge_weights
        d0 = self.complex.d0

        if self._is_simple_directed_cycle():
            phi = self._solve_tree_gauge(
                self.complex.edges, self.complex.num_vertices, k, omega.data,
                excluded_edge=int(np.argmin(w)),
            )
        else:
            phi, _, _, _ = np.linalg.lstsq(d0, omega.data, rcond=None)
            phi -= np.mean(phi, axis=0, keepdims=True)

        res_data = omega.data - d0 @ phi
        primal_val = float(np.sum(w * np.hypot.reduce(res_data, axis=1)))
        z_data = np.zeros((m, k), dtype=float)
        dual_val = 0.0

        signed_gap = primal_val - dual_val
        gap = abs(signed_gap)
        div = float(np.max(np.abs(d0.T @ z_data)))
        max_ball_viol = 0.0

        is_div = div <= self.tol
        is_feas = max_ball_viol <= self.tol
        is_zg = gap <= self.tol
        is_opt = is_div and is_feas and is_zg

        return SOCPDualityCertificate(
            primal_value=primal_val,
            dual_value=dual_val,
            duality_gap=gap,
            signed_duality_gap=signed_gap,
            primal_repair=phi,
            residual_cochain=Cochain(res_data, degree=1),
            dual_circulation=Cochain(z_data, degree=1),
            divergence_norm=div,
            max_dual_norm_violation=max_ball_viol,
            is_divergence_free=is_div,
            is_dual_feasible=is_feas,
            is_zero_gap=is_zg,
            is_optimal=is_opt,
            solver_method="zero_circulation",
            details={
                "verification_scope": "floating-point residual and weighted gap",
                "weighted_residual_norm": primal_val,
            },
        )

    def _solve_general_socp(self, omega: Cochain) -> SOCPDualityCertificate:
        """
        Tolerance-certified numerical SOCP primal-dual solver on arbitrary graph complexes.
        Dual:
            Maximize <N0 @ theta, omega> s.t. ||(N0 @ theta)_e||_2 <= w_e.
            d0^* z = 0 is satisfied identically via the cycle space null_space(d0.T).
        Primal:
            Minimize sum_e w_e ||omega_e - (d0 @ Vr @ y)_e||_2 via continuation.
        """
        m = self.complex.num_edges
        k = self.complex.stalk_dim
        w = self.complex.edge_weights
        w_data = omega.data
        d0 = self.complex.d0

        # Step 1: Null space of d0.T (Cycle Space)
        N0 = null_space(d0.T)
        B = N0.shape[1]

        if B == 0:
            # Forest/tree: no cycles exist, any cochain is coboundary
            return self._solve_zero_circulation(omega)

        # Step 2: Solve Dual SOCP in theta-space (B x k variables)
        def dual_objective(th_flat: np.ndarray) -> float:
            th = th_flat.reshape((B, k))
            z = N0 @ th
            return -float(np.sum(z * w_data))

        def dual_gradient(th_flat: np.ndarray) -> np.ndarray:
            return (-N0.T @ w_data).flatten()

        cons = []
        for e in range(m):
            def make_con(idx: int):
                return (
                    lambda th_f: 1.0
                    - float(np.linalg.norm(N0[idx : idx + 1, :] @ th_f.reshape((B, k))))
                    / w[idx]
                )
            cons.append({"type": "ineq", "fun": make_con(e)})

        th0 = np.zeros(B * k, dtype=float)

        res_d = minimize(
            fun=dual_objective,
            x0=th0,
            jac=dual_gradient,
            constraints=cons,
            method="SLSQP",
            options={"ftol": 1e-15, "maxiter": 1500},
        )

        th_opt = res_d.x.reshape((B, k))
        z_opt = N0 @ th_opt

        # Guarantee strict dual feasibility by safety clipping if numerical creep
        z_norms = np.linalg.norm(z_opt, axis=1)
        max_ratio = float(np.max(z_norms / w))
        if max_ratio > 1.0:
            z_opt = z_opt / max_ratio
            z_norms = z_norms / max_ratio

        dual_val = float(np.sum(z_opt * w_data))

        # Step 3: Solve Primal via Gauge-Reduced SVD Space
        U, s, Vt = svd(d0)
        rank = int(np.sum(s > 1e-10))
        Vr = Vt[:rank, :].T
        d0_Vr = d0 @ Vr

        def primal_smoothed_obj(
            y_flat: np.ndarray, eps: float
        ) -> Tuple[float, np.ndarray]:
            y = y_flat.reshape((rank, k))
            res = w_data - d0_Vr @ y
            norms = np.sqrt(np.sum(res**2, axis=1) + eps**2)
            val = float(np.sum(w * norms))
            grad_res = (w[:, None] * res) / norms[:, None]
            grad_y = -(d0_Vr.T @ grad_res)
            return val, grad_y.flatten()

        y_curr = np.zeros((rank, k), dtype=float)
        for eps_val in [1e-3, 1e-6, 1e-9, 1e-12]:
            res_p = minimize(
                fun=lambda yf, eps_cur=eps_val: primal_smoothed_obj(yf, eps_cur),
                x0=y_curr.flatten(),
                jac=True,
                method="L-BFGS-B",
                options={"gtol": 1e-12, "ftol": 1e-15, "maxiter": 3000},
            )
            y_curr = res_p.x.reshape((rank, k))

        phi_opt = Vr @ y_curr
        phi_opt -= np.mean(phi_opt, axis=0, keepdims=True)

        res_opt = w_data - d0 @ phi_opt
        exact_res_norms = np.linalg.norm(res_opt, axis=1)
        primal_val = float(np.sum(w * exact_res_norms))

        div = d0.T @ z_opt
        div_norm = float(np.max(np.abs(div)))
        max_ball_viol = float(np.max(np.maximum(0.0, z_norms - w)))
        signed_gap = primal_val - dual_val
        gap = abs(signed_gap)

        is_div = div_norm <= self.tol
        is_feas = max_ball_viol <= self.tol
        is_zg = gap <= self.tol
        is_opt = is_div and is_feas and is_zg

        return SOCPDualityCertificate(
            primal_value=primal_val,
            dual_value=dual_val,
            duality_gap=gap,
            signed_duality_gap=signed_gap,
            primal_repair=phi_opt,
            residual_cochain=Cochain(res_opt, degree=1),
            dual_circulation=Cochain(z_opt, degree=1),
            divergence_norm=div_norm,
            max_dual_norm_violation=max_ball_viol,
            is_divergence_free=is_div,
            is_dual_feasible=is_feas,
            is_zero_gap=is_zg,
            is_optimal=is_opt,
            solver_method="numerical_socp_subspace",
            details={
                "cycle_dim_B": B,
                "gauge_rank": rank,
                "dual_success": res_d.success,
                "dual_message": res_d.message,
            },
        )

    def certify(
        self,
        omega: Cochain,
        orientations: Optional[List[int] | np.ndarray] = None,
        method: str = "auto",
    ) -> SOCPDualityCertificate:
        """
        Produce candidate primal-dual duality certificate.
        method: "auto" (default: cycle closed form if cycle, else numerical),
                "cycle_closed_form" (enforces cycle closed-form),
                "numerical" (forces numerical subspace solve).
        """
        if method not in ("auto", "cycle_closed_form", "numerical"):
            raise ValueError(
                f"Unknown solver method '{method}'; expected 'auto', 'cycle_closed_form', or 'numerical'."
            )

        if omega.shape != (self.complex.num_edges, self.complex.stalk_dim):
            raise ValueError(
                f"Omega shape {omega.shape} does not match complex {(self.complex.num_edges, self.complex.stalk_dim)}."
            )

        if orientations is not None:
            ori_list = list(orientations)
            if len(ori_list) != self.complex.num_edges:
                raise ValueError(
                    f"Orientations length must match number of edges (got {len(ori_list)} for {self.complex.num_edges})."
                )
            for x in ori_list:
                if not (isinstance(x, (int, np.integer)) and not isinstance(x, bool) and x in (+1, -1)):
                    raise ValueError(
                        f"Orientation sign must be +1 or -1 (got {x}); Orientations must be in {{+1, -1}}."
                    )

        if method == "cycle_closed_form":
            if not self._is_simple_directed_cycle():
                raise ValueError("method='cycle_closed_form' requires a simple directed cycle complex.")
            return self._solve_cycle_closed_form(omega, orientations=orientations)

        if method == "numerical":
            return self._solve_general_socp(omega)

        # method == "auto"
        if self._is_simple_directed_cycle():
            return self._solve_cycle_closed_form(omega, orientations=orientations)

        # Residual coordinates alone ignore the declared edge weights. A zero
        # witness is useful only if its weighted primal-dual gap passes.
        zero_candidate = self._solve_zero_circulation(omega)
        if zero_candidate.is_optimal:
            return zero_candidate

        return self._solve_general_socp(omega)


class CycleClosedFormCertifier(SOCPCertifier):
    """
    Dedicated floating-point closed-form evaluator for single directed cycles.
    Valid only on simple cycles (m == n, connected degree 2).
    """

    def __init__(self, complex: GraphComplex, tol: float = 1e-7) -> None:
        super().__init__(complex, tol=tol)
        if not self._is_simple_directed_cycle():
            raise ValueError("CycleClosedFormCertifier requires a simple directed cycle complex.")

    def certify(
        self,
        omega: Cochain,
        orientations: Optional[List[int] | np.ndarray] = None,
        method: str = "cycle_closed_form",
    ) -> SOCPDualityCertificate:
        if method not in ("auto", "cycle_closed_form"):
            raise ValueError(
                f"Unknown solver method '{method}' for CycleClosedFormCertifier; expected 'cycle_closed_form' or 'auto'."
            )
        if omega.shape != (self.complex.num_edges, self.complex.stalk_dim):
            raise ValueError(
                f"Omega shape {omega.shape} does not match complex {(self.complex.num_edges, self.complex.stalk_dim)}."
            )
        if orientations is not None:
            ori_list = list(orientations)
            if len(ori_list) != self.complex.num_edges:
                raise ValueError(
                    f"Orientations length must match number of edges (got {len(ori_list)} for {self.complex.num_edges})."
                )
            for x in ori_list:
                if not (isinstance(x, (int, np.integer)) and not isinstance(x, bool) and x in (+1, -1)):
                    raise ValueError(
                        f"Orientation sign must be +1 or -1 (got {x}); Orientations must be in {{+1, -1}}."
                    )
        return self._solve_cycle_closed_form(omega, orientations=orientations)


# Backward-compatibility alias
ExactSOCPCertifier = SOCPCertifier
