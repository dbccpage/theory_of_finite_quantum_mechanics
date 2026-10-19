"""Actual integer-row combination and normalized counterexample equations."""
from fractions import Fraction as Q
from functools import reduce
from math import gcd
from pathlib import Path
import sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file());sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import bound,require,vector,rational
TASK='FQ-CABELLO-NO-INTEGER-FRAME'


def parity(frames,n,certificate):
    require(type(certificate) is dict and set(certificate)>={'multipliers','combined_coefficients','combined_rhs','divisor','remainder'},'G1_SCHEMA:parity_fields')
    multipliers=certificate['multipliers'];require(type(multipliers) is list and len(multipliers)==len(frames) and all(type(x) is int for x in multipliers),'G1_SCHEMA:multipliers')
    coefficients=[sum(w*frame.count(j) for w,frame in zip(multipliers,frames)) for j in range(n)];rhs=sum(multipliers);divisor=reduce(gcd,coefficients,0)
    require(certificate['combined_coefficients']==coefficients and all(type(x) is int for x in certificate['combined_coefficients']) and type(certificate['combined_rhs']) is int and certificate['combined_rhs']==rhs,'G3_WITNESS:combined_row')
    require(divisor>0 and type(certificate['divisor']) is int and certificate['divisor']==divisor and type(certificate['remainder']) is int and certificate['remainder']==rhs%divisor,'G3_WITNESS:divisibility')
    return rhs%divisor


def check(request,candidate):
    _,certificate,public=bound(request,candidate,TASK);data=certificate['data']
    require(type(data) is dict and set(data)=={'parity_main','frame_counterexample','even_control'},'G1_SCHEMA:data')
    rays,frames=public['rays'],public['frames'];require(len(rays)==18 and len(frames)==9 and all(len(r)==4 and all(type(x) is int for x in r) and any(r) for r in rays),'G1_SCHEMA:geometry')
    for f in frames:
        require(len(f)==4 and len(set(f))==4 and all(type(i) is int and 0<=i<18 for i in f),'G1_SCHEMA:frames')
        require(all(sum(rays[i][k]*rays[j][k] for k in range(4))==0 for i in f for j in f if i!=j),'G3_WITNESS:orthogonality')
    require(set(data['parity_main'])=={'multipliers','combined_coefficients','combined_rhs','divisor','remainder'} and parity(frames,18,data['parity_main'])!=0,'G4_COUNTERMODEL:no_integer_obstruction')
    raw=[[Q(x) for x in row] for row in public['raw_matrix']];require(len(raw)==4 and all(len(row)==4 for row in raw) and all(raw[i][j]==raw[j][i] for i in range(4) for j in range(4)),'G3_WITNESS:symmetric_raw_matrix')
    d=sum(raw[i][i] for i in range(4));require(d>0,'G3_WITNESS:positive_scale');c=data['frame_counterexample']
    require(type(c) is dict and set(c)=={'denominator','normalized_matrix','weights','frame_sums','negative_vector','raw_negative_value','negative_value','scaled_readout_remainders'},'G1_SCHEMA:counterexample_fields')
    require(rational(c['denominator'])==d,'G3_WITNESS:normalization_scale');h=[vector(row,4) for row in c['normalized_matrix']]
    require(len(h)==4 and all(h[i][j]*d==raw[i][j] for i in range(4) for j in range(4)),'G3_WITNESS:normalized_matrix')
    quad=lambda m,v:sum(m[i][j]*v[i]*v[j] for i in range(4) for j in range(4))
    w=vector(c['weights'],18);s=vector(c['frame_sums'],9)
    require(all(0<=f<=1 and f*sum(x*x for x in r)==quad(h,r) for r,f in zip(rays,w)) and s==[sum(w[j] for j in f) for f in frames] and s==[1]*9,'G3_WITNESS:actual_frame_readout')
    v=c['negative_vector'];require(v==public['negative_vector'] and all(type(x) is int for x in v),'G1_SCHEMA:vector_binding')
    require(rational(c['raw_negative_value'])==quad(raw,v) and rational(c['negative_value'])==quad(h,v)<0,'G4_COUNTERMODEL:actual_negative_quadratic')
    rem=c['scaled_readout_remainders'];actual=[int(4*quad(raw,r))%sum(x*x for x in r) for r in rays]
    require(type(rem) is list and len(rem)==18 and all(type(x) is int for x in rem) and rem==actual==[0]*18,'G3_WITNESS:unrounded_scaled_readout')
    even=public['even_control'];control=data['even_control'];require(type(control) is dict and set(control)=={'multipliers','combined_coefficients','combined_rhs','divisor','remainder','assignment','context_sums'},'G1_SCHEMA:even_control')
    require(parity(even['frames'],len(even['assignment']),control)==0 and control['assignment']==even['assignment'] and all(type(x) is int for x in control['assignment']),'G3_WITNESS:even_control_assignment')
    sums=[sum(control['assignment'][j] for j in f) for f in even['frames']]
    require(control['context_sums']==sums==[1]*len(even['frames']),'G3_WITNESS:even_control_equations')
    return {'integer_obstruction':{'divisor':data['parity_main']['divisor'],'rhs':data['parity_main']['combined_rhs'],'remainder':data['parity_main']['remainder']},'all_normalized_frame_sums_checked':9,'all_ray_values_checked':18,'negative_quadratic':c['negative_value'],'even_control_has_actual_integer_assignment':True,'scope':'Exact universal integer parity anchor plus the actual real-symmetric finite-frame counterexample; no complex-Hermitian theorem or arbitrary real PSD transport is imported.'}


if __name__=='__main__':
    import json
    print(json.dumps(check(*sys.argv[1:]),indent=2))
