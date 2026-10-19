"""Actual Bell attacks, exact host rejection, and scoped operad collection."""
import copy,hashlib,importlib.util,json
from pathlib import Path
from fractions import Fraction as Q
import sys,yaml

sys.dont_write_bytecode=True
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
TASK='FQ-BELL-RATIONAL-VIOLATION-14-5';RUN=ROOT/'dag/results'/TASK/'runs/20261019T015232Z_staged'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
prepare=module('prepare',ROOT/'dag/pfp/prepare_stage.py');checker=module('rational_bell_checker',RUN/'check_candidate.py')
def save(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('Refusing overwrite: '+str(p))
    p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def yaml_new(p,d):
    if p.exists():raise ValueError('Refusing overwrite')
    p.write_bytes(yaml.safe_dump(d,sort_keys=False,allow_unicode=True,width=100).encode())
accepted=RUN/'p3b/candidate.json';check=RUN/'p2_after_p3b/host_check.json'
host=json.loads(check.read_bytes())
if host['status']!='accepted_candidate_for_challenge':raise ValueError('No accepted candidate')
packet=prepare.build_packet(ROOT/'dag/prompts/FINITE_QM_CORE__FQ-BELL-RATIONAL-VIOLATION-14-5__PROVED_LEAN.yaml','P4_CHALLENGE',attempt_id='p4',reviewed_path=RUN/'p0/reviewed_missions.json',review_path=RUN/'p0/host_review.json',candidate_path=accepted,host_check_path=check)
save(RUN/'p4/request.json',packet)
candidate=json.loads(accepted.read_bytes());public=json.loads((RUN/'public_cases.json').read_bytes());main=candidate['data']['cases'][0]
mutations=[]
def mutant(name,field,value):
    a=copy.deepcopy(main);a[field]=value;p=RUN/'p4/mutants'/(name+'.json');save(p,a)
    try:checker.case(public[0],a)
    except ValueError as error:reason=str(error)
    else:raise ValueError('Accepted false Bell certificate '+name)
    mutations.append({'id':name,'path':p.relative_to(RUN).as_posix(),'rejected':True,'reason':reason})
mutant('normalized_wrong_Born_table','pairs',[['1/4']*4 for _ in range(4)])
e=copy.deepcopy(main['correlations']);e[0]='0';mutant('wrong_correlator','correlations',e)
mutant('wrong_support_count','support_assignments',15)
mutant('wrong_interval','separator_lower','0')
mutant('false_facet_obstruction','violating_mask',1)
raw=accepted.read_bytes();needle=b'"data":';bad=raw.replace(needle,b'"data":{},"data":',1);p=RUN/'p4/mutants/duplicate_raw_certificate.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(bad)
try:checker.check(RUN/'p3b/request.json',p)
except ValueError as error:reason=str(error)
else:raise ValueError('Duplicate raw key accepted')
mutations.append({'id':'duplicate_raw_key','path':p.relative_to(RUN).as_posix(),'rejected':True,'reason':reason})
uniform=candidate['data']['cases'][1];checker.case(public[1],uniform)
weights=[Q(1,16)]*16
for x in range(2):
    for y in range(2):
        row=[sum((weights[m] for m in range(16) if 2*((m>>x)&1)+((m>>(2+y))&1)==k),Q(0)) for k in range(4)]
        if row!=list(map(Q,uniform['pairs'][2*x+y])):raise ValueError('Uniform joint control failed')
controls={'full_support_obstructed':{'case':main['id'],'support_assignments':main['support_assignments'],'chsh':main['chsh'],'minimum_probability':main['minimum_probability']},'same_support_with_positive_joint':{'case':uniform['id'],'support_assignments':uniform['support_assignments'],'chsh':uniform['chsh'],'joint_weights':list(map(str,weights)),'projection_status':'all 16 actual pair cells checked'},'invalid_density_premise':'Gram weights and density equality are required by the same independent checker; this is an admitted-input guard, not a new physical theorem.'}
delta=yaml.safe_load((RUN/'p3b/operad_delta.yaml').read_bytes())
delta['counterexamples']=[{'id':'full_support_not_convex_extension','scope':'Support-set equality cannot supply nonnegative global weights.','controls':controls}]
for g in delta['add_or_refine_generators']:g['evidence_status']='Actual exact native chain checked on three explicit inputs; five kernel anchors prove the stated fixed matrices and scaled joint-law bound. No general probability-subtype operad theorem claimed.'
for r in delta['add_or_refine_relations']:
    r['evidence_status']='Consult literal fixed matrix and scaled assignment-law kernel anchors plus independent finite trace checks; general typed probability transport remains open.'
response={**{k:packet[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'near_miss':mutations,'challenged_predicate':'actual tensor/Born tables and convex positive common-joint feasibility, not support-only matching','valid_control':controls['same_support_with_positive_joint'],'challenge_result':'host-evaluated below; no independent model adversary','operad_delta':delta,'claim_boundary':json.loads((RUN/'p3b/response.json').read_bytes())['claim_boundary']}
save(RUN/'p4/candidate.json',response);save(RUN/'p4/raw_response.json',response);yaml_new(RUN/'p4/operad_delta.yaml',delta)
host4={**{k:packet[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'candidate_sha256':sha(RUN/'p4/candidate.json'),'status':'survives_executed_challenges','predicate_results':{'mutants':mutations,'controls':controls},'bounded_failure_codes':[],'operad_delta':delta}
save(RUN/'p4/host_check.json',host4)
binding={'task_id':TASK,'stage_id':'P5_RECORD','attempt_id':'p5','input_sha256':sha(RUN/'p4/host_check.json')}
save(RUN/'p5/request.json',{**binding,'checked_result':'../p2_after_p3b/host_check.json','challenge':'../p4/host_check.json'})
boundary={'supports':'The supplied rational two-qubit density is positive on its real interpretation, has trace one and binary observables, yields exact CHSH 14/5 with full pair support, and violates the scaled common-positive-assignment-law bound.','does_not_support':'Deriving Born/tensor structure, physical locality/setting independence, a complete formal arbitrary-rational-table transport theorem, or general probability-subtype operad coherence.','narrowest_claim':'Five literal kernel anchors for the fixed admitted quantum matrices and arbitrary Nat-weighted assignment obstruction, plus three independently checked exact native cases and actual mutation rejections.','next_test':'Batch-wide source/custody/claim review after the next nine prompts.'}
result={**binding,'result_or_obstruction':'Exact admitted rational quantum Bell violation with full support; support alone fails to characterize positive common-joint feasibility.','attempt_refs':['p0','p1','p2','p3','p2_after_repair','p3b','p2_after_p3b','p4'],'source_bindings':candidate['source_pins'],'remaining_obligations':delta['open_obligations'],'operad_delta':delta,'next_mathematical_step':'If requested later, connect a general rational joint-table normalization map to the scaled assignment theorem.','claim_boundary':boundary,'status':'prompt_execution_recorded_pending_batch_review','execution_accounting':{'external_provider_calls':0,'chat_cost':'unmeasured','researcher':'one local Codex researcher; independent native predicates, no independent human/model review'}}
save(RUN/'p5/candidate.json',result);save(RUN/'p5/raw_response.json',result);yaml_new(RUN/'p5/operad_delta.yaml',delta)
save(RUN/'p5/host_check.json',{**binding,'candidate_sha256':sha(RUN/'p5/candidate.json'),'status':'scoped_result_recorded_pending_batch_review','predicate_results':{'certificate_checks':3,'Python_tests':6,'Rust_tests':3,'kernel_anchors':5,'mutation_rejections':len(mutations)},'bounded_failure_codes':[],'claim_boundary':boundary})
cpath=ROOT/'dag/operads'/(TASK+'.yaml');c=yaml.safe_load(cpath.read_bytes())
colours=sorted({g['output'] for g in delta['add_or_refine_generators']}|{x for g in delta['add_or_refine_generators'] for x in g['ordered_inputs']})
c['presentation']={'status':'fixed_admitted_quantum_witness_and_scaled_joint_law_obstruction_checked','scope':boundary['narrowest_claim'],'colours':[{'id':x,'meaning':'Fixed-scenario semantic carrier; source hypotheses and basis conventions are retained.'} for x in colours],'generators':delta['add_or_refine_generators'],'relations':delta['add_or_refine_relations'],'compositions':delta['checked_compositions'],'identities':[{'colour':x,'proposed_operation':'id_'+x,'signature':x+' -> '+x,'status':'Semantic identity; no new formal probability-subtype instance claimed.'} for x in colours],'symmetric_actions':[],'coherence_obligations':delta['open_obligations'],'failed_compositions':delta['failed_compositions'],'counterexamples':delta['counterexamples']}
c['open_obligations']=delta['open_obligations'];c['operad_slots']=json.loads((RUN/'p0/reviewed_missions.json').read_bytes())['work_unit']['operad_slots']
c['operad_slots_scope']={'work_unit':(RUN/'p0/reviewed_missions.json').relative_to(ROOT).as_posix(),'scope':'Selected checkable Bell witness within the unmodified original target; FILLED means prerequisites, not independent theorem acceptance.'}
c['stage_history']=[{'stage':json.loads((RUN/folder/'request.json').read_bytes())['stage_id'],'attempt':folder,'run':RUN.relative_to(ROOT).as_posix(),'operad_delta':(RUN/folder/'operad_delta.yaml').relative_to(ROOT).as_posix(),'host_check':(RUN/folder/'host_check.json').relative_to(ROOT).as_posix()} for folder in result['attempt_refs']+['p5']]
c['latest_run']={'path':RUN.relative_to(ROOT).as_posix(),'stage':'P5_RECORD','status':'checked_scoped_result_pending_batch_review'}
c['scope_notes']=['Historical source label PROVED_LEAN does not certify the original full statement.','The density/tensor/Born inputs are admitted; positivity is proved on the canonical real interpretation.','Both actual rejected Lean attempts and their diagnostics remain retained; only the third kernel submission is accepted.']
cpath.write_bytes(yaml.safe_dump(c,sort_keys=False,allow_unicode=True,width=100).encode())
index=ROOT/'dag/operads/index.json';idx=json.loads(index.read_bytes());row=next(n for n in idx['nodes'] if n['node_id']==TASK);row.update({'current_stage':'P5_RECORD','ready_for_derivation':False,'latest_run':RUN.relative_to(ROOT).as_posix(),'status':'checked_scoped_result_pending_batch_review'});index.write_bytes((json.dumps(idx,indent=2,ensure_ascii=False)+'\n').encode())
readme='''# Rational Bell violation staged run

The admitted rational density, tensor observables and Born trace pairing yield
CHSH 14/5, minimum pair probability 1/20 and all 16 support-compatible global
assignments. An actual signed facet still excludes positive common joint weights.
The uniform-density control has the same full support and an explicitly checked
uniform common joint law. Support alone does not distinguish these cases.

Five Lean anchors prove real positivity of the rational density, normalization
and observable involutions, actual Born correlations, strict positivity of all
16 pair cells, and the obstruction for arbitrary positive-mass Nat-weighted
assignment lists. General arbitrary-rational-table transport is not added by a
label. Tensor/Born structure and physical assumptions remain admitted.

P0/P1/P2/P3/P2/P3/P2/P4/P5 are retained. The first two kernel submissions were
rejected and are never accepted as proof. The final compile reports only the
standard logical axioms. Six Python tests, three Rust tests, the independent
Gram/direct-index trace checker, exact Rust/Python agreement on all three inputs,
and six actual mutation rejections passed. No whole-repository or hosted-CI
success is claimed. These are local file-based PFP stages, not provider transcripts.

Every stage has an operad delta. The cumulative collection has six generators,
five relations, an explicit born_trace/tensor insertion, semantic identity scopes,
failed support/positivity insertions and the remaining transport/coherence work.
This result awaits the requested ten-prompt batch review. AuthorityEffect: None.
'''
(RUN/'README.md').write_bytes(readme.encode())
print(json.dumps({'node':TASK,'stage':'P5_RECORD','generators':len(delta['add_or_refine_generators']),'relations':len(delta['add_or_refine_relations']),'mutants_rejected':len(mutations),'batch_review':'pending'}))
