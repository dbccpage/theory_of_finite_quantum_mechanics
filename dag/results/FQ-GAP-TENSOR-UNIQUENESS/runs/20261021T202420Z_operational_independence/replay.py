"""Replay the operational-independence source-pinned gates in a new output directory.
AuthorityEffect: None. No canonical DAG changes, provider calls or Git writes.
"""
import argparse
import concurrent.futures
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[4]
PREFIX=RUN.relative_to(ROOT).as_posix()
BASE='0364c3c9744e72f05ec6a7ebd14f971f1ddd1c2c'
BASELINE='dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T200001Z_pr147/source_pins.json'
BASELINE_SHA='c187c5cc21fc2279440cb26549f22fc07c23889d06339aa97a7ea1ffddfc8fa2'
CANDIDATE_SHA='cfc4444eb4c8e1daacbf22283f2b2bddf1e9d57da0637cc62b15d4a407b6aa13'
REQUEST_SHA='b81e0146bd81d0b9d11fde7e13d865418d427e618f1fa3d15f1c0bdcb2baa558'
HEADLINES=set(['OperationalIndependence.product_state', 'OperationalIndependence.product_effect', 'OperationalIndependence.independent_probabilities', 'OperationalIndependence.act_invariant', 'OperationalIndependence.act_positive', 'OperationalIndependence.event_mass', 'OperationalIndependence.channel_state', 'OperationalIndependence.event_comp', 'OperationalIndependence.channel_comp', 'OperationalIndependence.event_parallel', 'OperationalIndependence.channel_parallel', 'OperationalIndependence.identity_channel', 'OperationalIndependence.act_comp', 'OperationalIndependence.comp_assoc', 'OperationalIndependence.interchange', 'OperationalIndependence.event_weighted', 'OperationalIndependence.channel_weighted', 'OperationalIndependence.prepare_channel', 'OperationalIndependence.test_event', 'OperationalIndependence.discard_channel', 'OperationalIndependence.discard_unique', 'OperationalIndependence.discard_comp', 'OperationalIndependence.reset_event', 'OperationalIndependence.global_effects_separate', 'OperationalIndependence.probability_interval', 'OperationalIndependence.cone_generating', 'OperationalIndependence.normalization_faithful', 'OperationalIndependence.normalized_preparations_span', 'OperationalIndependence.instrument_event', 'OperationalIndependence.instrument_probability', 'OperationalIndependence.instrument_adaptive', 'OperationalIndependence.instrument_parallel', 'OperationalIndependence.instrument_coarse', 'OperationalIndependence.event_completion', 'OperationalIndependence.record_channel', 'OperationalIndependence.controlled_channel', 'OperationalIndependence.no_signalling', 'OperationalIndependence.ancillary_process_separation', 'OperationalIndependence.comp_identity', 'OperationalIndependence.parallel_identity', 'OperationalIndependence.rename_channel', 'OperationalIndependence.rename_then', 'OperationalIndependence.rename_inverse', 'OperationalIndependence.associator_naturality', 'OperationalIndependence.swap_naturality', 'OperationalIndependence.left_unit_naturality', 'OperationalIndependence.right_unit_naturality', 'OperationalIndependence.pentagon', 'OperationalIndependence.triangle', 'OperationalIndependence.symmetry', 'OperationalIndependence.hexagon', 'OperationalIndependence.correlation_probe', 'OperationalIndependence.operational_laws', 'OperationalIndependence.operational_independence', 'OperationalIndependence.operational_laws_do_not_force_tomography', 'OperationalIndependence.operational_laws_do_not_forbid_tomography', 'OperationalIndependence.normalized_hidden_witness', 'OperationalIndependence.classical_tomography', 'OperationalIndependence.atom_not_tomographic', 'OperationalIndependence.rename_id', 'OperationalIndependence.rename_both'])
LEAN_SOURCES=['lean4/OperationalSymmetry.lean', 'lean4/OperationalCoherence.lean', 'lean4/OperationalIndependence.lean']
NEW_CODE=['code/python/src/qm/operational_independence.py', 'code/python/tests/test_operational_independence.py', 'code/rust/src/finite_probability/operational_independence.rs']
COMPANIONS=['code/python/src/qm/operational_independence.py.doc.yaml', 'code/python/tests/test_operational_independence.py.doc.yaml', 'code/rust/src/finite_probability/operational_independence.rs.doc.yaml', 'code/python/src/qm/operational_independence.contract.score.yaml', 'code/python/tests/test_operational_independence.contract.score.yaml', 'code/rust/src/finite_probability/operational_independence.contract.score.yaml']
RUN_SOURCES=('.gitignore','.gitattributes','README.md','user_request.txt','replay.py','derivation.json',
 'proposed_dag_delta.json','construction.py','candidate.json','upstream_changes.json')
INTEGRATION={'lean4/lakefile.lean','code/rust/src/finite_probability/lib.rs'}
UPSTREAM_CHANGES={'dag/derivation_dag.json': {'inherited_sha256': 'dc6d3485d5b3c8f38ef641defea4a52b88b1558138e6fd1b0e42a08b92b8182b', 'upstream_sha256': 'b034ee6b74c777c53e079ae71a89e846a71d85eaf8d37b204da86ef94b81f9be'}}


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_bytes((json.dumps(x,indent=2)+'\n').encode())


def inherited():
    if digest(ROOT/BASELINE)!=BASELINE_SHA: raise ValueError('BASELINE_PIN_ENVELOPE')
    return json.loads((ROOT/BASELINE).read_bytes())['files']


def required_sources():
    return set(inherited())|{BASELINE}|set(LEAN_SOURCES+NEW_CODE+COMPANIONS)|{PREFIX+'/'+s for s in RUN_SOURCES}


def verify_pins(pins):
    if type(pins) is not dict or set(pins)!={'base_sha','candidate_sha256','request_sha256','files'}: raise ValueError('PIN_ENVELOPE')
    if (pins['base_sha'],pins['candidate_sha256'],pins['request_sha256'])!=(BASE,CANDIDATE_SHA,REQUEST_SHA): raise ValueError('PIN_IDENTITY')
    if type(pins['files']) is not dict or set(pins['files'])!=required_sources(): raise ValueError('PIN_COVERAGE')
    for name,sha in pins['files'].items():
        p=(ROOT/name).resolve()
        if not p.is_relative_to(ROOT) or type(sha) is not str or not re.fullmatch('[0-9a-f]{64}',sha) or digest(p)!=sha:
            raise ValueError('PIN_MISMATCH:'+name)
    for name,sha in inherited().items():
        if name not in INTEGRATION:
            expected=UPSTREAM_CHANGES.get(name,{}).get('upstream_sha256',sha)
            if pins['files'][name]!=expected: raise ValueError('INHERITED_SOURCE_CHANGED:'+name)
            if name in UPSTREAM_CHANGES:
                baseline_bytes=subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
                if hashlib.sha256(baseline_bytes).hexdigest()!=expected: raise ValueError('UPSTREAM_SOURCE_MISMATCH:'+name)
    if digest(RUN/'candidate.json')!=CANDIDATE_SHA or digest(RUN/'user_request.txt')!=REQUEST_SHA: raise ValueError('INPUT_BYTES')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output.resolve();out.mkdir(parents=True,exist_ok=False)
    raw=(RUN/'source_pins.json').read_bytes();pins=json.loads(raw);verify_pins(pins)
    guards=[]
    for mode in ('missing','extra','corrupt'):
        bad=copy.deepcopy(pins);key=NEW_CODE[0]
        if mode=='missing':del bad['files'][key]
        elif mode=='extra':bad['files']['../outside']='0'*64
        else:bad['files'][key]='0'*64
        try:verify_pins(bad)
        except ValueError as exc:guards.append({'mode':mode,'rejected':True,'reason':str(exc)})
        else:raise RuntimeError('PIN_GUARD_ACCEPTED:'+mode)
    write(out/'pin_guards.json',guards)
    tasks=[
      ('lean',[['lake','build','OperationalIndependence','OperationalFilterFamily','OperationalFieldSelection','TensorHiddenCoordinates'],
        ['lake','env','lean','OperationalIndependence.lean']],ROOT/'lean4'),
      ('rust',[['cargo','test','--manifest-path','code/rust/Cargo.toml','--locked','--offline','-p','tfqm_finite_probability','--lib']],ROOT),
      ('python',[[sys.executable,'-X','utf8','-m','pytest','code/python/tests/test_operational_independence.py','code/python/tests/test_operational_filters.py',
        'code/python/tests/test_operational_tomography.py','code/python/tests/test_complex_selection.py','-q','--basetemp',str(out/'pytest_tmp')]],ROOT),
      ('candidate',[[sys.executable,'-I','-X','utf8',NEW_CODE[0],str(RUN/'candidate.json')]],ROOT),
      ('construction',[[sys.executable,'-I','-X','utf8',str(RUN/'construction.py'),'--output',str(out/'reconstructed_candidate.json')]],ROOT),
      ('dag',[[sys.executable,'-I','-X','utf8','dag/validate_derivation_dag.py','--no-files']],ROOT),
      ('sync_unified',[[sys.executable,'-I','-X','utf8','dag/sync_unified_dag.py','--check']],ROOT),
      ('sync_applications',[[sys.executable,'-I','-X','utf8','dag/sync_application_branches.py','--check']],ROOT),
      ('sync_pregenesis',[[sys.executable,'-I','-X','utf8','dag/sync_pregenesis_to_wdp.py','--check']],ROOT),
      ('contracts',[[sys.executable,'-X','utf8','scripts/contract_scores.py','check']],ROOT),
      ('whitespace',[['git','diff','--check',BASE]],ROOT),
    ]
    def execute(task):
        name,commands,cwd=task;env=os.environ.copy()
        env.setdefault('CARGO_TARGET_DIR',str(ROOT.parent/'cfs-target'))
        env.update(CARGO_PROFILE_DEV_DEBUG='0',CARGO_PROFILE_TEST_DEBUG='0',CARGO_INCREMENTAL='0')
        started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
        outputs=[];steps=[]
        for cmd in commands:
            p=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            outputs.append(p.stdout);steps.append({'argv':cmd,'exit_code':p.returncode})
            if p.returncode:break
        data=b'\n'.join(outputs);(out/(name+'.log')).write_bytes(data)
        record={'name':name,'cwd':str(cwd),'started_utc':started,'elapsed_seconds':round(time.monotonic()-t,3),
          'steps':steps,'exit_code':steps[-1]['exit_code'],'output':name+'.log','output_sha256':hashlib.sha256(data).hexdigest()}
        write(out/(name+'.command.json'),record);print(name+': '+str(record['exit_code']),flush=True)
        return record
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(execute,tasks))
    write(out/'commands.json',results)
    axioms={};log=(out/'lean.log').read_text(encoding='utf-8',errors='replace')
    for name,items in re.findall(r"'(OperationalIndependence\.[^']+)' depends on axioms: \[([^]]*)\]",log):
        axioms[name]=[x.strip() for x in items.split(',') if x.strip()]
    for name in re.findall(r"'(OperationalIndependence\.[^']+)' does not depend on any axioms",log):axioms[name]=[]
    allowed={'propext','Classical.choice','Quot.sound'}
    source='\n'.join((ROOT/p).read_text(encoding='utf-8') for p in LEAN_SOURCES)
    audit={'headlines':axioms,'expected':sorted(HEADLINES),'allowed':sorted(allowed),
        'all_passed':set(axioms)==HEADLINES and all(set(v)<=allowed for v in axioms.values()) and results[0]['exit_code']==0
        and not re.search(r'\b(sorry|admit|native_decide)\b',source) and not re.search(r'^\s*axiom\s',source,re.M)}
    write(out/'axioms.json',audit)
    reports={}
    for filename,expected in [('independence_mutations.json',237),('filter_mutations.json',623),('mutations.json',277)]:
        files=list((out/'pytest_tmp').rglob(filename))
        report=json.loads(files[0].read_bytes()) if len(files)==1 else {'all_rejected':False,'count':0}
        report['expected_count']=expected;report['coverage_passed']=report['count']==expected and report['all_rejected']
        reports[filename]=report;write(out/filename,report)
    identical=(out/'reconstructed_candidate.json').is_file() and (out/'reconstructed_candidate.json').read_bytes()==(RUN/'candidate.json').read_bytes()
    verify_pins(pins);unchanged=raw==(RUN/'source_pins.json').read_bytes()
    protected=['dag/derivation_dag.json','dag/pfp','dag/prompts','dag/operads','dag/results']
    diff=subprocess.run(['git','diff','--name-only',BASE,'--',*protected],cwd=ROOT,capture_output=True,check=True).stdout.decode().splitlines()
    changed_old=[p for p in diff if not p.startswith(PREFIX+'/')]
    custody={'historical_and_canonical_changes':changed_old,'unchanged':not changed_old,'baseline_pin_envelope_sha256':digest(ROOT/BASELINE)}
    write(out/'custody.json',custody)
    versions={}
    for name,cmd in [('git',['git','rev-parse','HEAD']),('python',[sys.executable,'--version']),
      ('lean',['lake','env','lean','--version']),('rust',['rustc','--version']),
      ('mathlib',['git','-C',str(ROOT/'lean4/.lake/packages/mathlib'),'rev-parse','HEAD'])]:
        p=subprocess.run(cmd,cwd=ROOT/'lean4',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        versions[name]={'argv':cmd,'exit_code':p.returncode,'output':p.stdout.decode(errors='replace').strip()}
    write(out/'environment.json',versions)
    candidate_passed=json.loads((out/'candidate.log').read_bytes())['all_passed']
    python_log=(out/'python.log').read_text(encoding='utf-8',errors='replace')
    rust_log=(out/'rust.log').read_text(encoding='utf-8',errors='replace')
    counts={'python':49 if re.search(r'\b49 passed\b',python_log) else None,
      'rust':347 if 'test result: ok. 347 passed; 0 failed' in rust_log else None}
    passed=candidate_passed and all(x['exit_code']==0 for x in results) and audit['all_passed'] and all(x['coverage_passed'] for x in reports.values()) and identical and unchanged and custody['unchanged'] and all(counts.values())
    receipt={'authority_effect':'None','all_passed':passed,'base_sha':BASE,'candidate_sha256':CANDIDATE_SHA,
       'source_pin_envelope_sha256':hashlib.sha256(raw).hexdigest(),'source_count':len(pins['files']),
       'sources_verified_before_and_after':unchanged,'historical_and_canonical_unchanged':custody['unchanged'],
       'construction_byte_identical':identical,'candidate_passed':candidate_passed,'headline_count':len(HEADLINES),
       'tests_passed':counts,'independence_mutants_rejected':reports['independence_mutations.json']['count'],
       'filter_mutants_rejected':reports['filter_mutations.json']['count'],'tomography_mutants_rejected':reports['mutations.json']['count'],
       'pin_guard_mutants_rejected':len(guards),
       'scope':'three new Lean modules with universal finite operational laws and independence; inherited filter/selection/hidden modules; full finite-probability Rust library; four Python modules; DAG sync and contracts; not the entire repository suite'}
    write(out/'receipt.json',receipt);print(json.dumps(receipt,indent=2),flush=True)
    if not passed:raise SystemExit(1)


if __name__=='__main__': main()
