"""Construct four exact reset families; no verifier imports. AuthorityEffect: None."""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path

PREMISES = [
    'field-linear carriers, positive cones and normalization are supplied',
    'test followed by preparation is an admitted selective operation',
    'global separating effects and spanning preparations suffice for irreducibility',
    'product-test reset irreducibility is equivalent to tomography',
    'global reset descent is not independently derived from primitives',
]


def build():
    models = {}
    for name,n,pc,ec in [('classical_product',4,4,4),('doubled_visible',8,4,4),
                         ('doubled_all_preparations',8,8,4),('doubled_global_tests',8,8,8)]:
        m = [[Q(int(i == j%4)) for j in range(n)] for i in range(4)]
        r = [[Q(int(i%4 == j),n//4) for j in range(4)] for i in range(n)]
        p = r if pc == 4 else [[Q(int(i == j)) for j in range(n)] for i in range(n)]
        e = m if ec == 4 else [[Q(int(i == j)) for j in range(n)] for i in range(n)]
        fs,ls = [],[]
        for a in range(pc):
            for b in range(ec):
                t = [[p[i][a]*e[b][j] for j in range(n)] for i in range(n)]
                # Independently index contraction: candidate observed action M T R.
                l = [[sum(m[i][k]*t[k][v]*r[v][j] for k in range(n) for v in range(n))
                      for j in range(4)] for i in range(4)]
                fs.append(t);ls.append(l)
        def enc(x): return [[str(v) for v in row] for row in x]
        models[name] = {'state_dimension':n,'local_frame_sizes':[2,2],
          'observe':enc(m),'prepare':enc(r),'preparations':enc(p),'effects':enc(e),
          'filters':[enc(t) for t in fs],'coordinate_filters':[enc(l) for l in ls]}
    return {'schema':'operational-filter-family.v1','authority_effect':'None',
            'premises':PREMISES,'models':models}


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();args.output.write_bytes((json.dumps(build(),indent=2)+'\n').encode())
