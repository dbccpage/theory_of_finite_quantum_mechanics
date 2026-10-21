"""Exhaustive census of lifts u : A -> B with typed recoveries r : B -> A + {refusal} on the old image.

Producer for PFP batch 01, node PG-OLD-IMAGE-INJECTIVE. Exact integers only. For each (|A|, |B|, |O|) every pair (u, r)
is enumerated (|B|^|A| lifts, (|A|+1)^|B| recoveries, index |A| meaning the refusal summand). A pair satisfies the
old-image law when r(u(a)) = a for every a. Per case the record counts: all pairs; law pairs; law pairs whose lift is
not injective (the injectivity theorem says none); law pairs that also refuse every off-image point (the domain
restriction) and those that do not (off-image rejection is not implied); injective lifts; and, over law pairs, the
(observation q: A -> O, q': B -> O) pairs, how many preserve observations (q' composed with u equals q), and the
(obstruction oA: A -> Bool, oB: B -> Bool) pairs in which an old obstruction persists through the lift or is cleared.
Scope: finite sets and functions; not a statement about S(n), repair of any engine obstruction, or physics.
AuthorityEffect: None.
"""
from itertools import product

CASES = [[0, 0, 2], [0, 3, 2], [1, 1, 2], [1, 2, 2], [2, 2, 2], [2, 3, 2], [2, 2, 3], [3, 3, 2], [3, 2, 2], [3, 4, 2], [4, 4, 2]]

FIELDS = ['pairs_total', 'law', 'law_noninjective', 'law_refusing', 'law_nonrefusing', 'injective_u',
          'obs_total', 'obs_preserved', 'persists', 'cleared']


def record(a, b, o):
    pairs = law = law_noninj = law_refusing = injective = 0
    obs_total = obs_pres = persists = cleared = 0
    for u in product(range(b), repeat=a):
        is_inj = len(set(u)) == a
        injective += 1 if is_inj else 0
        image = set(u)
        for r in product(range(a + 1), repeat=b):
            pairs += 1
            if not all(r[u[x]] == x for x in range(a)):
                continue
            law += 1
            if not is_inj:
                law_noninj += 1
            if all(r[y] == a for y in range(b) if y not in image):
                law_refusing += 1
            for q in product(range(o), repeat=a):
                for qq in product(range(o), repeat=b):
                    obs_total += 1
                    if all(qq[u[x]] == q[x] for x in range(a)):
                        obs_pres += 1
            for oa in product((0, 1), repeat=a):
                for ob in product((0, 1), repeat=b):
                    hit = any(oa[x] and ob[u[x]] for x in range(a))
                    persists += 1 if hit else 0
                    if any(oa) and not hit:
                        cleared += 1
    vals = [pairs, law, law_noninj, law_refusing, law - law_refusing, injective, obs_total, obs_pres, persists, cleared]
    rec = {'input': [a, b, o]}
    rec.update(dict(zip(FIELDS, vals)))
    return rec


def certificate(cases=CASES):
    return {'records': [record(*c) for c in cases]}


def wire_lines(data):
    return ['\t'.join(['lift'] + [str(x) for x in r['input']] + [str(r[f]) for f in FIELDS]) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('lift\t%d\t%d\t%d\n' % tuple(c) for c in cases)
