"""Create the ordered batch and install exact local operations without promotion."""
import importlib.util,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');SRC=Path(__file__).resolve().parent
ID='20261019T160201Z_prompts_22_31';BATCH=ROOT/'dag/results/batches'/ID;OLD=ROOT/'dag/results/batches/20261019T145000Z_prompts_12_21'
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('Refusing overwrite '+str(p))
    p.write_bytes(b)
put(BATCH/'.gitattributes',b'* -text whitespace=-trailing-space,-blank-at-eof\n')
for name in ('native.py','target_stages.py'):put(BATCH/name,(OLD/name).read_bytes().replace(b'20261019T145000Z_prompts_12_21',ID.encode()))
t=(OLD/'tools/init.py').read_text().replace('20261019T145000Z_prompts_12_21',ID).replace('20261019T145000Z_staged','20261019T160201Z_staged').replace('selected = nodes[11:21]','selected = nodes[21:31]').replace('positions 12 through 21 after the eleven completed nodes','positions 22 through 31 after the twenty-one completed nodes')
put(BATCH/'tools/init.py',t.encode());subprocess.run([sys.executable,'-X','utf8',str(BATCH/'tools/init.py')],cwd=ROOT,check=True)
put(BATCH/'index_before.json',(ROOT/'dag/operads/index.json').read_bytes())
for name,dest in [('structure_exact.py','code/python/src/qm/structure_exact.py'),('structure_exact.rs','code/rust/src/finite_probability/structure_exact.rs'),('structure_exact_replay.rs','code/rust/src/finite_probability/examples/structure_exact_replay.rs'),('structure_checker.py','dag/pfp/structure_checker.py'),('PromptStructure.lean','lean4/PromptStructure.lean'),('test_structure_exact.py','code/python/tests/test_structure_exact.py')]:put(ROOT/dest,(SRC/name).read_bytes())
p=ROOT/'code/rust/src/finite_probability/lib.rs';p.write_bytes(p.read_bytes()+b'\npub mod structure_exact;\n')
p=ROOT/'lean4/lakefile.lean';p.write_bytes(p.read_bytes().replace(b'    `PromptPhaseScope,',b'    `PromptPhaseScope,\n    `PromptStructure,'))
subprocess.run([str(Path.home()/'.cargo/bin/rustfmt.exe'),'--edition','2021',str(ROOT/'code/rust/src/finite_probability/structure_exact.rs'),str(ROOT/'code/rust/src/finite_probability/examples/structure_exact_replay.rs')],check=True)
deps=[]
def visit(name):
    if name in deps:return
    p=ROOT/'lean4'/(name+'.lean')
    for line in re.findall(r'^import\s+([^\r\n]+)',p.read_text(),re.M):
        for child in line.split():
            if (ROOT/'lean4'/(child+'.lean')).is_file():visit(child)
    deps.append(name)
visit('PromptStructure');put(BATCH/'lean_order.json',(json.dumps(deps,indent=2)+'\n').encode())
for name in ('setup.py','prepare.py','run.py'):put(BATCH/'tools'/name,(SRC/name).read_bytes())
print(json.dumps({'batch':ID,'local_Lean_modules':len(deps)}))
