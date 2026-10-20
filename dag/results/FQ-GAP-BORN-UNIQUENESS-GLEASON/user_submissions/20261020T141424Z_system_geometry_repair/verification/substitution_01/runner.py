from pathlib import Path
import json,hashlib,datetime,subprocess,os,sys
sys.stdout.reconfigure(encoding='utf-8')
BASE=Path(__file__).resolve().parents[1]
LEAN=Path(r'C:/Users/a343o/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean.exe')
PROJECT=Path(r'C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compile_source(name,label):
 source=BASE/name; dest=BASE/'verification'/label;dest.mkdir(parents=True,exist_ok=False)
 snapshot=dest/source.name;snapshot.write_bytes(source.read_bytes())
 (dest/'runner.py').write_bytes(Path(__file__).read_bytes())
 (BASE/'build').mkdir(exist_ok=True)
 artifact=BASE/'build'/(source.stem+'.olean')
 if artifact.exists(): artifact.unlink()
 env=os.environ.copy(); libs=[BASE/'build',BASE]+sorted((PROJECT/'.lake/packages').glob('*/.lake/build/lib/lean'))
 env['LEAN_PATH']=os.pathsep.join(map(str,libs))
 argv=[str(LEAN),'-o',str(artifact),str(snapshot)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 result=subprocess.run(argv,cwd=BASE,env=env,capture_output=True)
 (dest/'stdout.txt').write_bytes(result.stdout);(dest/'stderr.txt').write_bytes(result.stderr)
 receipt={'source':name,'source_sha256':sha(snapshot),'current_source_sha256_at_finish':sha(source),'snapshot':str(snapshot.relative_to(BASE)).replace('\\','/'),'argv':argv,'cwd':str(BASE),'lean_path':list(map(str,libs)),'compiler_sha256':sha(LEAN),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':result.returncode,'stdout_sha256':sha(dest/'stdout.txt'),'stderr_sha256':sha(dest/'stderr.txt')}
 receipt['compiled_artifact_sha256']=sha(artifact) if artifact.exists() and result.returncode==0 else None
 (dest/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
 print(result.stdout.decode('utf-8',errors='replace'));print(result.stderr.decode('utf-8',errors='replace'));print('EXIT',result.returncode)
 return result.returncode
if __name__=='__main__':sys.exit(compile_source(sys.argv[1],sys.argv[2]))