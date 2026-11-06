"""Simplicial Complexes, Higher Structures, and Boundary Cancellation Primitives.

Selected educational models related to 19L57G1:
- code/derivation/higher_structure.py
- code/derivation/boundary_cancellation.py
- lean4/Derivation/HigherStructure.lean
- lean4/Derivation/BoundaryCancellation.lean

Classification: Simplicial calculus and homological boundary algebra.
AuthorityEffect: None.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Mapping, Sequence

from .canonical import FrozenMap, validate_typed_fields
from .observer_inventory import (
    LocalSection,
    MeasurementContext,
    ObserverPresheaf,
    make_bipartite_section,
)

# ---------------------------------------------------------------------------
# Base Simplicial Cells and Chains
# ---------------------------------------------------------------------------

Cell = tuple[int, ...]
Edge = tuple[int, int]
Tri = tuple[int, int, int]
Tet = tuple[int, int, int, int]
Chain = list[tuple[int, Cell]]
CEvent = tuple[object, ...]


# ---------------------------------------------------------------------------
# Composed Simplicial Complex (0-, 1-, 2-, 3-simplices)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Complex:
    """4-graded finite simplicial complex:
    c0: vertices (0-simplices)
    c1: directed/ascending edges (1-simplices)
    c2: triangles (2-simplices)
    c3: tetrahedra (3-simplices)
    """

    c0: tuple[int, ...] = ()
    c1: tuple[Edge, ...] = ()
    c2: tuple[Tri, ...] = ()
    c3: tuple[Tet, ...] = ()

    def __post_init__(self) -> None:
        validate_typed_fields(self)
        if any(vertex < 0 for vertex in self.c0) or len(set(self.c0)) != len(self.c0):
            raise ValueError("REFUSED_SHAPE: distinct natural-number vertices required")
        for grade in (self.c1, self.c2, self.c3):
            if len(set(grade)) != len(grade) or any(
                len(set(cell)) != len(cell) or any(vertex not in self.c0 for vertex in cell)
                for cell in grade
            ):
                raise ValueError("REFUSED_SHAPE: repeated cells or vertices outside carrier")

    def validate_boundary(self) -> None:
        """Exact snapshot boundary: every declared cell has every declared face."""
        for grade, lower in ((self.c2, self.c1), (self.c3, self.c2)):
            for cell in grade:
                if any(cell[:index] + cell[index + 1 :] not in lower for index in range(len(cell))):
                    raise ValueError("REFUSED_SHAPE: missing simplicial boundary face")

    @property
    def dim(self) -> int:
        """Maximum dimension of non-empty simplices in the complex."""
        if len(self.c3) > 0:
            return 3
        if len(self.c2) > 0:
            return 2
        if len(self.c1) > 0:
            return 1
        return 0

    def json(self) -> dict[str, object]:
        return {
            "c0": list(self.c0),
            "c1": [list(e) for e in self.c1],
            "c2": [list(t) for t in self.c2],
            "c3": [list(q) for q in self.c3],
            "dim": self.dim,
        }


EMPTY_COMPLEX = Complex()


# ---------------------------------------------------------------------------
# Shell Invariants (Boundary Filling Preconditions)
# ---------------------------------------------------------------------------


def shell1(cx: Complex, i: int, j: int) -> bool:
    """Shell condition for edge (i, j): both vertices admitted, i != j, edge fresh."""
    return i in cx.c0 and j in cx.c0 and i != j and (i, j) not in cx.c1


def shell2(cx: Complex, i: int, j: int, k: int) -> bool:
    """Shell condition for triangle (i, j, k): boundary 1-skeleton complete, face fresh."""
    return (i, j) in cx.c1 and (j, k) in cx.c1 and (i, k) in cx.c1 and (i, j, k) not in cx.c2


def shell3(cx: Complex, i: int, j: int, k: int, l: int) -> bool:
    """Shell condition for tetrahedron (i, j, k, l): boundary 2-skeleton complete, cell fresh."""
    return (
        (j, k, l) in cx.c2
        and (i, k, l) in cx.c2
        and (i, j, l) in cx.c2
        and (i, j, k) in cx.c2
        and (i, j, k, l) not in cx.c3
    )


# ---------------------------------------------------------------------------
# Simplicial Stepper and Replay
# ---------------------------------------------------------------------------


def cstep(cx: Complex, e: CEvent) -> Complex:
    """Apply one cell attachment event."""
    kind = e[0]
    if kind == "addV":
        v = e[1]
        assert isinstance(v, int)
        if v in cx.c0:
            return cx
        return replace(cx, c0=cx.c0 + (v,))
    if kind == "addE":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if shell1(cx, i, j):
            return replace(cx, c1=cx.c1 + ((i, j),))
        return cx
    if kind == "addT":
        i, j, k = e[1], e[2], e[3]
        assert isinstance(i, int) and isinstance(j, int) and isinstance(k, int)
        if shell2(cx, i, j, k):
            return replace(cx, c2=cx.c2 + ((i, j, k),))
        return cx
    if kind == "addQ":
        i, j, k, l = e[1], e[2], e[3], e[4]
        assert (
            isinstance(i, int) and isinstance(j, int) and isinstance(k, int) and isinstance(l, int)
        )
        if shell3(cx, i, j, k, l):
            return replace(cx, c3=cx.c3 + ((i, j, k, l),))
        return cx
    raise ValueError(f"Unknown cell event: {kind!r}")


def creplay(events: Sequence[CEvent], cx: Complex = EMPTY_COMPLEX) -> Complex:
    """Replay cell events from complex."""
    res = cx
    for e in events:
        res = cstep(res, e)
    return res


# ---------------------------------------------------------------------------
# Boundary Operators and Cancellation (d^2 = 0)
# ---------------------------------------------------------------------------


def erase_idx(sigma: Cell, i: int) -> Cell:
    """Delete entry at position i from simplex cell."""
    if i >= len(sigma):
        return sigma
    return sigma[:i] + sigma[i + 1 :]


def sgn(i: int) -> int:
    """Alternating sign (-1)^i."""
    return 1 if i % 2 == 0 else -1


def asc(sigma: Cell) -> bool:
    """Strict ascent condition: strictly increasing vertex indices."""
    return all(a < b for a, b in zip(sigma, sigma[1:]))


def facets(sigma: Cell) -> list[Cell]:
    """Return codimension-1 facets of simplex cell."""
    return [erase_idx(sigma, i) for i in range(len(sigma))]


def boundary(sigma: Cell) -> Chain:
    """Oriented simplicial boundary operator: sum_{i=0}^k (-1)^i d_i(sigma)."""
    return [(sgn(i), erase_idx(sigma, i)) for i in range(len(sigma))]


def boundary_of_chain(chain: Chain) -> Chain:
    """Boundary of an algebraic formal chain."""
    out: list[tuple[int, Cell]] = []
    for coeff, cell in chain:
        for b_coeff, b_cell in boundary(cell):
            out.append((coeff * b_coeff, b_cell))
    return out


def reduce_chain(chain: Chain) -> Chain:
    """Reduce formal chain by collecting coefficients on identical faces."""
    totals: dict[Cell, int] = {}
    for coeff, cell in chain:
        totals[cell] = totals.get(cell, 0) + coeff
    return sorted((c, cell) for cell, c in totals.items() if c != 0)


def d2_vanishes(sigma: Cell) -> bool:
    """Verify that composite boundary d(d(sigma)) vanishes identically (d^2 = 0)."""
    b1 = boundary(sigma)
    b2 = boundary_of_chain(b1)
    reduced = reduce_chain(b2)
    return len(reduced) == 0


# ---------------------------------------------------------------------------
# Regge Calculus, Simplicial Metric, Deficit Angles, and Čech Gluing Obstruction
# ---------------------------------------------------------------------------


def _mat_det(m: list[list[float]]) -> float:
    """Computes determinant of a small square matrix via Gaussian elimination with partial pivoting."""
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    a = [row[:] for row in m]
    det = 1.0
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < 1e-13:
            return 0.0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        det *= a[col][col]
        diag = a[col][col]
        for row in range(col + 1, n):
            factor = a[row][col] / diag
            for c in range(col + 1, n):
                a[row][c] -= factor * a[col][c]
    return det


def _mat_cofactor(m: list[list[float]], i: int, j: int) -> float:
    r"""Computes cofactor C_{ij} = (-1)^{i+j} * det(M_{\setminus i, \setminus j})."""
    sub = [row[:j] + row[j + 1 :] for idx, row in enumerate(m) if idx != i]
    sgn = 1 if (i + j) % 2 == 0 else -1
    return sgn * _mat_det(sub)


@dataclass(frozen=True)
class ReggeComplex:
    """Higher-dimensional Regge calculus simplicial complex (Category 5).

    Wraps a combinatorial 4-graded simplicial complex (vertices c0, edges c1,
    triangles c2, tetrahedra c3) equipped with metric edge lengths ell(e) > 0.

    Mathematical Invariants:
    1. Metric Assignment: For every edge (u, v) in c1, a positive length ell(u, v) is defined.
    2. 2D Triangles: Angles theta_t(v) are evaluated via the exact law of cosines.
    3. 3D Tetrahedra: Dihedral angles theta_sigma(e) are evaluated via Cayley-Menger cofactors.
    4. Discrete Curvature: Deficit angles epsilon(h) = 2*pi - sum theta(h) at hinges
       (vertices in 2D, edges in 3D).
    5. Curvature Bounds: Enforces max_h |epsilon(h)| <= Delta.
    6. Regge Action: S_Regge = sum_h Vol(h) * epsilon(h).
    7. Discrete Gauss-Bonnet: For closed 2D surfaces, sum_v epsilon(v) = 2*pi * chi(K).
    8. Čech Gluing Obstruction: Local Euclidean charts around a hinge fail to glue
       into a single global chart with Čech obstruction gamma_Cech(h) = |epsilon(h)|.
    9. Sheaf Compatibility: Projects to Category 12 ObserverPresheaf with exact
       Čech 0-cycle compatibility (No-Signaling) and Fine-Abramsky-Brandenburger contextuality.
    """

    complex: Complex
    edge_lengths: Mapping[Edge, float | int]

    def __post_init__(self) -> None:
        object.__setattr__(self, "edge_lengths", FrozenMap(self.edge_lengths))
        validate_typed_fields(self)

    def edge_length(self, u: int | tuple[int, int], v: int | None = None) -> float:
        """Returns length ell(u, v) for edge joining vertices u and v, or for edge tuple e=(u, v)."""
        if v is None:
            if isinstance(u, tuple) and len(u) == 2:
                u_val, v_val = u
            else:
                raise ValueError(
                    "Must provide either (u, v) as two ints or a single edge tuple (u, v)"
                )
        else:
            u_val, v_val = int(u), int(v)
        key = (min(u_val, v_val), max(u_val, v_val))
        if key in self.edge_lengths:
            return self.edge_lengths[key]
        if (u_val, v_val) in self.edge_lengths:
            return self.edge_lengths[(u_val, v_val)]
        if (v_val, u_val) in self.edge_lengths:
            return self.edge_lengths[(v_val, u_val)]
        raise KeyError(f"No length defined for edge ({u_val}, {v_val})")

    def squared_edge_length(self, u: int, v: int) -> float:
        l = self.edge_length(u, v)
        return l * l

    def triangle_lengths(self, tri: Tri) -> tuple[float, float, float]:
        """Returns side lengths (a, b, c) opposite to vertices (tri[0], tri[1], tri[2])."""
        u, v, w = tri
        a = self.edge_length(v, w)
        b = self.edge_length(u, w)
        c = self.edge_length(u, v)
        return (a, b, c)

    def triangle_area(self, tri: Tri) -> float:
        """Calculates area of 2-simplex via Heron's formula."""
        a, b, c = self.triangle_lengths(tri)
        s = 0.5 * (a + b + c)
        radicand = s * (s - a) * (s - b) * (s - c)
        return math.sqrt(max(0.0, radicand))

    def triangle_angle(self, tri: Tri, vertex: int) -> float:
        """Calculates interior angle of triangle tri at vertex (in radians)."""
        if vertex not in tri:
            raise ValueError(f"Vertex {vertex} not in triangle {tri}")
        u, v, w = tri
        if vertex == u:
            adj1, adj2, opp = (u, v), (u, w), (v, w)
        elif vertex == v:
            adj1, adj2, opp = (v, u), (v, w), (u, w)
        else:
            adj1, adj2, opp = (w, u), (w, v), (u, v)

        b = self.edge_length(*adj1)
        c = self.edge_length(*adj2)
        a = self.edge_length(*opp)

        cos_theta = (b * b + c * c - a * a) / (2.0 * b * c)
        cos_theta = max(-1.0, min(1.0, cos_theta))
        return math.acos(cos_theta)

    def tetrahedron_volume(self, tet: Tet) -> float:
        """Calculates volume of 3-simplex via 5x5 Cayley-Menger determinant."""
        verts = tet
        M = [[0.0] * 5 for _ in range(5)]
        for i in range(1, 5):
            M[0][i] = 1.0
            M[i][0] = 1.0
        for i in range(4):
            for j in range(4):
                if i != j:
                    d2 = self.squared_edge_length(verts[i], verts[j])
                    M[i + 1][j + 1] = d2
        det = _mat_det(M)
        vol_sq = det / 288.0
        return math.sqrt(max(0.0, vol_sq))

    def tetrahedron_dihedral_angle(self, tet: Tet, edge: Edge) -> float:
        """Calculates dihedral angle of tetrahedron tet at edge (in radians)."""
        u, v = edge
        if u not in tet or v not in tet:
            raise ValueError(f"Edge {edge} not in tetrahedron {tet}")
        others = [x for x in tet if x != u and x != v]
        if len(others) != 2:
            raise ValueError(f"Expected 2 other vertices in tetrahedron {tet} for edge {edge}")
        w1, w2 = sorted(others)

        # Order vertices in Cayley-Menger: 0:border, 1:u, 2:v, 3:w1, 4:w2
        verts = (u, v, w1, w2)
        M = [[0.0] * 5 for _ in range(5)]
        for i in range(1, 5):
            M[0][i] = 1.0
            M[i][0] = 1.0
        for i in range(4):
            for j in range(4):
                if i != j:
                    d2 = self.squared_edge_length(verts[i], verts[j])
                    M[i + 1][j + 1] = d2

        # Face opposite w2 is (u, v, w1) -> row/col 4
        # Face opposite w1 is (u, v, w2) -> row/col 3
        c33 = _mat_cofactor(M, 3, 3)
        c44 = _mat_cofactor(M, 4, 4)
        c34 = _mat_cofactor(M, 3, 4)

        denom = math.sqrt(max(1e-15, c33 * c44))
        cos_theta = c34 / denom
        cos_theta = max(-1.0, min(1.0, cos_theta))
        return math.acos(cos_theta)

    def hinges(self) -> list[int | Edge]:
        """Returns the list of hinges (codimension-2 simplices).
        For 3D complex (with tetrahedra): hinges are edges in c1.
        For 2D complex (triangles only): hinges are vertices in c0.
        """
        if self.complex.c3:
            return list(self.complex.c1)
        return list(self.complex.c0)

    def incident_top_simplices(self, hinge: int | Edge) -> list[Tri | Tet]:
        """Returns all top-dimensional simplices incident to the given hinge."""
        if isinstance(hinge, int):
            return [t for t in self.complex.c2 if hinge in t]
        else:
            u, v = hinge
            return [q for q in self.complex.c3 if u in q and v in q]

    def is_internal_hinge(self, hinge: int | Edge) -> bool:
        """Determines if the hinge is strictly internal (its link forms a closed manifold cycle)."""
        inc = self.incident_top_simplices(hinge)
        if not inc:
            return False
        if isinstance(hinge, int):
            v = hinge
            edge_counts: dict[int, int] = {}
            for t in inc:
                for w in t:
                    if w != v:
                        edge_counts[w] = edge_counts.get(w, 0) + 1
            return all(count == 2 for count in edge_counts.values()) and len(edge_counts) >= 3
        else:
            u, v = hinge
            vertex_counts: dict[int, int] = {}
            for q in inc:
                for w in q:
                    if w != u and w != v:
                        vertex_counts[w] = vertex_counts.get(w, 0) + 1
            return all(count == 2 for count in vertex_counts.values()) and len(vertex_counts) >= 3

    def deficit_angle(self, hinge: int | Edge) -> float:
        """Calculates discrete deficit angle epsilon(h) at the hinge in radians.

        For internal 2D vertex: epsilon(v) = 2*pi - sum_{t supset v} theta_t(v).
        For boundary 2D vertex: epsilon(v) = pi - sum_{t supset v} theta_t(v).
        For internal 3D edge: epsilon(e) = 2*pi - sum_{q supset e} theta_q(e).
        For boundary 3D edge: epsilon(e) = pi - sum_{q supset e} theta_q(e).
        """
        inc = self.incident_top_simplices(hinge)
        if not inc:
            return 0.0

        is_int = self.is_internal_hinge(hinge)
        flat_angle = 2.0 * math.pi if is_int else math.pi

        if isinstance(hinge, int):
            v = hinge
            angle_sum = sum(self.triangle_angle(t, v) for t in inc)
        else:
            e = hinge
            angle_sum = sum(self.tetrahedron_dihedral_angle(q, e) for q in inc)

        return flat_angle - angle_sum

    def all_deficit_angles(self, internal_only: bool = False) -> dict[int | Edge, float]:
        """Calculates deficit angles across hinges, optionally filtering to internal hinges."""
        hinges = [h for h in self.hinges() if not internal_only or self.is_internal_hinge(h)]
        return {h: self.deficit_angle(h) for h in hinges}

    def check_curvature_bound(
        self, bound: float, internal_only: bool = False, tol: float = 1e-9
    ) -> tuple[bool, float, dict[int | Edge, float]]:
        """Verifies if the Regge complex satisfies the curvature bound:
            max_h |epsilon(h)| <= bound.

        Returns (is_bounded, max_curvature, all_deficits).
        """
        deficits = self.all_deficit_angles(internal_only=internal_only)
        max_curv = max((abs(eps) for eps in deficits.values()), default=0.0)
        is_bounded = max_curv <= bound + tol
        return is_bounded, max_curv, deficits

    def regge_action(self) -> float:
        """Evaluates discrete Regge action:
        2D: sum_v epsilon(v)
        3D: sum_e ell(e) * epsilon(e)
        """
        if self.complex.c3:
            total_act = 0.0
            for e in self.complex.c1:
                eps = self.deficit_angle(e)
                u, v = e
                l = self.edge_length(u, v)
                total_act += l * eps
            return total_act
        else:
            return sum(self.deficit_angle(v) for v in self.complex.c0)

    def euler_characteristic(self) -> int:
        """Topological Euler characteristic chi(K) = c0 - c1 + c2 - c3."""
        return (
            len(self.complex.c0)
            - len(self.complex.c1)
            + len(self.complex.c2)
            - len(self.complex.c3)
        )

    def discrete_gauss_bonnet_discrepancy(self) -> float:
        """Discrepancy |sum_v epsilon(v) - 2*pi * chi(K)| for 2D triangulated closed surface."""
        if self.complex.c3:
            return 0.0
        total_def = sum(self.deficit_angle(v) for v in self.complex.c0)
        expected = 2.0 * math.pi * self.euler_characteristic()
        return abs(total_def - expected)

    def cech_gluing_obstruction(self, hinge: int | Edge) -> float:
        """Computes the Čech cohomological gluing obstruction gamma_Cech(h) in [0, 2*pi].

        The obstruction to gluing local Euclidean coordinate charts around hinge h
        into a single global chart is given by the deficit angle magnitude:
            gamma_Cech(h) = |epsilon(h)|
        """
        return abs(self.deficit_angle(hinge))

    def max_cech_gluing_obstruction(self, internal_only: bool = False) -> float:
        """Maximum Čech gluing obstruction across hinges."""
        deficits = self.all_deficit_angles(internal_only=internal_only)
        return max((abs(eps) for eps in deficits.values()), default=0.0)

    def has_global_gluing(self, hinge: int | Edge, tol: float = 1e-7) -> bool:
        """True iff local charts around hinge h glue without angular obstruction."""
        return self.cech_gluing_obstruction(hinge) <= tol

    def to_observer_presheaf(self, hinge: int | Edge) -> ObserverPresheaf:
        """Projects the star around hinge h to a Category 12 ObserverPresheaf.

        Each incident top simplex sigma_i defines a MeasurementContext with local
        directional observables. The correlation between adjacent facets is cos(theta_i).
        The presheaf strictly satisfies Čech 0-cycle compatibility (No-Signaling),
        and its Čech gluing obstruction is bounded by the deficit angle |epsilon(h)|.
        """
        inc = self.incident_top_simplices(hinge)
        k = len(inc)
        if k < 2:
            raise ValueError(f"Hinge {hinge} has fewer than 2 incident simplices")

        # Assign cyclical observable names
        obs_names = [f"H{hinge}_Obs{i}" for i in range(k)]
        contexts_list: list[MeasurementContext] = []
        sections_dict: dict[MeasurementContext, LocalSection] = {}

        for i in range(k):
            o1 = obs_names[i]
            o2 = obs_names[(i + 1) % k]
            ctx = MeasurementContext((o1, o2))
            contexts_list.append(ctx)

            # Subtended angle
            if isinstance(hinge, int):
                theta = self.triangle_angle(inc[i], hinge)
            else:
                theta = self.tetrahedron_dihedral_angle(inc[i], hinge)

            corr = math.cos(theta)
            corr = max(-1.0, min(1.0, corr))
            sections_dict[ctx] = make_bipartite_section(ctx, corr)

        return ObserverPresheaf(contexts=tuple(contexts_list), sections=sections_dict)


# ---------------------------------------------------------------------------
# Canonical Regge Calculus Simplicial Fixtures
# ---------------------------------------------------------------------------


def make_regge_complex(
    c0: Sequence[int],
    c1: Sequence[Edge],
    c2: Sequence[Tri],
    c3: Sequence[Tet] = (),
    edge_lengths: Mapping[Edge, float] | None = None,
    default_edge_length: float = 1.0,
) -> ReggeComplex:
    """Constructs a normalized ReggeComplex from simplex sequences."""
    norm_c1 = tuple((min(u, v), max(u, v)) for u, v in c1)
    norm_c2 = tuple(tuple(sorted(t)) for t in c2)
    norm_c3 = tuple(tuple(sorted(q)) for q in c3)
    cx = Complex(c0=tuple(c0), c1=norm_c1, c2=norm_c2, c3=norm_c3)

    lengths: dict[Edge, float] = {}
    if edge_lengths is not None:
        for (u, v), l in edge_lengths.items():
            lengths[(min(u, v), max(u, v))] = float(l)
    for e in norm_c1:
        if e not in lengths:
            lengths[e] = float(default_edge_length)
    return ReggeComplex(complex=cx, edge_lengths=lengths)


def flat_2d_hexagon_regge_fixture() -> ReggeComplex:
    """Flat 2D Regge patch: 6 equilateral triangles meeting at central vertex 0.

    Sum of angles = 6 * (pi / 3) = 2*pi.
    Deficit angle epsilon(0) = 0.0.
    Čech gluing obstruction gamma(0) = 0.0 (Global Euclidean gluing exists).
    """
    c0 = tuple(range(7))
    spokes = tuple((min(0, i), max(0, i)) for i in range(1, 7))
    rim = tuple((min(i, i % 6 + 1), max(i, i % 6 + 1)) for i in range(1, 7))
    c1 = spokes + rim
    c2 = tuple((0, i, i % 6 + 1) for i in range(1, 7))
    lens = {e: 1.0 for e in c1}
    return ReggeComplex(Complex(c0=c0, c1=c1, c2=c2), lens)


def curved_2d_icosahedral_cap_regge_fixture() -> ReggeComplex:
    """Positively curved 2D Regge cap: 5 equilateral triangles meeting at vertex 0.

    Sum of angles = 5 * (pi / 3) = 5*pi / 3.
    Deficit angle epsilon(0) = 2*pi - 5*pi/3 = pi/3 approx 1.047198 rad (+60 deg).
    Čech gluing obstruction gamma(0) = pi/3 > 0 (Global Euclidean gluing obstructed).
    """
    c0 = tuple(range(6))
    spokes = tuple((min(0, i), max(0, i)) for i in range(1, 6))
    rim = tuple((min(i, i % 5 + 1), max(i, i % 5 + 1)) for i in range(1, 6))
    c1 = spokes + rim
    c2 = tuple((0, i, i % 5 + 1) for i in range(1, 6))
    lens = {e: 1.0 for e in c1}
    return ReggeComplex(Complex(c0=c0, c1=c1, c2=c2), lens)


def saddle_2d_hyperbolic_regge_fixture() -> ReggeComplex:
    """Negatively curved 2D Regge saddle: 7 equilateral triangles meeting at vertex 0.

    Sum of angles = 7 * (pi / 3) = 7*pi / 3.
    Deficit angle epsilon(0) = 2*pi - 7*pi/3 = -pi/3 approx -1.047198 rad (-60 deg).
    Čech gluing obstruction gamma(0) = pi/3 > 0 (Global Euclidean gluing obstructed).
    """
    c0 = tuple(range(8))
    spokes = tuple((min(0, i), max(0, i)) for i in range(1, 8))
    rim = tuple((min(i, i % 7 + 1), max(i, i % 7 + 1)) for i in range(1, 8))
    c1 = spokes + rim
    c2 = tuple((0, i, i % 7 + 1) for i in range(1, 8))
    lens = {e: 1.0 for e in c1}
    return ReggeComplex(Complex(c0=c0, c1=c1, c2=c2), lens)


def closed_2d_tetrahedron_surface_regge_fixture() -> ReggeComplex:
    """Closed 2D surface (boundary of a 3-simplex): 4 equilateral triangles.

    Vertices: 4. Edges: 6. Faces: 4.
    Euler characteristic chi(K) = 4 - 6 + 4 = 2.
    Deficit angle at each vertex: 2*pi - 3*(pi/3) = pi.
    Discrete Gauss-Bonnet: sum_v epsilon(v) = 4*pi = 2*pi * chi(K).
    """
    c0 = (0, 1, 2, 3)
    c1 = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    c2 = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
    lens = {e: 1.0 for e in c1}
    return ReggeComplex(Complex(c0=c0, c1=c1, c2=c2), lens)


def flat_3d_tetrahedral_cluster_regge_fixture() -> ReggeComplex:
    """Flat 3D Regge cluster: 4 tetrahedra meeting along central hinge edge (0, 1).

    Each tetrahedron has dihedral angle pi/2 around edge (0, 1).
    Sum of dihedral angles = 4 * (pi / 2) = 2*pi.
    Deficit angle epsilon((0, 1)) = 0.0.
    Čech gluing obstruction gamma((0, 1)) = 0.0 (Global Euclidean 3D gluing exists).
    """
    c0 = (0, 1, 2, 3, 4, 5)
    c1 = (
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 3),
        (3, 4),
        (4, 5),
        (2, 5),
    )
    c3 = ((0, 1, 2, 3), (0, 1, 3, 4), (0, 1, 4, 5), (0, 1, 2, 5))
    lens = {
        (0, 1): 1.0,
        (0, 2): 1.0,
        (0, 3): 1.0,
        (0, 4): 1.0,
        (0, 5): 1.0,
        (1, 2): math.sqrt(2.0),
        (1, 3): math.sqrt(2.0),
        (1, 4): math.sqrt(2.0),
        (1, 5): math.sqrt(2.0),
        (2, 3): math.sqrt(2.0),
        (3, 4): math.sqrt(2.0),
        (4, 5): math.sqrt(2.0),
        (2, 5): math.sqrt(2.0),
    }
    return ReggeComplex(Complex(c0=c0, c1=c1, c3=c3), lens)


def curved_3d_5_tetrahedra_star_regge_fixture() -> ReggeComplex:
    """Positively curved 3D Regge star: 5 regular tetrahedra sharing central edge (0, 1).

    Each regular tetrahedron has dihedral angle arccos(1/3) approx 1.230959 rad (70.53 deg).
    Sum of dihedral angles = 5 * arccos(1/3) approx 6.154797 rad < 2*pi.
    Deficit angle epsilon((0, 1)) = 2*pi - 5*arccos(1/3) approx 0.128388 rad (+7.36 deg).
    Čech gluing obstruction gamma((0, 1)) approx 0.128388 > 0 (Obstructed by Regge curvature).
    """
    c0 = (0, 1, 2, 3, 4, 5, 6)
    c1 = (
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (2, 6),
    )
    c3 = ((0, 1, 2, 3), (0, 1, 3, 4), (0, 1, 4, 5), (0, 1, 5, 6), (0, 1, 2, 6))
    lens = {e: 1.0 for e in c1}
    return ReggeComplex(Complex(c0=c0, c1=c1, c3=c3), lens)
