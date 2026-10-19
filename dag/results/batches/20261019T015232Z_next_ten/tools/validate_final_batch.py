"""Actual final-tree integration calls; refuses to overwrite each native receipt."""
import importlib.util,json,re,sys
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');BATCH=ROOT/'dag/results/batches/20261019T015232Z_next_ten';folder=BATCH/'review/final_integration'
sp=importlib.util.spec_from_file_location('native',BATCH/'native.py');n=importlib.util.module_from_spec(sp);sp.loader.exec_module(n)
sp=importlib.util.spec_from_file_location('audit',BATCH/'verify_batch.py');audit=importlib.util.module_from_spec(sp);sp.loader.exec_module(audit)
rows=json.loads((BATCH/'selection.json').read_bytes())['nodes'];sources=set();lean_order=[]
def visit(name):
    if name in lean_order:return
    p=ROOT/'lean4'/(name+'.lean')
    for line in re.findall(r'^import\s+([^\r\n]+)',p.read_text(),re.M):
        for child in line.split():
            if (ROOT/'lean4'/(child+'.lean')).is_file():visit(child)
    lean_order.append(name)
for node,(_,lean,_) in zip(rows,audit.NAMES):
    run=ROOT/node['run'];config=json.loads((run.parent.parent/'reviews'/audit.REVIEW/'config.json').read_bytes());sources.update(config['required_construction_sources']);visit(lean)
sources.update('lean4/'+name+'.lean' for name in lean_order);sources.add('code/rust/src/finite_probability/bell_separator_extension.rs');sources=sorted(ROOT/p for p in sources)
folder.mkdir(parents=True,exist_ok=True)
plan={'scope':'Fresh current source tree, distinct from historical per-attempt snapshots. Local exact gates, no whole-repository/hosted-CI claim.','source_pins':[{'path':p.relative_to(ROOT).as_posix(),'sha256':n.sha(p)} for p in sources],'lean_order':lean_order,'expected_Python_tests':46,'expected_project_kernel_anchors':50,'Mathlib_expected_git_rev':'0df444a360eaa60ab8c11dca51a86af692955474'}
plan_path=folder/'plan.json'
if plan_path.exists():
    if json.loads(plan_path.read_bytes())!=plan:raise ValueError('Final integration source plan changed')
else:plan_path.write_bytes((json.dumps(plan,indent=2)+'\n').encode())
def record(label,cmd,cwd=ROOT):
    if (folder/(label+'_receipt.json')).exists():
        receipt=json.loads((folder/(label+'_receipt.json')).read_bytes())
        if receipt['exit_code']!=0:raise ValueError('Recorded failed integration gate requires explicit repair: '+label)
        if receipt['argv']!=cmd:raise ValueError('Resume changed native command')
        print(json.dumps({'gate':label,'state':'previously terminal passed receipt retained'}),flush=True);return receipt
    r=n.record(folder,label,cmd,cwd=cwd,sources=sources);print(json.dumps({'gate':label,'exit_code':r['exit_code'],'seconds':r['seconds']}),flush=True)
    if r['exit_code']!=0:raise ValueError('Integration gate failed: '+label)
    return r
py=sys.executable;cargo=str(Path.home()/'.cargo/bin/cargo.exe');lean=str(Path.home()/'.elan/bin/lean.exe')
record('lean_version',[lean,'--version'],ROOT/'lean4')
record('Mathlib_rev',['git','-C',str(n.PACKAGES/'mathlib'),'rev-parse','HEAD'])
if (folder/'Mathlib_rev.stdout.log').read_text().strip()!=plan['Mathlib_expected_git_rev']:raise ValueError('Unexpected Mathlib revision')
for i,(name,_,_) in enumerate(audit.NAMES):
    test='rational_bell' if i==0 else 'cabello_frame' if i==2 else name
    record('python_'+name,[py,'-X','utf8','code/python/tests/test_'+test+'.py','-v'])
record('rust_library',[cargo,'test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib','--offline','--locked'])
for name in lean_order:record('lean_'+name,[lean,'-j','1','-o',str(n.LIB/(name+'.olean')),name+'.lean'],ROOT/'lean4')
record('structure',[py,'-X','utf8','dag/pfp/validate_prompts.py'])
record('protocol',[py,'-X','utf8','dag/pfp/test_staged_prompts.py','-v'])
for i,(_,name,_) in enumerate(audit.NAMES):
    anchors=audit.BELL_ANCHORS if i==0 else json.loads((ROOT/rows[i]['run']/'p0/profile.json').read_bytes())['lean_anchors'];audit.axiom_reports((folder/('lean_'+name+'.stdout.log')).read_text(),anchors)
total=0
for name,_,expected in audit.NAMES:
    match=re.search(r'Ran (\d+) tests[\s\S]*\bOK\s*$',(folder/('python_'+name+'.stderr.log')).read_text())
    if not match or int(match.group(1))!=expected:raise ValueError('Wrong final Python coverage')
    total+=int(match.group(1))
rust=re.search(r'test result: ok\. (\d+) passed; 0 failed',(folder/'rust_library.stdout.log').read_text())
if not rust:raise ValueError('Missing final Rust coverage')
result={'fresh_Python_tests':total,'fresh_Rust_library_tests':int(rust.group(1)),'fresh_project_kernel_anchors':50,'fresh_local_Lean_modules':len(lean_order),'scope':plan['scope']}
out=folder/'result.json'
if out.exists():
    if json.loads(out.read_bytes())!=result:raise ValueError('Result changed')
else:out.write_bytes((json.dumps(result,indent=2)+'\n').encode())
print(json.dumps(result),flush=True)
