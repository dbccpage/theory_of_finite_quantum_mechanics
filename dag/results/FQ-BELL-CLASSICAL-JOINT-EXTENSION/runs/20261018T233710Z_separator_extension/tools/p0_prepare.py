import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import yaml

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
NODE='FQ-BELL-CLASSICAL-JOINT-EXTENSION'
RUN=ROOT/'dag/results'/NODE/'runs/20261018T233710Z_separator_extension'
HERE=Path(__file__).parent
RUN.mkdir(parents=True,exist_ok=True);P0=RUN/'p0';P0.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def dump(p,x):
    with p.open('xb') as f:f.write((json.dumps(x,indent=2)+'\n').encode())
def module(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
prepare=module('prepare',ROOT/'dag/pfp/prepare_stage.py')
prompt=ROOT/'dag/prompts/FINITE_QM_CORE__FQ-BELL-CLASSICAL-JOINT-EXTENSION__PROVED_LEAN.yaml'
packet=prepare.build_packet(prompt,attempt_id='p0');dump(P0/'request.json',packet)
inputs=RUN/'inputs';inputs.mkdir(exist_ok=True)
pins=[]
for source in ['lean4/BellOperad.lean','lean4/BellClassicalJointExtension.lean','lean4/DerivationDagQMClosure.lean',
 'dag/pfp/stage_contracts.yaml','dag/pfp/workflow.yaml','dag/pfp/mode.yaml','dag/pfp/prepare_stage.py',
 'dag/operads/'+NODE+'.yaml','dag/results/'+NODE+'/reviews/20261018_claim_audit/check_certificate.py']:
    dest=inputs/source;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/source,dest)
    pins.append({'path':rel(dest),'sha256':sha(dest),'source_path':source})
shutil.copyfile(prompt,inputs/'prompt.yaml')
for file in ['check_candidate.py','cases.py','max_probe.lean']:
    shutil.copyfile(HERE/file,RUN/file)
note='''# Selected next Bell work unit: separator reduction

Pair order 00,01,10,11 and cells --,-+,+-,++. Admit exact Q-valued
nonnegative normalized pairs with matching one-party marginals. No supplied
four-variable law is assumed. For B_y=b let u=P(A0+,b), v=P(A1+,b),
w=P(b). The free ++b mass t_b obeys max(0,u+v-w)<=t_b<=min(u,v).
Thus the free separator r=P(A0+,A1+) lies in [sum lower_b,sum upper_b].
Choose r in both setting intervals. Split each triple using
t_-=max(lower_-,r-upper_+), t_+=r-t_-. Fill the other cells by
u-t_b, v-t_b, w-u-v+t_b. Glue the two triples by
p(s,b0,b1)=T0(s,b0)*T1(s,b1)/q(s) for q(s)>0; use zero for q(s)=0.
This zero branch is licensed by nonnegativity and equal separator marginals.

Prove at common integer scale D: the separator intervals overlap iff all
eight CHSH facets hold, assuming all 16 observed cells are nonnegative.
Prove existence of the two nonnegative triple cell systems with common r.
Retain the all-facet common-law necessity theorem. The general Q-valued
conditional-gluing and input-transport proofs remain explicit obligations;
native extension certificates are accepted only by actual projection checks.

Fine 1982 is source orientation, not an imported proof or accepted result:
https://doi.org/10.1103/PhysRevLett.48.291
Primary author-hosted paper: https://faculty.washington.edu/afine/PRL1982.pdf
The construction and forthcoming Lean proof in this run are new local work.
'''
(P0/'separator_construction.md').write_bytes(note.encode())
pins.append({'path':rel(P0/'separator_construction.md'),'sha256':sha(P0/'separator_construction.md')})
scope='Exact separator interval/CHSH-family reduction at integer scale, compatible triple existence, and independently checked rational extension or facet-obstruction certificates on explicit inputs. General rational gluing and input-transport formalization remain open; no full formal Fine converse or physical claim.'
cases=module('public_cases',RUN/'cases.py').public_cases()
dump(RUN/'public_cases.json',cases)
(RUN/'public_cases.tsv').write_bytes(('\n'.join(c['id']+'\t'+'\t'.join(v for row in c['pairs'] for v in row) for c in cases)+'\n').encode())
gen_specs=[
 ('pair_marginalize',['JointLaw'],'CompatiblePairData','Project one 16-state law to the four observed pair tables.'),
 ('separator_intervals',['FeasiblePairData'],'FeasibleSeparatorProblem','Retain input pairs and both setting Frechet intervals, with a nonempty intersection.'),
 ('select_separator',['FeasibleSeparatorProblem'],'SeparatorChoice','Retain input pairs and any r in the common interval; native constructor selects the lower endpoint.'),
 ('split_triples',['SeparatorChoice'],'CompatibleTriplePair','Construct both triple laws from the same r with observed pair marginals and equal separator law.'),
 ('conditional_glue',['CompatibleTriplePair'],'JointLaw','Zero-safe conditional product of two compatible triples; unary on the compatible-pair wrapper, despite two native arguments.'),
 ('chsh_family',['CompatiblePairData'],'FacetValues8','All odd-negative-sign CHSH sums in masks 1,2,4,7,8,11,13,14.')]
generators=[{'id':i,'ordered_inputs':ins,'output':out,'arity':len(ins),'carrier':'binary 2x2 pair scenario on A0,A1,B0,B1',
 'coefficient_ring':'Q natively; common-scale Int numerator model in Lean',
 'hypotheses':['nonnegative normalized observed pairs','matching one-party marginals','all chosen refinements retained with their input data'],
 'source_pins':pins,'semantic_predicate':sem,'evidence_status':'P0 source-scoped construction target; new implementation/proof requires P2'} for i,ins,out,sem in gen_specs]
relation_specs=[('interval_chsh_equivalence','At common positive integer scale, interval overlap iff the complete eight-facet CHSH family holds.','CompatiblePositive PairCounts','selected next theorem, not P0 accepted evidence'),
 ('triple_slice_feasibility','Separator interval membership yields nonnegative triple cells with prescribed two-pair marginals.','same source PairCounts and shared r','selected next theorem, not P0 accepted evidence'),
 ('conditional_glue_projection','Project(glue(split(select(intervals(p)))))=p.','compatible triple laws with exactly equal separator, nonnegative weights; zero slices handled without division','native certificate predicate; general Lean rational gluing proof remains open'),
 ('full_facet_necessity','Every common positive joint law satisfies all eight CHSH facets.','binary response products and common positive law','selected reuse/generalization theorem; must compile')]
relations=[{'id':i,'equation_or_predicate':eq,'typing_conditions':typ,'source_pins':pins,'evidence_status':status,
 'scope':'This work unit only; no symmetric action or complete syntactic operad presentation.'} for i,eq,typ,status in relation_specs]
compositions=[]
for outer,inner,colour,license in [('select_separator','separator_intervals','FeasibleSeparatorProblem','interval_chsh_equivalence'),
 ('split_triples','select_separator','SeparatorChoice','triple_slice_feasibility'),('conditional_glue','split_triples','CompatibleTriplePair','conditional_glue_projection'),
 ('pair_marginalize','conditional_glue','JointLaw','conditional_glue_projection')]:
    compositions.append({'outer_operation':outer,'input_slot':0,'inner_operation':inner,'colour_match':colour+' -> '+colour,
     'hypothesis_match':'Same retained pair data and shared separator; input refinements must be discharged.',
     'licensing_relations':[license],'evidence_status':'well-typed plan only; semantic acceptance awaits P2'})
obligations=['P1 implementation and native/kernel checks','P4 zero-slice, mismatch and full-facet challenges',
 'General Q conditional-gluing theorem in Lean','Formal transport from arbitrary rational observed tables to integer PairCounts',
 'Probability-subtype and complete operad presentation remain open; no physical inference']
delta={'add_or_refine_generators':generators,'add_or_refine_relations':relations,'checked_compositions':[],
 'failed_compositions':[],'counterexamples':[],'open_obligations':obligations}
(P0/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta,sort_keys=False,width=100).encode())
anchors=['lean4/BellSeparatorExtension.lean::separator_iff_chsh','lean4/BellSeparatorExtension.lean::chsh_has_two_triples',
 'lean4/BellSeparatorExtension.lean::full_family_joint_necessity','code/python/src/qm/bell_separator_extension.py::construct_extension',
 'code/rust/src/finite_probability/bell_separator_extension.rs::construct_extension']
slots={prepare.SLOTS[0]:{'mining_status':'FILLED','carrier':'Four binary pair tables with common one-party marginals; no supplied joint law',
 'coefficient_ring':'Q; positive common integer scaling for Lean','assumptions':['four nonnegative unit-mass pair tables','consistent A and B one-party marginals'],
 'source_pins':pins,'public_input':{'scope':scope,'cases':cases,'grid_denominators':[1,2,3,4],'required_anchors':anchors}},
 prepare.SLOTS[1]:{'mining_status':'FILLED','operations':[{'catalog_id':g['id'],'inputs':g['ordered_inputs'],'output':g['output'],'semantic_predicate':g['semantic_predicate']} for g in generators],
 'composition_plan':compositions},
 prepare.SLOTS[2]:{'mining_status':'FILLED','algebraic_relations':relations,'rejection_predicates':['independent actual pair and triple projection','nonnegative unit mass','all eight sign facets','equal separator before division'],
 'negative_control_plan':['all PR-box relabelings','one facet passes while another violates','incompatible pairs','mismatched triple separator','zero separator slices','false candidate fields and duplicate keys']},
 prepare.SLOTS[3]:{'mining_status':'FILLED','certificate_predicates':['G1 original exact shape, duplicate rejection, all context bindings',
 'G3 actual joint/triple projection and zero-safe cross-product identities','G4 obstruction must be an actual >2 odd-sign CHSH facet of compatible pair data',
 'G5 scope labels alone never accept a theorem; native source pins and kernel compilation separately required'],
 'anchors':anchors,'unpaid_imports':obligations[2:]}}
reviewed={'original_target':packet['public_context']['original_target']['source_statement'],'work_unit':{
 'schema_id':'omega.pfp.finite-qm-work-unit.v1','task_id':NODE,'objective':scope,
 'selected_catalog_ids':[g['id'] for g in generators],'operad_slots':slots,
 'answer_schema':{'type':'object','required':['schema_id','task_id','stage_id','attempt_id','input_sha256','scope','cases'],
 'properties':{'cases':{'type':'array','items':{'type':'object','description':'Exact rational extension witness with triple projections, or a violated CHSH facet. No expected numerical answers supplied.'}}}},
 'checker_id':rel(RUN/'check_candidate.py')},'catalog':{'entries':[{'id':g['id'],'inputs':g['ordered_inputs'],'output':g['output']} for g in generators]}}
dump(P0/'reviewed_missions.json',reviewed)
review={'task_id':NODE,'review_status':'accepted_for_next_step','reviewed_sha256':sha(P0/'reviewed_missions.json'),
 'checker_pin':{'path':rel(RUN/'check_candidate.py'),'sha256':sha(RUN/'check_candidate.py')},
 'reviewer':'local Codex source/contract review, not an independent human or model',
 'boundary':'FILLED means next-step prerequisites and checking contract, not acceptance of unbuilt Lean/native anchors.'}
dump(P0/'host_review.json',review)
response={**{k:packet[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},'status':'ready_for_host_review',
 'mission_patch':slots,'source_checks':pins,'next_missing_dependency':'P1 proof and executable witness construction followed by P2 independent gates',
 'operad_delta':delta,'claim_boundary':{'supports':'scoped problem and exact checker contract','does_not_support':'new theorem acceptance at P0',
 'narrowest_claim':scope,'next_test':'derive and compile the stated separator lemmas'}}
dump(P0/'candidate.json',response);shutil.copyfile(P0/'candidate.json',P0/'raw_response.txt')
dump(P0/'host_check.json',{**{k:packet[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},'status':'reviewed_for_next_step','review':review})
p1=RUN/'p1';p1.mkdir(exist_ok=True)
dump(p1/'request.json',prepare.build_packet(prompt,'P1_DERIVE',attempt_id='p1',reviewed_path=P0/'reviewed_missions.json',review_path=P0/'host_review.json'))
dump(RUN/'execution.json',{'task_id':NODE,'baseline_commit':'9eac15cab2b3b05cf98fded51d28ca741c7c50f1',
 'mode':'local Codex/exact-solver file-based PFP stages with native checkers; no external provider dispatched',
 'external_provider_calls':0,'external_provider_cost':'not incurred; active chat cost unmeasured','repair_budget':'one mathematical work unit; preserve any genuine P3 repair and stop after P5 for review',
 'source_orientation':{'title':'Arthur Fine, Hidden Variables, Joint Probability, and the Bell Inequalities (1982)',
 'doi':'https://doi.org/10.1103/PhysRevLett.48.291','primary_pdf':'https://faculty.washington.edu/afine/PRL1982.pdf','role':'target orientation, not an imported proof'},
 'raw_response_semantics':'serialized local artifacts, not provider transcripts','stages_completed':['P0_MINE_OPERAD'],'authority_effect':'None'})
dump(RUN/'presentation_plan.json',{'generators':generators,'relations':relations,'compositions':compositions})
print('P0 recorded; public inputs:',len(cases),'cases. No numerical witness or expected classification was public-prefilled.')
