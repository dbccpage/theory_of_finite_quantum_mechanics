import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
from fractions import Fraction as Q
import yaml

ROOT = Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
NODE = 'FQ-BELL-CLASSICAL-JOINT-EXTENSION'
RUN = ROOT / 'dag/results' / NODE / 'runs/20261018T225117Z_operad_expectation'
RUN.mkdir(parents=True, exist_ok=True)
P0 = RUN / 'p0'
P0.mkdir(exist_ok=True)
def dump(path, obj):
    path.write_bytes((json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def rel(path): return path.relative_to(ROOT).as_posix()
spec = importlib.util.spec_from_file_location('prepare', ROOT/'dag/pfp/prepare_stage.py')
prepare = importlib.util.module_from_spec(spec); spec.loader.exec_module(prepare)
prompt = ROOT/'dag/prompts/FINITE_QM_CORE__FQ-BELL-CLASSICAL-JOINT-EXTENSION__PROVED_LEAN.yaml'
packet = prepare.build_packet(prompt, attempt_id='p0')
dump(P0/'request.json', packet)
inputs = RUN/'inputs'; inputs.mkdir(exist_ok=True)
sources = ['lean4/BellClassicalJointExtension.lean', 'lean4/DerivationDagQMClosure.lean',
           'code/python/src/qm/bell_joint_extension.py', 'code/rust/src/finite_probability/bell_joint_extension.rs',
           'dag/pfp/workflow.yaml', 'dag/pfp/stage_contracts.yaml', 'dag/pfp/mode.yaml',
           'dag/pfp/prepare_stage.py', 'dag/operads/'+NODE+'.yaml']
pins = []
for source in sources:
    destination = inputs/source
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT/source, destination)
    pins.append({'path':rel(destination), 'sha256':sha(destination), 'original_path':source})
shutil.copyfile(prompt, inputs/'prompt.yaml')
shutil.copyfile(Path(__file__).with_name('check_certificate.py'), RUN/'check_certificate.py')
scope = 'Common nonnegative normalized rational joint law implies the standard CHSH bound; reusable exact expectation and substitution laws. No Fine converse or physical inference.'
cases = []
def case(name, w): cases.append({'id':name, 'weights':[str(Q(x)) for x in w]})
for i in range(16): case('vertex_'+str(i), [int(j==i) for j in range(16)])
case('uniform', [Q(1,16)]*16)
case('asymmetric', [Q(i,136) for i in range(1,17)])
for i,j,p in [(0,1,Q(1,7)), (3,10,Q(2,5)), (5,14,Q(11,13))]:
    w=[Q(0)]*16;w[i]+=p;w[j]+=1-p;case('mixture_'+str(i)+'_'+str(j),w)
w=[Q(0)]*16;w[0]=1-Q(1,10**100+3);w[1]=1-w[0];case('large_denominator',w)
anchors = ['lean4/BellOperad.lean::substitute_assoc', 'lean4/BellOperad.lean::substitute_left_unit',
           'lean4/BellOperad.lean::substitute_right_unit', 'lean4/BellOperad.lean::substitute_congr',
           'lean4/BellOperad.lean::expect_chsh', 'lean4/BellOperad.lean::bell_evaluation',
           'lean4/BellOperad.lean::bell_bound',
           'code/python/src/qm/bell_joint_extension.py::verify_joint_certificate',
           'code/rust/src/finite_probability/bell_joint_extension.rs::verify_joint_certificate']
operations = [
    {'catalog_id':'response_products','inputs':[],'output':'ResponseMap4','semantic_predicate':'omega maps to (a0*b0,a0*b1,a1*b0,a1*b1)'},
    {'catalog_id':'joint_expectation','inputs':['JointLaw','ResponseMap4'],'output':'CorrelatorTuple','semantic_predicate':'coordinatewise exact finite weighted sum on the same 16-point carrier'},
    {'catalog_id':'chsh_linear','inputs':['CorrelatorTuple'],'output':'Scalar','semantic_predicate':'e00+e01+e10-e11'},
]
slots = {
 prepare.SLOTS[0]: {'mining_status':'FILLED','carrier':'Omega={-1,+1}^4; JointLaw=nonnegative rational weights on Omega summing to one; ResponseMap4=Omega->Q^4',
 'coefficient_ring':'Q, represented by arbitrary precision rationals n/d with d>0; Lean common-denominator Nat rows, no floating point',
 'assumptions':['common law','nonnegative weights','normalization','fixed 00,01,10,11 order'], 'source_pins':pins,
 'public_input':{'cases':cases,'scope':scope,'required_anchors':anchors}},
 prepare.SLOTS[1]: {'mining_status':'FILLED','operations':operations,
 'composition_plan':['chsh_linear(joint_expectation(p,response_products()))', 'simultaneous typed substitution of finite function families; units and associativity under explicit Sigma reindexing']},
 prepare.SLOTS[2]: {'mining_status':'FILLED','algebraic_relations':['CHSH(E_p(f))=E_p(CHSH o f)', 'score(omega) in {-2,2}',
 'Pplus+Pminus=1; S=2*(Pplus-Pminus); 2+S=4*Pplus; 2-S=4*Pminus', 'function substitution is associative and unital; semantic equality is a congruence'],
 'rejection_predicates':['original public law unchanged','all certificate fields equal independent exact recomputation','native Lean anchors compile without sorry or added axioms'],
 'negative_control_plan':['wrong last sign with valid law','false slack or correlator','negative normalized law','four separate pair laws without one common law','wrong-colour insertion']},
 prepare.SLOTS[3]: {'mining_status':'FILLED','certificate_predicates':['G1 exact shape and all bindings','G3 independent exact certificate recomputation',
 'G5 scoped Lean kernel and Rust/Python native checks; no Fine claim','G2 not applicable: no chain complex','G4 applicable only to a claimed countermodel, none in P1'],
 'anchors':anchors,'unpaid_imports':['Fine converse and precise compatible pair-marginal hypotheses remain open','arbitrary presented syntactic quotients and symmetric actions not claimed','physical locality and setting independence not derived']}
}
reviewed = {'original_target':packet['public_context']['original_target']['source_statement'], 'work_unit':{
 'schema_id':'omega.pfp.finite-qm-work-unit.v1','task_id':NODE,
 'objective':'Extend the checked common-joint-law implication by extracting generic exact expectation and kernel-checked typed substitution coherence, with independently checked certificate consumers.',
 'selected_catalog_ids':[x['catalog_id'] for x in operations], 'operad_slots':slots,
 'answer_schema':{'type':'object','required':['schema_id','task_id','stage_id','attempt_id','input_sha256','samples','anchors','scope'],
 'properties':{'samples':{'type':'array','items':{'type':'object','description':'Exact rational strings for public law and all certificate components; independently checked.'}}}},
 'checker_id':rel(RUN/'check_certificate.py')}, 'catalog':{'entries':[{'id':x['catalog_id'],'inputs':x['inputs'],'output':x['output']} for x in operations]}}
dump(P0/'reviewed_missions.json', reviewed)
dump(P0/'host_review.json', {'task_id':NODE, 'review_status':'accepted_for_next_step', 'reviewed_sha256':sha(P0/'reviewed_missions.json'),
 'reviewer':'Codex local source/contract review; no separate human or provider review', 'checker_pin':{'path':rel(RUN/'check_certificate.py'),'sha256':sha(RUN/'check_certificate.py')},
 'finding':'All four slots cover this narrower next step only; they do not close the full historical target.'})
delta={'add_or_refine_generators':operations,'add_or_refine_relations':slots[prepare.SLOTS[2]]['algebraic_relations'],
 'checked_compositions':[],'failed_compositions':[], 'counterexamples':[],
 'open_obligations':['Implement generic expectation and certificate verification in both native languages','Prove finite typed function substitution laws and Bell specialization in Lean','Execute independent P2 and P4 checks','Fine converse remains open']}
response={'task_id':NODE,'stage_id':'P0_MINE_OPERAD','attempt_id':'p0','input_sha256':packet['input_sha256'],
 'status':'ready_for_host_review','mission_patch':slots,'source_checks':pins,'next_missing_dependency':'P1 constructions and their P2 native checks',
 'operad_delta':delta,'claim_boundary':{'supports':'source-scoped work unit and independent checker contract', 'does_not_support':'new theorem acceptance or Fine equivalence',
 'narrowest_claim':'ready for the explicit next derivation step', 'next_test':'P1 construction followed by native P2 gates'}}
dump(P0/'candidate.json',response)
shutil.copyfile(P0/'candidate.json', P0/'raw_response.txt')
(P0/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta,sort_keys=False).encode())
shutil.copyfile(P0/'host_review.json',P0/'host_check.json')
p1=RUN/'p1';p1.mkdir(exist_ok=True)
dump(p1/'request.json',prepare.build_packet(prompt,'P1_DERIVE',attempt_id='p1',reviewed_path=P0/'reviewed_missions.json',review_path=P0/'host_review.json'))
dump(RUN/'execution.json',{'task_id':NODE,'run_id':RUN.name,'baseline_commit':'90e4f2cb9a1abaee99ca46263c49c8654dead79b',
 'execution_mode':'local Codex researcher/exact solver with separate native checker executions; file-based PFP stage protocol',
 'external_provider_calls':0,'external_provider_cost':'not incurred; this does not measure the active Codex chat cost',
 'budget':'one selected work unit; P3 only for a real failed candidate; stop after P5 for user review', 'stages_completed':['P0_MINE_OPERAD'],
 'raw_response_semantics':'Serialized locally constructed stage artifact bytes, not a fabricated remote provider transcript.', 'authority_effect':'None'})
print(str(RUN))
