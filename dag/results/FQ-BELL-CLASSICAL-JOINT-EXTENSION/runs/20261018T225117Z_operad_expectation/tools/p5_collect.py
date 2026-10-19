import copy
import hashlib
import json
from pathlib import Path
import shutil
import yaml

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
NODE='FQ-BELL-CLASSICAL-JOINT-EXTENSION'
RUN=ROOT/'dag/results'/NODE/'runs/20261018T225117Z_operad_expectation'
P5=RUN/'p5';P5.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def dump(p,v):p.write_bytes((json.dumps(v,indent=2)+'\n').encode())
def ydump(p,v):p.write_bytes(yaml.safe_dump(v,sort_keys=False,width=100).encode())
record_path=ROOT/'dag/operads'/(NODE+'.yaml')
record=yaml.safe_load(record_path.read_bytes())
reviewed=json.loads((RUN/'p0/reviewed_missions.json').read_bytes())
scope=reviewed['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']['scope']
native_sources=['code/python/src/qm/bell_joint_extension.py','code/python/tests/test_bell_joint_extension.py',
 'code/rust/src/finite_probability/bell_joint_extension.rs','code/rust/src/finite_probability/examples/bell_operad_replay.rs',
 'lean4/BellOperad.lean','lean4/BellClassicalJointExtension.lean','lean4/DerivationDagQMClosure.lean','lean4/lakefile.lean',
 'lean4/lean-toolchain','code/rust/Cargo.lock','code/rust/src/finite_probability/Cargo.toml']
pins=[{'path':p,'sha256':sha(ROOT/p)} for p in native_sources]
proof_pins=[x for x in pins if x['path'] in ['lean4/BellOperad.lean','code/python/src/qm/bell_joint_extension.py','code/rust/src/finite_probability/bell_joint_extension.rs']]
# Retain old pilot custody rather than silently replacing its source pins.
for binding in record['source_bindings']:
    if binding.get('role')=='pilot_domain_result' and sha(ROOT/binding['path'])!=binding['sha256']:
        original=binding['path'];snapshot=RUN/'inputs'/original
        assert sha(snapshot)==binding['sha256']
        binding['source_path_at_pilot']=original;binding['path']=rel(snapshot)
        binding['retention_note']='Immutable P0 snapshot of the exact historical pilot source; current implementation has a separate binding.'
for source,symbol in [('lean4/BellOperad.lean','QuantumMechanics.BellOperad.bell_bound'),
 ('code/python/src/qm/bell_joint_extension.py','verify_joint_certificate'),
 ('code/rust/src/finite_probability/bell_joint_extension.rs','verify_joint_certificate')]:
    record['source_bindings'].append({'original_ref':source+'::'+symbol,'availability':'local','path':source,
     'repository':'this_repository','symbol':symbol,'sha256':sha(ROOT/source),'role':'staged_scoped_result',
     'declaration_status':'native_checked_in_bound_run','receipt':rel(RUN/'p2/host_check.json')})
presentation=record['presentation']
presentation['status']='scoped_semantic_substitution_laws_and_bell_composition_checked_full_target_open'
presentation['scope']='Exact rational native Bell generators; generic typed function substitution laws and Bell integer-numerator specialization checked in Lean. No Fine converse, symmetric action or syntactic quotient completeness.'
for g in presentation['generators']:
    g['previous_source_pins']=copy.deepcopy(g['source_pins'])
    g['source_pins']=copy.deepcopy(proof_pins)
    if g['id'] in ['response_products','joint_expectation','chsh_linear']:
        g['evidence_status']='native_exact_Q_API_checked_and_Lean_integer_numerator_model_compiled'
    else:g['evidence_status']='native_certificate_partition_route_checked; general_bound_from_pilot; no_separate_Lean_partition_slack_theorem'
for r in presentation['relations']:
    r['previous_source_pins']=copy.deepcopy(r['source_pins'])
    r['source_pins']=copy.deepcopy(proof_pins)
    if r['id']=='expectation_linearity':
        r['evidence_status']='generic_integral_table_theorem_BellOperad.expect_chsh_checked; exact_Q_native_tests'
        r['scope']='Arbitrary integral response tables in Lean; exact Q tables in Rust/Python; explicit general Q-to-common-denominator table transport remains open.'
    if r['id']=='positive_slacks':r['evidence_status']='independent_exact_sample_recomputation_and_native_tests; general_joint_bound_in_Lean; partition_identities_not_separately_formalized'
for c in presentation['compositions']:
    c['evidence_status']='scoped_Bell_composition_and_semantic_substitution_checked_in_run' if c['outer_operation']!='slack_certificate' else 'native_partition_certificate_route_checked'
for identity in presentation['identities']:
    identity['status']='generic_function_identity_and_simultaneous_substitution_unit_laws_checked; no_mathlib_operad_class_instance'
presentation['ambient_operad']={
 'model':'coloured endomorphism operations; finite ordered input-index restriction of the dependent-function substitution implementation',
 'operation_signature':'Op I A B = ((i:I)->A(i))->B',
 'composition':'substitute f g x = f (i |-> g(i) (j |-> x(i,j)))',
 'flattening':'Sigma input families with explicit index reassociation, supporting empty/nullary and unary families',
 'laws':{'left_unit':'BellOperad.substitute_left_unit','right_unit':'BellOperad.substitute_right_unit',
 'associativity':'BellOperad.substitute_assoc','semantic_congruence':'BellOperad.substitute_congr'},
 'bell_specialization':['productsOp','expectationOp','chshOp','bell_graft','bell_evaluation','bell_bound'],
 'source_pins':[proof_pins[2] if proof_pins[2]['path']=='lean4/BellOperad.lean' else next(x for x in proof_pins if x['path']=='lean4/BellOperad.lean')],
 'boundary':'Kernel-checked substitution semantics and Bell specialization; no named Mathlib Operad instance, explicit symmetric action, or completeness theorem for the listed syntactic presentation.'}
presentation['coherence_obligations']=[
 'Explicit Q-valued general response-table/common-denominator transport and probability-subtype transport in Lean; current generic theorem uses integral tables.',
 'Formal score-partition mass and exact slack identities for arbitrary laws, beyond the general bound theorem and finite native certificate checks.',
 'Specify and prove symmetric actions if subsequently claimed; this run uses nonsymmetric ordered substitution only.',
 'If a syntactic quotient presentation is claimed, define it and prove its universal/completeness property; semantic congruence alone is not that theorem.']
record['operad_slots']=copy.deepcopy(reviewed['work_unit']['operad_slots'])
record['operad_slots_scope']={'work_unit':rel(RUN/'p0/reviewed_missions.json'),'scope':scope,
 'warning':'FILLED means the prerequisites of this selected step were reviewed, not that the original source target or Fine converse is complete.'}
record['latest_run']={'path':rel(RUN),'stage':'P5_RECORD','status':'scoped_result_checked_full_target_open','stop':'user_review_requested'}
record['stage_history'].extend([{'stage':stage,'attempt':attempt,'run':rel(RUN),
 'operad_delta':rel(RUN/attempt/'operad_delta.yaml'),'host_check':rel(RUN/attempt/'host_check.json')}
 for stage,attempt in [('P0_MINE_OPERAD','p0'),('P1_DERIVE','p1'),('P2_VERIFY','p2'),('P4_CHALLENGE','p4'),('P5_RECORD','p5')]])
obligations=[
 'Fine converse remains open: specify compatible binary 2x2 pair-marginal data, check the full relevant inequality family, and construct or certify one common positive extension.',
 *presentation['coherence_obligations'],
 'Physical locality and setting independence remain assumptions, not consequences of finite common-law algebra.']
record['open_obligations']=obligations
record['scope_notes'].append('20261018 staged run checks reusable expectation/substitution semantics and the existing common-law implication. It does not promote the historical PROVED_LEAN label to Fine equivalence.')
# Keep the corpus-level source-candidate status: broad source mining and the full
# target remain open even though one particular work unit has passed P2/P4.
ydump(record_path,record)
index_path=ROOT/'dag/operads/index.json';index=json.loads(index_path.read_bytes())
row=next(x for x in index['nodes'] if x['node_id']==NODE)
row.update({'current_stage':'P5_RECORD','ready_for_derivation':False,'latest_run':rel(RUN),
 'status':'scoped_result_checked_full_target_open','stop_reason':'user_review_requested'})
dump(index_path,index)
delta={'add_or_refine_generators':presentation['generators'],
 'add_or_refine_relations':presentation['relations'], 'checked_compositions':presentation['compositions'],
 'failed_compositions':yaml.safe_load((RUN/'p4/operad_delta.yaml').read_bytes())['failed_compositions'],
 'counterexamples':yaml.safe_load((RUN/'p4/operad_delta.yaml').read_bytes())['counterexamples'], 'open_obligations':obligations}
ydump(P5/'operad_delta.yaml',delta)
attempts=[{'stage':stage,'attempt':attempt,'request':rel(RUN/attempt/'request.json'),
 'candidate':rel(RUN/attempt/'candidate.json'),'operad_delta':rel(RUN/attempt/'operad_delta.yaml')}
 for stage,attempt in [('P0_MINE_OPERAD','p0'),('P1_DERIVE','p1'),('P2_VERIFY','p2'),('P4_CHALLENGE','p4'),('P5_RECORD','p5')]]
request={'task_id':NODE,'stage_id':'P5_RECORD','attempt_id':'p5','input_sha256':sha(RUN/'p4/host_check.json'),
 'checked_result':'../p4/host_check.json','attempt_refs':attempts[:-1]}
dump(P5/'request.json',request)
candidate={**{k:request[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},
 'result_or_obstruction':{'result':scope,'new_work':'generic exact expectation and independent certificate consumers in Rust/Python; Lean substitution coherence, generic integral-table linearity, and Bell composition',
 'obstruction':'Original source target includes a Fine converse; this selected work unit does not establish it.'},
 'attempt_refs':attempts,'source_bindings':pins,'remaining_obligations':obligations,'operad_delta':delta,
 'next_mathematical_step':'After user review: define compatible binary pair-marginal inputs and an exact extension-certificate interface; prove the complete necessary family and pursue a checked extension construction.',
 'claim_boundary':{'supports':scope,'does_not_support':'Fine equivalence, full theorem completion, symmetric/syntactic quotient operad, physical inference',
 'narrowest_claim':'finite supplied-law Bell maps and typed function substitution laws with exact native certificates',
 'next_test':'review this run before any further target or extension work'},
 'execution_accounting':{'mode':'local Codex plus native tools','external_provider_calls':0,'external_provider_cost':'not incurred; active chat cost unmeasured',
 'P3_REPAIR':'not invoked: no mathematical candidate gate failed; P2 infrastructure retry retained separately'},
 'stop':'user_review_requested'}
dump(P5/'candidate.json',candidate);shutil.copyfile(P5/'candidate.json',P5/'raw_response.txt')
# P1's original certificate bytes remain immutable; this links their factual P2
# evaluation without rewriting a rejected or accepted submission.
dump(RUN/'p1/host_check.json',{'task_id':NODE,'stage_id':'P1_DERIVE','attempt_id':'p1',
 'input_sha256':json.loads((RUN/'p1/request.json').read_bytes())['input_sha256'],
 'candidate_sha256':sha(RUN/'p1/candidate.json'),'status':'see_host_stage','host_stage':'../p2/host_check.json'})
for source in native_sources:
    p=RUN/'sources'/source;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/source,p)
tools=RUN/'tools';tools.mkdir(exist_ok=True)
for name in ['p0.py','p1.py','p2_p4.py','native_check.py','install_p1.py','p5_collect.py']:
    shutil.copyfile(Path(__file__).with_name(name),tools/name)
execution=json.loads((RUN/'execution.json').read_bytes())
execution.update({'stages_completed':['P0_MINE_OPERAD','P1_DERIVE','P2_VERIFY','P4_CHALLENGE','P5_RECORD'],
 'P3_REPAIR':'not needed; no candidate defect was observed','status':'stopped_for_user_review_full_target_open',
 'independence':'One Codex researcher/source reviewer; independent native recomputation and Lean kernel checking; no separate adversarial model or human review.'})
dump(RUN/'execution.json',execution)
(RUN/'.gitattributes').write_bytes(b'*.json -text whitespace=cr-at-eol\n*.yaml -text whitespace=cr-at-eol\n*.txt -text whitespace=cr-at-eol\n*.log -text whitespace=cr-at-eol,-blank-at-eof\ninputs/** -text whitespace=-trailing-space,-blank-at-eof\np1/construction/** -text whitespace=-trailing-space,-blank-at-eof\nsources/** -text whitespace=-trailing-space,-blank-at-eof\n')
print('P5 result, cumulative operad collection, source snapshots, and stage history saved; final custody checks pending.')
