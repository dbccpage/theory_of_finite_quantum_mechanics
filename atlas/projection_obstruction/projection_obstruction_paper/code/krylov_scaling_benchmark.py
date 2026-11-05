"""Finite floating-point diagnostics for product mean-field trajectories.

Sampled normal-rate quadrature is an estimate, without an integration or ODE
error certificate. The separate interaction-norm envelope uses the analytic
inequality nu_e <= 2 ||h_e|| <= 2 (|Jxx| + |Jyy| + |Jzz|) for normalized pure
product states along the ideal mean-field flow. Sparse evolution and fourth-order
Taylor jets remain numerical calculations, not certified quantum theorems.
The coefficient ratio sqrt(c2 / |c4|) is a diagnostic, not a validity horizon.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

import numpy as np
import numpy.typing as npt
import scipy.sparse as sp
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.sparse.linalg import expm_multiply

ComplexMatrix = npt.NDArray[np.complex128]
ComplexVector = npt.NDArray[np.complex128]
RealVector = npt.NDArray[np.float64]

SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=np.complex128)
SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
IDENTITY_2 = np.eye(2, dtype=np.complex128)

SPARSE_X = sp.csr_matrix(SIGMA_X)
SPARSE_Y = sp.csr_matrix(SIGMA_Y)
SPARSE_Z = sp.csr_matrix(SIGMA_Z)
SPARSE_ID = sp.eye(2, dtype=np.complex128, format="csr")


@dataclass(frozen=True)
class SpinChainModel:
    """Specification of a spin-1/2 lattice model with general bond connectivity."""

    num_qubits: int
    j_xx: float = 0.0
    j_yy: float = 0.0
    j_zz: float = 1.0
    hx: float = 0.0
    hy: float = 0.0
    hz: float = 0.0
    periodic: bool = False
    site_hx: Sequence[float] | None = None
    site_hz: Sequence[float] | None = None
    bond_jzz: Sequence[float] | None = None
    bonds: Sequence[tuple[int, int]] | None = None

    def get_bonds(self) -> Sequence[tuple[int, int]]:
        """Return the list of interacting pairs (site_a, site_b)."""
        if self.bonds is not None:
            return self.bonds
        num_bonds = self.num_qubits if self.periodic else self.num_qubits - 1
        return [(i, (i + 1) % self.num_qubits) for i in range(num_bonds)]

    def get_bond_jzz(self, bond_idx: int) -> float:
        """Return the J_zz coupling for a given bond."""
        if self.bond_jzz is not None and bond_idx < len(self.bond_jzz):
            return float(self.bond_jzz[bond_idx])
        return self.j_zz

    def get_site_hx(self, site_idx: int) -> float:
        """Return transverse field h_x on site_idx."""
        if self.site_hx is not None and site_idx < len(self.site_hx):
            return float(self.site_hx[site_idx])
        return self.hx

    def get_site_hz(self, site_idx: int) -> float:
        """Return longitudinal field h_z on site_idx."""
        if self.site_hz is not None and site_idx < len(self.site_hz):
            return float(self.site_hz[site_idx])
        return self.hz


def build_2d_grid_model(
    rows: int,
    cols: int,
    j_zz: float = 1.0,
    hx: float = 0.8,
    lattice_type: str = "square",
) -> tuple[SpinChainModel, int]:
    """Construct a 2D grid model partitioned vertically into two equal halves.

    Sites are ordered such that columns 0..cols//2-1 (subsystem A) come first,
    followed by columns cols//2..cols-1 (subsystem B). Returns (model, cut_site).
    """
    col_mid = cols // 2
    a_pos = [(r, c) for r in range(rows) for c in range(col_mid)]
    b_pos = [(r, c) for r in range(rows) for c in range(col_mid, cols)]
    pos_to_idx = {pos: i for i, pos in enumerate(a_pos + b_pos)}

    bonds: list[tuple[int, int]] = []
    for r in range(rows):
        for c in range(cols):
            p1 = (r, c)
            i1 = pos_to_idx[p1]
            if c + 1 < cols:
                p2 = (r, c + 1)
                i2 = pos_to_idx[p2]
                bonds.append((i1, i2))
            if r + 1 < rows:
                p2 = (r + 1, c)
                i2 = pos_to_idx[p2]
                bonds.append((i1, i2))
            if lattice_type == "triangular" and r + 1 < rows and c + 1 < cols:
                p2 = (r + 1, c + 1)
                i2 = pos_to_idx[p2]
                bonds.append((i1, i2))

    total_qubits = len(a_pos + b_pos)
    cut_site = len(a_pos) - 1
    model = SpinChainModel(num_qubits=total_qubits, j_zz=j_zz, hx=hx, bonds=bonds)
    return model, cut_site


def build_sparse_hamiltonian(model: SpinChainModel) -> sp.csr_matrix:
    """Construct the exact 2^N x 2^N sparse CSR Hamiltonian for the spin lattice."""
    n = model.num_qubits
    dim = 1 << n
    hamiltonian = sp.csr_matrix((dim, dim), dtype=np.complex128)

    bonds = model.get_bonds()
    for bond_idx, (site_a, site_b) in enumerate(bonds):
        jzz = model.get_bond_jzz(bond_idx)

        for pauli, coeff in (
            (SPARSE_X, model.j_xx),
            (SPARSE_Y, model.j_yy),
            (SPARSE_Z, jzz),
        ):
            if abs(coeff) < 1.0e-14:
                continue
            ops = [SPARSE_ID] * n
            ops[site_a] = pauli
            ops[site_b] = pauli
            term = ops[0]
            for op in ops[1:]:
                term = sp.kron(term, op, format="csr")
            hamiltonian += coeff * term

    for site in range(n):
        hx_val = model.get_site_hx(site)
        hy_val = model.hy
        hz_val = model.get_site_hz(site)

        for pauli, coeff in (
            (SPARSE_X, hx_val),
            (SPARSE_Y, hy_val),
            (SPARSE_Z, hz_val),
        ):
            if abs(coeff) < 1.0e-14:
                continue
            ops = [SPARSE_ID] * n
            ops[site] = pauli
            term = ops[0]
            for op in ops[1:]:
                term = sp.kron(term, op, format="csr")
            hamiltonian += coeff * term

    return hamiltonian


def build_initial_product_state(
    site_states: Sequence[ComplexVector],
) -> tuple[ComplexVector, list[ComplexVector]]:
    """Normalize site vectors and compute their full 2^N tensor product vector."""
    if not site_states:
        raise ValueError("at least one site vector is required")
    normalized_sites = []
    for vector in site_states:
        v = np.asarray(vector, dtype=np.complex128)
        if v.shape != (2,) or not np.all(np.isfinite(v)):
            raise ValueError("site vectors must contain two finite amplitudes")
        magnitude = float(np.max(np.abs(v)))
        if magnitude == 0.0:
            raise ValueError("site vectors must be nonzero")
        scaled = v / magnitude
        normalized_sites.append(scaled / float(np.linalg.norm(scaled)))
    full_state = normalized_sites[0]
    for v in normalized_sites[1:]:
        full_state = np.kron(full_state, v)
    return full_state, normalized_sites


def solve_mean_field_trajectory(
    model: SpinChainModel,
    initial_sites: Sequence[ComplexVector],
    times: RealVector,
    rtol: float = 1.0e-9,
    atol: float = 1.0e-9,
) -> list[list[ComplexVector]]:
    """Integrate self-consistent product mean-field equations of motion."""
    n = model.num_qubits
    if len(initial_sites) != n:
        raise ValueError("initial site count must match the model")
    times = _time_grid(times)
    _, initial_sites = build_initial_product_state(initial_sites)
    if len(times) == 1:
        return [initial_sites]
    bonds = model.get_bonds()

    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for bond_idx, (sa, sb) in enumerate(bonds):
        adj[sa].append((sb, bond_idx))
        adj[sb].append((sa, bond_idx))

    def rhs(t: float, y: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        c_y = y[: 2 * n] + 1.0j * y[2 * n :]
        u = c_y.reshape((n, 2))

        # Compute instantaneous expectations
        sx_vals = [float(np.real(u[i].conj() @ (SIGMA_X @ u[i]))) for i in range(n)]
        sy_vals = [float(np.real(u[i].conj() @ (SIGMA_Y @ u[i]))) for i in range(n)]
        sz_vals = [float(np.real(u[i].conj() @ (SIGMA_Z @ u[i]))) for i in range(n)]

        dudt = np.zeros_like(u)
        for i in range(n):
            eff_hx = model.get_site_hx(i)
            eff_hy = model.hy
            eff_hz = model.get_site_hz(i)

            for nb, bond_idx in adj[i]:
                eff_hx += model.j_xx * sx_vals[nb]
                eff_hy += model.j_yy * sy_vals[nb]
                eff_hz += model.get_bond_jzz(bond_idx) * sz_vals[nb]

            h_eff = eff_hx * SIGMA_X + eff_hy * SIGMA_Y + eff_hz * SIGMA_Z
            # Remove scalar phase drift to ensure strict norm preservation
            e_scalar = float(np.real(u[i].conj() @ (h_eff @ u[i])))
            dudt[i] = -1.0j * (h_eff @ u[i] - e_scalar * u[i])

        d_flat = dudt.flatten()
        return np.concatenate([np.real(d_flat), np.imag(d_flat)])

    y0_c = np.array(initial_sites, dtype=np.complex128).flatten()
    y0 = np.concatenate([np.real(y0_c), np.imag(y0_c)])

    t_span = (float(times[0]), float(times[-1]))
    sol = solve_ivp(rhs, t_span, y0, t_eval=times, rtol=rtol, atol=atol)
    if not sol.success:
        raise RuntimeError("mean-field integration failed: " + sol.message)

    trajectory: list[list[ComplexVector]] = []
    for step_idx in range(len(times)):
        c_vec = sol.y[: 2 * n, step_idx] + 1.0j * sol.y[2 * n :, step_idx]
        site_array = c_vec.reshape((n, 2))
        normalized = [site_array[i] / float(np.linalg.norm(site_array[i])) for i in range(n)]
        trajectory.append(normalized)

    return trajectory


def compute_edge_normal_defects(
    model: SpinChainModel,
    sites: Sequence[ComplexVector],
) -> list[float]:
    """Compute instantaneous local normal defects nu_e = 2 * ||chi_e|| for all bonds."""
    bonds = model.get_bonds()
    defects: list[float] = []

    for bond_idx, (site_a, site_b) in enumerate(bonds):
        ua = sites[site_a]
        ub = sites[site_b]

        pa = np.outer(ua, ua.conj())
        pb = np.outer(ub, ub.conj())
        qa = IDENTITY_2 - pa
        qb = IDENTITY_2 - pb
        q_ab = np.kron(qa, qb)

        jzz = model.get_bond_jzz(bond_idx)
        h_ab = (
            model.j_xx * np.kron(SIGMA_X, SIGMA_X)
            + model.j_yy * np.kron(SIGMA_Y, SIGMA_Y)
            + jzz * np.kron(SIGMA_Z, SIGMA_Z)
        )
        chi_ab = q_ab @ (h_ab @ np.kron(ua, ub))
        nu_e = 2.0 * float(np.linalg.norm(chi_ab))
        defects.append(nu_e)

    return defects


def _time_grid(times: RealVector) -> RealVector:
    grid = np.asarray(times, dtype=np.float64)
    if (
        grid.ndim != 1
        or len(grid) == 0
        or not np.all(np.isfinite(grid))
        or grid[0] != 0.0
        or np.any(np.diff(grid) <= 0.0)
    ):
        raise ValueError("times must start at zero and increase strictly")
    return grid


def compute_cumulative_duhamel_estimate(
    model: SpinChainModel,
    mf_trajectory: Sequence[Sequence[ComplexVector]],
    times: RealVector,
) -> RealVector:
    """Sampled trapezoidal quadrature; it can underestimate the actual integral."""
    times = _time_grid(times)
    if len(mf_trajectory) != len(times):
        raise ValueError("trajectory and time grid lengths must match")
    rates = np.array([sum(compute_edge_normal_defects(model, u)) for u in mf_trajectory])
    return cumulative_trapezoid(rates, times, initial=0.0)


def compute_cumulative_duhamel_bound(
    model: SpinChainModel,
    mf_trajectory: Sequence[Sequence[ComplexVector]],
    times: RealVector,
) -> RealVector:
    """Conservative interaction-norm envelope for the ideal pure-product flow.

    The analytic Duhamel argument and nu_e <= 2 ||h_e|| give
    min(2, 2 t sum_e (|Jxx| + |Jyy| + |Jzz_e|)). This does not use sampled
    quadrature. Floating-point evaluation and numerical trajectories are not
    enclosed: the returned numbers carry no numerical certification claim.
    """
    times = _time_grid(times)
    if len(mf_trajectory) != len(times):
        raise ValueError("trajectory and time grid lengths must match")
    strength = sum(
        abs(model.j_xx) + abs(model.j_yy) + abs(model.get_bond_jzz(i))
        for i, _ in enumerate(model.get_bonds())
    )
    if not np.isfinite(strength):
        raise ValueError("interaction strengths must be finite")
    return np.minimum(2.0, 2.0 * strength * times)


def evolve_exact_krylov(
    hamiltonian: sp.csr_matrix,
    initial_full_state: ComplexVector,
    times: RealVector,
) -> list[ComplexVector]:
    """Compute exact time evolution |psi(t)> = exp(-i H t) |psi0> using Krylov iteration."""
    states: list[ComplexVector] = []
    for t in times:
        if abs(t) < 1.0e-15:
            states.append(initial_full_state.copy())
        else:
            psi_t = expm_multiply(-1.0j * hamiltonian * float(t), initial_full_state)
            norm_val = float(np.linalg.norm(psi_t))
            states.append(psi_t / norm_val)
    return states


def compute_trace_distance_pure(psi: ComplexVector, phi: ComplexVector) -> float:
    """Return the full trace norm, 2 sqrt(1 - |<psi|phi>|^2), for unit vectors.

    The conventional trace distance is half this value.
    """
    overlap = float(abs(np.vdot(psi, phi)))
    overlap = min(1.0, max(0.0, overlap))
    return float(2.0 * np.sqrt(max(0.0, 1.0 - overlap * overlap)))


def compute_local_z_expectation(psi: ComplexVector, site: int, num_qubits: int) -> float:
    """Compute <psi | sigma_site^z | psi> in O(2^N) time using bitwise indexing."""
    dim = len(psi)
    probs = np.abs(psi) ** 2
    shift = num_qubits - 1 - site
    indices = np.arange(dim, dtype=np.int64)
    bits = (indices >> shift) & 1
    signs = 1.0 - 2.0 * bits
    return float(np.dot(probs, signs))


def compute_bipartite_linear_entropy(psi: ComplexVector, cut_site: int, num_qubits: int) -> float:
    """Compute linear entropy S_L(rho_A) = 1 - Tr(rho_A^2) for cut between cut_site and cut_site+1."""
    dim_a = 1 << (cut_site + 1)
    dim_b = 1 << (num_qubits - 1 - cut_site)
    psi_matrix = psi.reshape((dim_a, dim_b))
    rho_a = psi_matrix @ psi_matrix.conj().T
    purity = float(np.real(np.trace(rho_a @ rho_a)))
    return float(max(0.0, 1.0 - purity))


@dataclass(frozen=True)
class EntropyExpansion:
    """Floating-point entropy coefficients and an optional quartic crossover.

    An unavailable ratio is not an infinite validity interval. The roundoff
    screen is a numerical heuristic, not a validated coefficient enclosure.
    """

    c2: float
    c3: float
    c4: float
    quartic_crossover_time: float | None
    quartic_status: Literal["available", "quartic_unresolved", "quadratic_unresolved"]


def compute_entropy_expansion(
    model: SpinChainModel,
    initial_sites: Sequence[ComplexVector],
    cut_site: int,
) -> EntropyExpansion:
    """Compute pure-site-product entropy jets and a quartic crossover diagnostic.

    The ratio compares only quadratic and quartic terms. It does not control
    a cubic term, higher orders or cancellations, or isolate bulk transport.
    Coefficients near cancellation are retained as computed, but the ratio
    is unavailable when either term is unresolved by a roundoff heuristic.
    No fitting window, exact arithmetic or Taylor remainder enclosure is used.
    """
    if len(initial_sites) != model.num_qubits:
        raise ValueError("initial site count must match the model")
    if not 0 <= cut_site < model.num_qubits - 1:
        raise ValueError("cut must split the system into two nonempty parts")
    hamiltonian = build_sparse_hamiltonian(model)
    full_state, _ = build_initial_product_state(initial_sites)
    # Scale and remove the scalar energy before generating the jets. Purity is
    # phase invariant; dimensionless jets avoid a Hamiltonian-dependent fit.
    scale = float(np.max(np.asarray(abs(hamiltonian).sum(axis=1))))
    if not np.isfinite(scale):
        raise ValueError("Hamiltonian must have finite entries")
    if scale == 0.0:
        return EntropyExpansion(0.0, 0.0, 0.0, None, "quadratic_unresolved")
    scaled_h = hamiltonian / scale
    energy = float(np.real(np.vdot(full_state, scaled_h @ full_state)))
    jets = [full_state]
    for degree in range(1, 5):
        jets.append(-1j * (scaled_h @ jets[-1] - energy * jets[-1]) / degree)
    da, db = 1 << (cut_site + 1), 1 << (model.num_qubits - cut_site - 1)
    matrices = [v.reshape(da, db) for v in jets]
    if da > db:
        matrices = [m.T for m in matrices]
    rho = [sum(matrices[k] @ matrices[n - k].conj().T for k in range(n + 1)) for n in range(5)]
    coefficients = []
    roundoff_screens = []
    for n in (2, 3, 4):
        terms = [np.sum(rho[k] * rho[n - k].T) for k in range(n + 1)]
        coefficients.append(-float(np.real(sum(terms))) * scale**n)
        # Screen cancellation in dimensionless jets before restoring units.
        # This deliberately does not declare a small coefficient exactly zero.
        magnitude = max(1.0, sum(abs(term) for term in terms))
        roundoff_screens.append(64 * np.finfo(float).eps * magnitude * scale**n)
    c2, c3, c4 = coefficients
    if c2 <= roundoff_screens[0]:
        return EntropyExpansion(c2, c3, c4, None, "quadratic_unresolved")
    if abs(c4) <= roundoff_screens[2]:
        return EntropyExpansion(c2, c3, c4, None, "quartic_unresolved")
    crossover = float(np.sqrt(c2 / abs(c4)))
    return EntropyExpansion(c2, c3, c4, crossover, "available")


def compute_higher_order_expansion_and_timescale(
    model: SpinChainModel,
    initial_sites: Sequence[ComplexVector],
    cut_site: int,
    ts: RealVector | None = None,
) -> tuple[float, float, float, float]:
    """Compatibility wrapper returning c2, c3, c4 and the quartic diagnostic.

    The legacy ts argument is ignored. An unavailable diagnostic is NaN, never
    an infinite validity interval. Use compute_entropy_expansion for its status.
    """
    result = compute_entropy_expansion(model, initial_sites, cut_site)
    crossover = result.quartic_crossover_time
    return result.c2, result.c3, result.c4, float("nan") if crossover is None else crossover


@dataclass(frozen=True)
class ScalingBenchmarkResult:
    """Numerical comparison; validity flags mean sampled inequalities only."""

    num_qubits: int
    model_name: str
    t_max: float
    num_steps: int
    is_duhamel_bound_valid: bool
    is_observable_bound_valid: bool
    max_trace_distance: float
    max_observable_error: float
    max_duhamel_bound: float
    mean_sharpness_ratio: float
    execution_time_seconds: float
    max_duhamel_estimate: float
    numerical_error_certified: bool = False


def run_single_scaling_benchmark(
    model: SpinChainModel,
    initial_sites: Sequence[ComplexVector],
    model_name: str,
    t_max: float = 0.2,
    num_steps: int = 5,
) -> ScalingBenchmarkResult:
    """Execute a single scaling benchmark comparing Duhamel bound against exact Krylov."""
    import time

    start_time = time.time()
    times = np.linspace(0.0, t_max, num_steps, dtype=np.float64)

    hamiltonian = build_sparse_hamiltonian(model)
    psi0, initial_sites = build_initial_product_state(initial_sites)

    psi_exact_list = evolve_exact_krylov(hamiltonian, psi0, times)
    mf_trajectory = solve_mean_field_trajectory(model, initial_sites, times)
    duhamel_bounds = compute_cumulative_duhamel_bound(model, mf_trajectory, times)
    duhamel_estimates = compute_cumulative_duhamel_estimate(model, mf_trajectory, times)

    max_dist = 0.0
    max_obs_err = 0.0
    bound_valid = True
    obs_valid = True
    ratios: list[float] = []

    for step in range(1, num_steps):
        psi_ex = psi_exact_list[step]
        sites_mf = mf_trajectory[step]

        # Product state full vector
        psi_mf = sites_mf[0]
        for s in sites_mf[1:]:
            psi_mf = np.kron(psi_mf, s)

        tr_dist = compute_trace_distance_pure(psi_ex, psi_mf)
        bound = float(duhamel_bounds[step])

        # Observable error on central site
        center = model.num_qubits // 2
        obs_ex = compute_local_z_expectation(psi_ex, center, model.num_qubits)
        obs_mf = float(np.real(sites_mf[center].conj() @ (SIGMA_Z @ sites_mf[center])))
        obs_err = abs(obs_ex - obs_mf)

        max_dist = max(max_dist, tr_dist)
        max_obs_err = max(max_obs_err, obs_err)

        if bound < tr_dist - 1.0e-7:
            bound_valid = False
        if bound < obs_err - 1.0e-7:
            obs_valid = False

        if tr_dist > 1.0e-8:
            ratios.append(bound / tr_dist)

    mean_ratio = float(np.mean(ratios)) if ratios else 1.0
    duration = time.time() - start_time

    return ScalingBenchmarkResult(
        num_qubits=model.num_qubits,
        model_name=model_name,
        t_max=t_max,
        num_steps=num_steps,
        is_duhamel_bound_valid=bound_valid,
        is_observable_bound_valid=obs_valid,
        max_trace_distance=max_dist,
        max_observable_error=max_obs_err,
        max_duhamel_bound=float(duhamel_bounds[-1]),
        mean_sharpness_ratio=mean_ratio,
        execution_time_seconds=duration,
        max_duhamel_estimate=float(duhamel_estimates[-1]),
    )
