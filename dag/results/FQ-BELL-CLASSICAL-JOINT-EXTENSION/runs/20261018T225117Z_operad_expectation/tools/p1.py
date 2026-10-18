import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import shutil
from fractions import Fraction as Q

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T225117Z_operad_expectation'
P1=RUN/'p1'
request=json.loads((P1/'request.json').read_bytes())
public=request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']
spec=importlib.util.spec_from_file_location('bell',ROOT/'code/python/src/qm/bell_joint_extension.py')
bell=importlib.util.module_from_spec(spec);sys.modules['bell']=bell;spec.loader.exec_module(bell)
samples=[]
for case in public['cases']:
    c=bell.certify_joint_law(list(map(Q,case['weights'])))
    samples.append({'id':case['id'],'weights':case['weights'],'correlators':list(map(str,c.correlators)),
    **{key:str(getattr(c,key)) for key in ['chsh','positive_score_mass','negative_score_mass','lower_slack','upper_slack']}})
candidate={'schema_id':'finite-qm.bell-operad-certificate.v1',**{k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},
 'samples':samples,'anchors':public['required_anchors'],'scope':public['scope']}
def dump(path,value):path.write_bytes((json.dumps(value,indent=2)+'\n').encode())
dump(P1/'candidate.json',candidate);shutil.copyfile(P1/'candidate.json',P1/'raw_response.txt')
sources=['code/python/src/qm/bell_joint_extension.py','code/python/tests/test_bell_joint_extension.py',
 'code/rust/src/finite_probability/bell_joint_extension.rs','lean4/BellOperad.lean','lean4/lakefile.lean']
pins=[]
for source in sources:
    destination=P1/'construction'/source;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/source,destination)
    pins.append({'path':destination.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'working_source':source})
delta={'add_or_refine_generators':[
 {'id':'joint_expectation','change':'generic exact rational response-table API in Rust and Python; arbitrary integral response-table operation in Lean common-denominator representation'},
 {'id':'endomorphism_substitute','change':'dependent typed simultaneous substitution, identities, associativity under explicit index reassociation'},
 {'id':'certificate_verify','change':'consumer checks every scalar and correlator against supplied law using a route separate from producer'}],
 'add_or_refine_relations':['generic expectation/CHSH linearity','typed simultaneous substitution units and associativity','semantic equality stable under substitution'],
 'checked_compositions':[], 'failed_compositions':[], 'counterexamples':[],
 'open_obligations':['P2 native compilation and independent certificate checking','P4 adversarial tests','Fine converse and symmetric/quotient presentation remain open']}
(P1/'operad_delta.yaml').write_bytes((json.dumps(delta,indent=2)+'\n').encode())
dump(P1/'response.json', {**{k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'candidate_certificate':'candidate.json',
 'construction':pins,'remaining_obligations':delta['open_obligations'],'operad_delta':delta,
 'claim_boundary':{'supports':'submitted exact certificates and proof source constructions', 'does_not_support':'acceptance before P2, Fine converse, symmetric quotient operad',
 'narrowest_claim':public['scope'],'next_test':'compile proof and run independently selected native gates'}})
# Compile an exact Rust producer over the SAME P0 public cases, not copied answers.
example=ROOT/'code/rust/src/finite_probability/examples/bell_operad_replay.rs';example.parent.mkdir(exist_ok=True)
rows=[]
for case in public['cases']:
    rows.append('    emit('+json.dumps(case['id'])+', &['+', '.join(json.dumps(x) for x in case['weights'])+']);')
source='''//! Replays the P0 public laws as exact rationals, emitting TSV for independent comparison.
//! Generated from the retained P0 inputs, with no expected certificate values.
use tfqm_finite_probability::bell_joint_extension::{certify_joint_law,verify_joint_certificate,joint_expectation,response_products,chsh_linear};
use num_bigint::BigInt;
use num_rational::BigRational as Q;
fn parse(s:&str)->Q { let (n,d)=s.split_once('/').unwrap_or((s,"1"));Q::new(n.parse::<BigInt>().unwrap(),d.parse::<BigInt>().unwrap()) }
fn emit(id:&str,raw:&[&str]) {
    let law:Vec<Q>=raw.iter().map(|s|parse(s)).collect();
    let c=certify_joint_law(&law).unwrap();verify_joint_certificate(&law,&c).unwrap();
    let table:Vec<[Q;4]>=response_products().iter().map(|r|r.map(|x|Q::from_integer(x.into()))).collect();
    assert_eq!(joint_expectation(&law,&table).unwrap(),c.correlators);
    assert_eq!(chsh_linear(&c.correlators).unwrap(),c.chsh);
    print!("{}",id);for x in c.correlators {print!("\\t{}",x);}
    for x in [c.chsh,c.positive_score_mass,c.negative_score_mass,c.lower_slack,c.upper_slack] {print!("\\t{}",x);}
    println!();
}
fn main(){
'''+ '\n'.join(rows)+'\n}\n'
example.write_bytes(source.encode())
dest=P1/'construction'/example.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(example,dest)
print('P1 candidate saved:',len(samples),'public laws; native checking pending.')
