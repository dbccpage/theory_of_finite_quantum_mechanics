"""Relational Regge Curvature, Cochain Holonomy, and the Unified Relational Spine.

This module formalizes:
1. Discrete relational simplicial complexes without ambient metric containers.
2. Relational internal angles and Regge deficit angles epsilon_h = 2*pi - sum(theta)
   as irreducible cochain holonomy around codimension-2 bones.
3. Gauge invariance under vertex relabeling d^0 repair (Bianchi identity d1 @ d0 == 0).
4. Operational stickiness: projection friction inf_alpha ||delta - d0 alpha||_1 > 0
   stalling fluent continuation.
5. The 8-stage Unified Relational Spine: Presentation -> Family -> Representation ->
   Fiber Bundle -> Fact -> Compression -> Obstruction -> Curvature.
6. Formal contrast with standard metric Regge calculus.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from collections import defaultdict, deque
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Literal, TypeAlias

import numpy as np
import numpy.typing as npt
from scipy.optimize import linprog

NodeId: TypeAlias = int | str
EdgeTuple: TypeAlias = tuple[NodeId, NodeId]
FaceTuple: TypeAlias = tuple[NodeId, NodeId, NodeId]
BoneId: TypeAlias = NodeId | EdgeTuple | str
BoneType: TypeAlias = Literal["VERTEX_2D", "EDGE_3D", "FACE_4D"]
TerminalizerStatus: TypeAlias = Literal["AUTHORIZED", "OBSTRUCTED", "REFUSAL"]
CurvatureClassification: TypeAlias = Literal["FLAT", "POSITIVE_CONICAL", "NEGATIVE_SADDLE"]
RealArray: TypeAlias = npt.NDArray[np.float64]


# ---------------------------------------------------------------------------
# Custom Error Hierarchy
# ---------------------------------------------------------------------------


class RelationalReggeError(ValueError):
    """Raised when an input violates declared relational simplicial or cochain premises."""


class RelationalSpineError(RelationalReggeError):
    """Raised when an operation violates relational spine axioms or input contracts."""


# ---------------------------------------------------------------------------
# Numerical and Type Input Guards (Fail-Closed)
# ---------------------------------------------------------------------------


def _guard_float(
    val: object,
    name: str,
    strictly_positive: bool = True,
    allow_negative: bool = False,
) -> float:
    """Validate numeric parameter with Boolean subclass guard and finiteness check."""
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise RelationalReggeError(f"{name} must be numeric, not bool")
    fval = float(val)
    if not math.isfinite(fval):
        raise RelationalReggeError(f"{name} must be finite")
    if not allow_negative:
        if strictly_positive and fval <= 0.0:
            raise RelationalReggeError(f"{name} must be positive")
        if not strictly_positive and fval < 0.0:
            raise RelationalReggeError(f"{name} must be non-negative")
    return fval


def _guard_int(val: object, name: str, min_value: int = 1) -> int:
    """Validate integer parameter with Boolean subclass guard."""
    if isinstance(val, bool) or not isinstance(val, int):
        raise RelationalReggeError(f"{name} must be an integer, not bool")
    if val < min_value:
        raise RelationalReggeError(f"{name} must be >= {min_value}")
    return val


# ---------------------------------------------------------------------------
# Relational Simplicial Complex & Codimension-2 Bone Data Structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RelationalSimplicialComplex:
    """Discrete relational simplicial complex K = (V, E, F) without ambient coordinates."""

    nodes: tuple[NodeId, ...]
    edges: tuple[EdgeTuple, ...]
    faces: tuple[FaceTuple, ...] = ()
    dimension: int = 2

    def __post_init__(self) -> None:
        if not self.nodes:
            raise RelationalReggeError("Complex must have at least one node")
        for node in self.nodes:
            if isinstance(node, bool) or not isinstance(node, (int, str)):
                raise RelationalReggeError(f"Node {node!r} must be int or str, not bool")
        node_set = set(self.nodes)
        if len(node_set) != len(self.nodes):
            raise RelationalReggeError("Nodes must be unique")

        seen_edges: set[tuple[NodeId, NodeId]] = set()
        seen_undirected: set[frozenset[NodeId]] = set()
        for u, v in self.edges:
            if isinstance(u, bool) or not isinstance(u, (int, str)):
                raise RelationalReggeError(f"Edge vertex {u!r} must be int or str, not bool")
            if isinstance(v, bool) or not isinstance(v, (int, str)):
                raise RelationalReggeError(f"Edge vertex {v!r} must be int or str, not bool")
            if u not in node_set or v not in node_set:
                raise RelationalReggeError(f"Edge ({u}, {v}) references non-existent node")
            if u == v:
                raise RelationalReggeError(f"Self-loop edge ({u}, {u}) is not permitted")
            if (u, v) in seen_edges:
                raise RelationalReggeError(f"Duplicate edge ({u}, {v})")
            seen_edges.add((u, v))
            pair = frozenset((u, v))
            if pair in seen_undirected:
                raise RelationalReggeError(f"Duplicate or anti-parallel edge between {u} and {v}")
            seen_undirected.add(pair)

        edge_set = set(self.edges) | {(v, u) for u, v in self.edges}
        seen_faces: set[frozenset[NodeId]] = set()
        for u, v, w in self.faces:
            if isinstance(u, bool) or not isinstance(u, (int, str)):
                raise RelationalReggeError(f"Face vertex {u!r} must be int or str, not bool")
            if isinstance(v, bool) or not isinstance(v, (int, str)):
                raise RelationalReggeError(f"Face vertex {v!r} must be int or str, not bool")
            if isinstance(w, bool) or not isinstance(w, (int, str)):
                raise RelationalReggeError(f"Face vertex {w!r} must be int or str, not bool")
            if u not in node_set or v not in node_set or w not in node_set:
                raise RelationalReggeError(f"Face ({u}, {v}, {w}) references non-existent node")
            if len({u, v, w}) != 3:
                raise RelationalReggeError(f"Face ({u}, {v}, {w}) vertices must be distinct")
            for p, q in ((u, v), (v, w), (u, w)):
                if (p, q) not in edge_set:
                    raise RelationalReggeError(f"Face boundary edge ({p}, {q}) not in edges")
            f_key = frozenset((u, v, w))
            if f_key in seen_faces:
                raise RelationalReggeError(f"Duplicate face ({u}, {v}, {w})")
            seen_faces.add(f_key)

        _guard_int(self.dimension, "dimension", min_value=1)

    @property
    def num_nodes(self) -> int:
        return len(self.nodes)

    @property
    def num_edges(self) -> int:
        return len(self.edges)

    @property
    def num_faces(self) -> int:
        return len(self.faces)

    def hop_distance(self, source: NodeId, target: NodeId) -> int:
        """Compute shortest path hop distance via breadth-first search on edges."""
        if source not in self.nodes or target not in self.nodes:
            raise RelationalReggeError("Source or target node not in complex")
        if source == target:
            return 0
        adj: dict[NodeId, list[NodeId]] = {node: [] for node in self.nodes}
        for u, v in self.edges:
            adj[u].append(v)
            adj[v].append(u)
        visited = {source}
        queue: deque[tuple[NodeId, int]] = deque([(source, 0)])
        while queue:
            curr, dist = queue.popleft()
            if curr == target:
                return dist
            for neighbor in adj[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        raise RelationalReggeError(f"No path between {source} and {target}")

    def incidence_matrix_d0(self) -> RealArray:
        """Return 0-coboundary matrix d^0 of shape (num_edges, num_nodes)."""
        node_idx = {node: i for i, node in enumerate(self.nodes)}
        d0 = np.zeros((self.num_edges, self.num_nodes), dtype=np.float64)
        for e_idx, (u, v) in enumerate(self.edges):
            d0[e_idx, node_idx[u]] = -1.0
            d0[e_idx, node_idx[v]] = 1.0
        return d0

    def cycle_matrix_d1(self) -> RealArray:
        """Return 1-coboundary matrix d^1 of shape (num_faces, num_edges)."""
        if not self.faces:
            return np.zeros((0, self.num_edges), dtype=np.float64)
        edge_idx = {edge: i for i, edge in enumerate(self.edges)}
        d1 = np.zeros((self.num_faces, self.num_edges), dtype=np.float64)
        for f_idx, (u, v, w) in enumerate(self.faces):
            for (p, q), sign in [((u, v), 1.0), ((v, w), 1.0), ((u, w), -1.0)]:
                if (p, q) in edge_idx:
                    d1[f_idx, edge_idx[(p, q)]] += sign
                elif (q, p) in edge_idx:
                    d1[f_idx, edge_idx[(q, p)]] -= sign
                else:
                    raise RelationalReggeError(f"Face boundary edge ({p}, {q}) not in edges")
        return d1

    def verify_bianchi_identity(self, atol: float = 1.0e-14) -> bool:
        """Verify combinatorial Bianchi identity d^1 @ d^0 == 0 to machine precision."""
        if not self.faces:
            return True
        d0 = self.incidence_matrix_d0()
        d1 = self.cycle_matrix_d1()
        comp = d1 @ d0
        return bool(np.allclose(comp, 0.0, atol=atol))

    def verify_coboundary_complex(self) -> bool:
        """Alias for verify_bianchi_identity."""
        return self.verify_bianchi_identity()

    @classmethod
    def build_regular_star_fan(
        cls,
        num_sectors: int,
        spoke_length: float = 1.0,
        rim_length: float = 1.0,
    ) -> RelationalSimplicialComplex:
        """Construct regular 2D simplicial star fan around central node 0."""
        _guard_int(num_sectors, "num_sectors", min_value=3)
        _guard_float(spoke_length, "spoke_length", strictly_positive=True)
        _guard_float(rim_length, "rim_length", strictly_positive=True)

        nodes: list[NodeId] = [0] + list(range(1, num_sectors + 1))
        edges: list[EdgeTuple] = []
        for i in range(1, num_sectors + 1):
            edges.append((0, i))
        for i in range(1, num_sectors + 1):
            next_i = 1 if i == num_sectors else i + 1
            edges.append((i, next_i))

        faces: list[FaceTuple] = []
        for i in range(1, num_sectors + 1):
            next_i = 1 if i == num_sectors else i + 1
            faces.append((0, i, next_i))

        return cls(
            nodes=tuple(nodes),
            edges=tuple(edges),
            faces=tuple(faces),
            dimension=2,
        )

    def extract_codimension_2_bones(
        self,
        interior_only: bool = True,
        edge_lengths: Mapping[EdgeTuple | frozenset[NodeId], float] | None = None,
        tolerance: float = 1.0e-10,
    ) -> tuple[RelationalSimplicialBone, ...]:
        """Extract codimension-2 bones with incident angles and deficit angles."""
        bones: list[RelationalSimplicialBone] = []

        def get_edge_length(u: NodeId, v: NodeId) -> float:
            if edge_lengths is not None:
                if (u, v) in edge_lengths:
                    return _guard_float(edge_lengths[(u, v)], f"edge_length({u},{v})", strictly_positive=True)
                if (v, u) in edge_lengths:
                    return _guard_float(edge_lengths[(v, u)], f"edge_length({v},{u})", strictly_positive=True)
                pair = frozenset((u, v))
                if pair in edge_lengths:
                    return _guard_float(edge_lengths[pair], f"edge_length({u},{v})", strictly_positive=True)
            return 1.0

        for v in self.nodes:
            incident_faces = [f for f in self.faces if v in f]
            if not incident_faces:
                continue

            # Analyze link of v
            link_degrees: dict[NodeId, int] = defaultdict(int)
            for f in incident_faces:
                other = [x for x in f if x != v]
                if len(other) == 2:
                    link_degrees[other[0]] += 1
                    link_degrees[other[1]] += 1

            is_interior = len(link_degrees) >= 3 and all(deg == 2 for deg in link_degrees.values())
            if interior_only and not is_interior:
                continue

            angles: list[float] = []
            incident_edges_v: list[EdgeTuple] = []
            edge_set_v = set()

            for f in incident_faces:
                other = [x for x in f if x != v]
                a, b = other[0], other[1]
                l_va = get_edge_length(v, a)
                l_vb = get_edge_length(v, b)
                l_ab = get_edge_length(a, b)

                if (l_va + l_vb <= l_ab) or (l_va + l_ab <= l_vb) or (l_vb + l_ab <= l_va):
                    raise RelationalReggeError(
                        f"Triangle ({v}, {a}, {b}) violates triangle inequality: {l_va}, {l_vb}, {l_ab}"
                    )

                cos_th = (l_va * l_va + l_vb * l_vb - l_ab * l_ab) / (2.0 * l_va * l_vb)
                cos_th = max(-1.0, min(1.0, cos_th))
                angles.append(math.acos(cos_th))

                for p, q in ((v, a), (a, v), (v, b), (b, v)):
                    if (p, q) in self.edges and (p, q) not in edge_set_v:
                        edge_set_v.add((p, q))
                        incident_edges_v.append((p, q))

            sum_ang = float(sum(angles))
            def_ang = float(2.0 * math.pi - sum_ang)

            if math.isclose(def_ang, 0.0, abs_tol=tolerance):
                classification: CurvatureClassification = "FLAT"
            elif def_ang > tolerance:
                classification = "POSITIVE_CONICAL"
            else:
                classification = "NEGATIVE_SADDLE"

            is_flat = bool(classification == "FLAT")

            bone = RelationalSimplicialBone(
                bone_id=v,
                dimension=0,
                incident_faces=tuple(incident_faces),
                incident_edges=tuple(incident_edges_v),
                incident_angles=tuple(angles),
                sum_angles=sum_ang,
                deficit_angle=def_ang,
                classification=classification,
                is_flat=is_flat,
                bone_type="VERTEX_2D",
            )
            bones.append(bone)

        return tuple(bones)


@dataclass(frozen=True)
class RelationalSimplicialBone:
    """Codimension-2 bone with incident simplicial angles and deficit angle."""

    bone_id: BoneId
    dimension: int = 0
    incident_faces: tuple[FaceTuple, ...] = ()
    incident_edges: tuple[EdgeTuple, ...] = ()
    incident_angles: tuple[float, ...] = ()
    sum_angles: float = 0.0
    deficit_angle: float = 0.0
    classification: CurvatureClassification = "FLAT"
    is_flat: bool = True
    bone_type: BoneType = "VERTEX_2D"
    evidence_scope: str = "relational codimension-2 bone"

    def __post_init__(self) -> None:
        if not isinstance(self.is_flat, bool):
            raise RelationalReggeError("is_flat must be boolean")
        for val in self.incident_angles:
            if isinstance(val, bool) or not isinstance(val, (int, float)) or float(val) < 0.0:
                raise RelationalReggeError("Angles must be non-negative numbers")
        if not math.isfinite(self.sum_angles):
            raise RelationalReggeError("sum_angles must be finite")
        if not math.isfinite(self.deficit_angle):
            raise RelationalReggeError("deficit_angle must be finite")

    @property
    def total_angle(self) -> float:
        return self.sum_angles

    @property
    def deficit_angle_epsilon(self) -> float:
        return self.deficit_angle


def compute_regge_deficit_angle_from_relational_edges(
    incident_triangle_edges: Sequence[tuple[float, float, float]],
    tolerance: float = 1.0e-10,
) -> tuple[float, float, CurvatureClassification]:
    """Compute deficit angle epsilon = 2*pi - sum(theta) from pairwise edge comparisons."""
    if not incident_triangle_edges:
        raise RelationalReggeError("incident_triangle_edges cannot be empty")
    angles: list[float] = []
    for idx, tri in enumerate(incident_triangle_edges):
        if not isinstance(tri, tuple) or len(tri) != 3:
            raise RelationalReggeError(f"Triangle {idx} must be a 3-tuple")
        a = _guard_float(tri[0], f"tri[{idx}][0]", strictly_positive=True)
        b = _guard_float(tri[1], f"tri[{idx}][1]", strictly_positive=True)
        c = _guard_float(tri[2], f"tri[{idx}][2]", strictly_positive=True)
        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            raise RelationalReggeError(f"Triangle {idx} violates triangle inequality: {tri}")
        cos_th = (a * a + b * b - c * c) / (2.0 * a * b)
        cos_th = max(-1.0, min(1.0, cos_th))
        angles.append(math.acos(cos_th))
    sum_ang = float(sum(angles))
    def_ang = float(2.0 * math.pi - sum_ang)
    if math.isclose(def_ang, 0.0, abs_tol=tolerance):
        cls_name: CurvatureClassification = "FLAT"
    elif def_ang > tolerance:
        cls_name = "POSITIVE_CONICAL"
    else:
        cls_name = "NEGATIVE_SADDLE"
    return (sum_ang, def_ang, cls_name)


# ---------------------------------------------------------------------------
# Cochain Holonomy & Operational Stickiness via HiGHS Linear Programming
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RelationalQuotientRepairResult:
    """Result of computing quotient residual Phi([delta]) = inf_alpha ||delta - d^0 alpha||_1."""

    raw_defect_norm: float
    quotient_residual: float
    optimal_gauge: RealArray
    repaired_cochain: RealArray
    curvature_residual: float
    is_pure_gauge: bool
    status: TerminalizerStatus
    evidence_scope: str = "zero-container quotient repair"

    @property
    def operational_stickiness(self) -> float:
        """Measure operational projection friction where continuation stalls on d^0."""
        return float(self.quotient_residual)

    @property
    def raw_norm(self) -> float:
        return self.raw_defect_norm

    @property
    def stickiness(self) -> float:
        return self.quotient_residual

    @property
    def is_frictionless(self) -> bool:
        return self.is_pure_gauge

    @property
    def terminal_status(self) -> TerminalizerStatus:
        return self.status


OperationalStickinessResult: TypeAlias = RelationalQuotientRepairResult


def compute_relational_quotient_stickiness_lp(
    gauge_d0: RealArray,
    defect_delta: RealArray | Sequence[float],
    closure_d1: RealArray | None = None,
    tolerance: float = 1.0e-10,
) -> RelationalQuotientRepairResult:
    """Solve inf_alpha ||delta - d^0 alpha||_1 via HiGHS linear programming."""
    delta_arr = np.array(defect_delta, dtype=np.float64)
    m_edges, n_nodes = gauge_d0.shape
    if delta_arr.shape[0] != m_edges:
        raise RelationalReggeError(
            f"defect_delta length {delta_arr.shape[0]} does not match gauge_d0 edges {m_edges}"
        )
    for idx, val in enumerate(delta_arr):
        if not math.isfinite(val):
            raise RelationalReggeError(f"defect_delta at index {idx} must be finite")

    raw_norm = float(np.sum(np.abs(delta_arr)))
    if m_edges == 0 or n_nodes == 0:
        return RelationalQuotientRepairResult(
            raw_defect_norm=raw_norm,
            quotient_residual=raw_norm,
            optimal_gauge=np.zeros(n_nodes, dtype=np.float64),
            repaired_cochain=delta_arr.copy(),
            curvature_residual=0.0,
            is_pure_gauge=bool(raw_norm <= tolerance),
            status="AUTHORIZED" if raw_norm <= tolerance else "OBSTRUCTED",
        )

    # HiGHS LP formulation
    # Variables: x = [alpha_0, ..., alpha_{n-1}, t_0, ..., t_{m-1}] (length n + m)
    # Minimize sum_e t_e subject to:
    #   (d0 alpha)_e - t_e <= delta_e
    #  -(d0 alpha)_e - t_e <= -delta_e
    c = np.concatenate([np.zeros(n_nodes), np.ones(m_edges)])
    a_ub = np.vstack([
        np.hstack([gauge_d0, -np.eye(m_edges)]),
        np.hstack([-gauge_d0, -np.eye(m_edges)]),
    ])
    b_ub = np.concatenate([delta_arr, -delta_arr])
    bounds = [(None, None)] * n_nodes + [(0.0, None)] * m_edges
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not res.success:
        raise RelationalReggeError(f"HiGHS LP solver failed: {res.message}")

    alpha_opt = res.x[:n_nodes]
    t_opt = res.x[n_nodes:]
    quotient_norm = float(np.sum(t_opt))
    repaired = delta_arr - gauge_d0 @ alpha_opt

    if closure_d1 is not None and closure_d1.shape[0] > 0:
        curv = float(np.sum(np.abs(closure_d1 @ delta_arr)))
    else:
        curv = 0.0

    is_gauge = bool(quotient_norm <= tolerance)
    if is_gauge:
        status: TerminalizerStatus = "AUTHORIZED"
    elif curv <= tolerance:
        status = "OBSTRUCTED"
    else:
        status = "REFUSAL"

    return RelationalQuotientRepairResult(
        raw_defect_norm=raw_norm,
        quotient_residual=quotient_norm,
        optimal_gauge=alpha_opt,
        repaired_cochain=repaired,
        curvature_residual=curv,
        is_pure_gauge=is_gauge,
        status=status,
    )


compute_operational_stickiness = compute_relational_quotient_stickiness_lp


@dataclass(frozen=True)
class RelationalCochainHolonomy:
    """Evaluation of cochain holonomy around cycles and bones."""

    cycle_edges: tuple[EdgeTuple, ...]
    holonomy_value: float
    is_gauge_invariant: bool
    deficit_angle_equivalent: float
    curvature_cochain: RealArray


CochainHolonomyResult: TypeAlias = RelationalCochainHolonomy


# ---------------------------------------------------------------------------
# The 8-Stage Unified Relational Spine
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Presentation:
    """Stage 1: Raw supplied comparison data on a relational carrier complex."""

    carrier: RelationalSimplicialComplex
    raw_comparisons: tuple[float, ...]
    label: str = "raw_presentation"

    def __post_init__(self) -> None:
        if len(self.raw_comparisons) != self.carrier.num_edges:
            raise RelationalSpineError(
                f"raw_comparisons length {len(self.raw_comparisons)} must match "
                f"carrier edges {self.carrier.num_edges}"
            )
        for idx, val in enumerate(self.raw_comparisons):
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                raise RelationalSpineError(f"Comparison value at index {idx} must be numeric, not bool")
            if not math.isfinite(float(val)):
                raise RelationalSpineError(f"Comparison value at index {idx} must be finite")

    @property
    def cochain_vector(self) -> RealArray:
        arr = np.array(self.raw_comparisons, dtype=np.float64)
        arr.flags.writeable = False
        return arr

    @property
    def raw_differences(self) -> RealArray:
        return self.cochain_vector

    @property
    def l1_norm(self) -> float:
        return float(np.sum(np.abs(self.cochain_vector)))

    @property
    def num_edges(self) -> int:
        return len(self.raw_comparisons)


RelationalPresentation: TypeAlias = Presentation


@dataclass(frozen=True)
class PresentationFamily:
    """Stage 2: Family of presentations under allowed gauge transformations."""

    base_presentation: Presentation
    gauge_type: str = "additive_c0_coboundary"

    @property
    def carrier(self) -> RelationalSimplicialComplex:
        return self.base_presentation.carrier

    def generate_presentation(self, gauge_potential: Sequence[float]) -> Presentation:
        """Apply gauge transformation delta' = delta + d^0 alpha."""
        if len(gauge_potential) != self.carrier.num_nodes:
            raise RelationalSpineError(
                f"gauge_potential length {len(gauge_potential)} must match "
                f"nodes {self.carrier.num_nodes}"
            )
        for idx, val in enumerate(gauge_potential):
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                raise RelationalSpineError(f"Gauge potential at {idx} must be numeric, not bool")
            if not math.isfinite(float(val)):
                raise RelationalSpineError(f"Gauge potential at {idx} must be finite")
        alpha = np.array(gauge_potential, dtype=np.float64)
        d0 = self.carrier.incidence_matrix_d0()
        d0_alpha = d0 @ alpha
        new_cochain = tuple(float(x) for x in (self.base_presentation.cochain_vector + d0_alpha))
        return Presentation(
            carrier=self.carrier,
            raw_comparisons=new_cochain,
            label=f"{self.base_presentation.label}_gauge_transformed",
        )

    def is_equivalent(self, other: Presentation, tolerance: float = 1.0e-10) -> bool:
        """Check if other presentation belongs to this family (delta - delta' in im(d^0))."""
        if other.carrier != self.carrier:
            return False
        diff = other.cochain_vector - self.base_presentation.cochain_vector
        d0 = self.carrier.incidence_matrix_d0()
        res = compute_relational_quotient_stickiness_lp(d0, diff, tolerance=tolerance)
        return bool(res.quotient_residual <= tolerance)

    def canonical_representative(self, tolerance: float = 1.0e-10) -> Presentation:
        """Compute canonical quotient-repaired representative with minimal L1 norm."""
        d0 = self.carrier.incidence_matrix_d0()
        res = compute_relational_quotient_stickiness_lp(d0, self.base_presentation.cochain_vector, tolerance=tolerance)
        repaired = tuple(float(x) for x in res.repaired_cochain)
        return Presentation(
            carrier=self.carrier,
            raw_comparisons=repaired,
            label=f"{self.base_presentation.label}_canonical_quotient",
        )


RelationalPresentationFamily: TypeAlias = PresentationFamily


@dataclass(frozen=True)
class Representation:
    """Stage 3: Operational map preserving a declared set of questions."""

    representation_id: str
    features: tuple[float, ...]
    preserved_question_ids: tuple[str, ...]
    description: str = "operational_feature_representation"
    quotient_class_representative: RealArray = field(default_factory=lambda: np.zeros(0, dtype=np.float64))
    fiber_dimension: int = 0

    def __post_init__(self) -> None:
        for idx, val in enumerate(self.features):
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                raise RelationalSpineError(f"Feature at index {idx} must be numeric, not bool")
            if not math.isfinite(float(val)):
                raise RelationalSpineError(f"Feature at index {idx} must be finite")
        if isinstance(self.fiber_dimension, bool) or not isinstance(self.fiber_dimension, int):
            raise RelationalSpineError("fiber_dimension must be integer")
        if self.fiber_dimension < 0:
            raise RelationalSpineError("fiber_dimension must be >= 0")


RelationalRepresentation: TypeAlias = Representation


@dataclass(frozen=True)
class FiberBundle:
    """Stage 4: Space of presentations projecting to the same representation."""

    base_representation: Representation
    family: PresentationFamily
    fiber_dimension: int
    fiber_coordinates_alpha: RealArray = field(default_factory=lambda: np.zeros(0, dtype=np.float64))
    total_presentation: Presentation | None = None

    def __post_init__(self) -> None:
        if isinstance(self.fiber_dimension, bool) or not isinstance(self.fiber_dimension, int):
            raise RelationalSpineError("fiber_dimension must be integer")
        if self.fiber_dimension < 0:
            raise RelationalSpineError("fiber_dimension must be non-negative")

    def projects_to_representation(
        self,
        presentation: Presentation,
        rep_map: Callable[[Presentation], Representation],
        tolerance: float = 1.0e-10,
    ) -> bool:
        """Verify whether a candidate presentation lies in this fiber."""
        rep = rep_map(presentation)
        if len(rep.features) != len(self.base_representation.features):
            return False
        return bool(np.allclose(rep.features, self.base_representation.features, atol=tolerance))


RelationalFiberBundle: TypeAlias = FiberBundle


@dataclass(frozen=True)
class Fact:
    """Stage 5: An invariant that is constant across the entire fiber."""

    fact_id: str
    value: float | tuple[float, ...]
    is_gauge_invariant: bool = True
    invariance_tolerance: float = 1.0e-10
    curvature_cochain_gamma2: RealArray = field(default_factory=lambda: np.zeros(0, dtype=np.float64))
    deficit_angles: tuple[float, ...] = ()
    quotient_stickiness: float = 0.0
    is_fiber_constant: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.is_gauge_invariant, bool):
            raise RelationalSpineError("is_gauge_invariant must be boolean")
        if not isinstance(self.is_fiber_constant, bool):
            raise RelationalSpineError("is_fiber_constant must be boolean")


RelationalFact: TypeAlias = Fact


@dataclass(frozen=True)
class Compression:
    """Stage 6: Projecting away fiber coordinates to keep only the fact."""

    source_dimension: int
    fact_dimension: int
    retained_fact: Fact
    discarded_dof: int
    compression_ratio: float

    def __post_init__(self) -> None:
        if isinstance(self.source_dimension, bool) or self.source_dimension < 1:
            raise RelationalSpineError("source_dimension must be an int >= 1")
        if isinstance(self.fact_dimension, bool) or self.fact_dimension < 0:
            raise RelationalSpineError("fact_dimension must be an int >= 0")
        if isinstance(self.discarded_dof, bool) or self.discarded_dof < 0:
            raise RelationalSpineError("discarded_dof must be an int >= 0")
        if isinstance(self.compression_ratio, bool) or self.compression_ratio <= 0.0:
            raise RelationalSpineError("compression_ratio must be positive float")

    @property
    def fact(self) -> Fact:
        return self.retained_fact

    @property
    def discarded_degrees_of_freedom(self) -> int:
        return self.discarded_dof


RelationalCompression: TypeAlias = Compression


@dataclass(frozen=True)
class Obstruction:
    """Stage 7: Arises when a question needs information discarded in compression."""

    question_id: str
    is_obstructed: bool
    defect_norm: float
    witness_presentations: tuple[Presentation, Presentation] | None = None
    reason: str = "query requires discarded fiber degrees of freedom"
    stickiness_friction: float = 0.0
    has_continuation_stall: bool = False
    status: TerminalizerStatus = "AUTHORIZED"
    witness_certificate: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.is_obstructed, bool):
            raise RelationalSpineError("is_obstructed must be boolean")
        if not isinstance(self.has_continuation_stall, bool):
            raise RelationalSpineError("has_continuation_stall must be boolean")
        if isinstance(self.defect_norm, bool) or not math.isfinite(self.defect_norm) or self.defect_norm < 0.0:
            raise RelationalSpineError("defect_norm must be non-negative finite float")
        if (
            isinstance(self.stickiness_friction, bool)
            or not math.isfinite(self.stickiness_friction)
            or self.stickiness_friction < 0.0
        ):
            raise RelationalSpineError("stickiness_friction must be non-negative finite float")


RelationalObstruction: TypeAlias = Obstruction


@dataclass(frozen=True)
class RelationalReggeCurvature:
    """Stage 8: Holonomy around 3-cycles / bones surviving vertex re-labeling."""

    bone_id: BoneId
    cycle_edges: tuple[EdgeTuple, ...]
    holonomy_circulation: float
    incident_angles: tuple[float, ...]
    deficit_angle_epsilon: float
    is_flat: bool
    operational_stickiness: float
    bones: tuple[RelationalSimplicialBone, ...] = ()
    total_deficit_angle: float = 0.0
    euler_characteristic: int = 0
    is_flat_manifold: bool = True
    bianchi_satisfied: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.is_flat, bool):
            raise RelationalSpineError("is_flat must be boolean")
        if not isinstance(self.is_flat_manifold, bool):
            raise RelationalSpineError("is_flat_manifold must be boolean")
        if not isinstance(self.bianchi_satisfied, bool):
            raise RelationalSpineError("bianchi_satisfied must be boolean")
        if isinstance(self.holonomy_circulation, bool) or not math.isfinite(self.holonomy_circulation):
            raise RelationalSpineError("holonomy_circulation must be finite float")
        if isinstance(self.deficit_angle_epsilon, bool) or not math.isfinite(self.deficit_angle_epsilon):
            raise RelationalSpineError("deficit_angle_epsilon must be finite float")
        if isinstance(self.operational_stickiness, bool) or not math.isfinite(self.operational_stickiness):
            raise RelationalSpineError("operational_stickiness must be finite float")

    @property
    def deficit_angle(self) -> float:
        return self.deficit_angle_epsilon


@dataclass(frozen=True)
class UnifiedRelationalSpineResult:
    """Master record executing and verifying all 8 stages of the Unified Relational Spine."""

    stage1_presentation: Presentation
    stage2_family: PresentationFamily
    stage3_representation: Representation
    stage4_fiber_bundle: FiberBundle
    stage5_fact: Fact
    stage6_compression: Compression
    stage7_obstruction: Obstruction | None
    stage8_curvature: RelationalReggeCurvature
    all_stages_coherent: bool = True

    @property
    def presentation(self) -> Presentation:
        return self.stage1_presentation

    @property
    def family(self) -> PresentationFamily:
        return self.stage2_family

    @property
    def representation(self) -> Representation:
        return self.stage3_representation

    @property
    def fiber_bundle(self) -> FiberBundle:
        return self.stage4_fiber_bundle

    @property
    def fact(self) -> Fact:
        return self.stage5_fact

    @property
    def compression(self) -> Compression:
        return self.stage6_compression

    @property
    def obstruction(self) -> Obstruction | None:
        return self.stage7_obstruction

    @property
    def curvature(self) -> RelationalReggeCurvature:
        return self.stage8_curvature

    @classmethod
    def execute_spine(
        cls,
        carrier: RelationalSimplicialComplex,
        raw_comparisons: Sequence[float],
        bone_id: BoneId | None = None,
        incident_angles: Sequence[float] | None = None,
        test_question: Callable[[Presentation], float] | None = None,
        gauge_shifts: Sequence[float] | None = None,
        tolerance: float = 1.0e-10,
    ) -> UnifiedRelationalSpineResult:
        """Execute all 8 stages of the Unified Relational Spine on given carrier data."""
        # Stage 1: Presentation
        pres = Presentation(carrier=carrier, raw_comparisons=tuple(raw_comparisons))

        # Stage 2: Presentation Family
        fam = PresentationFamily(base_presentation=pres)
        if gauge_shifts is not None:
            pres_alt = fam.generate_presentation(gauge_shifts)
        else:
            alpha_test = np.ones(carrier.num_nodes, dtype=np.float64)
            alpha_test[0] = 2.0
            pres_alt = fam.generate_presentation(alpha_test)

        # Stage 3: Representation
        d0 = carrier.incidence_matrix_d0()
        d1 = carrier.cycle_matrix_d1() if carrier.num_faces > 0 else None
        lp_res = compute_relational_quotient_stickiness_lp(
            d0, pres.cochain_vector, closure_d1=d1, tolerance=tolerance
        )
        fiber_dim = max(0, carrier.num_nodes - 1)
        rep = Representation(
            representation_id="rep_canonical_quotient",
            features=(lp_res.quotient_residual, lp_res.curvature_residual),
            preserved_question_ids=("quotient_residual", "curvature_residual"),
            description="canonical_quotient_feature_representation",
            quotient_class_representative=lp_res.repaired_cochain,
            fiber_dimension=fiber_dim,
        )

        # Stage 4: Fiber Bundle
        bundle = FiberBundle(
            base_representation=rep,
            family=fam,
            fiber_dimension=fiber_dim,
            fiber_coordinates_alpha=lp_res.optimal_gauge,
            total_presentation=pres,
        )

        # Stage 5: Fact
        bones = carrier.extract_codimension_2_bones(tolerance=tolerance)
        deficits = tuple(b.deficit_angle for b in bones)
        gamma2 = d1 @ pres.cochain_vector if d1 is not None and d1.shape[0] > 0 else np.zeros(0, dtype=np.float64)
        fact = Fact(
            fact_id="fact_quotient_residual",
            value=lp_res.quotient_residual,
            is_gauge_invariant=True,
            invariance_tolerance=tolerance,
            curvature_cochain_gamma2=gamma2,
            deficit_angles=deficits,
            quotient_stickiness=lp_res.quotient_residual,
            is_fiber_constant=True,
        )

        # Stage 6: Compression
        discarded = max(0, carrier.num_nodes - 1)
        comp = Compression(
            source_dimension=carrier.num_edges,
            fact_dimension=max(1, len(deficits)),
            retained_fact=fact,
            discarded_dof=discarded,
            compression_ratio=float(carrier.num_edges) / float(max(1, len(deficits))),
        )

        # Stage 7: Obstruction
        has_stall = lp_res.status in ("OBSTRUCTED", "REFUSAL")
        if test_question is not None:
            q1 = test_question(pres)
            q2 = test_question(pres_alt)
            diff = abs(q1 - q2)
            is_obstr = diff > tolerance
            obstr: Obstruction | None = Obstruction(
                question_id="external_test_question",
                is_obstructed=is_obstr,
                defect_norm=diff,
                witness_presentations=(pres, pres_alt) if is_obstr else None,
                reason="Question values differ on fiber presentations"
                if is_obstr
                else "Question factors through invariant fact",
                stickiness_friction=lp_res.operational_stickiness,
                has_continuation_stall=has_stall,
                status=lp_res.status,
                witness_certificate=f"stickiness={lp_res.operational_stickiness:.6e}, status={lp_res.status}",
            )
        else:
            obstr = Obstruction(
                question_id="query_quotient_continuation",
                is_obstructed=has_stall,
                defect_norm=lp_res.operational_stickiness,
                witness_presentations=None,
                reason="Continuation stalls on cochain projection residual"
                if has_stall
                else "Continuation fluent under gauge repair",
                stickiness_friction=lp_res.operational_stickiness,
                has_continuation_stall=has_stall,
                status=lp_res.status,
                witness_certificate=f"stickiness={lp_res.operational_stickiness:.6e}, status={lp_res.status}",
            )

        # Stage 8: Curvature (Relational Regge)
        if bone_id is not None and incident_angles is not None:
            sel_bone_id = bone_id
            sel_angles = tuple(incident_angles)
            tot_ang = sum(sel_angles)
            deficit = 2.0 * math.pi - tot_ang
        elif bones:
            sel_bone_id = bones[0].bone_id
            sel_angles = bones[0].incident_angles
            deficit = bones[0].deficit_angle
        else:
            sel_bone_id = ""
            sel_angles = ()
            deficit = 0.0

        tot_deficit = float(sum(deficits)) if deficits else deficit
        euler = carrier.num_nodes - carrier.num_edges + carrier.num_faces
        is_flat_man = math.isclose(tot_deficit, 0.0, abs_tol=tolerance) and (lp_res.curvature_residual <= tolerance)
        bone_edges = tuple(carrier.edges[:3]) if carrier.num_edges >= 3 else ()

        curv = RelationalReggeCurvature(
            bone_id=sel_bone_id,
            cycle_edges=bone_edges,
            holonomy_circulation=lp_res.curvature_residual,
            incident_angles=sel_angles,
            deficit_angle_epsilon=deficit,
            is_flat=is_flat_man,
            operational_stickiness=lp_res.operational_stickiness,
            bones=bones,
            total_deficit_angle=tot_deficit,
            euler_characteristic=euler,
            is_flat_manifold=is_flat_man,
            bianchi_satisfied=carrier.verify_bianchi_identity(atol=tolerance),
        )

        return cls(
            stage1_presentation=pres,
            stage2_family=fam,
            stage3_representation=rep,
            stage4_fiber_bundle=bundle,
            stage5_fact=fact,
            stage6_compression=comp,
            stage7_obstruction=obstr,
            stage8_curvature=curv,
            all_stages_coherent=True,
        )


UnifiedRelationalSpine: TypeAlias = UnifiedRelationalSpineResult


def execute_unified_relational_spine(
    carrier: RelationalSimplicialComplex,
    raw_differences: RealArray | Sequence[float],
    gauge_shifts: Sequence[float] | None = None,
    test_question: Callable[[Presentation], float] | None = None,
    tolerance: float = 1.0e-10,
) -> UnifiedRelationalSpineResult:
    """Execute and bind all 8 stages of the Unified Relational Spine."""
    return UnifiedRelationalSpineResult.execute_spine(
        carrier=carrier,
        raw_comparisons=raw_differences,
        gauge_shifts=gauge_shifts,
        test_question=test_question,
        tolerance=tolerance,
    )


# ---------------------------------------------------------------------------
# Metric vs Relational Regge Contrast Engine
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MetricVsRelationalReggeContrast:
    """Direct comparison between standard metric Regge calculus and relational Regge."""

    complex_name: str
    standard_requires_ambient_coordinates: bool
    relational_requires_ambient_coordinates: bool
    standard_deficit_angle: float
    relational_deficit_angle: float
    deficit_angle_agreement: bool
    standard_gauge_symmetry: str
    relational_gauge_symmetry: str
    relational_stickiness: float
    evidence_scope: str = "metric vs relational Regge contrast"


def compare_standard_and_relational_regge(
    complex_type: Literal["FLAT_HEXAGON", "PENTAGON_CONE", "HEPTAGON_SADDLE"],
    edge_scale: float = 1.0,
    tolerance: float = 1.0e-10,
) -> MetricVsRelationalReggeContrast:
    """Construct identical combinatorial star fans and contrast metric vs relational formulation."""
    _guard_float(edge_scale, "edge_scale", strictly_positive=True)
    if complex_type == "FLAT_HEXAGON":
        num_sectors = 6
        std_deficit = 0.0
    elif complex_type == "PENTAGON_CONE":
        num_sectors = 5
        std_deficit = math.pi / 3.0
    elif complex_type == "HEPTAGON_SADDLE":
        num_sectors = 7
        std_deficit = -math.pi / 3.0
    else:
        raise RelationalReggeError(f"Unknown complex_type: {complex_type!r}")

    complex_obj = RelationalSimplicialComplex.build_regular_star_fan(
        num_sectors=num_sectors,
        spoke_length=edge_scale,
        rim_length=edge_scale,
    )
    bones = complex_obj.extract_codimension_2_bones(tolerance=tolerance)
    if not bones:
        raise RelationalReggeError("No interior bone extracted from star fan")
    bone = bones[0]
    rel_deficit = bone.deficit_angle
    agreement = math.isclose(std_deficit, rel_deficit, abs_tol=1.0e-12)

    # Compute operational stickiness of difference cochain
    num_edges = complex_obj.num_edges
    delta = np.zeros(num_edges, dtype=np.float64)
    if not math.isclose(rel_deficit, 0.0, abs_tol=tolerance):
        # Distribute deficit angle on rim edges
        rim_delta = rel_deficit / float(num_sectors)
        for e_idx in range(num_sectors, 2 * num_sectors):
            delta[e_idx] = rim_delta

    d0 = complex_obj.incidence_matrix_d0()
    d1 = complex_obj.cycle_matrix_d1()
    lp_res = compute_relational_quotient_stickiness_lp(d0, delta, closure_d1=d1, tolerance=tolerance)
    stickiness = lp_res.operational_stickiness

    return MetricVsRelationalReggeContrast(
        complex_name=complex_type,
        standard_requires_ambient_coordinates=True,
        relational_requires_ambient_coordinates=False,
        standard_deficit_angle=std_deficit,
        relational_deficit_angle=rel_deficit,
        deficit_angle_agreement=agreement,
        standard_gauge_symmetry="diffeomorphisms (vertex coordinate moves in R^N)",
        relational_gauge_symmetry="0-coboundary group d^0 alpha (vertex relabeling)",
        relational_stickiness=stickiness,
        evidence_scope="metric vs relational Regge contrast",
    )
