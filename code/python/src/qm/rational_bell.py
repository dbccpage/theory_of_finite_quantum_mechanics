"""Exact Born tables for supplied real rational binary observables.

Tensor product, a density matrix and Born trace readout are admitted inputs.
No locality or setting-independence assumption is inferred from these tables.
"""
from fractions import Fraction as Q
from .pfp_exact import add,eye,is_psd,matrix,multiply,scale,tensor,trace,transpose
from .bell_separator_extension import construct_extension, validate_pairs


def projectors(observable):
    a=matrix(observable); n=len(a)
    if len(a[0])!=n or a!=transpose(a) or multiply(a,a)!=eye(n):
        raise ValueError('symmetric binary involution required')
    return tuple(scale(Q(1,2),add(eye(n),scale(sign,a))) for sign in (-1,1))


def born_pairs(rho,alice,bob):
    if len(alice)!=2 or len(bob)!=2:raise ValueError('two settings per party required')
    a=[projectors(x) for x in alice];b=[projectors(x) for x in bob]
    if any(len(x[0])!=len(a[0][0]) for x in a) or any(len(x[0])!=len(b[0][0]) for x in b):
        raise ValueError('party dimensions differ between settings')
    rho=matrix(rho)
    if len(rho)!=len(a[0][0])*len(b[0][0]) or trace(rho)!=1 or not is_psd(rho):
        raise ValueError('positive trace-one density matrix of tensor dimension required')
    pairs=tuple(tuple(trace(multiply(rho,tensor(a[x][i],b[y][j]))) for i in range(2) for j in range(2)) for x in range(2) for y in range(2))
    return validate_pairs(pairs)


def certify(rho,alice,bob):
    pairs=born_pairs(rho,alice,bob)
    e=tuple(row[0]-row[1]-row[2]+row[3] for row in pairs)
    decision=construct_extension(pairs)
    supported=sum(all(pairs[2*x+y][2*((m>>x)&1)+((m>>(2+y))&1)]>0 for x in range(2) for y in range(2)) for m in range(16))
    return {'pairs':[[str(p) for p in row] for row in pairs], 'correlations':list(map(str,e)),
            'chsh':str(e[0]+e[1]+e[2]-e[3]),'minimum_probability':str(min(p for row in pairs for p in row)),
            'support_assignments':supported,'locally_supported_assignments':supported,
            'separator_lower':str(decision.analysis.common_lower),'separator_upper':str(decision.analysis.common_upper),'violating_mask':decision.violating_mask}
