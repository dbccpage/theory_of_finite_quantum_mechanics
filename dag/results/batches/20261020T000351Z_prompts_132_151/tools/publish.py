"""Publish only sealed reviewed files, preserving disjoint upstream successors."""
import hashlib,json,subprocess
from datetime import datetime,timezone
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=next(p for p in B.parents if (p/'dag/pfp/prepare_stage.py').is_file());BRANCH='codex/pfp-prompts-132-through-151'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args,input=None):return subprocess.check_output(['git',*args],cwd=ROOT,input=input)
def rel(p):return p.relative_to(ROOT).as_posix()
def load(p):return json.loads(p.read_bytes())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def sealed():
 m=load(B/'manifest.json')
 for pin in m['files']:
  if sha(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Seal drift '+pin['path'])
 return m

def main():
 if git('branch','--show-current').decode().strip()!=BRANCH or git('diff','--cached','--name-only'):raise ValueError('Unexpected branch/index')
 m=sealed();execution=load(B/'selection.json')['base_commit'];head=git('rev-parse','HEAD').decode().strip();adoptions=[]
 if head!=execution:raise ValueError('Unexpected initial publication parent')
 while True:
  git('fetch','origin','main');remote=git('rev-parse','origin/main').decode().strip()
  if head==remote:break
  owned={p['path'] for p in m['files']}|{rel(B/'manifest.json')};changed=[p.decode() for p in git('diff','--name-only','-z',head,remote).split(b'\0') if p]
  if set(changed)&owned or any(p.startswith(('.agents/','rules/','dag/','lean4/','code/python/','code/rust/src/finite_probability/','code/rust/src/qm/','docs/','scripts/')) or Path(p).name.lower() in ('agents.md','scoring.md') or p in ('code/rust/Cargo.toml','code/rust/Cargo.lock') for p in changed):raise ValueError('Upstream source/build/instruction overlap requires substantive review')
  git('merge-base','--is-ancestor',head,remote);archive=B/'review/publication_upstream'/str(len(adoptions)+1)
  for name in ['manifest.json','summary.json','README.md']:
   target=archive/name;target.parent.mkdir(parents=True,exist_ok=True)
   if target.exists():raise ValueError('Prior adoption archive exists')
   target.write_bytes((B/name).read_bytes())
  git('merge','--ff-only','origin/main')
  for pin in m['files']:
   if sha(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Sealed bytes changed across fast-forward')
  adoptions.append({'previous_parent':head,'delivery_parent':remote,'changed_paths':changed,'owned_overlap':[],'unchanged_sealed_files':len(m['files']),'adopted_utc':datetime.now(timezone.utc).isoformat(),'integration_reuse':'All sealed source/build/native/kernel/candidate/review bytes unchanged; no DAG, Lean, Python, finite-probability, workspace/lock or instruction changes. No validation claim about independent upstream work.'});head=remote
  with (B/'README.md').open('ab') as f:f.write(('\nPublication adopted disjoint upstream '+remote+' ('+str(len(changed))+' changed paths) after proving all '+str(len(m['files']))+' sealed files unchanged. Earlier seal/report retained under review/publication_upstream. Native integration is reused only on this exact byte basis.\n').encode())
  # Report-only bytes change; all stage, code and mathematical evidence stays frozen.
  write(B/'delivery_base.json',{'execution_base':execution,'delivery_base':head,'adoptions':adoptions});s=load(B/'summary.json');s['delivery_base']=head;s['upstream_adoptions']=len(adoptions);write(B/'summary.json',s)
  paths={ROOT/p['path'] for p in m['files']};paths.update(p for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts);paths.discard(B/'manifest.json');write(B/'manifest.json',{'scope':'Final owned seal after explicit disjoint upstream adoption; prior seals retained; excludes itself.','files':[{'path':rel(p),'sha256':sha(p)} for p in sorted(paths)]});m=sealed()
 if not (B/'delivery_base.json').exists():
  write(B/'delivery_base.json',{'execution_base':execution,'delivery_base':head,'adoptions':[]});m['files'].append({'path':rel(B/'delivery_base.json'),'sha256':sha(B/'delivery_base.json')});m['files']=sorted(m['files'],key=lambda p:p['path']);write(B/'manifest.json',m);m=sealed()
 owned={p['path'] for p in m['files']}|{rel(B/'manifest.json')}
 for status in git('status','--porcelain=v1','-z','--untracked-files=all').split(b'\0'):
  if status and (status[:2] not in (b' M',b'??') or status[3:].decode() not in owned):raise ValueError('Unowned/index mutation')
 git('add','--pathspec-from-file=-','--pathspec-file-nul',input=b'\0'.join(p.encode() for p in sorted(owned))+b'\0')
 staged={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}
 if not staged or not staged<=owned:raise ValueError('Staged scope')
 ids={}
 for entry in git('ls-files','--stage','-z').split(b'\0'):
  if entry:
   meta,path=entry.split(b'\t',1)
   if path.decode() in owned:ids[path.decode()]=meta.split()[1].decode()
 if set(ids)!=owned:raise ValueError('Untracked sealed evidence')
 names=sorted(owned);raw=git('cat-file','--batch',input=('\n'.join(ids[p] for p in names)+'\n').encode());pos=0
 for name in names:
  end=raw.index(b'\n',pos);size=int(raw[pos:end].split()[-1]);pos=end+1;data=raw[pos:pos+size];pos+=size+1
  if data!=(ROOT/name).read_bytes():raise ValueError('Index bytes differ '+name)
 git('diff','--cached','--check');tree=git('write-tree').decode().strip();print(json.dumps({'staged_files':len(staged),'all_owned_blobs_verified':len(owned),'reviewed_tree':tree,'delivery_base':head}),flush=True)
 subprocess.run(['git','commit','--quiet','-m','Run PFP prompts 132-151 with exact Born-boundary operad evidence'],cwd=ROOT,check=True);commit=git('rev-parse','HEAD').decode().strip()
 if git('rev-parse','HEAD^{tree}').decode().strip()!=tree or git('status','--porcelain') or git('config','--get','core.bare').decode().strip()!='false':raise ValueError('Postcommit tree/state drift')
 subprocess.run(['git','push','--set-upstream','origin',BRANCH],cwd=ROOT,check=True)
 url=subprocess.check_output(['gh','pr','create','--base','main','--head',BRANCH,'--title','Run PFP prompts 132-151 with exact Born-boundary operad evidence','--body-file',str(B/'review/pr_body.md')],cwd=ROOT,text=True).strip();print(json.dumps({'pr_url':url,'head':commit,'reviewed_tree':tree,'delivery_base':head}),flush=True)
if __name__=='__main__':main()
