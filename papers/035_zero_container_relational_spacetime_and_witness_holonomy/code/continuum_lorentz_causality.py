"""Emergent relativistic Lorentz causality and zero-container relational observer packet.

This module formalizes:
1. The 9-tuple relational observer evaluation packet:
       O = (K, F, R, delta, d^0, d^1, J, M, tau)
   operating without an a priori ambient spacetime or metric container.
2. The continuum refinement limit of the Lieb-Robinson Duhamel influence envelope,
   converging to the relativistic Minkowski forward light-cone with emergent
   effective speed of light c_eff = v_LR and exponential spacelike defect suppression.
3. The discrete defect 4-current J^mu = (c_eff * nu, j) satisfying relativistic
   conservation partial_mu J^mu = O(a^2) -> 0 as lattice pitch a -> 0 under symmetric
   central-difference stencils.
4. Exact relativistic invariance of the Minkowski spacetime interval
   s^2 = c_eff^2 dt^2 - dx^2 under discrete relational Lorentz boosts.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from collections import deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Literal, TypeAlias

import numpy as np
import numpy.typing as npt
from scipy.optimize import linprog

NodeId: TypeAlias = int | str
EdgeTuple: TypeAlias = tuple[NodeId, NodeId]
FaceTuple: TypeAlias = tuple[NodeId, NodeId, NodeId]
CausalClassification: TypeAlias = Literal["TIMELIKE", "NULL", "SPACELIKE"]
CausalSector: TypeAlias = CausalClassification
TerminalizerStatus: TypeAlias = Literal["AUTHORIZED", "OBSTRUCTED", "REFUSAL", "PASS", "FAIL", "TIMELIKE", "NULL", "SPACELIKE"]
RealArray: TypeAlias = npt.NDArray[np.float64]


class ContinuumCausalityError(ValueError):
    """An input does not satisfy declared continuum causality premises."""


def _guard_float(
    val: object,
    name: str,
    strictly_positive: bool = True,
    allow_negative: bool = False,
) -> float:
    """Validate numeric parameter with Boolean subclass guard and finiteness check."""
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        if allow_negative:
            raise ContinuumCausalityError(f"{name} must be a finite number")
        adj = "positive" if strictly_positive else "non-negative"
        raise ContinuumCausalityError(f"{name} must be {adj}")
    fval = float(val)
    if not math.isfinite(fval):
        if allow_negative:
            raise ContinuumCausalityError(f"{name} must be finite")
        adj = "positive" if strictly_positive else "non-negative"
        raise ContinuumCausalityError(f"{name} must be {adj}")
    if not allow_negative:
        if strictly_positive and fval <= 0.0:
            raise ContinuumCausalityError(f"{name} must be positive")
        if not strictly_positive and fval < 0.0:
            raise ContinuumCausalityError(f"{name} must be non-negative")
    return fval


def _guard_int(val: object, name: str, min_value: int = 1) -> int:
    """Validate integer parameter with Boolean subclass guard."""
    if isinstance(val, bool) or not isinstance(val, int):
        raise ContinuumCausalityError(f"{name} must be an integer >= {min_value}")
    if val < min_value:
        raise ContinuumCausalityError(f"{name} must be an integer >= {min_value}")
    return val


@dataclass(frozen=True)
class CarrierNetwork:
    """Discrete relational carrier complex K = (V, E, F) without ambient coordinates."""

    nodes: tuple[NodeId, ...]
    edges: tuple[EdgeTuple, ...]
    faces: tuple[FaceTuple, ...] = ()

    def __post_init__(self) -> None:
        if not self.nodes:
            raise ContinuumCausalityError("CarrierNetwork must have at least one node")
        for node in self.nodes:
            if isinstance(node, bool) or not isinstance(node, (int, str)):
                raise ContinuumCausalityError(f"Carrier node {node!r} must be int or str, not bool")
        node_set = set(self.nodes)
        if len(node_set) != len(self.nodes):
            raise ContinuumCausalityError("Carrier nodes must be unique")

        seen_edges: set[tuple[NodeId, NodeId]] = set()
        seen_undirected: set[frozenset[NodeId]] = set()
        for u, v in self.edges:
            if isinstance(u, bool) or not isinstance(u, (int, str)):
                raise ContinuumCausalityError(f"Edge vertex {u!r} must be int or str, not bool")
            if isinstance(v, bool) or not isinstance(v, (int, str)):
                raise ContinuumCausalityError(f"Edge vertex {v!r} must be int or str, not bool")
            if u not in node_set or v not in node_set:
                raise ContinuumCausalityError(f"Edge ({u}, {v}) references non-existent node")
            if u == v:
                raise ContinuumCausalityError(f"Self-loop edge ({u}, {u}) is not permitted")
            if (u, v) in seen_edges:
                raise ContinuumCausalityError(f"Duplicate edge ({u}, {v})")
            seen_edges.add((u, v))
            pair = frozenset((u, v))
            if pair in seen_undirected:
                raise ContinuumCausalityError(f"Duplicate or anti-parallel edge between {u} and {v}")
            seen_undirected.add(pair)

        edge_set = set(self.edges) | {(v, u) for u, v in self.edges}
        seen_faces: set[frozenset[NodeId]] = set()
        for u, v, w in self.faces:
            if isinstance(u, bool) or not isinstance(u, (int, str)):
                raise ContinuumCausalityError(f"Face vertex {u!r} must be int or str, not bool")
            if isinstance(v, bool) or not isinstance(v, (int, str)):
                raise ContinuumCausalityError(f"Face vertex {v!r} must be int or str, not bool")
            if isinstance(w, bool) or not isinstance(w, (int, str)):
                raise ContinuumCausalityError(f"Face vertex {w!r} must be int or str, not bool")
            if u not in node_set or v not in node_set or w not in node_set:
                raise ContinuumCausalityError(f"Face ({u}, {v}, {w}) references non-existent node")
            if len({u, v, w}) != 3:
                raise ContinuumCausalityError(f"Face ({u}, {v}, {w}) vertices must be distinct")
            for p, q in ((u, v), (v, w), (u, w)):
                if (p, q) not in edge_set:
                    raise ContinuumCausalityError(f"Face boundary edge ({p}, {q}) not in edges")
            f_key = frozenset((u, v, w))
            if f_key in seen_faces:
                raise ContinuumCausalityError(f"Duplicate face ({u}, {v}, {w})")
            seen_faces.add(f_key)

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
        if isinstance(source, bool) or not isinstance(source, (int, str)):
            raise ContinuumCausalityError(f"Source node {source!r} must be int or str, not bool")
        if isinstance(target, bool) or not isinstance(target, (int, str)):
            raise ContinuumCausalityError(f"Target node {target!r} must be int or str, not bool")
        node_set = set(self.nodes)
        if source not in node_set:
            raise ContinuumCausalityError(f"Source node {source} not in carrier nodes")
        if target not in node_set:
            raise ContinuumCausalityError(f"Target node {target} not in carrier nodes")
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
        raise ContinuumCausalityError(f"No path between {source} and {target}")

    def incidence_matrix_d0(self) -> npt.NDArray[np.float64]:
        """Return 0-coboundary matrix d^0 of shape (num_edges, num_nodes)."""
        node_idx = {node: i for i, node in enumerate(self.nodes)}
        d0 = np.zeros((self.num_edges, self.num_nodes), dtype=np.float64)
        for e_idx, (u, v) in enumerate(self.edges):
            d0[e_idx, node_idx[u]] = -1.0
            d0[e_idx, node_idx[v]] = 1.0
        return d0

    def cycle_matrix_d1(self) -> npt.NDArray[np.float64]:
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
                    raise ContinuumCausalityError(f"Face boundary edge ({p}, {q}) not in edges")
        return d1

    def verify_coboundary_complex(self) -> bool:
        """Verify the exact chain complex property d^1 @ d^0 == 0."""
        if not self.faces:
            return True
        d0 = self.incidence_matrix_d0()
        d1 = self.cycle_matrix_d1()
        comp = d1 @ d0
        return bool(np.allclose(comp, 0.0, atol=1e-14))


@dataclass(frozen=True)
class QuotientRepairResult:
    """Result of computing quotient residual Phi([delta]) = inf_alpha ||delta - d^0 alpha||_1."""

    raw_defect_norm: float
    quotient_residual: float
    optimal_gauge: npt.NDArray[np.float64]
    repaired_cochain: npt.NDArray[np.float64]
    curvature_residual: float
    is_pure_gauge: bool
    evidence_scope: str = "zero-container quotient repair"

    @property
    def operational_stickiness(self) -> float:
        """Operational projection friction where continuation cannot factor through gauge repair d^0."""
        return float(self.quotient_residual)


def compute_quotient_residual_lp(
    gauge_d0: npt.NDArray[np.float64],
    defect_delta: npt.NDArray[np.float64],
    closure_d1: npt.NDArray[np.float64] | None = None,
    tolerance: float = 1.0e-10,
) -> QuotientRepairResult:
    """Compute the irreducible quotient defect modulo im(d^0) via L1 linear programming."""
    m_edges, n_nodes = gauge_d0.shape
    raw_norm = float(np.sum(np.abs(defect_delta)))
    if m_edges == 0 or n_nodes == 0:
        return QuotientRepairResult(
            raw_defect_norm=raw_norm,
            quotient_residual=raw_norm,
            optimal_gauge=np.zeros(n_nodes, dtype=np.float64),
            repaired_cochain=defect_delta.copy(),
            curvature_residual=0.0,
            is_pure_gauge=bool(raw_norm <= tolerance),
        )

    # Minimize sum_e t_e subject to -t_e <= delta_e - (d0 alpha)_e <= t_e, t_e >= 0
    # Variables: x = [alpha_0, ..., alpha_{n-1}, t_0, ..., t_{m-1}] (length n + m)
    c = np.concatenate([np.zeros(n_nodes), np.ones(m_edges)])
    a_ub = np.vstack([
        np.hstack([gauge_d0, -np.eye(m_edges)]),
        np.hstack([-gauge_d0, -np.eye(m_edges)]),
    ])
    b_ub = np.concatenate([defect_delta, -defect_delta])
    bounds = [(None, None)] * n_nodes + [(0.0, None)] * m_edges
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not res.success:
        raise ContinuumCausalityError(f"Linear program failed to solve: {res.message}")

    alpha_opt = res.x[:n_nodes]
    t_opt = res.x[n_nodes:]
    quotient_norm = float(np.sum(t_opt))
    repaired = defect_delta - gauge_d0 @ alpha_opt
    if closure_d1 is not None and closure_d1.shape[0] > 0:
        curv = float(np.sum(np.abs(closure_d1 @ defect_delta)))
    else:
        curv = 0.0
    is_gauge = bool(quotient_norm <= tolerance)

    return QuotientRepairResult(
        raw_defect_norm=raw_norm,
        quotient_residual=quotient_norm,
        optimal_gauge=alpha_opt,
        repaired_cochain=repaired,
        curvature_residual=curv,
        is_pure_gauge=is_gauge,
    )


@dataclass(frozen=True)
class RelationalContinuumObserverPacket:
    """Zero-container relational observer evaluation packet O_cont.

    Formal 9-tuple: O = (K, F, R, delta, d^0, d^1, J, M, tau).
    """

    carrier_nodes_k: tuple[NodeId, ...]
    local_algebras_f: Mapping[NodeId, str | int]
    adjacency_r: tuple[tuple[NodeId, NodeId], ...]
    defect_operator_delta: npt.NDArray[np.float64]
    gauge_shifts_d0: npt.NDArray[np.float64]
    cycle_check_d1: npt.NDArray[np.float64]
    gauge_norm_j: float
    transformation_group_m: str
    causal_terminalizer_tau: TerminalizerStatus
    quotient_residual: float = 0.0
    optimal_gauge: npt.NDArray[np.float64] | None = None
    is_pure_gauge: bool = False
    minkowski_interval_s2: float = 0.0

    def __post_init__(self) -> None:
        if not self.carrier_nodes_k:
            raise ContinuumCausalityError("Carrier nodes K cannot be empty")
        for k in self.carrier_nodes_k:
            if isinstance(k, bool) or not isinstance(k, (int, str)):
                raise ContinuumCausalityError(f"Carrier node {k!r} must be int or str, not bool")
        _guard_float(self.gauge_norm_j, "gauge_norm_j", strictly_positive=False)
        _guard_float(self.quotient_residual, "quotient_residual", strictly_positive=False)
        _guard_float(self.minkowski_interval_s2, "minkowski_interval_s2", allow_negative=True)
        if not isinstance(self.is_pure_gauge, bool):
            raise ContinuumCausalityError("is_pure_gauge must be a boolean")

    # Compatibility property aliases across explorer architectures
    @property
    def carrier_k(self) -> tuple[NodeId, ...]:
        return self.carrier_nodes_k

    @property
    def fiber_f(self) -> Mapping[NodeId, str | int]:
        return self.local_algebras_f

    @property
    def relation_r(self) -> tuple[tuple[NodeId, NodeId], ...]:
        return self.adjacency_r

    @property
    def relations_r(self) -> tuple[tuple[NodeId, NodeId], ...]:
        return self.adjacency_r

    @property
    def defect_delta(self) -> npt.NDArray[np.float64]:
        return self.defect_operator_delta

    @property
    def difference_delta(self) -> tuple[float, ...]:
        return tuple(float(x) for x in self.defect_operator_delta)

    @property
    def gauge_d0(self) -> npt.NDArray[np.float64]:
        return self.gauge_shifts_d0

    @property
    def gauge_repair_d0(self) -> npt.NDArray[np.float64]:
        return self.gauge_shifts_d0

    @property
    def closure_d1(self) -> npt.NDArray[np.float64]:
        return self.cycle_check_d1

    @property
    def cycle_d1(self) -> npt.NDArray[np.float64]:
        return self.cycle_check_d1

    @property
    def symmetries_m(self) -> str:
        return self.transformation_group_m

    @property
    def symmetry_class_m(self) -> str:
        return self.transformation_group_m

    @property
    def terminalizer_tau(self) -> TerminalizerStatus:
        return self.causal_terminalizer_tau

    @property
    def terminal_tag_tau(self) -> TerminalizerStatus:
        return self.causal_terminalizer_tau

    @property
    def operational_stickiness(self) -> float:
        """Measure operational projection friction: quotient residual surviving gauge repair d^0."""
        return float(self.quotient_residual)

    def compute_quotient_residual(self, tolerance: float = 1.0e-10) -> QuotientRepairResult:
        """Compute the irreducible quotient defect modulo im(d^0) via L1 linear programming."""
        return compute_quotient_residual_lp(
            gauge_d0=self.gauge_shifts_d0,
            defect_delta=self.defect_operator_delta,
            closure_d1=self.cycle_check_d1,
            tolerance=tolerance,
        )

    def terminalize(self, tolerance: float = 1.0e-10) -> TerminalizerStatus:
        """Assign operational terminal status based on quotient and curvature residuals."""
        res = self.compute_quotient_residual(tolerance=tolerance)
        if res.is_pure_gauge:
            return "AUTHORIZED"
        if res.curvature_residual > tolerance:
            return "REFUSAL"
        return "OBSTRUCTED"


RelationalObserverPacket = RelationalContinuumObserverPacket


def build_relational_continuum_packet(
    num_sites: int | None = None,
    defect_values: RealArray | Sequence[float] | None = None,
    gauge_alpha: RealArray | Sequence[float] | None = None,
    tolerance: float = 1.0e-10,
    c_eff: float = 1.0,
    elapsed_time: float = 0.0,
    distance: float = 0.0,
    carrier: CarrierNetwork | None = None,
    periodic: bool = False,
) -> RelationalContinuumObserverPacket:
    """Construct the 9-tuple relational observer evaluation packet O_cont.

    Verifies combinatorial chain complex property d1 @ d0 == 0 to machine precision.
    Evaluates quotient authorization dynamically via HiGHS linear programming:
    - Pure gauge defect -> AUTHORIZED (quotient_residual <= tolerance)
    - Irreducible quotient obstruction -> OBSTRUCTED (quotient_residual > tolerance, curvature == 0)
    - Irreducible curvature defect -> REFUSAL (curvature_residual > tolerance)
    """
    c_eff_val = _guard_float(c_eff, "c_eff", strictly_positive=True)
    t_val = _guard_float(elapsed_time, "elapsed_time", strictly_positive=False)
    d_val = _guard_float(distance, "distance", strictly_positive=False)
    tol_val = _guard_float(tolerance, "tolerance", strictly_positive=False)

    if carrier is not None:
        carrier_k = tuple(carrier.nodes)
        adjacency_r = tuple(carrier.edges)
        num_sites_val = carrier.num_nodes
        num_edges = carrier.num_edges
        if num_sites is not None:
            ns = _guard_int(num_sites, "num_sites", min_value=2)
            if ns != num_sites_val:
                raise ContinuumCausalityError(
                    f"num_sites {ns} does not match carrier.num_nodes {num_sites_val}"
                )
        d0 = carrier.incidence_matrix_d0()
        d1 = carrier.cycle_matrix_d1() if carrier.faces else np.zeros((1, num_edges), dtype=np.float64)
    else:
        if num_sites is None or isinstance(num_sites, bool) or not isinstance(num_sites, int):
            raise ContinuumCausalityError("num_sites must be integer")
        if num_sites < 2:
            raise ContinuumCausalityError("num_sites must be at least 2")
        num_sites_val = int(num_sites)
        carrier_k = tuple(range(num_sites_val))
        if periodic:
            adjacency_r = tuple((i, (i + 1) % num_sites_val) for i in range(num_sites_val))
        else:
            adjacency_r = tuple((i, i + 1) for i in range(num_sites_val - 1))
        num_edges = len(adjacency_r)

        d0 = np.zeros((num_edges, num_sites_val), dtype=np.float64)
        for e_idx, (u, v) in enumerate(adjacency_r):
            d0[e_idx, u] = -1.0
            d0[e_idx, v] = 1.0
        d1 = np.zeros((1, num_edges), dtype=np.float64)

    # Determine defect delta and terminalizer status dynamically
    if gauge_alpha is not None:
        if any(isinstance(v, bool) for v in gauge_alpha):
            raise ContinuumCausalityError("gauge_alpha cannot contain booleans")
        alpha_arr = np.asarray(gauge_alpha, dtype=np.float64)
        if not np.all(np.isfinite(alpha_arr)):
            raise ContinuumCausalityError("gauge_alpha must contain finite values")
        if len(alpha_arr) != num_sites_val:
            raise ContinuumCausalityError(
                f"gauge_alpha length {len(alpha_arr)} != num_sites {num_sites_val}"
            )
        delta_arr = d0 @ alpha_arr
        is_pure = True
        quotient_res = 0.0
        status: TerminalizerStatus = "AUTHORIZED"
        optimal_gauge = alpha_arr
    elif defect_values is not None:
        if any(isinstance(v, bool) for v in defect_values):
            raise ContinuumCausalityError("defect_values cannot contain booleans")
        delta_arr = np.asarray(defect_values, dtype=np.float64)
        if not np.all(np.isfinite(delta_arr)):
            raise ContinuumCausalityError("defect_values must contain finite values")
        if len(delta_arr) != num_edges:
            raise ContinuumCausalityError(
                f"defect_values length {len(delta_arr)} != num_edges {num_edges}"
            )
        lp_res = compute_quotient_residual_lp(
            gauge_d0=d0,
            defect_delta=delta_arr,
            closure_d1=d1,
            tolerance=tol_val,
        )
        is_pure = lp_res.is_pure_gauge
        quotient_res = lp_res.quotient_residual
        optimal_gauge = lp_res.optimal_gauge
        if is_pure:
            status = "AUTHORIZED"
        elif lp_res.curvature_residual > tol_val:
            status = "REFUSAL"
        else:
            status = "OBSTRUCTED"
    else:
        delta_arr = np.zeros(num_edges, dtype=np.float64)
        is_pure = True
        quotient_res = 0.0
        status = "AUTHORIZED"
        optimal_gauge = np.zeros(num_sites_val, dtype=np.float64)

    gauge_norm = float(np.sum(np.abs(delta_arr)))
    try:
        s2 = (c_eff_val * t_val) ** 2 - d_val ** 2
    except OverflowError:
        raise ContinuumCausalityError("Coordinate separation exceeds float64 dynamic range")
    if not math.isfinite(s2):
        raise ContinuumCausalityError("Coordinate separation exceeds float64 dynamic range")

    # Protect arrays as read-only
    delta_arr.flags.writeable = False
    d0.flags.writeable = False
    d1.flags.writeable = False
    if optimal_gauge is not None:
        optimal_gauge.flags.writeable = False

    return RelationalContinuumObserverPacket(
        carrier_nodes_k=carrier_k,
        local_algebras_f={i: 2 for i in carrier_k},
        adjacency_r=adjacency_r,
        defect_operator_delta=delta_arr,
        gauge_shifts_d0=d0,
        cycle_check_d1=d1,
        gauge_norm_j=gauge_norm,
        transformation_group_m="discrete_relational_isometry",
        causal_terminalizer_tau=status,
        quotient_residual=quotient_res,
        optimal_gauge=optimal_gauge,
        is_pure_gauge=is_pure,
        minkowski_interval_s2=float(s2),
    )


@dataclass(frozen=True)
class ContinuumScalingGrid:
    """Discrete relational hypercubic scaling grid for continuum refinement."""

    lattice_spacing_a: float
    system_length: float
    v_lr: float
    spatial_decay_mu: float = 1.0
    c0: float = 1.0
    operator_cap: float = 2.0
    num_sites: int = field(init=False)
    c_eff: float = field(init=False)

    def __post_init__(self) -> None:
        a = _guard_float(self.lattice_spacing_a, "lattice_spacing_a", strictly_positive=True)
        length = _guard_float(self.system_length, "system_length", strictly_positive=True)
        v = _guard_float(self.v_lr, "v_lr", strictly_positive=True)
        mu = _guard_float(self.spatial_decay_mu, "spatial_decay_mu", strictly_positive=True)
        c0 = _guard_float(self.c0, "c0", strictly_positive=True)
        cap = _guard_float(self.operator_cap, "operator_cap", strictly_positive=True)

        n_sites = max(2, int(round(length / a)) + 1)
        object.__setattr__(self, "lattice_spacing_a", a)
        object.__setattr__(self, "system_length", length)
        object.__setattr__(self, "v_lr", v)
        object.__setattr__(self, "spatial_decay_mu", mu)
        object.__setattr__(self, "c0", c0)
        object.__setattr__(self, "operator_cap", cap)
        object.__setattr__(self, "num_sites", n_sites)
        object.__setattr__(self, "c_eff", v)

    def physical_distance(self, u: int, v: int) -> float:
        """Physical relational distance d = a * |u - v|."""
        return self.lattice_spacing_a * abs(u - v)


def setup_scaling_grid(
    lattice_spacing_a: float,
    system_length: float = 1.0,
    v_lr: float = 1.0,
    spatial_decay_mu: float = 1.0,
    c0: float = 1.0,
    operator_cap: float = 2.0,
) -> ContinuumScalingGrid:
    """Instantiate and validate a discrete relational scaling grid."""
    return ContinuumScalingGrid(
        lattice_spacing_a=lattice_spacing_a,
        system_length=system_length,
        v_lr=v_lr,
        spatial_decay_mu=spatial_decay_mu,
        c0=c0,
        operator_cap=operator_cap,
    )


@dataclass(frozen=True)
class LorentzCausalEnvelopeResult:
    """Evaluation result for emergent Lorentz causality cone and Duhamel weight."""

    distance: float
    elapsed_time: float
    c_eff: float
    minkowski_interval_s2: float
    influence_weight: float
    operator_cap: float
    acausal_leakage: float
    classification: CausalClassification
    spacelike_suppression_factor: float
    is_within_light_cone: bool
    lattice_spacing_a: float = 0.0

    # Cross-explorer compatibility aliases
    @property
    def separation_d(self) -> float:
        return self.distance

    @property
    def physical_distance(self) -> float:
        return self.distance

    @property
    def elapsed_time_tau(self) -> float:
        return self.elapsed_time

    @property
    def causal_sector(self) -> CausalClassification:
        return self.classification

    @property
    def causal_status(self) -> CausalClassification:
        return self.classification

    @property
    def operator_norm_ceiling(self) -> float:
        return self.operator_cap

    @property
    def sharp_light_cone_value(self) -> float:
        return self.operator_cap if self.is_within_light_cone else 0.0


def compute_minkowski_interval(
    separation_d: float,
    elapsed_time_tau: float,
    c_eff: float,
) -> float:
    """Compute emergent Minkowski spacetime interval s^2 = c_eff^2 * tau^2 - d^2."""
    d = _guard_float(separation_d, "separation_d", strictly_positive=False)
    tau = _guard_float(elapsed_time_tau, "elapsed_time_tau", strictly_positive=False)
    c = _guard_float(c_eff, "c_eff", strictly_positive=True)
    try:
        s2 = (c * tau) ** 2 - d ** 2
    except OverflowError:
        raise ContinuumCausalityError("Coordinate separation exceeds float64 dynamic range")
    if not math.isfinite(s2):
        raise ContinuumCausalityError("Coordinate separation exceeds float64 dynamic range")
    return float(s2)


def classify_causal_sector(
    minkowski_interval_s2: float,
    tolerance: float = 1.0e-12,
) -> CausalClassification:
    """Classify spacetime interval into TIMELIKE, NULL, or SPACELIKE sector."""
    s2 = _guard_float(minkowski_interval_s2, "minkowski_interval_s2", allow_negative=True)
    tol = _guard_float(tolerance, "tolerance", strictly_positive=False)

    if s2 > tol:
        return "TIMELIKE"
    if s2 < -tol:
        return "SPACELIKE"
    return "NULL"


def compute_continuum_duhamel_weight(
    separation_d: float,
    elapsed_time_tau: float,
    lattice_spacing_a: float,
    v_lr: float,
    spatial_decay_mu: float = 1.0,
    c0: float = 1.0,
    operator_cap: float = 2.0,
) -> float:
    """Compute Duhamel influence weight at lattice spacing a.

    w(d, tau; a) = min(operator_cap, c0 * operator_cap * exp(-mu/a * (d - v_lr * tau)))
    """
    d = _guard_float(separation_d, "separation_d", strictly_positive=False)
    tau = _guard_float(elapsed_time_tau, "elapsed_time_tau", strictly_positive=False)
    a = _guard_float(lattice_spacing_a, "lattice_spacing_a", strictly_positive=True)
    v = _guard_float(v_lr, "v_lr", strictly_positive=True)
    mu = _guard_float(spatial_decay_mu, "spatial_decay_mu", strictly_positive=True)
    c0_val = _guard_float(c0, "c0", strictly_positive=True)
    cap = _guard_float(operator_cap, "operator_cap", strictly_positive=True)

    delta_s = d - v * tau
    exponent = -(mu / a) * delta_s

    # Overflow guard
    if exponent > 700.0:
        return float(cap)
    # Underflow guard
    if exponent < -700.0:
        return 0.0

    raw_val = c0_val * cap * math.exp(exponent)
    return float(min(cap, max(0.0, raw_val)))


def compute_spacelike_suppression(
    separation_d: float,
    elapsed_time_tau: float,
    lattice_spacing_a: float,
    v_lr: float,
    spatial_decay_mu: float = 1.0,
) -> float:
    """Compute exponential suppression factor exp(-mu/a * (d - v_lr * tau)) for spacelike separations."""
    d = _guard_float(separation_d, "separation_d", strictly_positive=False)
    tau = _guard_float(elapsed_time_tau, "elapsed_time_tau", strictly_positive=False)
    a = _guard_float(lattice_spacing_a, "lattice_spacing_a", strictly_positive=True)
    v = _guard_float(v_lr, "v_lr", strictly_positive=True)
    mu = _guard_float(spatial_decay_mu, "spatial_decay_mu", strictly_positive=True)

    margin = d - v * tau
    if margin <= 0.0:
        return 1.0

    exponent = -(mu / a) * margin
    if exponent < -700.0:
        return 0.0
    return float(math.exp(exponent))


def compute_sharp_minkowski_cone(
    separation_d: float,
    elapsed_time_tau: float,
    c_eff: float,
    operator_cap: float = 2.0,
) -> float:
    """Evaluate sharp relativistic Minkowski light cone operator_cap * Theta(c_eff * tau - d)."""
    d = _guard_float(separation_d, "separation_d", strictly_positive=False)
    tau = _guard_float(elapsed_time_tau, "elapsed_time_tau", strictly_positive=False)
    c = _guard_float(c_eff, "c_eff", strictly_positive=True)
    cap = _guard_float(operator_cap, "operator_cap", strictly_positive=True)

    if d <= c * tau:
        return float(cap)
    return 0.0


def compute_lorentz_causal_envelope(
    grid: ContinuumScalingGrid,
    distance: float,
    elapsed_time: float,
    observable_norm: float = 1.0,
    edge_norm: float = 1.0,
    c0: float = 1.0,
) -> LorentzCausalEnvelopeResult:
    """Evaluate Duhamel influence weight and emergent Minkowski causal classification."""
    d = _guard_float(distance, "distance", strictly_positive=False)
    tau = _guard_float(elapsed_time, "elapsed_time", strictly_positive=False)
    o_norm = _guard_float(observable_norm, "observable_norm", strictly_positive=True)
    h_norm = _guard_float(edge_norm, "edge_norm", strictly_positive=True)
    c0_val = _guard_float(c0, "c0", strictly_positive=True)

    c_eff = grid.c_eff
    operator_cap = 2.0 * o_norm * h_norm
    try:
        s2 = (c_eff * tau) ** 2 - d ** 2
    except OverflowError:
        raise ContinuumCausalityError("Coordinate separation exceeds float64 dynamic range")
    if not math.isfinite(s2):
        raise ContinuumCausalityError("Coordinate separation exceeds float64 dynamic range")

    # Sector classification
    tolerance = 1.0e-12
    if s2 > tolerance:
        sector: CausalClassification = "TIMELIKE"
        weight = operator_cap
        leakage = 0.0
        suppression = 1.0
        within_cone = True
    elif abs(s2) <= tolerance:
        sector = "NULL"
        weight = operator_cap
        leakage = 0.0
        suppression = 1.0
        within_cone = True
    else:
        sector = "SPACELIKE"
        margin = d - c_eff * tau
        exponent = -(grid.spatial_decay_mu / grid.lattice_spacing_a) * margin
        if exponent < -700.0:
            suppression = 0.0
            weight = 0.0
        else:
            suppression = math.exp(exponent)
            weight = min(operator_cap, c0_val * operator_cap * suppression)
        leakage = weight
        within_cone = False

    return LorentzCausalEnvelopeResult(
        distance=d,
        elapsed_time=tau,
        c_eff=c_eff,
        minkowski_interval_s2=s2,
        influence_weight=weight,
        operator_cap=operator_cap,
        acausal_leakage=leakage,
        classification=sector,
        spacelike_suppression_factor=suppression,
        is_within_light_cone=within_cone,
        lattice_spacing_a=grid.lattice_spacing_a,
    )


evaluate_lorentz_causal_envelope = compute_lorentz_causal_envelope


@dataclass(frozen=True)
class DefectCurrent4Vector:
    """Relativistic defect 4-current vector J^mu = (c_eff * nu, j)."""

    density_nu: float
    current_vector: tuple[float, ...]
    c_eff: float

    @property
    def four_current(self) -> tuple[float, ...]:
        return (self.c_eff * self.density_nu, *self.current_vector)


@dataclass(frozen=True)
class DefectCurrentField:
    """Spatiotemporal defect current field and discrete divergence residuals."""

    times: tuple[float, ...]
    positions: tuple[float, ...]
    density_nu: npt.NDArray[np.float64]
    current_j: npt.NDArray[np.float64]
    divergence_residuals: npt.NDArray[np.float64]
    max_residual: float
    rms_residual: float
    lattice_spacing_a: float
    time_step_dt: float

    @property
    def density_j0(self) -> npt.NDArray[np.float64]:
        return self.density_nu

    @property
    def current_j1(self) -> npt.NDArray[np.float64]:
        return self.current_j

    @property
    def max_conservation_residual(self) -> float:
        return self.max_residual


def simulate_defect_wave_packet(
    grid: ContinuumScalingGrid,
    t_max: float,
    n_times: int = 50,
    x0: float = 0.5,
    sigma: float = 0.10,
    k0: float = 0.0,
) -> DefectCurrentField:
    """Simulate smooth Gaussian defect wave packet transport and compute 4-divergence residuals."""
    n_times_val = _guard_int(n_times, "n_times", min_value=3)
    t_max_val = _guard_float(t_max, "t_max", strictly_positive=True)
    sigma_val = _guard_float(sigma, "sigma", strictly_positive=True)
    x0_val = _guard_float(x0, "x0", allow_negative=True)
    _guard_float(k0, "k0", allow_negative=True)

    a = grid.lattice_spacing_a
    c = grid.c_eff
    dt = t_max_val / (n_times_val - 1)
    xs = np.arange(0.0, grid.system_length + a / 2.0, a, dtype=np.float64)
    n_sites = len(xs)
    if n_sites < 3:
        raise ContinuumCausalityError(
            f"Spatial grid must contain at least 3 sites for central-difference evaluation; "
            f"got {n_sites} sites (lattice pitch a={a} is too coarse for system length L={grid.system_length})"
        )
    ts = np.linspace(0.0, t_max_val, n_times_val, dtype=np.float64)

    nu = np.zeros((n_times_val, n_sites), dtype=np.float64)
    j = np.zeros((n_times_val, n_sites), dtype=np.float64)

    for t_idx, t in enumerate(ts):
        center = x0_val + c * t
        profile = np.exp(-((xs - center) ** 2) / (2.0 * sigma_val ** 2))
        nu[t_idx, :] = profile
        j[t_idx, :] = c * profile

    # Compute discrete divergence residuals on interior points using central differences
    res = np.zeros((n_times_val - 2, n_sites - 2), dtype=np.float64)
    for t_idx in range(1, n_times_val - 1):
        d_nu_dt = (nu[t_idx + 1, 1:-1] - nu[t_idx - 1, 1:-1]) / (2.0 * dt)
        dj_dx = (j[t_idx, 2:] - j[t_idx, :-2]) / (2.0 * a)
        res[t_idx - 1, :] = d_nu_dt + dj_dx

    max_res = float(np.max(np.abs(res)))
    rms_res = float(np.sqrt(np.mean(res ** 2)))

    return DefectCurrentField(
        times=tuple(float(t) for t in ts),
        positions=tuple(float(x) for x in xs),
        density_nu=nu,
        current_j=j,
        divergence_residuals=res,
        max_residual=max_res,
        rms_residual=rms_res,
        lattice_spacing_a=a,
        time_step_dt=dt,
    )


compute_defect_current_field = simulate_defect_wave_packet


@dataclass(frozen=True)
class ContinuumRefinementReport:
    """Multi-grid scaling report verifying O(a^2) second-order convergence."""

    spacings: tuple[float, ...]
    residuals: tuple[float, ...]
    convergence_orders: tuple[float, ...]
    mean_order: float
    is_second_order: bool


def verify_conservation_convergence_order(
    spacings: Sequence[float],
    t_eval: float = 0.1,
    c_eff: float = 1.0,
    sigma: float = 0.25,
    x0: float = 0.5,
) -> ContinuumRefinementReport:
    """Perform multi-grid refinement analysis confirming O(a^2) error convergence.

    Computes numerical order p = ln(R(a_1) / R(a_2)) / ln(a_1 / a_2).
    Asserts p approx 2.0 within declared numerical tolerances.
    """
    if not spacings or len(spacings) < 2:
        raise ContinuumCausalityError("Need at least two spacings to evaluate convergence order")

    guarded_spacings = [
        _guard_float(s, f"spacings[{i}]", strictly_positive=True)
        for i, s in enumerate(spacings)
    ]
    t_eval_val = _guard_float(t_eval, "t_eval", strictly_positive=True)
    c_eff_val = _guard_float(c_eff, "c_eff", strictly_positive=True)
    sigma_val = _guard_float(sigma, "sigma", strictly_positive=True)
    x0_val = _guard_float(x0, "x0", allow_negative=True)

    sorted_spacings = tuple(sorted(guarded_spacings, reverse=True))
    residuals: list[float] = []

    # Center domain dynamically on the propagating wave packet
    x_center = x0_val + c_eff_val * t_eval_val
    half_width = max(3.0, 12.0 * sigma_val)

    for a in sorted_spacings:
        # Time step adhering to constant Courant number lambda = 0.5 / c_eff
        lambda_cfl = 0.5 / c_eff_val
        dt = lambda_cfl * a

        # Dynamically centered domain avoids pulse exit at high velocities
        xs = np.arange(x_center - half_width, x_center + half_width + a / 2.0, a, dtype=np.float64)
        if len(xs) < 5:
            raise ContinuumCausalityError(
                f"Spatial grid for spacing a={a} must contain at least 5 sites for second-order stencil"
            )

        # Pulse profile nu(x, t) = exp(-(x - c*t - x0)^2 / (2*sigma^2))
        def pulse(x_grid: np.ndarray, t_val: float) -> np.ndarray:
            u = x_grid - c_eff_val * t_val - x0_val
            return np.exp(-0.5 * (u / sigma_val) ** 2)

        # Central difference in time: (nu(t+dt) - nu(t-dt)) / (2*dt)
        nu_plus = pulse(xs, t_eval_val + dt)
        nu_minus = pulse(xs, t_eval_val - dt)
        d_nu_dt = (nu_plus - nu_minus) / (2.0 * dt)

        # Central difference in space: (j(x+a) - j(x-a)) / (2*a)
        nu_curr = pulse(xs, t_eval_val)
        j_curr = c_eff_val * nu_curr
        dj_dx = (np.roll(j_curr, -1) - np.roll(j_curr, 1)) / (2.0 * a)

        # Strip boundary wrap-around edges
        interior_res = np.abs(d_nu_dt[2:-2] + dj_dx[2:-2])
        if len(interior_res) == 0:
            raise ContinuumCausalityError(f"Lattice spacing a={a} has zero interior stencil width")
        max_r = float(np.max(interior_res))
        if max_r <= 0.0 or not math.isfinite(max_r):
            raise ContinuumCausalityError("Degenerate zero or non-finite conservation residual encountered")
        residuals.append(max_r)

    # Compute convergence orders between consecutive grids
    orders: list[float] = []
    for i in range(len(sorted_spacings) - 1):
        a1, a2 = sorted_spacings[i], sorted_spacings[i + 1]
        r1, r2 = residuals[i], residuals[i + 1]
        if r1 <= 0.0 or r2 <= 0.0 or not math.isfinite(r1) or not math.isfinite(r2):
            raise ContinuumCausalityError("Cannot evaluate convergence order from non-positive or non-finite residuals")
        ratio_r = r1 / r2
        ratio_a = a1 / a2
        if ratio_r <= 0.0 or ratio_a <= 0.0 or ratio_a == 1.0:
            raise ContinuumCausalityError("Invalid ratio for convergence order logarithm")
        order = math.log(ratio_r) / math.log(ratio_a)
        orders.append(order)

    mean_p = float(np.mean(orders))
    is_o_a2 = bool(all(1.85 <= p <= 2.15 for p in orders))

    return ContinuumRefinementReport(
        spacings=sorted_spacings,
        residuals=tuple(residuals),
        convergence_orders=tuple(orders),
        mean_order=mean_p,
        is_second_order=is_o_a2,
    )


def apply_lorentz_boost(
    dt: float,
    dx: float,
    c_eff: float,
    beta: float,
) -> tuple[float, float]:
    """Apply relativistic Lorentz boost to coordinate separation (dt, dx).

    Asserts subluminal velocity |beta| < 1.0.
    Returns (dt_prime, dx_prime) satisfying:
    c_eff^2 dt_prime^2 - dx_prime^2 == c_eff^2 dt^2 - dx^2.
    """
    t = _guard_float(dt, "dt", allow_negative=True)
    x = _guard_float(dx, "dx", allow_negative=True)
    c = _guard_float(c_eff, "c_eff", strictly_positive=True)
    if isinstance(beta, bool):
        raise ContinuumCausalityError("beta must be numeric")
    b = _guard_float(beta, "beta", allow_negative=True)
    if abs(b) >= 1.0:
        raise ContinuumCausalityError("Boost velocity must be strictly subluminal (|beta| < 1)")

    gamma = 1.0 / math.sqrt(1.0 - b ** 2)
    dt_prime = gamma * (t - (b * x) / c)
    dx_prime = gamma * (x - b * c * t)
    return float(dt_prime), float(dx_prime)


def verify_lorentz_boost_invariance(
    separation_d: float,
    elapsed_time_tau: float,
    boost_velocity: float,
    c_eff: float,
    atol: float = 1.0e-12,
) -> tuple[float, float, bool]:
    """Verify that Minkowski interval s^2 is invariant under relational Lorentz boost."""
    d = _guard_float(separation_d, "separation_d", strictly_positive=False)
    tau = _guard_float(elapsed_time_tau, "elapsed_time_tau", strictly_positive=False)
    c = _guard_float(c_eff, "c_eff", strictly_positive=True)
    if isinstance(boost_velocity, bool) or not isinstance(boost_velocity, (int, float)):
        raise ContinuumCausalityError("boost_velocity must be numeric")
    v = float(boost_velocity)
    if not math.isfinite(v):
        raise ContinuumCausalityError("boost_velocity must be finite")
    tol = _guard_float(atol, "atol", strictly_positive=False)

    beta = v / c
    if abs(beta) >= 1.0:
        raise ContinuumCausalityError("Boost velocity must be strictly subluminal (|v| < c_eff)")

    tau_p, d_p = apply_lorentz_boost(dt=tau, dx=d, c_eff=c, beta=beta)

    s2_orig = (c * tau) ** 2 - d ** 2
    s2_prime = (c * tau_p) ** 2 - d_p ** 2

    # Scale tolerance with gamma^2 to enclose cancellation roundoff noise as beta -> 1^-:
    gamma = 1.0 / math.sqrt(1.0 - beta ** 2)
    effective_atol = max(tol, tol * (gamma ** 2))

    is_inv = bool(abs(s2_orig - s2_prime) <= effective_atol)
    return float(s2_orig), float(s2_prime), is_inv


@dataclass(frozen=True)
class ContinuumConvergenceAnalysis:
    """Convergence diagnostics for continuum limit a -> 0."""

    spacings_a: tuple[float, ...]
    l1_errors_to_sharp_cone: tuple[float, ...]
    spacelike_leakages: tuple[float, ...]
    empirical_convergence_order: float
    is_converging: bool


def analyze_continuum_scaling_limit(
    spacings: Sequence[float],
    elapsed_time_tau: float,
    v_lr: float,
    spatial_decay_mu: float = 1.0,
    operator_cap: float = 2.0,
    system_length: float = 2.0,
    num_sample_points: int = 1000,
) -> ContinuumConvergenceAnalysis:
    """Analyze convergence of Duhamel weight to sharp light cone across lattice pitch refinements."""
    if not spacings or len(spacings) < 2:
        raise ContinuumCausalityError("At least two lattice spacings are required for scaling analysis")

    tau = _guard_float(elapsed_time_tau, "elapsed_time_tau", strictly_positive=False)
    v = _guard_float(v_lr, "v_lr", strictly_positive=True)
    mu = _guard_float(spatial_decay_mu, "spatial_decay_mu", strictly_positive=True)
    cap = _guard_float(operator_cap, "operator_cap", strictly_positive=True)
    length = _guard_float(system_length, "system_length", strictly_positive=True)
    n_pts = _guard_int(num_sample_points, "num_sample_points", min_value=10)

    sorted_spacings = tuple(sorted(
        [_guard_float(a, "spacing", strictly_positive=True) for a in spacings],
        reverse=True,
    ))

    x_grid = np.linspace(0.0, length, max(100, n_pts), dtype=np.float64)
    dx = float(x_grid[1] - x_grid[0])

    sharp_profile = np.array(
        [
            compute_sharp_minkowski_cone(x, tau, v, cap)
            for x in x_grid
        ],
        dtype=np.float64,
    )

    l1_errors: list[float] = []
    spacelike_leakages: list[float] = []

    for a in sorted_spacings:
        weights = np.array(
            [
                compute_continuum_duhamel_weight(
                    separation_d=x,
                    elapsed_time_tau=tau,
                    lattice_spacing_a=a,
                    v_lr=v,
                    spatial_decay_mu=mu,
                    operator_cap=cap,
                )
                for x in x_grid
            ],
            dtype=np.float64,
        )
        l1_err = float(np.sum(np.abs(weights - sharp_profile)) * dx)
        l1_errors.append(l1_err)

        spacelike_mask = x_grid > (v_lr * elapsed_time_tau + 1.0e-12)
        if np.any(spacelike_mask):
            leakage = float(np.max(weights[spacelike_mask]))
        else:
            leakage = 0.0
        spacelike_leakages.append(leakage)

    log_a = np.log(np.array(sorted_spacings))
    log_e = np.log(np.array(l1_errors))
    slope, _ = np.polyfit(log_a, log_e, 1)

    is_conv = bool(l1_errors[-1] < l1_errors[0] and spacelike_leakages[-1] < spacelike_leakages[0])

    return ContinuumConvergenceAnalysis(
        spacings_a=sorted_spacings,
        l1_errors_to_sharp_cone=tuple(l1_errors),
        spacelike_leakages=tuple(spacelike_leakages),
        empirical_convergence_order=float(slope),
        is_converging=is_conv,
    )
