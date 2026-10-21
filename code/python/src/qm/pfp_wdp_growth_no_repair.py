"""Growth does not repair a quotient residual: restriction, attachment and edits on small graph windows.

Producer for PFP batch 01, node PG-WDP-GROWTH-NO-REPAIR. Exact Fractions only.
Scope: graph windows as in the degree-1 window node (weighted L1, positive integer weights, integer d1 rows and
cochain). A pair is a window A plus one operation: `restrict` (keep a set of edges with their cochain values and
the 2-cells supported inside; optionally replace the weights), `attach` (add 2-cell rows), `edit_h`, `edit_w`.
The table records Phi1 and Gamma2 before and after; it does not assert the monotonicity for norms other than weighted L1,
nor anything about equal-weight subdivision. AuthorityEffect: None.
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


# ---- node: PG-WDP-GROWTH-NO-REPAIR ----

TRI_E = [[0, 1], [1, 2], [0, 2]]
TRI_D1 = [[1, 1, -1]]
K4_E = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
K4_D1 = [[1, -1, 0, 1, 0, 0], [1, 0, -1, 0, 1, 0], [0, 1, -1, 0, 0, 1], [0, 0, 0, 1, -1, 1]]
PAR_E = [[0, 1], [0, 1], [0, 1]]
C4_E = [[0, 1], [1, 2], [2, 3], [0, 3]]


def pair(id_, nv, edges, w, d1, h, kind, arg):
    return {'id': id_, 'nv': nv, 'edges': edges, 'w': w, 'd1': d1, 'h': h, 'kind': kind, 'arg': arg}


CASES = [
    pair('k4_restrict_to_triangle', 4, K4_E, [1] * 6, K4_D1, [1, 0, 2, 1, 0, 1], 'restrict', '0,1,3|-'),
    pair('k4_restrict_triangle_pendant', 4, K4_E, [1] * 6, K4_D1, [1, 0, 2, 1, 0, 1], 'restrict', '0,1,3,5|-'),
    pair('k4_restrict_one_edge', 4, K4_E, [1] * 6, K4_D1, [1, 0, 2, 1, 0, 1], 'restrict', '4|-'),
    pair('k4_restrict_disjoint_edges', 4, K4_E, [1] * 6, K4_D1, [1, 0, 2, 1, 0, 1], 'restrict', '0,5|-'),
    pair('k4_restrict_five_edges', 4, K4_E, [1] * 6, K4_D1, [1, 0, 2, 1, 0, 1], 'restrict', '0,1,2,3,4|-'),
    pair('k4_restrict_four_cycle', 4, K4_E, [1] * 6, K4_D1, [1, 0, 2, 1, 0, 1], 'restrict', '0,2,3,5|-'),
    pair('parallel_restrict_equal_weights', 2, PAR_E, [2, 2, 2], [[1, -1, 0]], [1, -1, 0], 'restrict', '0,1|-'),
    pair('parallel_restrict_rescaled_weights', 2, PAR_E, [2, 2, 2], [[1, -1, 0]], [1, -1, 0], 'restrict', '0,1|3,3'),
    pair('parallel_restrict_downweighted', 2, PAR_E, [2, 2, 2], [[1, -1, 0]], [1, -1, 0], 'restrict', '0,1|1,1'),
    pair('tri_unfilled_attach_face', 3, TRI_E, [1, 1, 1], [], [1, 0, 0], 'attach', '1,1,-1'),
    pair('tri_exact_attach_duplicate_face', 3, TRI_E, [1, 1, 1], TRI_D1, [1, 2, 3], 'attach', '1,1,-1'),
    pair('tri_active_attach_scaled_face', 3, TRI_E, [1, 1, 1], TRI_D1, [1, 1, 0], 'attach', '2,2,-2'),
    pair('tri_attach_invalid_row', 3, TRI_E, [1, 1, 1], [], [1, 0, 0], 'attach', '1,0,0'),
    pair('square_attach_filling_face', 4, C4_E, [1] * 4, [], [1, 0, 0, 0], 'attach', '1,1,1,-1'),
    pair('loop_attach_face', 1, [[0, 0]], [1], [], [3], 'attach', '1'),
    pair('tri_edit_h_to_exact', 3, TRI_E, [1, 1, 1], [], [1, 0, 0], 'edit_h', '1,1,2'),
    pair('tri_edit_h_gauge_shift', 3, TRI_E, [1, 1, 1], TRI_D1, [1, 1, 0], 'edit_h', '2,1,1'),
    pair('tri_edit_w_down', 3, TRI_E, [3, 3, 3], TRI_D1, [1, 1, 0], 'edit_w', '1,1,1'),
    pair('tri_edit_w_up', 3, TRI_E, [1, 1, 1], [], [1, 0, 0], 'edit_w', '2,2,2'),
]


def derive_b(c):
    """The second window of a pair: (nv, edges, w, d1, h)."""
    nv, edges, w, d1, h = c['nv'], c['edges'], c['w'], c['d1'], c['h']
    kind, arg = c['kind'], c['arg']
    if kind == 'restrict':
        keep_s, neww = arg.split('|')
        keep = [int(x) for x in keep_s.split(',')]
        kept = set(keep)
        rows = [[row[i] for i in keep] for row in d1 if all(row[e] == 0 for e in range(len(edges)) if e not in kept)]
        wb = [w[i] for i in keep] if neww == '-' else [int(x) for x in neww.split(',')]
        return nv, [edges[i] for i in keep], wb, rows, [h[i] for i in keep]
    if kind == 'attach':
        rows = [[int(x) for x in r.split(',')] for r in arg.split(';')]
        return nv, edges, w, d1 + rows, h
    if kind == 'edit_h':
        return nv, edges, w, d1, [int(x) for x in arg.split(',')]
    if kind == 'edit_w':
        return nv, edges, [int(x) for x in arg.split(',')], d1, h
    raise ValueError(kind)


def side(nv, edges, w, d1, h):
    ok = cochain_defect(nv, edges, d1) is None
    phi = phi1(nv, edges, w, h)
    gam = gamma2(d1, h)
    return ok, phi, gam, (diag_class(phi, gam) if ok else 'NoRule')


def verdict(kind, ok_b, phi_a, phi_b, gam_a, gam_b):
    if kind == 'restrict':
        return 'sub_phi_le' if phi_b <= phi_a else 'sub_phi_gt'
    if kind == 'attach':
        if not ok_b:
            return 'attach_not_a_window'
        if phi_b != phi_a:
            return 'attach_phi_changed'
        return 'phi_equal_gamma_up' if gam_b > gam_a else 'phi_equal_gamma_same'
    return 'phi_lower' if phi_b < phi_a else ('phi_same' if phi_b == phi_a else 'phi_higher')


def record(c):
    ok_a, phi_a, gam_a, cls_a = side(c['nv'], c['edges'], c['w'], c['d1'], c['h'])
    nvb, eb, wb, db, hb = derive_b(c)
    ok_b, phi_b, gam_b, cls_b = side(nvb, eb, wb, db, hb)
    return {
        'id': c['id'], 'kind': c['kind'], 'm_a': len(c['edges']), 'm_b': len(eb), 'k_a': len(c['d1']), 'k_b': len(db),
        'complex_a': ok_a, 'complex_b': ok_b, 'phi_a': fs(phi_a), 'phi_b': fs(phi_b), 'gamma_a': fs(gam_a), 'gamma_b': fs(gam_b),
        'diag_a': cls_a, 'diag_b': cls_b, 'verdict': verdict(c['kind'], ok_b, phi_a, phi_b, gam_a, gam_b),
    }


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def wire_lines(data):
    return [chr(9).join(['pair', r['id'], r['kind'], str(r['m_a']), str(r['m_b']), str(r['k_a']), str(r['k_b']),
                         str(int(r['complex_a'])), str(int(r['complex_b'])), r['phi_a'], r['phi_b'], r['gamma_a'], r['gamma_b'],
                         r['diag_a'], r['diag_b'], r['verdict']]) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('pair' + chr(9) + tsv_window(c) + chr(9) + c['kind'] + chr(9) + c['arg'] + chr(10) for c in cases)
