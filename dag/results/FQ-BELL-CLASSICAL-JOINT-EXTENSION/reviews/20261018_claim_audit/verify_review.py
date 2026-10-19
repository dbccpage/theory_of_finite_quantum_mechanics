"""Fail-closed custody and claim checks for the Bell review, including python -O.

No receipt is an authority token. This replays data and checks the completeness
of retained native evidence; run_checks.py performs the actual fresh executions.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('strict_bell', HERE/'check_certificate.py')
strict = importlib.util.module_from_spec(spec); spec.loader.exec_module(strict)
require = strict.require


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(root, relative):
    require(type(relative) is str, 'custody:path_type')
    path = (root/relative).resolve()
    require(path.is_relative_to(root.resolve()) and path != root.resolve(), 'custody:path_escape')
    return path


def verify_inventory(directory, manifest, manifest_name='source_manifest.json'):
    rows = manifest.get('artifacts', manifest.get('files'))
    require(type(rows) is list and bool(rows), 'custody:empty_inventory')
    names = [row['path'] for row in rows]
    require(len(names) == len(set(names)), 'custody:duplicate_path')
    for row in rows:
        path = contained(directory, row['path'])
        require(path.is_file() and sha(path) == row['sha256'], 'custody:digest:' + row['path'])
    actual = {p.relative_to(directory).as_posix() for p in directory.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.name != manifest_name}
    require(actual == set(names), 'custody:inventory_mismatch')
    return len(rows)


def validate_receipts(kind, receipts, evidence):
    count = 4 if kind == 'lean' else 1
    require(type(receipts) is list and len(receipts) == count, 'native:missing_invocations:' + kind)
    for row in receipts:
        require(type(row.get('exit_code')) is int and row['exit_code'] == 0, 'native:failed:' + kind)
        require(type(row.get('argv')) is list and bool(row['argv']), 'native:missing_command:' + kind)
        for key in ('stdout', 'stderr'):
            require(contained(evidence, row[key]).is_file(), 'native:missing_log:' + kind)
    if kind == 'lean':
        require(receipts[0]['argv'][-1] == '--version', 'native:lean_version_command')
        require([r['argv'][-1] for r in receipts[1:]] == [
            'DerivationDagQMClosure.lean', 'BellClassicalJointExtension.lean', 'BellOperad.lean'], 'native:lean_module_coverage')
    return count


def main():
    import yaml
    root = next(p for p in HERE.parents if (p/'dag/pfp/prepare_stage.py').is_file())
    config = strict.read_json(HERE/'review_config.json')
    review_manifest = HERE/'review_manifest.json'
    require(review_manifest.is_file(), 'custody:missing_review_manifest')
    review_count = verify_inventory(HERE, strict.read_json(review_manifest), 'review_manifest.json')
    run = contained(root, config['original_run'])
    manifest_path = run/'source_manifest.json'
    require(sha(manifest_path) == config['original_manifest_sha256'], 'custody:historical_manifest_changed')
    original = strict.read_json(manifest_path)
    count = verify_inventory(run, original)
    for stage in ('p0', 'p1', 'p4'):
        packet = strict.read_json(run/stage/'request.json')
        require(strict.context_digest(packet['public_context']) == packet['input_sha256'], 'binding:stage_context:' + stage)
    missions = run/'p0/reviewed_missions.json'
    require(sha(missions) == strict.read_json(run/'p0/host_review.json')['reviewed_sha256'], 'binding:host_review')
    for row in strict.read_json(missions)['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['source_pins']:
        require(sha(contained(root, row['path'])) == row['sha256'], 'custody:mission_source')
    result = strict.check(run/'p1/request.json', run/'p1/candidate.json')
    candidate = strict.read_json(run/'p1/candidate.json')
    host = strict.read_json(run/'p2/host_check.json')
    require(result['candidate_sha256'] == host['candidate_sha256'], 'binding:candidate_to_host')
    for kind in ('python','rust_retry','rust_replay','lean','certificate'):
        validate_receipts(kind, strict.read_json(run/'p2'/(kind+'_receipt.json')), run)
    for row in config['working_sources']:
        require(sha(contained(root,row['path'])) == row['sha256'], 'custody:working_source:' + row['path'])
    collection = yaml.safe_load((root/'dag/operads/FQ-BELL-CLASSICAL-JOINT-EXTENSION.yaml').read_bytes())
    presentation = collection['presentation']
    generator_fields = {'id','ordered_inputs','output','arity','carrier','coefficient_ring','hypotheses','source_pins','semantic_predicate','evidence_status'}
    for generator in presentation['generators']:
        require(generator_fields <= set(generator), 'operad:missing_generator_field')
        require(type(generator['arity']) is int and generator['arity'] == len(generator['ordered_inputs']), 'operad:arity')
        for pin in generator['source_pins']:
            require(sha(contained(root,pin['path'])) == pin['sha256'], 'operad:source_digest')
    require('Fine converse' in ' '.join(collection['open_obligations']), 'scope:Fine_converse_not_open')
    for kind in ('python','rust','rust_replay','lean','protocol','review_tests'):
        validate_receipts(kind, strict.read_json(HERE/'validation'/(kind+'_receipt.json')), HERE)
    lean = (HERE/'validation/lean_3.stdout.log').read_text()
    for name in ('substitute_left_unit','substitute_right_unit','substitute_assoc','substitute_congr','expect_chsh','bell_evaluation','bell_bound','bell_nullary_graft'):
        require("'QuantumMechanics.BellOperad."+name+"'" in lean, 'native:missing_axiom_report:' + name)
    require('sorryAx' not in lean, 'native:unproved_Lean_anchor')
    require('version 4.33.1' in (HERE/'validation/lean_0.stdout.log').read_text(), 'native:Lean_version')
    python = (HERE/'validation/python_0.stderr.log').read_text()
    protocol = (HERE/'validation/protocol_0.stderr.log').read_text()
    tests = (HERE/'validation/review_tests_0.stderr.log').read_text()
    rust = (HERE/'validation/rust_0.stdout.log').read_text()
    pycount = lambda text: int(re.search(r'Ran (\d+) tests?', text).group(1))
    for text in (python,protocol,tests): require(re.search(r'\bOK\s*$',text) is not None, 'native:unittest_summary')
    rustmatch = re.search(r'test result: ok\. (\d+) passed; 0 failed', rust)
    require(rustmatch is not None and int(rustmatch.group(1)) > 0, 'native:Rust_summary')
    from fractions import Fraction as Q
    lines = (HERE/'validation/rust_replay_0.stdout.log').read_text().splitlines()
    require(len(lines) == len(candidate['samples']), 'native:Rust_replay_cardinality')
    for line, sample in zip(lines,candidate['samples']):
        row = line.split('\t')
        values = sample['correlators'] + [sample[k] for k in ('chsh','positive_score_mass','negative_score_mass','lower_slack','upper_slack')]
        require(row[0] == sample['id'] and list(map(Q,row[1:])) == list(map(Q,values)), 'native:Rust_Python_disagreement')
    print(json.dumps({'historical_artifacts_checked':count,'review_artifacts_checked':review_count,'exact_public_laws':result['checked_samples'],
                     'python_tests':pycount(python),'Rust_tests':int(rustmatch.group(1)),
                     'PFP_protocol_tests':pycount(protocol),'review_regression_tests':pycount(tests),
                     'Lean':'4.33.1; eight named axiom reports including actual nullary graft',
                     'claim':'Checked supplied-law implication and scoped endomorphism substitution semantics; Fine converse, symmetric action and quotient completeness remain open.'},indent=2))


if __name__ == '__main__': main()
