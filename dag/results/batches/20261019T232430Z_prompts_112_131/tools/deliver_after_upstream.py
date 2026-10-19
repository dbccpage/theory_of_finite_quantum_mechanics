"""Retain a prior seal, adopt a disjoint upstream base, reseal and explicitly stage."""
import ast,hashlib,json,subprocess,sys,yaml
from datetime import datetime,timezone
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=next(p for p in B.parents if (p/'dag/pfp/prepare_stage.py').is_file())
def git(*args,input=None):return subprocess.check_output(['git',*args],cwd=ROOT,input=input)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def save(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():raise ValueError('Refusing overwrite '+str(p))
 p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def rewrite(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def prepare():
 selection=json.loads((B/'selection.json').read_bytes());base=selection['base_commit'];new=git('rev-parse','origin/main').decode().strip();manifest=json.loads((B/'manifest.json').read_bytes());owned={p['path'] for p in manifest['files']}|{rel(B/'manifest.json')}
 if git('rev-parse','HEAD').decode().strip()!=base or git('diff','--cached','--name-only'):raise ValueError('Pre-adoption state drift')
 git('merge-base','--is-ancestor',base,new)
 names=[p.decode() for p in git('diff','--name-only','-z',base,new).split(b'\0') if p]
 if owned.intersection(names):raise ValueError('Upstream overlaps sealed paths')
 if any(p.startswith(('.agents/','rules/')) or Path(p).name.lower() in ('agents.md','scoring.md') for p in names):raise ValueError('Instruction change needs review')
 for p in manifest['files']:
  if sha(ROOT/p['path'])!=p['sha256']:raise ValueError('Pre-adoption seal drift')
 archive=B/'review/pre_upstream_merge'
 for name in ['manifest.json','summary.json','README.md','review/companion_records.json']:
  dst=archive/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((B/name).read_bytes())
 save(B/'review/upstream_advance/guard_stop.json',{'observed_command':['py','-3.9','-X','utf8',rel(B/'tools/stage.py')],'observed_exit_code':1,'observed_reason':'Upstream advanced; inspect disjointness before delivery','stage_script_sha256':sha(B/'tools/stage.py'),'base_at_stop':base,'upstream_at_stop':new,'index_unchanged':True,'source':'Recorded observation from the actual failed shell tool call; no invented runtime or timestamp.'})
 git('merge','--ff-only','origin/main')
 for p in manifest['files']:
  if sha(ROOT/p['path'])!=p['sha256']:raise ValueError('Post-adoption seal drift')
 save(B/'delivery_base.json',{'execution_base':base,'delivery_base':new,'adopted_utc':datetime.now(timezone.utc).isoformat(),'upstream_changed_paths':names,'sealed_owned_overlap':[],'sealed_owned_files_unchanged':len(manifest['files']),'math_integration_reuse':{'path':rel(B/'review/final_integration/result.json'),'sha256':sha(B/'review/final_integration/result.json'),'basis':'All previously sealed files, including every math source/build/request/certificate/native receipt and review, are byte-identical. Upstream changes are category/homology files plus attributes restricted to their snapshots; no instructions, DAG files, Python, Lean, finite-probability package or Cargo workspace/lock change.'},'scope':'Adopt the external category/homology merge without claiming its full validation as part of this PFP batch.'})
 # This new delivery helper receives its own triad, retaining the previous records.
 subject=Path(__file__).resolve();digest=sha(subject)
 for suffix in ('.contract.yaml','.score.yaml','.doc.yaml'):
  template=yaml.safe_load((B/('tools/stage.py'+suffix)).read_bytes());template.update(subject=rel(subject),source_sha256=digest)
  if suffix=='.contract.yaml':template['contract_urn']='urn:finite-qm:pfp:112-131:delivery-after-upstream';template['symbols']=[n.name for n in ast.parse(subject.read_text()).body if isinstance(n,ast.FunctionDef)]
  target=subject.with_name(subject.name+suffix)
  if target.exists():raise ValueError('Companion exists')
  target.write_bytes(yaml.safe_dump(template,sort_keys=False,allow_unicode=True,width=100).encode())
 cpath=B/'review/companion_records.json';c=json.loads(cpath.read_bytes());c['records'].append({'subject':rel(subject),'sha256':digest,'capability_level':'L2','engineering_grade':None,'companions':[rel(subject)+s for s in ('.contract.yaml','.score.yaml','.doc.yaml')]});c['subjects']+=1;c['companions']+=3;rewrite(cpath,c)
 summary=json.loads((B/'summary.json').read_bytes());summary['delivery_base']=new;summary['integration_reuse_receipt']={'path':rel(B/'delivery_base.json'),'sha256':sha(B/'delivery_base.json')};summary['upstream_guard_stops_retained']=1;rewrite(B/'summary.json',summary)
 with (B/'README.md').open('ab') as f:f.write(('\nPublication guard: main advanced from '+base+' to '+new+' with 14,634 disjoint category/homology paths. The original report and seal are retained in review/pre_upstream_merge. All '+str(len(manifest['files']))+' sealed files remained byte-identical across the fast-forward, so mathematical integration is reused by exact digest. No new claim about the upstream category/homology campaign is made. The execution base remains literal; delivery_base.json records the adopted parent.\n').encode())
 paths={ROOT/p['path'] for p in manifest['files']};paths.update(p for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts);paths.discard(B/'manifest.json')
 rewrite(B/'manifest.json',{'scope':'Final owned seal after disjoint upstream adoption; old seal retained. Manifest excludes itself.','files':[{'path':rel(p),'sha256':sha(p)} for p in sorted(paths)]})
 print(json.dumps({'adopted_parent':new,'unchanged_prior_sealed_files':len(manifest['files']),'final_sealed_files':len(paths),'subjects':c['subjects'],'companions':c['companions']}),flush=True)
def stage():
 base=json.loads((B/'delivery_base.json').read_bytes())['delivery_base'];manifest=json.loads((B/'manifest.json').read_bytes());owned={p['path'] for p in manifest['files']}|{rel(B/'manifest.json')}
 if git('branch','--show-current').decode().strip()!='codex/pfp-prompts-112-through-131' or git('rev-parse','HEAD').decode().strip()!=base:raise ValueError('Branch/base drift')
 git('fetch','origin','main')
 if git('rev-parse','origin/main').decode().strip()!=base:raise ValueError('Upstream advanced again')
 for p in manifest['files']:
  if sha(ROOT/p['path'])!=p['sha256']:raise ValueError('Sealed artifact changed')
 names=[]
 for raw in git('status','--porcelain=v1','-z','--untracked-files=all').split(b'\0'):
  if not raw:continue
  if raw[:2] not in (b' M',b'??') or raw[3:].decode() not in owned:raise ValueError('Unowned or staged change')
  names.append(raw[3:].decode())
 git('add','--pathspec-from-file=-','--pathspec-file-nul',input=b'\0'.join(p.encode() for p in names)+b'\0')
 staged=[p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p]
 if set(staged)!=set(names):raise ValueError('Staged coverage')
 wanted=set(names);ids={}
 for e in git('ls-files','--stage','-z').split(b'\0'):
  if e:
   m,p=e.split(b'\t',1)
   if p.decode() in wanted:ids[p.decode()]=m.split()[1].decode()
 raw=git('cat-file','--batch',input=('\n'.join(ids[n] for n in staged)+'\n').encode());pos=0
 for name in staged:
  end=raw.index(b'\n',pos);size=int(raw[pos:end].split()[-1]);pos=end+1;data=raw[pos:pos+size];pos+=size+1
  if data!=(ROOT/name).read_bytes():raise ValueError('Staged bytes differ '+name)
 git('diff','--cached','--check');print(json.dumps({'staged_files':len(names),'tree':git('write-tree').decode().strip(),'base':base}),flush=True)
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare()
 elif sys.argv[1]=='stage':stage()
 else:raise ValueError('Unknown mode')
