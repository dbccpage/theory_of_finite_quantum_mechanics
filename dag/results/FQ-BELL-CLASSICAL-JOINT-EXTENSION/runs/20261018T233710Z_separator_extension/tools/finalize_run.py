import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T233710Z_separator_extension'
HERE=Path(__file__).parent
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_bytes((json.dumps(x,indent=2)+'\n').encode())
protocol=json.loads((RUN/'p5/protocol_receipt.json').read_bytes())
require(len(protocol)==1 and protocol[0]['exit_code']==0,'protocol_tests_did_not_pass')
shutil.copyfile(HERE/'replay.py',RUN/'replay.py')
shutil.copyfile(HERE/'test_replay_guards.py',RUN/'p5/test_replay_guards.py')
command=[sys.executable,'-X','utf8',str(RUN/'p5/test_replay_guards.py'),'-v']
guard=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(RUN/'p5/logs/guards_0.stdout.log').write_bytes(guard.stdout);(RUN/'p5/logs/guards_0.stderr.log').write_bytes(guard.stderr)
dump(RUN/'p5/guards_receipt.json',[{'argv':command,'cwd':str(ROOT),'exit_code':guard.returncode,
 'stdout':'p5/logs/guards_0.stdout.log','stderr':'p5/logs/guards_0.stderr.log'}])
require(guard.returncode==0,guard.stderr.decode(errors='replace'))
text=(HERE/'README.md').read_text()
candidate=json.loads((RUN/'p5/candidate.json').read_bytes());counts=candidate['result_or_obstruction']['native_result']
logs={key:(RUN/path).read_text() for key,path in [('pytests','p2/logs/python_0.stderr.log'),('rusttests','p2/logs/rust_0.stdout.log'),
 ('protocol','p5/logs/protocol_0.stderr.log'),('guards','p5/logs/guards_0.stderr.log')]}
numbers={'extended':counts['extended'],'blocked':counts['blocked'],'cases':sum(counts.values())}
for key,log in logs.items():
    pattern=r'test result: ok\. (\d+) passed; 0 failed' if key=='rusttests' else r'Ran (\d+) tests'
    match=re.search(pattern,log);require(match is not None,'missing_native_summary:'+key);numbers[key]=int(match.group(1))
for key,value in numbers.items():text=text.replace('{{'+key+'}}',str(value))
require('{{' not in text,'unfilled_readme_value');(RUN/'README.md').write_bytes(text.encode())
# P5 remains a local draft until this host recording. Preserve the draft while
# narrowing the summary to the actual Nat-weighted theorem signature.
shutil.copyfile(RUN/'p5/candidate.json',RUN/'p5/candidate_draft.json')
shutil.copyfile(RUN/'p5/raw_response.txt',RUN/'p5/raw_response_draft.txt')
candidate['result_or_obstruction']['formal_result']='At a positive common integer scale, CompatiblePositive PairCounts have a separator iff the eight CHSH facets hold; explicit triple-cell positivity systems have witnesses; every Nat-weighted binary assignment list satisfies the scaled full-facet bound.'
candidate['scope_editorial_note']='The P5 draft was narrowed to exact theorem signatures before host recording; no mathematical input, numerical witness or native source was changed.'
(RUN/'p5/candidate.json').write_bytes((json.dumps(candidate,separators=(',',':'))+'\n').encode())
shutil.copyfile(RUN/'p5/candidate.json',RUN/'p5/raw_response.txt')
for pin in json.loads((RUN/'p3/response.json').read_bytes())['construction']:
    require(sha(ROOT/pin['working_source'])==pin['sha256'],'source_changed_after_native_checks:'+pin['working_source'])
spec=importlib.util.spec_from_file_location('audit',ROOT/'dag/pfp/validate_prompts.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
structural=audit.validate();require(not structural['errors'],str(structural))
dump(RUN/'p5/structural_validation.json',structural)
dump(RUN/'p5/host_check.json',{'task_id':candidate['task_id'],'stage_id':'P5_RECORD','attempt_id':'p5','input_sha256':candidate['input_sha256'],
 'candidate_sha256':sha(RUN/'p5/candidate.json'),'status':'scoped_result_recorded_stopped_for_user_review',
 'predicate_results':{'source_snapshots_match_executed_P3':True,'actual_counts':numbers,'corpus_structure':structural,
 'Lean':'four named repaired reports; no sorry or added axiom acceptance','initial_failed_attempt':'retained in p2, not accepted as theorem evidence'},
 'bounded_failure_codes':[],'operad_delta':'operad_delta.yaml','claim_boundary':candidate['claim_boundary']})
for p in HERE.iterdir():
    if p.is_file():shutil.copyfile(p,RUN/'tools'/p.name)
parent=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/README.md'
prefix=b'> **Latest separator stage:** [20261018 separator extension](runs/20261018T233710Z_separator_extension/README.md). Use that run\'s replay for current source checks. Earlier audit/source pins remain historical. Stopped for review; full formal rational Fine converse remains open.\n\n'
require(not parent.read_bytes().startswith(prefix),'finalizer_already_ran');parent.write_bytes(prefix+parent.read_bytes())
working=candidate['source_bindings']+[{'path':p,'sha256':sha(ROOT/p)} for p in [
 'dag/operads/FQ-BELL-CLASSICAL-JOINT-EXTENSION.yaml','dag/operads/index.json','dag/pfp/prepare_stage.py','dag/pfp/validate_prompts.py','dag/pfp/test_staged_prompts.py']]
def seal():
    manifest={'schema_id':'finite-qm.bell-separator-custody.v1','exclusion':'manifest.json itself and disposable __pycache__ bytecode',
     'working_sources':working,'artifacts':[{'path':p.relative_to(RUN).as_posix(),'sha256':sha(p)} for p in sorted(RUN.rglob('*'))
       if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts]}
    dump(RUN/'manifest.json',manifest)
    return len(manifest['artifacts'])
for label,extra in [('normal',[]),('optimized',['-O'])]:
    seal();argv=[sys.executable,'-X','utf8']+extra+[str(RUN/'replay.py'),'--working-sources']
    result=subprocess.run(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    require(result.returncode==0,result.stderr.decode(errors='replace'))
    (RUN/'p5/logs'/('replay_'+label+'.stdout.log')).write_bytes(result.stdout)
    (RUN/'p5/logs'/('replay_'+label+'.stderr.log')).write_bytes(result.stderr)
    dump(RUN/'p5'/('replay_'+label+'_receipt.json'),{'argv':argv,'exit_code':result.returncode,
      'stdout':'p5/logs/replay_'+label+'.stdout.log','stderr':'p5/logs/replay_'+label+'.stderr.log'})
    print(result.stdout.decode(),flush=True)
print('Final manifest artifacts:',seal(),'; stopped uncommitted for user review.')
