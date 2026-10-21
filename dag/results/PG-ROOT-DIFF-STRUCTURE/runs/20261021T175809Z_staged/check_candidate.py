"""Independent checker for PG-ROOT-DIFF-STRUCTURE (an admitted primitive: nothing here derives either channel).

Recomputes every record from the public cases without importing the producer: counts of maps out of the
coproduct by the closed forms c^(a+b) = c^a * c^b, the number of retractions onto a channel as |channel|^|other|
(every map g : B -> A gives exactly one retraction copair(id, g)), existence of a retraction by the emptiness
criterion (nonempty difference channel or empty structure channel), and the injection facts from explicit
tagged sets. AuthorityEffect: None.
"""
import sys
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-ROOT-DIFF-STRUCTURE'
KEYS = {
    'maps': {'kind', 'a', 'b', 'c', 'total_maps', 'left_maps', 'right_maps', 'product_matches', 'unique_copairs', 'inl_injective',
             'inr_injective', 'disjoint', 'covering'},
    'reduction': {'kind', 'a', 'b', 'maps_b_to_a', 'maps_a_to_b', 'retractions_to_pd', 'retractions_to_s', 'exists_to_pd', 'exists_to_s'},
    'posit': {'kind', 'a', 'b', 'nonempty_pd', 'nonempty_s', 'coproduct_size', 'nonempty_real0', 'real0_nonempty_iff_a_channel_is'},
}
BOOLS = {'product_matches', 'inl_injective', 'inr_injective', 'disjoint', 'covering', 'exists_to_pd', 'exists_to_s',
         'nonempty_pd', 'nonempty_s', 'nonempty_real0', 'real0_nonempty_iff_a_channel_is'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def maps_expected(a, b, c):
    """Enumerate every map coproduct -> C (dictionaries on tagged elements), group by the pair of restrictions, count copairs."""
    left = [('pd', i) for i in range(a)]
    right = [('st', j) for j in range(b)]
    everything = left + right
    total = 0
    groups = {}
    for values in product(range(c), repeat=len(everything)):
        h = dict(zip(everything, values))
        total += 1
        key = (tuple(h[x] for x in left), tuple(h[x] for x in right))
        groups[key] = groups.get(key, 0) + 1
    left_maps = sum(1 for _ in product(range(c), repeat=a))
    right_maps = sum(1 for _ in product(range(c), repeat=b))
    require(total == c ** (a + b) and len(groups) == left_maps * right_maps, 'G3_WITNESS:maps_out_closed_form')
    return {'kind': 'maps', 'a': a, 'b': b, 'c': c, 'total_maps': total, 'left_maps': left_maps, 'right_maps': right_maps,
            'product_matches': total == left_maps * right_maps, 'unique_copairs': sum(1 for v in groups.values() if v == 1),
            'inl_injective': len(set(left)) == a, 'inr_injective': len(set(right)) == b,
            'disjoint': set(left).isdisjoint(right), 'covering': len(set(left) | set(right)) == a + b}


def reduction_expected(a, b):
    return {'kind': 'reduction', 'a': a, 'b': b, 'maps_b_to_a': a ** b, 'maps_a_to_b': b ** a,
            'retractions_to_pd': a ** b, 'retractions_to_s': b ** a,
            'exists_to_pd': a > 0 or b == 0, 'exists_to_s': b > 0 or a == 0}


def posit_expected(a, b):
    return {'kind': 'posit', 'a': a, 'b': b, 'nonempty_pd': a > 0, 'nonempty_s': b > 0, 'coproduct_size': a + b,
            'nonempty_real0': a + b > 0, 'real0_nonempty_iff_a_channel_is': True}


_CACHE = {}


def expected(case):
    key = repr(case)
    if key not in _CACHE:
        kind = case[0]
        if kind == 'maps':
            _CACHE[key] = maps_expected(case[1], case[2], case[3])
        elif kind == 'reduction':
            _CACHE[key] = reduction_expected(case[1], case[2])
        elif kind == 'posit':
            _CACHE[key] = posit_expected(case[1], case[2])
        else:
            raise ValueError('G2_COVERAGE:unknown_case_kind')
    return _CACHE[key]


def key_of(r):
    return repr((r['kind'], r['a'], r['b'], r.get('c')))


def check_types(r):
    kind = r['kind']
    require(type(kind) is str and kind in KEYS and set(r) == KEYS[kind], 'G1_SCHEMA:record_keys')
    for k, v in r.items():
        if k == 'kind':
            continue
        if k in BOOLS:
            require(type(v) is bool, 'G1_SCHEMA:bool_field')
        else:
            require(type(v) is int, 'G1_SCHEMA:int_field')


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
            if r['kind'] == 'maps':
                require(r['product_matches'] and r['disjoint'] and r['covering'], 'G3_WITNESS:coproduct_property')
            if r['kind'] == 'reduction':
                # no reduction in general: an empty channel facing a nonempty one admits no retraction onto it
                if r['a'] == 0 and r['b'] > 0:
                    require(not r['exists_to_pd'], 'G3_WITNESS:no_reduction_into_empty_difference_channel')
                if r['b'] == 0 and r['a'] > 0:
                    require(not r['exists_to_s'], 'G3_WITNESS:no_reduction_into_empty_structure_channel')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ZeroDivisionError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
