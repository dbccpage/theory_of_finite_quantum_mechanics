"""Execute P2/P4/P5 with actual native gates and output-coordinate challenges."""
import importlib.util,json,sys
from fractions import Fraction
from pathlib import Path
BATCH=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('s',BATCH/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
attempt=sys.argv[1] if len(sys.argv)>1 else 'p1'
checkpoint='p2' if attempt=='p1' else 'p2_after_'+attempt
for node in json.loads((BATCH/'selection.json').read_bytes())['nodes']:
    task=node['node_id'];run=s.root_run(task)
    if (run/checkpoint/'host_check.json').exists():host=json.loads((run/checkpoint/'host_check.json').read_bytes())
    else:host=s.p2(task,attempt=attempt,checkpoint=checkpoint)
    if host['status']!='accepted_candidate_for_challenge':raise ValueError('Actual gate failure requires retained P3 repair: '+task)
    if (run/'p5/candidate.json').exists():continue
    candidate=json.loads((run/attempt/'candidate.json').read_bytes());records=candidate['data']['records'];mutations=[]
    for i,record in enumerate(records):
        for j,value in enumerate(record['output']):
            def alter(data,i=i,j=j,value=value):data['records'][i]['output'][j]=str(Fraction(value)+1)
            mutations.append(('output_'+str(i)+'_'+str(j),alter))
    mutations += [('missing_record',lambda d:d['records'].pop()),('wrong_input',lambda d:d['records'][0]['input'].__setitem__(0,'123456789')),('boolean_alias',lambda d:d['records'][0]['output'].__setitem__(0,True)),('noncanonical_rational',lambda d:d['records'][0]['output'].__setitem__(0,'2/2'))]
    controls=[{'id':'retained_domain_controls','records':records,'scope':'Actual computed values; interpretations are restricted by profile claim_boundary. These are not expected-answer inputs.'}]
    history=['p0','p1','p2']+(['p3','p2_after_p3'] if attempt!='p3' else [])+[attempt,checkpoint,'p4']
    result=s.p4(task,mutations,attempt=attempt,host_checkpoint=checkpoint,controls=controls);s.p5(task,attempt=attempt,host_checkpoint=checkpoint,attempts=history)
    print(json.dumps({'task':task,'P4_rejected_mutants':len(result),'P5':'recorded; batch review remains'}),flush=True)
