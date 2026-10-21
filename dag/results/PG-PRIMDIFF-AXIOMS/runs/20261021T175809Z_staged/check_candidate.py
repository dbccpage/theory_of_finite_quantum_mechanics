"""Independent checker for PG-PRIMDIFF-AXIOMS.

Recomputes every record from the public cases without importing the producer, by different algorithms:
structures as bitmasks (producer: edge lists and integer matrices); A4 by mask transposition; A5 and A7 by the face
rule "boundary edges all present or all absent" and by brute force over all potentials in {-1,0,1}^n respectively
(producer: matrix product and unit vectors); the closure record by the intersection of all preorders containing the
relation and by boolean matrix power; kernel counts by closed forms; the triad tables by brute-force potentials in a
box (producer: spanning forests). AuthorityEffect: None.
"""
import sys
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-PRIMDIFF-AXIOMS'
NAMES = ['A01NonIdentification', 'A02UnentailedAdmission', 'A03EvaluationRelation', 'A04DirectedEvaluationCarrier',
         'A05NilpotentCoboundary', 'A06QuotientDefectPurity', 'A07DescendedClosureMap', 'A08TriadTrichotomy',
         'A09ObserverSelectedMetric', 'A10AntiReificationFirewall']
STATUS = ['state_predicate', 'not_a_state_predicate', 'theorem_true_in_every_structure', 'state_predicate', 'state_predicate',
          'checked_on_named_complexes', 'equivalent_to_A5', 'checked_on_named_complexes', 'checked_on_named_complexes',
          'state_predicate']
KEYS = {
    'axiom': {'kind', 'index', 'name', 'status', 'models_by_n'},
    'models': {'kind', 'n', 'total', 'all_hold', 'violate_only', 'violate_a5_a7_jointly', 'a5_equals_a7', 'well_formed_models',
               'a5_without_well_formed', 'distinct_signatures'},
    'unentailed': {'kind', 'n', 'models', 'offdiag_pairs', 'with_each_offdiag_pair', 'without_each_offdiag_pair',
                   'diagonal_pairs_in_a_model', 'models_with_empty_d'},
    'kernel': {'kind', 'n', 'probes', 'ok', 'err_a1', 'err_carrier', 'token_irrelevant', 'empty_token_admitted', 'duplicates_stored',
               'reverse_orientation_admitted', 'a1_before_carrier'},
    'closure': {'kind', 'n', 'relations', 'distinct_closures', 'all_preorders', 'contains_relation', 'equals_reachability'},
    'triad': {'kind', 'name', 'n', 'edges', 'faces', 'cochains', 'exact', 'closed_nonexact', 'rupture', 'exact_nonclosed',
              'rcl_refusals', 'phi1_sum', 'phi1_max', 'gauge_invariant', 'relabel_invariant', 'nilpotent', 'well_formed'},
}
BOOLS = {'a5_equals_a7', 'token_irrelevant', 'empty_token_admitted', 'duplicates_stored', 'reverse_orientation_admitted',
         'a1_before_carrier', 'all_preorders', 'contains_relation', 'equals_reachability', 'gauge_invariant', 'relabel_invariant',
         'nilpotent', 'well_formed'}
STRS = {'kind', 'name', 'status'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


# ---------------------------------------------------------------- bitmask structures
def bit(n, u, v):
    return 1 << (u * n + v)


def diag_mask(n):
    return sum(bit(n, u, u) for u in range(n))


def transpose(n, mask):
    return sum(bit(n, v, u) for u in range(n) for v in range(n) if mask & bit(n, u, v))


def face_edge_mask(n):
    return bit(n, 0, 1) | bit(n, 1, 2) | bit(n, 0, 2)


def a5_mask(n, e, f):
    if not f:
        return True
    present = bin(e & face_edge_mask(n)).count('1')
    return present in (0, 3)


def a7_mask(n, e, f):
    """d1 vanishes on every potential: brute force over {-1,0,1}^n (descent to the quotient by im d0)."""
    if not f:
        return True
    for phi in product((-1, 0, 1), repeat=n):
        def psi(u, v):
            return phi[v] - phi[u] if e & bit(n, u, v) else 0
        if psi(1, 2) - psi(0, 2) + psi(0, 1) != 0:
            return False
    return True


def a3_mask(n, e):
    """reflexive-transitive closure by boolean matrix power is a preorder containing e"""
    a = [[1 if (u == v or e & bit(n, u, v)) else 0 for v in range(n)] for u in range(n)]
    power = [row[:] for row in a]
    for _ in range(max(n, 1)):
        power = [[1 if any(power[i][k] and a[k][j] for k in range(n)) else 0 for j in range(n)] for i in range(n)]
    refl = all(power[i][i] for i in range(n))
    trans = all(not (power[i][j] and power[j][k]) or power[i][k] for i in range(n) for j in range(n) for k in range(n))
    return bool(refl and trans and all(power[u][v] for u in range(n) for v in range(n) if e & bit(n, u, v)))


def hist(n):
    d_hist, ef_hist = {}, {}
    for d in range(1 << (n * n)):
        s = (d & diag_mask(n)) == 0
        d_hist[s] = d_hist.get(s, 0) + 1
    for e in range(1 << (n * n)):
        for f in ((0, 1) if n == 3 else (0,)):
            a4 = (e & diag_mask(n)) == 0 and (e & transpose(n, e)) == 0
            well = (not f) or (e & face_edge_mask(n)) == face_edge_mask(n)
            sig = (a3_mask(n, e), a4, a5_mask(n, e, f), a7_mask(n, e, f), well)
            ef_hist[sig] = ef_hist.get(sig, 0) + 1
    return d_hist, ef_hist


_H = {}


def get_hist(n):
    if n not in _H:
        _H[n] = hist(n)
    return _H[n]


def joint(n):
    d_hist, ef_hist = get_hist(n)
    out = {}
    for a1, cd in d_hist.items():
        for (a3, a4, a5, a7, w), ce in ef_hist.items():
            for a10 in (True, False):
                key = (a1, a3, a4, a5, a7, a10, w)
                out[key] = out.get(key, 0) + cd * ce
    return out


def axiom_expected(k):
    counts = [-1, -1, -1]
    status = STATUS[k - 1]
    if status in ('state_predicate', 'theorem_true_in_every_structure', 'equivalent_to_A5'):
        position = {1: 0, 3: 1, 4: 2, 5: 3, 7: 4, 10: 5}[k]
        counts = [sum(c for key, c in joint(n).items() if key[position]) for n in (1, 2, 3)]
    return {'kind': 'axiom', 'index': k, 'name': NAMES[k - 1], 'status': status, 'models_by_n': counts}


def models_expected(n):
    h = joint(n)
    total = sum(h.values())
    violate = [sum(c for key, c in h.items() if not key[i] and all(key[j] for j in range(6) if j != i)) for i in range(6)]
    jointly = sum(c for key, c in h.items() if not key[3] and not key[4] and all(key[j] for j in (0, 1, 2, 5)))
    all_hold = sum(c for key, c in h.items() if all(key[:6]))
    # closed forms for the two factors that make up the all-hold count
    d_models = 2 ** (n * n - n)
    antisym = 3 ** (n * (n - 1) // 2)
    face_ok = antisym if n < 3 else 27 + 9
    require(all_hold == d_models * face_ok, 'G3_WITNESS:all_hold_closed_form')
    return {'kind': 'models', 'n': n, 'total': total, 'all_hold': all_hold, 'violate_only': violate, 'violate_a5_a7_jointly': jointly,
            'a5_equals_a7': all(key[3] == key[4] for key in h), 'well_formed_models': sum(c for key, c in h.items() if key[6]),
            'a5_without_well_formed': sum(c for key, c in h.items() if key[3] and not key[6]),
            'distinct_signatures': len({key[:6] for key in h})}


def unentailed_expected(n):
    d_hist, ef_hist = get_hist(n)
    ef_models = sum(c for (a3, a4, a5, a7, w), c in ef_hist.items() if a3 and a4 and a5 and a7)
    d_models = d_hist[True]
    off = n * (n - 1)
    with_each = (d_models // 2) * ef_models  # by symmetry exactly half of the irreflexive D contain a given off-diagonal pair
    # confirm the symmetry claim by direct counting of D containing the pair (0,1)
    contain = sum(1 for d in range(1 << (n * n)) if (d & diag_mask(n)) == 0 and d & bit(n, 0, 1))
    require(contain == d_models // 2, 'G3_WITNESS:half_of_D_contains_each_pair')
    diag_in_model = sum(1 for d in range(1 << (n * n)) if (d & diag_mask(n)) == 0 and d & diag_mask(n))
    return {'kind': 'unentailed', 'n': n, 'models': d_models * ef_models, 'offdiag_pairs': off, 'with_each_offdiag_pair': with_each,
            'without_each_offdiag_pair': d_models * ef_models - with_each, 'diagonal_pairs_in_a_model': diag_in_model, 'models_with_empty_d': ef_models}


class _Kernel:
    """Independent transcription of GenesisAdmissionKernel::admit_difference: A1 first, then carrier; the token is only stored."""

    def __init__(self, n):
        self.carrier = frozenset(range(n))
        self.admitted = []

    def admit(self, a, b, token):
        if a == b:
            return 'a1'
        if not (a in self.carrier and b in self.carrier):
            return 'carrier'
        self.admitted.append((a, b, token))
        return 'ok'


def kernel_expected(n):
    tally = {'ok': 0, 'a1': 0, 'carrier': 0}
    token_irrelevant = True
    for a in range(n + 1):
        for b in range(n + 1):
            results = [_Kernel(n).admit(a, b, tok) for tok in (0, 1)]
            for r in results:
                tally[r] += 1
            token_irrelevant = token_irrelevant and results[0] == results[1]
    k = _Kernel(n)
    first = k.admit(0, 1, 0)
    second = k.admit(0, 1, 0)
    third = k.admit(1, 0, 1)
    return {'kind': 'kernel', 'n': n, 'probes': sum(tally.values()), 'ok': tally['ok'], 'err_a1': tally['a1'], 'err_carrier': tally['carrier'],
            'token_irrelevant': token_irrelevant, 'empty_token_admitted': first == 'ok',
            'duplicates_stored': second == 'ok' and k.admitted.count((0, 1, 0)) == 2, 'reverse_orientation_admitted': third == 'ok',
            'a1_before_carrier': _Kernel(n).admit(n, n, 0) == 'a1'}


def closure_expected(n):
    full = (1 << (n * n)) - 1
    cells = [(u, v) for u in range(n) for v in range(n)]

    def holds(mask, u, v):
        return bool(mask & bit(n, u, v))

    def is_preorder(mask):
        return all(holds(mask, u, u) for u in range(n)) and all(
            not (holds(mask, u, v) and holds(mask, v, w)) or holds(mask, u, w) for u in range(n) for v in range(n) for w in range(n))

    preorders = [m for m in range(full + 1) if is_preorder(m)]
    contains = reach = True
    for e in range(full + 1):
        inter = full
        for p in preorders:
            if p & e == e:
                inter &= p
        # boolean matrix power (I + A)^(n-1)
        a = [[1 if (u == v or holds(e, u, v)) else 0 for v in range(n)] for u in range(n)]
        power = [row[:] for row in a]
        for _ in range(max(n - 1, 1)):
            power = [[1 if any(power[i][k] and a[k][j] for k in range(n)) else 0 for j in range(n)] for i in range(n)]
        mask = sum(bit(n, u, v) for u, v in cells if power[u][v])
        reach = reach and mask == inter
        contains = contains and (inter & e) == e
    return {'kind': 'closure', 'n': n, 'relations': full + 1, 'distinct_closures': len(preorders), 'all_preorders': True,
            'contains_relation': contains, 'equals_reachability': reach}


def parse_edges(text):
    return [] if text == '-' else [tuple(int(x) for x in part.split('-')) for part in text.split(',')]


def triad_expected(name, n, edges_text, faces_text):
    edges, faces = parse_edges(edges_text), parse_edges(faces_text)
    touched = {x for e in edges for x in e}
    require(not touched or 0 in touched, 'G2_COVERAGE:complex_touches_vertex_zero')
    rng = range(-7, 8)

    def phi1(edge_list, h):
        best = None
        for rest in product(rng, repeat=n - 1):
            phi = (0,) + rest
            cost = sum(abs(h[i] - (phi[v] - phi[u])) for i, (u, v) in enumerate(edge_list))
            if best is None or cost < best:
                best = cost
        return best

    def coboundary(h):
        out = []
        for a, b, c in faces:
            val = 0
            for sign, e in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
                if e in edges:
                    val += sign * h[edges.index(e)]
            out.append(val)
        return out

    box = list(product((-1, 0, 1), repeat=len(edges)))
    counts = {'E': 0, 'C': 0, 'R': 0, 'X': 0}
    refusals = 0
    total = peak = 0
    gauge = relabel = True
    for h in box:
        p = phi1(edges, h)
        total += p
        peak = max(peak, p)
        cob = coboundary(h)
        closed = all(x == 0 for x in cob)
        gamma = sum(abs(x) for x in cob)
        # R_cl on (Phi, Gamma): Fraction(gamma, phi) when phi != 0; 0 when both vanish; refusal (None) otherwise
        ratio = Fraction(gamma, p) if p != 0 else (Fraction(0) if gamma == 0 else None)
        refusals += ratio is None
        counts['E' if p == 0 and closed else 'X' if p == 0 else 'C' if closed else 'R'] += 1
        for psi in product((-1, 0, 1), repeat=n):
            shifted = [h[i] + psi[v] - psi[u] for i, (u, v) in enumerate(edges)]
            if phi1(edges, shifted) != p:
                gauge = False
        for perm in permutations(range(n)):
            if phi1([(perm[u], perm[v]) for u, v in edges], h) != p:
                relabel = False
    present_ok = all(sum(1 for e in ((a, b), (b, c), (a, c)) if e in edges) in (0, 3) for a, b, c in faces)
    well = all(all(e in edges for e in ((a, b), (b, c), (a, c))) for a, b, c in faces)
    return {'kind': 'triad', 'name': name, 'n': n, 'edges': [list(e) for e in edges], 'faces': [list(f) for f in faces],
            'cochains': len(box), 'exact': counts['E'], 'closed_nonexact': counts['C'], 'rupture': counts['R'],
            'exact_nonclosed': counts['X'], 'rcl_refusals': refusals, 'phi1_sum': total, 'phi1_max': peak,
            'gauge_invariant': gauge, 'relabel_invariant': relabel, 'nilpotent': present_ok, 'well_formed': well}


_CACHE = {}


def expected(case):
    key = repr(case)
    if key not in _CACHE:
        kind = case[0]
        if kind == 'axiom':
            _CACHE[key] = axiom_expected(case[1])
        elif kind == 'models':
            _CACHE[key] = models_expected(case[1])
        elif kind == 'unentailed':
            _CACHE[key] = unentailed_expected(case[1])
        elif kind == 'kernel':
            _CACHE[key] = kernel_expected(case[1])
        elif kind == 'closure':
            _CACHE[key] = closure_expected(case[1])
        elif kind == 'triad':
            _CACHE[key] = triad_expected(case[1], case[2], case[3], case[4])
        else:
            raise ValueError('G2_COVERAGE:unknown_case_kind')
    return _CACHE[key]


def key_of(r):
    k = r['kind']
    if k == 'axiom':
        return repr((k, r['index']))
    if k == 'triad':
        return repr((k, r['name']))
    return repr((k, r['n']))


def check_types(r):
    kind = r['kind']
    require(type(kind) is str and kind in KEYS and set(r) == KEYS[kind], 'G1_SCHEMA:record_keys')
    for k, v in r.items():
        if k in BOOLS:
            require(type(v) is bool, 'G1_SCHEMA:bool_field')
        elif k in STRS:
            require(type(v) is str, 'G1_SCHEMA:string_field')
        elif k == 'models_by_n':
            require(type(v) is list and len(v) == 3 and all(is_int(x) for x in v), 'G1_SCHEMA:models_by_n')
        elif k == 'violate_only':
            require(type(v) is list and len(v) == 6 and all(is_int(x) for x in v), 'G1_SCHEMA:violate_only')
        elif k in ('edges', 'faces'):
            require(type(v) is list and all(type(t) is list and all(is_int(x) for x in t) for t in v), 'G1_SCHEMA:edge_list')
        else:
            require(is_int(v), 'G1_SCHEMA:int_field')


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = public['cases']
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        for r in records:
            require(type(r) is dict and 'kind' in r, 'G1_SCHEMA:record')
            check_types(r)
        want = {key_of(expected(c)): expected(c) for c in cases}
        require(len(want) == len(cases), 'G2_COVERAGE:duplicate_cases')
        got = {key_of(r): r for r in records}
        require(len(got) == len(records) and set(got) == set(want), 'G2_COVERAGE:records_are_the_public_cases')
        for k, r in got.items():
            w = want[k]
            for field in w:
                require(r[field] == w[field], 'G3_WITNESS:%s:%s' % (r['kind'], field))
            # Reading of the candidate itself, beyond recomputation:
            if r['kind'] == 'models':
                require(r['a5_equals_a7'] and r['violate_only'][1] == 0 and r['violate_only'][3] == 0 and r['violate_only'][4] == 0,
                        'G3_WITNESS:a3_always_a5_equals_a7')
                require((r['violate_a5_a7_jointly'] > 0) == (r['n'] >= 3), 'G3_WITNESS:a5_independent_only_from_three_vertices')
                require(r['all_hold'] > 0, 'G3_WITNESS:axioms_jointly_consistent')
            if r['kind'] == 'kernel':
                require(r['token_irrelevant'] and r['empty_token_admitted'], 'G3_WITNESS:token_is_stored_not_checked')
            if r['kind'] == 'triad':
                require((r['rcl_refusals'] > 0) == (not r['nilpotent']), 'G3_WITNESS:r_cl_refuses_only_without_nilpotence')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ZeroDivisionError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
