"""Retain native checker inputs, stdout, stderr and exit status without accepting model verdicts."""
import hashlib,json,os,subprocess,time
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
ROOT=next(p for p in R.parents if (p/'dag/pfp/prepare_stage.py').is_file())
PACKAGES=Path(r'C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/.lake/packages')
LIBS=[ROOT/'lean4/.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in PACKAGES.iterdir() if (p/'.lake/build/lib/lean').is_dir()]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(folder,label,args,*,cwd=ROOT,sources=()):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);receipt=folder/(label+'_receipt.json')
 if receipt.exists():raise ValueError('immutable receipt exists')
 paths=list(dict.fromkeys([Path(__file__),*(Path(p) for p in sources)]))
 frozen=folder/(label+'_inputs');frozen.mkdir()
 pins=[]
 for i,p in enumerate(paths):
  raw=p.read_bytes();snapshot=frozen/(str(i)+'_'+p.name);snapshot.write_bytes(raw);pins.append({'path':str(p.resolve()),'sha256':sha(p),'snapshot':str(snapshot.relative_to(R))})
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',LEAN_PATH=os.pathsep.join(map(str,LIBS)))
 start=time.monotonic();began=datetime.now(timezone.utc).isoformat();p=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 (folder/(label+'.stdout.log')).write_bytes(p.stdout);(folder/(label+'.stderr.log')).write_bytes(p.stderr)
 unchanged=all(sha(q['path'])==q['sha256'] for q in pins)
 data={'argv':args,'cwd':str(cwd),'started_utc':began,'seconds':round(time.monotonic()-start,3),'exit_code':p.returncode,'sources':pins,'sources_unchanged':unchanged,'LEAN_PATH':env['LEAN_PATH'],'claim':'Actual process result only; proof/semantic acceptance is a separate host decision.'}
 receipt.write_bytes((json.dumps(data,indent=2)+'\n').encode())
 if not unchanged:raise ValueError('source changed during native invocation')
 return data
