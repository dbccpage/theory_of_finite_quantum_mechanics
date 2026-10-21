"""Semantic controls and mutation challenges for conditional tomography."""
import copy
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest

ROOT=Path(__file__).resolve().parents[3]
RUN=ROOT/'dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography'
SPEC=importlib.util.spec_from_file_location('operational_tomography',ROOT/'code/python/src/qm/operational_tomography.py')
ot=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(ot)
RAW=(RUN/'p1/candidate.json').read_bytes()


def matrices(name):
    e=json.loads(RAW)['examples'][name]
    n=e['state_dimension']
    return (ot.parse_matrix(e['observe'],4,n),ot.parse_matrix(e['prepare'],n,4),
            [ot.parse_matrix(t,n,n) for t in e['operations']],
            [ot.parse_matrix(t,4,4) for t in e['coordinate_operations']])


def test_original_bytes_and_independent_construction():
    result=ot.verify_candidate_bytes(RAW)
    spec=importlib.util.spec_from_file_location('construction',RUN/'p1/construction.py')
    build=importlib.util.module_from_spec(spec); spec.loader.exec_module(build)
    assert json.loads(RAW)==build.make_candidate()
    assert result['examples']['doubled_filters']['hidden_dimension']==4
    assert result['examples']['irreducible_without_descent']['descent'] is False
    assert result['examples']['tomographic_identity']['tomographic'] is True
    assert result['examples']['tomographic_identity']['full_operator_span'] is False


def test_doubled_normalized_states_and_protected_question():
    M,R,ops,loc=matrices('doubled_filters')
    for i in range(4):
        x=[[F(k==i)] for k in range(8)]
        y=[[F(k==i+4)] for k in range(8)]
        h=ot.subtract(x,y)
        assert x != y and sum(r[0] for r in x)==sum(r[0] for r in y)==1
        assert all(r[0]>=0 for r in x+y)
        assert ot.multiply(M,x)==ot.multiply(M,y)
        assert sum(r[0] for r in x[:4])==1 and sum(r[0] for r in y[:4])==0
        for t in ops:
            assert ot.multiply(M,ot.multiply(t,h))==ot.matrix(4,1)
        all_ops=matrices('irreducible_without_descent')[2]
        assert any(ot.multiply(M,ot.multiply(t,h))!=ot.matrix(4,1) for t in all_ops)


def test_local_product_calibration_factorization_and_filters():
    M,R,ops,_=matrices('product_filters')
    # Independent scalar product formula, including non-basis probabilities.
    a,b=[F(1,3),F(2,3)],[F(3,4),F(1,4)]
    state=[[a[i]*b[j]] for i in range(2) for j in range(2)]
    assert sum(row[0] for row in state)==1
    assert ot.multiply(M,state)==state
    for i in range(4):
        for j in range(4):
            t=ops[4*i+j]
            for k in range(4):
                for l in range(4):
                    assert t[k][l]==F(k//2==i//2 and l//2==j//2)*F(k%2==i%2 and l%2==j%2)
            out=ot.multiply(t,state)
            assert all(row[0]>=0 for row in out)
            assert sum(row[0] for row in out)<=1


def test_normalization_kernel_and_nonzero_premise():
    # Any column-stochastic matrix preserves sum-zero differences. Use permutations
    # plus a noninvertible reset to avoid relying on reversibility in this control.
    from itertools import permutations
    h=[[F(1)],[F(-1)],[F(0)],[F(0)]]
    stochastic=[[[F(i==p[j]) for j in range(4)] for i in range(4)] for p in permutations(range(4))]
    stochastic.append([[F(i==0) for _ in range(4)] for i in range(4)])
    for t in stochastic:
        assert sum(row[0] for row in ot.multiply(t,h))==0
    z=ot.matrix(1,2)
    r=ot.analyze(z,ot.matrix(2,1),ot.units(2),[ot.matrix(1,1)]*4)
    assert r['descent'] and r['full_operator_span'] and not r['nonzero_observation']
    assert not r['tomographic'] and not r['calibrated']


def mutants():
    c=json.loads(RAW)
    for name,e in c['examples'].items():
        for key in ('observe','prepare'):
            for i,row in enumerate(e[key]):
                for j,value in enumerate(row):
                    bad=copy.deepcopy(c)
                    bad['examples'][name][key][i][j]=str(F(value)+1)
                    yield f'{name}/{key}/{i}/{j}',bad
        for key in ('operations','coordinate_operations'):
            bad=copy.deepcopy(c); bad['examples'][name][key][0][0][0]='2'
            yield f'{name}/{key}/entry',bad
            bad=copy.deepcopy(c); bad['examples'][name][key].pop()
            yield f'{name}/{key}/omission',bad
        for value in (True,4.0,'4',-1):
            bad=copy.deepcopy(c); bad['examples'][name]['state_dimension']=value
            yield f'{name}/dimension/{value!r}',bad
        for value in ([True,2],[2.0,2],[2,2,1]):
            bad=copy.deepcopy(c); bad['examples'][name]['local_frame_sizes']=value
            yield f'{name}/frame/{value!r}',bad
        for value in (True,1,0.5,'2/2','0/1','nan','1/0'):
            bad=copy.deepcopy(c); bad['examples'][name]['observe'][0][0]=value
            yield f'{name}/rational/{value!r}',bad
    for key in c:
        bad=copy.deepcopy(c); del bad[key]
        yield 'missing/'+key,bad
    for key,value in [('authority_effect','Promote'),('claim','local tomography derived from primitive difference'),('premises',[])]:
        bad=copy.deepcopy(c); bad[key]=value
        yield 'scope/'+key,bad
    for i in range(len(c['premises'])):
        bad=copy.deepcopy(c); bad['premises'].pop(i)
        yield 'missing_premise/'+str(i),bad


def challenge_report():
    outcomes=[]
    for name,bad in mutants():
        try:
            ot.verify_candidate_bytes(json.dumps(bad).encode())
        except (ValueError,TypeError) as exc:
            outcomes.append({'id':name,'rejected':True,'failure':str(exc)})
        else:
            raise AssertionError('accepted mutant: '+name)
    return {'valid_control':ot.verify_candidate_bytes(RAW)['candidate_sha256'],
            'count':len(outcomes),'all_rejected':True,'outcomes':outcomes}


def test_mutation_challenges(tmp_path):
    report=challenge_report()
    (tmp_path/'mutations.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    assert report['count']>=250


def test_duplicate_keys_and_ragged_direct_calls():
    with pytest.raises(ValueError,match='DUPLICATE_KEY'):
        ot.verify_candidate_bytes(RAW.replace(b'"schema":',b'"schema":"bad","schema":',1))
    with pytest.raises(ValueError,match='MATRIX_SHAPE'):
        ot.analyze([[F(1),F(0)]],[[F(1)],[F(0)]],[[[F(1)],[F(0),F(1)]]],[[[F(1)]]])


def test_optimized_checker_keeps_scope_guard(tmp_path):
    bad=json.loads(RAW); bad['premises'].pop()
    path=tmp_path/'bad.json'; path.write_bytes(json.dumps(bad).encode())
    script=ROOT/'code/python/src/qm/operational_tomography.py'
    good=subprocess.run([sys.executable,'-I','-O',str(script),str(RUN/'p1/candidate.json')],capture_output=True)
    rejected=subprocess.run([sys.executable,'-I','-O',str(script),str(path)],capture_output=True)
    assert good.returncode==0
    assert rejected.returncode!=0 and b'PREMISES' in rejected.stderr


def test_direct_integer_inputs_remain_exact():
    for n in (2**54, 10**100):
        a = [[n, n+1], [n+1, n+2]]
        assert a[0][0]*a[1][1] - a[0][1]*a[1][0] == -1
        assert ot.rank(a) == 2
        assert ot.analyze(a, [[1,0],[0,1]], [ot.identity(2)],
                          [ot.identity(2)])['tomographic'] is True


@pytest.mark.parametrize('bad', [[], [[]], [[1,2],[3]], [[1],[2,3]]])
def test_direct_matrix_shape_rejected(bad):
    for op in (ot.rank, lambda a: ot.multiply(a, [[1],[1]]),
               lambda a: ot.subtract(a, a),
               lambda a: ot.analyze(a, [[1]], [[[1]]], [[[1]]])):
        with pytest.raises(ValueError, match='MATRIX_SHAPE'):
            op(bad)


@pytest.mark.parametrize('scalar', [True, False, 0.5, 1.0, '1'])
def test_direct_inexact_or_ambiguous_scalars_rejected(scalar):
    a = [[scalar]]
    for op in (ot.rank, lambda a: ot.multiply(a, [[1]]),
               lambda a: ot.subtract(a, a),
               lambda a: ot.analyze(a, [[1]], [[[1]]], [[[1]]])):
        with pytest.raises(ValueError, match='SCALAR_TYPE'):
            op(a)
