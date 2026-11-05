"""Cochain Holonomy Bridge linking PO-034 higher-cell projections to PO-035 boundary cochains.

AuthorityEffect: None.

This module formalizes Phase 3 of the Cycles 005-007 integration plan:
1. Product tangent projector P preserves all single-site marginals (PO-034 Theorem C1).
   Tr_{\\setminus j}[P(Z)] = Tr_{\\setminus j}[Z] for all single sites j.
   Consequently, normal defect projector Q = I - P has vanishing single-site marginal traces:
   Tr_{\\setminus j}[Q(Z)] = 0 for all single sites j.
2. Defect velocity nu = ||Q [H, rho]||_1:
   - For 1-local Hamiltonians H = sum_j h_j, Q([H, rho]) = 0 and nu = 0.
   - For 2-site entangling interactions H_{12}, Q([H_{12}, rho]) != 0 and nu > 0.
   - Single-site marginals of Q([H_{12}, rho]) vanish identically, confirming that local
     marginal observers see zero instantaneous change from the entangling defect speed
     (the algebraic core of Cycle 007's no-signalling theorem).
3. Simplicial cochain mapping:
   - Maps 2-site interaction terms on a simplicial complex K (e.g. a 3-simplex cell)
     to an edge 1-cochain delta in C^1(K).
   - Boundary face holonomies Gamma_2 = d^1 delta in C^2(K) measure circulation around faces.
   - Rate of holonomy accumulation across face boundaries is bounded by the entangling
     defect velocities nu_e on boundary edges.
4. Quotient stickiness via HiGHS linear programming (or least squares):
   - inf_alpha ||delta - d^0 alpha||_1 measures irreducible holonomy / projection friction
     that cannot be gauged away by local site phase rotations (PO-035).
5. Discrete-to-continuum membrane firewall (Cycle 006):
   - Rational bone holonomies Gamma_2 in Q/Z (finite torsion) are algebraically fenced
     from continuous U(1) gauge rotation whose kernel lattice ker(exp) = 2*pi*Z is infinite.
   - Forbids identifying discrete torsion with U(1) without an explicit Level-Q membrane contract.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np

from ._validation import integer, matrix, nonnegative, reference
from .defect_bounds import schatten_1_norm
from .k_cell_retraction import (
    embed_local_operator,
    k_cell_normal_projector,
    k_cell_tangent_projector,
    partial_trace_keep_single,
    tensor_product_list,
    verify_marginal_preservation,
)
from .simplicial_complex import (
    SimplicialComplex,
    simplicial_coboundary_matrix,
)

try:
    from scipy.optimize import linprog

    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DefectVelocityResult:
    """Result of product tangent-normal decomposition on an operator perturbation."""

    defect_velocity_nu: float
    tangent_norm: float
    normal_norm: float
    single_site_marginal_traces_normal: tuple[float, ...]
    marginal_preservation_passed: bool
    normal_annihilation_passed: bool
    evidence_scope: str = "product tangent-normal decomposition (PO-034 Theorem C1, C3)"


@dataclass(frozen=True)
class QuotientStickinessResult:
    """Result of quotient residual repair inf_alpha ||delta - d^0 alpha||_1."""

    raw_norm: float
    quotient_residual: float
    optimal_gauge: np.ndarray
    repaired_cochain: np.ndarray
    curvature_residual: float
    is_pure_gauge: bool
    status: str
    evidence_scope: str = "relational quotient repair (PO-035)"


@dataclass(frozen=True)
class HolonomyAccumulationReport:
    """Report linking higher-cell quantum defect velocity to boundary cochain holonomies."""

    complex_dimension: int
    num_nodes: int
    num_edges: int
    num_faces: int
    edge_cochain: np.ndarray
    face_holonomies: np.ndarray
    defect_velocity_total: float
    max_face_holonomy_rate: float
    quotient_stickiness_l1: float
    is_pure_gauge: bool
    terminal_status: str
    evidence_scope: str = "higher-cell relational cochain holonomy bridge (PO-034 <-> PO-035)"


@dataclass(frozen=True)
class DiscreteContinuumMembrane:
    """Discrete-to-continuum membrane fence distinguishing Q/Z torsion from U(1)."""

    rational_holonomy: tuple[int, int]
    continuous_phase_angle: float
    kernel_lattice: str = "2*pi*Z (infinite non-torsion lattice, Cycle 006)"
    discrete_group: str = "Z_N (finite cyclic torsion group)"
    membrane_authorized: bool = False
    status: str = "REFUSAL"
    refusal_reason: str | None = None
    evidence_scope: str = "discrete-to-continuum membrane fence (Cycle 006 <-> PO-035)"


# ---------------------------------------------------------------------------
# Core Bridge Functions
# ---------------------------------------------------------------------------


def evaluate_hamiltonian_defect_velocity(
    hamiltonian: np.ndarray,
    marginals: Sequence[np.ndarray],
    dims: Sequence[int],
    tol: float = 1e-11,
) -> DefectVelocityResult:
    """Evaluate product tangent-normal decomposition and entangling defect velocity nu.

    Computes Z = -i [H, rho], P(Z), Q(Z), and nu = ||Q(Z)||_1.
    Checks marginal preservation and normal marginal annihilation.
    """
    tol = nonnegative(tol, "tol")
    ds, rhos = reference(marginals, dims)
    size = math.prod(ds)
    h = matrix(hamiltonian, "hamiltonian", (size, size))
    if not np.allclose(h, h.conj().T, atol=tol, rtol=0):
        raise ValueError("Hamiltonian must be Hermitian")

    rho = tensor_product_list(rhos)
    z = -1j * (h @ rho - rho @ h)
    pz = k_cell_tangent_projector(z, rhos, ds)
    qz = k_cell_normal_projector(z, rhos, ds)

    nu = schatten_1_norm(qz)
    t_norm = schatten_1_norm(pz)
    n_norm = nu

    traces = tuple(
        float(np.linalg.norm(partial_trace_keep_single(qz, ds, j), ord="fro"))
        for j in range(len(ds))
    )
    preservation = verify_marginal_preservation(z, rhos, ds, tol=tol)
    annihilation = all(t <= tol for t in traces)

    return DefectVelocityResult(
        defect_velocity_nu=nu,
        tangent_norm=t_norm,
        normal_norm=n_norm,
        single_site_marginal_traces_normal=traces,
        marginal_preservation_passed=preservation,
        normal_annihilation_passed=annihilation,
    )


def build_3simplex_cell_complex() -> SimplicialComplex:
    """Construct canonical 3-simplex cell Delta^3 on 4 vertices {0, 1, 2, 3}."""
    return SimplicialComplex([(0, 1, 2, 3)])


def map_edge_interactions_to_cochain(
    complex_: SimplicialComplex,
    edge_couplings: Mapping[tuple[int, int], float],
) -> np.ndarray:
    """Map pairwise coupling strengths to an oriented 1-cochain delta in C^1(K)."""
    edges = complex_.get_simplices(1)
    edge_index = {e: i for i, e in enumerate(edges)}
    delta = np.zeros(len(edges), dtype=np.float64)

    for (u, v), strength in edge_couplings.items():
        val = float(strength)
        if not math.isfinite(val):
            raise ValueError(f"coupling for edge ({u}, {v}) must be finite")
        if (u, v) in edge_index:
            delta[edge_index[(u, v)]] += val
        elif (v, u) in edge_index:
            delta[edge_index[(v, u)]] -= val
        else:
            raise ValueError(f"edge ({u}, {v}) not found in simplicial complex")

    return delta


def compute_boundary_face_holonomies(
    complex_: SimplicialComplex,
    edge_cochain: np.ndarray,
) -> np.ndarray:
    """Compute face holonomies Gamma_2 = d^1 delta in C^2(K)."""
    d1 = simplicial_coboundary_matrix(complex_, 1)
    cochain = np.asarray(edge_cochain, dtype=np.float64)
    if cochain.shape != (complex_.num_simplices(1),):
        raise ValueError(
            f"edge_cochain shape {cochain.shape} must match num_edges {complex_.num_simplices(1)}"
        )
    return d1 @ cochain


def compute_quotient_stickiness_lp(
    d0: np.ndarray,
    delta: np.ndarray,
    d1: np.ndarray | None = None,
    tol: float = 1e-10,
) -> QuotientStickinessResult:
    """Compute quotient residual inf_alpha ||delta - d^0 alpha||_1 and classify status.

    Uses HiGHS linear programming when SciPy is available, or least-squares fallback.
    """
    tol = nonnegative(tol, "tol")
    delta_arr = np.asarray(delta, dtype=np.float64)
    m_edges, n_nodes = d0.shape
    if delta_arr.shape != (m_edges,):
        raise ValueError(f"delta shape {delta_arr.shape} does not match d0 rows {m_edges}")

    raw_norm = float(np.sum(np.abs(delta_arr)))

    if m_edges == 0 or n_nodes == 0:
        return QuotientStickinessResult(
            raw_norm=raw_norm,
            quotient_residual=raw_norm,
            optimal_gauge=np.zeros(n_nodes, dtype=np.float64),
            repaired_cochain=delta_arr.copy(),
            curvature_residual=0.0,
            is_pure_gauge=bool(raw_norm <= tol),
            status="AUTHORIZED" if raw_norm <= tol else "OBSTRUCTED",
        )

    if _HAS_SCIPY:
        # Variables: x = [alpha_0, ..., alpha_{n-1}, t_0, ..., t_{m-1}]
        # Minimize sum_e t_e subject to:
        #   (d0 alpha)_e - t_e <= delta_e
        #  -(d0 alpha)_e - t_e <= -delta_e
        c = np.concatenate([np.zeros(n_nodes), np.ones(m_edges)])
        a_ub = np.vstack([
            np.hstack([d0, -np.eye(m_edges)]),
            np.hstack([-d0, -np.eye(m_edges)]),
        ])
        b_ub = np.concatenate([delta_arr, -delta_arr])
        bounds = [(None, None)] * n_nodes + [(0.0, None)] * m_edges
        res = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if not res.success:
            raise ValueError(f"HiGHS LP solver failed: {res.message}")
        alpha_opt = res.x[:n_nodes]
        t_opt = res.x[n_nodes:]
        quotient_norm = float(np.sum(t_opt))
    else:
        # Least squares fallback projection
        alpha_opt = np.linalg.lstsq(d0, delta_arr, rcond=tol)[0]
        quotient_norm = float(np.sum(np.abs(delta_arr - d0 @ alpha_opt)))

    repaired = delta_arr - d0 @ alpha_opt

    if d1 is not None and d1.shape[0] > 0:
        curv = float(np.sum(np.abs(d1 @ delta_arr)))
    else:
        curv = 0.0

    is_gauge = bool(quotient_norm <= tol)
    if is_gauge:
        status = "AUTHORIZED"
    elif curv <= tol:
        status = "OBSTRUCTED"
    else:
        status = "REFUSAL"

    return QuotientStickinessResult(
        raw_norm=raw_norm,
        quotient_residual=quotient_norm,
        optimal_gauge=alpha_opt,
        repaired_cochain=repaired,
        curvature_residual=curv,
        is_pure_gauge=is_gauge,
        status=status,
    )


def evaluate_cochain_holonomy_bridge(
    complex_: SimplicialComplex,
    edge_hamiltonians: Mapping[tuple[int, int], np.ndarray],
    marginals: Sequence[np.ndarray],
    dims: Sequence[int],
    tol: float = 1e-11,
) -> HolonomyAccumulationReport:
    """Link 2-site entangling Hamiltonian defects to simplicial cochain holonomies."""
    tol = nonnegative(tol, "tol")
    ds, rhos = reference(marginals, dims)
    edges = complex_.get_simplices(1)
    edge_index = {e: i for i, e in enumerate(edges)}

    h_total = np.zeros((math.prod(ds), math.prod(ds)), dtype=complex)
    cochain = np.zeros(len(edges), dtype=np.float64)

    for (u, v), h_local in edge_hamiltonians.items():
        u_idx = integer(u, "u")
        v_idx = integer(v, "v")
        if (u_idx, v_idx) not in edge_index and (v_idx, u_idx) not in edge_index:
            raise ValueError(f"edge ({u_idx}, {v_idx}) not in simplicial complex")

        sign = 1.0 if (u_idx, v_idx) in edge_index else -1.0
        e_pos = edge_index[(u_idx, v_idx)] if sign > 0 else edge_index[(v_idx, u_idx)]

        h_full = embed_local_operator(h_local, [u_idx, v_idx], ds)
        h_total += h_full

        # Defect speed for this specific bond
        res = evaluate_hamiltonian_defect_velocity(h_full, rhos, ds, tol=tol)
        cochain[e_pos] += sign * res.defect_velocity_nu

    total_res = evaluate_hamiltonian_defect_velocity(h_total, rhos, ds, tol=tol)

    d0 = simplicial_coboundary_matrix(complex_, 0)
    d1 = simplicial_coboundary_matrix(complex_, 1)

    face_holonomies = d1 @ cochain
    max_rate = float(np.max(np.abs(face_holonomies))) if face_holonomies.size > 0 else 0.0

    stickiness = compute_quotient_stickiness_lp(d0, cochain, d1, tol=tol)

    return HolonomyAccumulationReport(
        complex_dimension=complex_.max_dimension,
        num_nodes=complex_.num_simplices(0),
        num_edges=len(edges),
        num_faces=complex_.num_simplices(2),
        edge_cochain=cochain,
        face_holonomies=face_holonomies,
        defect_velocity_total=total_res.defect_velocity_nu,
        max_face_holonomy_rate=max_rate,
        quotient_stickiness_l1=stickiness.quotient_residual,
        is_pure_gauge=stickiness.is_pure_gauge,
        terminal_status=stickiness.status,
    )


def evaluate_discrete_continuum_membrane(
    p: int,
    q: int,
    require_membrane_contract: bool = True,
    custom_membrane: dict | None = None,
) -> DiscreteContinuumMembrane:
    """Apply the discrete-to-continuum firewall distinguishing Q/Z torsion from U(1).

    In Cycle 006 (qm_u1_torsion_exclusion.md), Lean 4 verified ker(exp) = 2*pi*Z.
    Rational holonomies in Q/Z cannot be continuously promoted to U(1) without an
    explicitly declared Level-Q membrane contract.
    """
    p_val = integer(p, "p", minimum=-1000000)
    q_val = integer(q, "q", minimum=1)

    if not require_membrane_contract:
        angle = 2.0 * math.pi * (p_val / q_val) % (2.0 * math.pi)
        return DiscreteContinuumMembrane(
            rational_holonomy=(p_val, q_val),
            continuous_phase_angle=angle,
            membrane_authorized=True,
            status="UNFENCED_WARNING",
            refusal_reason="Contract requirement waived; lacks formal continuum boundary fence",
        )

    if custom_membrane is None or custom_membrane.get("contract") != "Level-Q-Membrane-v1":
        return DiscreteContinuumMembrane(
            rational_holonomy=(p_val, q_val),
            continuous_phase_angle=0.0,
            membrane_authorized=False,
            status="REFUSAL",
            refusal_reason=(
                "CONTINUUM_MEMBRANE_REQUIRED: Rational holonomy in Q/Z belongs to a finite "
                "torsion subgroup and cannot be continuously identified with the U(1) infinite "
                "period lattice (2*pi*Z, Cycle 006) without an explicit Level-Q membrane contract."
            ),
        )

    angle = 2.0 * math.pi * (p_val / q_val) % (2.0 * math.pi)
    return DiscreteContinuumMembrane(
        rational_holonomy=(p_val, q_val),
        continuous_phase_angle=angle,
        membrane_authorized=True,
        status="AUTHORIZED",
        refusal_reason=None,
    )
