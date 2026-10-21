"""Independent checker for L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.

Recomputes every record without importing the producer and without the closed forms |S|, the composition count or the
mass-face description: the class of c is enumerated as c - d0 h over a gauge-fixed integer box of potentials h (h_0 = 0),
and the minimum of the (weighted) L1 form, the full set of minimizing residuals, their lexicographic extremes, the
sector-weight tuples and the extremes of the sum of squares are read off that enumeration. Box bound, unweighted: a
minimizer r has L1(r) <= L1(c), so |r_j| <= sum|c| and |h_i| <= 2 sum|c|; weighted with masses m: sum m|r| <= sum m|c|
gives sum|r_j| <= (sum m|c|)/m_min =: B and |h_i| <= sum|c| + B. The two-cycle records enumerate each cycle
separately. Gamma2 is MODELLED as the holonomy (class invariant); the sum-of-squares reading is recorded, not assumed.
AuthorityEffect: None.
"""
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'dag/pfp/prepare_stage.py').is_file())
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED'
KEYS = {
    'residual': {'kind', 'input', 'holonomy', 'phi1', 'minimizer_count', 'lex_min', 'lex_max', 'sector_vectors', 'determined', 'unique',
                 'symmetric', 'symmetric_integral', 'sumsq_min', 'sumsq_max', 'status'},
    'weighted': {'kind', 'input', 'holonomy', 'weighted_phi1', 'minimizer_count', 'lex_min', 'lex_max', 'sector_vectors', 'determined',
                 'unique', 'status'},
    'twocycle': {'kind', 'input', 'holonomies', 'phi1', 'minimizer_count', 'total_holonomy', 'total_gives_phi1'}}
_CACHE = {}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def int_list(x, size=None, positive=False):
    return (type(x) is list and all(is_int(v) and (v >= 1 or not positive) for v in x) and (size is None or len(x) == size))


def enumerate_class(n, c, masses):
    """Brute force over the class {c - d0 h}: (min weighted L1, sorted minimizing residuals, holonomies seen, sums of squares)."""
    key = (n, tuple(c), tuple(masses))
    if key in _CACHE:
        return _CACHE[key]
    mmin = min(masses)
    bc = sum(m * abs(v) for m, v in zip(masses, c)) // mmin
    box = sum(abs(v) for v in c) + bc  # sum|r_j| <= (sum m|r|)/m_min <= bc, so |h_i| <= sum|c| + bc
    best, mins, hols = None, [], set()
    for tail in product(range(-box, box + 1), repeat=n - 1):
        h = (0,) + tail
        r = tuple(c[i] - (h[(i + 1) % n] - h[i]) for i in range(n))
        norm = sum(m * abs(v) for m, v in zip(masses, r))
        if best is None or norm < best:
            best, mins = norm, [r]
        elif norm == best:
            mins.append(r)
        hols.add(sum(r))
    mins = sorted(set(mins))
    _CACHE[key] = (best, mins, hols)
    return _CACHE[key]


def sector_tuples(mins, sizes):
    cuts, acc = [], 0
    for s in sizes:
        cuts.append((acc, acc + s))
        acc += s
    return sorted({tuple(sum(abs(r[i]) for i in range(a, b)) for a, b in cuts) for r in mins})


def expected_residual(n, c, sizes):
    ones = tuple([1] * n)
    best, mins, hols = enumerate_class(n, c, ones)
    vecs = sector_tuples(mins, sizes)
    S = sum(c)
    sym = Fraction(best, n)
    require(hols == {S}, 'G3_WITNESS:holonomy_is_not_a_class_invariant')
    sign = 1 if S > 0 else -1 if S < 0 else 0
    require(all(sign * v >= 0 for r in mins for v in r), 'G3_WITNESS:minimizer_sign')
    require(n * sym == best, 'G3_WITNESS:symmetric_point_mass')
    squares = [sum(v * v for v in r) for r in mins]
    return {'holonomy': S, 'phi1': best, 'minimizer_count': len(mins), 'lex_min': list(mins[0]), 'lex_max': list(mins[-1]),
            'sector_vectors': [list(v) for v in vecs], 'determined': len(vecs) == 1, 'unique': len(mins) == 1,
            'symmetric': [sym.numerator, sym.denominator], 'symmetric_integral': sym.denominator == 1,
            'sumsq_min': min(squares), 'sumsq_max': max(squares), 'status': 'zero_mass_refused' if best == 0 else 'ok'}


def expected_weighted(n, c, sizes, masses):
    best, mins, hols = enumerate_class(n, c, tuple(masses))
    vecs = sector_tuples(mins, sizes)
    S = sum(c)
    mmin = min(masses)
    require(hols == {S}, 'G3_WITNESS:holonomy_is_not_a_class_invariant')
    sign = 1 if S > 0 else -1 if S < 0 else 0
    require(all(sign * v >= 0 for r in mins for v in r), 'G3_WITNESS:minimizer_sign')
    require(all(masses[i] == mmin or r[i] == 0 for r in mins for i in range(n)), 'G3_WITNESS:minimizers_live_on_minimal_mass_edges')
    require(best == abs(S) * mmin, 'G3_WITNESS:weighted_minimum')
    return {'holonomy': S, 'weighted_phi1': best, 'minimizer_count': len(mins), 'lex_min': list(mins[0]), 'lex_max': list(mins[-1]),
            'sector_vectors': [list(v) for v in vecs], 'determined': len(vecs) == 1, 'unique': len(mins) == 1,
            'status': 'zero_mass_refused' if best == 0 else 'ok'}


def expected_twocycle(n1, c1, n2, c2):
    b1, m1, h1 = enumerate_class(n1, c1, tuple([1] * n1))
    b2, m2, h2 = enumerate_class(n2, c2, tuple([1] * n2))
    require(h1 == {sum(c1)} and h2 == {sum(c2)}, 'G3_WITNESS:holonomy_is_not_a_class_invariant')
    total = sum(c1) + sum(c2)
    return {'holonomies': [sum(c1), sum(c2)], 'phi1': b1 + b2, 'minimizer_count': len(m1) * len(m2), 'total_holonomy': total,
            'total_gives_phi1': abs(total) == b1 + b2}


def expected(inp):
    kind = inp[0]
    if kind == 'residual':
        require(len(inp) == 4 and is_int(inp[1]) and inp[1] >= 1 and int_list(inp[2], inp[1]) and int_list(inp[3], None, True)
                and sum(inp[3]) == inp[1], 'G1_SCHEMA:input')
        return expected_residual(inp[1], tuple(inp[2]), tuple(inp[3]))
    if kind == 'weighted':
        require(len(inp) == 5 and is_int(inp[1]) and inp[1] >= 1 and int_list(inp[2], inp[1]) and int_list(inp[3], None, True)
                and sum(inp[3]) == inp[1] and int_list(inp[4], inp[1], True), 'G1_SCHEMA:input')
        return expected_weighted(inp[1], tuple(inp[2]), tuple(inp[3]), tuple(inp[4]))
    if kind == 'twocycle':
        require(len(inp) == 5 and is_int(inp[1]) and inp[1] >= 1 and int_list(inp[2], inp[1]) and is_int(inp[3]) and inp[3] >= 1
                and int_list(inp[4], inp[3]), 'G1_SCHEMA:input')
        return expected_twocycle(inp[1], tuple(inp[2]), inp[3], tuple(inp[4]))
    raise ValueError('G1_SCHEMA:unknown_kind')


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        records = data['records']
        require(len(records) == len(public['cases']), 'G2_COVERAGE:record_count')
        seen = []
        for r in records:
            require(type(r) is dict and r.get('kind') in KEYS and set(r) == KEYS[r['kind']], 'G1_SCHEMA:record_keys')
            require(type(r['input']) is list and r['input'][:1] == [r['kind']], 'G1_SCHEMA:input')
            seen.append(repr(r['input']))
            want = expected(r['input'])
            for k in want:
                require(r[k] == want[k] and type(r[k]) is type(want[k]), 'G3_WITNESS:' + r['kind'] + '_' + k)
            # the node's claim (weights not derivable from Phi1, Gamma2) must be visible exactly where its hypotheses hold
            if r['kind'] == 'residual':
                n, sizes = r['input'][1], r['input'][3]
                if n >= 2 and want['phi1'] > 0 and len(sizes) >= 2:
                    require(not r['determined'], 'G3_WITNESS:sector_weights_determined_but_hypotheses_hold')
                if n >= 2 and want['phi1'] > 0:
                    require(not r['unique'], 'G3_WITNESS:unique_minimizer_but_hypotheses_hold')
                if n >= 2 and want['phi1'] >= 2:
                    require(r['sumsq_min'] < r['sumsq_max'], 'G3_WITNESS:sum_of_squares_is_not_constant_on_minimizers')
                if want['phi1'] == 0:
                    require(r['status'] == 'zero_mass_refused' and r['unique'], 'G3_WITNESS:zero_mass')
            if r['kind'] == 'weighted' and want['weighted_phi1'] == 0:
                require(r['status'] == 'zero_mass_refused' and r['unique'], 'G3_WITNESS:zero_mass')
        require(sorted(seen) == sorted(repr(c) for c in public['cases']), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
