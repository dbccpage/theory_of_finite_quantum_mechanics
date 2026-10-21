"""Exact positive/negative controls for selective resets and the descent boundary."""
import copy
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest

ROOT=Path(__file__).resolve().parents[3]
RUN=ROOT/'dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family'
SPEC=importlib.util.spec_from_file_location('operational_filters',ROOT/'code/python/src/qm/operational_filters.py')
f=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(f)
a=f.a
RAW=(RUN/'candidate.json').read_bytes()


def test_exact_models_and_independent_builder():
    r=f.verify(RAW)
    spec=importlib.util.spec_from_file_location('filter_builder',RUN/'construction.py')
    builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
    assert json.loads(RAW)==builder.build()
    assert r['models']['doubled_all_preparations']['preparation_span']==8
    assert r['models']['doubled_all_preparations']['effect_span']==4
    assert r['models']['doubled_all_preparations']['descent']
    assert not r['models']['doubled_all_preparations']['full_operator_span_sufficient']
    assert r['models']['doubled_global_tests']['full_operator_span_sufficient']
    assert not r['models']['doubled_global_tests']['descent']


def test_local_product_pullback_and_positive_states():
    # Compute outcome probabilities by independent scalar indexing, including
    # non-basis inputs and unnormalized states. Do not merely re-run the checker.
    obj=json.loads(RAW)['models']['classical_product']
    states=[[Q(1,3),Q(2,3),Q(0),Q(0)], [Q(2,7)]*4]
    for i in range(4):
        for j in range(4):
            t=a.parse_matrix(obj['filters'][4*i+j],4,4)
            for k in range(4):
                for l in range(4):
                    assert t[k][l]==int(k//2==i//2 and l//2==j//2)*int(k%2==i%2 and l%2==j%2)
            for x in states:
                y=[sum(t[k][l]*x[l] for l in range(4)) for k in range(4)]
                assert y==[x[j] if k==i else 0 for k in range(4)]
                assert all(z>=0 for z in y) and sum(y)<=sum(x)


def test_hidden_kernel_survives_sequences_and_linear_closure():
    model=json.loads(RAW)['models']['doubled_all_preparations']
    ts=[a.parse_matrix(t,8,8) for t in model['filters']]
    m=a.parse_matrix(model['observe'],4,8)
    h=[[Q(int(i==0)-int(i==4))] for i in range(8)]
    # Identity need not annihilate the hidden vector, but every generated word
    # and algebraic linear combination preserves the observation kernel.
    for t in [a.identity(8),*ts]:
        for s in [a.identity(8),ts[0],ts[-1]]:
            word=a.multiply(t,s)
            combination=a.subtract(word,[[3*x for x in row] for row in s])
            assert a.multiply(m,a.multiply(word,h))==a.matrix(4,1)
            assert a.multiply(m,a.multiply(combination,h))==a.matrix(4,1)


def test_reset_descent_requires_a_visible_output():
    m=[[Q(1),Q(1)]];r=[[Q(1,2)],[Q(1,2)]];e=[[Q(1),Q(0)]]
    # A zero preparation hides every effect; visible normalization in the iff
    # theorem is essential. A nonzero first-block preparation exposes it.
    z=a.matrix(2,1);p=[[Q(1)],[Q(0)]]
    assert e!=a.multiply(a.multiply(e,r),m)
    assert a.multiply(m,a.multiply(z,e))==a.matrix(1,2)
    t=a.multiply(p,e);loc=a.multiply(a.multiply(m,t),r)
    assert a.multiply(m,t)!=a.multiply(loc,m)


def test_coarse_graining_needs_a_joint_outcome_bound():
    t=a.matrix_unit(2,0,0)
    doubled=[[2*x for x in row] for row in t]
    x=[[Q(1)],[Q(0)]]
    assert sum(row[0] for row in a.multiply(t,x))==1
    assert sum(row[0] for row in a.multiply(doubled,x))==2
    # Positivity and subnormalization compose, but arbitrary sums need not.
    for s in a.units(2):
        for u in a.units(2):
            out=a.multiply(a.multiply(s,u),x)
            assert all(row[0]>=0 for row in out) and sum(row[0] for row in out)<=1


def mutants():
    obj=json.loads(RAW)
    for name,v in obj['models'].items():
        for key in ('observe','prepare','preparations','effects'):
            for i,row in enumerate(v[key]):
                for j,s in enumerate(row):
                    bad=copy.deepcopy(obj);bad['models'][name][key][i][j]=str(Q(s)+1)
                    yield name+'/'+key+'/'+str(i)+'/'+str(j),bad
        for key in ('filters','coordinate_filters'):
            for mode in ('missing','empty','extra','entry','ragged'):
                bad=copy.deepcopy(obj);target=bad['models'][name][key]
                if mode=='missing':target.pop()
                elif mode=='empty':target.clear()
                elif mode=='extra':target.append(copy.deepcopy(target[0]))
                elif mode=='entry':target[0][0][0]='3'
                else:target[0][0].pop()
                yield name+'/'+key+'/'+mode,bad
        for value in (True,4.0,'4'):
            bad=copy.deepcopy(obj);bad['models'][name]['state_dimension']=value
            yield name+'/dimension/'+repr(value),bad
        for value in (True,1,0.5,'2/2','1/0'):
            bad=copy.deepcopy(obj);bad['models'][name]['effects'][0][0]=value
            yield name+'/scalar/'+repr(value),bad
    for key in obj:
        bad=copy.deepcopy(obj);del bad[key];yield 'missing/'+key,bad
    for key,value in [('authority_effect','Promote'),('premises',[]),('models',{})]:
        bad=copy.deepcopy(obj);bad[key]=value;yield 'scope/'+key,bad


def test_fixture_integrity_controls(tmp_path):
    f.verify(RAW)
    outcomes=[]
    for name,bad in mutants():
        with pytest.raises((ValueError,TypeError)) as exc:
            f.verify(json.dumps(bad).encode())
        outcomes.append({'id':name,'rejected':True,'reason':str(exc.value)})
    assert len(outcomes)==len({x['id'] for x in outcomes}) and len(outcomes)>500
    (tmp_path/'filter_mutations.json').write_bytes((json.dumps({'kind':'fixture_integrity','all_rejected':True,
        'count':len(outcomes),'outcomes':outcomes},indent=2)+'\n').encode())


def test_duplicate_keys_and_optimized_scope(tmp_path):
    with pytest.raises(ValueError,match='DUPLICATE_KEY'):
        f.verify(RAW.replace(b'"schema":',b'"schema":"wrong","schema":',1))
    bad=json.loads(RAW);bad['premises'].pop()
    p=tmp_path/'bad.json';p.write_bytes(json.dumps(bad).encode())
    script=ROOT/'code/python/src/qm/operational_filters.py'
    for path,code in [(RUN/'candidate.json',0),(p,1)]:
        result=subprocess.run([sys.executable,'-I','-O',str(script),str(path)],capture_output=True)
        assert (result.returncode==0)==(code==0)
        if code: assert b'PREMISES' in result.stderr


def test_semantic_nonseparating_effects_preserve_a_proper_kernel():
    # All basis preparations are available, but the sole normalization effect
    # cannot distinguish e0 from e1. Reset maps are valid channels, not malformed.
    preps=a.identity(2);effects=[[Q(1),Q(1)]]
    ts=[[[preps[k][i]*effects[0][j] for j in range(2)] for k in range(2)] for i in range(2)]
    report=a.analyze(a.identity(2),a.identity(2),ts,ts)
    assert report['calibrated'] and report['descent'] and report['tomographic']
    assert report['positive_subnormalized_filters'] and report['normalization_preserved']
    assert a.rank(preps)==2 and a.rank(effects)==1
    hidden=[[Q(1)],[Q(-1)]]
    assert a.multiply(effects,hidden)==[[Q(0)]]
    assert all(a.multiply(t,hidden)==a.matrix(2,1) for t in ts)
    assert a.multiply(effects,[[Q(1)],[Q(0)]])==[[Q(1)]]  # kernel is proper

def test_semantic_adding_separating_effects_restores_irreducibility():
    # Change only the effect family from the preceding near-miss.
    preps=a.identity(2);effects=a.identity(2)
    ts=[[[preps[k][i]*effects[j][l] for l in range(2)] for k in range(2)]
        for i in range(2) for j in range(2)]
    assert a.rank(preps)==a.rank(effects)==2
    report=a.analyze(a.identity(2),a.identity(2),ts,ts)
    assert report['positive_subnormalized_filters'] and report['full_operator_span']
    assert report['descent'] and report['tomographic']

def test_semantic_global_resets_break_descent_without_breaking_positivity():
    m=[[Q(1),Q(1)]];r=[[Q(1,3)],[Q(2,3)]]
    ts=a.units(2);loc=[a.multiply(a.multiply(m,t),r) for t in ts]
    report=a.analyze(m,r,ts,loc)
    assert report['calibrated'] and report['positive_subnormalized_filters']
    assert report['full_operator_span'] and not report['descent'] and not report['tomographic']
    h=[[Q(1)],[Q(-1)]]
    assert a.multiply(m,h)==[[Q(0)]]
    assert a.multiply(m,a.multiply(ts[0],h))==[[Q(1)]]
