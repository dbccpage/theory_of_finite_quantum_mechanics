from pathlib import Path
import argparse,datetime,hashlib,json,re,subprocess,tempfile,os,sys
B=Path(__file__).resolve().parents[1];ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def need(ok,message):
 if not ok:raise RuntimeError(message)
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def git(*args):
 r=subprocess.run(['git',*args],cwd=ROOT,capture_output=True);need(r.returncode==0,'git '+args[0]+' failed: '+r.stderr.decode('utf-8',errors='replace'));return r.stdout

def seal():
 r=subprocess.run([sys.executable,'-O','-B',str(B/'tools/verify_review.py'),'--repo',str(ROOT)],capture_output=True,text=True)
 need(r.returncode==0,r.stdout+r.stderr)
 (B/'verification/final_review_check.stdout.txt').write_text(r.stdout,encoding='utf-8')
 (B/'verification/final_review_check.stderr.txt').write_text(r.stderr,encoding='utf-8')
 check=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True)
 need(check.returncode==0,'Git whitespace check failed outside captured evidence')
 save(B/'verification/git_diff_check.json',{'argv':['git','diff','--check'],'exit_code':check.returncode,'stdout':check.stdout.decode(),'stderr':check.stderr.decode(),'scope':'Raw captured research whitespace is exempt by .gitattributes; active authored whitespace is checked by verify_review.py.'})
 paths={e['path'] for e in load(B/'provenance.json')['publication_dependency_closure']}
 for p in B.rglob('*'):
  if p.is_file() and not p.is_relative_to(B/'build'):paths.add(str(p.relative_to(ROOT)).replace('\\','/'))
 index=ROOT/'dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/README.md'
 for p in [B/'manifest.json',B/'publication_paths.json',ROOT/'.gitattributes',index]:paths.add(str(p.relative_to(ROOT)).replace('\\','/'))
 save(B/'publication_paths.json',{'scope':'Only the complete sealed dependency closure, this focused audit, raw-byte Git policy, and mutable discovery index. Excludes transient builds and unsealed local leftovers.','paths':sorted(paths)})
 patterns=[r'sk-ant-[A-Za-z0-9_-]{20,}',r'gh[pousr]_[A-Za-z0-9]{30,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
 scanned=0
 for name in paths:
  p=ROOT/name
  if p==B/'manifest.json' and not p.exists():continue
  need(p.is_file(),'publication path missing: '+name)
  text=p.read_bytes().decode('utf-8',errors='ignore')
  need(not any(re.search(pattern,text) for pattern in patterns),'Potential credential literal found; values withheld')
  scanned+=1
 save(B/'verification/final_secret_scan.json',{'scope':'Recognizable provider/GitHub/private-key literals in enumerated publication inputs; not an exhaustive secret-detection guarantee.','files_checked':scanned,'matches':0})
 # The scan report itself is also part of this seal and publication inventory.
 paths.add(str((B/'verification/final_secret_scan.json').relative_to(ROOT)).replace('\\','/'))
 save(B/'publication_paths.json',{'scope':'Only sealed dependencies, focused audit, raw-byte Git policy and discovery index. Transient builds and unsealed leftovers excluded.','paths':sorted(paths)})
 files=[]
 for p in sorted(B.rglob('*')):
  if not p.is_file() or p==B/'manifest.json' or p.is_relative_to(B/'build'):continue
  need('__pycache__' not in p.parts,'Python cache appeared inside sealed evidence')
  files.append({'path':str(p.relative_to(B)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)})
 save(B/'manifest.json',{'schema_version':1,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files,'scope_exclusions':['manifest.json self-exclusion','build/ disposable compiled import products and local post-seal publication receipts'],'current_discovery_index':{'path':str(index.relative_to(ROOT)).replace('\\','/'),'sha256':sha(index)},'repository_byte_policy':{'path':'.gitattributes','sha256':sha(ROOT/'.gitattributes')},'authority_effect':'None'})
 verify_seal();print(json.dumps({'status':'SEALED','review_files':len(files),'publication_paths':len(paths),'manifest_sha256':sha(B/'manifest.json')},indent=2))

def verify_seal():
 m=load(B/'manifest.json')
 for e in m['files']:
  p=B/e['path'];need(p.is_file() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'review seal mismatch: '+e['path'])
 for key in ['current_discovery_index','repository_byte_policy']:
  need(sha(ROOT/m[key]['path'])==m[key]['sha256'],key+' changed')
 return m

def object_map(ref=None):
 raw=git('ls-tree','-r','-z',ref) if ref else git('ls-files','--stage','-z');result={}
 for entry in raw.split(b'\0'):
  if not entry:continue
  left,path=entry.split(b'\t',1);parts=left.split();oid=parts[2] if ref else parts[1]
  if not ref:need(parts[2]==b'0','Unmerged index entry')
  result[path.decode('utf-8')]=oid.decode()
 return result

def check_objects(ref=None):
 verify_seal();paths=load(B/'publication_paths.json')['paths'];mapping=object_map(ref);ids=[]
 for name in paths:
  need(name in mapping,'Git object missing: '+name);ids.append(mapping[name])
 proc=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=('\n'.join(ids)+'\n').encode(),capture_output=True);need(proc.returncode==0,'Cannot read Git objects')
 offset=0
 for name,oid in zip(paths,ids):
  end=proc.stdout.index(b'\n',offset);header=proc.stdout[offset:end].split();need(header[0].decode()==oid and header[1]==b'blob','Unexpected Git object');size=int(header[2]);offset=end+1;data=proc.stdout[offset:offset+size];offset+=size+1
  need(len(data)==size and hashlib.sha256(data).hexdigest()==sha(ROOT/name),'Git changed sealed publication bytes: '+name)
 need(offset==len(proc.stdout),'Unexpected Git batch output')
 if not ref:
  changed=set(n.decode() for n in git('diff','--cached','--name-only','-z').split(b'\0') if n)
  need(changed==set(paths),'Staged path set differs from reviewed inventory')
 return {'status':'PASS_EXACT_GIT_BYTES','ref':ref or 'INDEX','paths':len(paths),'tree':git('rev-parse',ref+'^{tree}').decode().strip() if ref else git('write-tree').decode().strip(),'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}

def stage():
 verify_seal();paths=load(B/'publication_paths.json')['paths']
 fd,name=tempfile.mkstemp(prefix='finiteqm_publication_paths_',suffix='.nul');os.close(fd);p=Path(name)
 try:
  p.write_bytes(b'\0'.join(s.encode('utf-8') for s in paths)+b'\0')
  git('add','-f','--pathspec-from-file='+str(p),'--pathspec-file-nul')
 finally:p.unlink()
 git('diff','--cached','--check')
 result=check_objects();save(B/'build/staged_byte_receipt.json',result);print(json.dumps(result,indent=2))

def main():
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['seal','stage','check']);p.add_argument('--ref');a=p.parse_args()
 if a.mode=='seal':seal()
 elif a.mode=='stage':stage()
 else:
  result=check_objects(a.ref);save(B/'build'/('committed_byte_receipt.json' if a.ref else 'staged_byte_receipt.json'),result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()