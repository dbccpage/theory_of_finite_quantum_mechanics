"""Quantum Regge Calculus Primitives: 10 Targets Reachable from Genesis and WDP.

AuthorityEffect: None.
Mathematical Domain: Tullio Regge's Discrete Gravity & Quantum Path Integral Formulations.
Corresponds to targets RQ-01 through RQ-10 bridging Genesis Categories 5, 12, 17
and WDP Levels 04, 15, 16, 17, 18.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Any, List, Tuple

from .simplicial_complex import ReggeComplex, make_regge_complex

# ==============================================================================
# 1. Classical Regge Action with Cosmological Constant (RQ-01)
# ==============================================================================


@dataclass
class ReggeActionWithLambdaResult:
    curvature_term: float
    cosmological_term: float
    total_action: float
    lambda_param: float


def compute_regge_action_with_lambda(
    regge: ReggeComplex,
    lambda_param: float = 0.0,
    internal_only: bool = False,
) -> ReggeActionWithLambdaResult:
    """Compute S_Regge = sum_{h} A_h * epsilon_h - Lambda * sum_{sigma} V_sigma."""
    dim = regge.complex.dim
    curv_term = 0.0

    if dim == 2:
        for v in regge.complex.c0:
            if internal_only and not regge.is_internal_hinge(v):
                continue
            eps = regge.deficit_angle(v)
            curv_term += 1.0 * eps
        total_vol = sum(regge.triangle_area(t) for t in regge.complex.c2)
    elif dim == 3:
        for e in regge.complex.c1:
            if internal_only and not regge.is_internal_hinge(e):
                continue
            eps = regge.deficit_angle(e)
            ell = regge.edge_length(e)
            curv_term += ell * eps
        total_vol = sum(regge.tetrahedron_volume(tet) for tet in regge.complex.c3)
    else:
        total_vol = 0.0

    cosmo_term = lambda_param * total_vol
    total_action = curv_term - cosmo_term
    return ReggeActionWithLambdaResult(
        curvature_term=curv_term,
        cosmological_term=cosmo_term,
        total_action=total_action,
        lambda_param=lambda_param,
    )


# ==============================================================================
# 2. Regge Field Equations & Schläfli Identity (RQ-02)
# ==============================================================================


@dataclass
class SchlafliIdentityCheck:
    simplex_id: Tuple[int, ...]
    sum_a_dtheta: float
    is_vanishing: bool


def verify_schlafli_identity_2d(
    regge: ReggeComplex, tri: Tuple[int, int, int], delta: float = 1e-6
) -> SchlafliIdentityCheck:
    """Schläfli identity for a triangle: sum_{i=0}^2 d theta_i = 0.
    In 2D, the sum of interior angles is constant (pi), so d(sum theta) = 0 identically!
    """
    angles = [regge.triangle_angle(tri, v) for v in tri]
    tot = sum(angles)
    err = abs(tot - math.pi)
    return SchlafliIdentityCheck(
        simplex_id=tri,
        sum_a_dtheta=err,
        is_vanishing=(err < 1e-9),
    )


def compute_regge_edge_gradient(
    regge: ReggeComplex, edge: Tuple[int, int], delta: float = 1e-6
) -> float:
    """Numerical gradient dS / d ell_e of the Regge action with respect to edge length."""
    curr_len = regge.edge_length(edge)
    # Forward step
    new_lengths_fwd = dict(regge.edge_lengths)
    new_lengths_fwd[edge] = curr_len + delta
    regge_fwd = ReggeComplex(regge.complex, new_lengths_fwd)
    s_fwd = regge_fwd.regge_action()

    # Backward step
    new_lengths_bwd = dict(regge.edge_lengths)
    new_lengths_bwd[edge] = curr_len - delta
    regge_bwd = ReggeComplex(regge.complex, new_lengths_bwd)
    s_bwd = regge_bwd.regge_action()

    return (s_fwd - s_bwd) / (2.0 * delta)


# ==============================================================================
# 3. Simplicial Metric Triangle & Polytope Inequalities (RQ-03)
# ==============================================================================


@dataclass
class MetricPolytopeCheck:
    is_admissible: bool
    triangle_inequality_violations: List[Tuple[Tuple[int, int, int], str]]
    cayley_menger_violations: List[Tuple[Tuple[int, ...], float]]


def check_metric_polytope_admissibility(regge: ReggeComplex) -> MetricPolytopeCheck:
    """Check that edge lengths define a valid Riemannian simplicial geometry:
    1. Triangle inequalities for all 2-simplices.
    2. Cayley-Menger volume positivity for all simplices.
    """
    tri_viol = []
    cm_viol = []

    for t in regge.complex.c2:
        u, v, w = t
        a = regge.edge_length((min(v, w), max(v, w)))
        b = regge.edge_length((min(u, w), max(u, w)))
        c = regge.edge_length((min(u, v), max(u, v)))
        if not (a + b > c and a + c > b and b + c > a):
            tri_viol.append((t, f"Sides ({a}, {b}, {c}) violate triangle inequality"))

    if regge.complex.dim >= 3:
        for tet in regge.complex.c3:
            vol = regge.tetrahedron_volume(tet)
            if vol <= 0.0 or math.isnan(vol):
                cm_viol.append((tet, vol))

    is_ok = len(tri_viol) == 0 and len(cm_viol) == 0
    return MetricPolytopeCheck(
        is_admissible=is_ok,
        triangle_inequality_violations=tri_viol,
        cayley_menger_violations=cm_viol,
    )


# ==============================================================================
# 4. Tullio Regge Discrete Quantum Path Integral Propagator (RQ-04)
# ==============================================================================


@dataclass
class QuantumReggePropagatorResult:
    amplitude: complex
    phase_sum: float
    admissible_configs: int
    total_configs_sampled: int


def compute_quantum_regge_path_integral_1d_edge(
    regge: ReggeComplex,
    interior_edge: Tuple[int, int],
    length_range: Tuple[float, float],
    steps: int = 50,
    hbar: float = 1.0,
) -> QuantumReggePropagatorResult:
    """Compute Z = int d ell mu(ell) exp(i S_Regge[ell] / hbar) over an interior edge length."""
    l_min, l_max = length_range
    step_size = (l_max - l_min) / float(steps)

    amp = complex(0.0, 0.0)
    phase_tot = 0.0
    admissible_count = 0

    orig_lengths = dict(regge.edge_lengths)

    for i in range(steps):
        ell = l_min + (i + 0.5) * step_size
        test_lengths = dict(orig_lengths)
        test_lengths[interior_edge] = ell
        regge_i = ReggeComplex(regge.complex, test_lengths)

        # Check metric polytope
        poly_check = check_metric_polytope_admissibility(regge_i)
        if poly_check.is_admissible:
            s = regge_i.regge_action()
            # DeWitt measure: mu(ell) = ell
            weight = ell * step_size
            phase = s / hbar
            amp += weight * cmath.exp(complex(0.0, phase))
            phase_tot += phase
            admissible_count += 1

    return QuantumReggePropagatorResult(
        amplitude=amp,
        phase_sum=phase_tot,
        admissible_configs=admissible_count,
        total_configs_sampled=steps,
    )


# ==============================================================================
# 5. Discrete Wheeler-DeWitt Hamiltonian Constraint Operator (RQ-05)
# ==============================================================================


@dataclass
class WheelerDeWittConstraintResult:
    vertex: int
    kinetic_term: float
    potential_term: float
    total_constraint_residual: float


def evaluate_simplicial_wheeler_dewitt(
    regge: ReggeComplex, vertex: int, psi_val: float = 1.0, psi_hessian_trace: float = 0.0
) -> WheelerDeWittConstraintResult:
    """Simplicial Wheeler-DeWitt constraint H_v Psi = 0:
    H_v = -hbar^2 * kinetic_term - 2 * sum_{e \ni v} ell_e * eps_e.
    """
    # Potential term: 2 * sum_{e \ni v} ell_e * eps_e
    potential = 0.0
    for e in regge.complex.c1:
        if vertex in e:
            eps = regge.deficit_angle(e)
            ell = regge.edge_length(e)
            potential += 2.0 * ell * eps

    kinetic = -1.0 * psi_hessian_trace
    residual = kinetic - potential * psi_val

    return WheelerDeWittConstraintResult(
        vertex=vertex,
        kinetic_term=kinetic,
        potential_term=potential,
        total_constraint_residual=residual,
    )


# ==============================================================================
# 6. Ponzano-Regge Semiclassical Amplitude (6j-Symbol) (RQ-06)
# ==============================================================================


@dataclass
class PonzanoReggeAsymptotics:
    regge_action: float
    tetrahedron_volume: float
    cosine_amplitude: float
    phase_factor: float


def compute_ponzano_regge_amplitude(
    tetrahedron_lengths: Tuple[float, float, float, float, float, float],
) -> PonzanoReggeAsymptotics:
    """Ponzano-Regge formula for a tetrahedron:
    {6j} ~ 1 / sqrt(12 pi V) * cos( sum_{e=1}^6 j_e theta_e + pi/4 ).
    """
    # Create single tetrahedron complex
    tet_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    edge_map = {tet_edges[i]: tetrahedron_lengths[i] for i in range(6)}
    regge = make_regge_complex(
        c0=(0, 1, 2, 3),
        c1=tet_edges,
        c2=[(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)],
        c3=[(0, 1, 2, 3)],
        edge_lengths=edge_map,
    )

    vol = regge.tetrahedron_volume((0, 1, 2, 3))
    if vol <= 0.0:
        raise ValueError(f"Tetrahedron has non-positive Cayley-Menger volume: {vol}")

    # Compute sum of ell_e * theta_e
    action = 0.0
    for e in tet_edges:
        ell = edge_map[e]
        theta = regge.tetrahedron_dihedral_angle((0, 1, 2, 3), e)
        action += ell * theta

    phase = action + math.pi / 4.0
    denom = math.sqrt(12.0 * math.pi * vol)
    amp = math.cos(phase) / denom

    return PonzanoReggeAsymptotics(
        regge_action=action,
        tetrahedron_volume=vol,
        cosine_amplitude=amp,
        phase_factor=phase,
    )


# ==============================================================================
# 7. Quantum Tetrahedron Area & Volume Spectrum (RQ-07)
# ==============================================================================


@dataclass
class QuantumTetrahedronSpectrum:
    spins: Tuple[float, float, float, float]
    face_areas: List[float]
    volume_eigenvalue_estimate: float


def compute_quantum_tetrahedron_spectrum(
    j1: float,
    j2: float,
    j3: float,
    j4: float,
    gamma: float = 0.2375,  # Barbero-Immirzi parameter
    l_p: float = 1.0,  # Planck length
) -> QuantumTetrahedronSpectrum:
    """Compute quantum area spectrum A_i = 8 pi gamma l_P^2 sqrt(j_i (j_i + 1))
    and Barrett-Crane intertwiner volume eigenvalue estimate.
    """
    spins = (j1, j2, j3, j4)
    areas = [8.0 * math.pi * gamma * (l_p**2) * math.sqrt(j * (j + 1.0)) for j in spins]
    # Semiclassical volume estimate from mean area
    a_mean = sum(areas) / 4.0
    vol_est = (a_mean**1.5) / (6.0 * math.sqrt(2.0))

    return QuantumTetrahedronSpectrum(
        spins=spins,
        face_areas=areas,
        volume_eigenvalue_estimate=vol_est,
    )


# ==============================================================================
# 8. Discrete Diffeomorphism Zero Modes (RQ-08)
# ==============================================================================


@dataclass
class ZeroModeAnalysis:
    eigenvalues: List[float]
    zero_mode_count: int
    is_diffeo_invariant: bool


def analyze_flat_triangulation_zero_modes(
    regge: ReggeComplex, interior_edges: List[Tuple[int, int]], delta: float = 1e-5
) -> ZeroModeAnalysis:
    """Analyze the Hessian matrix of S_Regge with respect to interior edges.
    In flat triangulations, displacement of interior vertices produces zero modes!
    """
    k = len(interior_edges)
    hessian = [[0.0] * k for _ in range(k)]

    for i in range(k):
        for j in range(k):
            e_i = interior_edges[i]
            e_j = interior_edges[j]
            # Numerical 2nd derivative
            lengths = dict(regge.edge_lengths)
            # ++
            lengths[e_i] += delta
            lengths[e_j] += delta
            s_pp = ReggeComplex(regge.complex, lengths).regge_action()
            # +-
            lengths[e_j] -= 2.0 * delta
            s_pm = ReggeComplex(regge.complex, lengths).regge_action()
            # -+
            lengths[e_i] -= 2.0 * delta
            lengths[e_j] += 2.0 * delta
            s_mp = ReggeComplex(regge.complex, lengths).regge_action()
            # --
            lengths[e_j] -= 2.0 * delta
            s_mm = ReggeComplex(regge.complex, lengths).regge_action()

            hessian[i][j] = (s_pp - s_pm - s_mp + s_mm) / (4.0 * delta * delta)

    # Simplified eigenvalue trace / determinant estimate
    sum(hessian[i][i] for i in range(k))
    # Count small diagonal entries as candidate zero modes
    zero_modes = sum(1 for i in range(k) if abs(hessian[i][i]) < 1e-4)

    return ZeroModeAnalysis(
        eigenvalues=[hessian[i][i] for i in range(k)],
        zero_mode_count=zero_modes,
        is_diffeo_invariant=(zero_modes > 0),
    )


# ==============================================================================
# 9. Discrete Deficit Curvature Bounds in Quantum Phase Space (RQ-09)
# ==============================================================================


@dataclass
class CurvatureBoundPathIntegralResult:
    unbounded_amplitude: complex
    bounded_amplitude: complex
    suppression_factor: float
    curvature_bound: float


def compute_curvature_bounded_path_integral(
    regge: ReggeComplex,
    edge: Tuple[int, int],
    length_range: Tuple[float, float],
    bound_delta: float,
    steps: int = 50,
    hbar: float = 1.0,
) -> CurvatureBoundPathIntegralResult:
    """Compute quantum amplitude with and without the curvature bound Theta(Delta - max |eps|)."""
    l_min, l_max = length_range
    step_size = (l_max - l_min) / float(steps)

    amp_unbounded = complex(0.0, 0.0)
    amp_bounded = complex(0.0, 0.0)

    for i in range(steps):
        ell = l_min + (i + 0.5) * step_size
        test_lens = dict(regge.edge_lengths)
        test_lens[edge] = ell
        regge_i = ReggeComplex(regge.complex, test_lens)

        if check_metric_polytope_admissibility(regge_i).is_admissible:
            s = regge_i.regge_action()
            weight = ell * step_size
            phase = s / hbar
            term = weight * cmath.exp(complex(0.0, phase))
            amp_unbounded += term

            # Check curvature bound
            bound_ok, max_eps, _ = regge_i.check_curvature_bound(bound_delta, internal_only=True)
            if bound_ok:
                amp_bounded += term

    mag_unb = abs(amp_unbounded)
    mag_bnd = abs(amp_bounded)
    supp = mag_bnd / mag_unb if mag_unb > 1e-12 else 1.0

    return CurvatureBoundPathIntegralResult(
        unbounded_amplitude=amp_unbounded,
        bounded_amplitude=amp_bounded,
        suppression_factor=supp,
        curvature_bound=bound_delta,
    )


# ==============================================================================
# 10. Regge-Čech Sheaf Quantum Entanglement Bridge (RQ-10)
# ==============================================================================


@dataclass
class ReggeCechQuantumBridge:
    hinge: Any
    deficit_angle: float
    cech_obstruction: float
    bell_chsh_violation_bound: float
    is_contextual: bool


def bridge_regge_to_quantum_cech(regge: ReggeComplex, hinge: Any) -> ReggeCechQuantumBridge:
    """Map Regge curvature directly to Category 12 Sheaf Contextuality and Bell bounds:
    The holonomy deficit angle |eps| acts as an obstruction to global section gluing.
    In the Bell-CHSH setting, gamma = max(0, S_CHSH - 2).
    Here, gamma = |eps|, yielding an operational bound S_CHSH <= 2 + |eps|.
    """
    eps = regge.deficit_angle(hinge)
    abs_eps = abs(eps)
    cech_obs = regge.cech_gluing_obstruction(hinge)

    if abs_eps < 1e-9:
        eps = 0.0
        abs_eps = 0.0
        cech_obs = 0.0
        chsh_bound = 2.0
        is_contextual = False
    else:
        chsh_bound = min(4.0, 2.0 + abs_eps)
        is_contextual = True

    return ReggeCechQuantumBridge(
        hinge=hinge,
        deficit_angle=eps,
        cech_obstruction=cech_obs,
        bell_chsh_violation_bound=chsh_bound,
        is_contextual=is_contextual,
    )
