"""Reuse unchanged native math evidence; run fresh audits after a header-only source-lead repair."""
import importlib.util,json,re,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
sys.path.insert(0,str(B));import verify_batch as audit
old=B/'review/final_integration';out=B/'review/final_integration_after_source_successor';rows=json.loads((B/'selection.json').read_bytes())['nodes'];first=s.ROOT/rows[0]['run'];candidate=json.loads((first/'p1/candidate.json').read_bytes());production=[s.ROOT/p['path'].split('/p1/construction/',1)[1] for p in candidate['source_pins']]
versions=json.loads((B/'review/source_successor_audit_tools/source_versions.json').read_bytes())['records'];historic={str((s.ROOT/p['original_path']).resolve()):p for p in versions}
tests={'code/python/tests/test_rational_bell.py','code/python/tests/test_phase_scope.py','code/python/tests/test_structure_exact.py','code/python/tests/test_dynamics_exact.py','code/python/tests/test_born_boundary_exact.py','code/python/tests/test_l1_import_exact.py','code/python/tests/test_genesis_impl_exact.py'}
for batch in ['20261019T015232Z_next_ten','20261019T145000Z_prompts_12_21','20261019T160201Z_prompts_22_31','20261019T164251Z_prompts_32_51','20261019T184100Z_prompts_52_71','20261019T201403Z_prompts_72_91']:
 for row in json.loads((s.ROOT/'dag/results/batches'/batch/'selection.json').read_bytes())['nodes']:
  p=s.ROOT/row['run']/'p0/profile.json'
  if p.is_file():tests.add(json.loads(p.read_bytes())['python_test'])
expected={Path(t).stem for t in tests}|{'lean_version','rust_version','mathlib_rev','atlas','atlas_pytest','rust_library','lean_PromptBornBoundaries'}|{'final_rust_replay_'+str(i) for i in range(20)}
actual={p.name[:-len('_receipt.json')] for p in old.glob('*_receipt.json')}
if actual!=expected|{'prompt_validator_normal'}:raise ValueError('Prior native gate coverage differs')
reused=[]
for label in sorted(expected):
 r=json.loads((old/(label+'_receipt.json')).read_bytes())
 if r['exit_code'] or not r['sources_unchanged']:raise ValueError('Nonpassing native evidence '+label)
 for pin in r['source_pins']:
  path=Path(pin['path']);key=str(path.resolve())
  if key in historic:
   h=historic[key]
   if pin['sha256']!=h['sha256'] or s.sha(s.ROOT/h['snapshot'])!=pin['sha256']:raise ValueError('Historical audit source drift')
  elif s.sha(path)!=pin['sha256']:raise ValueError('Mathematical source drift '+str(path))
 reused.append({'label':label,'receipt':s.pin(old/(label+'_receipt.json')),'source_basis':'Unchanged live math/build/validation sources; changed audit versions retained with exact hashes.'})
audit.audit_source_successor()
anchors={'QuantumMechanics.PromptBornBoundaries.'+name for name in re.findall(r'^theorem (\w+)',(s.ROOT/'lean4/PromptBornBoundaries.lean').read_text(),re.M)};audit.axiom_reports((old/'lean_PromptBornBoundaries.stdout.log').read_text(),anchors)
for i,row in enumerate(rows):
 run=s.ROOT/row['run'];c=json.loads((run/'p1/candidate.json').read_bytes());sp=importlib.util.spec_from_file_location('wire'+str(i),run/'format_certificate.py');w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
 if (old/('final_rust_replay_'+str(i)+'.stdout.log')).read_text().splitlines()!=w.lines(c['data']):raise ValueError('Retained native output mismatch')
if (old/'mathlib_rev.stdout.log').read_text().strip()!='0df444a360eaa60ab8c11dca51a86af692955474':raise ValueError('Mathlib revision drift')
sources=production+[Path(__file__),B/'verify_batch.py',B/'test_custody_guards.py',B/'tools/review.py',B/'tools/integrate.py',s.ROOT/'dag/pfp/validate_prompts.py',s.ROOT/'code/rust/src/category_theory/mssn_functor_bridge.rs',s.ROOT/'dag/operads/pg_sn_carrier.yaml',B/'custody/pg_sn_header_successor/receipt.json']+[s.ROOT/p for p in ['scripts/verify_qm_atlas_loc.py','scripts/install_qm_atlas_hook.py','code/python/tests/test_qm_atlas_loc.py','docs/QM_PROBLEM_AND_PROOF_ATLAS.md','code/python/src/qm/textbook_problems.py','code/rust/src/qm/textbook_problems.rs']]
for optimized,label in [(False,'normal'),(True,'optimized')]:
 opts=[sys.executable,'-X','utf8']+(['-O'] if optimized else [])
 for name,path in [('prompt_validator','dag/pfp/validate_prompts.py'),('protocol','dag/pfp/test_staged_prompts.py'),('filename_custody','dag/pfp/test_custody.py'),('guards',str(B/'test_custody_guards.py')),('replay',str(B/'verify_batch.py'))]:
  r=s.native.record(out,name+'_'+label,opts+[path]+(['-v'] if name in ('protocol','filename_custody','guards') else []),sources=sources)
  print(json.dumps({'gate':name+'_'+label,'exit_code':r['exit_code'],'seconds':r['seconds']}),flush=True)
  if r['exit_code']:raise ValueError('Fresh repaired audit failed')
def count(p):
 m=re.search(r'Ran (\d+) tests[\s\S]*\bOK\s*$',p.read_text())
 if not m:raise ValueError('No actual test count '+str(p))
 return int(m.group(1))
rust=re.search(r'test result: ok\. (\d+) passed; 0 failed',(old/'rust_library.stdout.log').read_text());atlas=re.search(r'(\d+) passed',(old/'atlas_pytest.stdout.log').read_text())
if not rust or not atlas:raise ValueError('Missing passing native counts')
if (out/'replay_normal.stdout.log').read_bytes()!=(out/'replay_optimized.stdout.log').read_bytes():raise ValueError('Optimized replay differs')
s.save(out/'reused_native_receipts.json',{'receipts':reused,'historical_audit_versions':versions,'boundary':'Only the corpus/source-lead audit failed; all retained native mathematical commands passed. Source-aware replay does not convert that failed validator into a pass.'})
result={'retained_exact_source_Rust_replay_runs':len(rows),'targeted_PFP_domain_Python_tests':sum(count(old/(Path(t).stem+'.stderr.log')) for t in tests),'atlas_pytest_tests':int(atlas.group(1)),'Rust_library_tests':int(rust.group(1)),'retained_local_Lean_modules':1,'new_kernel_theorems_in_module':len(anchors),'protocol_tests_per_mode':count(out/'protocol_normal.stderr.log'),'filename_custody_tests_per_mode':count(out/'filename_custody_normal.stderr.log'),'batch_guard_tests_per_mode':count(out/'guards_normal.stderr.log'),'modes':['normal','Python -O'],'corpus_prompts':177,'header_only_source_lead_successors':1,'reused_native_receipt_count':len(reused),'scope':'Unchanged-source passing native math/atlas evidence plus fresh repaired normal/optimized corpus/protocol/custody/guard/replay audits. Original failed validator and old audit sources retained. No full Mathlib/transitive/whole repository/hosted-CI claim.'};result['targeted_unique_Python_tests']=result['targeted_PFP_domain_Python_tests']+result['atlas_pytest_tests'];s.save(out/'result.json',result);print(json.dumps(result),flush=True)
