"""Replay retained stage bindings and exact certificates without modifying evidence.

Use --working-sources to also require the current implementation to match this
run. Native command receipts are retained evidence; this command does not rerun
Rust or Lean or infer new compiler success from old receipts.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from fractions import Fraction as Q


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--working-sources',action='store_true')
    args=parser.parse_args()
    run=Path(__file__).resolve().parent
    root=next(p for p in run.parents if (p/'dag/pfp/prepare_stage.py').is_file())
    manifest=json.loads((run/'source_manifest.json').read_bytes())
    for item in manifest['artifacts']:
        path=run/item['path'];assert run in path.resolve().parents
        assert path.is_file() and sha(path)==item['sha256'],item['path']
    inventory={p.relative_to(run).as_posix() for p in run.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='source_manifest.json'}
    assert inventory=={x['path'] for x in manifest['artifacts']},'changed artifact inventory'
    if args.working_sources:
        for item in manifest['working_sources']:assert sha(root/item['path'])==item['sha256'],item['path']
    for stage in ('p0','p1','p4'):
        request=json.loads((run/stage/'request.json').read_bytes())
        canonical=json.dumps(request['public_context'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
        assert hashlib.sha256(canonical).hexdigest()==request['input_sha256']
    reviewed=run/'p0/reviewed_missions.json';review=json.loads((run/'p0/host_review.json').read_bytes())
    assert sha(reviewed)==review['reviewed_sha256']
    for pin in json.loads(reviewed.read_bytes())['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['source_pins']:
        assert sha(root/pin['path'])==pin['sha256']
    assert sha(root/review['checker_pin']['path'])==review['checker_pin']['sha256']
    check=json.loads((run/'p2/host_check.json').read_bytes())
    assert sha(run/'p1/candidate.json')==check['candidate_sha256']
    # Disable bytecode creation so this command writes no new run evidence.
    import sys
    sys.dont_write_bytecode=True
    spec=importlib.util.spec_from_file_location('independent_bell_checker',run/'check_certificate.py')
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    result=checker.check(run/'p1/request.json',run/'p1/candidate.json')
    original=json.loads((run/'p1/candidate.json').read_bytes())
    rust=(run/'p2/logs/rust_replay_0.stdout.log').read_text().splitlines()
    assert len(rust)==len(original['samples'])
    for line,sample in zip(rust,original['samples']):
        row=line.split('\t');assert row[0]==sample['id']
        values=sample['correlators']+[sample[k] for k in ['chsh','positive_score_mass','negative_score_mass','lower_slack','upper_slack']]
        assert list(map(Q,row[1:]))==list(map(Q,values))
    p4=json.loads((run/'p4/host_check.json').read_bytes())
    assert sha(run/'p4/candidate.json')==p4['candidate_sha256']
    for mutant in p4['predicate_results']['mutants']:
        try:checker.check(run/'p1/request.json',run/mutant['candidate'])
        except ValueError as e:assert str(e)==mutant['reason']
        else:raise AssertionError('mutant accepted')
    for kind in ('python','rust_retry','rust_replay','lean','certificate'):
        assert all(x['exit_code']==0 for x in json.loads((run/'p2'/(kind+'_receipt.json')).read_bytes()))
    p5=json.loads((run/'p5/candidate.json').read_bytes())
    assert sha(run/'p4/host_check.json')==p5['input_sha256']
    assert p5['stop']=='user_review_requested'
    print(json.dumps({'artifacts_checked':len(manifest['artifacts']),'exact_samples_replayed':result['checked_samples'],
     'mutation_rejections_replayed':len(p4['predicate_results']['mutants']), 'working_sources_checked':args.working_sources,
     'claim':'Retained bytes, bindings, exact recomputation, and recorded native statuses; no fresh compiler execution.'},indent=2))


if __name__=='__main__':main()
