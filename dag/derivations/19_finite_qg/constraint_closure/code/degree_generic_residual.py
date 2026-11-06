from __future__ import annotations
"""Degree-Generic Residual Engine.

Provides degree-generic residual evaluation (phi_k, gamma_{k+1}, chi_k) over SimplexComplex carriers
using l1_gauge repair, l1_joint minimization, or passthrough evaluation.

AuthorityEffect: None.
"""

from dataclasses import field
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Optional
import numpy as np
from scipy.optimize import linprog

from higher_simplex_assembly import (
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
    unrecognized_mass: float = 0.0
    is_certified: bool = False
    is_upper_bound: bool = False
    lp_success: bool = True
    authority_effect: str = "None"

    def as_triple(self) -> Tuple[float, float, float]:
        return (self.phi, self.gamma, self.chi)


def _solve_l1_linear_system(
    A: np.ndarray,
    b: np.ndarray,
    atol: float = 1e-9,
) -> Tuple[np.ndarray, np.ndarray, float, bool]:
    """Solve min_x ||b - A x||_1 via linear programming.

    Returns (x_opt, residual_vec, min_l1_norm, lp_success).
    If the solver fails, x_opt=0 is returned and min_l1_norm is ||b||_1.
    This value is an upper bound rather than the certified minimum.
    """
    n_rows, n_cols = A.shape
    if n_cols == 0 or n_rows == 0:
        return np.zeros(n_cols), b.copy(), float(np.sum(np.abs(b))), True

    c = np.zeros(n_cols + n_rows)
    c[n_cols:] = 1.0

    I_m = np.eye(n_rows)
    A_ub = np.block([[A, -I_m], [-A, -I_m]])
    b_ub = np.concatenate([b, -b])

    bounds = [(None, None)] * n_cols + [(0.0, None)] * n_rows

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if res.success:
        x_opt = res.x[:n_cols]
        residual_vec = b - A @ x_opt
        min_l1 = float(np.sum(np.abs(residual_vec)))
        return x_opt, residual_vec, min_l1, True
    else:
        return np.zeros(n_cols), b.copy(), float(np.sum(np.abs(b))), False


def simplex_permutation_sign(cell: Tuple[Any, ...]) -> Tuple[Tuple[Any, ...], int]:
    """Return (sorted_cell, sign) where sign is +1 or -1 for the permutation sorting cell.

    Returns (sorted_cell, 0) if cell contains duplicate vertices (degenerate simplex).
    """
    n = len(cell)
    if len(set(cell)) < n:
        return tuple(sorted(cell)), 0
    inversions = 0
    for i in range(n):
        for j in range(i + 1, n):
            if cell[i] > cell[j]:
                inversions += 1
    sign = -1 if (inversions % 2 != 0) else 1
    return tuple(sorted(cell)), sign


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
        unrecognized_mass = sum(abs(v) for v in cochain.values())
        return ResidualReport(
            phi=unrecognized_mass,
            gamma=0.0,
            chi=unrecognized_mass,
            degree=degree,
            cell_counts=cell_counts,
            method=method,
            unrecognized_mass=unrecognized_mass,
            authority_effect="None",
        )

    cell_index_k = {cell: idx for idx, cell in enumerate(cells_k)}
    w_vec = np.zeros(n_k, dtype=float)
    unrecognized_mass = 0.0
    for cell, val in cochain.items():
        sorted_cell, sgn = simplex_permutation_sign(cell)
        if sgn == 0:
            continue
        if sorted_cell in cell_index_k:
            w_vec[cell_index_k[sorted_cell]] += sgn * val
        else:
            unrecognized_mass += abs(val)

    cells_km1 = complex_obj.cells.get(degree - 1, [])
    if cells_km1:
        d_k_lower = boundary_matrix(cells_k, cells_km1)
        B_km1 = d_k_lower.T
    else:
        B_km1 = np.zeros((n_k, 0), dtype=float)

    cells_kp1 = complex_obj.cells.get(degree + 1, [])
    if cells_kp1:
        d_kp1_upper = boundary_matrix(cells_kp1, cells_k)
        D_k = d_kp1_upper.T
    else:
        D_k = np.zeros((0, n_k), dtype=float)

    potentials_dict: Dict[Tuple[Any, ...], float] = {}
    coexact_dict: Dict[Tuple[Any, ...], float] = {}
    lp_success: bool = True
    is_upper_bound: bool = False

    if method == "l1_gauge":
        alpha, res_vec, phi, lp_success = _solve_l1_linear_system(B_km1, w_vec)
        if not lp_success:
            is_upper_bound = True
        if len(cells_km1) > 0:
            potentials_dict = {cells_km1[i]: float(alpha[i]) for i in range(len(cells_km1))}
    elif method == "l1_joint":
        if cells_kp1:
            coexact_mat = boundary_matrix(cells_kp1, cells_k)
        else:
            coexact_mat = np.zeros((n_k, 0), dtype=float)

        A_joint = np.block([B_km1, coexact_mat])
        x_joint, res_vec, phi, lp_success = _solve_l1_linear_system(A_joint, w_vec)
        if not lp_success:
            is_upper_bound = True

        n_pot = B_km1.shape[1]
        alpha = x_joint[:n_pot]
        beta = x_joint[n_pot:]

        if len(cells_km1) > 0:
            potentials_dict = {cells_km1[i]: float(alpha[i]) for i in range(len(cells_km1))}
        if len(cells_kp1) > 0:
            coexact_dict = {cells_kp1[i]: float(beta[i]) for i in range(len(cells_kp1))}
    else:
        res_vec = w_vec.copy()
        phi = float(np.sum(np.abs(res_vec)))

    if D_k.shape[0] > 0:
        curv_vec = D_k @ res_vec
        gamma = float(np.sum(np.abs(curv_vec)))
    else:
        gamma = 0.0

    phi_total = phi + unrecognized_mass
    chi = phi_total if gamma < tol else unrecognized_mass

    res_cochain = {cells_k[i]: float(res_vec[i]) for i in range(n_k)}

    duality_gap: Optional[float] = None
    is_certified: bool = False

    return ResidualReport(
        phi=phi_total,
        gamma=gamma,
        chi=chi,
        degree=degree,
        residual_cochain=res_cochain,
        potentials=potentials_dict,
        coexact_coeffs=coexact_dict,
        cell_counts=cell_counts,
        method=method,
        duality_gap=duality_gap,
        unrecognized_mass=unrecognized_mass,
        is_certified=is_certified and lp_success,
        is_upper_bound=is_upper_bound,
        lp_success=lp_success,
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
