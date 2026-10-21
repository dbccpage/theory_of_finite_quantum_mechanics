"""Independent checker for PG-PREGEN-CONSTRUCTIVE-SUMMARY.

Does not import the producer. First-match reconstruction depends only on the order of first occurrences in a
listing, so the checker enumerates the injective sequences of first occurrences (permutations of subsets of the
population) and weights each by the number of listings of length <= ell that reduce to it, sum_k S2(k,t) with S2
the Stirling numbers of the second kind. Reconstruction uses a first-occurrence table per report; listed fiber
constancy uses pairwise equality on the listed set. Totals are cross-checked against sum_{k<=ell} p^k.
AuthorityEffect: None.
"""
import sys
from itertools import permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-PREGEN-CONSTRUCTIVE-SUMMARY'
COUNT_KEYS = ['lists', 'triples', 'listed_fc', 'recon_correct', 'mismatch', 'complete_triples', 'complete_mismatch',
              'partial_false_positive', 'unlisted_refused', 'unlisted_correct', 'unlisted_wrong']
KEYS = {'input'} | set(COUNT_KEYS)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def stirling2_table(n):
    table = [[0] * (n + 2) for _ in range(n + 1)]
    table[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            table[i][j] = j * table[i - 1][j] + table[i - 1][j - 1]
    return table


def expected(p, ell, v, s):
    table = stirling2_table(ell)
    out = {k: 0 for k in COUNT_KEYS}
    reports = list(product(range(v), repeat=p))
    answers = list(product(range(s), repeat=p))
    for t in range(0, min(ell, p) + 1):
        weight = sum(table[k][t] for k in range(ell + 1))
        for seq in permutations(range(p), t):
            listed = set(seq)
            complete = len(listed) == p
            unlisted = [h for h in range(p) if h not in listed]
            out['lists'] += weight
            for rep in reports:
                first = {}
                for h in seq:
                    first.setdefault(rep[h], h)
                for ans in answers:
                    out['triples'] += weight
                    pair_ok = all(ans[a] == ans[b] for a in listed for b in listed if rep[a] == rep[b])
                    recon_ok = all(ans[first[rep[h]]] == ans[h] for h in seq)
                    global_ok = all(ans[a] == ans[b] for a in range(p) for b in range(p) if rep[a] == rep[b])
                    out['listed_fc'] += weight * pair_ok
                    out['recon_correct'] += weight * recon_ok
                    out['mismatch'] += weight * (pair_ok != recon_ok)
                    if complete:
                        out['complete_triples'] += weight
                        out['complete_mismatch'] += weight * (pair_ok != global_ok)
                    elif pair_ok and not global_ok:
                        out['partial_false_positive'] += weight
                    if pair_ok:
                        for h in unlisted:
                            if rep[h] not in first:
                                out['unlisted_refused'] += weight
                            elif ans[first[rep[h]]] == ans[h]:
                                out['unlisted_correct'] += weight
                            else:
                                out['unlisted_wrong'] += weight
    require(out['lists'] == sum(p ** k for k in range(ell + 1)), 'G3_WITNESS:listing_weights')
    require(out['triples'] == out['lists'] * v ** p * s ** p, 'G3_WITNESS:triple_total')
    out['input'] = [p, ell, v, s]
    return out


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
            require(type(r['input']) is list and len(r['input']) == 4 and all(is_int(x) and x >= 0 for x in r['input']), 'G1_SCHEMA:input')
            for key in COUNT_KEYS:
                require(is_int(r[key]), 'G1_SCHEMA:int_' + key)
            seen.append(tuple(r['input']))
            want = expected(*r['input'])
            for key in COUNT_KEYS:
                require(r[key] == want[key], 'G3_WITNESS:' + key)
            # Theorem-level consistency of the record itself: the listed criterion is an equivalence.
            require(r['mismatch'] == 0 and r['listed_fc'] == r['recon_correct'], 'G3_WITNESS:recon_correct_iff_listed_fiber_constant')
            require(r['complete_mismatch'] == 0, 'G3_WITNESS:complete_listing_agrees_with_global_criterion')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
