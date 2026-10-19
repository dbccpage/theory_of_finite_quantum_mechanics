"""Run unmodified global checks on exact upstream and current trees; reject regressions.

A successful comparison is not a successful global validator or protocol suite.
Actual failures, logs, source bytes and the checkout policy are retained.
"""
import contextlib,hashlib,importlib.util,io,json,os,subprocess,sys,tempfile,unittest,zipfile,yaml
from pathlib import Path
sys.dont_write_bytecode=True
DRIVER_SHA=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
B=Path(__file__).resolve().parents[1];ROOT=next(p for p in B.parents if (p/'dag/pfp/prepare_stage.py').is_file());OUT=B/'review/upstream_baseline_comparison_complete_sources';UP=json.loads((B/'upstream/reconciliation_plan.json').read_bytes())['upstream_commit']
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('Refuse overwrite '+str(p))
    p.write_bytes(b)
def save(p,data):put(p,(json.dumps(data,indent=2)+'\n').encode())
def module(path,name):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def check(root,label):
    validate=module(root/'dag/pfp/validate_prompts.py','baseline_validator_'+label);structure=validate.validate();save(OUT/(label+'_structure.json'),structure)
    protocol=module(root/'dag/pfp/test_staged_prompts.py','protocol_probe');log=io.StringIO()
    with contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(protocol))
    put(OUT/(label+'_protocol.log'),log.getvalue().encode())
    def failures(rows):return [{'test':test.id(),'traceback':message.replace(str(root),'$ROOT')} for test,message in rows]
    data={'tests_run':result.testsRun,'failures':failures(result.failures),'errors':failures(result.errors),'skipped':[(t.id(),r) for t,r in result.skipped],'scope':'Actual unmodified global protocol suite; errors and failures retained, not waived.'};save(OUT/(label+'_protocol.json'),data)
    return structure,data
with tempfile.TemporaryDirectory(prefix='pfp_upstream_') as temp:
    temp=Path(temp).resolve();checkout=temp/'source';checkout.mkdir();index=temp/'git.index';env=dict(os.environ,GIT_INDEX_FILE=str(index))
    subprocess.run(['git','read-tree',UP],cwd=ROOT,env=env,check=True)
    tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',UP],cwd=ROOT,text=True).splitlines();paths={p for p in tracked if p=='.gitattributes' or p.startswith(('dag/prompts/','dag/operads/','dag/pfp/','dag/derivations/','lean4/'))}
    tracked_set=set(tracked)
    # Include every local binding, including code and historical Bell snapshots.
    index_data=json.loads(subprocess.check_output(['git','show',UP+':dag/operads/index.json'],cwd=ROOT))
    for row in index_data['nodes']:
        record=yaml.safe_load(subprocess.check_output(['git','show',UP+':'+row['operad_collection']],cwd=ROOT))
        for source in record['source_bindings']:
            if source['availability']=='local' and source['path'] in tracked_set:paths.add(source['path'])
    paths=sorted(paths)
    # Every checkout target is anchored below the fresh temporary directory.
    for name in paths:
        if checkout.resolve() not in (checkout/name).resolve().parents:raise ValueError('Escaping archive path')
    prefix=str(checkout).replace('\\','/')+'/'
    subprocess.run(['git','checkout-index','--force','--prefix='+prefix,'-z','--stdin'],cwd=ROOT,env=env,input=b'\0'.join(p.encode() for p in paths)+b'\0',check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    archive=B/'upstream/global_check_source_complete.zip'
    if archive.exists():raise ValueError('Refuse archive overwrite')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(checkout.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(checkout).as_posix())
    save(OUT/'baseline_source.json',{'commit':UP,'archive':archive.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'files':len(paths),'checkout_policy':'Alternate Git index at the pinned upstream commit; checkout-index applies this repository configuration and attributes, with no changes to the live index or tracked worktree.'})
    before,protocol_before=check(checkout,'upstream');after,protocol_after=check(ROOT,'current')
    if before!=after:raise ValueError('Global structure regression or unmatched baseline; inspect retained JSON')
    # Compare failure/error identities, normalized tracebacks and actual test coverage.
    if protocol_before!=protocol_after:raise ValueError('Protocol regression or unmatched baseline; inspect retained actual outputs')
    if hashlib.sha256(Path(__file__).read_bytes()).hexdigest()!=DRIVER_SHA:raise ValueError('Comparison driver changed during execution')
    result={'comparison_driver_sha256':DRIVER_SHA,'upstream_commit':UP,'new_structure_errors':0,'known_upstream_structure_errors':len(before['errors']),'structure_prompts':before['prompts'],'protocol_tests_run':protocol_after['tests_run'],'known_upstream_protocol_failures':[r['test'] for r in protocol_after['failures']],'known_upstream_protocol_errors':[r['test'] for r in protocol_after['errors']],'new_protocol_failures':0,'status':'No new global check failures relative to exact upstream; full global checks remain failing.','scope':'Targeted batch native/kernel acceptance is separate from this baseline comparison.'};save(OUT/'result.json',result);print(json.dumps(result),flush=True)
