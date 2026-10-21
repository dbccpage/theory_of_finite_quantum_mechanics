"""Independent checker for PG-HISTORY-REPORT-CRITERION.

Does not import the producer and does not enumerate functions. Counts are recomputed from closed forms.
factoring = sum_k R_k s^k with R_k = C(v,k) k! S2(h,k) the number of reports with image of size k (Stirling
numbers of the second kind by recurrence). fiber_constant is computed SEPARATELY, from the partitions of the
histories induced by a report (restricted growth strings): a report inducing a partition with k blocks is one of
v(v-1)...(v-k+1), and an answer constant on the blocks is one of s^k. mismatch = fiber_constant - factoring,
because every factoring pair is fiber constant (kernel theorem fiberConstant_of_factors), so no pair is
factoring-but-not-constant. Extensions of (report, question) to V -> S number v^h s^v in total; a factoring pair has
s^(v-k) extensions, so it is non-unique off the image exactly when s^(v-k) >= 2 (a surjective report has k = v and
so is never non-unique: computed, not assumed). The factor multiplicity 1 is the kernel theorem factor_unique_on_image.
AuthorityEffect: None.
"""
import sys
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-HISTORY-REPORT-CRITERION'
KEYS = {'input', 'pairs', 'fiber_constant', 'factoring', 'mismatch', 'image_hist', 'max_factor_multiplicity',
        'extensions_total', 'nonunique_off_image', 'surjective_reports', 'surjective_nonunique'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def stirling2(n, k):
    table = [[0] * (k + 1) for _ in range(n + 1)]
    table[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            table[i][j] = j * table[i - 1][j] + table[i - 1][j - 1]
    return table[n][k]


def partitions_by_blocks(h):
    """Number of set partitions of {0..h-1} with k blocks, by enumerating restricted growth strings."""
    counts = {}

    def extend(prefix, top):
        if len(prefix) == h:
            counts[top] = counts.get(top, 0) + 1
            return
        for value in range(top):
            extend(prefix + [value], top)
        extend(prefix + [top], top + 1)

    extend([], 0)
    return counts


def falling(v, k):
    out = 1
    for i in range(k):
        out *= v - i
    return out


def expected(h, v, s):
    reports_by_image = {k: comb(v, k) * factorial(k) * stirling2(h, k) for k in range(0, min(h, v) + 1)}
    reports_by_image = {k: c for k, c in reports_by_image.items() if c}
    factoring = sum(c * s ** k for k, c in reports_by_image.items())
    nonunique = sum(c * s ** k for k, c in reports_by_image.items() if s ** (v - k) >= 2)
    fiber_constant = sum(blocks_count * falling(v, k) * s ** k for k, blocks_count in partitions_by_blocks(h).items())
    return {'input': [h, v, s], 'pairs': v ** h * s ** h, 'fiber_constant': fiber_constant, 'factoring': factoring,
            'mismatch': fiber_constant - factoring,
            'image_hist': [[k, reports_by_image[k]] for k in sorted(reports_by_image)],
            'max_factor_multiplicity': 1 if factoring else 0, 'extensions_total': v ** h * s ** v,
            'nonunique_off_image': nonunique, 'surjective_reports': reports_by_image.get(v, 0),
            'surjective_nonunique': sum(c * s ** k for k, c in reports_by_image.items() if k == v and s ** (v - k) >= 2)}


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
            for key in KEYS - {'input', 'image_hist'}:
                require(is_int(r[key]), 'G1_SCHEMA:int_' + key)
            require(type(r['image_hist']) is list and all(type(p) is list and len(p) == 2 and all(is_int(x) for x in p)
                                                          for p in r['image_hist']), 'G1_SCHEMA:image_hist')
            seen.append(tuple(r['input']))
            want = expected(*r['input'])
            for key in sorted(KEYS):
                require(r[key] == want[key], 'G3_WITNESS:' + key)
            # The criterion as a theorem-level consistency of the record itself:
            require(r['fiber_constant'] == r['factoring'] and r['mismatch'] == 0, 'G3_WITNESS:factors_iff_fiber_constant')
            require(r['surjective_nonunique'] == 0, 'G3_WITNESS:surjective_extension_unique')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
