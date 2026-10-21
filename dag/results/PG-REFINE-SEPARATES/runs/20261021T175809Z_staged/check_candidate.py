"""Independent checker for PG-REFINE-SEPARATES.

Recomputes every record from the public cases without importing the producer, by different algorithms:
components by union-find; the number of proper one-bit tags as 2^components when a breadth-first
two-colouring succeeds (else 0); the chromatic number by dynamic programming over vertex subsets (cover
by independent sets); the minimal bit count as bit_length(chi-1); the odd girth as the least odd k with
a nonzero trace of A^k; the enumeration tables by bitmask graphs with the identity
sum over bipartite G of 2^c(G) = sum_k C(n,k) 2^(k(n-k)); injective tag counts as falling factorials;
the refinement counts by closed forms. AuthorityEffect: None.
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

TASK = 'PG-REFINE-SEPARATES'
KEYS = {
    'graph': {'kind', 'name', 'n', 'edges', 'components', 'bipartite', 'one_bit_tags', 'chi', 'min_bits', 'odd_girth'},
    'enum': {'kind', 'n', 'graphs', 'bipartite', 'bipartite_colouring_pairs', 'by_min_bits'},
    'fiber': {'kind', 'm', 'min_bits', 'injective_tags_by_bits'},
    'fiberbits': {'kind', 'm', 'min_bits'},
    'refine': {'kind', 'n', 'o', 't', 'quadruples', 'iff_failures', 'separated_by_tag', 'refined_equal', 'old_separation_kept'},
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def int_list(x, size=None):
    return type(x) is list and all(is_int(v) for v in x) and (size is None or len(x) == size)


def parse_edges(text):
    if text == '-':
        return []
    out = set()
    for part in text.split(','):
        u, v = part.split('-')
        out.add((min(int(u), int(v)), max(int(u), int(v))))
    return sorted(out)


def union_find_components(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        parent[find(u)] = find(v)
    return len({find(x) for x in range(n)})


def bfs_bipartite(n, edges):
    nbr = {x: [] for x in range(n)}
    for u, v in edges:
        nbr[u].append(v)
        nbr[v].append(u)
    side = {}
    for s in range(n):
        if s in side:
            continue
        side[s] = 0
        frontier = [s]
        while frontier:
            nxt = []
            for x in frontier:
                for y in nbr[x]:
                    if y not in side:
                        side[y] = 1 - side[x]
                        nxt.append(y)
                    elif side[y] == side[x]:
                        return False
            frontier = nxt
    return True


def chi_by_subsets(n, edges):
    adjmask = [0] * n
    for u, v in edges:
        adjmask[u] |= 1 << v
        adjmask[v] |= 1 << u
    full = (1 << n) - 1
    independent = [True] * (full + 1)
    for s in range(1, full + 1):
        low = (s & -s).bit_length() - 1
        rest = s & (s - 1)
        independent[s] = independent[rest] and not (adjmask[low] & rest)
    best = [0] + [99] * full
    for s in range(1, full + 1):
        low = s & -s
        sub = s
        while sub:
            if sub & low and independent[sub] and best[s ^ sub] + 1 < best[s]:
                best[s] = best[s ^ sub] + 1
            sub = (sub - 1) & s
    return best[full]


def odd_girth_by_trace(n, edges):
    a = [[0] * n for _ in range(n)]
    for u, v in edges:
        a[u][v] = a[v][u] = 1
    power = [row[:] for row in a]
    k = 1
    while k <= n:
        if sum(power[i][i] for i in range(n)) > 0:
            return k
        # advance by two steps: A^(k+2)
        for _ in range(2):
            power = [[sum(power[i][t] * a[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        k += 2
    return 0


def graph_expected(name, n, text):
    edges = parse_edges(text)
    bip = bfs_bipartite(n, edges)
    comps = union_find_components(n, edges)
    chi = chi_by_subsets(n, edges)
    return {'kind': 'graph', 'name': name, 'n': n, 'edges': [list(e) for e in edges], 'components': comps, 'bipartite': bip,
            'one_bit_tags': 2 ** comps if bip else 0, 'chi': chi, 'min_bits': (chi - 1).bit_length(), 'odd_girth': odd_girth_by_trace(n, edges)}


def enum_expected(n):
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    bip_count = 0
    colouring_pairs = 0
    by_bits = [0, 0, 0, 0]
    for mask in range(1 << len(pairs)):
        edges = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        chi = chi_by_subsets(n, edges)
        by_bits[(chi - 1).bit_length()] += 1
        if bfs_bipartite(n, edges):
            bip_count += 1
            colouring_pairs += 2 ** union_find_components(n, edges)
    closed = sum(comb(n, k) * 2 ** (k * (n - k)) for k in range(n + 1))
    require(colouring_pairs == closed, 'G3_WITNESS:colouring_pair_identity')
    require(bip_count == by_bits[0] + by_bits[1], 'G3_WITNESS:bipartite_equals_at_most_one_bit')
    return {'kind': 'enum', 'n': n, 'graphs': 2 ** len(pairs), 'bipartite': bip_count, 'bipartite_colouring_pairs': closed, 'by_min_bits': by_bits}


def falling(k, m):
    out = 1
    for i in range(m):
        out *= max(k - i, 0)
    return out


def fiber_expected(m):
    return {'kind': 'fiber', 'm': m, 'min_bits': (m - 1).bit_length(), 'injective_tags_by_bits': [falling(2 ** b, m) for b in range(4)]}


def refine_expected(n, o, t):
    """Evaluate the refinement (q, t) on every (q, t, a, b) and compare with the closed forms."""
    total = failures = sep = equal = old = 0
    for q in product(range(o), repeat=n):
        for g in product(range(t), repeat=n):
            ref = [(q[x], g[x]) for x in range(n)]
            for a in range(n):
                for b in range(n):
                    total += 1
                    same_ref = ref[a] == ref[b]
                    equal += same_ref
                    failures += same_ref != (q[a] == q[b] and g[a] == g[b])
                    if q[a] == q[b] and g[a] != g[b]:
                        sep += 1
                        failures += same_ref
                    if q[a] != q[b]:
                        old += 1
                        failures += same_ref
    require(sep == n * (n - 1) * o ** (n - 1) * t ** (n - 1) * (t - 1), 'G3_WITNESS:separated_closed_form')
    require(old == n * (n - 1) * o ** (n - 1) * (o - 1) * t ** n, 'G3_WITNESS:old_kept_closed_form')
    return {'kind': 'refine', 'n': n, 'o': o, 't': t, 'quadruples': total, 'iff_failures': failures,
            'separated_by_tag': sep, 'refined_equal': equal, 'old_separation_kept': old}


_CACHE = {}


def expected(case):
    key = repr(case)
    if key not in _CACHE:
        _CACHE[key] = _expected(case)
    return _CACHE[key]


def _expected(case):
    kind = case[0]
    if kind == 'graph':
        return graph_expected(case[1], case[2], case[3])
    if kind == 'enum':
        return enum_expected(case[1])
    if kind == 'fiber':
        return fiber_expected(case[1])
    if kind == 'fiberbits':
        return {'kind': 'fiberbits', 'm': case[1], 'min_bits': (case[1] - 1).bit_length()}
    if kind == 'refine':
        return refine_expected(case[1], case[2], case[3])
    raise ValueError('G2_COVERAGE:unknown_case_kind')


def key_of(item):
    return repr((item['kind'], item.get('name'), item.get('n'), item.get('m'), item.get('o'), item.get('t')))


def check_types(r):
    kind = r['kind']
    require(kind in KEYS and set(r) == KEYS[kind], 'G1_SCHEMA:record_keys')
    for k, v in r.items():
        if k in ('kind', 'name'):
            require(type(v) is str, 'G1_SCHEMA:string_field')
        elif k == 'bipartite' and kind == 'graph':
            require(type(v) is bool, 'G1_SCHEMA:bool_field')
        elif k == 'edges':
            require(type(v) is list and all(int_list(e, 2) for e in v), 'G1_SCHEMA:edges')
        elif k == 'by_min_bits':
            require(int_list(v, 4), 'G1_SCHEMA:by_min_bits')
        elif k == 'injective_tags_by_bits':
            require(int_list(v, 4), 'G1_SCHEMA:injective_tags_by_bits')
        else:
            require(is_int(v), 'G1_SCHEMA:int_field')


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = public['cases']
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        for r in records:
            require(type(r) is dict and 'kind' in r, 'G1_SCHEMA:record')
            check_types(r)
        want = {key_of(expected(c)): dict(expected(c)) for c in cases}
        require(len(want) == len(cases), 'G2_COVERAGE:duplicate_cases')
        got = {key_of(r): r for r in records}
        require(len(got) == len(records) and set(got) == set(want), 'G2_COVERAGE:records_are_the_public_cases')
        for k, r in got.items():
            w = want[k]
            for field in w:
                require(r[field] == w[field], 'G3_WITNESS:%s:%s' % (r['kind'], field))
            # Theorem-level consistency read off the candidate itself:
            if r['kind'] == 'graph':
                require(r['bipartite'] == (r['odd_girth'] == 0), 'G3_WITNESS:odd_cycle_refuses_one_bit')
                require(r['bipartite'] == (r['min_bits'] <= 1), 'G3_WITNESS:one_bit_iff_two_colourable')
                require(2 ** r['min_bits'] >= r['chi'] > 2 ** (r['min_bits'] - 1) if r['min_bits'] else r['chi'] == 1,
                        'G3_WITNESS:bits_are_ceil_log2_chi')
            if r['kind'] == 'refine':
                require(r['iff_failures'] == 0, 'G3_WITNESS:refine_iff_holds')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ZeroDivisionError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
