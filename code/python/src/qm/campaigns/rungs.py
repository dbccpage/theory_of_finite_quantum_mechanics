"""Rungs 1 through 8 foundational walk for finite quantum mechanics.

Decomposed from foundations.py monolith. Integrates with omega_engine crates.
AuthorityEffect: None.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

import numpy as np
import scipy.linalg
from scipy.linalg import expm

from ..domain.primitives import (
    partial_trace_b,
    purity,
    von_neumann_entropy,
)
from . import cochain, cptp_channel, mermin_peres
from .born_normalization import (
    l1_to_l2_amplitude_lift,
)
from .contextuality_f2 import (
    parity_obstruction,
)
from .interference import (
    cross_term,
    interfered_weight,
)


class RungFrameError(Exception):
    """A rational frame or a rational cocycle failed an exact check."""


def _rational_or_none(value: object) -> Fraction | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if not isinstance(value, (int, float, Fraction)):
        return None
    return Fraction(value)


def primitive_difference(x: float | int, y: float | int) -> float:
    """Float helper. The certificate is exact_cocycle_defect."""
    return float(y - x)


def exact_primitive_difference(x: Fraction | int, y: Fraction | int) -> Fraction:
    """D(x, y) = y - x over the rationals."""
    return Fraction(y) - Fraction(x)


def exact_cocycle_defect(x: Fraction | int, y: Fraction | int, z: Fraction | int) -> Fraction:
    """(y - x) + (z - y) minus the direct step (z - x)."""
    left = Fraction(x)
    middle = Fraction(y)
    right = Fraction(z)
    telescoping = exact_primitive_difference(left, middle) + exact_primitive_difference(middle, right)
    return telescoping - exact_primitive_difference(left, right)


def is_same(x: float | int, y: float | int, tol: float = 1e-9) -> bool:
    """Sameness is equality of the rational values. `tol` is not consulted."""
    del tol
    left = _rational_or_none(x)
    right = _rational_or_none(y)
    if left is None or right is None:
        return False
    return exact_primitive_difference(left, right) == 0


def check_difference_cocycle(x: float, y: float, z: float, tol: float = 1e-12) -> bool:
    """Cocycle identity on 0-simplexes, decided by exact_cocycle_defect."""
    del tol
    if any(_rational_or_none(value) is None for value in (x, y, z)):
        return False
    return exact_cocycle_defect(x, y, z) == 0


def check_difference_antisymmetry(x: float, y: float, tol: float = 1e-12) -> bool:
    """Antisymmetry: D(x, y) + D(y, x) == 0 over the rationals."""
    del tol
    left = _rational_or_none(x)
    right = _rational_or_none(y)
    if left is None or right is None:
        return False
    return exact_primitive_difference(left, right) + exact_primitive_difference(right, left) == 0


def triangle_boundary_rank() -> int:
    """Rank of the triangle coboundary over Fraction, by Gaussian elimination."""
    matrix = [
        [Fraction(-1), Fraction(1), Fraction(0)],
        [Fraction(-1), Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(-1), Fraction(1)],
    ]
    rows = len(matrix)
    cols = len(matrix[0])
    rank = 0
    pivot_col = 0
    while rank < rows and pivot_col < cols:
        pivot = None
        for row in range(rank, rows):
            if matrix[row][pivot_col] != 0:
                pivot = row
                break
        if pivot is None:
            pivot_col += 1
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][pivot_col]
        for col in range(pivot_col, cols):
            matrix[rank][col] /= scale
        for row in range(rows):
            if row == rank or matrix[row][pivot_col] == 0:
                continue
            factor = matrix[row][pivot_col]
            for col in range(pivot_col, cols):
                matrix[row][col] -= factor * matrix[rank][col]
        rank += 1
        pivot_col += 1
    return rank



@dataclass(frozen=True)
class CochainPacket:
    """Finite cochain packet over a declared 2-complex.

    Wraps Complex and computes coboundaries, exactness, cohomology dimensions,
    and the Phi_1 / Gamma_2 diagnostic trichotomy.
    """
    complex: cochain.Complex

    def d0(self) -> np.ndarray:
        return self.complex.d0()

    def d1(self) -> np.ndarray:
        return self.complex.d1()

    def verify_d1_d0_nilpotent(self, tol: float = 1e-9) -> bool:
        """Verifies d1 d0 = 0 (QM-001-C5)."""
        return cochain.d1_d0_is_zero(self.complex, tol=tol)

    def b1_dim(self, tol: float = 1e-9) -> int:
        """Dimension of B^1 = im(d0)."""
        s = scipy.linalg.svdvals(self.d0())
        return int(np.sum(s > tol))

    def z1_dim(self, tol: float = 1e-9) -> int:
        """Dimension of Z^1 = ker(d1)."""
        m = self.d1()
        s = scipy.linalg.svdvals(m)
        rank = int(np.sum(s > tol))
        return int(m.shape[1] - rank)

    def h1_dim(self, tol: float = 1e-9) -> int:
        """Dimension of first cohomology H^1 = Z^1 / B^1."""
        return self.z1_dim(tol) - self.b1_dim(tol)

    def phi_1(self, x: np.ndarray) -> float:
        """Quotient mass Phi_1([x]) = inf_alpha ||x - d0 alpha||_{1,w}."""
        return cochain.phi_1(self.complex, x)

    def gamma_2(self, x: np.ndarray) -> float:
        """Closure defect Gamma_2([x]) = ||d1 x||_1."""
        return cochain.gamma_2(self.complex, x)

    def classify(self, x: np.ndarray, tol: float = 1e-9) -> str:
        """Trichotomy: ExactClass, ClosedResidual, or ActiveClosureFailure."""
        return cochain.classify(self.complex, x, tol=tol)


def build_triangle_packet(weights: tuple[float, ...] | None = None) -> CochainPacket:
    """Builds standard oriented 3-cycle triangle packet."""
    return CochainPacket(cochain.triangle(weights=weights))



def weights_to_probabilities(weights: np.ndarray) -> np.ndarray:
    """Rung 3: L^1 normalization of positive residual weights into probabilities."""
    w = np.asarray(weights, dtype=float)
    if np.any(w < 0):
        raise ValueError("weights must be non-negative")
    total = np.sum(w)
    if total <= 0:
        raise ValueError("sum of weights must be strictly positive")
    return w / total


def verify_ray_invariance(weights: np.ndarray, scale: float, tol: float = 1e-12) -> bool:
    """Rung 3: Probabilities are ray invariant under positive scaling w -> c*w."""
    if scale <= 0:
        raise ValueError("scale must be strictly positive")
    p1 = weights_to_probabilities(weights)
    p2 = weights_to_probabilities(scale * weights)
    return bool(np.allclose(p1, p2, atol=tol))


def amplitudes_to_probabilities(psi: np.ndarray) -> np.ndarray:
    """Rung 3: Quadratic Born rule mapping complex state amplitudes to probabilities."""
    psi = np.asarray(psi, dtype=complex)
    norm_sq = np.sum(np.abs(psi) ** 2)
    if norm_sq <= 1e-15:
        raise ValueError("norm of amplitude vector must be non-zero")
    return (np.abs(psi) ** 2) / norm_sq


def born_normalization(psi: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Rung 3: Normalizes a state vector psi to unit L^2 norm and constructs rank-1 Born projector P = |psi><psi|."""
    psi = np.asarray(psi, dtype=complex)
    norm = float(np.linalg.norm(psi))
    if norm <= 1e-15:
        raise ValueError("amplitude vector must be non-zero")
    psi_norm = psi / norm
    p_proj = np.outer(psi_norm, psi_norm.conj())
    tr = float(np.real(np.trace(p_proj)))
    return psi_norm, p_proj, tr


def verify_born_normalization_redundancy(rho: np.ndarray, povm_effects: list[np.ndarray], tol: float = 1e-9) -> dict[str, Any]:
    """Rung 3: Verifies that sum_k Tr(E_k rho) == 1 is an algebraic redundancy under complete POVM resolution."""
    if not is_valid_povm(povm_effects, tol=tol):
        raise ValueError("effects must form a valid POVM resolution of identity")
    probs = povm_probabilities(rho, povm_effects)
    total_prob = float(np.sum(probs))
    rho_tr = float(np.real(np.trace(rho)))
    is_redundant = bool(np.isclose(total_prob, rho_tr, atol=tol) and np.isclose(total_prob, 1.0, atol=tol))
    return {
        "probabilities": probs,
        "total_probability": total_prob,
        "density_trace": rho_tr,
        "is_redundant": is_redundant,
    }


def weights_to_born_density(weights: np.ndarray, phases: np.ndarray | None = None) -> np.ndarray:
    """Rung 3: L^1 positive residual weights lifted to a pure state Born projector P = |psi><psi|."""
    w = np.asarray(weights, dtype=float)
    if np.any(w < 0):
        raise ValueError("weights must be non-negative")
    total = np.sum(w)
    if total <= 0:
        raise ValueError("sum of weights must be strictly positive")
    if phases is not None:
        p = np.asarray(phases, dtype=float)
        if p.shape != w.shape:
            raise ValueError("phases shape must match weights shape")
    amplitudes = l1_to_l2_amplitude_lift(w, phases)
    _, p_proj, _ = born_normalization(amplitudes)
    return p_proj



def compute_cycle_holonomy(edge_phases: np.ndarray, cycle_edges: list[tuple[int, int]]) -> float:
    """Rung 4: Computes U(1) holonomy phase around a directed closed cycle."""
    phase_sum = 0.0
    for edge_idx, orientation in cycle_edges:
        phase_sum += orientation * edge_phases[edge_idx]
    return float(phase_sum % (2.0 * math.pi))


def two_path_interference(a1: complex, a2: complex) -> tuple[float, float]:
    """Rung 4: Evaluates two-path interference via canonical interference crate.

    Returns:
        total_prob: |a1 + a2|^2
        interference_term: total_prob - (|a1|^2 + |a2|^2)
    """
    amps = [a1, a2]
    p_total = float(interfered_weight(amps))
    i_term = float(cross_term(amps))
    return p_total, i_term


def sorkin_3slit_parameter(a1: complex, a2: complex, a3: complex) -> float:
    """Rung 4: Sorkin 3-slit interference parameter I_3(A, B, C) via canonical interference crate.

    I_3 = P(1,2,3) - [P(1,2) + P(2,3) + P(3,1)] + [P(1) + P(2) + P(3)].
    Under standard quadratic Born rule quantum mechanics, I_3 == 0 identically.
    """
    p123 = float(interfered_weight([a1, a2, a3]))
    p12 = float(interfered_weight([a1, a2]))
    p23 = float(interfered_weight([a2, a3]))
    p31 = float(interfered_weight([a3, a1]))
    p1 = float(interfered_weight([a1]))
    p2 = float(interfered_weight([a2]))
    p3 = float(interfered_weight([a3]))
    return float(p123 - (p12 + p23 + p31) + (p1 + p2 + p3))


def superposition_quotient_fiber(target: int | np.ndarray) -> dict[str, Any]:
    """Rung 4: Analyzes superposition as the quotient fiber over classical probability.

    If `target` is an integer n_sectors, delegates to the canonical interference crate.
    If `target` is an amplitude vector psi, projects |psi> to classical diagonal weights.
    The quotient map projects |psi> to classical diagonal weights p_i = |psi_i|^2 / ||psi||^2.
    The fiber contains the relative phase degrees of freedom that generate interference.
    """
    if isinstance(target, (int, np.integer)):
        from . import interference as _interference
        return _interference.superposition_quotient_fiber(int(target))
    psi = target
    psi = np.asarray(psi, dtype=complex)
    norm = float(np.linalg.norm(psi))
    if norm <= 1e-15:
        raise ValueError("amplitude vector must be non-zero")
    psi_norm = psi / norm
    probs = np.abs(psi_norm) ** 2
    active = np.where(probs > 1e-12)[0]
    is_superposition = len(active) > 1
    interference_capacity = 0.0
    n = len(psi_norm)
    for j in range(n):
        for k in range(j + 1, n):
            interference_capacity += 2.0 * float(np.abs(psi_norm[j]) * np.abs(psi_norm[k]))
    relative_phases = np.zeros(n, dtype=float)
    if len(active) > 0:
        ref_phase = float(np.angle(psi_norm[active[0]]))
        for idx in active:
            relative_phases[idx] = float((np.angle(psi_norm[idx]) - ref_phase) % (2.0 * math.pi))
    return {
        "probabilities": probs,
        "is_superposition": is_superposition,
        "active_components": int(len(active)),
        "interference_capacity": float(interference_capacity),
        "relative_phases": relative_phases,
    }


def superposition_interference_test(c1: complex, c2: complex, phase_shift: float) -> dict[str, float]:
    """Rung 4: Demonstrates 2-state superposition interference fringes under a beam splitter."""
    psi_in = np.array([c1, c2 * np.exp(1j * phase_shift)], dtype=complex)
    norm = np.linalg.norm(psi_in)
    if norm <= 1e-15:
        raise ValueError("initial amplitudes cannot both be zero")
    psi_norm = psi_in / norm
    u_bs = (1.0 / math.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
    psi_out = u_bs @ psi_norm
    p_out = np.abs(psi_out) ** 2
    cross_term = float(p_out[0] - 0.5)
    return {
        "prob_port0": float(p_out[0]),
        "prob_port1": float(p_out[1]),
        "cross_term": cross_term,
    }



def schmidt_decomposition(psi: np.ndarray, dim_a: int, dim_b: int) -> np.ndarray:
    """Rung 5: Computes Schmidt coefficients of a bipartite pure state in H_A ⊗ H_B."""
    psi = np.asarray(psi, dtype=complex).reshape((dim_a, dim_b))
    return scipy.linalg.svdvals(psi)


def is_entangled_pure_state(psi: np.ndarray, dim_a: int, dim_b: int, tol: float = 1e-6) -> bool:
    """Rung 5: Entanglement as an obstruction to product factorization (Schmidt rank > 1)."""
    s = schmidt_decomposition(psi, dim_a, dim_b)
    s_norm = s / np.linalg.norm(s)
    rank = int(np.sum(s_norm > tol))
    return rank > 1


def verify_mermin_peres_contextuality() -> bool:
    """Rung 5: Verifies Mermin-Peres 3x3 contextuality obstruction on C^2 ⊗ C^2 via contextuality_f2."""
    return bool(parity_obstruction() and mermin_peres.verify_mermin_peres_parity())


def partial_trace(rho_ab: np.ndarray, dim_a: int, dim_b: int) -> np.ndarray:
    """Rung 5: Partial trace of bipartite density matrix rho_AB over subsystem B."""
    rho_ab = np.asarray(rho_ab, dtype=complex)
    if rho_ab.shape != (dim_a * dim_b, dim_a * dim_b):
        raise ValueError("rho_AB dimension must equal dim_a * dim_b")
    return partial_trace_b(rho_ab, dim_a, dim_b)


def bipartite_linear_entropy(rho_ab: np.ndarray, dim_a: int, dim_b: int) -> float:
    """Rung 5: Computes linear entropy S_L(rho_A) = 1 - Tr(rho_A^2) of the reduced state."""
    rho_a = partial_trace(rho_ab, dim_a, dim_b)
    pur = purity(rho_a)
    return max(0.0, float(1.0 - pur))


def bipartite_von_neumann_entropy(rho_ab: np.ndarray, dim_a: int, dim_b: int, base: float = 2.0) -> float:
    """Rung 5: Computes von Neumann entanglement entropy S(rho_A) = -Tr(rho_A log(rho_A))."""
    rho_a = partial_trace(rho_ab, dim_a, dim_b)
    return float(von_neumann_entropy(rho_a, base=base))


def bell_state(index: int) -> np.ndarray:
    """Rung 5: Returns one of the four canonical maximally entangled Bell states (indices 0..3).

    0: |Phi+> = (|00> + |11>)/sqrt(2)
    1: |Phi-> = (|00> - |11>)/sqrt(2)
    2: |Psi+> = (|01> + |10>)/sqrt(2)
    3: |Psi-> = (|01> - |10>)/sqrt(2)
    """
    if index not in (0, 1, 2, 3):
        raise ValueError("Bell state index must be 0, 1, 2, or 3")
    inv_sqrt2 = 1.0 / math.sqrt(2.0)
    if index == 0:
        return inv_sqrt2 * np.array([1.0, 0.0, 0.0, 1.0], dtype=complex)
    elif index == 1:
        return inv_sqrt2 * np.array([1.0, 0.0, 0.0, -1.0], dtype=complex)
    elif index == 2:
        return inv_sqrt2 * np.array([0.0, 1.0, 1.0, 0.0], dtype=complex)
    else:
        return inv_sqrt2 * np.array([0.0, 1.0, -1.0, 0.0], dtype=complex)


def verify_non_signaling(rho_ab: np.ndarray, dim_a: int, dim_b: int, u_b: np.ndarray, tol: float = 1e-9) -> bool:
    """Rung 5: Verifies the non-signaling theorem Tr_B((I_A ⊗ U_B) rho_AB (I_A ⊗ U_B^dagger)) == Tr_B(rho_AB)."""
    if not is_unitary(u_b, tol=tol):
        raise ValueError("operator U_B must be unitary")
    op_total = np.kron(np.eye(dim_a, dtype=complex), u_b)
    rho_prime = op_total @ rho_ab @ op_total.conj().T
    rho_a_orig = partial_trace(rho_ab, dim_a, dim_b)
    rho_a_prime = partial_trace(rho_prime, dim_a, dim_b)
    return bool(np.allclose(rho_a_orig, rho_a_prime, atol=tol))



def is_unitary(u: np.ndarray, tol: float = 1e-9) -> bool:
    """Rung 6: Verifies U^dagger U = I."""
    if u.ndim != 2 or u.shape[0] != u.shape[1]:
        return False
    ident = np.eye(u.shape[0], dtype=complex)
    return bool(np.allclose(u.conj().T @ u, ident, atol=tol))


def discrete_unitary_step(state: np.ndarray, u: np.ndarray) -> np.ndarray:
    """Rung 6: Discrete time evolution psi(t+1) = U psi(t) or rho(t+1) = U rho(t) U^dagger."""
    if not is_unitary(u):
        raise ValueError("evolution operator must be unitary")
    if state.ndim == 1:
        return u @ state
    elif state.ndim == 2:
        return u @ state @ u.conj().T
    raise ValueError("state must be 1D vector or 2D density matrix")


def continuous_generator_branch_count(u: np.ndarray, tol: float = 1e-9) -> int:
    """Rung 6: Exhibits the continuous-time generator obstruction.

    A discrete unitary operator U has infinitely many Hamiltonian generators
    H_k = H_0 + 2 pi k I for integer k, since exp(-i H_k) = exp(-i H_0) exp(-2 pi i k I) = U.
    Returns the number of distinct branch cuts within |k| <= 2 (evaluating non-uniqueness).
    """
    if not is_unitary(u, tol=tol):
        raise ValueError("operator must be unitary")
    d = u.shape[0]
    evals, evecs = np.linalg.eig(u)
    evals_c = np.asarray(evals, dtype=complex)
    log_evals = np.log(evals_c) / (-1j)
    H0 = evecs @ np.diag(log_evals) @ np.linalg.inv(evecs)
    H0 = (H0 + H0.conj().T) / 2.0

    valid_branches = 0
    for k in range(-2, 3):
        H_k = H0 + 2.0 * np.pi * k * np.eye(d)
        U_k = expm(-1j * H_k)
        if np.allclose(U_k, u, atol=1e-7):
            valid_branches += 1
    return valid_branches



def is_valid_povm(effects: list[np.ndarray], tol: float = 1e-9) -> bool:
    """Rung 7: Verifies that a collection of matrices forms a valid POVM (E_m >= 0, sum E_m = I)."""
    if not effects:
        return False
    d = effects[0].shape[0]
    total = np.zeros((d, d), dtype=complex)
    for e in effects:
        if e.shape != (d, d):
            return False
        if not np.allclose(e, e.conj().T, atol=tol):
            return False
        evals = np.linalg.eigvalsh(e)
        if np.any(evals < -tol):
            return False
        total += e
    return bool(np.allclose(total, np.eye(d), atol=tol))


def povm_probabilities(rho: np.ndarray, effects: list[np.ndarray]) -> np.ndarray:
    """Rung 7: Computes Born probabilities p(m) = Tr(E_m rho) for a POVM."""
    if not is_valid_povm(effects):
        raise ValueError("effects do not form a valid POVM")
    probs = [float(np.real(np.trace(e @ rho))) for e in effects]
    return np.asarray(probs, dtype=float)


def non_selective_measurement_decoherence(rho: np.ndarray, projectors: list[np.ndarray]) -> np.ndarray:
    """Rung 7: Non-selective measurement state update rho' = sum_m P_m rho P_m (decoherence)."""
    rho_out = np.zeros(rho.shape, dtype=complex)
    for p in projectors:
        rho_out += p @ rho @ p
    return rho_out


def verify_cptp_contractivity(rho1: np.ndarray, rho2: np.ndarray, p: float) -> bool:
    """Rung 7: Verifies monotonicity of trace distance under depolarizing CPTP channel."""
    return cptp_channel.verify_cptp_contractivity(rho1, rho2, p)



@dataclass(frozen=True)
class BoundaryDefense:
    """Rung 8: Exact defended statement of where the finite presentation stops.

    The finite programme closes across Rungs 1-7 in discrete dimension d < infty.
    The four continuum interfaces are defended non-claims and explicit obstructions.
    """
    dimension: int
    has_continuous_observables: bool = False
    gleason_applies: bool = False
    continuous_time_canonical: bool = False
    continuum_lift_refused: bool = True

    def defense_rationale(self) -> dict[str, str]:
        return {
            "GAP-F001-S000-002": (
                "Continuum Hilbert lift: Refused. Infinite-dimensional L^2 completion "
                "is an open asymptotic interface not derived from finite cochain complexes. "
                "Costed: requires topological completion of l1/l2 normed space, infinite-dimensional "
                "operator domain, and non-admitted canonical commutation [X, P] = i hbar I by Wintner-Wielandt."
            ),
            "GAP-F001-S000-004": (
                f"Born uniqueness (Gleason): Gleason dimension condition requires d >= 3. "
                f"For d = {self.dimension}, Gleason {'holds' if self.dimension >= 3 else 'fails (2-label host admits non-contextual hidden variables)'}. "
                "Costed: requires dimension >= 3 lattice of projections, sigma-additivity on orthogonal subspaces, "
                "and frame function continuity."
            ),
            "GAP-F001-S000-008": (
                "Continuous time and Stone's theorem: Discrete toggles have branch ambiguity "
                "in matrix logarithm; continuous one-parameter groups remain declared hypotheses. "
                "Costed: requires one-parameter continuous group U(t) = exp(-iHt), resolving logarithmic "
                "branch ambiguities in finite complex isometries."
            ),
            "GAP-F001-S000-010": (
                "Gleason dimension condition at n >= 3: Unit-effect contract has disagreeing pairings "
                "on binary hosts (Bool); 3-label cardinality surrogate cannot be proved from below. "
                "Costed: at d=2 frame functions admit non-contextual hidden variables; at d>=3 noncontextuality forces Gleason."
            ),
        }


def get_boundary_defense(dimension: int) -> BoundaryDefense:
    """Rung 8: Constructs the boundary defense object for a given carrier dimension."""
    return BoundaryDefense(
        dimension=dimension,
        has_continuous_observables=False,
        gleason_applies=(dimension >= 3),
        continuous_time_canonical=False,
        continuum_lift_refused=True,
    )



def is_orthonormal_frame(frame: list[np.ndarray], tol: float = 1e-9) -> bool:
    """Checks whether a set of d vectors forms an orthonormal basis for C^d or R^d."""
    d = len(frame)
    for j in range(d):
        for k in range(d):
            expected = 1.0 if j == k else 0.0
            actual = np.vdot(frame[j], frame[k])
            if not np.isclose(actual, expected, atol=tol):
                return False
    return True


def evaluate_frame_function(f: Any, frame: list[np.ndarray]) -> float:
    """Evaluates the sum of a candidate frame function f over an orthonormal frame."""
    return float(sum(f(v) for v in frame))


def density_matrix_frame_function(rho: np.ndarray) -> Any:
    """Constructs the canonical Gleason frame function f_rho(v) = <v| rho |v>."""
    def f(v: np.ndarray) -> float:
        v = np.asarray(v, dtype=complex)
        return float(np.real(np.vdot(v, rho @ v)))
    return f


def verify_gleason_frame_additivity(rho: np.ndarray, frames: list[list[np.ndarray]], tol: float = 1e-9) -> bool:
    """Verifies that f_rho(v) = <v|rho|v> sums to 1.0 across all supplied orthonormal frames."""
    f = density_matrix_frame_function(rho)
    for frame in frames:
        if not is_orthonormal_frame(frame, tol=tol):
            raise ValueError("each frame in frames must be orthonormal")
        val = evaluate_frame_function(f, frame)
        if not np.isclose(val, 1.0, atol=tol):
            return False
    return True


def gleason_dimension_2_counterexample() -> dict[str, Any]:
    """Exhibits the failure of Gleason's Theorem in dimension d = 2.

    In d = 2, there exist non-Bornian (non-quadratic) frame functions that sum to 1
    on all orthogonal pairs in R^2 but take values only in {0, 1} and cannot be
    written as v^T rho v for any valid density matrix rho.
    """
    def non_bornian_f2(v: np.ndarray) -> float:
        """Discontinuous indicator frame function on R^2:
        Assigns 1 to vectors in quadrants I & III, 0 to quadrants II & IV.
        Every orthogonal pair has exactly one vector in Q1/Q3 and one in Q2/Q4.
        """
        x, y = float(v[0]), float(v[1])
        angle = math.atan2(y, x) % math.pi
        return 1.0 if angle < (math.pi / 2.0) else 0.0

    test_angles = [0.0, math.pi / 6.0, math.pi / 4.0, math.pi / 3.0, 0.723, 1.15]
    all_pairs_sum_to_one = True
    for theta in test_angles:
        v1 = np.array([math.cos(theta), math.sin(theta)])
        v2 = np.array([-math.sin(theta), math.cos(theta)])
        frame = [v1, v2]
        val = sum(non_bornian_f2(v) for v in frame)
        if not np.isclose(val, 1.0):
            all_pairs_sum_to_one = False
            break

    return {
        "dimension": 2,
        "all_pairs_sum_to_one": all_pairs_sum_to_one,
        "is_non_bornian": True,
        "explanation": (
            "Gleason's theorem fails at d = 2: non-contextual binary valuations f(v) in {0, 1} "
            "satisfy f(v1) + f(v2) = 1 for all orthogonal frames, but cannot be represented as "
            "v^T rho v for any density matrix. Hence Gleason requires d >= 3."
        ),
    }


def discrete_gleason_triads_d3() -> list[list[np.ndarray]]:
    """Returns a collection of orthogonal triad frames in R^3 for testing discrete Gleason."""
    e0 = np.array([1.0, 0.0, 0.0])
    e1 = np.array([0.0, 1.0, 0.0])
    e2 = np.array([0.0, 0.0, 1.0])
    f1 = [e0, e1, e2]
    inv_s2 = 1.0 / math.sqrt(2.0)
    u0 = np.array([inv_s2, inv_s2, 0.0])
    u1 = np.array([-inv_s2, inv_s2, 0.0])
    u2 = e2
    f2 = [u0, u1, u2]
    w0 = e0
    w1 = np.array([0.0, inv_s2, inv_s2])
    w2 = np.array([0.0, -inv_s2, inv_s2])
    f3 = [w0, w1, w2]
    return [f1, f2, f3]



def rational_pythagorean_frames_d2() -> list[list[tuple[Fraction, Fraction]]]:
    """Constructs exact rational orthonormal 2-frames in Q^2 via primitive Pythagorean triples.

    Each frame is a pair [u1, u2] where u1, u2 in Q^2, <u1, u2> = 0, and ||u1||^2 = ||u2||^2 = 1.
    """
    triples = [
        (0, 1, 1),
        (3, 4, 5),
        (5, 12, 13),
        (8, 15, 17),
        (7, 24, 25),
    ]
    frames = []
    for a, b, c in triples:
        if a == 0:
            u1 = (Fraction(1), Fraction(0))
            u2 = (Fraction(0), Fraction(1))
        else:
            u1 = (Fraction(a, c), Fraction(b, c))
            u2 = (Fraction(-b, c), Fraction(a, c))
        dot = u1[0] * u2[0] + u1[1] * u2[1]
        norm1_sq = u1[0] ** 2 + u1[1] ** 2
        norm2_sq = u2[0] ** 2 + u2[1] ** 2
        if dot != 0 or norm1_sq != 1 or norm2_sq != 1:
            raise RungFrameError(
                f"frame ({a}, {b}, {c}) has dot {dot} and norms {norm1_sq}, {norm2_sq}"
            )
        frames.append([u1, u2])
    return frames

__all__ = ['BoundaryDefense', 'CochainPacket', 'RungFrameError', 'amplitudes_to_probabilities', 'exact_cocycle_defect', 'exact_primitive_difference', 'triangle_boundary_rank', 'bell_state', 'bipartite_linear_entropy', 'bipartite_von_neumann_entropy', 'born_normalization', 'build_triangle_packet', 'check_difference_antisymmetry', 'check_difference_cocycle', 'compute_cycle_holonomy', 'continuous_generator_branch_count', 'density_matrix_frame_function', 'discrete_gleason_triads_d3', 'discrete_unitary_step', 'evaluate_frame_function', 'get_boundary_defense', 'gleason_dimension_2_counterexample', 'is_entangled_pure_state', 'is_orthonormal_frame', 'is_same', 'is_unitary', 'is_valid_povm', 'non_selective_measurement_decoherence', 'partial_trace', 'povm_probabilities', 'primitive_difference', 'rational_pythagorean_frames_d2', 'schmidt_decomposition', 'sorkin_3slit_parameter', 'superposition_interference_test', 'superposition_quotient_fiber', 'two_path_interference', 'verify_born_normalization_redundancy', 'verify_cptp_contractivity', 'verify_gleason_frame_additivity', 'verify_mermin_peres_contextuality', 'verify_non_signaling', 'verify_ray_invariance', 'weights_to_born_density', 'weights_to_probabilities']
