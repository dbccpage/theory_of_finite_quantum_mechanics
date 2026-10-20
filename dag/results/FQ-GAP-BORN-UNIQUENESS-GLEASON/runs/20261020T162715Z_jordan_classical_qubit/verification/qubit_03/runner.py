"""Source-only replay into a NEW output label; no optimized-Python assert bypasses."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,subprocess,sys
sys.stdout.reconfigure(encoding='utf-8')
BASE=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(condition,message):
 if not condition:raise RuntimeError(message)
def save(p,obj):p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('label');parser.add_argument('--lean',required=True);parser.add_argument('--project',required=True)
 args=parser.parse_args();lean=Path(args.lean).resolve();project=Path(args.project).resolve();source=BASE/args.source
 require(source.is_file() and source.parent==BASE,'Expected an authored top-level source')
 dest=BASE/'verification'/args.label;require(not dest.exists(),'Refusing to overwrite an earlier receipt');dest.mkdir(parents=True)
 snapshot=dest/source.name;snapshot.write_bytes(source.read_bytes());(dest/'runner.py').write_bytes(Path(__file__).read_bytes())
 build=BASE/'build';build.mkdir(exist_ok=True);artifact=build/(source.stem+'.olean')
 require(not artifact.exists(),'Refusing to reuse/overwrite an existing local module; use a fresh copy of this bundle')
 libraries=[build]+sorted((project/'.lake/packages').glob('*/.lake/build/lib/lean'));require(len(libraries)>1,'Configured Mathlib package cache is absent')
 env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join(map(str,libraries))
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();argv=[str(lean),'-o',str(artifact),str(snapshot)]
 version=subprocess.run([str(lean),'--version'],capture_output=True);result=subprocess.run(argv,cwd=BASE,env=env,capture_output=True)
 (dest/'stdout.txt').write_bytes(result.stdout);(dest/'stderr.txt').write_bytes(result.stderr)
 dep_argv=[str(lean),'--deps',str(snapshot)];deps=subprocess.run(dep_argv,cwd=BASE,env=env,capture_output=True)
 (dest/'deps.stdout.txt').write_bytes(deps.stdout);(dest/'deps.stderr.txt').write_bytes(deps.stderr)
 imports=[]
 for line in deps.stdout.decode('utf-8',errors='replace').splitlines():
  p=Path(line.strip())
  if p.is_file():
   for candidate in [p,Path(str(p)+'.private'),Path(str(p)+'.server')]:
    if candidate.is_file():imports.append({'path':str(candidate),'bytes':candidate.stat().st_size,'sha256':sha(candidate)})
 r={'source':source.name,'source_sha256':sha(snapshot),'source_bytes':snapshot.stat().st_size,'snapshot':str(snapshot.relative_to(BASE)).replace('\\','/'),'runner_sha256':sha(dest/'runner.py'),'argv':argv,'cwd':str(BASE),'lean_path':list(map(str,libraries)),'compiler':{'path':str(lean),'sha256':sha(lean),'version':version.stdout.decode('utf-8').strip(),'version_exit':version.returncode},'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':result.returncode,'stdout_sha256':sha(dest/'stdout.txt'),'stderr_sha256':sha(dest/'stderr.txt'),'dependency_argv':dep_argv,'dependency_exit':deps.returncode,'direct_dependency_artifacts':imports,'source_unchanged_at_finish':sha(source)==sha(snapshot),'dependency_scope':'Resolved direct imports and available private/server sidecars; Mathlib cache is reused, not rebuilt'}
 if result.returncode==0:
  require(artifact.exists(),'Compiler returned success without an artifact')
  (dest/'compiled.olean.bin').write_bytes(artifact.read_bytes());r['compiled_artifact_sha256']=sha(artifact)
 save(dest/'receipt.json',r)
 print(result.stdout.decode('utf-8',errors='replace'));print(result.stderr.decode('utf-8',errors='replace'));print('EXIT',result.returncode,flush=True)
 require(r['source_unchanged_at_finish'],'Source changed during compilation')
 return result.returncode
if __name__=='__main__':sys.exit(main())