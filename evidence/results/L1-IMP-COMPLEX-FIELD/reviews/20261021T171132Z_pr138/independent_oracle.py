"""Review oracle using real operator matrices and integer row elimination.
Imports no production code. Finite checks only; not a classification proof.
"""
from fractions import Fraction
from functools import reduce
from math import gcd
from pathlib import Path
import argparse
import json


def transpose(a):
    return [list(r) for r in zip(*a)]


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def plus(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def rank(a):
    # Integer, fraction-free row reduction. GCD division preserves rational rank.
    a = [list(row) for row in a]
    r = 0
    for c in range(len(a[0]) if a else 0):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        for i in range(r+1, len(a)):
            if a[i][c]:
                row = [a[r][c]*x-a[i][c]*y for x,y in zip(a[i],a[r])]
                divisor = reduce(gcd, row, 0)
                a[i] = [x//divisor for x in row] if divisor else row
        r += 1
        if r == len(a):
            break
    return r


# Left regular action of 1,i,j,k on the ordered real basis (1,i,j,k).
I = [[int(i == j) for j in range(4)] for i in range(4)]
U = [I,
     [[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]],
     [[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]],
     [[0,0,0,-1],[0,0,-1,0],[0,1,0,0],[1,0,0,0]]]
ZERO = [[0]*4 for _ in range(4)]


def operator_basis(n, d):
    out = []
    for i in range(n):
        a = [[ZERO for _ in range(n)] for _ in range(n)]
        a[i][i] = I
        out.append(a)
    for i in range(n):
        for j in range(i+1, n):
            for u in U[:d]:
                a = [[ZERO for _ in range(n)] for _ in range(n)]
                a[i][j], a[j][i] = u, transpose(u)
                out.append(a)
    return out


def expanded(a):
    return [[a[i][j][r][s] for j in range(len(a)) for s in range(4)]
            for i in range(len(a)) for r in range(4)]


def product(a, b):
    return expanded([[multiply(a[i][j], b[k][l])
                      for j in range(len(a)) for l in range(len(b))]
                     for i in range(len(a)) for k in range(len(b))])


def flat(a):
    return [x for r in a for x in r]


def real_basis(n):
    out = []
    for i in range(n):
        for j in range(i, n):
            a = [[0]*n for _ in range(n)]
            a[i][j] = a[j][i] = 1
            out.append(a)
    return out


def audit(candidate):
    negI = [[-x for x in r] for r in I]
    assert all(multiply(u,u) == negI and transpose(u) == [[-x for x in r] for r in u] for u in U[1:])
    assert multiply(U[1], U[2]) == U[3]
    assert multiply(U[2], U[1]) == [[-x for x in r] for r in U[3]]
    spans = {}
    for d in (1,2,4):
        basis = operator_basis(2,d)
        ps = [product(a,b) for a in basis for b in basis]
        report = {'local_dimension':len(basis), 'joint_dimension':len(operator_basis(4,d)),
                  'raw_rank':rank([flat(p) for p in ps]),
                  'nonhermitian_products':sum(p != transpose(p) for p in ps),
                  'hermitian_projection_rank':rank([flat(plus(p,transpose(p))) for p in ps])}
        assert report == candidate['spans'][str(d)]
        spans[str(d)] = report
    # Construct state certificates from Gram vectors, independently of Y tensor Y.
    vectors = [[1,0,0,1],[0,1,-1,0],[1,0,0,-1],[0,1,1,0]]
    states = []
    for key, pair in [('rho_plus',vectors[:2]),('rho_minus',vectors[2:])]:
        gram = [[sum(v[i]*v[j] for v in pair) for j in range(4)] for i in range(4)]
        state = [[Fraction(x,4) for x in row] for row in gram]
        assert state == [[Fraction(x) for x in row] for row in candidate[key]]
        assert sum(state[i][i] for i in range(4)) == 1
        states.append(state)
    assert states[0] != states[1]
    delta = [[2*(states[0][i][j]-states[1][i][j]) for j in range(4)] for i in range(4)]
    assert delta == [[Fraction(x) for x in row] for row in candidate['delta']]
    assert multiply(delta,delta) == I
    for a in real_basis(2):
        for b in real_basis(2):
            p = [[a[i][j]*b[k][l] for j in range(2) for l in range(2)] for i in range(2) for k in range(2)]
            assert sum(delta[i][j]*p[j][i] for i in range(4) for j in range(4)) == 0
    commutants = {}
    for n in range(1,5):
        J = [[(int(i-n==j) if i>=n else -int(i==j-n)) for j in range(2*n)] for i in range(2*n)]
        constraints = []
        bs = real_basis(2*n)
        for a in bs:
            aj, ja = multiply(a,J), multiply(J,a)
            constraints.append([x-y for x,y in zip(flat(aj),flat(ja))])
        commutants[str(n)] = len(bs)-rank(constraints)
        assert commutants[str(n)] == n*n
    return {'passed':True, 'spans':spans, 'states':'exact Gram certificates',
            'commutant_dimensions':commutants,
            'method':'real regular operators; integer elimination; no production imports',
            'authority_effect':'None', 'scope':'finite checks, not universal evidence'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(json.loads(args.candidate.read_bytes())), indent=2))
