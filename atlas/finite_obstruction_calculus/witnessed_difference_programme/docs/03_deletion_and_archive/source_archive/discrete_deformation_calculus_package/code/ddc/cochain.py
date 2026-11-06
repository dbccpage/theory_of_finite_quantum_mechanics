"""Exact finite cochain complexes over Q for the DDC chapters and demos.

A complex has named vertices, oriented edges and oriented faces. ``d0`` sends a
vertex potential to edge differences; ``d1`` sums signed edge values around
each face. Construction refuses a complex whose faces break ``d1 d0 = 0``.

The diagnostics follow CODA-FOC:

* ``phi1`` is the weighted l1 distance from a 1-cochain to ``im d0``;
* ``gamma2`` is ``||d1 x||_1``, the face-closure defect;
* ``classify`` returns ExactRepair (phi1 = 0), ClosedResidual (phi1 > 0,
  gamma2 = 0) or ActiveClosureFailure (gamma2 > 0).

Everything is exact rational arithmetic; floats and bools are refused.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from math import comb
from types import MappingProxyType
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

Edge = Tuple[str, str]
Face = Tuple[Tuple[int, int], ...]
Matrix = Tuple[Tuple[Fraction, ...], ...]

EXACT_REPAIR = "ExactRepair"
CLOSED_RESIDUAL = "ClosedResidual"
ACTIVE_CLOSURE_FAILURE = "ActiveClosureFailure"

# Spanning-forest subsets examined by ``phi1`` before it refuses.
PHI1_SUBSET_BUDGET = 200_000


class CochainError(ValueError):
    """A malformed complex, cochain or budget, carrying a typed code."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def exact(value: object) -> Fraction:
    """Admit an exact rational; refuse floats, bools and anything else."""
    if isinstance(value, bool):
        raise CochainError("BOOL_FORBIDDEN", repr(value))
    if isinstance(value, float):
        raise CochainError("FLOAT_FORBIDDEN", repr(value))
    if isinstance(value, (int, Fraction)):
        return Fraction(value)
    raise CochainError("NOT_EXACT", repr(value))


def exact_vector(values: Sequence[object]) -> Tuple[Fraction, ...]:
    return tuple(exact(v) for v in values)


def l1(values: Sequence[Fraction]) -> Fraction:
    return sum((abs(v) for v in values), Fraction(0))


@dataclass(frozen=True)
class Complex:
    """A finite oriented 2-complex with optional positive edge weights."""

    vertices: Tuple[str, ...]
    edges: Tuple[Edge, ...]
    faces: Tuple[Face, ...] = ()
    weights: Optional[Tuple[Fraction, ...]] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "vertices", tuple(self.vertices))
        object.__setattr__(self, "edges", tuple(tuple(edge) for edge in self.edges))
        object.__setattr__(self, "faces", tuple(tuple(tuple(term) for term in face) for face in self.faces))
        if any(not isinstance(v, str) or not v for v in self.vertices):
            raise CochainError("MALFORMED_VERTEX", "vertices must be nonempty strings")
        if self.weights is not None:
            object.__setattr__(self, "weights", exact_vector(self.weights))
        if len(set(self.vertices)) != len(self.vertices):
            raise CochainError("DUPLICATE_VERTEX", repr(self.vertices))
        known = set(self.vertices)
        for u, v in self.edges:
            if u not in known or v not in known:
                raise CochainError("UNKNOWN_VERTEX", repr((u, v)))
            if u == v:
                raise CochainError("SELF_LOOP", f"{u} -> {v} is not a primitive difference")
        for face in self.faces:
            for index, sign in face:
                if (
                    type(index) is not int
                    or type(sign) is not int
                    or not 0 <= index < len(self.edges)
                    or sign not in (1, -1)
                ):
                    raise CochainError("MALFORMED_FACE", repr(face))
        if self.weights is not None:
            if len(self.weights) != len(self.edges):
                raise CochainError("WEIGHT_LENGTH", f"{len(self.weights)} != {len(self.edges)}")
            for w in self.weights:
                if exact(w) <= 0:
                    raise CochainError("NONPOSITIVE_WEIGHT", repr(w))
        for vertex in self.vertices:
            basis = {v: Fraction(1 if v == vertex else 0) for v in self.vertices}
            if any(value != 0 for value in self.d1(self.d0(basis))):
                raise CochainError("CHAIN_LAW_VIOLATED", f"d1 d0 != 0 at vertex {vertex}")

    # -- coboundaries -----------------------------------------------------

    def d0(self, potential: Mapping[str, Fraction]) -> Tuple[Fraction, ...]:
        missing = [v for v in self.vertices if v not in potential]
        if missing:
            raise CochainError("POTENTIAL_NOT_TOTAL", repr(missing))
        return tuple(exact(potential[v]) - exact(potential[u]) for u, v in self.edges)

    def d1(self, cochain: Sequence[Fraction]) -> Tuple[Fraction, ...]:
        x = self._edge_cochain(cochain)
        return tuple(sum((sign * x[i] for i, sign in face), Fraction(0)) for face in self.faces)

    def d0_matrix(self) -> Matrix:
        rows = []
        for u, v in self.edges:
            rows.append(
                tuple(Fraction(1 if w == v else -1 if w == u else 0) for w in self.vertices)
            )
        return tuple(rows)

    def d1_matrix(self) -> Matrix:
        rows = []
        for face in self.faces:
            row = [Fraction(0)] * len(self.edges)
            for index, sign in face:
                row[index] += sign
            rows.append(tuple(row))
        return tuple(rows)

    def weight(self, index: int) -> Fraction:
        return Fraction(1) if self.weights is None else exact(self.weights[index])

    def _edge_cochain(self, cochain: Sequence[object]) -> Tuple[Fraction, ...]:
        if len(cochain) != len(self.edges):
            raise CochainError("COCHAIN_LENGTH", f"{len(cochain)} != {len(self.edges)}")
        return exact_vector(cochain)

    # -- structure --------------------------------------------------------

    def components(self) -> List[List[str]]:
        parent = {v: v for v in self.vertices}

        def find(v: str) -> str:
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v

        for u, v in self.edges:
            parent[find(u)] = find(v)
        groups: Dict[str, List[str]] = {}
        for v in self.vertices:
            groups.setdefault(find(v), []).append(v)
        return list(groups.values())

    def spanning_forest(self) -> Tuple[int, ...]:
        """Edge indices of a BFS spanning forest, rooted at each component's first vertex."""
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

    def first_betti_of_graph(self) -> int:
        return len(self.edges) - len(self.vertices) + len(self.components())


def forest_potential(
    cx: Complex, cochain: Sequence[Fraction], forest: Sequence[int]
) -> Dict[str, Fraction]:
    """The potential that matches ``cochain`` exactly on the forest edges.

    Each component's first vertex is fixed at zero (the gauge choice).
    """
    x = cx._edge_cochain(cochain)
    adjacency: Dict[str, List[Tuple[str, Fraction]]] = {v: [] for v in cx.vertices}
    for index in forest:
        u, v = cx.edges[index]
        adjacency[u].append((v, x[index]))
        adjacency[v].append((u, -x[index]))
    potential: Dict[str, Fraction] = {}
    for root in cx.vertices:
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
    return potential


def exact_potential(cx: Complex, cochain: Sequence[Fraction]) -> Optional[Dict[str, Fraction]]:
    """A potential with ``d0 phi = cochain``, or ``None`` when the cochain is not exact."""
    x = cx._edge_cochain(cochain)
    potential = forest_potential(cx, x, cx.spanning_forest())
    return potential if cx.d0(potential) == x else None


def cycle_coordinates(cx: Complex, cochain: Sequence[Fraction]) -> Tuple[Fraction, ...]:
    """Circulation of the cochain around each fundamental cycle.

    One coordinate per non-forest edge, so ``len == b1`` of the 1-skeleton.
    Every coordinate is zero exactly when the cochain is exact.
    """
    x = cx._edge_cochain(cochain)
    forest = set(cx.spanning_forest())
    potential = forest_potential(cx, x, sorted(forest))
    d0 = cx.d0(potential)
    return tuple(x[i] - d0[i] for i in range(len(cx.edges)) if i not in forest)


def gamma2(cx: Complex, cochain: Sequence[Fraction]) -> Fraction:
    return l1(cx.d1(cochain))


def phi1(cx: Complex, cochain: Sequence[Fraction]) -> Fraction:
    """Weighted l1 distance from the cochain to ``im d0``, computed exactly.

    The objective is convex and piecewise linear in the potential, so a
    minimiser exists at a vertex of its linearity regions. There the tight edges
    contain a spanning forest, and the forest fixes the potential. Enumerating
    spanning forests therefore finds the minimum. Refuses as ``BUDGET_UNKNOWN``
    when the enumeration would exceed ``PHI1_SUBSET_BUDGET`` subsets.
    """
    x = cx._edge_cochain(cochain)
    if exact_potential(cx, x) is not None:
        return Fraction(0)
    rank = len(cx.vertices) - len(cx.components())
    if comb(len(cx.edges), rank) > PHI1_SUBSET_BUDGET:
        raise CochainError("BUDGET_UNKNOWN", f"C({len(cx.edges)}, {rank}) forests")
    best: Optional[Fraction] = None
    for subset in combinations(range(len(cx.edges)), rank):
        if not _is_forest(cx, subset):
            continue
        d0 = cx.d0(forest_potential(cx, x, subset))
        value = sum((cx.weight(i) * abs(x[i] - d0[i]) for i in range(len(x))), Fraction(0))
        if best is None or value < best:
            best = value
    assert best is not None  # a spanning forest always exists
    return best


@dataclass(frozen=True)
class Phi1Certificate:
    """Primal potential and dual flow whose objectives agree (strong duality).

    ``dual`` is an edge vector ``y`` with ``d0^T y = 0`` and ``|y_e| <= w_e``;
    ``<y, x>`` bounds Phi1 from below, and the potential attains it from above.
    """

    value: Fraction
    potential: Mapping[str, Fraction]
    dual: Tuple[Fraction, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", exact(self.value))
        object.__setattr__(self, "potential", MappingProxyType({k: exact(v) for k, v in self.potential.items()}))
        object.__setattr__(self, "dual", exact_vector(self.dual))


def _primal_value(cx: Complex, x: Sequence[Fraction], potential: Mapping[str, Fraction]) -> Fraction:
    d0 = cx.d0(potential)
    return sum((cx.weight(i) * abs(x[i] - d0[i]) for i in range(len(x))), Fraction(0))


def check_certificate(cx: Complex, cochain: Sequence[Fraction], cert: "Phi1Certificate") -> bool:
    """Verify primal attainment, dual feasibility and equal objectives, exactly."""
    x = cx._edge_cochain(cochain)
    try:
        dual = exact_vector(cert.dual)
        value = exact(cert.value)
        potential = {key: exact(v) for key, v in cert.potential.items()}
    except CochainError:
        return False
    if len(dual) != len(x) or set(potential) != set(cx.vertices):
        return False
    divergence = matvec(transpose(cx.d0_matrix()), dual) if cx.edges else ()
    feasible = all(v == 0 for v in divergence) and all(
        abs(y) <= cx.weight(i) for i, y in enumerate(dual)
    )
    dual_value = sum((y * xe for y, xe in zip(dual, x)), Fraction(0))
    return feasible and dual_value == value == _primal_value(cx, x, potential)


def phi1_certificate(cx: Complex, cochain: Sequence[Fraction]) -> Phi1Certificate:
    """Phi1 with a primal potential and a dual flow, both exact.

    Dual vertices set ``y_e = +-w_e`` off a spanning forest and solve the forest
    edges by flow conservation, so enumerating forests and signs finds a dual
    optimum; strong duality is then checked, never assumed.
    """
    x = cx._edge_cochain(cochain)
    rank = len(cx.vertices) - len(cx.components())
    cycles = len(cx.edges) - rank
    if comb(len(cx.edges), rank) * (2 ** cycles) > PHI1_SUBSET_BUDGET:
        raise CochainError("BUDGET_UNKNOWN", f"C({len(cx.edges)}, {rank}) forests x 2^{cycles} signs")
    forests = [s for s in combinations(range(len(cx.edges)), rank) if _is_forest(cx, s)]
    best_primal: Optional[Tuple[Fraction, Dict[str, Fraction]]] = None
    for forest in forests:
        potential = forest_potential(cx, x, forest)
        value = _primal_value(cx, x, potential)
        if best_primal is None or value < best_primal[0]:
            best_primal = (value, potential)
    d0t = transpose(cx.d0_matrix()) if cx.edges else ()
    best_dual: Optional[Tuple[Fraction, Tuple[Fraction, ...]]] = None
    for forest in forests:
        others = [i for i in range(len(cx.edges)) if i not in forest]
        columns = tuple(tuple(row[j] for j in forest) for row in d0t)
        for signs in product((-1, 1), repeat=len(others)):
            y = [Fraction(0)] * len(cx.edges)
            for i, sign in zip(others, signs):
                y[i] = sign * cx.weight(i)
            rhs = tuple(-v for v in matvec(d0t, y)) if cx.edges else ()
            flows = solve_consistent(columns, rhs) if forest else ()
            for i, flow in zip(forest, flows):
                y[i] = flow
            if any(abs(y[i]) > cx.weight(i) for i in forest):
                continue
            value = sum((a * b for a, b in zip(y, x)), Fraction(0))
            if best_dual is None or value > best_dual[0]:
                best_dual = (value, tuple(y))
    assert best_primal is not None and best_dual is not None
    cert = Phi1Certificate(best_primal[0], best_primal[1], best_dual[1])
    if not check_certificate(cx, x, cert):
        raise CochainError("DUALITY_GAP", f"primal {best_primal[0]} != dual {best_dual[0]}")
    return cert


def _is_forest(cx: Complex, subset: Sequence[int]) -> bool:
    parent = {v: v for v in cx.vertices}

    def find(v: str) -> str:
        while parent[v] != v:
            v = parent[v]
        return v

    for index in subset:
        u, v = cx.edges[index]
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True


def classify(cx: Complex, cochain: Sequence[Fraction]) -> str:
    """FOC trichotomy; an open closure defect dominates (witness dominance)."""
    if gamma2(cx, cochain) > 0:
        return ACTIVE_CLOSURE_FAILURE
    if exact_potential(cx, cochain) is not None:
        return EXACT_REPAIR
    return CLOSED_RESIDUAL


# -- exact linear algebra ---------------------------------------------------


def exact_matrix(m: Sequence[Sequence[object]]) -> Matrix:
    result = tuple(exact_vector(row) for row in m)
    if len({len(row) for row in result}) > 1:
        raise CochainError("SHAPE", "matrix rows must have equal lengths")
    return result


def transpose(m: Matrix) -> Matrix:
    m = exact_matrix(m)
    if not m:
        return ()
    return tuple(tuple(row[j] for row in m) for j in range(len(m[0])))


def matmul(a: Matrix, b: Matrix) -> Matrix:
    a, b = exact_matrix(a), exact_matrix(b)
    if a and len(a[0]) != len(b):
        raise CochainError("SHAPE", "left columns must equal right rows")
    cols = transpose(b)
    return tuple(
        tuple(sum((x * y for x, y in zip(row, col)), Fraction(0)) for col in cols) for row in a
    )


def matvec(m: Matrix, v: Sequence[Fraction]) -> Tuple[Fraction, ...]:
    m, v = exact_matrix(m), exact_vector(v)
    if m and len(m[0]) != len(v):
        raise CochainError("SHAPE", "matrix columns must equal vector length")
    return tuple(sum((x * y for x, y in zip(row, v)), Fraction(0)) for row in m)


def solve_consistent(a: Matrix, b: Sequence[Fraction]) -> Tuple[Fraction, ...]:
    """One exact solution of ``a z = b``; free variables are set to zero."""
    a, b = exact_matrix(a), exact_vector(b)
    if len(a) != len(b):
        raise CochainError("SHAPE", "matrix rows must equal right-hand side length")
    rows = [list(row) + [value] for row, value in zip(a, b)]
    n = len(a[0]) if a else 0
    pivots: List[int] = []
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        lead = rows[r][c]
        rows[r] = [value / lead for value in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                factor = rows[i][c]
                rows[i] = [x - factor * y for x, y in zip(rows[i], rows[r])]
        pivots.append(c)
        r += 1
    for row in rows[r:]:
        if row[-1] != 0:
            raise CochainError("INCONSISTENT_SYSTEM", "no exact solution")
    z = [Fraction(0)] * n
    for i, c in enumerate(pivots):
        z[c] = rows[i][-1]
    return tuple(z)


def hodge_split(
    cx: Complex, cochain: Sequence[Fraction]
) -> Tuple[Tuple[Fraction, ...], Tuple[Fraction, ...], Tuple[Fraction, ...]]:
    """Exact, co-exact and harmonic parts under the standard inner product.

    ``exact`` lies in ``im d0``, ``coexact`` in ``im d1^T``, and ``harmonic`` in
    ``ker d1 ∩ ker d0^T``. The three are pairwise orthogonal and sum to the input.
    """
    x = cx._edge_cochain(cochain)
    d0 = cx.d0_matrix()
    d0t = transpose(d0)
    potential = solve_consistent(matmul(d0t, d0), matvec(d0t, x)) if d0 else ()
    exact_part = matvec(d0, potential) if d0 else tuple(Fraction(0) for _ in x)
    remainder = tuple(a - b for a, b in zip(x, exact_part))
    if cx.faces:
        d1 = cx.d1_matrix()
        d1t = transpose(d1)
        psi = solve_consistent(matmul(d1, d1t), matvec(d1, remainder))
        coexact_part = matvec(d1t, psi)
    else:
        coexact_part = tuple(Fraction(0) for _ in x)
    harmonic = tuple(a - b for a, b in zip(remainder, coexact_part))
    return exact_part, coexact_part, harmonic


def _same_shape(left: Matrix, right: Matrix) -> bool:
    same_rows = len(left) == len(right)
    same_widths = all(len(a) == len(b) for a, b in zip(left, right))
    rectangular = len({len(row) for row in left}) <= 1
    return same_rows and same_widths and rectangular


def deformation_obstruction(d0: Matrix, d1: Matrix, mu0: Matrix, mu1: Matrix) -> Matrix:
    """``(d1 + mu1)(d0 + mu0)``; the deformation is lawful iff this is zero.

    With ``d1 d0 = 0`` it equals ``d1 mu0 + mu1 d0 + mu1 mu0``, the
    Maurer-Cartan expression of ``OE010-05``.
    """
    d0, d1, mu0, mu1 = (exact_matrix(m) for m in (d0, d1, mu0, mu1))
    if not _same_shape(d0, mu0) or not _same_shape(d1, mu1):
        raise CochainError("SHAPE", "a deformation must match the operator it deforms")
    if d1 and d0 and len(d1[0]) != len(d0):
        raise CochainError("SHAPE", "d1 columns must equal d0 rows")
    s1 = tuple(tuple(x + y for x, y in zip(r1, r2)) for r1, r2 in zip(d1, mu1))
    s0 = tuple(tuple(x + y for x, y in zip(r1, r2)) for r1, r2 in zip(d0, mu0))
    return matmul(s1, s0)
