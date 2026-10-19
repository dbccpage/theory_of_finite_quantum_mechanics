import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T233710Z_separator_extension'
KIND=sys.argv[1];ATTEMPT=sys.argv[2] if len(sys.argv)>2 else 'p2'
OUT=RUN/ATTEMPT;OUT.mkdir(exist_ok=True);(OUT/'logs').mkdir(exist_ok=True)
PY=r'C:\Users\a343o\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
CARGO=r'C:\Users\a343o\.cargo\bin\cargo.exe';LEAN=r'C:\Users\a343o\.elan\bin\lean.exe'
source_attempt='p3' if ATTEMPT=='p2_after_repair' else 'p1'
commands={
 'python':[(PY,['code/python/tests/test_bell_separator_extension.py','-v'],ROOT)],
 'rust':[(CARGO,['test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib','bell_separator_extension','--offline','--locked'],ROOT)],
 'rust_replay':[(CARGO,['run','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--example','bell_separator_replay','--offline','--locked'],ROOT)],
 'certificate':[(PY,[str(RUN/'check_candidate.py'),str(RUN/source_attempt/'request.json'),str(RUN/source_attempt/'candidate.json')],ROOT)],
 'protocol':[(sys.executable,['-X','utf8','-m','unittest','discover','-s','dag/pfp','-p','test_staged_prompts.py','-v'],ROOT)],
 'lean':[(LEAN,['--version'],ROOT/'lean4')]+[(LEAN,['-o',str(ROOT/'lean4/.lake/build/lib/lean'/(name+'.olean')),name+'.lean'],ROOT/'lean4')
    for name in ['DerivationDagQMClosure','BellClassicalJointExtension','BellOperad','BellSeparatorExtension']]
}
env=os.environ.copy();env['CARGO_INCREMENTAL']='0';env['LEAN_PATH']=str(ROOT/'lean4/.lake/build/lib/lean')
if KIND=='lean_recheck':commands[KIND]=[commands['lean'][0],commands['lean'][-1]]
receipts=[]
for i,(exe,args,cwd) in enumerate(commands[KIND]):
    prefix=OUT/'logs'/(KIND+'_'+str(i));stdout=prefix.with_suffix('.stdout.log');stderr=prefix.with_suffix('.stderr.log')
    with stdout.open('xb') as out,stderr.open('xb') as err:
        start=time.time();p=subprocess.run([exe]+args,cwd=cwd,env=env,stdout=out,stderr=err,
            input=(RUN/'public_cases.tsv').read_bytes() if KIND=='rust_replay' else None)
    receipts.append({'argv':[exe]+args,'cwd':str(cwd),'exit_code':p.returncode,'seconds':round(time.time()-start,3),
     'environment_overrides':{'CARGO_INCREMENTAL':'0','LEAN_PATH':env['LEAN_PATH']},
     'stdin':'public_cases.tsv' if KIND=='rust_replay' else None,
     'stdout':stdout.relative_to(RUN).as_posix(),'stderr':stderr.relative_to(RUN).as_posix()})
    print(KIND,i,'exit',p.returncode,flush=True)
    if p.returncode:print(stdout.read_text(errors='replace')+stderr.read_text(errors='replace'),flush=True);break
with (OUT/(KIND+'_receipt.json')).open('x',encoding='utf8',newline='\n') as f:json.dump(receipts,f,indent=2);f.write('\n')
sys.exit(any(x['exit_code'] for x in receipts))
