"""Independent checker for PG-WDP-DEGREE1-WINDOW.

Recomputes every record from the public windows without importing the producer. Phi1 is obtained from the DUAL linear program
(vertices of {y : d0^T y = 0, |y_e| <= w_e}, each vertex from m - rank edges pinned to +-w_e), not by the producer's primal vertex
enumeration. The certificate carries a primal potential x and a dual vector y per window; the checker VERIFIES them exactly:
cost(x) = y.h = Phi1, d0^T y = 0, |y_e| <= w_e (this is the statement of the kernel theorem isPhi_of_certificate). Ranks use
fraction-free (Bareiss) elimination; d1 d0 is expanded directly. Two public windows whose cochains differ by a coboundary must
carry the same Phi1, Gamma2 and class. AuthorityEffect: None.
"""
import sys
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path

ROOT = next((p for p in Path(__file__).resolve().parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-WDP-DEGREE1-WINDOW'
KEYS = {'id', 'nv', 'm', 'k', 'rank_d0', 'rank_d1', 'complex', 'dim_q1', 'dim_h1', 'phi1', 'gamma2', 'r_cl', 'diag',
        'kappa_witness', 'witness'}
EXPECTED_IDS = ['tri_filled_active', 'tri_filled_active_shifted', 'tri_filled_exact', 'tri_unfilled_closed', 'tri_filled_zero_class',
                'tri_heavy_weights', 'tri_mixed_weights', 'tri_d1_zero_row', 'square_two_triangles', 'square_unfilled_closed',
                'k4_three_faces', 'loop_active', 'disconnected_exact', 'disconnected_cycle_closed', 'parallel_bigon_active',
                'violates_d1d0_edge', 'violates_d1d0_signs']


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
    """Edge-by-vertex matrix: -1 at the source, +1 at the target, zero row for a loop."""
    return [[(1 if (v == t and s != t) else 0) - (1 if (v == s and s != t) else 0) for v in range(nv)] for s, t in edges]


def unique_solution(cols, rhs):
    """Solve sum_j y_j cols[j] = rhs (n equations, len(cols) unknowns) by elimination; None unless unique."""
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
    """Exact certificate check: x primal feasible with cost Phi1, y dual feasible with y.h = Phi1 (isPhi_of_certificate)."""
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
    import json
    c = json.loads(key)
    nv, edges, w, d1, h = c['nv'], c['edges'], c['w'], c['d1'], c['h']
    m = len(edges)
    d0 = coboundary(nv, edges)
    r0, r1 = bareiss_rank(d0), bareiss_rank(d1) if d1 else 0
    bad = None
    for v in range(nv):
        vec = [sum(row[e] * d0[e][v] for e in range(m)) for row in d1]
        if any(x != 0 for x in vec):
            bad = (v, vec)
            break
    phi = dual_phi(nv, edges, w, h)
    gam = sum(abs(sum(row[e] * h[e] for e in range(m))) for row in d1)
    ok = bad is None
    if ok:
        diag = 'ExactClass' if phi == 0 else ('ClosedResidual' if gam == 0 else 'ActiveClosureFailure')
    else:
        diag = 'NotAWindow'
    rec = {'id': c['id'], 'nv': nv, 'm': m, 'k': len(d1), 'rank_d0': r0, 'rank_d1': r1, 'complex': ok,
           'dim_q1': m - r0, 'dim_h1': (m - r1 - r0) if ok else None, 'phi1': str(Fraction(phi)),
           'gamma2': str(Fraction(gam)) if ok else None,
           'r_cl': str(Fraction(gam) / phi) if ok and phi > 0 else None, 'diag': diag,
           'kappa_witness': None if ok else '%d:%s' % (bad[0], ','.join(str(x) for x in bad[1]))}
    return rec, (phi, gam, sum(w[e] * abs(h[e]) for e in range(m)))


def expected(c):
    import json
    return _expected(json.dumps(c, sort_keys=True))


def validate_case(c):
    require(type(c['nv']) is int and c['nv'] >= 1 and len(c['edges']) >= 1, 'G1_SCHEMA:public_window_shape')
    m = len(c['edges'])
    require(all(0 <= s < c['nv'] and 0 <= t < c['nv'] for s, t in c['edges']), 'G1_SCHEMA:public_endpoints')
    require(len(c['w']) == m and len(c['h']) == m and all(type(x) is int and x > 0 for x in c['w']) and all(type(x) is int for x in c['h']),
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
        wants = {}
        for c in cases:
            r = by_id[c['id']]
            require(set(r) == KEYS, 'G1_SCHEMA:record_keys')
            require(all(is_int(r[k]) for k in ('nv', 'm', 'k', 'rank_d0', 'rank_d1', 'dim_q1')) and type(r['complex']) is bool
                    and (r['dim_h1'] is None or is_int(r['dim_h1'])), 'G1_SCHEMA:ints')
            require(all(type(r[k]) is str for k in ('phi1', 'diag', 'witness')) and all(r[k] is None or type(r[k]) is str for k in ('gamma2', 'r_cl', 'kappa_witness')),
                    'G1_SCHEMA:strings')
            want, (phi, gam, unrepaired) = expected(c)
            for key in want:
                require(r[key] == want[key], 'G3_WITNESS:' + key)
            wants[c['id']] = want
            verify_witness(c, r['witness'], phi)
            # theorem-level consistency of the candidate itself
            require(0 <= phi <= unrepaired, 'G3_WITNESS:phi_between_zero_and_unrepaired')
            if want['complex']:
                require(not (phi == 0 and gam != 0), 'G3_WITNESS:exact_class_has_closed_representative')
                require(want['dim_h1'] >= 0 and want['dim_q1'] == want['dim_h1'] + want['rank_d1'], 'G3_WITNESS:exact_sequence_dimensions')
            else:
                require(r['dim_h1'] is None and r['r_cl'] is None and r['gamma2'] is None and r['diag'] == 'NotAWindow', 'G3_WITNESS:refusal_shape')
        # repair invariance: windows with the same structure whose cochains differ by a coboundary carry the same invariants
        shifted = 0
        for a, b in combinations(cases, 2):
            if (a['nv'], a['edges'], a['w'], a['d1']) == (b['nv'], b['edges'], b['w'], b['d1']):
                d0 = coboundary(a['nv'], a['edges'])
                diff = [x - y for x, y in zip(a['h'], b['h'])]
                if bareiss_rank([d0[e] + [diff[e]] for e in range(len(diff))]) == bareiss_rank(d0):
                    shifted += 1
                    ra, rb = by_id[a['id']], by_id[b['id']]
                    require(all(ra[k] == rb[k] for k in ('phi1', 'gamma2', 'r_cl', 'diag')), 'G3_WITNESS:invariants_depend_on_the_representative')
        require(shifted >= 1, 'G2_COVERAGE:a_gauge_shifted_pair_is_present')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ZeroDivisionError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))
    except ValueError as error:
        if str(error).startswith('G'):
            raise
        raise ValueError('G3_WITNESS:unparsable ' + str(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
