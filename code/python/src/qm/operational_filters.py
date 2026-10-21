"""Exact finite reset-family witnesses; no unconditional tomography inference."""
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

_spec=importlib.util.spec_from_file_location('filter_matrix_algebra',Path(__file__).with_name('operational_tomography.py'))
a=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(a)
PREMISES=(
    'field-linear carriers, positive cones and normalization are supplied',
    'test followed by preparation is an admitted selective operation',
    'global separating effects and spanning preparations suffice for irreducibility',
    'product-test reset irreducibility is equivalent to tomography',
    'global reset descent is not independently derived from primitives',
)
MODELS={'classical_product':(4,4,4,True), 'doubled_visible':(8,4,4,True),
        'doubled_all_preparations':(8,8,4,True), 'doubled_global_tests':(8,8,8,False)}


def require(ok,code):
    if not ok: raise ValueError(code)


def verify(raw):
    require(len(raw)<1_000_000,'SIZE_LIMIT')
    obj=json.loads(raw,object_pairs_hook=a.no_duplicates)
    require(type(obj) is dict and set(obj)=={'schema','authority_effect','premises','models'},'ENVELOPE')
    require(obj['schema']=='operational-filter-family.v1' and obj['authority_effect']=='None','SCOPE')
    require(obj['premises']==list(PREMISES),'PREMISES')
    require(type(obj['models']) is dict and set(obj['models'])==set(MODELS),'COVERAGE')
    parsed={}
    # Check every supplied matrix and all operation counts before numeric analysis.
    for name,(n,np,ne,descends) in MODELS.items():
        v=obj['models'][name]
        require(type(v) is dict and set(v)=={'state_dimension','local_frame_sizes','observe','prepare',
            'preparations','effects','filters','coordinate_filters'},'MODEL_FIELDS')
        require(type(v['state_dimension']) is int and v['state_dimension']==n,'DIMENSION')
        require(type(v['local_frame_sizes']) is list and all(type(x) is int for x in v['local_frame_sizes'])
                and v['local_frame_sizes']==[2,2],'LOCAL_FRAMES')
        m=a.parse_matrix(v['observe'],4,n);r=a.parse_matrix(v['prepare'],n,4)
        p=a.parse_matrix(v['preparations'],n,np);e=a.parse_matrix(v['effects'],ne,n)
        expected_m=a.identity(4) if n==4 else [row+row for row in a.identity(4)]
        expected_r=a.identity(4) if n==4 else [[x/2 for x in row] for row in a.identity(4)]*2
        require(m==expected_m and r==expected_r,'CALIBRATION_MODEL')
        require(p==(r if np==4 else a.identity(8)) and e==(m if ne==4 else a.identity(8)),'RESET_MODEL')
        require(type(v['filters']) is list and type(v['coordinate_filters']) is list
                and len(v['filters'])==len(v['coordinate_filters'])==np*ne,'OPERATION_COVERAGE')
        ts=[a.parse_matrix(t,n,n) for t in v['filters']]
        ls=[a.parse_matrix(l,4,4) for l in v['coordinate_filters']]
        for i in range(np):
            for j in range(ne):
                t=[[p[k][i]*e[j][l] for l in range(n)] for k in range(n)]
                require(ts[i*ne+j]==t,'RESET_EQUATION')
                require(ls[i*ne+j]==a.multiply(a.multiply(m,t),r),'COORDINATE_ACTION')
        parsed[name]=(m,r,p,e,ts,ls)
    reports={}
    for name,(m,r,p,e,ts,ls) in parsed.items():
        n,np,ne,descends=MODELS[name]
        out=a.analyze(m,r,ts,ls)
        require(out['calibrated'] and out['positive_subnormalized_filters'],'OUTCOME_FILTER')
        require(all(sum(row[j] for row in p)==1 for j in range(np)) and all(x>=0 for row in p for x in row),'PREPARATIONS')
        require(all(0<=x<=1 for row in e for x in row),'EFFECT_INTERVAL')
        factors=e==a.multiply(a.multiply(e,r),m)
        require(factors==descends and out['descent']==descends,'DESCENT_FACTOR_EQUIVALENCE')
        pr,er=a.rank(p),a.rank(e)
        require(out['operator_span_rank']==pr*er==np*ne,'RESET_SPAN')
        require(out['full_operator_span']==(name in ('classical_product','doubled_global_tests')),'IRREDUCIBLE_CONTROL')
        h=a.subtract(a.identity(n),a.multiply(r,m))
        annihilates=all(a.multiply(t,h)==a.matrix(n,n) for t in ts)
        require(annihilates==descends,'HIDDEN_ANNIHILATION')
        if n==8:
            x=[[Q(int(i==0))] for i in range(n)]
            y=[[Q(int(i==4))] for i in range(n)]
            require(a.multiply(m,x)==a.multiply(m,y) and x!=y,'HIDDEN_STATES')
            require(any(a.multiply(m,a.multiply(t,x))!=a.multiply(m,a.multiply(t,y)) for t in ts)==(not descends),'PROTECTED_RESET')
        reports[name]={'preparation_span':pr,'effect_span':er,'operator_span':out['operator_span_rank'],
            'descent':out['descent'],'effects_factor':factors,'hidden_dimension':out['hidden_dimension'],
            'annihilates_hidden':annihilates,'positive_subnormalized':out['positive_subnormalized_filters'],
            'full_operator_span_sufficient':out['full_operator_span'],
            'irreducibility_control':'full operator span' if out['full_operator_span'] else 'explicit nonzero proper invariant observation kernel'}
    return {'all_passed':True,'authority_effect':'None','candidate_sha256':hashlib.sha256(raw).hexdigest(),
            'models':reports,'claim':'conditional reset construction and a tomography obstruction; finite controls only'}


if __name__=='__main__':
    print(json.dumps(verify(Path(sys.argv[1]).read_bytes()),indent=2))
