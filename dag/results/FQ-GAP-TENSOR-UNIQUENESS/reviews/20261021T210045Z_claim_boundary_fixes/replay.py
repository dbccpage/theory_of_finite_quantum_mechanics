"""Replay the claim-boundary repairs without rewriting historical evidence.
AuthorityEffect: None. Scoped source custody, not a hermetic whole-repository build.
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

REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parents[4]
PREFIX=REVIEW.relative_to(ROOT).as_posix()
BASE='d65cbaf95732567cc558946f43e816508e232b18'
BASELINE='dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T200001Z_pr147/source_pins.json'
BASELINE_SHA='c187c5cc21fc2279440cb26549f22fc07c23889d06339aa97a7ea1ffddfc8fa2'
TOM='dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography'
FIL='dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family'
DOCS={TOM+'/README.md',FIL+'/README.md',
 'dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T182843Z_pr144/README.md',
 'dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T200001Z_pr147/README.md'}
LEAN=['OperationalTomography','OperationalFilterFamily','OperationalFieldSelection','OperationalBoundaryWitnesses']
REPAIRED=set(DOCS)|{'lean4/'+x+'.lean' for x in LEAN}|{'lean4/lakefile.lean'}
for stem,ext in [('code/python/tests/test_operational_tomography','.py'),('code/python/tests/test_operational_filters','.py'),
 ('code/rust/src/finite_probability/operational_tomography','.rs'),('code/rust/src/finite_probability/operational_filters','.rs')]:
 REPAIRED.update([stem+ext,stem+ext+'.doc.yaml',stem+'.contract.score.yaml'])
REVIEW_INPUTS=['README.md','user_request.txt','replay.py','audit_spec.json','.gitignore','.gitattributes']

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_bytes((json.dumps(x,indent=2)+'\n').encode())
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def inherited():
 if digest(ROOT/BASELINE)!=BASELINE_SHA:raise ValueError('BASELINE_PIN_ENVELOPE')
 return json.loads((ROOT/BASELINE).read_bytes())['files']
def required_sources():
 # All crate sources at the fixed base are covered, as well as task dependencies.
 rust=git('ls-tree','-r','--name-only',BASE,'--','code/rust/src/finite_probability').decode().splitlines()
 return set(inherited())|{BASELINE,'dag/render_dag_views.py'}|REPAIRED|{PREFIX+'/'+s for s in REVIEW_INPUTS}|{p for p in rust if p.endswith('.rs')}
def verify_pins(pins):
 if set(pins)!={'base_sha','request_sha256','files'} or pins['base_sha']!=BASE:raise ValueError('PIN_ENVELOPE')
 if type(pins['files']) is not dict or set(pins['files'])!=required_sources():raise ValueError('PIN_COVERAGE')
 for name,sha in pins['files'].items():
  p=(ROOT/name).resolve()
  if not p.is_relative_to(ROOT) or not isinstance(sha,str) or not re.fullmatch('[0-9a-f]{64}',sha) or digest(p)!=sha:raise ValueError('PIN_MISMATCH:'+name)
 if pins['request_sha256']!=digest(REVIEW/'user_request.txt'):raise ValueError('REQUEST_BYTES')
 for name,sha in inherited().items():
  if name=='dag/derivation_dag.json':
   if (ROOT/name).read_bytes()!=git('show',BASE+':'+name):raise ValueError('DAG_BASE_BYTES')
  elif name not in REPAIRED and pins['files'][name]!=sha:
   if (ROOT/name).read_bytes()!=git('show',BASE+':'+name):raise ValueError('UNREVIEWED_SOURCE_CHANGE:'+name)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
 out=parser.parse_args().output.resolve();out.mkdir(parents=True,exist_ok=False)
 raw=(REVIEW/'source_pins.json').read_bytes();pins=json.loads(raw);verify_pins(pins)
 guards=[]
 for mode in ('missing','extra','corrupt'):
  bad=copy.deepcopy(pins);key='lean4/OperationalBoundaryWitnesses.lean'
  if mode=='missing':del bad['files'][key]
  elif mode=='extra':bad['files']['../outside']='0'*64
  else:bad['files'][key]='0'*64
  try:verify_pins(bad)
  except ValueError as exc:guards.append({'mode':mode,'rejected':True,'reason':str(exc)})
  else:raise RuntimeError('PIN_GUARD_ACCEPTED:'+mode)
 write(out/'pin_guards.json',guards)
 py=[sys.executable,'-X','utf8'];isolated=[sys.executable,'-I','-X','utf8']
 tasks=[('lean',[['lake','build',*LEAN,'TensorHiddenCoordinates'],['lake','env','lean','OperationalBoundaryWitnesses.lean']],ROOT/'lean4'),
  ('rust',[['cargo','test','--manifest-path','code/rust/Cargo.toml','--locked','--offline','-p','tfqm_finite_probability','--lib']],ROOT),
  ('python',[py+['-m','pytest','code/python/tests/test_operational_tomography.py','code/python/tests/test_operational_filters.py','code/python/tests/test_complex_selection.py','-q','--basetemp',str(out/'pytest_tmp')]],ROOT),
  ('oracle144',[isolated+['dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T182843Z_pr144/independent_oracle.py',TOM+'/p1/candidate.json']],ROOT),
  ('oracle147',[isolated+['dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T200001Z_pr147/independent_oracle.py',FIL+'/candidate.json']],ROOT),
  ('construct144',[isolated+[TOM+'/p1/construction.py','--output',str(out/'candidate144.json')]],ROOT),
  ('construct147',[isolated+[FIL+'/construction.py','--output',str(out/'candidate147.json')]],ROOT),
  ('dag',[isolated+['dag/validate_derivation_dag.py','--no-files']],ROOT),
  ('sync_unified',[isolated+['dag/sync_unified_dag.py','--check']],ROOT),
  ('sync_applications',[isolated+['dag/sync_application_branches.py','--check']],ROOT),
  ('sync_pregenesis',[isolated+['dag/sync_pregenesis_to_wdp.py','--check']],ROOT),
  ('contracts',[py+['scripts/contract_scores.py','check']],ROOT),
  ('whitespace',[['git','diff','--check',BASE]],ROOT)]
 def execute(task):
  name,commands,cwd=task;env=os.environ.copy();env.setdefault('CARGO_TARGET_DIR',str(ROOT.parent/'cfs-target'))
  env.update(CARGO_PROFILE_DEV_DEBUG='0',CARGO_PROFILE_TEST_DEBUG='0',CARGO_INCREMENTAL='0')
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();outputs=[];steps=[]
  for cmd in commands:
   p=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   outputs.append(p.stdout);steps.append({'argv':cmd,'exit_code':p.returncode})
   if p.returncode:break
  data=b'\n'.join(outputs);(out/(name+'.log')).write_bytes(data)
  record={'name':name,'cwd':str(cwd),'started_utc':start,'elapsed_seconds':round(time.monotonic()-t,3),'steps':steps,'exit_code':steps[-1]['exit_code'],'output':name+'.log','output_sha256':hashlib.sha256(data).hexdigest()}
  write(out/(name+'.command.json'),record);print(name+': '+str(record['exit_code']),flush=True);return record
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(execute,tasks))
 write(out/'commands.json',results)
 expected=set(json.loads((REVIEW/'audit_spec.json').read_bytes())['headlines']);axioms={}
 log=(out/'lean.log').read_text(encoding='utf-8',errors='replace')
 for name,items in re.findall(r"'(Operational[^']+)' depends on axioms: \[([^]]*)\]",log):
  axioms[name]=[x.strip() for x in items.split(',') if x.strip()]
 for name in re.findall(r"'(Operational[^']+)' does not depend on any axioms",log):axioms[name]=[]
 allowed={'propext','Classical.choice','Quot.sound'}
 source='\n'.join((ROOT/'lean4'/ (x+'.lean')).read_text(encoding='utf-8') for x in LEAN)
 audit={'expected':sorted(expected),'headlines':axioms,'allowed':sorted(allowed),'all_passed':expected==set(axioms) and all(set(v)<=allowed for v in axioms.values()) and results[0]['exit_code']==0 and not re.search(r'\b(sorry|admit|native_decide)\b',source) and not re.search(r'^\s*axiom\s',source,re.M)}
 write(out/'axioms.json',audit)
 reports={}
 for filename,count in [('mutations.json',277),('filter_mutations.json',623)]:
  files=list((out/'pytest_tmp').rglob(filename));report=json.loads(files[0].read_bytes()) if len(files)==1 else {}
  report['coverage_passed']=report.get('count')==count and report.get('all_rejected') is True and report.get('kind')=='fixture_integrity'
  reports[filename]=report;write(out/('fixture_integrity_'+filename),report)
 identical=all((out/f'candidate{n}.json').is_file() and (out/f'candidate{n}.json').read_bytes()==(ROOT/path).read_bytes() for n,path in [(144,TOM+'/p1/candidate.json'),(147,FIL+'/candidate.json')])
 oracle_passed=all(json.loads((out/(name+'.log')).read_bytes()).get('all_passed') is True for name in ['oracle144','oracle147'])
 changed=git('diff','--name-only',BASE,'--','dag/derivation_dag.json','dag/pfp','dag/prompts','dag/operads','dag/results').decode().splitlines()
 unexpected=[p for p in changed if p not in DOCS and not p.startswith(PREFIX+'/')]
 custody={'expected_document_edits':sorted(DOCS),'unexpected_historical_or_canonical_changes':unexpected,'passed':not unexpected,'historical_pin_envelope_sha256':digest(ROOT/BASELINE)}
 write(out/'custody.json',custody)
 verify_pins(pins);unchanged=raw==(REVIEW/'source_pins.json').read_bytes()
 versions={}
 for name,cmd in [('git',['git','rev-parse','HEAD']),('python',[sys.executable,'--version']),('lean',['lake','env','lean','--version']),('rust',['rustc','--version']),('mathlib',['git','-C',str(ROOT/'lean4/.lake/packages/mathlib'),'rev-parse','HEAD'])]:
  p=subprocess.run(cmd,cwd=ROOT/'lean4',stdout=subprocess.PIPE,stderr=subprocess.STDOUT);versions[name]={'argv':cmd,'exit_code':p.returncode,'output':p.stdout.decode(errors='replace').strip()}
 versions['local_rust_path_dependencies']='Existing external Omega crates specified by Cargo.toml; not vendored or included in this task source envelope.'
 write(out/'environment.json',versions)
 passed=all(r['exit_code']==0 for r in results) and audit['all_passed'] and all(r['coverage_passed'] for r in reports.values()) and identical and oracle_passed and custody['passed'] and unchanged
 receipt={'authority_effect':'None','all_passed':passed,'base_sha':BASE,'source_pin_envelope_sha256':hashlib.sha256(raw).hexdigest(),'source_count':len(pins['files']),'sources_verified_before_and_after':unchanged,'headline_count':len(expected),'historical_candidates_byte_identical':identical,'historical_custody_passed':custody['passed'],'independent_oracles_passed':oracle_passed,'fixture_integrity_counts':{name:r.get('count') for name,r in reports.items()},'scope':'Four operational Lean modules plus TensorHiddenCoordinates; full finite-probability Rust library; three Python modules; DAG/sync/contracts; not the entire repository suite or a hermetic external-dependency build.'}
 write(out/'receipt.json',receipt);print(json.dumps(receipt,indent=2),flush=True)
 if not passed:raise SystemExit(1)
if __name__=='__main__':main()
