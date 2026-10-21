"""Independent checker for PG-DEMAND-ACCOUNTING.

Recomputes every record without importing the producer and by different algorithms:
* demand records: a dynamic program over the u universe elements. Each element is in one of 8 states (in W?, in D?,
  in B?); the program tracks (|W|, |D|, |B|, x, y) where x = |D minus W| and y = |(W minus D) intersect B|, with its
  multiplicity. The next cardinality is |W| - |D| + x + |B| - y; the hypotheses hold iff x = 0 and y = 0.
* sequence records: the admissible (|D|, |B|) splits of a step are found by enumerating every D inside W = range(s)
  and every B outside the survivors with the right size (set enumeration, not the arithmetic of the producer).
* listreg records: closed forms. Duplicate-free lists of length k over a letters number a!/(a-k)!; for k active letters
  and j survivors there are C(k,j) 2^(a-k) (list, discharge) choices; duplicate-free births of length m avoiding j
  letters number (a-j)!/(a-j-m)!.
AuthorityEffect: None.
"""
import itertools
import json
import sys
from math import comb, perm
from pathlib import Path

ROOT = next((p for p in Path(__file__).resolve().parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-DEMAND-ACCOUNTING'
LISTREG_FIELDS = ['total', 'identity_holds', 'nodup_inputs', 'disjoint_inputs', 'nodup_when_disjoint', 'nodup_when_overlap']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def expected_demand(u):
    states = [(w, d, b) for w in (0, 1) for d in (0, 1) for b in (0, 1)]
    dist = {(0, 0, 0, 0, 0): 1}
    for _ in range(u):
        new = {}
        for (s, d, b, x, y), mult in dist.items():
            for (w, dd, bb) in states:
                key = (s + w, d + dd, b + bb, x + (1 if (dd and not w) else 0), y + (1 if (w and not dd and bb) else 0))
                new[key] = new.get(key, 0) + mult
        dist = new
    tally = [[0, 0, 0] for _ in range(4)]
    for (s, d, b, x, y), mult in dist.items():
        card = s - d + x + b - y
        k = (1 if x > 0 else 0) + (2 if y > 0 else 0)
        tally[k][0] += mult
        if card == s - d + b:
            tally[k][1] += mult
        if card == max(0, s - d) + b:
            tally[k][2] += mult
    return {'kind': 'demand', 'u': u, 'total': 8 ** u, 'classes': tally}


def split_pairs(s, t):
    """The set of (|D|, |B|) over admissible (W = range(s), D, B): D inside W, B avoiding the survivors, |next| = t."""
    universe = list(range(s + t))
    w = frozenset(range(s))
    pairs = set()
    for bits in itertools.product((0, 1), repeat=s):
        d = frozenset(i for i, bit in enumerate(bits) if bit)
        surv = w - d
        rest = [i for i in universe if i not in surv]
        need = t - len(surv)
        if need < 0:
            continue
        for b in itertools.combinations(rest, need):
            if len(surv | frozenset(b)) == t:
                pairs.add((len(d), len(b)))
    return pairs


def expected_sequence(seq):
    steps = list(zip(seq[:-1], seq[1:]))
    counts = [len(split_pairs(s, t)) for s, t in steps]
    return {'kind': 'sequence', 'seq': list(seq), 'decompositions': counts, 'underdetermined': any(c >= 2 for c in counts)}


def expected_listreg(a, maxlen):
    nlists = sum(a ** k for k in range(maxlen + 1))
    total = nlists * (2 ** a) * nlists
    nodup_lists = sum(perm(a, k) for k in range(maxlen + 1))
    nodup_inputs = nodup_lists * (2 ** a) * nodup_lists
    disjoint = 0
    for k in range(maxlen + 1):
        for j in range(k + 1):
            births = sum(perm(a - j, m) for m in range(maxlen + 1))
            disjoint += perm(a, k) * comb(k, j) * (2 ** (a - k)) * births
    return {'kind': 'listreg', 'input': [a, maxlen], 'total': total, 'identity_holds': total, 'nodup_inputs': nodup_inputs,
            'disjoint_inputs': disjoint, 'nodup_when_disjoint': disjoint, 'nodup_when_overlap': 0}


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = public['cases']
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        want_keys = sorted(json.dumps(c, sort_keys=True) for c in cases)
        got_keys = []
        for r in records:
            require(type(r) is dict and type(r.get('kind')) is str, 'G1_SCHEMA:record')
            if r['kind'] == 'demand':
                require(set(r) == {'kind', 'u', 'total', 'classes'}, 'G1_SCHEMA:demand_keys')
                require(is_int(r['u']) and 0 <= r['u'] <= 6, 'G1_SCHEMA:u')
                require(is_int(r['total']), 'G1_SCHEMA:total')
                require(type(r['classes']) is list and all(type(c) is list and all(is_int(v) for v in c) for c in r['classes']), 'G1_SCHEMA:classes')
                got_keys.append(json.dumps(['demand', r['u']], sort_keys=True))
                want = expected_demand(r['u'])
                require(r['total'] == want['total'], 'G3_WITNESS:total')
                require(r['classes'] == want['classes'], 'G3_WITNESS:classes')
                # theorem-level consistency of the candidate itself
                require(r['classes'][0][1] == r['classes'][0][0] and r['classes'][0][2] == r['classes'][0][0],
                        'G3_WITNESS:identity_must_hold_when_both_hypotheses_hold')
                require(r['classes'][1][1] == 0 and r['classes'][2][1] == 0,
                        'G3_WITNESS:integer_identity_must_fail_for_a_single_violation')
                require(sum(c[0] for c in r['classes']) == r['total'], 'G3_WITNESS:classes_partition_total')
                require(r['classes'][0][0] == 5 ** r['u'], 'G3_WITNESS:births_may_coincide_with_discharged_elements')
            elif r['kind'] == 'sequence':
                require(set(r) == {'kind', 'seq', 'decompositions', 'underdetermined'}, 'G1_SCHEMA:sequence_keys')
                require(type(r['seq']) is list and all(is_int(v) and 0 <= v <= 8 for v in r['seq']), 'G1_SCHEMA:seq')
                require(type(r['decompositions']) is list and all(is_int(v) for v in r['decompositions']), 'G1_SCHEMA:decompositions')
                require(type(r['underdetermined']) is bool, 'G1_SCHEMA:flags')
                got_keys.append(json.dumps(['sequence', r['seq']], sort_keys=True))
                want = expected_sequence(r['seq'])
                require(r['decompositions'] == want['decompositions'], 'G3_WITNESS:decompositions')
                require(r['underdetermined'] == want['underdetermined'], 'G3_WITNESS:underdetermined')
            elif r['kind'] == 'listreg':
                require(set(r) == {'kind', 'input'} | set(LISTREG_FIELDS), 'G1_SCHEMA:listreg_keys')
                require(type(r['input']) is list and len(r['input']) == 2 and all(is_int(v) and v >= 0 for v in r['input']), 'G1_SCHEMA:listreg_input')
                require(all(is_int(r[k]) for k in LISTREG_FIELDS), 'G1_SCHEMA:listreg_fields')
                a, maxlen = r['input']
                require(a <= 4 and maxlen <= 4, 'G1_SCHEMA:listreg_range')
                got_keys.append(json.dumps(['listreg', a, maxlen], sort_keys=True))
                want = expected_listreg(a, maxlen)
                for k in LISTREG_FIELDS:
                    require(r[k] == want[k], 'G3_WITNESS:listreg_' + k)
                require(r['identity_holds'] == r['total'], 'G3_WITNESS:list_length_identity_needs_no_disjointness')
                require(r['nodup_when_overlap'] == 0 and r['nodup_when_disjoint'] == r['disjoint_inputs'], 'G3_WITNESS:nodup_iff_disjoint')
                require(r['disjoint_inputs'] < r['nodup_inputs'] or r['input'][0] == 0, 'G3_WITNESS:overlap_cases_exist')
            else:
                raise ValueError('G1_SCHEMA:kind')
        require(sorted(got_keys) == want_keys, 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
