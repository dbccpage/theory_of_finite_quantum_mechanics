"""Retain a semantic carrier correction, without overwriting prior stage evidence."""
import copy,importlib.util,json,sys,yaml
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');B=ROOT/'dag/results/batches/20261019T164251Z_prompts_32_51'
plan=json.loads((B/'upstream/reconciliation_plan.json').read_bytes());task='DS-CPTP-COMPLETE-POSITIVITY-IMPORT';node=next(n for n in json.loads((B/'selection.json').read_bytes())['nodes'] if n['node_id']==task)
run=ROOT/node['run'];review=run.parent.parent/'reviews/20261019_dynamics_audit';path=ROOT/plan['nodes'][task]['operad_collection'];collection=yaml.safe_load(path.read_bytes());delta=yaml.safe_load((review/'operad_delta.yaml').read_bytes())
old='RationalPositiveRankOneMatrix4';new='RationalNonnegativeRankAtMostOneMatrix4'
def replace(value):
    if isinstance(value,str):return value.replace(old,new)
    if isinstance(value,list):return [replace(v) for v in value]
    if isinstance(value,dict):return {k:replace(v) for k,v in value.items()}
    return value
accepted=json.loads((run/'accepted.json').read_bytes());candidate=json.loads((run/accepted['attempt']/'candidate.json').read_bytes());zero=next(r for r in candidate['data']['records'] if r['input']==['0'])
sys.path.insert(0,str(ROOT/'dag/pfp'));from dynamics_checker import verify
verify('cptp',zero['input'],zero['output'])
if zero['output'][:32]!=['0']*32:raise ValueError('Zero-scale matrices are not zero')
delta=replace(delta);delta['counterexamples'].append({'id':'zero_scale_rank_control','input':['0'],'actual_zero_matrix_entries':zero['output'][:16],'finding':'At t=0 the Bell matrix has rank zero. The admitted nonnegative-scale carrier must say rank at most one; rank one and a strictly negative witness require t>0.'})
delta['failed_compositions'].append({'proposal':'Map all nonnegative scales, including zero, into an exactly rank-one carrier','reason':'The retained t=0 matrix is zero. The corrected carrier is nonnegative and rank at most one.'})
for p,data in [(review/'operad_delta_v2.yaml',delta),(review/'scope_review_v2.json',{'task_id':task,'finding':'Corrected the zero-scale rank-one carrier annotation to nonnegative rank at most one. The negative witness remains conditional on t>0.','actual_retained_zero_scale_record':zero,'unchanged':'Every original numerical record and stage receipt; no failed checkpoint promoted.','supersedes':'scope_review.json for this carrier annotation only','authority_effect':'None'})]:
    if p.exists():raise ValueError('Refuse overwrite '+str(p))
    p.write_bytes((yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=100) if p.suffix=='.yaml' else json.dumps(data,indent=2)+'\n').encode())
collection['presentation']=replace(collection['presentation']);collection['presentation'].update(generators=delta['add_or_refine_generators'],relations=delta['add_or_refine_relations'],compositions=delta['checked_compositions'],counterexamples=delta['counterexamples'],failed_compositions=delta['failed_compositions'])
collection['operad_slots']=replace(collection['operad_slots']);collection['latest_review']['operad_delta']=(review/'operad_delta_v2.yaml').relative_to(ROOT).as_posix();collection['latest_review']['carrier_refinement']=(review/'scope_review_v2.json').relative_to(ROOT).as_posix();path.write_bytes(yaml.safe_dump(collection,sort_keys=False,allow_unicode=True,width=100).encode())
p=B/'tools/finalize.py';t=p.read_text();oldtext="delta=yaml.safe_load((review/'operad_delta.yaml').read_bytes())";newtext="canonical=yaml.safe_load((s.ROOT/migration['nodes'][task]['operad_collection']).read_bytes());delta=yaml.safe_load((s.ROOT/canonical['latest_review']['operad_delta']).read_bytes())"
if oldtext not in t:raise ValueError('Missing finalizer delta binding')
t=t.replace(oldtext,newtext).replace('Source labels and original prompts','Source labels and original prompts')
t=t.replace('Specific repairs/fences include:', 'The Bell-input carrier was also corrected to rank at most one: the retained zero-scale control has rank zero, and negativity requires positive scale. Specific repairs/fences include:')
p.write_bytes(t.encode());(B/'tools/post_review_repairs.py').write_bytes(Path(__file__).read_bytes());print('Retained and corrected the zero-scale carrier counterexample.')
