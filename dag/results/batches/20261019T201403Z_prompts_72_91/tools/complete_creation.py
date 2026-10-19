"""Finish the unexecuted creation tail after Python importlib initialization."""
import importlib.util,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');SRC=Path(__file__).resolve().parent;ID='20261019T201403Z_prompts_72_91';RUN='20261019T201403Z_staged';B=ROOT/'dag/results/batches'/ID;OLD=ROOT/'dag/results/batches/20261019T184100Z_prompts_52_71'
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('refuse overwrite '+str(p))
    p.write_bytes(b)
put(B/'custody/creation_import_failure.json',(json.dumps({'exit_code':1,'failure':"AttributeError: module importlib has no attribute util",'phase':'Creation driver, after P0 preparation and before native derivation','resolution':'Explicitly import importlib.util and execute only the previously unexecuted tail; no existing request/source is overwritten.'},indent=2)+'\n').encode())
setup=(SRC/'setup.py').read_text();tail=setup[setup.index("sp=importlib.util.spec_from_file_location('producer_for_declared_tables'"):];ns=dict(globals(),__file__=str(SRC/'setup.py'));exec(compile(tail,str(SRC/'setup.py')+' completed tail','exec'),ns)
for name in ('resume_setup.py','finish_setup.py','complete_creation.py'):put(B/'tools'/name,(SRC/name).read_bytes())
