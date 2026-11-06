"""Construct the four finite rational controls independently of the checker.
AuthorityEffect: None. Use --output with a new destination; never replace evidence.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def make_candidate():
    def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
    def us(n):
        return [[[F((i,j)==(k,l)) for j in range(n)] for i in range(n)]
                for k in range(n) for l in range(n)]
    def mul(a,b):
        return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
                 for j in range(len(b[0]))] for i in range(len(a))]
    I=eye(4)
    doubleM=[r+r for r in I]
    doubleR=[[v/2 for v in r] for r in I]*2
    doubleT=[[[t[i%4][j%4] if i//4==j//4 else F(0) for j in range(8)]
              for i in range(8)] for t in us(4)]
    examples={}
    for name,M,R,ops in [('product_filters',I,I,us(4)),
                         ('doubled_filters',doubleM,doubleR,doubleT),
                         ('tomographic_identity',I,I,[I]),
                         ('irreducible_without_descent',doubleM,doubleR,us(8))]:
        encode=lambda a:[[str(x) for x in row] for row in a]
        examples[name]={'state_dimension':len(R),'local_frame_sizes':[2,2],
            'observe':encode(M),'prepare':encode(R),
            'operations':[encode(t) for t in ops],
            'coordinate_operations':[encode(mul(mul(M,t),R)) for t in ops]}
    return {'schema':'operational-tomography.v1','authority_effect':'None',
      'premises':['field-linear state and observation spaces are supplied',
        'independent preparation and test calibration is supplied',
        'observation descent under admitted operations is supplied',
        'irreducibility is an additional sufficient assumption',
        'physical availability of the admitted filters remains open'],
      'claim':'conditional theorem with an unconditional obstruction','examples':examples}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    with args.output.open('xb') as f:
        f.write((json.dumps(make_candidate(),indent=2)+'\n').encode())
