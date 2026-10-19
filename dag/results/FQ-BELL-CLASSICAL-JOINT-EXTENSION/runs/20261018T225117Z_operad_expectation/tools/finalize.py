import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import yaml

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
NODE='FQ-BELL-CLASSICAL-JOINT-EXTENSION'
RUN=ROOT/'dag/results'/NODE/'runs/20261018T225117Z_operad_expectation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_bytes((json.dumps(v,indent=2)+'\n').encode())
spec=importlib.util.spec_from_file_location('audit',ROOT/'dag/pfp/validate_prompts.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
structural=audit.validate();assert not structural['errors'],structural
dump(RUN/'p5/structural_validation.json',structural)
for stage in ('p0','p1','p2','p4','p5'):
    delta=yaml.safe_load((RUN/stage/'operad_delta.yaml').read_bytes())
    assert set(delta)=={'add_or_refine_generators','add_or_refine_relations','checked_compositions','failed_compositions','counterexamples','open_obligations'}
for p in (RUN/'p1/construction').rglob('*'):
    if p.is_file():assert sha(p)==sha(ROOT/p.relative_to(RUN/'p1/construction')),str(p)
lean=(RUN/'p2/logs/lean_3.stdout.log').read_text()
assert 'sorryAx' not in lean
assert "'QuantumMechanics.BellOperad.substitute_assoc' does not depend on any axioms" in lean
python=(RUN/'p2/logs/python_0.stderr.log').read_text()
rust=(RUN/'p2/logs/rust_retry_0.stdout.log').read_text()
assert re.search(r'Ran 12 tests.*?OK',python,re.S)
assert '10 passed; 0 failed' in rust
# This records the actual tool completion already observed. It is explicitly an
# excerpt, not reconstructed full stdout or a hosted-CI claim.
dump(RUN/'p5/protocol_tests_receipt.json',{
 'argv':['py','-3.9','-X','utf8','-m','unittest','discover','-s','dag/pfp','-p','test_staged_prompts.py','-v'],
 'cwd':str(ROOT),'exit_code':0,'tool_session_id':26201,'receipt_kind':'transcribed native tool completion excerpt',
 'completion_output_excerpt':'Ran 12 tests in 61.048s\n\nOK',
 'scope':'12 PFP protocol/corpus tests, not executions of the other 176 mathematical targets'})
shutil.copyfile(ROOT/'dag/operads'/(NODE+'.yaml'),RUN/'p5/collection_after.yaml')
for p in Path(__file__).parent.iterdir():
    if p.is_file():shutil.copyfile(p,RUN/'tools'/p.name)
parent=ROOT/'dag/results'/NODE/'README.md'
prefix=b'> **Latest staged run:** [20261018 expectation/operad run](runs/20261018T225117Z_operad_expectation/README.md). P0/P1/P2/P4/P5 completed; stopped for review. Fine converse remains open.\n\n'
assert not parent.read_bytes().startswith(prefix)
parent.write_bytes(prefix+parent.read_bytes())
request=json.loads((RUN/'p5/request.json').read_bytes())
dump(RUN/'p5/host_check.json',{
 **{k:request[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},
 'candidate_sha256':sha(RUN/'p5/candidate.json'),'status':'scoped_result_recorded_stopped_for_user_review',
 'predicate_results':{'all_executed_stages_have_operad_delta':True,'source_custody':'P1 construction matches executed working sources',
 'PFP_protocol_tests':12,'python_domain_tests':12,'rust_domain_tests':10,'exact_cross_language_public_laws':22,
 'Lean':'4.33.1 target dependency chain and BellOperad compiled; axiom reports retained',
 'negative_controls':'four candidate mutants and wrong-colour graft rejected; Lean wrong-sign equality rejected; missing-premise controls retained',
 'corpus_structure':structural},
 'bounded_failure_codes':[],
 'remaining_obligations':'candidate.json and operad_delta.yaml',
 'not_claimed':['Fine converse','full repository test suite','hosted CI','independent human or adversarial model review'],
 'claim_boundary':json.loads((RUN/'p5/candidate.json').read_bytes())['claim_boundary']})
working=json.loads((RUN/'p5/candidate.json').read_bytes())['source_bindings']
working=working+[{'path':p,'sha256':sha(ROOT/p)} for p in ['dag/operads/'+NODE+'.yaml','dag/operads/index.json']]
manifest={'schema_id':'finite-qm.bell-stage-custody.v1','exclusion':'source_manifest.json itself and disposable __pycache__ bytecode',
 'working_sources':working,'artifacts':[{'path':p.relative_to(RUN).as_posix(),'sha256':sha(p)} for p in sorted(RUN.rglob('*'))
 if p.is_file() and p.name!='source_manifest.json' and '__pycache__' not in p.parts]}
dump(RUN/'source_manifest.json',manifest)
p=subprocess.run([sys.executable,'-X','utf8',str(RUN/'replay.py'),'--working-sources'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
print(p.stdout.decode());print(p.stderr.decode());assert p.returncode==0
print('Final P5 source/custody validation passed. Changes are uncommitted for review.')
