"""Finite oriented simplicial complexes, exact coboundaries, and torsion witnesses.

Ranks are computed by exact Gaussian elimination over Q or over F_p.  The
six-vertex RP^2 witness shows that a rational-coefficient calculation reports
H^2 = 0 while the F_2 calculation reports a one-dimensional H^2.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import isqrt
from typing import Callable, Hashable, Mapping, Sequence

from .cochains import Edge, FiniteComplex, Vertex, _edge_value, _validate_cochain, d0
from .exact import as_fraction, exact_row, l1
from .obstruction import (
    DiagnosticClass,
    MatrixQuotientCertificate,
    classify_signature,
    d0_adjoint,
    matrix_product,
    matrix_quotient_l1,
)
from .outcomes import Accepted, Outcome, RefusalCode, Refused
from .native_functionals import closure

Simplex = tuple[Hashable, ...]
Matrix = tuple[tuple[Fraction, ...], ...]
ExactScalar = int | str | Fraction


def _complex_problem(vertices: object, simplices: object) -> str | None:
    if type(vertices) is not tuple or type(simplices) is not tuple:
        return "vertices and simplices must be immutable tuples"
    if len(set(vertices)) != len(vertices):
        return "vertices must be unique"
    order = {vertex: index for index, vertex in enumerate(vertices)}
    for simplex in simplices:
        if type(simplex) is not tuple or not simplex or any(vertex not in order for vertex in simplex):
            return f"simplex {simplex!r} is not a nonempty tuple of carrier vertices"
        if len(set(simplex)) != len(simplex):
            return f"simplex {simplex!r} is degenerate"
        if [order[vertex] for vertex in simplex] != sorted(order[vertex] for vertex in simplex):
            return f"simplex {simplex!r} is not stored in vertex order"
    declared = set(simplices)
    if len(declared) != len(simplices):
        return "simplices must not repeat"
    if any((vertex,) not in declared for vertex in vertices):
        return "every vertex must be a declared 0-simplex"
    for simplex in simplices:
        faces = (simplex[:index] + simplex[index + 1 :] for index in range(len(simplex)))
        if len(simplex) > 1 and any(face not in declared for face in faces):
            return f"simplex {simplex!r} is missing a face: not downward closed"
    return None


@dataclass(frozen=True)
class OrientedSimplicialComplex:
    """Vertices in a declared total order; simplices stored as order-sorted tuples."""

    vertices: tuple[Hashable, ...]
    simplices: tuple[Simplex, ...]

    def __post_init__(self) -> None:
        problem = _complex_problem(self.vertices, self.simplices)
        if problem is not None:
            raise ValueError(problem)

    @property
    def dimension(self) -> int:
        return max((len(simplex) - 1 for simplex in self.simplices), default=-1)

    def k_simplices(self, k: int) -> tuple[Simplex, ...]:
        order = {vertex: index for index, vertex in enumerate(self.vertices)}
        chosen = (simplex for simplex in self.simplices if len(simplex) == k + 1)
        return tuple(sorted(chosen, key=lambda simplex: tuple(order[vertex] for vertex in simplex)))

    def coboundary_matrix(self, k: int) -> Matrix:
        """delta^k: rows are (k+1)-simplices, columns are k-simplices."""

        if type(k) is not int or k < 0:
            raise ValueError("coboundary degree must be a non-negative integer")
        columns = self.k_simplices(k)
        position = {simplex: index for index, simplex in enumerate(columns)}
        rows = []
        for simplex in self.k_simplices(k + 1):
            row = [Fraction(0)] * len(columns)
            for index in range(len(simplex)):
                row[position[simplex[:index] + simplex[index + 1 :]]] += (-1) ** index
            rows.append(tuple(row))
        return tuple(rows)

    def verify_nilpotence(self) -> Outcome[int]:
        """Check delta^{k+1} delta^k = 0 for every k; return the number of checked pairs."""

        checked = 0
        for k in range(max(self.dimension - 1, 0)):
            product = matrix_product(
                self.coboundary_matrix(k + 1), self.coboundary_matrix(k), len(self.k_simplices(k))
            )
            if any(entry != 0 for row in product for entry in row):
                return Refused(RefusalCode.CERTIFICATE_MISMATCH, f"delta^{k + 1} delta^{k} is not zero")
            checked += 1
        return Accepted(checked)

    def betti_numbers(self, field: str | int = "Q") -> Outcome[tuple[int, ...]]:
        """dim H^k = n_k - rank delta^k - rank delta^(k-1) over Q or F_p."""

        rank = _field_rank(field)
        if rank is None:
            return Refused(RefusalCode.INVALID_INPUT, "field must be 'Q' or a prime integer p")
        ranks = [rank(self.coboundary_matrix(k)) for k in range(self.dimension + 1)]
        return Accepted(
            tuple(
                len(self.k_simplices(k)) - ranks[k] - (ranks[k - 1] if k else 0)
                for k in range(self.dimension + 1)
            )
        )

    def degree_k_signature(self, k: int, cochain: Mapping[Simplex, ExactScalar]) -> Outcome[DegreeSignature]:
        """(Phi_k, Gamma_{k+1}, ||delta^k||_{1->1}) with an exact quotient certificate."""

        if type(k) is not int or not 0 <= k <= self.dimension:
            return Refused(RefusalCode.OUTSIDE_CARRIER, f"degree {k!r} is outside the complex")
        simplices = self.k_simplices(k)
        if not isinstance(cochain, Mapping) or set(cochain) != set(simplices):
            return Refused(RefusalCode.INVALID_INPUT, "cochain must define every k-simplex exactly once")
        lower = self.coboundary_matrix(k - 1) if k else tuple(() for _ in simplices)
        solved = matrix_quotient_l1(
            lower, tuple(cochain[simplex] for simplex in simplices), columns=len(self.k_simplices(k - 1))
        )
        if isinstance(solved, Refused):
            return solved
        cert = solved.value
        upper = self.coboundary_matrix(k)
        gamma = closure(lower, cert.columns, upper, cert.delta)
        norm = max((l1(column) for column in zip(*upper)), default=Fraction(0))
        if gamma > norm * cert.value:
            return Refused(RefusalCode.CERTIFICATE_MISMATCH, "Gamma_{k+1} exceeds ||delta^k|| Phi_k")
        ratio = None if cert.value == 0 else gamma / cert.value
        return Accepted(
            DegreeSignature(k, cert.value, gamma, ratio, norm, classify_signature(cert.value, gamma), cert)
        )


@dataclass(frozen=True)
class DegreeSignature:
    degree: int
    phi: Fraction
    gamma: Fraction
    closure_ratio: Fraction | None
    opnorm: Fraction
    diagnostic_class: DiagnosticClass
    certificate: MatrixQuotientCertificate


def make_simplicial_complex(
    vertices: tuple[Hashable, ...],
    simplices: Sequence[Sequence[Hashable]],
) -> Outcome[OrientedSimplicialComplex]:
    """Sort each declared simplex by the vertex order, then validate it."""

    if type(vertices) is not tuple or len(set(vertices)) != len(vertices):
        return Refused(RefusalCode.INVALID_INPUT, "vertices must be a unique immutable tuple")
    order = {vertex: index for index, vertex in enumerate(vertices)}
    stored = []
    for simplex in simplices:
        if isinstance(simplex, (str, bytes)) or not isinstance(simplex, Sequence):
            return Refused(RefusalCode.INVALID_INPUT, f"simplex {simplex!r} must be a sequence of vertices")
        if any(vertex not in order for vertex in simplex):
            return Refused(RefusalCode.OUTSIDE_CARRIER, f"simplex {tuple(simplex)!r} leaves the carrier")
        stored.append(tuple(sorted(simplex, key=order.__getitem__)))
    problem = _complex_problem(vertices, tuple(stored))
    if problem is not None:
        return Refused(RefusalCode.INVALID_INPUT, problem)
    return Accepted(OrientedSimplicialComplex(vertices, tuple(stored)))


def from_facets(
    vertices: tuple[Hashable, ...],
    facets: Sequence[Sequence[Hashable]],
) -> Outcome[OrientedSimplicialComplex]:
    """The downward closure of declared facets, plus every vertex."""

    closure: set[frozenset[Hashable]] = {frozenset((vertex,)) for vertex in vertices}
    for facet in facets:
        if isinstance(facet, (str, bytes)) or not isinstance(facet, Sequence):
            return Refused(RefusalCode.INVALID_INPUT, f"facet {facet!r} must be a sequence of vertices")
        if len(set(facet)) != len(facet):
            return Refused(RefusalCode.INVALID_INPUT, f"facet {tuple(facet)!r} is degenerate")
        for size in range(1, len(facet) + 1):
            closure.update(frozenset(face) for face in combinations(facet, size))
    return make_simplicial_complex(vertices, tuple(tuple(face) for face in closure))


def _rectangular(rows: list[list[object]]) -> int:
    widths = {len(row) for row in rows}
    if len(widths) > 1:
        raise ValueError("matrix rows must have equal length")
    return widths.pop() if widths else 0


def _rank(rows: list[list], inverse: Callable, reduce: Callable) -> int:  # type: ignore[type-arg]
    width = _rectangular(rows)
    rank = 0
    for column in range(width):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column] != 0), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = inverse(rows[rank][column])
        for r in range(rank + 1, len(rows)):
            factor = rows[r][column] * scale
            rows[r] = [reduce(a - factor * b) for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def rank_rational(matrix: Sequence[Sequence[ExactScalar]]) -> int:
    """Exact rank over Q; floats and bools are refused by ``as_fraction``."""

    if isinstance(matrix, (str, bytes)):
        raise TypeError("a matrix is a sequence of rows, not a string")
    return _rank([list(exact_row(row)) for row in matrix], lambda x: 1 / x, lambda x: x)


def _is_prime(p: object) -> bool:
    return type(p) is int and p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def rank_mod_p(matrix: Sequence[Sequence[ExactScalar]], p: int) -> int:
    """Exact rank over F_p of a p-integral rational matrix."""

    if not _is_prime(p):
        raise ValueError("p must be a prime integer")
    rows = []
    for row in matrix:
        converted = []
        for value in row:
            exact = as_fraction(value)
            if exact.denominator % p == 0:
                raise ValueError(f"entry {exact} is not p-integral for p={p}")
            converted.append(exact.numerator * pow(exact.denominator, -1, p) % p)
        rows.append(converted)
    return _rank(rows, lambda x: pow(x, -1, p), lambda x: x % p)


def _field_rank(field: object) -> Callable[[Matrix], int] | None:
    if field == "Q" and type(field) is str:
        return rank_rational
    if _is_prime(field):
        return lambda matrix: rank_mod_p(matrix, field)  # type: ignore[arg-type]
    return None


RP2_FACETS = (
    (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 1, 5),
    (1, 2, 4), (2, 3, 5), (1, 3, 4), (2, 4, 5), (1, 3, 5),
)
RP2_TORSION_EDGES = ((1, 3), (1, 4), (2, 4), (2, 5), (3, 5))


def rp2_six_vertex() -> OrientedSimplicialComplex:
    """The ten-triangle six-vertex triangulation of the real projective plane."""

    simplices = {(vertex,) for vertex in range(6)}
    for facet in RP2_FACETS:
        simplices.update(combinations(facet, 2))
        simplices.add(facet)
    return OrientedSimplicialComplex(tuple(range(6)), tuple(sorted(simplices, key=lambda s: (len(s), s))))


@dataclass(frozen=True)
class RP2TorsionRecord:
    face_counts: tuple[int, int, int]
    euler_characteristic: int
    nilpotent_pairs: int
    rank_delta0_q: int
    rank_delta1_q: int
    rank_delta0_f2: int
    rank_delta1_f2: int
    h2_q: int
    h2_f2: int
    h1_f2: int
    torsion_cocycle: tuple[int, ...]
    integral_coboundary: tuple[int, ...]
    bockstein_nonzero: bool
    triangle_class_rationally_exact: bool
    triangle_class_nonzero_mod2: bool
    rational_solver_misses_torsion: bool


def _with_column(matrix: Matrix, column: Sequence[int]) -> Matrix:
    return tuple(row + (Fraction(value),) for row, value in zip(matrix, column))


def rp2_torsion_witness() -> Outcome[RP2TorsionRecord]:
    """H^2(RP^2; Q) = 0 but H^2(RP^2; F_2) = F_2, with a chain-level Bockstein check."""

    complex_ = rp2_six_vertex()
    nilpotent = complex_.verify_nilpotence()
    if isinstance(nilpotent, Refused):
        return nilpotent
    counts = tuple(len(complex_.k_simplices(k)) for k in range(3))
    delta0, delta1 = complex_.coboundary_matrix(0), complex_.coboundary_matrix(1)
    rank0_q, rank1_q = rank_rational(delta0), rank_rational(delta1)
    rank0_f2, rank1_f2 = rank_mod_p(delta0, 2), rank_mod_p(delta1, 2)
    edges = complex_.k_simplices(1)
    cocycle = tuple(int(edge in RP2_TORSION_EDGES) for edge in edges)
    lifted = tuple(int(sum(a * b for a, b in zip(row, cocycle))) for row in delta1)
    bockstein = tuple((value // 2) % 2 for value in lifted)
    cocycle_mod2 = all(value % 2 == 0 for value in lifted)
    not_coboundary = rank_mod_p(_with_column(delta0, cocycle), 2) > rank0_f2
    class_nonzero = rank_mod_p(_with_column(delta1, bockstein), 2) > rank1_f2
    triangle = (1,) + (0,) * (counts[2] - 1)
    rationally_exact = rank_rational(_with_column(delta1, triangle)) == rank1_q
    nonzero_mod2 = rank_mod_p(_with_column(delta1, triangle), 2) > rank1_f2
    h2_q, h2_f2 = counts[2] - rank1_q, counts[2] - rank1_f2
    return Accepted(
        RP2TorsionRecord(
            (counts[0], counts[1], counts[2]),
            counts[0] - counts[1] + counts[2],
            nilpotent.value,
            rank0_q,
            rank1_q,
            rank0_f2,
            rank1_f2,
            h2_q,
            h2_f2,
            counts[1] - rank1_f2 - rank0_f2,
            cocycle,
            lifted,
            cocycle_mod2 and not_coboundary and any(lifted) and class_nonzero,
            rationally_exact,
            nonzero_mod2,
            h2_q == 0 and h2_f2 == 1 and rationally_exact and nonzero_mod2,
        )
    )


def tetrahedron() -> OrientedSimplicialComplex:
    """The full 3-simplex on vertices 0 < 1 < 2 < 3."""

    vertices = (0, 1, 2, 3)
    simplices = tuple(face for size in range(1, 5) for face in combinations(vertices, size))
    return OrientedSimplicialComplex(vertices, simplices)


@dataclass(frozen=True)
class BianchiRecord:
    curvature: tuple[Fraction, ...]
    curvature_coboundary: tuple[Fraction, ...]


def bianchi_identity(
    complex_: OrientedSimplicialComplex,
    connection: Mapping[Simplex, ExactScalar],
) -> Outcome[BianchiRecord]:
    """F = delta^1 A and delta^2 F; the second vanishes by nilpotence."""

    if not isinstance(complex_, OrientedSimplicialComplex) or complex_.dimension < 2:
        return Refused(RefusalCode.INVALID_INPUT, "the Bianchi check needs a complex of dimension >= 2")
    edges = complex_.k_simplices(1)
    if not isinstance(connection, Mapping) or set(connection) != set(edges):
        return Refused(RefusalCode.INVALID_INPUT, "connection must define every edge exactly once")
    try:
        values = tuple(as_fraction(connection[edge]) for edge in edges)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"connection must be exact: {error}")
    curvature = _apply(complex_.coboundary_matrix(1), values)
    return Accepted(BianchiRecord(curvature, _apply(complex_.coboundary_matrix(2), curvature)))


def _apply(matrix: Matrix, vector: Sequence[Fraction]) -> tuple[Fraction, ...]:
    return tuple(sum((a * b for a, b in zip(row, vector)), start=Fraction(0)) for row in matrix)


def divergence_total(complex_: FiniteComplex, x: Mapping[Edge, ExactScalar]) -> Fraction:
    """sum over v of (d0* x)(v); zero on every finite oriented graph."""

    return sum(d0_adjoint(complex_, x).values(), start=Fraction(0))


def _components(complex_: FiniteComplex) -> list[list[tuple[Vertex, Edge | None]]]:
    """Breadth-first spanning forest: each vertex with the tree edge to its parent."""

    incident: dict[Vertex, list[tuple[Vertex, Edge]]] = {vertex: [] for vertex in complex_.vertices}
    for tail, head in complex_.edges:
        incident[tail].append((head, (tail, head)))
        incident[head].append((tail, (tail, head)))
    seen: set[Vertex] = set()
    forest = []
    for root in complex_.vertices:
        if root in seen:
            continue
        seen.add(root)
        order: list[tuple[Vertex, Edge | None]] = [(root, None)]
        queue: deque[Vertex] = deque([root])
        while queue:
            for neighbour, edge in incident[queue.popleft()]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    order.append((neighbour, edge))
                    queue.append(neighbour)
        forest.append(order)
    return forest


def gauss_law_solvable(
    complex_: FiniteComplex,
    rho: Mapping[Vertex, ExactScalar],
) -> Outcome[dict[Edge, Fraction]]:
    """Solve d0* x = rho exactly; sum(rho) = 0 is necessary on every finite graph."""

    if not isinstance(rho, Mapping) or set(rho) != set(complex_.vertices):
        return Refused(RefusalCode.INVALID_INPUT, "charge must be declared on every vertex exactly once")
    try:
        charge = {vertex: as_fraction(value) for vertex, value in rho.items()}
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"charge must be exact: {error}")
    total = sum(charge.values(), start=Fraction(0))
    if total != 0:
        return Refused(RefusalCode.INFEASIBLE, f"net charge {total} is nonzero, but sum_v (d0* x)(v) = 0 always")
    flow = {edge: Fraction(0) for edge in complex_.edges}
    for component in _components(complex_):
        subtree = {vertex: charge[vertex] for vertex, _ in component}
        for vertex, edge in reversed(component[1:]):
            tail, head = edge  # type: ignore[misc]
            flow[edge] = subtree[vertex] if head == vertex else -subtree[vertex]  # type: ignore[index]
            subtree[tail if head == vertex else head] += subtree[vertex]
        if subtree[component[0][0]] != 0:
            return Refused(RefusalCode.INFEASIBLE, f"component of {component[0][0]!r} has nonzero net charge")
    return Accepted(flow)


@dataclass(frozen=True)
class CyclePairingRecord:
    before: Fraction
    after: Fraction
    invariant: bool


def cycle_pairing_gauge_invariant(
    complex_: FiniteComplex,
    connection: Mapping[Edge, ExactScalar],
    cycle: Mapping[Edge, ExactScalar],
    gauge: Mapping[Vertex, ExactScalar],
) -> Outcome[CyclePairingRecord]:
    """<A, gamma> = <A + d0 lambda, gamma> whenever the chain gamma has zero boundary."""

    try:
        _validate_cochain(complex_, connection)
        field = tuple(_edge_value(connection, *edge) for edge in complex_.edges)
        boundary = d0_adjoint(complex_, cycle)
        chain = tuple(_edge_value(cycle, *edge) for edge in complex_.edges)
        shift = d0(complex_, gauge)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"invalid pairing data: {error}")
    if any(value != 0 for value in boundary.values()):
        return Refused(RefusalCode.NOT_CLOSED, "the chain has nonzero boundary; it is not a cycle")
    before = sum((a * g for a, g in zip(field, chain)), start=Fraction(0))
    moved = (a + shift[edge] for a, edge in zip(field, complex_.edges))
    after = sum((a * g for a, g in zip(moved, chain)), start=Fraction(0))
    return Accepted(CyclePairingRecord(before, after, before == after))


# Executable finite evidence; AuthorityEffect: None.
