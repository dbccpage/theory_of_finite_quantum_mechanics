"""Independent checker for PG-SIX-OPERATIONS.

Recomputes every record from the public cases without importing the producer. The state machine is
re-implemented with integer bitmasks (items are bits) instead of frozensets; trace counts come from a
dynamic programme over state multiplicities (level by level) cross-checked with closed forms
sum_k (6n)^k - (6n-j)^k, instead of enumerating traces; conflation witnesses are counted over PAIRS of
states by a second dynamic programme, and the first witness (lexicographic in kind then item order) is
found by explicit search. AuthorityEffect: None.
"""
import sys
from collections import Counter
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-SIX-OPERATIONS'
KINDS = ['mention', 'supply', 'designate', 'admit', 'retain', 'operate']
CONFLATIONS = {
    'mention_includes_admit': ('mention', 'admit'), 'supply_includes_admit': ('supply', 'admit'),
    'designate_includes_admit': ('designate', 'admit'), 'retain_includes_admit': ('retain', 'admit'),
    'operate_includes_admit': ('operate', 'admit'), 'designate_includes_retain': ('designate', 'retain'),
    'mention_includes_supply': ('mention', 'supply'),
}
KEYS = {
    'trace': {'kind', 'items', 'max_len', 'init_mask', 'traces', 'changed', 'with_admit', 'with_new_admit', 'mismatches', 'distinct_final_states'},
    'footprint': {'kind', 'op', 'new_item_fields', 'old_item_fields'},
    'pair': {'kind', 'a', 'b', 'min_len', 'contexts'},
    'conflation': {'kind', 'name', 'min_len', 'witness_count', 'witness', 'six_state', 'conflated_state', 'differing_fields', 'admitted_differs'},
    'reading': {'kind', 'token', 'conflation', 'six_L_admitted', 'six_F_admitted', 'conflated_L_admitted', 'conflated_F_admitted', 'six_separated', 'conflated_separated'},
}
BOOLS = {'admitted_differs', 'six_separated', 'conflated_separated'}
STRS = {'kind', 'op', 'a', 'b', 'name', 'conflation', 'new_item_fields', 'old_item_fields', 'differing_fields'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


# State: (mentioned mask, supplied mask, designated 0|item+1, admitted mask, retained mask, outputs mask)
def mstep(s, kind, x):
    bit = 1 << x
    m, u, d, a, r, o = s
    if kind == 'mention':
        return (m | bit, u, d, a, r, o)
    if kind == 'supply':
        return (m, u | bit, d, a, r, o)
    if kind == 'designate':
        return (m, u, x + 1, a, r, o)
    if kind == 'admit':
        return (m, u, d, a | bit, r, o)
    if kind == 'retain':
        return (m, u, d, a, r | bit, o) if a & bit else s
    return (m, u, d, a, r, o | bit) if a & bit else s


def bits(mask, items=2):
    return [i for i in range(items) if mask >> i & 1]


def listed(s):
    return [bits(s[0]), bits(s[1]), [s[2] - 1] if s[2] else [], bits(s[3]), bits(s[4]), bits(s[5])]


def diff_fields(a, b):
    return ''.join('1' if a[i] != b[i] else '0' for i in range(6))


def trace_expected(items, max_len, mask):
    n_ops = 6 * items
    init = (0, 0, 0, mask, 0, 0)
    # state of the programme: (machine state, an Admit occurred, an Admit of an item outside the initial admitted set occurred)
    level = Counter({(init, False, False): 1})
    total = changed = with_admit_dp = with_new_dp = mismatches = 0
    seen = {init}
    for length in range(max_len + 1):
        total += sum(level.values())
        for (st, has_admit, has_new), c in level.items():
            moved = st[3] != mask
            changed += c * moved
            with_admit_dp += c * has_admit
            with_new_dp += c * has_new
            mismatches += c * (moved != has_new)
        if length < max_len:
            nxt = Counter()
            for (st, has_admit, has_new), c in level.items():
                for kind in KINDS:
                    for x in range(items):
                        is_admit = kind == 'admit'
                        nxt[(mstep(st, kind, x), has_admit or is_admit, has_new or (is_admit and not (mask >> x & 1)))] += c
            level = nxt
            seen.update(key[0] for key in level)
    known = items - bin(mask).count('1')
    closed_total = sum(n_ops ** k for k in range(max_len + 1))
    with_admit = closed_total - sum((n_ops - items) ** k for k in range(max_len + 1))
    with_new = closed_total - sum((n_ops - known) ** k for k in range(max_len + 1))
    require(total == closed_total, 'G3_WITNESS:trace_total_closed_form')
    require(with_admit_dp == with_admit and with_new_dp == with_new, 'G3_WITNESS:admit_counts_closed_form')
    return {'kind': 'trace', 'items': items, 'max_len': max_len, 'init_mask': mask, 'traces': total, 'changed': changed,
            'with_admit': with_admit_dp, 'with_new_admit': with_new_dp, 'mismatches': mismatches, 'distinct_final_states': len(seen)}


def footprint_expected(kind):
    probe = (0, 0, 0, 1, 0, 0)
    return {'kind': 'footprint', 'op': kind,
            'new_item_fields': diff_fields(probe, mstep(probe, kind, 1)), 'old_item_fields': diff_fields(probe, mstep(probe, kind, 0))}


def pair_expected(a, b):
    level = Counter({(0, 0, 0, 0, 0, 0): 1})
    min_len, contexts = -1, 0
    for length in range(4):
        hits = sum(c * sum(1 for x in range(2) if mstep(st, a, x) != mstep(st, b, x)) for st, c in level.items())
        if hits and min_len < 0:
            min_len = length
        if length <= 2:
            contexts += hits
        nxt = Counter()
        for st, c in level.items():
            for kind in KINDS:
                for x in range(2):
                    nxt[mstep(st, kind, x)] += c
        level = nxt
    return {'kind': 'pair', 'a': a, 'b': b, 'min_len': min_len, 'contexts': contexts}


def conflation_expected(name):
    a_kind, b_kind = CONFLATIONS[name]
    ops = [(k, x) for k in KINDS for x in range(2)]
    z = (0, 0, 0, 0, 0, 0)
    level = Counter({(z, z): 1})
    for length in range(1, 5):
        nxt = Counter()
        for (s6, sc), c in level.items():
            for kind, x in ops:
                nxt[(mstep(s6, kind, x), conf_step(sc, kind, x, a_kind, b_kind))] += c
        level = nxt
        count = sum(c for (s6, sc), c in level.items() if s6 != sc)
        if count:
            for trace in product(ops, repeat=length):
                s6, sc = z, z
                for kind, x in trace:
                    s6, sc = mstep(s6, kind, x), conf_step(sc, kind, x, a_kind, b_kind)
                if s6 != sc:
                    return {'kind': 'conflation', 'name': name, 'min_len': length, 'witness_count': count,
                            'witness': ['%s:%d' % op for op in trace], 'six_state': listed(s6), 'conflated_state': listed(sc),
                            'differing_fields': diff_fields(s6, sc), 'admitted_differs': s6[3] != sc[3]}
    raise ValueError('G3_WITNESS:no_conflation_witness')


def conf_step(s, kind, x, a_kind, b_kind):
    if kind == a_kind:
        s = mstep(s, b_kind, x)
    return mstep(s, kind, x)


READING_MODELS = {'supply_includes_admit': ('supply', 'admit'), 'admit_includes_supply': ('admit', 'supply')}


def reading_expected(token, name):
    a_kind, b_kind = READING_MODELS[name]
    z = (0, 0, 0, 0, 0, 0)
    six_l = mstep(z, 'supply', token)[3]
    six_f = mstep(mstep(z, 'supply', token), 'admit', token)[3]
    after_supply = conf_step(z, 'supply', token, a_kind, b_kind)
    conf_l = after_supply[3]
    conf_f = conf_step(after_supply, 'admit', token, a_kind, b_kind)[3]
    return {'kind': 'reading', 'token': token, 'conflation': name, 'six_L_admitted': bits(six_l), 'six_F_admitted': bits(six_f),
            'conflated_L_admitted': bits(conf_l), 'conflated_F_admitted': bits(conf_f),
            'six_separated': six_l != six_f, 'conflated_separated': conf_l != conf_f}


_CACHE = {}


def expected(case):
    key = repr(case)
    if key not in _CACHE:
        kind = case[0]
        if kind == 'trace':
            _CACHE[key] = trace_expected(case[1], case[2], case[3])
        elif kind == 'footprint':
            _CACHE[key] = footprint_expected(case[1])
        elif kind == 'pair':
            _CACHE[key] = pair_expected(case[1], case[2])
        elif kind == 'conflation':
            _CACHE[key] = conflation_expected(case[1])
        elif kind == 'reading':
            _CACHE[key] = reading_expected(case[1], case[2])
        else:
            raise ValueError('G2_COVERAGE:unknown_case_kind')
    return _CACHE[key]


def key_of(r):
    k = r['kind']
    if k == 'trace':
        return repr((k, r['items'], r['max_len'], r['init_mask']))
    if k == 'footprint':
        return repr((k, r['op']))
    if k == 'pair':
        return repr((k, r['a'], r['b']))
    if k == 'conflation':
        return repr((k, r['name']))
    return repr((k, r['token'], r['conflation']))


def check_types(r):
    kind = r['kind']
    require(type(kind) is str and kind in KEYS and set(r) == KEYS[kind], 'G1_SCHEMA:record_keys')
    for k, v in r.items():
        if k in BOOLS:
            require(type(v) is bool, 'G1_SCHEMA:bool_field')
        elif k in STRS:
            require(type(v) is str, 'G1_SCHEMA:string_field')
        elif k == 'witness':
            require(type(v) is list and v and all(type(t) is str for t in v), 'G1_SCHEMA:witness')
        elif k in ('six_state', 'conflated_state'):
            require(type(v) is list and len(v) == 6 and all(type(c) is list and all(is_int(i) for i in c) for c in v), 'G1_SCHEMA:state')
        elif k in ('six_L_admitted', 'six_F_admitted', 'conflated_L_admitted', 'conflated_F_admitted'):
            require(type(v) is list and all(is_int(i) for i in v), 'G1_SCHEMA:admitted_list')
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
            if r['kind'] == 'trace':
                require(r['mismatches'] == 0 and r['changed'] == r['with_new_admit'], 'G3_WITNESS:only_a_new_admit_changes_admitted')
            if r['kind'] == 'footprint':
                require(r['op'] == 'admit' or r['new_item_fields'][3] == '0' and r['old_item_fields'][3] == '0', 'G3_WITNESS:only_admit_writes_admitted')
            if r['kind'] == 'reading':
                require(r['six_separated'] and r['conflated_separated'] == (r['conflation'] == 'admit_includes_supply'), 'G3_WITNESS:readings_collapse_only_when_supply_admits')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ZeroDivisionError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
