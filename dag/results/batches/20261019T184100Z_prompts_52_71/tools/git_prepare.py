"""Stage only owned, sealed bytes after fresh Git base/head inspection."""
import hashlib,json,subprocess
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=next(p for p in B.parents if (p/'dag/pfp/prepare_stage.py').is_file())
def git(*args,**kw):return subprocess.check_output(['git',*args],cwd=ROOT,**kw)
selection=json.loads((B/'selection.json').read_bytes());manifest=json.loads((B/'manifest.json').read_bytes());base=selection['base_commit'];branch=git('branch','--show-current',text=True).strip();head=git('rev-parse','HEAD',text=True).strip()
if branch!='codex/pfp-prompts-52-through-71' or head!=base:raise ValueError('Unexpected branch/base/head; inspect before Git write')
git('fetch','origin','main')
if git('rev-parse','origin/main',text=True).strip()!=base:raise ValueError('Upstream main advanced; integrate and revalidate first')
owned={p['path'] for p in manifest['files']}|{(B/'manifest.json').relative_to(ROOT).as_posix()}
for p in manifest['files']:
    if hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()!=p['sha256']:raise ValueError('Sealed source changed '+p['path'])
status=git('status','--porcelain=v1','-z','--untracked-files=all').split(b'\0')
changed=[]
for line in status:
    if not line:continue
    state=line[:2].decode();name=line[3:].decode().replace('\\','/')
    if state not in (' M','??'):raise ValueError('Unexpected index state '+repr(line))
    if name not in owned:raise ValueError('Unowned path '+name)
    changed.append(name)
git('add','--pathspec-from-file=-','--pathspec-file-nul',input=b'\0'.join(n.encode() for n in sorted(owned))+b'\0')
staged=git('diff','--cached','--name-only','-z').split(b'\0');names={n.decode() for n in staged if n}
if names!=set(changed):raise ValueError('Staged path coverage differs')
for name in sorted(names):
    sealed=git('show',':'+name)
    if sealed!=(ROOT/name).read_bytes():raise ValueError('Git attributes changed staged bytes '+name)
subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
print(json.dumps({'base_commit':base,'branch':branch,'staged_files':len(names),'staged_tree':git('write-tree',text=True).strip(),'staged_bytes_match_working_files':True}))
