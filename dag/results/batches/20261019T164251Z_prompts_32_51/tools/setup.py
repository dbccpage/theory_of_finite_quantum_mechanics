"""Install a new ordered twenty-node batch, preserving all previous evidence."""
import json,re,subprocess,sys
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');SRC=Path(__file__).resolve().parent
ID='20261019T164251Z_prompts_32_51';BATCH=ROOT/'dag/results/batches'/ID;OLD=ROOT/'dag/results/batches/20261019T160201Z_prompts_22_31'
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('Refusing overwrite '+str(p))
    p.write_bytes(b)
put(BATCH/'.gitattributes',b'* -text whitespace=-trailing-space,-blank-at-eof\n')
for name in ('native.py','target_stages.py'):
    put(BATCH/name,(OLD/name).read_bytes().replace(b'20261019T160201Z_prompts_22_31',ID.encode()).replace(b'ten-prompt',b'twenty-prompt'))
t=(OLD/'tools/init.py').read_text().replace('20261019T160201Z_prompts_22_31',ID).replace('20261019T160201Z_staged','20261019T164251Z_staged').replace('selected = nodes[21:31]','selected = nodes[31:51]').replace('positions 22 through 31 after the twenty-one completed nodes','positions 32 through 51 after the thirty-one completed nodes').replace('ten ordered','twenty ordered').replace('all ten','all twenty').replace('After ten','After twenty')
# Refuse to silently replay an existing completed node.
t=t.replace("name = node['node_id']; run =", "name = node['node_id']\n    if any((ROOT/'dag/results'/name/'runs').glob('*/p5/candidate.json')):raise ValueError('Selected prompt already run: '+name)\n    run =")
put(BATCH/'tools/init.py',t.encode());subprocess.run([sys.executable,'-X','utf8',str(BATCH/'tools/init.py')],cwd=ROOT,check=True)
put(BATCH/'index_before.json',(ROOT/'dag/operads/index.json').read_bytes())
for name,dest in [('dynamics_exact.py','code/python/src/qm/dynamics_exact.py'),('dynamics_exact.rs','code/rust/src/finite_probability/dynamics_exact.rs'),('dynamics_exact_replay.rs','code/rust/src/finite_probability/examples/dynamics_exact_replay.rs'),('dynamics_checker.py','dag/pfp/dynamics_checker.py'),('PromptDynamics.lean','lean4/PromptDynamics.lean'),('test_dynamics_exact.py','code/python/tests/test_dynamics_exact.py')]:put(ROOT/dest,(SRC/name).read_bytes())
p=ROOT/'code/rust/src/finite_probability/lib.rs';p.write_bytes(p.read_bytes()+b'\npub mod dynamics_exact;\n')
p=ROOT/'lean4/lakefile.lean';p.write_bytes(p.read_bytes().replace(b'    `PromptStructure,',b'    `PromptStructure,\n    `PromptDynamics,'))
subprocess.run([str(Path.home()/'.cargo/bin/rustfmt.exe'),'--edition','2021',str(ROOT/'code/rust/src/finite_probability/dynamics_exact.rs'),str(ROOT/'code/rust/src/finite_probability/examples/dynamics_exact_replay.rs')],check=True)
deps=[]
def visit(name):
    if name in deps:return
    p=ROOT/'lean4'/(name+'.lean')
    for line in re.findall(r'^import\s+([^\r\n]+)',p.read_text(),re.M):
        for child in line.split():
            if (ROOT/'lean4'/(child+'.lean')).is_file():visit(child)
    deps.append(name)
visit('PromptDynamics');put(BATCH/'lean_order.json',(json.dumps(deps,indent=2)+'\n').encode())
put(BATCH/'tools/setup.py',Path(__file__).read_bytes());put(BATCH/'tools/specs.py',(SRC/'specs.py').read_bytes())
t=(OLD/'tools/prepare.py').read_text();a=t.index('def G(');b=t.index("nodes=json.loads")
t=t[:a]+"from specs import S\n\n"+t[b:]
t=t.replace("sp=importlib.util.spec_from_file_location('producer',s.ROOT/'code/python/src/qm/structure_exact.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)","import importlib,types\npkg=types.ModuleType('batch_dynamics');pkg.__path__=[str(s.ROOT/'code/python/src/qm')];sys.modules['batch_dynamics']=pkg\nm=importlib.import_module('batch_dynamics.dynamics_exact')")
t=t.replace('structure_exact','dynamics_exact').replace('structure_checker','dynamics_checker').replace('PromptStructure','PromptDynamics').replace('independent-structure-','independent-dynamics-').replace("'structure_'+kind","'dynamics_'+kind").replace('range(10)','range(20)').replace('Q(sqrt2)','Q(sqrt5)').replace('Real.rpow only in the stated Lean equation','a real root only under the stated Lean hypotheses')
# Producer dependencies are part of the complete construction source set.
t=t.replace("build=['code/rust", "production+=['code/python/src/qm/structure_exact.py','code/rust/src/finite_probability/structure_exact.rs','dag/pfp/structure_checker.py',(BATCH/'tools/specs.py').relative_to(s.ROOT).as_posix()]\nbuild=['code/rust")
put(BATCH/'tools/prepare.py',t.encode())
put(BATCH/'tools/run.py',(OLD/'tools/run.py').read_bytes().replace(b'range(10)',b'range(20)'))
print(json.dumps({'batch':ID,'local_Lean_modules':len(deps)}))
