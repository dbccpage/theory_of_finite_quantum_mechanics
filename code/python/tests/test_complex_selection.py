"""Independent rational replays and coordinate/scope challenges for complex selection."""
import copy
import json
from pathlib import Path
from fractions import Fraction as F
import pytest
import importlib.util
import sys
_spec = importlib.util.spec_from_file_location('complex_selection', Path(__file__).resolve().parents[1]/'src/qm/complex_selection.py')
cs = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = cs
_spec.loader.exec_module(cs)

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT/'dag/results/L1-IMP-COMPLEX-FIELD/runs/20261021T162659Z_complex_selection'


def test_actual_candidate_bytes():
    result = cs.verify_candidate_bytes((RUN/'p1/candidate.json').read_bytes())
    assert result['finite_checks'] == 'passed'
    assert result['census_cases'] == 108


def test_dimension_polynomial_and_boundary():
    for d in range(8):
        for n in range(7):
            for m in range(7):
                defect = cs.dimension(d,n*m)-cs.dimension(d,n)*cs.dimension(d,m)
                assert 4*defect == d*(2-d)*n*m*(n-1)*(m-1)
                if n == 1 or m == 1:
                    assert defect == 0
    assert [d for d in range(100) if cs.dimension(d,4)==cs.dimension(d,2)**2] == [0,2]
    assert cs.dimension(1,4) == 10
    assert cs.dimension(4,4) == 28


@pytest.mark.parametrize('d,raw,projected,bad',[(1,9,9,0),(2,16,16,0),(4,31,28,6)])
def test_span_ranks(d,raw,projected,bad):
    r = cs.span_census(d)
    assert (r['raw_rank'],r['hermitian_projection_rank'],r['nonhermitian_products']) == (raw,projected,bad)


def test_states_are_psd_and_invisible():
    delta,plus,minus = cs.witness()
    assert cs.multiply(delta,delta) == cs.identity(4)
    assert plus != minus
    for a in (plus,minus):
        assert min(cs.principal_minors(a)) >= 0
        assert sum(a[i][i] for i in range(4)) == 1
    for a in cs.hermitian_basis(2,1):
        for b in cs.hermitian_basis(2,1):
            p = cs.kron(a,b)
            assert cs.trace_pair(delta,p) == 0
            assert cs.trace_pair(plus,p) == cs.trace_pair(minus,p)
    assert cs.trace_pair(delta,plus) == 1
    assert cs.trace_pair(delta,minus) == -1


def test_quaternion_failure_is_codomain_not_rational_bilinearity():
    i,j,k = (cs.Quaternion(0,1),cs.Quaternion(0,0,1),cs.Quaternion(0,0,0,1))
    assert i*j == k and j*i == -k
    basis = cs.hermitian_basis(2,4)
    p = cs.kron(basis[3],basis[4])
    assert p != cs.adjoint(p)
    assert cs.hermitian_part(p) == cs.matrix(4,4)
    assert cs.kron(basis[3],basis[4]) == [
        [x.scale(-1) for x in row] for row in cs.kron(basis[4],basis[3])]


@pytest.mark.parametrize('n',[1,2,3,4])
def test_complex_structure_reimports_complex_scalars(n):
    j = cs.complex_structure(n)
    assert cs.multiply(j,j) == [[-x for x in row] for row in cs.identity(2*n)]
    assert cs.j_commutant_symmetric_dimension(n) == n*n
    for h in cs.hermitian_basis(n,2):
        r = cs.realify(h)
        assert r == cs.adjoint(r)
        assert cs.multiply(r,j) == cs.multiply(j,r)


def mutants(c):
    out = []
    for key in ('delta','rho_plus','rho_minus'):
        for i in range(4):
            for j in range(4):
                m = copy.deepcopy(c)
                m[key][i][j] = str(F(m[key][i][j])+1)
                out.append((f'{key}_{i}_{j}',m))
    for d in ('1','2','4'):
        for key in c['spans'][d]:
            m = copy.deepcopy(c)
            m['spans'][d][key] += 1
            out.append((f'span_{d}_{key}',m))
    for idx,row in enumerate(c['census']):
        for col in (3,4):
            m = copy.deepcopy(c)
            m['census'][idx][col] += 1
            out.append((f'census_{idx}_{col}',m))
    for name,path,value in [
        ('J_without_complex_structure',('real_with_J','scalar_structure'),'R'),
        ('J_ordinary_real_tensor',('real_with_J','composition'),'ordinary_real_tensor'),
        ('spin_factor_exclusion_claimed',('spin_factors','exclusion'),'PROVED'),
        ('spin_factor_gap_hidden',('spin_factors','derivation_status'),'CLOSED'),
        ('trivial_factor',('universal_claim','n_min'),1),
        ('single_instance_as_general',('universal_claim','evidence'),'finite_pair_check_only'),
        ('missing_d_positive',('universal_claim','domain'),'all_natural_d'),
        ('bool_integer',('universal_claim','n_min'),True),
    ]:
        m = copy.deepcopy(c)
        m[path[0]][path[1]] = value
        out.append((name,m))
    for name,key,value in [('unconditional','status','PROVED_LEAN'),
                            ('complete','completeness','DERIVED'),
                            ('zero_solution_hidden','unrestricted_solutions',[2]),
                            ('independence_dropped','premises',cs.PREMISES[:2]+cs.PREMISES[3:])]:
        m = copy.deepcopy(c)
        m[key] = value
        out.append((name,m))
    return out


def test_coordinate_and_semantic_mutants():
    c = json.loads((RUN/'p1/candidate.json').read_text(encoding='utf-8'))
    assert cs.verify_candidate_bytes(json.dumps(c).encode())['finite_checks'] == 'passed'
    for name,m in mutants(c):
        with pytest.raises(ValueError,match='mismatch'):
            cs.verify_candidate_bytes(json.dumps(m).encode())


def test_strict_parser():
    with pytest.raises(ValueError,match='duplicate'):
        cs.verify_candidate_bytes(b'{"x":1,"x":2}')
    with pytest.raises(ValueError,match='floating'):
        cs.verify_candidate_bytes(b'{"x":1.0}')
    with pytest.raises(ValueError):
        cs.dimension(True,2)


def test_single_passing_pair_is_valid_with_the_algebraic_bridge():
    # A passing pair is a valid premise. The invalid mutant omits the proof
    # from that premise to the universal statement, not the true premise itself.
    for d in (1,2,4):
        pair = cs.dimension(d,4)==cs.dimension(d,2)**2
        universal_on_census = all(joint==product for dd,n,m,joint,product in cs.census()
                                  if dd==d and n>=2 and m>=2)
        assert pair == universal_on_census == (d==2)



def test_spin_factor_dimension_count_alone_does_not_exclude():
    # V_k has dimension k+1. Dimension multiplication alone can nominate V_l;
    # this supplies no admissible Jordan product/composite or exclusion proof.
    for k in (2,3,4,5,7):
        for h in (2,3,4,5,7):
            joint_spin_index = (k+1)*(h+1)-1
            assert joint_spin_index+1 == (k+1)*(h+1)
    assert cs.make_candidate()['spin_factors']['derivation_status'] == 'OPEN'


@pytest.mark.parametrize("warm_cache", [False, True])
def test_candidate_cannot_mutate_verifier_premises(warm_cache):
    original = tuple(cs.PREMISES)
    cs._expected_json.cache_clear()
    try:
        if warm_cache:
            cs.verify_candidate_bytes((RUN/'p1/candidate.json').read_bytes())
        candidate = cs.make_candidate()
        candidate['premises'].pop()
        with pytest.raises(ValueError, match='premises'):
            cs.verify_candidate_bytes(json.dumps(candidate).encode())
        assert tuple(cs.PREMISES) == original
        assert cs.make_candidate()['premises'] == list(original)
    finally:
        # Restore legacy module state even when this regression fails pre-fix.
        if isinstance(cs.PREMISES, list):
            cs.PREMISES[:] = original
        cs._expected_json.cache_clear()
