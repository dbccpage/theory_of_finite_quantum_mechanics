"""Independent weight-ray certificate equations; no native normalizer import."""
from fractions import Fraction as Q
from pathlib import Path
import sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file());sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import bound,require,rational,vector
TASK='FQ-BORN-NORMALIZATION-REDUNDANCY'


def case(public,answer):
    fields={'id','left_sum','right_sum','normalized','normalized_twice','normalized_scaled','same_weight_ray','ray_scale','separating_minor'}
    require(type(answer) is dict and set(answer)==fields and answer['id']==public['id'],'G1_SCHEMA:case_fields')
    n=len(public['left']);left=vector(public['left'],n);right=vector(public['right'],n);c=rational(public['positive_scale'])
    require(n>0 and min(left)>=0 and min(right)>=0 and sum(left)>0 and sum(right)>0 and c>0,'G3_WITNESS:admitted_weights')
    lmass,rmass=sum(left),sum(right)
    require(rational(answer['left_sum'])==lmass and rational(answer['right_sum'])==rmass,'G3_WITNESS:mass')
    normalized=vector(answer['normalized'],n)
    require(sum(normalized)==1 and all(q*lmass==w for q,w in zip(normalized,left)),'G3_WITNESS:normalization')
    require(vector(answer['normalized_twice'],n)==normalized and vector(answer['normalized_scaled'],n)==normalized,'G3_WITNESS:idempotent_scale')
    same=all(w*rmass==v*lmass for w,v in zip(left,right))
    require(type(answer['same_weight_ray']) is bool and answer['same_weight_ray']==same,'G3_WITNESS:ray_class')
    if same:
        scale=rational(answer['ray_scale']);require(scale>0 and all(v==scale*w for w,v in zip(left,right)) and answer['separating_minor'] is None,'G3_WITNESS:ray_scalar')
    else:
        minor=answer['separating_minor'];require(answer['ray_scale'] is None and type(minor) is dict and set(minor)=={'indices','value'},'G1_SCHEMA:minor')
        ij=minor['indices'];require(type(ij) is list and len(ij)==2 and all(type(i) is int for i in ij) and 0<=ij[0]<ij[1]<n,'G1_SCHEMA:minor_indices')
        i,j=ij;d=right[i]*left[j]-left[i]*right[j]
        require(d!=0 and rational(minor['value'])==d,'G4_COUNTERMODEL:separating_minor')
    return same


def amplitude(public,answer):
    require(type(answer) is dict and set(answer)=={'left_weights','right_weights','normalized_left','normalized_right','amplitude_minor'},'G1_SCHEMA:amplitude_fields')
    a=[vector(z,2) for z in public['left']];b=[vector(z,2) for z in public['right']]
    require(len(a)==len(b)==2,'G1_SCHEMA:amplitude_size')
    w=[[x*x+y*y for x,y in p] for p in (a,b)]
    require(vector(answer['left_weights'],2)==w[0] and vector(answer['right_weights'],2)==w[1] and w[0]==w[1],'G3_WITNESS:Born_weights')
    require(vector(answer['normalized_left'],2)==[x/sum(w[0]) for x in w[0]] and vector(answer['normalized_right'],2)==[x/sum(w[1]) for x in w[1]],'G3_WITNESS:amplitude_normalization')
    mul=lambda x,y:(x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    u,v=mul(a[0],b[1]),mul(a[1],b[0]);d=[u[i]-v[i] for i in range(2)]
    require(vector(answer['amplitude_minor'],2)==d and any(d),'G4_COUNTERMODEL:amplitude_minor')


def check(request,candidate):
    _,certificate,public=bound(request,candidate,TASK);data=certificate['data']
    require(type(data) is dict and set(data)=={'cases','amplitude_control'},'G1_SCHEMA:data')
    require(type(data['cases']) is list and len(data['cases'])==len(public['cases']) and len({p['id'] for p in public['cases']})==len(public['cases']),'G1_SCHEMA:case_count')
    results=[case(p,a) for p,a in zip(public['cases'],data['cases'])];amplitude(public['amplitude_control'],data['amplitude_control'])
    return {'cases_checked':len(results),'same_weight_rays':sum(results),'different_weight_rays':len(results)-sum(results),'phase_control':'same Born weights, actual nonzero complex amplitude minor; no amplitude-ray classification'}


if __name__=='__main__':
    import json
    print(json.dumps(check(*sys.argv[1:]),indent=2))
