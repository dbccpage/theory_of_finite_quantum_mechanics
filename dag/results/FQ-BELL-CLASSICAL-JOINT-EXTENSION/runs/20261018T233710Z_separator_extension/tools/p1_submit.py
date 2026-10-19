import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
from fractions import Fraction as Q
import yaml

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T233710Z_separator_extension'
P1=RUN/'p1'
request=json.loads((P1/'request.json').read_bytes())
public=request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']
spec=importlib.util.spec_from_file_location('separator',ROOT/'code/python/src/qm/bell_separator_extension.py')
bell=importlib.util.module_from_spec(spec);sys.modules[spec.name]=bell;spec.loader.exec_module(bell)
answers=[]
for case in public['cases']:
    p=[[Q(x) for x in row] for row in case['pairs']];a=bell.construct_extension(p)
    answers.append({'id':case['id'],'status':'extended' if a.weights is not None else 'blocked',
     'lower':list(map(str,a.analysis.lower)),'upper':list(map(str,a.analysis.upper)),'facets':list(map(str,a.analysis.facets)),
     'separator':str(a.separator) if a.separator is not None else None,'triples':[list(map(str,t)) for t in a.triples] if a.triples is not None else None,
     'weights':list(map(str,a.weights)) if a.weights is not None else None,'violating_mask':a.violating_mask})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):
    with p.open('xb') as f:f.write((json.dumps(x,separators=(',',':'))+'\n').encode())
candidate={'schema_id':'finite-qm.bell-separator-certificate.v1',**{k:request[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},
 'scope':public['scope'],'cases':answers}
dump(P1/'candidate.json',candidate)
sources=['code/python/src/qm/bell_separator_extension.py','code/python/tests/test_bell_separator_extension.py',
 'code/rust/src/finite_probability/bell_separator_extension.rs','code/rust/src/finite_probability/examples/bell_separator_replay.rs',
 'code/rust/src/finite_probability/lib.rs','lean4/BellSeparatorExtension.lean','lean4/lakefile.lean']
pins=[]
for name in sources:
    dest=P1/'construction'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
    pins.append({'path':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest),'working_source':name})
plan=json.loads((RUN/'presentation_plan.json').read_bytes())
for g in plan['generators']:g['source_pins']=pins;g['evidence_status']='P1 submitted implementation; not yet accepted by P2'
for r in plan['relations']:r['source_pins']=pins;r['evidence_status']='P1 submitted proof source or native certificate predicate; P2 pending'
delta={'add_or_refine_generators':plan['generators'],'add_or_refine_relations':plan['relations'],
 'checked_compositions':[],'failed_compositions':[],'counterexamples':[],
 'open_obligations':['P2 native and Lean verification','P4 same-premise and missing-premise challenges','General rational gluing and input-transport formalization remain open']}
(P1/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta,sort_keys=False,width=100).encode())
response={**{k:request[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},
 'candidate_certificate':{'path':'candidate.json','sha256':sha(P1/'candidate.json')},'construction':pins,
 'remaining_obligations':delta['open_obligations'],'operad_delta':delta,
 'claim_boundary':{'supports':'submitted exact certificates and formal source constructions; not acceptance','does_not_support':'full formal Fine converse or new theorem acceptance before P2',
 'narrowest_claim':public['scope'],'next_test':'independent projection checks and native/kernel compilation'}}
dump(P1/'response.json',response);shutil.copyfile(P1/'response.json',P1/'raw_response.txt')
print('P1 original candidate and construction saved:',len(answers),'cases. P2 pending.')
