"""Substantial-vs-artificial & hierarchical non-Abelian DFM control for QM-213.

AuthorityEffect: None.

Computes over exact rational matrices ``GL(2, Q)`` and the Borel subgroup
``B_2(Q) = T ltia N`` on the 4-vertex punctured diamond cell complex and the
5-vertex extended diamond poset ``P_5 = {0 < {1, 2} < 3 < 4}``:

1. Substantial vs. artificial symmetry classification via ``LocalGreen`` /
   ``GlobalRed`` patch cohomology (``GaugeTrivial`` pure gauge vs.
   ``FlatNontrivial`` punctured-cycle holonomy vs. ``Curved`` face holonomy,
   plus residual ambiguity of the second kind under spanning-tree changes
   ``T_1 -> T_2``).
2. Two-stage hierarchical non-Abelian subgroup dressing ``N <| B_2(Q)`` with
   normal unipotent subgroup ``N`` and diagonal quotient torus ``T = B/N``:
   Stage 1 ``u_N : V -> N`` reduces every tree edge to the diagonal quotient
   ``T`` while preserving ``pi_{B/N}`` on all edges; Stage 2 ``u_T : V -> T``
   neutralizes the residual diagonal tree connection and reproduces the full
   tree-gauge residual ``u_T(v) u_N(v) = T_B(v)^{-1}``.
3. Incidence DGA curvature covariance ``K^u = b A^u + A^u cup A^u = u K u^{-1}``
   and the exact discrete Bianchi identity ``D_{A^u} K^u = 0`` in ``C^3(P_5)``
   under Stage 1 unipotent dressing ``N`` and Stage 2 quotient transformations
   ``B/N``.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

Mat2 = Tuple[Tuple[Fraction, Fraction], Tuple[Fraction, Fraction]]


def mat2(
    a00: int | Fraction, a01: int | Fraction, a10: int | Fraction, a11: int | Fraction
) -> Mat2:
    """Construct an exact 2x2 rational matrix."""
    return (
        (Fraction(a00), Fraction(a01)),
        (Fraction(a10), Fraction(a11)),
    )


def id2() -> Mat2:
    """Return the 2x2 identity matrix over Q."""
    return mat2(1, 0, 0, 1)


def zero2() -> Mat2:
    """Return the 2x2 zero matrix over Q."""
    return mat2(0, 0, 0, 0)


def borel2(d1: int | Fraction, b: int | Fraction, d2: int | Fraction) -> Mat2:
    """Construct an upper-triangular 2x2 Borel matrix [[d1, b], [0, d2]]."""
    if Fraction(d1) == 0 or Fraction(d2) == 0:
        raise ValueError("Borel matrix diagonal entries must be non-zero.")
    return mat2(d1, b, 0, d2)


def mat2_add(a: Mat2, b: Mat2) -> Mat2:
    """Exact 2x2 matrix addition."""
    return (
        (a[0][0] + b[0][0], a[0][1] + b[0][1]),
        (a[1][0] + b[1][0], a[1][1] + b[1][1]),
    )


def mat2_sub(a: Mat2, b: Mat2) -> Mat2:
    """Exact 2x2 matrix subtraction."""
    return (
        (a[0][0] - b[0][0], a[0][1] - b[0][1]),
        (a[1][0] - b[1][0], a[1][1] - b[1][1]),
    )


def mat2_mul(a: Mat2, b: Mat2) -> Mat2:
    """Exact 2x2 matrix multiplication."""
    return (
        (
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ),
        (
            a[1][0] * b[0][0] + a[1][1] * b[1][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ),
    )


def mat2_det(a: Mat2) -> Fraction:
    """Exact determinant of a 2x2 rational matrix."""
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def mat2_trace(a: Mat2) -> Fraction:
    """Exact trace of a 2x2 rational matrix."""
    return a[0][0] + a[1][1]


def mat2_inv(a: Mat2) -> Mat2:
    """Exact inverse of an invertible 2x2 rational matrix."""
    det = mat2_det(a)
    if det == 0:
        raise ValueError("Singular 2x2 matrix.")
    return (
        (a[1][1] / det, -a[0][1] / det),
        (-a[1][0] / det, a[0][0] / det),
    )


def borel2_torus_part(m: Mat2) -> Mat2:
    """Project a Borel matrix to the diagonal quotient torus T = B/N."""
    return mat2(m[0][0], 0, 0, m[1][1])


def borel2_unipotent_part(m: Mat2) -> Mat2:
    """Extract the right unipotent factor n(M) = diag(d1, d2)^{-1} M in N."""
    return mat2(1, m[0][1] / m[0][0], 0, 1)


def is_unit_upper_triangular(m: Mat2) -> bool:
    """Check whether m lies in the normal unipotent subgroup N <| B_2(Q)."""
    return m[0][0] == 1 and m[1][0] == 0 and m[1][1] == 1


def is_diagonal_2x2(m: Mat2) -> bool:
    """Check whether m lies in the diagonal torus subgroup T subset B_2(Q)."""
    return m[0][1] == 0 and m[1][0] == 0


DIAMOND_EDGES: Tuple[Tuple[int, int], ...] = (
    (0, 1),
    (1, 2),
    (0, 2),
    (2, 3),
    (1, 3),
)


def gauge_transform_edges(
    edges: Sequence[Tuple[int, int]],
    edge_mats: Sequence[Mat2],
    vertex_gauge: Sequence[Mat2],
) -> List[Mat2]:
    """Compute U'_e = g(t) U_e g(s)^{-1} for every directed edge e = (s -> t)."""
    g_inv = [mat2_inv(g) for g in vertex_gauge]
    return [
        mat2_mul(mat2_mul(vertex_gauge[t], mat), g_inv[s]) for (s, t), mat in zip(edges, edge_mats)
    ]


def tree_transport_and_dressing(
    vertex_count: int,
    edges: Sequence[Tuple[int, int]],
    edge_mats: Sequence[Mat2],
    tree_edges: Sequence[int],
    root: int = 0,
) -> Tuple[List[Mat2], List[Mat2], List[Mat2]]:
    """Compute root-to-vertex transport T(v), dressing u_T(v) = T(v)^{-1}, and residual R_e."""
    adj: List[List[Tuple[int, int, int]]] = [[] for _ in range(vertex_count)]
    for e_idx in tree_edges:
        s, t = edges[e_idx]
        adj[s].append((t, e_idx, 1))
        adj[t].append((s, e_idx, -1))
    transport: List[Mat2] = [id2() for _ in range(vertex_count)]
    visited = [False] * vertex_count
    visited[root] = True
    queue: deque[int] = deque([root])
    while queue:
        u = queue.popleft()
        for v, e_idx, direction in adj[u]:
            if not visited[v]:
                visited[v] = True
                step_mat = edge_mats[e_idx] if direction == 1 else mat2_inv(edge_mats[e_idx])
                transport[v] = mat2_mul(step_mat, transport[u])
                queue.append(v)
    dressing = [mat2_inv(t) for t in transport]
    residual = gauge_transform_edges(edges, edge_mats, dressing)
    return transport, dressing, residual


def walk_holonomy(
    edge_mats: Sequence[Mat2],
    steps: Sequence[Tuple[int, int]],
) -> Mat2:
    """Compute path-ordered product along oriented steps (edge_index, direction)."""
    acc = id2()
    for e_idx, direction in steps:
        step_mat = edge_mats[e_idx] if direction == 1 else mat2_inv(edge_mats[e_idx])
        acc = mat2_mul(step_mat, acc)
    return acc


def classify_punctured_diamond_connection(
    edge_mats: Sequence[Mat2],
    tree_edges: Sequence[int] = (0, 2, 3),
) -> str:
    """Classify a connection on the punctured diamond into GaugeTrivial, FlatNontrivial, or Curved."""
    # Face f0 = (0 -> 1 -> 2 -> 0) uses steps (e0, +1), (e1, +1), (e2, -1)
    face_f0 = walk_holonomy(edge_mats, ((0, 1), (1, 1), (2, -1)))
    if face_f0 != id2():
        return "Curved"
    _, _, residual = tree_transport_and_dressing(4, DIAMOND_EDGES, edge_mats, tree_edges)
    if all(mat == id2() for mat in residual):
        return "GaugeTrivial"
    return "FlatNontrivial"


# ============================================================================
# Poset Restriction DGA over P_5 = {0 < {1, 2} < 3 < 4}
# ============================================================================

POSET_P5_COVERS: Tuple[Tuple[int, int], ...] = (
    (0, 1),
    (0, 2),
    (1, 3),
    (2, 3),
    (3, 4),
)

POSET_P5_LESS: Dict[int, Tuple[int, ...]] = {
    0: (1, 2, 3, 4),
    1: (3, 4),
    2: (3, 4),
    3: (4,),
    4: (),
}


def poset_p5_chains(degree: int) -> List[Tuple[int, ...]]:
    """Enumerate all strict chains [v_0, ..., v_degree] in P_5."""
    results: List[Tuple[int, ...]] = []

    def backtrack(prefix: List[int]) -> None:
        if len(prefix) == degree + 1:
            results.append(tuple(prefix))
            return
        last = prefix[-1]
        for nxt in POSET_P5_LESS[last]:
            prefix.append(nxt)
            backtrack(prefix)
            prefix.pop()

    for start in range(5):
        backtrack([start])
    return results


def flat_cover_extension_p5(
    covers: Dict[Tuple[int, int], Mat2],
) -> Tuple[bool, Dict[Tuple[int, ...], Mat2] | Tuple[int, int, Tuple[int, ...], Tuple[int, ...]]]:
    """Extend cover maps along saturated chains in P_5; refuse if two saturated paths disagree."""
    saturated_paths: Dict[Tuple[int, int], List[Tuple[int, ...]]] = {
        (0, 1): [(0, 1)],
        (0, 2): [(0, 2)],
        (1, 3): [(1, 3)],
        (2, 3): [(2, 3)],
        (3, 4): [(3, 4)],
        (0, 3): [(0, 1, 3), (0, 2, 3)],
        (1, 4): [(1, 3, 4)],
        (2, 4): [(2, 3, 4)],
        (0, 4): [(0, 1, 3, 4), (0, 2, 3, 4)],
    }
    cochain1: Dict[Tuple[int, ...], Mat2] = {}
    for pair in poset_p5_chains(1):
        u, v = pair
        paths = saturated_paths[(u, v)]
        first_prod = id2()
        for idx in range(len(paths[0]) - 1):
            first_prod = mat2_mul(first_prod, covers[(paths[0][idx], paths[0][idx + 1])])
        for other in paths[1:]:
            other_prod = id2()
            for idx in range(len(other) - 1):
                other_prod = mat2_mul(other_prod, covers[(other[idx], other[idx + 1])])
            if other_prod != first_prod:
                return False, (u, v, paths[0], other)
        cochain1[pair] = first_prod
    return True, cochain1


def dga_internal_differential(
    degree: int,
    cochain: Dict[Tuple[int, ...], Mat2],
) -> Dict[Tuple[int, ...], Mat2]:
    """Compute b(f) on chains of degree + 1 by deleting internal vertices i in 1..=degree."""
    out: Dict[Tuple[int, ...], Mat2] = {}
    for chain in poset_p5_chains(degree + 1):
        acc = zero2()
        for i in range(1, degree + 1):
            face = chain[:i] + chain[i + 1 :]
            if i % 2 == 0:
                acc = mat2_add(acc, cochain[face])
            else:
                acc = mat2_sub(acc, cochain[face])
        out[chain] = acc
    return out


def dga_cup(
    deg_f: int,
    f: Dict[Tuple[int, ...], Mat2],
    deg_g: int,
    g: Dict[Tuple[int, ...], Mat2],
) -> Dict[Tuple[int, ...], Mat2]:
    """Compute (f cup g)_{[v_0, ..., v_{p+q}]} = f_{[v_0, ..., v_p]} * g_{[v_p, ..., v_{p+q}]}."""
    out: Dict[Tuple[int, ...], Mat2] = {}
    for chain in poset_p5_chains(deg_f + deg_g):
        left = chain[: deg_f + 1]
        right = chain[deg_f:]
        out[chain] = mat2_mul(f[left], g[right])
    return out


def dga_curvature(a: Dict[Tuple[int, ...], Mat2]) -> Dict[Tuple[int, ...], Mat2]:
    """Compute K(A) = b A + A cup A in C^2(P_5)."""
    ba = dga_internal_differential(1, a)
    aa = dga_cup(1, a, 1, a)
    return {ch: mat2_add(ba[ch], aa[ch]) for ch in poset_p5_chains(2)}


def dga_covariant_differential_deg2(
    k: Dict[Tuple[int, ...], Mat2],
    a: Dict[Tuple[int, ...], Mat2],
) -> Dict[Tuple[int, ...], Mat2]:
    """Compute D_A K = b K + A cup K - K cup A in C^3(P_5)."""
    bk = dga_internal_differential(2, k)
    ak = dga_cup(1, a, 2, k)
    ka = dga_cup(2, k, 1, a)
    return {ch: mat2_sub(mat2_add(bk[ch], ak[ch]), ka[ch]) for ch in poset_p5_chains(3)}


def dga_gauge(
    degree: int,
    f: Dict[Tuple[int, ...], Mat2],
    vertex_g: Sequence[Mat2],
) -> Dict[Tuple[int, ...], Mat2]:
    """Compute (f^g)_{[v_0, ..., v_p]} = g_{v_0} f_{[v_0, ..., v_p]} g_{v_p}^{-1}."""
    g_inv = [mat2_inv(m) for m in vertex_g]
    return {ch: mat2_mul(mat2_mul(vertex_g[ch[0]], mat), g_inv[ch[-1]]) for ch, mat in f.items()}


@dataclass(frozen=True)
class Qm213NonAbelianDfmReceipt:
    """Summary receipt for the QM-213 substantial-vs-artificial & hierarchical DFM control."""

    artificial_verdict: str
    artificial_local_dressing_neutralizes_all_edges: bool
    artificial_poset_flat_cover_extension_is_ok: bool
    artificial_poset_extended_curvature_is_zero: bool
    substantial_verdict: str
    substantial_face_f0_is_local_green: bool
    substantial_tree_dressing_neutralizes_tree_only: bool
    substantial_poset_returns_path_dependent_global_red: bool
    second_kind_tree_change_intertwiner_exact: bool
    second_kind_cycle_traces_and_dets_invariant: bool
    curved_verdict: str
    stage1_u_n_all_in_normal_unipotent_subgroup: bool
    stage1_tree_edges_reduced_to_diagonal_quotient: bool
    stage1_preserves_b_mod_n_projection_on_all_edges: bool
    stage1_residual_first_kind_torus_preserves_diagonal_tree: bool
    stage2_u_t_all_in_diagonal_torus: bool
    two_stage_factorization_matches_full_tree_gauge: bool
    stage2_matches_tree_gauge_residual_exactly: bool
    dga_poset_vertex_count: int
    dga_poset_two_chain_count: int
    dga_poset_three_chain_count: int
    dga_b_squared_zero_on_a: bool
    dga_undressed_curvature_nonzero: bool
    dga_undressed_bianchi_identity_zero: bool
    dga_stage1_curvature_equals_gauged_curvature: bool
    dga_stage1_preserves_diagonal_b_mod_n_curvature: bool
    dga_stage1_bianchi_identity_zero: bool
    dga_quotient_b_mod_n_covariance_exact: bool
    dga_composite_two_stage_curvature_matches: bool
    dga_stage2_bianchi_identity_zero: bool


def run_qm213_nonabelian_dfm_control() -> Qm213NonAbelianDfmReceipt:
    """Execute the full QM-213 substantial-vs-artificial and hierarchical DFM control."""
    potentials = [
        borel2(1, 0, 1),
        borel2(2, 3, Fraction(1, 2)),
        borel2(Fraction(1, 3), -2, 3),
        borel2(Fraction(3, 2), 5, Fraction(2, 3)),
    ]
    u_art = gauge_transform_edges(DIAMOND_EDGES, [id2() for _ in range(5)], potentials)
    verdict_art = classify_punctured_diamond_connection(u_art)
    _, _, res_art = tree_transport_and_dressing(4, DIAMOND_EDGES, u_art, (0, 2, 3))
    art_all_id = all(m == id2() for m in res_art)

    chord = borel2(2, 3, Fraction(1, 2))
    base_sub = [id2(), id2(), id2(), id2(), chord]
    u_sub = gauge_transform_edges(DIAMOND_EDGES, base_sub, potentials)
    verdict_sub = classify_punctured_diamond_connection(u_sub)
    face_f0_sub = walk_holonomy(u_sub, ((0, 1), (1, 1), (2, -1)))
    _, u_t1, res_t1 = tree_transport_and_dressing(4, DIAMOND_EDGES, u_sub, (0, 2, 3))
    _, u_t2, res_t2 = tree_transport_and_dressing(4, DIAMOND_EDGES, u_sub, (0, 1, 4))
    sub_tree_only = all(res_t1[e] == id2() for e in (0, 2, 3)) and res_t1[4] != id2()

    transition_c = [mat2_mul(g2, mat2_inv(g1)) for g1, g2 in zip(u_t1, u_t2)]
    regauged_t1 = gauge_transform_edges(DIAMOND_EDGES, res_t1, transition_c)
    second_kind_intertwiner = (
        regauged_t1 == res_t2
        and all(res_t1[e] == id2() for e in (0, 2, 3))
        and all(res_t2[e] == id2() for e in (0, 1, 4))
    )
    right_loop = ((1, 1), (3, 1), (4, -1))
    hol_t1 = walk_holonomy(res_t1, right_loop)
    hol_t2 = walk_holonomy(res_t2, right_loop)
    second_kind_invariants = mat2_trace(hol_t1) == mat2_trace(hol_t2) and mat2_det(
        hol_t1
    ) == mat2_det(hol_t2)

    u_curv = [borel2(2, 1, 1), borel2(1, 2, 3), id2(), id2(), id2()]
    verdict_curv = classify_punctured_diamond_connection(u_curv)

    # Part (b): Two-stage hierarchical non-Abelian subgroup dressing N <| B_2(Q)
    borel_conn = [
        borel2(2, 3, Fraction(1, 2)),
        borel2(3, -1, 2),
        borel2(Fraction(1, 2), 4, 3),
        borel2(4, 2, Fraction(1, 3)),
        borel2(Fraction(5, 2), -3, Fraction(2, 5)),
    ]
    tree_edges = (0, 2, 3)
    t_borel, full_dressing, full_residual = tree_transport_and_dressing(
        4, DIAMOND_EDGES, borel_conn, tree_edges
    )
    u_n_vec: List[Mat2] = []
    u_t_vec: List[Mat2] = []
    for v in range(4):
        d_v = borel2_torus_part(t_borel[v])
        d_v_inv = mat2_inv(d_v)
        n_v = borel2_unipotent_part(t_borel[v])
        n_v_inv = mat2_inv(n_v)
        u_n_vec.append(mat2_mul(mat2_mul(d_v, n_v_inv), d_v_inv))
        u_t_vec.append(d_v_inv)

    conn_stage1 = gauge_transform_edges(DIAMOND_EDGES, borel_conn, u_n_vec)
    stage1_tree_diag = all(is_diagonal_2x2(conn_stage1[e]) for e in tree_edges)
    stage1_preserves_quot = all(
        borel2_torus_part(conn_stage1[e]) == borel2_torus_part(borel_conn[e]) for e in range(5)
    )
    residual_torus_gauge = [
        borel2(3, 0, Fraction(1, 5)),
        borel2(Fraction(2, 3), 0, Fraction(7, 2)),
        borel2(Fraction(5, 4), 0, Fraction(3, 7)),
        borel2(Fraction(1, 2), 0, 4),
    ]
    conn_stage1_torus = gauge_transform_edges(DIAMOND_EDGES, conn_stage1, residual_torus_gauge)
    stage1_residual_diag = all(is_diagonal_2x2(conn_stage1_torus[e]) for e in tree_edges)

    conn_stage2 = gauge_transform_edges(DIAMOND_EDGES, conn_stage1, u_t_vec)
    factorization_matches = all(
        mat2_mul(u_t_vec[v], u_n_vec[v]) == full_dressing[v] for v in range(4)
    )

    # Part (c): Poset Restriction DGA on P_5
    m01 = mat2(2, 1, 0, 1)
    m13 = mat2(1, 3, 0, 2)
    m02_flat = mat2(1, 2, 0, 2)
    m23_flat = mat2(2, 6, 0, 1)
    m34 = mat2(1, -1, 0, 1)
    ok_flat, ext_flat = flat_cover_extension_p5(
        {(0, 1): m01, (1, 3): m13, (0, 2): m02_flat, (2, 3): m23_flat, (3, 4): m34}
    )
    assert isinstance(ext_flat, dict)
    curv_flat = dga_curvature(ext_flat)
    flat_curv_zero = all(m == zero2() for m in curv_flat.values())

    ok_sub, ext_sub = flat_cover_extension_p5(
        {
            (0, 1): m01,
            (1, 3): m13,
            (0, 2): mat2(1, 1, 0, 1),
            (2, 3): mat2(2, 1, 0, 2),
            (3, 4): m34,
        }
    )
    path_dep_global_red = (not ok_sub) and ext_sub == (0, 3, (0, 1, 3), (0, 2, 3))

    a_cochain: Dict[Tuple[int, ...], Mat2] = {}
    for idx, ch in enumerate(poset_p5_chains(1)):
        step = idx + 1
        a_cochain[ch] = mat2(1 + (step % 2), step, 0, 1 + ((step + 1) % 2))

    b_a = dga_internal_differential(1, a_cochain)
    b2_a = dga_internal_differential(2, b_a)
    k_cochain = dga_curvature(a_cochain)
    bianchi_0 = dga_covariant_differential_deg2(k_cochain, a_cochain)

    u_n_p5 = [
        borel2(1, 2, 1),
        borel2(1, Fraction(-3, 2), 1),
        borel2(1, Fraction(5, 3), 1),
        borel2(1, Fraction(-7, 4), 1),
        borel2(1, Fraction(11, 5), 1),
    ]
    a_u_n = dga_gauge(1, a_cochain, u_n_p5)
    k_from_a_u_n = dga_curvature(a_u_n)
    k_gauged_u_n = dga_gauge(2, k_cochain, u_n_p5)
    bianchi_1 = dga_covariant_differential_deg2(k_from_a_u_n, a_u_n)
    stage1_preserves_diag_k = all(
        k_cochain[ch][0][0] == k_from_a_u_n[ch][0][0]
        and k_cochain[ch][1][1] == k_from_a_u_n[ch][1][1]
        for ch in poset_p5_chains(2)
    )

    t_p5 = [
        borel2(2, 0, 3),
        borel2(Fraction(1, 2), 0, Fraction(5, 3)),
        borel2(Fraction(3, 4), 0, Fraction(2, 5)),
        borel2(Fraction(5, 2), 0, Fraction(1, 3)),
        borel2(Fraction(4, 3), 0, Fraction(3, 2)),
    ]
    a_stage2 = dga_gauge(1, a_u_n, t_p5)
    k_from_a_stage2 = dga_curvature(a_stage2)
    k_gauged_stage2 = dga_gauge(2, k_from_a_u_n, t_p5)
    bianchi_2 = dga_covariant_differential_deg2(k_from_a_stage2, a_stage2)

    u_tot_p5 = [mat2_mul(t_m, n_m) for t_m, n_m in zip(t_p5, u_n_p5)]
    k_composite = dga_gauge(2, k_cochain, u_tot_p5)

    return Qm213NonAbelianDfmReceipt(
        artificial_verdict=verdict_art,
        artificial_local_dressing_neutralizes_all_edges=art_all_id,
        artificial_poset_flat_cover_extension_is_ok=ok_flat,
        artificial_poset_extended_curvature_is_zero=flat_curv_zero,
        substantial_verdict=verdict_sub,
        substantial_face_f0_is_local_green=(face_f0_sub == id2()),
        substantial_tree_dressing_neutralizes_tree_only=sub_tree_only,
        substantial_poset_returns_path_dependent_global_red=path_dep_global_red,
        second_kind_tree_change_intertwiner_exact=second_kind_intertwiner,
        second_kind_cycle_traces_and_dets_invariant=second_kind_invariants,
        curved_verdict=verdict_curv,
        stage1_u_n_all_in_normal_unipotent_subgroup=all(
            is_unit_upper_triangular(m) for m in u_n_vec
        ),
        stage1_tree_edges_reduced_to_diagonal_quotient=stage1_tree_diag,
        stage1_preserves_b_mod_n_projection_on_all_edges=stage1_preserves_quot,
        stage1_residual_first_kind_torus_preserves_diagonal_tree=stage1_residual_diag,
        stage2_u_t_all_in_diagonal_torus=all(is_diagonal_2x2(m) for m in u_t_vec),
        two_stage_factorization_matches_full_tree_gauge=factorization_matches,
        stage2_matches_tree_gauge_residual_exactly=(conn_stage2 == full_residual),
        dga_poset_vertex_count=5,
        dga_poset_two_chain_count=len(poset_p5_chains(2)),
        dga_poset_three_chain_count=len(poset_p5_chains(3)),
        dga_b_squared_zero_on_a=all(m == zero2() for m in b2_a.values()),
        dga_undressed_curvature_nonzero=any(m != zero2() for m in k_cochain.values()),
        dga_undressed_bianchi_identity_zero=all(m == zero2() for m in bianchi_0.values()),
        dga_stage1_curvature_equals_gauged_curvature=(k_from_a_u_n == k_gauged_u_n),
        dga_stage1_preserves_diagonal_b_mod_n_curvature=stage1_preserves_diag_k,
        dga_stage1_bianchi_identity_zero=all(m == zero2() for m in bianchi_1.values()),
        dga_quotient_b_mod_n_covariance_exact=(k_from_a_stage2 == k_gauged_stage2),
        dga_composite_two_stage_curvature_matches=(k_from_a_stage2 == k_composite),
        dga_stage2_bianchi_identity_zero=all(m == zero2() for m in bianchi_2.values()),
    )
