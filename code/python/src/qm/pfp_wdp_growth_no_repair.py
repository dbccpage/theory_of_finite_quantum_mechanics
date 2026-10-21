"""Growth does not repair a quotient residual: restriction, attachment and edits on small graph windows.

Producer for PFP batch 01, node PG-WDP-GROWTH-NO-REPAIR. Exact Fractions only.
Scope: graph windows as in the degree-1 window node (weighted L1, positive integer weights, integer d1 rows and
cochain). A pair is a window A plus one operation: `restrict` (keep a set of edges with their cochain values and
the 2-cells supported inside; optionally replace the weights), `attach` (add 2-cell rows), `edit_h`, `edit_w`.
The table records Phi1 and Gamma2 before and after; it does not assert the monotonicity for norms other than weighted L1,
nor anything about equal-weight subdivision. AuthorityEffect: None.
"""
from fractions import Fraction
from itertools import combinations, product

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


def cost(d0, w, h, x):
    return sum(Fraction(w[i]) * abs(h[i] - sum(d0[i][j] * x[j] for j in range(len(x)))) for i in range(len(d0)))


def phi1_x(nv, edges, w, h):
    """Primal: attained minimum of sum_e w_e |h_e - (d0 x)_e| and a minimising potential x (first best vertex)."""
    d0 = d0_rows(nv, edges)
    m = len(d0)
    r = rank(d0)
    if r == 0:
        return sum((Fraction(w[i]) * abs(h[i]) for i in range(m)), Fraction(0)), [Fraction(0)] * nv
    best, best_x = None, None
    for sub in combinations(range(m), r):
        x = solve_rows([d0[i] for i in sub], [h[i] for i in sub])
        if x is None:
            continue
        c = cost(d0, w, h, x)
        if best is None or c < best:
            best, best_x = c, x
    return best, best_x


def phi1(nv, edges, w, h):
    return phi1_x(nv, edges, w, h)[0]


def unique_solution(cols, rhs):
    """Solve sum_j y_j cols[j] = rhs; None unless the solution exists and is unique."""
    r, n = len(cols), len(rhs)
    rows = [[Fraction(cols[j][i]) for j in range(r)] + [Fraction(rhs[i])] for i in range(n)]
    used = []
    for j in range(r):
        p = next((i for i in range(n) if i not in used and rows[i][j] != 0), None)
        if p is None:
            return None
        used.append(p)
        pivot = rows[p][j]
        rows[p] = [a / pivot for a in rows[p]]
        for i in range(n):
            if i != p and rows[i][j] != 0:
                f = rows[i][j]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[p])]
    if any(rows[i][r] != 0 for i in range(n) if i not in used):
        return None
    return [rows[used[j]][r] for j in range(r)]


def dual_y(nv, edges, w, h):
    """Dual: maximum of y.h over d0^T y = 0, |y_e| <= w_e, and the first maximising vertex y."""
    d0 = d0_rows(nv, edges)
    m = len(edges)
    r = rank(d0)
    best, best_y = None, None
    for pinned in combinations(range(m), m - r):
        free = [e for e in range(m) if e not in pinned]
        for signs in product((1, -1), repeat=len(pinned)):
            y = {e: Fraction(s * w[e]) for e, s in zip(pinned, signs)}
            if free:
                rhs = [-sum(y[e] * d0[e][v] for e in pinned) for v in range(nv)]
                sol = unique_solution([[d0[e][v] for v in range(nv)] for e in free], rhs)
                if sol is None:
                    continue
                for e, val in zip(free, sol):
                    y[e] = val
                if any(abs(y[e]) > w[e] for e in free):
                    continue
            elif any(sum(y[e] * d0[e][v] for e in pinned) != 0 for v in range(nv)):
                continue
            val = sum(y[e] * h[e] for e in range(m))
            if best is None or val > best:
                best, best_y = val, [y[e] for e in range(m)]
    return best, best_y


def fs(x):
    return str(Fraction(x))


def witness(nv, edges, w, h):
    """(Phi1, witness string 'x=..|y=..'): a primal potential and a dual vector with equal values."""
    phi, x = phi1_x(nv, edges, w, h)
    val, y = dual_y(nv, edges, w, h)
    assert phi == val == sum(y[e] * h[e] for e in range(len(h))), 'primal and dual values differ'
    return phi, 'x=' + ','.join(fs(v) for v in x) + '|y=' + ','.join(fs(v) for v in y)


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


def k4_subsets():
    """All 63 non-empty edge subsets of K4 (one cochain), restricted with the inherited weights."""
    out = []
    for mask in range(1, 64):
        keep = [i for i in range(6) if mask & (1 << i)]
        out.append(pair('k4_sub_%02d' % mask, 4, K4_E, [1] * 6, K4_D1, [1, 0, 2, 1, 0, 1], 'restrict', ','.join(map(str, keep)) + '|-'))
    return out


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
] + k4_subsets()


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
    phi, wit = witness(nv, edges, w, h)
    gam = gamma2(d1, h)
    return ok, phi, (gam if ok else None), (diag_class(phi, gam) if ok else 'NotAWindow'), wit


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
    ok_a, phi_a, gam_a, cls_a, wit_a = side(c['nv'], c['edges'], c['w'], c['d1'], c['h'])
    nvb, eb, wb, db, hb = derive_b(c)
    ok_b, phi_b, gam_b, cls_b, wit_b = side(nvb, eb, wb, db, hb)
    return {
        'id': c['id'], 'kind': c['kind'], 'm_a': len(c['edges']), 'm_b': len(eb), 'k_a': len(c['d1']), 'k_b': len(db),
        'complex_a': ok_a, 'complex_b': ok_b, 'phi_a': fs(phi_a), 'phi_b': fs(phi_b),
        'gamma_a': None if gam_a is None else fs(gam_a), 'gamma_b': None if gam_b is None else fs(gam_b),
        'diag_a': cls_a, 'diag_b': cls_b, 'verdict': verdict(c['kind'], ok_b, phi_a, phi_b, gam_a, gam_b),
        'witness_a': wit_a, 'witness_b': wit_b,
    }


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def _t(x):
    return '-' if x is None else str(x)


def wire_lines(data):
    return [chr(9).join(['pair', r['id'], r['kind'], str(r['m_a']), str(r['m_b']), str(r['k_a']), str(r['k_b']),
                         str(int(r['complex_a'])), str(int(r['complex_b'])), r['phi_a'], r['phi_b'], _t(r['gamma_a']), _t(r['gamma_b']),
                         r['diag_a'], r['diag_b'], r['verdict'], r['witness_a'], r['witness_b']]) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('pair' + chr(9) + tsv_window(c) + chr(9) + c['kind'] + chr(9) + c['arg'] + chr(10) for c in cases)
