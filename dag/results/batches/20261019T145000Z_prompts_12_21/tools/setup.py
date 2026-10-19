"""Install and prepare the next ten ordered, scoped local PFP stages."""
import hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
SRC=Path(__file__).resolve().parent
ID='20261019T145000Z_prompts_12_21';BATCH=ROOT/'dag/results/batches'/ID
OLD=ROOT/'dag/results/batches/20261019T015232Z_next_ten'
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('overwrite '+str(p))
    p.write_bytes(b)
BATCH.mkdir(parents=True,exist_ok=True)
put(BATCH/'.gitattributes',b'* -text whitespace=-trailing-space,-blank-at-eof\n')
for name in ('native.py','target_stages.py'):
    text=(OLD/name).read_text().replace('20261019T015232Z_next_ten',ID)
    if name=='native.py':
        text=text.replace("pins=[{'path'", "sources=list(dict.fromkeys(list(sources)+[Path(__file__),Path(__file__).parent/'target_stages.py']))\n    pins=[{'path'")
    put(BATCH/name,text.encode())
text=(OLD/'tools/init_next_ten.py').read_text().replace('20261019T015232Z_next_ten',ID).replace('20261019T015232Z_staged','20261019T145000Z_staged').replace('selected = nodes[1:11]','selected = nodes[11:21]')
text=text.replace('The ten indexed prompts immediately following the completed FQ-BELL-CLASSICAL-JOINT-EXTENSION; no cherry picking.','Ordered index positions 12 through 21 after the eleven completed nodes; no cherry picking.').replace('No merge requested.','Merge explicitly requested.').replace('open PR; no merge.','open PR and merge after verified checks.')
put(BATCH/'tools/init.py',text.encode());subprocess.run([sys.executable,'-X','utf8',str(BATCH/'tools/init.py')],cwd=ROOT,check=True)
put(BATCH/'index_before.json',(ROOT/'dag/operads/index.json').read_bytes())
for name,target in [('phase_scope.py','code/python/src/qm/phase_scope.py'),('test_phase_scope.py','code/python/tests/test_phase_scope.py'),('phase_scope.rs','code/rust/src/finite_probability/phase_scope.rs'),('phase_scope_replay.rs','code/rust/src/finite_probability/examples/phase_scope_replay.rs'),('PromptPhaseScope.lean','lean4/PromptPhaseScope.lean'),('phase_scope_checker.py','dag/pfp/phase_scope_checker.py')]:put(ROOT/target,(SRC/name).read_bytes())
p=ROOT/'code/python/tests/test_phase_scope.py';p.write_bytes(p.read_bytes().replace(b'from qm.phase_scope import evaluate,binary_ray',b"import importlib.util\nsp=importlib.util.spec_from_file_location('phase_scope',Path(__file__).resolve().parents[1]/'src/qm/phase_scope.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)\nevaluate,binary_ray=m.evaluate,m.binary_ray"))
p=ROOT/'code/rust/src/finite_probability/lib.rs';p.write_bytes(p.read_bytes()+b'\npub mod phase_scope;\n')
p=ROOT/'lean4/lakefile.lean';p.write_bytes(p.read_bytes().replace(b'    `PromptBornGap,',b'    `PromptBornGap,\n    `PromptPhaseScope,'))
subprocess.run([str(Path.home()/'.cargo/bin/rustfmt.exe'),'--edition','2021',str(ROOT/'code/rust/src/finite_probability/phase_scope.rs'),str(ROOT/'code/rust/src/finite_probability/examples/phase_scope_replay.rs')],check=True)
put(BATCH/'tools/setup.py',(SRC/'setup.py').read_bytes())
print(ID,flush=True)
