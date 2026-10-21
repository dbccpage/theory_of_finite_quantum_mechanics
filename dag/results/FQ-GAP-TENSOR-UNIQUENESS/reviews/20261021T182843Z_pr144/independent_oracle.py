"""Independent finite oracle using determinants and orthogonal operator witnesses.
No imports from the candidate builder, Python checker, or replay driver.
This verifies four rational models, not a universal operational reconstruction.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def parse(value):
    require(type(value) is list and len(value) > 0, 'empty matrix')
    width = len(value[0])
    require(width > 0 and all(type(r) is list and len(r) == width for r in value), 'shape')
    for row in value:
        for x in row:
            require(type(x) is str and str(Q(x)) == x, 'canonical rational')
    return [[Q(x) for x in row] for row in value]


def eye(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def product(a, b):
    require(len(a[0]) == len(b), 'product shape')
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def difference(a, b):
    require(len(a) == len(b) and len(a[0]) == len(b[0]), 'difference shape')
    return [[a[i][j]-b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def zero(a):
    return all(x == 0 for row in a for x in row)


def determinant(matrix):
    # Bareiss elimination; unlike either PR rank implementation, uses no row
    # normalization and verifies a determinant witness rather than computing rank.
    a = [row[:] for row in matrix]
    n = len(a)
    require(n > 0 and all(len(row) == n for row in a), 'determinant shape')
    previous, sign = Q(1), Q(1)
    for k in range(n-1):
        pivot_row = next((i for i in range(k,n) if a[i][k] != 0), None)
        if pivot_row is None:
            return Q(0)
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                a[i][j] = (pivot*a[i][j]-a[i][k]*a[k][j])/previous
            a[i][k] = Q(0)
        previous = pivot
    return sign*a[-1][-1]


def verify(raw):
    c = json.loads(raw)
    require(c['authority_effect'] == 'None', 'authority')
    expected = {
        'product_filters': (4,16,True),
        'doubled_filters': (8,16,True),
        'tomographic_identity': (4,1,True),
        'irreducible_without_descent': (8,64,False),
    }
    require(set(c['examples']) == set(expected), 'coverage')
    result = {}
    for name, (n,count,descends) in expected.items():
        e = c['examples'][name]
        m, r = parse(e['observe']), parse(e['prepare'])
        require(len(m) == 4 and len(m[0]) == n and len(r) == n and len(r[0]) == 4, 'dimensions')
        require(product(m,r) == eye(4), 'calibration')
        # The columns of R and explicit anti-diagonal Z form a basis; MR=I and
        # MZ=0 then prove rank(M)=4 and ker(M)=im(Z), independently of rank code.
        z = [[Q(int(i == j)-int(i == j+4)) for j in range(n-4)] for i in range(n)]
        basis = [r[i]+z[i] for i in range(n)]
        det = determinant(basis)
        require(det != 0, 'basis determinant')
        if n > 4:
            require(zero(product(m,z)), 'kernel basis')
        h = difference(eye(n),product(r,m))
        require(product(h,h) == h and zero(product(m,h)), 'hidden projection')
        ts = [parse(t) for t in e['operations']]
        ls = [parse(l) for l in e['coordinate_operations']]
        require(len(ts) == len(ls) == count, 'operation coverage')
        require(all(len(t) == n and len(t[0]) == n for t in ts), 'state operation dimensions')
        require(all(len(l) == 4 and len(l[0]) == 4 for l in ls), 'coordinate operation dimensions')
        descent = [product(m,ts[k]) == product(ls[k],m) for k in range(count)]
        require(all(descent) == descends, 'descent')
        # Distinct matrix units, doubled units, or the sole identity are pairwise
        # Frobenius orthogonal with nonzero norm; this proves linear independence.
        norms = []
        for k in range(count):
            for l in range(count):
                pairing = sum((ts[k][i][j]*ts[l][i][j]
                               for i in range(n) for j in range(n)), Q(0))
                require(pairing > 0 if k == l else pairing == 0, 'operator Gram witness')
                if k == l:
                    norms.append(str(pairing))
        require(all(x >= 0 for t in ts for row in t for x in row), 'positive filters')
        sums = [sum(t[i][j] for i in range(n)) for t in ts for j in range(n)]
        require(all(s <= 1 for s in sums), 'subnormalized filters')
        require(all(s == 1 for s in sums) == (name == 'tomographic_identity'), 'normalization')
        if n == 8:
            for j in range(4):
                x = [[Q(int(i == j))] for i in range(n)]
                y = [[Q(int(i == j+4))] for i in range(n)]
                require(product(m,x) == product(m,y) and x != y, 'hidden states')
                require(sum(row[0] for row in x) == sum(row[0] for row in y) == 1, 'normalized states')
                require(sum(x[i][0] for i in range(4)) == 1 and sum(y[i][0] for i in range(4)) == 0, 'protected question')
                visible = [not zero(product(m,product(t,difference(x,y)))) for t in ts]
                require(any(visible) == (not descends), 'hidden invariance control')
        if name == 'product_filters':
            for a in range(4):
                for b in range(4):
                    require(ts[4*a+b] == [[Q(int(i//2 == a//2 and j//2 == b//2)
                        * int(i%2 == a%2 and j%2 == b%2)) for j in range(4)] for i in range(4)], 'local tensor factorization')
        result[name] = {'basis_determinant':str(det),'observation_rank':4,
                        'hidden_dimension':n-4,'operator_span_rank':count,
                        'operator_gram_diagonal':norms,'descent':all(descent)}
    # Calibrate the determinant oracle on small, singular, row-swap, and large
    # exact inputs. Integer matrices here are converted explicitly to rationals.
    require(determinant([[Q(0),Q(1)],[Q(1),Q(0)]]) == -1, 'row swap')
    require(determinant([[Q(1),Q(2)],[Q(2),Q(4)]]) == 0, 'singular')
    for n in (2**54,10**100):
        require(determinant([[Q(n),Q(n+1)],[Q(n+1),Q(n+2)]]) == -1, 'integer exactness')
    return {'all_passed':True,'authority_effect':'None',
            'candidate_sha256':hashlib.sha256(raw).hexdigest(),'models':result,
            'scope':'finite rational determinant, Gram, positivity and kernel witnesses; no physical availability inference'}


if __name__ == '__main__':
    print(json.dumps(verify(Path(sys.argv[1]).read_bytes()),indent=2))
