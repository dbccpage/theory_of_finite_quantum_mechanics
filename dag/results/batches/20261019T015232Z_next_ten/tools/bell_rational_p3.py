from pathlib import Path
import copy,hashlib,json,shutil,sys,yaml

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-RATIONAL-VIOLATION-14-5/runs/20261019T015232Z_staged'
STAGING=Path(__file__).resolve().parent
shutil.copyfile(STAGING/'PromptBellRational.lean',ROOT/'lean4/PromptBellRational.lean')
oldstage=sys.argv[1] if len(sys.argv)>1 else 'p1';attempt=sys.argv[2] if len(sys.argv)>2 else 'p3'
old=json.loads((RUN/oldstage/'candidate.json').read_bytes());request=json.loads((RUN/attempt/'request.json').read_bytes())
new=copy.deepcopy(old)
for key in ('task_id','stage_id','attempt_id','input_sha256'):new[key]=request[key]
new['source_pins']=[]
for pin in old['source_pins']:
    relative=pin['path'].split('/'+oldstage+'/construction/',1)[1];target=RUN/attempt/'construction'/relative
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/relative,target)
    new['source_pins'].append({'path':target.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
def save(p,d):
    if p.exists():raise ValueError('Refusing overwrite')
    p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
if old['data']!=new['data']:raise ValueError('Repair changed numerical data')
save(RUN/attempt/'candidate.json',new)
delta=yaml.safe_load((RUN/oldstage/'operad_delta.yaml').read_bytes())
delta['failed_compositions'].append({'outer_operation':'Mathlib rational StarOrderedRing Gram lemma','input_slot':0,'inner_operation':'rational density Gram factorization','colour_match':'Missing required StarOrderedRing Rat instance for the imported lemma','hypothesis_match':'The arithmetic matrix remains rational; positivity is now proved on its canonical real interpretation. No false type-class instance was introduced.','licensing_relations':[],'evidence_status':'Actual P2 compiler rejection retained; representation repaired at P3, recheck still required.'})
delta['add_or_refine_relations']=[r for r in delta['add_or_refine_relations'] if r['id']!='rational_density_real_interpretation']
delta['add_or_refine_relations'].append({'id':'rational_density_real_interpretation','equation_or_predicate':'The entrywise real interpretation of the supplied rational density equals (1/2) phi phi^T and is positive semidefinite.','typing_conditions':'Canonical Q -> R embedding, imported real star-ordered positivity; no new scalar law on Q assumed','source_pins':new['source_pins'],'evidence_status':'P3 proof candidate; await fresh P2 kernel output.','scope':'This concrete density and its exact rational Born tables.'})
response={**{k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'replacement_candidate_certificate':new,'repaired_invariants':['G5_SCOPE: prove positivity on the canonical real interpretation rather than requesting an unavailable Q type-class instance','Use explicit rational entries and kernel-checked finite expansions instead of opaque scalar-action reduction'],'remaining_obligations':delta['open_obligations'],'operad_delta':delta,'claim_boundary':json.loads((RUN/'p1/response.json').read_bytes())['claim_boundary'],'repair_context':'One local researcher used real compiler diagnostics; public P3 feedback contains only bounded G5. No blinded model trial is claimed.'}
if oldstage!='p1':
    response['repaired_invariants']=['G5_SCOPE: import the actual Mathlib real star-order instance; remove an incomplete finite-list case split. All mathematical statements and numerical certificates remain unchanged.']
    delta['failed_compositions'][-1]['evidence_status']='First P3 repair still lacked the real star-order import; no mathematical replacement or weakening of positivity. Both failed kernel outputs retained.'
save(RUN/attempt/'raw_response.json',response);save(RUN/attempt/'response.json',response)
(RUN/attempt/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta,sort_keys=False,allow_unicode=True,width=100).encode())
print('P3 replacement submitted with identical numerical inputs and certificates; original P1 remains retained.')
