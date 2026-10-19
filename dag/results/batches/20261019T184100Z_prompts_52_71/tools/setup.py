"""Install fresh twenty-node source and request custody without old evidence edits."""
import json,re,sys,subprocess
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
SRC=Path(__file__).resolve().parent
ID='20261019T184100Z_prompts_52_71';RUN='20261019T184100Z_staged'
B=ROOT/'dag/results/batches'/ID;OLD=ROOT/'dag/results/batches/20261019T164251Z_prompts_32_51'
def put(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('refusing overwrite '+str(p))
    p.write_bytes(data)
put(B/'.gitattributes',b'* -text whitespace=-trailing-space,-blank-at-eof\n')
for name in ('native.py','target_stages.py'):
    put(B/name,(OLD/name).read_bytes().replace(b'20261019T164251Z_prompts_32_51',ID.encode()))
t=(OLD/'tools/init.py').read_text().replace('20261019T164251Z_prompts_32_51',ID).replace('20261019T164251Z_staged',RUN).replace('selected = nodes[31:51]','selected = nodes[51:71]').replace('positions 32 through 51 after the thirty-one completed nodes','positions 52 through 71 after the fifty-one completed nodes')
t=t.replace("index = ROOT/'dag/operads/index.json'","sys.path.insert(0,str(ROOT/'dag/pfp'))\nfrom custody import Custody\ncustody=Custody(ROOT)\nindex = ROOT/'dag/operads/index.json'")
old="record['actual_sha256']=sha(actual);record['matches_recorded_pin']=expected is None or expected==record['actual_sha256']"
new=old+"\n            if expected and not record['matches_recorded_pin']:\n                if not custody.matches('paper',relative,expected,name):raise ValueError('Unresolved source pin '+relative)\n                record['pin_resolution']='Explicit filename-custody migration; original expected digest retained'\n                record['custody_ledger_sha256']=sha(ROOT/'dag/pfp/filename_custody.json')"
t=t.replace(old,new)
put(B/'tools/init.py',t.encode());subprocess.run([sys.executable,'-X','utf8',str(B/'tools/init.py')],cwd=ROOT,check=True)
put(B/'index_before.json',(ROOT/'dag/operads/index.json').read_bytes())
for name,dest in [('resources_exact.py','code/python/src/qm/resources_exact.py'),('resources_exact.rs','code/rust/src/finite_probability/resources_exact.rs'),('resources_checker.py','dag/pfp/resources_checker.py'),('PromptResources.lean','lean4/PromptResources.lean'),('test_resources_exact.py','code/python/tests/test_resources_exact.py')]:put(ROOT/dest,(SRC/name).read_bytes())
p=ROOT/'code/rust/src/finite_probability/lib.rs';p.write_bytes(p.read_bytes()+b'\npub mod resources_exact;\n')
p=ROOT/'lean4/lakefile.lean';p.write_bytes(p.read_bytes().replace(b'    `PromptDynamics,',b'    `PromptDynamics,\n    `PromptResources,'))
lean=ROOT/'lean4/PromptResources.lean';text=lean.read_text();anchors=re.findall(r'^theorem (\w+)',text,re.M);lean.write_bytes((text+'\n'+'\n'.join('#print axioms QuantumMechanics.PromptResources.'+a for a in anchors)+'\n').encode())
put(ROOT/'code/rust/src/finite_probability/examples/resources_exact_replay.rs',(ROOT/'code/rust/src/finite_probability/examples/dynamics_exact_replay.rs').read_bytes().replace(b'dynamics_exact',b'resources_exact'))
put(B/'tools/specs.py',(SRC/'specs.py').read_bytes())
# Tests have actual mathematical inequalities/controls, not label acceptance.
sys.path.insert(0,str(SRC));from specs import S
p=ROOT/'code/rust/src/finite_probability/resources_exact.rs';text=p.read_text();text+='\n#[cfg(test)] mod tests { use super::*; fn run(k:&str,s:&[&str])->Vec<Q>{evaluate(k,&s.iter().map(|x|x.to_string()).collect::<Vec<_>>()).iter().map(|x|q(x)).collect()}\n'
checks={
 'projection':'assert_eq!(v[4],n(0));assert_ne!(v[6],v[7]);',
 'fiber':'assert_eq!(v[0],v[2]);assert_eq!(v[1],v[3]);assert_ne!(v[4],v[5]);',
 'buildability':'assert_eq!(v[5],n(1));',
 'interference':'assert_eq!(v[6],v[7]);assert_eq!(v[6],n(2));',
 'torsion':'assert_eq!(v[..4],[n(1),n(0),n(0),n(1)]);',
 'selector':'assert_eq!(v[6],v[9]);assert!(v[7].is_zero()&&v[8].is_zero());',
 'holonomy':'assert_eq!(v[6..8],v[8..10]);assert_eq!(v[12],v[13]);',
 'annex':'assert_eq!(v[3],n(0));assert_eq!(v[4],v[5]);assert!(v[9]<=v[8]);',
 'product':'assert_eq!(v[21],n(4)*sq(&v[22]));assert!(v[21]>n(0));',
 'witness':'assert_eq!(v[20],n(1));assert_eq!(v[22],v[23]);assert!(v[21]<=n(1)/n(2));',
 'qubit':'assert_eq!(v[0],v[4]);assert_ne!(v[14],v[15]);assert_eq!(v[16],n(1));',
 'bell_import':'assert!(v[16+32]<=n(4));assert_eq!(v[16+20..16+28],vec![n(0);8]);',
 'chsh':'assert!(v[20].abs()<=n(2));assert_eq!(v[21],n(2));',
 'nosignal':'assert_eq!(v[20..28],vec![n(0);8]);assert_ne!(v[33],n(0));',
 'trace_select':'assert_eq!(v[4],v[5]);assert_eq!(v[7],n(2)*&v[4]);',
 'dual':'assert_eq!(v[0],v[1]);assert_eq!(v[2],v[3]);',
 'monotone':'assert!(v[3]<=v[2]);assert_eq!(v[5],n(2)*&v[3]);',
 'stochastic':'assert!(v[7]<=v[6]);',
 'channel':'assert_eq!(v[20..24],[n(1),n(0),n(0),n(1)]);assert_eq!(&v[24]+&v[27],n(1));',
 'firewall':'assert_eq!(v[3],v[5]);assert_eq!(v[3],n(1));'}
for s in S:
    vals=','.join(json.dumps(v) for v in s['cases'][0]);k=s['kind'];text+=f'#[test] fn resources_{k}(){{let v=run("{k}",&[{vals}]);{checks[k]}}}\n'
text+='#[test] #[should_panic] fn resources_reject_invalid_kernel(){run("monotone",&["2","0","1","-1"]);}\n}\n';p.write_bytes(text.encode())
subprocess.run([str(Path.home()/'.cargo/bin/rustfmt.exe'),'--edition','2021',str(p),str(ROOT/'code/rust/src/finite_probability/examples/resources_exact_replay.rs')],check=True)
deps=[]
def visit(name):
    if name in deps:return
    p=ROOT/'lean4'/(name+'.lean')
    for line in re.findall(r'^import\s+([^\r\n]+)',p.read_text(),re.M):
        for child in line.split():
            if (ROOT/'lean4'/(child+'.lean')).is_file():visit(child)
    deps.append(name)
visit('PromptResources');put(B/'lean_order.json',(json.dumps(deps,indent=2)+'\n').encode())
t=(OLD/'tools/prepare.py').read_text();start=t.index("    if kind=='census':");end=t.index("    public=",start);t=t[:start]+t[end:]
t=t.replace("import importlib,types\npkg=types.ModuleType('batch_dynamics');pkg.__path__=[str(s.ROOT/'code/python/src/qm')];sys.modules['batch_dynamics']=pkg\nm=importlib.import_module('batch_dynamics.dynamics_exact')","mp=importlib.util.spec_from_file_location('resources_producer',s.ROOT/'code/python/src/qm/resources_exact.py');m=importlib.util.module_from_spec(mp);mp.loader.exec_module(m)")
t=t.replace('dynamics_exact','resources_exact').replace('dynamics_checker','resources_checker').replace('PromptDynamics','PromptResources').replace('independent-dynamics-','independent-resources-').replace("'dynamics_'+kind","'resources_'+kind")
t=t.replace("production+=['code/python/src/qm/structure_exact.py','code/rust/src/finite_probability/structure_exact.rs','dag/pfp/structure_checker.py',(BATCH/'tools/specs.py').relative_to(s.ROOT).as_posix()]","production += [(BATCH/'tools/specs.py').relative_to(s.ROOT).as_posix(),'dag/pfp/custody.py','dag/pfp/filename_custody.json']")
t=t.replace('Exact Z, Q, Q(i), Q(sqrt5); admitted a real root only under the stated Lean hypotheses','Exact Z, Q, Gaussian rational pairs and supplied Boolean fields')
put(B/'tools/prepare.py',t.encode());put(B/'tools/run.py',(OLD/'tools/run.py').read_bytes());put(B/'tools/setup.py',Path(__file__).read_bytes())
print(json.dumps({'batch':ID,'Lean_anchors':len(anchors),'local_Lean_modules':deps}))
