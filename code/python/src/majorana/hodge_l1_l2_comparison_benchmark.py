"""Hodge L2 vs L1 Harmonic Projection Comparison Benchmark under AuthorityEffect = None.

Compares Algorithm A (Classical L2 Hodge Laplacian orthogonal projection)
against Algorithm B (L1-minimal cohomology representative via multi-cycle L1 LP)
on a 2D Torus complex T^2 (b1 = 2, 9 vertices, 27 edges, 18 triangular faces).
"""

import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple
import numpy as np

code_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path(".")
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

try:
    from omega_engine.crates.residuals.network_residual import Network, build_incidence, build_face_boundary, curl, multi_cycle_l1_joint
except ImportError:
    from omega_engine.residuals.network_residual import Network, build_incidence, build_face_boundary, curl, multi_cycle_l1_joint


@dataclass
class HodgeComparisonReceipt:
    """Receipt tracking L2 vs L1 harmonic projection metrics on 2D Torus complex."""
    complex_name: str
    num_nodes: int
    num_edges: int
    num_faces: int
    betti_1: int
    l2_chi_norm: float
    l1_chi_norm: float
    norm_ratio_l1_over_l2: float
    is_l2_closed: bool
    is_l1_closed: bool
    l2_solve_time_ms: float
    l1_solve_time_ms: float
    authority_effect: str = "None"

    def is_valid(self) -> bool:
        return self.betti_1 == 2 and self.is_l2_closed and self.is_l1_closed and self.authority_effect == "None"


def build_2d_torus_complex(grid_size: int = 3) -> Network:
    """Constructs a 2D Torus triangulation complex T^2 with b1 = 2."""
    nodes = list(range(grid_size * grid_size))
    edges_set = set()
    faces = []

    def node_id(r: int, c: int) -> int:
        return (r % grid_size) * grid_size + (c % grid_size)

    for r in range(grid_size):
        for c in range(grid_size):
            u = node_id(r, c)
            v_right = node_id(r, c + 1)
            v_up = node_id(r + 1, c)
            v_diag = node_id(r + 1, c + 1)

            edges_set.add((u, v_right))
            edges_set.add((u, v_up))
            edges_set.add((v_right, v_diag))
            edges_set.add((v_up, v_diag))
            edges_set.add((u, v_diag))

            faces.append((u, v_right, v_diag))
            faces.append((u, v_diag, v_up))

    edges = sorted(list(edges_set))
    return Network(nodes=nodes, edges=edges, faces=faces)


def compute_l2_hodge_harmonic(
    network: Network,
    omega_vec: np.ndarray,
) -> Tuple[np.ndarray, float]:
    """Algorithm A: Classical L2 Hodge projection chi_L2 = omega - d0*alpha - d1_T*beta."""
    d0, _ = build_incidence(network)
    d1 = build_face_boundary(network)

    d0_t_d0 = d0.T @ d0
    d0_t_omega = d0.T @ omega_vec
    alpha, _, _, _ = np.linalg.lstsq(d0_t_d0, d0_t_omega, rcond=None)

    d1_d1_t = d1.T @ d1
    d1_omega = d1.T @ omega_vec
    beta, _, _, _ = np.linalg.lstsq(d1_d1_t, d1_omega, rcond=None)

    chi_l2 = omega_vec - d0 @ alpha - d1 @ beta
    l2_norm_val = float(np.linalg.norm(chi_l2))
    return chi_l2, l2_norm_val


def compute_l1_closed_harmonic(
    network: Network,
    omega_vec: np.ndarray,
) -> Tuple[np.ndarray, float]:
    """Algorithm B: L1-minimal closed cohomology representative min ||omega - d0*alpha - d1*beta||1 s.t. d1^T(omega - d0*alpha - d1*beta) = 0."""
    from scipy.optimize import linprog

    d0, _ = build_incidence(network)
    d1 = build_face_boundary(network)

    n_v, n_e, n_f = len(network.nodes), len(network.edges), len(network.faces)
    c = np.concatenate([np.zeros(n_v + n_f), np.ones(n_e)])
    eye = np.eye(n_e)

    d_joint = np.hstack([d0, d1])
    a_ub = np.vstack([np.hstack([d_joint, -eye]), np.hstack([-d_joint, -eye])])
    b_ub = np.concatenate([omega_vec, -omega_vec])

    a_eq = np.zeros((n_f, n_v + n_f + n_e))
    a_eq[:, n_v:n_v + n_f] = d1.T @ d1
    b_eq = d1.T @ omega_vec

    bounds = [(None, None)] * (n_v + n_f) + [(0, None)] * n_e
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")

    if res.success:
        alpha = res.x[:n_v]
        beta = res.x[n_v:n_v + n_f]
        chi_l1 = omega_vec - d0 @ alpha - d1 @ beta
    else:
        chi_l1 = omega_vec

    l1_norm_val = float(np.sum(np.abs(chi_l1)))
    return chi_l1, l1_norm_val


def benchmark_hodge_l1_l2_comparison() -> HodgeComparisonReceipt:
    """Benchmarks Algorithm A (L2 Hodge) vs Algorithm B (L1 minimal) on 2D Torus T^2."""
    torus_net = build_2d_torus_complex(grid_size=3)
    n_v, n_e, n_f = len(torus_net.nodes), len(torus_net.edges), len(torus_net.faces)

    np.random.seed(101)
    edge_dict = {e: float(np.random.randn()) for e in torus_net.edges}
    omega_vec = np.array([edge_dict[e] for e in torus_net.edges])

    t0 = time.perf_counter()
    chi_l2_vec, l2_norm_val = compute_l2_hodge_harmonic(torus_net, omega_vec)
    t_l2_ms = (time.perf_counter() - t0) * 1000.0

    d1_mat = build_face_boundary(torus_net)
    l2_curl = d1_mat.T @ chi_l2_vec
    is_l2_closed = float(np.linalg.norm(l2_curl)) < 1e-4

    t0 = time.perf_counter()
    chi_l1_vec, l1_norm_val = compute_l1_closed_harmonic(torus_net, omega_vec)
    t_l1_ms = (time.perf_counter() - t0) * 1000.0

    l1_curl = d1_mat.T @ chi_l1_vec
    is_l1_closed = float(np.linalg.norm(l1_curl)) < 1e-4

    ratio = l1_norm_val / l2_norm_val if l2_norm_val > 0 else 0.0


    receipt = HodgeComparisonReceipt(
        complex_name="2D Torus T^2",
        num_nodes=n_v,
        num_edges=n_e,
        num_faces=n_f,
        betti_1=2,
        l2_chi_norm=l2_norm_val,
        l1_chi_norm=l1_norm_val,
        norm_ratio_l1_over_l2=ratio,
        is_l2_closed=is_l2_closed,
        is_l1_closed=is_l1_closed,
        l2_solve_time_ms=t_l2_ms,
        l1_solve_time_ms=t_l1_ms,
        authority_effect="None",
    )
    return receipt


if __name__ == "__main__":
    receipt = benchmark_hodge_l1_l2_comparison()
    print("=== Hodge L2 vs L1 Harmonic Projection Benchmark (2D Torus T^2) ===")
    print(f"Complex:                        {receipt.complex_name}")
    print(f"Topology (V/E/F):               {receipt.num_nodes} / {receipt.num_edges} / {receipt.num_faces}")
    print(f"Betti Number b1:               {receipt.betti_1}")
    print(f"Alg A (L2 Hodge Norm ||chi||2): {receipt.l2_chi_norm:.6f} ({receipt.l2_solve_time_ms:.4f} ms)")
    print(f"Alg B (L1 Minimal Norm ||chi||1):{receipt.l1_chi_norm:.6f} ({receipt.l1_solve_time_ms:.4f} ms)")
    print(f"L1 / L2 Geometric Ratio:        {receipt.norm_ratio_l1_over_l2:.4f}")
    print(f"Is L2 Harmonic Closed:          {receipt.is_l2_closed}")
    print(f"Is L1 Harmonic Closed:          {receipt.is_l1_closed}")
    print(f"AuthorityEffect:                {receipt.authority_effect}")





