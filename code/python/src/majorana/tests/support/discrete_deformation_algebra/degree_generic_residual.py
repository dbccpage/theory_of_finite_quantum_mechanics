"""Degree-Generic Residual Engine.

Provides degree-generic residual evaluation (φ_k, γ_{k+1}, χ_k) over SimplexComplex carriers
using l1_gauge repair, l1_joint minimization, or passthrough evaluation.

AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import field
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Optional
import numpy as np
from scipy.optimize import linprog

from omega_engine.crates.functional.higher_simplex_assembly import (
    SimplexComplex,
    assemble_from_network,
    boundary_matrix,
)


@dataclass
class ResidualReport:
    """Certificate-bearing result for degree-generic residual evaluation."""

    phi: float
    gamma: float
    chi: float
    degree: int
    residual_cochain: Dict[Tuple[Any, ...], float] = field(default_factory=dict)
    potentials: Dict[Tuple[Any, ...], float] = field(default_factory=dict)
    coexact_coeffs: Dict[Tuple[Any, ...], float] = field(default_factory=dict)
    cell_counts: Dict[int, int] = field(default_factory=dict)
    method: str = "l1_gauge"
    duality_gap: Optional[float] = None
    is_certified: bool = False
    authority_effect: str = "None"

    def as_triple(self) -> Tuple[float, float, float]:
        return (self.phi, self.gamma, self.chi)


def _solve_l1_linear_system(
    A: np.ndarray,
    b: np.ndarray,
    atol: float = 1e-9,
) -> Tuple[np.ndarray, np.ndarray, float]:
    """Solve min_x ||b - A x||_1 via linear programming.

    Returns (x_opt, residual_vec, min_l1_norm).
    """
    n_rows, n_cols = A.shape
    if n_cols == 0 or n_rows == 0:
        return np.zeros(n_cols), b.copy(), float(np.sum(np.abs(b)))

    # Variables: x (n_cols), t (n_rows)
    # Objective: min sum(t)
    c = np.zeros(n_cols + n_rows)
    c[n_cols:] = 1.0

    # Constraints:
    # A x - t <= b  =>  [A, -I] [x; t] <= b
    # -A x - t <= -b => [-A, -I] [x; t] <= -b
    I_m = np.eye(n_rows)
    A_ub = np.block([[A, -I_m], [-A, -I_m]])
    b_ub = np.concatenate([b, -b])

    bounds = [(None, None)] * n_cols + [(0.0, None)] * n_rows

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if res.success:
        x_opt = res.x[:n_cols]
        residual_vec = b - A @ x_opt
        min_l1 = float(np.sum(np.abs(residual_vec)))
        return x_opt, residual_vec, min_l1
    else:
        # Fallback to zero x
        return np.zeros(n_cols), b.copy(), float(np.sum(np.abs(b)))


def evaluate_residual(
    complex_obj: SimplexComplex,
    degree: int,
    cochain: Dict[Tuple[Any, ...], float],
    method: str = "l1_gauge",
    tol: float = 1e-6,
) -> ResidualReport:
    """Core degree-generic residual evaluation engine operating on a SimplexComplex."""
    cells_k = complex_obj.cells.get(degree, [])
    n_k = len(cells_k)
    cell_counts = {dim: len(c) for dim, c in complex_obj.cells.items()}

    if n_k == 0:
        return ResidualReport(
            phi=0.0,
            gamma=0.0,
            chi=0.0,
            degree=degree,
            cell_counts=cell_counts,
            method=method,
            authority_effect="None",
        )

    cell_index_k = {cell: idx for idx, cell in enumerate(cells_k)}
    w_vec = np.zeros(n_k, dtype=float)
    for cell, val in cochain.items():
        # Handle orientation/sorting if needed
        sorted_cell = tuple(sorted(cell))
        if sorted_cell in cell_index_k:
            w_vec[cell_index_k[sorted_cell]] += val

    # 1. Lower coboundary operator d_{k-1}^\top: C^{k-1} -> C^k
    # boundary_matrix(cells_k, cells_{k-1}) is d_k: C^k -> C^{k-1} of shape (N_{k-1}, N_k)
    # Its transpose d_k^\top is the coboundary operator C^{k-1} -> C^k of shape (N_k, N_{k-1})
    cells_km1 = complex_obj.cells.get(degree - 1, [])
    if cells_km1:
        d_k_lower = boundary_matrix(cells_k, cells_km1)  # shape (N_{k-1}, N_k)
        B_km1 = d_k_lower.T  # shape (N_k, N_{k-1})
    else:
        B_km1 = np.zeros((n_k, 0), dtype=float)

    # 2. Upper coboundary operator d_k^\top: C^k -> C^{k+1}
    # boundary_matrix(cells_{k+1}, cells_k) is d_{k+1}: C^{k+1} -> C^k of shape (N_k, N_{k+1})
    # Its transpose d_{k+1}^\top is coboundary C^k -> C^{k+1} of shape (N_{k+1}, N_k)
    cells_kp1 = complex_obj.cells.get(degree + 1, [])
    if cells_kp1:
        d_kp1_upper = boundary_matrix(cells_kp1, cells_k)  # shape (N_k, N_{k+1})
        D_k = d_kp1_upper.T  # shape (N_{k+1}, N_k)
    else:
        D_k = np.zeros((0, n_k), dtype=float)

    potentials_dict: Dict[Tuple[Any, ...], float] = {}
    coexact_dict: Dict[Tuple[Any, ...], float] = {}

    if method == "l1_gauge":
        alpha, res_vec, phi = _solve_l1_linear_system(B_km1, w_vec)
        if len(cells_km1) > 0:
            potentials_dict = {cells_km1[i]: float(alpha[i]) for i in range(len(cells_km1))}
    elif method == "l1_joint":
        # Joint gauge + coexact repair
        # Gauge matrix: B_km1 (N_k, N_{k-1})
        # Coexact matrix: d_{k+1} of shape (N_k, N_{k+1})
        if cells_kp1:
            d_kp1_matrix = boundary_matrix(cells_kp1, cells_k).T  # shape (N_k, N_{k+1})
            # Wait, coexact vectors in C^k are represented by d_{k+1} (columns of d_{k+1})
            # boundary_matrix(cells_kp1, cells_k) is shape (N_k, N_{k+1})
            coexact_mat = boundary_matrix(cells_kp1, cells_k)  # shape (N_k, N_{k+1})
        else:
            coexact_mat = np.zeros((n_k, 0), dtype=float)

        A_joint = np.block([B_km1, coexact_mat])
        x_joint, res_vec, phi = _solve_l1_linear_system(A_joint, w_vec)

        n_pot = B_km1.shape[1]
        alpha = x_joint[:n_pot]
        beta = x_joint[n_pot:]

        if len(cells_km1) > 0:
            potentials_dict = {cells_km1[i]: float(alpha[i]) for i in range(len(cells_km1))}
        if len(cells_kp1) > 0:
            coexact_dict = {cells_kp1[i]: float(beta[i]) for i in range(len(cells_kp1))}
    else:
        # Passthrough
        res_vec = w_vec.copy()
        phi = float(np.sum(np.abs(res_vec)))

    # Compute curvature mass gamma_{k+1} = ||D_k res_vec||_1
    if D_k.shape[0] > 0:
        curv_vec = D_k @ res_vec
        gamma = float(np.sum(np.abs(curv_vec)))
    else:
        gamma = 0.0

    chi = phi if gamma < tol else 0.0

    res_cochain = {cells_k[i]: float(res_vec[i]) for i in range(n_k)}

    duality_gap: Optional[float] = None
    is_certified: bool = False

    if method == "l1_gauge":
        try:
            from omega_engine.crates.functional.degree_k_phi import phi_k_on_complex
            receipt_k = phi_k_on_complex(complex_obj, degree=degree, cochain_values=cochain)
            duality_gap = float(receipt_k.duality_gap)
            is_certified = bool(receipt_k.is_certified)
        except Exception:
            pass

    return ResidualReport(
        phi=phi,
        gamma=gamma,
        chi=chi,
        degree=degree,
        residual_cochain=res_cochain,
        potentials=potentials_dict,
        coexact_coeffs=coexact_dict,
        cell_counts=cell_counts,
        method=method,
        duality_gap=duality_gap,
        is_certified=is_certified,
        authority_effect="None",
    )


def evaluate_residual_on_network(
    network: Any,
    degree: int,
    cochain_values: Dict[Tuple[Any, ...], float],
    method: str = "l1_gauge",
    max_dim: Optional[int] = None,
    tol: float = 1e-6,
) -> ResidualReport:
    """Convenience wrapper assembling SimplexComplex from Network and evaluating residual."""
    target_dim = max(degree + 1, max_dim if max_dim is not None else 0)
    complex_obj = assemble_from_network(network, max_dim=target_dim)
    return evaluate_residual(complex_obj, degree, cochain_values, method=method, tol=tol)


def residual_triple_for_lift(
    network: Any,
    degree: int,
    cochain_values: Dict[Tuple[Any, ...], float],
    method: str = "l1_gauge",
) -> Tuple[float, float, float]:
    """Returns just the (phi, gamma, chi) residual triple expected by lift_or_terminate."""
    report = evaluate_residual_on_network(network, degree, cochain_values, method=method)
    return report.as_triple()






