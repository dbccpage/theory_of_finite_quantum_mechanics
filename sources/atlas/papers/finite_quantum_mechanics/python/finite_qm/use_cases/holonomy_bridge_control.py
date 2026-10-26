"""Finite multi-report holonomy bridge control for QM-207 through QM-211.

Every quantity here is computed exactly in a cyclotomic field Q(zeta_N) using
``CyclotomicElement``. Nothing is approximated. The control separates, for each
of the five imports of the L1-to-QM cascade, three layers:

1. a finite transition-cycle invariant that is exactly computed here;
2. a Cauchy-completion step that carries the finite invariant to its continuum
   value and is itself an import (completeness of the reals);
3. a residual structural import that neither layer 1 nor layer 2 supplies.

The honest status of each layer is returned by ``residual_import_ledger``.
The control does not claim that the five imports are independent of one
another, and it does not claim a derivation of any import from L1 weights.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Any, Dict, List, Sequence, Tuple

from finite_qm.domain.cyclotomic_tower import CyclotomicElement
from finite_qm.use_cases.cancellation_certificates import sorkin_i3

Edge = Tuple[int, int]
Walk = Sequence[int]
Matrix = List[List[CyclotomicElement]]


class HolonomyControlRefusal(ValueError):
    """Typed refusal: the supplied data is outside the declared finite model."""


def _one(conductor: int) -> CyclotomicElement:
    return CyclotomicElement.rational(1, conductor)


def _zero(conductor: int) -> CyclotomicElement:
    return CyclotomicElement.rational(0, conductor)


def root_of_unity(conductor: int, k: int) -> CyclotomicElement:
    """zeta_N^k as an exact element of Q(zeta_N)."""
    return CyclotomicElement.zeta(conductor) ** (k % conductor)


def is_root_of_unity(x: CyclotomicElement) -> bool:
    """x is a unit (x conj(x) = 1) of finite order dividing the conductor."""
    n = x.conductor
    return (x * x.conjugate()) == _one(n) and (x**n) == _one(n)


def root_exponent(x: CyclotomicElement) -> int:
    """The k with x = zeta_N^k. Refuses if x is not a root of unity of conductor N."""
    n = x.conductor
    for k in range(n):
        if root_of_unity(n, k) == x:
            return k
    raise HolonomyControlRefusal("value is not a root of unity of the declared conductor")


@dataclass(frozen=True)
class FiniteCarrierGraph:
    """Finite connected graph with a BFS spanning tree and fundamental cycles."""

    vertex_count: int
    edges: Tuple[Edge, ...]

    def __post_init__(self) -> None:
        if self.vertex_count < 1:
            raise HolonomyControlRefusal("a carrier needs at least one locus")
        for u, v in self.edges:
            if not (0 <= u < self.vertex_count and 0 <= v < self.vertex_count) or u == v:
                raise HolonomyControlRefusal("edges must join two distinct declared loci")
        if len(set(self.edges)) != len(self.edges):
            raise HolonomyControlRefusal("parallel edges are not part of this model")
        if len(self.spanning_tree()) != self.vertex_count - 1:
            raise HolonomyControlRefusal("carrier graph must be connected")

    def edge_index(self, u: int, v: int) -> Tuple[int, int]:
        """(index, sign): sign +1 if (u, v) is an edge, -1 if (v, u) is."""
        for i, (a, b) in enumerate(self.edges):
            if (a, b) == (u, v):
                return i, 1
            if (a, b) == (v, u):
                return i, -1
        raise HolonomyControlRefusal(f"no edge between {u} and {v}")

    def spanning_tree(self) -> Tuple[int, ...]:
        """Edge indices of the BFS spanning tree rooted at locus 0."""
        adjacency: Dict[int, List[Tuple[int, int]]] = {v: [] for v in range(self.vertex_count)}
        for i, (a, b) in enumerate(self.edges):
            adjacency[a].append((b, i))
            adjacency[b].append((a, i))
        seen = {0}
        tree: List[int] = []
        queue = deque([0])
        while queue:
            u = queue.popleft()
            for w, i in adjacency[u]:
                if w not in seen:
                    seen.add(w)
                    tree.append(i)
                    queue.append(w)
        return tuple(tree)

    def tree_parent(self) -> Dict[int, Tuple[int, int]]:
        """child -> (parent, edge index) along the BFS tree."""
        tree = set(self.spanning_tree())
        adjacency: Dict[int, List[Tuple[int, int]]] = {v: [] for v in range(self.vertex_count)}
        for i in tree:
            a, b = self.edges[i]
            adjacency[a].append((b, i))
            adjacency[b].append((a, i))
        parent: Dict[int, Tuple[int, int]] = {}
        seen = {0}
        queue = deque([0])
        while queue:
            u = queue.popleft()
            for w, i in adjacency[u]:
                if w not in seen:
                    seen.add(w)
                    parent[w] = (u, i)
                    queue.append(w)
        return parent

    def cotree_edges(self) -> Tuple[int, ...]:
        tree = set(self.spanning_tree())
        return tuple(i for i in range(len(self.edges)) if i not in tree)

    def first_betti_number(self) -> int:
        """b_1 = |E| - |V| + 1 for a connected graph."""
        return len(self.edges) - self.vertex_count + 1

    def tree_path(self, u: int, v: int) -> List[int]:
        """Unique tree path from u to v as a vertex sequence."""
        parent = self.tree_parent()

        def to_root(x: int) -> List[int]:
            path = [x]
            while x in parent:
                x = parent[x][0]
                path.append(x)
            return path

        up, vp = to_root(u), to_root(v)
        common = next(x for x in up if x in set(vp))
        head = up[: up.index(common) + 1]
        tail = vp[: vp.index(common)]
        return head + tail[::-1]

    def fundamental_cycle(self, cotree_edge: int) -> List[int]:
        """Closed walk: tree path from b to a, then the cotree edge a -> b (traversed forward)."""
        a, b = self.edges[cotree_edge]
        return self.tree_path(b, a) + [b]


@dataclass(frozen=True)
class U1Cochain:
    """A U(1) 1-cochain with values in the roots of unity of conductor N."""

    graph: FiniteCarrierGraph
    values: Tuple[CyclotomicElement, ...]

    def __post_init__(self) -> None:
        if len(self.values) != len(self.graph.edges):
            raise HolonomyControlRefusal("one value per edge is required")
        for x in self.values:
            if x.conductor != self.conductor or not is_root_of_unity(x):
                raise HolonomyControlRefusal(
                    "every edge value must be a root of unity of one conductor"
                )

    @property
    def conductor(self) -> int:
        return self.values[0].conductor

    def transport(self, walk: Walk) -> CyclotomicElement:
        """Ordered product of edge values along a walk; reversed edges contribute the conjugate."""
        if len(walk) < 1:
            raise HolonomyControlRefusal("a walk needs at least one locus")
        acc = _one(self.conductor)
        for u, v in zip(walk, walk[1:]):
            i, sign = self.graph.edge_index(u, v)
            x = self.values[i]
            acc = acc * (x if sign == 1 else x.conjugate())
        return acc

    def holonomy(self, closed_walk: Walk) -> CyclotomicElement:
        if closed_walk[0] != closed_walk[-1]:
            raise HolonomyControlRefusal("holonomy needs a closed walk")
        return self.transport(closed_walk)

    def gauge_transform(self, chi: Sequence[CyclotomicElement]) -> "U1Cochain":
        """A(u,v) -> chi(u) A(u,v) conj(chi(v))."""
        if len(chi) != self.graph.vertex_count or not all(is_root_of_unity(c) for c in chi):
            raise HolonomyControlRefusal("gauge must assign one root of unity to each locus")
        new = tuple(
            chi[u] * x * chi[v].conjugate() for (u, v), x in zip(self.graph.edges, self.values)
        )
        return U1Cochain(self.graph, new)

    def cycle_invariants(self) -> Tuple[CyclotomicElement, ...]:
        """Holonomies around the fundamental cycles: the image of A in Hom(H_1, mu_N)."""
        return tuple(
            self.holonomy(self.graph.fundamental_cycle(e)) for e in self.graph.cotree_edges()
        )

    def tree_gauge(self) -> "U1Cochain":
        """Gauge-equivalent cochain whose spanning-tree values are all 1 (proved construction)."""
        parent = self.graph.tree_parent()
        chi: List[CyclotomicElement] = [_one(self.conductor)] * self.graph.vertex_count
        order = sorted(parent, key=lambda v: len(self.graph.tree_path(0, v)))
        for v in order:
            p, i = parent[v]
            a, _ = self.graph.edges[i]
            x = self.values[i] if a == p else self.values[i].conjugate()
            chi[v] = chi[p] * x
        return self.gauge_transform(chi)

    def winding_coordinates(self, closed_walk: Walk) -> Dict[int, int]:
        """Signed traversal count of each cotree edge: the H_1 coordinates of the walk."""
        counts = {e: 0 for e in self.graph.cotree_edges()}
        for u, v in zip(closed_walk, closed_walk[1:]):
            i, sign = self.graph.edge_index(u, v)
            if i in counts:
                counts[i] += sign
        return counts


def holonomy_factorizes(cochain: U1Cochain, closed_walk: Walk) -> bool:
    """Hol(walk) == product over fundamental invariants^(winding coefficient). Exact."""
    inv = dict(zip(cochain.graph.cotree_edges(), cochain.cycle_invariants()))
    acc = _one(cochain.conductor)
    for e, k in cochain.winding_coordinates(closed_walk).items():
        acc = acc * (inv[e] ** (k % cochain.conductor))
    return acc == cochain.holonomy(closed_walk)


def gauge_orbit_census(graph: FiniteCarrierGraph, conductor: int) -> Dict[str, Any]:
    """Enumerate every mu_N cochain, group by cycle invariants, check the orbit count.

    Exactly computed: the classes are N^{b_1} in number, each of size N^{|V|-1},
    and two cochains share a class exactly when they are gauge equivalent.
    """
    roots = [root_of_unity(conductor, k) for k in range(conductor)]
    classes: Dict[Tuple[int, ...], int] = {}
    for assignment in product(range(conductor), repeat=len(graph.edges)):
        cochain = U1Cochain(graph, tuple(roots[k] for k in assignment))
        key = tuple(root_exponent(h) for h in cochain.cycle_invariants())
        classes[key] = classes.get(key, 0) + 1
    b1 = graph.first_betti_number()
    expected_classes = conductor**b1
    expected_size = conductor ** (graph.vertex_count - 1)
    return {
        "conductor": conductor,
        "edge_count": len(graph.edges),
        "first_betti_number": b1,
        "class_count": len(classes),
        "expected_class_count": expected_classes,
        "all_classes_have_expected_size": all(c == expected_size for c in classes.values()),
        "expected_class_size": expected_size,
        "hom_h1_mu_n_classification_exact": len(classes) == expected_classes
        and all(c == expected_size for c in classes.values()),
    }


def gauge_equivalence_matches_invariants(graph: FiniteCarrierGraph, conductor: int) -> bool:
    """Both directions, by enumeration: same invariants <=> some gauge maps one to the other."""
    roots = [root_of_unity(conductor, k) for k in range(conductor)]
    cochains = [
        U1Cochain(graph, tuple(roots[k] for k in a))
        for a in product(range(conductor), repeat=len(graph.edges))
    ]
    gauges = [
        tuple(roots[k] for k in g) for g in product(range(conductor), repeat=graph.vertex_count)
    ]
    for a in cochains:
        orbit = {tuple(root_exponent(x) for x in a.gauge_transform(g).values) for g in gauges}
        key_a = tuple(root_exponent(h) for h in a.cycle_invariants())
        for b in cochains:
            same_key = tuple(root_exponent(h) for h in b.cycle_invariants()) == key_a
            in_orbit = tuple(root_exponent(x) for x in b.values) in orbit
            if same_key != in_orbit:
                return False
    return True


def l1_weights(amplitudes: Sequence[CyclotomicElement]) -> List[CyclotomicElement]:
    """Phase-blind diagonal weights w_i = c_i conj(c_i)."""
    return [c.born_weight() for c in amplitudes]


def l1_phase_blind(
    amplitudes: Sequence[CyclotomicElement], chi: Sequence[CyclotomicElement]
) -> bool:
    """Weights are invariant under every locus gauge chi: the L1 shadow cannot see phase."""
    rotated = [c * g for c, g in zip(amplitudes, chi)]
    return l1_weights(rotated) == l1_weights(amplitudes)


def report_amplitudes(
    cochain: U1Cochain, source_amplitude: CyclotomicElement, reports: Sequence[Walk]
) -> List[CyclotomicElement]:
    """Transport one source amplitude along each report (a path) to the common sink."""
    sinks = {r[-1] for r in reports}
    sources = {r[0] for r in reports}
    if len(sinks) != 1 or len(sources) != 1:
        raise HolonomyControlRefusal("all reports must share one source and one sink")
    return [source_amplitude * cochain.transport(r) for r in reports]


def relative_report_phase(cochain: U1Cochain, p1: Walk, p2: Walk) -> CyclotomicElement:
    """Hol(p1 . p2^{-1}) = U(p1) conj(U(p2)); gauge invariant."""
    return cochain.transport(p1) * cochain.transport(p2).conjugate()


def l1_readout(amplitudes: Sequence[CyclotomicElement]) -> CyclotomicElement:
    acc = _zero(amplitudes[0].conductor)
    for w in l1_weights(amplitudes):
        acc = acc + w
    return acc


def quadratic_readout(amplitudes: Sequence[CyclotomicElement]) -> CyclotomicElement:
    acc = _zero(amplitudes[0].conductor)
    for c in amplitudes:
        acc = acc + c
    return acc.born_weight()


def quartic_readout(amplitudes: Sequence[CyclotomicElement]) -> CyclotomicElement:
    """Negative control: a non-quadratic readout |sum c|^4."""
    q = quadratic_readout(amplitudes)
    return q * q


def second_order_interference(amplitudes: Sequence[CyclotomicElement]) -> CyclotomicElement:
    """I_2 = quadratic readout minus L1 readout = sum_{i<j} 2 Re(c_i conj c_j)."""
    return quadratic_readout(amplitudes) - l1_readout(amplitudes)


def third_order_interference(
    readout: Any, amplitudes: Sequence[CyclotomicElement]
) -> CyclotomicElement:
    """Sorkin I_3 for an arbitrary readout rule on three amplitudes."""
    if len(amplitudes) != 3:
        raise HolonomyControlRefusal("I_3 needs three amplitudes")
    a, b, c = amplitudes
    return (
        readout([a, b, c])
        - readout([a, b])
        - readout([a, c])
        - readout([b, c])
        + readout([a])
        + readout([b])
        + readout([c])
    )


def identity(n: int, conductor: int) -> Matrix:
    return [[_one(conductor) if i == j else _zero(conductor) for j in range(n)] for i in range(n)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    n, m, p = len(a), len(b), len(b[0])
    conductor = a[0][0].conductor
    out = [[_zero(conductor) for _ in range(p)] for _ in range(n)]
    for i in range(n):
        for k in range(m):
            if a[i][k].is_zero():
                continue
            for j in range(p):
                out[i][j] = out[i][j] + a[i][k] * b[k][j]
    return out


def dagger(a: Matrix) -> Matrix:
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def mat_eq(a: Matrix, b: Matrix) -> bool:
    return all(x == y for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def is_unitary(a: Matrix) -> bool:
    return mat_eq(matmul(dagger(a), a), identity(len(a), a[0][0].conductor))


def scalar_multiple_of_identity(a: Matrix) -> CyclotomicElement:
    """Return c with a = c I, else refuse."""
    c = a[0][0]
    if not mat_eq(
        a, [[c if i == j else _zero(c.conductor) for j in range(len(a))] for i in range(len(a))]
    ):
        raise HolonomyControlRefusal("matrix is not a scalar multiple of the identity")
    return c


def weyl_shift(d: int, conductor: int) -> Matrix:
    if conductor % d != 0:
        raise HolonomyControlRefusal("the Weyl dimension must divide the conductor")
    return [
        [_one(conductor) if j == (k + 1) % d else _zero(conductor) for k in range(d)]
        for j in range(d)
    ]


def weyl_clock(d: int, conductor: int) -> Matrix:
    if conductor % d != 0:
        raise HolonomyControlRefusal("the Weyl dimension must divide the conductor")
    omega = root_of_unity(conductor, conductor // d)
    return [[omega**j if j == k else _zero(conductor) for k in range(d)] for j in range(d)]


def group_commutator(a: Matrix, b: Matrix) -> Matrix:
    """a b a^dagger b^dagger: the holonomy around the 4-cycle of context transitions."""
    return matmul(matmul(a, b), matmul(dagger(a), dagger(b)))


def commutator_holonomy(a: Matrix, b: Matrix) -> CyclotomicElement:
    """Central U(1) holonomy of the commutator cycle; refuses if it is not central."""
    return scalar_multiple_of_identity(group_commutator(a, b))


def fourier_matrix_d4(conductor: int) -> Matrix:
    """The d=4 Fourier matrix (1/2) i^{jk}: exact since sqrt(4) = 2."""
    if conductor % 4 != 0:
        raise HolonomyControlRefusal("d=4 Fourier needs 4 | conductor")
    i_unit = root_of_unity(conductor, conductor // 4)
    half = CyclotomicElement.rational(Fraction(1, 2), conductor)
    return [[half * (i_unit ** ((j * k) % 4)) for k in range(4)] for j in range(4)]


def apply(a: Matrix, v: Sequence[CyclotomicElement]) -> List[CyclotomicElement]:
    return [row[0] for row in matmul(a, [[x] for x in v])]


def born_in_context(
    transition: Matrix, amplitudes: Sequence[CyclotomicElement]
) -> List[CyclotomicElement]:
    """Born weights read in the context reached by the transition: |U c|^2 componentwise."""
    return l1_weights(apply(transition, amplitudes))


def pauli_2qubit(conductor: int) -> Dict[str, Matrix]:
    i_unit = root_of_unity(conductor, conductor // 4)
    one, zero = _one(conductor), _zero(conductor)
    single = {
        "I": [[one, zero], [zero, one]],
        "X": [[zero, one], [one, zero]],
        "Y": [[zero, zero - i_unit], [i_unit, zero]],
        "Z": [[one, zero], [zero, zero - one]],
    }

    def kron(a: Matrix, b: Matrix) -> Matrix:
        return [[a[i // 2][j // 2] * b[i % 2][j % 2] for j in range(4)] for i in range(4)]

    return {p + q: kron(single[p], single[q]) for p in "IXYZ" for q in "IXYZ"}


def peres_mermin_parity_holonomy(conductor: int) -> Dict[str, Any]:
    """Z/2 holonomy of the Peres-Mermin context cycle, computed exactly over Q(i).

    Rows and columns are commuting contexts of two-qubit Paulis. Every context
    product is +I or -I. The product of all six context signs is -1, which no
    assignment of +/-1 values to the nine observables can reproduce (each
    observable sits in exactly two contexts, so any value assignment gives +1).
    """
    if conductor % 4 != 0:
        raise HolonomyControlRefusal("Pauli matrices need 4 | conductor")
    P = pauli_2qubit(conductor)
    square = [["XI", "IX", "XX"], ["IZ", "ZI", "ZZ"], ["XZ", "ZX", "YY"]]
    contexts = [row for row in square] + [[square[r][c] for r in range(3)] for c in range(3)]
    signs: List[int] = []
    one = _one(conductor)
    zero_minus_one = _zero(conductor) - one
    for ctx in contexts:
        prod = identity(4, conductor)
        for name in ctx:
            prod = matmul(prod, P[name])
        s = scalar_multiple_of_identity(prod)
        if s == one:
            signs.append(1)
        elif s == zero_minus_one:
            signs.append(-1)
        else:
            raise HolonomyControlRefusal("context product is not +/- identity")
    pairwise_commute = all(
        mat_eq(matmul(P[a], P[b]), matmul(P[b], P[a])) for ctx in contexts for a in ctx for b in ctx
    )
    parity = 1
    for s in signs:
        parity *= s
    return {
        "contexts": contexts,
        "context_signs": signs,
        "contexts_commute_internally": pairwise_commute,
        "parity_holonomy": parity,
        "value_assignment_parity": 1,
        "z2_obstruction": parity != 1,
    }


def clock_refinement_tower(d: int, levels: int, conductor: int) -> Dict[str, Any]:
    """Finite clocks U_k = diag(zeta_{d 2^k}^j) with U_{k+1}^2 = U_k, all inside Q(zeta_N).

    Exactly computed: each level is unitary, has the declared finite order, and
    squares to the previous level. The tower is the finite part of the Cauchy
    completion Q/Z -> R/Z of the time axis; the limit itself is not computed.
    """
    orders = [d * (2**k) for k in range(levels)]
    if any(conductor % m != 0 for m in orders):
        raise HolonomyControlRefusal("every clock order must divide the conductor")
    clocks = [weyl_clock(m, conductor) for m in orders]
    square_consistent = all(
        mat_eq(_restrict_square(clocks[k + 1], orders[k]), clocks[k]) for k in range(levels - 1)
    )
    return {
        "orders": orders,
        "all_unitary": all(is_unitary(c) for c in clocks),
        "finite_orders_exact": all(
            mat_eq(_pow(c, m), identity(m, conductor)) for c, m in zip(clocks, orders)
        ),
        "no_smaller_order": all(
            not mat_eq(_pow(c, k), identity(m, conductor))
            for c, m in zip(clocks, orders)
            for k in range(1, m)
        ),
        "half_step_squares_to_previous": square_consistent,
        "eigenphase_exponents": [[j for j in range(m)] for m in orders],
    }


def _pow(a: Matrix, k: int) -> Matrix:
    out = identity(len(a), a[0][0].conductor)
    for _ in range(k):
        out = matmul(out, a)
    return out


def _restrict_square(clock_fine: Matrix, coarse_order: int) -> Matrix:
    """The fine clock squared, restricted to the first coarse_order eigenlines.

    diag(zeta_{2m}^j)^2 = diag(zeta_m^j); the first m eigenlines of the fine
    clock, after squaring, are exactly the coarse clock.
    """
    sq = matmul(clock_fine, clock_fine)
    return [[sq[i][j] for j in range(coarse_order)] for i in range(coarse_order)]


def residual_import_ledger() -> List[Dict[str, str]]:
    """Per import: what is exactly computed, what completion carries it, what remains imported."""
    return [
        {
            "import": "QM-207 complex phase fiber U(1)",
            "finite_invariant": "cycle holonomies in mu_N on cotree edges: Hom(H_1(G), mu_N) = mu_N^{b_1}",
            "finite_status": "exactly computed (orbit census) and proved (tree gauge, factorization)",
            "completion_step": "Cauchy completion of (Q/Z, circle metric) to R/Z = U(1); mu_infty is dense",
            "completion_status": "imported: completeness of R",
            "residual_import": "existence of a nontrivial fiber group acting on amplitude labels; L1 weights are gauge invariant and cannot select it",
        },
        {
            "import": "QM-208 quadratic l2 readout",
            "finite_invariant": "I_2 = |sum c|^2 - sum |c|^2 != 0 and Sorkin I_3 = 0, exactly in Q(zeta_N)",
            "finite_status": "exactly computed; I_3 = 0 proved for the quadratic rule by polynomial identity",
            "completion_step": "none for the rule; amplitudes sqrt(w) need an algebraic (not Cauchy) extension when w is not a square",
            "completion_status": "algebraic extension imported where used",
            "residual_import": "the composition rule add-then-square itself; I_3 = 0 characterizes it within a rule family but does not derive it",
        },
        {
            "import": "QM-209 noncommutative contexts",
            "finite_invariant": "central commutator holonomy X Z X^-1 Z^-1 = omega^-1 I in mu_d for the Weyl pair; = I for any diagonal pair",
            "finite_status": "exactly computed",
            "completion_step": "unitaries with entries in Q(zeta_N) over all N are dense in U(d); limits give general U(d)",
            "completion_status": "imported: completeness of R; density is a standard fact, not re-proved here",
            "residual_import": "the existence of a second context at all; L1 has one diagonal",
        },
        {
            "import": "QM-210 Born pairing",
            "finite_invariant": "diagonal Born weights equal the L1 weights (identity); transported weights |U c|^2 sum to the same total; Peres-Mermin Z/2 parity holonomy = -1",
            "finite_status": "exactly computed; the diagonal identity is immediate from the lift definition",
            "completion_step": "Gleason uniqueness of the quadratic frame function needs all frames in dimension >= 3",
            "completion_status": "imported: a continuum theorem, not reduced to finite cycles here",
            "residual_import": "noncontextuality of the frame function; finite KS/PM sets give obstructions, not uniqueness",
        },
        {
            "import": "QM-211 continuous unitary dynamics",
            "finite_invariant": "Z/m clocks with eigenphases in mu_m and half-step refinements squaring exactly to the coarse clock",
            "finite_status": "exactly computed",
            "completion_step": "direct limit of the refinement tower is Q/Z; Cauchy completion gives R/Z and the one-parameter group",
            "completion_status": "imported: completeness of R and strong continuity (Stone)",
            "residual_import": "continuity of t -> U(t) and the action unit; a finite clock fixes neither",
        },
    ]


def evaluate_holonomy_bridge_control(
    conductor: int = 12, census_conductor: int = 3
) -> Dict[str, Any]:
    """Run the whole finite control exactly and return JSON-serializable results."""
    if conductor % 12 != 0:
        raise HolonomyControlRefusal(
            "the control needs 12 | conductor (mu_3, mu_4 and mu_6 are used)"
        )
    # Carrier: the diamond 0-1-3, 0-2-3 with the chord 1-2. b_1 = 2. Three reports from 0 to 3.
    graph = FiniteCarrierGraph(4, ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)))
    z = lambda k: root_of_unity(conductor, k)  # noqa: E731
    cochain = U1Cochain(graph, (z(1), z(0), z(2), z(5), z(7)))
    reports: List[Walk] = [[0, 1, 3], [0, 2, 3], [0, 1, 2, 3]]
    gauge = [z(3), z(11), z(4), z(6)]
    gauged = cochain.gauge_transform(gauge)
    loops = [graph.fundamental_cycle(e) for e in graph.cotree_edges()] + [
        [0, 1, 2, 0],
        [0, 1, 3, 2, 1, 3, 2, 0],
    ]
    tree_gauge = cochain.tree_gauge()
    one = _one(conductor)

    amps = report_amplitudes(cochain, one, reports)
    chi_blind = [z(5), z(2), z(9)]
    i2 = second_order_interference(amps)
    i3_quadratic = third_order_interference(quadratic_readout, amps)
    i3_quartic = third_order_interference(quartic_readout, amps)
    i3_reused = sorkin_i3((amps[0], amps[1], amps[2]))
    trivial = U1Cochain(graph, tuple(one for _ in graph.edges))
    amps_trivial = report_amplitudes(trivial, one, reports)

    X, Z = weyl_shift(4, conductor), weyl_clock(4, conductor)
    F = fourier_matrix_d4(conductor)
    comm = commutator_holonomy(X, Z)
    diag_pair_comm = commutator_holonomy(Z, weyl_clock(4, conductor))

    state = [z(0), z(3), z(6), z(9)]
    half = CyclotomicElement.rational(Fraction(1, 2), conductor)
    state = [half * s for s in state]
    born_diag = l1_weights(state)
    born_fourier = born_in_context(F, state)
    total = lambda ws: sum(ws[1:], ws[0])  # noqa: E731

    pm = peres_mermin_parity_holonomy(conductor)
    tower = clock_refinement_tower(3, 3, conductor)

    return {
        "conductor": conductor,
        "qm207": {
            "carrier": {
                "vertices": 4,
                "edges": list(graph.edges),
                "first_betti_number": graph.first_betti_number(),
            },
            "cycle_invariant_exponents": [root_exponent(h) for h in cochain.cycle_invariants()],
            "cycle_invariants_gauge_invariant": gauged.cycle_invariants()
            == cochain.cycle_invariants(),
            "tree_gauge_has_unit_tree_edges": all(
                tree_gauge.values[i] == one for i in graph.spanning_tree()
            ),
            "tree_gauge_same_invariants": tree_gauge.cycle_invariants()
            == cochain.cycle_invariants(),
            "holonomy_factorizes_on_all_test_loops": all(
                holonomy_factorizes(cochain, w) for w in loops
            ),
            "relative_report_phase_exponents": [
                root_exponent(relative_report_phase(cochain, reports[i], reports[j]))
                for i in range(3)
                for j in range(i + 1, 3)
            ],
            "relative_report_phase_gauge_invariant": all(
                relative_report_phase(gauged, reports[i], reports[j])
                == relative_report_phase(cochain, reports[i], reports[j])
                for i in range(3)
                for j in range(i + 1, 3)
            ),
            "l1_weights_phase_blind": l1_phase_blind(amps, chi_blind),
            "orbit_census": gauge_orbit_census(graph, census_conductor),
            "gauge_equivalence_iff_same_invariants": gauge_equivalence_matches_invariants(
                FiniteCarrierGraph(3, ((0, 1), (1, 2), (0, 2))), 2
            ),
        },
        "qm208": {
            "l1_readout": str(l1_readout(amps).as_rational()),
            "quadratic_readout_is_rational": quadratic_readout(amps).is_rational(),
            "second_order_interference_nonzero": not i2.is_zero(),
            "second_order_interference_real": i2.is_real(),
            "trivial_fiber_interference": str(
                second_order_interference(amps_trivial).as_rational()
            ),
            "trivial_fiber_interference_positive": (
                second_order_interference(amps_trivial).as_rational() or 0
            )
            > 0,
            "sorkin_i3_quadratic_zero": i3_quadratic.is_zero(),
            "sorkin_i3_matches_reused_certifier": i3_quadratic == i3_reused,
            "sorkin_i3_quartic_on_reports": str(i3_quartic.as_rational()),
            "sorkin_i3_quartic_on_trivial_fiber": str(
                third_order_interference(quartic_readout, amps_trivial).as_rational()
            ),
            "sorkin_i3_quartic_nonzero_somewhere": not third_order_interference(
                quartic_readout, amps_trivial
            ).is_zero(),
        },
        "qm209": {
            "shift_clock_unitary": is_unitary(X) and is_unitary(Z) and is_unitary(F),
            "commutator_holonomy_exponent": root_exponent(comm),
            "commutator_holonomy_is_primitive_4th_root": root_exponent(comm)
            in (conductor // 4, 3 * conductor // 4),
            "diagonal_pair_commutator_trivial": diag_pair_comm == one,
            "fourier_conjugates_clock_to_inverse_shift": mat_eq(
                matmul(matmul(F, Z), dagger(F)), dagger(X)
            ),
        },
        "qm210": {
            "diagonal_born_equals_l1": born_diag == l1_weights(state),
            "transported_weights": [str(w.as_rational()) for w in born_fourier],
            "transported_total_equals_l1_total": total(born_fourier) == total(born_diag),
            "peres_mermin": pm,
        },
        "qm211": tower,
        "residual_import_ledger": residual_import_ledger(),
    }
