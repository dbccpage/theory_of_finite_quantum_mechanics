"""Adversarial Perturbations, Fault Injections, Audits, and Recovery Operators for GS-000.

AuthorityEffect: None. Break-and-recover harness across axioms H1-H5, quantum operator supports, and gauge holonomies.
"""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np
from coord_additivity import Seminorm, coord_l1

# ==============================================================================
# 1. Coordinate Permutation Symmetry (H2)
# ==============================================================================

def inject_anisotropic_shear(k: int, shear_factor: float = 2.0) -> tuple[float, ...]:
    """Inject unequal coordinate weights violating H2 permutation symmetry."""
    if k < 2:
        raise ValueError("Dimension must be at least 2 for coordinate symmetry")
    if shear_factor <= 1.0:
        raise ValueError("shear_factor must be > 1.0")
    weights = [1.0] + [shear_factor] * (k - 1)
    return tuple(weights)


def audit_coordinate_symmetry(
    weights: Sequence[float],
    atol: float = 1e-9,
) -> tuple[bool, float]:
    """Audit whether coordinate weights are isotropic (permutation symmetric).

    Returns (is_compliant, max_discrepancy).
    """
    w_arr = np.asarray(weights, dtype=float)
    if w_arr.size <= 1:
        return True, 0.0
    diff = float(np.max(w_arr) - np.min(w_arr))
    return (diff <= atol, diff)


def recover_permutation_symmetry(weights: Sequence[float]) -> tuple[float, ...]:
    """Recover H2 compliance by projecting anisotropic weights to their isotropic mean."""
    w_arr = np.asarray(weights, dtype=float)
    mean_w = float(np.mean(w_arr))
    return tuple([mean_w] * len(weights))


# ==============================================================================
# 2. Disjoint-Coordinate Additivity (H3)
# ==============================================================================

def inject_cross_coordinate_coupling(coupling_strength: float = 0.5) -> Seminorm:
    """Inject non-additive cross-coordinate coupling: ν(x) = ||x||_1 + ε * sqrt(|x0 * x1|)."""
    if coupling_strength <= 0.0:
        raise ValueError("coupling_strength must be > 0.0")

    def coupled_nu(x: np.ndarray) -> float:
        v = np.asarray(x, dtype=float).ravel()
        base = coord_l1(v)
        if len(v) >= 2:
            cross = coupling_strength * np.sqrt(abs(v[0] * v[1]))
            return float(base + cross)
        return float(base)

    return coupled_nu


def audit_disjoint_additivity(
    nu: Seminorm,
    dim: int,
    test_scale: float = 1.0,
    atol: float = 1e-9,
) -> tuple[bool, float]:
    """Audit H3 disjoint-coordinate additivity on standard basis vectors:

    Checks |ν(e0 + e1) - (ν(e0) + ν(e1))|.
    """
    if dim < 2:
        return True, 0.0
    e0 = np.zeros(dim, dtype=float)
    e1 = np.zeros(dim, dtype=float)
    e0[0] = test_scale
    e1[1] = test_scale

    val_sum = nu(e0 + e1)
    val_add = nu(e0) + nu(e1)
    discrepancy = float(abs(val_sum - val_add))
    return (discrepancy <= atol, discrepancy)


def recover_disjoint_additivity(nu_corrupted: Seminorm, dim: int) -> Seminorm:
    """Recover H3 compliance by extracting basis weights w_i = ν(e_i) and synthesizing uncoupled l1."""
    weights = [nu_corrupted(np.eye(dim, dtype=float)[i]) for i in range(dim)]
    mean_w = float(np.mean(weights))

    def clean_nu(x: np.ndarray) -> float:
        return float(mean_w * np.sum(np.abs(np.asarray(x, dtype=float).ravel())))

    return clean_nu


# ==============================================================================
# 3. Edge Locality (H1)
# ==============================================================================

def inject_cross_edge_coupling(
    coupling_strength: float = 0.5,
) -> Callable[[list[np.ndarray]], float]:
    """Inject cross-edge coupling: ν_G(δ) = sum_e ||δ_e||_1 + ε * |sum_e δ_{e,0}|."""
    if coupling_strength <= 0.0:
        raise ValueError("coupling_strength must be > 0.0")

    def non_local_nu(edge_vectors: list[np.ndarray]) -> float:
        total_l1 = sum(coord_l1(ev) for ev in edge_vectors)
        cross_sum = sum(ev[0] if len(ev) > 0 else 0.0 for ev in edge_vectors)
        return float(total_l1 + coupling_strength * abs(cross_sum))

    return non_local_nu


def audit_edge_locality(
    global_nu: Callable[[list[np.ndarray]], float],
    num_edges: int,
    k: int,
    atol: float = 1e-9,
) -> tuple[bool, float]:
    """Audit whether global_nu decomposes additively across edges:

    Tests ν_G(δ_1 ⊕ δ_2) == ν_G(δ_1 ⊕ 0) + ν_G(0 ⊕ δ_2).
    """
    if num_edges < 2:
        return True, 0.0
    v1 = np.ones(k, dtype=float)
    v2 = -np.ones(k, dtype=float)

    # State with edge 0 active, others 0
    state_0 = [v1 if e == 0 else np.zeros(k) for e in range(num_edges)]
    # State with edge 1 active, others 0
    state_1 = [v2 if e == 1 else np.zeros(k) for e in range(num_edges)]
    # Combined state
    state_comb = [v1 if e == 0 else (v2 if e == 1 else np.zeros(k)) for e in range(num_edges)]

    val_comb = global_nu(state_comb)
    val_sep = global_nu(state_0) + global_nu(state_1)
    discrepancy = float(abs(val_comb - val_sep))
    return (discrepancy <= atol, discrepancy)


def recover_edge_locality(
    corrupted_global_nu: Callable[[list[np.ndarray]], float],
    num_edges: int,
    k: int,
) -> Callable[[list[np.ndarray]], float]:
    """Recover H1 compliance by decoupling: isolate each edge's contribution and sum."""
    def clean_global_nu(edge_vectors: list[np.ndarray]) -> float:
        total = 0.0
        for e, ev in enumerate(edge_vectors):
            isolated = [ev if i == e else np.zeros(k) for i in range(num_edges)]
            total += corrupted_global_nu(isolated)
        return float(total)

    return clean_global_nu


# ==============================================================================
# 4. Absolute Homogeneity (H5)
# ==============================================================================

def inject_non_homogeneous_scaling(power_p: float = 2.0) -> Seminorm:
    """Inject non-homogeneous power gauge: ν(x) = sum |x_i|^p."""
    if abs(power_p - 1.0) < 1e-6:
        raise ValueError("power_p must be different from 1.0")

    def power_nu(x: np.ndarray) -> float:
        return float(np.sum(np.abs(np.asarray(x, dtype=float).ravel()) ** power_p))

    return power_nu


def audit_homogeneity(
    nu: Seminorm,
    probe: np.ndarray,
    scalar: float = 2.0,
    atol: float = 1e-9,
) -> tuple[bool, float]:
    """Audit H5 homogeneity: |ν(c * x) - |c| * ν(x)|."""
    val_scaled = nu(scalar * probe)
    val_expected = abs(scalar) * nu(probe)
    discrepancy = float(abs(val_scaled - val_expected))
    return (discrepancy <= atol, discrepancy)


def recover_homogeneity(nu_power: Seminorm, dim: int) -> Seminorm:
    """Recover H5 homogeneity by linearizing around unit probe."""
    unit_probe = np.zeros(dim, dtype=float)
    unit_probe[0] = 1.0
    w = float(nu_power(unit_probe))

    def clean_nu(x: np.ndarray) -> float:
        return float(w * np.sum(np.abs(np.asarray(x, dtype=float).ravel())))

    return clean_nu


# ==============================================================================
# 5. Orbit Weight Uniformity (H4 / Theorem 3)
# ==============================================================================

def inject_orbit_weight_asymmetry(
    base_weights: Sequence[float],
    skew_factor: float = 2.5,
) -> tuple[float, ...]:
    """Inject asymmetry across orbit weights."""
    if len(base_weights) < 2:
        raise ValueError("Must have at least 2 orbits to inject asymmetry")
    out = list(base_weights)
    out[0] = out[0] * skew_factor
    return tuple(out)


def audit_orbit_uniformity(
    orbit_weights: Sequence[float],
    atol: float = 1e-9,
) -> tuple[bool, float]:
    """Audit whether all orbit weights are identical within atol."""
    w_arr = np.asarray(orbit_weights, dtype=float)
    if w_arr.size <= 1:
        return True, 0.0
    spread = float(np.max(w_arr) - np.min(w_arr))
    return (spread <= atol, spread)


def recover_orbit_uniformity(orbit_weights: Sequence[float]) -> tuple[float, ...]:
    """Recover edge-uniformity by setting all weights to the arithmetic mean."""
    mean_w = float(np.mean(orbit_weights))
    return tuple([mean_w] * len(orbit_weights))


# ==============================================================================
# 6. Quantum Orthogonal Operator Support
# ==============================================================================

def inject_quantum_support_leakage(
    a: np.ndarray,
    b: np.ndarray,
    leakage_angle: float = 0.3,
) -> np.ndarray:
    """Perturb operator B by rotating it into the subspace of A, breaking orthogonality:

    B_leaked = cos(theta) * B + sin(theta) * (A / ||A||_F) * ||B||_F.
    """
    ma = np.asarray(a, dtype=complex)
    mb = np.asarray(b, dtype=complex)
    norm_a = np.linalg.norm(ma, "fro")
    norm_b = np.linalg.norm(mb, "fro")
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Operators must be non-zero")

    a_normalized = ma / norm_a
    b_leaked = np.cos(leakage_angle) * mb + np.sin(leakage_angle) * (a_normalized * norm_b)
    return b_leaked


def audit_orthogonal_support(
    a: np.ndarray,
    b: np.ndarray,
    atol: float = 1e-9,
) -> tuple[bool, float]:
    """Audit whether A and B have mutually orthogonal support (AB^dagger = 0 and A^dagger B = 0)."""
    ma = np.asarray(a, dtype=complex)
    mb = np.asarray(b, dtype=complex)
    ab_dag = ma @ mb.conj().T
    a_dag_b = ma.conj().T @ mb
    leakage = float(max(np.linalg.norm(ab_dag), np.linalg.norm(a_dag_b)))
    return (leakage <= atol, leakage)


def recover_orthogonal_support(a: np.ndarray, b_corrupted: np.ndarray) -> np.ndarray:
    """Recover orthogonal support by projecting b_corrupted onto the orthogonal complements

    of the range and co-range of A.
    """
    ma = np.asarray(a, dtype=complex)
    mb = np.asarray(b_corrupted, dtype=complex)

    u, s, vh = np.linalg.svd(ma, full_matrices=True)
    tol = 1e-12
    rank = int(np.sum(s > tol))

    # Projectors onto orthogonal complements
    # Range of A is spanned by first `rank` columns of u.
    # Co-range is spanned by first `rank` rows of vh (columns of v).
    dim_m, dim_n = ma.shape
    p_range_perp = np.eye(dim_m, dtype=complex) - u[:, :rank] @ u[:, :rank].conj().T
    p_corange_perp = np.eye(dim_n, dtype=complex) - vh[:rank, :].conj().T @ vh[:rank, :]

    b_clean = p_range_perp @ mb @ p_corange_perp
    return b_clean
