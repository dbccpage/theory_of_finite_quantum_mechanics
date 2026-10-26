"""Exact finite quotient sections, sign switching, and signed-sum diagnostics.

AuthorityEffect: None.
The rational section is a normal form modulo im(d0), not an L1 minimizer.
The switching section is a normal form for diagonal +/-1 gauges on a fixed
ordered, labelled graph. Neither is a general solution of the sign problem.
Legacy finite float inputs denote their exact binary rational values; use
Fraction or rational strings when a decimal/rational value is intended.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from itertools import combinations
from math import comb, isfinite
from typing import Any, Dict, List, Optional, Tuple


def exact_rational(value: Any) -> Fraction:
    """Convert without tolerance or rounded equality; reject booleans/NaN/inf."""
    if isinstance(value, bool):
        raise ValueError("Boolean is not a rational coefficient")
    if isinstance(value, float):
        if not isfinite(value):
            raise ValueError("Non-finite coefficient")
        return Fraction.from_float(value)
    if not isinstance(value, (int, Fraction, str)):
        raise ValueError("Expected integer, Fraction, rational string, or finite legacy float")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("Invalid rational coefficient") from exc


def _dot(left, right):
    total = Fraction(0)
    for x, y in zip(left, right):
        total += x * y
    return total


def _rref(rows, width):
    """RREF with a row-operation witness; leftmost pivots, first available row."""
    result = [list(row) for row in rows]
    transform = [[Fraction(i == j) for j in range(len(rows))] for i in range(len(rows))]
    pivots = []
    rank = 0
    for column in range(width):
        pivot = next((i for i in range(rank, len(result)) if result[i][column]), None)
        if pivot is None:
            continue
        result[rank], result[pivot] = result[pivot], result[rank]
        transform[rank], transform[pivot] = transform[pivot], transform[rank]
        scale = result[rank][column]
        result[rank] = [x / scale for x in result[rank]]
        transform[rank] = [x / scale for x in transform[rank]]
        for i in range(len(result)):
            if i == rank:
                continue
            scale = result[i][column]
            result[i] = [x - scale * y for x, y in zip(result[i], result[rank])]
            transform[i] = [x - scale * y for x, y in zip(transform[i], transform[rank])]
        pivots.append(column)
        rank += 1
        if rank == len(result):
            break
    return result[:rank], transform[:rank], tuple(pivots)


class TerminalRoute(str, Enum):
    EXACT_REPAIR = "ExactRepair"
    EXACT_CANCELLATION = "ExactCancellation"
    STABILIZED_SURVIVOR = "StabilizedSurvivor"
    OPEN_SIGN_OBSTRUCTION = "OpenSignObstruction"
    REFUSED = "Refused"


@dataclass
class CochainComplex:
    """Finite rational complex, with dimensions and d1*d0 checked exactly."""
    dim_c0: int
    dim_c1: int
    dim_c2: int
    d0: List[List[Fraction]]
    d1: List[List[Fraction]]

    def __post_init__(self):
        for dim in (self.dim_c0, self.dim_c1, self.dim_c2):
            if type(dim) is not int or dim < 0:
                raise ValueError("Dimensions must be nonnegative integers")
        for name, height, width in (("d0", self.dim_c1, self.dim_c0), ("d1", self.dim_c2, self.dim_c1)):
            matrix = getattr(self, name)
            if len(matrix) != height or any(len(row) != width for row in matrix):
                raise ValueError(f"{name} dimension mismatch")
            setattr(self, name, [[exact_rational(x) for x in row] for row in matrix])

    def check_nilpotence(self, tol=None) -> bool:
        """The compatibility tolerance argument has no effect on exact equality."""
        return all(
            _dot(row, [self.d0[k][j] for k in range(self.dim_c1)]) == 0
            for row in self.d1 for j in range(self.dim_c0)
        )


@dataclass(frozen=True)
class QuotientNormalForm:
    representative: Tuple[Fraction, ...]
    gauge: Tuple[Fraction, ...]
    pivot_coordinates: Tuple[int, ...]


@dataclass
class InvolutionWitness:
    mapping: Dict[int, int]
    is_valid: bool
    description: str


@dataclass(frozen=True)
class SignSwitchingNormalForm:
    parities: Tuple[int, ...]
    gauge: Tuple[int, ...]
    forest_edges: Tuple[int, ...]
    obstruction_cycles: Tuple[Tuple[int, ...], ...]


def normalize_sign_cochain(vertex_count, edges, parities) -> SignSwitchingNormalForm:
    """Normalize F2 edge signs modulo vertex switching on a fixed ordered graph.

    Parallel edges, loops, disconnected graphs and isolated vertices are admitted.
    Forest edges are chosen by scanning the declared edge order. Each component
    is rooted at its least vertex with gauge zero. Nonzero chord coordinates
    carry explicit odd-parity fundamental cycles. Complexity is polynomial in
    this explicitly supplied graph, which may itself be exponentially large.
    """
    if type(vertex_count) is not int or vertex_count < 0:
        raise ValueError("Invalid vertex count")
    edges = tuple(tuple(edge) for edge in edges)
    parities = tuple(parities)
    if len(edges) != len(parities) or any(type(s) is not int or s not in (0, 1) for s in parities):
        raise ValueError("Expected one integer parity in {0,1} per edge")
    if any(len(edge) != 2 or any(type(v) is not int or not 0 <= v < vertex_count for v in edge) for edge in edges):
        raise ValueError("Invalid graph endpoint")
    parents = list(range(vertex_count))

    def root(v):
        while parents[v] != v:
            parents[v] = parents[parents[v]]
            v = parents[v]
        return v

    adjacency = [[] for _ in range(vertex_count)]
    forest = []
    for i, (u, v) in enumerate(edges):
        ru, rv = root(u), root(v)
        if ru != rv:
            parents[rv] = ru
            forest.append(i)
            adjacency[u].append((v, i))
            adjacency[v].append((u, i))
    gauge = [None] * vertex_count
    paths = [()] * vertex_count
    for start in range(vertex_count):
        if gauge[start] is not None:
            continue
        gauge[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v, i in adjacency[u]:
                if gauge[v] is None:
                    gauge[v] = gauge[u] ^ parities[i]
                    paths[v] = paths[u] + (i,)
                    queue.append(v)
    normal = tuple(s ^ gauge[u] ^ gauge[v] for s, (u, v) in zip(parities, edges))
    cycles = []
    for i, ((u, v), bit) in enumerate(zip(edges, normal)):
        if bit:
            cycles.append(tuple(sorted(set(paths[u]) ^ set(paths[v]) ^ {i})))
    return SignSwitchingNormalForm(normal, tuple(gauge), tuple(forest), tuple(cycles))


class BQNFSignEvaluator:
    """Exact quotient section plus separately scoped finite diagnostics."""
    def __init__(self, complex_data: CochainComplex):
        self.complex = complex_data
        if not self.complex.check_nilpotence():
            raise ValueError("Invalid cochain complex: d1 . d0 != 0")
        columns = [[row[j] for row in self.complex.d0] for j in range(self.complex.dim_c0)]
        self._basis, self._transport, self._pivots = _rref(columns, self.complex.dim_c1)

    def _vector(self, values):
        if len(values) != self.complex.dim_c1:
            raise ValueError("Cochain dimension mismatch")
        return [exact_rational(x) for x in values]

    def compute_l1_norm(self, vec):
        total = Fraction(0)
        for value in vec:
            total += abs(exact_rational(value))
        return total

    def normalize_cochain(self, c1) -> QuotientNormalForm:
        """Unique representative with the RREF pivot coordinates set to zero.

        Equivalence is c~c' iff c-c' belongs to im(d0), with fixed ambient
        coordinate order. The returned gauge witnesses c - N(c) = d0*gauge.
        Its L1 norm is generally NOT the quotient L1 distance.
        """
        residual = self._vector(c1)
        gauge = [Fraction(0)] * self.complex.dim_c0
        for basis, transport, pivot in zip(self._basis, self._transport, self._pivots):
            coefficient = residual[pivot]
            residual = [x - coefficient * y for x, y in zip(residual, basis)]
            gauge = [x + coefficient * y for x, y in zip(gauge, transport)]
        return QuotientNormalForm(tuple(residual), tuple(gauge), self._pivots)

    def solve_quotient_distance(self, c1, max_iters=None, step_size=None, *, max_candidates=100_000):
        """Exact finite L1 minimization by vertices of the residual arrangement.

        Enumerates at most binomial(dim C1, rank d0) candidate sets, refusing
        above max_candidates. This is a bounded reference solver, not a claim
        of polynomial complexity. Legacy descent parameters are ignored.
        """
        values = self._vector(c1)
        rank = len(self._basis)
        if type(max_candidates) is not int or max_candidates < 1:
            raise ValueError("max_candidates must be a positive integer")
        if comb(len(values), rank) > max_candidates:
            raise RuntimeError("Exact quotient-distance candidate budget exceeded")
        best = None
        for active in combinations(range(len(values)), rank):
            augmented = [[self._basis[j][i] for j in range(rank)] + [values[i]] for i in active]
            rows, _, pivots = _rref(augmented, rank)
            if len(pivots) != rank:
                continue
            coefficients = [row[-1] for row in rows]
            residual = tuple(values[i] - _dot(coefficients, [basis[i] for basis in self._basis]) for i in range(len(values)))
            score = self.compute_l1_norm(residual)
            if best is None or (score, residual) < best[:2]:
                gauge = tuple(_dot(coefficients, [row[j] for row in self._transport]) for j in range(self.complex.dim_c0))
                best = (score, residual, gauge)
        if best is None:
            raise ArithmeticError("No full-rank residual vertex found")
        return best[0], list(best[2])

    def search_meron_involution(self, path_weights, signs, tol=None) -> Optional[InvolutionWitness]:
        """Exact equal-weight pairing on supplied active rows, not cluster discovery.

        A successful result certifies cancellation of this finite signed sum.
        It does not establish physical meron-cluster factorization or efficiency.
        """
        if len(path_weights) != len(signs) or any(type(s) is not int or s not in (-1, 1) for s in signs):
            raise ValueError("Expected one sign in {-1,+1} per weight")
        weights = [exact_rational(x) for x in path_weights]
        if any(w < 0 for w in weights):
            raise ValueError("Path magnitudes must be nonnegative")
        buckets = defaultdict(lambda: ([], []))
        for i, (weight, sign) in enumerate(zip(weights, signs)):
            if weight:
                buckets[weight][0 if sign == 1 else 1].append(i)
        mapping = {}
        for positive, negative in buckets.values():
            if len(positive) != len(negative):
                return None
            for i, j in zip(positive, negative):
                mapping[i], mapping[j] = j, i
        return InvolutionWitness(mapping, True, "Exact equal-weight opposite-sign pairing of supplied active rows")

    def evaluate_sign_packet(self, c1_defect, path_signs, tol=None, *, max_candidates=100_000):
        """Route exact finite cochain evidence; tolerance never implies exactness.

        The legacy API uses abs(c1_defect) as the supplied path magnitudes.
        Rational additive boundaries are not automatically physical sign gauges.
        A physical identification must be supplied by the model separately.
        """
        try:
            values = self._vector(c1_defect)
            if len(path_signs) != len(values) or any(type(s) is not int or s not in (-1, 1) for s in path_signs):
                raise ValueError("Invalid path sign vector")
            normal = self.normalize_cochain(values)
        except (ValueError, TypeError) as exc:
            return {"route": TerminalRoute.REFUSED, "reason": str(exc)}
        gamma = self.compute_l1_norm([_dot(row, values) for row in self.complex.d1])
        try:
            phi, best_gauge = self.solve_quotient_distance(values, max_candidates=max_candidates)
            distance_status = "exact"
        except RuntimeError:
            phi, best_gauge = None, None
            distance_status = "budget_unknown"
        result = {"phi_1_residual": phi, "gamma_2_closure": gamma,
                  "quotient_representative": normal.representative,
                  "normalization_gauge": normal.gauge, "optimal_gauge": best_gauge,
                  "distance_status": distance_status,
                  "claim_scope": "finite rational cochain and supplied signed rows; no automatic physical sign-gauge identification"}
        if not any(normal.representative):
            result.update(route=TerminalRoute.EXACT_REPAIR, witness="Exact rational boundary witness d0*alpha = c1")
            result["phi_1_residual"] = Fraction(0)
            result["distance_status"] = "exact"
            return result
        involution = self.search_meron_involution([abs(x) for x in values], path_signs)
        if involution is not None:
            result.update(route=TerminalRoute.EXACT_CANCELLATION, witness=involution.description,
                          pairing=involution.mapping, pair_count=len(involution.mapping) // 2)
        elif gamma == 0:
            result.update(route=TerminalRoute.STABILIZED_SURVIVOR,
                          witness="Exactly closed, nonzero rational quotient class; variance unclassified")
        else:
            result.update(route=TerminalRoute.OPEN_SIGN_OBSTRUCTION,
                          witness="Nonzero rational closure defect; no equal-weight row pairing")
        return result
