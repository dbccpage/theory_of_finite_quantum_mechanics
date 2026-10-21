"""Independent checker for PG-COLLAPSE-BARRIER.

Does not import the producer.  The producer enumerates every profile p and task s and every factor g (and every
tag t) by brute force.  This checker recomputes by closed forms and a different criterion:

* number of profiles with image size j  =  C(my, j) * Surj(n, j),  Surj by inclusion-exclusion;
* tasks constant on the fibres of p  =  mz ** |image p|   (the task is a free function on the image);
* tasks factoring through p  =  the same, but only when mz >= 1 or p is onto Y (the off-image points of Y need a value);
* triples (p, s, g) with g . p = s  =  my ** n * mz ** my  (every pair (p, g) fixes s);
* least added tag alphabet (size k >= 0)  =  0 for empty X, else max(1, largest number of distinct task values inside one
  fibre of p), found by enumerating (p, s) and grouping, never by enumerating tags.
AuthorityEffect: None.
"""
import sys
from itertools import product
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-COLLAPSE-BARRIER'
KEYS = {'input', 'total', 'fibre_constant', 'collapsed_separated', 'factoring', 'factorizations', 'violations', 'min_tag_hist'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def surjections(n, j):
    return sum((-1) ** i * comb(j, i) * (j - i) ** n for i in range(j + 1))


def expected(n, my, mz):
    total = my ** n * mz ** n
    fc = fac = 0
    for j in range(0, min(n, my) + 1):
        profiles = comb(my, j) * surjections(n, j)
        fc += profiles * mz ** j
        if mz >= 1 or j == my:
            fac += profiles * mz ** j
    hist = {}
    for p in product(range(my), repeat=n):
        for s in product(range(mz), repeat=n):
            fibres = {}
            for a, b in zip(p, s):
                fibres.setdefault(a, set()).add(b)
            # alphabet size 0 works exactly for empty X; otherwise the largest number of distinct task values in one fibre (at least 1)
            k = 0 if n == 0 else max([1] + [len(v) for v in fibres.values()])
            hist[k] = hist.get(k, 0) + 1
    return {'input': [n, my, mz], 'total': total, 'fibre_constant': fc, 'collapsed_separated': total - fc,
            'factoring': fac, 'factorizations': my ** n * mz ** my, 'violations': 0,
            'min_tag_hist': [[k, hist[k]] for k in sorted(hist)]}


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
            require(type(r) is dict and set(r) == KEYS, 'G1_SCHEMA:record_keys')
            inp = r['input']
            require(type(inp) is list and len(inp) == 3 and all(is_int(x) and x >= 0 for x in inp), 'G1_SCHEMA:input')
            seen.append(tuple(inp))
            for key in KEYS - {'input', 'min_tag_hist'}:
                require(is_int(r[key]), 'G1_SCHEMA:' + key)
            hist = r['min_tag_hist']
            require(type(hist) is list and all(type(e) is list and len(e) == 2 and all(is_int(x) for x in e) for e in hist),
                    'G1_SCHEMA:min_tag_hist')
            want = expected(*inp)
            for key in sorted(KEYS):
                require(r[key] == want[key], 'G3_WITNESS:' + key)
            # Theorem-level consistency of the candidate itself: the barrier has no exceptions, and the pairs
            # that do not factor are exactly the ones whose least tag alphabet exceeds the empty tag.
            require(r['violations'] == 0, 'G3_WITNESS:barrier_has_no_exceptions')
            require(r['fibre_constant'] + r['collapsed_separated'] == r['total'], 'G3_WITNESS:partition')
            require(r['factoring'] <= r['fibre_constant'], 'G3_WITNESS:factoring_implies_fibre_constant')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
