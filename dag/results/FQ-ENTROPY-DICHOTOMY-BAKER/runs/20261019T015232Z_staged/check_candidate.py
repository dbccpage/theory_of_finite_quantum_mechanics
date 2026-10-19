"""Independently recompute integer power sums and rational series certificates."""
from fractions import Fraction as Q
from math import gcd
from pathlib import Path
import sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file());sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import bound,require,vector,rational
TASK='FQ-ENTROPY-DICHOTOMY-BAKER'
def check(request,candidate):
    _,c,p=bound(request,candidate,TASK);d=c['data']
    require(type(d) is dict and set(d)=={'cases'} and type(d['cases']) is list and len(d['cases'])==len(p['cases']),'G1_SCHEMA:cases')
    for inp,a in zip(p['cases'],d['cases']):
        fields={'id','spectrum','denominator','integer_weights','terms','purity','purity_deficit','integer_power_sums','power_traces','term_bounds','entropy_lower','entropy_upper','interval_width','classification','log_base','Baker_status'}
        require(type(a) is dict and set(a)==fields and a['id']==inp['id'],'G1_SCHEMA:case')
        ps=vector(inp['spectrum'],len(inp['spectrum']));require(ps and min(ps)>=0 and sum(ps)==1,'G3_WITNESS:spectrum')
        require(vector(a['spectrum'],len(ps))==ps and type(a['terms']) is int and a['terms']==inp['terms'] and 1<=a['terms']<=256,'G3_WITNESS:input_binding')
        den=1
        for x in ps:den=den*x.denominator//gcd(den,x.denominator)
        weights=[int(x*den) for x in ps]
        require(rational(a['denominator'])==den and a['denominator']==str(den) and a['integer_weights']==list(map(str,weights)),'G3_WITNESS:integer_spectrum')
        purity=sum(x*x for x in ps);require(rational(a['purity'])==purity and rational(a['purity_deficit'])==1-purity,'G3_WITNESS:purity')
        require(a['integer_power_sums']==[str(sum(w**k for w in weights)) for k in (2,3,4)] and vector(a['power_traces'],3)==[Q(sum(w**k for w in weights),den**k) for k in (2,3,4)],'G3_WITNESS:actual_Renyi_powers')
        require(type(a['term_bounds']) is list and len(a['term_bounds'])==len(ps),'G1_SCHEMA:term_count');lower=Q(0);upper=Q(0)
        for x,b in zip(ps,a['term_bounds']):
            require(type(b) is dict and set(b)=={'mode','t','partial','tail','lower','upper'},'G1_SCHEMA:term')
            if x==0:t=partial=tail=lo=hi=Q(0);mode='zero_weight'
            else:
                n=a['terms'];t=(x-1)/(x+1);u=-t;require(0<=u<1,'G3_WITNESS:series_domain')
                # Positive-series entropy lower sum, independently formed from u.
                h=sum((Q(2,2*k+1)*u**(2*k+1) for k in range(n)),Q(0));partial=-h
                tail=Q(2,2*n+1)*u**(2*n+1)/(1-u*u);lo=x*h;hi=x*(h+tail);mode='positive_weight'
            require(b['mode']==mode and [rational(b[k]) for k in ('t','partial','tail','lower','upper')]==[t,partial,tail,lo,hi],'G3_WITNESS:series_and_remainder')
            lower+=lo;upper+=hi
        require([rational(a[k]) for k in ('entropy_lower','entropy_upper','interval_width')]==[lower,upper,upper-lower] and lower>=0 and upper>=lower,'G3_WITNESS:entropy_interval')
        require(a['classification']==('PURE' if any(x==1 for x in ps) else 'MIXED') and ((purity==1)==any(x==1 for x in ps)),'G3_WITNESS:purity_classification')
        require(a['log_base']=='natural' and a['Baker_status']=='EXPLICIT_UNPAID_HYPOTHESIS','G5_SCOPE:Baker_or_log_units')
        if a['classification']=='MIXED':require(lower>0,'G3_WITNESS:mixed_positive_lower')
    return {'spectra':len(d['cases']),'integer_Renyi_orders':[2,3,4],'log_base':'natural','Baker_hypothesis_discharged':False,'scope':'Exact rational series arithmetic and interval derivation; source kernel purity/positivity, conditional Baker theorem and log cancellation remain distinct.'}
if __name__=='__main__':
    import json
    print(json.dumps(check(*sys.argv[1:]),indent=2))
