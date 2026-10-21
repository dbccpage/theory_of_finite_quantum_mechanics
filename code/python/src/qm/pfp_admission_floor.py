"""Admission floor: exhaustive tables of relations, cuts, laws and identifications on small carriers.

Producer for PFP batch 01, node PG-ADMISSION-FLOOR.  A relation on Fin n is a bitmask (bit i*n+j = R(i, j)).
`classify` rows enumerate every relation on n = 0..4 points and every marked pair (a, b); `identify` rows
enumerate, for n = 1..3, every irreflexive relation R, every map q : Fin n -> Fin n and every irreflexive
target T on Fin n, to test "q carries R into a law-bearing T".  Exact integers only.
Scope: the listed carrier sizes; the law is supplied data and is not derived from distinctness.
AuthorityEffect: None.
"""
from itertools import product

CASES = [('classify', 0), ('classify', 1), ('classify', 2), ('classify', 3), ('classify', 4),
         ('identify', 1), ('identify', 2), ('identify', 3)]


def bit(mask, n, i, j):
    return (mask >> (i * n + j)) & 1


def irreflexive(mask, n):
    return all(not bit(mask, n, i, i) for i in range(n))


def classify(n):
    rel = law = cuts = triples = inst_no_law = law_no_inst = 0
    quad = {'related_equal': 0, 'related_distinct': 0, 'unrelated_equal': 0, 'unrelated_distinct': 0}
    irreflexive_related_equal = 0
    for mask in range(1 << (n * n)):
        rel += 1
        lawful = irreflexive(mask, n)
        nonempty = mask != 0
        law += lawful
        cuts += lawful and nonempty
        inst_no_law += nonempty and not lawful
        law_no_inst += lawful and not nonempty
        for a in range(n):
            for b in range(n):
                related = bit(mask, n, a, b)
                key = ('related' if related else 'unrelated') + ('_equal' if a == b else '_distinct')
                quad[key] += 1
                if lawful and related:
                    triples += 1
                    if a == b:
                        irreflexive_related_equal += 1
    return {'kind': 'classify', 'n': n, 'relations': rel, 'law_bearing': law, 'cut_relations': cuts, 'cut_triples': triples,
            'instance_without_law': inst_no_law, 'law_without_instance': law_no_inst,
            'related_equal': quad['related_equal'], 'related_distinct': quad['related_distinct'],
            'unrelated_equal': quad['unrelated_equal'], 'unrelated_distinct': quad['unrelated_distinct'],
            'irreflexive_related_equal': irreflexive_related_equal}


def identify(n):
    lawful_masks = [m for m in range(1 << (n * n)) if irreflexive(m, n)]
    rq = with_target = identifying = overlap = cut_q = cut_with_target = cut_ident = cut_ident_with_target = 0
    for q in product(range(n), repeat=n):
        for R in lawful_masks:
            related = [(a, b) for a in range(n) for b in range(n) if bit(R, n, a, b)]
            has_target = any(all(bit(T, n, q[a], q[b]) for a, b in related) for T in lawful_masks)
            ident = any(q[a] == q[b] for a, b in related)
            rq += 1
            with_target += has_target
            identifying += ident
            overlap += has_target and ident
            for a, b in related:
                cut_q += 1
                cut_with_target += has_target
                cut_ident += q[a] == q[b]
                cut_ident_with_target += has_target and q[a] == q[b]
    return {'kind': 'identify', 'n': n, 'rq_pairs': rq, 'rq_with_target': with_target, 'rq_identifying': identifying,
            'rq_overlap': overlap, 'cut_q': cut_q, 'cut_q_with_target': cut_with_target,
            'cut_q_identified': cut_ident, 'cut_q_identified_with_target': cut_ident_with_target}


CLASSIFY_FIELDS = ['relations', 'law_bearing', 'cut_relations', 'cut_triples', 'instance_without_law', 'law_without_instance',
                   'related_equal', 'related_distinct', 'unrelated_equal', 'unrelated_distinct', 'irreflexive_related_equal']
IDENTIFY_FIELDS = ['rq_pairs', 'rq_with_target', 'rq_identifying', 'rq_overlap', 'cut_q', 'cut_q_with_target',
                   'cut_q_identified', 'cut_q_identified_with_target']


def certificate(cases=CASES):
    return {'records': [classify(n) if kind == 'classify' else identify(n) for kind, n in cases]}


def wire_lines(data):
    out = []
    for r in data['records']:
        fields = CLASSIFY_FIELDS if r['kind'] == 'classify' else IDENTIFY_FIELDS
        out.append('\t'.join([r['kind'], str(r['n'])] + [str(r[f]) for f in fields]))
    return out


def public_tsv(cases=CASES):
    return ''.join('%s\t%d\n' % c for c in cases)
