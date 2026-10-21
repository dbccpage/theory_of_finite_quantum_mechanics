"""Independent checker for PG-WDP-QUOTIENT-EXACT-SEQUENCE.

Recomputes every record from the public windows without importing the producer. Phi1 comes from the DUAL linear program
(vertices of {y : d0^T y = 0, |y_e| <= w_e}); the certificate also carries a primal potential x and a dual vector y per window
and the checker VERIFIES them exactly (cost(x) = y.h = Phi1, d0^T y = 0, |y_e| <= w_e, the statement of the kernel theorem
isPhi_of_certificate). dim H1 is recomputed from an EXPLICIT nullspace basis of d1 (each basis vector checked to be killed by d1,
the basis checked independent, d1 d0 = 0 checked entrywise) minus rank d0, rather than from the formula m - rank d1 - rank d0 used
by the producer. Membership of h in im d0 is an augmented rank comparison; the operator norm is the largest ratio of column L1 sum
to weight. Theorem-level checks restate what the kernel proves for complexes. Gamma2 is the representative norm ||d1 h||_1, which
equals the source's value at the minimal residual only when d1 d0 = 0, so it is withheld for a non-window. AuthorityEffect: None.
"""
import json
import sys
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import lcm
from pathlib import Path

ROOT = next((p for p in Path(__file__).resolve().parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-WDP-QUOTIENT-EXACT-SEQUENCE'
KEYS = {'id', 'complex', 'm', 'rank_d0', 'rank_d1', 'dim_q1', 'dim_h1', 'dim_im', 'exact_dims', 'section_dim', 'canonical_split',
        'class_zero', 'norm_ok', 'phi1', 'gamma2', 'diag', 'classes_hit', 'opnorm', 'bound_holds', 'phi_zero_iff_class_zero', 'witness'}
EXPECTED_IDS = ['tri_filled_active', 'tri_unfilled_closed', 'two_triangles_mixed', 'k4_all_faces', 'k4_two_faces', 'square_two_triangles',
                'loop_three_faces', 'tri_heavy_weights', 'parallel_bigon_active', 'disconnected_exact', 'tri_filled_zero_cochain',
                'violates_d1d0_edge', 'seminorm_zero_weight_unfilled', 'seminorm_zero_weight_filled']
INTS = ('m', 'rank_d0', 'rank_d1', 'dim_q1', 'dim_im')
OPT_INTS = ('dim_h1', 'section_dim', 'classes_hit')
BOOLS = ('complex', 'class_zero', 'norm_ok', 'phi_zero_iff_class_zero')
OPT_BOOLS = ('exact_dims', 'canonical_split', 'bound_holds')
STRS = ('id', 'phi1', 'diag', 'witness')
OPT_STRS = ('gamma2', 'opnorm')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def bareiss_rank(rows):
    m = [list(map(int, r)) for r in rows]
    if not m or not m[0]:
        return 0
    nr, nc = len(m), len(m[0])
    rk, prev, col = 0, 1, 0
    while rk < nr and col < nc:
        piv = next((i for i in range(rk, nr) if m[i][col] != 0), None)
        if piv is None:
            col += 1
            continue
        m[rk], m[piv] = m[piv], m[rk]
        for i in range(rk + 1, nr):
            for j in range(col + 1, nc):
                m[i][j] = (m[rk][col] * m[i][j] - m[i][col] * m[rk][j]) // prev
            m[i][col] = 0
        prev = m[rk][col]
        rk += 1
        col += 1
    return rk


def coboundary(nv, edges):
    return [[(1 if (v == t and s != t) else 0) - (1 if (v == s and s != t) else 0) for v in range(nv)] for s, t in edges]


def unique_solution(cols, rhs):
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


def dual_phi(nv, edges, w, h):
    d0 = coboundary(nv, edges)
    m = len(edges)
    r = bareiss_rank(d0)
    best = None
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
                best = val
    return best


def nullspace(rows, m):
    """Explicit basis of {z : rows z = 0} by reduced row echelon form; each vector returned with integer entries."""
    mat = [[Fraction(x) for x in row] for row in rows]
    pivots, rk = [], 0
    for col in range(m):
        piv = next((i for i in range(rk, len(mat)) if mat[i][col] != 0), None)
        if piv is None:
            continue
        mat[rk], mat[piv] = mat[piv], mat[rk]
        lead = mat[rk][col]
        mat[rk] = [a / lead for a in mat[rk]]
        for i in range(len(mat)):
            if i != rk and mat[i][col] != 0:
                f = mat[i][col]
                mat[i] = [a - f * b for a, b in zip(mat[i], mat[rk])]
        pivots.append(col)
        rk += 1
    basis = []
    for free in (c for c in range(m) if c not in pivots):
        z = [Fraction(0)] * m
        z[free] = Fraction(1)
        for i, pc in enumerate(pivots):
            z[pc] = -mat[i][free]
        scale = lcm(*[v.denominator for v in z])
        basis.append([int(v * scale) for v in z])
    return basis


def parse_fractions(text, count):
    parts = text.split(',')
    require(len(parts) == count, 'G3_WITNESS:witness_length')
    out = []
    for part in parts:
        value = Fraction(part)
        require(str(value) == part, 'G3_WITNESS:witness_not_canonical')
        out.append(value)
    return out


def verify_witness(c, text, phi):
    nv, edges, w, h = c['nv'], c['edges'], c['w'], c['h']
    m = len(edges)
    require(type(text) is str and text.startswith('x=') and '|y=' in text and text.count('|') == 1, 'G3_WITNESS:witness_shape')
    xt, yt = text[2:].split('|y=')
    x, y = parse_fractions(xt, nv), parse_fractions(yt, m)
    d0 = coboundary(nv, edges)
    require(all(sum(y[e] * d0[e][v] for e in range(m)) == 0 for v in range(nv)), 'G3_WITNESS:dual_not_annihilating_coboundaries')
    require(all(abs(y[e]) <= w[e] for e in range(m)), 'G3_WITNESS:dual_exceeds_weights')
    primal = sum(w[e] * abs(h[e] - sum(d0[e][v] * x[v] for v in range(nv))) for e in range(m))
    require(primal == phi and sum(y[e] * h[e] for e in range(m)) == phi, 'G3_WITNESS:primal_dual_values_differ')


@lru_cache(maxsize=None)
def _expected(key):
    c = json.loads(key)
    nv, edges, w, d1, h = c['nv'], c['edges'], c['w'], c['d1'], c['h']
    m = len(edges)
    d0 = coboundary(nv, edges)
    r0, r1 = bareiss_rank(d0), (bareiss_rank(d1) if d1 else 0)
    ok = all(sum(row[e] * d0[e][v] for e in range(m)) == 0 for row in d1 for v in range(nv))
    phi = dual_phi(nv, edges, w, h)
    gam = sum(abs(sum(row[e] * h[e] for e in range(m))) for row in d1)
    zero = bareiss_rank([d0[e] + [h[e]] for e in range(m)]) == r0
    # explicit kernel of d1: basis killed by d1 and independent; H1 = ker d1 / im d0 when d1 d0 = 0
    kernel = nullspace(d1, m) if d1 else [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    require(all(sum(row[e] * z[e] for e in range(m)) == 0 for row in d1 for z in kernel), 'G3_WITNESS:nullspace_not_in_kernel')
    require(bareiss_rank(kernel) == len(kernel), 'G3_WITNESS:nullspace_not_independent')
    dim_h1 = (len(kernel) - r0) if ok else None
    cols = [sum(abs(row[e]) for row in d1) for e in range(m)]
    infinite = any(w[e] == 0 and cols[e] > 0 for e in range(m))
    ratios = [Fraction(cols[e], w[e]) for e in range(m) if w[e] > 0]
    op = None if infinite else max(ratios + [Fraction(0)])
    hit = (phi == 0) + (phi > 0 and gam == 0) + (phi > 0 and gam > 0)
    rec = {'id': c['id'], 'complex': ok, 'm': m, 'rank_d0': r0, 'rank_d1': r1, 'dim_q1': m - r0, 'dim_h1': dim_h1, 'dim_im': r1,
           'exact_dims': (m - r0 == dim_h1 + r1) if ok else None, 'section_dim': (dim_h1 * r1) if ok else None,
           'canonical_split': (dim_h1 * r1 == 0) if ok else None, 'class_zero': zero, 'norm_ok': min(w) > 0,
           'phi1': str(Fraction(phi)), 'gamma2': str(Fraction(gam)) if ok else None,
           'diag': (('ExactClass' if phi == 0 else ('ClosedResidual' if gam == 0 else 'ActiveClosureFailure')) if ok else 'NotAWindow'),
           'classes_hit': int(hit) if ok else None, 'opnorm': None if op is None else str(op),
           'bound_holds': (gam <= op * phi) if (ok and op is not None) else None, 'phi_zero_iff_class_zero': (phi == 0) == zero}
    return rec, (phi, gam, op)


def expected(c):
    return _expected(json.dumps(c, sort_keys=True))


def validate_case(c):
    require(type(c['nv']) is int and c['nv'] >= 1 and len(c['edges']) >= 1, 'G1_SCHEMA:public_window_shape')
    m = len(c['edges'])
    require(all(0 <= s < c['nv'] and 0 <= t < c['nv'] for s, t in c['edges']), 'G1_SCHEMA:public_endpoints')
    require(len(c['w']) == m and len(c['h']) == m and all(type(x) is int and x >= 0 for x in c['w']) and all(type(x) is int for x in c['h']),
            'G1_SCHEMA:public_weights_cochain')
    require(all(len(row) == m and all(type(x) is int for x in row) for row in c['d1']), 'G1_SCHEMA:public_d1')


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = public['cases']
        require([c['id'] for c in cases] == EXPECTED_IDS, 'G2_COVERAGE:public_cases_are_the_declared_family')
        for c in cases:
            validate_case(c)
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        require(all(type(r) is dict and type(r.get('id')) is str for r in records), 'G1_SCHEMA:record_ids')
        by_id = {r['id']: r for r in records}
        require(len(by_id) == len(records) and set(by_id) == {c['id'] for c in cases}, 'G2_COVERAGE:ids_are_the_public_cases')
        for c in cases:
            r = by_id[c['id']]
            require(set(r) == KEYS, 'G1_SCHEMA:record_keys')
            require(all(is_int(r[k]) for k in INTS) and all(r[k] is None or is_int(r[k]) for k in OPT_INTS), 'G1_SCHEMA:ints')
            require(all(type(r[k]) is bool for k in BOOLS) and all(r[k] is None or type(r[k]) is bool for k in OPT_BOOLS), 'G1_SCHEMA:bools')
            require(all(type(r[k]) is str for k in STRS) and all(r[k] is None or type(r[k]) is str for k in OPT_STRS), 'G1_SCHEMA:strings')
            want, (phi, gam, op) = expected(c)
            for key in want:
                require(r[key] == want[key], 'G3_WITNESS:' + key)
            verify_witness(c, r['witness'], phi)
            # theorem-level consistency: what the kernel proves for a complex must hold in the data
            if want['complex']:
                require(want['classes_hit'] == 1, 'G3_WITNESS:exactly_one_class')
                require(want['exact_dims'] is True, 'G3_WITNESS:exact_sequence_dimensions')
                if op is not None:
                    require(gam <= op * phi, 'G3_WITNESS:gamma2_le_opnorm_times_phi1')
                if want['norm_ok']:
                    require(want['phi_zero_iff_class_zero'] is True, 'G3_WITNESS:phi1_zero_iff_zero_class')
                    require(not (phi == 0 and gam != 0), 'G3_WITNESS:exact_class_is_closed')
            else:
                require(all(r[k] is None for k in ('dim_h1', 'exact_dims', 'section_dim', 'canonical_split', 'gamma2', 'classes_hit', 'bound_holds'))
                        and r['diag'] == 'NotAWindow', 'G3_WITNESS:refusal_shape')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ZeroDivisionError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))
    except ValueError as error:
        if str(error).startswith('G'):
            raise
        raise ValueError('G3_WITNESS:unparsable ' + str(error))


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
