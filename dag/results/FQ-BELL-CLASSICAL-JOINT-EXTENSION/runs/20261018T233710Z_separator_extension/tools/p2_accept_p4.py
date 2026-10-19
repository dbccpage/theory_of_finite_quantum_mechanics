import copy
import hashlib
import importlib.util
import json
from fractions import Fraction as Q
from pathlib import Path
import shutil
import sys
import yaml

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T233710Z_separator_extension'
NODE='FQ-BELL-CLASSICAL-JOINT-EXTENSION'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):
    with p.open('xb') as f:f.write((json.dumps(x,separators=(',',':'))+'\n').encode())
def require(ok,msg):
    if not ok:raise ValueError(msg)
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
checker=module('checker',RUN/'check_candidate.py');prepare=module('prepare',ROOT/'dag/pfp/prepare_stage.py')
bell=module('separator',ROOT/'code/python/src/qm/bell_separator_extension.py')
accepted=RUN/'p3/candidate.json';request=json.loads((RUN/'p3/request.json').read_bytes());candidate=json.loads(accepted.read_bytes())
for kind in ('python','rust','rust_replay'):
    receipt=json.loads((RUN/'p2'/(kind+'_receipt.json')).read_bytes());require(len(receipt)==1 and receipt[0]['exit_code']==0,'native_failure:'+kind)
for kind,count in [('certificate',1),('lean_recheck',2)]:
    receipt=json.loads((RUN/'p2_after_repair'/(kind+'_receipt.json')).read_bytes());require(len(receipt)==count and all(r['exit_code']==0 for r in receipt),'recheck_failure:'+kind)
lean=(RUN/'p2_after_repair/logs/lean_recheck_1.stdout.log').read_text()
require('sorryAx' not in lean,'unproved_Lean_anchor')
for name in ['separator_iff_chsh','split_triple_exists','chsh_has_two_triples','full_family_joint_necessity']:
    require("'QuantumMechanics.BellSeparatorExtension."+name+"'" in lean,'missing_Lean_anchor:'+name)
for pin in json.loads((RUN/'p3/response.json').read_bytes())['construction']:
    require(sha(ROOT/pin['working_source'])==pin['sha256'],'working_source_changed:'+pin['working_source'])
lines=(RUN/'p2/logs/rust_replay_0.stdout.log').read_text().splitlines()
require(len(lines)==len(candidate['cases']),'native_replay_count')
for line,answer in zip(lines,candidate['cases']):
    fields=line.split('\t');require(fields[:2]==[answer['id'],answer['status']],'native_case_binding')
    flat=answer['lower']+answer['upper']+answer['facets']
    if answer['status']=='extended':flat+=[answer['separator']]+answer['triples'][0]+answer['triples'][1]+answer['weights']
    else:flat+=[str(answer['violating_mask'])]
    require(list(map(Q,fields[2:]))==list(map(Q,flat)),'native_Rust_Python_disagreement:'+answer['id'])
result=checker.check(RUN/'p3/request.json',accepted)
delta=yaml.safe_load((RUN/'p3/operad_delta.yaml').read_bytes())
for g in delta['add_or_refine_generators']:
    g['evidence_status']='exact native composition checked on retained inputs; probability-subtype operad interpretation remains a scoped semantic wrapper'
    g['implementation_note']='Context-retaining mathematical wrapper; construct_extension retains pair data in its local environment. No new formal Lean probability-subtype operad instance is claimed.'
evidence={
 'interval_chsh_equivalence':'Lean separator_iff_chsh at integer scale; explicit rational input transport remains open',
 'triple_slice_feasibility':'Lean existence of r,t0,t1 satisfying the explicit eight-cell positivity systems; normalized Q-array projection additionally checked natively, not yet a general Lean table theorem',
 'conditional_glue_projection':'all retained extension witnesses checked by actual exact pair/triple projection and cross-product equations; general Lean Q gluing remains open',
 'full_facet_necessity':'Lean full_family_joint_necessity for four one-minus faces with both signs, arbitrary Nat-weighted assignment lists'}
for r in delta['add_or_refine_relations']:r['evidence_status']=evidence[r['id']]
plan=json.loads((RUN/'presentation_plan.json').read_bytes())
delta['checked_compositions']=plan['compositions']
for c in delta['checked_compositions']:c['evidence_status']='well-typed semantic plan with exact finite native witness checks; specific Q-subtype operad instantiation remains open'
delta['open_obligations']=['P4 challenge','General rational conditional-gluing theorem in Lean','Formal rational pair-table/common-integer-scale transport and normalized table subtype identities','Full probability-subtype operad instantiation and presentation completeness, if subsequently claimed']
P2=RUN/'p2_after_repair'
(P2/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta,sort_keys=False,width=100).encode())
dump(P2/'request.json',{'task_id':NODE,'stage_id':'P2_VERIFY','attempt_id':'p2_after_repair','input_sha256':sha(accepted),'candidate':'../p3/candidate.json'})
host={'task_id':NODE,'stage_id':'P2_VERIFY','attempt_id':'p2_after_repair','input_sha256':sha(accepted),
 'candidate_sha256':sha(accepted),'status':'accepted_candidate_for_challenge','bounded_failure_codes':[],
 'checker_pins':[{'path':(RUN/'check_candidate.py').relative_to(ROOT).as_posix(),'sha256':sha(RUN/'check_candidate.py')}],
 'predicate_results':{'G1_SCHEMA':'original exact shape, all bindings and context digest passed','G2_COCHAIN':'not applicable: no chain complex',
 'G3_WITNESS':result,'G4_COUNTERMODEL':'all nonextension claims have actual compatible pair data and violated odd-sign CHSH facets',
 'G5_SCOPE':'repaired named kernel anchors compiled with standard axioms only; Q gluing/input transport not promoted'},
 'source_receipt_reuse':'Rust/Python implementations are byte-identical to P1 and their passed native receipts are retained in p2; only the repaired Lean source and changed certificate binding were rechecked.',
 'exact_cross_language_cases':len(lines),'operad_delta':delta,
 'claim_boundary':{'supports':'integer separator/CHSH equivalence, positive cell systems, all-facet necessity and exact finite native certificates',
 'does_not_support':'full formal Fine converse, a general Lean Q gluing theorem, or full probability-subtype operad presentation',
 'narrowest_claim':candidate['scope'],'next_test':'P4 exact zero-slice, separator and obstruction challenges'}}
dump(P2/'host_check.json',host);dump(P2/'candidate.json',{'checked_candidate':'../p3/candidate.json','candidate_sha256':sha(accepted)})
shutil.copyfile(P2/'host_check.json',P2/'raw_response.txt')
prompt=ROOT/'dag/prompts/FINITE_QM_CORE__FQ-BELL-CLASSICAL-JOINT-EXTENSION__PROVED_LEAN.yaml'
P4=RUN/'p4';P4.mkdir(exist_ok=True)
packet=prepare.build_packet(prompt,'P4_CHALLENGE',attempt_id='p4',reviewed_path=RUN/'p0/reviewed_missions.json',review_path=RUN/'p0/host_review.json',candidate_path=accepted,host_check_path=P2/'host_check.json')
dump(P4/'request.json',packet)
public=request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']['cases']
byid={case['id']:case for case in public};answers={a['id']:a for a in candidate['cases']}
extended=next(a for a in candidate['cases'] if a['status']=='extended')
blocked=next(a for a in candidate['cases'] if a['status']=='blocked' and a['violating_mask']!=8)
uniform=next(a for a in candidate['cases'] if all(Q(q)==Q(1,4) for row in byid[a['id']]['pairs'] for q in row))
mutants=P4/'mutants';mutants.mkdir(exist_ok=True);results=[]
def reject_case(name,answer,mutation):
    changed=copy.deepcopy(answer);mutation(changed);p=mutants/(name+'.json');dump(p,changed)
    try:checker.check_case(byid[changed['id']],changed)
    except ValueError as error:results.append({'id':name,'case':changed['id'],'candidate':p.relative_to(RUN).as_posix(),'rejected':True,'reason':str(error)})
    else:raise ValueError('challenge accepted:'+name)
reject_case('wrong_normalized_joint',uniform,lambda a:a.__setitem__('weights',['1']+['0']*15))
reject_case('false_interval',extended,lambda a:a['upper'].__setitem__(0,'2'))
reject_case('wrong_facet_obstruction',blocked,lambda a:a.__setitem__('violating_mask',8))
reject_case('false_triple',uniform,lambda a:a['triples'][0].__setitem__(0,'1'))
# Original raw duplicate bytes, rather than an already-normalized object.
raw=accepted.read_bytes();duplicate=raw.replace(b'"status":"extended"',b'"status":"blocked","status":"extended"',1)
require(duplicate!=raw,'duplicate_probe_did_not_mutate')
dup=mutants/'duplicate_raw_candidate.json';dup.write_bytes(duplicate)
try:checker.check(RUN/'p3/request.json',dup)
except ValueError as error:results.append({'id':'duplicate_raw_key','candidate':dup.relative_to(RUN).as_posix(),'rejected':True,'reason':str(error)})
else:raise ValueError('duplicate raw key accepted')
invalid_pairs=[[str(Q(1,4))]*4 for _ in range(4)];invalid_pairs[0]=['1/2','1/2','0','0']
try:checker.valid_pairs(invalid_pairs)
except ValueError as error:incompatible_reason=str(error)
else:raise ValueError('incompatible pair input accepted')
left=[Q(1)]+[Q(0)]*7;right=[Q(0),Q(1)]+[Q(0)]*6
try:bell.conditional_glue(left,right)
except ValueError as error:mismatch_reason=str(error)
else:raise ValueError('mismatched separator accepted')
ts=[[Q(q) for q in t] for t in uniform['triples']]
naive=[ts[0][(m&3)+4*((m>>2)&1)]*ts[1][(m&3)+4*((m>>3)&1)] for m in range(16)]
require(sum(naive)!=1,'naive-product challenge lacks a violation')
zero_slices=sum(1 for a in candidate['cases'] if a['status']=='extended' and any(Q(a['triples'][0][s])+Q(a['triples'][0][s+4])==0 for s in range(4)))
controls={'valid_control':uniform['id'],'naive_unconditional_product_mass':str(sum(naive)),
 'correct_glued_mass':str(sum(map(Q,uniform['weights']))),'zero_separator_cases_checked':zero_slices,
 'invalid_compatible_premise':{'pairs':invalid_pairs,'rejection':incompatible_reason,'classification':'invalid input, not a nonextension witness for the admitted theorem'},
 'mismatched_triples':{'left':list(map(str,left)),'right':list(map(str,right)),'rejection':mismatch_reason},
 'nonstandard_facet_control':{'case':blocked['id'],'violating_mask':blocked['violating_mask'],'standard_facet_value':blocked['facets'][4],
 'actual_violated_value':blocked['facets'][bell.FACET_MASKS.index(blocked['violating_mask'])]}}
dump(P4/'controls.json',controls)
delta4=copy.deepcopy(delta)
delta4['failed_compositions']=[{'outer_operation':'conditional_glue','input_slot':0,'inner_operation':'unrestricted_triple_pair',
 'colour_match':'fails: arbitrary triple pair is not CompatibleTriplePair','hypothesis_match':'common separator equality is missing',
 'licensing_relations':[],'evidence_status':'native guard refused two positive normalized triples with differing separator marginals'}]
delta4['counterexamples']=[{'id':'naive_product','scope':'omitting conditional denominator violates unit mass; not a counterexample to the correctly typed gluing rule',**controls},
 {'id':'one_facet_is_insufficient','scope':'standard CHSH facet passes but a different odd-sign facet violates the bound',**controls['nonstandard_facet_control']}]
delta4['open_obligations']=delta['open_obligations'][1:]
(P4/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta4,sort_keys=False,width=100).encode())
response={**{k:packet[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},'near_miss':results,
 'challenged_predicate':['actual projection','interval values','all-facet obstruction','triple cells','raw key uniqueness','common separator','zero slices'],
 'valid_control':uniform,'challenge_result':{'mutants':results,'controls':controls},'operad_delta':delta4,
 'claim_boundary':host['claim_boundary']}
dump(P4/'candidate.json',response);shutil.copyfile(P4/'candidate.json',P4/'raw_response.txt')
dump(P4/'host_check.json',{'task_id':NODE,'stage_id':'P4_CHALLENGE','attempt_id':'p4','input_sha256':packet['input_sha256'],
 'candidate_sha256':sha(P4/'candidate.json'),'status':'survives_executed_challenges','predicate_results':response['challenge_result'],'bounded_failure_codes':[],
 'checker_pins':host['checker_pins'],'operad_delta':delta4})
print('Repaired P2 accepted:',result['counts'],'; exact Rust/Python cases:',len(lines),'; P4 rejected:',len(results),'mutants; zero-slice cases:',zero_slices)
