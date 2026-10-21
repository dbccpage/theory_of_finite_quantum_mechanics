"""The exact sequence 0 -> H1 -> Q1 -> im d1 -> 0, its splitting freedom and the bound Gamma2 <= ||d1|| Phi1.

Producer for PFP batch 01, node PG-WDP-QUOTIENT-EXACT-SEQUENCE. Exact Fractions only.
Scope: graph windows (d0 = coboundary of a directed multigraph), integer d1 rows, integer NON-NEGATIVE edge weights
(weight 0 makes J a seminorm and is a hypothesis-violating control), integer cochain h. Dimensions over Q:
dim Q1 = m - rank d0; when d1 d0 = 0, dim H1 = m - rank d1 - rank d0 and dim im d1 = rank d1. The space of linear
sections of Q1 -> im d1 is an affine space over Hom(im d1, H1) of dimension dim H1 * dim im d1, so a canonical splitting
exists only when that product is 0. ||d1|| is the operator norm from (C1, weighted L1) to (C2, L1):
max over edges with w_e > 0 of (column L1 sum)/w_e, undefined (None) when a weight-0 edge has a nonzero column.
Not a statement about norms other than weighted L1 or complex coefficients. AuthorityEffect: None.
"""
from fractions import Fraction
from itertools import combinations

# ---- shared window core (duplicated verbatim in the three wdp producers) ----


def d0_rows(nv, edges):
    rows = []
    for s, t in edges:
        row = [0] * nv
        if s != t:
            row[s] = -1
            row[t] = 1
        rows.append(row)
    return rows


def rank(rows):
    mat = [[Fraction(x) for x in r] for r in rows]
    rk = 0
    ncol = len(mat[0]) if mat else 0
    for c in range(ncol):
        piv = None
        for i in range(rk, len(mat)):
            if mat[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[rk], mat[piv] = mat[piv], mat[rk]
        for i in range(len(mat)):
            if i != rk and mat[i][c] != 0:
                f = mat[i][c] / mat[rk][c]
                mat[i] = [a - f * b for a, b in zip(mat[i], mat[rk])]
        rk += 1
    return rk


def solve_rows(rows, rhs):
    """Solve rows * x = rhs for linearly independent rows (free variables 0); None when dependent."""
    r, n = len(rows), len(rows[0])
    mat = [[Fraction(x) for x in rows[i]] + [Fraction(rhs[i])] for i in range(r)]
    pivs = []
    rk = 0
    for c in range(n):
        piv = None
        for i in range(rk, r):
            if mat[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[rk], mat[piv] = mat[piv], mat[rk]
        pv = mat[rk][c]
        mat[rk] = [a / pv for a in mat[rk]]
        for i in range(r):
            if i != rk and mat[i][c] != 0:
                f = mat[i][c]
                mat[i] = [a - f * b for a, b in zip(mat[i], mat[rk])]
        pivs.append(c)
        rk += 1
        if rk == r:
            break
    if rk < r:
        return None
    x = [Fraction(0)] * n
    for i, c in enumerate(pivs):
        x[c] = mat[i][n]
    return x


def phi1(nv, edges, w, h):
    """Quotient defect: attained minimum of sum_e w_e |h_e - (d0 x)_e| over potentials x."""
    d0 = d0_rows(nv, edges)
    m = len(d0)
    r = rank(d0)
    if r == 0:
        return sum(Fraction(w[i]) * abs(h[i]) for i in range(m))
    best = None
    for sub in combinations(range(m), r):
        x = solve_rows([d0[i] for i in sub], [h[i] for i in sub])
        if x is None:
            continue
        cost = sum(Fraction(w[i]) * abs(h[i] - sum(d0[i][j] * x[j] for j in range(nv))) for i in range(m))
        if best is None or cost < best:
            best = cost
    return best


def gamma2(d1, h):
    return sum((abs(sum(row[e] * h[e] for e in range(len(h)))) for row in d1), Fraction(0))


def cochain_defect(nv, edges, d1):
    """First vertex v with d1 d0 e_v != 0, as (v, vector over the 2-cells); None when d1 d0 = 0."""
    d0 = d0_rows(nv, edges)
    for v in range(nv):
        vec = [sum(row[e] * d0[e][v] for e in range(len(edges))) for row in d1]
        if any(vec):
            return v, vec
    return None


def diag_class(phi, gam):
    if phi == 0:
        return 'ExactClass'
    return 'ClosedResidual' if gam == 0 else 'ActiveClosureFailure'


def fs(x):
    return str(Fraction(x))


def tsv_window(c):
    edges = ','.join('%d>%d' % (s, t) for s, t in c['edges'])
    d1 = ';'.join(','.join(str(x) for x in row) for row in c['d1']) or '-'
    return '\t'.join([c['id'], str(c['nv']), edges, ','.join(str(x) for x in c['w']), d1, ','.join(str(x) for x in c['h'])])


# ---- node: PG-WDP-QUOTIENT-EXACT-SEQUENCE ----

TRI_E = [[0, 1], [1, 2], [0, 2]]
TRI_D1 = [[1, 1, -1]]
K4_E = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
SQ_E = [[0, 1], [1, 2], [0, 2], [2, 3], [0, 3]]


def win(id_, nv, edges, w, d1, h):
    return {'id': id_, 'nv': nv, 'edges': edges, 'w': w, 'd1': d1, 'h': h}


CASES = [
    win('tri_filled_active', 3, TRI_E, [1, 1, 1], TRI_D1, [1, 1, 0]),
    win('tri_unfilled_closed', 3, TRI_E, [1, 1, 1], [], [1, 0, 0]),
    win('two_triangles_mixed', 6, TRI_E + [[3, 4], [4, 5], [3, 5]], [1] * 6, [[1, 1, -1, 0, 0, 0]], [1, 1, 0, 1, 0, 0]),
    win('k4_all_faces', 4, K4_E, [1] * 6, [[1, -1, 0, 1, 0, 0], [1, 0, -1, 0, 1, 0], [0, 1, -1, 0, 0, 1], [0, 0, 0, 1, -1, 1]], [1, 0, 2, 1, 0, 1]),
    win('k4_two_faces', 4, K4_E, [1] * 6, [[1, -1, 0, 1, 0, 0], [1, 0, -1, 0, 1, 0]], [1, 0, 2, 1, 0, 1]),
    win('square_two_triangles', 4, SQ_E, [1] * 5, [[1, 1, -1, 0, 0], [0, 0, 1, 1, -1]], [2, 1, 0, 3, 0]),
    win('loop_three_faces', 1, [[0, 0]], [1], [[1], [1], [1]], [1]),
    win('tri_heavy_weights', 3, TRI_E, [3, 3, 3], TRI_D1, [1, 1, 0]),
    win('parallel_bigon_active', 2, [[0, 1], [0, 1], [0, 1]], [1, 1, 1], [[1, -1, 0]], [1, -1, 0]),
    win('disconnected_exact', 4, [[0, 1], [2, 3]], [1, 1], [], [5, -7]),
    win('tri_filled_zero_cochain', 3, TRI_E, [1, 1, 1], TRI_D1, [0, 0, 0]),
    win('violates_d1d0_edge', 2, [[0, 1]], [1], [[1]], [2]),
    win('seminorm_zero_weight_unfilled', 3, TRI_E, [0, 1, 1], [], [1, 0, 0]),
    win('seminorm_zero_weight_filled', 3, TRI_E, [0, 1, 1], TRI_D1, [1, 0, 0]),
]


def class_zero(nv, edges, h):
    d0 = d0_rows(nv, edges)
    return rank([row + [h[i]] for i, row in enumerate(d0)]) == rank(d0)


def opnorm(d1, w):
    """Least c with ||d1 v||_1 <= c ||v||_J for all v (None when no finite c exists)."""
    best = Fraction(0)
    for e in range(len(w)):
        col = sum(abs(row[e]) for row in d1)
        if w[e] == 0:
            if col > 0:
                return None
        else:
            best = max(best, Fraction(col, w[e]))
    return best


def record(c):
    nv, edges, d1, h, w = c['nv'], c['edges'], c['d1'], c['h'], c['w']
    m = len(edges)
    r0 = rank(d0_rows(nv, edges))
    r1 = rank(d1) if d1 else 0
    ok = cochain_defect(nv, edges, d1) is None
    phi = phi1(nv, edges, w, h)
    gam = gamma2(d1, h)
    zero = class_zero(nv, edges, h)
    dim_h1 = (m - r1 - r0) if ok else None
    section = dim_h1 * r1 if ok else None
    on = opnorm(d1, w)
    classes = [phi == 0, phi > 0 and gam == 0, phi > 0 and gam > 0]
    return {
        'id': c['id'], 'complex': ok, 'm': m, 'rank_d0': r0, 'rank_d1': r1, 'dim_q1': m - r0, 'dim_h1': dim_h1, 'dim_im': r1,
        'exact_dims': (m - r0 == dim_h1 + r1) if ok else None, 'section_dim': section,
        'canonical_split': (section == 0) if ok else None, 'class_zero': zero, 'norm_ok': all(x > 0 for x in w),
        'phi1': fs(phi), 'gamma2': fs(gam), 'diag': diag_class(phi, gam) if ok else 'NoRule', 'classes_hit': sum(classes),
        'opnorm': None if on is None else fs(on), 'bound_holds': None if on is None else gam <= on * phi,
        'phi_zero_iff_class_zero': (phi == 0) == zero,
    }


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def _t(x):
    return '-' if x is None else (str(int(x)) if isinstance(x, bool) else str(x))


def wire_lines(data):
    keys = ['complex', 'm', 'rank_d0', 'rank_d1', 'dim_q1', 'dim_h1', 'dim_im', 'exact_dims', 'section_dim', 'canonical_split', 'class_zero',
            'norm_ok', 'phi1', 'gamma2', 'diag', 'classes_hit', 'opnorm', 'bound_holds', 'phi_zero_iff_class_zero']
    return [chr(9).join(['seq', r['id']] + [_t(r[k]) for k in keys]) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('window' + chr(9) + tsv_window(c) + chr(10) for c in cases)
