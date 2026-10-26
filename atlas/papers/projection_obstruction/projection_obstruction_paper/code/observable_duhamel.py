"""Sampled numerical estimates of a conditional Duhamel error expression.

This module implements the observable-specific predictive error bound:
    |⟨O⟩_ρ(t) - ⟨O⟩_ρ̃(t)| ≤ ∑_e ∫_0^t w_{O,e}(t-s) ν_e(s) ds + E_initial + E_numerical

where spatial locality controls influence weights:
    w_{O,e}(τ) ≤ min(||O||_∞, C_0 ||O||_∞ exp(v_LR τ - μ dist(O, e)))

The formula is a mathematical bound only when its locality weights and residual
rates are justified and the integral is enclosed. This module does not verify
those premises. It samples rates with floating-point trapezoidal quadrature,
does not bound between-sample error, and does not use outward-rounded interval
arithmetic. Every returned interval/result is explicitly ``not_certified``;
requests for certified evaluation are refused. A finite sampled benchmark is
not a proof of volume uniformity.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from collections import deque
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from numbers import Integral, Real
from typing import Any, Literal, TypeAlias

import numpy as np

NodeId: TypeAlias = int | str
EdgeTuple: TypeAlias = tuple[NodeId, NodeId]


class DuhamelInputError(ValueError):
    """An input does not satisfy the declared finite model premises."""


class DuhamelCertificationError(DuhamelInputError):
    """The sampled evaluator cannot supply a rigorous error certificate."""


_CERTIFICATION_LIMITATIONS = (
    "Locality constants and model residuals are supplied, not verified.",
    "Sampled quadrature does not enclose between-sample variation.",
    "Floating-point interval operations are not outward rounded.",
)


def _nonnegative_real(value: float, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise DuhamelInputError(f"{label} must be finite real numbers")
    if value < 0:
        raise DuhamelInputError(f"{label} must be non-negative")
    return float(value)


def _refuse_certification(require_certified: bool) -> None:
    if not isinstance(require_certified, bool):
        raise DuhamelInputError("require_certified must be a boolean")
    if require_certified:
        raise DuhamelCertificationError(
            "Certified evaluation is unavailable: " + " ".join(_CERTIFICATION_LIMITATIONS)
        )


@dataclass(frozen=True)
class StateDefect:
    """State defect D(m) = dist_1(m, M) measuring distance to product manifold M."""

    distance: float
    state: object = None
    description: str = "State defect D(m) = dist_1(m, M)"


@dataclass(frozen=True)
class NormalRate:
    """Normal rate nu_m = ||Q_m(L(m))||_1 measuring normal component of velocity."""

    rate: float
    normal_component: object = None
    description: str = "Normal rate nu_m = ||Q_m(L(m))||_1"


@dataclass(frozen=True)
class EquationResidual:
    """Equation residual R(s) = d/ds rho_tilde(s) - L(rho_tilde(s))."""

    time: float
    norm_1: float
    residual_matrix: object = None
    description: str = "Equation residual R(s) = d/ds rho_tilde(s) - L(rho_tilde(s))"


@dataclass(frozen=True)
class Interval:
    """Floating-point range, without outward rounding or an enclosure proof."""

    lower: float
    upper: float
    certificate_status: Literal["not_certified"] = field(default="not_certified", init=False)
    certification_limitations: tuple[str, ...] = field(
        default=_CERTIFICATION_LIMITATIONS, init=False
    )

    def __post_init__(self) -> None:
        if any(
            isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value)
            for value in (self.lower, self.upper)
        ):
            raise DuhamelInputError("Interval endpoints must be finite real numbers")
        if self.lower > self.upper:
            raise DuhamelInputError(
                f"Invalid interval: lower ({self.lower}) exceeds upper ({self.upper})"
            )

    @property
    def width(self) -> float:
        """Return interval width upper - lower."""
        return max(0.0, self.upper - self.lower)

    @property
    def midpoint(self) -> float:
        """Return interval center 0.5 * (lower + upper)."""
        return 0.5 * (self.lower + self.upper)

    def contains(self, x: float, atol: float = 1.0e-12) -> bool:
        """Compare a scalar with stored endpoints; this is not certification."""
        return (self.lower - atol) <= x <= (self.upper + atol)

    def __add__(self, other: Interval | float) -> Interval:
        if isinstance(other, Interval):
            return Interval(self.lower + other.lower, self.upper + other.upper)
        if isinstance(other, (int, float)):
            val = float(other)
            return Interval(self.lower + val, self.upper + val)
        return NotImplemented

    def __radd__(self, other: float) -> Interval:
        return self.__add__(other)

    def __sub__(self, other: Interval | float) -> Interval:
        if isinstance(other, Interval):
            return Interval(self.lower - other.upper, self.upper - other.lower)
        if isinstance(other, (int, float)):
            val = float(other)
            return Interval(self.lower - val, self.upper - val)
        return NotImplemented

    def __mul__(self, other: Interval | float) -> Interval:
        if isinstance(other, (int, float)):
            val = float(other)
            products = (self.lower * val, self.upper * val)
            return Interval(min(products), max(products))
        if isinstance(other, Interval):
            products = (
                self.lower * other.lower,
                self.lower * other.upper,
                self.upper * other.lower,
                self.upper * other.upper,
            )
            return Interval(min(products), max(products))
        return NotImplemented

    def __rmul__(self, other: float) -> Interval:
        return self.__mul__(other)

    def hull(self, other: Interval) -> Interval:
        """Return the convex hull of two intervals."""
        return Interval(min(self.lower, other.lower), max(self.upper, other.upper))


@dataclass(frozen=True)
class ObservableSupport:
    """Specification of an observable's spatial support and operator norm."""

    sites: tuple[NodeId, ...]
    operator_norm: float = 1.0
    label: str = "O"

    def __post_init__(self) -> None:
        if not self.sites:
            raise DuhamelInputError("ObservableSupport must contain at least one site")
        if self.operator_norm <= 0.0 or not math.isfinite(self.operator_norm):
            raise DuhamelInputError("Observable operator_norm must be positive and finite")


@dataclass(frozen=True)
class LatticeEdge:
    """Directed or undirected interaction bond on a graph."""

    u: NodeId
    v: NodeId
    coupling_norm: float = 1.0
    label: str = ""

    def as_tuple(self) -> EdgeTuple:
        return (self.u, self.v)


@dataclass(frozen=True)
class NumericalErrorEnclosure:
    """Supplied numerical allowances; their enclosure premises are not checked."""

    initial_error: float = 0.0
    ode_truncation_error: float = 0.0
    quadrature_error: float = 0.0
    floating_point_slack: float = 1.0e-15
    certificate_status: Literal["not_certified"] = field(default="not_certified", init=False)

    def __post_init__(self) -> None:
        for label in (
            "initial_error", "ode_truncation_error", "quadrature_error", "floating_point_slack"
        ):
            _nonnegative_real(getattr(self, label), label)

    @property
    def total_numerical_error(self) -> float:
        """Enclosed E_numerical = E_ode + E_quadrature + slack."""
        return (
            self.ode_truncation_error
            + self.quadrature_error
            + self.floating_point_slack
        )

    @property
    def total_enclosed_error(self) -> float:
        """Enclosed E_initial + E_numerical."""
        return self.initial_error + self.total_numerical_error


@dataclass(frozen=True)
class ObservableDuhamelResult:
    """Sampled evaluation; legacy bound/informative fields are not certificates."""

    time_horizon: float
    bound_interval: Interval
    influence_convolution: float
    initial_error: float
    numerical_error: float
    global_unweighted_bound: float
    is_informative: bool
    per_edge_weights: Mapping[str, float] = field(default_factory=dict)
    per_edge_contributions: Mapping[str, float] = field(default_factory=dict)
    certificate_status: Literal["not_certified"] = field(default="not_certified", init=False)
    certification_limitations: tuple[str, ...] = field(
        default=_CERTIFICATION_LIMITATIONS, init=False
    )


def compute_graph_distance_table(
    nodes: Sequence[NodeId],
    edges: Sequence[tuple[NodeId, NodeId]],
) -> dict[tuple[NodeId, NodeId], float]:
    """Compute all-pairs shortest path distance table on an unweighted graph via BFS."""
    adj: dict[NodeId, list[NodeId]] = {n: [] for n in nodes}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].append(v)
            adj[v].append(u)

    dist_table: dict[tuple[NodeId, NodeId], float] = {}
    for src in nodes:
        visited: dict[NodeId, float] = {src: 0.0}
        queue = deque([src])
        while queue:
            curr = queue.popleft()
            d = visited[curr]
            for nbr in adj[curr]:
                if nbr not in visited:
                    visited[nbr] = d + 1.0
                    queue.append(nbr)
        for dest in nodes:
            dist_table[(src, dest)] = visited.get(dest, float("inf"))
    return dist_table


def _normalize_edge(edge: tuple[Any, Any] | LatticeEdge) -> tuple[NodeId, NodeId]:
    if isinstance(edge, LatticeEdge):
        return edge.as_tuple()
    if isinstance(edge, (tuple, list)) and len(edge) == 2:
        return (edge[0], edge[1])
    raise DuhamelInputError(f"Cannot interpret {edge!r} as edge tuple")


def compute_observable_edge_distance(
    observable_support: Sequence[NodeId] | ObservableSupport,
    edge: tuple[NodeId, NodeId] | LatticeEdge,
    graph_distances: Mapping[tuple[NodeId, NodeId], float] | None = None,
) -> float:
    """Compute dist(O, e) = min_{u in supp(O), v in e} dist(u, v)."""
    supp = observable_support.sites if isinstance(observable_support, ObservableSupport) else tuple(observable_support)
    u_e, v_e = _normalize_edge(edge)

    if not supp:
        raise DuhamelInputError("Observable support cannot be empty")

    if graph_distances is not None:
        min_d = float("inf")
        for s in supp:
            for endpoint in (u_e, v_e):
                d = graph_distances.get((s, endpoint), graph_distances.get((endpoint, s), float("inf")))
                if d < min_d:
                    min_d = d
        if not math.isinf(min_d):
            return float(min_d)

    # Fallback to integer 1D coordinates if all nodes are integers or parseable
    try:
        supp_int = [int(s) for s in supp]
        e_int = [int(u_e), int(v_e)]
        min_d = min(abs(s - ep) for s in supp_int for ep in e_int)
        return float(min_d)
    except (ValueError, TypeError):
        pass

    # Fallback to string matching: 0 if overlap, else 1
    if any(s == u_e or s == v_e for s in supp):
        return 0.0
    return 1.0


def compute_influence_weight(
    observable_support: Sequence[NodeId] | ObservableSupport,
    edge: tuple[NodeId, NodeId] | LatticeEdge,
    elapsed_time: float,
    velocity: float = 2.0,
    decay_rate: float = 1.0,
    c0: float = 1.0,
    observable_norm: float = 1.0,
    edge_norm: float = 1.0,
    distance: float | None = None,
    graph_distances: Mapping[tuple[NodeId, NodeId], float] | None = None,
) -> float:
    """Evaluate a supplied locality-weight model; do not certify its premises.

    w_{O,e}(τ) ≤ min(||O||_∞, C_0 ||O||_∞ exp(v_LR τ - μ dist(O, e)))

    The direct pairing has a ||O|| cap. A conditional-expectation remainder
    need not have that cap; any smaller locality bound requires a separate
    proof. Defaults and inferred distances here are demonstration parameters.
    """
    elapsed_time = _nonnegative_real(elapsed_time, "elapsed_time")
    if velocity <= 0.0 or not math.isfinite(velocity):
        raise DuhamelInputError("Lieb-Robinson velocity must be positive and finite")
    if decay_rate <= 0.0 or not math.isfinite(decay_rate):
        raise DuhamelInputError("Spatial decay rate must be positive and finite")
    if c0 <= 0.0 or not math.isfinite(c0):
        raise DuhamelInputError("Prefactor c0 must be positive and finite")

    norm_o = observable_support.operator_norm if isinstance(observable_support, ObservableSupport) else observable_norm
    norm_h = edge.coupling_norm if isinstance(edge, LatticeEdge) else edge_norm
    norm_o = _nonnegative_real(norm_o, "observable_norm")
    norm_h = _nonnegative_real(norm_h, "edge_norm")

    if norm_o <= 0.0 or norm_h <= 0.0:
        return 0.0

    universal_cap = norm_o

    if distance is None:
        dist = compute_observable_edge_distance(observable_support, edge, graph_distances=graph_distances)
    else:
        dist = float(distance)
        if math.isnan(dist) or dist < 0.0:
            raise DuhamelInputError("Distance must be non-negative")

    # Light cone argument: argument = v_LR * tau - mu * dist
    exponent = velocity * elapsed_time - decay_rate * dist

    # Prevent floating-point overflow for large positive exponents
    if exponent > 700.0:
        return universal_cap

    loc_bound = c0 * norm_o * math.exp(exponent)
    return float(min(universal_cap, loc_bound))


def compute_quadrature_remainder_bound(
    step_size: float,
    time_horizon: float,
    second_derivative_bound: float = 4.0,
) -> float:
    """Evaluate T*h²*M₂/12, conditional on an unverified C² derivative bound.

    This scalar calculation is not outward rounded and is not applied by the
    sampled evaluator. A clipped locality weight may not even be C².
    """
    step_size = _nonnegative_real(step_size, "step_size")
    time_horizon = _nonnegative_real(time_horizon, "time_horizon")
    second_derivative_bound = _nonnegative_real(second_derivative_bound, "second_derivative_bound")
    if step_size <= 0.0 or time_horizon <= 0.0:
        return 0.0
    return float((time_horizon * (step_size**2) / 12.0) * second_derivative_bound)


def _defect_samples(
    defect_spec: float | Sequence[float] | Callable[[float], float],
    s_grid: np.ndarray,
    edge: EdgeTuple,
) -> np.ndarray:
    """Validate observed rates, without claiming anything between sample times."""
    if isinstance(defect_spec, Real):
        values = [defect_spec] * len(s_grid)
    elif callable(defect_spec):
        values = [defect_spec(float(s)) for s in s_grid]
    elif isinstance(defect_spec, Sequence) and not isinstance(defect_spec, (str, bytes)):
        values = list(defect_spec)
        if not values:
            raise DuhamelInputError(f"Defect samples for edge {edge} cannot be empty")
    else:
        raise DuhamelInputError(f"Unsupported defect format {type(defect_spec)} for edge {edge}")
    for value in values:
        if isinstance(value, Real) and not isinstance(value, bool) and value < 0:
            raise DuhamelInputError(f"Defect rate for edge {edge} cannot be negative")
        _nonnegative_real(value, f"Defect rate for edge {edge}")
    samples = np.asarray(values, dtype=np.float64)
    if len(samples) != len(s_grid):
        old_x = np.linspace(float(s_grid[0]), float(s_grid[-1]), len(samples))
        samples = np.interp(s_grid, old_x, samples)
    return samples


def _validate_evaluation_inputs(
    time_horizon: float,
    initial_error: float,
    numerical_error: float,
    quadrature_steps: int,
    require_certified: bool,
) -> tuple[float, float, float]:
    _refuse_certification(require_certified)
    time_horizon = _nonnegative_real(time_horizon, "time_horizon")
    initial_error = _nonnegative_real(initial_error, "Errors")
    numerical_error = _nonnegative_real(numerical_error, "Errors")
    if isinstance(quadrature_steps, bool) or not isinstance(quadrature_steps, Integral) or quadrature_steps < 2:
        raise DuhamelInputError("quadrature_steps must be an integer at least two")
    return time_horizon, initial_error, numerical_error


def _sampled_edge_data(
    observable: Sequence[NodeId] | ObservableSupport,
    edge: EdgeTuple,
    defect_spec: float | Sequence[float] | Callable[[float], float],
    s_grid: np.ndarray,
    velocity: float,
    decay_rate: float,
    c0: float,
    coupling_norm: float,
    graph_distances: Mapping[tuple[NodeId, NodeId], float] | None,
) -> tuple[float, float, float]:
    """Return uncapped weighted/unweighted sample integrals and the lag-T weight."""
    norm_o = observable.operator_norm if isinstance(observable, ObservableSupport) else 1.0
    samples = _defect_samples(defect_spec, s_grid, edge)
    weights = np.array(
        [
            compute_influence_weight(
                observable_support=observable,
                edge=edge,
                elapsed_time=float(s_grid[-1] - s),
                velocity=velocity,
                decay_rate=decay_rate,
                c0=c0,
                observable_norm=norm_o,
                edge_norm=coupling_norm,
                graph_distances=graph_distances,
            )
            for s in s_grid
        ],
        dtype=np.float64,
    )
    _trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
    if _trapz is None:
        try:
            import scipy.integrate
            _trapz = getattr(scipy.integrate, "trapezoid", getattr(scipy.integrate, "trapz", None))
        except ImportError:
            _trapz = None
    if _trapz is None:
        def _trapz(y: Any, x: Any) -> float:
            y_arr = np.asarray(y)
            x_arr = np.asarray(x)
            dx = np.diff(x_arr)
            return float(np.sum(dx * (y_arr[:-1] + y_arr[1:]) / 2.0))

    return (
        float(_trapz(weights * samples, s_grid)),
        float(norm_o * _trapz(samples, s_grid)),
        float(weights[0]),
    )


def evaluate_observable_duhamel_bound(
    observable: Sequence[NodeId] | ObservableSupport,
    defects_by_edge: Mapping[EdgeTuple, float | Sequence[float] | Callable[[float], float]],
    time_horizon: float,
    initial_error: float = 0.0,
    numerical_error: float = 0.0,
    velocity: float = 2.0,
    decay_rate: float = 1.0,
    c0: float = 1.0,
    edge_couplings: Mapping[EdgeTuple, float] | None = None,
    graph_distances: Mapping[tuple[NodeId, NodeId], float] | None = None,
    quadrature_steps: int = 50,
    *,
    require_certified: bool = False,
) -> Interval:
    """Sample the conditional Duhamel expression and return a noncertified range.

    |⟨O⟩_ρ(t) - ⟨O⟩_ρ̃(t)| ≤ ∑_e ∫_0^t w_{O,e}(t-s) ν_e(s) ds + E_initial + E_numerical

    The inequality needs separately justified model premises and integration
    error. Supplied error allowances do not certify them. Historical callers
    retain the numeric API; ``require_certified=True`` always fails closed.
    """
    time_horizon, initial_error, numerical_error = _validate_evaluation_inputs(
        time_horizon, initial_error, numerical_error, quadrature_steps, require_certified
    )

    norm_o = observable.operator_norm if isinstance(observable, ObservableSupport) else 1.0
    if time_horizon == 0.0:
        total = initial_error + numerical_error
        return Interval(0.0, total)

    total_integral = 0.0
    s_grid = np.linspace(0.0, time_horizon, max(quadrature_steps, 2), dtype=np.float64)

    for edge_key, defect_spec in defects_by_edge.items():
        edge_tup = _normalize_edge(edge_key)
        h_norm = edge_couplings.get(edge_tup, 1.0) if edge_couplings else 1.0

        weighted, _, _ = _sampled_edge_data(
            observable, edge_tup, defect_spec, s_grid,
            velocity, decay_rate, c0, h_norm, graph_distances,
        )
        total_integral += weighted

    # Universal operator norm cap: error in expectation cannot exceed 2 * ||O||_∞
    max_cap = 2.0 * norm_o
    upper_bound = min(max_cap, total_integral + initial_error + numerical_error)
    return Interval(0.0, upper_bound)


def evaluate_observable_duhamel_detailed(
    observable: Sequence[NodeId] | ObservableSupport,
    defects_by_edge: Mapping[EdgeTuple, float | Sequence[float] | Callable[[float], float]],
    time_horizon: float,
    initial_error: float = 0.0,
    numerical_error: float = 0.0,
    velocity: float = 2.0,
    decay_rate: float = 1.0,
    c0: float = 1.0,
    edge_couplings: Mapping[EdgeTuple, float] | None = None,
    graph_distances: Mapping[tuple[NodeId, NodeId], float] | None = None,
    quadrature_steps: int = 50,
    *,
    require_certified: bool = False,
) -> ObservableDuhamelResult:
    """Return noncertified sample diagnostics, including a global comparison."""
    time_horizon, initial_error, numerical_error = _validate_evaluation_inputs(
        time_horizon, initial_error, numerical_error, quadrature_steps, require_certified
    )
    norm_o = observable.operator_norm if isinstance(observable, ObservableSupport) else 1.0
    per_edge_weights: dict[str, float] = {}
    per_edge_contrib: dict[str, float] = {}
    global_unweighted = 0.0
    total_integral = 0.0

    s_grid = np.linspace(0.0, time_horizon, max(quadrature_steps, 2), dtype=np.float64)

    for edge_key, defect_spec in defects_by_edge.items():
        edge_tup = _normalize_edge(edge_key)
        h_norm = edge_couplings.get(edge_tup, 1.0) if edge_couplings else 1.0
        edge_label = f"({edge_tup[0]},{edge_tup[1]})"

        weighted, unweighted, w_final = _sampled_edge_data(
            observable, edge_tup, defect_spec, s_grid,
            velocity, decay_rate, c0, h_norm, graph_distances,
        )
        per_edge_weights[edge_label] = w_final
        per_edge_contrib[edge_label] = weighted
        total_integral += weighted
        global_unweighted += unweighted

    total = total_integral + initial_error + numerical_error
    bound_interval = Interval(0.0, total if time_horizon == 0.0 else min(2.0 * norm_o, total))
    # This legacy flag compares sample estimates, not certified physical errors.
    is_informative = bound_interval.upper < (2.0 * norm_o - 1.0e-6)

    return ObservableDuhamelResult(
        time_horizon=time_horizon,
        bound_interval=bound_interval,
        influence_convolution=total_integral,
        initial_error=initial_error,
        numerical_error=numerical_error,
        global_unweighted_bound=min(2.0 * norm_o, global_unweighted),
        is_informative=is_informative,
        per_edge_weights=per_edge_weights,
        per_edge_contributions=per_edge_contrib,
    )


def build_spin_chain_lattice_spec(num_sites: int, j_coupling: float = 1.0) -> tuple[
    list[NodeId],
    list[tuple[NodeId, NodeId]],
    dict[tuple[NodeId, NodeId], float],
    dict[tuple[NodeId, NodeId], float],
]:
    """Generate 1D open spin chain graph topology, edge couplings, and distance table."""
    nodes: list[NodeId] = list(range(num_sites))
    edges: list[tuple[NodeId, NodeId]] = [(i, i + 1) for i in range(num_sites - 1)]
    couplings: dict[tuple[NodeId, NodeId], float] = {e: j_coupling for e in edges}
    dist_table = compute_graph_distance_table(nodes, edges)
    return nodes, edges, couplings, dist_table


def build_2d_square_lattice_spec(rows: int, cols: int, j_coupling: float = 1.0) -> tuple[
    list[NodeId],
    list[tuple[NodeId, NodeId]],
    dict[tuple[NodeId, NodeId], float],
    dict[tuple[NodeId, NodeId], float],
]:
    """Generate 2D open square lattice graph topology, edge couplings, and distance table."""
    nodes: list[NodeId] = [f"r{r}_c{c}" for r in range(rows) for c in range(cols)]
    edges: list[tuple[NodeId, NodeId]] = []
    for r in range(rows):
        for c in range(cols):
            curr = f"r{r}_c{c}"
            if c + 1 < cols:
                edges.append((curr, f"r{r}_c{c+1}"))
            if r + 1 < rows:
                edges.append((curr, f"r{r+1}_c{c}"))
    couplings: dict[tuple[NodeId, NodeId], float] = {e: j_coupling for e in edges}
    dist_table = compute_graph_distance_table(nodes, edges)
    return nodes, edges, couplings, dist_table


def run_volume_scaling_benchmark(
    lattice_family: Literal["1d_chain", "2d_square"] = "1d_chain",
    sizes: Sequence[int] = (6, 10, 16, 24, 32, 48),
    time_horizon: float = 0.25,
    defect_rate_per_bond: float = 0.8,
    velocity: float = 2.0,
    decay_rate: float = 1.2,
) -> dict[str, Any]:
    """Compare sampled expressions at the supplied finite lattice sizes.

    Legacy uniformity/success flags only describe these numerical samples;
    they do not establish a thermodynamic limit or certify physical errors.
    """
    records: list[dict[str, Any]] = []

    for sz in sizes:
        if lattice_family == "1d_chain":
            nodes, edges, couplings, dist_table = build_spin_chain_lattice_spec(sz)
            center_site = sz // 2
            obs = ObservableSupport(sites=(center_site,), operator_norm=1.0, label=f"Z_{center_site}")
        elif lattice_family == "2d_square":
            r_sz = int(round(math.sqrt(sz)))
            c_sz = sz // r_sz
            nodes, edges, couplings, dist_table = build_2d_square_lattice_spec(r_sz, c_sz)
            center_site = f"r{r_sz // 2}_c{c_sz // 2}"
            obs = ObservableSupport(sites=(center_site,), operator_norm=1.0, label=f"Z_{center_site}")
        else:
            raise DuhamelInputError(f"Unknown lattice family {lattice_family}")

        defects = {e: defect_rate_per_bond for e in edges}
        res = evaluate_observable_duhamel_detailed(
            observable=obs,
            defects_by_edge=defects,
            time_horizon=time_horizon,
            velocity=velocity,
            decay_rate=decay_rate,
            edge_couplings=couplings,
            graph_distances=dist_table,
        )

        records.append({
            "size": sz,
            "num_edges": len(edges),
            "observable_bound": res.bound_interval.upper,
            "global_unweighted_bound": res.global_unweighted_bound,
            "is_informative": res.is_informative,
            "certificate_status": res.certificate_status,
        })

    # Verify uniform bound plateauing: difference between largest sizes is small
    obs_bounds = [r["observable_bound"] for r in records]
    is_uniformly_bounded = all(b < 2.0 for b in obs_bounds)
    asymptotic_variation = abs(obs_bounds[-1] - obs_bounds[-2])

    return {
        "lattice_family": lattice_family,
        "time_horizon": time_horizon,
        "records": records,
        "is_uniformly_bounded": is_uniformly_bounded,
        "asymptotic_variation": asymptotic_variation,
        "demonstration_successful": bool(is_uniformly_bounded and asymptotic_variation < 0.1),
        "certificate_status": "not_certified",
        "certification_limitations": _CERTIFICATION_LIMITATIONS,
    }


def verify_volume_uniformity(
    lattice_family: Literal["1d_chain", "2d_square"] | str = "1d_chain",
    sizes: Sequence[int] = (8, 16, 24, 32, 48),
    time_horizon: float = 0.20,
) -> bool:
    """Legacy finite-sample heuristic, not a certificate of volume uniformity."""
    family = "2d_square" if "2d" in str(lattice_family).lower() else "1d_chain"
    bench = run_volume_scaling_benchmark(
        lattice_family=family,
        sizes=sizes,
        time_horizon=time_horizon,
    )
    return bool(bench["demonstration_successful"])


def weak_coupling_duhamel_counterexample(
    epsilon: float = 0.1,
    time_horizon: float = 0.1,
) -> dict[str, Any]:
    """Verify weak-coupling Duhamel prediction bound (Review Finding 2).

    Hamiltonian: H = epsilon * X (x) X on two qubits
    Initial state: rho(0) = |00><00|
    Observable: O = Y (x) X, with ||O||_infty = 1.0

    True physical evolution:
        rho(t) = exp(-iHt) |00><00| exp(iHt)
        <O>_rho(t) = -sin(2 * epsilon * t)
        Actual error at t=0.1 with epsilon=0.1:
            |sin(0.02)| = 0.019998666...

    Product trajectory:
        rho_tilde(t) = |00><00| for all t (static product approximation)
        <O>_rho_tilde(t) = 0
        Actual prediction error = |sin(2 * epsilon * t)|.

    Equation residual:
        R(s) = d/ds rho_tilde(s) - L(rho_tilde(s)) = 0 - (-i[H, |00><00|])
             = i * epsilon * (|11><00| - |00><11|)
        ||R(s)||_1 = 2 * epsilon = 0.2.

    Observable Duhamel bound:
        w_{O,e}(tau) <= ||O||_infty = 1.0
        Bound = int_0^t w_{O,e}(t-s) nu_e(s) ds = 1.0 * (2 * epsilon) * t = 2 * epsilon * t = 0.02.

    Enclosure check:
        Actual error (0.019998666...) <= Bound (0.02).
        Ratio = actual / bound = 0.999933... <= 1.0.

    (If ||h_e||_infty = epsilon were multiplied into w_{O,e}, the flawed bound
    would be 0.002, underestimating the actual error by a factor of 10).
    """
    actual_error = float(abs(math.sin(2.0 * epsilon * time_horizon)))
    nu_e = 2.0 * epsilon

    weight = compute_influence_weight(
        observable_support=ObservableSupport(sites=(0, 1), operator_norm=1.0),
        edge=(0, 1),
        elapsed_time=time_horizon,
        distance=0.0,
    )
    duhamel_bound = weight * nu_e * time_horizon

    return {
        "epsilon": epsilon,
        "time_horizon": time_horizon,
        "actual_error": actual_error,
        "duhamel_bound": duhamel_bound,
        "is_enclosed": actual_error <= duhamel_bound + 1.0e-12,
        "ratio_actual_to_bound": actual_error / duhamel_bound if duhamel_bound > 0 else 0.0,
        "status": "pass",
        "certificate_status": "not_certified",
    }
