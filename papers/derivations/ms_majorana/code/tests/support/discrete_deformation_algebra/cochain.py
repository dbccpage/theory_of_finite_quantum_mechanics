"""M3 — Finite cochain window over ℤ with square-zero and Φ₁/Γ₂."""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Sequence, Tuple

from omega_engine.crates.terminalizers.termz_finite_obstruction_calculus import classify_phi_gamma, TerminalizerVerdict


@dataclass(frozen=True)
class CoboundaryComplex:
    dim_c0: int
    dim_c1: int
    dim_c2: int
    d0: Tuple[Tuple[int, ...], ...]  # dim_c1 × dim_c0
    d1: Tuple[Tuple[int, ...], ...]  # dim_c2 × dim_c1

    def __post_init__(self) -> None:
        if len(self.d0) != self.dim_c1:
            raise ValueError("d0 row count must equal dim_c1")
        if any(len(r) != self.dim_c0 for r in self.d0):
            raise ValueError("d0 row width must equal dim_c0")
        if len(self.d1) != self.dim_c2:
            raise ValueError("d1 row count must equal dim_c2")
        if any(len(r) != self.dim_c1 for r in self.d1):
            raise ValueError("d1 row width must equal dim_c1")

    @staticmethod
    def path_graph_exact(n_nodes: int = 2) -> "CoboundaryComplex":
        if n_nodes < 2:
            raise ValueError("need at least 2 nodes")
        n_edges = n_nodes - 1
        d0_rows = []
        for e in range(n_edges):
            row = [0] * n_nodes
            row[e] = -1
            row[e + 1] = 1
            d0_rows.append(tuple(row))
        return CoboundaryComplex(
            dim_c0=n_nodes,
            dim_c1=n_edges,
            dim_c2=0,
            d0=tuple(d0_rows),
            d1=tuple(),
        )

    @staticmethod
    def triangle_lggr_z2() -> "CoboundaryComplex":
        """Three vertices, three edges, one face — LGGR triangle (Demo 2).

        d0 incidence of oriented cycle; d1 sums edge values around face.
        A 1-cochain that is locally edge-consistent but globally non-closed
        yields Γ₂ > 0.
        """
        # edges: 0→1, 1→2, 2→0
        d0 = (
            (-1, 1, 0),
            (0, -1, 1),
            (1, 0, -1),
        )
        d1 = ((1, 1, 1),)  # holonomy around the triangle
        return CoboundaryComplex(dim_c0=3, dim_c1=3, dim_c2=1, d0=d0, d1=d1)

    @staticmethod
    def broken_square_zero() -> "CoboundaryComplex":
        return CoboundaryComplex(dim_c0=1, dim_c1=1, dim_c2=1, d0=((1,),), d1=((1,),))

    @staticmethod
    def grid_2x2_complex() -> "CoboundaryComplex":
        """2x2 grid cell complex (9 vertices, 12 edges, 4 faces).
        Used for testing high-dimensional integer co-exact CVP / ILP cochain solvers.
        """
        d0 = (
            (-1, 1, 0, 0, 0, 0, 0, 0, 0),  # e0: 0->1
            (0, -1, 1, 0, 0, 0, 0, 0, 0),  # e1: 1->2
            (0, 0, 0, -1, 1, 0, 0, 0, 0),  # e2: 3->4
            (0, 0, 0, 0, -1, 1, 0, 0, 0),  # e3: 4->5
            (0, 0, 0, 0, 0, 0, -1, 1, 0),  # e4: 6->7
            (0, 0, 0, 0, 0, 0, 0, -1, 1),  # e5: 7->8
            (-1, 0, 0, 1, 0, 0, 0, 0, 0),  # e6: 0->3
            (0, -1, 0, 0, 1, 0, 0, 0, 0),  # e7: 1->4
            (0, 0, -1, 0, 0, 1, 0, 0, 0),  # e8: 2->5
            (0, 0, 0, -1, 0, 0, 1, 0, 0),  # e9: 3->6
            (0, 0, 0, 0, -1, 0, 0, 1, 0),  # e10: 4->7
            (0, 0, 0, 0, 0, -1, 0, 0, 1),  # e11: 5->8
        )
        d1 = (
            (1, 0, -1, 0, 0, 0, -1, 1, 0, 0, 0, 0),  # f0
            (0, 1, 0, -1, 0, 0, 0, -1, 1, 0, 0, 0),  # f1
            (0, 0, 1, 0, -1, 0, 0, 0, 0, -1, 1, 0),  # f2
            (0, 0, 0, 1, 0, -1, 0, 0, 0, 0, -1, 1),  # f3
        )
        return CoboundaryComplex(dim_c0=9, dim_c1=12, dim_c2=4, d0=d0, d1=d1)

    @staticmethod
    def cube_complex() -> "CoboundaryComplex":
        """Closed 3D cube cell complex (8 vertices, 12 edges, 6 faces).
        Homology bound guarantees sum of 6 faces is 0, rank of C² is 5 < 6.
        Demonstrates exact HNF rank reduction savings in integer co-exact solver.
        """
        d0 = (
            (-1, 1, 0, 0, 0, 0, 0, 0),  # e0: 0->1
            (0, -1, 1, 0, 0, 0, 0, 0),  # e1: 1->2
            (0, 0, -1, 1, 0, 0, 0, 0),  # e2: 2->3
            (1, 0, 0, -1, 0, 0, 0, 0),  # e3: 3->0
            (0, 0, 0, 0, -1, 1, 0, 0),  # e4: 4->5
            (0, 0, 0, 0, 0, -1, 1, 0),  # e5: 5->6
            (0, 0, 0, 0, 0, 0, -1, 1),  # e6: 6->7
            (0, 0, 0, 0, 1, 0, 0, -1),  # e7: 7->4
            (-1, 0, 0, 0, 1, 0, 0, 0),  # e8: 0->4
            (0, -1, 0, 0, 0, 1, 0, 0),  # e9: 1->5
            (0, 0, -1, 0, 0, 0, 1, 0),  # e10: 2->6
            (0, 0, 0, -1, 0, 0, 0, 1),  # e11: 3->7
        )
        d1 = (
            (1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),  # f0
            (0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0),  # f1
            (1, 0, 0, 0, -1, 0, 0, 0, -1, 1, 0, 0),  # f2
            (0, 1, 0, 0, 0, -1, 0, 0, 0, -1, 1, 0),  # f3
            (0, 0, 1, 0, 0, 0, -1, 0, 0, 0, -1, 1),  # f4
            (0, 0, 0, 1, 0, 0, 0, -1, 1, 0, 0, -1),  # f5
        )
        return CoboundaryComplex(dim_c0=8, dim_c1=12, dim_c2=6, d0=d0, d1=d1)


def mat_mul(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> List[List[int]]:
    if not a:
        return []
    if not b:
        return [[] for _ in a]
    n, k, m = len(a), len(b), len(b[0])
    if any(len(row) != k for row in a):
        raise ValueError("incompatible shapes")
    out = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            out[i][j] = sum(a[i][t] * b[t][j] for t in range(k))
    return out


def square_zero_check(cx: CoboundaryComplex) -> dict:
    if cx.dim_c2 == 0:
        return {"ok": True, "defect": [], "l1_defect_mass": 0}
    if cx.dim_c1 == 0:
        return {
            "ok": True,
            "defect": [[0] * cx.dim_c0 for _ in range(cx.dim_c2)],
            "l1_defect_mass": 0,
        }
    comp = mat_mul([list(r) for r in cx.d1], [list(r) for r in cx.d0])
    mass = sum(abs(x) for row in comp for x in row)
    return {"ok": mass == 0, "defect": comp, "l1_defect_mass": mass}


def apply_d1(cx: CoboundaryComplex, c1: Sequence[int]) -> List[int]:
    if len(c1) != cx.dim_c1:
        raise ValueError("c1 length")
    if cx.dim_c2 == 0:
        return []
    out = []
    for row in cx.d1:
        out.append(sum(row[j] * c1[j] for j in range(cx.dim_c1)))
    return out


def apply_d0(cx: CoboundaryComplex, c0: Sequence[int]) -> List[int]:
    if len(c0) != cx.dim_c0:
        raise ValueError("c0 length")
    out = []
    for row in cx.d0:
        out.append(sum(row[j] * c0[j] for j in range(cx.dim_c0)))
    return out


def gamma2_of(cx: CoboundaryComplex, c1: Sequence[int]) -> int:
    """Γ₂ = ‖d₁ x‖₁."""
    return sum(abs(v) for v in apply_d1(cx, c1))


def phi1_brute(cx: CoboundaryComplex, c1: Sequence[int], c0_radius: int = 3) -> int:
    """Φ₁ = inf_α ‖x − d₀α‖₁ over a finite integer search box (exact on small toys)."""
    if cx.dim_c0 == 0:
        return sum(abs(x) for x in c1)
    best = sum(abs(x) for x in c1)
    # search α in [-radius, radius]^dim_c0
    from itertools import product

    ranges = [range(-c0_radius, c0_radius + 1) for _ in range(cx.dim_c0)]
    for alpha in product(*ranges):
        d0a = apply_d0(cx, alpha)
        mass = sum(abs(c1[i] - d0a[i]) for i in range(cx.dim_c1))
        if mass < best:
            best = mass
    return best


def brute_integer_coexact_closure(
    cx: CoboundaryComplex, omega: Sequence[int], radius: int = 5
) -> Tuple[Tuple[int, ...], Tuple[int, ...], int]:
    """Exact integer co-exact closure inside declared finite search radius.
    Finds y in Z^{dim_c2} minimizing ||d1(omega + (d1).T y)||_1.
    Returns (delta_c, y, min_gamma2).
    """
    from itertools import product

    if cx.dim_c2 == 0 or cx.dim_c1 == 0:
        return tuple([0] * cx.dim_c1), (), gamma2_of(cx, c1=list(omega))

    # Transpose of d1: (d1)^T is dim_c1 x dim_c2
    d1t = tuple(tuple(cx.d1[r][c] for r in range(cx.dim_c2)) for c in range(cx.dim_c1))

    best_y = tuple(0 for _ in range(cx.dim_c2))
    best_delta = tuple(0 for _ in range(cx.dim_c1))
    best_gamma = gamma2_of(cx, list(omega))

    for y in product(range(-radius, radius + 1), repeat=cx.dim_c2):
        # (d1)^T y
        delta = tuple(
            sum(d1t[c][r] * y[r] for r in range(cx.dim_c2)) for c in range(cx.dim_c1)
        )
        candidate = tuple(w + d for w, d in zip(omega, delta))
        gamma = gamma2_of(cx, candidate)

        if gamma < best_gamma:
            best_gamma = gamma
            best_y = y
            best_delta = delta

    return best_delta, best_y, best_gamma


def residual_verdict(
    cx: CoboundaryComplex, c1: Sequence[int], *, c0_radius: int = 3
) -> TerminalizerVerdict:
    phi = phi1_brute(cx, c1, c0_radius=c0_radius)
    gamma = gamma2_of(cx, c1)
    return classify_phi_gamma(phi, gamma)




