"""Run the actual P2 host gates; retain failure and never self-certify from labels."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import yaml

sys.dont_write_bytecode=True
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
TASK='FQ-BELL-RATIONAL-VIOLATION-14-5';RUN=ROOT/'dag/results'/TASK/'runs/20261019T015232Z_staged'
spec=importlib.util.spec_from_file_location('native',ROOT/'dag/results/batches/20261019T015232Z_next_ten/native.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def save(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode()
    if p.exists():
        if p.read_bytes()==raw:return
        raise ValueError('Refusing overwrite')
    p.write_bytes(raw)


prior=sys.argv[1] if len(sys.argv)>1 else 'p1'
checkpoint='p2' if prior=='p1' else 'p2_after_repair' if prior=='p3' else 'p2_after_'+prior
candidate=json.loads((RUN/prior/'candidate.json').read_bytes())
for pin in candidate['source_pins']:
    relative=pin['path'].split('/'+prior+'/construction/',1)[1]
    if sha(ROOT/relative)!=pin['sha256']:raise ValueError('Working source differs from submitted source: '+relative)
folder=RUN/checkpoint;digest=sha(RUN/prior/'candidate.json')
binding={'task_id':TASK,'stage_id':'P2_VERIFY','attempt_id':checkpoint,'input_sha256':digest}
save(folder/'request.json',{**binding,'candidate':'../'+prior+'/candidate.json','host_action':'Native and independent exact domain predicates; inspect literal theorem scope.'})
save(folder/'candidate.json',{'candidate_sha256':digest})
PY=sys.executable;CARGO=str(Path.home()/'.cargo/bin/cargo.exe');LEAN=str(Path.home()/'.elan/bin/lean.exe')
sources=[ROOT/pin['path'].split('/'+prior+'/construction/',1)[1] for pin in candidate['source_pins']]
records={}
commands=[('certificate',[PY,'-X','utf8',str(RUN/'check_candidate.py'),str(RUN/prior/'request.json'),str(RUN/prior/'candidate.json')],None),('python',[PY,'-X','utf8','code/python/tests/test_rational_bell.py','-v'],None),('rust',[CARGO,'test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib','rational_bell','--offline','--locked'],None),('lean',[LEAN,'-j','1','-o',str(native.LIB/'PromptBellRational.olean'),'PromptBellRational.lean'],None),('rust_replay',[CARGO,'run','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--example','rational_bell_replay','--offline','--locked'],(RUN/'public_cases.tsv').read_bytes())]
for label,command,stdin in commands:
    receipt=native.record(folder/'native',label,command,cwd=ROOT/'lean4' if label=='lean' else ROOT,sources=sources+([RUN/'check_candidate.py',ROOT/'dag/pfp/exact_json.py'] if label=='certificate' else []),stdin=stdin)
    records[label]=receipt;print(json.dumps({'gate':label,'exit_code':receipt['exit_code'],'seconds':receipt['seconds']}),flush=True)
ok=all(r['exit_code']==0 for r in records.values())
lean=(folder/'native/lean.stdout.log').read_text();anchors=['density_positive','rational_density_and_involutions','exact_born_correlations','all_born_cells_strictly_positive','no_scaled_joint_law']
reports=re.findall(r"'QuantumMechanics\.PromptBellRational\.([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",lean)
anchor_ok=len(reports)==len(anchors) and {n for n,_ in reports}==set(anchors) and all({a.strip() for a in axioms.split(',') if a.strip()}<={'propext','Classical.choice','Quot.sound'} for _,axioms in reports) and 'sorryAx' not in lean
cross=False
if records['rust_replay']['exit_code']==0:
    lines=(folder/'native/rust_replay.stdout.log').read_text().splitlines();cross=len(lines)==len(candidate['data']['cases'])
    for line,answer in zip(lines,candidate['data']['cases']):
        values=[answer['id']]+[q for row in answer['pairs'] for q in row]+answer['correlations']+[answer['chsh'],answer['minimum_probability'],str(answer['support_assignments']),answer['separator_lower'],answer['separator_upper'],str(answer['violating_mask']) if answer['violating_mask'] is not None else 'none']
        cross=cross and line.split('\t')==values
ok=ok and anchor_ok and cross
delta=yaml.safe_load((RUN/prior/'operad_delta.yaml').read_bytes())
for row in delta['add_or_refine_generators']:row['evidence_status']='P2 native and kernel gates evaluated; consult bound host status, not this label.'
result={**binding,'candidate_sha256':digest,'status':'accepted_candidate_for_challenge' if ok else 'repairable_candidate_defect','checker_pins':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in (RUN/'check_candidate.py',ROOT/'dag/pfp/exact_json.py')],'predicate_results':{'native_exit_codes':{k:v['exit_code'] for k,v in records.items()},'kernel_named_reports':anchor_ok,'actual_cross_language_certificate_equality':cross,'scope':'Fixed admitted quantum rational matrices and Nat-weighted assignment-law obstruction; rational array transport still separate.'},'bounded_failure_codes':[] if ok else ['G5_SCOPE'],'operad_delta':delta}
save(folder/'host_check.json',result);save(folder/'raw_response.json',result)
(folder/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta,sort_keys=False,allow_unicode=True,width=100).encode())
save(RUN/prior/'host_check.json',{**{k:candidate[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'candidate_sha256':digest,'status':'see_host_checkpoint','host_check':'../'+checkpoint+'/host_check.json'})
print(json.dumps({'node':TASK,'P2_status':result['status'],'reports':anchor_ok,'cross_language':cross}),flush=True)
