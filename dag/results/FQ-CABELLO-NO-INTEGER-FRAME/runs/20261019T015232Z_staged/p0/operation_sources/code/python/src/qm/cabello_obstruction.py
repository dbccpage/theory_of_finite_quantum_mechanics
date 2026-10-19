"""Integer frame parity and an actual normalized indefinite frame function."""
from functools import reduce
from math import gcd
from fractions import Fraction as Q
from .cabello_frame import system,quadratic
from .pfp_exact import matrix,trace,transpose


def parity(frames,n):
    if type(n) is not int or n<=0 or not frames:raise ValueError('nonempty integer incidence required')
    if any(any(type(i) is not int or not 0<=i<n for i in f) for f in frames):raise ValueError('declared ray index required')
    coefficients=[sum(f.count(i) for f in frames) for i in range(n)]
    divisor=reduce(gcd,coefficients,0);rhs=len(frames)
    if divisor==0:raise ValueError('zero combined row needs a separate contract')
    return {'multipliers':[1]*len(frames),'combined_coefficients':coefficients,'combined_rhs':rhs,'divisor':divisor,'remainder':rhs%divisor}


def certify(rays,frames,raw,negative_vector,even_frames,even_assignment):
    rays,frames=system(rays,frames);raw=matrix(raw)
    if len(raw)!=4 or len(raw[0])!=4 or raw!=transpose(raw):raise ValueError('real symmetric four-matrix required')
    if any(x.denominator!=1 for row in raw for x in row):raise ValueError('source raw matrix must be integer')
    d=trace(raw)
    if d<=0:raise ValueError('positive trace for normalization required')
    h=tuple(tuple(x/d for x in row) for row in raw)
    if len(negative_vector)!=4 or any(type(x) is not int for x in negative_vector):raise ValueError('explicit integer negative vector required')
    weights=[quadratic(h,r)/sum(x*x for x in r) for r in rays]
    sums=[sum(weights[i] for i in f) for f in frames]
    if min(weights)<0 or max(weights)>1 or any(x!=1 for x in sums):raise ValueError('admitted nonnegative normalized frame function required')
    value=quadratic(h,negative_vector)
    if value>=0:raise ValueError('actual negative quadratic witness required')
    raw_values=[quadratic(raw,r) for r in rays]
    remainders=[int(4*q)%sum(x*x for x in r) for q,r in zip(raw_values,rays)]
    even=parity(even_frames,len(even_assignment));control_sums=[sum(even_assignment[i] for i in f) for f in even_frames]
    if any(type(x) is not int for x in even_assignment) or any(x!=1 for x in control_sums):raise ValueError('actual integer assignment control required')
    return {'parity_main':parity(frames,len(rays)),
            'frame_counterexample':{'denominator':str(d),'normalized_matrix':[[str(x) for x in row] for row in h],
                                    'weights':list(map(str,weights)),'frame_sums':list(map(str,sums)),
                                    'negative_vector':list(negative_vector),'raw_negative_value':str(quadratic(raw,negative_vector)),
                                    'negative_value':str(value),'scaled_readout_remainders':remainders},
            'even_control':{**even,'assignment':list(even_assignment),'context_sums':control_sums}}
