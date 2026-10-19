"""Execute fresh selected checks and retain actual stdout/stderr once per run."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'dag/pfp/prepare_stage.py').is_file())
OUT=HERE/'validation';OUT.mkdir(exist_ok=True)
PY=r'C:\Users\a343o\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
LEAN=r'C:\Users\a343o\.elan\bin\lean.exe'
CARGO=r'C:\Users\a343o\.cargo\bin\cargo.exe'
kind=sys.argv[1]
commands={
 'python':[(PY,['code/python/tests/test_bell_joint_extension.py','-v'],ROOT)],
 'rust':[(CARGO,['test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib','bell_joint_extension','--offline','--locked'],ROOT)],
 'rust_replay':[(CARGO,['run','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--example','bell_operad_replay','--offline','--locked'],ROOT)],
 'protocol':[(sys.executable,['-X','utf8','-m','unittest','discover','-s','dag/pfp','-p','test_staged_prompts.py','-v'],ROOT)],
 'review_tests':[(sys.executable,['-X','utf8',str(HERE/'test_review.py'),'-v'],ROOT)],
 'lean':[(LEAN,['--version'],ROOT/'lean4')]+[(LEAN,['-o',str(ROOT/'lean4/.lake/build/lib/lean'/(name+'.olean')),name+'.lean'],ROOT/'lean4')
    for name in ['DerivationDagQMClosure','BellClassicalJointExtension','BellOperad']]
}
env=os.environ.copy();env['CARGO_INCREMENTAL']='0';env['LEAN_PATH']=str(ROOT/'lean4/.lake/build/lib/lean')
receipts=[]
for i,(exe,args,cwd) in enumerate(commands[kind]):
    prefix=OUT/(kind+'_'+str(i));stdout=prefix.with_suffix('.stdout.log');stderr=prefix.with_suffix('.stderr.log')
    with stdout.open('xb') as out, stderr.open('xb') as err:
        start=time.time();p=subprocess.run([exe]+args,cwd=cwd,env=env,stdout=out,stderr=err)
    receipts.append({'argv':[exe]+args,'cwd':str(cwd),'exit_code':p.returncode,'seconds':round(time.time()-start,3),
     'environment_overrides':{'CARGO_INCREMENTAL':'0','LEAN_PATH':env['LEAN_PATH']},
     'stdout':stdout.relative_to(HERE).as_posix(),'stderr':stderr.relative_to(HERE).as_posix()})
    print(kind,i,'exit',p.returncode,flush=True)
    if p.returncode:print(stdout.read_text(errors='replace')+stderr.read_text(errors='replace'),flush=True);break
with (OUT/(kind+'_receipt.json')).open('x',encoding='utf8',newline='\n') as f:json.dump(receipts,f,indent=2);f.write('\n')
sys.exit(any(x['exit_code'] for x in receipts))
