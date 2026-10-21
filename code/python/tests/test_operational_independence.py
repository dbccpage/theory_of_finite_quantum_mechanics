"""Independent operational controls, including ancillary process distinctions."""
import copy
from fractions import Fraction as Q
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT/'dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T202420Z_operational_independence'
SPEC = importlib.util.spec_from_file_location('operational_independence',ROOT/'code/python/src/qm/operational_independence.py')
f = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(f)
a = f.a
RAW = (RUN/'candidate.json').read_bytes()
C = json.loads(RAW)
FLIP = [1,0,3,2]


def channels():
    return [a.parse_matrix(v,4,4) for v in C['channels'].values()]


def apply(t,p):
    return [row[0] for row in a.multiply(t,[[x] for x in p])]


def test_models_and_independent_builder():
    report = f.verify(RAW)
    assert [s['hidden_dimension'] for s in report['systems']] == [0,0,4,24,112]
    spec = importlib.util.spec_from_file_location('independence_builder',RUN/'construction.py')
    builder = importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
    assert builder.build() == C


def test_local_operations_do_not_signal_on_all_joint_orbit_states():
    ff = f.combined_flip(FLIP,FLIP)
    for k in range(16):
        p = [Q(int(x == k)+int(x == ff[k]),2) for x in range(16)]
        for t,s in itertools.product(channels(),repeat=2):
            joint = f.tensor(t,s)
            f.validate_event(joint,ff,ff,True)
            out = apply(joint,p)
            marginal = [sum(p[4*x+y] for y in range(4)) for x in range(4)]
            assert [sum(out[4*x+y] for y in range(4)) for x in range(4)] == apply(t,marginal)
            assert sum(out) == 1 and all(x >= 0 for x in out)


def test_ancillary_distinctions_are_not_quotiented_away():
    identity, flag = channels()[:2]
    # These two channels agree on every local invariant basis preparation.
    for k in (0,2):
        p = [Q(int(x == k)+int(x == FLIP[k]),2) for x in range(4)]
        assert apply(identity,p) == apply(flag,p)
    corr = [Q(int(i == j),4) for i in range(4) for j in range(4)]
    first = apply(f.tensor(identity,identity),corr)
    second = apply(f.tensor(flag,identity),corr)
    assert first != second
    # The normalized diagonal correlation actually recovers every matrix entry.
    for t in channels():
        out = apply(f.tensor(t,identity),corr)
        assert all(out[4*y+x]*4 == t[y][x] for y in range(4) for x in range(4))


def test_instruments_adaptation_coarse_graining_and_event_completion():
    ts = [a.parse_matrix(t,4,4) for t in C['instrument']]
    adaptations = [channels()[2],channels()[3]]
    composed = [a.multiply(adaptations[i],ts[i]) for i in range(2)]
    coarse = [[sum(t[y][x] for t in composed) for x in range(4)] for y in range(4)]
    for t in composed:
        f.validate_event(t,FLIP,FLIP)
    f.validate_event(coarse,FLIP,FLIP,True)
    for t in ts:
        missing = [1-sum(row[x] for row in t) for x in range(4)]
        failure = [[Q(1,4)*missing[x] for x in range(4)] for _ in range(4)]
        f.validate_event(failure,FLIP,FLIP)
        f.validate_event([[t[y][x]+failure[y][x] for x in range(4)] for y in range(4)],FLIP,FLIP,True)
    with pytest.raises(ValueError,match='COLUMN_BOUND'):
        f.validate_event([[2*x for x in row] for row in ts[0]],FLIP,FLIP)


def test_coherence_and_interchange():
    assoc = lambda p: (p[0][0],(p[0][1],p[1]))
    swap = lambda p: (p[1],p[0])
    for a0,b,c,d in itertools.product(range(4),repeat=4):
        x = (((a0,b),c),d)
        short = assoc(assoc(x))
        first = (assoc(x[0]),x[1])
        second = assoc(first)
        long = (second[0],assoc(second[1]))
        assert short == long == (a0,(b,(c,d)))
        left = assoc(swap(assoc(((a0,b),c))))
        right = (b,(c,a0))
        assert left == right
        assert swap(swap((a0,b))) == (a0,b)
    t,s,u,v = channels()
    assert f.tensor(a.multiply(s,t),a.multiply(v,u)) == a.multiply(f.tensor(s,v),f.tensor(t,u))
    assert f.tensor(f.tensor(t,s),u) == f.tensor(t,f.tensor(s,u))


def mutants():
    for i,system in enumerate(C['systems']):
        for key in system:
            bad=copy.deepcopy(C);del bad['systems'][i][key];yield f'system/{i}/missing/{key}',bad
        for key in ('atoms','points'):
            for value in (True,1.0,'1'):
                bad=copy.deepcopy(C);bad['systems'][i][key]=value;yield f'system/{i}/{key}/{value!r}',bad
        for key in ('observe','prepare'):
            for row,col in {(0,0),(len(system[key])-1,len(system[key][0])-1)}:
                bad=copy.deepcopy(C);bad['systems'][i][key][row][col]=str(Q(system[key][row][col])+1)
                yield f'system/{i}/{key}/{row}/{col}',bad
        for mode in ('missing','extra','wrong','boolean'):
            bad=copy.deepcopy(C);target=bad['systems'][i]['orbits']
            if mode=='missing':target.pop()
            elif mode=='extra':target.append(target[0][:])
            elif mode=='wrong':target[0][0]=-1
            else:target[0][0]=False
            yield f'system/{i}/orbit/{mode}',bad
        bad=copy.deepcopy(C);bad['systems'][i]['flip'][0]=True;yield f'system/{i}/flip_type',bad
        if i:
            bad=copy.deepcopy(C);bad['systems'][i]['flip']=list(range(system['points']));yield f'system/{i}/trivial_flip',bad
    for name,t in C['channels'].items():
        for y,x in itertools.product(range(4),repeat=2):
            bad=copy.deepcopy(C);bad['channels'][name][y][x]=str(Q(t[y][x])+1)
            yield f'channel/{name}/{y}/{x}',bad
    for name,vector in C['hidden_states'].items():
        for i,x in enumerate(vector):
            bad=copy.deepcopy(C);bad['hidden_states'][name][i]=str(Q(x)+1);yield f'witness/{name}/{i}',bad
    for key in C:
        bad=copy.deepcopy(C);del bad[key];yield 'missing/'+key,bad
    for key,value in [('premises',[]),('authority_effect','Promote'),('systems',[]),('instrument',[]),('channels',{})]:
        bad=copy.deepcopy(C);bad[key]=value;yield 'scope/'+key,bad
    bad=copy.deepcopy(C);bad['unconditional_quantum_reconstruction']=True;yield 'extra_claim',bad
    for value in (True,1,0.5,'1/0','2/2'):
        bad=copy.deepcopy(C);bad['channels']['identity'][0][0]=value;yield 'scalar/'+repr(value),bad


def test_mutation_controls(tmp_path):
    f.verify(RAW)
    outcomes=[]
    for name,bad in mutants():
        with pytest.raises((ValueError,TypeError)) as exc:
            f.verify(json.dumps(bad).encode())
        outcomes.append({'id':name,'rejected':True,'reason':str(exc.value)})
    assert len(outcomes) == len({x['id'] for x in outcomes}) and len(outcomes)>200
    (tmp_path/'independence_mutations.json').write_bytes((json.dumps({'all_rejected':True,'count':len(outcomes),'outcomes':outcomes},indent=2)+'\n').encode())


def test_duplicate_keys_and_optimized_scope(tmp_path):
    with pytest.raises(ValueError,match='DUPLICATE_KEY'):
        f.verify(RAW.replace(b'"schema":',b'"schema":"wrong","schema":',1))
    bad=copy.deepcopy(C);bad['premises'].pop()
    path=tmp_path/'bad.json';path.write_bytes(json.dumps(bad).encode())
    for file,valid in [(RUN/'candidate.json',True),(path,False)]:
        p=subprocess.run([sys.executable,'-I','-O',str(ROOT/'code/python/src/qm/operational_independence.py'),str(file)],capture_output=True)
        assert (p.returncode == 0) == valid
        if not valid:
            assert b'PREMISES' in p.stderr


def test_numeric_boundary_rejects_inexact_scalars_and_bad_shapes():
    for value in (True,0.5):
        bad=a.identity(4);bad[0][0]=value
        with pytest.raises(ValueError,match='SCALAR_TYPE'):
            f.validate_event(bad,FLIP,FLIP)
    with pytest.raises(ValueError,match='MATRIX_SHAPE'):
        f.tensor([[Q(1)],[]],a.identity(4))
