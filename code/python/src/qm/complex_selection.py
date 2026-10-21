"""Exact finite carrier checks; classification and dimension multiplicativity are inputs.

AuthorityEffect: None. A census is finite evidence, never a proof for all sizes.
The Lean companion supplies the universal implication with d > 0.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Gaussian:
    re: F = F(0)
    im: F = F(0)

    def __add__(self, other):
        return Gaussian(self.re + other.re, self.im + other.im)

    def __neg__(self):
        return Gaussian(-self.re, -self.im)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        return Gaussian(self.re * other.re - self.im * other.im,
                        self.re * other.im + self.im * other.re)

    def conj(self):
        return Gaussian(self.re, -self.im)

    def scale(self, q):
        return Gaussian(q * self.re, q * self.im)

    def coords(self):
        return (self.re, self.im)


@dataclass(frozen=True)
class Quaternion:
    re: F = F(0)
    i: F = F(0)
    j: F = F(0)
    k: F = F(0)

    def __add__(self, other):
        return Quaternion(*(a+b for a,b in zip(self.coords(), other.coords())))

    def __neg__(self):
        return self.scale(-1)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        a,b,c,d = self.coords()
        e,f,g,h = other.coords()
        return Quaternion(a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g,
                          a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)

    def conj(self):
        return Quaternion(self.re, -self.i, -self.j, -self.k)

    def scale(self, q):
        return Quaternion(*(q*a for a in self.coords()))

    def coords(self):
        return (self.re, self.i, self.j, self.k)


def dimension(d: int, n: int) -> int:
    if type(d) is not int or type(n) is not int or d < 0 or n < 0:
        raise ValueError('natural numbers required')
    return n + d*n*(n-1)//2


def census():
    return [[d,n,m,dimension(d,n*m),dimension(d,n)*dimension(d,m)]
            for d in (1,2,4) for n in range(1,7) for m in range(1,7)]


def scalar(d, q=0):
    if d == 1:
        return F(q)
    if d == 2:
        return Gaussian(F(q))
    if d == 4:
        return Quaternion(F(q))
    raise ValueError('carrier not in supplied family')


def conjugate(x):
    return x.conj() if hasattr(x, 'conj') else x


def scale(x, q):
    return x.scale(q) if hasattr(x, 'scale') else q*x


def matrix(n, d):
    return [[scalar(d) for _ in range(n)] for _ in range(n)]


def hermitian_basis(n, d):
    units = [scalar(d,1)]
    if d == 2:
        units += [Gaussian(F(0),F(1))]
    if d == 4:
        units += [Quaternion(F(0),F(1)), Quaternion(F(0),F(0),F(1)),
                  Quaternion(F(0),F(0),F(0),F(1))]
    out = []
    for i in range(n):
        a = matrix(n,d)
        a[i][i] = scalar(d,1)
        out.append(a)
    for i in range(n):
        for j in range(i+1,n):
            for u in units:
                a = matrix(n,d)
                a[i][j],a[j][i] = u,conjugate(u)
                out.append(a)
    return out


def kron(a,b):
    return [[a[i][j]*b[k][l] for j in range(len(a)) for l in range(len(b))]
            for i in range(len(a)) for k in range(len(b))]


def adjoint(a):
    return [[conjugate(a[j][i]) for j in range(len(a))] for i in range(len(a))]


def hermitian_part(a):
    ah = adjoint(a)
    return [[scale(x+y,F(1,2)) for x,y in zip(r,s)] for r,s in zip(a,ah)]


def flatten(a):
    return [q for row in a for x in row
            for q in (x.coords() if hasattr(x,'coords') else (x,))]


def rank(rows):
    """Gaussian elimination over Fraction, with exact zero detection."""
    a = [[F(x) for x in row] for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r,len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r],a[pivot] = a[pivot],a[r]
        p = a[r][c]
        a[r] = [x/p for x in a[r]]
        for i in range(len(a)):
            if i != r:
                q = a[i][c]
                a[i] = [x-q*y for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r


def span_census(d):
    basis = hermitian_basis(2,d)
    products = [kron(a,b) for a in basis for b in basis]
    projected = [hermitian_part(a) for a in products]
    return {'local_dimension':len(basis), 'joint_dimension':len(hermitian_basis(4,d)),
            'raw_rank':rank([flatten(a) for a in products]),
            'nonhermitian_products':sum(a != adjoint(a) for a in products),
            'hermitian_projection_rank':rank([flatten(a) for a in projected])}


def trace_pair(a,b):
    return sum((a[i][j]*b[j][i] for i in range(len(a)) for j in range(len(a))), F(0))


def multiply(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(a))),F(0))
             for j in range(len(a))] for i in range(len(a))]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def witness():
    y = [[F(0),F(-1)],[F(1),F(0)]]
    delta = kron(y,y)
    rhos = [[[ (F(i==j)+s*delta[i][j])/4 for j in range(4)] for i in range(4)]
            for s in (1,-1)]
    return delta,*rhos


def determinant(a):
    if not a:
        return F(1)
    return sum(((-1)**j*a[0][j]*determinant([row[:j]+row[j+1:] for row in a[1:]])
                for j in range(len(a))),F(0))


def principal_minors(a):
    return [determinant([[a[i][j] for j in range(len(a)) if mask>>j&1]
                         for i in range(len(a)) if mask>>i&1])
            for mask in range(1,1<<len(a))]


def encode_matrix(a):
    return [[str(x) for x in row] for row in a]


def decode_matrix(a, n):
    if type(a) is not list or len(a) != n or any(type(r) is not list or len(r) != n for r in a):
        raise ValueError('matrix shape')
    if any(type(x) is not str for r in a for x in r):
        raise ValueError('canonical rational strings required')
    b = [[F(x) for x in r] for r in a]
    if encode_matrix(b) != a:
        raise ValueError('noncanonical rationals')
    return b


def realify(a):
    n = len(a)
    return [[(a[i%n][j%n].re if (i<n)==(j<n) else
             (-a[i%n][j%n].im if i<n else a[i%n][j%n].im))
             for j in range(2*n)] for i in range(2*n)]


def complex_structure(n):
    return [[F(0) if (i<n)==(j<n) else F((-1 if i<n else 1)*(i%n==j%n))
             for j in range(2*n)] for i in range(2*n)]


def j_commutant_symmetric_dimension(n):
    basis = hermitian_basis(2*n,1)
    j = complex_structure(n)
    constraints = []
    for a in basis:
        aj,ja = multiply(a,j),multiply(j,a)
        constraints.append(flatten([[x-y for x,y in zip(r,s)] for r,s in zip(aj,ja)]))
    return len(basis)-rank(constraints)


PREMISES = ('matrix_carriers_R_C_H_only', 'same_family_nm_composite',
            'independent_product_preparations_and_factorized_tests', 'local_tomography')


def make_candidate():
    delta,plus,minus = witness()
    return {'schema':'tfqm.complex-selection.v1', 'authority_effect':'None',
            'premises':list(PREMISES), 'status':'CONDITIONAL',
            'universal_claim':{'domain':'positive_natural_d', 'n_min':2,'m_min':2,
                               'selected_d':2, 'evidence':'Lean:dimension_selection'},
            'unrestricted_solutions':[0,2], 'census':census(),
            'spans':{str(d):span_census(d) for d in (1,2,4)},
            'delta':encode_matrix(delta), 'rho_plus':encode_matrix(plus),
            'rho_minus':encode_matrix(minus),
            'real_with_J':{'local_n2_dimension':j_commutant_symmetric_dimension(2),
                           'joint_n4_dimension':j_commutant_symmetric_dimension(4),
                           'composition':'complex_balanced_tensor', 'scalar_structure':'Q(i)'},
            'spin_factors':{'notation':'V_k = Q + Q^k','dimension':'k+1',
                            'exclusion':'IMPORTED','derivation_status':'OPEN'},
            'completeness':'IMPORTED'}


@lru_cache(maxsize=1)
def _expected_json():
    # Cache recomputed coordinates as JSON, with no mutable candidate references.
    # The constructor shares arithmetic with this checker; it is not an independent oracle.
    return json.dumps(make_candidate(), sort_keys=True)


def verify_candidate_bytes(raw: bytes):
    """Recompute finite equations and check scope. This does not run the Lean kernel.

The host must separately compile the source pinned by the P2 receipt. The evidence
label here states the obligation, and is not accepted as proof of that obligation.
"""
    def unique_pairs(pairs):
        out = {}
        for k,v in pairs:
            if k in out:
                raise ValueError('duplicate key')
            out[k] = v
        return out
    c = json.loads(raw,object_pairs_hook=unique_pairs,
                   parse_float=lambda _: (_ for _ in ()).throw(ValueError('floating point')))
    expected = json.loads(_expected_json())
    if type(c) is not dict or set(c) != set(expected):
        raise ValueError('schema fields')
    # Canonical JSON equality distinguishes bool from int; every coordinate is checked.
    for key in c:
        if json.dumps(c[key],sort_keys=True) != json.dumps(expected[key],sort_keys=True):
            raise ValueError('coordinate or scope mismatch: '+key)
    delta = decode_matrix(c['delta'],4)
    plus,minus = (decode_matrix(c[k],4) for k in ('rho_plus','rho_minus'))
    if delta != adjoint(delta) or multiply(delta,delta) != identity(4):
        raise ValueError('hidden operator')
    if plus == minus:
        raise ValueError('state distinction')
    for state in (plus,minus):
        if state != adjoint(state) or sum(state[i][i] for i in range(4)) != 1:
            raise ValueError('state symmetry or normalization')
        if min(principal_minors(state)) < 0:
            raise ValueError('state positivity')
    for a in hermitian_basis(2,1):
        for b in hermitian_basis(2,1):
            p = kron(a,b)
            if trace_pair(delta,p) != 0 or trace_pair(plus,p) != trace_pair(minus,p):
                raise ValueError('local statistics')
    return {'finite_checks':'passed', 'universal_Lean_obligation':'separate kernel receipt required',
            'census_cases':len(c['census']), 'spans':c['spans']}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify_candidate_bytes(args.candidate.read_bytes()),indent=2))
