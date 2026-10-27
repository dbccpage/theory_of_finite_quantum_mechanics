"""Replay the supplemental real/normed uncertainty and correction census offline."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,subprocess,tempfile,sys
ROOT=Path(__file__).resolve().parents[1]
ALLOWED={'propext','Quot.sound','Classical.choice'}
def digest(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def replay(record=False):
 lean=ROOT/'lean4'; vendor=lean/'projection_vendor'
 spec=json.loads((vendor/'manifest.json').read_text(encoding='utf-8'))
 arc=vendor/'dependencies.tar.gz'
 if digest(arc)!=spec['archive_sha256'] or arc.stat().st_size!=spec['archive_bytes']:raise ValueError('dependency archive digest mismatch')
 files=[lean/'ProjectionBounds.lean',lean/'ProjectionCensus.lean',lean/'projection_lakefile.lean',vendor/'lakefile.lean',vendor/'manifest.json',arc]
 before={p.relative_to(ROOT).as_posix():digest(p) for p in files}
 home=Path(os.environ.get('ELAN_HOME',str(Path.home()/'.elan')))
 lake=home/'toolchains/leanprover--lean4---v4.35.0/bin'/('lake.exe' if os.name=='nt' else 'lake')
 if not lake.is_file():raise ValueError('Install Lean 4.35.0 and set ELAN_HOME')
 env=dict(os.environ);env['PATH']=str(lake.parent)+os.pathsep+env.get('PATH','')
 version=subprocess.check_output([str(lake),'--version'],env=env,text=True)
 if 'Lean version 4.35.0' not in version:raise ValueError('compiler pin mismatch')
 print('Checking fresh proof build with pinned offline dependencies',flush=True)
 with tempfile.TemporaryDirectory(prefix='projection-lean-') as td:
  work=Path(td)
  for p in files[:3]:
   rel=p.relative_to(lean)
   if p.name=='projection_lakefile.lean':rel=Path('lakefile.lean')
   target=work/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
  config=work/"lakefile.lean"
  config.write_text(config.read_text().replace('from "projection_vendor"', "from "+json.dumps(vendor.as_posix())),encoding="utf-8")
  (work/'lean-toolchain').write_text('leanprover/lean4:v4.35.0\n')
  logs=[]
  for args in [['build'],['env','lean','ProjectionCensus.lean']]:
   cp=subprocess.run([str(lake),*args],cwd=work,env=env,capture_output=True,text=True,encoding='utf-8',timeout=900)
   logs.append(cp.stdout+cp.stderr)
   if cp.returncode:raise ValueError(logs[-1])
  declarations={}
  for name,axioms in re.findall(r"^'([^']+)' depends on axioms: \[([^\]]*)\]$",logs[-1],re.M):
   values=sorted(x.strip() for x in axioms.split(',') if x.strip())
   if not set(values)<=ALLOWED:raise ValueError('unapproved axiom '+name+': '+str(values))
   declarations[name]=values
  for name in re.findall(r"^'([^']+)' does not depend on any axioms$",logs[-1],re.M):declarations[name]=[]
  expected=re.findall(r'^#print axioms (\S+)$',(lean/'ProjectionCensus.lean').read_text(),re.M)
  if set(expected)!=set(declarations) or len(expected)!=len(declarations):raise ValueError('incomplete census')
  print('Proof compiled; checking dependency bytes',flush=True)
  # Every packaged dependency byte is checked after extraction as well.
  cache=lean/'.lake/vendor'
  for rel,item in spec['files'].items():
   p=cache/rel
   if not p.is_file() or p.stat().st_size!=item['bytes'] or digest(p)!=item['sha256']:raise ValueError('dependency mismatch '+rel)
 if before!={p.relative_to(ROOT).as_posix():digest(p) for p in files}:raise ValueError('source changed during replay')
 result={'schema_version':1,'date':'2026-10-23','toolchain':'leanprover/lean4:v4.35.0','sources':before,'declarations':declarations,'count':len(declarations),'fresh_compilation':True,'custom_axioms':[],'scope':'Real scalar and normed-carrier bounds. Continuous evolution, tensor step bounds and validated numerical enclosures remain explicit premises.'}
 path=lean/'projection_axiom_census.json'
 if record:
  path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
  (lean/'projection_axiom_report.txt').write_text(version+'\n'+logs[-1],encoding='utf-8')
 else:
  if json.loads(path.read_text(encoding='utf-8'))!=result:raise ValueError('stored census differs from fresh replay')
 print('PASS fresh supplemental census:',len(declarations),'theorems; no custom axioms')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');a=p.parse_args()
 try:replay(a.record)
 except Exception as e:print('FAIL',e);sys.exit(1)
