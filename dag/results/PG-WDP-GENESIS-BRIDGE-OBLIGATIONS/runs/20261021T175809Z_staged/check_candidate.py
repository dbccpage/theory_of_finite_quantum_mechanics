"""Independent checker for PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.

Recomputes every ledger record from the public status codes without importing the producer: counts by filtering,
the programme-order test as a pairwise implication over all position pairs, and the upgrade counts by SIMULATING every
strict single-position update and testing the end-to-end predicate on the updated vector (the producer uses closed
forms). Every leaf is compared with strict type equality. The end-to-end predicate is the definitional conjunction
'all five discharged' (a modelling choice). AuthorityEffect: None.
"""
import sys
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-WDP-GENESIS-BRIDGE-OBLIGATIONS'
KEYS = {'v', 'n_open', 'n_control', 'n_discharged', 'end_to_end', 'controls_run', 'prefix_order', 'upgrades',
        'completing_upgrades', 'node_reading'}
N = 5


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_eq(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, list):
        return len(a) == len(b) and all(strict_eq(x, y) for x, y in zip(a, b))
    return a == b


def end_to_end(v):
    return all(s == 2 for s in v)


def expected(code):
    v = [int(c) for c in code]
    upgrades = completing = 0
    for k in range(N):
        for s in (1, 2):
            if s > v[k]:
                w = v[:k] + [s] + v[k + 1:]
                upgrades += 1
                completing += end_to_end(w)
    prefix = all(v[j] == 2 for j in range(N) for k in range(j, N) if v[k] == 2)
    return {'v': v, 'n_open': sum(1 for s in v if s == 0), 'n_control': sum(1 for s in v if s == 1),
            'n_discharged': sum(1 for s in v if s == 2), 'end_to_end': end_to_end(v), 'controls_run': min(v) >= 1,
            'prefix_order': prefix, 'upgrades': upgrades, 'completing_upgrades': completing, 'node_reading': v == [1, 1, 1, 1, 1]}


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = public['cases']
        require(type(cases) is list and all(type(c) is str and len(c) == N and set(c) <= set('012') for c in cases), 'G1_SCHEMA:public_cases')
        require(cases == [''.join(str(d) for d in v) for v in product(range(3), repeat=N)], 'G2_COVERAGE:public_cases_are_all_243_status_vectors')
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        seen = []
        for r in records:
            require(type(r) is dict and set(r) == KEYS, 'G1_SCHEMA:record_keys')
            require(type(r['v']) is list and len(r['v']) == N and all(type(s) is int and 0 <= s <= 2 for s in r['v']), 'G1_SCHEMA:v')
            code = ''.join(str(s) for s in r['v'])
            seen.append(code)
            want = expected(code)
            for key in sorted(KEYS):
                require(strict_eq(r[key], want[key]), 'G3_WITNESS:' + key)
            # Theorem-level consistency of the candidate itself:
            if r['end_to_end']:
                require(r['v'] == [2] * N and r['upgrades'] == 0, 'G3_WITNESS:end_to_end_only_all_discharged')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        require(len(set(seen)) == len(seen), 'G2_COVERAGE:duplicate_vectors')
        require(sum(1 for r in records if r['end_to_end']) == 1, 'G3_WITNESS:exactly_one_vector_is_end_to_end')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))
