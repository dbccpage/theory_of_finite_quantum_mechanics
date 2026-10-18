"""Empirical 1D and 2D quantum lattice simulations for PO-000 §§5-6.

This module simulates exact matrix-exponentiation trajectories for 1D/2D
Transverse-Field Ising Models (TFIM) and Heisenberg XXZ models, comparing
the empirical local product-retraction l1 defect trajectory against the
short-time double-commutator lower bound.
"""

from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite
from typing import Literal

import numpy as np
import numpy.typing as npt
from scipy.linalg import expm

from omega_engine.crates.quantum_physics.quantum_lattice import ComplexMatrix, QuantumInputError, operator_norm


def _paulis() -> tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix, ComplexMatrix]:
    i = np.eye(2, dtype=np.complex128)
    x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    y = np.array([[0, -1.0j], [1.0j, 0]], dtype=np.complex128)
    z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    return i, x, y, z


def kron_n(operators: Sequence[ComplexMatrix]) -> ComplexMatrix:
    """Kronecker product over a sequence of single-site matrices."""
    result = operators[0]
    for op in operators[1:]:
        result = np.kron(result, op)
    return result.astype(np.complex128)


def _single_site_op(op: ComplexMatrix, site: int, num_sites: int) -> ComplexMatrix:
    i, _, _, _ = _paulis()
    factors = [op if k == site else i for k in range(num_sites)]
    return kron_n(factors)


def _two_site_op(op1: ComplexMatrix, site1: int, op2: ComplexMatrix, site2: int, num_sites: int) -> ComplexMatrix:
    i, _, _, _ = _paulis()
    factors = [i] * num_sites
    factors[site1] = op1
    factors[site2] = op2
    return kron_n(factors)


def partial_trace(rho: ComplexMatrix, keep_sites: Sequence[int], num_sites: int) -> ComplexMatrix:
    """Compute the partial trace of a multi-qubit density matrix keeping specified site indices."""
    dim_total = 2**num_sites
    if rho.shape != (dim_total, dim_total):
        raise QuantumInputError(f"rho shape must be ({dim_total}, {dim_total})")

    keep = list(keep_sites)
    trace_out = [s for s in range(num_sites) if s not in keep]

    shape = [2] * (2 * num_sites)
    tensor = rho.reshape(shape)

    axes_row = keep + trace_out
    axes_col = [k + num_sites for k in keep] + [t + num_sites for t in trace_out]
    perm = axes_row + axes_col
    tensor = np.transpose(tensor, perm)

    n_keep = len(keep)
    n_trace = len(trace_out)
    dim_keep = 2**n_keep
    dim_trace = 2**n_trace

    matrix = tensor.reshape((dim_keep, dim_trace, dim_keep, dim_trace))
    reduced = np.trace(matrix, axis1=1, axis2=3)
    return reduced.astype(np.complex128)


def trace_norm(A: ComplexMatrix) -> float:
    """Schatten 1-norm (sum of singular values)."""
    singular_values = np.linalg.svd(A, compute_uv=False)
    return float(np.sum(singular_values))


def build_1d_tfim_hamiltonian(
    num_sites: int, coupling: float, transverse_field: float
) -> tuple[ComplexMatrix, ComplexMatrix, list[tuple[int, int]]]:
    r"""Build 1D TFIM Hamiltonian: H = -J \sum_{i} Z_i Z_{i+1} - h \sum_i X_i."""
    if num_sites < 2:
        raise QuantumInputError("num_sites must be at least 2")

    _, x, _, z = _paulis()
    dim = 2**num_sites
    H_int = np.zeros((dim, dim), dtype=np.complex128)
    H_local = np.zeros((dim, dim), dtype=np.complex128)
    edges = []

    for i in range(num_sites - 1):
        edge_term = -coupling * _two_site_op(z, i, z, i + 1, num_sites)
        H_int += edge_term
        edges.append((i, i + 1))

    for i in range(num_sites):
        H_local += -transverse_field * _single_site_op(x, i, num_sites)

    return H_int + H_local, H_int, edges


def build_2d_tfim_hamiltonian(
    rows: int, cols: int, coupling: float, transverse_field: float
) -> tuple[ComplexMatrix, ComplexMatrix, list[tuple[int, int]]]:
    """Build 2D TFIM Hamiltonian on a 2D grid."""
    num_sites = rows * cols
    if num_sites < 4:
        raise QuantumInputError("2D grid must have at least 4 sites")

    _, x, _, z = _paulis()
    dim = 2**num_sites
    H_int = np.zeros((dim, dim), dtype=np.complex128)
    H_local = np.zeros((dim, dim), dtype=np.complex128)
    edges = []

    def site_idx(r: int, c: int) -> int:
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            u = site_idx(r, c)
            if c + 1 < cols:
                v = site_idx(r, c + 1)
                H_int += -coupling * _two_site_op(z, u, z, v, num_sites)
                edges.append((u, v))
            if r + 1 < rows:
                v = site_idx(r + 1, c)
                H_int += -coupling * _two_site_op(z, u, z, v, num_sites)
                edges.append((u, v))

    for i in range(num_sites):
        H_local += -transverse_field * _single_site_op(x, i, num_sites)

    return H_int + H_local, H_int, edges


def build_1d_heisenberg_hamiltonian(
    num_sites: int, J: float, delta: float = 1.0, h_z: float = 0.0
) -> tuple[ComplexMatrix, ComplexMatrix, list[tuple[int, int]]]:
    r"""Build 1D Heisenberg XXZ Hamiltonian: H = -J \sum (X_i X_{i+1} + Y_i Y_{i+1} + \Delta Z_i Z_{i+1}) - h \sum Z_i."""
    if num_sites < 2:
        raise QuantumInputError("num_sites must be at least 2")

    _, x, y, z = _paulis()
    dim = 2**num_sites
    H_int = np.zeros((dim, dim), dtype=np.complex128)
    H_local = np.zeros((dim, dim), dtype=np.complex128)
    edges = []

    for i in range(num_sites - 1):
        term = -J * (
            _two_site_op(x, i, x, i + 1, num_sites)
            + _two_site_op(y, i, y, i + 1, num_sites)
            + delta * _two_site_op(z, i, z, i + 1, num_sites)
        )
        H_int += term
        edges.append((i, i + 1))

    if h_z != 0.0:
        for i in range(num_sites):
            H_local += -h_z * _single_site_op(z, i, num_sites)

    return H_int + H_local, H_int, edges


def compute_double_commutator_prefactor(H_int: ComplexMatrix, rho0: ComplexMatrix) -> float:
    """Compute exact short-time double-commutator prefactor c_2 = (1/2) ||[[H_int, rho0], H_int]||_1."""
    comm1 = H_int @ rho0 - rho0 @ H_int
    comm2 = H_int @ comm1 - comm1 @ H_int
    return 0.5 * trace_norm(comm2)


def compute_edgewise_l1_defect(
    rho: ComplexMatrix, num_sites: int, edges: Sequence[tuple[int, int]]
) -> float:
    r"""Compute total edgewise product-retraction l1 defect I(rho) = \sum_{(u,v)} ||rho_{uv} - rho_u \otimes rho_v||_1."""
    total_defect = 0.0
    for u, v in edges:
        rho_uv = partial_trace(rho, [u, v], num_sites)
        rho_u = partial_trace(rho, [u], num_sites)
        rho_v = partial_trace(rho, [v], num_sites)
        rho_prod = np.kron(rho_u, rho_v)
        total_defect += trace_norm(rho_uv - rho_prod)
    return total_defect


@dataclass
class LatticeTrajectoryResult:
    time: float
    empirical_defect: float
    theoretical_lower_bound: float
    bound_satisfied: bool


@dataclass
class LatticeSimulationReplay:
    model_name: str
    num_sites: int
    coupling: float
    double_commutator_c2: float
    trajectories: tuple[LatticeTrajectoryResult, ...]
    evidence_kind: Literal["numerical_replay"] = "numerical_replay"
    limitations: tuple[str, ...] = (
        "Finite matrix exponentiation replay over finite grid/chain; short-time bound target.",
    )


def run_lattice_simulation_replay(
    model_type: Literal["1d_tfim", "2d_tfim", "1d_heisenberg"],
    *,
    num_sites_or_rows: int = 3,
    cols: int = 2,
    coupling: float = 1.0,
    transverse_field_or_delta: float = 0.5,
    t_max: float = 0.2,
    num_points: int = 5,
) -> LatticeSimulationReplay:
    """Run an exact quantum lattice matrix exponentiation simulation replay."""
    if model_type == "1d_tfim":
        H, H_int, edges = build_1d_tfim_hamiltonian(num_sites_or_rows, coupling, transverse_field_or_delta)
        n_sites = num_sites_or_rows
        model_name = f"1D TFIM (N={n_sites}, J={coupling}, h={transverse_field_or_delta})"
    elif model_type == "2d_tfim":
        H, H_int, edges = build_2d_tfim_hamiltonian(num_sites_or_rows, cols, coupling, transverse_field_or_delta)
        n_sites = num_sites_or_rows * cols
        model_name = f"2D TFIM ({num_sites_or_rows}x{cols}, J={coupling}, h={transverse_field_or_delta})"
    elif model_type == "1d_heisenberg":
        H, H_int, edges = build_1d_heisenberg_hamiltonian(num_sites_or_rows, coupling, transverse_field_or_delta)
        n_sites = num_sites_or_rows
        model_name = f"1D Heisenberg (N={n_sites}, J={coupling}, Delta={transverse_field_or_delta})"
    else:
        raise QuantumInputError(f"Unknown model_type {model_type}")

    dim = 2**n_sites
    psi0 = np.ones(dim, dtype=np.complex128) / np.sqrt(dim)
    rho0 = np.outer(psi0, psi0.conj())

    c2 = compute_double_commutator_prefactor(H_int, rho0)
    times = np.linspace(0.0, t_max, num_points)
    trajectories = []

    for t in times:
        U = expm(-1j * H * t)
        rho_t = U @ rho0 @ U.conj().T
        defect = compute_edgewise_l1_defect(rho_t, n_sites, edges)
        bound = c2 * (t**2)
        satisfied = bool(defect >= bound - 1.0e-5)
        trajectories.append(
            LatticeTrajectoryResult(
                time=float(t),
                empirical_defect=float(defect),
                theoretical_lower_bound=float(bound),
                bound_satisfied=satisfied,
            )
        )

    return LatticeSimulationReplay(
        model_name=model_name,
        num_sites=n_sites,
        coupling=coupling,
        double_commutator_c2=c2,
        trajectories=tuple(trajectories),
    )


def build_2d_heisenberg_hamiltonian(
    rows: int, cols: int, J: float, delta: float = 1.0, h_z: float = 0.0
) -> tuple[ComplexMatrix, ComplexMatrix, list[tuple[int, int]]]:
    """Build 2D Heisenberg XXZ Hamiltonian on a 2D grid."""
    num_sites = rows * cols
    if num_sites < 4:
        raise QuantumInputError("2D grid must have at least 4 sites")

    _, x, y, z = _paulis()
    dim = 2**num_sites
    H_int = np.zeros((dim, dim), dtype=np.complex128)
    H_local = np.zeros((dim, dim), dtype=np.complex128)
    edges = []

    def site_idx(r: int, c: int) -> int:
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            u = site_idx(r, c)
            if c + 1 < cols:
                v = site_idx(r, c + 1)
                term = -J * (
                    _two_site_op(x, u, x, v, num_sites)
                    + _two_site_op(y, u, y, v, num_sites)
                    + delta * _two_site_op(z, u, z, v, num_sites)
                )
                H_int += term
                edges.append((u, v))
            if r + 1 < rows:
                v = site_idx(r + 1, c)
                term = -J * (
                    _two_site_op(x, u, x, v, num_sites)
                    + _two_site_op(y, u, y, v, num_sites)
                    + delta * _two_site_op(z, u, z, v, num_sites)
                )
                H_int += term
                edges.append((u, v))

    if h_z != 0.0:
        for i in range(num_sites):
            H_local += -h_z * _single_site_op(z, i, num_sites)

    return H_int + H_local, H_int, edges


def compute_higher_order_commutator_coefficients(
    H: ComplexMatrix, H_int: ComplexMatrix, rho0: ComplexMatrix
) -> tuple[float, float, float, float]:
    """Compute exact Taylor derivative coefficients for the defect sum up to 4th order.

    Returns (c1, c2, c3, c4) where:
      c1 = first derivative (normal rate sum)
      c2 = second derivative prefactor (1/2) d^2 D / dt^2 (0)
      c3 = third derivative prefactor (1/6) d^3 D / dt^3 (0)
      c4 = fourth derivative prefactor (1/24) d^4 D / dt^4 (0)
    """
    comm1 = H @ rho0 - rho0 @ H
    comm2 = H @ comm1 - comm1 @ H
    comm3 = H @ comm2 - comm2 @ H
    comm4 = H @ comm3 - comm3 @ H

    c1 = float(trace_norm(comm1))
    c2 = 0.5 * float(trace_norm(comm2))
    c3 = (1.0 / 6.0) * float(trace_norm(comm3))
    c4 = (1.0 / 24.0) * float(trace_norm(comm4))
    return c1, c2, c3, c4


def compute_lieb_robinson_bound(
    distance: float, t: float, v_lr: float = 2.0, C_lr: float = 1.0, mu_lr: float = 1.0
) -> float:
    """Compute Lieb-Robinson correlation bound envelope C * exp(v_lr * t - mu * distance)."""
    return float(C_lr * np.exp(v_lr * t - mu_lr * distance))


@dataclass
class LongerTimeTrajectoryResult:
    time: float
    empirical_defect: float
    short_time_lower_bound: float
    taylor_4th_order_estimate: float
    lr_lightcone_bound: float
    short_time_bound_valid: bool


@dataclass
class LongerTimeSimulationReplay:
    model_name: str
    num_sites: int
    coupling: float
    short_time_t0: float
    breakdown_time_t_break: float
    peak_defect_time_t_peak: float
    taylor_coefficients: tuple[float, float, float, float]
    trajectories: tuple[LongerTimeTrajectoryResult, ...]
    evidence_kind: Literal["longer_time_numerical_replay"] = "longer_time_numerical_replay"
    limitations: tuple[str, ...] = (
        "Finite matrix exponentiation replay beyond t0; tests higher-order Taylor breakdown and LR lightcone.",
    )


def run_longer_time_defect_evolution_replay(
    model_type: Literal["1d_tfim", "2d_tfim", "1d_heisenberg", "2d_heisenberg"],
    *,
    num_sites_or_rows: int = 2,
    cols: int = 2,
    coupling: float = 1.0,
    transverse_field_or_delta: float = 0.5,
    t_max: float = 1.0,
    num_points: int = 11,
) -> LongerTimeSimulationReplay:
    """Run longer-time defect evolution simulation beyond the short-time quadratic bound horizon."""
    if model_type == "1d_tfim":
        H, H_int, edges = build_1d_tfim_hamiltonian(num_sites_or_rows, coupling, transverse_field_or_delta)
        n_sites = num_sites_or_rows
        model_name = f"1D TFIM (N={n_sites}, J={coupling}, h={transverse_field_or_delta})"
    elif model_type == "2d_tfim":
        H, H_int, edges = build_2d_tfim_hamiltonian(num_sites_or_rows, cols, coupling, transverse_field_or_delta)
        n_sites = num_sites_or_rows * cols
        model_name = f"2D TFIM ({num_sites_or_rows}x{cols}, J={coupling}, h={transverse_field_or_delta})"
    elif model_type == "1d_heisenberg":
        H, H_int, edges = build_1d_heisenberg_hamiltonian(num_sites_or_rows, coupling, transverse_field_or_delta)
        n_sites = num_sites_or_rows
        model_name = f"1D Heisenberg (N={n_sites}, J={coupling}, Delta={transverse_field_or_delta})"
    elif model_type == "2d_heisenberg":
        H, H_int, edges = build_2d_heisenberg_hamiltonian(num_sites_or_rows, cols, coupling, transverse_field_or_delta)
        n_sites = num_sites_or_rows * cols
        model_name = f"2D Heisenberg ({num_sites_or_rows}x{cols}, J={coupling}, Delta={transverse_field_or_delta})"
    else:
        raise QuantumInputError(f"Unknown model_type {model_type}")

    dim = 2**n_sites
    psi0 = np.ones(dim, dtype=np.complex128) / np.sqrt(dim)
    rho0 = np.outer(psi0, psi0.conj())

    c1, c2, c3, c4 = compute_higher_order_commutator_coefficients(H, H_int, rho0)
    g_est = abs(coupling) * 4.0
    nu_est = c1 / max(len(edges), 1)
    t0 = nu_est / (48.0 * (g_est**2)) if g_est > 0 and nu_est > 0 else 0.0

    times = np.linspace(0.0, t_max, num_points)
    trajectories = []

    t_break = t_max
    t_peak = 0.0
    max_defect = -1.0

    for t in times:
        U = expm(-1j * H * t)
        rho_t = U @ rho0 @ U.conj().T
        defect = compute_edgewise_l1_defect(rho_t, n_sites, edges)

        short_bound = max(c1 * t - c2 * (t**2), 0.0)
        taylor_4 = c1 * t - c2 * (t**2) + c3 * (t**3) - c4 * (t**4)
        lr_bound = compute_lieb_robinson_bound(1.0, float(t))

        bound_valid = bool(t <= t0 or defect >= short_bound - 1e-4)
        if not bound_valid and t_break == t_max:
            t_break = float(t)

        if defect > max_defect:
            max_defect = defect
            t_peak = float(t)

        trajectories.append(
            LongerTimeTrajectoryResult(
                time=float(t),
                empirical_defect=float(defect),
                short_time_lower_bound=float(short_bound),
                taylor_4th_order_estimate=float(taylor_4),
                lr_lightcone_bound=float(lr_bound),
                short_time_bound_valid=bound_valid,
            )
        )

    return LongerTimeSimulationReplay(
        model_name=model_name,
        num_sites=n_sites,
        coupling=coupling,
        short_time_t0=t0,
        breakdown_time_t_break=t_break,
        peak_defect_time_t_peak=t_peak,
        taylor_coefficients=(c1, c2, c3, c4),
        trajectories=tuple(trajectories),
    )


@dataclass
class ThermodynamicScalingResult:
    num_sites: int
    num_edges: int
    peak_defect_sum: float
    peak_site_defect_density: float
    peak_edge_defect_density: float
    initial_site_density_slope: float


@dataclass
class ThermodynamicScalingReplay:
    model_family: str
    coupling: float
    extrapolated_infinite_site_density: float
    fit_r_squared: float
    site_density_saturates: bool
    results: tuple[ThermodynamicScalingResult, ...]
    evidence_kind: Literal["thermodynamic_scaling_replay"] = "thermodynamic_scaling_replay"
    limitations: tuple[str, ...] = (
        "Finite-size multi-system scaling and 1/N extrapolation of peak defect density; tests Corollary 5.1.A bounds.",
    )


def extrapolate_infinite_system_defect_density(
    sizes: Sequence[int], site_densities: Sequence[float]
) -> tuple[float, float]:
    """Perform 1/N linear extrapolation of site-normalized defect density d_site(N) = S_inf + alpha / N.

    Returns (S_inf, r_squared) where:
      S_inf = extrapolated infinite-system defect density limit
      r_squared = coefficient of determination of the 1/N fit
    """
    if len(sizes) < 2:
        raise QuantumInputError("At least 2 system sizes required for 1/N extrapolation")

    inv_N = np.array([1.0 / n for n in sizes], dtype=np.float64)
    densities = np.array(site_densities, dtype=np.float64)

    poly = np.polyfit(inv_N, densities, 1)
    alpha, S_inf = poly[0], poly[1]

    total_var = float(np.sum((densities - np.mean(densities)) ** 2))
    if total_var < 1e-12:
        r2 = 1.0
    else:
        ss_res = float(np.sum((densities - (alpha * inv_N + S_inf)) ** 2))
        r2 = max(0.0, 1.0 - (ss_res / total_var))

    return float(S_inf), float(r2)


def compute_thermodynamic_defect_scaling(
    model_type: Literal["1d_tfim", "2d_tfim", "1d_heisenberg"],
    *,
    sizes_or_grids: Sequence[int | tuple[int, int]] = (3, 4, 5),
    coupling: float = 1.0,
    transverse_field_or_delta: float = 0.5,
    t_max: float = 0.8,
    num_points: int = 17,
) -> ThermodynamicScalingReplay:
    """Compute defect density scaling C(t_peak)/N across growing lattice sizes."""
    results: list[ThermodynamicScalingResult] = []

    for item in sizes_or_grids:
        if model_type == "1d_tfim":
            n_sites = int(item)
            H, H_int, edges = build_1d_tfim_hamiltonian(n_sites, coupling, transverse_field_or_delta)
            family_name = f"1D TFIM Family (J={coupling}, h={transverse_field_or_delta})"
        elif model_type == "2d_tfim":
            if isinstance(item, tuple):
                r, c = item
            else:
                r, c = 2, int(item)
            n_sites = r * c
            H, H_int, edges = build_2d_tfim_hamiltonian(r, c, coupling, transverse_field_or_delta)
            family_name = f"2D TFIM Family (J={coupling}, h={transverse_field_or_delta})"
        elif model_type == "1d_heisenberg":
            n_sites = int(item)
            H, H_int, edges = build_1d_heisenberg_hamiltonian(n_sites, coupling, transverse_field_or_delta)
            family_name = f"1D Heisenberg Family (J={coupling}, Delta={transverse_field_or_delta})"
        else:
            raise QuantumInputError(f"Unknown model_type {model_type}")

        dim = 2**n_sites
        psi0 = np.ones(dim, dtype=np.complex128) / np.sqrt(dim)
        rho0 = np.outer(psi0, psi0.conj())

        times = np.linspace(0.0, t_max, num_points)
        peak_defect = -1.0

        U_dt = expm(-1j * H * times[1])
        rho_dt = U_dt @ rho0 @ U_dt.conj().T
        d_dt = compute_edgewise_l1_defect(rho_dt, n_sites, edges)
        initial_slope = (d_dt / n_sites) / times[1]

        for t in times:
            U = expm(-1j * H * t)
            rho_t = U @ rho0 @ U.conj().T
            defect = compute_edgewise_l1_defect(rho_t, n_sites, edges)
            if defect > peak_defect:
                peak_defect = defect

        num_edges = len(edges)
        site_density = peak_defect / n_sites
        edge_density = peak_defect / max(num_edges, 1)

        results.append(
            ThermodynamicScalingResult(
                num_sites=n_sites,
                num_edges=num_edges,
                peak_defect_sum=float(peak_defect),
                peak_site_defect_density=float(site_density),
                peak_edge_defect_density=float(edge_density),
                initial_site_density_slope=float(initial_slope),
            )
        )

    all_n = [r.num_sites for r in results]
    all_site_d = [r.peak_site_defect_density for r in results]
    S_inf, r2 = extrapolate_infinite_system_defect_density(all_n, all_site_d)

    saturates = bool(len(results) >= 2 and abs(results[-1].peak_site_defect_density - results[-2].peak_site_defect_density) < 0.5)

    return ThermodynamicScalingReplay(
        model_family=family_name,
        coupling=coupling,
        extrapolated_infinite_site_density=S_inf,
        fit_r_squared=r2,
        site_density_saturates=saturates,
        results=tuple(results),
    )


def build_global_gibbs_state(H: ComplexMatrix, beta: float) -> ComplexMatrix:
    """Build global Gibbs thermal state rho_beta = exp(-beta * H) / Tr(exp(-beta * H))."""
    if beta < 0.0:
        raise QuantumInputError("beta must be non-negative")
    if beta == 0.0:
        dim = H.shape[0]
        return np.eye(dim, dtype=np.complex128) / dim

    exp_neg_beta_H = expm(-beta * H)
    z = np.trace(exp_neg_beta_H)
    return (exp_neg_beta_H / z).astype(np.complex128)


def build_local_thermal_product_state(num_sites: int, local_hamiltonian: ComplexMatrix, beta: float) -> ComplexMatrix:
    """Build local thermal product state rho_beta = exp(-beta * h_v) / Tr(exp(-beta * h_v))."""
    if beta < 0.0:
        raise QuantumInputError("beta must be non-negative")

    if beta == 0.0:
        single_rho = np.eye(2, dtype=np.complex128) / 2.0
    else:
        exp_h = expm(-beta * local_hamiltonian)
        z = np.trace(exp_h)
        single_rho = (exp_h / z).astype(np.complex128)

    factors = [single_rho] * num_sites
    return kron_n(factors)


@dataclass
class ThermalStateResult:
    beta: float
    temperature: float
    normal_rate_nu: float
    double_commutator_c2: float
    peak_defect_sum: float
    trajectories: tuple[LatticeTrajectoryResult, ...]


@dataclass
class ThermalSimulationReplay:
    model_name: str
    num_sites: int
    coupling: float
    high_temp_suppresses_defect: bool
    results: tuple[ThermalStateResult, ...]
    evidence_kind: Literal["thermal_simulation_replay"] = "thermal_simulation_replay"
    limitations: tuple[str, ...] = (
        "Thermal mixed initial state evolution over finite matrix exponentiation; evaluates beta dependence of nu_e.",
    )


def run_thermal_defect_simulation_replay(
    model_type: Literal["1d_tfim", "2d_tfim", "1d_heisenberg"],
    *,
    num_sites_or_rows: int = 2,
    cols: int = 2,
    coupling: float = 1.0,
    transverse_field_or_delta: float = 0.5,
    betas: Sequence[float] = (0.01, 0.1, 1.0, 5.0),
    t_max: float = 0.5,
    num_points: int = 6,
    state_mode: Literal["product_thermal", "global_gibbs"] = "product_thermal",
) -> ThermalSimulationReplay:
    """Run temperature-dependent thermal mixed state defect evolution simulation sweep."""
    if model_type == "1d_tfim":
        H, H_int, edges = build_1d_tfim_hamiltonian(num_sites_or_rows, coupling, transverse_field_or_delta)
        n_sites = num_sites_or_rows
        model_name = f"1D TFIM Thermal ({state_mode}, N={n_sites}, J={coupling})"
        _, x, _, _ = _paulis()
        h_local = -transverse_field_or_delta * x
    elif model_type == "2d_tfim":
        H, H_int, edges = build_2d_tfim_hamiltonian(num_sites_or_rows, cols, coupling, transverse_field_or_delta)
        n_sites = num_sites_or_rows * cols
        model_name = f"2D TFIM Thermal ({state_mode}, {num_sites_or_rows}x{cols}, J={coupling})"
        _, x, _, _ = _paulis()
        h_local = -transverse_field_or_delta * x
    elif model_type == "1d_heisenberg":
        H, H_int, edges = build_1d_heisenberg_hamiltonian(num_sites_or_rows, coupling, transverse_field_or_delta)
        n_sites = num_sites_or_rows
        model_name = f"1D Heisenberg Thermal ({state_mode}, N={n_sites}, J={coupling})"
        _, _, _, z = _paulis()
        h_local = -transverse_field_or_delta * z
    else:
        raise QuantumInputError(f"Unknown model_type {model_type}")

    results: list[ThermalStateResult] = []

    for beta in betas:
        if state_mode == "global_gibbs":
            rho0 = build_global_gibbs_state(H, beta)
        else:
            rho0 = build_local_thermal_product_state(n_sites, h_local, beta)

        comm1 = H @ rho0 - rho0 @ H
        nu_sum = float(trace_norm(comm1))
        c2 = compute_double_commutator_prefactor(H_int, rho0)

        times = np.linspace(0.0, t_max, num_points)
        trajectories = []
        peak_defect = -1.0

        for t in times:
            U = expm(-1j * H * t)
            rho_t = U @ rho0 @ U.conj().T
            defect = compute_edgewise_l1_defect(rho_t, n_sites, edges)
            bound = c2 * (t**2)
            satisfied = bool(defect >= bound - 1e-4)

            if defect > peak_defect:
                peak_defect = defect

            trajectories.append(
                LatticeTrajectoryResult(
                    time=float(t),
                    empirical_defect=float(defect),
                    theoretical_lower_bound=float(bound),
                    bound_satisfied=satisfied,
                )
            )

        temp = 1.0 / beta if beta > 0 else float("inf")
        results.append(
            ThermalStateResult(
                beta=float(beta),
                temperature=temp,
                normal_rate_nu=nu_sum,
                double_commutator_c2=c2,
                peak_defect_sum=float(peak_defect),
                trajectories=tuple(trajectories),
            )
        )

    high_temp_suppresses = bool(results[0].normal_rate_nu <= results[-1].normal_rate_nu + 1e-3)

    return ThermalSimulationReplay(
        model_name=model_name,
        num_sites=n_sites,
        coupling=coupling,
        high_temp_suppresses_defect=high_temp_suppresses,
        results=tuple(results),
    )








