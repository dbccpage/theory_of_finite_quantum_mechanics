"""Public inputs only; no extension witnesses or expected classifications."""
from fractions import Fraction as Q


def public_cases():
    cases=[]
    for d in (1,2,3,4):
        for a in range(d+1):
            for c in range(d+1):
                for b0 in range(d+1):
                    for b1 in range(d+1):
                        ranges=[range(max(0,u+b-d),min(u,b)+1) for u,b in ((a,b0),(a,b1),(c,b0),(c,b1))]
                        from itertools import product
                        for xs in product(*ranges):
                            rows=[]
                            for u,b,x in zip((a,a,c,c),(b0,b1,b0,b1),xs):
                                rows.append([str(Q(n,d)) for n in (d-u-b+x,b-x,u-x,x)])
                            cases.append({'id':'grid_'+'_'.join(map(str,(d,a,c,b0,b1,*xs))),'pairs':rows})
    # A denominator far outside the bounded grid exercises arbitrary precision.
    d=10**80+7
    law=[Q(i+1) for i in range(16)];law[0]+=d;total=sum(law);law=[p/total for p in law]
    pairs=[[Q(0)]*4 for _ in range(4)]
    for m,p in enumerate(law):
        for x in range(2):
            for y in range(2):pairs[2*x+y][2*((m>>x)&1)+((m>>(2+y))&1)]+=p
    cases.append({'id':'arbitrary_precision_marginals','pairs':[[str(q) for q in row] for row in pairs]})
    return cases
