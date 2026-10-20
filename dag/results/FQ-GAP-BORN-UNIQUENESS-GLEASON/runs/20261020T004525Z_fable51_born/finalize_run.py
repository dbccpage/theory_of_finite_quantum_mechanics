"""Record the review-stopped checkpoint; never turn provider thinking into a theorem."""
from pathlib import Path
import json,hashlib,re,ast,yaml
R=Path(__file__).resolve().parent
ROOT=next(p for p in R.parents if (p/'dag/pfp/prepare_stage.py').is_file())
def load(p):return json.loads(Path(p).read_bytes())
def save(p,v):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
reg=load(R/'registration.json');budget=load(R/'budget.json');p0=load(R/'p0_mine/candidate.json')
if budget['output_used']!=120000 or budget['unknown_outcome'] or (R/'p1_derive/response.txt').read_bytes():raise ValueError('stop-state mismatch')
receipt=load(R/'p2_prepared/matrix_instance_repaired_lean_receipt.json');log=(R/'p2_prepared/matrix_instance_repaired_lean.stdout.log').read_text(encoding='utf-8')
if receipt['exit_code']!=0 or 'sorryAx' in log or 'error:' in log or log.count('depends on axioms:')!=8:raise ValueError('control kernel gate')
for match in re.findall(r'depends on axioms: \[(.*?)\]',log):
 if not set(re.findall(r'[A-Za-z_.]+',match))<={'propext','Classical.choice','Quot.sound'}:raise ValueError('nonstandard axiom')
pins=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in [R/'MatrixInstanceRepaired.lean',R/'contract.lean',R/'p2_prepared/matrix_instance_repaired_lean_receipt.json',R/'numeric_checker.py',R/'numeric_replay.rs',R/'public_input.json']]
gens=[]
for name,ins,out,sem,anchor in [('matrix_add',['Sym2Q','Sym2Q'],'Sym2Q','Coordinate addition','qf_add'),('matrix_scale',['Q','Sym2Q'],'Sym2Q','Rational scalar action','qf_scale'),('qform',['Sym2Q','Q','Q'],'Q','A00*x^2+2*A01*x*y+A11*y^2','qf'),('positive_control',['Effect(space)'],'Q','First diagonal coordinate; a concrete positive unital additive effect valuation','positiveControl')]:
 gens.append({'id':name,'ordered_inputs':ins,'output':out,'arity':len(ins),'carrier':'Fin3->Q, symmetric 2x2 rational quadratic forms with the explicit pointwise quadratic-form order.','coefficient_ring':'Q','hypotheses':['Supplied rational carrier and order; no physical derivation.'],'source_pins':pins,'semantic_predicate':sem,'evidence_status':'host_kernel_checked_control','anchor':'BornMatrixCheck.'+anchor})
rels=[]
for name,eq,anchor in [('qform_add','qf(A+B,x,y)=qf(A,x,y)+qf(B,x,y)','qf_add'),('qform_scale','qf(q*A,x,y)=q*qf(A,x,y)','qf_scale'),('control_positive_unital_additive','positiveControl inhabits EffectValuation(space)','positiveControl')]:
 rels.append({'id':name,'equation_or_predicate':eq,'typing_conditions':['The explicitly supplied rational matrix carrier and, for the valuation, its effect interval.'],'source_pins':pins,'evidence_status':'kernel_checked_control','scope':'Not uniqueness of arbitrary valuations.','anchor':'BornMatrixCheck.'+anchor})
comps=[{'outer_operation':'qform','input_slot':0,'inner_operation':inner,'colour_match':'Sym2Q output matches Sym2Q slot0','hypothesis_match':'Same rational coordinate carrier; no effect-readout inference.','licensing_relations':[rel],'evidence_status':'checked_partial_presentation'} for inner,rel in [('matrix_add','qform_add'),('matrix_scale','qform_scale')]]
delta={'add_or_refine_generators':gens,'add_or_refine_relations':rels,'checked_compositions':comps,'failed_compositions':[{'outer_operation':'positive_control','inner_operation':'matrix_add','reason':'Sym2Q is not Effect(space). Adding E11 to itself exits the effect interval; a summability certificate is required.'},{'outer_operation':'general_effect_valuation','inner_operation':'effect_scale','reason':'No P1 proof of valuation homogeneity was returned.'}],'counterexamples':[{'id':'nonpositive_trace','statement':'The diag(2,-1) functional is unital and additive, but evaluates E22 to -1.','evidence':['BornMatrixCheck.bad_unital','BornMatrixCheck.bad_additive','BornMatrixCheck.bad_not_positive']}],'open_obligations':['All eight general targets in target_types.txt remain without an accepted P1 certificate.','Order-unit extension, rational trace representation and real extension remain proposed.','Complex Hermitian extension, original projective Gleason uniqueness and operational justification remain open.','Full refined-carrier operad unit/substitution/equivariance/coherence is not instantiated.']}
save(R/'host_control_operad_delta.json',delta)
review=load(R/'p0_mine/claim_review.json')
for c in review['claims']:
 n=c['n'];c['disposition']='not_accepted_no_P1_proof_certificate' if n<=6 else 'deferred_not_accepted' if n in (7,8,12) else 'matrix_premises_checked_nonextension_conclusion_deferred' if n==9 else 'explicit_countercontrol_independently_checked' if n==10 else 'source_audit_with_nodup_correction_and_declared_unchecked_dependencies'
save(R/'p0_mine/claim_review.json',review)
p5={'task_id':reg['task_id'],'stage_id':'P5_RECORD','status':'generation_budget_exhausted_stop_for_human_review','result_or_obstruction':'P0 returned a mining proposal. P1 used its entire remaining allowance in thinking and returned zero visible answer bytes. No general effect-valuation theorem or full Born/Gleason uniqueness is accepted. Independent exact controls and a concrete Lean matrix model passed.','attempt_refs':['p0_mine','p1_derive','p2_verify'],'skipped_stages':{'P3_REPAIR':'No generation budget remains.','P4_CHALLENGE':'No accepted P1 certificate exists; independent control checks are not a substitute.'},'source_bindings':['source_manifest.json','additional_source_manifest.json','custody/receipt.json'],'operad_delta':delta,'remaining_obligations':delta['open_obligations'],'next_mathematical_step':'Resume at the frozen P1 contract, first proving rational homogeneity on the effect interval. Do not repeat mining. A complete proof must pass host_type_wrappers.txt before challenge.','provider_usage':{'calls':2,'input_tokens':56166,'output_tokens':120000,'thinking_tokens':88004,'standard_rated_usd':'6.56166','invoice_cost':'UNOBSERVED'},'accepted_general_effect_measure_lemmas':0,'full_Born_uniqueness_proved':False,'proposed_mining_counts':{k:len(v) for k,v in p0['operad_delta'].items()},'host_checked_control_counts':{'generators':4,'relations':3,'compositions':2},'authority_effect':'None','publication':'No commit, push, new PR or merge.'}
save(R/'p5_record/checkpoint.json',p5);save(R/'p5_record/operad_delta.json',delta)
a=load(R/'additional_source_manifest.json')
for name in ['dag/pfp/custody.py','dag/pfp/exact_json.py','dag/pfp/filename_custody.json']:
 p=ROOT/name;t=R/'additional_sources'/name;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(p.read_bytes())
 if not any(v['path']==name for v in a['files']):a['files'].append({'path':name,'snapshot':str(t),'sha256':sha(p)})
save(R/'additional_source_manifest.json',a)
report='''# Born-rule uniqueness: Fable 5.1 review checkpoint

AuthorityEffect: None. **Stopped for review: the 120000-token total generation ceiling was reached. No general Born-rule or effect-valuation uniqueness theorem is accepted.**

The cap was interpreted as a total across this run, including thinking and answer text. Two `claude-fable-5-1` calls used `xhigh`. P0 returned a detailed mining proposal: 78058 output tokens, including46062 thinking tokens. P1 used its remaining41942 output tokens entirely in thinking, ended with `max_tokens`, and returned **zero visible answer bytes**. It supplied no proof certificate or operad delta. No retry was sent. P2 records absence of a candidate; P3/P4 were not entered. P5 records the budget stop.

Total measured API usage:56166 input tokens and120000 output tokens, including88004 thinking tokens. Published standard-rate estimate: **USD6.56166**. Invoice cost is unobserved. The adapter initially classified the non-end-turn response as unknown; the retained terminal `message_delta`/`message_stop` provided authoritative usage for an offline accounting reconciliation. That reconciliation accepts no mathematics.

The original SSE stream and timestamped received-line log are saved for both calls. `response.json` is reconstructed from those events. `response.txt` contains only the visible answer; the P1 file is intentionally empty. The service did not expose the counted private thinking text. The raw response, error, original reservation and accounting reconciliation are preserved separately.

P0 collected12 proposed generators,13 relations,5 composition proposals,5 failed compositions and6 counterexample proposals. These are proposals, not established operads. The host separately checked four control operations, three relations and two typed compositions on the explicit rational symmetric-matrix carrier. Its matrix algebra/readout is supplied, not derived physics. Full refined-carrier operad coherence remains open.

Independent validation: Python Fraction and standalone Rust agree on all four complete numeric records; eight Rust tests and52 field/type mutations pass. The repaired concrete matrix module compiles with eight named axiom reports containing only propext, Classical.choice and Quot.sound. A concrete positive effect valuation witnesses consistency of the admitted hypotheses. The original failed matrix compiler run and its recovery sorryAx reports remain rejected. These checks do not provide any of the eight general Fable target proofs. Twelve stage-protocol tests also passed. Final custody/audit receipts are under `final_checks`.

Review corrected a Fable source-audit mistake: `Enum` in HWKernel.lean has a nodup field, so duplicate entries cannot inflate that enumeration. Label cardinality still does not establish Hilbert dimension. The historical/current paper-hash difference was reconciled by the exact existing filename/line-ending migration, retaining both byte versions. Every P0 claim has an explicit disposition in `p0_mine/claim_review.json`; extension, trace-representation and real-continuum claims are not promoted.

The first missing lemma is rational homogeneity of an effect-additive valuation: prove p(qA)=q p(A) for rational0<=q<=1 without assuming linearity, while proving intermediate arguments remain effects. `contract.lean`, `target_types.txt` and `host_type_wrappers.txt` freeze the larger eight-lemma interface. A future attempt should start directly at P1, not repeat mining. Full projective Gleason uniqueness and operational justification of effect additivity remain separate obligations.

Key files: `p0_mine/response.txt`, `p0_mine/operad_delta.json`, `p0_mine/claim_review.json`, `p1_derive/raw.sse`, `accounting_reconciliation/receipt.json`, `p5_record/checkpoint.json`, `host_control_operad_delta.json`, and `verify_run.py`.

The earlier canonical operad collections and all prior staged evidence remain unchanged. No commit, push, PR or merge was performed.
'''
(R/'README.md').write_bytes(report.encode())
# Adjacent companions for live/rejected development code; frozen input copies are custody assets.
for p in list(R.glob('*.py'))+list(R.glob('*.rs'))+list(R.glob('*.lean'))+[R/'preflight_native/MathlibPreflight.lean']:
 common={'schema_id':'finite-qm.code-companion.v1','subject':p.relative_to(ROOT).as_posix(),'source_sha256':sha(p),'authority_effect':'None'}
 rejected=p.name=='MatrixInstance.lean';gates={g:{'grade':None,'status':'formal_scoring_not_performed'} for g in ['G1','G2','G3','G4','G5']}
 if rejected:gates['G3']={'grade':'E','status':'retained_rejected_compiler_input','evidence':'p2_prepared/matrix_instance_lean_receipt.json','reason':'Actual nonzero compiler result and recovery sorryAx outputs; never accepted.'}
 score=dict(common,rubric='SCORING.md v2.0.0 section1.4',capability_level='L2',engineering_grade=None,composite_score=None,assessment_status='incomplete_no_completed_score_token',gates=gates,refusal_reason='Five-gate assessment incomplete. Recorded receipts and explicit failure dispositions do not award an engineering grade.')
 contract=dict(common,contract_urn='urn:finite-qm:born-fable51:'+p.stem,owned_invariants=['Only literal source/checkpoint scope is claimed.','Provider outputs are proposals; terminal usage is not proof acceptance.'],boundaries=['No general Born/Gleason uniqueness is established.','contract.lean retains its dispatched filename as an immutable custody exception.'],evidence=['p5_record/checkpoint.json','README.md'])
 doc=dict(common,purpose='Run-local streaming/accounting, exact control verification, or a frozen/rejected formal input.',status='rejected_development_asset' if rejected else 'scoped_run_support',boundaries=['The earlier raw streams, failed compiler versions and prior-stage evidence are preserved.','Not a production API or a full formal operad.'])
 for suffix,value in [('score',score),('contract',contract),('doc',doc)]:Path(str(p)+'.'+suffix+'.yaml').write_bytes(yaml.safe_dump(value,sort_keys=False).encode())
print('review checkpoint and companions saved; all general Fable targets remain unaccepted')