"""Bind the source-lead repair to real Git blobs and retain infrastructure scope."""
from pathlib import Path
B=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics\dag\results\batches\20261019T201403Z_prompts_72_91')
p=B/'verify_batch.py';t=p.read_text().replace('import hashlib,importlib.util,json,re,sys,yaml','import hashlib,importlib.util,json,re,sys,yaml,subprocess,copy')
needle='    total=0;records=0;anchors=set();failed=0'
insert='''    base=load(BATCH/'selection.json')['base_commit']
    for commit,field in [(successor['historical_commit'],'historical_snapshot'),(base,'current_snapshot')]:
        blob=subprocess.check_output(['git','show',commit+':'+successor['source_path']],cwd=ROOT)
        require(blob==(ROOT/successor[field]).read_bytes(),'source successor differs from real Git blob')
    require(successor['current_commit']==base,'successor is not the selected base')
    old_collection=yaml.safe_load((BATCH/'custody/majorana_collection_before.yaml').read_bytes())
    original_blob=subprocess.check_output(['git','show',base+':dag/operads/ds_qm212_majorana_problem.yaml'],cwd=ROOT)
    require(yaml.safe_load(original_blob)==old_collection,'original collection differs from Git base')
    expected_collection=copy.deepcopy(old_collection)
    for binding in expected_collection['source_bindings']:
        if binding.get('repository')=='this_repository' and binding.get('path')==successor['source_path']:
            require(binding['sha256']==successor['historical_sha256'],'original source pin differs')
            binding['sha256']=successor['current_sha256']
    expected_collection['source_pin_successors'].append({'path':successor['source_path'],'historical_sha256':successor['historical_sha256'],'current_sha256':successor['current_sha256'],'review':(BATCH/'custody/majorana_source_successor.json').relative_to(ROOT).as_posix(),'role':'source_lead_only','authority_effect':'None'})
    majorana=next(row for row in rows if row['node_id']=='DS-QM212-MAJORANA-PROBLEM')
    active=ROOT/majorana['run']/'inputs_after_source_review/this_repository'/majorana['operad_collection']
    require(yaml.safe_load(active.read_bytes())==expected_collection,'undeclared source collection change')
'''
if needle not in t:raise ValueError('Unexpected verifier state')
t=t.replace(needle,insert+needle)
needle="        host=load(h/'host_check.json');"
insert='''        for incomplete in accepted.get('infrastructure_checkpoints',[]):
            partial=load(run/incomplete/'host_check.json')
            require(partial['status']=='infrastructure_recording_failure' and partial['predicate_results']['native_exit_codes']['rust'] is None,'incomplete IO gate promoted')
'''
t=t.replace(needle,insert+needle);p.write_bytes(t.encode())
p=B/'tools/finalize.py';t=p.read_text().replace("'retained_failed_checkpoints':0,","'retained_failed_checkpoints':0,'retained_incomplete_native_checkpoints':0,'preparation_failures_retained':3,")
t=t.replace('    for key,field in',"    counts['retained_incomplete_native_checkpoints']+=len(acc.get('infrastructure_checkpoints',[]))\n    for key,field in");p.write_bytes(t.encode())
(B/'tools/strengthen_review.py').write_bytes(Path(__file__).read_bytes())
