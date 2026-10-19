import copy
import hashlib
import importlib.util
import json
from fractions import Fraction as Q
from pathlib import Path
import shutil
import subprocess
import os
import yaml

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T225117Z_operad_expectation'
NODE='FQ-BELL-CLASSICAL-JOINT-EXTENSION'
P2=RUN/'p2';P4=RUN/'p4';P4.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_bytes((json.dumps(v,indent=2)+'\n').encode())
def loadmod(name,p):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
prepare=loadmod('prepare',ROOT/'dag/pfp/prepare_stage.py')
checker=loadmod('checker',RUN/'check_certificate.py')
candidate=json.loads((RUN/'p1/candidate.json').read_bytes())
required=['python','rust_retry','rust_replay','lean','certificate']
receipts={kind:json.loads((P2/(kind+'_receipt.json')).read_bytes()) for kind in required}
if any(x['exit_code'] for receipt in receipts.values() for x in receipt):raise ValueError('required_native_gate_failed')
# Independent comparison of native Rust output, with exact rational parsing.
rust=(P2/'logs/rust_replay_0.stdout.log').read_text().splitlines()
samples=candidate['samples']
assert len(rust)==len(samples)
for line,sample in zip(rust,samples):
    parts=line.split('\t');assert parts[0]==sample['id']
    flat=sample['correlators']+[sample[k] for k in ['chsh','positive_score_mass','negative_score_mass','lower_slack','upper_slack']]
    assert list(map(Q,parts[1:]))==list(map(Q,flat))
domain=checker.check(RUN/'p1/request.json',RUN/'p1/candidate.json')
hostpins=[]
for source in ['check_certificate.py','p0/reviewed_missions.json','p1/construction/lean4/BellOperad.lean']:
    p=RUN/source;hostpins.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
delta={'add_or_refine_generators':[], 'add_or_refine_relations':[
 {'id':'endomorphism_coherence','evidence_status':'Lean kernel checked units and associativity (no axioms); congruence uses Quot.sound'},
 {'id':'expectation_linearity','evidence_status':'Lean kernel checked generic integral table theorem; exact Q Rust/Python tests'},
 {'id':'certificate_component_binding','evidence_status':'all 22 public law certificates independently recomputed and exactly matched by Rust'}],
 'checked_compositions':[{'outer_operation':'chsh_linear','input_slot':0,'inner_operation':'joint_expectation',
 'colour_match':'Q^4 -> Q^4; Lean common-denominator numerator representation','hypothesis_match':'same law and fixed coordinate order',
 'licensing_relations':['expectation_linearity'],'evidence_status':'compiled BellOperad.bell_evaluation and bell_graft; exact native replay'}],
 'failed_compositions':[], 'counterexamples':[], 'open_obligations':['P4 challenges','Fine converse','explicit symmetric action or syntactic quotient completeness if subsequently claimed']}
(P2/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta,sort_keys=False).encode())
p2req={'task_id':NODE,'stage_id':'P2_VERIFY','attempt_id':'p2','input_sha256':sha(RUN/'p1/candidate.json'),
 'candidate':'../p1/candidate.json','contract':'../../../../../pfp/stage_contracts.yaml',
 'required_gates':['G1_SCHEMA','G3_WITNESS','G5_SCOPE'],'not_applicable':{'G2_COCHAIN':'no cochain complex','G4_COUNTERMODEL':'P1 makes no countermodel claim'}}
dump(P2/'request.json',p2req)
host={**{k:p2req[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},
 'candidate_sha256':sha(RUN/'p1/candidate.json'),'status':'accepted_candidate_for_challenge',
 'checker_pins':hostpins,'predicate_results':{'G1_SCHEMA':'passed: original candidate bytes, binding, public laws, exact shape',
 'G2_COCHAIN':'not_applicable: no supplied cochain complex','G3_WITNESS':domain,
 'G4_COUNTERMODEL':'not_applicable: no P1 countermodel claim','G5_SCOPE':'narrowed common-law implication and explicitly listed anchors only; native checks executed'},
 'native_receipts':{k:k+'_receipt.json' for k in required}, 'rust_python_exact_agreement':len(samples),
 'infrastructure_retry':{'original_receipt':'rust_receipt.json','cause':'OS error 112: disk full while writing disposable incremental cache',
 'action':'removed this isolated worktree incremental caches only; reran unchanged sources with CARGO_INCREMENTAL=0','resolved':True},
 'bounded_failure_codes':[],'operad_delta':delta,
 'review_limitation':'same Codex agent performed source/scope review; independent native consumers and Lean kernel provided execution checks. No independent human/provider review.',
 'claim_boundary':{'supports':candidate['scope'],'does_not_support':'Fine converse, physical inference, full symmetric or syntactically presented quotient operad',
 'narrowest_claim':'finite-law Bell maps plus typed substitution semantic coherence','next_test':'P4 same-premise mutants and missing-premise controls'}}
dump(P2/'host_check.json',host);dump(P2/'candidate.json',{'checked_candidate':'../p1/candidate.json','candidate_sha256':host['candidate_sha256']})
shutil.copyfile(P2/'host_check.json',P2/'raw_response.txt')
prompt=ROOT/'dag/prompts/FINITE_QM_CORE__FQ-BELL-CLASSICAL-JOINT-EXTENSION__PROVED_LEAN.yaml'
packet=prepare.build_packet(prompt,'P4_CHALLENGE',attempt_id='p4',reviewed_path=RUN/'p0/reviewed_missions.json',review_path=RUN/'p0/host_review.json',
 candidate_path=RUN/'p1/candidate.json',host_check_path=P2/'host_check.json')
dump(P4/'request.json',packet)
mutants=P4/'mutants';mutants.mkdir(exist_ok=True)
results=[]
def reject(name,mutation):
    changed=copy.deepcopy(candidate);mutation(changed)
    p=mutants/(name+'.json');dump(p,changed)
    try:checker.check(RUN/'p1/request.json',p)
    except (ValueError,AssertionError) as e:results.append({'id':name,'candidate':p.relative_to(RUN).as_posix(),'rejected':True,'reason':str(e)})
    else:raise ValueError('challenge mutant accepted: '+name)
reject('false_upper_slack',lambda c:c['samples'][0].__setitem__('upper_slack','1'))
reject('false_correlator',lambda c:c['samples'][0]['correlators'].__setitem__(0,'0'))
reject('last_sign_plus',lambda c:c['samples'][0].__setitem__('chsh','4'))
reject('stale_input_binding',lambda c:c.__setitem__('input_sha256','0'*64))
valid=checker.check(RUN/'p1/request.json',RUN/'p1/candidate.json')
audit=loadmod('audit',ROOT/'dag/pfp/validate_prompts.py')
presentation=yaml.safe_load((ROOT/'dag/operads'/ (NODE+'.yaml')).read_bytes())['presentation']
assert not audit.check_presentation(presentation)
wrong=copy.deepcopy(presentation);wrong['compositions'][1]['inner_operation']='response_products'
colour_errors=audit.check_presentation(wrong);assert 'graft colour mismatch' in colour_errors
dump(P4/'wrong_colour_presentation.json',wrong)
# Uniform one-party marginals and positive normalized pairs still do not supply
# the common law required by this target (a PR box). This is NOT a countermodel
# satisfying the actual theorem's common-joint-law premise.
pairs=[['1/2','0','0','1/2']]*3+[['0','1/2','1/2','0']]
correlations=[]
for row in pairs:
    p=list(map(Q,row));assert min(p)>=0 and sum(p)==1
    assert p[0]+p[1]==p[2]+p[3]==p[0]+p[2]==p[1]+p[3]==Q(1,2)
    correlations.append(p[0]-p[1]-p[2]+p[3])
assert correlations[0]+correlations[1]+correlations[2]-correlations[3]==4
signed=[Q(0)]*16;signed[0]=Q(3,2);signed[1]=Q(-1,2)
assert sum(signed)==1 and 2*signed[0]-2*signed[1]==4
missing={'pair_order':['00','01','10','11'],'outcome_order':['--','-+','+-','++'],'pair_laws':pairs,'correlators':list(map(str,correlations)),
 'chsh':'4','single_party_marginals':'all uniform; verified exactly',
 'classification':'disproves weakening to separately normalized compatible pair laws; no supplied common law, hence NOT a counterexample to the actual theorem',
 'signed_law':list(map(str,signed)),'signed_chsh':'4','signed_classification':'normalization retained; nonnegativity premise fails; native tests require rejection'}
dump(P4/'missing_premise_controls.json',missing)
# An actual Lean kernel rejection of the wrong final sign, with the already
# compiled Bell theorem as the valid native control.
decoy=P4/'WrongSign.lean'
decoy.write_bytes(b'''import BellOperad
open QuantumMechanics.BellOperad QuantumMechanics.BellClassicalJointExtension
-- Deliberately false: the valid all-minus assignment gives four here, not two.
example : products plusAssignment 0 + products plusAssignment 1 +
    products plusAssignment 2 + products plusAssignment 3 = score plusAssignment := by decide
''')
env=os.environ.copy();env['LEAN_PATH']=str(ROOT/'lean4/.lake/build/lib/lean')
argv=[r'C:\Users\a343o\.elan\bin\lean.exe',str(decoy)]
p=subprocess.run(argv,cwd=ROOT/'lean4',env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(P4/'lean_wrong_sign.stdout.log').write_bytes(p.stdout);(P4/'lean_wrong_sign.stderr.log').write_bytes(p.stderr)
assert p.returncode!=0 and b'decide' in p.stdout
delta={'add_or_refine_generators':[], 'add_or_refine_relations':[
 {'id':'generic_table_scope','equation_or_predicate':'linearity holds for arbitrary response tables; CHSH bound requires binary product table',
 'evidence_status':'native generic-table example gives S=4, actual Bell table control accepted'}],
 'checked_compositions':[{'outer_operation':'chsh_linear','input_slot':0,'inner_operation':'joint_expectation','evidence_status':'valid structural and native controls retained'}],
 'failed_compositions':[{'outer_operation':'chsh_linear','input_slot':0,'inner_operation':'response_products','reason':'ResponseMap4 does not match CorrelatorTuple; omitted expectation/law'}],
 'counterexamples':[missing,{'id':'wrong_final_sign','valid_law':'vertex_0','mutant_value':'4','actual_chsh':'2','evidence_status':'independent checker and Lean both reject mutated equality'}],
 'open_obligations':['Fine converse under precise pair-marginal compatibility','symmetric action and arbitrary presented quotient completeness are not claimed']}
(P4/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta,sort_keys=False).encode())
response={**{k:packet[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},
 'near_miss':[x['candidate'] for x in results]+['missing_premise_controls.json','WrongSign.lean'],
 'challenged_predicate':['exact certificate equations','binding','same common law','nonnegative law','typed graft','last CHSH sign'],
 'valid_control':valid,'challenge_result':{'mutants':results,'wrong_colour_errors':colour_errors,'missing_premises':missing,
 'lean_wrong_sign':{'argv':argv,'exit_code':p.returncode,'stdout':'lean_wrong_sign.stdout.log','stderr':'lean_wrong_sign.stderr.log','expected_behavior':'reject false equality'}},
 'operad_delta':delta, 'claim_boundary':{'supports':'scoped candidate survives the executed attacks', 'does_not_support':'exhaustive adversarial robustness, Fine converse, physical claim',
 'narrowest_claim':candidate['scope'],'next_test':'P5 preserve results and open converse obligation'}}
dump(P4/'candidate.json',response);shutil.copyfile(P4/'candidate.json',P4/'raw_response.txt')
dump(P4/'host_check.json',{'task_id':NODE,'stage_id':'P4_CHALLENGE','attempt_id':'p4','input_sha256':packet['input_sha256'],
 'candidate_sha256':sha(P4/'candidate.json'),'status':'survives_executed_challenges','predicate_results':response['challenge_result'],
 'bounded_failure_codes':[],'operad_delta':delta})
print('P2 accepted scoped candidate; P4 rejected all actual mutants, retained valid control and missing-premise examples.')
