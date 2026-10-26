"""Exact witness for the 4D simplicial bivector, closure, Bianchi, and SO(4) transport carrier in derivation.md."""

from __future__ import annotations

from fractions import Fraction

VERTICES: tuple[tuple[int, int, int, int], ...] = (
    (0, 0, 0, 0),
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
)


def wedge(u: tuple[int, int, int, int], w: tuple[int, int, int, int]) -> tuple[int, ...]:
    return (
        u[0] * w[1] - u[1] * w[0],
        u[0] * w[2] - u[2] * w[0],
        u[0] * w[3] - u[3] * w[0],
        u[1] * w[2] - u[2] * w[1],
        u[1] * w[3] - u[3] * w[1],
        u[2] * w[3] - u[3] * w[2],
    )


def hinge_bivector(i: int, j: int, k: int) -> tuple[int, ...]:
    vi, vj, vk = VERTICES[i], VERTICES[j], VERTICES[k]
    u = (vj[0] - vi[0], vj[1] - vi[1], vj[2] - vi[2], vj[3] - vi[3])
    w = (vk[0] - vi[0], vk[1] - vi[1], vk[2] - vi[2], vk[3] - vi[3])
    return wedge(u, w)


def pfaffian(b: tuple[int, ...]) -> int:
    return b[0] * b[5] - b[1] * b[4] + b[2] * b[3]


def add_bivector(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))


def hinges() -> list[tuple[int, int, int]]:
    return [
        (i, j, k)
        for i in range(5)
        for j in range(i + 1, 5)
        for k in range(j + 1, 5)
    ]


def tetrahedra() -> list[tuple[int, int, int, int]]:
    return [
        (a, b, c, d)
        for a in range(5)
        for b in range(a + 1, 5)
        for c in range(b + 1, 5)
        for d in range(c + 1, 5)
    ]


def cayley_so4_xy() -> list[list[Fraction]]:
    return [
        [Fraction(3, 5), Fraction(-4, 5), Fraction(0), Fraction(0)],
        [Fraction(4, 5), Fraction(3, 5), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
    ]


def witness() -> dict[str, int | Fraction | tuple[Fraction, Fraction]]:
    hs = hinges()
    tets = tetrahedra()
    single_max = max(abs(pfaffian(hinge_bivector(*h))) for h in hs)
    intra_max = 0
    closure_max = 0
    for tet in tets:
        faces = [
            (tet[1], tet[2], tet[3]),
            (tet[0], tet[2], tet[3]),
            (tet[0], tet[1], tet[3]),
            (tet[0], tet[1], tet[2]),
        ]
        for p in range(4):
            for q in range(p + 1, 4):
                b_sum = add_bivector(hinge_bivector(*faces[p]), hinge_bivector(*faces[q]))
                intra_max = max(intra_max, abs(pfaffian(b_sum)))
        vec_sum = [0] * 6
        for m, f in enumerate(faces):
            sign = 1 if m % 2 == 0 else -1
            bf = hinge_bivector(*f)
            for idx in range(6):
                vec_sum[idx] += sign * bf[idx]
        closure_max = max(closure_max, max(abs(x) for x in vec_sum))

    opposite_nonzero = 0
    for p in range(len(hs)):
        for q in range(p + 1, len(hs)):
            if pfaffian(add_bivector(hinge_bivector(*hs[p]), hinge_bivector(*hs[q]))) != 0:
                opposite_nonzero += 1

    d4 = (1, -1, 1, -1, 1)
    d3_d4_max = 0
    for h in hs:
        coeff = 0
        for t_idx, tet in enumerate(tets):
            faces = [
                (tet[1], tet[2], tet[3]),
                (tet[0], tet[2], tet[3]),
                (tet[0], tet[1], tet[3]),
                (tet[0], tet[1], tet[2]),
            ]
            for m, f in enumerate(faces):
                if f == h:
                    coeff += (1 if m % 2 == 0 else -1) * d4[t_idx]
        d3_d4_max = max(d3_d4_max, abs(coeff))

    u = cayley_so4_xy()
    trace_u = sum(u[i][i] for i in range(4))
    coord_area = Fraction(1, 2)
    outer_area_sq = Fraction(3, 4)
    coord_turn_deficit = Fraction(1, 12)
    coord_regge_action_turns = 6 * coord_area * coord_turn_deficit
    hinge_deficit_interval = (
        Fraction(523_598_775, 1_000_000_000),
        Fraction(523_598_776, 1_000_000_000),
    )
    return {
        "boundary_tetrahedra": len(tets),
        "triangular_hinges": len(hs),
        "single_hinge_pfaffian_max": single_max,
        "intra_tetrahedral_pfaffian_max": intra_max,
        "opposite_hinge_nonzero_pairs": opposite_nonzero,
        "tetrahedral_closure_max_norm": closure_max,
        "chain_boundary_squared_max": d3_d4_max,
        "coordinate_hinge_area": coord_area,
        "outer_hinge_area_sq": outer_area_sq,
        "coordinate_regge_action_turns": coord_regge_action_turns,
        "cayley_so4_trace": trace_u,
        "hinge_deficit_interval": hinge_deficit_interval,
    }


def reject_universal_bivector_simplicity() -> None:
    b012 = hinge_bivector(0, 1, 2)
    b034 = hinge_bivector(0, 3, 4)
    if pfaffian(add_bivector(b012, b034)) != 0:
        raise ValueError("opposite hinges [0,1,2] and [0,3,4] have Pfaffian 1 and are not cross-simple")


def reject_unproved_eh_action_bound(claim: str) -> None:
    if "|S_Regge - S_EH|" in claim or "Einstein-Hilbert" in claim:
        raise ValueError("a single 4-simplex does not establish a continuum Einstein-Hilbert error bound")
