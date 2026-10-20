from pathlib import Path
import importlib.util,json,hashlib,tempfile,shutil
B=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('catalogue_evidence',B/'tools/evidence.py');ev=importlib.util.module_from_spec(spec);spec.loader.exec_module(ev)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
cases=[('source','Source custody mismatch'),('axiom','Unexpected axiom'),('global_promotion','Unbuilt global catalogue promoted'),('extension_promotion','Conditional extension promoted'),('signature','Operation proof custody mismatch')];records=[]
for name,expected in cases:
 parent=Path(tempfile.gettempdir()).resolve();tmp=Path(tempfile.mkdtemp(prefix='jordan_catalogue_controls_')).resolve()
 if tmp.parent!=parent or not tmp.name.startswith('jordan_catalogue_controls_'):raise RuntimeError('Unexpected temporary path')
 try:
  clone=tmp/'bundle';shutil.copytree(B,clone,ignore=shutil.ignore_patterns('build'))
  if name=='source':
   p=clone/'ClassicalModel.lean';p.write_bytes(p.read_bytes()+b'\n-- deliberate source mutation\n')
  elif name=='axiom':
   d=clone/'verification/helpers_02';p=d/'stdout.txt';p.write_bytes(p.read_bytes().replace(b'propext',b'sorryAx',1));r=json.loads((d/'receipt.json').read_text(encoding='utf-8'));r['stdout_sha256']=sha(p);save(d/'receipt.json',r)
  elif name=='global_promotion':
   p=clone/'claim_status.json';d=json.loads(p.read_text(encoding='utf-8'));d['global_catalogue_value']='CONSTRUCTED';save(p,d)
  elif name=='extension_promotion':
   p=clone/'operad_delta.json';d=json.loads(p.read_text(encoding='utf-8'));next(r for r in d['records'] if r['id']=='JC-11')['status']='UNCONDITIONAL_COMPLETE_CATALOGUE';save(p,d)
  elif name=='signature':
   p=clone/'operad_delta.json';d=json.loads(p.read_text(encoding='utf-8'));next(r for r in d['records'] if r['id']=='JC-10')['proofs'][0]['formal_signature']='True';save(p,d)
  ev.B=clone
  try:ev.verify()
  except RuntimeError as error:
   if expected not in str(error):raise RuntimeError('Unexpected rejection: '+str(error))
   records.append({'case':name,'optimization':'python -O','status':'REJECTED_AS_EXPECTED','reason':str(error)})
  else:raise RuntimeError('Mutation escaped: '+name)
 finally:
  ev.B=B;target=tmp.resolve()
  if target.parent!=parent or not target.name.startswith('jordan_catalogue_controls_'):raise RuntimeError('Unsafe temporary cleanup')
  shutil.rmtree(target)
save(B/'verification/mutation_controls.json',{'status':'PASS','cases':records,'scope':'Custody and scope guard tests; not new mathematical theorems.'})
print('Rejected all',len(records),'source/axiom/scope/signature mutations under optimized Python')