"""L1 residual minimizers on the n-cycle and the (non-)determination of sector weights.

Producer for PFP batch 01, node L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED. Exact integers and Fractions only.
Model: an integer edge cochain c on the n-cycle, the class of c in C^1 / im d0 (invariant: the holonomy
S = sum c, which is how Gamma2 is MODELLED here), the L1 form, Phi1(c) = min over the class, and the set of
minimizing residuals. Three record kinds:
  residual  unweighted (equal edge masses): Phi1 = |S|, minimizers = cochains with sum S whose entries all have the
            sign of S (a scaled simplex), sector weights = block sums of |r_i|, the cyclically invariant minimizer |S|/n,
            and the min / max of sum r_i^2 over the minimizers (Gamma2 read as a sum of squares is NOT constant on them);
  weighted  declared positive integer edge masses m_i, form sum m_i |r_i|: minimizers are the sign-definite cochains
            supported on the edges of minimal mass (a face of the simplex, a single point when the minimum is attained
            once, so the sector weights can then be determined by the masses themselves);
  twocycle  two disjoint cycles (cycle rank 2): the class is the pair of holonomies and Phi1 = |S1| + |S2|, which a
            single total holonomy does not determine.
Not a statement about graphs of other shape, the Hilbert lift or physics. AuthorityEffect: None.
"""
from fractions import Fraction
from math import comb

CASES = [
    ['residual', 4, [1, 0, 1, 0], [2, 2]],
    ['residual', 4, [0, 1, 0, 1], [1, 1, 1, 1]],
    ['residual', 4, [1, 0, 0, 0], [2, 2]],
    ['residual', 4, [3, -1, -1, 0], [2, 2]],
    ['residual', 4, [1, 1, 0, 0], [4]],
    ['residual', 3, [1, 1, 1], [1, 2]],
    ['residual', 4, [-2, 0, -1, 0], [2, 2]],
    ['residual', 4, [1, -1, 0, 0], [2, 2]],
    ['residual', 2, [0, 0], [1, 1]],
    ['residual', 1, [5], [1]],
    ['residual', 5, [1, 0, 0, 0, 1], [2, 3]],
    ['residual', 2, [3, 0], [1, 1]],
    ['residual', 6, [1, 0, 0, 0, 0, 0], [3, 3]],
    ['residual', 4, [4, 0, 0, 0], [2, 2]],
    ['residual', 3, [2, -3, 0], [1, 1, 1]],
    ['residual', 5, [0, 0, 0, 0, 0], [5]],
    ['weighted', 4, [1, 0, 1, 0], [2, 2], [1, 1, 1, 1]],
    ['weighted', 4, [1, 0, 1, 0], [2, 2], [1, 2, 3, 4]],
    ['weighted', 4, [1, 0, 1, 0], [2, 2], [2, 1, 1, 3]],
    ['weighted', 3, [2, -3, 0], [1, 2], [5, 2, 2]],
    ['weighted', 4, [1, -1, 0, 0], [2, 2], [1, 2, 3, 4]],
    ['weighted', 4, [3, 0, 0, 0], [2, 2], [2, 2, 1, 1]],
    ['twocycle', 3, [1, 0, 0], 3, [1, 0, 0]],
    ['twocycle', 3, [2, 0, 0], 3, [-1, 0, 0]],
    ['twocycle', 2, [1, -1], 2, [0, 0]],
    ['twocycle', 3, [1, 1, 0], 2, [-1, 0]],
]


def weak_compositions(total, parts):
    """All tuples of `parts` nonnegative integers summing to `total`, in ascending lexicographic order."""
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, parts - 1):
            yield (first,) + rest


def _blocks(sizes):
    cuts, acc = [], 0
    for s in sizes:
        cuts.append((acc, acc + s))
        acc += s
    return cuts


def record_residual(n, c, sizes):
    assert len(c) == n and sum(sizes) == n and all(s >= 1 for s in sizes)
    S = sum(c)
    M = abs(S)
    if S >= 0:
        lex_min, lex_max = [0] * (n - 1) + [M], [M] + [0] * (n - 1)
    else:
        lex_min, lex_max = [-M] + [0] * (n - 1), [0] * (n - 1) + [-M]
    vecs = [list(v) for v in weak_compositions(M, len(sizes))]
    sym = Fraction(M, n)
    q, r = divmod(M, n)
    return {
        'kind': 'residual',
        'input': ['residual', n, list(c), list(sizes)],
        'holonomy': S,
        'phi1': M,
        'minimizer_count': comb(M + n - 1, n - 1),
        'lex_min': lex_min,
        'lex_max': lex_max,
        'sector_vectors': vecs,
        'determined': len(vecs) == 1,
        'unique': comb(M + n - 1, n - 1) == 1,
        'symmetric': [sym.numerator, sym.denominator],
        'symmetric_integral': sym.denominator == 1,
        'sumsq_min': r * (q + 1) ** 2 + (n - r) * q * q,
        'sumsq_max': M * M,
        'status': 'zero_mass_refused' if M == 0 else 'ok',
    }


def record_weighted(n, c, sizes, masses):
    assert len(c) == n and len(masses) == n and sum(sizes) == n and all(s >= 1 for s in sizes) and all(m >= 1 for m in masses)
    S = sum(c)
    M = abs(S)
    mmin = min(masses)
    E = [i for i in range(n) if masses[i] == mmin]
    k = len(E)
    sign = 1 if S >= 0 else -1
    lo, hi = (E[-1], E[0]) if S >= 0 else (E[0], E[-1])
    lex_min = [sign * M if i == lo else 0 for i in range(n)]
    lex_max = [sign * M if i == hi else 0 for i in range(n)]
    blocks = _blocks(sizes)
    vecs = set()
    for comp in weak_compositions(M, k):
        w = [0] * n
        for pos, val in zip(E, comp):
            w[pos] = val
        vecs.add(tuple(sum(w[a:b]) for a, b in blocks))
    vecs = [list(v) for v in sorted(vecs)]
    count = comb(M + k - 1, k - 1)
    return {
        'kind': 'weighted',
        'input': ['weighted', n, list(c), list(sizes), list(masses)],
        'holonomy': S,
        'weighted_phi1': M * mmin,
        'minimizer_count': count,
        'lex_min': lex_min,
        'lex_max': lex_max,
        'sector_vectors': vecs,
        'determined': len(vecs) == 1,
        'unique': count == 1,
        'status': 'zero_mass_refused' if M == 0 else 'ok',
    }


def record_twocycle(n1, c1, n2, c2):
    S1, S2 = sum(c1), sum(c2)
    phi1 = abs(S1) + abs(S2)
    return {
        'kind': 'twocycle',
        'input': ['twocycle', n1, list(c1), n2, list(c2)],
        'holonomies': [S1, S2],
        'phi1': phi1,
        'minimizer_count': comb(abs(S1) + n1 - 1, n1 - 1) * comb(abs(S2) + n2 - 1, n2 - 1),
        'total_holonomy': S1 + S2,
        'total_gives_phi1': abs(S1 + S2) == phi1,
    }


def record(case):
    kind = case[0]
    if kind == 'residual':
        return record_residual(*case[1:])
    if kind == 'weighted':
        return record_weighted(*case[1:])
    return record_twocycle(*case[1:])


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def _ints(xs):
    return ','.join(str(x) for x in xs)


def wire_lines(data):
    out = []
    for r in data['records']:
        i = r['input']
        if r['kind'] == 'residual':
            vecs = ';'.join(_ints(v) for v in r['sector_vectors'])
            out.append('\t'.join([
                'residual', str(i[1]), _ints(i[2]), _ints(i[3]), str(r['holonomy']), str(r['phi1']), str(r['minimizer_count']),
                _ints(r['lex_min']), _ints(r['lex_max']), vecs, str(int(r['determined'])), str(int(r['unique'])),
                '%d/%d' % tuple(r['symmetric']), str(int(r['symmetric_integral'])), str(r['sumsq_min']), str(r['sumsq_max']), r['status']]))
        elif r['kind'] == 'weighted':
            vecs = ';'.join(_ints(v) for v in r['sector_vectors'])
            out.append('\t'.join([
                'weighted', str(i[1]), _ints(i[2]), _ints(i[3]), _ints(i[4]), str(r['holonomy']), str(r['weighted_phi1']),
                str(r['minimizer_count']), _ints(r['lex_min']), _ints(r['lex_max']), vecs, str(int(r['determined'])),
                str(int(r['unique'])), r['status']]))
        else:
            out.append('\t'.join([
                'twocycle', str(i[1]), _ints(i[2]), str(i[3]), _ints(i[4]), _ints(r['holonomies']), str(r['phi1']),
                str(r['minimizer_count']), str(r['total_holonomy']), str(int(r['total_gives_phi1']))]))
    return out


def public_tsv(cases=CASES):
    out = []
    for c in cases:
        if c[0] == 'residual':
            out.append('residual\t%d\t%s\t%s\n' % (c[1], _ints(c[2]), _ints(c[3])))
        elif c[0] == 'weighted':
            out.append('weighted\t%d\t%s\t%s\t%s\n' % (c[1], _ints(c[2]), _ints(c[3]), _ints(c[4])))
        else:
            out.append('twocycle\t%d\t%s\t%d\t%s\n' % (c[1], _ints(c[2]), c[3], _ints(c[4])))
    return ''.join(out)
