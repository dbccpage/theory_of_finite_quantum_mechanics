"""Read-only exact replay and artifact custody, not a fresh compiler invocation."""
import hashlib,importlib.util,json,re,sys,yaml,subprocess,copy
from pathlib import Path
sys.dont_write_bytecode=True
BATCH=Path(__file__).resolve().parent;ROOT=next(p for p in BATCH.parents if (p/'dag/pfp/prepare_stage.py').is_file())
def load(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def module(name,p):
    sp=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def axiom_reports(text,anchors):
    reports=re.findall(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",text);matches=[(n,a) for n,a in reports if n in anchors]
    require(len(matches)==len(anchors) and {n for n,_ in matches}==set(anchors),'named kernel report coverage');require('sorryAx' not in text,'recovery proof rejected')
    for _,a in matches:require({s.strip() for s in a.split(',') if s.strip()}<={'propext','Classical.choice','Quot.sound'},'unexpected axiom')
def main():
    if (BATCH/'manifest.json').exists():
        for p in load(BATCH/'manifest.json')['files']:require(sha(ROOT/p['path'])==p['sha256'],'sealed artifact changed '+p['path'])
    rows=load(BATCH/'selection.json')['nodes'];before=load(BATCH/'index_before.json');current=load(ROOT/'dag/operads/index.json');ids={r['node_id'] for r in rows}
    require([r['node_id'] for r in rows]==[r['node_id'] for r in before['nodes'][71:91]],'ordered next-twenty selection')
    require([n for n in before['nodes'] if n['node_id'] not in ids]==[n for n in current['nodes'] if n['node_id'] not in ids],'unrelated index row changed')
    sys.path.insert(0,str(ROOT/'dag/pfp'))
    from custody import Custody
    custody=Custody(ROOT)
    successor=load(BATCH/'custody/majorana_source_successor.json')
    for field,key in [('historical_snapshot','historical_sha256'),('current_snapshot','current_sha256')]:require(sha(ROOT/successor[field])==successor[key],'Majorana source successor bytes')
    require((ROOT/successor['source_path']).read_bytes()==(ROOT/successor['current_snapshot']).read_bytes(),'Majorana current source drift')
    base=load(BATCH/'selection.json')['base_commit']
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
    repair=load(BATCH/'source_repair/anticommutator.json')
    rb=(ROOT/repair['before_snapshot']).read_bytes();ra=(ROOT/repair['after_snapshot']).read_bytes()
    require(sha(ROOT/repair['before_snapshot'])==repair['before_sha256'] and sha(ROOT/repair['after_snapshot'])==repair['after_sha256'],'Rust source successor hashes')
    old=repair['exact_replacement']['before'].encode();new=repair['exact_replacement']['after'].encode()
    require(rb.count(old)==1 and rb.replace(old,new)==ra and (ROOT/repair['source_path']).read_bytes()==ra,'Rust successor is not the exact declared sign repair')
    total=0;records=0;anchors=set();failed=0
    for i,node in enumerate(rows):
        task=node['node_id'];run=ROOT/node['run'];accepted=load(run/'accepted.json');a=run/accepted['attempt'];h=run/accepted['host'];c=load(a/'candidate.json');profile=load(run/'p0/profile.json')
        checker=module('exact_checker'+str(i),run/'check_candidate.py');result=checker.check(a/'request.json',a/'candidate.json');records+=result['records_checked']
        inventory=load(run/'p0/source_inventory.json')['source_records'];captured=next(p for p in inventory if p['repository']=='this_repository' and p['source_path']==node['operad_collection']);original=yaml.safe_load((ROOT/captured['snapshot']).read_bytes());collection=yaml.safe_load((ROOT/node['operad_collection']).read_bytes())
        for key in ('target','source_bindings','source_provenance','collection_status'):require(original[key]==collection[key],'historical claim mutated '+key)
        for attempt in load(run/'p1/review_contract.json')['attempts']:require(load(run/attempt/'candidate.json')['data']==c['data'],'numeric certificate altered by proof repair')
        for checkpoint in accepted['failed_checkpoints']:
            old=load(run/checkpoint/'host_check.json');require(old['status']=='repairable_candidate_defect' and any(v!=0 for v in old['predicate_results']['native_exit_codes'].values()),'failed gate promoted');failed+=1
        for incomplete in accepted.get('infrastructure_checkpoints',[]):
            partial=load(run/incomplete/'host_check.json')
            require(partial['status']=='infrastructure_recording_failure' and partial['predicate_results']['native_exit_codes']['rust'] is None,'incomplete IO gate promoted')
        host=load(h/'host_check.json');require(host['status']=='accepted_candidate_for_challenge' and host['candidate_sha256']==sha(a/'candidate.json'),'accepted candidate binding')
        require(all(v==0 for v in host['predicate_results']['native_exit_codes'].values()),'accepted failed native gate')
        for receipt in (h/'native').glob('*_receipt.json'):
            r=load(receipt);require(r['sources_unchanged'] and r['exit_code']==0,'accepted native receipt')
            for pin in r['source_pins']:
                live=Path(pin['path'])
                if live==(ROOT/repair['source_path']) and pin['sha256']==repair['before_sha256']:
                    require(sha(ROOT/repair['before_snapshot'])==pin['sha256'],'historical accepted Rust bytes drift')
                else:require(sha(live)==pin['sha256'],'accepted native working bytes drift')
        axiom_reports((h/'native/lean.stdout.log').read_text(),profile['lean_anchors']);anchors.update(profile['lean_anchors'])
        wire=module('wire'+str(i),run/'format_certificate.py');require(wire.lines(c['data'])==(h/'native/rust_replay.stdout.log').read_text().splitlines(),'exact complete cross-language output')
        mutants=load(run/'p4/host_check.json')['predicate_results']['mutants'];require(len(mutants)==4+sum(len(r['output']) for r in c['data']['records']),'every-coordinate challenge coverage')
        for mutant in mutants:
            try:checker.check(a/'request.json',run/mutant['path'])
            except ValueError:pass
            else:raise ValueError('Mutant accepted '+mutant['id'])
        total+=len(mutants)
        for source in load(run/'p0/source_inventory.json')['source_records']:
            require(source['available'],'missing source')
            require(sha(ROOT/source['snapshot'])==source['actual_sha256'],'source custody')
            if source['recorded_sha256'] and source['recorded_sha256']!=source['actual_sha256']:
                require(custody.matches('paper',source['source_path'],source['recorded_sha256'],task),'unresolved historical pin')
                require(source.get('custody_ledger_sha256')==sha(ROOT/'dag/pfp/filename_custody.json'),'migration ledger custody')
        review=run.parent.parent/'reviews/20261019_boundaries_audit'
        for pin in load(review/'run_manifest.json')['artifacts']:require(sha(run/pin['path'])==pin['sha256'],'retained stage artifact changed')
        require({stage['attempt'] for stage in collection['stage_history']}=={p.parent.name for p in run.glob('*/request.json')},'complete stage history')
        print(json.dumps({'task_id':task,'exact_records':result['records_checked'],'rejected_P4_mutations':len(mutants),'named_prompt_anchors':len(profile['lean_anchors']),'remaining':profile['claim_boundary']['does_not_support']}))
    print(json.dumps({'runs':len(rows),'exact_records':records,'rejected_P4_mutations':total,'unique_named_prompt_anchors':len(anchors),'retained_failed_checkpoints':failed,'scope':'Read-only replay; saved native/kernel receipts checked, compilers not rerun.'}))
if __name__=='__main__':main()
