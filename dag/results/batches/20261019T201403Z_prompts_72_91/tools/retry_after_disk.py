"""Retain incomplete IO evidence, then rerun P2 in a fresh named checkpoint."""
import copy,importlib.util,json,sys,yaml
from fractions import Fraction
from pathlib import Path
B=Path(__file__).resolve().parents[1] if (Path(__file__).resolve().parents[1]/'target_stages.py').exists() else Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics\dag\results\batches\20261019T201403Z_prompts_72_91')
sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
node=json.loads((B/'selection.json').read_bytes())['nodes'][0];task=node['node_id'];run=s.root_run(task);old=run/'p2_after_p3';binding=json.loads((old/'request.json').read_bytes());delta=yaml.safe_load((run/'p3/operad_delta.yaml').read_bytes())
if not (old/'host_check.json').exists():
    result={**{k:binding[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'candidate_sha256':s.sha(run/'p3/candidate.json'),'status':'infrastructure_recording_failure','predicate_results':{'native_exit_codes':{'certificate':0,'python':0,'rust':None,'lean':None,'rust_replay':None},'failure':'OSError errno28 while saving Rust process stdout; its exit status was not retained. Partial output is not accepted as a valid native gate.','disposable_cache_removed':'Resolved ignored code/rust/target/debug/examples only; source/results/operads preserved.'},'bounded_failure_codes':[],'operad_delta':delta,'claim_boundary':'No result accepted from this incomplete checkpoint.'}
    s.save(old/'host_check.json',result);s.save(old/'raw_response.json',result);s.yaml_new(old/'operad_delta.yaml',delta)
h='p2_after_p3_disk_retry';host=s.p2(task,attempt='p3',checkpoint=h,lean_dependencies=[])
if host['status']!='accepted_candidate_for_challenge':raise ValueError('Actual retry failed; retain and repair it')
c=json.loads((run/'p3/candidate.json').read_bytes());mutations=[]
for i,row in enumerate(c['data']['records']):
    for j,v in enumerate(row['output']):
        def mutate(d,i=i,j=j,v=v):d['records'][i]['output'][j]=str(Fraction(v)+1)
        mutations.append(('coordinate_'+str(i)+'_'+str(j),mutate))
mutations += [('missing_record',lambda d:d['records'].pop()),('wrong_input',lambda d:d['records'][0]['input'].__setitem__(0,'123456789')),('boolean_alias',lambda d:d['records'][0]['output'].__setitem__(0,True)),('noncanonical',lambda d:d['records'][0]['output'].__setitem__(0,'2/2'))]
s.p4(task,mutations,attempt='p3',host_checkpoint=h,controls=[{'id':'actual_declared_registry_controls','records':c['data']['records'],'scope':'Declared finite registry/rank inputs, not audited physical interfaces.'}]);s.p5(task,attempt='p3',host_checkpoint=h,attempts=['p0','p1','p2','p3','p2_after_p3',h,'p4']);s.save(run/'accepted.json',{'attempt':'p3','host':h,'failed_checkpoints':['p2'],'infrastructure_checkpoints':['p2_after_p3']})
