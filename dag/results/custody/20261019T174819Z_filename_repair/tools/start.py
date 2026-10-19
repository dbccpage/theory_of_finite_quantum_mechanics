"""Retain the actual failing baseline before installing the custody successor."""
import hashlib,json,os,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
R=ROOT/'dag/results/custody/20261019T174819Z_filename_repair'
def put(p,b):
    if p.exists():raise ValueError('Refusing overwrite '+str(p))
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def save(p,x):put(p,(json.dumps(x,indent=2)+'\n').encode())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
put(R/'.gitattributes',b'* -text whitespace=-trailing-space,-blank-at-eof\n')
put(R/'tools/start.py',Path(__file__).read_bytes())
for name in ('validate_prompts.py','test_staged_prompts.py','prompt_audit.json'):
    put(R/'before/dag/pfp'/name,(ROOT/'dag/pfp'/name).read_bytes())
save(R/'selection.json',{'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'historical_commit':'d7ba086146b96811114651afaabd0afdd49ac7c2','migration_commit':'e5f7defe28e8a2f64273d5ffb157120ace83adee','scope':'Repair live custody and protocol checks only. No previous staged artifact, prompt text, canonical operad, historical audit or mathematical value is to be overwritten.','authority_effect':'None'})
for name,argv in [('validator',[sys.executable,'-X','utf8','dag/pfp/validate_prompts.py']),('protocol',[sys.executable,'-X','utf8','dag/pfp/test_staged_prompts.py','-v'])]:
    sources=[ROOT/'dag/pfp/validate_prompts.py',ROOT/'dag/pfp/test_staged_prompts.py',Path(__file__)]
    pins={str(p):sha(p) for p in sources};start=time.perf_counter();stamp=datetime.now(timezone.utc).isoformat()
    p=subprocess.run(argv,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    put(R/'baseline'/(name+'.stdout.log'),p.stdout);put(R/'baseline'/(name+'.stderr.log'),p.stderr)
    same=all(sha(Path(p))==h for p,h in pins.items());save(R/'baseline'/(name+'_receipt.json'),{'argv':argv,'started_utc':stamp,'seconds':round(time.perf_counter()-start,3),'exit_code':p.returncode,'source_pins':pins,'sources_unchanged':same})
    if not same or p.returncode==0:raise ValueError('Baseline differs from the reported failures')
    print(json.dumps({'gate':name,'actual_exit_code':p.returncode,'seconds':round(time.perf_counter()-start,3)}),flush=True)
