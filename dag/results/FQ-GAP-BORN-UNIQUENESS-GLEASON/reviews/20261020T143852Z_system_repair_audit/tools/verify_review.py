"""Read-only focused review checks. Explicit guards stay active with python -O."""
from pathlib import Path
import argparse,hashlib,json,re,sys
DEFAULT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,message):
 if not ok:raise RuntimeError(message)
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def verify(bundle,repo,sealed=False):
 prior=load(bundle/'provenance.json');count=0
 for r in prior['prior_seals']:
  p=repo/r['manifest'];need(sha(p)==r['sha256'],'prior manifest hash mismatch: '+r['manifest'])
  for e in load(p)['files']:
   q=p.parent/e['path'];need(q.is_file() and q.stat().st_size==e['bytes'] and sha(q)==e['sha256'],'prior sealed byte mismatch: '+e['path']);count+=1
 need(count==prior['prior_file_count']==927,'prior evidence count mismatch')
 for e in prior['publication_dependency_closure']:
  p=repo/e['path'];need(p.is_file() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'publication dependency mismatch: '+e['path'])
 reviewed=repo/prior['reviewed_bundle'];accepted=load(bundle/'accepted_modules.json');all_axioms=[];source_counts={};compiler_hashes=set();direct_deps=0
 expected_old_names={r['name'] for r in load(reviewed/'verification/kernel_axioms.json')['printed_receipts']}
 expected_compiler=load(reviewed/'verification/toolchain_dependencies.json')['compiler']['sha256']
 for source,label in accepted.items():
  d=bundle/'verification'/label;r=load(d/'receipt.json');code=(bundle/source).read_text(encoding='utf-8')
  need(r['exit_code']==0,'compiler exit failure: '+source);need(r['dependency_exit']==0,'dependency resolution failure: '+source)
  need(r['source']==source and r['source_unchanged_at_finish'],'source identity or concurrent-write failure: '+source)
  need(sha(bundle/source)==r['source_sha256']==sha(bundle/r['snapshot']),'source snapshot mismatch: '+source)
  need(sha(d/'compiled.olean.bin')==r['compiled_artifact_sha256'],'compiled artifact mismatch: '+source)
  need(sha(d/'stdout.txt')==r['stdout_sha256'] and sha(d/'stderr.txt')==r['stderr_sha256'],'compiler output hash mismatch: '+source)
  need(sha(d/'runner.py')==r['runner_sha256'],'compiler runner mismatch: '+source)
  need(not (d/'stderr.txt').read_text(encoding='utf-8').strip(),'nonempty compiler stderr: '+source)
  out=(d/'stdout.txt').read_text(encoding='utf-8');need(not re.search(r'\b(error|warning)(?:\(|:)',out),'compiler diagnostic in accepted output: '+source)
  need(not re.search(r'^\s*(axiom|constant|opaque|unsafe\s+def)\s',code,re.M),'unsafe/custom global declaration: '+source)
  need(not re.search(r'\b(sorry|admit|sorryAx)\b',code),'proof hole token: '+source)
  need(not re.search(r'import\s+Reconstruction(?:Conditional|UnsafeDiagnostic)',code),'unsafe archive imported: '+source)
  entries=[]
  for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",out,re.S):
   deps=[s.strip() for s in (m[2] or '').split(',') if s.strip()]
   need(set(deps)<= {'propext','Classical.choice','Quot.sound'},'unexpected axiom: '+m[1])
   entries.append({'name':m[1],'axioms':deps,'source':source,'source_sha256':sha(bundle/source),'receipt':f'verification/{label}/receipt.json'})
  need(len(entries)==len(re.findall(r'^#print axioms ',code,re.M)),'missing printed axiom receipt: '+source)
  all_axioms+=entries;source_counts[source]=len(entries);compiler_hashes.add(r['compiler']['sha256'])
  need(r['compiler']['sha256']==expected_compiler==sha(Path(r['compiler']['path'])),'compiler binary custody mismatch')
  need('4.33.1' in r['compiler']['version'],'wrong Lean version: '+source)
  need(r['compiler']['version_exit']==0,'compiler version check failed')
  for dep in r['direct_dependency_artifacts']:
   p=Path(dep['path']);need(p.is_file() and sha(p)==dep['sha256'],'direct imported artifact changed: '+str(p));direct_deps+=1
  if source in ['ReconstructionArithmetic.lean','ClassicalExclusion.lean','ReconstructionGeometry.lean','ConvexSubstitution.lean']:
   need((bundle/source).read_bytes()==(reviewed/source).read_bytes(),'accepted source changed from reviewed predecessor: '+source)
 need(len(compiler_hashes)==1,'mixed compiler binaries')
 need(len(all_axioms)==len(set(r['name'] for r in all_axioms))==59 and set(r['name'] for r in all_axioms)>=expected_old_names,'expected axiom-receipt coverage mismatch')
 need(source_counts.get('SystemAudit.lean')==8,'missing audit nonvacuity/negative-control receipts')
 need(source_counts.get('TheoremSignatures.lean')==0,'signature export is not an added proof')
 signatures=(bundle/'verification'/accepted['TheoremSignatures.lean']/'stdout.txt').read_text(encoding='utf-8')
 for name in expected_old_names:need(name in signatures,'theorem signature omitted: '+name)
 need('FiniteQM.ReconstructionGeometry.JordanBridge.classify' in signatures,'input-contract signature omitted')
 names=re.findall(r'^#check @([\w.]+)',(bundle/'TheoremSignatures.lean').read_text(encoding='utf-8'),re.M)
 starts=[]
 for name in names:
  match=re.search(r'^@?'+re.escape(name)+r'(?:\.\{[^}]*\})?\s*:',signatures,re.M)
  need(match is not None,'signature block absent: '+name);starts.append((match.start(),name))
 starts.sort();canonical={name:signatures[start:(starts[i+1][0] if i+1<len(starts) else len(signatures))].strip() for i,(start,name) in enumerate(starts)}
 operations=load(bundle/'operad_delta.json')['records'];need(len(operations)==16,'operation count mismatch')
 contract=next((o for o in operations if o['id']=='RC-G12'),None)
 need(contract is not None and contract['status']=='EXPLICIT_INPUT_CONTRACT_NOT_INSTANTIATED' and not contract['proofs'],'classification input promoted to a proved operation')
 need(contract['input_contract_signature']==canonical['FiniteQM.ReconstructionGeometry.JordanBridge.classify'],'classification signature premises changed')
 known={r['name']:r for r in all_axioms}
 for op in operations:
  for p in op['proofs']:
   need(p['name'] in known,'operation cites an unchecked declaration')
   need(p['formal_signature']==canonical[p['name']],'operation signature premises changed: '+p['name'])
   need(p['source_sha256']==known[p['name']]['source_sha256'],'operation source pin mismatch')
   need(p['signature_output_sha256']==sha(bundle/p['signature_output']),'operation signature custody mismatch')
   need(p['name'] in signatures or p['name'].startswith('FiniteQM.ReconstructionAudit.'),'operation lacks an exported signature')
 ledger=load(bundle/'assumptions.json')['ledger']
 need(next(x for x in ledger if x['id']=='A05')['status']=='UNINSTANTIATED_INPUT_CONTRACT','catalogue status promoted')
 need(next(x for x in ledger if x['id']=='A07')['status']=='UNPROVED_INPUT_CONTRACT','Jordan bridge status promoted')
 # The archive has -whitespace to preserve literal captures. Check authored source/report whitespace here.
 for p in list(bundle.glob('*.lean'))+list(bundle.glob('*.md'))+list((bundle/'tools').glob('*.py')):
  need(not any(line.endswith((' ','\t')) for line in p.read_text(encoding='utf-8').splitlines()),'authored trailing whitespace: '+p.name)
 if sealed:
  m=load(bundle/'manifest.json')
  for e in m['files']:
   p=bundle/e['path'];need(p.is_file() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'review seal mismatch: '+e['path'])
  index=repo/m['current_discovery_index']['path'];need(sha(index)==m['current_discovery_index']['sha256'],'discovery index seal mismatch')
 return {'status':'PASS','accepted_compilations':len(accepted),'printed_axiom_receipts':len(all_axioms),'preserved_receipts':51,'new_audit_receipts':8,'source_receipt_counts':source_counts,'prior_seals':len(prior['prior_seals']),'prior_sealed_files':count,'publication_predecessor_files':len(prior['publication_dependency_closure']),'operations':len(operations),'proof_bearing_operation_collections':sum(bool(o['proofs']) for o in operations),'unproved_input_contract_records':1,'recorded_direct_artifacts':direct_deps,'kernel_axioms':all_axioms}
def main():
 p=argparse.ArgumentParser();p.add_argument('--bundle',type=Path,default=DEFAULT);p.add_argument('--repo',type=Path,required=True);p.add_argument('--sealed',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
 try:
  r=verify(a.bundle.resolve(),a.repo.resolve(),a.sealed)
  if a.output:a.output.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
  print(json.dumps({k:v for k,v in r.items() if k!='kernel_axioms'},indent=2));return 0
 except Exception as e:print('FAIL: '+str(e));return 1
if __name__=='__main__':sys.exit(main())