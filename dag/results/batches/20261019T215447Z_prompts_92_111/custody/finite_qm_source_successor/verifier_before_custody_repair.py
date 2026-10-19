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
    require(sha(BATCH/'index_before.json')==load(BATCH/'selection.json')['index_sha256'],'selection index seal')
    require(subprocess.check_output(['git','show',load(BATCH/'selection.json')['base_commit']+':dag/operads/index.json'],cwd=ROOT)==(BATCH/'index_before.json').read_bytes(),'selection index differs from Git base')
    require([r['node_id'] for r in rows]==[r['node_id'] for r in before['nodes'][91:111]],'ordered next-twenty selection')
    require([n for n in before['nodes'] if n['node_id'] not in ids]==[n for n in current['nodes'] if n['node_id'] not in ids],'unrelated index row changed')
    sys.path.insert(0,str(ROOT/'dag/pfp'))
    from custody import Custody
    custody=Custody(ROOT)
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
                require(sha(live)==pin['sha256'],'accepted native working bytes drift')
        axiom_reports((h/'native/lean.stdout.log').read_text(),profile['lean_anchors']);anchors.update(profile['lean_anchors'])
        wire=module('wire'+str(i),run/'format_certificate.py');require(wire.lines(c['data'])==(h/'native/rust_replay.stdout.log').read_text().splitlines(),'exact complete cross-language output')
        mutants=load(run/'p4/host_check.json')['predicate_results']['mutants'];require(len(mutants)==4+sum(len(r['output']) for r in c['data']['records']),'every-coordinate challenge coverage')
        for mutant in mutants:
            try:checker.check(a/'request.json',run/mutant['path'])
            except ValueError:pass
            else:raise ValueError('Mutant accepted '+mutant['id'])
        total+=len(mutants)
        for source in load(run/'p0/source_inventory.json')['source_records']+(load(run/'p0/additional_source_inventory.json')['source_records'] if (run/'p0/additional_source_inventory.json').exists() else []):
            require(source['available'],'missing source')
            require(sha(ROOT/source['snapshot'])==source['actual_sha256'],'source custody')
            if source['recorded_sha256'] and source['recorded_sha256']!=source['actual_sha256']:
                require(custody.matches('paper',source['source_path'],source['recorded_sha256'],task),'unresolved historical pin')
                require(source.get('custody_ledger_sha256')==sha(ROOT/'dag/pfp/filename_custody.json'),'migration ledger custody')
        review=run.parent.parent/'reviews/20261019_genesis_impl_audit'
        for pin in load(review/'run_manifest.json')['artifacts']:require(sha(run/pin['path'])==pin['sha256'],'retained stage artifact changed')
        delta=yaml.safe_load((review/'operad_delta.yaml').read_bytes())
        for target,field in [('generators','add_or_refine_generators'),('relations','add_or_refine_relations'),('compositions','checked_compositions'),('failed_compositions','failed_compositions'),('counterexamples','counterexamples')]:
            require(collection['presentation'][target]==delta[field],'reviewed operad presentation drift '+target)
        genes={g['id']:g for g in delta['add_or_refine_generators']};relation_ids={q['id'] for q in delta['add_or_refine_relations']}
        for g in genes.values():require(g['arity']==len(g['ordered_inputs']) and bool(g['hypotheses']),'operation arity or hypotheses missing')
        for composition in delta['checked_compositions']:
            outer=genes[composition['outer_operation']];inner=genes[composition['inner_operation']]
            require(outer['ordered_inputs'][composition['input_slot']]==inner['output'],'ill-typed reviewed graft')
            require(set(composition['licensing_relations'])<=relation_ids and bool(composition['hypothesis_match']),'unlicensed reviewed graft')
        ambient=collection['operad_slots']['slot_m1_layer0_ambient_carrier']
        expected_hypotheses=list(dict.fromkeys(hyp for g in delta['add_or_refine_generators'] for hyp in g['hypotheses']))
        require(ambient['work_unit_admitted_hypotheses']==expected_hypotheses,'unpaid work-unit hypotheses lost')
        require(ambient['admitted_assumptions']==list(dict.fromkeys(ambient['historical_source_assumptions']+expected_hypotheses)),'assumptions silently removed')
        if load(run/'public_input.json')['kind']=='mss0':require('stage_floor_only' in delta['review_scope_clarifications'] and any('Higher-stage' in o for o in collection['open_obligations']),'MSS0 scope correction lost')
        if load(run/'public_input.json')['kind']=='float':require('policy_field_only' in delta['review_scope_clarifications'],'f64 enforcement boundary lost')
        require(len(collection['stage_history'])==len({s['attempt'] for s in collection['stage_history']}),'duplicate historical checkpoint')
        require({stage['attempt'] for stage in collection['stage_history']}=={p.parent.name for p in run.glob('*/request.json')},'complete stage history')
        print(json.dumps({'task_id':task,'exact_records':result['records_checked'],'rejected_P4_mutations':len(mutants),'named_prompt_anchors':len(profile['lean_anchors']),'remaining':profile['claim_boundary']['does_not_support']}))
    print(json.dumps({'runs':len(rows),'exact_records':records,'rejected_P4_mutations':total,'unique_named_prompt_anchors':len(anchors),'retained_failed_checkpoints':failed,'scope':'Read-only replay; saved native/kernel receipts checked, compilers not rerun.'}))
if __name__=='__main__':main()
