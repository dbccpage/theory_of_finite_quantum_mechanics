"""Receipt verification, kernel-axiom collection and file sealing for this run; no optimized-Python assert bypasses."""
from pathlib import Path
import datetime,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parents[1]
ALLOWED={'propext','Classical.choice','Quot.sound'}
SKIP_DIRS={'build'}
SKIP_NAMES={'manifest.json'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def receipts():
    accepted=load(B/'accepted_modules.json');entries=[];compilers=set()
    for source,label in accepted.items():
        d=B/'verification'/label;r=load(d/'receipt.json');p=B/source;code=p.read_text(encoding='utf-8')
        require(r['exit_code']==0 and r['dependency_exit']==0,'Rejected compile: '+label)
        require(r['source']==source and r['source_unchanged_at_finish'],'Source changed during compile: '+label)
        require(sha(p)==r['source_sha256']==sha(B/r['snapshot']),'Source custody mismatch: '+source)
        require(sha(d/'runner.py')==r['runner_sha256'],'Runner custody mismatch: '+label)
        require(sha(d/'stdout.txt')==r['stdout_sha256'] and sha(d/'stderr.txt')==r['stderr_sha256'],'Compiler-output custody mismatch: '+label)
        require(sha(d/'compiled.olean.bin')==r['compiled_artifact_sha256'],'Compiled-artifact custody mismatch: '+label)
        require(not re.search(r'^\s*(axiom|opaque|constant|unsafe\s+def)\s',code,re.M),'Unsafe/global custom declaration: '+source)
        require(not re.search(r'\b(sorry|admit|sorryAx)\b',code),'Proof hole in accepted source: '+source)
        out=(d/'stdout.txt').read_text(encoding='utf-8')
        require(not re.search(r'\b(error|warning)(?:\(|:)',out),'Diagnostic in accepted compile: '+label)
        require(not (d/'stderr.txt').read_bytes().strip(),'Nonempty compiler stderr: '+label)
        require('4.33.1' in r['compiler']['version'] and r['compiler']['version_exit']==0,'Unexpected Lean version: '+label)
        compilers.add(r['compiler']['sha256'])
        local=[]
        for m in re.finditer(r"'(.+?)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",out,re.S):
            axioms=[a.strip() for a in (m[2] or '').split(',') if a.strip()];require(set(axioms)<=ALLOWED,'Unexpected axiom: '+m[1])
            local.append({'name':m[1],'axioms':axioms,'source':source,'source_sha256':sha(p),'receipt':f'verification/{label}/receipt.json'})
        require(len(local)==len(re.findall(r'^#print axioms ',code,re.M)),'Missing axiom receipt: '+source)
        require(len(local)==len({e['name'] for e in local}),'Duplicate receipt names: '+source);entries+=local
    require(len(compilers)==1,'Mixed compiler binaries')
    save(B/'verification/kernel_axioms.json',{'allowed_standard_axioms':sorted(ALLOWED),'printed_receipts':entries,'custom_axioms':[],'premise_rule':'Every explicit and implicit binder remains a requirement; a clean axiom report does not discharge theorem parameters.'})
    print(json.dumps({'sources':len(accepted),'receipts':len(entries)}))
def files():
    out=[]
    for p in sorted(B.rglob('*')):
        rel=p.relative_to(B)
        if not p.is_file() or rel.parts[0] in SKIP_DIRS or rel.name in SKIP_NAMES or rel.suffix=='.tmp' or '__pycache__' in rel.parts:continue
        out.append({'path':str(rel).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)})
    return out
def manifest():
    save(B/'manifest.json',{'schema_version':1,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'excluded':sorted(SKIP_DIRS|SKIP_NAMES),'files':files()});print(json.dumps({'sealed_files':len(files())}))
def verify():
    m=load(B/'manifest.json');now={f['path']:f for f in files()}
    require({f['path'] for f in m['files']}=={*now},'File set changed since seal')
    for f in m['files']:require(now[f['path']]['sha256']==f['sha256'] and now[f['path']]['bytes']==f['bytes'],'Sealed bytes changed: '+f['path'])
    print(json.dumps({'verified_files':len(m['files'])}))
if __name__=='__main__':{'receipts':receipts,'manifest':manifest,'verify':verify}[sys.argv[1]]()
