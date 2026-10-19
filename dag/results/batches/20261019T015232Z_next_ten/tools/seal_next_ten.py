"""Seal the completed run reviews and batch inventory without rewriting attempts."""
import hashlib,importlib.util,json,shutil,sys
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');BATCH=ROOT/'dag/results/batches/20261019T015232Z_next_ten';STAGING=Path(__file__).resolve().parent;REVIEW='20261019_next_ten_audit'
sp=importlib.util.spec_from_file_location('s',BATCH/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
if json.loads((BATCH/'summary.json').read_bytes())['status']!='all_ten_staged_runs_reviewed':raise ValueError('Review not complete')
receipt=json.loads((BATCH/'review/validation/final_structure/structure_receipt.json').read_bytes())
if receipt['exit_code']!=0:raise ValueError('Final structure did not pass')
structure=json.loads((BATCH/'review/validation/final_structure/structure.stdout.log').read_bytes())
if structure['errors'] or structure['prompts']!=177:raise ValueError('Final corpus changed')
protocol=(BATCH/'review/final_integration/protocol.stderr.log').read_text()
if 'Ran 12 tests' not in protocol or not protocol.rstrip().endswith('OK'):raise ValueError('Protocol suite is incomplete')
shutil.copyfile(STAGING/'seal_next_ten.py',BATCH/'tools/seal_next_ten.py')
rows=json.loads((BATCH/'selection.json').read_bytes())['nodes'];review_manifests=[]
for n in rows:
    review=ROOT/'dag/results'/n['node_id']/'reviews'/REVIEW;collection=ROOT/n['operad_collection'];shutil.copyfile(collection,review/'collection_after_review.yaml')
    artifacts=[{'path':p.relative_to(review).as_posix(),'sha256':s.sha(p)} for p in sorted(review.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json']
    manifest={'schema_id':'finite-qm.scoped-review-manifest.v1','task_id':n['node_id'],'artifacts':artifacts,'canonical_collection':{'path':n['operad_collection'],'sha256':s.sha(collection),'snapshot':'collection_after_review.yaml'},'scope':'Snapshot and replay custody; no independent author or complete transitive dependency attestation.'}
    s.save(review/'manifest.json',manifest);review_manifests.append({'path':(review/'manifest.json').relative_to(ROOT).as_posix(),'sha256':s.sha(review/'manifest.json')})
sources={p['path'] for p in json.loads((BATCH/'review/final_integration/plan.json').read_bytes())['source_pins']}
sources.update(n['operad_collection'] for n in rows);sources.update(['dag/operads/index.json','dag/pfp/exact_json.py','dag/pfp/review_exact_json.py','dag/pfp/prepare_stage.py','dag/pfp/validate_prompts.py','dag/pfp/test_staged_prompts.py'])
pins=[]
for name in sorted(sources):
    src=ROOT/name;target=BATCH/'final_sources'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target);pins.append({'path':name,'sha256':s.sha(src),'snapshot':target.relative_to(BATCH).as_posix()})
artifacts=[{'path':p.relative_to(BATCH).as_posix(),'sha256':s.sha(p)} for p in sorted(BATCH.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p!=BATCH/'manifest.json']
s.save(BATCH/'manifest.json',{'schema_id':'finite-qm.reviewed-staged-batch-manifest.v1','base_commit':'e6ce7b0970d4609bbdde95c2bd418b8600533bc4','artifacts':artifacts,'review_manifests':review_manifests,'working_sources':pins,'scope':'Exact local source, stage and receipt inventory; no mathematical theorem follows from this hash manifest.'})
print(json.dumps({'batch_artifacts':len(artifacts),'reviews':len(review_manifests),'final_source_pins':len(pins)}))
