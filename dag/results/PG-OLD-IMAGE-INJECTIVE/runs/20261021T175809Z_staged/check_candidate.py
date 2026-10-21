"""Independent checker for PG-OLD-IMAGE-INJECTIVE.

Recomputes every count from closed forms, without enumerating any function and without importing the producer.
Given |A| = a, |B| = b, |O| = o: an old-image law forces u injective, so the number of law pairs is the number of
injective lifts b!/(b-a)! (zero when a > b) times the free values (a+1)^(b-a) of the recovery at the off-image points;
exactly one of those recoveries per lift refuses every off-image point; over law pairs the observation pairs preserved
are determined by q' (o^b of the o^a * o^b pairs); and the number of obstruction pairs (oA, oB) in which no old
obstruction persists is 3^a * 2^(b-a) (an independent choice per source point), of which 2^b have an empty oA.
AuthorityEffect: None.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-OLD-IMAGE-INJECTIVE'
FIELDS = ['pairs_total', 'law', 'law_noninjective', 'law_refusing', 'law_nonrefusing', 'injective_u',
          'obs_total', 'obs_preserved', 'persists', 'cleared']
KEYS = {'input'} | set(FIELDS)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def expected(a, b, o):
    inj = 0
    if a <= b:
        inj = 1
        for k in range(a):
            inj *= b - k
    law = inj * (a + 1) ** (b - a) if a <= b else 0
    refusing = inj
    return {'input': [a, b, o], 'pairs_total': b ** a * (a + 1) ** b, 'law': law, 'law_noninjective': 0,
            'law_refusing': refusing, 'law_nonrefusing': law - refusing, 'injective_u': inj,
            'obs_total': law * o ** a * o ** b, 'obs_preserved': law * o ** b,
            'persists': law * 2 ** (b - a) * (4 ** a - 3 ** a) if a <= b else 0,
            'cleared': law * (3 ** a * 2 ** (b - a) - 2 ** b) if a <= b else 0}


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = [list(c) for c in public['cases']]
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        seen = []
        for r in records:
            require(type(r) is dict and set(r) == KEYS, 'G1_SCHEMA:record_keys')
            require(type(r['input']) is list and len(r['input']) == 3 and all(is_int(x) and x >= 0 for x in r['input']), 'G1_SCHEMA:input')
            require(all(is_int(r[f]) for f in FIELDS), 'G1_SCHEMA:fields')
            seen.append(list(r['input']))
            want = expected(*r['input'])
            for f in FIELDS:
                require(r[f] == want[f], 'G3_WITNESS:' + f)
            # theorem-level consistency of the candidate itself
            require(r['law_noninjective'] == 0, 'G3_WITNESS:law_implies_injective')
            require(r['law_refusing'] + r['law_nonrefusing'] == r['law'], 'G3_WITNESS:refusing_partition')
            if r['input'][0] > r['input'][1]:
                require(r['law'] == 0, 'G3_WITNESS:no_recovery_when_source_larger')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
