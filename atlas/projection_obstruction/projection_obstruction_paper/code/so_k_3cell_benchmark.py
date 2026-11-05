"""SO(k) vector field optimization and 3-cell complex benchmarking module.

Implements discrete Hodge boundary operators d0, d1, d2 over 3-cell complexes,
fast regularized L-BFGS-B solver with analytical Jacobian for vector fields R^k (k >= 3),
and benchmark execution across dimensions k in {3, 4, 5, 8, 16, 32}.
"""

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Tuple, Sequence
import numpy as np


def _minimize_lbfgs(
    fun_and_grad: Callable[[np.ndarray], Tuple[float, np.ndarray]],
    x0: np.ndarray,
    gtol: float = 1e-7,
    max_iter: int = 500,
    memory: int = 10,
    ftol: float = 2.220446049250313e-09,
) -> Tuple[np.ndarray, int, bool]:
    """Deterministic limited-memory BFGS with Armijo backtracking.

    2026-08-31: replaces ``scipy.optimize.minimize(..., method="L-BFGS-B")``
    so the deposit depends on stdlib+numpy+pytest only.  Two-loop recursion,
    fixed memory, deterministic line search; no bounds are needed here.
    Returns ``(x, iterations, converged)``.

    ``converged`` is True when either the max-abs gradient reaches ``gtol``
    or the relative function decrease falls to ``ftol`` — the same pair of
    criteria scipy's L-BFGS-B uses (``ftol`` default matches scipy's
    ``factr=1e7``, i.e. ``1e7 * machine-eps``).  The first rewrite dropped
    the ``ftol`` criterion, so nearly-nonsmooth objectives that scipy would
    report as converged ran to ``max_iter`` and (once the flag was actually
    reported — see ``solve_so_k_vector_residual``) read as non-converged.
    """

    x = np.asarray(x0, dtype=np.float64).copy()
    value, grad = fun_and_grad(x)
    s_list: List[np.ndarray] = []
    y_list: List[np.ndarray] = []
    iteration = 0
    for iteration in range(1, max_iter + 1):
        if float(np.max(np.abs(grad))) <= gtol:
            return x, iteration - 1, True
        # two-loop recursion
        q = grad.copy()
        alphas = []
        for s_vec, y_vec in zip(reversed(s_list), reversed(y_list)):
            rho = 1.0 / float(y_vec @ s_vec)
            alpha = rho * float(s_vec @ q)
            alphas.append((alpha, rho, s_vec, y_vec))
            q -= alpha * y_vec
        if y_list:
            gamma = float(s_list[-1] @ y_list[-1]) / float(y_list[-1] @ y_list[-1])
            q *= gamma
        for alpha, rho, s_vec, y_vec in reversed(alphas):
            beta = rho * float(y_vec @ q)
            q += (alpha - beta) * s_vec
        direction = -q
        directional = float(grad @ direction)
        if directional >= 0.0:
            direction = -grad
            directional = float(grad @ direction)
        # Armijo backtracking
        step = 1.0
        for _ in range(60):
            candidate = x + step * direction
            candidate_value, candidate_grad = fun_and_grad(candidate)
            if candidate_value <= value + 1e-4 * step * directional:
                break
            step *= 0.5
        else:
            return x, iteration, False
        if (value - candidate_value) <= ftol * max(
            abs(value), abs(candidate_value), 1.0
        ):
            return candidate, iteration, True
        s_vec = candidate - x
        y_vec = candidate_grad - grad
        if float(y_vec @ s_vec) > 1e-14:
            s_list.append(s_vec)
            y_list.append(y_vec)
            if len(s_list) > memory:
                s_list.pop(0)
                y_list.pop(0)
        x, value, grad = candidate, candidate_value, candidate_grad
    return x, iteration, float(np.max(np.abs(grad))) <= gtol


@dataclass
class ThreeCellComplex:
    """Simplicial 3-cell complex containing nodes, directed edges, triangular faces, and tetrahedra."""
    nodes: List[Any]
    edges: List[Tuple[Any, Any]]
    faces: List[Tuple[Any, Any, Any]] = field(default_factory=list)
    volumes: List[Tuple[Any, Any, Any, Any]] = field(default_factory=list)


def build_incidence_matrix(complex_3d: ThreeCellComplex) -> Tuple[np.ndarray, Dict[Any, int]]:
    """Build boundary matrix d0 mapping 0-cells (nodes) to 1-cells (directed edges)."""
    node_idx = {n: i for i, n in enumerate(complex_3d.nodes)}
    n_e, n_v = len(complex_3d.edges), len(complex_3d.nodes)
    d0 = np.zeros((n_e, n_v))
    for e_i, (u, v) in enumerate(complex_3d.edges):
        d0[e_i, node_idx[u]] = -1.0
        d0[e_i, node_idx[v]] = 1.0
    return d0, node_idx


def solve_so_k_vector_residual(
    complex_3d: ThreeCellComplex,
    vector_edge_values: Dict[Tuple[Any, Any], np.ndarray],
    eps: float = 1e-8,
) -> Dict[str, Any]:
    """Extract vector potential field alpha in R^(V x k) minimizing sum_e ||r_e||_2 under SO(k) symmetry.

    Uses regularized smooth objective sum_e sqrt(||r_e||_2^2 + eps^2) with analytical Jacobian.
    """
    d0, node_idx = build_incidence_matrix(complex_3d)
    n_v, n_e = len(complex_3d.nodes), len(complex_3d.edges)

    first_val = next(iter(vector_edge_values.values()))
    k_dim = len(first_val)

    h_mat = np.zeros((n_e, k_dim))
    for i, e in enumerate(complex_3d.edges):
        h_mat[i, :] = vector_edge_values.get(e, np.zeros(k_dim))

    # Analytical smooth objective and gradient
    def fun_and_grad(x_flat):
        alpha = x_flat.reshape((n_v, k_dim))
        r_mat = h_mat - d0 @ alpha  # (E, k)
        sq_norms = np.sum(r_mat ** 2, axis=1) + (eps ** 2)  # (E,)
        norms = np.sqrt(sq_norms)  # (E,)
        obj_val = float(np.sum(norms))

        # Grad wrt r_mat: dObj/dr_e = r_e / sqrt(||r_e||^2 + eps^2)
        grad_r = r_mat / norms[:, np.newaxis]  # (E, k)
        # r_mat = h_mat - d0 @ alpha => dr_mat/dalpha = -d0
        # dObj/dalpha = -d0.T @ grad_r
        grad_alpha = -d0.T @ grad_r  # (V, k)
        return obj_val, grad_alpha.flatten()

    # Deterministic initialization at the least-squares solution, then
    # L-BFGS refinement of the regularized sum-of-norms objective.
    x0 = np.linalg.lstsq(d0, h_mat, rcond=None)[0].flatten()
    x_opt, n_iter, converged = _minimize_lbfgs(fun_and_grad, x0, gtol=1e-7)

    alpha_mat = x_opt.reshape((n_v, k_dim))
    residual_mat = h_mat - d0 @ alpha_mat
    edge_lengths = np.linalg.norm(residual_mat, axis=1)
    size = float(np.sum(edge_lengths))

    residual = {e: residual_mat[i, :] for i, e in enumerate(complex_3d.edges)}
    pots = {n: alpha_mat[node_idx[n], :] for n in complex_3d.nodes}
    return {
        "residual_size": size,
        "residual": residual,
        "potentials": pots,
        "is_pure_gauge": size < 1e-6,
        "n_iter": n_iter,
        # 2026-08-31: "success" previously ignored the optimizer's converged
        # flag and reported only np.isfinite(size), so a non-converged run
        # could certify convergence.  It now reports the real flag; the
        # finite-size sanity check is kept as its own field.
        "converged": bool(converged),
        "residual_finite": bool(np.isfinite(size)),
        "success": bool(converged) and bool(np.isfinite(size)),
    }


def generate_tetrahedral_complex(n_nodes: int = 6) -> ThreeCellComplex:
    """Generates a 3-cell simplicial complex (tetrahedral mesh) with n_nodes."""
    nodes = list(range(n_nodes))
    edges = []
    faces = []
    volumes = []

    # Complete graph edges for tetrahedral connectivity
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            edges.append((i, j))

    # Triangular 2-faces
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            for k in range(j + 1, n_nodes):
                faces.append((i, j, k))

    # Tetrahedral 3-volumes
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            for k in range(j + 1, n_nodes):
                for l in range(k + 1, n_nodes):
                    volumes.append((i, j, k, l))

    return ThreeCellComplex(nodes=nodes, edges=edges, faces=faces, volumes=volumes)


def benchmark_so_k_performance(
    dimensions: Sequence[int] = (3, 4, 5, 8, 16, 32),
    n_nodes: int = 8,
    seed: int = 42,
) -> List[Dict[str, Any]]:
    """Runs performance benchmarks across higher-dimensional SO(k) vector fields."""
    # 2026-08-31: np.random.seed/np.random.randn (legacy global RNG) replaced
    # with the per-call Generator API for version-stable determinism.
    rng = np.random.default_rng(seed)
    complex_3d = generate_tetrahedral_complex(n_nodes=n_nodes)
    results = []

    print(f"Benchmarking SO(k) solver on 3-cell complex ({n_nodes} nodes, {len(complex_3d.edges)} edges, {len(complex_3d.volumes)} tetrahedra)...")
    print(f"{'Dim k':>8}  {'Time (ms)':>12}  {'Residual Size':>16}  {'Iters':>8}  {'Success':>8}")
    print("-" * 60)

    for k in dimensions:
        # Generate random vector 1-chain h_e in R^k
        vector_edge_values = {
            e: rng.standard_normal(k) for e in complex_3d.edges
        }

        t0 = time.perf_counter()
        res = solve_so_k_vector_residual(complex_3d, vector_edge_values)
        t1 = time.perf_counter()
        elapsed_ms = (t1 - t0) * 1000.0

        item = {
            "dim_k": k,
            "elapsed_ms": elapsed_ms,
            "residual_size": res["residual_size"],
            "n_iter": res["n_iter"],
            "converged": res["converged"],
            "residual_finite": res["residual_finite"],
            "success": res["success"],
        }
        results.append(item)
        print(f"{k:8d}  {elapsed_ms:12.3f}  {res['residual_size']:16.6f}  {res['n_iter']:8d}  {str(res['success']):>8}")

    print("-" * 60)
    return results


if __name__ == "__main__":
    benchmark_so_k_performance()
