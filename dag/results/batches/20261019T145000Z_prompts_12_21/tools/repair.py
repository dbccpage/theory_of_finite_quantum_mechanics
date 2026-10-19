"""P3: repair rejected shared Lean syntax/tactics, retaining all old bytes."""
import copy,importlib.util,json,sys,yaml
from pathlib import Path
BATCH=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('s',BATCH/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
attempt=sys.argv[1] if len(sys.argv)>1 else 'p3'
old_attempt='p1' if attempt=='p3' else 'p3'
old_host='p2' if attempt=='p3' else 'p2_after_p3'
for node in json.loads((BATCH/'selection.json').read_bytes())['nodes']:
    task=node['node_id'];run=s.root_run(task)
    request=s.prepare.build_packet(s.ROOT/node['prompt'],'P3_REPAIR',attempt_id=attempt,reviewed_path=run/'p0/reviewed_missions.json',review_path=run/'p0/host_review.json',candidate_path=run/old_attempt/'candidate.json',host_check_path=run/old_host/'host_check.json')
    s.save(run/attempt/'request.json',request)
    old=json.loads((run/old_attempt/'candidate.json').read_bytes());new=copy.deepcopy(old)
    new.update({k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')})
    names=[p['path'].split('/'+old_attempt+'/construction/',1)[1] for p in old['source_pins']]
    new['source_pins']=s.snapshots(names,run/attempt/'construction');s.save(run/attempt/'candidate.json',new)
    if new['data']!=old['data']:raise ValueError('Numerical mutation during proof repair')
    delta=yaml.safe_load((run/old_attempt/'operad_delta.yaml').read_bytes())
    delta['failed_compositions'].append({'proposal':'Accept the shared initial Lean proof submission','reason':'Actual P2 rejected aliases lacking required type syntax and rational decide reductions; compiler recovery sorryAx was detected and rejected. Old raw errors and failed candidate bytes are retained.','repair':'Add inferred statement type placeholders and numeric proof tactics without altering intended statements or numerical data.'})
    if attempt!='p3':delta['failed_compositions'][-1]={'proposal':'Infer theorem header placeholders from proof terms','reason':'Actual P2_after_p3 rejected theorem header holes before proof elaboration. The numeric tactic repairs passed; the aliases still require full explicit types.','repair':'Write each complete statement with explicit quantifiers/carriers; reuse its exact source proof. No numerical data or theorem hypothesis is weakened.'}
    for r in delta['add_or_refine_relations']:r['source_pins']=new['source_pins'];r['evidence_status']='P3 proof candidate; fresh P2 acceptance required.'
    response={**{k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'replacement_candidate_certificate':new,'repaired_invariants':['G5_SCOPE: compile the intended exact proof statements; reject every sorryAx recovery report'],'operad_delta':delta,'remaining_obligations':delta['open_obligations'],'claim_boundary':json.loads((run/'p0/profile.json').read_bytes())['claim_boundary'],'execution':'Local source repair using actual compiler diagnostics; no blinded-model or independent-author trial.'}
    s.save(run/attempt/'response.json',response);s.save(run/attempt/'raw_response.json',response);s.yaml_new(run/attempt/'operad_delta.yaml',delta)
    p=run/'p1/review_contract.json';contract=json.loads(p.read_bytes());contract['attempts'][attempt]={'request_sha256':s.sha(run/attempt/'request.json'),'source_pins':{p['path']:p['sha256'] for p in new['source_pins']}}
    # Configuration evolution is retained explicitly; no numeric values are stored.
    s.save(run/attempt/'review_contract_before.json',json.loads(p.read_bytes()));p.write_bytes((json.dumps(contract,indent=2)+'\n').encode());s.save(run/attempt/'review_contract_after.json',contract)
    print(task,attempt,'submitted with identical numeric data',flush=True)
