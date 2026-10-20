from pathlib import Path
import json,hashlib,tempfile,shutil,subprocess,sys
B=Path(__file__).resolve().parents[1];ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
cases=[('source_bytes','source snapshot mismatch'),('compiled_bytes','compiled artifact mismatch'),('proof_axiom','unexpected axiom'),('classification_promotion','classification input promoted'),('signature_premises','operation signature premises changed')]
records=[]
for name,expected in cases:
 parent=Path(tempfile.gettempdir()).resolve();temp=Path(tempfile.mkdtemp(prefix='finiteqm_system_review_')).resolve()
 if temp.parent!=parent or not temp.name.startswith('finiteqm_system_review_'):raise RuntimeError('Unsafe allocated temporary path')
 try:
  copy=temp/'bundle';shutil.copytree(B,copy,ignore=shutil.ignore_patterns('build'))
  if name=='source_bytes':
   p=copy/'ClassicalExclusion.lean';p.write_bytes(p.read_bytes()+b'\n-- deliberate source custody mutation\n')
  elif name=='compiled_bytes':
   p=copy/'verification/classicalexclusion_audit/compiled.olean.bin';a=bytearray(p.read_bytes());a[0]^=1;p.write_bytes(a)
  elif name=='proof_axiom':
   d=copy/'verification/classicalexclusion_audit';p=d/'stdout.txt';p.write_bytes(p.read_bytes().replace(b'propext',b'sorryAx',1));r=json.loads((d/'receipt.json').read_text(encoding='utf-8'));r['stdout_sha256']=sha(p);save(d/'receipt.json',r)
  elif name=='classification_promotion':
   p=copy/'operad_delta.json';v=json.loads(p.read_text(encoding='utf-8'));next(r for r in v['records'] if r['id']=='RC-G12')['status']='KERNEL_CHECKED_THEOREM';save(p,v)
  elif name=='signature_premises':
   p=copy/'operad_delta.json';v=json.loads(p.read_text(encoding='utf-8'));next(r for r in v['records'] if r['id']=='RC-G13')['proofs'][0]['formal_signature']='True';save(p,v)
  argv=[sys.executable,'-O','-B',str(B/'tools/verify_review.py'),'--bundle',str(copy),'--repo',str(ROOT)];r=subprocess.run(argv,capture_output=True,text=True)
  if r.returncode==0 or expected not in r.stdout:raise RuntimeError('Mutation was not rejected as intended: '+name+' '+r.stdout)
  records.append({'case':name,'optimization':'python -O','exit_code':r.returncode,'expected_rejection':expected,'stdout':r.stdout.strip(),'stderr':r.stderr.strip(),'status':'REJECTED_AS_EXPECTED'})
 finally:
  resolved=temp.resolve()
  if resolved.parent!=parent or not resolved.name.startswith('finiteqm_system_review_'):raise RuntimeError('Unsafe temporary cleanup target')
  shutil.rmtree(resolved)
save(B/'verification/mutation_controls.json',{'status':'PASS','baseline':'verification/review_checks.json','cases':records,'scope':'Negative controls for evidence custody and assumption-status validation; these are not new mathematical theorems.'})
print('Rejected all',len(records),'custody/assumption mutations under python -O')