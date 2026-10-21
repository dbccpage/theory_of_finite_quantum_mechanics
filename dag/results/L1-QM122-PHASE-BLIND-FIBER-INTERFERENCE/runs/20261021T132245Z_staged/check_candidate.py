"""Independent checker for L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE.

Recomputes every record from the public weight pairs without importing the producer: fibers by brute force over
the integer box, the readout by the closed form (W + 2c, W - 2c) with c = Re(a conj b), and the descent flag from
the number of distinct readouts. AuthorityEffect: None.
"""
import sys
from math import isqrt
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'dag/pfp/prepare_stage.py').is_file())
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE'
KEYS = {'input', 'fiber_sizes', 'realizable', 'readouts', 'distinct_readouts', 'total_doubled', 'descends'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def box_fiber(w):
    r = isqrt(w) + 1
    return [(x, y) for x in range(-r, r + 1) for y in range(-r, r + 1) if x * x + y * y == w]


def expected(w0, w1):
    f0, f1 = box_fiber(w0), box_fiber(w1)
    W = w0 + w1
    reads = sorted({(W + 2 * (a[0] * b[0] + a[1] * b[1]), W - 2 * (a[0] * b[0] + a[1] * b[1])) for a in f0 for b in f1})
    return {'input': [w0, w1], 'fiber_sizes': [len(f0), len(f1)], 'realizable': bool(f0 and f1),
            'readouts': [list(r) for r in reads], 'distinct_readouts': len(reads),
            'total_doubled': all(r[0] + r[1] == 2 * W for r in reads), 'descends': len(reads) <= 1}


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
            require(type(r['input']) is list and len(r['input']) == 2 and all(is_int(x) for x in r['input']), 'G1_SCHEMA:input')
            seen.append(tuple(r['input']))
            want = expected(*r['input'])
            require(type(r['fiber_sizes']) is list and all(is_int(x) for x in r['fiber_sizes']), 'G1_SCHEMA:fiber_sizes')
            require(type(r['readouts']) is list and all(type(v) is list and all(is_int(x) for x in v) for v in r['readouts']), 'G1_SCHEMA:readouts')
            require(is_int(r['distinct_readouts']) and type(r['realizable']) is bool and type(r['total_doubled']) is bool
                    and type(r['descends']) is bool, 'G1_SCHEMA:types')
            require(r['fiber_sizes'] == want['fiber_sizes'], 'G3_WITNESS:fiber_sizes')
            require(r['realizable'] == want['realizable'], 'G3_WITNESS:realizable')
            require(r['readouts'] == want['readouts'], 'G3_WITNESS:readouts')
            require(r['distinct_readouts'] == want['distinct_readouts'], 'G3_WITNESS:distinct_readouts')
            require(r['total_doubled'] == want['total_doubled'], 'G3_WITNESS:total_doubled')
            require(r['descends'] == want['descends'], 'G3_WITNESS:descends')
            # Theorem-level consistency of the candidate itself (not only of the recomputation):
            if r['input'][0] > 0 and r['input'][1] > 0 and r['realizable']:
                require(not r['descends'], 'G3_WITNESS:nonzero_sectors_must_not_descend')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
