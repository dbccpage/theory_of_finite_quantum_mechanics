"""One-time native validation recorder. Refuses to overwrite a sealed review."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'dag/pfp/prepare_stage.py').is_file())
RUN = HERE.parent.parent/'runs/20261018T233710Z_separator_extension'
if (HERE/'review_manifest.json').exists():
    raise SystemExit('Review is sealed. Use verify_review.py for read-only replay.')
LOGS = HERE/'validation/logs'; LOGS.mkdir(parents=True, exist_ok=True)
PY = sys.executable
CARGO = str(Path.home()/'.cargo/bin/cargo.exe')
LEAN = str(Path.home()/'.elan/bin/lean.exe')
LIB = ROOT/'lean4/.lake/build/lib/lean'
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', CARGO_INCREMENTAL='0', LEAN_PATH=str(LIB))
REL = HERE.relative_to(ROOT).as_posix()
plans = {
 'python': {'cwd':'.','commands':[[PY,'-X','utf8','code/python/tests/test_bell_separator_extension.py','-v']]},
 'rust': {'cwd':'.','commands':[[CARGO,'test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib','bell_separator_extension','--offline','--locked']]},
 'rust_replay': {'cwd':'.','commands':[[CARGO,'run','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--example','bell_separator_replay','--offline','--locked']], 'stdin':{'path':(RUN/'public_cases.tsv').relative_to(ROOT).as_posix(),'sha256':hashlib.sha256((RUN/'public_cases.tsv').read_bytes()).hexdigest()}},
 'python_replay': {'cwd':'.','commands':[[PY,'-X','utf8',REL+'/recheck_python.py']]},
 'lean': {'cwd':'lean4','commands':[[LEAN,'--version']]+[[LEAN,'-o',str(LIB/(name+'.olean')),name+'.lean'] for name in ['DerivationDagQMClosure','BellClassicalJointExtension','BellOperad','BellSeparatorExtension']]},
 'protocol': {'cwd':'.','commands':[[PY,'-X','utf8','dag/pfp/test_staged_prompts.py','-v']]},
 'guards': {'cwd':'.','commands':[[PY,'-X','utf8',REL+'/test_review_guards.py','-v']]},
 'guards_optimized': {'cwd':'.','commands':[[PY,'-X','utf8','-O',REL+'/test_review_guards.py','-v']]},
 'structure': {'cwd':'.','commands':[[PY,'-X','utf8','dag/pfp/validate_prompts.py']]}}


def write_json(path, value):
    path.write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())


write_json(HERE/'validation_plan.json', plans)


def run(kind):
    plan = plans[kind]; receipts = []
    for i, command in enumerate(plan['commands']):
        start = time.perf_counter(); now = datetime.now(timezone.utc).isoformat()
        stdin = (ROOT/plan['stdin']['path']).read_bytes() if 'stdin' in plan else None
        result = subprocess.run(command,cwd=ROOT/plan['cwd'],env=environment,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out, err = LOGS/(kind+'_'+str(i)+'.stdout.log'), LOGS/(kind+'_'+str(i)+'.stderr.log')
        out.write_bytes(result.stdout); err.write_bytes(result.stderr)
        receipts.append({'argv':command,'cwd':str(ROOT/plan['cwd']),'started_utc':now,'seconds':round(time.perf_counter()-start,3),'exit_code':result.returncode,'environment_overrides':{k:environment[k] for k in ('PYTHONDONTWRITEBYTECODE','CARGO_INCREMENTAL','LEAN_PATH')},'stdin':plan.get('stdin'),'stdout':out.relative_to(HERE).as_posix(),'stderr':err.relative_to(HERE).as_posix()})
        write_json(HERE/'validation'/(kind+'_receipt.json'),receipts)
        if result.returncode:
            raise RuntimeError(kind+' failed; see '+str(err))
    if kind in ('structure','python_replay'):
        write_json(HERE/'validation'/(kind+'.json'),json.loads(result.stdout))
    return {'kind':kind,'calls':len(receipts),'seconds':sum(r['seconds'] for r in receipts)}


# Independent processes may run concurrently. Cargo test/replay stay sequential.
requested = sys.argv[1:] or list(plans)
if any(k not in plans for k in requested):
    raise SystemExit('Unknown validation group')
with ThreadPoolExecutor(max_workers=5) as pool:
    pending={pool.submit(run,k):k for k in requested if k!='rust_replay'}
    for future in as_completed(pending):
        print(json.dumps(future.result()),flush=True)
if 'rust_replay' in requested:
    print(json.dumps(run('rust_replay')),flush=True)
