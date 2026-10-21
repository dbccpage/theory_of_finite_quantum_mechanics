"""Exact finite controls for OperationalTomography. AuthorityEffect: None.

The generic analyzer proves no universal statement. Full operator span is a
sufficient irreducibility certificate over Q, not its definition or a necessary
condition. All model matrices and scopes are independently checked.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

PREMISES = (
    'field-linear state and observation spaces are supplied',
    'independent preparation and test calibration is supplied',
    'observation descent under admitted operations is supplied',
    'irreducibility is an additional sufficient assumption',
    'physical availability of the admitted filters remains open',
)


def matrix(rows, cols):
    return [[Q(0) for _ in range(cols)] for _ in range(rows)]


def identity(n):
    a = matrix(n, n)
    for i in range(n):
        a[i][i] = Q(1)
    return a


def multiply(a, b):
    if not a or not b or len(a[0]) != len(b):
        raise ValueError('MATRIX_SHAPE')
    return [[sum((x*y for x,y in zip(row, col)), Q(0))
             for col in zip(*b)] for row in a]


def subtract(a, b):
    if len(a) != len(b) or any(len(x) != len(y) for x,y in zip(a,b)):
        raise ValueError('MATRIX_SHAPE')
    return [[x-y for x,y in zip(row,other)] for row,other in zip(a,b)]


def rank(a):
    a = [row[:] for row in a]
    r = 0
    for j in range(len(a[0])):
        k = next((i for i in range(r,len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        divisor = a[r][j]
        a[r] = [x/divisor for x in a[r]]
        for i in range(r+1,len(a)):
            factor = a[i][j]
            a[i] = [x-factor*y for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r


def matrix_unit(n, i, j):
    a = matrix(n,n)
    a[i][j] = Q(1)
    return a


def units(n):
    return [matrix_unit(n,i,j) for i in range(n) for j in range(n)]


def analyze(M, R, operations, coordinate_operations):
    c, n = len(M), len(M[0])
    if not operations or len(operations) != len(coordinate_operations):
        raise ValueError('OPERATION_COUNT')
    # Shapes are also checked for direct callers, before any zip-based algebra.
    for a, rows, cols in [(M,c,n),(R,n,c), *[(t,n,n) for t in operations],
                          *[(l,c,c) for l in coordinate_operations]]:
        if len(a) != rows or any(len(row) != cols for row in a):
            raise ValueError('MATRIX_SHAPE')
    hidden = subtract(identity(n),multiply(R,M))
    r = rank(M)
    return {
        'calibrated': multiply(M,R) == identity(c),
        'descent': all(multiply(M,t) == multiply(l,M)
                       for t,l in zip(operations,coordinate_operations)),
        'nonzero_observation': any(x for row in M for x in row),
        'full_operator_span': rank([[x for row in t for x in row] for t in operations]) == n*n,
        'operator_span_rank': rank([[x for row in t for x in row] for t in operations]),
        'tomographic': r == n,
        'observation_rank': r,
        'hidden_dimension': n-r,
        'hidden': hidden,
        'normalization_preserved': all(all(sum(t[i][j] for i in range(n)) == 1
                                          for j in range(n)) for t in operations),
        'positive_subnormalized_filters': all(all(x >= 0 for row in t for x in row)
            and all(sum(t[i][j] for i in range(n)) <= 1 for j in range(n)) for t in operations),
    }


def parse_matrix(value, rows, cols):
    if type(value) is not list or len(value) != rows:
        raise ValueError('MATRIX_SHAPE')
    out = []
    for row in value:
        if type(row) is not list or len(row) != cols:
            raise ValueError('MATRIX_SHAPE')
        parsed = []
        for s in row:
            if type(s) is not str or len(s) > 48:
                raise ValueError('RATIONAL_TYPE')
            try:
                q = Q(s)
            except (ValueError,ZeroDivisionError):
                raise ValueError('RATIONAL_FORMAT') from None
            if str(q) != s:
                raise ValueError('RATIONAL_CANONICAL')
            parsed.append(q)
        out.append(parsed)
    return out


def no_duplicates(pairs):
    result = {}
    for k,v in pairs:
        if k in result:
            raise ValueError('DUPLICATE_KEY')
        result[k] = v
    return result


def verify_candidate_bytes(raw):
    if len(raw) > 1_000_000:
        raise ValueError('SIZE_LIMIT')
    c = json.loads(raw, object_pairs_hook=no_duplicates)
    if type(c) is not dict or set(c) != {'schema','authority_effect','premises','claim','examples'}:
        raise ValueError('ENVELOPE')
    if c['schema'] != 'operational-tomography.v1' or c['authority_effect'] != 'None':
        raise ValueError('SCOPE')
    if c['premises'] != list(PREMISES) or c['claim'] != 'conditional theorem with an unconditional obstruction':
        raise ValueError('PREMISES')
    expected = {
        'product_filters': (4,4,True,True,True,True,0,16,False),
        'doubled_filters': (8,4,True,True,False,False,4,16,False),
        'tomographic_identity': (4,4,True,True,False,True,0,1,True),
        'irreducible_without_descent': (8,4,True,False,True,False,4,64,False),
    }
    if type(c['examples']) is not dict or set(c['examples']) != set(expected):
        raise ValueError('COVERAGE')
    results = {}
    for name,(n,d,cal,des,full,tomo,defect,span,preserve) in expected.items():
        e = c['examples'][name]
        if type(e) is not dict or set(e) != {'state_dimension','local_frame_sizes','observe','prepare','operations','coordinate_operations'}:
            raise ValueError('EXAMPLE_SCHEMA')
        if type(e['state_dimension']) is not int or e['state_dimension'] != n:
            raise ValueError('DIMENSION')
        if type(e['local_frame_sizes']) is not list or any(type(k) is not int for k in e['local_frame_sizes']) or e['local_frame_sizes'] != [2,2]:
            raise ValueError('LOCAL_FRAMES')
        M = parse_matrix(e['observe'],d,n)
        R = parse_matrix(e['prepare'],n,d)
        if type(e['operations']) is not list or type(e['coordinate_operations']) is not list or len(e['operations']) != span or len(e['coordinate_operations']) != span:
            raise ValueError('OPERATION_COUNT')
        ops = [parse_matrix(t,n,n) for t in e['operations']]
        loc = [parse_matrix(t,d,d) for t in e['coordinate_operations']]
        result = analyze(M,R,ops,loc)
        fields = ('calibrated','descent','full_operator_span','tomographic','hidden_dimension','operator_span_rank','normalization_preserved')
        if tuple(result[k] for k in fields) != (cal,des,full,tomo,defect,span,preserve):
            raise ValueError('SEMANTIC_CONTROL:'+name)
        if not result['positive_subnormalized_filters']:
            raise ValueError('FILTER_POSITIVITY')
        # Verify the actual intended models, not merely ranks compatible with them.
        want_M = identity(4) if n == 4 else [row+row for row in identity(4)]
        want_R = identity(4) if n == 4 else [[x/2 for x in row] for row in identity(4)]*2
        if M != want_M or R != want_R:
            raise ValueError('MODEL_CALIBRATION')
        us = units(4)
        doubled_units = [[row+[Q(0)]*4 for row in t]+[[Q(0)]*4+row for row in t] for t in us]
        want_ops = {'product_filters':us, 'doubled_filters':doubled_units,
                    'tomographic_identity':[identity(4)], 'irreducible_without_descent':units(8)}[name]
        want_loc = [multiply(multiply(M,t),R) for t in want_ops]
        if ops != want_ops or loc != want_loc:
            raise ValueError('MODEL_OPERATIONS')
        H = result['hidden']
        if multiply(M,H) != matrix(d,n) or multiply(H,H) != H:
            raise ValueError('HIDDEN_PROJECTION')
        results[name] = {k:v for k,v in result.items() if k != 'hidden'}
    return {'authority_effect':'None','candidate_sha256':hashlib.sha256(raw).hexdigest(),
            'finite_checks':'passed','examples':results,'premises':list(PREMISES)}


if __name__ == '__main__':
    print(json.dumps(verify_candidate_bytes(Path(sys.argv[1]).read_bytes()),indent=2))
