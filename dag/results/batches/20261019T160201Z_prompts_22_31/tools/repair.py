"""Retained P3 repair of real missing dependencies/compiler failures."""
import copy,importlib.util,json,sys,yaml
from pathlib import Path
BATCH=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('s',BATCH/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
node=json.loads((BATCH/'selection.json').read_bytes())['nodes'][0];task=node['node_id'];run=s.root_run(task)
attempt=sys.argv[1] if len(sys.argv)>1 else 'p3';old_attempt='p1' if attempt=='p3' else sys.argv[2];host='p2' if old_attempt=='p1' else 'p2_after_'+old_attempt
request=s.prepare.build_packet(s.ROOT/node['prompt'],'P3_REPAIR',attempt_id=attempt,reviewed_path=run/'p0/reviewed_missions.json',review_path=run/'p0/host_review.json',candidate_path=run/old_attempt/'candidate.json',host_check_path=run/host/'host_check.json');s.save(run/attempt/'request.json',request)
old=json.loads((run/old_attempt/'candidate.json').read_bytes());new=copy.deepcopy(old);new.update({k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')})
names=[p['path'].split('/'+old_attempt+'/construction/',1)[1] for p in old['source_pins']]
names=list(dict.fromkeys(names+['lean4/E003_projection_fiber_primitive_difference.lean','lean4/E005_fiber_quotient_equivalence.lean']))
new['source_pins']=s.snapshots(names,run/attempt/'construction');s.save(run/attempt/'candidate.json',new)
if new['data']!=old['data']:raise ValueError('Numerical certificate changed in dependency repair')
delta=yaml.safe_load((run/old_attempt/'operad_delta.yaml').read_bytes());finding='Fresh P2 found H000 imports E003/E005 without local source or oleans. Add new minimal report-fiber definitions/proofs with explicit provenance; do not pretend they are recovered historical bytes.' if attempt=='p3' else 'Retained compiler diagnostics require the explicit successor proof repair; no original numerical candidate or intended statement is changed.'
delta['failed_compositions'].append({'proposal':'Accept the prior uncompiled shared proof submission','reason':finding})
for relation in delta['add_or_refine_relations']:relation['source_pins']=new['source_pins'];relation['evidence_status']='P3 repair awaiting actual fresh native/kernel acceptance.'
s.yaml_new(run/attempt/'operad_delta.yaml',delta)
response={**{k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'replacement_candidate_certificate':new,'repaired_invariants':['G5_SCOPE: '+finding],'remaining_obligations':delta['open_obligations'],'operad_delta':delta,'claim_boundary':json.loads((run/'p0/profile.json').read_bytes())['claim_boundary'],'execution':'Local actual compiler/dependency repair, not an independent-author or blinded model trial.'}
s.save(run/attempt/'response.json',response);s.save(run/attempt/'raw_response.json',response)
p=run/'p1/review_contract.json';contract=json.loads(p.read_bytes());s.save(run/attempt/'review_contract_before.json',contract);contract['attempts'][attempt]={'request_sha256':s.sha(run/attempt/'request.json'),'source_pins':{p['path']:p['sha256'] for p in new['source_pins']}};p.write_bytes((json.dumps(contract,indent=2)+'\n').encode());s.save(run/attempt/'review_contract_after.json',contract)
result=s.p2(task,attempt=attempt,checkpoint='p2_after_'+attempt,lean_dependencies=['E003_projection_fiber_primitive_difference','E005_fiber_quotient_equivalence','H000FinitePresentedCarrier'])
print(result['status'],flush=True)
