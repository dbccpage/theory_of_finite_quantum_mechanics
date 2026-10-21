"""Symmetry price of selecting a point on an n-point set: invariant points and the minimal-input frontier.

Producer for PFP batch 01, node PG-WDP-PROTECTED-QUESTIONS. Exact integers only (subsets of {0..n-1} are bit masks).
Model (a MODELLING CHOICE, narrower than WDP-CH03-D01): a declared input set S is fixed pointwise; a point x is
invariant under S when every permutation fixing S pointwise fixes x; S is selecting when some point is invariant;
the frontier is the family of inclusion-minimal selecting sets. Closed form used here (not an enumeration of
permutations): inv(S) = S, plus the complement of S when it is a single point.
Symmetry-price bookkeeping only. AuthorityEffect: None.
"""

CASES = [0, 1, 2, 3, 4, 5, 6]  # replay bound n <= 6 (at most 720 permutations x 64 subsets); not part of the Lean claim


def popcount(x):
    return bin(x).count('1')


def invariant_mask(n, mask):
    full = (1 << n) - 1
    comp = full & ~mask
    return mask | comp if popcount(comp) == 1 else mask


def is_minimal(n, mask):
    """Closed form of 'selecting with no selecting proper subset'."""
    if n == 0:
        return False
    if n == 1:
        return mask == 0
    return popcount(mask) == 1


def record(n):
    table = []
    for mask in range(1 << n):
        inv = invariant_mask(n, mask)
        table.append([mask, inv, inv != 0, is_minimal(n, mask)])
    selecting = [t[0] for t in table if t[2]]
    frontier = [t[0] for t in table if t[3]]
    return {
        'n': n,
        'selecting_count': len(selecting),
        'frontier': frontier,
        'frontier_size': len(frontier),
        'min_price': min(popcount(m) for m in selecting) if selecting else None,
        'table': table,
    }


def certificate(cases=CASES):
    return {'records': [record(n) for n in cases]}


def wire_lines(data):
    out = []
    for r in data['records']:
        front = ';'.join(str(m) for m in r['frontier']) or '-'
        table = ';'.join('%d:%d:%d:%d' % (t[0], t[1], int(t[2]), int(t[3])) for t in r['table'])
        out.append('\t'.join(['sel', str(r['n']), str(r['selecting_count']), str(r['frontier_size']), '-' if r['min_price'] is None else str(r['min_price']), front, table]))
    return out


def public_tsv(cases=CASES):
    return ''.join('sel\t%d\n' % n for n in cases)
