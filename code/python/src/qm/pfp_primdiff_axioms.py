"""Primitive-difference axioms A1-A10 and the admission kernel: exhaustive finite models on carriers of size 1, 2, 3.

Producer for PFP batch 01, node PG-PRIMDIFF-AXIOMS. Exact integers only; no random numbers; no floats.

Source facts used. The Rust enum `PrimitiveDifferenceAxiom` (code/rust/src/wdp/primitive_axiomatics.rs, line 24) lists
ten axiom NAMES with no predicate; the only code that realises any of them is `GenesisAdmissionKernel::admit_difference`
(A1 and carrier membership), `EvaluationPreorder` (A3, reflexive-transitive closure), the cochain tests (A5) and the
triad tests (A8-like classification). The transcriptions below are therefore OURS and each is labelled by status:
a state predicate, a theorem true in every structure, equivalent to another axiom, checked on named complexes only,
or not a state predicate. Independence and consistency on carriers of size at most 3 is NOT a derivation of the list.
AuthorityEffect: None.
"""
from functools import lru_cache
from itertools import permutations, product

NAMES = ['A01NonIdentification', 'A02UnentailedAdmission', 'A03EvaluationRelation', 'A04DirectedEvaluationCarrier',
         'A05NilpotentCoboundary', 'A06QuotientDefectPurity', 'A07DescendedClosureMap', 'A08TriadTrichotomy',
         'A09ObserverSelectedMetric', 'A10AntiReificationFirewall']
STATUS = ['state_predicate', 'not_a_state_predicate', 'theorem_true_in_every_structure', 'state_predicate', 'state_predicate',
          'checked_on_named_complexes', 'equivalent_to_A5', 'checked_on_named_complexes', 'checked_on_named_complexes',
          'state_predicate']
COMPLEXES = {
    'filled_triangle': (3, '0-1,1-2,0-2', '0-1-2'),
    'open_triangle': (3, '0-1,1-2,0-2', '-'),
    'path2': (3, '0-1,1-2', '-'),
    'broken_face': (3, '0-1,1-2', '0-1-2'),
    'floating_face': (3, '-', '0-1-2'),
    'double_edge': (2, '0-1,1-0', '-'),
}
CASES = ([['axiom', k] for k in range(1, 11)] + [['models', n] for n in (1, 2, 3)] + [['unentailed', n] for n in (2, 3)]
         + [['kernel', n] for n in (2, 3)] + [['closure', n] for n in (1, 2, 3)]
         + [['triad', name, c[0], c[1], c[2]] for name, c in COMPLEXES.items()])


# ---------------------------------------------------------------- structures
def pairs(n):
    return [(u, v) for u in range(n) for v in range(n)]


def relation(n, mask):
    return [(u, v) for i, (u, v) in enumerate(pairs(n)) if mask >> i & 1]


def faces_of(n, f):
    return [(0, 1, 2)] if f and n == 3 else []


def closure(n, edges):
    reach = [[u == v for v in range(n)] for u in range(n)]
    for u, v in edges:
        reach[u][v] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = True
    return reach


def a3_holds(n, edges):
    r = closure(n, edges)
    reflexive = all(r[i][i] for i in range(n))
    transitive = all(not (r[i][j] and r[j][k]) or r[i][k] for i in range(n) for j in range(n) for k in range(n))
    return reflexive and transitive and all(r[u][v] for u, v in edges)


def d0_matrix(n, edges):
    rows = []
    for u, v in edges:
        row = [0] * n
        row[v] += 1
        row[u] -= 1
        rows.append(row)
    return rows


def d1_matrix(edges, faces):
    index = {e: i for i, e in enumerate(edges)}
    rows = []
    for a, b, c in faces:
        row = [0] * len(edges)
        if (b, c) in index:
            row[index[(b, c)]] += 1
        if (a, c) in index:
            row[index[(a, c)]] -= 1
        if (a, b) in index:
            row[index[(a, b)]] += 1
        rows.append(row)
    return rows


def matmul(m1, m2, inner):
    return [[sum(r[k] * m2[k][j] for k in range(inner)) for j in range(len(m2[0]) if m2 else 0)] for r in m1]


def a5_holds(n, edges, faces):
    """d1 o d0 = 0 as an integer matrix product."""
    if not faces:
        return True
    d0, d1 = d0_matrix(n, edges), d1_matrix(edges, faces)
    if not edges:
        return True
    prod = matmul(d1, d0, len(edges))
    return all(x == 0 for row in prod for x in row)


def a7_holds(n, edges, faces):
    """d1 vanishes on the image of d0, tested on the unit potentials (descent to the quotient)."""
    for v in range(n):
        phi = [1 if x == v else 0 for x in range(n)]
        psi = {e: phi[e[1]] - phi[e[0]] for e in edges}
        for a, b, c in faces:
            total = psi.get((b, c), 0) - psi.get((a, c), 0) + psi.get((a, b), 0)
            if total != 0:
                return False
    return True


def well_formed(edges, faces):
    return all((a, b) in edges and (b, c) in edges and (a, c) in edges for a, b, c in faces)


def a1_holds(d_edges):
    return all(u != v for u, v in d_edges)


def a4_holds(edges):
    s = set(edges)
    return all(u != v for u, v in edges) and all((v, u) not in s for u, v in edges)


@lru_cache(maxsize=None)
def block_histograms(n):
    d_hist, ef_hist = {}, {}
    for mask in range(1 << (n * n)):
        sig = a1_holds(relation(n, mask))
        d_hist[sig] = d_hist.get(sig, 0) + 1
    for mask in range(1 << (n * n)):
        edges = relation(n, mask)
        for f in ((0, 1) if n == 3 else (0,)):
            faces = faces_of(n, f)
            sig = (a3_holds(n, edges), a4_holds(edges), a5_holds(n, edges, faces), a7_holds(n, edges, faces), well_formed(edges, faces))
            ef_hist[sig] = ef_hist.get(sig, 0) + 1
    return d_hist, ef_hist, {True: 1, False: 1}


@lru_cache(maxsize=None)
def joint(n):
    """Exhaustive joint histogram over all structures (D, E, F, alpha): predicates read one block each, so the number
    of structures with a signature is the product of the block counts."""
    d_hist, ef_hist, a_hist = block_histograms(n)
    out = {}
    for a1, cd in d_hist.items():
        for (a3, a4, a5, a7, w), ce in ef_hist.items():
            for a10, ca in a_hist.items():
                key = (a1, a3, a4, a5, a7, a10, w)
                out[key] = out.get(key, 0) + cd * ce * ca
    return out


def axiom_record(k):
    counts = [-1, -1, -1]
    status = STATUS[k - 1]
    if status in ('state_predicate', 'theorem_true_in_every_structure', 'equivalent_to_A5'):
        position = {1: 0, 3: 1, 4: 2, 5: 3, 7: 4, 10: 5}[k]
        counts = []
        for n in (1, 2, 3):
            counts.append(sum(c for key, c in joint(n).items() if key[position]))
    return {'kind': 'axiom', 'index': k, 'name': NAMES[k - 1], 'status': status, 'models_by_n': counts}


def models_record(n):
    hist = joint(n)
    total = sum(hist.values())
    violate = [0] * 6
    a5_a7_jointly = 0
    all_hold = 0
    w_models = a5_not_w = 0
    patterns = set()
    for key, c in hist.items():
        bits = key[:6]
        patterns.add(bits)
        if all(bits):
            all_hold += c
        missing = [i for i in range(6) if not bits[i]]
        if len(missing) == 1:
            violate[missing[0]] += c
        if missing == [3, 4]:
            a5_a7_jointly += c
        if key[6]:
            w_models += c
        if key[3] and not key[6]:
            a5_not_w += c
    return {'kind': 'models', 'n': n, 'total': total, 'all_hold': all_hold, 'violate_only': violate, 'violate_a5_a7_jointly': a5_a7_jointly,
            'a5_equals_a7': all(key[3] == key[4] for key in hist), 'well_formed_models': w_models, 'a5_without_well_formed': a5_not_w,
            'distinct_signatures': len(patterns)}


def unentailed_record(n):
    d_hist, ef_hist, a_hist = block_histograms(n)
    ef_models = sum(c for (a3, a4, a5, a7, w), c in ef_hist.items() if a3 and a4 and a5 and a7) * a_hist[True]
    offdiag = [(u, v) for u, v in pairs(n) if u != v]
    withs = set()
    for p in offdiag:
        count = sum(1 for mask in range(1 << (n * n)) if a1_holds(relation(n, mask)) and p in relation(n, mask))
        withs.add(count * ef_models)
    diag_in_model = sum(1 for mask in range(1 << (n * n)) if a1_holds(relation(n, mask)) and any(u == v for u, v in relation(n, mask)))
    models = d_hist[True] * ef_models
    if len(withs) != 1:
        raise ValueError('pair counts differ')
    with_each = withs.pop()
    return {'kind': 'unentailed', 'n': n, 'models': models, 'offdiag_pairs': len(offdiag), 'with_each_offdiag_pair': with_each,
            'without_each_offdiag_pair': models - with_each, 'diagonal_pairs_in_a_model': diag_in_model, 'models_with_empty_d': ef_models}


# ---------------------------------------------------------------- kernel
def kernel_admit(carrier, admitted, a, b, token):
    """Transcription of GenesisAdmissionKernel::admit_difference: A1 first, then carrier membership; the token is stored."""
    if a == b:
        return 'a1'
    if a not in carrier or b not in carrier:
        return 'carrier'
    admitted.append((a, b, token))
    return 'ok'


def kernel_record(n):
    carrier = set(range(n))
    names = range(n + 1)
    counts = {'ok': 0, 'a1': 0, 'carrier': 0}
    token_irrelevant = True
    for a in names:
        for b in names:
            outcomes = set()
            for token in (0, 1):
                outcome = kernel_admit(carrier, [], a, b, token)
                outcomes.add(outcome)
                counts[outcome] += 1
            token_irrelevant = token_irrelevant and len(outcomes) == 1
    store = []
    first = kernel_admit(carrier, store, 0, 1, 0)
    second = kernel_admit(carrier, store, 0, 1, 0)
    reverse = kernel_admit(carrier, store, 1, 0, 1)
    return {'kind': 'kernel', 'n': n, 'probes': 2 * (n + 1) ** 2, 'ok': counts['ok'], 'err_a1': counts['a1'], 'err_carrier': counts['carrier'],
            'token_irrelevant': token_irrelevant, 'empty_token_admitted': first == 'ok', 'duplicates_stored': second == 'ok' and store.count((0, 1, 0)) == 2,
            'reverse_orientation_admitted': reverse == 'ok', 'a1_before_carrier': kernel_admit(carrier, [], n, n, 0) == 'a1'}


# ---------------------------------------------------------------- closure (A3)
def closure_record(n):
    seen = set()
    all_preorders = contains = reach_equal = True
    count = 0
    for mask in range(1 << (n * n)):
        edges = relation(n, mask)
        count += 1
        r = closure(n, edges)
        all_preorders = all_preorders and a3_holds(n, edges)
        contains = contains and all(r[u][v] for u, v in edges)
        seen.add(tuple(tuple(row) for row in r))
        # reachability by depth-first search from every vertex
        for s in range(n):
            stack, visited = [s], {s}
            while stack:
                x = stack.pop()
                for u, v in edges:
                    if u == x and v not in visited:
                        visited.add(v)
                        stack.append(v)
            reach_equal = reach_equal and all(r[s][t] == (t in visited) for t in range(n))
    return {'kind': 'closure', 'n': n, 'relations': count, 'distinct_closures': len(seen), 'all_preorders': all_preorders,
            'contains_relation': contains, 'equals_reachability': reach_equal}


# ---------------------------------------------------------------- triads (A6, A8, A9 on named complexes)
def parse_edges(text):
    return [] if text == '-' else [tuple(int(x) for x in part.split('-')) for part in text.split(',')]


def parse_faces(text):
    return [] if text == '-' else [tuple(int(x) for x in part.split('-')) for part in text.split(',')]


def phi1(n, edges, h):
    """Unit-weight L1 distance from h to the image of d0, by enumeration of spanning forests (exact integers)."""
    real = [i for i, (u, v) in enumerate(edges) if u != v]
    comps = n
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for i in real:
        ru, rv = find(edges[i][0]), find(edges[i][1])
        if ru != rv:
            parent[ru] = rv
            comps -= 1
    size = n - comps
    best = None
    for tree in subsets(real, size):
        uf = list(range(n))

        def root(x):
            while uf[x] != x:
                x = uf[x]
            return x

        acyclic = True
        for i in tree:
            ru, rv = root(edges[i][0]), root(edges[i][1])
            if ru == rv:
                acyclic = False
                break
            uf[ru] = rv
        if not acyclic:
            continue
        phi = [None] * n
        for start in range(n):
            if phi[start] is not None:
                continue
            phi[start] = 0
            stack = [start]
            while stack:
                x = stack.pop()
                for i in tree:
                    u, v = edges[i]
                    if u == x and phi[v] is None:
                        phi[v] = phi[u] + h[i]
                        stack.append(v)
                    elif v == x and phi[u] is None:
                        phi[u] = phi[v] - h[i]
                        stack.append(u)
        cost = sum(abs(h[i] - (phi[edges[i][1]] - phi[edges[i][0]])) for i in range(len(edges)))
        if best is None or cost < best:
            best = cost
    return best if best is not None else 0


def subsets(items, size):
    """All subsets of `items` of the given size."""
    if size == 0:
        yield ()
        return
    for i, x in enumerate(items):
        for rest in subsets(items[i + 1:], size - 1):
            yield (x,) + rest


def coboundary(edges, faces, h):
    index = {e: i for i, e in enumerate(edges)}
    out = []
    for a, b, c in faces:
        out.append((h[index[(b, c)]] if (b, c) in index else 0) - (h[index[(a, c)]] if (a, c) in index else 0)
                   + (h[index[(a, b)]] if (a, b) in index else 0))
    return out


def triad_record(name, n, edges_text, faces_text):
    edges, faces = parse_edges(edges_text), parse_faces(faces_text)
    counts = {'E': 0, 'C': 0, 'R': 0, 'X': 0}
    phi_sum = phi_max = 0
    gauge = relabel = True
    box = list(product((-1, 0, 1), repeat=len(edges)))
    gauges = list(product((-1, 0, 1), repeat=n))
    for h in box:
        p = phi1(n, edges, h)
        phi_sum += p
        phi_max = max(phi_max, p)
        closed = all(x == 0 for x in coboundary(edges, faces, h))
        exact = p == 0
        counts['E' if exact and closed else 'X' if exact else 'C' if closed else 'R'] += 1
        for psi in gauges:
            shifted = [h[i] + psi[edges[i][1]] - psi[edges[i][0]] for i in range(len(edges))]
            if phi1(n, edges, shifted) != p:
                gauge = False
        for perm in permutations(range(n)):
            moved = [(perm[u], perm[v]) for u, v in edges]
            if phi1(n, moved, h) != p:
                relabel = False
    return {'kind': 'triad', 'name': name, 'n': n, 'edges': [list(e) for e in edges], 'faces': [list(f) for f in faces],
            'cochains': len(box), 'exact': counts['E'], 'closed_nonexact': counts['C'], 'rupture': counts['R'],
            'exact_nonclosed': counts['X'], 'rcl_refusals': counts['X'], 'phi1_sum': phi_sum, 'phi1_max': phi_max,
            'gauge_invariant': gauge, 'relabel_invariant': relabel, 'nilpotent': a5_holds(n, edges, faces),
            'well_formed': well_formed(edges, faces)}


def record(case):
    kind = case[0]
    if kind == 'axiom':
        return axiom_record(case[1])
    if kind == 'models':
        return models_record(case[1])
    if kind == 'unentailed':
        return unentailed_record(case[1])
    if kind == 'kernel':
        return kernel_record(case[1])
    if kind == 'closure':
        return closure_record(case[1])
    if kind == 'triad':
        return triad_record(case[1], case[2], case[3], case[4])
    raise ValueError('unknown case kind ' + str(kind))


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def _text(items):
    return ','.join('-'.join(str(x) for x in it) for it in items) or '-'


def _line(r):
    k = r['kind']
    if k == 'axiom':
        return '\t'.join(['axiom', str(r['index']), r['name'], r['status']] + [str(x) for x in r['models_by_n']])
    if k == 'models':
        return '\t'.join(['models', str(r['n']), str(r['total']), str(r['all_hold'])] + [str(x) for x in r['violate_only']] + [str(r['violate_a5_a7_jointly'])]
                         + [str(int(r['a5_equals_a7'])), str(r['well_formed_models']), str(r['a5_without_well_formed']), str(r['distinct_signatures'])])
    if k == 'unentailed':
        return '\t'.join(['unentailed', str(r['n']), str(r['models']), str(r['offdiag_pairs']), str(r['with_each_offdiag_pair']),
                          str(r['without_each_offdiag_pair']), str(r['diagonal_pairs_in_a_model']), str(r['models_with_empty_d'])])
    if k == 'kernel':
        return '\t'.join(['kernel', str(r['n']), str(r['probes']), str(r['ok']), str(r['err_a1']), str(r['err_carrier']),
                          str(int(r['token_irrelevant'])), str(int(r['empty_token_admitted'])), str(int(r['duplicates_stored'])),
                          str(int(r['reverse_orientation_admitted'])), str(int(r['a1_before_carrier']))])
    if k == 'closure':
        return '\t'.join(['closure', str(r['n']), str(r['relations']), str(r['distinct_closures']), str(int(r['all_preorders'])),
                          str(int(r['contains_relation'])), str(int(r['equals_reachability']))])
    return '\t'.join(['triad', r['name'], str(r['n']), _text(r['edges']), _text(r['faces']), str(r['cochains']), str(r['exact']),
                      str(r['closed_nonexact']), str(r['rupture']), str(r['exact_nonclosed']), str(r['rcl_refusals']), str(r['phi1_sum']),
                      str(r['phi1_max']), str(int(r['gauge_invariant'])), str(int(r['relabel_invariant'])), str(int(r['nilpotent'])),
                      str(int(r['well_formed']))])


def wire_lines(data):
    return [_line(r) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('\t'.join(str(x) for x in c) + '\n' for c in cases)
