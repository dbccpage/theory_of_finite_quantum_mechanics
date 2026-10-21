"""Small exact rational matrix primitives for staged certificates.

All quantities are integers/Fractions. Native computations are certificates on
explicit finite inputs, not general Lean correctness proofs of this module.
"""
from fractions import Fraction as Q
from itertools import combinations

MAX_BITS: int = 1024
MAX_PRINCIPAL_MINOR_DIM: int = 8


def scalar(x):
    if isinstance(x, float):
        raise TypeError('float refused')
    if type(x) is bool:
        raise TypeError('boolean refused')
    if type(x) is int:
        if x.bit_length() > MAX_BITS:
            raise ValueError(f'integer exceeds {MAX_BITS}-bit limit')
        return Q(x)
    if isinstance(x, Q):
        if x.numerator.bit_length() > MAX_BITS or x.denominator.bit_length() > MAX_BITS:
            raise ValueError(f'rational component exceeds {MAX_BITS}-bit limit')
        return x
    raise TypeError('exact integer or Fraction required')


def matrix(rows):
    result = tuple(tuple(scalar(x) for x in row) for row in rows)
    if not result or not result[0] or any(len(row) != len(result[0]) for row in result):
        raise ValueError('nonempty rectangular matrix required')
    return result


def eye(n):
    if type(n) is not int or n <= 0:
        raise ValueError('positive dimension required')
    return tuple(tuple(Q(i == j) for j in range(n)) for i in range(n))


def transpose(a):
    return tuple(zip(*matrix(a)))


def scale(c, a):
    c = scalar(c)
    return tuple(tuple(c*x for x in row) for row in matrix(a))


def add(a, b):
    a, b = matrix(a), matrix(b)
    if (len(a),len(a[0])) != (len(b),len(b[0])):
        raise ValueError('matrix shape mismatch')
    return tuple(tuple(x+y for x,y in zip(r,s)) for r,s in zip(a,b))


def multiply(a, b):
    a, b = matrix(a), matrix(b)
    if len(a[0]) != len(b):
        raise ValueError('matrix product shape mismatch')
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(len(b))),Q(0)) for j in range(len(b[0]))) for i in range(len(a)))


def tensor(a, b):
    a,b = matrix(a),matrix(b)
    return tuple(tuple(x*y for x in r for y in s) for r in a for s in b)


def trace(a):
    a = matrix(a)
    if len(a) != len(a[0]):
        raise ValueError('square matrix required')
    return sum((a[i][i] for i in range(len(a))),Q(0))


def rref(a):
    rows = [list(row) for row in matrix(a)]; pivots=[]; rank=0
    for j in range(len(rows[0])):
        pivot=next((i for i in range(rank,len(rows)) if rows[i][j]),None)
        if pivot is None: continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        c=rows[rank][j];rows[rank]=[x/c for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][j]:
                c=rows[i][j];rows[i]=[x-c*y for x,y in zip(rows[i],rows[rank])]
        pivots.append(j);rank+=1
        if rank==len(rows):break
    return tuple(tuple(row) for row in rows),tuple(pivots)


def rank(a):
    return len(rref(a)[1])


def solve_unique(a,b):
    a=matrix(a);b=tuple(scalar(x) for x in b)
    if len(a)!=len(b):raise ValueError('linear system shape mismatch')
    reduced,pivots=rref([list(row)+[value] for row,value in zip(a,b)])
    n=len(a[0])
    if n in pivots or len(pivots)!=n:raise ValueError('system has no unique solution')
    return tuple(reduced[i][-1] for i in range(n))


def determinant(a):
    a=[list(row) for row in matrix(a)]
    if len(a)!=len(a[0]):raise ValueError('square matrix required')
    det=Q(1)
    for j in range(len(a)):
        p=next((i for i in range(j,len(a)) if a[i][j]),None)
        if p is None:return Q(0)
        if p!=j:a[j],a[p]=a[p],a[j];det=-det
        c=a[j][j];det*=c
        for i in range(j+1,len(a)):
            f=a[i][j]/c
            for k in range(j+1,len(a)):a[i][k]-=f*a[j][k]
    return det


def principal_minors(a):
    a=matrix(a)
    if a!=transpose(a):raise ValueError('symmetric matrix required')
    if len(a) > MAX_PRINCIPAL_MINOR_DIM:
        raise ValueError(f'dimension {len(a)} exceeds principal minor evaluation envelope (max {MAX_PRINCIPAL_MINOR_DIM})')
    return tuple((indices,determinant([[a[i][j] for j in indices] for i in indices])) for n in range(1,len(a)+1) for indices in combinations(range(len(a)),n))


def is_psd(a):
    return all(d>=0 for _,d in principal_minors(a))
