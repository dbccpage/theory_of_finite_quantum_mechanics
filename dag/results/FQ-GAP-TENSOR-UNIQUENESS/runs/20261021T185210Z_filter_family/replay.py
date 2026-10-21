"""Reproduce the source-pinned outcome-filter gates in a new output directory.
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
BASE='3b50a1a980fa8535590356a65ff82b1d682dac29'
BASELINE='dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T182843Z_pr144/source_pins.json'
BASELINE_SHA='e26db6ed0100619f9c37a5e13c23bc802da232132a946dead5dbf89ea3f1edf9'
CANDIDATE_SHA='6ab882ecce87c148400784d3b9b5035fe4d404a5c98f7888f4d6d0276deebe69'
REQUEST_SHA='504c0e7d4f66ff315929209449e5ea45a05e2e2b252a7907b49d871737070bbf'
HEADLINES=set(['OperationalFilterFamily.reset_is_sequential', 'OperationalFilterFamily.reset_admitted', 'OperationalFilterFamily.reset_outcome_filter', 'OperationalFilterFamily.outcome_filter_comp', 'OperationalFilterFamily.resets_irreducible', 'OperationalFilterFamily.reset_pullback', 'OperationalFilterFamily.reset_kills_hidden', 'OperationalFilterFamily.reset_descent_iff_effect_factor', 'OperationalFilterFamily.global_reset_descent_iff_tomography', 'OperationalFilterFamily.circuits_preserve_hidden', 'OperationalFilterFamily.lift_descent', 'OperationalFilterFamily.lift_comp', 'OperationalFilterFamily.lift_irreducible', 'OperationalFilterFamily.product_resets_irreducible_iff', 'OperationalFilterFamily.product_reset_formula', 'OperationalFilterFamily.product_test_pullback', 'OperationalFilterFamily.doubled_reset_kills_hidden', 'OperationalFilterFamily.doubled_protected_reset_no_descent', 'OperationalFilterFamily.admitted_reset_family', 'OperationalFilterFamily.normalized_preparations_span', 'OperationalFilterFamily.normalized_reset_family', 'OperationalFilterFamily.normalization_faithful'])
NEW_CODE=('lean4/OperationalFilterFamily.lean','code/python/src/qm/operational_filters.py',
 'code/python/tests/test_operational_filters.py','code/rust/src/finite_probability/operational_filters.rs')
RUN_SOURCES=('.gitignore','.gitattributes','README.md','user_request.txt','replay.py',
 'construction.py','candidate.json','derivation.json','proposed_dag_delta.json')
INTEGRATION={'lean4/lakefile.lean','code/rust/src/finite_probability/lib.rs'}


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_bytes((json.dumps(x,indent=2)+'\n').encode())


def inherited():
    if digest(ROOT/BASELINE)!=BASELINE_SHA: raise ValueError('BASELINE_PIN_ENVELOPE')
    return json.loads((ROOT/BASELINE).read_bytes())['files']


def required_sources():
    subjects=NEW_CODE[1:]
    companions={s+'.doc.yaml' for s in subjects}|{Path(s).with_suffix('.contract.score.yaml').as_posix() for s in subjects}
    return set(inherited())|set(NEW_CODE)|companions|{BASELINE}|{PREFIX+'/'+s for s in RUN_SOURCES}


def verify_pins(pins):
    if type(pins) is not dict or set(pins)!={'base_sha','candidate_sha256','request_sha256','files'}: raise ValueError('PIN_ENVELOPE')
    if (pins['base_sha'],pins['candidate_sha256'],pins['request_sha256'])!=(BASE,CANDIDATE_SHA,REQUEST_SHA): raise ValueError('PIN_IDENTITY')
    if set(pins['files'])!=required_sources(): raise ValueError('PIN_COVERAGE')
    for name,sha in pins['files'].items():
        p=(ROOT/name).resolve()
        if not p.is_relative_to(ROOT) or type(sha) is not str or not re.fullmatch('[0-9a-f]{64}',sha) or digest(p)!=sha:
            raise ValueError('PIN_MISMATCH:'+name)
    for name,sha in inherited().items():
        if name not in INTEGRATION and pins['files'][name]!=sha: raise ValueError('INHERITED_SOURCE_CHANGED:'+name)
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
      ('lean',[['lake','build','OperationalFilterFamily','OperationalFieldSelection','TensorHiddenCoordinates'],
        ['lake','env','lean','OperationalFilterFamily.lean']],ROOT/'lean4'),
      ('rust',[['cargo','test','--manifest-path','code/rust/Cargo.toml','--locked','--offline','-p','tfqm_finite_probability','--lib']],ROOT),
      ('python',[[sys.executable,'-X','utf8','-m','pytest','code/python/tests/test_operational_filters.py',
        'code/python/tests/test_operational_tomography.py','code/python/tests/test_complex_selection.py','-q','--basetemp',str(out/'pytest_tmp')]],ROOT),
      ('candidate',[[sys.executable,'-I','-X','utf8',NEW_CODE[1],str(RUN/'candidate.json')]],ROOT),
      ('construction',[[sys.executable,'-I','-X','utf8',str(RUN/'construction.py'),'--output',str(out/'reconstructed_candidate.json')]],ROOT),
      ('dag',[[sys.executable,'-I','-X','utf8','dag/validate_derivation_dag.py','--no-files']],ROOT),
      ('sync_unified',[[sys.executable,'-I','-X','utf8','dag/sync_unified_dag.py','--check']],ROOT),
      ('sync_applications',[[sys.executable,'-I','-X','utf8','dag/sync_application_branches.py','--check']],ROOT),
      ('sync_pregenesis',[[sys.executable,'-I','-X','utf8','dag/sync_pregenesis_to_wdp.py','--check']],ROOT),
      ('contracts',[[sys.executable,'-X','utf8','scripts/contract_scores.py','check']],ROOT),
      ('whitespace',[['git','diff','--check']],ROOT),
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
    for name,items in re.findall(r"'(OperationalFilterFamily\.[^']+)' depends on axioms: \[([^]]*)\]",log):
        axioms[name]=[x.strip() for x in items.split(',') if x.strip()]
    for name in re.findall(r"'(OperationalFilterFamily\.[^']+)' does not depend on any axioms",log):axioms[name]=[]
    allowed={'propext','Classical.choice','Quot.sound'}
    source=(ROOT/NEW_CODE[0]).read_text(encoding='utf-8')
    audit={'headlines':axioms,'expected':sorted(HEADLINES),'allowed':sorted(allowed),
        'all_passed':set(axioms)==HEADLINES and all(set(v)<=allowed for v in axioms.values()) and results[0]['exit_code']==0
        and not re.search(r'\b(sorry|admit|native_decide)\b',source) and not re.search(r'^\s*axiom\s',source,re.M)}
    write(out/'axioms.json',audit)
    reports={}
    for filename,expected in [('filter_mutations.json',623),('mutations.json',277)]:
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
    passed=all(x['exit_code']==0 for x in results) and audit['all_passed'] and all(x['coverage_passed'] for x in reports.values()) and identical and unchanged and custody['unchanged']
    receipt={'authority_effect':'None','all_passed':passed,'base_sha':BASE,'candidate_sha256':CANDIDATE_SHA,
       'source_pin_envelope_sha256':hashlib.sha256(raw).hexdigest(),'source_count':len(pins['files']),
       'sources_verified_before_and_after':unchanged,'historical_and_canonical_unchanged':custody['unchanged'],
       'construction_byte_identical':identical,'headline_count':len(HEADLINES),'filter_mutants_rejected':reports['filter_mutations.json']['count'],
       'tomography_mutants_rejected':reports['mutations.json']['count'],'pin_guard_mutants_rejected':len(guards),
       'scope':'new Lean filter-family module and existing selection/hidden modules; full finite-probability Rust library; three Python modules; DAG sync and contracts; not the entire repository suite'}
    write(out/'receipt.json',receipt);print(json.dumps(receipt,indent=2),flush=True)
    if not passed:raise SystemExit(1)


if __name__=='__main__': main()
