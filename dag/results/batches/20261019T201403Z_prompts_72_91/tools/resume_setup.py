"""Account for the real upstream public-export change, then resume preparation."""
import hashlib,json,re,subprocess,sys,yaml
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');SRC=Path(__file__).resolve().parent
ID='20261019T201403Z_prompts_72_91';RUN='20261019T201403Z_staged';B=ROOT/'dag/results/batches'/ID
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('refuse overwrite '+str(p))
    p.write_bytes(b)
def sha(b):return hashlib.sha256(b).hexdigest()
path='code/rust/src/majorana/lib.rs';before=subprocess.check_output(['git','show','8065b3ad51e1c1475647102ce5bdf489486d8616:'+path],cwd=ROOT);after=(ROOT/path).read_bytes();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
if sha(before)!='52ae069258fd48e01024574bc1c0deeab5dbbbf54399cb618e394c43e374bcb3' or sha(after)!='79c6d2979fad71feaa154bc2f60df4771a7b0f3060b52b4cb124f7bb5be3edb9':raise ValueError('Unexpected source change')
pattern=rb'pub use\s+[\s\S]*?;'
outside=lambda b:b'\n'.join(line for line in re.sub(pattern,b'',b).splitlines() if line.strip())
if outside(before)!=outside(after):raise ValueError('Change outside public exports')
def exports(b):
    names=set()
    for module,body in re.findall(rb'pub use\s+([\w:]+)::\{([^}]*)\};',b):
        names.update(module.decode()+'::'+n.decode().strip() for n in body.split(b',') if n.strip())
    return names
old,new=exports(before),exports(after)
if not old<=new:raise ValueError('Existing exports removed')
for label,data in [('before',before),('after',after)]:put(B/'custody'/label/path,data)
receipt={'node_id':'DS-QM212-MAJORANA-PROBLEM','source_path':path,'historical_commit':'8065b3ad51e1c1475647102ce5bdf489486d8616','current_commit':head,'historical_sha256':sha(before),'current_sha256':sha(after),'historical_snapshot':(B/'custody/before'/path).relative_to(ROOT).as_posix(),'current_snapshot':(B/'custody/after'/path).relative_to(ROOT).as_posix(),'added_public_exports':sorted(new-old),'all_existing_exports_retained':True,'nonblank_bytes_outside_pub_use_blocks_identical':True,'scope':'Upstream PR83 changed the public-export facade. This refreshes one file-only source lead, preserving both source versions. No implementation, theorem or physical claim is revalidated by the metadata repair.','authority_effect':'None'}
rp=B/'custody/majorana_source_successor.json';put(rp,(json.dumps(receipt,indent=2)+'\n').encode())
cp=ROOT/'dag/operads/ds_qm212_majorana_problem.yaml';d=yaml.safe_load(cp.read_bytes());put(B/'custody/majorana_collection_before.yaml',cp.read_bytes())
bindings=[v for v in d['source_bindings'] if v.get('repository')=='this_repository' and v.get('path')==path]
if len(bindings)!=1 or bindings[0]['sha256']!=sha(before) or bindings[0]['declaration_status']!='file_only_no_symbol':raise ValueError('Unexpected binding')
bindings[0]['sha256']=sha(after);d.setdefault('source_pin_successors',[]).append({'path':path,'historical_sha256':sha(before),'current_sha256':sha(after),'review':rp.relative_to(ROOT).as_posix(),'role':'source_lead_only','authority_effect':'None'});cp.write_bytes(yaml.safe_dump(d,sort_keys=False,allow_unicode=True,width=100).encode())
put(B/'custody/initial_preparation_failure.json',(json.dumps({'stage':'P0 preparation before mathematical derivation','exit_code':1,'failure':'Unresolved source pin code/rust/src/majorana/lib.rs','source_change':'Upstream PR83 additive public exports; the actual refusal is retained, not treated as a passing stage.','partial_requests_preserved':14,'resolution':rp.relative_to(ROOT).as_posix()},indent=2)+'\n').encode())
# Keep the failed creation and request bytes, then create an explicit successor
# that resumes only matching existing requests/inventories/snapshots.
old_init=B/'tools/init.py';t=old_init.read_text()
t=t.replace("    if p.exists():\n        raise ValueError('Refusing overwrite: '+str(p))","    if p.exists():\n        if p.name=='request.json':return\n        if json.loads(p.read_bytes())!=value:raise ValueError('Existing preparation artifact differs '+str(p))\n        return")
t=t.replace("snapshot = run/'inputs'/repository/relative;snapshot.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(actual,snapshot)","snapshot = run/'inputs'/repository/relative;snapshot.parent.mkdir(parents=True,exist_ok=True)\n            if snapshot.exists():\n                if snapshot.read_bytes()!=actual.read_bytes():raise ValueError('Existing snapshot differs '+relative)\n            else:shutil.copyfile(actual,snapshot)")
put(B/'tools/init_after_source_review.py',t.encode());subprocess.run([sys.executable,'-X','utf8',str(B/'tools/init_after_source_review.py')],cwd=ROOT,check=True)
# Resume the unexecuted tail of the original creation driver using the same IDs.
setup=(SRC/'setup.py').read_text();tail=setup[setup.index("for name,dest in "):]
ns={'__file__':str(SRC/'setup.py'),'ROOT':ROOT,'SRC':SRC,'B':B,'OLD':ROOT/'dag/results/batches/20261019T184100Z_prompts_52_71','ID':ID,'RUN':RUN,'put':put,'re':re,'sys':sys,'json':json,'subprocess':subprocess,'importlib':__import__('importlib'),'Path':Path}
put(B/'index_before.json',(ROOT/'dag/operads/index.json').read_bytes());exec(compile(tail,str(SRC/'setup.py')+' resumed tail','exec'),ns)
put(B/'tools/resume_setup.py',Path(__file__).read_bytes())
