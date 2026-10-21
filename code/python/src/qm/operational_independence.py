"""Exact finite controls for the compositional independence theorem.
The universal scope is in Lean; fixtures through four atoms are finite checks.
"""
from fractions import Fraction as Q
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys

_spec = importlib.util.spec_from_file_location('independence_algebra', Path(__file__).with_name('operational_tomography.py'))
a = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a)
PREMISES = (
    'finite nonempty carriers with a declared involutive symmetry',
    'real invariant state vectors with coordinatewise positivity and sum normalization',
    'all nonnegative equivariant matrices are processes; events have column sums at most one',
    'parallel composition uses the diagonal symmetry on the Cartesian product',
    'finite instruments have total column sum one and transformations retain ancillary distinctions',
    'this package does not assume purification, local complex quantum structure or primitive selection',
)


def require(ok, code):
    if not ok:
        raise ValueError(code)


def involution(f, n):
    require(type(f) is list and len(f) == n and all(type(x) is int for x in f), 'FLIP_TYPE')
    require(sorted(f) == list(range(n)) and all(f[f[x]] == x for x in range(n)), 'INVOLUTION')


def validate_event(t, input_flip, output_flip, channel=False):
    t = a.exact_matrix(t)
    n, m = len(t[0]), len(t)
    involution(input_flip, n)
    involution(output_flip, m)
    require(all(t[y][x] >= 0 and t[output_flip[y]][input_flip[x]] == t[y][x]
                for y in range(m) for x in range(n)), 'POSITIVE_EQUIVARIANT')
    sums = [sum(t[y][x] for y in range(m)) for x in range(n)]
    require(all(s == 1 if channel else s <= 1 for s in sums), 'COLUMN_BOUND')
    return t


def tensor(t, s):
    t, s = a.exact_matrix(t), a.exact_matrix(s)
    return [[t[y][x]*s[b][v] for x in range(len(t[0])) for v in range(len(s[0]))]
            for y in range(len(t)) for b in range(len(s))]


def combined_flip(f, g):
    return [f[x]*len(g)+g[y] for x in range(len(f)) for y in range(len(g))]


def vector(v, n):
    return a.parse_matrix([v], 1, n)[0]


def pairing(e, p):
    return sum(x*y for x,y in zip(e,p))


def verify(raw):
    require(len(raw) < 1_000_000, 'SIZE_LIMIT')
    c = json.loads(raw, object_pairs_hook=a.no_duplicates)
    require(type(c) is dict and set(c) == {'schema','authority_effect','premises','systems','channels','instrument','hidden_states'}, 'ENVELOPE')
    require(c['schema'] == 'operational-independence.v1' and c['authority_effect'] == 'None', 'SCOPE')
    require(c['premises'] == list(PREMISES), 'PREMISES')
    require(type(c['systems']) is list and len(c['systems']) == 5, 'SYSTEM_COVERAGE')
    reports = []
    for n, s in enumerate(c['systems']):
        require(type(s) is dict and set(s) == {'atoms','points','flip','orbits','observe','prepare'}, 'SYSTEM_FIELDS')
        require(type(s['atoms']) is int and s['atoms'] == n and type(s['points']) is int and s['points'] == 4**n, 'DIMENSION')
        points = list(itertools.product(range(4), repeat=n))
        index = {p:i for i,p in enumerate(points)}
        f = [index[tuple(d ^ 1 for d in p)] for p in points]
        involution(s['flip'], len(points))
        require(s['flip'] == f, 'DIAGONAL_ACTION')
        orbits = [sorted({i, f[i]}) for i in range(len(points)) if i <= f[i]]
        require(type(s['orbits']) is list and all(type(o) is list and all(type(x) is int for x in o) for o in s['orbits']), 'ORBIT_TYPES')
        require(s['orbits'] == orbits, 'ORBIT_COVERAGE')
        def visible(i):
            bits = tuple(d//2 for d in points[i])
            return sum(b*2**(n-j-1) for j,b in enumerate(bits))
        k, d = len(orbits), 2**n
        m = a.parse_matrix(s['observe'], d, k)
        r = a.parse_matrix(s['prepare'], k, d)
        expected_m = [[Q(visible(o[0]) == j) for o in orbits] for j in range(d)]
        counts = [sum(visible(o[0]) == j for o in orbits) for j in range(d)]
        expected_r = [[Q(visible(o[0]) == j, counts[j]) for j in range(d)] for o in orbits]
        require(m == expected_m and r == expected_r, 'PRODUCT_COORDINATES')
        require(a.multiply(m,r) == a.identity(d), 'CALIBRATION')
        require(a.rank(m) == d and k == (1 if n == 0 else 2**(2*n-1)), 'RANK')
        reports.append({'atoms':n,'state_dimension':k,'product_dimension':d,'hidden_dimension':k-d})
    require(type(c['channels']) is dict and set(c['channels']) == {'identity','flag_flip','visible_flip','noise'}, 'CHANNEL_COVERAGE')
    f = [1,0,3,2]
    for name, permutation in [('identity',[0,1,2,3]),('flag_flip',f),('visible_flip',[2,3,0,1]),('noise',None)]:
        t = validate_event(a.parse_matrix(c['channels'][name],4,4),f,f,True)
        want = [[Q(1,4) if permutation is None else Q(y == permutation[x]) for x in range(4)] for y in range(4)]
        require(t == want, 'CHANNEL_MODEL')
    require(type(c['instrument']) is list and len(c['instrument']) == 2, 'INSTRUMENT_COVERAGE')
    ts = [validate_event(a.parse_matrix(t,4,4),f,f) for t in c['instrument']]
    require(all(ts[j] == [[Q(y == x and x//2 == j) for x in range(4)] for y in range(4)] for j in range(2)), 'INSTRUMENT_MODEL')
    require(all(sum(t[y][x] for t in ts for y in range(4)) == 1 for x in range(4)), 'INSTRUMENT_NORMALIZATION')
    w = c['hidden_states']
    require(type(w) is dict and set(w) == {'rho','sigma','effect'}, 'WITNESS_FIELDS')
    rho, sigma, effect = [vector(w[k],16) for k in ('rho','sigma','effect')]
    for name,p in [('rho',rho),('sigma',sigma)]:
        want = [Q(1,2) if x in ([0,5] if name == 'rho' else [1,4]) else Q(0) for x in range(16)]
        require(p == want and sum(p) == 1 and all(x >= 0 for x in p), 'HIDDEN_STATE')
        ff = combined_flip(f,f)
        require(all(p[ff[x]] == p[x] for x in range(16)), 'STATE_INVARIANCE')
    require(effect == [Q((x//4)%2 == x%2) for x in range(16)], 'GLOBAL_EFFECT')
    require(pairing(effect,rho) == 1 and pairing(effect,sigma) == 0, 'GLOBAL_SEPARATION')
    for i,j in itertools.product(range(2),repeat=2):
        e = [Q((x//4)//2 == i and (x%4)//2 == j) for x in range(16)]
        require(pairing(e,rho) == pairing(e,sigma), 'PRODUCT_INVISIBILITY')
    return {'all_passed':True,'authority_effect':'None','candidate_sha256':hashlib.sha256(raw).hexdigest(),
        'systems':reports,'witness':{'global_rho':'1','global_sigma':'0','all_product_basis_tests_agree':True},
        'scope':'finite exact controls only; unrestricted finite-system laws and independence are Lean theorems'}


if __name__ == '__main__':
    print(json.dumps(verify(Path(sys.argv[1]).read_bytes()),indent=2))
