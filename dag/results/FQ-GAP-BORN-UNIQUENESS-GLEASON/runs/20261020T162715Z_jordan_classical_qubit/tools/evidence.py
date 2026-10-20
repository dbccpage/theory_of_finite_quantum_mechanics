from pathlib import Path
import argparse,datetime,hashlib,json,re,subprocess,sys
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
ALLOWED={'propext','Classical.choice','Quot.sound'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def signature_blocks():
 out=B/'verification/signatures_01/stdout.txt';text=out.read_text(encoding='utf-8');names=re.findall(r'^#check @([\w.]+)',(B/'CatalogueSignatures.lean').read_text(encoding='utf-8'),re.M);starts=[]
 for name in names:
  m=re.search(r'^@?'+re.escape(name)+r'(?:\.\{[^}]*\})?\s*:',text,re.M);need(m is not None,'Missing signature: '+name);starts.append((m.start(),name))
 starts.sort();return {name:text[start:(starts[i+1][0] if i+1<len(starts) else len(text))].strip() for i,(start,name) in enumerate(starts)}
def checked_declarations(verify_deps=True):
 accepted=load(B/'accepted_modules.json');entries=[];per_source={};compiler=set()
 for source,label in accepted.items():
  d=B/'verification'/label;r=load(d/'receipt.json');p=B/source;code=p.read_text(encoding='utf-8')
  need(r['exit_code']==r['dependency_exit']==0,'Rejected compile: '+label)
  need(r['source']==source and r['source_unchanged_at_finish'],'Source changed during compile')
  need(sha(p)==r['source_sha256']==sha(B/r['snapshot']),'Source custody mismatch: '+source)
  need(sha(d/'runner.py')==r['runner_sha256'],'Runner custody mismatch')
  need(sha(d/'stdout.txt')==r['stdout_sha256'] and sha(d/'stderr.txt')==r['stderr_sha256'],'Compiler-output custody mismatch')
  need(sha(d/'compiled.olean.bin')==r['compiled_artifact_sha256'],'Compiled-artifact custody mismatch')
  need(not re.search(r'^\s*(axiom|opaque|constant|unsafe\s+def)\s',code,re.M),'Unsafe/global custom declaration')
  need(not re.search(r'\b(sorry|admit|sorryAx)\b',code),'Proof hole in accepted source')
  out=(d/'stdout.txt').read_text(encoding='utf-8')
  need(not re.search(r'\b(error|warning)(?:\(|:)',out),'Diagnostic in accepted compile')
  need(not (d/'stderr.txt').read_bytes().strip(),'Nonempty compiler stderr')
  need('4.33.1' in r['compiler']['version'] and r['compiler']['version_exit']==0,'Unexpected Lean version')
  need(sha(Path(r['compiler']['path']))==r['compiler']['sha256'],'Compiler binary changed');compiler.add(r['compiler']['sha256'])
  if verify_deps:
   for dep in r['direct_dependency_artifacts']:need(sha(Path(dep['path']))==dep['sha256'],'Imported dependency changed')
  local=[]
  for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",out,re.S):
   axioms=[a.strip() for a in (m[2] or '').split(',') if a.strip()];need(set(axioms)<=ALLOWED,'Unexpected axiom: '+m[1]);local.append({'name':m[1],'axioms':axioms,'source':source,'source_sha256':sha(p),'receipt':f'verification/{label}/receipt.json'})
  need(len(local)==len(re.findall(r'^#print axioms ',code,re.M)),'Missing axiom receipt');entries+=local;per_source[source]=len(local)
 need(len(compiler)==1,'Mixed compiler binaries');need(len(entries)==len({e['name'] for e in entries})==112,'Declaration coverage mismatch')
 return entries,per_source

def collect():
 accepted=load(B/'accepted_modules.json');accepted['CatalogueSignatures.lean']='signatures_01';save(B/'accepted_modules.json',accepted)
 entries,per_source=checked_declarations();signatures=signature_blocks();output='verification/signatures_01/stdout.txt';digest=sha(B/output)
 for e in entries:e.update({'formal_signature':signatures[e['name']],'signature_output':output,'signature_output_sha256':digest,'premise_rule':'Every explicit and implicit binder remains a requirement; a clean axiom report does not discharge theorem parameters.'})
 save(B/'verification/kernel_axioms.json',{'allowed_standard_axioms':sorted(ALLOWED),'printed_receipts':entries,'custom_axioms':[]})
 save(B/'verification/exported_signatures.json',{'source':'CatalogueSignatures.lean','source_sha256':sha(B/'CatalogueSignatures.lean'),'output':output,'output_sha256':digest,'signatures':signatures})
 by={e['name']:e for e in entries};records=[]
 def op(id,name,inputs,result,proofs,status='KERNEL_CHECKED_TYPED_OPERATION'):
  records.append({'id':id,'name':name,'inputs':inputs,'output_or_relation':result,'status':status,'admissible_substitution':'Only substitute matching carrier/affine-space types and supply all displayed signature premises. Jordan multiplication is not assumed associative.','proofs':[by[p] for p in proofs]})
 H='FiniteQM.CatalogueGeometry.';P='FiniteQM.ConcreteJordanProducts.';C='FiniteQM.ClassicalModel.';Q='FiniteQM.QubitModel.';J='FiniteQM.SupportedJordanCatalogue.';S='FiniteQM.JordanConeSquares.';A='FiniteQM.CatalogueApplications.'
 op('JC-01','Affine combinations and unique maxima','Real affine functional; two coefficients summing to one; unique maximizer on a state set','Affine preservation; unique maxima are extreme',[H+'affine_combo',H+'extreme_of_unique_affine_max'])
 op('JC-02','Central reflection capacity bound','Origin-containing centrally symmetric states; normalized affine measurement distinguishing a finite frame','Reflection equation and frame size <=2',[H+'affine_reflection',H+'symmetric_frame_bound'])
 op('JC-03','Classical Jordan product','Finite real coordinate vectors','Commutative unital bilinear product; Jordan relation; positive squares; trace normalization',[n for n in by if n.startswith(P+'classical_')])
 op('JC-04','Spin product and normalized states','Real scalar plus real three-vector; named spinMul product and Lorentz cone','Unital commutative bilinear Jordan product identities; positive squares; exact normalized Bloch correspondence',[n for n in by if n.startswith(P) and not n.startswith(P+'classical_')])
 op('JC-05','Classical probability chart and vertices','n>=0, a fixed affine basis with n+1 vertices, state membership where required','Exact normalized probability chart, reconstruction and extreme vertices',[C+n for n in ['basis','coord_nonneg','coord_le_one','coord_one_unique','vertex_extreme','pure_eq_vertices','coords_probability','coords_reconstruct','coords_image']])
 op('JC-06','Calibrated classical System','The constructed simplex and coordinate effects','Attained capacity n+1, homogenized dimension n+1, finite polytope and spectrality',[C+n for n in ['vertex_frame','frame_bound','system','rank_eq','dim_eq','finite_polytope','spectral']])
 op('JC-07','Antipodal qubit test','Unit real three-vector; state in the ball for effect bounds','Bounded normalized affine effects and a pure antipodal frame',[Q+n for n in ['axisFunctional_apply','inner_bounds','axisEffect','unit_ne_neg','unit_pair_frame']])
 op('JC-08','Calibrated qubit System','Constructed real unit ball; diameter parameter in [-1,1]','Capacity2, dimension4, pure sphere, state chart and spectral decomposition',[Q+n for n in ['pure_eq_sphere','frame_bound','system','rank_eq','dim_eq','state_chart','diameter_mem','spectral']])
 op('JC-09','Exact square-cone witnesses','Coordinatewise nonnegative tuple or Lorentz-positive spin element','Positivity iff existence of a Jordan square; zero and boundary cases included',[S+'classical_positive_iff_square',S+'spin_positive_iff_square'])
 op('JC-10','Supported catalogue entry construction','A well-formed arithmetic tag satisfying IsClassical or a singleton qubit-tag witness','Actual calibrated Entry on precisely the supported subset',[J+n for n in ['qubit_invariants','qubit_not_classical','classicalEntry','qubitEntry','entry','classical_entry_calibrated','supported_entry_calibrated','complexQubit_supported','spinQubit_supported']])
 op('JC-11','Conditional catalogue extension','REQUIRES an Entry for every unsupported tag; no such remaining argument is supplied','Assembles a full catalogue only when the remaining entries are provided; agreement on supported tags',[J+'completeCatalogue',J+'extension_agrees'],'CONDITIONAL_EXTENSION_NOT_INSTANTIATED')
 op('JC-12','Concrete state/algebra applications','Constructed models; Composite laws for the exclusion application','No classical composite with a concrete qubit marginal; state membership equals normalized Jordan-square conditions',[A+'no_classical_composite',A+'classical_states_are_normalized_squares',A+'qubit_states_are_normalized_squares'])
 save(B/'operad_delta.json',{'schema_version':2,'namespace':'JC-CONCRETE-CLASSICAL-QUBIT','records':records,'formal_operad_claim':'Scoped typed algebra, affine and catalogue operations with checked relations and exact signatures; no complete higher-arity operad is claimed.','authority_effect':'None'})
 label='applications_02';r=load(B/'verification'/label/'receipt.json')
 save(B/'operads/05_model_applications.json',{'stage':'05_model_applications','collected_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'receipt':f'verification/{label}/receipt.json','source_snapshot':r['snapshot'],'source_sha256':r['source_sha256'],'checked_declarations':[e for e in entries if e['source']=='CatalogueApplications.lean'],'scope':'Concrete model and Jordan-square vertical slice; no classification bridge.','authority_effect':'None'})
 save(B/'stage_index.json',{'stages':[str(p.relative_to(B)).replace('\\','/') for p in sorted((B/'operads').glob('*.json'))],'candidate_policy':'Final accepted_modules.json pins final sources. Earlier passing snapshots remain scoped historical evidence; failed attempts never certify a final source.','authority_effect':'None'})
 print(json.dumps({'declarations':len(entries),'new_declarations':sum(n for source,n in per_source.items() if source not in ['ReconstructionArithmetic.lean','ClassicalExclusion.lean','ReconstructionGeometry.lean']),'signatures':len(signatures),'operations':len(records)},indent=2))

def verify(sealed=False):
 prov=load(B/'provenance.json');count=0
 for e in prov['prior_seals']:
  p=ROOT/e['manifest'];need(sha(p)==e['sha256'],'Prior manifest changed')
  for f in load(p)['files']:
   q=p.parent/f['path'];need(q.stat().st_size==f['bytes'] and sha(q)==f['sha256'],'Prior sealed bytes changed');count+=1
 need(count==prov['prior_files']==1015,'Prior custody coverage mismatch')
 previous=ROOT/prov['previous_bundle']
 for name in ['ReconstructionArithmetic.lean','ClassicalExclusion.lean','ReconstructionGeometry.lean']:
  need((B/name).read_bytes()==(previous/name).read_bytes(),'Preserved source changed: '+name)
 need((B/'context/SystemAudit.lean').read_bytes()==(previous/'SystemAudit.lean').read_bytes(),'Historical System witness changed')
 entries,per_source=checked_declarations();canonical=signature_blocks();saved=load(B/'verification/kernel_axioms.json')['printed_receipts'];need({e['name'] for e in saved}=={e['name'] for e in entries},'Saved proof coverage mismatch')
 for e in saved:need(e['formal_signature']==canonical[e['name']] and e['signature_output_sha256']==sha(B/e['signature_output']),'Exact premise/signature custody mismatch')
 records=load(B/'operad_delta.json')['records'];need(len(records)==12,'Operation count mismatch');extension=next(r for r in records if r['id']=='JC-11');need(extension['status']=='CONDITIONAL_EXTENSION_NOT_INSTANTIATED','Conditional extension promoted')
 known={e['name']:e for e in saved}
 for op in records:
  for e in op['proofs']:need(e==known[e['name']],'Operation proof custody mismatch')
 flags=load(B/'claim_status.json');need(flags['global_catalogue_value']=='NOT_CONSTRUCTED','Unbuilt global catalogue promoted');need(flags['classification_bridge']=='NOT_PROVED','Unproved classification promoted');need(flags['complex_matrix_isomorphism']=='NOT_PROVED','Unproved matrix identification promoted');need(flags['strong_symmetry_models']=='NOT_YET_PROVED','Unproved strong symmetry promoted')
 stage_paths=load(B/'stage_index.json')['stages'];need(len(stage_paths)==8,'Missing stage ledger')
 for name in stage_paths:
  stage=load(B/name);r=load(B/stage['receipt']);need(r['exit_code']==0 and r['source_sha256']==stage['source_sha256']==sha(B/stage['source_snapshot']),'Invalid stage receipt')
 for p in list(B.glob('*.lean'))+list(B.glob('*.md'))+list((B/'tools').glob('*.py')):
  need(not any(l.endswith((' ','\t')) for l in p.read_text(encoding='utf-8').splitlines()),'Authored trailing whitespace: '+p.name)
 if sealed:
  m=load(B/'manifest.json')
  for e in m['files']:
   p=B/e['path'];need(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'New seal mismatch: '+e['path'])
  need(sha(ROOT/m['current_discovery_index']['path'])==m['current_discovery_index']['sha256'],'Index seal mismatch')
 return {'status':'PASS','accepted_compilations':len(load(B/'accepted_modules.json')),'printed_axiom_receipts':len(entries),'new_receipts':65,'preserved_arithmetic_receipts':per_source['ReconstructionArithmetic.lean'],'declaration_counts':per_source,'exact_signatures':len(canonical),'operations':len(records),'staged_ledgers':len(stage_paths),'prior_manifests':len(prov['prior_seals']),'prior_files':count,'global_catalogue_instantiated':False,'provider_calls':0,'publication':'NOT_PERFORMED_REVIEW_STOP','authority_effect':'None'}

def seal():
 summary=verify();summary['validated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save(B/'validation.json',summary)
 attempts=[];accepted_labels=set(load(B/'accepted_modules.json').values())
 for p in sorted((B/'verification').glob('*/receipt.json')):
  r=load(p);attempts.append({'label':p.parent.name,'source':r['source'],'exit_code':r['exit_code'],'source_sha256':r['source_sha256'],'accepted_for_final_source':p.parent.name in accepted_labels})
 save(B/'verification/attempt_index.json',{'attempts':attempts,'failed_attempts_preserved':True})
 index=ROOT/'dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/README.md';previous=(B/'context/previous_task_readme.md').read_bytes();marker=b'AuthorityEffect: None.';link=f'\n\n- [Concrete classical and qubit models: staged partial Jordan catalogue, square cones, exact Lean checks and collected operations](runs/{B.name}/README.md).'.encode();expected=previous.replace(marker,marker+link,1);need(index.read_bytes() in [previous,expected],'Discovery index changed concurrently');index.write_bytes(expected)
 files=[]
 for p in sorted(B.rglob('*')):
  if not p.is_file() or p==B/'manifest.json' or p.is_relative_to(B/'build'):continue
  need('__pycache__' not in p.parts,'Python cache in evidence')
  files.append({'path':str(p.relative_to(B)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)})
 save(B/'manifest.json',{'schema_version':1,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files,'scope_exclusions':['manifest.json self-exclusion','build/ transient import artifacts; accepted compiled bytes are saved under verification'],'current_discovery_index':{'path':str(index.relative_to(ROOT)).replace('\\','/'),'sha256':sha(index)},'authority_effect':'None'})
 verify(True);print(json.dumps({'status':'SEALED_REVIEW_STOP','files':len(files),'manifest_sha256':sha(B/'manifest.json')},indent=2))

def main():
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['collect','verify','seal']);p.add_argument('--sealed',action='store_true');a=p.parse_args()
 if a.mode=='collect':collect()
 elif a.mode=='seal':seal()
 else:print(json.dumps(verify(a.sealed),indent=2))
if __name__=='__main__':main()