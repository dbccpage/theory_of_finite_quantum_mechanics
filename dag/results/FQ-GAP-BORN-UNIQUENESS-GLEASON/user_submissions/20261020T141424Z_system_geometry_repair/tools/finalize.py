from pathlib import Path
import json,hashlib,re,datetime,subprocess
BASE=Path(__file__).resolve().parents[1]
ROOT=next(p for p in BASE.parents if (p/'lean4/lakefile.lean').exists())
RESULT=ROOT/'dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON'
PREVIOUS=RESULT/'user_submissions/20261020T042856Z_reconstruction_lean_skeleton'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data):
 (BASE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def textfile(name,data):(BASE/name).write_text(data,encoding='utf-8')
FINAL={'ReconstructionArithmetic.lean':'arithmetic_final','ClassicalExclusion.lean':'geometry_final','ReconstructionGeometry.lean':'interface_final','ConvexSubstitution.lean':'substitution_final'}
ALLOWED={'propext','Classical.choice','Quot.sound'}
receipts={};axioms=[]
for source,label in FINAL.items():
 d=BASE/'verification'/label;r=json.loads((d/'receipt.json').read_text(encoding='utf-8'))
 assert r['exit_code']==0 and r['source']==source
 assert sha(BASE/source)==sha(BASE/r['snapshot'])==r['source_sha256']==r['current_source_sha256_at_finish']
 assert sha(d/'compiled.olean.bin')==r['compiled_artifact_sha256']==sha(BASE/'build'/(Path(source).stem+'.olean'))
 assert sha(d/'stdout.txt')==r['stdout_sha256'] and sha(d/'stderr.txt')==r['stderr_sha256']
 out=(d/'stdout.txt').read_text(encoding='utf-8')
 assert not (d/'stderr.txt').read_text(encoding='utf-8').strip()
 assert not re.search(r'\b(error|warning)(?:\(|:)',out),label
 entries=[]
 for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",out,re.S):
  deps=[s.strip() for s in (m[2] or '').split(',') if s.strip()]
  assert set(deps)<=ALLOWED,(m[1],deps)
  entry={'name':m[1],'axioms':deps,'source':source,'source_sha256':sha(BASE/source),'receipt':f'verification/{label}/receipt.json'}
  entries.append(entry);axioms.append(entry)
 assert len(entries)==len(re.findall(r'^#print axioms ',(BASE/source).read_text(encoding='utf-8'),re.M))
 code=(BASE/source).read_text(encoding='utf-8')
 assert not re.search(r'^\s*(axiom|opaque|constant)\s',code,re.M)
 assert not re.search(r'\b(sorry|admit|sorryAx)\b',code)
 assert not re.search(r'\bimport\s+Reconstruction(Conditional|UnsafeDiagnostic)',code)
 receipts[source]={'label':label,'checked_receipts':len(entries),'source_sha256':sha(BASE/source)}
assert len(axioms)==51,len(axioms)
assert (BASE/'ReconstructionArithmetic.lean').read_bytes()==(PREVIOUS/'ReconstructionArithmetic.lean').read_bytes()==(BASE/'input/ReconstructionArithmetic.lean').read_bytes()
# Reverify every prior sealed byte, rather than trusting the earlier saved verdict.
prov=json.loads((BASE/'provenance.json').read_text(encoding='utf-8'))
prior_count=0
for entry in prov['prior_seals_reverified']:
 p=ROOT/entry['manifest'];assert sha(p)==entry['sha256']
 for e in json.loads(p.read_text(encoding='utf-8'))['files']:
  f=p.parent/e['path'];assert sha(f)==e['sha256'] and f.stat().st_size==e['bytes'];prior_count+=1
assert prior_count==824
D=json.loads((BASE/'verification/toolchain_dependencies.json').read_text(encoding='utf-8'))
assert sha(Path(D['compiler']['path']))==D['compiler']['sha256']
assert all(x['head_exit']==0 and x['status_exit']==0 and not x['tracked_status'] for x in D['packages'])
assert next(x for x in D['packages'] if x['name']=='mathlib')['head']==D['mathlib_expected_commit']
for rec in D['sources']:
 assert rec['exit_code']==0 and rec['source_sha256']==sha(BASE/rec['source'])
 for dep in rec['resolved_dependency_files']:
  for e in [dep]+dep['sidecars']:assert sha(Path(e['path']))==e['sha256']
save('verification/kernel_axioms.json',{'allowed_standard_axioms':sorted(ALLOWED),'printed_receipts':axioms,'custom_axioms_in_accepted_receipts':[]})
# Earlier attempts stay historical and are never promoted to acceptance.
earlier=[]
for p in sorted((BASE/'verification').glob('*/receipt.json')):
 if p.parent.name in FINAL.values():continue
 r=json.loads(p.read_text(encoding='utf-8'));snap=BASE/r['snapshot']
 earlier.append({'label':p.parent.name,'exit_code':r['exit_code'],'snapshot_sha256':sha(snap),'receipt_source_sha256':r['source_sha256'],'snapshot_matches_receipt':sha(snap)==r['source_sha256'],'accepted_for_final_source':False})
save('verification/earlier_attempts.json',{'attempts':earlier,'policy':'Only *_final receipts certify the accepted sources. Failed elaboration output is not proof.'})
# Reusable operations with exact proof custody.
byname={e['name']:e for e in axioms}
records=[]
def op(id,stage,name,inputs,output,names,status='KERNEL_CHECKED_CONDITIONAL_OPERATION',admissibility=None):
 refs=[]
 for n in names:
  q=byname[n];code=(BASE/q['source']).read_text(encoding='utf-8');short=n.split('.')[-1]
  line=next(i for i,l in enumerate(code.splitlines(),1) if re.search(r'\b(theorem|def)\s+(?:[\w.]+\.)?'+re.escape(short)+r'\b',l))
  refs.append({**q,'line':line})
 records.append({'id':id,'stage':stage,'name':name,'inputs':inputs,'output':output,'admissible_compositions':admissibility or 'Only substitute terms with the displayed types and supply every stated premise.','status':status,'proofs':refs})
A='FiniteQM.ReconstructionArithmetic.';G='FiniteQM.ClassicalExclusion.';R='FiniteQM.ReconstructionGeometry.';O='FiniteQM.ConvexSubstitution.'
op('RC-G01','preservation','Arithmetic tag arithmetic','Well-formed simple tags and nonempty direct-sum lists','Counting obstruction and qubit-tag selector',[A+'no_simple_dim4m_rank2m',A+'qubit_algebra'])
op('RC-G02','geometry','Affine finite-hull transport','Affine map f; finite convex generating set of S','Finite convex generating set f(vertices) of f(S)',[G+'affine_image_finite_polytope'])
op('RC-G03','geometry','Section-to-image relation','MapsTo f S T; section maps T into S and f(section y)=y','f(S)=T',[G+'image_eq_of_section'])
op('RC-G04','geometry','Sphere parameter witness','Real t; points ((1-t²)/(1+t²),2t/(1+t²),0)','Unit norm; parameter recovery; injective family',[G+'circlePoint_norm',G+'circlePoint_recover',G+'circlePoint_injective'])
op('RC-G05','geometry','Exposed support point','Unit u; x in real three-ball; inner(u,x)=1','x=u; continuous support functional exposes {u}',[G+'unit_support_unique',G+'unit_isExposed'])
op('RC-G06','geometry','Finite/infinite extreme-point separation','Finite convex generation versus natural-parameter sphere witnesses','Three-ball is not a finite polytope',[G+'finite_extremePoints',G+'ball3_infinite_extremePoints',G+'ball3_not_finite_polytope'])
op('RC-G07','geometry','Sectioned ball marginal exclusion','Affine marginal into ball; state-preserving section with right inverse','Domain is not a finite polytope',[G+'no_polytope_with_ball_marginal'])
op('RC-G08','interface','Lawful reversible maps','Real affine state-preserving equivalences','Identity, inverse and composition preserve states',[R+'System.Reversible.identity',R+'System.Reversible.inverse',R+'System.Reversible.compose'])
op('RC-G09','interface','Rank-one phantom rejection','Full affine span; or spectral capacity-one System','Singleton states imply dimension1; spectral rank1 implies dimension1',[R+'System.subsingleton_dim_one',R+'System.rank_one_pure',R+'System.rank_one_dim_one'])
op('RC-G10','interface','Composite marginal transport','Nonempty left System; affine marginal/product laws','Onto right marginal; polytope generation descends',[R+'Composite.marginal_image',R+'Composite.marginal_finite_polytope'])
op('RC-G11','interface','Representation geometry transport','Catalogue calibrated model; actual affine equivalence; rank equality','Dimension equality; classical polytope and qubit-ball charts transfer',[R+'Representation.dim_eq',R+'Representation.classical_polytope',R+'Representation.qubit_ball'])
op('RC-G12','interface','Safe Jordan classification boundary','Explicit catalogue; repaired spectral and strongly symmetric System; supplied JordanBridge proof','Representation and simple/classical dichotomy',[],status='EXPLICIT_INPUT_CONTRACT_NOT_INSTANTIATED')
op('RC-G13','interface','Classical composite exclusion','Composite laws; representations; classical AB tag; qubit B tag','Contradiction from actual affine ball marginal',[R+'no_classical_composite_with_qubit'])
op('RC-G14','composition','Classical factor exclusion','Representations; simple/classical AB dichotomy; dimension product; rank lower bound; rank(A)>=2; rank(B)=2; dim(B)=4','A cannot have classical tag',[R+'no_classical_factor_with_qubit'])
op('RC-G15','composition','Affine substitution fragment','Composable real affine maps, matched ambient spaces, state set S','Image unit, substitution and associativity equations; finite generation preserved',[O+'image_unit',O+'image_substitution',O+'image_associativity',O+'finite_polytope_substitution'],admissibility='Unary composition only: codomain ambient space must equal the next domain. Unit is AffineMap.id. Associativity is proved. This does not supply higher arities or a complete colored operad.')
save('operad_delta.json',{'schema_version':1,'namespace':'RC-GEOMETRY-ROW8','records':records,'formal_operad_claim':'Kernel-checked unary affine-substitution fragment and typed reusable proof operations. No complete many-arity operad is claimed.','authority_effect':'None'})
save('claim_status.json',{'system_interface':'IMPLEMENTED_CONCRETE_REAL_COMPACT_CONVEX_GEOMETRY','unsafe_global_bridge':'RETIRED_FROM_ACTIVE_IMPORTS_HISTORICAL_BYTES_PRESERVED','arithmetic':'BYTE_IDENTICAL_19_RECEIPTS_RECHECKED','classical_exclusion':'PROVED_FOR_CONCRETE_AFFINE_MARGINAL_INTERFACE','classical_factor_exclusion':'PROVED_WITH_EXPLICIT_REPRESENTATION_AND_COMPOSITION_PREMISES','rank_one_dim_one':'KERNEL_CHECKED_NO_CLASSIFICATION_INPUT','jordan_catalogue':'EXPLICIT_INPUT_CONTRACT_NO_INSTANCE_SUPPLIED','jordan_bridge':'EXPLICIT_GUARDED_INPUT_CONTRACT_NO_PROOF_SUPPLIED','local_tomography_to_dimension_product':'NOT_ESTABLISHED','actual_jordan_multiplication':'NOT_CONSTRUCTED','complex_scalar_selection':'NOT_ESTABLISHED','dynamics_or_full_operational_equivalence':'NOT_ESTABLISHED','higher_arity_operad':'NOT_ESTABLISHED','review_stop':True,'authority_effect':'None'})
textfile('README.md',f'''# Row 8: geometric System and classical-exclusion repair

Status: **compiled and ready for review**. AuthorityEffect: None.

- [Repaired System and guarded Jordan interface](ReconstructionGeometry.lean): actual compact convex real state spaces, calibrated capacity/dimension, affine reversibles and composites. The old phantom is excluded by a proved rank-one/dimension-one theorem.
- [Concrete classical-exclusion chain](ClassicalExclusion.lean): affine hull transport, marginal sections, exposed sphere witnesses, infinitely many extreme points, and no affine polytope marginal onto the three-ball.
- [Preserved arithmetic](ReconstructionArithmetic.lean): byte-identical to the previous sealed extraction; all 19 printed receipts rechecked.
- [Affine substitution laws](ConvexSubstitution.lean) and [15 typed operation records](operad_delta.json): unit, substitution and associativity are proved for the unary affine fragment.
- [Independent mathematical review and remaining inputs](review.md), [claim boundaries](claim_status.json), [kernel axiom receipts](verification/kernel_axioms.json), and [compiler/dependency custody](verification/toolchain_dependencies.json).
- [Validation](validation.json), [prior evidence custody](provenance.json), and [file manifest](manifest.json).

Four accepted modules compile with pinned Lean 4.33.1. Their **51 printed axiom receipts** contain only standard Lean logical axioms (or none): 19 preserved arithmetic receipts and 32 new receipts, including 3 reversible-map constructors. No accepted source contains a global custom axiom, sorry or admit.

The elementary classical-composite exclusion is now proved from concrete affine geometry. The combined classical-factor theorem also names its representation, dichotomy, dimension-product and rank-bound premises. **A concrete Jordan catalogue/classification proof, tensor compatibility, complex selection and full process equivalence remain open inputs.** This repair does not establish all of Row 8.

All 824 earlier sealed files were reverified. Earlier failed compilation attempts and API probes remain in [verification](verification/harness_notes.json); only the four *_final receipts certify accepted sources. `Probe.lean` is an unsuccessful exploratory API probe, not an accepted module. The old unsafe sources under [input](input/README.md) are historical context and are not imported.

The source snapshots, exact compiler commands, stdout/stderr and compiled artifact bytes are saved under verification/*_final. Transient build/ import files are excluded from the file seal; their accepted bytes are sealed as compiled.olean.bin. Dependency custody records the resolved direct imports and available sidecars, plus source-package commits; it does not claim a fresh build of Mathlib. [The compiler runner](tools/evidence.py) compiles frozen copies; replay should use a fresh copy of this bundle to preserve this seal.

Stopped for review. No provider calls or Git publication actions were performed.
''')
# Exact discovery-index insertion; all predecessor bytes remain as a subsequence.
index=RESULT/'README.md';previous=(BASE/'context/previous_task_readme.md').read_bytes()
link=f'\n\n- [Repaired geometric System, guarded Jordan boundary, compiled classical exclusion and operation records](user_submissions/{BASE.name}/README.md).'.encode()
marker=b'AuthorityEffect: None.'
expected=previous.replace(marker,marker+link,1)
assert index.read_bytes() in [previous,expected]
index.write_bytes(expected)
# Explicit source observations and active-source binding.
branch=subprocess.run(['git','branch','--show-current'],cwd=ROOT,capture_output=True,text=True)
head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True)
save('source_observations.json',{'branch':branch.stdout.strip(),'head':head.stdout.strip(),'active_sources':receipts,'arithmetic_predecessor_sha256':sha(PREVIOUS/'ReconstructionArithmetic.lean'),'old_global_axioms_imported':False,'jordan_bridge_instance_supplied':False,'provider_calls':0,'live_native_library_edits':0,'historical_sources':'input/ and the predecessor sealed bundle are preserved, not active modules','authority_effect':'None'})
# Relevant local links in new authored reports.
links=[]
for name in ['README.md','review.md']:
 for link in re.findall(r'\]\(([^)]+)\)',(BASE/name).read_text(encoding='utf-8')):
  if '://' in link:continue
  target=BASE/link.split('#')[0]
  if link in ['manifest.json','validation.json']:continue
  assert target.exists(),(name,link)
  links.append({'source':name,'target':link})
check=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True)
(BASE/'verification/git_diff_check.stdout.txt').write_bytes(check.stdout)
(BASE/'verification/git_diff_check.stderr.txt').write_bytes(check.stderr)
assert check.returncode==0
validation={'status':'PASS_REPAIR_AND_KERNEL_CHECK_REVIEW_STOP','validated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'accepted_modules':receipts,'accepted_printed_axiom_receipts':len(axioms),'preserved_arithmetic_receipts':19,'new_printed_receipts':32,'new_theorem_receipts':29,'new_reversible_constructor_receipts':3,'allowed_standard_axioms':sorted(ALLOWED),'custom_axioms_in_accepted_receipts':0,'arithmetic_byte_preserved':True,'prior_manifests_reverified':len(prov['prior_seals_reverified']),'prior_files_reverified':prior_count,'operation_records':len(records),'operation_records_with_kernel_receipts':sum(bool(r['proofs']) for r in records),'input_contract_records':1,'direct_dependency_paths_recorded':sum(len(r['resolved_dependency_files']) for r in D['sources']),'new_report_relative_links_checked':len(links),'git_diff_check_exit':check.returncode,'live_native_library_edits':0,'provider_calls':0,'publication':'NOT_PERFORMED_REVIEW_STOP','authority_effect':'None'}
save('validation.json',validation)
assert (BASE/'validation.json').is_file()
# All substantive bytes except the manifest itself and disposable local build products.
files=[]
for p in sorted(BASE.rglob('*')):
 if not p.is_file() or p==BASE/'manifest.json' or p.is_relative_to(BASE/'build'):continue
 assert '__pycache__' not in p.parts
 files.append({'path':str(p.relative_to(BASE)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)})
manifest={'schema_version':1,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files,'scope_exclusions':['build/ disposable compiler import products; accepted bytes copied to verification/*_final/compiled.olean.bin','manifest.json self-exclusion'],'current_discovery_index':{'path':str(index.relative_to(ROOT)).replace('\\','/'),'sha256':sha(index)},'authority_effect':'None'}
save('manifest.json',manifest)
# Read back every sealed file, including this validator and all failed attempts.
for e in json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))['files']:
 p=BASE/e['path'];assert p.stat().st_size==e['bytes'] and sha(p)==e['sha256']
print(json.dumps({'status':'PASS','sealed_files':len(files),'axiom_receipts':len(axioms),'prior_files':prior_count,'manifest_sha256':sha(BASE/'manifest.json')},indent=2))