"""Fresh final-source native gates, separately from retained staged attempts."""
import importlib.util,json,re,sys
from pathlib import Path
BATCH=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('s',BATCH/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
folder=BATCH/'review/final_integration';rows=json.loads((BATCH/'selection.json').read_bytes())['nodes']
profile=json.loads((s.root_run(rows[0]['node_id'])/'p0/profile.json').read_bytes());accepted=json.loads((s.root_run(rows[0]['node_id'])/'accepted.json').read_bytes());source_names=[p['path'].split('/'+accepted['attempt']+'/construction/',1)[1] for p in json.loads((s.root_run(rows[0]['node_id'])/accepted['attempt']/'candidate.json').read_bytes())['source_pins']];sources=[s.ROOT/p for p in source_names]+[Path(__file__),BATCH/'review.py' if (BATCH/'review.py').exists() else BATCH/'tools/review.py',BATCH/'verify_batch.py',BATCH/'test_custody_guards.py']
def record(name,argv,cwd=s.ROOT):
    receipt=folder/(name+'_receipt.json')
    if receipt.exists():
        r=json.loads(receipt.read_bytes())
        if r['exit_code']!=0:raise ValueError('Retained failed integration gate: '+name)
    else:r=s.native.record(folder,name,argv,cwd=cwd,sources=sources)
    print(json.dumps({'gate':name,'exit_code':r['exit_code'],'seconds':r['seconds']}),flush=True)
    if r['exit_code']!=0:raise ValueError('Integration failure: '+name)
py=sys.executable;cargo=str(Path.home()/'.cargo/bin/cargo.exe');lean=str(Path.home()/'.elan/bin/lean.exe')
record('lean_version',[lean,'--version'],s.ROOT/'lean4')
record('mathlib_rev',['git','-C',str(s.native.PACKAGES/'mathlib'),'rev-parse','HEAD'])
record('rust_version',[cargo,'--version'])
old=s.ROOT/'dag/results/batches/20261019T015232Z_next_ten';tests=set()
for row in json.loads((old/'selection.json').read_bytes())['nodes']:
    p=s.ROOT/row['run']/'p0/profile.json'
    if p.is_file():tests.add(json.loads(p.read_bytes())['python_test'])
    elif row['node_id']=='FQ-BELL-RATIONAL-VIOLATION-14-5':tests.add('code/python/tests/test_rational_bell.py')
    else:raise ValueError('Unknown prior test mapping')
tests.add('code/python/tests/test_phase_scope.py');tests.add('code/python/tests/test_structure_exact.py');tests.add('code/python/tests/test_dynamics_exact.py')
for test in sorted(tests):record(Path(test).stem,[py,'-X','utf8',test,'-v'])
record('rust_library',[cargo,'test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib','--offline','--locked'])
for local in json.loads((BATCH/'lean_order.json').read_bytes())[:-1]:record('lean_dependency_'+local,[lean,'-j','1','-o',str(s.native.LIB/(local+'.olean')),local+'.lean'],s.ROOT/'lean4')
record('lean_final',[lean,'-j','1','-o',str(s.native.LIB/'PromptDynamics.olean'),'PromptDynamics.lean'],s.ROOT/'lean4')
record('structure',[py,'-X','utf8','dag/pfp/validate_prompts.py'])
record('protocol',[py,'-X','utf8','dag/pfp/test_staged_prompts.py','-v'])
for optimized,label in [(False,'normal'),(True,'optimized')]:
    opts=[py,'-X','utf8']+(['-O'] if optimized else [])
    record('guards_'+label,opts+[str(BATCH/'test_custody_guards.py'),'-v'])
    record('replay_'+label,opts+[str(BATCH/'verify_batch.py')])
sys.path.insert(0,str(BATCH));import verify_batch as audit
anchors={a for row in rows for a in json.loads((s.root_run(row['node_id'])/'p0/profile.json').read_bytes())['lean_anchors']}
audit.axiom_reports((folder/'lean_final.stdout.log').read_text(),anchors)
def tests_count(path):
    match=re.search(r'Ran (\d+) tests[\s\S]*\bOK\s*$',path.read_text());
    if not match:raise ValueError('No actual test count: '+str(path))
    return int(match.group(1))
python=sum(tests_count(folder/(Path(p).stem+'.stderr.log')) for p in tests)
rust=re.search(r'test result: ok\. (\d+) passed; 0 failed',(folder/'rust_library.stdout.log').read_text())
if not rust:raise ValueError('No actual Rust count')
if (folder/'mathlib_rev.stdout.log').read_text().strip()!='0df444a360eaa60ab8c11dca51a86af692955474':raise ValueError('Mathlib revision drift')
if (folder/'replay_normal.stdout.log').read_bytes()!=(folder/'replay_optimized.stdout.log').read_bytes():raise ValueError('Optimized exact replay differs')
result={'fresh_targeted_Python_tests':python,'fresh_Rust_library_tests':int(rust.group(1)),'unique_new_kernel_anchors':len(anchors),'fresh_local_Lean_modules':len(json.loads((BATCH/'lean_order.json').read_bytes())),'custody_regressions_per_mode':tests_count(folder/'guards_normal.stderr.log'),'modes':['normal','Python -O'],'scope':'Targeted local source integration; cached pinned Mathlib, not fresh full Mathlib or whole-repository/hosted CI. Twenty shared Python tests are unique, not counted twenty times.'}
s.save(folder/'result.json',result);print(json.dumps(result),flush=True)
