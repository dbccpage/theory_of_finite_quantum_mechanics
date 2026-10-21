"""The root coproduct Real_0 = PrimitiveDifference + Structure: exhaustive counts on small finite channels.

Producer for PFP batch 01, node PG-ROOT-DIFF-STRUCTURE (an ADMITTED PRIMITIVE). Exact integers only; no random numbers.
Channels are sets {0..a-1} and {0..b-1}; the coproduct is the set of tagged elements. The tables verify the
coproduct property (disjoint injections, universal property, count of maps out = product of counts) and show that
the construction is neutral about the two posits (retractions exist or not depending only on emptiness).
They do not derive either channel or any reduction. AuthorityEffect: None.
"""
from itertools import product

CASES = ([['maps', a, b, c] for a in range(3) for b in range(3) for c in range(4)]
         + [['maps', 3, 2, 2], ['maps', 2, 3, 2]]
         + [['reduction', a, b] for a in range(4) for b in range(4)]
         + [['posit', a, b] for a in range(2) for b in range(2)])


def coproduct(a, b):
    """Elements of the coproduct as tagged pairs; position of an element is its index in this list."""
    return [('pd', i) for i in range(a)] + [('st', j) for j in range(b)]


def maps_record(a, b, c):
    cop = coproduct(a, b)
    inl = [cop.index(('pd', i)) for i in range(a)]
    inr = [cop.index(('st', j)) for j in range(b)]
    total = 0
    pair_counts = {}
    for h in product(range(c), repeat=a + b):
        total += 1
        key = (tuple(h[i] for i in inl), tuple(h[i] for i in inr))
        pair_counts[key] = pair_counts.get(key, 0) + 1
    left = sum(1 for _ in product(range(c), repeat=a))
    right = sum(1 for _ in product(range(c), repeat=b))
    return {'kind': 'maps', 'a': a, 'b': b, 'c': c, 'total_maps': total, 'left_maps': left, 'right_maps': right,
            'product_matches': total == left * right,
            'unique_copairs': sum(1 for v in pair_counts.values() if v == 1),
            'inl_injective': len(set(inl)) == a, 'inr_injective': len(set(inr)) == b,
            'disjoint': not (set(inl) & set(inr)), 'covering': len(set(inl) | set(inr)) == len(cop)}


def reduction_record(a, b):
    cop = coproduct(a, b)
    retr_a = sum(1 for h in product(range(a), repeat=a + b) if all(h[cop.index(('pd', i))] == i for i in range(a)))
    retr_b = sum(1 for h in product(range(b), repeat=a + b) if all(h[cop.index(('st', j))] == j for j in range(b)))
    return {'kind': 'reduction', 'a': a, 'b': b, 'maps_b_to_a': sum(1 for _ in product(range(a), repeat=b)),
            'maps_a_to_b': sum(1 for _ in product(range(b), repeat=a)), 'retractions_to_pd': retr_a, 'retractions_to_s': retr_b,
            'exists_to_pd': retr_a > 0, 'exists_to_s': retr_b > 0}


def posit_record(a, b):
    cop = coproduct(a, b)
    return {'kind': 'posit', 'a': a, 'b': b, 'nonempty_pd': a > 0, 'nonempty_s': b > 0, 'coproduct_size': len(cop),
            'nonempty_real0': len(cop) > 0, 'real0_nonempty_iff_a_channel_is': (len(cop) > 0) == (a > 0 or b > 0)}


def record(case):
    kind = case[0]
    if kind == 'maps':
        return maps_record(case[1], case[2], case[3])
    if kind == 'reduction':
        return reduction_record(case[1], case[2])
    if kind == 'posit':
        return posit_record(case[1], case[2])
    raise ValueError('unknown case kind ' + str(kind))


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def _line(r):
    k = r['kind']
    if k == 'maps':
        return '\t'.join(['maps', str(r['a']), str(r['b']), str(r['c']), str(r['total_maps']), str(r['left_maps']), str(r['right_maps']),
                          str(int(r['product_matches'])), str(r['unique_copairs']), str(int(r['inl_injective'])),
                          str(int(r['inr_injective'])), str(int(r['disjoint'])), str(int(r['covering']))])
    if k == 'reduction':
        return '\t'.join(['reduction', str(r['a']), str(r['b']), str(r['maps_b_to_a']), str(r['maps_a_to_b']), str(r['retractions_to_pd']),
                          str(r['retractions_to_s']), str(int(r['exists_to_pd'])), str(int(r['exists_to_s']))])
    return '\t'.join(['posit', str(r['a']), str(r['b']), str(int(r['nonempty_pd'])), str(int(r['nonempty_s'])), str(r['coproduct_size']),
                      str(int(r['nonempty_real0'])), str(int(r['real0_nonempty_iff_a_channel_is']))])


def wire_lines(data):
    return [_line(r) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('\t'.join(str(x) for x in c) + '\n' for c in cases)
