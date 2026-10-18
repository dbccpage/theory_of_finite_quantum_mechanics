import json
import os
from pathlib import Path
import subprocess
import sys
import time
import hashlib

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T225117Z_operad_expectation'
P2=RUN/'p2';P2.mkdir(exist_ok=True)
(P2/'logs').mkdir(exist_ok=True)
PY=r'C:\Users\a343o\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
kind=sys.argv[1]
commands={
 'python':[(PY,['code/python/tests/test_bell_joint_extension.py','-v'],ROOT)],
 'rust':[(r'C:\Users\a343o\.cargo\bin\cargo.exe',['test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib','bell_joint_extension','--offline','--locked'],ROOT)],
 'rust_replay':[(r'C:\Users\a343o\.cargo\bin\cargo.exe',['run','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--example','bell_operad_replay','--offline','--locked'],ROOT)],
 'certificate':[(PY,[str(RUN/'check_certificate.py'),str(RUN/'p1/request.json'),str(RUN/'p1/candidate.json')],ROOT)],
 'lean':[(r'C:\Users\a343o\.elan\bin\lean.exe',['--version'],ROOT/'lean4')]+[
 (r'C:\Users\a343o\.elan\bin\lean.exe',['-o',str(ROOT/'lean4/.lake/build/lib/lean'/(name+'.olean')),name+'.lean'],ROOT/'lean4')
 for name in ['DerivationDagQMClosure','BellClassicalJointExtension','BellOperad']]
}
env=os.environ.copy();env['LEAN_PATH']=str(ROOT/'lean4/.lake/build/lib/lean')
env['CARGO_INCREMENTAL']='0'
if kind == 'rust_retry': commands[kind]=commands['rust']
(ROOT/'lean4/.lake/build/lib/lean').mkdir(parents=True,exist_ok=True)
receipts=[]
for i,(exe,args,cwd) in enumerate(commands[kind]):
    start=time.time(); p=subprocess.run([exe]+args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    prefix=P2/'logs'/(kind+'_'+str(i))
    prefix.with_suffix('.stdout.log').write_bytes(p.stdout);prefix.with_suffix('.stderr.log').write_bytes(p.stderr)
    receipts.append({'argv':[exe]+args,'cwd':str(cwd),'exit_code':p.returncode,'seconds':round(time.time()-start,3),
      'stdout':prefix.with_suffix('.stdout.log').relative_to(RUN).as_posix(),'stderr':prefix.with_suffix('.stderr.log').relative_to(RUN).as_posix()})
    print(kind,i,'exit',p.returncode,flush=True)
    if p.returncode: print(p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'),flush=True);break
(P2/(kind+'_receipt.json')).write_bytes((json.dumps(receipts,indent=2)+'\n').encode())
sys.exit(any(x['exit_code']!=0 for x in receipts))
