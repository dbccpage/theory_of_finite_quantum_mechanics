"""Obligation monoid: exact tables for counter vectors, event traces and the generate/discharge ledger.

Producer for PFP batch 01, node PG-OBLIGATION-MONOID.  Five record kinds:

* laws       k n   : the box {0..n-1}^k of obligation counter vectors under pointwise sum; every triple tested for
                     associativity, commutativity, unit, cancellation, and every nonzero vector tested for an inverse.
* bounded    k M   : the partial combine that refuses when a count would exceed the bound M (the CountOverflow rule,
                     bound 2^64 - 1 in the Rust source); both bracketings of every triple compared.
* saturating cap   : the saturating-sum alternative (k = 1), which the Rust source refuses to use; cancellation FAILS.
* events     word  : words over D(eclareTerm), A(ssertDiff), R(emoveDiff), I(dentifyTerms) mapped to the 3-counter vector.
* ledger     ops   : generate / discharge operations on three ids A, B, C with the u64 bound; first error stops the run.

Scope: the listed finite cases and a three-id alphabet; Genesis events / S(n) maps are NOT shown to be monoid morphisms.
Exact integers only.  AuthorityEffect: None.
"""
from itertools import permutations, product

U64 = 2 ** 64 - 1
CASES = [
    ['laws', 1, 5], ['laws', 2, 3], ['laws', 3, 3], ['laws', 3, 4],
    ['bounded', 1, 6], ['bounded', 2, 5], ['bounded', 3, 3],
    ['saturating', 3], ['saturating', 6],
    ['events', '-'], ['events', 'D'], ['events', 'A'], ['events', 'R'], ['events', 'I'], ['events', 'DA'], ['events', 'AD'],
    ['events', 'DAR'], ['events', 'DARI'], ['events', 'RI'], ['events', 'IR'], ['events', 'DDAA'], ['events', 'ADDA'],
    ['ledger', '-'],
    ['ledger', 'g:A:2,d:A:1,d:A:1'],
    ['ledger', 'g:A:2,g:B:1,d:A:2,d:B:1'],
    ['ledger', 'd:A:1'],
    ['ledger', 'd:A:0'],
    ['ledger', 'g:A:2,d:A:3'],
    ['ledger', 'g:A:2,d:A:2,d:A:1'],
    ['ledger', 'g:A:0,d:A:1'],
    ['ledger', 'g:C:18446744073709551615,g:C:1'],
    ['ledger', 'g:C:18446744073709551615,g:B:5,d:C:18446744073709551615'],
    ['ledger', 'g:A:18446744073709551615,d:A:18446744073709551615'],
    ['ledger', 'g:A:1,g:B:2,g:A:4,d:B:1,d:A:5,d:C:1,g:C:1'],
]

LETTER = {'D': (1, 0, 0), 'A': (0, 1, 0), 'R': (0, 0, 1), 'I': (0, 0, 1)}


def vadd(x, y):
    return tuple(a + b for a, b in zip(x, y))


def box(k, n):
    return list(product(range(n), repeat=k))


def laws(k, n):
    els = box(k, n)
    zero = (0,) * k
    assoc = comm = unit = cancel = 0
    for x in els:
        unit += (vadd(x, zero) != x) + (vadd(zero, x) != x)
        for y in els:
            comm += vadd(x, y) != vadd(y, x)
            for z in els:
                assoc += vadd(vadd(x, y), z) != vadd(x, vadd(y, z))
                cancel += (vadd(x, z) == vadd(y, z)) and (x != y)
    invertible = sum(1 for x in els if x != zero and any(vadd(x, y) == zero for y in els))
    return {'kind': 'laws', 'args': [k, n], 'elements': len(els), 'triples': len(els) ** 3, 'assoc_failures': assoc,
            'comm_failures': comm, 'unit_failures': unit, 'cancel_failures': cancel, 'invertible_nonzero': invertible}


def combine_bounded(x, y, bound):
    s = vadd(x, y)
    return s if all(c <= bound for c in s) else None


def bounded(k, m):
    els = box(k, m + 1)
    pairs = len(els) ** 2
    defined = sum(1 for x in els for y in els if combine_bounded(x, y, m) is not None)
    triples = defined_triples = def_mismatch = val_mismatch = 0
    for x in els:
        for y in els:
            xy = combine_bounded(x, y, m)
            for z in els:
                triples += 1
                left = combine_bounded(xy, z, m) if xy is not None else None
                yz = combine_bounded(y, z, m)
                right = combine_bounded(x, yz, m) if yz is not None else None
                defined_triples += left is not None
                def_mismatch += (left is None) != (right is None)
                val_mismatch += (left is not None and right is not None and left != right)
    return {'kind': 'bounded', 'args': [k, m], 'elements': len(els), 'pairs': pairs, 'defined_pairs': defined,
            'overflow_pairs': pairs - defined, 'triples': triples, 'defined_triples': defined_triples,
            'definedness_mismatch': def_mismatch, 'value_mismatch': val_mismatch}


def saturating(cap):
    def op(a, b):
        return min(a + b, cap)
    els = range(cap + 1)
    assoc = comm = unit = cancel = 0
    for x in els:
        unit += (op(x, 0) != x) + (op(0, x) != x)
        for y in els:
            comm += op(x, y) != op(y, x)
            for z in els:
                assoc += op(op(x, y), z) != op(x, op(y, z))
                cancel += (op(x, z) == op(y, z)) and (x != y)
    return {'kind': 'saturating', 'args': [cap], 'elements': cap + 1, 'triples': (cap + 1) ** 3, 'assoc_failures': assoc,
            'comm_failures': comm, 'unit_failures': unit, 'cancel_failures': cancel}


def trace(word):
    v = (0, 0, 0)
    for ch in word:
        v = vadd(v, LETTER[ch])
    return v


def events(arg):
    word = '' if arg == '-' else arg
    t = trace(word)
    split_failures = sum(1 for cut in range(len(word) + 1) if vadd(trace(word[:cut]), trace(word[cut:])) != t)
    perms = set(permutations(word))
    perm_failures = sum(1 for p in perms if trace(p) != t)
    seen_declare = False
    ordered = False
    for ch in word:
        if ch == 'D':
            seen_declare = True
        elif ch == 'A' and seen_declare:
            ordered = True
    return {'kind': 'events', 'args': [arg], 'terms': t[0], 'assertions': t[1], 'destructive': t[2], 'cost': sum(t),
            'length': len(word), 'valid_fresh': t[0] >= 1 and t[1] >= 1, 'declare_then_assert': ordered,
            'perm_count': len(perms), 'perm_trace_failures': perm_failures, 'split_failures': split_failures}


def parse_ops(arg):
    if arg == '-':
        return []
    out = []
    for item in arg.split(','):
        kind, name, count = item.split(':')
        out.append((kind, 'ABC'.index(name), int(count)))
    return out


def ledger(arg):
    gen, dis = [0, 0, 0], [0, 0, 0]
    status, fail = 'ok', -1
    for idx, (kind, i, count) in enumerate(parse_ops(arg)):
        if kind == 'g':
            if gen[i] + count > U64:
                status, fail = 'CountOverflow', idx
                break
            gen[i] += count
        else:
            if count == 0:
                continue
            if gen[i] == 0:
                status, fail = 'NeverGenerated', idx
                break
            if count > gen[i] - dis[i]:
                status, fail = 'OverDischarge', idx
                break
            dis[i] += count
    out = [g - d for g, d in zip(gen, dis)]
    return {'kind': 'ledger', 'args': [arg], 'status': status, 'fail_index': fail, 'generated': gen, 'discharged': dis,
            'outstanding': out, 'settled': all(o == 0 for o in out)}


MAKERS = {'laws': laws, 'bounded': bounded, 'saturating': saturating, 'events': events, 'ledger': ledger}
FIELDS = {
    'laws': ['elements', 'triples', 'assoc_failures', 'comm_failures', 'unit_failures', 'cancel_failures', 'invertible_nonzero'],
    'bounded': ['elements', 'pairs', 'defined_pairs', 'overflow_pairs', 'triples', 'defined_triples', 'definedness_mismatch', 'value_mismatch'],
    'saturating': ['elements', 'triples', 'assoc_failures', 'comm_failures', 'unit_failures', 'cancel_failures'],
    'events': ['terms', 'assertions', 'destructive', 'cost', 'length', 'valid_fresh', 'declare_then_assert', 'perm_count',
               'perm_trace_failures', 'split_failures'],
    'ledger': ['status', 'fail_index', 'generated', 'discharged', 'outstanding', 'settled'],
}


def certificate(cases=CASES):
    return {'records': [MAKERS[c[0]](*c[1:]) for c in cases]}


def render(value):
    if isinstance(value, bool):
        return str(int(value))
    if isinstance(value, list):
        return ','.join(str(x) for x in value)
    return str(value)


def wire_lines(data):
    return ['\t'.join([r['kind']] + [str(a) for a in r['args']] + [render(r[f]) for f in FIELDS[r['kind']]])
            for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('\t'.join(str(x) for x in c) + '\n' for c in cases)
