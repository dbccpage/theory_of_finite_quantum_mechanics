"""Independent checker for PG-ADMISSION-FLOOR.

Does not import the producer.  The producer enumerates every relation bitmask, marked pair, map q and target T.
This checker uses closed forms only:

* classify: 2^(n^2) relations; 2^(n^2-n) irreflexive (law-bearing) ones; cut data = irreflexive and nonempty;
  exhibited cuts (R, a, b) = n(n-1) 2^(n^2-n-1); the four (related?, equal?) quadrants of (R, a, b) have
  n 2^(n^2-1) or n(n-1) 2^(n^2-1) members; a related pair under an irreflexive R is never equal.
* identify: for a map q the irreflexive relations R that q can carry into some irreflexive target are exactly the
  subsets of the separated pairs {(x, y) : q x != q y}, so their number is 2^(separated); fibre sizes of q give the
  count of separated pairs as n^2 - sum f^2.
AuthorityEffect: None.
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

TASK = 'PG-ADMISSION-FLOOR'
CLASSIFY_KEYS = {'kind', 'n', 'relations', 'law_bearing', 'cut_relations', 'cut_triples', 'instance_without_law', 'law_without_instance',
                 'related_equal', 'related_distinct', 'unrelated_equal', 'unrelated_distinct', 'irreflexive_related_equal'}
IDENTIFY_KEYS = {'kind', 'n', 'rq_pairs', 'rq_with_target', 'rq_identifying', 'rq_overlap', 'cut_q', 'cut_q_with_target',
                 'cut_q_identified', 'cut_q_identified_with_target'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def expected_classify(n):
    sq = n * n
    law = 2 ** (sq - n)
    half = n * 2 ** (sq - 1) if n else 0
    return {'kind': 'classify', 'n': n, 'relations': 2 ** sq, 'law_bearing': law, 'cut_relations': law - 1,
            'cut_triples': n * (n - 1) * 2 ** (sq - n - 1) if n >= 2 else 0,
            'instance_without_law': 2 ** sq - law, 'law_without_instance': 1,
            'related_equal': half, 'related_distinct': (n - 1) * half if n else 0,
            'unrelated_equal': half, 'unrelated_distinct': (n - 1) * half if n else 0, 'irreflexive_related_equal': 0}


def expected_identify(n):
    sq = n * n
    with_target = cut_with_target = cut_ident = 0
    for q in product(range(n), repeat=n):
        same = sum(c * c for c in Counter(q).values())
        sep = sq - same
        with_target += 2 ** sep
        if sep:
            cut_with_target += sep * 2 ** (sep - 1)
        if n >= 2:
            cut_ident += (same - n) * 2 ** (sq - n - 1)
    rq = 2 ** (sq - n) * n ** n
    return {'kind': 'identify', 'n': n, 'rq_pairs': rq, 'rq_with_target': with_target, 'rq_identifying': rq - with_target,
            'rq_overlap': 0, 'cut_q': n * (n - 1) * 2 ** (sq - n - 1) * n ** n if n >= 2 else 0,
            'cut_q_with_target': cut_with_target, 'cut_q_identified': cut_ident, 'cut_q_identified_with_target': 0}


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = [tuple(c) for c in public['cases']]
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        seen = []
        for r in records:
            require(type(r) is dict and r.get('kind') in ('classify', 'identify'), 'G1_SCHEMA:kind')
            keys = CLASSIFY_KEYS if r['kind'] == 'classify' else IDENTIFY_KEYS
            require(set(r) == keys, 'G1_SCHEMA:record_keys')
            require(all(is_int(r[k]) for k in keys - {'kind'}), 'G1_SCHEMA:ints')
            require(0 <= r['n'] <= 6, 'G1_SCHEMA:n')
            seen.append((r['kind'], r['n']))
            want = expected_classify(r['n']) if r['kind'] == 'classify' else expected_identify(r['n'])
            for k in sorted(keys):
                require(r[k] == want[k], 'G3_WITNESS:' + k)
            # theorem-level consistency of the candidate itself
            if r['kind'] == 'classify':
                require(r['irreflexive_related_equal'] == 0, 'G3_WITNESS:apartness')
                if r['n'] <= 1:
                    require(r['cut_relations'] == 0 and r['cut_triples'] == 0, 'G3_WITNESS:no_cut_on_subsingleton')
                require(r['law_without_instance'] == 1, 'G3_WITNESS:law_without_instance')
            else:
                require(r['rq_overlap'] == 0 and r['cut_q_identified_with_target'] == 0, 'G3_WITNESS:identification_breaks_law')
                require(r['rq_with_target'] + r['rq_identifying'] == r['rq_pairs'], 'G3_WITNESS:complementarity')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
