"""Read-only sealed exact replay. Does not rerun compilers or promote targets."""
import hashlib,importlib.util,json,re,sys,tempfile,copy
from pathlib import Path
sys.dont_write_bytecode=True
BATCH=Path(__file__).resolve().parent
ROOT=next(p for p in BATCH.parents if (p/'dag/pfp/prepare_stage.py').is_file())
def load(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def module(name,p):
    sp=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def axiom_reports(text,anchors):
    reports=re.findall(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",text)
    matches=[(n,a) for n,a in reports if n in anchors]
    require(len(matches)==len(anchors) and {n for n,_ in matches}==set(anchors),'named anchor coverage')
    require('sorryAx' not in text,'compiler recovery proof')
    for _,a in matches:require({v.strip() for v in a.split(',') if v.strip()}<={'propext','Classical.choice','Quot.sound'},'unexpected axiom')
def main():
    if (BATCH/'manifest.json').exists():
        for pin in load(BATCH/'manifest.json')['files']:require(sha(ROOT/pin['path'])==pin['sha256'],'sealed bytes '+pin['path'])
    selected=load(BATCH/'selection.json');base=load(BATCH/'index_before.json');current=load(ROOT/'dag/operads/index.json')
    rows=selected['nodes'];require([r['node_id'] for r in rows]==[r['node_id'] for r in base['nodes'][11:21]],'ordered selection')
    ids={r['node_id'] for r in rows}
    require([n for n in base['nodes'] if n['node_id'] not in ids]==[n for n in current['nodes'] if n['node_id'] not in ids],'unrelated index changes')
    total=0;anchors=set();records=0
    for i,node in enumerate(rows):
        task=node['node_id'];run=ROOT/node['run'];checker=module('checker_'+str(i),run/'check_candidate.py');profile=load(run/'p0/profile.json');a=run/'p3b';candidate=load(a/'candidate.json')
        import yaml
        original=yaml.safe_load((run/'inputs/this_repository'/node['operad_collection']).read_bytes());collection=yaml.safe_load((ROOT/node['operad_collection']).read_bytes())
        for key in ('target','source_bindings','source_provenance','collection_status'):require(collection[key]==original[key],'historical/source claim changed '+key)
        result=checker.check(a/'request.json',a/'candidate.json');records+=result['records_checked']
        require(candidate['data']==load(run/'p1/candidate.json')['data']==load(run/'p3/candidate.json')['data'],'proof repair changed numeric data')
        for old in ('p2','p2_after_p3'):
            h=load(run/old/'host_check.json');require(h['status']=='repairable_candidate_defect' and h['predicate_results']['native_exit_codes']['lean']!=0,'failed attempt promoted')
        h=load(run/'p2_after_p3b/host_check.json');require(h['status']=='accepted_candidate_for_challenge' and all(v==0 for v in h['predicate_results']['native_exit_codes'].values()),'accepted native gate')
        require(h['candidate_sha256']==sha(a/'candidate.json'),'host candidate binding')
        for r in (run/'p2_after_p3b/native').glob('*_receipt.json'):
            receipt=load(r);require(receipt['exit_code']==0 and receipt['sources_unchanged'],'accepted receipt exit/source')
        axiom_reports((run/'p2_after_p3b/native/lean.stdout.log').read_text(),profile['lean_anchors']);anchors.update(profile['lean_anchors'])
        wire=module('wire_'+str(i),run/'format_certificate.py');require((run/'p2_after_p3b/native/rust_replay.stdout.log').read_text().splitlines()==wire.lines(candidate['data']),'full Rust output')
        outcomes=load(run/'p4/host_check.json')['predicate_results']['mutants']
        for m in outcomes:
            try:checker.check(a/'request.json',run/m['path'])
            except ValueError:pass
            else:raise ValueError('mutant accepted '+m['id'])
        total+=len(outcomes)
        for source in load(run/'p0/source_inventory.json')['source_records']:
            if source['available']:require(sha(ROOT/source['snapshot'])==source['actual_sha256'],'original source snapshot')
        review=run.parent.parent/'reviews/20261019_scope_audit'
        for p in load(review/'run_manifest.json')['artifacts']:require(sha(run/p['path'])==p['sha256'],'staged artifact changed')
        print(json.dumps({'task_id':task,'exact_records':result['records_checked'],'rejected_coordinate_and_schema_mutations':len(outcomes),'Lean_anchors':len(profile['lean_anchors']),'remaining':profile['claim_boundary']['does_not_support']}))
    print(json.dumps({'runs':len(rows),'records':records,'rejected_P4_mutations':total,'unique_new_kernel_anchors':len(anchors),'scope':'Read-only exact replay and saved receipt verification; no fresh compiler execution.'}))
if __name__=='__main__':main()
