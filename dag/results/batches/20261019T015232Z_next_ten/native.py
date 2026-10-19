"""Retain actual native calls with source bytes before/after each invocation."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file())
LIB = ROOT/'lean4/.lake/build/lib/lean'
PACKAGES = Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\lean4\.lake\packages')
LEAN_LIBS = [LIB]+[p/'.lake/build/lib/lean' for p in PACKAGES.iterdir() if (p/'.lake/build/lib/lean').is_dir()]
ENV = {'PYTHONDONTWRITEBYTECODE':'1','CARGO_INCREMENTAL':'0','LEAN_PATH':os.pathsep.join(map(str,LEAN_LIBS))}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(folder, label, command, *, cwd=ROOT, sources=(), stdin=None):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    receipt_path=folder/(label+'_receipt.json')
    if receipt_path.exists():
        raise ValueError('Native call already recorded: '+str(receipt_path))
    pins=[{'path':str(p),'sha256':sha(Path(p))} for p in sources]
    start=time.perf_counter();started=datetime.now(timezone.utc).isoformat()
    result=subprocess.run(command,cwd=cwd,env=dict(os.environ,**ENV),input=stdin,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=folder/(label+'.stdout.log'),folder/(label+'.stderr.log')
    out.write_bytes(result.stdout);err.write_bytes(result.stderr)
    unchanged=all(sha(Path(p['path']))==p['sha256'] for p in pins)
    receipt={'argv':command,'cwd':str(cwd),'started_utc':started,'seconds':round(time.perf_counter()-start,3),'exit_code':result.returncode,'environment_overrides':ENV,'source_pins':pins,'sources_unchanged':unchanged,'stdin_sha256':None if stdin is None else hashlib.sha256(stdin).hexdigest(),'stdout':out.name,'stderr':err.name}
    receipt_path.write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
    if not unchanged:
        raise ValueError('Source mutated during native call')
    return receipt
