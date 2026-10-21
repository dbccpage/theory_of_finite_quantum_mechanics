"""Independent checker for PG-WDP-PROTECTED-QUESTIONS.

Recomputes every record from the public carrier sizes n without importing the producer: for each subset S of
{0..n-1} it enumerates ALL n! permutations, keeps those fixing S pointwise, intersects their fixed-point sets
(the invariant points), and decides minimality from the definition over all proper subsets. The producer uses the
closed form (S, plus the complement when it is a single point). Every leaf is compared with strict type equality.
AuthorityEffect: None.
"""
import itertools
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-WDP-PROTECTED-QUESTIONS'
KEYS = {'n', 'selecting_count', 'frontier', 'frontier_size', 'min_price', 'table'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_eq(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, list):
        return len(a) == len(b) and all(strict_eq(x, y) for x, y in zip(a, b))
    return a == b


def expected(n):
    perms = list(itertools.permutations(range(n)))
    size = 1 << n
    inv = {}
    for mask in range(size):
        stab = [p for p in perms if all(p[i] == i for i in range(n) if (mask >> i) & 1)]
        inv[mask] = sum(1 << x for x in range(n) if all(p[x] == x for p in stab))
    sel = {mask: inv[mask] != 0 for mask in inv}
    table = []
    for mask in range(size):
        proper = [s for s in range(size) if s != mask and (s & mask) == s]
        minimal = sel[mask] and not any(sel[s] for s in proper)
        table.append([mask, inv[mask], sel[mask], minimal])
    chosen = [t[0] for t in table if t[2]]
    prices = [bin(t).count('1') for t in chosen]
    frontier = [t[0] for t in table if t[3]]
    return {'n': n, 'selecting_count': len(chosen), 'frontier': frontier, 'frontier_size': len(frontier),
            'min_price': min(prices) if prices else None, 'table': table}


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = public['cases']
        require(type(cases) is list and all(type(c) is int and 0 <= c <= 6 for c in cases), 'G1_SCHEMA:public_cases')
        require(cases == [0, 1, 2, 3, 4, 5, 6], 'G2_COVERAGE:public_cases_are_carrier_sizes_0_to_6')
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        seen = []
        for r in records:
            require(type(r) is dict and set(r) == KEYS, 'G1_SCHEMA:record_keys')
            require(type(r['n']) is int, 'G1_SCHEMA:n')
            seen.append(r['n'])
            want = expected(r['n'])
            require(strict_eq(r['table'], want['table']), 'G3_WITNESS:table')
            require(strict_eq(r['selecting_count'], want['selecting_count']), 'G3_WITNESS:selecting_count')
            require(strict_eq(r['frontier'], want['frontier']), 'G3_WITNESS:frontier')
            require(strict_eq(r['frontier_size'], want['frontier_size']), 'G3_WITNESS:frontier_size')
            require(strict_eq(r['min_price'], want['min_price']), 'G3_WITNESS:min_price')
            # Theorem-level consistency of the candidate itself, beyond recomputation:
            if r['n'] >= 2:
                require(r['table'][0][2] is False, 'G3_WITNESS:empty_declaration_must_not_select')
                require(r['frontier'] == [1 << i for i in range(r['n'])], 'G3_WITNESS:frontier_is_singletons')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))
