"""Explicit staging and Git-index byte checks for the sealed owned artifacts."""
import hashlib,json,subprocess,tempfile
from pathlib import Path
BATCH=Path(__file__).resolve().parents[1];ROOT=next(p for p in BATCH.parents if (p/'dag/pfp/prepare_stage.py').is_file())
def git(*args,**kw):return subprocess.check_output(['git',*args],cwd=ROOT,**kw)
selection=json.loads((BATCH/'selection.json').read_bytes())
integration=json.loads((BATCH/'upstream/integration_head.json').read_bytes())
if git('rev-parse','HEAD',text=True).strip()!=integration['integrated_head']:raise ValueError('Integrated HEAD changed')
for parent in [selection['base_commit'],integration['upstream_commit']]:
    subprocess.run(['git','merge-base','--is-ancestor',parent,'HEAD'],cwd=ROOT,check=True)
if git('branch','--show-current',text=True).strip()!='codex/pfp-prompts-32-through-51':raise ValueError('Wrong branch')
if git('diff','--cached','--name-only'):raise ValueError('Existing staged changes')
pins=json.loads((BATCH/'manifest.json').read_bytes())['files'];paths={p['path'] for p in pins};paths.add((BATCH/'manifest.json').relative_to(ROOT).as_posix())
for p in pins:
    if hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()!=p['sha256']:raise ValueError('Changed sealed bytes '+p['path'])
changed=set(git('diff','--name-only',text=True).splitlines())
if not changed<=paths:raise ValueError('Unexpected tracked modifications '+repr(changed-paths))
if any(p.startswith('dag/prompts/') for p in changed):raise ValueError('Original prompts changed')
with tempfile.NamedTemporaryFile(delete=False,suffix='.paths') as f:
    f.write(b'\0'.join(p.encode() for p in sorted(paths))+b'\0');plan=Path(f.name)
try:subprocess.run(['git','add','--force','--pathspec-from-file='+str(plan),'--pathspec-file-nul'],cwd=ROOT,check=True)
finally:plan.unlink()
staged=set(git('diff','--cached','--name-only',text=True).splitlines())
if not staged<=paths:raise ValueError('Unexpected staged paths')
# Inspect the exact index blobs, including snapshots/logs governed by -text.
ordered=sorted(paths);result=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=''.join(':'+p+'\n' for p in ordered).encode(),stdout=subprocess.PIPE,check=True).stdout
at=0
for path in ordered:
    end=result.index(b'\n',at);header=result[at:end].split();size=int(header[-1]);blob=result[end+1:end+1+size];at=end+size+2
    if hashlib.sha256(blob).digest()!=hashlib.sha256((ROOT/path).read_bytes()).digest():raise ValueError('Git index changed bytes '+path)
subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
print(json.dumps({'sealed_paths_byte_verified_in_Git_index':len(paths),'staged_changed_paths':len(staged),'base_commit':selection['base_commit']}))
