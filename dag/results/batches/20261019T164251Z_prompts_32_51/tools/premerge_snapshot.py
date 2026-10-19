"""Seal this batch before integrating a concurrent, explicitly pinned main update."""
import hashlib,json,subprocess,tempfile,yaml
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');B=ROOT/'dag/results/batches/20261019T164251Z_prompts_32_51'
UP='e5f7defe28e8a2f64273d5ffb157120ace83adee'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,data):
    if p.exists():raise ValueError('Refuse overwrite '+str(p))
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
def save(p,data):put(p,(json.dumps(data,indent=2)+'\n').encode())
sel=json.loads((B/'selection.json').read_bytes());before=json.loads((B/'index_before.json').read_bytes())
if git('rev-parse','HEAD').decode().strip()!=sel['base_commit']:raise ValueError('Unexpected premerge HEAD')
if git('diff','--cached','--name-only'):raise ValueError('Existing staged paths')
up_raw=git('show',UP+':dag/operads/index.json');up=json.loads(up_raw)
if [n['node_id'] for n in before['nodes']]!=[n['node_id'] for n in up['nodes']]:raise ValueError('Upstream node selection changed')
save(B/'upstream/index.json',up);mapping={}
for row in sel['nodes']:
    n=next(n for n in up['nodes'] if n['node_id']==row['node_id'])
    if any(row[k]!=n[k] for k in row if k not in ['prompt','operad_collection','position','run','original_target','status']):
        # Only path differences and this branch's own progress are expected.
        old=next(x for x in before['nodes'] if x['node_id']==row['node_id'])
        if any(old[k]!=n.get(k) for k in old if k not in ['prompt','operad_collection']):raise ValueError('Unreviewed upstream status change')
    raw=git('show',UP+':'+n['operad_collection']);p=B/'upstream/collections'/(row['node_id']+'.yaml');put(p,raw)
    old=yaml.safe_load((ROOT/row['run']/'inputs/this_repository'/row['operad_collection']).read_bytes());new=yaml.safe_load(raw)
    for k in ('source_statement','declared_assumptions','source_claim_label','statement_status'):
        if old['target'][k]!=new['target'][k]:raise ValueError('Changed mathematical target '+k)
    mapping[row['node_id']]={'old_prompt':row['prompt'],'prompt':n['prompt'],'old_operad_collection':row['operad_collection'],'operad_collection':n['operad_collection'],'upstream_collection_snapshot':p.relative_to(ROOT).as_posix(),'upstream_collection_sha256':sha(p),'upstream_collection_git_blob':git('rev-parse',UP+':'+n['operad_collection']).decode().strip()}
save(B/'upstream/reconciliation_plan.json',{'upstream_commit':UP,'captured_batch_base':sel['base_commit'],'upstream_index_git_blob':git('rev-parse',UP+':dag/operads/index.json').decode().strip(),'nodes':mapping,'policy':'Retain all original run/request/source bytes. Preserve the upstream path migration and dependency enhancements. Carry only this batch progress into the migrated canonical index and collections; rebuild and recheck final sources before merge.'})
put(B/'tools/premerge_snapshot.py',Path(__file__).read_bytes())
paths={ROOT/'dag/operads/index.json'}
for row in sel['nodes']:
    run=ROOT/row['run'];review=run.parent.parent/'reviews/20261019_dynamics_audit'
    paths.add(ROOT/row['operad_collection']);paths.add(run.parent.parent/'.gitattributes')
    for folder in (run,review):paths.update(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.olean','.ilean'))
    accepted=json.loads((run/'accepted.json').read_bytes());c=json.loads((run/accepted['attempt']/'candidate.json').read_bytes())
    paths.update(ROOT/p['path'].split('/'+accepted['attempt']+'/construction/',1)[1] for p in c['source_pins'])
paths.update(p for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.olean','.ilean'))
pins=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(paths)]
save(B/'premerge_manifest.json',{'scope':'Pre-integration checkpoint, not final-source acceptance. Original stage/review artifacts remain immutable; canonical paths and build dependencies may receive an explicitly recorded upstream successor.','files':pins});paths.add(B/'premerge_manifest.json')
names=sorted(p.relative_to(ROOT).as_posix() for p in paths)
changed=set(git('diff','--name-only').decode().splitlines())
if not changed<=set(names):raise ValueError('Unowned tracked changes '+repr(changed-set(names)))
with tempfile.NamedTemporaryFile(delete=False) as f:
    f.write(b'\0'.join(n.encode() for n in names)+b'\0');plan=Path(f.name)
try:subprocess.run(['git','add','--force','--pathspec-from-file='+str(plan),'--pathspec-file-nul'],cwd=ROOT,check=True)
finally:plan.unlink()
blobs=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=''.join(':'+n+'\n' for n in names).encode(),stdout=subprocess.PIPE,check=True).stdout;at=0
for name in names:
    end=blobs.index(b'\n',at);size=int(blobs[at:end].split()[-1]);blob=blobs[end+1:end+1+size];at=end+size+2
    if hashlib.sha256(blob).hexdigest()!=sha(ROOT/name):raise ValueError('Index byte conversion '+name)
subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
subprocess.run(['git','commit','--quiet','-m','Record twenty staged PFP runs and operads before upstream reconciliation'],cwd=ROOT,check=True)
print(json.dumps({'premerge_commit':git('rev-parse','HEAD').decode().strip(),'index_paths_verified':len(names),'upstream_commit':UP}))
