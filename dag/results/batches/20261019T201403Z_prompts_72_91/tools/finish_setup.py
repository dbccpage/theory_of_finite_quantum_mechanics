"""Resume P0 with an explicit successor snapshot, keeping initial bytes intact."""
import hashlib,importlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');SRC=Path(__file__).resolve().parent;ID='20261019T201403Z_prompts_72_91';RUN='20261019T201403Z_staged';B=ROOT/'dag/results/batches'/ID;OLD=ROOT/'dag/results/batches/20261019T184100Z_prompts_52_71'
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('refuse overwrite '+str(p))
    p.write_bytes(b)
t=(B/'tools/init_after_source_review.py').read_text()
t=t.replace("if snapshot.read_bytes()!=actual.read_bytes():raise ValueError('Existing snapshot differs '+relative)","if snapshot.read_bytes()!=actual.read_bytes():\n                    if name!='DS-QM212-MAJORANA-PROBLEM' or relative!='dag/operads/ds_qm212_majorana_problem.yaml' or snapshot.read_bytes()!=(BATCH/'custody/majorana_collection_before.yaml').read_bytes():raise ValueError('Unreviewed snapshot drift '+relative)\n                    record['historical_collection_snapshot']=snapshot.relative_to(ROOT).as_posix()\n                    snapshot=run/'inputs_after_source_review'/repository/relative\n                    snapshot.parent.mkdir(parents=True,exist_ok=True)\n                    if snapshot.exists():raise ValueError('Successor snapshot exists')\n                    shutil.copyfile(actual,snapshot)")
put(B/'tools/init_with_successor_snapshot.py',t.encode())
put(B/'custody/resume_refusal.json',(json.dumps({'exit_code':1,'failure':'Existing snapshot differs dag/operads/ds_qm212_majorana_problem.yaml','resolution':'Original snapshot retained; the reviewed collection successor receives a separate inputs_after_source_review path. No original P0 request or snapshot is overwritten.'},indent=2)+'\n').encode())
subprocess.run([sys.executable,'-X','utf8',str(B/'tools/init_with_successor_snapshot.py')],cwd=ROOT,check=True);put(B/'index_before.json',(ROOT/'dag/operads/index.json').read_bytes())
setup=(SRC/'setup.py').read_text();tail=setup[setup.index('for name,dest in '):];exec(compile(tail,str(SRC/'setup.py')+' resumed tail','exec'),globals())
put(B/'tools/resume_setup.py',(SRC/'resume_setup.py').read_bytes());put(B/'tools/finish_setup.py',Path(__file__).read_bytes())
