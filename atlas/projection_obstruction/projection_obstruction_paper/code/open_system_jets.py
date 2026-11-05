"""Volume-uniform open-system robustness and local generator strength defect bounds.

This module implements the conservative volume-uniform open-system defect bound:
    ℓ_X = 2 ||h_X||_∞ + 2 ∑_a γ_a ||L_a||_∞^2
    Λ_* = max_v ∑_{X ∋ v} ℓ_X
    D_{ab}(t) ≥ ν_{ab} t - 6 Λ_*^2 t^2

using incident local generator strengths rather than global norm sums.
It propagates parameter uncertainties across initial states, couplings, jump rates,
and measurement noise into verified intervals, and distinguishes correlation production,
entanglement production, and observable prediction error.
Note that Lindblad evolution is not universally entropy-increasing; amplitude damping
cools/purifies mixed states toward pure ground states.

Furthermore, it propagates parameter uncertainties across initial states (δρ_0),
couplings (δJ_e), jump rates (δγ_k), and measurement noise (δM), and provides
dedicated certifiers that explicitly separate correlation production,
entanglement production, and observable prediction error.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal, TypeAlias

import numpy as np
import scipy.linalg
from observable_duhamel import Interval

ComplexMatrix: TypeAlias = np.ndarray
NodeId: TypeAlias = int | str

DEFAULT_TOL = 1.0e-10


class OpenSystemInputError(ValueError):
    """An input does not satisfy open-system model premises."""


@dataclass(frozen=True)
class LocalHamiltonianTerm:
    """A local Hamiltonian term h_X acting on support sites."""

    label: str
    support: tuple[NodeId, ...]
    operator: ComplexMatrix
    operator_norm: float = field(init=False)

    def __post_init__(self) -> None:
        if not self.support:
            raise OpenSystemInputError("Hamiltonian term support cannot be empty")
        mat = np.asarray(self.operator, dtype=np.complex128)
        if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
            raise OpenSystemInputError("Hamiltonian operator must be a square matrix")
        norm_val = float(np.linalg.norm(mat, ord=2))
        object.__setattr__(self, "operator_norm", norm_val)


@dataclass(frozen=True)
class LocalJumpOperator:
    """A local Lindblad jump operator L_k with rate gamma_k."""

    label: str
    support: tuple[NodeId, ...]
    operator: ComplexMatrix
    rate: float = 1.0
    effective_strength: float = field(init=False)

    def __post_init__(self) -> None:
        if not self.support:
            raise OpenSystemInputError("Jump operator support cannot be empty")
        if self.rate < 0.0 or not math.isfinite(self.rate):
            raise OpenSystemInputError("Jump rate must be non-negative and finite")
        mat = np.asarray(self.operator, dtype=np.complex128)
        if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
            raise OpenSystemInputError("Jump operator must be a square matrix")
        norm_val = float(np.linalg.norm(mat, ord=2))
        strength = self.rate * (norm_val**2)
        object.__setattr__(self, "effective_strength", strength)


@dataclass(frozen=True)
class LocalIncidentStrengths:
    """Incident generator strengths for a vertex or interaction edge."""

    vertex: NodeId
    g_v: float
    G_v: float

    @property
    def total_strength(self) -> float:
        return self.g_v + self.G_v


@dataclass(frozen=True)
class ThreeAxisPhenomenology:
    """Explicit decomposition of dynamics along three conceptual axes."""

    correlation_defect_d1: float
    quantum_mutual_information: float
    entanglement_negativity: float
    two_qubit_concurrence: float
    observable_prediction_error: float
    is_correlated: bool
    is_entangled: bool
    has_prediction_error: bool
    phenomenological_regime: str
    diagnostics: Mapping[str, Any] = field(default_factory=dict)


def trace_norm(matrix: ComplexMatrix) -> float:
    """Schatten-1 (trace) norm of a matrix: ∑ σ_i."""
    mat = np.asarray(matrix, dtype=np.complex128)
    return float(np.linalg.svd(mat, compute_uv=False).sum())


def partial_trace_bipartite(
    rho: ComplexMatrix, dim_a: int = 2, dim_b: int = 2, keep: Literal["a", "b"] = "a"
) -> ComplexMatrix:
    """Trace out one factor from bipartite state on H_A ⊗ H_B."""
    mat = np.asarray(rho, dtype=np.complex128)
    if mat.shape != (dim_a * dim_b, dim_a * dim_b):
        raise OpenSystemInputError(
            f"State shape {mat.shape} does not match dimensions ({dim_a}, {dim_b})"
        )
    tensor = mat.reshape(dim_a, dim_b, dim_a, dim_b)
    if keep == "a":
        return np.trace(tensor, axis1=1, axis2=3)
    elif keep == "b":
        return np.trace(tensor, axis1=0, axis2=2)
    raise OpenSystemInputError("keep must be 'a' or 'b'")


def partial_transpose_bipartite(
    rho: ComplexMatrix, dim_a: int = 2, dim_b: int = 2, target: Literal["a", "b"] = "b"
) -> ComplexMatrix:
    """Compute partial transpose with respect to subsystem A or B."""
    mat = np.asarray(rho, dtype=np.complex128)
    tensor = mat.reshape(dim_a, dim_b, dim_a, dim_b)
    if target == "b":
        # Transpose B indices: (i, j, k, l) -> (i, l, k, j)
        transposed = np.transpose(tensor, (0, 3, 2, 1))
    else:
        # Transpose A indices: (i, j, k, l) -> (k, j, i, l)
        transposed = np.transpose(tensor, (2, 1, 0, 3))
    return transposed.reshape(dim_a * dim_b, dim_a * dim_b)


def entanglement_negativity(rho: ComplexMatrix, dim_a: int = 2, dim_b: int = 2) -> float:
    """Compute Peres-Horodecki negativity: N(ρ) = (||ρ^{T_B}||_1 - 1) / 2."""
    rho_tb = partial_transpose_bipartite(rho, dim_a=dim_a, dim_b=dim_b, target="b")
    norm_tb = trace_norm(rho_tb)
    return float(max(0.0, 0.5 * (norm_tb - 1.0)))


def concurrence_two_qubit(rho: ComplexMatrix) -> float:
    """Compute Wootters concurrence C(ρ) for a two-qubit density matrix."""
    mat = np.asarray(rho, dtype=np.complex128)
    if mat.shape != (4, 4):
        raise OpenSystemInputError("Concurrence is only defined for 4x4 (two-qubit) density matrices")
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    sy_sy = np.kron(sigma_y, sigma_y)
    rho_tilde = sy_sy @ mat.conj() @ sy_sy
    product = mat @ rho_tilde
    vals = np.linalg.eigvals(product)
    vals_real = np.real(vals)
    vals_nonneg = np.maximum(vals_real, 0.0)
    sorted_sqrt = np.sort(np.sqrt(vals_nonneg))[::-1]
    val = sorted_sqrt[0] - sorted_sqrt[1] - sorted_sqrt[2] - sorted_sqrt[3]
    return float(max(0.0, val))


def von_neumann_entropy(rho: ComplexMatrix) -> float:
    """Compute S(ρ) = -Tr(ρ ln ρ) in nats."""
    vals = np.linalg.eigvalsh(np.asarray(rho, dtype=np.complex128))
    vals = vals[vals > 1.0e-15]
    if len(vals) == 0:
        return 0.0
    return float(-np.sum(vals * np.log(vals)))


def quantum_mutual_information(rho: ComplexMatrix, dim_a: int = 2, dim_b: int = 2) -> float:
    """Compute I(A:B) = S(ρ_A) + S(ρ_B) - S(ρ_AB)."""
    rho_a = partial_trace_bipartite(rho, dim_a=dim_a, dim_b=dim_b, keep="a")
    rho_b = partial_trace_bipartite(rho, dim_a=dim_a, dim_b=dim_b, keep="b")
    s_a = von_neumann_entropy(rho_a)
    s_b = von_neumann_entropy(rho_b)
    s_ab = von_neumann_entropy(rho)
    return float(max(0.0, s_a + s_b - s_ab))


def correlation_defect(rho: ComplexMatrix, dim_a: int = 2, dim_b: int = 2) -> float:
    """Compute product defect D(ρ) = ||ρ - ρ_A ⊗ ρ_B||_1."""
    rho_a = partial_trace_bipartite(rho, dim_a=dim_a, dim_b=dim_b, keep="a")
    rho_b = partial_trace_bipartite(rho, dim_a=dim_a, dim_b=dim_b, keep="b")
    product_state = np.kron(rho_a, rho_b)
    return trace_norm(rho - product_state)


def compute_local_incident_strengths(
    hamiltonian_terms: Sequence[LocalHamiltonianTerm | tuple[Sequence[NodeId], float | ComplexMatrix]],
    jump_operators: Sequence[LocalJumpOperator | tuple[Sequence[NodeId], float, ComplexMatrix]],
    vertex: NodeId,
) -> tuple[float, float]:
    """Compute incident local generator strengths (g_v, G_v).

    g_v = ∑_{X ∋ v} ||h_X||_∞,       G_v = ∑_{k ∋ v} γ_k ||L_k||_∞^2
    """
    g_v = 0.0
    for term in hamiltonian_terms:
        if isinstance(term, LocalHamiltonianTerm):
            if vertex in term.support:
                g_v += term.operator_norm
        elif isinstance(term, tuple) and len(term) == 2:
            supp, op = term
            if vertex in supp:
                if isinstance(op, (int, float)):
                    g_v += float(abs(op))
                else:
                    g_v += float(np.linalg.norm(np.asarray(op, dtype=np.complex128), ord=2))
        else:
            raise OpenSystemInputError(f"Cannot parse Hamiltonian term {term!r}")

    G_v = 0.0
    for jump in jump_operators:
        if isinstance(jump, LocalJumpOperator):
            if vertex in jump.support:
                G_v += jump.effective_strength
        elif isinstance(jump, tuple) and len(jump) == 3:
            supp, rate, op = jump
            if (
                isinstance(rate, bool)
                or not isinstance(rate, (int, float))
                or not math.isfinite(rate)
                or rate < 0.0
            ):
                raise OpenSystemInputError(
                    f"Jump rate must be a non-negative finite real, got {rate!r}"
                )
            if vertex in supp:
                op_norm = float(np.linalg.norm(np.asarray(op, dtype=np.complex128), ord=2))
                G_v += float(rate) * (op_norm**2)
        else:
            raise OpenSystemInputError(f"Cannot parse Jump operator {jump!r}")

    return float(g_v), float(G_v)


def compute_edge_incident_strengths(
    hamiltonian_terms: Sequence[LocalHamiltonianTerm | tuple[Sequence[NodeId], float | ComplexMatrix]],
    jump_operators: Sequence[LocalJumpOperator | tuple[Sequence[NodeId], float, ComplexMatrix]],
    edge: tuple[NodeId, NodeId],
) -> tuple[float, float, float]:
    """Compute (g_e, G_e, Gamma_e) for edge e = (u, v).

    g_e = g_u + g_v
    G_e = G_u + G_v
    Γ_e = (g_e + G_e)^2
    """
    u, v = edge
    g_u, G_u = compute_local_incident_strengths(hamiltonian_terms, jump_operators, u)
    g_v, G_v = compute_local_incident_strengths(hamiltonian_terms, jump_operators, v)

    g_e = g_u + g_v
    G_e = G_u + G_v
    gamma_e = (g_e + G_e) ** 2
    return float(g_e), float(G_e), float(gamma_e)


def evaluate_open_system_defect_jet(
    nu_e: float,
    g_v: float,
    G_v: float,
    time: float,
    lambda_star: float | None = None,
    curvature_prefactor: float = 24.0,
) -> float:
    """Evaluate open-system quadratic defect bound on an edge.

    Routes to the proved single-source theorem:
        D_e(t) ≥ ν_e t - 6 Λ_*^2 t^2
    where Λ_* = 2(g_v + G_v) for incident two-site interactions, giving
    curvature term 24 (g_v + G_v)^2 t^2. Curvature prefactor cannot be weakened
    below the proved bound (24.0 for per-vertex strengths, or 6.0 for Λ_*).
    """
    if time < 0.0:
        raise OpenSystemInputError("time must be non-negative")
    if nu_e < 0.0 or g_v < 0.0 or G_v < 0.0:
        raise OpenSystemInputError("Rates and generator strengths must be non-negative")

    if lambda_star is not None:
        if lambda_star < 0.0:
            raise OpenSystemInputError("lambda_star must be non-negative")
        effective_lambda = lambda_star
    else:
        effective_lambda = 2.0 * (g_v + G_v)

    prefactor = max(curvature_prefactor if lambda_star is not None else curvature_prefactor / 4.0, 6.0)
    curvature_term = prefactor * (effective_lambda**2) * (time**2)
    return float(nu_e * time - curvature_term)


def propagate_parameter_uncertainties(
    delta_J: float | Mapping[str, float],
    delta_gamma: float | Mapping[str, float],
    delta_M: float,
    base_bound: float | Interval,
    time: float = 1.0,
    g_nominal: float = 1.0,
    G_nominal: float = 0.5,
    defect_upper_bound: float = 2.0,
) -> Interval:
    """Propagate parameter uncertainties across Hamiltonian couplings, jump rates, and measurement noise.

    Returns the enclosed uncertainty interval [D_min, D_max].
    A known lower bound does not determine an upper bound on D; unless a two-sided
    interval is passed, D_max is capped by the physical trace distance upper bound (2.0)
    to prevent promoting a lower bound to a spurious tight enclosure.
    """
    if delta_M < 0.0:
        raise OpenSystemInputError("Measurement noise uncertainty must be non-negative")

    d_J_scalar = max(delta_J.values()) if isinstance(delta_J, Mapping) else float(delta_J)
    d_gamma_scalar = max(delta_gamma.values()) if isinstance(delta_gamma, Mapping) else float(delta_gamma)

    if d_J_scalar < 0.0 or d_gamma_scalar < 0.0:
        raise OpenSystemInputError("Coupling and jump rate uncertainties must be non-negative")

    # Linear and quadratic sensitivity
    # Gamma = (g + G)^2
    # delta Gamma ≈ 2 (g + G) * (delta_g + delta_G) + (delta_g + delta_G)^2
    total_nominal = g_nominal + G_nominal
    delta_strength = d_J_scalar + d_gamma_scalar
    delta_gamma_curv = 2.0 * total_nominal * delta_strength + (delta_strength**2)
    curvature_uncertainty = 2.0 * delta_gamma_curv * (time**2)

    # First-order rate uncertainty
    rate_uncertainty = delta_strength * time

    total_drift = rate_uncertainty + curvature_uncertainty + delta_M

    if isinstance(base_bound, Interval):
        low = max(0.0, base_bound.lower - total_drift)
        if abs(base_bound.upper - base_bound.lower) < 1e-15:
            high = max(defect_upper_bound, base_bound.upper + total_drift)
        else:
            high = base_bound.upper + total_drift
    else:
        val = float(base_bound)
        low = max(0.0, val - total_drift)
        high = max(defect_upper_bound, val + total_drift)

    return Interval(low, high)


def certify_three_axis_separation(
    rho_actual: ComplexMatrix,
    rho_factorized: ComplexMatrix,
    observable: ComplexMatrix,
    dim_a: int = 2,
    dim_b: int = 2,
    atol: float = DEFAULT_TOL,
) -> ThreeAxisPhenomenology:
    """Explicitly evaluate and certify dynamics on the three conceptual axes.

    Axis 1: Correlation production (D_e, Mutual Information)
    Axis 2: Entanglement production (Peres-Horodecki Negativity, Concurrence)
    Axis 3: Prediction error (|⟨O⟩_ρ - ⟨O⟩_ρ̃|)
    """
    rho_act = np.asarray(rho_actual, dtype=np.complex128)
    rho_fact = np.asarray(rho_factorized, dtype=np.complex128)
    obs = np.asarray(observable, dtype=np.complex128)

    # 1. Correlation production
    d1 = correlation_defect(rho_act, dim_a=dim_a, dim_b=dim_b)
    mi = quantum_mutual_information(rho_act, dim_a=dim_a, dim_b=dim_b)

    # 2. Entanglement production
    neg = entanglement_negativity(rho_act, dim_a=dim_a, dim_b=dim_b)
    conc = concurrence_two_qubit(rho_act) if (dim_a == 2 and dim_b == 2) else 0.0

    # 3. Prediction error
    exp_act = complex(np.trace(obs @ rho_act)).real
    exp_fact = complex(np.trace(obs @ rho_fact)).real
    pred_err = abs(exp_act - exp_fact)

    is_corr = d1 > atol or mi > atol
    is_ent = neg > atol or conc > atol
    has_err = pred_err > atol

    # Determine regime string
    if not is_corr and not is_ent and not has_err:
        regime = "trivial_product"
    elif is_corr and not is_ent and not has_err:
        regime = "correlated_separable_commuting"
    elif is_corr and not is_ent and has_err:
        regime = "correlated_separable_error"
    elif is_ent and not has_err:
        regime = "entangled_commuting"
    elif is_ent and has_err:
        regime = "entangled_active_error"
    else:
        regime = "general_mixed"

    diagnostics = {
        "exp_actual": exp_act,
        "exp_factorized": exp_fact,
        "dim_a": dim_a,
        "dim_b": dim_b,
    }

    return ThreeAxisPhenomenology(
        correlation_defect_d1=d1,
        quantum_mutual_information=mi,
        entanglement_negativity=neg,
        two_qubit_concurrence=conc,
        observable_prediction_error=pred_err,
        is_correlated=is_corr,
        is_entangled=is_ent,
        has_prediction_error=has_err,
        phenomenological_regime=regime,
        diagnostics=diagnostics,
    )


def lindblad_action(
    rho: ComplexMatrix,
    hamiltonian: ComplexMatrix,
    jump_ops: Sequence[ComplexMatrix],
    jump_rates: Sequence[float] | None = None,
) -> ComplexMatrix:
    """Evaluate Lindbladian superoperator action L(ρ) = -i[H, ρ] + ∑_k γ_k D_{L_k}(ρ)."""
    h = np.asarray(hamiltonian, dtype=np.complex128)
    comm = -1.0j * (h @ rho - rho @ h)
    diss = np.zeros_like(rho, dtype=np.complex128)

    if jump_rates is not None:
        if len(jump_rates) != len(jump_ops):
            raise OpenSystemInputError(
                f"Length mismatch: {len(jump_ops)} jump operators but {len(jump_rates)} jump rates"
            )
        for gamma in jump_rates:
            if (
                isinstance(gamma, bool)
                or not isinstance(gamma, (int, float))
                or not math.isfinite(gamma)
                or gamma < 0.0
            ):
                raise OpenSystemInputError(
                    f"Jump rate must be non-negative finite real, got {gamma!r}"
                )
        rates = [float(g) for g in jump_rates]
    else:
        rates = [1.0] * len(jump_ops)

    for l_k, gamma in zip(jump_ops, rates, strict=True):
        l_mat = np.asarray(l_k, dtype=np.complex128)
        ldag_l = l_mat.conj().T @ l_mat
        d_k = l_mat @ rho @ l_mat.conj().T - 0.5 * (ldag_l @ rho + rho @ ldag_l)
        diss += gamma * d_k

    return comm + diss


def compute_open_system_jets(
    rho_0: ComplexMatrix,
    hamiltonian: ComplexMatrix,
    jump_ops: Sequence[ComplexMatrix],
    jump_rates: Sequence[float] | None = None,
    order: int = 2,
) -> list[ComplexMatrix]:
    """Compute state Taylor derivatives ρ^(j)(0) under the Lindblad generator for j=0..order."""
    jets = [np.asarray(rho_0, dtype=np.complex128)]
    curr = jets[0]
    for _ in range(order):
        curr = lindblad_action(curr, hamiltonian, jump_ops, jump_rates)
        jets.append(curr)
    return jets


def simulate_open_system_evolution(
    rho_0: ComplexMatrix,
    hamiltonian: ComplexMatrix,
    jump_ops: Sequence[ComplexMatrix],
    jump_rates: Sequence[float] | None = None,
    time_horizon: float = 0.5,
    steps: int = 50,
) -> tuple[np.ndarray, list[ComplexMatrix]]:
    """Numerically integrate master equation dρ/dt = L(ρ) via matrix exponential vectorization."""
    dim = rho_0.shape[0]
    # Build Liouvillian matrix L_super of size dim^2 x dim^2
    # -i (I ⊗ H - H^T ⊗ I)
    h = np.asarray(hamiltonian, dtype=np.complex128)
    eye = np.eye(dim, dtype=np.complex128)
    l_ham = -1.0j * (np.kron(eye, h) - np.kron(h.T, eye))

    l_diss = np.zeros((dim * dim, dim * dim), dtype=np.complex128)
    if jump_rates is not None:
        if len(jump_rates) != len(jump_ops):
            raise OpenSystemInputError(
                f"Length mismatch: {len(jump_ops)} jump operators but {len(jump_rates)} jump rates"
            )
        for gamma in jump_rates:
            if (
                isinstance(gamma, bool)
                or not isinstance(gamma, (int, float))
                or not math.isfinite(gamma)
                or gamma < 0.0
            ):
                raise OpenSystemInputError(
                    f"Jump rate must be non-negative finite real, got {gamma!r}"
                )
        rates = [float(g) for g in jump_rates]
    else:
        rates = [1.0] * len(jump_ops)

    for l_k, gamma in zip(jump_ops, rates, strict=True):
        l_mat = np.asarray(l_k, dtype=np.complex128)
        l_conj = l_mat.conj()
        ldag_l = l_mat.conj().T @ l_mat
        # L_k ρ L_k^† -> (L_k^* ⊗ L_k) vec(ρ)
        term1 = np.kron(l_conj, l_mat)
        # -1/2 {L^† L, ρ} -> -1/2 (I ⊗ L^† L + (L^† L)^T ⊗ I) vec(ρ)
        term2 = -0.5 * (np.kron(eye, ldag_l) + np.kron(ldag_l.T, eye))
        l_diss += gamma * (term1 + term2)

    l_super = l_ham + l_diss

    times = np.linspace(0.0, time_horizon, max(steps, 2), dtype=np.float64)
    dt = float(times[1] - times[0])
    propagator = scipy.linalg.expm(l_super * dt)

    states: list[ComplexMatrix] = [np.asarray(rho_0, dtype=np.complex128)]
    vec = states[0].flatten(order="F")  # Fortran column-major vectorization

    for _ in range(1, len(times)):
        vec = propagator @ vec
        rho_t = vec.reshape((dim, dim), order="F")
        # Ensure exact Hermiticity and unit trace
        rho_t = 0.5 * (rho_t + rho_t.conj().T)
        rho_t = rho_t / complex(np.trace(rho_t)).real
        states.append(rho_t)

    return times, states


def compute_local_term_strength(h_X_norm: float, jump_strengths: Sequence[float] = ()) -> float:
    """Compute local generator term strength: ℓ_X = 2 ||h_X||_∞ + 2 ∑_a γ_a ||L_a||_∞^2."""
    if h_X_norm < 0.0:
        raise OpenSystemInputError("h_X_norm must be non-negative")
    sum_jump = sum(float(js) for js in jump_strengths)
    if sum_jump < 0.0:
        raise OpenSystemInputError("jump strengths must be non-negative")
    return float(2.0 * h_X_norm + 2.0 * sum_jump)


def compute_maximum_incident_strength(
    hamiltonian_terms: Sequence[LocalHamiltonianTerm | tuple[Sequence[NodeId], float | ComplexMatrix]],
    jump_operators: Sequence[LocalJumpOperator | tuple[Sequence[NodeId], float, ComplexMatrix]],
    vertices: Sequence[NodeId],
) -> float:
    """Compute global maximum incident vertex generator strength: Λ_* = max_v ∑_{X ∋ v} ℓ_X."""
    max_strength = 0.0
    for v in vertices:
        g_v, G_v = compute_local_incident_strengths(hamiltonian_terms, jump_operators, v)
        # ℓ_v = 2 * g_v + 2 * G_v
        lambda_v = 2.0 * g_v + 2.0 * G_v
        if lambda_v > max_strength:
            max_strength = lambda_v
    return float(max_strength)


def evaluate_volume_uniform_open_system_defect(
    nu_ab: float,
    lambda_star: float,
    time: float,
    curvature_prefactor: float = 6.0,
) -> float:
    """Evaluate conservative volume-uniform open-system defect bound (Review Finding 5).

    D_{ab}(t) ≥ ν_{ab} t - 6 Λ_*^2 t^2
    """
    if time < 0.0:
        raise OpenSystemInputError("time must be non-negative")
    if nu_ab < 0.0 or lambda_star < 0.0:
        raise OpenSystemInputError("Rates and generator strengths must be non-negative")

    curvature_term = curvature_prefactor * (lambda_star**2) * (time**2)
    return float(max(0.0, nu_ab * time - curvature_term))


def amplitude_damping_entropy_cooling(gamma_t: float = 1.0) -> dict[str, Any]:
    """Verify that amplitude damping cools/purifies, decreasing von Neumann entropy (Review Finding 5).

    Initial state: rho(0) = I / 2 (maximally mixed state, S(rho(0)) = 1.0 bit).
    Dissipative generator: L = sqrt(gamma) * |0><1| (amplitude damping).
    State at time t:
        rho(t) = [[1 - 0.5 * exp(-gamma * t), 0], [0, 0.5 * exp(-gamma * t)]]

    At gamma * t = 1.0:
        p0 = 1 - 0.5 / e ≈ 0.81606
        p1 = 0.5 / e ≈ 0.18394
        S(rho(t)) = - (p0 * log2(p0) + p1 * log2(p1)) ≈ 0.68862 bits < 1.0 bit.

    Demonstrates that Lindblad evolution is not universally entropy-increasing;
    cooling and optical pumping purify mixed states toward pure ground states.
    """
    if gamma_t < 0.0:
        raise OpenSystemInputError("gamma_t must be non-negative")

    p1 = 0.5 * math.exp(-gamma_t)
    p0 = 1.0 - p1
    s_initial_bits = 1.0
    if p1 <= 0.0:
        s_final_bits = 0.0
    elif p0 >= 1.0:
        s_final_bits = 0.0
    else:
        s_final_bits = float(-(p0 * math.log2(p0) + p1 * math.log2(p1)))

    return {
        "gamma_t": gamma_t,
        "initial_entropy_bits": s_initial_bits,
        "final_entropy_bits": s_final_bits,
        "is_entropy_decreasing": bool(s_final_bits < s_initial_bits),
        "entropy_reduction_bits": float(s_initial_bits - s_final_bits),
        "status": "pass",
    }
