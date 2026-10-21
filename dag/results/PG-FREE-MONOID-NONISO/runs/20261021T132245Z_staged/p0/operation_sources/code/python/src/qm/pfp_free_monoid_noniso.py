"""Free monoids on alphabets of different sizes: exact counts, exhaustive homomorphism search, set bijection.

Producer for PFP batch 01, node PG-FREE-MONOID-NONISO. Exact integers only.
For an alphabet pair (n, m) and a bound d <= 2 on the length of generator images:
  * words of each length <= 4 and the atoms (indecomposable words) among them, by brute force;
  * every monoid homomorphism FreeMonoid(n) -> FreeMonoid(m) whose generator images have length <= d
    (such a homomorphism is determined by the images of the n generators), classified as onto the letters
    (every one-letter word is the image of a word of length <= 2), injective on all words of length <= 2,
    and both ("bijective candidate"), with a check that every candidate is a letter permutation;
  * the pairs of maps Fin n -> Fin m, Fin m -> Fin n that are mutually inverse (the equivalences of the
    discrete categories);
  * the explicit shortlex-rank bijection between the underlying sets on the first 30 words, and the number of
    pairs of words among them on which it fails to be multiplicative.
These are finite instances; the general theorem (arbitrary alphabets) is the Lean module FreeMonoidNoniso.
AuthorityEffect: None.
"""
from itertools import product

CASES = [(0, 0, 2), (0, 1, 2), (1, 0, 2), (1, 1, 2), (1, 2, 2), (2, 1, 2), (2, 2, 2), (2, 3, 2), (3, 2, 2), (3, 3, 2),
         (2, 4, 2), (4, 2, 2), (3, 4, 1), (4, 3, 1), (4, 4, 1)]
MAX_LEN = 4
PREFIX = 30
FIELDS = ['words_n', 'words_m', 'atoms_n', 'atoms_m', 'homs', 'letters_onto', 'injective_bounded', 'bijective_candidates',
          'bijective_not_permutation', 'permutation_homs', 'discrete_equivalences', 'set_bijection', 'homomorphism_violations']


def words_upto(base, max_len):
    out = []
    for k in range(max_len + 1):
        out += list(product(range(base), repeat=k))
    return out


def atoms(base, max_len):
    """Nonempty words of length <= max_len with no split into two nonempty words."""
    found = 0
    for w in words_upto(base, max_len):
        if w and not any(w[:i] and w[i:] for i in range(1, len(w))):
            found += 1
    return found


def rank(word, base):
    """Shortlex rank of a word over `base` letters (base >= 1)."""
    k = len(word)
    if base == 1:
        return k
    value = 0
    for x in word:
        value = value * base + x
    return (base ** k - 1) // (base - 1) + value


def unrank(r, base):
    if base == 1:
        return (0,) * r
    k = 0
    while (base ** (k + 1) - 1) // (base - 1) <= r:
        k += 1
    value = r - (base ** k - 1) // (base - 1)
    digits = []
    for _ in range(k):
        digits.append(value % base)
        value //= base
    return tuple(reversed(digits))


def hom_image(images, word):
    out = ()
    for x in word:
        out += images[x]
    return out


def set_bijection(n, m):
    """(flag, violations): the shortlex-composite map on the first PREFIX words, and its failures of multiplicativity."""
    if n == 0 or m == 0:
        return (1, 0) if n == m else (0, 0)
    first_n = [unrank(i, n) for i in range(PREFIX)]
    first_m = [unrank(i, m) for i in range(PREFIX)]
    phi = {w: first_m[i] for i, w in enumerate(first_n)}
    bijective = len(set(phi.values())) == PREFIX and set(phi.values()) == set(first_m)
    violations = 0
    for u in first_n:
        for v in first_n:
            if unrank(rank(u + v, n), m) != phi[u] + phi[v]:
                violations += 1
    return (int(bijective), violations)


def record(n, m, d):
    assert d <= 2
    images_pool = words_upto(m, d)
    probe = words_upto(n, 2)
    letters = [(b,) for b in range(m)]
    homs = onto = inj = cand = not_perm = perms = 0
    for images in product(images_pool, repeat=n):
        homs += 1
        values = [hom_image(images, w) for w in probe]
        is_onto = all(l in values for l in letters)
        is_inj = len(set(values)) == len(probe)
        onto += is_onto
        inj += is_inj
        is_perm = all(len(g) == 1 for g in images) and len({g for g in images}) == n and n == m
        perms += is_perm
        if is_onto and is_inj:
            cand += 1
            not_perm += not is_perm
    discrete = 0
    for f in product(range(m), repeat=n):
        for g in product(range(n), repeat=m):
            if all(g[f[x]] == x for x in range(n)) and all(f[g[y]] == y for y in range(m)):
                discrete += 1
    flag, violations = set_bijection(n, m)
    return {'input': [n, m, d], 'words_n': [n ** k for k in range(MAX_LEN + 1)], 'words_m': [m ** k for k in range(MAX_LEN + 1)],
            'atoms_n': atoms(n, MAX_LEN), 'atoms_m': atoms(m, MAX_LEN), 'homs': homs, 'letters_onto': onto, 'injective_bounded': inj,
            'bijective_candidates': cand, 'bijective_not_permutation': not_perm, 'permutation_homs': perms,
            'discrete_equivalences': discrete, 'set_bijection': flag, 'homomorphism_violations': violations}


def certificate(cases=CASES):
    return {'records': [record(*c) for c in cases]}


def _cell(value):
    return ':'.join(str(x) for x in value) if isinstance(value, list) else str(value)


def wire_lines(data):
    return ['\t'.join(['monoid'] + [str(x) for x in r['input']] + [_cell(r[f]) for f in FIELDS]) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('monoid\t%d\t%d\t%d\n' % c for c in cases)
