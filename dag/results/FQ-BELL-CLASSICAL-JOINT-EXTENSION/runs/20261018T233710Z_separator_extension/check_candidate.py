"""Independent extension/obstruction checker. Does not import either solver.

All math quantities are exact canonical rational strings. Native compilation and
source scope are separate gates; a label match cannot accept a theorem.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys


def require(condition,message):
    if not condition:raise ValueError(message)


def _object(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,'G1_SCHEMA:duplicate_key');result[k]=v
    return result


def _nonexact(value):raise ValueError('G1_SCHEMA:nonexact_json')


def load(path):return json.loads(Path(path).read_bytes(),object_pairs_hook=_object,parse_float=_nonexact,parse_constant=_nonexact)


def exact(x):
    require(type(x) is str,'G1_SCHEMA:rational_string')
    try:q=Q(x)
    except (ValueError,ZeroDivisionError) as e:raise ValueError('G1_SCHEMA:rational') from e
    require(str(q)==x,'G1_SCHEMA:canonical_rational');return q


def valid_pairs(raw):
    require(type(raw) is list and len(raw)==4 and all(type(row) is list and len(row)==4 for row in raw),'G1_SCHEMA:pair_shape')
    p=[list(map(exact,row)) for row in raw]
    require(all(min(row)>=0 and sum(row)==1 for row in p),'G3_WITNESS:pair_law')
    require(all(p[2*x][2]+p[2*x][3]==p[2*x+1][2]+p[2*x+1][3] for x in range(2)) and
            all(p[y][1]+p[y][3]==p[2+y][1]+p[2+y][3] for y in range(2)),'G3_WITNESS:compatibility')
    return p


def check_case(public,answer):
    fields={'id','status','lower','upper','facets','separator','triples','weights','violating_mask'}
    require(type(answer) is dict and set(answer)==fields and answer['id']==public['id'],'G1_SCHEMA:case_binding')
    p=valid_pairs(public['pairs'])
    # Independent route via shared single-party marginals and ++ cells.
    a=p[0][2]+p[0][3];c=p[2][2]+p[2][3]
    bounds=[]
    for y in range(2):
        b=p[y][1]+p[y][3];x=p[y][3];z=p[2+y][3]
        bounds.append((max(Q(0),x+z-b)+max(Q(0),a+c-x-z-1+b),min(x,z)+min(a-x,c-z)))
    require(list(map(exact,answer['lower']))==[b[0] for b in bounds] and list(map(exact,answer['upper']))==[b[1] for b in bounds],'G3_WITNESS:interval_values')
    e=[row[0]-row[1]-row[2]+row[3] for row in p]
    masks=[m for m in range(16) if bin(m).count('1')%2]
    facets=[sum((-1 if m&(1<<j) else 1)*e[j] for j in range(4)) for m in masks]
    require(list(map(exact,answer['facets']))==facets,'G3_WITNESS:facet_values')
    if answer['status']=='blocked':
        require(answer['weights'] is None and answer['triples'] is None and answer['separator'] is None,'G1_SCHEMA:blocked_fields')
        mask=answer['violating_mask']
        require(type(mask) is int and mask in masks and facets[masks.index(mask)]>2,'G4_COUNTERMODEL:nonextension_obstruction')
        require(max(b[0] for b in bounds)>min(b[1] for b in bounds),'G3_WITNESS:interval_gap')
        return 'blocked'
    require(answer['status']=='extended' and answer['violating_mask'] is None,'G1_SCHEMA:decision')
    r=exact(answer['separator']);require(max(b[0] for b in bounds)<=r<=min(b[1] for b in bounds),'G3_WITNESS:separator')
    raw=answer['weights'];require(type(raw) is list and len(raw)==16,'G1_SCHEMA:joint_shape')
    law=list(map(exact,raw));require(min(law)>=0 and sum(law)==1,'G3_WITNESS:joint_law')
    # Project the witness itself. No solver decision or forward verifier is used.
    for x in range(2):
        for y in range(2):
            row=[sum((law[m] for m in range(16) if (2*((m>>x)&1)+((m>>(2+y))&1))==cell),Q(0)) for cell in range(4)]
            require(row==p[2*x+y],'G3_WITNESS:pair_projection')
    ts=answer['triples'];require(type(ts) is list and len(ts)==2 and all(type(t) is list and len(t)==8 for t in ts),'G1_SCHEMA:triple_shape')
    triples=[list(map(exact,t)) for t in ts]
    for y,t in enumerate(triples):
        require(min(t)>=0 and sum(t)==1,'G3_WITNESS:triple_law')
        # Every claimed intermediate triple must be the corresponding marginal
        # of the final joint law, including all zero separator slices.
        projected=[sum((law[m] for m in range(16) if (m&3)+4*((m>>(2+y))&1)==k),Q(0)) for k in range(8)]
        require(projected==t,'G3_WITNESS:triple_projection')
    q=[triples[0][s]+triples[0][s+4] for s in range(4)]
    require(q==[triples[1][s]+triples[1][s+4] for s in range(4)] and q[3]==r,'G3_WITNESS:separator_match')
    for m in range(16):
        s=m&3;product=triples[0][s+4*((m>>2)&1)]*triples[1][s+4*((m>>3)&1)]
        require((law[m]==0 and product==0) if q[s]==0 else law[m]*q[s]==product,'G3_WITNESS:conditional_glue')
    require(all(f<=2 for f in facets),'G3_WITNESS:extended_facet')
    return 'extended'


def check(request_path,candidate_path):
    request=load(request_path);candidate=load(candidate_path)
    canonical=json.dumps(request['public_context'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
    require(hashlib.sha256(canonical).hexdigest()==request['input_sha256'],'G1_SCHEMA:context_digest')
    require(type(candidate) is dict and set(candidate)=={'schema_id','task_id','stage_id','attempt_id','input_sha256','scope','cases'},'G1_SCHEMA:fields')
    require(candidate['schema_id']=='finite-qm.bell-separator-certificate.v1','G1_SCHEMA:schema')
    for k in ('task_id','stage_id','attempt_id','input_sha256'):require(candidate[k]==request[k],'G1_SCHEMA:binding')
    public=request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']
    require(candidate['scope']==public['scope'],'G5_SCOPE:public_label_only')
    require(type(candidate['cases']) is list and len(candidate['cases'])==len(public['cases']),'G1_SCHEMA:case_count')
    counts={'extended':0,'blocked':0}
    for instance,answer in zip(public['cases'],candidate['cases']):counts[check_case(instance,answer)]+=1
    return {'candidate_sha256':hashlib.sha256(Path(candidate_path).read_bytes()).hexdigest(),'counts':counts,
            'claim':'Exact finite witnesses/obstructions and actual projections checked; no automatic theorem acceptance from scope labels.'}


if __name__=='__main__':print(json.dumps(check(*sys.argv[1:]),indent=2))
