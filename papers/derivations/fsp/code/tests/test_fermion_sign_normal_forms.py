"""Schema evidence is distinct from normalization and recomputed route evidence."""
import copy
from pathlib import Path
import sys
import pytest
import yaml

code_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(code_dir))
from fermion_sign_nf_evaluator import NormalFormEvaluator

normal_forms_dir = code_dir.parent / 'normal_forms'

@pytest.fixture
def evaluator():
    return NormalFormEvaluator(normal_forms_dir)

def test_all_contracts_valid(evaluator):
    results=evaluator.lint_all_contracts()
    assert len(results) == 30
    assert all(r['valid'] for r in results.values()), results
    assert sum(r['normal_form_status']=='canonicalizer' for r in results.values()) == 2

def test_bqnf_recomputes_route(evaluator):
    packet={'complex':{'dim_c0':1,'dim_c1':2,'dim_c2':0,'d0':[[1],[1]],'d1':[]}, 'c1_defect':[1,1],'path_signs':[1,1]}
    assert evaluator.evaluate_bqnf_instance(packet)=='ExactRepair'
    packet['complex']['d0']=[[0],[0]]
    packet['path_signs']=[1,-1]
    assert evaluator.evaluate_bqnf_instance(packet)=='ExactCancellation'
    packet['c1_defect']=[1,2]
    assert evaluator.evaluate_bqnf_instance(packet)=='StabilizedSurvivor'
    packet['complex']['dim_c2']=1
    packet['complex']['d1']=[[1,0]]
    assert evaluator.evaluate_bqnf_instance(packet)=='OpenSignObstruction'

@pytest.mark.parametrize('packet',[{}, {'phi_1_residual':0}, {'phi_1_residual':1e-30}, {'has_meron_pairing':True}, {'dimension_error':True}])
def test_summary_claims_are_not_certificates(evaluator,packet):
    assert evaluator.evaluate_bqnf_instance(packet)=='Refused'

@pytest.mark.parametrize('mutation',['missing_field','bad_enum','bad_route','missing_law'])
def test_schema_linter_detects_actual_schema_violations(evaluator,tmp_path,mutation):
    data=yaml.safe_load((normal_forms_dir/'nf.change.rational_quotient.yaml').read_text(encoding='utf-8'))
    if mutation=='missing_field': del data['certification']['verifier_required']
    if mutation=='bad_enum': data['identity']['verification_status']='verified'
    if mutation=='bad_route': data['terminal_route_map']={'wrong':'Preserve'}
    if mutation=='missing_law': del data['normalization']['laws']['idempotence']
    path=tmp_path/'invalid.yaml'
    path.write_text(yaml.safe_dump(data),encoding='utf-8')
    assert not evaluator.lint_single_contract(path)['valid']
