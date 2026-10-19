"""Finish the corrected baseline audit; reuse only unchanged passing native gates.

No receipt is relabeled as a new compiler execution. The prior actual compilation
on the integrated tree remains authoritative only for its exact source bytes.
"""
import importlib.util,json,re,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
ROOT=s.ROOT;OLD=B/'review/final_integration_after_baseline_review';OUT=B/'review/final_integration_complete'
receipts=[]
for p in sorted(OLD.glob('*_receipt.json')):
    r=json.loads(p.read_bytes())
    if r['exit_code']!=0:continue
    if not r['sources_unchanged']:raise ValueError('Invalid passing receipt')
    for pin in r['source_pins']:
        if s.sha(Path(pin['path']))!=pin['sha256']:raise ValueError('Changed source prevents receipt reuse: '+pin['path'])
    receipts.append({'path':p.relative_to(ROOT).as_posix(),'sha256':s.sha(p),'scope':'Prior actual passing native call on the integrated source tree, with every recorded source digest rechecked now.'})
required={'lean_final','rust_library'}|{'lean_dependency_'+name for name in json.loads((B/'lean_order.json').read_bytes())[:-1]}
if not required<={Path(p['path']).name.removesuffix('_receipt.json') for p in receipts}:raise ValueError('Incomplete native gate reuse')
s.save(OUT/'reused_native_receipts.json',{'receipts':receipts,'scope':'These are references to the prior actual compilation/test invocations, not new invocations.'})
rows=json.loads((B/'selection.json').read_bytes())['nodes'];first=ROOT/rows[0]['run'];a=json.loads((first/'accepted.json').read_bytes())['attempt'];candidate=json.loads((first/a/'candidate.json').read_bytes())
sources=[ROOT/p['path'].split('/'+a+'/construction/',1)[1] for p in candidate['source_pins']]+[Path(__file__),B/'tools/check_upstream_baseline_complete.py',B/'verify_batch.py',B/'test_custody_guards.py']
def record(name,args):
    r=s.native.record(OUT,name,args,cwd=ROOT,sources=sources);print(json.dumps({'gate':name,'exit_code':r['exit_code'],'seconds':r['seconds']}),flush=True)
    if r['exit_code']!=0:raise ValueError('Actual final audit failed: '+name)
py=sys.executable
record('complete_upstream_baseline',[py,'-X','utf8',str(B/'tools/check_upstream_baseline_complete.py')])
for optimized,label in [(False,'normal'),(True,'optimized')]:
    opts=[py,'-X','utf8']+(['-O'] if optimized else [])
    record('guards_'+label,opts+[str(B/'test_custody_guards.py'),'-v'])
    record('replay_'+label,opts+[str(B/'verify_batch.py')])
sys.path.insert(0,str(B));import verify_batch as audit
anchors={x for row in rows for x in json.loads((ROOT/row['run']/'p0/profile.json').read_bytes())['lean_anchors']};audit.axiom_reports((OLD/'lean_final.stdout.log').read_text(),anchors)
def count(p):
    m=re.search(r'Ran (\d+) tests[\s\S]*\bOK\s*$',p.read_text())
    if not m:raise ValueError('Missing actual passed test count '+str(p))
    return int(m.group(1))
python=sum(count(p) for p in OLD.glob('test_*.stderr.log'));rust=re.search(r'test result: ok\. (\d+) passed; 0 failed',(OLD/'rust_library.stdout.log').read_text())
if not rust:raise ValueError('Missing actual Rust count')
if (OUT/'replay_normal.stdout.log').read_bytes()!=(OUT/'replay_optimized.stdout.log').read_bytes():raise ValueError('Optimized replay differs')
result={'fresh_targeted_Python_tests':python,'fresh_Rust_library_tests':int(rust.group(1)),'unique_new_kernel_anchors':len(anchors),'fresh_local_Lean_modules':len(json.loads((B/'lean_order.json').read_bytes())),'custody_regressions_per_mode':count(OUT/'guards_normal.stderr.log'),'modes':['normal','Python -O'],'global_structure_and_protocol_baseline':json.loads((B/'review/upstream_baseline_comparison_complete_sources/result.json').read_bytes()),'reused_passing_native_receipts':(OUT/'reused_native_receipts.json').relative_to(ROOT).as_posix(),'scope':'Actual fresh native gates on the integrated tree, reused only after all recorded source digests matched. New complete upstream comparison and custody replays ran here. No full global success; no fresh full Mathlib or transitive dependency custody.'}
s.save(OUT/'result.json',result);print(json.dumps(result),flush=True)
