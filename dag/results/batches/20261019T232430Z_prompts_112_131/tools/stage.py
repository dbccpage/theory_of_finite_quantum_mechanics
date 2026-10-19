"""Guarded explicit-path staging with exact staged Git blob verification."""
import hashlib,json,subprocess
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=next(p for p in B.parents if (p/'dag/pfp/prepare_stage.py').is_file())
def git(*args,input=None):return subprocess.check_output(['git',*args],cwd=ROOT,input=input)
selection=json.loads((B/'selection.json').read_bytes());base=selection['base_commit']
if git('branch','--show-current').decode().strip()!='codex/pfp-prompts-112-through-131':raise ValueError('Branch drift')
if git('rev-parse','HEAD').decode().strip()!=base:raise ValueError('Local base drift')
git('fetch','origin','main')
if git('rev-parse','origin/main').decode().strip()!=base:raise ValueError('Upstream advanced; inspect disjointness before delivery')
manifest=json.loads((B/'manifest.json').read_bytes());owned={p['path'] for p in manifest['files']}|{(B/'manifest.json').relative_to(ROOT).as_posix()}
for pin in manifest['files']:
 if hashlib.sha256((ROOT/pin['path']).read_bytes()).hexdigest()!=pin['sha256']:raise ValueError('Sealed file drift '+pin['path'])
status=git('status','--porcelain=v1','-z','--untracked-files=all').split(b'\0');changed=[]
for raw in status:
 if not raw:continue
 if raw[:2] not in (b' M',b'??'):raise ValueError('Unexpected index state '+repr(raw[:2]))
 name=raw[3:].decode()
 if name not in owned:raise ValueError('Unowned changed path '+name)
 changed.append(name)
if not changed:raise ValueError('No changes')
git('add','--pathspec-from-file=-','--pathspec-file-nul',input=b'\0'.join(p.encode() for p in changed)+b'\0')
staged=git('diff','--cached','--name-only','-z').split(b'\0');names=[p.decode() for p in staged if p]
if set(names)!=set(changed):raise ValueError('Staged path drift')
entries=git('ls-files','--stage','-z').split(b'\0');oids={}
for e in entries:
 if not e:continue
 meta,p=e.split(b'\t',1);name=p.decode()
 if name in changed:oids[name]=meta.split()[1].decode()
raw=git('cat-file','--batch',input=('\n'.join(oids[n] for n in names)+'\n').encode());pos=0
for name in names:
 end=raw.index(b'\n',pos);header=raw[pos:end].split();size=int(header[-1]);pos=end+1;content=raw[pos:pos+size];pos+=size+1
 if content!=(ROOT/name).read_bytes():raise ValueError('Staged byte mismatch '+name)
git('diff','--cached','--check')
print(json.dumps({'staged_files':len(names),'tree':git('write-tree').decode().strip(),'base':base}),flush=True)
