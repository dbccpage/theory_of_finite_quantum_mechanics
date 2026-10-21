"""Independent checker for PG-OBLIGATION-MONOID.

Does not import the producer.  Differences in method:

* laws: counter vectors are packed into one integer in a positional base large enough to avoid carries, so vector
  addition is integer addition; failures are counted on the packed integers (producer: tuples of coordinates).
* bounded: per-coordinate counts raised to the k (a + b <= M has (M+1)(M+2)/2 solutions; definedness of each bracket and the
  mismatch count are recomputed from per-coordinate flags; the value mismatch is 0 because both brackets equal x+y+z when defined).
* saturating: clamp-form operator, cancellation failures closed form cap(cap+1)(cap+2)/3.
* events: str.count, a regular expression for "declared before an assertion", multinomial for distinct permutations.
* ledger: tracks generated and outstanding counts (producer: generated and discharged) with exact big integers; the
  discharged vector is recovered as generated minus outstanding.
AuthorityEffect: None.
"""
import re
import sys
from itertools import permutations, product
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-OBLIGATION-MONOID'
U64 = 18446744073709551615
KEYS = {
    'laws': ['elements', 'triples', 'assoc_failures', 'comm_failures', 'unit_failures', 'cancel_failures', 'invertible_nonzero'],
    'bounded': ['elements', 'pairs', 'defined_pairs', 'overflow_pairs', 'triples', 'defined_triples', 'definedness_mismatch', 'value_mismatch'],
    'saturating': ['elements', 'triples', 'assoc_failures', 'comm_failures', 'unit_failures', 'cancel_failures'],
    'events': ['terms', 'assertions', 'destructive', 'cost', 'length', 'valid_fresh', 'declare_then_assert', 'perm_count',
               'perm_trace_failures', 'split_failures'],
    'ledger': ['status', 'fail_index', 'generated', 'discharged', 'outstanding', 'settled'],
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def expected_laws(k, n):
    base = 4 * n + 1
    els = [sum(c * base ** j for j, c in enumerate(t)) for t in product(range(n), repeat=k)]
    assoc = comm = unit = cancel = 0
    for x in els:
        unit += (x + 0 != x) + (0 + x != x)
        for y in els:
            comm += (x + y != y + x)
            for z in els:
                assoc += ((x + y) + z != x + (y + z))
                cancel += (x + z == y + z and x != y)
    invertible = sum(1 for x in els if x != 0 and any(x + y == 0 for y in els))
    return dict(elements=n ** k, triples=n ** (3 * k), assoc_failures=assoc, comm_failures=comm, unit_failures=unit,
                cancel_failures=cancel, invertible_nonzero=invertible)


def expected_bounded(k, m):
    pairs_one = (m + 1) * (m + 2) // 2
    elements = (m + 1) ** k
    # per coordinate triple (a, b, c): the left bracket (a+b)+c is defined iff a+b <= m and a+b+c <= m, the right one iff
    # b+c <= m and a+b+c <= m; a vector triple is defined iff every coordinate is, so counts are powers of coordinate counts
    left = right = both = 0
    for a, b, c in product(range(m + 1), repeat=3):
        lf = a + b <= m and a + b + c <= m
        rf = b + c <= m and a + b + c <= m
        left += lf
        right += rf
        both += (lf and rf)
    mismatch = left ** k + right ** k - 2 * both ** k
    return dict(elements=elements, pairs=elements ** 2, defined_pairs=pairs_one ** k, overflow_pairs=elements ** 2 - pairs_one ** k,
                triples=elements ** 3, defined_triples=left ** k, definedness_mismatch=mismatch, value_mismatch=0)


def expected_saturating(cap):
    def op(a, b):
        return a + b if a + b < cap else cap
    assoc = comm = unit = 0
    for x in range(cap + 1):
        unit += (op(x, 0) != x) + (op(0, x) != x)
        for y in range(cap + 1):
            comm += op(x, y) != op(y, x)
            for z in range(cap + 1):
                assoc += op(op(x, y), z) != op(x, op(y, z))
    return dict(elements=cap + 1, triples=(cap + 1) ** 3, assoc_failures=assoc, comm_failures=comm, unit_failures=unit,
                cancel_failures=cap * (cap + 1) * (cap + 2) // 3)


def expected_events(arg):
    word = '' if arg == '-' else arg
    require(re.fullmatch(r'[DARI]*', word) is not None, 'G1_SCHEMA:event_word')
    t, a, d = word.count('D'), word.count('A'), word.count('R') + word.count('I')
    perm = factorial(len(word))
    for ch in 'DARI':
        perm //= factorial(word.count(ch))
    perm_fail = 0
    for p in set(permutations(word)):
        s = ''.join(p)
        perm_fail += (s.count('D'), s.count('A'), s.count('R') + s.count('I')) != (t, a, d)
    split_fail = 0
    for cut in range(len(word) + 1):
        u, v = word[:cut], word[cut:]
        split_fail += (u.count('D') + v.count('D'), u.count('A') + v.count('A'), u.count('R') + v.count('R') + u.count('I') + v.count('I')) != (t, a, d)
    return dict(terms=t, assertions=a, destructive=d, cost=len(word), length=len(word), valid_fresh=(t >= 1 and a >= 1),
                declare_then_assert=re.search('D.*A', word) is not None, perm_count=perm, perm_trace_failures=perm_fail,
                split_failures=split_fail)


def expected_ledger(arg):
    ops = []
    if arg != '-':
        for item in arg.split(','):
            m = re.fullmatch(r'([gd]):([ABC]):(0|[1-9][0-9]*)', item)
            require(m is not None, 'G1_SCHEMA:ledger_op')
            ops.append((m.group(1), 'ABC'.index(m.group(2)), int(m.group(3))))
    generated, outstanding = [0, 0, 0], [0, 0, 0]
    status, fail = 'ok', -1
    for index, (kind, i, count) in enumerate(ops):
        if kind == 'g':
            if generated[i] + count > U64:
                status, fail = 'CountOverflow', index
                break
            generated[i] += count
            outstanding[i] += count
        elif count > 0:
            if generated[i] == 0:
                status, fail = 'NeverGenerated', index
                break
            if count > outstanding[i]:
                status, fail = 'OverDischarge', index
                break
            outstanding[i] -= count
    return dict(status=status, fail_index=fail, generated=generated, discharged=[g - o for g, o in zip(generated, outstanding)],
                outstanding=outstanding, settled=(outstanding == [0, 0, 0]))


EXPECT = {'laws': expected_laws, 'bounded': expected_bounded, 'saturating': expected_saturating,
          'events': expected_events, 'ledger': expected_ledger}


_CACHE = {}


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
            require(type(r) is dict and r.get('kind') in EXPECT, 'G1_SCHEMA:kind')
            require(set(r) == {'kind', 'args'} | set(KEYS[r['kind']]), 'G1_SCHEMA:record_keys')
            require(type(r['args']) is list, 'G1_SCHEMA:args')
            seen.append([r['kind']] + r['args'])
            require(any(same(seen[-1], c) for c in cases), 'G2_COVERAGE:args_are_public_case')
            key = (r['kind'], tuple(r['args']))
            if key not in _CACHE:
                _CACHE[key] = EXPECT[r['kind']](*r['args'])
            want = _CACHE[key]
            for f in KEYS[r['kind']]:
                require(same(r[f], want[f]), 'G3_WITNESS:%s:%s' % (r['kind'], f))
            # theorem-level consistency of the candidate itself
            if r['kind'] == 'laws':
                require(r['assoc_failures'] == r['comm_failures'] == r['unit_failures'] == r['cancel_failures'] == 0, 'G3_WITNESS:monoid_laws_and_cancellation')
                require(r['invertible_nonzero'] == 0, 'G3_WITNESS:not_a_group')
            if r['kind'] == 'bounded':
                require(r['definedness_mismatch'] == 0 and r['value_mismatch'] == 0, 'G3_WITNESS:partial_associativity')
            if r['kind'] == 'saturating':
                require(r['cancel_failures'] > 0 and r['assoc_failures'] == 0, 'G3_WITNESS:saturating_not_cancellative')
            if r['kind'] == 'events':
                require(r['cost'] == r['length'] and r['perm_trace_failures'] == 0 and r['split_failures'] == 0, 'G3_WITNESS:trace_hom')
            if r['kind'] == 'ledger':
                require(all(g - d == o and d <= g for g, d, o in zip(r['generated'], r['discharged'], r['outstanding'])), 'G3_WITNESS:ledger_invariant')
        require(sorted(map(repr, seen)) == sorted(map(repr, cases)), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ValueError) as error:
        if isinstance(error, ValueError) and str(error).startswith('G'):
            raise
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
