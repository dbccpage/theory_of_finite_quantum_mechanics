"""DDC letter R: residual projection that carries, never erases, a residual.

R moves a defect to a canonical representative of its class by subtracting a
coboundary. Subtracting ``d0 phi`` changes neither Phi1 (the class in
``C1 / im d0`` is fixed) nor Gamma2 (``d1 d0 = 0``), which is exactly R's step
law. What is left is recorded with one coordinate per independent cycle.

* ``ResidualProjector`` handles one oriented cycle (mean circulation is the
  harmonic part, the deviation from it is exact).
* ``GraphResidualProjector`` handles any finite graph: the representative is
  supported on the edges outside a spanning forest, one per independent cycle.

Leaf module: standard library only, loadable by path. AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

Edge = Tuple[str, str]


def _exact(value: object) -> Fraction:
    if isinstance(value, (bool, float)) or not isinstance(value, (int, Fraction)):
        raise ValueError(f"NOT_EXACT: {value!r}")
    return Fraction(value)


def _norm(values: Dict[Edge, Fraction]) -> Fraction:
    return sum((abs(v) for v in values.values()), Fraction(0))


@dataclass(frozen=True)
class XiTiePrecondition:
    """Precondition for using secondary metric Xi as a tie-breaker.

    Requires strict equality on primary diagnostics:
    Phi_{1,A} == Phi_{1,B} and Gamma_{2,A} == Gamma_{2,B}.
    Xi cannot override worsening primary diagnostics.
    """

    phi1_a: Fraction
    gamma2_a: Fraction
    phi1_b: Fraction
    gamma2_b: Fraction

    def __post_init__(self) -> None:
        for name in ("phi1_a", "gamma2_a", "phi1_b", "gamma2_b"):
            value = _exact(getattr(self, name))
            if value < 0:
                raise ValueError("NEGATIVE_DIAGNOSTIC")
            object.__setattr__(self, name, value)

    def is_satisfied(self) -> bool:
        return self.phi1_a == self.phi1_b and self.gamma2_a == self.gamma2_b


@dataclass(frozen=True)
class XiTieBreakCertificate:
    """Certificate of lawful tie-break under primary diagnostic equality."""

    precondition: XiTiePrecondition
    xi_a: Fraction
    xi_b: Fraction
    tie_broken: bool
    winner: Optional[str] = None
    authority_effect: str = "None"


def evaluate_xi_tie_break(
    candidate_a: str,
    phi1_a: object,
    gamma2_a: object,
    xi_a: object,
    candidate_b: str,
    phi1_b: object,
    gamma2_b: object,
    xi_b: object,
) -> XiTieBreakCertificate:
    """Evaluate secondary metric Xi to break ties between candidate_a and candidate_b.

    Enforces the contract invariant: Xi is admissible ONLY under strict primary diagnostic
    equality (Phi_{1,A} == Phi_{1,B} and Gamma_{2,A} == Gamma_{2,B}).
    """
    p1_a, g2_a, x_a = _exact(phi1_a), _exact(gamma2_a), _exact(xi_a)
    p1_b, g2_b, x_b = _exact(phi1_b), _exact(gamma2_b), _exact(xi_b)
    precondition = XiTiePrecondition(p1_a, g2_a, p1_b, g2_b)
    if not precondition.is_satisfied():
        raise ValueError(
            "XI_TIE_PRECONDITION_FAILED: Primary diagnostics are not equal; "
            "Xi cannot override primary worsening."
        )
    if x_b < x_a:
        winner: Optional[str] = candidate_b
        tie_broken = True
    elif x_a < x_b:
        winner = candidate_a
        tie_broken = True
    else:
        winner = None
        tie_broken = False
    return XiTieBreakCertificate(
        precondition=precondition,
        xi_a=x_a,
        xi_b=x_b,
        tie_broken=tie_broken,
        winner=winner,
    )


@dataclass(frozen=True)
class ResidualProjectionReceipt:
    operation: str
    paper_id: str
    raw_norm: Fraction
    exact_norm: Fraction
    residual_norm: Fraction
    exact_component: Dict[Edge, Fraction]
    residual_component: Dict[Edge, Fraction]
    status: str
    cycle_coordinates: Tuple[Fraction, ...] = field(default_factory=tuple)
    authority_effect: str = "None"


def _status(residual_norm: Fraction) -> str:
    return "RESIDUAL_RETAINED" if residual_norm > 0 else "EXACT_TENSION_ONLY"


class ResidualProjector:
    """Projector for a single oriented cycle ``e1 e2 ... ek`` (head of each is tail of next)."""

    def __init__(self, cycle_edges: List[Edge]):
        if not cycle_edges:
            raise ValueError("cycle_edges must be non-empty")
        for (_, head), (tail, _) in zip(cycle_edges, cycle_edges[1:] + cycle_edges[:1]):
            if head != tail:
                raise ValueError(f"NOT_A_CYCLE: {head!r} does not meet {tail!r}")
        if len(cycle_edges) < 2 or len({u for u, _ in cycle_edges}) != len(cycle_edges):
            raise ValueError("NOT_A_SIMPLE_CYCLE: each vertex must occur once")
        self.cycle_edges = tuple(cycle_edges)
        self.k = len(cycle_edges)

    def project(self, defect: Dict[Edge, Fraction]) -> ResidualProjectionReceipt:
        """Split into mean circulation (harmonic, retained) and exact deviation."""
        undeclared = sorted(set(defect) - set(self.cycle_edges))
        if undeclared:
            raise ValueError(f"UNTYPED_DEFECT: {undeclared!r} are not cycle edges")
        values = {e: _exact(defect.get(e, Fraction(0))) for e in self.cycle_edges}
        circulation = sum(values.values(), Fraction(0))
        mean = circulation / self.k
        harmonic = {e: mean for e in self.cycle_edges}
        exact_component = {e: values[e] - mean for e in self.cycle_edges}
        residual_norm = _norm(harmonic)
        return ResidualProjectionReceipt(
            operation="R",
            paper_id="DDC-R",
            raw_norm=_norm(values),
            exact_norm=_norm(exact_component),
            residual_norm=residual_norm,
            exact_component=exact_component,
            residual_component=harmonic,
            status=_status(residual_norm),
            cycle_coordinates=(circulation,),
        )


class GraphResidualProjector:
    """Projector for any finite graph, with one coordinate per independent cycle."""

    def __init__(self, vertices: List[str], edges: List[Edge]):
        if len(set(vertices)) != len(vertices) or len(set(edges)) != len(edges):
            raise ValueError("DUPLICATE_CARRIER: vertices and directed edges must be unique")
        self.vertices = sorted(set(vertices))
        known = set(self.vertices)
        for u, v in edges:
            if u not in known or v not in known or u == v:
                raise ValueError(f"MALFORMED_EDGE: {(u, v)!r}")
        self.edges = tuple(edges)
        self.forest = self._spanning_forest()

    def _spanning_forest(self) -> Tuple[int, ...]:
        adjacency: Dict[str, List[Tuple[str, int]]] = {v: [] for v in self.vertices}
        for index, (u, v) in enumerate(self.edges):
            adjacency[u].append((v, index))
            adjacency[v].append((u, index))
        seen: set = set()
        tree: List[int] = []
        for root in self.vertices:
            if root in seen:
                continue
            seen.add(root)
            queue = [root]
            while queue:
                current = queue.pop(0)
                for neighbour, index in adjacency[current]:
                    if neighbour not in seen:
                        seen.add(neighbour)
                        tree.append(index)
                        queue.append(neighbour)
        return tuple(sorted(tree))

    @property
    def independent_cycles(self) -> int:
        return len(self.edges) - len(self.forest)

    def project(self, defect: Dict[Edge, Fraction]) -> ResidualProjectionReceipt:
        """Subtract the forest potential's coboundary; keep one value per cycle."""
        undeclared = sorted(set(defect) - set(self.edges))
        if undeclared:
            raise ValueError(f"UNTYPED_DEFECT: {undeclared!r} are not carrier edges")
        values = [_exact(defect.get(e, Fraction(0))) for e in self.edges]
        potential: Dict[str, Fraction] = {}
        adjacency: Dict[str, List[Tuple[str, Fraction]]] = {v: [] for v in self.vertices}
        for index in self.forest:
            u, v = self.edges[index]
            adjacency[u].append((v, values[index]))
            adjacency[v].append((u, -values[index]))
        for root in self.vertices:
            if root in potential:
                continue
            potential[root] = Fraction(0)
            queue = [root]
            while queue:
                current = queue.pop(0)
                for neighbour, step in adjacency[current]:
                    if neighbour not in potential:
                        potential[neighbour] = potential[current] + step
                        queue.append(neighbour)
        exact_component = {
            (u, v): potential[v] - potential[u] for (u, v) in self.edges
        }
        residual = {
            e: values[i] - exact_component[e] for i, e in enumerate(self.edges)
        }
        coordinates = tuple(
            residual[self.edges[i]] for i in range(len(self.edges)) if i not in self.forest
        )
        residual_norm = _norm(residual)
        return ResidualProjectionReceipt(
            operation="R",
            paper_id="DDC-R",
            raw_norm=sum((abs(v) for v in values), Fraction(0)),
            exact_norm=_norm(exact_component),
            residual_norm=residual_norm,
            exact_component=exact_component,
            residual_component=residual,
            status=_status(residual_norm),
            cycle_coordinates=coordinates,
        )
