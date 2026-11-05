"""M-compatible gauges, convex body duality, and CPTP rigidity facade for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Callable, Sequence
import numpy as np

from norms import (
    l1,
    l2,
    linf,
    anisotropic_gauge,
    exact_induced_operator_norm,
    sample_lower_bound_induced_norm,
)
from convex import (
    minkowski_functional,
    unit_ball_scaling,
    polytope_unit_ball_membership,
    probe_minkowski_boundary_continuity,
)
from diagrams import (
    EdgeDiagram,
    InvalidWeightError,
    PresheafRestrictionError,
    path_coherence_holds,
    evaluate_p1_edgewise_sum,
    evaluate_max_edgewise,
    evaluate_zero_diagnostic,
    evaluate_anisotropic_edgewise_sum,
    stiff_weight_condition_number,
    diagram_connected_components,
    audit_disconnected_component_decoupling,
    validate_presheaf_restrictions,
    S9bNecessityRow,
    check_p1_additivity,
    check_p2_faithfulness,
    check_p3_maximal_symmetry,
    check_p4_edge_uniformity,
    verify_s9b_two_sided_necessity_table,
)
from rigidity import (
    rank_one_map,
    construct_hahn_banach_rank_one,
    is_maximal_end_compatible,
)
from cptp import (
    cptp_measure_and_prepare,
    is_cptp_trace_norm_rigid,
    trace_norm,
    is_hermitian_trace_zero,
)
from probes import (
    CounterexampleResult,
    probe_counterexample_search,
)

Gauge = Callable[[np.ndarray], float]


def is_faithful(
    j: Gauge, sample_vectors: Sequence[np.ndarray], atol: float = 1e-9
) -> bool:
    """Check faithfulness j(x) > 0 for all non-zero sample vectors."""
    if atol < 0:
        raise ValueError("Tolerance atol must be non-negative")
    for v in sample_vectors:
        if np.iscomplexobj(v):
            raise TypeError("Real vector inputs required")
        arr = np.asarray(v, dtype=float)
        if not np.allclose(arr, 0.0, atol=atol) and j(arr) <= atol:
            return False
    return True


def is_absolutely_homogeneous(
    j: Gauge, x: np.ndarray, scalars: Sequence[float], atol: float = 1e-9
) -> bool:
    """Check absolute homogeneity j(c x) = |c| j(x) over scalars."""
    if atol < 0:
        raise ValueError("Tolerance atol must be non-negative")
    if np.iscomplexobj(x):
        raise TypeError("Real vector inputs required")
    arr = np.asarray(x, dtype=float)
    base = j(arr)
    for c in scalars:
        if abs(j(c * arr) - abs(c) * base) > atol:
            return False
    return True


def is_subadditive(
    j: Gauge, vector_pairs: Sequence[tuple[np.ndarray, np.ndarray]], atol: float = 1e-9
) -> bool:
    """Check subadditivity j(u + v) <= j(u) + j(v) over vector pairs."""
    if atol < 0:
        raise ValueError("Tolerance atol must be non-negative")
    for u, v in vector_pairs:
        if np.iscomplexobj(u) or np.iscomplexobj(v):
            raise TypeError("Real vector inputs required")
        u_arr = np.asarray(u, dtype=float)
        v_arr = np.asarray(v, dtype=float)
        if j(u_arr + v_arr) > j(u_arr) + j(v_arr) + atol:
            return False
    return True


def is_m_compatible(
    j: Gauge,
    operators: Sequence[np.ndarray],
    ambient_norm: Gauge = l2,
    probe_vectors: Sequence[np.ndarray] | None = None,
    atol: float = 1e-9,
) -> bool:
    """Check compatibility j(T x) <= ||T||_{ambient -> ambient} j(x) over operators and probe vectors."""
    if atol < 0:
        raise ValueError("Tolerance atol must be non-negative")
    if probe_vectors is None:
        probe_vectors = [
            np.array([1.0, 0.0]),
            np.array([0.0, 1.0]),
            np.array([1.0, 1.0]),
        ]

    for T in operators:
        arr = np.asarray(T, dtype=float)
        if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
            raise ValueError("Operators must be square real matrices")
        op_norm = exact_induced_operator_norm(arr, "l2", "l2")
        for v in probe_vectors:
            v_arr = np.asarray(v, dtype=float)
            j_v = j(v_arr)
            j_Tv = j(arr @ v_arr)
            if j_Tv > op_norm * j_v + atol:
                return False
    return True


def monoid_trivial(n: int = 2) -> list[np.ndarray]:
    """Trivial monoid {I_n}."""
    return [np.eye(n)]


def monoid_signed_permutations_r2() -> list[np.ndarray]:
    """Octic group C_4v (signed permutation matrices) on R^2."""
    return [
        np.array([[1.0, 0.0], [0.0, 1.0]]),
        np.array([[-1.0, 0.0], [0.0, 1.0]]),
        np.array([[1.0, 0.0], [0.0, -1.0]]),
        np.array([[-1.0, 0.0], [0.0, -1.0]]),
        np.array([[0.0, 1.0], [1.0, 0.0]]),
        np.array([[0.0, -1.0], [1.0, 0.0]]),
        np.array([[0.0, 1.0], [-1.0, 0.0]]),
        np.array([[0.0, -1.0], [-1.0, 0.0]]),
    ]


def cyclic_rotation_group_c4() -> list[np.ndarray]:
    """Cyclic rotation group C_4 (90-degree rotations) on R^2."""
    return [
        np.array([[1.0, 0.0], [0.0, 1.0]]),
        np.array([[0.0, -1.0], [1.0, 0.0]]),
        np.array([[-1.0, 0.0], [0.0, -1.0]]),
        np.array([[0.0, 1.0], [-1.0, 0.0]]),
    ]


def monoid_so2_discrete(n_samples: int = 16) -> list[np.ndarray]:
    """Sample discrete rotations in SO(2)."""
    angles = np.linspace(0, 2 * np.pi, n_samples, endpoint=False)
    return [np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]) for a in angles]


__all__ = [
    "l1",
    "l2",
    "linf",
    "anisotropic_gauge",
    "exact_induced_operator_norm",
    "sample_lower_bound_induced_norm",
    "minkowski_functional",
    "unit_ball_scaling",
    "polytope_unit_ball_membership",
    "probe_minkowski_boundary_continuity",
    "EdgeDiagram",
    "InvalidWeightError",
    "PresheafRestrictionError",
    "path_coherence_holds",
    "evaluate_p1_edgewise_sum",
    "evaluate_max_edgewise",
    "evaluate_zero_diagnostic",
    "evaluate_anisotropic_edgewise_sum",
    "stiff_weight_condition_number",
    "diagram_connected_components",
    "audit_disconnected_component_decoupling",
    "validate_presheaf_restrictions",
    "S9bNecessityRow",
    "check_p1_additivity",
    "check_p2_faithfulness",
    "check_p3_maximal_symmetry",
    "check_p4_edge_uniformity",
    "verify_s9b_two_sided_necessity_table",
    "rank_one_map",
    "construct_hahn_banach_rank_one",
    "is_maximal_end_compatible",
    "cptp_measure_and_prepare",
    "is_cptp_trace_norm_rigid",
    "trace_norm",
    "is_hermitian_trace_zero",
    "CounterexampleResult",
    "probe_counterexample_search",
    "is_faithful",
    "is_absolutely_homogeneous",
    "is_subadditive",
    "is_m_compatible",
    "monoid_trivial",
    "monoid_signed_permutations_r2",
    "cyclic_rotation_group_c4",
    "monoid_so2_discrete",
]
