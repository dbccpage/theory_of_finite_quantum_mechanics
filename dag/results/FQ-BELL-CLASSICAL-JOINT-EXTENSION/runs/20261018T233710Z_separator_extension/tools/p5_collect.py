import copy
import hashlib
import json
from pathlib import Path
import shutil
import yaml

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
NODE='FQ-BELL-CLASSICAL-JOINT-EXTENSION'
RUN=ROOT/'dag/results'/NODE/'runs/20261018T233710Z_separator_extension'
HERE=Path(__file__).parent
P5=RUN/'p5';P5.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def dump(p,x):
    with p.open('xb') as f:f.write((json.dumps(x,separators=(',',':'))+'\n').encode())
def yd(p,x):
    with p.open('xb') as f:f.write(yaml.safe_dump(x,sort_keys=False,width=100).encode())
host=json.loads((RUN/'p2_after_repair/host_check.json').read_bytes())
if host['status']!='accepted_candidate_for_challenge':raise ValueError('no accepted scoped result')
delta=yaml.safe_load((RUN/'p4/operad_delta.yaml').read_bytes())
control=json.loads((RUN/'p4/two_sided_chsh_control.json').read_bytes())
delta['counterexamples'].append({'id':control['id'],'scope':control['scope'],'source':rel(RUN/'p4/two_sided_chsh_control.json'),
 'standard_CHSH_value':control['standard_CHSH_value'],'violated_facet_value':control['violated_facet_value'],
 'evidence_status':'checked against actual compatible positive pair data; standard two-sided CHSH passes while another signed facet exceeds two'})
native_sources=['code/python/src/qm/bell_separator_extension.py','code/python/tests/test_bell_separator_extension.py',
 'code/rust/src/finite_probability/bell_separator_extension.rs','code/rust/src/finite_probability/examples/bell_separator_replay.rs',
 'code/rust/src/finite_probability/lib.rs','code/rust/src/finite_probability/Cargo.toml','code/rust/Cargo.lock',
 'lean4/BellSeparatorExtension.lean','lean4/BellOperad.lean','lean4/BellClassicalJointExtension.lean',
 'lean4/DerivationDagQMClosure.lean','lean4/lakefile.lean','lean4/lean-toolchain']
pins=[{'path':p,'sha256':sha(ROOT/p)} for p in native_sources]
proof_pins=[p for p in pins if p['path'] in ['lean4/BellSeparatorExtension.lean','code/python/src/qm/bell_separator_extension.py','code/rust/src/finite_probability/bell_separator_extension.rs']]
for g in delta['add_or_refine_generators']:
    g['source_pins']=copy.deepcopy(proof_pins)
    if g['id']=='pair_marginalize':g['hypotheses']=['one nonnegative normalized 16-state joint law','fixed bit and pair-cell order']
    elif g['id']=='chsh_family':g['hypotheses']=['four nonnegative normalized pair tables','matching one-party marginals','ordered odd-negative sign masks']
    elif g['id']=='conditional_glue':g['hypotheses']=['two nonnegative normalized triple laws','exactly equal separator marginals','zero separator slices forced to zero by nonnegativity']
    elif g['id']=='split_triples':g['hypotheses']=['same retained compatible pair data','one r in both setting intervals']
    else:g['hypotheses']=['same retained compatible pair data','nonempty common separator interval']
for r in delta['add_or_refine_relations']:r['source_pins']=copy.deepcopy(proof_pins)
for r in delta['add_or_refine_relations']:
    if r['id']=='conditional_glue_projection':r['relation_kind']='exact checked predicate on retained certificates; general Lean rational operator identity remains an obligation'
obligations=[
 'Full formal rational Fine converse remains open: prove zero-safe rational conditional-gluing marginal preservation and unit mass for arbitrary compatible triples.',
 'Formalize transport from arbitrary rational observed pair arrays to positive common-integer-scale PairCounts and back.',
 'Connect the Lean TripleCellsPositive parameter systems to normalized table arrays and their explicit projection identities.',
 'Instantiate the context-retaining probability-subtype operations as a formal operad if that stronger claim is desired; current generators are scoped semantic wrappers around native primitives.',
 'General Q response-table transport, score-partition/slack formalization, symmetric actions and syntactic quotient completeness from prior work remain open.',
 'Physical locality and setting independence remain additional assumptions, not consequences of this finite algebra.']
delta['open_obligations']=obligations
record_path=ROOT/'dag/operads'/(NODE+'.yaml');record=yaml.safe_load(record_path.read_bytes())
presentation=record['presentation']
new_colours=[('CompatiblePairData','Four exact rational binary pair tables with nonnegative unit mass and consistent one-party marginals.'),
 ('FeasiblePairData','CompatiblePairData whose computed common separator interval is nonempty; this is a refined input domain.'),
 ('FeasibleSeparatorProblem','Semantic wrapper retaining the same pair data and the nonempty setting intervals.'),
 ('SeparatorChoice','Semantic wrapper retaining pair data and a separator ++ mass r in both intervals.'),
 ('CompatibleTriplePair','Two nonnegative normalized triple laws with matching A0,A1 separator, retaining their observed pair-data provenance.'),
 ('FacetValues8','Eight rational signed CHSH values in mask order 1,2,4,7,8,11,13,14.')]
existing={c['id'] for c in presentation['colours']}
for name,meaning in new_colours:
    if name not in existing:presentation['colours'].append({'id':name,'meaning':meaning})
presentation['generators'].extend(delta['add_or_refine_generators']);presentation['relations'].extend(delta['add_or_refine_relations'])
presentation['compositions'].extend(delta['checked_compositions'])
presentation['composition_plans'].append({'id':'feasible_pair_data_to_extension_projection',
 'tree':{'outer':'pair_marginalize','slot':0,'inner':{'outer':'conditional_glue','slot':0,'inner':{
 'outer':'split_triples','slot':0,'inner':{'outer':'select_separator','slot':0,'inner':'separator_intervals'}}}},
 'ordered_inputs':['FeasiblePairData'],'output':'CompatiblePairData',
 'scope':'Typed context-retaining semantic plan; exact saved certificates satisfy its projection predicate. No general Lean Q-subtype operad equation is claimed.'})
presentation['status']='scoped_integer_separator_reduction_and_exact_native_extension_certificates_checked_full_formal_converse_open'
presentation['scope']='Previous Bell function-substitution semantics plus new separator-refined generator interpretations. Integer interval/CHSH equivalence and positive cell systems are kernel checked; rational extensions and projections are independently checked on retained inputs.'
presentation['coherence_obligations'].extend(obligations[:4])
record['open_obligations']=obligations
record['operad_slots']=copy.deepcopy(json.loads((RUN/'p0/reviewed_missions.json').read_bytes())['work_unit']['operad_slots'])
# The cumulative record links the public cases rather than duplicating thousands
# of mathematical inputs; the reviewed stage packet retains all original bytes.
record['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']={
 'scope':json.loads((RUN/'p3/candidate.json').read_bytes())['scope'],
 'cases_ref':{'path':rel(RUN/'public_cases.json'),'sha256':sha(RUN/'public_cases.json')},
 'recipe_ref':{'path':rel(RUN/'cases.py'),'sha256':sha(RUN/'cases.py')},'scope_rule':'The entrypoint is P0; this record does not auto-admit a later step or close Fine converse.'}
record['operad_slots_scope']={'work_unit':rel(RUN/'p0/reviewed_missions.json'),
 'scope':'This selected separator work unit only; FILLED means reviewed prerequisites, not completed full source target.',
 'checker':{'path':rel(RUN/'check_candidate.py'),'sha256':sha(RUN/'check_candidate.py')},
 'M4_note':'Scope-label matching is not theorem acceptance. The failed P2 and accepted repaired kernel gates are retained separately.'}
record['latest_run']={'path':rel(RUN),'stage':'P5_RECORD','status':'separator_reduction_and_finite_certificates_checked_full_formal_converse_open','stop':'user_review_requested'}
record['stage_history'].extend([{'stage':s,'attempt':a,'run':rel(RUN),'operad_delta':rel(RUN/a/'operad_delta.yaml'),'host_check':rel(RUN/a/'host_check.json')}
 for s,a in [('P0_MINE_OPERAD','p0'),('P1_DERIVE','p1'),('P2_VERIFY','p2'),('P3_REPAIR','p3'),('P2_VERIFY','p2_after_repair'),('P4_CHALLENGE','p4'),('P5_RECORD','p5')]])
for path,symbol in [('lean4/BellSeparatorExtension.lean','QuantumMechanics.BellSeparatorExtension.separator_iff_chsh'),
 ('code/python/src/qm/bell_separator_extension.py','construct_extension'),('code/rust/src/finite_probability/bell_separator_extension.rs','construct_extension')]:
    record['source_bindings'].append({'original_ref':path+'::'+symbol,'availability':'local','path':path,'repository':'this_repository',
     'symbol':symbol,'sha256':sha(ROOT/path),'role':'checked_separator_work_unit','declaration_status':'scope_checked_in_repaired_P2; general rational gluing and transport remain open',
     'receipt':rel(RUN/'p2_after_repair/host_check.json')})
record['scope_notes'].append('Separator stage retains a genuine P2 kernel rejection and P3 repair. The general integer reduction is distinct from the 4010 finite native inputs; neither alone is promoted to the full formal rational Fine converse.')
record_path.write_bytes(yaml.safe_dump(record,sort_keys=False,width=100).encode())
index_path=ROOT/'dag/operads/index.json';index=json.loads(index_path.read_bytes());row=next(x for x in index['nodes'] if x['node_id']==NODE)
row.update({'current_stage':'P5_RECORD','latest_run':rel(RUN),'ready_for_derivation':False,
 'status':'separator_work_unit_checked_full_formal_converse_open','stop_reason':'user_review_requested'})
index_path.write_bytes((json.dumps(index,indent=2)+'\n').encode())
yd(P5/'operad_delta.yaml',delta)
yd(P5/'collection_after.yaml',record)
request={'task_id':NODE,'stage_id':'P5_RECORD','attempt_id':'p5','input_sha256':sha(RUN/'p4/host_check.json'),
 'checked_result':'../p2_after_repair/host_check.json','challenge':'../p4/host_check.json','supplemental_control':'../p4/two_sided_chsh_control.json'}
dump(P5/'request.json',request)
counts=host['predicate_results']['G3_WITNESS']['counts']
attempts=[{'stage':s,'attempt':a,'request':rel(RUN/a/'request.json'),'candidate':rel(RUN/a/'candidate.json'),
 'operad_delta':rel(RUN/a/'operad_delta.yaml')} for s,a in [('P0_MINE_OPERAD','p0'),('P1_DERIVE','p1'),('P2_VERIFY','p2'),
 ('P3_REPAIR','p3'),('P2_VERIFY','p2_after_repair'),('P4_CHALLENGE','p4'),('P5_RECORD','p5')]]
candidate={**{k:request[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},
 'result_or_obstruction':{'formal_result':'CompatiblePositive PairCounts admit an integer separator iff all eight CHSH facets hold; positive triple-cell parameter systems exist; every common law satisfies the full facet family.',
 'native_result':counts,'cross_language_cases':sum(counts.values()),'full_formal_converse':'OPEN: rational gluing, table projection/subtype and input-scaling transport remain'},
 'attempt_refs':attempts,'source_bindings':pins,'remaining_obligations':obligations,'operad_delta':delta,
 'next_mathematical_step':'After review: prove the zero-safe rational conditional-gluing marginal theorem and normalized table identity, then connect the integer separator theorem through common-denominator transport.',
 'claim_boundary':{'supports':'general integer separator/CHSH reduction plus exact finite rational extension or facet-obstruction certificates',
 'does_not_support':'a fully formal rational Fine converse, generic Q probability-subtype operad instantiation, complete symmetric/quotient operad, or physical inference',
 'narrowest_claim':record['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']['scope'],
 'next_test':'user review before any further mathematical step'},
 'execution_accounting':{'external_provider_calls':0,'external_provider_cost':'not incurred; active chat cost unmeasured',
 'independence':'one local Codex researcher; separate native processes and independent certificate predicates; no independent human/model review'},
 'stop':'user_review_requested'}
dump(P5/'candidate.json',candidate);shutil.copyfile(P5/'candidate.json',P5/'raw_response.txt')
# Link submissions to the actual host checkpoints without changing their bytes.
for stage,hoststage in [('p1','p2'),('p3','p2_after_repair')]:
    packet=json.loads((RUN/stage/'request.json').read_bytes())
    dump(RUN/stage/'host_check.json',{'task_id':NODE,'stage_id':packet['stage_id'],'attempt_id':stage,'input_sha256':packet['input_sha256'],
     'candidate_sha256':sha(RUN/stage/'candidate.json'),'status':'see_host_checkpoint','host_check':'../'+hoststage+'/host_check.json'})
for name in native_sources:
    dest=RUN/'sources'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
for name in ['replay.py','native_checks.py']:
    shutil.copyfile(HERE/name,RUN/name)
tools=RUN/'tools';tools.mkdir(exist_ok=True)
for p in HERE.iterdir():
    if p.is_file():shutil.copyfile(p,tools/p.name)
execution=json.loads((RUN/'execution.json').read_bytes())
execution.update({'stages_completed':['P0_MINE_OPERAD','P1_DERIVE','P2_VERIFY:rejected','P3_REPAIR','P2_VERIFY:accepted','P4_CHALLENGE','P5_RECORD'],
 'status':'stopped_for_user_review_full_formal_converse_open','actual_counts':counts,
 'repair_history':'original kernel timeout/dependency errors retained; simplified proof accepted after P3',
 'finite_scope':'complete compatible numerator grids for denominators 1..4 and one additional arbitrary-precision input; finite validation is not the general proof',
 'claim_boundary':candidate['claim_boundary']})
(RUN/'execution.json').write_bytes((json.dumps(execution,indent=2)+'\n').encode())
(RUN/'.gitattributes').write_bytes(b'*.json -text whitespace=cr-at-eol\n*.yaml -text whitespace=cr-at-eol\n*.txt -text whitespace=cr-at-eol\n*.log -text whitespace=cr-at-eol,-blank-at-eof\ninputs/** -text whitespace=-trailing-space,-blank-at-eof\np1/construction/** -text whitespace=-trailing-space,-blank-at-eof\np3/construction/** -text whitespace=-trailing-space,-blank-at-eof\nsources/** -text whitespace=-trailing-space,-blank-at-eof\ntools/*.txt -text whitespace=-blank-at-eof\n')
print('P5 result and cumulative typed operad collection saved. Final protocol and custody checks pending.')
