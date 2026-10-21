"""Independent checker for PG-WDP-GROWTH-NO-REPAIR.

Recomputes every record from the public window pairs without importing the producer. Phi1 of both windows is obtained from
the DUAL linear program (vertices of {y : d0^T y = 0, |y_e| <= w_e}); the certificate also carries a primal potential x and a
dual vector y per window and the checker VERIFIES them exactly (cost(x) = y.h = Phi1, d0^T y = 0, |y_e| <= w_e, the statement of
the kernel theorem isPhi_of_certificate). Ranks use fraction-free (Bareiss) elimination; the second window of a pair is rebuilt
from the operation with a different decomposition (row filter by support complement). Gamma2 is the representative norm
||d1 h||_1, which equals the source's value at the minimal residual only when d1 d0 = 0, so it is withheld for a non-window.
Theorem-level checks: restriction with weights not raised never raises Phi1 (this includes all 63 edge subsets of K4);
attaching a valid 2-cell leaves Phi1 unchanged and does not lower Gamma2. AuthorityEffect: None.
"""
import json
import sys
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path

ROOT = next((p for p in Path(__file__).resolve().parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-WDP-GROWTH-NO-REPAIR'
KEYS = {'id', 'kind', 'm_a', 'm_b', 'k_a', 'k_b', 'complex_a', 'complex_b', 'phi_a', 'phi_b', 'gamma_a', 'gamma_b',
        'diag_a', 'diag_b', 'verdict', 'witness_a', 'witness_b'}
EXPECTED_IDS = ['k4_restrict_to_triangle', 'k4_restrict_triangle_pendant', 'k4_restrict_one_edge', 'k4_restrict_disjoint_edges',
                'k4_restrict_five_edges', 'k4_restrict_four_cycle', 'parallel_restrict_equal_weights', 'parallel_restrict_rescaled_weights',
                'parallel_restrict_downweighted', 'tri_unfilled_attach_face', 'tri_exact_attach_duplicate_face', 'tri_active_attach_scaled_face',
                'tri_attach_invalid_row', 'square_attach_filling_face', 'loop_attach_face', 'tri_edit_h_to_exact', 'tri_edit_h_gauge_shift',
                'tri_edit_w_down', 'tri_edit_w_up'] + ['k4_sub_%02d' % mask for mask in range(1, 64)]


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


def parse_fractions(text, count):
    parts = text.split(',')
    require(len(parts) == count, 'G3_WITNESS:witness_length')
    out = []
    for part in parts:
        value = Fraction(part)
        require(str(value) == part, 'G3_WITNESS:witness_not_canonical')
        out.append(value)
    return out


def verify_witness(nv, edges, w, h, text, phi):
    m = len(edges)
    require(type(text) is str and text.startswith('x=') and '|y=' in text and text.count('|') == 1, 'G3_WITNESS:witness_shape')
    xt, yt = text[2:].split('|y=')
    x, y = parse_fractions(xt, nv), parse_fractions(yt, m)
    d0 = coboundary(nv, edges)
    require(all(sum(y[e] * d0[e][v] for e in range(m)) == 0 for v in range(nv)), 'G3_WITNESS:dual_not_annihilating_coboundaries')
    require(all(abs(y[e]) <= w[e] for e in range(m)), 'G3_WITNESS:dual_exceeds_weights')
    primal = sum(w[e] * abs(h[e] - sum(d0[e][v] * x[v] for v in range(nv))) for e in range(m))
    require(primal == phi and sum(y[e] * h[e] for e in range(m)) == phi, 'G3_WITNESS:primal_dual_values_differ')


def second_window(c):
    """Rebuild window B of a pair from the operation, independently of the producer."""
    nv, edges, w, d1, h = c['nv'], c['edges'], c['w'], c['d1'], c['h']
    kind, arg = c['kind'], c['arg']
    if kind == 'restrict':
        keep_text, new_w = arg.split('|')
        keep = list(map(int, keep_text.split(',')))
        outside = [e for e in range(len(edges)) if e not in keep]
        rows = []
        for row in d1:
            if not any(row[e] for e in outside):
                rows.append([row[e] for e in keep])
        new_weights = [w[e] for e in keep] if new_w == '-' else list(map(int, new_w.split(',')))
        return nv, [edges[e] for e in keep], new_weights, rows, [h[e] for e in keep]
    if kind == 'attach':
        return nv, edges, w, d1 + [list(map(int, part.split(','))) for part in arg.split(';')], h
    if kind == 'edit_h':
        return nv, edges, w, d1, list(map(int, arg.split(',')))
    if kind == 'edit_w':
        return nv, edges, list(map(int, arg.split(','))), d1, h
    raise ValueError('G1_SCHEMA:kind')


def summary(nv, edges, w, d1, h):
    d0 = coboundary(nv, edges)
    m = len(edges)
    ok = all(sum(row[e] * d0[e][v] for e in range(m)) == 0 for row in d1 for v in range(nv))
    phi = dual_phi(nv, edges, w, h)
    gam = sum(abs(sum(row[e] * h[e] for e in range(m))) for row in d1)
    cls = ('ExactClass' if phi == 0 else ('ClosedResidual' if gam == 0 else 'ActiveClosureFailure')) if ok else 'NotAWindow'
    return ok, phi, gam, cls


@lru_cache(maxsize=None)
def _expected(key):
    c = json.loads(key)
    ok_a, phi_a, gam_a, cls_a = summary(c['nv'], c['edges'], c['w'], c['d1'], c['h'])
    nvb, eb, wb, db, hb = second_window(c)
    ok_b, phi_b, gam_b, cls_b = summary(nvb, eb, wb, db, hb)
    kind = c['kind']
    if kind == 'restrict':
        verdict = 'sub_phi_le' if phi_b <= phi_a else 'sub_phi_gt'
    elif kind == 'attach':
        if not ok_b:
            verdict = 'attach_not_a_window'
        elif phi_b != phi_a:
            verdict = 'attach_phi_changed'
        else:
            verdict = 'phi_equal_gamma_up' if gam_b > gam_a else 'phi_equal_gamma_same'
    else:
        verdict = 'phi_lower' if phi_b < phi_a else ('phi_same' if phi_b == phi_a else 'phi_higher')
    rec = {'id': c['id'], 'kind': kind, 'm_a': len(c['edges']), 'm_b': len(eb), 'k_a': len(c['d1']), 'k_b': len(db),
           'complex_a': ok_a, 'complex_b': ok_b, 'phi_a': str(Fraction(phi_a)), 'phi_b': str(Fraction(phi_b)),
           'gamma_a': str(Fraction(gam_a)) if ok_a else None, 'gamma_b': str(Fraction(gam_b)) if ok_b else None,
           'diag_a': cls_a, 'diag_b': cls_b, 'verdict': verdict}
    weights_ok = None
    if kind == 'restrict':
        weights_ok = all(x <= c['w'][e] for x, e in zip(wb, map(int, c['arg'].split('|')[0].split(','))))
    return rec, (phi_a, phi_b, gam_a, gam_b, ok_a, ok_b, weights_ok), (nvb, eb, wb, hb)


def expected(c):
    return _expected(json.dumps(c, sort_keys=True))


def validate_case(c):
    require(type(c['nv']) is int and c['nv'] >= 1 and len(c['edges']) >= 1, 'G1_SCHEMA:public_window_shape')
    m = len(c['edges'])
    require(all(0 <= s < c['nv'] and 0 <= t < c['nv'] for s, t in c['edges']), 'G1_SCHEMA:public_endpoints')
    require(len(c['w']) == m and len(c['h']) == m and all(type(x) is int and x > 0 for x in c['w']) and all(type(x) is int for x in c['h']),
            'G1_SCHEMA:public_weights_cochain')
    require(all(len(row) == m and all(type(x) is int for x in row) for row in c['d1']), 'G1_SCHEMA:public_d1')
    d0 = coboundary(c['nv'], c['edges'])
    require(all(sum(row[e] * d0[e][v] for e in range(m)) == 0 for row in c['d1'] for v in range(c['nv'])), 'G1_SCHEMA:public_base_window_is_closed')


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
        subsets = 0
        for c in cases:
            r = by_id[c['id']]
            require(type(r) is dict and set(r) == KEYS, 'G1_SCHEMA:record_keys')
            require(all(is_int(r[k]) for k in ('m_a', 'm_b', 'k_a', 'k_b')) and type(r['complex_a']) is bool and type(r['complex_b']) is bool,
                    'G1_SCHEMA:ints_bools')
            require(all(type(r[k]) is str for k in ('id', 'kind', 'phi_a', 'phi_b', 'diag_a', 'diag_b', 'verdict', 'witness_a', 'witness_b'))
                    and all(r[k] is None or type(r[k]) is str for k in ('gamma_a', 'gamma_b')), 'G1_SCHEMA:strings')
            want, (phi_a, phi_b, gam_a, gam_b, ok_a, ok_b, weights_ok), (nvb, eb, wb, hb) = expected(c)
            for key in want:
                require(r[key] == want[key], 'G3_WITNESS:' + key)
            verify_witness(c['nv'], c['edges'], c['w'], c['h'], r['witness_a'], phi_a)
            verify_witness(nvb, eb, wb, hb, r['witness_b'], phi_b)
            # theorem-level checks of the pair itself
            if c['kind'] == 'restrict' and weights_ok:
                require(phi_b <= phi_a, 'G3_WITNESS:restriction_with_restricted_weights_raised_phi1')
                subsets += c['id'].startswith('k4_sub_')
            if c['kind'] == 'attach' and ok_b:
                require(phi_b == phi_a and gam_b >= gam_a, 'G3_WITNESS:attachment_changed_phi1_or_lowered_gamma2')
        require(subsets == 63, 'G2_COVERAGE:all_63_k4_edge_subsets_checked')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ZeroDivisionError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))
    except ValueError as error:
        if str(error).startswith('G'):
            raise
        raise ValueError('G3_WITNESS:unparsable ' + str(error))


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
