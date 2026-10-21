"""Exact spectra, integer power sums, and rational atanh-series bounds.

Natural logarithms are used. The real analytic remainder transport is described
in the result folder; no native number certifies Baker's cited hypothesis.
"""
from fractions import Fraction as Q
from math import lcm
def _admit_exact_scalar(x, max_bits=1024) -> Q:
    if type(x) is bool or isinstance(x, float):
        raise ValueError("unadmitted float or boolean on exact path")
    if isinstance(x, (int, Q)):
        num = x.numerator if isinstance(x, Q) else x
        den = x.denominator if isinstance(x, Q) else 1
        if type(num) is not int or type(den) is not int:
            raise ValueError("scalar numerator and denominator must be int")
        if num.bit_length() > max_bits or den.bit_length() > max_bits:
            raise ValueError(f"integer exceeds {max_bits} bits")
        return Q(num, den)
    raise ValueError(f"unadmitted scalar type: {type(x)}")


def certify(spectrum, terms):
    if type(terms) is not int or not 1 <= terms <= 256:
        raise ValueError("explicit positive finite series budget <=256 required")
    if not spectrum or len(spectrum) > 256:
        raise ValueError("exact nonempty spectrum <=256 entries required")
    p = [_admit_exact_scalar(x) for x in spectrum]
    if min(p) < 0 or sum(p) != 1:
        raise ValueError("nonnegative normalized spectrum required")
    d=lcm(*(x.denominator for x in p));weights=[int(x*d) for x in p];purity=sum(x*x for x in p);bounds=[]
    for x in p:
        if x==0:bounds.append({'mode':'zero_weight','t':'0','partial':'0','tail':'0','lower':'0','upper':'0'});continue
        t=(x-1)/(x+1);s=2*sum((t**(2*k+1)/Q(2*k+1) for k in range(terms)),Q(0));tail=2*abs(t)**(2*terms+1)/(Q(2*terms+1)*(1-t*t));lo=-x*s;hi=lo+x*tail
        bounds.append({'mode':'positive_weight','t':str(t),'partial':str(s),'tail':str(tail),'lower':str(lo),'upper':str(hi)})
    lo=sum((Q(x['lower']) for x in bounds),Q(0));hi=sum((Q(x['upper']) for x in bounds),Q(0))
    return {'spectrum':list(map(str,p)),'denominator':str(d),'integer_weights':list(map(str,weights)),'terms':terms,'purity':str(purity),'purity_deficit':str(1-purity),'integer_power_sums':[str(sum(w**k for w in weights)) for k in (2,3,4)],'power_traces':[str(sum(x**k for x in p)) for k in (2,3,4)],'term_bounds':bounds,'entropy_lower':str(lo),'entropy_upper':str(hi),'interval_width':str(hi-lo),'classification':'PURE' if purity==1 else 'MIXED','log_base':'natural','Baker_status':'EXPLICIT_UNPAID_HYPOTHESIS'}
