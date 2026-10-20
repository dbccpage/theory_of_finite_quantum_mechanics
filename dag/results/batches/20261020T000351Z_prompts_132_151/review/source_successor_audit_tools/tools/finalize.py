"""Seal owned batch evidence and verify all prior results against base Git blobs."""
import importlib.util,json,subprocess,yaml
from pathlib import Path
B=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
selection=json.loads((B/'selection.json').read_bytes());integration=json.loads((B/'review/final_integration/result.json').read_bytes());paths=set();table=[]
counts={'runs':0,'exact_records':0,'rejected_P4_mutations':0,'reviewed_generators':0,'reviewed_relations':0,'reviewed_compositions':0,'retained_failed_checkpoints':0,'external_provider_calls':0,'chat_cost':'unmeasured'}
for row in selection['nodes']:
 run=s.ROOT/row['run'];review=run.parent.parent/'reviews/20261020_born_boundary_audit';acc=json.loads((run/'accepted.json').read_bytes());prof=json.loads((run/'p0/profile.json').read_bytes());candidate=json.loads((run/acc['attempt']/'candidate.json').read_bytes());delta=yaml.safe_load((review/'operad_delta.yaml').read_bytes());mutants=json.loads((run/'p4/host_check.json').read_bytes())['predicate_results']['mutants']
 counts['runs']+=1;counts['exact_records']+=len(candidate['data']['records']);counts['rejected_P4_mutations']+=len(mutants);counts['retained_failed_checkpoints']+=len(acc['failed_checkpoints'])
 for key,field in [('reviewed_generators','add_or_refine_generators'),('reviewed_relations','add_or_refine_relations'),('reviewed_compositions','checked_compositions')]:counts[key]+=len(delta[field])
 s.save(review/'delivery_review_result.json',{'task_id':row['node_id'],'status':'scoped_result_or_obstruction_reviewed','accepted':acc,'integration':s.pin(B/'review/final_integration/result.json'),'claim_boundary':prof['claim_boundary'],'rejected_P4_mutations':len(mutants),'authority_effect':'None'})
 path=s.ROOT/row['operad_collection'];c=yaml.safe_load(path.read_bytes());c['latest_review'].update(status='scoped_result_or_obstruction_reviewed',delivery_result=(review/'delivery_review_result.json').relative_to(s.ROOT).as_posix());path.write_bytes(yaml.safe_dump(c,sort_keys=False,allow_unicode=True,width=100).encode());paths.add(path);paths.add(run.parent.parent/'.gitattributes')
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
readme="""# PFP prompts 132 through 151

All twenty ordered previously un-run prompts have their own source-sealed P0/P1/P2/P4/P5 stages and retained operation deltas. Four reviewed missions precede exact construction. Independent predicates, Rust/Python native execution and literal Lean axiom reports precede challenges and P5 recording. One local researcher performed the review; separate native/checker code is not an independent author/model panel. No external provider calls; chat cost unmeasured.

This batch computes all Boolean-map linear extensions and Gram tests; rational orthogonal projectors/frame readouts; exact normalized rational-square refusals; finite/common phase controls; signed diagonal/singular-value/scale-loss arrays; column-stochastic channel composition; coherence/dephasing non-descent; normalization and positive-ray controls; scalar/disjoint defects; natural-power strictness; row sparsity versus monomial/rank controls; supplied Gaussian lift redundancy; complete three-sector C4 conjugation/readout tables; normalized atom-map rivals; quadratic-ansatz frame tomography; admitted reversible rotations; every retained two-state stochastic path; Gaussian pairing/frame rivals; cyclic regular-representation matrices; and the full M2(Q) matrix-unit multiplication table.

Substantive corrected qualifications are explicit in canonical reviewed_target_qualification fields, not silently folded into historical source text. Disjoint-support l1 defect is zero regardless of signs: the same-sign criterion belongs to scalar D1. At-most-one nonzero per row does not imply an invertible monomial map: the retained matrix(1,0;2,0) has rank1. Positive-ray normalization classification needs both totals positive, while negative scaling also preserves algebraic normalization. The local Gleason-named file begins with a quadratic ansatz; it does not derive that ansatz or prove arbitrary frame-function uniqueness. The local C17 anchor is diagonal multiplication, not general residual-density Markov factorization. ConnectednessShadow and selector Boolean fields do not establish topological connectedness or a circle selector. The new explicit matrix/probe yields37/16 but does not authenticate historical source construction. Raw quartic pairings change unit totals; normalized quartic and swapped raw rivals have different stated contracts.

Every operation carries literal admitted hypotheses and fixed context. The typed unary generators, relations and substitutions are reusable partial presentations, not a completed refined-carrier operad. Identity/substitution/symmetry/coherence, native-array-to-Lean/source refinement and all specified physical/continuum/import bridges remain open. Historical PROVED_LEAN/provider PASS/route/index labels are retained as source material, never acceptance predicates. Square-root/normalization/zero-mass failures use explicit tags, with no decimal approximations or invented costs.

The actual failed development Lean compiler invocations, their recovery sorryAx outputs and exact source versions are retained; no recovery proof is accepted. A lexical repair, the explicit pinned Mathlib absolute-product import and pre-P1 EOF newline normalization precede every sealed candidate. Named P2 and final Lean reports are checked for standard axioms only, with no sorryAx. All published sources have exact byte custody, complete construction sets and sealed request bytes. Strict primitive/schema/source challenges run under normal and optimized Python.

Final validation covers all previously targeted domain tests plus this batch, the full finite-probability Rust library, a fresh shared Lean module, twenty complete Rust replays, all177 prompt contracts, protocol/filename/batch guards in both Python modes and the required QM atlas LOC/symbol/parity/pytest gate. Cached pinned Mathlib is imported; no full Mathlib/transitive dependency/whole repository/hosted-CI success is asserted. Companion score/contract/doc records cover live production and replay code; frozen snapshots remain custody assets. Engineering grades are unassessed under SCORING1.4, with no completed score token.

"""
readme+='Measured counts:\n\n'+json.dumps(counts,sort_keys=True)+'\n\nTargeted integration:\n\n'+json.dumps(integration,sort_keys=True)+'\n\nPrior files preserved: '+str(len(preserved))+'. Remaining un-run prompts: '+str(remaining)+'.\n\n| Prompt | Supported step | Remaining obligation |\n|---|---|---|\n'+'\n'.join(table)+'\n\nRead-only replay:\n\n    py -3.9 -X utf8 '+B.relative_to(s.ROOT).as_posix()+'/verify_batch.py\n    py -3.9 -X utf8 -O '+B.relative_to(s.ROOT).as_posix()+'/verify_batch.py\n\nAll owned files, including per-node custody attributes, are sealed in manifest.json; the manifest excludes itself. Publication binds a concrete Git tree and independently verifies the merge. AuthorityEffect: None.\n'
paths.update(s.ROOT/p for p in ['scripts/verify_qm_atlas_loc.py', 'scripts/install_qm_atlas_hook.py', 'code/python/tests/test_qm_atlas_loc.py', 'docs/QM_PROBLEM_AND_PROOF_ATLAS.md', 'code/python/src/qm/textbook_problems.py', 'code/rust/src/qm/textbook_problems.rs'])
(B/'README.md').write_bytes(readme.encode());paths.add(s.ROOT/'dag/operads/index.json');paths.update(p for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
s.save(B/'manifest.json',{'scope':'Complete owned source/build, stage, native, review, companion, canonical and custody-attribute seal. Manifest excludes itself.','files':[s.pin(p) for p in sorted(paths) if p!=B/'manifest.json']})
print(json.dumps({'counts':counts,'preserved':len(preserved),'remaining':remaining,'sealed_files':len(paths)}),flush=True)
