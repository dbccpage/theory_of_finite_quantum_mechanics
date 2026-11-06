"""Independent finite certificate constructor. AuthorityEffect: None."""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path

PREMISES = [
    'finite nonempty carriers with a declared involutive symmetry',
    'real invariant state vectors with coordinatewise positivity and sum normalization',
    'all nonnegative equivariant matrices are processes; events have column sums at most one',
    'parallel composition uses the diagonal symmetry on the Cartesian product',
    'finite instruments have total column sum one and transformations retain ancillary distinctions',
    'this package does not assume purification, local complex quantum structure or primitive selection',
]


def build():
    systems = []
    for n in range(5):
        size = 4**n
        mask = sum(4**j for j in range(n))
        flip = [x ^ mask for x in range(size)]
        orbits = [[x] if flip[x] == x else [x,flip[x]] for x in range(size) if x <= flip[x]]
        def visible(x):
            value = 0
            for j in range(n):
                value += ((x // 4**j)//2 % 2) * 2**j
            return value
        m = [[Q(visible(o[0]) == j) for o in orbits] for j in range(2**n)]
        divisor = Q(1 if n == 0 else 2**(n-1))
        prep = [[Q(visible(o[0]) == j)/divisor for j in range(2**n)] for o in orbits]
        systems.append({'atoms':n,'points':size,'flip':flip,'orbits':orbits,
            'observe':[[str(x) for x in row] for row in m],
            'prepare':[[str(x) for x in row] for row in prep]})
    channels = {}
    for name,perm in [('identity',list(range(4))),('flag_flip',[1,0,3,2]),('visible_flip',[2,3,0,1])]:
        channels[name] = [[str(int(y == perm[x])) for x in range(4)] for y in range(4)]
    channels['noise'] = [['1/4']*4 for _ in range(4)]
    instruments = [[[str(int(y == x and x//2 == j)) for x in range(4)] for y in range(4)] for j in range(2)]
    rho,sigma,e = [],[],[]
    for x in range(16):
        a,b = divmod(x,4)
        good = a//2 == b//2 == 0
        equal = a%2 == b%2
        rho.append(str(Q(1,2) if good and equal else Q(0)))
        sigma.append(str(Q(1,2) if good and not equal else Q(0)))
        e.append(str(int(equal)))
    return {'schema':'operational-independence.v1','authority_effect':'None','premises':PREMISES,
        'systems':systems,'channels':channels,'instrument':instruments,
        'hidden_states':{'rho':rho,'sigma':sigma,'effect':e}}


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    out=p.parse_args().output
    out.write_bytes((json.dumps(build(),indent=2)+'\n').encode())
