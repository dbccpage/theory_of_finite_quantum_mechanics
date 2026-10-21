"""Bind measurement proof claims to the checked sources and exact Lean replay."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def test_measurement_receipt_has_fresh_complete_admission_free_replay():
    receipt = json.loads((ROOT / 'dag/research/tensor_measurement_validation.json').read_text(encoding='utf-8'))
    replay = receipt['lean_replay']
    expected = {
        'TensorConeReconstruction', 'TensorTomography', 'TensorCoordinates',
        'TensorSchmidt', 'TensorReachability', 'TensorOperationalCone', 'TensorComposition',
        'TensorEffectOrder', 'TensorEffectCone', 'TensorMeasurements',
        'FiniteGraphDressing', 'SwitchingNormalForm', 'MeronCharacter',
    }
    assert len(replay['results']) == len(expected)
    assert {r['module'] for r in replay['results']} == expected
    assert 'version 4.35.0,' in replay['lean_version']
    assert replay['mathlib_source_sha'] == '56a005855ea17e0b0958f73ec801ae140b0a1679'
    outputs = ''
    for result in replay['results']:
        raw = (ROOT / f"lean4/{result['module']}.lean").read_bytes()
        assert hashlib.sha256(raw).hexdigest() == result['sha256']
        code = re.sub(r'/\-.*?\-/|--[^\n]*', '', raw.decode('utf-8'), flags=re.S)
        assert not re.search(r'\b(sorry|admit|axiom|sorryAx|unsafe)\b', code)
        assert result['exit_code'] == 0
        for flag in ('axiom_audit_passed', 'admission_scan_passed', 'source_unchanged_during_build'):
            assert result[flag] is True
        lists = re.findall(r'depends on axioms: \[([^]]*)\]', result['output'])
        assert lists
        assert all(set(names.split(', ')) <= {'propext', 'Classical.choice', 'Quot.sound'} for names in lists)
        outputs += result['output']
    for theorem in ('positive_iff_pairing', 'binary_iff_bounds', 'binary_iff_normalized',
                    'effect_cone_eq_positive', 'validEffect_iff_binary',
                    'available_effects_eq_interval', 'test_iff_povm',
                    'operational_effect_cone', 'quantum_measurements'):
        assert re.search(r"\." + theorem + r"' depends on axioms:", outputs)


def test_historical_measurement_manifest_and_current_dag_claims_remain_bound():
    receipt = json.loads((ROOT / 'dag/research/tensor_measurement_validation.json').read_text(encoding='utf-8'))
    for path, expected_hash in receipt['sha256'].items():
        raw = subprocess.check_output(['git', 'show', receipt['verification_source_head'] + ':' + path], cwd=ROOT)
        assert hashlib.sha256(raw).hexdigest() == expected_hash, path
    graph = json.loads((ROOT / 'dag/derivation_dag.json').read_text(encoding='utf-8'))
    nodes = {n['id']: n for n in graph['nodes']}
    assert len(graph['nodes']) == receipt['counts']['dag_nodes']
    assert len(graph['routes']) == receipt['counts']['dag_routes']
    for name in ('TENSOR-GENERATED-EFFECT-CONE', 'TENSOR-BINARY-EFFECT-INTERVAL',
                 'TENSOR-FINITE-POVM-AVAILABILITY'):
        assert nodes[name]['status'] == 'PROVED_LEAN'
    assert nodes['FQ-GAP-TENSOR-UNIQUENESS']['status'] == 'CONDITIONAL'
    assert 'EffectSaturated' in nodes['TENSOR-BINARY-EFFECT-INTERVAL']['imported_structure'][-1]
    assert 'FiniteTestSaturated' in nodes['TENSOR-FINITE-POVM-AVAILABILITY']['imported_structure']
