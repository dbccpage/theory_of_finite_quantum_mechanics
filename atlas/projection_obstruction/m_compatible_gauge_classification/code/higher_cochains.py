"""Higher-degree cochains, curvature bicomplexes, and C^2 maximal-monoid rigidity for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence, Dict, Tuple, List, Set
import numpy as np

from diagrams import InvalidWeightError, PresheafRestrictionError

Gauge = Callable[[np.ndarray], float]


@dataclass(frozen=True)
class SimplicialPoset2D:
    """A 2-dimensional finite simplicial complex / poset.

    Vertices: 0, ..., n_v - 1
    Edges: tuples of (u, v) with u < v
    Faces: tuples of (u, v, w) with u < v < w
    """

    num_vertices: int
    edges: Tuple[Tuple[int, int], ...]
    faces: Tuple[Tuple[int, int, int], ...]

    def __post_init__(self) -> None:
        if self.num_vertices <= 0:
            raise ValueError("num_vertices must be positive")
        for u, v in self.edges:
            if not (0 <= u < v < self.num_vertices):
                raise ValueError(f"Invalid edge: ({u}, {v})")
        for u, v, w in self.faces:
            if not (0 <= u < v < w < self.num_vertices):
                raise ValueError(f"Invalid face: ({u}, {v}, {w})")
            # All boundary edges must be present
            b_edges = {(u, v), (v, w), (u, w)}
            if not b_edges.issubset(set(self.edges)):
                raise ValueError(
                    f"Face ({u}, {v}, {w}) boundary edges missing from edge set"
                )

    @property
    def num_edges(self) -> int:
        return len(self.edges)

    @property
    def num_faces(self) -> int:
        return len(self.faces)


def poset_connected_components(poset: SimplicialPoset2D) -> List[Set[int]]:
    """Partition vertices of a SimplicialPoset2D into connected components."""
    adj: Dict[int, List[int]] = {i: [] for i in range(poset.num_vertices)}
    for u, v in poset.edges:
        adj[u].append(v)
        adj[v].append(u)

    visited: Set[int] = set()
    components: List[Set[int]] = []

    for v in range(poset.num_vertices):
        if v not in visited:
            comp: Set[int] = set()
            queue = [v]
            visited.add(v)
            while queue:
                curr = queue.pop(0)
                comp.add(curr)
                for nxt in adj[curr]:
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)
            components.append(comp)

    return components


def coboundary_d0(poset: SimplicialPoset2D, c0: np.ndarray) -> np.ndarray:
    """Compute 0-coboundary d_0: C^0 -> C^1.

    (d_0 s)(u, v) = s(v) - s(u)
    """
    s = np.asarray(c0, dtype=float)
    if s.shape[0] != poset.num_vertices:
        raise ValueError(f"c0 length {s.shape[0]} != num_vertices {poset.num_vertices}")

    c1 = np.zeros(poset.num_edges, dtype=float)
    for idx, (u, v) in enumerate(poset.edges):
        c1[idx] = s[v] - s[u]
    return c1


def coboundary_d1(poset: SimplicialPoset2D, c1: np.ndarray) -> np.ndarray:
    """Compute 1-coboundary d_1: C^1 -> C^2.

    For face (u, v, w): (d_1 c)(u, v, w) = c(v, w) - c(u, w) + c(u, v)
    """
    c = np.asarray(c1, dtype=float)
    if c.shape[0] != poset.num_edges:
        raise ValueError(f"c1 length {c.shape[0]} != num_edges {poset.num_edges}")

    edge_index: Dict[Tuple[int, int], int] = {e: i for i, e in enumerate(poset.edges)}
    c2 = np.zeros(poset.num_faces, dtype=float)

    for idx, (u, v, w) in enumerate(poset.faces):
        e_uv = edge_index[(u, v)]
        e_uw = edge_index[(u, w)]
        e_vw = edge_index[(v, w)]
        c2[idx] = c[e_vw] - c[e_uw] + c[e_uv]

    return c2


def verify_chain_complex_property(
    poset: SimplicialPoset2D, c0: np.ndarray, atol: float = 1e-12
) -> bool:
    """Verify exactness condition d_1 o d_0 = 0 on any 0-cochain."""
    c1 = coboundary_d0(poset, c0)
    c2 = coboundary_d1(poset, c1)
    return bool(np.allclose(c2, 0.0, atol=atol))


def coboundary_d0_presheaf(
    poset: SimplicialPoset2D,
    c0_sections: Dict[int, np.ndarray],
    restrictions: Dict[Tuple[int, int], np.ndarray],
) -> Dict[Tuple[int, int], np.ndarray]:
    """Compute presheaf coboundary d_0^{rho}: C^0(F) -> C^1(F).

    For edge (u, v): (d_0^{rho} s)(u, v) = s(v) - R_{uv} s(u).
    """
    for v in range(poset.num_vertices):
        if v not in c0_sections:
            raise ValueError(f"Missing c0 section at vertex {v}")

    c1: Dict[Tuple[int, int], np.ndarray] = {}
    for u, v in poset.edges:
        if (u, v) not in restrictions:
            raise PresheafRestrictionError(f"Missing restriction map for edge ({u}, {v})")
        r_uv = restrictions[(u, v)]
        s_u = np.asarray(c0_sections[u], dtype=float)
        s_v = np.asarray(c0_sections[v], dtype=float)
        c1[(u, v)] = s_v - (r_uv @ s_u)
    return c1


def coboundary_d1_presheaf(
    poset: SimplicialPoset2D,
    c1_cochains: Dict[Tuple[int, int], np.ndarray],
    restrictions: Dict[Tuple[int, int], np.ndarray],
) -> Dict[Tuple[int, int, int], np.ndarray]:
    """Compute presheaf coboundary d_1^{rho}: C^1(F) -> C^2(F).

    For face (u, v, w): (d_1^{rho} c)(u, v, w) = c(v, w) - c(u, w) + R_{vw} c(u, v).
    """
    c2: Dict[Tuple[int, int, int], np.ndarray] = {}
    for u, v, w in poset.faces:
        if (u, v) not in c1_cochains or (v, w) not in c1_cochains or (u, w) not in c1_cochains:
            raise ValueError(f"Missing 1-cochain for boundary of face ({u}, {v}, {w})")
        for e in ((u, v), (v, w), (u, w)):
            if e not in restrictions:
                raise PresheafRestrictionError(f"Missing restriction map for edge {e}")

        r_vw = restrictions[(v, w)]
        c_uv = c1_cochains[(u, v)]
        c_uw = c1_cochains[(u, w)]
        c_vw = c1_cochains[(v, w)]

        c2[(u, v, w)] = c_vw - c_uw + (r_vw @ c_uv)
    return c2


def verify_presheaf_chain_complex(
    poset: SimplicialPoset2D,
    c0_sections: Dict[int, np.ndarray],
    restrictions: Dict[Tuple[int, int], np.ndarray],
    atol: float = 1e-12,
) -> Tuple[bool, float]:
    """Verify d_1^{rho} o d_0^{rho} = 0 under presheaf restrictions.

    Returns (is_exact, max_curvature_norm).
    If path coherence fails: (d_1^{rho} d_0^{rho} s)(u, v, w) = (R_{uw} - R_{vw} R_{uv}) s(u) != 0.
    """
    c1 = coboundary_d0_presheaf(poset, c0_sections, restrictions)
    c2 = coboundary_d1_presheaf(poset, c1, restrictions)

    max_norm = 0.0
    for face, val in c2.items():
        nrm = float(np.linalg.norm(val))
        if nrm > max_norm:
            max_norm = nrm

    return (max_norm <= atol, max_norm)


def c2_curvature_diagnostic(
    poset: SimplicialPoset2D,
    c1: np.ndarray,
    face_weights: Sequence[float] | None = None,
) -> float:
    """Compute C^2 curvature diagnostic Gamma_2(c1) = sum_f w_f |(d_1 c1)_f|."""
    c2 = coboundary_d1(poset, c1)
    if face_weights is None:
        weights = np.ones(poset.num_faces, dtype=float)
    else:
        weights = np.asarray(face_weights, dtype=float)
        if weights.shape[0] != poset.num_faces:
            raise ValueError(
                f"Weights length {weights.shape[0]} != num_faces {poset.num_faces}"
            )
        for idx, w in enumerate(weights):
            if np.isnan(w) or np.isinf(w) or w <= 0:
                raise InvalidWeightError(
                    f"Face weights must be strictly positive and finite, got {w} at index {idx}"
                )

    return float(np.sum(weights * np.abs(c2)))


def c2_maximal_rigidity_check(
    face_stalk_dim: int,
    gauge: Gauge,
    target_norm: Gauge,
    n_probes: int = 50,
    seed: int = 42,
) -> bool:
    """Verify that a C^2 face-stalk gauge compatible with End_b(V_f) is proportional to target_norm.

    Tests direction independence: for random unit vectors u, v (with target_norm(u) = target_norm(v) = 1),
    constructs Hahn-Banach rank-one operator T = v (x) u^* with ||T||_op = 1,
    asserts gauge(v) <= gauge(u) and gauge(u) <= gauge(v).
    """
    rng = np.random.default_rng(seed)
    # Sample unit vectors under target_norm
    unit_vectors = []
    for _ in range(n_probes):
        raw = rng.normal(size=face_stalk_dim)
        nrm = target_norm(raw)
        if nrm > 1e-12:
            unit_vectors.append(raw / nrm)

    if len(unit_vectors) < 2:
        return False

    base_val = gauge(unit_vectors[0])
    if base_val <= 1e-12:
        return False

    for v in unit_vectors[1:]:
        val = gauge(v)
        if abs(val - base_val) > 1e-7:
            return False

    return True
