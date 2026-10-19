"""Exact normalization and positive-ray classification of Born weight vectors.

This quotient is on nonnegative weight vectors. It does not classify amplitude
rays: Born weights forget relative phases before normalization.
"""
from fractions import Fraction as Q
from .pfp_exact import scalar


def weights(values):
    result=tuple(scalar(x) for x in values)
    if not result or min(result)<0 or sum(result)<=0:
        raise ValueError('nonnegative nonzero weight vector required')
    return result


def normalize(values):
    values=weights(values);total=sum(values)
    return tuple(x/total for x in values)


def born_weights(amplitudes):
    result=[]
    for pair in amplitudes:
        if len(pair)!=2:raise ValueError('Gaussian rational pair required')
        re,im=map(scalar,pair);result.append(re*re+im*im)
    return weights(result)


def certify(left,right,positive_scale):
    left,right=weights(left),weights(right);c=scalar(positive_scale)
    if len(left)!=len(right):raise ValueError('same weight carrier required')
    if c<=0:raise ValueError('positive scale required')
    nl,nr=normalize(left),normalize(right);same=nl==nr
    minor=None
    if not same:
        minor=next(({'indices':[i,j],'value':str(right[i]*left[j]-left[i]*right[j])} for i in range(len(left)) for j in range(i+1,len(left)) if right[i]*left[j]!=left[i]*right[j]),None)
        if minor is None:raise ArithmeticError('unequal normalized vectors without a nonzero minor')
    return {'left_sum':str(sum(left)),'right_sum':str(sum(right)),'normalized':list(map(str,nl)),
            'normalized_twice':list(map(str,normalize(nl))),'normalized_scaled':list(map(str,normalize(tuple(c*x for x in left)))),
            'same_weight_ray':same,'ray_scale':str(sum(right)/sum(left)) if same else None,'separating_minor':minor}
