"""Independent checker for PG-FREE-MONOID-NONISO.

Does not import the producer. Word counts are n^k; atoms are the nonempty words of length <= 4 that are NOT in the
set of products u+v of two nonempty words (a complement test, not the producer's split test); the number of
homomorphisms is (sum_{k<=d} m^k)^n; the number onto the letters is recomputed by inclusion-exclusion over
missing letters; injectivity and the bijective candidates are recomputed with string-valued homomorphisms; the
discrete-category equivalences are counted as the bijective maps Fin n -> Fin m (the inverse is then forced); the
set bijection uses explicit shortlex lists built by enumeration and a dictionary, not rank arithmetic. The record is
also required to satisfy the node's statement on the bounded range: bijective candidates are exactly the letter
permutations, so there are n! of them if n = m and none otherwise. AuthorityEffect: None.
"""
import sys
from functools import lru_cache
from itertools import product
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-FREE-MONOID-NONISO'
LIST_KEYS = ['words_n', 'words_m']
INT_KEYS = ['atoms_n', 'atoms_m', 'homs', 'letters_onto', 'injective_bounded', 'bijective_candidates', 'bijective_not_permutation',
            'permutation_homs', 'discrete_equivalences', 'set_bijection', 'homomorphism_violations']
KEYS = {'input'} | set(LIST_KEYS) | set(INT_KEYS)
MAX_LEN = 4
PREFIX = 30


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def strings(base, max_len):
    alphabet = ''.join(chr(ord('a') + i) for i in range(base))
    return [''.join(t) for k in range(max_len + 1) for t in product(alphabet, repeat=k)]


def atom_count(base):
    words = strings(base, MAX_LEN)
    products = {u + v for u in words if u for v in words if v and len(u + v) <= MAX_LEN}
    return sum(1 for w in words if w and w not in products)


def shortlex(base, count):
    out, k = [], 0
    while len(out) < count:
        level = list(product(range(base), repeat=k))
        out += level
        k += 1
        if base == 0:
            break
    return out[:count]


def set_side(n, m):
    first_n, first_m = shortlex(n, PREFIX), shortlex(m, PREFIX)
    if len(first_n) != len(first_m):
        return 0, 0
    phi = dict(zip(first_n, first_m))
    flag = int(len(set(phi.values())) == len(first_m))
    if n == 0 or m == 0:
        return flag, 0
    longest = max(len(w) for w in first_n)
    everything = [w for k in range(2 * longest + 1) for w in product(range(n), repeat=k)]
    index = {w: i for i, w in enumerate(everything)}
    target = shortlex(m, max(index[u + v] for u in first_n for v in first_n) + 1)
    return flag, sum(1 for u in first_n for v in first_n if target[index[u + v]] != phi[u] + phi[v])


@lru_cache(maxsize=None)
def expected(n, m, d):
    pool = strings(m, d)
    probe = strings(n, 2)
    width = len(pool)
    letters = strings(m, 1)[1:]
    onto = sum((-1) ** j * comb(m, j) * (width - j) ** n for j in range(m + 1))
    inj = cand = not_perm = 0
    for images in product(pool, repeat=n):
        table = dict(zip(strings(n, 1)[1:], images))
        values = [''.join(table[c] for c in w) for w in probe]
        is_inj = len(set(values)) == len(probe)
        inj += is_inj
        if is_inj and all(l in values for l in letters):
            cand += 1
            not_perm += not (all(len(g) == 1 for g in images) and len(set(images)) == n and n == m)
    bijections = sum(1 for f in product(range(m), repeat=n) if len(set(f)) == n == m)
    flag, violations = set_side(n, m)
    return {'input': [n, m, d], 'words_n': [n ** k for k in range(MAX_LEN + 1)], 'words_m': [m ** k for k in range(MAX_LEN + 1)],
            'atoms_n': atom_count(n), 'atoms_m': atom_count(m), 'homs': width ** n, 'letters_onto': onto, 'injective_bounded': inj,
            'bijective_candidates': cand, 'bijective_not_permutation': not_perm, 'permutation_homs': factorial(n) if n == m else 0,
            'discrete_equivalences': bijections, 'set_bijection': flag, 'homomorphism_violations': violations}


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
            require(type(r['input']) is list and len(r['input']) == 3 and all(is_int(x) and x >= 0 for x in r['input']), 'G1_SCHEMA:input')
            for key in INT_KEYS:
                require(is_int(r[key]), 'G1_SCHEMA:int_' + key)
            for key in LIST_KEYS:
                require(type(r[key]) is list and all(is_int(x) for x in r[key]), 'G1_SCHEMA:list_' + key)
            n, m, d = r['input']
            require(d <= 2, 'G1_SCHEMA:image_length_bound')
            seen.append((n, m, d))
            want = expected(n, m, d)
            for key in sorted(KEYS):
                require(r[key] == want[key], 'G3_WITNESS:' + key)
            # The node's claim on the bounded range, as consistency of the record itself:
            require(r['bijective_not_permutation'] == 0, 'G3_WITNESS:bijective_candidates_are_permutations')
            require(r['bijective_candidates'] == r['permutation_homs'], 'G3_WITNESS:candidates_equal_permutations')
            require(r['discrete_equivalences'] == r['permutation_homs'], 'G3_WITNESS:discrete_equivalences_equal_bijections')
            if n != m:
                require(r['bijective_candidates'] == 0 and r['discrete_equivalences'] == 0, 'G3_WITNESS:unequal_sizes_have_no_isomorphism')
            if n == 0 or m == 0:
                require(r['set_bijection'] == int(n == m) and r['homomorphism_violations'] == 0, 'G3_WITNESS:empty_alphabet_set_bijection_only_with_itself')
            if n >= 1 and m >= 1:
                require(r['set_bijection'] == 1, 'G3_WITNESS:set_bijection_exists_for_nonempty_alphabets')
                require((r['homomorphism_violations'] == 0) == (n == m), 'G3_WITNESS:shortlex_bijection_multiplicative_only_for_equal_sizes')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
