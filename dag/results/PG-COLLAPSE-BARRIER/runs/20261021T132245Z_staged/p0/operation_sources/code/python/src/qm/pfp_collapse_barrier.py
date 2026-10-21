"""Collapsed observation barrier: exhaustive counts of profiles, tasks, factorisations and added tags.

Producer for PFP batch 01, node PG-COLLAPSE-BARRIER.  Carrier X = Fin n, profile p : X -> Fin my,
task s : X -> Fin mz.  For every (p, s) the producer decides by brute force whether some g : Y -> Z
has g . p = s, whether s is constant on the fibres of p, and the least size k >= 0 of an added tag
t : X -> Fin k such that s factors through the refined profile (p, t) : X -> Y x Fin k (k = 0 works exactly when X is
empty; -1 would mean no k up to max(1, n) works and does not occur).
Exact integers only.  Scope: finite carriers of the listed sizes; no physical or selection claim.
AuthorityEffect: None.
"""
from itertools import product

CASES = [(0, 0, 1), (0, 1, 0), (1, 1, 2), (2, 0, 2), (2, 1, 2), (2, 2, 2), (3, 1, 2), (3, 2, 2), (3, 3, 2),
         (3, 2, 3), (4, 2, 2), (4, 2, 3), (4, 1, 4), (4, 3, 3), (5, 2, 2)]


def fibre_constant(p, s):
    seen = {}
    for a, b in zip(p, s):
        if seen.setdefault(a, b) != b:
            return False
    return True


def count_g(codes, codomain, s, zsize):
    """Number of g : codomain -> Z with g(codes[x]) = s[x]: brute force over every g."""
    return sum(1 for g in product(range(zsize), repeat=codomain) if all(g[c] == v for c, v in zip(codes, s)))


def factors_via(codes, codomain, s, zsize):
    return count_g(codes, codomain, s, zsize) > 0


def min_tag(p, s, my, mz, n):
    for k in range(0, max(1, n) + 1):
        for t in product(range(k), repeat=n):
            codes = [a * k + b for a, b in zip(p, t)]
            # g exists iff s is constant on the code fibres and (Z inhabited or every code is hit); this
            # criterion is cross-checked against the g-enumeration of count_g for k = 1 in the tests.
            if fibre_constant(codes, s) and (mz >= 1 or len(set(codes)) == my * k):
                return k
    return -1


def record(n, my, mz):
    total = fc = fac = viol = facs = 0
    hist = {}
    for p in product(range(my), repeat=n):
        for s in product(range(mz), repeat=n):
            total += 1
            const = fibre_constant(p, s)
            fc += const
            cg = count_g(list(p), my, s, mz)
            facs += cg
            f = cg > 0
            fac += f
            viol += (f and not const)
            k = min_tag(p, s, my, mz, n)
            hist[k] = hist.get(k, 0) + 1
    return {'input': [n, my, mz], 'total': total, 'fibre_constant': fc, 'collapsed_separated': total - fc,
            'factoring': fac, 'factorizations': facs, 'violations': viol,
            'min_tag_hist': [[k, hist[k]] for k in sorted(hist)]}


def certificate(cases=CASES):
    return {'records': [record(*c) for c in cases]}


def wire_lines(data):
    out = []
    for r in data['records']:
        hist = ';'.join('%d:%d' % (k, c) for k, c in r['min_tag_hist']) or '-'
        out.append('\t'.join(['tag'] + [str(x) for x in r['input']] + [str(r[k]) for k in (
            'total', 'fibre_constant', 'collapsed_separated', 'factoring', 'factorizations', 'violations')] + [hist]))
    return out


def public_tsv(cases=CASES):
    return ''.join('tag\t%d\t%d\t%d\n' % c for c in cases)
