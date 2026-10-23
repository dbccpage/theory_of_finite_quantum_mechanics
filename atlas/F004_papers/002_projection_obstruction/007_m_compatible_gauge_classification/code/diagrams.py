"""Finite edge diagrams, path coherence, S9b necessity verification, and d0 coboundaries for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence, Callable, Dict, Tuple, List, Set
import numpy as np

Gauge = Callable[[np.ndarray], float]


class InvalidWeightError(ValueError):
    """Raised when edge weights are non-positive, NaN, infinite, or complex."""

    pass


class PresheafRestrictionError(ValueError):
    """Raised when presheaf restriction maps fail path coherence F(a <= c) = F(b <= c) o F(a <= b)."""

    pass


@dataclass(frozen=True)
class EdgeDiagram:
    """Finite covering-edge Banach presheaf diagram over a finite poset."""

    edges: tuple[tuple[int, int], ...]  # list of edges (source, target)
    edge_weights: tuple[float, ...]  # edge scalar weights w_e > 0
    edge_gauges: tuple[Gauge, ...]  # edge native norms nu_e

    def __post_init__(self) -> None:
        if len(self.edges) != len(self.edge_weights):
            raise ValueError("Edge count mismatch with edge_weights")
        if len(self.edges) != len(self.edge_gauges):
            raise ValueError("Edge count mismatch with edge_gauges")

        for idx, w in enumerate(self.edge_weights):
            if np.iscomplexobj(w):
                raise TypeError(
                    f"Edge weight at index {idx} must be real, got complex {w}"
                )
            try:
                w_flt = float(w)
            except (ValueError, TypeError) as e:
                raise InvalidWeightError(
                    f"Edge weight at index {idx} is not a valid float: {w}"
                ) from e
            if np.isnan(w_flt):
                raise InvalidWeightError(f"Edge weight at index {idx} is NaN")
            if np.isinf(w_flt):
                raise InvalidWeightError(
                    f"Edge weight at index {idx} is infinite: {w_flt}"
                )
            if w_flt <= 0.0:
                raise InvalidWeightError(
                    f"Edge weights must be strictly positive, got {w_flt} at index {idx}"
                )


def path_coherence_holds(
    f_ab: np.ndarray, f_bc: np.ndarray, f_ac: np.ndarray, atol: float = 1e-9
) -> bool:
    """Verify presheaf path coherence F(a <= c) = F(b <= c) o F(a <= b)."""
    ab = np.asarray(f_ab, dtype=float)
    bc = np.asarray(f_bc, dtype=float)
    ac = np.asarray(f_ac, dtype=float)
    return bool(np.allclose(bc @ ab, ac, atol=atol))


def validate_presheaf_restrictions(
    restrictions: Dict[Tuple[int, int], np.ndarray],
    triangles: Sequence[Tuple[int, int, int]],
    atol: float = 1e-9,
) -> bool:
    """Validate that presheaf restriction maps satisfy path coherence on all 2-simplices.

    For each triangle (u, v, w) with u < v < w, asserts:
        R_{vw} @ R_{uv} == R_{uw}
    Raises PresheafRestrictionError on violation.
    """
    for u, v, w in triangles:
        if (u, v) not in restrictions:
            raise PresheafRestrictionError(
                f"Missing restriction map for edge ({u}, {v})"
            )
        if (v, w) not in restrictions:
            raise PresheafRestrictionError(
                f"Missing restriction map for edge ({v}, {w})"
            )
        if (u, w) not in restrictions:
            raise PresheafRestrictionError(
                f"Missing restriction map for edge ({u}, {w})"
            )

        r_uv = restrictions[(u, v)]
        r_vw = restrictions[(v, w)]
        r_uw = restrictions[(u, w)]

        composed = r_vw @ r_uv
        diff = np.max(np.abs(composed - r_uw))
        if diff > atol:
            raise PresheafRestrictionError(
                f"Presheaf restriction path coherence failure on triangle ({u}, {v}, {w}): "
                f"max deviation {diff:.4e} > atol {atol:.4e}"
            )
    return True


def evaluate_p1_edgewise_sum(
    diagram: EdgeDiagram, edge_cochain_components: Sequence[np.ndarray]
) -> float:
    """Evaluate edgewise weighted l1 sum diagnostic D(s) = sum_e w_e nu_e(delta_e s).

    P1 edgewise additivity forces global diagnostic to be a weighted l1 sum over edge components.
    Uses math.fsum for full IEEE 754 exactness across disparate scales.
    """
    if len(edge_cochain_components) != len(diagram.edges):
        raise ValueError("Cochain components count mismatch with diagram edge count")

    terms = [
        float(w) * float(nu(delta_e))
        for w, nu, delta_e in zip(
            diagram.edge_weights, diagram.edge_gauges, edge_cochain_components
        )
    ]
    return float(math.fsum(terms))


def evaluate_max_edgewise(
    diagram: EdgeDiagram, edge_cochain_components: Sequence[np.ndarray]
) -> float:
    """Evaluate bottleneck max diagnostic nu_max(delta) = max_e ||delta_e|| (violates P1)."""
    if len(edge_cochain_components) != len(diagram.edges):
        raise ValueError("Cochain components count mismatch with diagram edge count")
    if not edge_cochain_components:
        return 0.0
    return float(
        max(float(nu(c)) for nu, c in zip(diagram.edge_gauges, edge_cochain_components))
    )


def evaluate_zero_diagnostic(
    diagram: EdgeDiagram, edge_cochain_components: Sequence[np.ndarray]
) -> float:
    """Evaluate zero diagnostic nu_zero(delta) = 0.0 (violates P2 faithfulness)."""
    if len(edge_cochain_components) != len(diagram.edges):
        raise ValueError("Cochain components count mismatch with diagram edge count")
    return 0.0


def evaluate_anisotropic_edgewise_sum(
    diagram: EdgeDiagram,
    edge_cochain_components: Sequence[np.ndarray],
    weights_per_dim: Sequence[float] = (1.0, 2.0),
) -> float:
    """Evaluate anisotropic edgewise sum diagnostic (violates P3 maximal symmetry)."""
    if len(edge_cochain_components) != len(diagram.edges):
        raise ValueError("Cochain components count mismatch with diagram edge count")

    dim_w = np.asarray(weights_per_dim, dtype=float)
    total = 0.0
    for delta_e in edge_cochain_components:
        arr = np.abs(np.asarray(delta_e, dtype=float).ravel())
        if arr.shape[0] != dim_w.shape[0]:
            raise ValueError("Dimension mismatch between vector and weights_per_dim")
        total += float(np.sum(dim_w * arr))
    return float(total)


def stiff_weight_condition_number(diagram: EdgeDiagram) -> float:
    """Compute stiff condition number kappa(w) = max(w) / min(w) across edge weights."""
    if not diagram.edge_weights:
        return 1.0
    return float(max(diagram.edge_weights) / min(diagram.edge_weights))


def diagram_connected_components(diagram: EdgeDiagram) -> List[List[int]]:
    """Partition edges into connected components based on shared vertices.

    Returns a list of edge-index lists for each connected component.
    """
    if not diagram.edges:
        return []

    # Map each vertex to its incident edge indices
    vertex_to_edges: Dict[int, List[int]] = {}
    for e_idx, (u, v) in enumerate(diagram.edges):
        vertex_to_edges.setdefault(u, []).append(e_idx)
        vertex_to_edges.setdefault(v, []).append(e_idx)

    visited_edges: Set[int] = set()
    components: List[List[int]] = []

    for start_edge in range(len(diagram.edges)):
        if start_edge in visited_edges:
            continue
        comp: List[int] = []
        queue = [start_edge]
        visited_edges.add(start_edge)

        while queue:
            curr_edge = queue.pop(0)
            comp.append(curr_edge)
            u, v = diagram.edges[curr_edge]
            for neighbor_edge in vertex_to_edges[u] + vertex_to_edges[v]:
                if neighbor_edge not in visited_edges:
                    visited_edges.add(neighbor_edge)
                    queue.append(neighbor_edge)

        components.append(sorted(comp))

    return components


def audit_disconnected_component_decoupling(
    diagram: EdgeDiagram,
    cochain: Sequence[np.ndarray],
    perturbation: np.ndarray,
    target_edge_idx: int,
) -> Dict[str, float | bool]:
    """Verify that a defect injected into one component does not alter gauge values in other components."""
    comps = diagram_connected_components(diagram)
    if len(comps) < 2:
        raise ValueError("Diagram must have at least 2 disconnected components to test decoupling")

    # Find which component contains target_edge_idx
    target_comp_idx = -1
    for c_idx, comp in enumerate(comps):
        if target_edge_idx in comp:
            target_comp_idx = c_idx
            break

    if target_comp_idx == -1:
        raise IndexError(f"Target edge {target_edge_idx} not found in diagram components")

    # Baseline evaluation per component
    def component_val(c_indices: Sequence[int], cochain_vecs: Sequence[np.ndarray]) -> float:
        sub_diag = EdgeDiagram(
            edges=tuple(diagram.edges[i] for i in c_indices),
            edge_weights=tuple(diagram.edge_weights[i] for i in c_indices),
            edge_gauges=tuple(diagram.edge_gauges[i] for i in c_indices),
        )
        sub_cochain = [cochain_vecs[i] for i in c_indices]
        return evaluate_p1_edgewise_sum(sub_diag, sub_cochain)

    base_vals = [component_val(comp, cochain) for comp in comps]

    # Apply perturbation to target edge
    perturbed_cochain = [np.array(v, copy=True) for v in cochain]
    perturbed_cochain[target_edge_idx] = perturbed_cochain[target_edge_idx] + perturbation

    new_vals = [component_val(comp, perturbed_cochain) for comp in comps]

    # Target component must change
    target_delta = abs(new_vals[target_comp_idx] - base_vals[target_comp_idx])

    # Other components must have EXACTLY 0 change
    other_deltas = [
        abs(new_vals[i] - base_vals[i])
        for i in range(len(comps))
        if i != target_comp_idx
    ]
    max_other_delta = max(other_deltas) if other_deltas else 0.0

    return {
        "decoupled": bool(max_other_delta <= 1e-12 and target_delta > 1e-9),
        "target_delta": float(target_delta),
        "max_other_delta": float(max_other_delta),
        "num_components": len(comps),
    }


# ============================================================================
# S9b TWO-SIDED INDEPENDENCE & NECESSITY VERIFICATION
# ============================================================================


@dataclass(frozen=True)
class S9bNecessityRow:
    """A row in the two-sided necessity table (S9b)."""

    name: str
    dropped_property: str
    p1_additive: bool
    p2_faithful: bool
    p3_maximal_symmetry: bool
    p4_uniform: bool
    is_two_sided_witness: bool


def check_p1_additivity(
    diagnostic_fn: Callable[[Sequence[np.ndarray]], float],
    cochain1: Sequence[np.ndarray],
    cochain2: Sequence[np.ndarray],
    atol: float = 1e-9,
) -> bool:
    """Verify P1 edgewise additivity D(c1 + c2) = D(c1) + D(c2) for disjointly supported cochains."""
    val1 = diagnostic_fn(cochain1)
    val2 = diagnostic_fn(cochain2)
    sum_cochain = [c1 + c2 for c1, c2 in zip(cochain1, cochain2)]
    val_sum = diagnostic_fn(sum_cochain)
    return bool(abs(val_sum - (val1 + val2)) <= atol)


def check_p2_faithfulness(
    diagnostic_fn: Callable[[Sequence[np.ndarray]], float],
    non_zero_cochains: Sequence[Sequence[np.ndarray]],
    atol: float = 1e-9,
) -> bool:
    """Verify P2 faithfulness: D(c) > atol for all non-zero cochains, and D(0) = 0."""
    zero_cochain = [np.zeros_like(c) for c in non_zero_cochains[0]]
    if abs(diagnostic_fn(zero_cochain)) > atol:
        return False
    for c in non_zero_cochains:
        if diagnostic_fn(c) <= atol:
            return False
    return True


def check_p3_maximal_symmetry(
    diagram: EdgeDiagram,
    probe_operators: Sequence[np.ndarray] | None = None,
    probe_vectors: Sequence[np.ndarray] | None = None,
    atol: float = 1e-9,
) -> bool:
    """Verify P3 maximal bounded-linear symmetry across all edge stalks."""
    if probe_operators is None:
        # Default reflection, permutation, and scaling operators
        probe_operators = [
            np.array([[-1.0, 0.0], [0.0, 1.0]]),
            np.array([[0.0, 1.0], [1.0, 0.0]]),
            np.array([[1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)], [1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)]]),
        ]
    if probe_vectors is None:
        probe_vectors = [
            np.array([1.0, 0.0]),
            np.array([0.0, 1.0]),
            np.array([1.0, 1.0]),
        ]

    for nu in diagram.edge_gauges:
        for T in probe_operators:
            # Op norm under l2
            op_norm = float(np.linalg.norm(T, 2))
            for v in probe_vectors:
                val_v = nu(v)
                val_Tv = nu(T @ v)
                if val_Tv > op_norm * val_v + atol:
                    return False
    return True


def check_p4_edge_uniformity(diagram: EdgeDiagram, atol: float = 1e-9) -> bool:
    """Verify P4 edge uniformity: all edge weights are identical within atol."""
    if not diagram.edge_weights:
        return True
    return bool((max(diagram.edge_weights) - min(diagram.edge_weights)) <= atol)


def verify_s9b_two_sided_necessity_table() -> Dict[str, S9bNecessityRow]:
    """Explicitly verify the complete two-sided necessity table (S9b).

    Evaluates:
      1. nu_max (drops P1): fails P1, satisfies P2, P3, P4.
      2. nu_zero (drops P2): fails P2, satisfies P1, P3, P4.
      3. nu_aniso (drops P3): fails P3, satisfies P1, P2, P4.
      4. nu_weighted (drops P4): fails P4, satisfies P1, P2, P3.
      5. nu_uniform (canonical): satisfies P1, P2, P3, P4.
    """
    from norms import l2

    edges = ((0, 1), (1, 2))

    # Standard cochain test probes on R^2
    c1 = [np.array([1.0, 0.0]), np.array([0.0, 0.0])]  # supported on e0
    c2 = [np.array([0.0, 0.0]), np.array([0.0, 1.0])]  # supported on e1
    sample_cochains = [
        [np.array([1.0, 0.0]), np.array([0.0, 1.0])],
        [np.array([3.0, -4.0]), np.array([1.0, 2.0])],
    ]

    # 1. nu_max (Drops P1)
    diag_max = EdgeDiagram(edges, (1.0, 1.0), (l2, l2))
    p1_max = check_p1_additivity(lambda c: evaluate_max_edgewise(diag_max, c), c1, c2)
    p2_max = check_p2_faithfulness(lambda c: evaluate_max_edgewise(diag_max, c), sample_cochains)
    p3_max = check_p3_maximal_symmetry(diag_max)
    p4_max = check_p4_edge_uniformity(diag_max)

    row_max = S9bNecessityRow(
        name="nu_max",
        dropped_property="P1",
        p1_additive=p1_max,
        p2_faithful=p2_max,
        p3_maximal_symmetry=p3_max,
        p4_uniform=p4_max,
        is_two_sided_witness=(not p1_max and p2_max and p3_max and p4_max),
    )

    # 2. nu_zero (Drops P2)
    diag_zero = EdgeDiagram(edges, (1.0, 1.0), (l2, l2))
    p1_zero = check_p1_additivity(lambda c: evaluate_zero_diagnostic(diag_zero, c), c1, c2)
    p2_zero = check_p2_faithfulness(lambda c: evaluate_zero_diagnostic(diag_zero, c), sample_cochains)
    p3_zero = check_p3_maximal_symmetry(diag_zero)
    p4_zero = check_p4_edge_uniformity(diag_zero)

    row_zero = S9bNecessityRow(
        name="nu_zero",
        dropped_property="P2",
        p1_additive=p1_zero,
        p2_faithful=p2_zero,
        p3_maximal_symmetry=p3_zero,
        p4_uniform=p4_zero,
        is_two_sided_witness=(p1_zero and not p2_zero and p3_zero and p4_zero),
    )

    # 3. nu_aniso (Drops P3)
    def aniso(v: np.ndarray) -> float:
        a = np.asarray(v, dtype=float).ravel()
        return float(abs(a[0]) + 2.0 * abs(a[1]))

    diag_aniso = EdgeDiagram(edges, (1.0, 1.0), (aniso, aniso))
    p1_aniso = check_p1_additivity(lambda c: evaluate_p1_edgewise_sum(diag_aniso, c), c1, c2)
    p2_aniso = check_p2_faithfulness(lambda c: evaluate_p1_edgewise_sum(diag_aniso, c), sample_cochains)
    p3_aniso = check_p3_maximal_symmetry(diag_aniso)
    p4_aniso = check_p4_edge_uniformity(diag_aniso)

    row_aniso = S9bNecessityRow(
        name="nu_aniso",
        dropped_property="P3",
        p1_additive=p1_aniso,
        p2_faithful=p2_aniso,
        p3_maximal_symmetry=p3_aniso,
        p4_uniform=p4_aniso,
        is_two_sided_witness=(p1_aniso and p2_aniso and not p3_aniso and p4_aniso),
    )

    # 4. nu_weighted (Drops P4)
    diag_weighted = EdgeDiagram(edges, (1.0, 3.0), (l2, l2))
    p1_weighted = check_p1_additivity(lambda c: evaluate_p1_edgewise_sum(diag_weighted, c), c1, c2)
    p2_weighted = check_p2_faithfulness(lambda c: evaluate_p1_edgewise_sum(diag_weighted, c), sample_cochains)
    p3_weighted = check_p3_maximal_symmetry(diag_weighted)
    p4_weighted = check_p4_edge_uniformity(diag_weighted)

    row_weighted = S9bNecessityRow(
        name="nu_weighted",
        dropped_property="P4",
        p1_additive=p1_weighted,
        p2_faithful=p2_weighted,
        p3_maximal_symmetry=p3_weighted,
        p4_uniform=p4_weighted,
        is_two_sided_witness=(p1_weighted and p2_weighted and p3_weighted and not p4_weighted),
    )

    # 5. nu_uniform (Target Unique Canonical)
    diag_uniform = EdgeDiagram(edges, (2.0, 2.0), (l2, l2))
    p1_u = check_p1_additivity(lambda c: evaluate_p1_edgewise_sum(diag_uniform, c), c1, c2)
    p2_u = check_p2_faithfulness(lambda c: evaluate_p1_edgewise_sum(diag_uniform, c), sample_cochains)
    p3_u = check_p3_maximal_symmetry(diag_uniform)
    p4_u = check_p4_edge_uniformity(diag_uniform)

    row_uniform = S9bNecessityRow(
        name="nu_uniform",
        dropped_property="None",
        p1_additive=p1_u,
        p2_faithful=p2_u,
        p3_maximal_symmetry=p3_u,
        p4_uniform=p4_u,
        is_two_sided_witness=(p1_u and p2_u and p3_u and p4_u),
    )

    return {
        "nu_max": row_max,
        "nu_zero": row_zero,
        "nu_aniso": row_aniso,
        "nu_weighted": row_weighted,
        "nu_uniform": row_uniform,
    }
