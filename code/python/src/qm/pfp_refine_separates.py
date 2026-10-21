"""Supplied binary tag refinement and many conflicts: exact finite tables.

Producer for PFP batch 01, node PG-REFINE-SEPARATES. Exact integers only; no random numbers.
Scope: a report q, a supplied tag t, the refined report (q, t); conflict graphs on small vertex sets,
their proper 1-bit tags (2-colourings), minimal bit counts, all labelled graphs on up to 5 vertices,
and fibres of size m. Finding a tag is a search problem: these tables are NOT an algorithmic claim.
AuthorityEffect: None.
"""
from itertools import product

CASES = [
    ['graph', 'edgeless3', 3, '-'],
    ['graph', 'edge', 2, '0-1'],
    ['graph', 'path4', 4, '0-1,1-2,2-3'],
    ['graph', 'cycle4', 4, '0-1,1-2,2-3,0-3'],
    ['graph', 'triangle', 3, '0-1,1-2,0-2'],
    ['graph', 'triangle_plus_isolated', 4, '0-1,1-2,0-2'],
    ['graph', 'two_disjoint_edges', 4, '0-1,2-3'],
    ['graph', 'cycle5', 5, '0-1,1-2,2-3,3-4,0-4'],
    ['graph', 'cycle7', 7, '0-1,1-2,2-3,3-4,4-5,5-6,0-6'],
    ['graph', 'k4', 4, '0-1,0-2,0-3,1-2,1-3,2-3'],
    ['graph', 'k5', 5, '0-1,0-2,0-3,0-4,1-2,1-3,1-4,2-3,2-4,3-4'],
    ['graph', 'k33', 6, '0-3,0-4,0-5,1-3,1-4,1-5,2-3,2-4,2-5'],
    ['graph', 'wheel5', 6, '0-1,1-2,2-3,3-4,0-4,0-5,1-5,2-5,3-5,4-5'],
    ['graph', 'petersen', 10, '0-1,1-2,2-3,3-4,0-4,0-5,1-6,2-7,3-8,4-9,5-7,7-9,9-6,6-8,8-5'],
    ['enum', 1], ['enum', 2], ['enum', 3], ['enum', 4], ['enum', 5],
    ['fiber', 1], ['fiber', 2], ['fiber', 3], ['fiber', 4], ['fiber', 5],
    ['fiberbits', 6], ['fiberbits', 8], ['fiberbits', 9], ['fiberbits', 17],
    ['refine', 2, 2, 2], ['refine', 3, 2, 2], ['refine', 3, 3, 2], ['refine', 3, 2, 3], ['refine', 4, 2, 2],
]


def parse_edges(text):
    if text == '-':
        return []
    out = set()
    for part in text.split(','):
        u, v = part.split('-')
        u, v = int(u), int(v)
        out.add((min(u, v), max(u, v)))
    return sorted(out)


def edges_text(edges):
    return ','.join('%d-%d' % (u, v) for u, v in edges) or '-'


def adjacency(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def components(n, edges):
    adj = adjacency(n, edges)
    seen = [False] * n
    count = 0
    for s in range(n):
        if seen[s]:
            continue
        count += 1
        stack = [s]
        seen[s] = True
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if not seen[y]:
                    seen[y] = True
                    stack.append(y)
    return count


def one_bit_tags(n, edges):
    """Number of tags t: V -> {0,1} with t(u) != t(v) on every edge, by exhaustive enumeration."""
    return sum(1 for t in product((0, 1), repeat=n) if all(t[u] != t[v] for u, v in edges))


def colourable(n, edges, k):
    """Backtracking search for a proper colouring with k colours."""
    adj = adjacency(n, edges)
    colour = [-1] * n

    def go(v):
        if v == n:
            return True
        for c in range(k):
            if all(colour[w] != c for w in adj[v] if w < v):
                colour[v] = c
                if go(v + 1):
                    return True
        colour[v] = -1
        return False

    return go(0)


def chromatic_number(n, edges):
    k = 1
    while not colourable(n, edges, k):
        k += 1
    return k


def min_bits(n, edges):
    b = 0
    while not colourable(n, edges, 2 ** b):
        b += 1
    return b


def odd_girth(n, edges):
    """Length of a shortest odd cycle (0 if none): breadth-first levels, equal-level edge gives 2d+1."""
    adj = adjacency(n, edges)
    best = 0
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        queue = [s]
        for x in queue:
            for y in adj[x]:
                if dist[y] < 0:
                    dist[y] = dist[x] + 1
                    queue.append(y)
        for u, v in edges:
            if dist[u] >= 0 and dist[u] == dist[v]:
                length = 2 * dist[u] + 1
                if best == 0 or length < best:
                    best = length
    return best


def graph_record(name, n, text):
    edges = parse_edges(text)
    tags = one_bit_tags(n, edges)
    return {'kind': 'graph', 'name': name, 'n': n, 'edges': [list(e) for e in edges], 'components': components(n, edges),
            'bipartite': tags > 0, 'one_bit_tags': tags, 'chi': chromatic_number(n, edges), 'min_bits': min_bits(n, edges),
            'odd_girth': odd_girth(n, edges)}


def enum_record(n):
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    total = 0
    bipartite = 0
    colouring_pairs = 0
    by_bits = [0, 0, 0, 0]
    for mask in range(1 << len(pairs)):
        edges = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        total += 1
        tags = one_bit_tags(n, edges)
        if tags:
            bipartite += 1
            colouring_pairs += tags
        by_bits[min_bits(n, edges)] += 1
    return {'kind': 'enum', 'n': n, 'graphs': total, 'bipartite': bipartite, 'bipartite_colouring_pairs': colouring_pairs,
            'by_min_bits': by_bits}


def fiber_bits(m):
    b = 0
    while 2 ** b < m:
        b += 1
    return b


def fiber_record(m):
    counts = []
    for b in range(4):
        k = 2 ** b
        counts.append(sum(1 for t in product(range(k), repeat=m) if len(set(t)) == m))
    return {'kind': 'fiber', 'm': m, 'min_bits': fiber_bits(m), 'injective_tags_by_bits': counts}


def refine_record(n, o, t):
    total = 0
    failures = 0
    sep_by_tag = 0
    refined_equal = 0
    old_kept = 0
    for q in product(range(o), repeat=n):
        for g in product(range(t), repeat=n):
            ref = [(q[a], g[a]) for a in range(n)]
            for a in range(n):
                for b in range(n):
                    total += 1
                    equal = ref[a] == ref[b]
                    both = q[a] == q[b] and g[a] == g[b]
                    if equal != both:
                        failures += 1
                    if q[a] == q[b] and g[a] != g[b]:
                        sep_by_tag += 1
                        if equal:
                            failures += 1
                    if q[a] != q[b]:
                        old_kept += 1
                        if equal:
                            failures += 1
                    if equal:
                        refined_equal += 1
    return {'kind': 'refine', 'n': n, 'o': o, 't': t, 'quadruples': total, 'iff_failures': failures, 'separated_by_tag': sep_by_tag,
            'refined_equal': refined_equal, 'old_separation_kept': old_kept}


def record(case):
    kind = case[0]
    if kind == 'graph':
        return graph_record(case[1], case[2], case[3])
    if kind == 'enum':
        return enum_record(case[1])
    if kind == 'fiber':
        return fiber_record(case[1])
    if kind == 'fiberbits':
        return {'kind': 'fiberbits', 'm': case[1], 'min_bits': fiber_bits(case[1])}
    if kind == 'refine':
        return refine_record(case[1], case[2], case[3])
    raise ValueError('unknown case kind ' + str(kind))


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def _line(r):
    k = r['kind']
    if k == 'graph':
        return '\t'.join(['graph', r['name'], str(r['n']), str(len(r['edges'])), str(r['components']), str(int(r['bipartite'])),
                          str(r['one_bit_tags']), str(r['chi']), str(r['min_bits']), str(r['odd_girth']), edges_text(r['edges'])])
    if k == 'enum':
        return '\t'.join(['enum', str(r['n']), str(r['graphs']), str(r['bipartite']), str(r['bipartite_colouring_pairs'])]
                        + [str(x) for x in r['by_min_bits']])
    if k == 'fiber':
        return '\t'.join(['fiber', str(r['m']), str(r['min_bits'])] + [str(x) for x in r['injective_tags_by_bits']])
    if k == 'fiberbits':
        return '\t'.join(['fiberbits', str(r['m']), str(r['min_bits'])])
    return '\t'.join(['refine', str(r['n']), str(r['o']), str(r['t']), str(r['quadruples']), str(r['iff_failures']),
                      str(r['separated_by_tag']), str(r['refined_equal']), str(r['old_separation_kept'])])


def wire_lines(data):
    return [_line(r) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('\t'.join(str(x) for x in c) + '\n' for c in cases)
