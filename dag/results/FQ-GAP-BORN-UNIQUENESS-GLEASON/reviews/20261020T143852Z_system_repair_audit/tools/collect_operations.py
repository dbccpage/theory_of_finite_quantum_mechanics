from pathlib import Path
import json,re,hashlib
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
accepted={'ReconstructionArithmetic.lean':'reconstructionarithmetic_audit','ClassicalExclusion.lean':'classicalexclusion_audit','ReconstructionGeometry.lean':'reconstructiongeometry_audit','ConvexSubstitution.lean':'convexsubstitution_audit','SystemAudit.lean':'systemaudit_01','TheoremSignatures.lean':'signatures_final'}
(B/'accepted_modules.json').write_text(json.dumps(accepted,indent=2)+'\n',encoding='utf-8')
sig_rel='verification/signatures_final/stdout.txt';sig=(B/sig_rel).read_text(encoding='utf-8')
names=re.findall(r'^#check @([\w.]+)',(B/'TheoremSignatures.lean').read_text(encoding='utf-8'),re.M)
starts=[]
for name in names:
 m=re.search(r'^@?'+re.escape(name)+r'(?:\.\{[^}]*\})?\s*:',sig,re.M)
 if not m:raise RuntimeError('Missing exported signature: '+name)
 starts.append((m.start(),name))
starts.sort();signatures={name:sig[start:(starts[i+1][0] if i+1<len(starts) else len(sig))].strip() for i,(start,name) in enumerate(starts)}
byname={}
for source,label in accepted.items():
 r=load(B/'verification'/label/'receipt.json')
 if r['exit_code']!=0:raise RuntimeError('Rejected compile: '+label)
 text=(B/'verification'/label/'stdout.txt').read_text(encoding='utf-8')
 for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",text,re.S):
  deps=[s.strip() for s in (m[2] or '').split(',') if s.strip()]
  if not set(deps)<={'propext','Classical.choice','Quot.sound'}:raise RuntimeError('Unexpected axiom')
  byname[m[1]]={'name':m[1],'axioms':deps,'source':source,'source_sha256':sha(B/source),'receipt':f'verification/{label}/receipt.json','signature_output':sig_rel,'signature_output_sha256':sha(B/sig_rel),'formal_signature':signatures[m[1]],'premise_rule':'Every explicit or implicit argument in this signature remains required. Logical axiom receipts do not discharge those arguments.'}
old=ROOT/load(B/'provenance.json')['reviewed_bundle'];records=load(old/'operad_delta.json')['records']
for op in records:
 op['proofs']=[byname[p['name']] for p in op['proofs']]
 op['review_assumption_ledger']='assumptions.json'
 if op['id']=='RC-G01':op['inputs']='Counting: m>=2, a well-formed simple tag s, s.dim=4*m, 2*m<=s.rank. Selector: a nonempty well-formed EJA-tag list J with J.rank=2 and J.dim=4. See separate exact signatures.'
 if op['id']=='RC-G09':op['inputs']='For subsingleton_dim_one: an actual full-affine-span System and A.states.Subsingleton. For rank_one_pure/dim_one: an actual System, A.Spectral, A.rank=1 (and state membership for purity).'
 if op['id']=='RC-G11':op['inputs']='Explicit catalogue contract and Representation certificate. dim_eq derives dimension preservation; classical_polytope additionally requires R.tag.IsClassical; qubit_ball additionally requires a singleton simple tag and its IsQubitAlgebra witness. Catalogue geometry fields remain inputs.'
 if op['id']=='RC-G12':
  op['input_contract_signature']=signatures['FiniteQM.ReconstructionGeometry.JordanBridge.classify'];op['signature_output']=sig_rel;op['signature_output_sha256']=sha(B/sig_rel)
records.append({'id':'RC-G16','stage':'review_regression','name':'Inhabited System and phantom rejection','inputs':'Concrete singleton state set in real Euclidean dimension0; fields constructed explicitly. Negative control accepts any spectral System and rejects rank1/dim2. No catalogue or JordanBridge input.','output':'Constructed System0 of rank1 and dimension1, spectral and strongly symmetric; kernel proof excluding the old phantom.','admissible_compositions':'Use the actual trivialSystem term or instantiate the negative theorem only with its displayed System and spectrality arguments.','status':'KERNEL_CHECKED_CONSTRUCTION_AND_CONDITIONAL_THEOREMS','proofs':[v for k,v in byname.items() if k.startswith('FiniteQM.ReconstructionAudit.')],'review_assumption_ledger':'assumptions.json'})
(B/'operad_delta.json').write_text(json.dumps({'schema_version':2,'namespace':'RC-GEOMETRY-ROW8-REVIEW','records':records,'formal_operad_claim':'Unary affine substitution laws and typed conditional operations are checked. One classification input contract remains unproved. No complete higher-arity operad or process theory is claimed.','authority_effect':'None'},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(B/'verification/kernel_axioms.json').write_text(json.dumps({'allowed_standard_axioms':['propext','Classical.choice','Quot.sound'],'printed_receipts':list(byname.values()),'custom_axioms':[]},indent=2)+'\n',encoding='utf-8')
(B/'verification/exported_signatures.json').write_text(json.dumps({'source':'TheoremSignatures.lean','source_sha256':sha(B/'TheoremSignatures.lean'),'output':sig_rel,'output_sha256':sha(B/sig_rel),'signatures':signatures},indent=2)+'\n',encoding='utf-8')
print('Collected',len(records),'records,',len(byname),'axiom receipts,',len(signatures),'exact signatures')