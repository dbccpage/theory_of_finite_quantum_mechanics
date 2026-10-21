"""The degree-1 window (C0, C1, C2, d0, d1) with a weighted-L1 norm J: invariants and diagnostic classes.

Producer for PFP batch 01, node PG-WDP-DEGREE1-WINDOW. Exact Fractions only.
Scope: graph windows (d0 = coboundary of a directed multigraph on nv vertices, d0 row of a loop is zero), an
integer 2-cell matrix d1 given by rows over the edges, positive integer edge weights (J = weighted L1),
an integer 1-cochain h. Phi1 is the attained minimum over potentials x of sum_e w_e |h_e - (d0 x)_e|, found
by enumerating the vertices of the repair arrangement (r = rank d0 edges forced to zero residual).
Gamma2 = unweighted L1 norm of d1 h. Not a statement about complex coefficients, other norms, or the origin of
the window (it is declared). AuthorityEffect: None.
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


# ---- node: PG-WDP-DEGREE1-WINDOW ----

TRI_E = [[0, 1], [1, 2], [0, 2]]
TRI_D1 = [[1, 1, -1]]
K4_E = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
SQ_E = [[0, 1], [1, 2], [0, 2], [2, 3], [0, 3]]


def win(id_, nv, edges, w, d1, h):
    return {'id': id_, 'nv': nv, 'edges': edges, 'w': w, 'd1': d1, 'h': h}


CASES = [
    win('tri_filled_active', 3, TRI_E, [1, 1, 1], TRI_D1, [1, 1, 0]),
    win('tri_filled_active_shifted', 3, TRI_E, [1, 1, 1], TRI_D1, [2, 1, 1]),  # h + d0 (0,1,1): same class
    win('tri_filled_exact', 3, TRI_E, [1, 1, 1], TRI_D1, [1, 2, 3]),
    win('tri_unfilled_closed', 3, TRI_E, [1, 1, 1], [], [1, 0, 0]),
    win('tri_filled_zero_class', 3, TRI_E, [1, 1, 1], TRI_D1, [0, 0, 0]),
    win('tri_heavy_weights', 3, TRI_E, [3, 3, 3], TRI_D1, [1, 1, 0]),
    win('tri_mixed_weights', 3, TRI_E, [1, 5, 5], TRI_D1, [2, 0, 0]),
    win('tri_d1_zero_row', 3, TRI_E, [1, 1, 1], [[0, 0, 0]], [1, 0, 0]),
    win('square_two_triangles', 4, SQ_E, [1, 1, 1, 1, 1], [[1, 1, -1, 0, 0], [0, 0, 1, 1, -1]], [2, 1, 0, 3, 0]),
    win('square_unfilled_closed', 4, [[0, 1], [1, 2], [2, 3], [0, 3]], [1, 1, 1, 1], [], [1, 0, 0, 0]),
    win('k4_three_faces', 4, K4_E, [1, 1, 1, 1, 1, 1],
        [[1, -1, 0, 1, 0, 0], [1, 0, -1, 0, 1, 0], [0, 1, -1, 0, 0, 1]], [1, 0, 2, 1, 0, 1]),
    win('loop_active', 1, [[0, 0]], [1], [[1]], [3]),
    win('disconnected_exact', 4, [[0, 1], [2, 3]], [1, 1], [], [5, -7]),
    win('disconnected_cycle_closed', 5, TRI_E + [[3, 4]], [1, 1, 1, 1], [], [1, 0, 0, 9]),
    win('parallel_bigon_active', 2, [[0, 1], [0, 1], [0, 1]], [1, 1, 1], [[1, -1, 0]], [1, -1, 0]),
    win('violates_d1d0_edge', 2, [[0, 1]], [1], [[1]], [2]),
    win('violates_d1d0_signs', 3, TRI_E, [1, 1, 1], [[1, 1, 1]], [1, 1, 0]),
]


def record(c):
    nv, edges, d1, h, w = c['nv'], c['edges'], c['d1'], c['h'], c['w']
    d0 = d0_rows(nv, edges)
    r0 = rank(d0)
    r1 = rank(d1) if d1 else 0
    bad = cochain_defect(nv, edges, d1)
    ok = bad is None
    phi, wit = witness(nv, edges, w, h)
    gam = gamma2(d1, h)
    return {
        'id': c['id'], 'nv': nv, 'm': len(edges), 'k': len(d1), 'rank_d0': r0, 'rank_d1': r1, 'complex': ok,
        'dim_q1': len(edges) - r0, 'dim_h1': (len(edges) - r1 - r0) if ok else None,
        'phi1': fs(phi), 'gamma2': fs(gam) if ok else None,
        'r_cl': fs(gam / phi) if ok and phi > 0 else None,
        'diag': diag_class(phi, gam) if ok else 'NotAWindow',
        'kappa_witness': None if ok else '%d:%s' % (bad[0], ','.join(str(x) for x in bad[1])),
        'witness': wit,
    }


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def wire_lines(data):
    out = []
    for r in data['records']:
        out.append(chr(9).join([
            'window', r['id'], str(r['nv']), str(r['m']), str(r['k']), str(r['rank_d0']), str(r['rank_d1']),
            str(int(r['complex'])), str(r['dim_q1']), '-' if r['dim_h1'] is None else str(r['dim_h1']),
            r['phi1'], '-' if r['gamma2'] is None else r['gamma2'], '-' if r['r_cl'] is None else r['r_cl'], r['diag'],
            '-' if r['kappa_witness'] is None else r['kappa_witness'], r['witness']]))
    return out


def public_tsv(cases=CASES):
    return ''.join('window' + chr(9) + tsv_window(c) + chr(10) for c in cases)
