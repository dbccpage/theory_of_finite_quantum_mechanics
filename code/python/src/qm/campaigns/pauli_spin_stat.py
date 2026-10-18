"""QM-223: Identical particles, Pauli exclusion, topological spin-statistics
on finite graphs (`Conf_2(G)`), Jordan-Wigner CAR Clifford nilpotency,
Slater determinant vs. bosonic permanent, and atomic shell capacities `2*n^2`
over `Q`.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations


@dataclass(frozen=True)
class Conf2GraphSummary:
    """Topological invariants of the 2-particle unordered configuration 1-skeleton
    Conf_2^(1)(G) and Abramsky-Ghrist square 2-complex Conf_2^(2)(G).
    """

    graph_id: str
    base_vertices: int
    base_edges: int
    conf2_vertices: int
    conf2_edges: int
    conf2_components: int
    conf2_betti_1: int
    conf2_squares: int = 0
    conf2_2complex_betti_1_q: int = 0
    conf2_2complex_betti_1_f2: int = 0
    conf2_z2_torsion_rank: int = 0
    has_y_junction_exchange_cycle: bool = False
    admissible_1d_exchange_characters: tuple[str, ...] = ()


@dataclass(frozen=True)
class PauliSpinStatisticsCertificate:
    """Complete QM-223 verification certificate over exact rationals Q."""

    control_id: str
    conf2_p3: Conf2GraphSummary
    conf2_c4: Conf2GraphSummary
    conf2_k5: Conf2GraphSummary
    pauli_same_orbital_slater: Fraction
    swap_ratio_fermion: Fraction
    swap_ratio_boson: Fraction
    fermi_hole_coincidence_probability: Fraction
    hbt_boson_bunching_ratio: Fraction
    jordan_wigner_nilpotent: bool
    jordan_wigner_car_exact: bool
    jordan_wigner_fock_number_trace: Fraction
    shell_orbital_degeneracies_1_to_4: tuple[int, ...]
    shell_capacities_1_to_4: tuple[int, ...]
    noble_gas_atomic_numbers: tuple[int, ...]
    passed: bool
    conf2_y_star: Conf2GraphSummary | None = None
    conf2_k4: Conf2GraphSummary | None = None


def _rank_over_q(rows: list[list[int]], ncols: int) -> int:
    if not rows or ncols == 0:
        return 0
    mat = [[Fraction(x, 1) for x in row] for row in rows]
    rank = 0
    for col in range(ncols):
        piv = next((r for r in range(rank, len(mat)) if mat[r][col] != 0), None)
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        lead = mat[rank][col]
        mat[rank] = [val / lead for val in mat[rank]]
        for r in range(len(mat)):
            if r != rank and mat[r][col] != 0:
                factor = mat[r][col]
                mat[r] = [mat[r][k] - factor * mat[rank][k] for k in range(ncols)]
        rank += 1
    return rank


def _rank_over_f2(rows: list[list[int]], ncols: int) -> int:
    if not rows or ncols == 0:
        return 0
    mat = [[x & 1 for x in row] for row in rows]
    rank = 0
    for col in range(ncols):
        piv = next((r for r in range(rank, len(mat)) if mat[r][col] != 0), None)
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        for r in range(len(mat)):
            if r != rank and mat[r][col] != 0:
                mat[r] = [mat[r][k] ^ mat[rank][k] for k in range(ncols)]
        rank += 1
    return rank


def _validate_and_build_base_adjacency(n_vertices: int, edges: list[tuple[int, int]]) -> tuple[list[tuple[int, int]], list[set[int]]]:
    if n_vertices < 2:
        raise ValueError(f"n_vertices must be >= 2, got {n_vertices}")
    base_adj: list[set[int]] = [set() for _ in range(n_vertices)]
    canonical_edges_set: set[tuple[int, int]] = set()
    for u, v in edges:
        if u < 0 or v < 0 or u >= n_vertices or v >= n_vertices or u == v:
            raise ValueError(f"Invalid edge ({u}, {v}) for n_vertices={n_vertices}")
        a, b = (u, v) if u < v else (v, u)
        canonical_edges_set.add((a, b))
        base_adj[a].add(b)
        base_adj[b].add(a)
    return sorted(canonical_edges_set), base_adj


def _build_conf2_adjacency(n_vertices: int, base_adj: list[set[int]]) -> tuple[list[tuple[int, int]], dict[tuple[int, int], int], int, list[set[int]], dict[tuple[int, int], int], int]:
    conf_nodes = list(combinations(range(n_vertices), 2))
    node_to_idx = {pair: idx for idx, pair in enumerate(conf_nodes)}
    n_conf = len(conf_nodes)
    conf_adj: list[set[int]] = [set() for _ in range(n_conf)]
    conf_edge_to_idx: dict[tuple[int, int], int] = {}
    conf_edges = 0

    for i in range(n_conf):
        u1, v1 = conf_nodes[i]
        for j in range(i + 1, n_conf):
            u2, v2 = conf_nodes[j]
            hop = (
                (v2 in base_adj[v1]) if u1 == u2 else
                (u2 in base_adj[v1]) if u1 == v2 else
                (v2 in base_adj[u1]) if v1 == u2 else
                (u2 in base_adj[u1]) if v1 == v2 else
                False
            )
            if hop:
                conf_adj[i].add(j)
                conf_adj[j].add(i)
                conf_edge_to_idx[(i, j)] = conf_edges
                conf_edges += 1
    return conf_nodes, node_to_idx, n_conf, conf_adj, conf_edge_to_idx, conf_edges


def _find_conf2_components(n_conf: int, conf_adj: list[set[int]]) -> int:
    visited = [False] * n_conf
    components = 0
    for start in range(n_conf):
        if visited[start]:
            continue
        components += 1
        queue = deque([start])
        visited[start] = True
        while queue:
            curr = queue.popleft()
            for nbr in conf_adj[curr]:
                if not visited[nbr]:
                    visited[nbr] = True
                    queue.append(nbr)
    return components


def _build_square_2complex_boundaries(
    sorted_base_edges: list[tuple[int, int]],
    node_to_idx: dict[tuple[int, int], int],
    conf_edges: int,
    conf_edge_to_idx: dict[tuple[int, int], int],
) -> list[list[int]]:
    square_boundary_rows: list[list[int]] = []
    for idx1 in range(len(sorted_base_edges)):
        a1, b1 = sorted_base_edges[idx1]
        for idx2 in range(idx1 + 1, len(sorted_base_edges)):
            a2, b2 = sorted_base_edges[idx2]
            if len({a1, b1, a2, b2}) == 4:
                v00 = node_to_idx[(a1, a2) if a1 < a2 else (a2, a1)]
                v10 = node_to_idx[(b1, a2) if b1 < a2 else (a2, b1)]
                v11 = node_to_idx[(b1, b2) if b1 < b2 else (b2, b1)]
                v01 = node_to_idx[(a1, b2) if a1 < b2 else (b2, a1)]
                row = [0] * conf_edges
                for p, q in ((v00, v10), (v10, v11), (v11, v01), (v01, v00)):
                    if p < q:
                        row[conf_edge_to_idx[(p, q)]] += 1
                    else:
                        row[conf_edge_to_idx[(q, p)]] -= 1
                square_boundary_rows.append(row)
    return square_boundary_rows


def analyze_conf2_graph(
    graph_id: str,
    n_vertices: int,
    edges: list[tuple[int, int]],
) -> Conf2GraphSummary:
    """Construct the 1-skeleton Conf_2^(1)(G) and square 2-complex Conf_2^(2)(G)
    for 2 non-colliding identical particles on G.
    """
    sorted_base_edges, base_adj = _validate_and_build_base_adjacency(n_vertices, edges)
    (
        conf_nodes,
        node_to_idx,
        n_conf,
        conf_adj,
        conf_edge_to_idx,
        conf_edges,
    ) = _build_conf2_adjacency(n_vertices, base_adj)
    components = _find_conf2_components(n_conf, conf_adj)
    betti_1 = conf_edges - n_conf + components

    square_boundary_rows = _build_square_2complex_boundaries(
        sorted_base_edges, node_to_idx, conf_edges, conf_edge_to_idx
    )
    n_squares = len(square_boundary_rows)
    rank_q = _rank_over_q(square_boundary_rows, conf_edges)
    rank_f2 = _rank_over_f2(square_boundary_rows, conf_edges)
    b1_2complex_q = betti_1 - rank_q
    b1_2complex_f2 = betti_1 - rank_f2
    z2_torsion_rank = b1_2complex_f2 - b1_2complex_q

    has_z2_exchange_torsion = z2_torsion_rank > 0

    if betti_1 == 0:
        chars = ("NONE_NO_EXCHANGE_LOOP",)
    elif not has_z2_exchange_torsion:
        chars = ("BRAID_U1_CYCLOTOMIC_PHASE",)
    else:
        chars = ("+1_BOSON", "-1_FERMION")

    return Conf2GraphSummary(
        graph_id=graph_id,
        base_vertices=n_vertices,
        base_edges=len(sorted_base_edges),
        conf2_vertices=n_conf,
        conf2_edges=conf_edges,
        conf2_components=components,
        conf2_betti_1=betti_1,
        conf2_squares=n_squares,
        conf2_2complex_betti_1_q=b1_2complex_q,
        conf2_2complex_betti_1_f2=b1_2complex_f2,
        conf2_z2_torsion_rank=z2_torsion_rank,
        has_y_junction_exchange_cycle=has_z2_exchange_torsion,
        admissible_1d_exchange_characters=chars,
    )
def _permutation_sign(perm: tuple[int, ...]) -> int:
    inversions = 0
    n = len(perm)
    for i in range(n):
        for j in range(i + 1, n):
            if perm[i] > perm[j]:
                inversions += 1
    return -1 if (inversions % 2 == 1) else 1


def orbital_slater_or_permanent(
    matrix: list[list[Fraction]],
    *,
    alternating: bool,
) -> Fraction:
    """Compute exact NxN Slater determinant (alternating=True) or permanent (alternating=False)."""
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("Orbital matrix must be non-empty and square")
    total = Fraction(0, 1)
    for perm in permutations(range(n)):
        sign = _permutation_sign(perm) if alternating else 1
        prod = Fraction(sign, 1)
        for i in range(n):
            prod *= matrix[i][perm[i]]
        total += prod
    return total


def verify_two_mode_jordan_wigner_car() -> tuple[bool, bool, Fraction]:
    """Verify exact 2-mode Jordan-Wigner CAR Clifford algebra on Fock space Q^4."""
    zero4 = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    id4 = [[Fraction(1 if i == j else 0) for j in range(4)] for i in range(4)]

    c1 = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    c1[0][2] = Fraction(1)
    c1[1][3] = Fraction(1)

    c2 = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    c2[0][1] = Fraction(1)
    c2[2][3] = Fraction(-1)

    def transpose(m: list[list[Fraction]]) -> list[list[Fraction]]:
        return [[m[r][c] for r in range(4)] for c in range(4)]

    def add(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
        return [[a[r][c] + b[r][c] for c in range(4)] for r in range(4)]

    def mul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
        return [
            [sum((a[r][k] * b[k][c] for k in range(4)), Fraction(0)) for c in range(4)]
            for r in range(4)
        ]

    c1_dag = transpose(c1)
    c2_dag = transpose(c2)

    all_nilpotent = (
        mul(c1, c1) == zero4
        and mul(c2, c2) == zero4
        and mul(c1_dag, c1_dag) == zero4
        and mul(c2_dag, c2_dag) == zero4
        and mul(mul(c1_dag, c2_dag), c1_dag) == zero4
    )

    ac_11 = add(mul(c1, c1_dag), mul(c1_dag, c1))
    ac_22 = add(mul(c2, c2_dag), mul(c2_dag, c2))
    ac_12 = add(mul(c1, c2_dag), mul(c2_dag, c1))
    ac_c1_c2 = add(mul(c1, c2), mul(c2, c1))

    car_exact = ac_11 == id4 and ac_22 == id4 and ac_12 == zero4 and ac_c1_c2 == zero4

    n1 = mul(c1_dag, c1)
    n2 = mul(c2_dag, c2)
    n_tot = add(n1, n2)
    tr_sum = sum((n_tot[i][i] for i in range(4)), Fraction(0))

    return all_nilpotent, car_exact, tr_sum


def _check_conf2_p3_y_star(p3: Conf2GraphSummary, y: Conf2GraphSummary) -> bool:
    return (
        p3.conf2_betti_1 == 0
        and p3.conf2_z2_torsion_rank == 0
        and y.conf2_betti_1 == 1
        and y.conf2_squares == 0
        and y.conf2_2complex_betti_1_q == 1
        and y.conf2_z2_torsion_rank == 0
        and not y.has_y_junction_exchange_cycle
    )


def _check_conf2_c4_k4_k5(c4: Conf2GraphSummary, k4: Conf2GraphSummary, k5: Conf2GraphSummary) -> bool:
    c4_ok = (
        c4.conf2_betti_1 == 3
        and c4.conf2_squares == 2
        and c4.conf2_2complex_betti_1_q == 1
        and c4.conf2_z2_torsion_rank == 0
        and not c4.has_y_junction_exchange_cycle
    )
    k4_ok = (
        k4.conf2_betti_1 == 7
        and k4.conf2_squares == 3
        and k4.conf2_2complex_betti_1_q == 4
        and k4.conf2_z2_torsion_rank == 0
        and not k4.has_y_junction_exchange_cycle
    )
    k5_ok = (
        k5.conf2_betti_1 == 21
        and k5.conf2_squares == 15
        and k5.conf2_2complex_betti_1_q == 6
        and k5.conf2_2complex_betti_1_f2 == 7
        and k5.conf2_z2_torsion_rank == 1
        and k5.has_y_junction_exchange_cycle
    )
    return c4_ok and k4_ok and k5_ok


def _check_slater_and_hbt(
    pauli_same_slater: Fraction,
    swap_ratio_fermion: Fraction,
    swap_ratio_boson: Fraction,
    fermi_hole_prob: Fraction,
    hbt_ratio: Fraction,
) -> bool:
    return (
        pauli_same_slater == Fraction(0)
        and swap_ratio_fermion == Fraction(-1)
        and swap_ratio_boson == Fraction(1)
        and fermi_hole_prob == Fraction(0)
        and hbt_ratio == Fraction(2)
    )


def _check_jw_and_shells(
    jw_nil: bool,
    jw_car: bool,
    jw_tr: Fraction,
    orb_deg: tuple[int, ...],
    shell_caps: tuple[int, ...],
    noble_closures: list[int],
) -> bool:
    return (
        jw_nil
        and jw_car
        and jw_tr == Fraction(4)
        and orb_deg == (1, 4, 9, 16)
        and shell_caps == (2, 8, 18, 32)
        and tuple(noble_closures) == (2, 10, 18, 36, 54, 86, 118)
    )


def build_pauli_spin_statistics_certificate() -> PauliSpinStatisticsCertificate:
    """Build and verify the complete QM-223 Pauli exclusion and spin-statistics certificate."""
    conf2_p3 = analyze_conf2_graph("P_3_1D_path", 3, [(0, 1), (1, 2)])
    conf2_y_star = analyze_conf2_graph("Y_star_K1_3", 4, [(0, 1), (0, 2), (0, 3)])
    conf2_c4 = analyze_conf2_graph("C_4_2D_cycle", 4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    k4_edges = [(u, v) for u in range(4) for v in range(u + 1, 4)]
    conf2_k4 = analyze_conf2_graph("K_4_planar_3connected", 4, k4_edges)
    k5_edges = [(u, v) for u in range(5) for v in range(u + 1, 5)]
    conf2_k5 = analyze_conf2_graph("K_5_nonplanar_3connected", 5, k5_edges)

    a, b = Fraction(3, 5), Fraction(4, 5)
    c, d = Fraction(5, 13), Fraction(12, 13)

    same_orbital = [[a, b], [a, b]]
    pauli_same_slater = orbital_slater_or_permanent(same_orbital, alternating=True)

    orb_12 = [[a, b], [c, d]]
    orb_21 = [[c, d], [a, b]]
    slater_12 = orbital_slater_or_permanent(orb_12, alternating=True)
    slater_21 = orbital_slater_or_permanent(orb_21, alternating=True)
    perm_12 = orbital_slater_or_permanent(orb_12, alternating=False)
    perm_21 = orbital_slater_or_permanent(orb_21, alternating=False)

    swap_ratio_fermion = slater_21 / slater_12
    swap_ratio_boson = perm_21 / perm_12

    fermi_hole_prob = pauli_same_slater * pauli_same_slater
    perm_coincide = orbital_slater_or_permanent(same_orbital, alternating=False)
    boson_coincide_weight = perm_coincide * perm_coincide
    distinguishable_coincide_weight = (a * b) ** 2 + (b * a) ** 2
    hbt_ratio = boson_coincide_weight / distinguishable_coincide_weight

    jw_nil, jw_car, jw_tr = verify_two_mode_jordan_wigner_car()

    orb_deg = tuple(sum(2 * l + 1 for l in range(n)) for n in range(1, 5))
    shell_caps = tuple(2 * deg for deg in orb_deg)

    subshells: list[tuple[int, int, int]] = []
    for sum_nl in range(1, 9):
        for n in range(1, sum_nl + 1):
            l = sum_nl - n
            if l < n and n <= 7:
                subshells.append((n, l, 2 * (2 * l + 1)))
    cumulative = 0
    noble_closures: list[int] = []
    for n, l, cap in subshells:
        cumulative += cap
        if (n == 1 and l == 0) or (n >= 2 and l == 1):
            noble_closures.append(cumulative)

    passed = (
        _check_conf2_p3_y_star(conf2_p3, conf2_y_star)
        and _check_conf2_c4_k4_k5(conf2_c4, conf2_k4, conf2_k5)
        and _check_slater_and_hbt(pauli_same_slater, swap_ratio_fermion, swap_ratio_boson, fermi_hole_prob, hbt_ratio)
        and _check_jw_and_shells(jw_nil, jw_car, jw_tr, orb_deg, shell_caps, noble_closures)
    )

    return PauliSpinStatisticsCertificate(
        control_id="QM-223",
        conf2_p3=conf2_p3,
        conf2_c4=conf2_c4,
        conf2_k5=conf2_k5,
        pauli_same_orbital_slater=pauli_same_slater,
        swap_ratio_fermion=swap_ratio_fermion,
        swap_ratio_boson=swap_ratio_boson,
        fermi_hole_coincidence_probability=fermi_hole_prob,
        hbt_boson_bunching_ratio=hbt_ratio,
        jordan_wigner_nilpotent=jw_nil,
        jordan_wigner_car_exact=jw_car,
        jordan_wigner_fock_number_trace=jw_tr,
        shell_orbital_degeneracies_1_to_4=orb_deg,
        shell_capacities_1_to_4=shell_caps,
        noble_gas_atomic_numbers=tuple(noble_closures),
        passed=passed,
        conf2_y_star=conf2_y_star,
        conf2_k4=conf2_k4,
    )

