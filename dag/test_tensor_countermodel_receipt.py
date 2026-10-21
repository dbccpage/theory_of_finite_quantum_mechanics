"""Verify the TFQ-0413 proof receipt, scope, and DAG/master synchronization."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent
NEW_MODULES = {
    'TensorPartialTranspose', 'TensorCountermodelCones', 'TensorCountermodelWitnesses',
    'TensorCountermodelEmbeddings', 'TensorHiddenCoordinates',
}
DEPENDENCIES = {
    'TensorConeReconstruction', 'TensorTomography', 'TensorCoordinates',
    'TensorSchmidt', 'TensorReachability', 'TensorOperationalCone', 'TensorComposition',
    'TensorEffectOrder', 'TensorEffectCone', 'TensorMeasurements',
}
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def receipt():
    return json.loads((ROOT / 'dag/research/tensor_countermodel_validation.json').read_text(encoding='utf-8'))


def test_countermodel_dependency_replay_is_complete_and_admission_free():
    replay = receipt()['lean_replay']
    assert 'version 4.35.0,' in replay['lean_version']
    assert replay['mathlib_source_sha'] == '56a005855ea17e0b0958f73ec801ae140b0a1679'
    assert len(replay['results']) == 15
    assert {r['module'] for r in replay['results']} == NEW_MODULES | DEPENDENCIES
    output = ''
    for r in replay['results']:
        raw = (ROOT / f"lean4/{r['module']}.lean").read_bytes()
        assert hashlib.sha256(raw).hexdigest() == r['sha256']
        code = re.sub(r'/\-.*?\-/|--[^\n]*', '', raw.decode('utf-8'), flags=re.S)
        assert not re.search(r'\b(sorry|admit|axiom|sorryAx|unsafe)\b', code)
        assert r['exit_code'] == 0
        assert all(r[key] is True for key in ('source_unchanged_during_build',
                   'admission_scan_passed', 'axiom_audit_passed'))
        lists = re.findall(r'depends on axioms: \[([^]]*)\]', r['output'])
        assert lists
        assert all(set(re.split(r',\s*', names.strip())) <= ALLOWED_AXIOMS for names in lists)
        output += r['output']
    for name in (
        'pairing_gamma_gamma', 'gamma_conjMap_product', 'blockPositive_iff_dual_sep',
        'twisted_self_dual', 'twist_reversible', 'twist_trace', 'twist_path_continuous',
        'binary_product_statistics_separate', 'cone_separations_all_dimensions',
        'sep_fails_controlled_shift', 'bp_fails_inverse_controlled_shift',
        'coherent_calibration_separates', 'imaginary_effect_binary', 'plus_binary', 'seed_normalized',
        'dephased_controlled_shift_not_injective', 'hidden_normalized_states',
        'no_local_tomography', 'dimension_doubled', 'basis_state_normalized',
    ):
        assert re.search(r"\." + name + r"' depends on axioms:", output), name


def test_countermodel_manifest_and_promotion_match_verified_scope():
    r = receipt()
    assert r['authority_effect'] == 'None'
    for path, digest in r['sha256'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    nodes = {n['id']: n for n in graph['nodes']}
    node = nodes['TENSOR-ASSUMPTION-COUNTERMODELS']
    assert node['status'] == 'PROVED_LEAN'
    assert nodes['FQ-GAP-TENSOR-UNIQUENESS']['status'] == 'CONDITIONAL'
    assert 'external' in node['bottleneck']
    assert 'two-qubit' in node['statement'].lower()
    assert 'n,m>=2' in node['statement']
    route = next(t for t in graph['routes'] if t['output'] == node['id'])
    assert route['status'] == 'DERIVED_LEAN'
    assert set(route['inputs']) == {'TENSOR-TOMOGRAPHIC-COORDINATES',
        'TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION', 'TENSOR-BINARY-EFFECT-INTERVAL'}
    records = [json.loads(line) for line in (ROOT / 'dag/theory_of_finite_qm.jsonl').read_text(encoding='utf-8').splitlines()]
    record = next(x for x in records if x['id'] == 'TFQ-0413')
    assert record['record_status'] == node['status']
    assert record['lean4'] == node['lean']
    assert {Path(ref.split('::')[0]).stem for ref in node['lean']} == NEW_MODULES
    assert r['counts'] == {'dag_nodes': len(nodes), 'dag_routes': len(graph['routes']),
                           'master_records': len(records)}
    assert r['proof_boundary']['effect_availability'] == 'No operational saturation is inferred.'
    assert r['proof_boundary']['external_classification'] == 'External theorem, not included in this Lean replay.'
