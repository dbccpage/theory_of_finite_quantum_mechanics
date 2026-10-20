from pathlib import Path
import sys,subprocess,json,os,hashlib,datetime
sys.path.insert(0,str(Path(__file__).resolve().parent))
from evidence import BASE,LEAN,PROJECT,sha
sys.stdout.reconfigure(encoding='utf-8')
libs=[BASE/'build',BASE]+sorted((PROJECT/'.lake/packages').glob('*/.lake/build/lib/lean'))
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join(map(str,libs))
records=[]
for name in ['ReconstructionArithmetic.lean','ClassicalExclusion.lean','ReconstructionGeometry.lean','ConvexSubstitution.lean']:
 argv=[str(LEAN),'--deps',str(BASE/name)]
 r=subprocess.run(argv,cwd=BASE,env=env,capture_output=True)
 (BASE/'verification'/(name+'.deps.stdout.txt')).write_bytes(r.stdout)
 (BASE/'verification'/(name+'.deps.stderr.txt')).write_bytes(r.stderr)
 deps=[]
 for line in r.stdout.decode('utf-8').splitlines():
  p=Path(line.strip())
  if p.is_file():
   item={'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
   sidecars=[]
   if p.suffix=='.olean':
    for suffix in ['.private','.server']:
     side=Path(str(p)+suffix)
     if side.exists():sidecars.append({'path':str(side),'bytes':side.stat().st_size,'sha256':sha(side)})
   item['sidecars']=sidecars;deps.append(item)
 records.append({'source':name,'source_sha256':sha(BASE/name),'argv':argv,'exit_code':r.returncode,'resolved_dependency_files':deps,'stdout':name+'.deps.stdout.txt'})
assert all(r['exit_code']==0 for r in records)
packages=[]
for package in sorted((PROJECT/'.lake/packages').iterdir()):
 if not package.is_dir():continue
 head=subprocess.run(['git','-C',str(package),'rev-parse','HEAD'],capture_output=True)
 status=subprocess.run(['git','-C',str(package),'status','--porcelain','-uno'],capture_output=True)
 packages.append({'name':package.name,'path':str(package),'head':head.stdout.decode().strip(),'head_exit':head.returncode,'tracked_status':status.stdout.decode(),'status_exit':status.returncode})
version=subprocess.run([str(LEAN),'--version'],capture_output=True)
data={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'compiler':{'path':str(LEAN),'sha256':sha(LEAN),'version':version.stdout.decode().strip(),'version_exit':version.returncode},'lean_path':list(map(str,libs)),'mathlib_expected_commit':'0df444a360eaa60ab8c11dca51a86af692955474','packages':packages,'sources':records,'dependency_scope':'lean --deps resolved imported modules plus available private/server sidecars; not a claim to recompile all of Mathlib','project_toolchain':{'path':str(PROJECT/'lean-toolchain'),'sha256':sha(PROJECT/'lean-toolchain')},'project_lake_manifest':{'path':str(PROJECT/'lake-manifest.json'),'sha256':sha(PROJECT/'lake-manifest.json')}}
(BASE/'verification/toolchain_dependencies.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('Recorded dependency files:',sum(len(r['resolved_dependency_files']) for r in records))