"""Fresh local native integration; every failed invocation remains recorded."""
import importlib.util,json,re,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
folder=B/'review/final_integration';rows=json.loads((B/'selection.json').read_bytes())['nodes'];first=s.ROOT/rows[0]['run'];accepted=json.loads((first/'accepted.json').read_bytes());a=accepted['attempt'];c=json.loads((first/a/'candidate.json').read_bytes())
sources=[s.ROOT/p['path'].split('/'+a+'/construction/',1)[1] for p in c['source_pins']]+[Path(__file__),B/'verify_batch.py',B/'test_custody_guards.py',B/'tools/review.py']
def record(name,argv,cwd=s.ROOT):
    rp=folder/(name+'_receipt.json')
    if rp.exists():
        r=json.loads(rp.read_bytes())
        if r['exit_code']:raise ValueError('Retained failed gate: '+name)
        for pin in r['source_pins']:
            if s.sha(Path(pin['path']))!=pin['sha256']:raise ValueError('Receipt source drift '+name)
    else:r=s.native.record(folder,name,argv,cwd=cwd,sources=sources)
    print(json.dumps({'gate':name,'exit_code':r['exit_code'],'seconds':r['seconds']}),flush=True)
    if r['exit_code']:raise ValueError('Actual integration failure '+name)
py=sys.executable;cargo=str(Path.home()/'.cargo/bin/cargo.exe');lean=str(Path.home()/'.elan/bin/lean.exe')
record('lean_version',[lean,'--version'],s.ROOT/'lean4');record('rust_version',[cargo,'--version'])
record('mathlib_rev',['git','-C',str(s.native.PACKAGES/'mathlib'),'rev-parse','HEAD'])
tests={'code/python/tests/test_rational_bell.py','code/python/tests/test_phase_scope.py','code/python/tests/test_structure_exact.py','code/python/tests/test_dynamics_exact.py','code/python/tests/test_resources_exact.py'}
for batch in ['20261019T015232Z_next_ten','20261019T145000Z_prompts_12_21','20261019T160201Z_prompts_22_31','20261019T164251Z_prompts_32_51']:
    old=s.ROOT/'dag/results/batches'/batch
    for row in json.loads((old/'selection.json').read_bytes())['nodes']:
        p=s.ROOT/row['run']/'p0/profile.json'
        if p.is_file():tests.add(json.loads(p.read_bytes())['python_test'])
for test in sorted(tests):record(Path(test).stem,[py,'-X','utf8',test,'-v'])
record('rust_library',[cargo,'test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib','--offline','--locked'])
for name in json.loads((B/'lean_order.json').read_bytes()):record('lean_'+name,[lean,'-j','1','-o',str(s.native.LIB/(name+'.olean')),name+'.lean'],s.ROOT/'lean4')
for optimized,label in [(False,'normal'),(True,'optimized')]:
    opts=[py,'-X','utf8']+(['-O'] if optimized else [])
    for name,path in [('prompt_validator','dag/pfp/validate_prompts.py'),('protocol','dag/pfp/test_staged_prompts.py'),('filename_custody','dag/pfp/test_custody.py'),('guards',str(B/'test_custody_guards.py')),('replay',str(B/'verify_batch.py'))]:
        record(name+'_'+label,opts+[path]+(['-v'] if name in ('protocol','filename_custody','guards') else []))
sys.path.insert(0,str(B));import verify_batch as audit
all_anchors={'QuantumMechanics.PromptResources.'+n for n in re.findall(r'^theorem (\w+)',(s.ROOT/'lean4/PromptResources.lean').read_text(),re.M)}
audit.axiom_reports((folder/'lean_PromptResources.stdout.log').read_text(),all_anchors)
def count(path):
    m=re.search(r'Ran (\d+) tests[\s\S]*\bOK\s*$',path.read_text())
    if not m:raise ValueError('No test execution count '+str(path))
    return int(m.group(1))
r=re.search(r'test result: ok\. (\d+) passed; 0 failed',(folder/'rust_library.stdout.log').read_text())
if not r:raise ValueError('No Rust test count')
if (folder/'mathlib_rev.stdout.log').read_text().strip()!='0df444a360eaa60ab8c11dca51a86af692955474':raise ValueError('Mathlib revision drift')
if (folder/'replay_normal.stdout.log').read_bytes()!=(folder/'replay_optimized.stdout.log').read_bytes():raise ValueError('Optimized replay differs')
result={'targeted_unique_Python_tests':sum(count(folder/(Path(t).stem+'.stderr.log')) for t in tests),'Rust_library_tests':int(r.group(1)),'fresh_local_Lean_modules':len(json.loads((B/'lean_order.json').read_bytes())),'new_kernel_theorems_in_module':len(all_anchors),'protocol_tests_per_mode':count(folder/'protocol_normal.stderr.log'),'filename_custody_tests_per_mode':count(folder/'filename_custody_normal.stderr.log'),'batch_guard_tests_per_mode':count(folder/'guards_normal.stderr.log'),'modes':['normal','Python -O'],'corpus_prompts':177,'scope':'Targeted local integration and live corpus/protocol validation. Cached pinned Mathlib imported; no full Mathlib, transitive-dependency, whole-repository or hosted-CI claim.'}
s.save(folder/'result.json',result);print(json.dumps(result),flush=True)
