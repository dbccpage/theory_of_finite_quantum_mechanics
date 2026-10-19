"""Independent Mobius-polynomial quotient arithmetic and declared-scope checking."""
from fractions import Fraction as Q
from functools import lru_cache
from math import gcd,lcm
from pathlib import Path
import sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file());sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import bound,require,vector
TASK='FQ-CARRIER-CONTRACT-V2'
ARRAYS=('source_coefficients','conjugate_coefficients','norm_coefficients','embedded_coefficients','via_intermediate_coefficients','embedded_norm_coefficients','norm_after_embedding','embedded_sum','sum_after_embedding','embedded_product','product_after_embedding','embedded_conjugate','conjugate_after_embedding')


def trim(a):
    while len(a)>1 and a[-1]==0:a.pop()
    return a


def multiply(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return trim(out)


def quotient(a,b):
    a=list(map(Q,a));result=[Q(0)]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and any(a):
        k=len(a)-len(b);c=a[-1]/b[-1];result[k]=c
        for i,x in enumerate(b):a[k+i]-=c*x
        trim(a)
    require(not any(a),'G3_WITNESS:cyclotomic_exact_division')
    return trim(result)


def mobius(n):
    factors=0;p=2
    while p*p<=n:
        if n%p==0:
            n//=p;factors+=1
            if n%p==0:return 0
        p+=1
    if n>1:factors+=1
    return -1 if factors%2 else 1


@lru_cache(None)
def phi(n):
    numerator,denominator=[1],[1]
    for d in range(1,n+1):
        if n%d:continue
        mu=mobius(n//d);factor=[-1]+[0]*(d-1)+[1]
        if mu==1:numerator=multiply(numerator,factor)
        elif mu==-1:denominator=multiply(denominator,factor)
    result=quotient(numerator,denominator);require(all(x.denominator==1 for x in result),'G3_WITNESS:cyclotomic_integrality')
    return tuple(int(x) for x in result)


def reduce(a,n):
    a=list(map(Q,a));modulus=phi(n);degree=len(modulus)-1
    while len(a)>degree:
        i=len(a)-1;c=a[-1]
        for j,x in enumerate(modulus):a[i-degree+j]-=c*x
        a.pop()
    return a+[Q(0)]*(degree-len(a))


def power(n,k):
    k%=n;return reduce([0]*k+[1],n)


def add(a,b):return [x+y for x,y in zip(a,b)]
def mul(a,b,n):return reduce(multiply(a,b),n)
def conjugate(a,n):
    out=reduce([0],n)
    for i,x in enumerate(a):out=add(out,[x*c for c in power(n,-i)])
    return out
def lift(a,n,target):
    require(target%n==0,'G3_WITNESS:lift_hypothesis');out=reduce([0],target)
    for i,x in enumerate(a):out=add(out,[x*c for c in power(target,i*(target//n))])
    return out


def check(request,candidate):
    _,certificate,public=bound(request,candidate,TASK);data=certificate['data']
    require(type(data) is dict and set(data)=={'inventory_target_ids','inventory_conductors','distinct_conductors','label_lcm','samples','declaration_boundary'},'G1_SCHEMA:data')
    ids=[t['target_id'] for t in public['targets']];conductors=[t['conductor'] for t in public['targets']]
    require(len(ids)==len(set(ids))==23 and all(type(x) is int and x>0 for x in ids+conductors),'G3_WITNESS:source_inventory')
    require(data['inventory_target_ids']==ids and data['inventory_conductors']==conductors and all(type(x) is int for x in data['inventory_target_ids']+data['inventory_conductors']),'G3_WITNESS:inventory_binding')
    require(type(data['label_lcm']) is int and data['label_lcm']==lcm(*conductors)==120 and data['distinct_conductors']==sorted(set(conductors))==[1,2,3,4,5,8,12],'G3_WITNESS:label_lcm')
    require(type(data['samples']) is list and len(data['samples'])==len(public['samples']),'G1_SCHEMA:sample_count')
    for p,a in zip(public['samples'],data['samples']):
        require(type(a) is dict and set(a)=={'id','source_conductor','intermediate_conductor','target_conductor','source_polynomial','target_polynomial',*ARRAYS} and a['id']==p['id'],'G1_SCHEMA:sample_fields')
        n,mid,target=(p[k] for k in ('source_conductor','intermediate_conductor','target_conductor'))
        require(all(type(a[k]) is int and a[k]==p[k] for k in ('source_conductor','intermediate_conductor','target_conductor')) and mid%n==0 and target%mid==0,'G3_WITNESS:directed_chain')
        require(a['source_polynomial']==list(phi(n)) and a['target_polynomial']==list(phi(target)) and all(type(x) is int for x in a['source_polynomial']+a['target_polynomial']),'G3_WITNESS:actual_cyclotomic_modulus')
        x,y=vector(p['a'],len(phi(n))-1),vector(p['b'],len(phi(n))-1);cx=conjugate(x,n);norm=mul(x,cx,n);ex=lift(x,n,target);ey=lift(y,n,target)
        expected={'source_coefficients':x,'conjugate_coefficients':cx,'norm_coefficients':norm,'embedded_coefficients':ex,'via_intermediate_coefficients':lift(lift(x,n,mid),mid,target),'embedded_norm_coefficients':lift(norm,n,target),'norm_after_embedding':mul(ex,conjugate(ex,target),target),'embedded_sum':lift(add(x,y),n,target),'sum_after_embedding':add(ex,ey),'embedded_product':lift(mul(x,y,n),n,target),'product_after_embedding':mul(ex,ey,target),'embedded_conjugate':lift(cx,n,target),'conjugate_after_embedding':conjugate(ex,target)}
        for key,value in expected.items():require(vector(a[key],len(value))==value,'G3_WITNESS:coefficient_identity:'+key)
        require(norm==conjugate(norm,n),'G3_WITNESS:real_fixed_norm')
        # The substituted source relation must actually vanish in the target quotient.
        relation=reduce([0],target)
        for i,c in enumerate(phi(n)):relation=add(relation,[Q(c)*z for z in power(target,i*(target//n))])
        require(not any(relation),'G3_WITNESS:source_relation_transport')
    boundary=data['declaration_boundary'];require(type(boundary) is dict and boundary=={'colimit_constructed':False,'Kronecker_Weber':'DECLARED','field_minimality_proved':False,'all_target_amplitudes_verified':False} and all(type(boundary[k]) is bool for k in ('colimit_constructed','field_minimality_proved','all_target_amplitudes_verified')),'G5_SCOPE:declaration_promoted')
    return {'inventory_targets':len(ids),'selected_field_elements_checked':len(data['samples']),'target_polynomial_degree':len(phi(120))-1,'declared_colimit_or_KW_proof':False,'scope':'Actual finite quotient arithmetic and selected lift compositions; label LCM is not field minimality or complete target-amplitude coverage.'}


if __name__=='__main__':
    import json
    print(json.dumps(check(*sys.argv[1:]),indent=2))
