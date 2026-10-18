"""Regge climb: SU(2) on a tetrahedron, U(1) from deficit, Witten Q on cochains.

Pencil-and-paper structures that actually live on a simplicial complex.
AuthorityEffect: None. Stdlib only.

This is not the MSSM, not PDG, not v×360. It is Regge calculus plus
the cochain supercharge that any incidence geometry already has.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from itertools import product

# --- integer linear algebra on small tuples ---

def dot(u: tuple[int, ...], v: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(u, v))


def mat_vec(m: tuple[tuple[int, ...], ...], v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(dot(row, v) for row in m)


def transpose(m: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    cols = len(m[0])
    return tuple(tuple(m[r][c] for r in range(len(m))) for c in range(cols))


def mat_mul(
    a: tuple[tuple[int, ...], ...], b: tuple[tuple[int, ...], ...]
) -> tuple[tuple[int, ...], ...]:
    bt = transpose(b)
    return tuple(tuple(dot(row, col) for col in bt) for row in a)


def l1(v: Sequence[int]) -> int:
    return sum(abs(x) for x in v)


# --- 2D Regge deficit (equilateral) ---

def regge_deficit_2d(valency: int) -> tuple[int, int]:
    """Deficit in units of π/3: (6 - k). Flat k=6 ⇒ 0."""
    return (6 - valency, 3)


# --- 3D regular tetrahedron dihedral: arccos(1/3), flat ~5.1 around an edge ---

def tetra_dihedral_cos() -> tuple[int, int]:
    """cos θ = 1/3 as a rational pair (num, den)."""
    return (1, 3)


# --- Ponzano–Regge: SU(2) spins on a tetrahedron ---

# Six edges of a tetrahedron, opposite pairs (01,23), (02,13), (03,12).
# Spins are nonnegative integers 2j (so j half-integer iff 2j odd).

TetraEdges = tuple[int, int, int, int, int, int]


def _triangle_ok(a: int, b: int, c: int) -> bool:
    """Admissible SU(2) triad: triangle inequalities and even sum (2j integers)."""
    if a < 0 or b < 0 or c < 0:
        return False
    if a + b < c or a + c < b or b + c < a:
        return False
    return (a + b + c) % 2 == 0


def tetra_faces(spins: TetraEdges) -> tuple[tuple[int, int, int], ...]:
    j01, j02, j03, j12, j13, j23 = spins
    return (
        (j01, j02, j12),
        (j01, j03, j13),
        (j02, j03, j23),
        (j12, j13, j23),
    )


def su2_tetra_admissible(spins: TetraEdges) -> bool:
    """A 3D Regge simplex carries SU(2) iff every face is an admissible triad.

    This is the Ponzano–Regge kinematic constraint. It is not a 6j evaluation
    and not a continuum limit.
    """
    return all(_triangle_ok(*face) for face in tetra_faces(spins))


def count_admissible_tetras(jmax: int) -> tuple[int, int]:
    """How many 2j-assignments with 0 ≤ 2j ≤ jmax are SU(2)-admissible."""
    total = 0
    ok = 0
    rng = range(jmax + 1)
    for spins in product(rng, repeat=6):
        total += 1
        if su2_tetra_admissible(spins):  # type: ignore[arg-type]
            ok += 1
    return ok, total


# Small exact 6j from Racah (all arguments integers, 2j even).
# {1 1 1; 1 1 1} = 1/6.
def sixj_111_111() -> tuple[int, int]:
    return (1, 6)


# --- U(1) holonomy from oriented deficit ---

def u1_holonomy_from_deficit(deficit_units: int, period: int = 6) -> int:
    """Cyclic phase class from 2D deficit units of π/3.

    Flat: 0. A single π/3 deficit is class 1 in Z/6Z.  Interpreting
    that class as a U(1) phase additionally supplies the embedding
    n ↦ exp(2πin/period); this integer function does not construct it.
    """
    if period <= 0:
        raise ValueError("period must be positive")
    return deficit_units % period


def face_holonomy_add(edge_phases: tuple[int, int, int], period: int = 6) -> int:
    """Oriented sum of edge phases around a triangle, mod period."""
    return sum(edge_phases) % period


# --- SU(3) on the 2-simplex: available after extras, not forced ---

def c3_from_triangle_vertices() -> int:
    """Real dimension of vertex functions on a 2-simplex: 3."""
    return 3


def su3_extras_needed() -> dict[str, bool]:
    """What you still have to admit to promote C^3 to SU(3).

    Hermitian inner product → U(3). Unit determinant → SU(3).
    Adjoint dimension 8 is then End_0(C^3), not a vertex count.
    """
    return {
        "hermitian_form": True,
        "unit_determinant": True,
        "adjoint_eight_from_vertex_count": False,
    }


# --- Witten supercharge on the triangle 1-skeleton ---
# Vertices 0,1,2. Oriented edges 01, 12, 20.
# d0: C^0 → C^1, (a,b,c) ↦ (b-a, c-b, a-c)
# d0*: C^1 → C^0 is the transpose (graph coboundary / divergence).

D0: tuple[tuple[int, ...], ...] = (
    (-1, 1, 0),
    (0, -1, 1),
    (1, 0, -1),
)
D0T: tuple[tuple[int, ...], ...] = transpose(D0)


def d0(alpha: tuple[int, int, int]) -> tuple[int, int, int]:
    return mat_vec(D0, alpha)


def d0_star(omega: tuple[int, int, int]) -> tuple[int, int, int]:
    return mat_vec(D0T, omega)


def d1(omega: tuple[int, int, int]) -> tuple[int, ...]:
    """Filled triangle: d1 is the sum of oriented edges (one 2-cell)."""
    return (omega[0] + omega[1] + omega[2],)


def d1_d0_zero(alpha: tuple[int, int, int]) -> bool:
    return d1(d0(alpha)) == (0,)


@dataclass(frozen=True)
class SuperPair:
    even: tuple[int, int, int]
    odd: tuple[int, int, int]


def Q(pair: SuperPair) -> SuperPair:
    """Witten supercharge Q = d + d* on C^0 ⊕ C^1.

    Q(even, odd) = (d* odd, d even). Odd derivation: swaps parity.
    """
    return SuperPair(even=d0_star(pair.odd), odd=d0(pair.even))


def Q2(pair: SuperPair) -> SuperPair:
    return Q(Q(pair))


def vertex_laplacian(alpha: tuple[int, int, int]) -> tuple[int, int, int]:
    return d0_star(d0(alpha))


def edge_laplacian(omega: tuple[int, int, int]) -> tuple[int, int, int]:
    return d0(d0_star(omega))


def q_squares_to_laplacian(pair: SuperPair) -> bool:
    got = Q2(pair)
    want = SuperPair(
        even=vertex_laplacian(pair.even),
        odd=edge_laplacian(pair.odd),
    )
    return got == want


def q_is_odd(pair: SuperPair) -> bool:
    """Q exchanges even and odd slots; Q^2 preserves them."""
    once = Q(pair)
    return once.even == d0_star(pair.odd) and once.odd == d0(pair.even)


def climb_report() -> dict[str, object]:
    tetra = (2, 2, 2, 2, 2, 2)
    bad_tetra = (3, 0, 0, 0, 0, 0)
    ok_n, total_n = count_admissible_tetras(2)
    pair = SuperPair(even=(1, 0, -1), odd=(2, -1, 0))
    return {
        "authority_effect": "None",
        "regge_deficit_k5": regge_deficit_2d(5),
        "su2_regular_tetra": su2_tetra_admissible(tetra),
        "su2_inadmissible_example": su2_tetra_admissible(bad_tetra),
        "su2_admissible_count_jmax2": (ok_n, total_n),
        "sixj_111_111": sixj_111_111(),
        "u1_holonomy_k5": u1_holonomy_from_deficit(1),
        "c3_dim": c3_from_triangle_vertices(),
        "su3_extras": su3_extras_needed(),
        "d1_d0_zero": d1_d0_zero((1, -2, 4)),
        "q2_is_laplacian": q_squares_to_laplacian(pair),
        "is_mssm": False,
        "is_su3_forced": False,
        "su2_label_fixture_admissible": su2_tetra_admissible(tetra),
        "cyclic_phase_from_deficit": True,
        "u1_embedding_constructed": False,
        "graph_supercharge_identity": q_squares_to_laplacian(pair),
        "physical_susy_identification": False,
    }
