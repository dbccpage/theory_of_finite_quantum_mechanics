"""Actual gates and per-output challenges, one task or all prepared tasks."""
import importlib.util,json,sys
from fractions import Fraction
from pathlib import Path
BATCH=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('s',BATCH/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
indices=[int(sys.argv[1])] if len(sys.argv)>1 else list(range(20));attempt=sys.argv[2] if len(sys.argv)>2 else 'p1';checkpoint='p2' if attempt=='p1' else 'p2_after_'+attempt
rows=json.loads((BATCH/'selection.json').read_bytes())['nodes']
for i in indices:
    task=rows[i]['node_id'];run=s.root_run(task)
    if (run/'p5/candidate.json').exists():continue
    deps=json.loads((BATCH/'lean_order.json').read_bytes()) if i==0 and attempt=='p1' else []
    host=json.loads((run/checkpoint/'host_check.json').read_bytes()) if (run/checkpoint/'host_check.json').exists() else s.p2(task,attempt=attempt,checkpoint=checkpoint,lean_dependencies=deps)
    if host['status']!='accepted_candidate_for_challenge':raise ValueError('Actual failure retained; repair required: '+task)
    candidate=json.loads((run/attempt/'candidate.json').read_bytes());records=candidate['data']['records'];mutations=[]
    for a,record in enumerate(records):
        for b,value in enumerate(record['output']):
            def alter(data,a=a,b=b,value=value):data['records'][a]['output'][b]=str(Fraction(value)+1)
            mutations.append(('coordinate_'+str(a)+'_'+str(b),alter))
    mutations += [('missing_record',lambda d:d['records'].pop()),('wrong_input',lambda d:d['records'][0]['input'].__setitem__(0,'123456789')),('boolean_alias',lambda d:d['records'][0]['output'].__setitem__(0,True)),('noncanonical',lambda d:d['records'][0]['output'].__setitem__(0,'2/2'))]
    s.p4(task,mutations,attempt=attempt,host_checkpoint=checkpoint,controls=[{'id':'retained_actual_domain_controls','records':records,'scope':'Computed values, with the source/kernel/native distinctions retained in claim_boundary.'}])
    history=['p0']
    for a in json.loads((run/'p1/review_contract.json').read_bytes())['attempts']:
        h='p2' if a=='p1' else 'p2_after_'+a
        if (run/h/'host_check.json').exists():history += [a,h]
    history+=['p4'];s.p5(task,attempt=attempt,host_checkpoint=checkpoint,attempts=history)
    s.save(run/'accepted.json',{'attempt':attempt,'host':checkpoint,'failed_checkpoints':[p.parent.name for p in run.glob('p2*/host_check.json') if json.loads(p.read_bytes())['status']=='repairable_candidate_defect']})
    print(json.dumps({'task':task,'accepted_attempt':attempt,'rejected_mutations':len(mutations)}),flush=True)
