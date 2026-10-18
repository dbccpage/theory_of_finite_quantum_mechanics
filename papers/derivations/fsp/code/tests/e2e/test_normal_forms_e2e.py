"""End-to-end compatibility adapter and non-vacuous finite packet routing."""
import importlib.util
from pathlib import Path

paper_dir=Path(__file__).resolve().parents[3]
nf_dir=paper_dir/'normal_forms'
spec=importlib.util.spec_from_file_location('nf_compat_e2e',nf_dir/'fermion_sign_nf_evaluator.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_contract_adapter_reports_scope():
    results=module.NormalFormEvaluator(nf_dir).lint_all_contracts()
    assert len(results)==30
    assert all(r['valid'] for r in results.values())
    assert results['nf.physics.wdwnf.yaml']['normal_form_status']=='operational_contract'
    assert results['nf.change.sign_switching.yaml']['normal_form_status']=='canonicalizer'

def test_recomputed_packet_refuses_laundered_summaries():
    evaluator=module.NormalFormEvaluator(nf_dir)
    assert evaluator.evaluate_bqnf_instance({'phi_1_residual':0.0})=='Refused'
    assert evaluator.evaluate_bqnf_instance({'has_meron_pairing':True})=='Refused'
    packet={'complex':{'dim_c0':1,'dim_c1':2,'dim_c2':0,'d0':[[0],[0]],'d1':[]},'c1_defect':['1/3','1/3'],'path_signs':[1,-1]}
    assert evaluator.evaluate_bqnf_instance(packet)=='ExactCancellation'
    packet['c1_defect'][1]='1000000000001/3000000000000'
    assert evaluator.evaluate_bqnf_instance(packet)=='StabilizedSurvivor'
