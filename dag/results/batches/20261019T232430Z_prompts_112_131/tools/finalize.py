"""Seal owned batch evidence and verify all prior results against base Git blobs."""
import importlib.util,json,subprocess,yaml
from pathlib import Path
B=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
selection=json.loads((B/'selection.json').read_bytes());integration=json.loads((B/'review/final_integration/result.json').read_bytes());paths=set();table=[]
counts={'runs':0,'exact_records':0,'rejected_P4_mutations':0,'reviewed_generators':0,'reviewed_relations':0,'reviewed_compositions':0,'retained_failed_checkpoints':0,'external_provider_calls':0,'chat_cost':'unmeasured'}
for row in selection['nodes']:
 run=s.ROOT/row['run'];review=run.parent.parent/'reviews/20261019_l1_import_audit';acc=json.loads((run/'accepted.json').read_bytes());prof=json.loads((run/'p0/profile.json').read_bytes());candidate=json.loads((run/acc['attempt']/'candidate.json').read_bytes());delta=yaml.safe_load((review/'operad_delta.yaml').read_bytes());mutants=json.loads((run/'p4/host_check.json').read_bytes())['predicate_results']['mutants']
 counts['runs']+=1;counts['exact_records']+=len(candidate['data']['records']);counts['rejected_P4_mutations']+=len(mutants);counts['retained_failed_checkpoints']+=len(acc['failed_checkpoints'])
 for key,field in [('reviewed_generators','add_or_refine_generators'),('reviewed_relations','add_or_refine_relations'),('reviewed_compositions','checked_compositions')]:counts[key]+=len(delta[field])
 s.save(review/'delivery_review_result.json',{'task_id':row['node_id'],'status':'scoped_result_or_obstruction_reviewed','accepted':acc,'integration':s.pin(B/'review/final_integration/result.json'),'claim_boundary':prof['claim_boundary'],'rejected_P4_mutations':len(mutants),'authority_effect':'None'})
 path=s.ROOT/row['operad_collection'];c=yaml.safe_load(path.read_bytes());c['latest_review'].update(status='scoped_result_or_obstruction_reviewed',delivery_result=(review/'delivery_review_result.json').relative_to(s.ROOT).as_posix());path.write_bytes(yaml.safe_dump(c,sort_keys=False,allow_unicode=True,width=100).encode());paths.add(path)
 paths.update(p for folder in (run,review) for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
 for pin in candidate['source_pins']:paths.add(s.ROOT/pin['path'].split('/'+acc['attempt']+'/construction/',1)[1])
 table.append('| '+row['node_id']+' | '+prof['claim_boundary']['supports'].replace('|','/')+' | '+prof['claim_boundary']['does_not_support'].replace('|','/')+' |')
base=selection['base_commit'];selected={r['operad_collection'] for r in selection['nodes']}
tracked=subprocess.check_output(['git','ls-tree','-r','-z',base,'--','dag/results','dag/prompts','dag/operads','dag/pfp'],cwd=s.ROOT).split(b'\0');old=[]
for line in tracked:
 if not line:continue
 meta,raw=line.split(b'\t',1);name=raw.decode();oid=meta.split()[-1].decode()
 if name=='dag/operads/index.json' or name in selected:continue
 old.append((name,oid))
actual=subprocess.check_output(['git','hash-object','--no-filters','--stdin-paths'],input='\n'.join(n for n,_ in old)+'\n',cwd=s.ROOT,text=True).splitlines()
if len(actual)!=len(old):raise ValueError('Preservation coverage')
preserved=[]
for (name,oid),live in zip(old,actual):
 if oid!=live:raise ValueError('Prior artifact changed '+name)
 preserved.append({'path':name,'git_blob':oid,'sha256':s.sha(s.ROOT/name)})
s.save(B/'review/preservation.json',{'base_commit':base,'files':preserved,'count':len(preserved),'scope':'Every prior tracked result, prompt, PFP file and unselected operad collection; original selected target/source/status fields checked separately.'})
counts['retained_failed_development_compiler_invocations']=sum(json.loads(p.read_bytes())['exit_code']!=0 for p in (B/'development').glob('*/*_receipt.json'))
companions=json.loads((B/'review/companion_records.json').read_bytes())
for row in companions['records']:
 if s.sha(s.ROOT/row['subject'])!=row['sha256']:raise ValueError('Companion source drift')
 for name in row['companions']:
  c=yaml.safe_load((s.ROOT/name).read_bytes())
  if c['source_sha256']!=row['sha256'] or c['subject']!=row['subject']:raise ValueError('Companion identity drift')
  paths.add(s.ROOT/name)
remaining=sum(not n.get('latest_run') for n in json.loads((s.ROOT/'dag/operads/index.json').read_bytes())['nodes'])
s.save(B/'summary.json',{'batch_id':selection['batch_id'],'status':'twenty_scoped_stages_reviewed','counts':counts,'integration':integration,'preserved_prior_files':len(preserved),'remaining_unrun_prompts':remaining,'scope':'Local scoped results/counterexamples and partial operad presentations; no blanket target, physical or full coherence promotion.'})
readme='''# PFP prompts 112 through 131

All twenty ordered previously un-run prompts have local file-based P0/P1/P2/P4/P5 results in their own results folders. Four reviewed missions precede candidate construction; actual independent predicates, Python/Rust executions and named Lean axiom reports precede mutation challenges and canonical recording. Stage-local pending labels are preserved as historical records; separate reviews and canonical metadata give the final status. No external provider was dispatched; active chat cost is unmeasured. One local researcher performed the review, with separate native/checker implementations, not an independent author/model panel.

The batch constructs actual triangle incidence/face products, weighted quotient minimizers and primal/dual constraints; coordinate aggregation and bounded symmetry countercontrols; replicas and supplied witness masses; cyclic group tables and Gaussian inverse/nonfield controls; Boolean map-square obstructions and two exact complex toggle roots; rational truncation/tail identities; all prepared-false collapse dilations and reset Choi matrices; effect/frame rivals; tensor/dumpRight arrays; signed-square density lifts; independent/correlated phase tables and admitted Gram forms.

The density-lift control explicitly rejects strictness from complementary slackness alone when capacities can vanish: disjoint supports have saturation and Xi squared equal to 1. Positive capacity on active residual support or another nonzero-overlap premise is required for the strict bound. Only exact rational Xi squared is reported, not an invented decimal square root. Undefined ratios/inverses/lifts have explicit tags; zero placeholders are not claimed values. Signed-square density inputs are a supplied restricted carrier. Original target wording and historical paper/provider annotations remain immutable source material, not accepted proof certificates.

The eight signed permutations do not establish maximal bounded-linear symmetry. Observer axioms stay hypotheses; differing source receipt H-number labels do not discharge them. The triangle quotient has an explicit primal construction and triangle-inequality lower bound, but full arbitrary-window/Banach refinement remains open. Squared l2 energy is replica-extensive too. Finite phase averages do not construct Haar measure; unitary square roots do not construct continuous time; rational truncations do not construct a completion; admitted inner products/complex coefficients/tensor conventions do not derive their physical selection. All remaining transports are stated per prompt.

Each prompt retains three typed unary generators, one relation and two context-preserving substitutions, with source pins, hypotheses, countercontrols and failed target promotions. These are reusable partial presentations. General identity, substitution, symmetry and coherence on the refined carriers remain open. The forty shared Lean declarations have literal scalar/finite scope; twenty P2 scope modules import the freshly compiled module and report the two relevant theorem axioms. Native-array-to-kernel representation refinement is not inferred from matching labels.

Two actual development compiler failures and the corresponding original source bytes are retained, followed by a passing repaired module. The first used an unavailable Mathlib Omega import, replaced with core Init.Omega. The second required a function-application space. Review also strengthened the time lemma to the actual root equations; no numerical certificate was rewritten. Accepted P2 sources are frozen and individually pinned. The independent checkers require complete construction-source sets, exact sealed requests, canonical rational strings and strict primitive types, including under Python -O.

Final integration checks all previously targeted domain tests plus the new tests, the full finite-probability Rust library, a fresh shared Lean module, all twenty complete Rust replays, all177 prompt contracts, protocol/filename/batch guards in normal and optimized Python, and the required atlas LOC/symbol/parity/pytest gates. Cached pinned Mathlib is imported; no full Mathlib/transitive dependency/whole repository/hosted CI claim is made. Companion score/contract/doc records cover live code and wrappers; immutable captured sources receive no documentary backfill. Engineering grades remain unassessed under SCORING1.4; no completed score token is invented.

'''
readme+='Measured batch counts:\n\n'+json.dumps(counts,sort_keys=True)+'\n\nTargeted integration:\n\n'+json.dumps(integration,sort_keys=True)+'\n\nPrior files preserved: '+str(len(preserved))+'. Remaining un-run prompts: '+str(remaining)+'.\n\n| Prompt | Supported step | Remaining obligation |\n|---|---|---|\n'+'\n'.join(table)+'\n\nRead-only replay:\n\n    py -3.9 -X utf8 '+B.relative_to(s.ROOT).as_posix()+'/verify_batch.py\n    py -3.9 -X utf8 -O '+B.relative_to(s.ROOT).as_posix()+'/verify_batch.py\n\nAll owned files are sealed in manifest.json, excluding the manifest itself. GitHub delivery is separately verified after publication. AuthorityEffect: None.\n'
(B/'README.md').write_bytes(readme.encode());paths.add(s.ROOT/'dag/operads/index.json');paths.update(p for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
s.save(B/'manifest.json',{'scope':'All owned batch, per-run, per-review, source/build, companion and canonical collection artifacts. This manifest excludes itself.','files':[s.pin(p) for p in sorted(paths) if p!=B/'manifest.json']})
print(json.dumps({'counts':counts,'preserved':len(preserved),'remaining':remaining,'manifest_files':len(paths)}),flush=True)
