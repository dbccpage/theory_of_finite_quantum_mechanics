"""Independent direct-index Born checker; does not import a native solver."""
from fractions import Fraction as Q
from pathlib import Path
import sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file())
sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import bound,require,rational,vector

TASK='FQ-BELL-RATIONAL-VIOLATION-14-5'


def mat(value,n):
    require(type(value) is list and len(value)==n,'G1_SCHEMA:matrix_shape')
    return [vector(row,n) for row in value]


def case(public,answer):
    require(type(answer) is dict and set(answer)=={'id','pairs','correlations','chsh','minimum_probability','support_assignments','separator_lower','separator_upper','violating_mask'} and answer['id']==public['id'],'G1_SCHEMA:case_fields')
    rho=mat(public['rho'],4);alice=[mat(x,2) for x in public['alice']];bob=[mat(x,2) for x in public['bob']]
    require(len(alice)==len(bob)==2,'G1_SCHEMA:setting_count')
    gram=[(rational(term['weight']),vector(term['vector'],4)) for term in public['gram']]
    require(bool(gram) and all(w>=0 for w,_ in gram),'G3_WITNESS:gram_weights')
    require(all(rho[i][j]==sum(w*v[i]*v[j] for w,v in gram) for i in range(4) for j in range(4)) and sum(rho[i][i] for i in range(4))==1,'G3_WITNESS:density')
    for a in alice+bob:
        require(all(a[i][j]==a[j][i] and sum(a[i][k]*a[k][j] for k in range(2))==int(i==j) for i in range(2) for j in range(2)),'G3_WITNESS:observable')
    probabilities=[]
    for a in alice:
        for b in bob:
            probabilities.append([sum(rho[2*i+k][2*j+l]*(Q(i==j)+s*a[j][i])*(Q(k==l)+t*b[l][k])/4 for i in range(2) for j in range(2) for k in range(2) for l in range(2)) for s in (-1,1) for t in (-1,1)])
    actual=[vector(row,4) for row in answer['pairs']]
    require(len(actual)==4 and actual==probabilities,'G3_WITNESS:Born_pairs')
    require(all(min(row)>=0 and sum(row)==1 for row in actual),'G3_WITNESS:pair_law')
    e=[p[0]-p[1]-p[2]+p[3] for p in probabilities]
    require(vector(answer['correlations'],4)==e and rational(answer['chsh'])==e[0]+e[1]+e[2]-e[3],'G3_WITNESS:correlations')
    require(rational(answer['minimum_probability'])==min(x for row in actual for x in row),'G3_WITNESS:minimum')
    support=sum(all(actual[2*x+y][2*((m>>x)&1)+((m>>(2+y))&1)]>0 for x in range(2) for y in range(2)) for m in range(16))
    require(type(answer['support_assignments']) is int and answer['support_assignments']==support,'G3_WITNESS:support')
    a=actual[0][2]+actual[0][3];c=actual[2][2]+actual[2][3];bounds=[]
    for y in range(2):
        b=actual[y][1]+actual[y][3];x=actual[y][3];z=actual[2+y][3]
        bounds.append((max(Q(0),x+z-b)+max(Q(0),a+c-x-z-1+b),min(x,z)+min(a-x,c-z)))
    lo,hi=max(t[0] for t in bounds),min(t[1] for t in bounds)
    require(rational(answer['separator_lower'])==lo and rational(answer['separator_upper'])==hi,'G3_WITNESS:separator')
    mask=answer['violating_mask']
    if lo>hi:
        require(type(mask) is int and mask in (1,2,4,7,8,11,13,14) and sum((-1 if mask&(1<<j) else 1)*e[j] for j in range(4))>2,'G4_COUNTERMODEL:facet_obstruction')
    else:require(mask is None,'G3_WITNESS:false_obstruction')
    return {'chsh':answer['chsh'],'support_assignments':support,'interval_empty':lo>hi}


def check(request,candidate):
    request,candidate,public=bound(request,candidate,TASK)
    require(type(candidate['data']) is dict and set(candidate['data'])=={'cases'},'G1_SCHEMA:data')
    answers=candidate['data']['cases'];inputs=public['cases']
    require(type(answers) is list and len(answers)==len(inputs) and len({p['id'] for p in inputs})==len(inputs),'G1_SCHEMA:case_count')
    results=[case(p,a) for p,a in zip(inputs,answers)]
    main=results[[p['id'] for p in inputs].index('rational_triangle')]
    require(Q(main['chsh'])==Q(14,5) and main['support_assignments']==16 and main['interval_empty'],'G3_WITNESS:stated_target')
    return {'cases_checked':len(results),'results':results,'scope':'Exact admitted tensor/Born construction and a signed facet obstruction; arbitrary rational joint-law transport is not silently added to Lean.'}


if __name__=='__main__':
    import json
    print(json.dumps(check(*sys.argv[1:]),indent=2))
