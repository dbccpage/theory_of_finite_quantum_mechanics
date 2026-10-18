from __future__ import annotations
"""Exact finite audits for the RE1--RE5 hierarchy in PO-000 §4.

The previous package stored asserted conclusions in Boolean fields. This
module instead evaluates the five equations on an explicit finite exact
domain and returns counterexamples when a premise fails.
"""


from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, product
from typing import TypeAlias

from sympy import Abs, Basic, Rational, simplify, sqrt

ExactVector: TypeAlias = tuple[Rational, ...]
Point: TypeAlias = Mapping[str, ExactVector]
Gauge: TypeAlias = Callable[[ExactVector], Basic]
Diagnostic: TypeAlias = Callable[[tuple[str, ...], Point], Basic]


@dataclass
class AxiomCounterexample:
    axiom: str
    detail: str


@dataclass
class ReplicaAxiomAudit:
    """Finite exhaustive result over the declared sample grid."""

    checked_points: int
    re1_global_gauge: bool
    re2_local_magnitude_sufficiency: bool
    re3_disjoint_replica_additivity: bool
    re4_edge_exchange_symmetry: bool
    re5_singleton_calibration: bool
    counterexamples: tuple[AxiomCounterexample, ...]


@dataclass
class ReplicaConclusionCertificate:
    """Pointwise exact identity derived from checked RE premises."""

    edge_order: tuple[str, ...]
    diagnostic_value: Basic
    singleton_sum: Basic
    local_gauge_sum: Basic | None
    singleton_decomposition_holds: bool
    singleton_calibration_holds: bool | None
    unweighted_conclusion_holds: bool | None


class FiniteDiagnosticFamily:
    """A diagnostic family, local gauges, and declared edge-type orbits."""

    def __init__(
        self,
        edges: Sequence[str],
        gauges: Mapping[str, Gauge],
        diagnostic: Diagnostic,
        edge_types: Mapping[str, str] | None = None,
    ):
        if not edges:
            raise ValueError("a diagnostic family needs at least one edge")
        if len(set(edges)) != len(edges):
            raise ValueError("edge identifiers must be unique")
        if set(gauges) != set(edges):
            raise ValueError("each edge needs exactly one local gauge")
        self.edges = tuple(edges)
        self.gauges = dict(gauges)
        self.diagnostic = diagnostic
        self.edge_types = {edge: edge for edge in edges} if edge_types is None else dict(edge_types)
        if set(self.edge_types) != set(edges):
            raise ValueError("edge_types must cover exactly the declared edges")

    def evaluate(self, subset: Sequence[str], point: Point) -> Basic:
        ordered = tuple(subset)
        if not set(ordered) <= set(self.edges):
            raise ValueError("diagnostic subset contains an unknown edge")
        if set(point) != set(ordered):
            raise ValueError("point domain must equal the diagnostic subset")
        return simplify(self.diagnostic(ordered, point))

    def _all_points(
        self, ordered_edges: Sequence[str], samples: Mapping[str, Sequence[ExactVector]]
    ) -> tuple[dict[str, ExactVector], ...]:
        return tuple(
            dict(zip(ordered_edges, values, strict=True))
            for values in product(*(samples[edge] for edge in ordered_edges))
        )

    def audit(
        self,
        samples: Mapping[str, Sequence[ExactVector]],
        scalars: Sequence[Rational] = (Rational(0), Rational(1), Rational(2)),
    ) -> ReplicaAxiomAudit:
        """Exhaustively audit RE1--RE5 on a declared finite exact grid."""

        if set(samples) != set(self.edges) or any(not samples[edge] for edge in self.edges):
            raise ValueError("sample grids must be nonempty and cover every edge")
        if not scalars or any(scalar < 0 for scalar in scalars):
            raise ValueError("homogeneity scalars must be nonempty and nonnegative")

        def is_nonnegative(value: Basic) -> bool:
            try:
                return bool(simplify(value) >= 0)
            except TypeError:
                return False

        counters: list[AxiomCounterexample] = []
        full_points = self._all_points(self.edges, samples)

        # RE1: faithful convex gauge (finite checks of codomain, zero,
        # positive homogeneity, and subadditivity on the declared grid).
        re1 = True
        point_values: list[Basic] = []
        zero_point = {edge: tuple(Rational(0) for _ in samples[edge][0]) for edge in self.edges}
        zero_value = self.evaluate(self.edges, zero_point)
        if not is_nonnegative(zero_value):
            re1 = False
            counters.append(
                AxiomCounterexample("RE1", f"codomain violation at zero: J={zero_value}")
            )
        elif zero_value != 0:
            re1 = False
            counters.append(AxiomCounterexample("RE1", "J(0) != 0"))

        if re1:
            for point in full_points:
                value = self.evaluate(self.edges, point)
                if not is_nonnegative(value):
                    re1 = False
                    counters.append(
                        AxiomCounterexample("RE1", f"codomain violation J={value} at {point}")
                    )
                    break
                point_values.append(value)
                is_zero_point = point == zero_point
                if (value == 0) != is_zero_point:
                    re1 = False
                    counters.append(AxiomCounterexample("RE1", f"faithfulness failed at {point}"))
                    break
                for scalar in scalars:
                    scaled = {
                        edge: tuple(scalar * coordinate for coordinate in point[edge])
                        for edge in self.edges
                    }
                    scaled_value = self.evaluate(self.edges, scaled)
                    if not is_nonnegative(scaled_value):
                        re1 = False
                        counters.append(
                            AxiomCounterexample(
                                "RE1",
                                f"codomain violation J={scaled_value} at scaled "
                                f"point {point}, lambda={scalar}",
                            )
                        )
                        break
                    if simplify(scaled_value - scalar * value) != 0:
                        re1 = False
                        counters.append(
                            AxiomCounterexample(
                                "RE1",
                                f"positive homogeneity failed at {point}, lambda={scalar}",
                            )
                        )
                        break
                if not re1:
                    break

        if re1:
            for left_index, left in enumerate(full_points):
                left_value = point_values[left_index]
                for right_index, right in enumerate(full_points):
                    right_value = point_values[right_index]
                    summed = {
                        edge: tuple(a + b for a, b in zip(left[edge], right[edge], strict=True))
                        for edge in self.edges
                    }
                    lhs = self.evaluate(self.edges, summed)
                    if not is_nonnegative(lhs):
                        re1 = False
                        counters.append(
                            AxiomCounterexample(
                                "RE1", f"codomain violation J={lhs} at sum {left}+{right}"
                            )
                        )
                        break
                    rhs = left_value + right_value
                    if bool(simplify(lhs - rhs) > 0):
                        re1 = False
                        counters.append(
                            AxiomCounterexample("RE1", f"subadditivity failed at {left}, {right}")
                        )
                        break
                if not re1:
                    break

        # RE2: points with equal local magnitudes have equal diagnostics.
        re2 = True
        for left, right in combinations(full_points, 2):
            left_magnitudes = tuple(simplify(self.gauges[edge](left[edge])) for edge in self.edges)
            right_magnitudes = tuple(
                simplify(self.gauges[edge](right[edge])) for edge in self.edges
            )
            if (
                left_magnitudes == right_magnitudes
                and simplify(self.evaluate(self.edges, left) - self.evaluate(self.edges, right))
                != 0
            ):
                re2 = False
                counters.append(
                    AxiomCounterexample("RE2", f"equal magnitudes differed at {left}, {right}")
                )
                break

        # RE3: every unique nontrivial bipartition of every declared union.
        # Requiring the union's first edge on the left removes only the
        # duplicate obtained by swapping the two disjoint parts.
        re3 = True
        for union_size in range(2, len(self.edges) + 1):
            for union_edges in combinations(self.edges, union_size):
                union_points = self._all_points(union_edges, samples)
                anchor = union_edges[0]
                for left_size in range(1, len(union_edges)):
                    for left_edges in combinations(union_edges, left_size):
                        if anchor not in left_edges:
                            continue
                        right_edges = tuple(edge for edge in union_edges if edge not in left_edges)
                        for point in union_points:
                            left_point = {edge: point[edge] for edge in left_edges}
                            right_point = {edge: point[edge] for edge in right_edges}
                            defect = simplify(
                                self.evaluate(union_edges, point)
                                - self.evaluate(left_edges, left_point)
                                - self.evaluate(right_edges, right_point)
                            )
                            if defect != 0:
                                re3 = False
                                counters.append(
                                    AxiomCounterexample(
                                        "RE3",
                                        f"disjoint additivity defect {defect} on "
                                        f"union {union_edges} for "
                                        f"{left_edges}|{right_edges}",
                                    )
                                )
                                break
                        if not re3:
                            break
                    if not re3:
                        break
                if not re3:
                    break
            if not re3:
                break

        # RE4: pairwise swaps inside a declared type orbit.
        re4 = True
        for i, left_edge in enumerate(self.edges):
            for right_edge in self.edges[i + 1 :]:
                if self.edge_types[left_edge] != self.edge_types[right_edge]:
                    continue
                for point in full_points:
                    swapped = dict(point)
                    swapped[left_edge], swapped[right_edge] = (
                        point[right_edge],
                        point[left_edge],
                    )
                    if (
                        simplify(
                            self.evaluate(self.edges, point) - self.evaluate(self.edges, swapped)
                        )
                        != 0
                    ):
                        re4 = False
                        counters.append(
                            AxiomCounterexample(
                                "RE4", f"type-preserving swap {left_edge}<->{right_edge} failed"
                            )
                        )
                        break
                if not re4:
                    break
            if not re4:
                break

        # RE5: exact singleton calibration.
        re5 = True
        for edge in self.edges:
            for value in samples[edge]:
                diagnostic_value = self.evaluate((edge,), {edge: value})
                gauge_value = simplify(self.gauges[edge](value))
                if simplify(diagnostic_value - gauge_value) != 0:
                    re5 = False
                    counters.append(
                        AxiomCounterexample(
                            "RE5",
                            f"singleton {edge} has J={diagnostic_value}, j={gauge_value}",
                        )
                    )
                    break
            if not re5:
                break

        return ReplicaAxiomAudit(
            checked_points=len(full_points),
            re1_global_gauge=re1,
            re2_local_magnitude_sufficiency=re2,
            re3_disjoint_replica_additivity=re3,
            re4_edge_exchange_symmetry=re4,
            re5_singleton_calibration=re5,
            counterexamples=tuple(counters),
        )

    def conclusion_certificate(self, point: Point) -> ReplicaConclusionCertificate:
        """Recompute the RE3 and RE3+RE5 conclusions at one exact point."""

        if set(point) != set(self.edges):
            raise ValueError("point must cover the full edge family")
        diagnostic_value = self.evaluate(self.edges, point)
        singleton_values = tuple(self.evaluate((edge,), {edge: point[edge]}) for edge in self.edges)
        singleton_sum = simplify(sum(singleton_values))
        local_sum = simplify(sum(self.gauges[edge](point[edge]) for edge in self.edges))
        calibration = all(
            simplify(singleton - self.gauges[edge](point[edge])) == 0
            for edge, singleton in zip(self.edges, singleton_values, strict=True)
        )
        decomposition = simplify(diagnostic_value - singleton_sum) == 0
        return ReplicaConclusionCertificate(
            edge_order=self.edges,
            diagnostic_value=diagnostic_value,
            singleton_sum=singleton_sum,
            local_gauge_sum=local_sum,
            singleton_decomposition_holds=decomposition,
            singleton_calibration_holds=calibration,
            unweighted_conclusion_holds=decomposition
            and calibration
            and simplify(diagnostic_value - local_sum) == 0,
        )


def absolute_gauge(vector: ExactVector) -> Basic:
    """One-dimensional faithful local gauge used by exact fixtures."""

    if len(vector) != 1:
        raise ValueError("absolute_gauge expects one coordinate")
    return Abs(vector[0])


def unweighted_l1_diagnostic(edges: tuple[str, ...], point: Point) -> Basic:
    return simplify(sum(absolute_gauge(point[edge]) for edge in edges))


def weighted_l1_diagnostic(weights: Mapping[str, Rational]) -> Diagnostic:
    if any(weight <= 0 for weight in weights.values()):
        raise ValueError("weights must be strictly positive")

    def evaluate(edges: tuple[str, ...], point: Point) -> Basic:
        missing = set(edges) - set(weights)
        if missing:
            raise ValueError(f"missing weights for {sorted(missing)}")
        return simplify(sum(weights[edge] * absolute_gauge(point[edge]) for edge in edges))

    return evaluate


def lp_counterexample_diagnostic(edges: tuple[str, ...], point: Point) -> Basic:
    """The exact ``p=2`` drop-RE3 countermodel from §4.5."""

    return sqrt(sum(absolute_gauge(point[edge]) ** 2 for edge in edges))


def scaled_sum_counterexample(scale: Rational) -> Diagnostic:
    """The exact drop-RE5 countermodel ``c * sum j_e``."""

    if scale <= 0 or scale == 1:
        raise ValueError("the RE5 countermodel needs c>0 and c!=1")

    def evaluate(edges: tuple[str, ...], point: Point) -> Basic:
        return simplify(scale * unweighted_l1_diagnostic(edges, point))

    return evaluate



