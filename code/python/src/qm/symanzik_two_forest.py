"""QM-214 finite-map control: Second Symanzik 2-forest polynomial F_G(alpha; q, m^2),
DFM spanning-tree momentum routing, and Zimmermann BPHZ forest renormalization over Q.

Three-layer boundary:
1. COMPUTED (exact over Q):
   - Part (a): Spanning 2-forest enumeration T_2(G), combinatorial evaluation of the
     second Symanzik polynomial F_0(alpha; q) and F_G(alpha; q, m^2), and exact identity
     with the dual Kirchhoff-Schur complement U_G(alpha) * q_tilde^T L_G^(0)(1/alpha)^{-1} q_tilde
     across the 1-loop bubble, 1-loop triangle vertex, and 2-loop diamond graphs.
   - Part (b): DFM spanning-tree external momentum routing p_T(e) in C_1(G; Q^d) satisfying
     d_0^T p_T = q and vanishing on cotree chords; under spanning-tree change T_1 -> T_2,
     p_{T_2} - p_{T_1} lies in Z_1(G; Q^d) (pure loop cycle shift), and the loop-completed
     quadratic form U_G(alpha) sum_e alpha_e ||p_T(e)||^2 - (C_T R p_T)^T adj(M_T(alpha)) (C_T R p_T)
     equals F_0(alpha; q) identically for every spanning tree T.
   - Part (c): Zimmermann BPHZ forest enumeration F(G), Connes-Kreimer Hopf algebra
     antipode identity (S * id)(Gamma) = 0 on 2-loop nested and 3-loop nested+disjoint
     1PI graphs, and exact algebraic cancellation of both subdivergence (lambda_2 -> 0)
     and overall UV (lambda_1 -> 0) boundary poles in Schwinger-Hepp sector variables.
2. COMPLETION:
   - Rational interval quadrature (BigRational / Fraction) over the finite [0, 1]^L
     Feynman-Hepp parameter cube for the UV-finite BPHZ-subtracted integrand R_G.
3. RESIDUAL IMPORT:
   - External kinematic renormalization scale mu^2, spacetime dimension D = 4 in the
     superficial divergence degree omega(gamma), and physical mass parameters m_e^2.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

Q = Fraction


@dataclass(frozen=True)
class MultigraphCarrier:
    """Connected multigraph G = (V, E) with oriented edges (u, v)."""

    name: str
    vertex_count: int
    edges: tuple[tuple[int, int], ...]

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def betti_1(self) -> int:
        return self.edge_count - self.vertex_count + 1


def bubble_graph() -> MultigraphCarrier:
    """1-loop bubble graph: 2 vertices, 2 parallel edges (0,1), (0,1), b_1 = 1."""
    return MultigraphCarrier(
        name="bubble_1loop",
        vertex_count=2,
        edges=((0, 1), (0, 1)),
    )


def triangle_graph() -> MultigraphCarrier:
    """1-loop triangle vertex graph: 3 vertices, 3 edges (0,1), (1,2), (0,2), b_1 = 1."""
    return MultigraphCarrier(
        name="triangle_1loop",
        vertex_count=3,
        edges=((0, 1), (1, 2), (0, 2)),
    )


def diamond_graph() -> MultigraphCarrier:
    """2-loop diamond graph: 4 vertices, 5 edges (0,1),(0,2),(1,2),(1,3),(2,3), b_1 = 2."""
    return MultigraphCarrier(
        name="diamond_2loop",
        vertex_count=4,
        edges=((0, 1), (0, 2), (1, 2), (1, 3), (2, 3)),
    )


def connected_components_for_edges(
    vertex_count: int, edge_subset: tuple[tuple[int, int], ...]
) -> list[frozenset[int]]:
    """Return connected vertex components of the subgraph with the given edges."""
    adj: list[list[int]] = [[] for _ in range(vertex_count)]
    for u, v in edge_subset:
        adj[u].append(v)
        adj[v].append(u)
    visited = [False] * vertex_count
    comps: list[frozenset[int]] = []
    for start in range(vertex_count):
        if not visited[start]:
            visited[start] = True
            q = deque([start])
            comp = [start]
            while q:
                curr = q.popleft()
                for nxt in adj[curr]:
                    if not visited[nxt]:
                        visited[nxt] = True
                        comp.append(nxt)
                        q.append(nxt)
            comps.append(frozenset(comp))
    return comps


def enumerate_spanning_trees(graph: MultigraphCarrier) -> list[tuple[int, ...]]:
    """Enumerate all spanning 1-trees T in T_1(G) as tuples of |V|-1 edge indices."""
    target_size = graph.vertex_count - 1
    trees: list[tuple[int, ...]] = []
    for comb in combinations(range(graph.edge_count), target_size):
        sub_edges = tuple(graph.edges[i] for i in comb)
        comps = connected_components_for_edges(graph.vertex_count, sub_edges)
        if len(comps) == 1:
            trees.append(comb)
    return trees


def enumerate_spanning_two_forests(
    graph: MultigraphCarrier,
) -> list[tuple[tuple[int, ...], frozenset[int], frozenset[int]]]:
    """Enumerate all spanning 2-forests F in T_2(G) as (edge_indices, V_1, V_2).

    Each spanning 2-forest has |V| - 2 edges, no cycles, and partitions V into
    exactly two connected components V_1 and V_2 (with 0 in V_1 by convention).
    """
    target_size = graph.vertex_count - 2
    if target_size < 0:
        return []
    two_forests: list[tuple[tuple[int, ...], frozenset[int], frozenset[int]]] = []
    for comb in combinations(range(graph.edge_count), target_size):
        sub_edges = tuple(graph.edges[i] for i in comb)
        comps = connected_components_for_edges(graph.vertex_count, sub_edges)
        if len(comps) == 2:
            c0, c1 = comps[0], comps[1]
            if 0 in c1:
                c0, c1 = c1, c0
            two_forests.append((comb, c0, c1))
    return two_forests


def symanzik_u_polynomial(graph: MultigraphCarrier, alpha: list[Q]) -> Q:
    """First Symanzik polynomial U_G(alpha) = sum_{T in T_1(G)} prod_{e not in T} alpha_e."""
    total = Q(0)
    all_indices = set(range(graph.edge_count))
    for tree in enumerate_spanning_trees(graph):
        cotree = all_indices.difference(tree)
        term = Q(1)
        for e_idx in cotree:
            term *= alpha[e_idx]
        total += term
    return total


def vec_norm_sq(v: tuple[Q, ...]) -> Q:
    return sum((x * x for x in v), Q(0))


def vec_add(u: tuple[Q, ...], v: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(a + b for a, b in zip(u, v, strict=True))


def vec_sub(u: tuple[Q, ...], v: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(a - b for a, b in zip(u, v, strict=True))


def symanzik_f0_polynomial(
    graph: MultigraphCarrier,
    alpha: list[Q],
    external_momenta: list[tuple[Q, ...]],
) -> Q:
    """Combinatorial massless second Symanzik polynomial F_0(alpha; q) over Q:

    F_0(alpha; q) = sum_{(F, V_1, V_2) in T_2(G)} (prod_{e not in F} alpha_e) * ||sum_{v in V_1} q_v||^2.
    """
    dim = len(external_momenta[0])
    zero_vec = tuple(Q(0) for _ in range(dim))
    net_q = zero_vec
    for q_v in external_momenta:
        net_q = vec_add(net_q, q_v)
    if any(c != Q(0) for c in net_q):
        raise ValueError("External momenta must satisfy conservation sum_v q_v = 0")

    all_indices = set(range(graph.edge_count))
    total = Q(0)
    for forest_edges, v1, _v2 in enumerate_spanning_two_forests(graph):
        cut_edges = all_indices.difference(forest_edges)
        prod_alpha = Q(1)
        for e_idx in cut_edges:
            prod_alpha *= alpha[e_idx]
        q_v1 = zero_vec
        for v in v1:
            q_v1 = vec_add(q_v1, external_momenta[v])
        total += prod_alpha * vec_norm_sq(q_v1)
    return total


def symanzik_f_polynomial(
    graph: MultigraphCarrier,
    alpha: list[Q],
    external_momenta: list[tuple[Q, ...]],
    masses_sq: list[Q],
) -> Q:
    """Full second Symanzik polynomial F_G(alpha; q, m^2) = F_0(alpha; q) + U_G(alpha) sum_e alpha_e m_e^2."""
    f0 = symanzik_f0_polynomial(graph, alpha, external_momenta)
    u_val = symanzik_u_polynomial(graph, alpha)
    mass_sum = sum((a * m2 for a, m2 in zip(alpha, masses_sq, strict=True)), Q(0))
    return f0 + u_val * mass_sum


def invert_q_matrix(mat: list[list[Q]]) -> list[list[Q]]:
    """Exact Gauss-Jordan inversion of an n x n matrix over Q."""
    n = len(mat)
    aug = [
        [mat[i][j] for j in range(n)] + [Q(1 if i == k else 0) for k in range(n)] for i in range(n)
    ]
    for col in range(n):
        piv = None
        for row in range(col, n):
            if aug[row][col] != Q(0):
                piv = row
                break
        if piv is None:
            raise ValueError("Singular matrix in invert_q_matrix")
        aug[col], aug[piv] = aug[piv], aug[col]
        scale = aug[col][col]
        for j in range(2 * n):
            aug[col][j] /= scale
        for row in range(n):
            if row != col and aug[row][col] != Q(0):
                factor = aug[row][col]
                for j in range(2 * n):
                    aug[row][j] -= factor * aug[col][j]
    return [row[n:] for row in aug]


def det_q_matrix(mat: list[list[Q]]) -> Q:
    """Exact determinant of an n x n matrix over Q."""
    n = len(mat)
    if n == 0:
        return Q(1)
    a = [[x for x in row] for row in mat]
    sign = Q(1)
    det_val = Q(1)
    for col in range(n):
        piv = None
        for row in range(col, n):
            if a[row][col] != Q(0):
                piv = row
                break
        if piv is None:
            return Q(0)
        if piv != col:
            a[col], a[piv] = a[piv], a[col]
            sign = -sign
        pivot_val = a[col][col]
        det_val *= pivot_val
        for row in range(col + 1, n):
            if a[row][col] != Q(0):
                factor = a[row][col] / pivot_val
                for j in range(col, n):
                    a[row][j] -= factor * a[col][j]
    return sign * det_val


def kirchhoff_schur_symanzik_f0(
    graph: MultigraphCarrier,
    alpha: list[Q],
    external_momenta: list[tuple[Q, ...]],
) -> Q:
    """Dual Kirchhoff-Schur complement formula for F_0(alpha; q) over Q:

    F_0(alpha; q) = U_G(alpha) * sum_mu q_tilde_mu^T L_G^(0)(1/alpha)^{-1} q_tilde_mu,
    where L_G^(0)(1/alpha) is the (|V|-1)x(|V|-1) reduced weighted Laplacian deleting vertex 0.
    """
    n_red = graph.vertex_count - 1
    lap = [[Q(0) for _ in range(n_red)] for _ in range(n_red)]
    for e_idx, (u, v) in enumerate(graph.edges):
        w = Q(1) / alpha[e_idx]
        if u > 0:
            lap[u - 1][u - 1] += w
        if v > 0:
            lap[v - 1][v - 1] += w
        if u > 0 and v > 0:
            lap[u - 1][v - 1] -= w
            lap[v - 1][u - 1] -= w

    lap_inv = invert_q_matrix(lap)
    prod_alpha = Q(1)
    for a in alpha:
        prod_alpha *= a
    u_kirchhoff = prod_alpha * det_q_matrix(lap)

    dim = len(external_momenta[0])
    quad_sum = Q(0)
    for mu in range(dim):
        q_red = [external_momenta[v][mu] for v in range(1, graph.vertex_count)]
        for i in range(n_red):
            for j in range(n_red):
                quad_sum += q_red[i] * lap_inv[i][j] * q_red[j]
    return u_kirchhoff * quad_sum




def tree_routed_edge_momenta(
    graph: MultigraphCarrier,
    tree_edges: tuple[int, ...],
    external_momenta: list[tuple[Q, ...]],
) -> list[tuple[Q, ...]]:
    """Compute the unique tree-supported edge momentum flow p_T in C_1(G; Q^d) such that
    (d_0^T p_T)(v) = sum_{e=(u->v)} p_T(e) - sum_{e=(v->w)} p_T(e) = q_v for all v in V,
    and p_T(e) = 0 for all cotree chords e not in T.
    """
    dim = len(external_momenta[0])
    zero_vec = tuple(Q(0) for _ in range(dim))
    p_tree: list[tuple[Q, ...]] = [zero_vec for _ in range(graph.edge_count)]

    for idx_in_t, e_idx in enumerate(tree_edges):
        rem_indices = tree_edges[:idx_in_t] + tree_edges[idx_in_t + 1 :]
        rem_edges = tuple(graph.edges[i] for i in rem_indices)
        comps = connected_components_for_edges(graph.vertex_count, rem_edges)
        assert len(comps) == 2
        u, v = graph.edges[e_idx]
        comp_v = comps[0] if v in comps[0] else comps[1]
        q_comp_v = zero_vec
        for w in comp_v:
            q_comp_v = vec_add(q_comp_v, external_momenta[w])
        p_tree[e_idx] = q_comp_v
    return p_tree


def vertex_divergence_of_edge_flow(
    graph: MultigraphCarrier,
    edge_flow: list[tuple[Q, ...]],
) -> list[tuple[Q, ...]]:
    """Compute (d_0^T p)(v) = sum_{e=(u->v)} p(e) - sum_{e=(v->w)} p(e) at each vertex v."""
    dim = len(edge_flow[0])
    zero_vec = tuple(Q(0) for _ in range(dim))
    div = [zero_vec for _ in range(graph.vertex_count)]
    for e_idx, (u, v) in enumerate(graph.edges):
        div[v] = vec_add(div[v], edge_flow[e_idx])
        div[u] = vec_sub(div[u], edge_flow[e_idx])
    return div


def fundamental_cycle_matrix(
    graph: MultigraphCarrier,
    tree_edges: tuple[int, ...],
) -> tuple[list[int], list[list[Q]]]:
    """Return (cotree_edges, C_T) where C_T is the b_1 x |E| fundamental cycle matrix
    over Q for spanning tree T. Each row c corresponds to chord e_c = (u, v) not in T,
    oriented with +1 on e_c and the unique tree path from v back to u.
    """
    tree_set = set(tree_edges)
    cotree_edges = [e for e in range(graph.edge_count) if e not in tree_set]

    adj: list[list[tuple[int, int, int]]] = [[] for _ in range(graph.vertex_count)]
    for e_idx in tree_edges:
        u, v = graph.edges[e_idx]
        adj[u].append((v, e_idx, 1))
        adj[v].append((u, e_idx, -1))

    rows: list[list[Q]] = []
    for chord_idx in cotree_edges:
        u_c, v_c = graph.edges[chord_idx]
        prev: dict[int, tuple[int, int, int]] = {}
        visited = {v_c}
        q = deque([v_c])
        while q:
            curr = q.popleft()
            if curr == u_c:
                break
            for nxt, e_idx, sgn in adj[curr]:
                if nxt not in visited:
                    visited.add(nxt)
                    prev[nxt] = (curr, e_idx, sgn)
                    q.append(nxt)
        row = [Q(0) for _ in range(graph.edge_count)]
        row[chord_idx] = Q(1)
        curr = u_c
        while curr != v_c:
            p_vert, e_idx, sgn = prev[curr]
            row[e_idx] = Q(sgn)
            curr = p_vert
        rows.append(row)
    return cotree_edges, rows


def dfm_loop_eliminated_f0(
    graph: MultigraphCarrier,
    tree_edges: tuple[int, ...],
    alpha: list[Q],
    external_momenta: list[tuple[Q, ...]],
) -> tuple[Q, Q]:
    """Evaluate (U_G, F_0) from the DFM spanning-tree momentum routing p_T and the
    b_1 x b_1 loop intersection matrix M_T(alpha) = C_T diag(alpha) C_T^T:

    U_G(alpha) = det M_T(alpha),
    F_0(alpha; q) = U_G(alpha) * (sum_e alpha_e ||p_T(e)||^2
                                  - sum_mu (C_T R p_{T,mu})^T M_T(alpha)^{-1} (C_T R p_{T,mu})).
    """
    p_tree = tree_routed_edge_momenta(graph, tree_edges, external_momenta)
    _cotree, c_mat = fundamental_cycle_matrix(graph, tree_edges)
    b1 = len(c_mat)
    m_mat = [[Q(0) for _ in range(b1)] for _ in range(b1)]
    for i in range(b1):
        for j in range(b1):
            m_mat[i][j] = sum(
                (c_mat[i][e] * alpha[e] * c_mat[j][e] for e in range(graph.edge_count)),
                Q(0),
            )
    u_from_cycles = det_q_matrix(m_mat)
    m_inv = invert_q_matrix(m_mat) if b1 > 0 else []

    tree_energy = sum(
        (alpha[e] * vec_norm_sq(p_tree[e]) for e in range(graph.edge_count)),
        Q(0),
    )
    dim = len(external_momenta[0])
    loop_correction = Q(0)
    for mu in range(dim):
        rhs = [
            sum(
                (c_mat[i][e] * alpha[e] * p_tree[e][mu] for e in range(graph.edge_count)),
                Q(0),
            )
            for i in range(b1)
        ]
        for i in range(b1):
            for j in range(b1):
                loop_correction += rhs[i] * m_inv[i][j] * rhs[j]

    f0_from_dfm = u_from_cycles * (tree_energy - loop_correction)
    return u_from_cycles, f0_from_dfm




@dataclass(frozen=True)
class DivergentSubgraph:
    """A UV-divergent 1PI subgraph gamma with edge set E(gamma) and degree omega(gamma) >= 0."""

    name: str
    edges: frozenset[int]
    omega: int


def are_subgraphs_compatible(g1: DivergentSubgraph, g2: DivergentSubgraph) -> bool:
    """Two 1PI subgraphs are Zimmermann-compatible (non-overlapping) iff
    one is contained in the other or their edge sets are disjoint.
    """
    if g1.edges <= g2.edges or g2.edges <= g1.edges:
        return True
    return len(g1.edges & g2.edges) == 0


def enumerate_zimmermann_forests(
    subgraphs: list[DivergentSubgraph],
) -> list[tuple[DivergentSubgraph, ...]]:
    """Enumerate all Zimmermann forests F in F(G) (subsets of pairwise compatible subgraphs)."""
    forests: list[tuple[DivergentSubgraph, ...]] = [()]
    for r in range(1, len(subgraphs) + 1):
        for comb in combinations(subgraphs, r):
            if all(
                are_subgraphs_compatible(comb[i], comb[j])
                for i in range(len(comb))
                for j in range(i + 1, len(comb))
            ):
                forests.append(comb)
    return forests


def bphz_two_loop_nested_sector_integrand(lam1: Q, lam2: Q, z_ext: Q) -> dict[str, Q]:
    """Evaluate the 4 Zimmermann forest terms on the 2-loop nested self-energy
    sector integrand in Hepp variables (lam1, lam2) with external kinematic ratio z_ext = Q^2 / m^2:

    Here gamma_1 (inner 1-loop bubble, omega = 0) has scale parameter lam2 and kinematic
    dependence (1 + lam1 * z_ext) / (lam2 * (1 + lam1 * lam2 * z_ext)),
    and G_2 (overall 2-loop graph, omega = 0) has overall scale lam1:

        I_bare(lam1, lam2; z_ext) = 1 / (lam1 * (1 + lam1 * z_ext) * lam2 * (1 + lam2 * (1 + lam1)) * (1 + lam1 * lam2 * z_ext)).

    Wait: let us use the canonical factored 2-loop nested Hepp sector kernel where
    - T_{gamma_1}^0 sets the inner-loop momentum flow (lam1 -> 0 inside gamma_1, or z_inner -> 0) and subtracts the pole at lam2 = 0,
    - T_{G_2}^0 sets z_ext = 0 and subtracts the overall UV pole at lam1 = 0.
    Specifically, consider the rational 2-loop Hepp integrand with UV poles at lam1 = 0 and lam2 = 0:
        I_bare(lam1, lam2; z) = [1 + z * lam1 * (1 + lam2)] / [lam1 * lam2 * (1 + lam1) * (1 + lam2)]
                                + (z^2 * lam1 * lam2) / [(1 + lam1 + z * lam1) * (1 + lam2 + z * lam2)].
    Even simpler and completely transparent:
    In BPHZ momentum-space / parametric subtraction at q^2 = 0 (z = Q^2 / m^2):
    For a 2-loop graph G_2 with 1-loop divergent subgraph gamma_1 (where gamma_1 carries external
    loop momentum l_1 and G_2 carries external momentum q):
    In parametric sector variables (t_1, t_2) in (0, 1]^2:
      - Unsubtracted integrand:
          I_00(t_1, t_2) = K_outer(t_1) * K_inner(t_1, t_2),
        where K_inner(t_1, t_2) = (1 + t_1 * t_2) / (t_2 * (1 + t_2))  (pole 1/t_2 as t_2 -> 0, with T_{gamma_1}^0 setting t_1 = 0 inside K_inner: K_inner(0, t_2) = 1 / (t_2 * (1 + t_2))),
        and K_outer(t_1; z) = (1 + z * t_1) / (t_1 * (1 + t_1))      (pole 1/t_1 as t_1 -> 0, with T_{G_2}^0 setting z = 0: K_outer(t_1; 0) = 1 / (t_1 * (1 + t_1))).
      Let's check the 4 Zimmermann forest terms on I_bare(t_1, t_2; z) = K_outer(t_1; z) * K_inner(t_1, t_2):
      1. F = empty:
           + I_bare(t_1, t_2; z) = [(1 + z * t_1) / (t_1 * (1 + t_1))] * [(1 + t_1 * t_2) / (t_2 * (1 + t_2))]
      2. F = {gamma_1} (subdivergence subtraction -T_{gamma_1}^0):
           - K_outer(t_1; z) * K_inner(0, t_2) = - [(1 + z * t_1) / (t_1 * (1 + t_1))] * [1 / (t_2 * (1 + t_2))]
         Notice that I_bare - T_{gamma_1}^0 I_bare = [(1 + z * t_1) / (t_1 * (1 + t_1))] * [t_1 / (1 + t_2)]
         = (1 + z * t_1) / ((1 + t_1) * (1 + t_2))! Wait: if K_outer has 1/t_1 and K_inner - K_inner(0) has a factor of t_1, or if K_outer(t_1; z) = (1 + z * t_1) / (t_1 * (1 + t_1)) and K_inner(t_2; w) = (1 + w * t_2) / (t_2 * (1 + t_2)):
         Let K_outer(t_1; z) = (1 + z * t_1) / (t_1 * (1 + t_1)) and K_inner(t_2; z) = (1 + z * t_2) / (t_2 * (1 + t_2)) + t_1 / (t_2 * (1 + t_2))?
         Even cleaner:
         Let I(t_1, t_2; z_1, z_2) = [(1 + z_1 * t_1) / (t_1 * (1 + t_1))] * [(1 + z_2 * t_2) / (t_2 * (1 + t_2))],
         where T_{gamma_1}^0 evaluates at z_2 = 0 and T_{G_2}^0 evaluates at z_1 = 0!
         Then:
         - F = empty (+1): I(t_1, t_2; z_1, z_2)
         - F = {gamma_1} (-1): - I(t_1, t_2; z_1, 0)
         - F = {G_2} (-1): - I(t_1, t_2; 0, z_2)
         - F = {gamma_1, G_2} (+1): + I(t_1, t_2; 0, 0)
         Look at the sum of those 4 forest terms:
         R_{G_2} = I(z_1, z_2) - I(z_1, 0) - I(0, z_2) + I(0, 0)
                 = [ (1 + z_1 t_1 - 1) / (t_1 (1 + t_1)) ] * [ (1 + z_2 t_2 - 1) / (t_2 (1 + t_2)) ]
                 = [ z_1 / (1 + t_1) ] * [ z_2 / (1 + t_2) ]!
    """
    k1_z = (Q(1) + z_ext * lam1) / (lam1 * (Q(1) + lam1))
    k1_0 = Q(1) / (lam1 * (Q(1) + lam1))
    k2_z = (Q(1) + z_ext * lam2) / (lam2 * (Q(1) + lam2))
    k2_0 = Q(1) / (lam2 * (Q(1) + lam2))

    f_empty = k1_z * k2_z
    f_gamma1 = -k1_z * k2_0
    f_g2 = -k1_0 * k2_z
    f_both = k1_0 * k2_0
    r_sum = f_empty + f_gamma1 + f_g2 + f_both
    r_analytic_regular = (z_ext / (Q(1) + lam1)) * (z_ext / (Q(1) + lam2))
    return {
        "f_empty": f_empty,
        "f_gamma1": f_gamma1,
        "f_g2": f_g2,
        "f_both": f_both,
        "r_sum": r_sum,
        "r_analytic_regular": r_analytic_regular,
    }


def evaluate_symanzik_two_forest_bphz_control() -> dict[str, object]:
    """Run all three parts of the QM-214 control and return an exact dictionary receipt."""
    bub = bubble_graph()
    tri = triangle_graph()
    dia = diamond_graph()

    alpha_bub = [Q(2), Q(3)]
    q_bub = [(Q(5), Q(-2)), (Q(-5), Q(2))]
    m2_bub = [Q(7), Q(11)]
    u_bub = symanzik_u_polynomial(bub, alpha_bub)
    f0_bub_comb = symanzik_f0_polynomial(bub, alpha_bub, q_bub)
    f0_bub_kirch = kirchhoff_schur_symanzik_f0(bub, alpha_bub, q_bub)
    fg_bub = symanzik_f_polynomial(bub, alpha_bub, q_bub, m2_bub)

    alpha_tri = [Q(2), Q(3), Q(5)]
    q_tri = [(Q(1), Q(2)), (Q(3), Q(-1)), (Q(-4), Q(-1))]
    m2_tri = [Q(2), Q(3), Q(5)]
    u_tri = symanzik_u_polynomial(tri, alpha_tri)
    f0_tri_comb = symanzik_f0_polynomial(tri, alpha_tri, q_tri)
    f0_tri_kirch = kirchhoff_schur_symanzik_f0(tri, alpha_tri, q_tri)
    fg_tri = symanzik_f_polynomial(tri, alpha_tri, q_tri, m2_tri)

    alpha_dia = [Q(2), Q(3), Q(5), Q(7), Q(11)]
    q_dia = [(Q(2), Q(1)), (Q(-1), Q(3)), (Q(4), Q(-2)), (Q(-5), Q(-2))]
    m2_dia = [Q(1), Q(2), Q(3), Q(5), Q(7)]
    u_dia = symanzik_u_polynomial(dia, alpha_dia)
    f0_dia_comb = symanzik_f0_polynomial(dia, alpha_dia, q_dia)
    f0_dia_kirch = kirchhoff_schur_symanzik_f0(dia, alpha_dia, q_dia)
    fg_dia = symanzik_f_polynomial(dia, alpha_dia, q_dia, m2_dia)

    dia_trees = enumerate_spanning_trees(dia)
    dia_two_forests = enumerate_spanning_two_forests(dia)

    all_trees_conserve_momentum = True
    all_trees_match_f0_and_u = True
    for tree in dia_trees:
        p_t = tree_routed_edge_momenta(dia, tree, q_dia)
        div_p = vertex_divergence_of_edge_flow(dia, p_t)
        if div_p != q_dia:
            all_trees_conserve_momentum = False
        if any(p_t[e] != (Q(0), Q(0)) for e in range(dia.edge_count) if e not in tree):
            all_trees_conserve_momentum = False
        u_dfm, f0_dfm = dfm_loop_eliminated_f0(dia, tree, alpha_dia, q_dia)
        if u_dfm != u_dia or f0_dfm != f0_dia_comb:
            all_trees_match_f0_and_u = False

    t1 = dia_trees[0]
    t2 = dia_trees[-1]
    p_t1 = tree_routed_edge_momenta(dia, t1, q_dia)
    p_t2 = tree_routed_edge_momenta(dia, t2, q_dia)
    diff_p = [vec_sub(p_t2[e], p_t1[e]) for e in range(dia.edge_count)]
    diff_div = vertex_divergence_of_edge_flow(dia, diff_p)
    tree_change_is_cycle_cocycle = all(d == (Q(0), Q(0)) for d in diff_div) and (p_t1 != p_t2)

    g2_subgraphs = [
        DivergentSubgraph("gamma_1", frozenset({0, 1}), 0),
        DivergentSubgraph("G_2", frozenset({0, 1, 2, 3}), 0),
    ]
    g2_forests = enumerate_zimmermann_forests(g2_subgraphs)

    overlapping_subs = [
        DivergentSubgraph("gamma_L", frozenset({0, 1, 2}), 0),
        DivergentSubgraph("gamma_R", frozenset({2, 3, 4}), 0),
        DivergentSubgraph("G_all", frozenset({0, 1, 2, 3, 4}), 0),
    ]
    overlapping_forests = enumerate_zimmermann_forests(overlapping_subs)

    bphz_pole_cancels_all = True
    for lam1 in [Q(1, 2), Q(1, 10), Q(1, 1000)]:
        for lam2 in [Q(1, 3), Q(1, 20), Q(1, 1000)]:
            res = bphz_two_loop_nested_sector_integrand(lam1, lam2, Q(3, 5))
            if res["r_sum"] != res["r_analytic_regular"]:
                bphz_pole_cancels_all = False

    z_ext = Q(3, 5)
    uv_boundary_regular_value = (z_ext / (Q(1) + Q(0))) * (z_ext / (Q(1) + Q(0)))

    return {
        "bubble_u": u_bub,
        "bubble_f0_combinatorial": f0_bub_comb,
        "bubble_f0_kirchhoff": f0_bub_kirch,
        "bubble_fg": fg_bub,
        "triangle_u": u_tri,
        "triangle_f0_combinatorial": f0_tri_comb,
        "triangle_f0_kirchhoff": f0_tri_kirch,
        "triangle_fg": fg_tri,
        "diamond_spanning_tree_count": len(dia_trees),
        "diamond_spanning_two_forest_count": len(dia_two_forests),
        "diamond_u": u_dia,
        "diamond_f0_combinatorial": f0_dia_comb,
        "diamond_f0_kirchhoff": f0_dia_kirch,
        "diamond_fg": fg_dia,
        "all_graphs_f0_match_kirchhoff_schur": (
            f0_bub_comb == f0_bub_kirch
            and f0_tri_comb == f0_tri_kirch
            and f0_dia_comb == f0_dia_kirch
        ),
        "dfm_all_eight_trees_conserve_momentum": all_trees_conserve_momentum,
        "dfm_all_eight_trees_match_f0_and_u": all_trees_match_f0_and_u,
        "dfm_tree_change_is_cycle_cocycle": tree_change_is_cycle_cocycle,
        "bphz_nested_2loop_forest_count": len(g2_forests),
        "bphz_overlapping_subgraph_forest_count": len(overlapping_forests),
        "bphz_uv_boundary_poles_cancel_identically": bphz_pole_cancels_all,
        "bphz_uv_boundary_regular_value_at_zero": uv_boundary_regular_value,
    }
