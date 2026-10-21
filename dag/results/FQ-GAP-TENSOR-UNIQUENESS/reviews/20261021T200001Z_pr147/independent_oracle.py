"""Independent rational determinant and hidden-kernel checks; no builder/checker imports.
Finite controls only. The universal results are Lean theorems with explicit hypotheses.
"""
from fractions import Fraction as Q
import json
from pathlib import Path
import sys


def require(ok, why):
    if not ok:
        raise ValueError(why)


def mul(a, b):
    require(len(a[0]) == len(b), 'shape')
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def det(a):
    """Bareiss determinant on a square rational minor; no numerical tolerance."""
    a = [row[:] for row in a]
    n = len(a)
    require(n > 0 and all(len(r) == n for r in a), 'square')
    sign, previous = Q(1), Q(1)
    for k in range(n-1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return Q(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        x = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                a[i][j] = (x*a[i][j]-a[i][k]*a[k][j])/previous
            a[i][k] = Q(0)
        previous = x
    return sign*a[-1][-1]


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def outer(p, e):
    return [[x*y for y in e] for x in p]


def family_minor(p, e, ts):
    n, np, ne = len(p), len(p[0]), len(e)
    pd = det([row[:] for row in p[:np]])
    ed = det([row[:ne] for row in e])
    # Select one independent operator-entry coordinate for each preparation/effect pair.
    td = det([[t[r][c] for r in range(np) for c in range(ne)] for t in ts])
    require(pd != 0 and ed != 0 and td != 0, 'independent minors')
    require(td == pd**ne * ed**np, 'Kronecker determinant identity')
    require(len(ts) == np*ne, 'complete reset family')
    return {'preparation_minor': str(pd), 'effect_minor': str(ed),
            'operator_minor': str(td), 'operator_count': len(ts),
            'spans_full_operator_space': len(ts) == n*n}


def check_candidate(path):
    obj = json.loads(path.read_bytes())
    reports = {}
    for name, n, np, ne, descends in [
        ('classical_product',4,4,4,True), ('doubled_visible',8,4,4,True),
        ('doubled_all_preparations',8,8,4,True), ('doubled_global_tests',8,8,8,False)]:
        model = obj['models'][name]
        def read(key):
            return [[Q(x) for x in row] for row in model[key]]
        m, r, p, e = [read(key) for key in ('observe','prepare','preparations','effects')]
        ts = [[[Q(x) for x in row] for row in t] for t in model['filters']]
        ls = [[[Q(x) for x in row] for row in t] for t in model['coordinate_filters']]
        require(len(ts) == len(ls) == np*ne, 'operation coverage')
        require(mul(m,r) == eye(4), 'calibration')
        require(det([row[:4] for row in m]) != 0, 'full observation rank')
        for i in range(np):
            pi = [p[k][i] for k in range(n)]
            require(sum(pi) == 1 and all(x >= 0 for x in pi), 'normalized preparation')
            for j in range(ne):
                t = ts[i*ne+j]
                require(t == outer(pi,e[j]), 'reset definition')
                require(all(0 <= x <= 1 for x in e[j]), 'bounded effect')
                require(ls[i*ne+j] == mul(mul(m,t),r), 'coordinate action')
        require(all(mul(m,t) == mul(l,m) for t,l in zip(ts,ls)) == descends, 'descent')
        require((e == mul(mul(e,r),m)) == descends, 'effect factorization')
        report = family_minor(p,e,ts)
        report.update(hidden_dimension=n-4, descent=descends)
        if n == 8:
            hidden = [[Q(i == 0)-Q(i == 4)] for i in range(8)]
            require(mul(m,hidden) == [[Q(0)] for _ in range(4)], 'hidden direction')
            require(all(mul(t,hidden) == [[Q(0)] for _ in range(8)] for t in ts) == descends,
                    'hidden annihilation')
            require(any(mul(m,mul(t,hidden)) != [[Q(0)] for _ in range(4)] for t in ts) != descends,
                    'protected reset')
        reports[name] = report
    return reports


def nonorthogonal_controls():
    # Full reset families need no orthogonality. These normalized preparations
    # and bounded effects lie away from the orthogonal fixtures in the PR.
    p = [[Q(1),Q(1,2),Q(1,3)], [Q(0),Q(1,2),Q(1,3)], [Q(0),Q(0),Q(1,3)]]
    e = [[Q(1),Q(1,2),Q(1,3)], [Q(1,3),Q(1),Q(1,2)], [Q(1,2),Q(1,3),Q(1)]]
    ts = [outer([row[i] for row in p],row) for i in range(3) for row in e]
    report = family_minor(p,e,ts)
    require(all(sum(t[k][j] for k in range(3)) <= 1 for t in ts for j in range(3)), 'outcome bound')
    # An asymmetric positive calibrated observation still has a hidden sector.
    m = [[Q(1),Q(0),Q(1)], [Q(0),Q(1),Q(0)]]
    r = [[Q(1,3),Q(0)], [Q(0),Q(1)], [Q(2,3),Q(0)]]
    require(mul(m,r) == eye(2), 'asymmetric calibration')
    h = [[Q(1)], [Q(0)], [Q(-1)]]
    require(mul(m,h) == [[Q(0)],[Q(0)]], 'asymmetric hidden direction')
    for i in range(3):
        for f in m:
            t = outer([row[i] for row in p],f)
            require(mul(m,t) == mul(mul(mul(m,t),r),m), 'asymmetric pullback')
            require(mul(t,h) == [[Q(0)] for _ in range(3)], 'asymmetric annihilation')
    # Nonzero output alone is insufficient for the algebraic iff: an output
    # in the hidden kernel conceals a nonfactoring effect.
    effect = [[Q(1),Q(0),Q(0)]]
    hidden_output = outer([row[0] for row in h],effect[0])
    require(effect != mul(mul(effect,r),m), 'nonfactoring effect')
    require(mul(m,hidden_output) == [[Q(0)]*3 for _ in range(2)], 'invisible nonzero output')
    return report


def main():
    # Guard the independent determinant routine against pivoting, singularity,
    # and exact fractional examples before using it for certificates.
    require(det([[Q(0),Q(1)],[Q(2),Q(3)]]) == -2, 'pivot control')
    require(det([[Q(1),Q(2)],[Q(2),Q(4)]]) == 0, 'singular control')
    require(det([[Q(1,2),Q(1,3)],[Q(1,4),Q(1,5)]]) == Q(1,60), 'rational control')
    print(json.dumps({'all_passed':True, 'authority_effect':'None',
        'fixtures':check_candidate(Path(sys.argv[1])), 'nonorthogonal_controls':nonorthogonal_controls(),
        'scope':'finite exact determinants and hidden witnesses only; no operational postulate derivation'},indent=2))


if __name__ == '__main__':
    main()
