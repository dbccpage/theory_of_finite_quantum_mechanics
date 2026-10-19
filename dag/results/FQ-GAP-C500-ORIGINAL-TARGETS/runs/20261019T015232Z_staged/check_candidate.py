"""Bind every ledger claim to retained gap/review bytes; statuses are annotations."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
import yaml
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file());sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import bound,require,load
TASK='FQ-GAP-C500-ORIGINAL-TARGETS'
def snapshot(pin):
    p=(ROOT/pin['snapshot']).resolve();require(p.is_relative_to(ROOT),'G5_SCOPE:path');require(hashlib.sha256(p.read_bytes()).hexdigest()==pin['sha256'],'G5_SCOPE:source_digest');return p
def check(request,candidate):
    _,cert,p=bound(request,candidate,TASK);d=cert['data'];require(type(d) is dict and set(d)=={'blocks','total_targets','source_satisfied_targets','total_clauses','open_or_invalid_clauses','evidence_inventory','ledger_status'},'G1_SCHEMA:data')
    gaps=yaml.safe_load(snapshot(p['gap_source']).read_bytes())['gaps'];all_ids=[];clauses=0;unpaid=0
    require(type(d['blocks']) is list and len(d['blocks'])==len(p['blocks'])==10,'G1_SCHEMA:blocks')
    for i,(public,a,pin) in enumerate(zip(p['blocks'],d['blocks'],p['review_sources']),1):
        review=load(snapshot(pin));gap=next(g for g in gaps if g['gap_id']==f'GAP-C500-B{i:02}')
        require(public['review']==review and public['gap']=={k:gap[k] for k in public['gap']},'G5_SCOPE:raw_source_binding')
        required={'block','gap_status_annotation','gap_resolution_annotation','launch_precondition_annotation','review_scope_annotation','original_targets','clauses','open_or_invalid_clause_ids','target_count','source_satisfied_target_count','clause_counts','original_scope_evidence_ceiling'}
        require(type(a) is dict and set(a)==required and a['block']==review['block']==f'block_{i:02}','G1_SCHEMA:block')
        require(a['original_targets']==review['targets'] and a['clauses']==review['scores'],'G5_SCOPE:original_contract_changed')
        ids=[t['id'] for t in review['targets']];expected=[f'C500-T{300+25*(i-1)+j}' for j in range(1,26)];require(ids==expected==gap['unresolved_targets'],'G3_WITNESS:actual_target_coverage');all_ids+=ids
        require(all(t['plan_target_satisfied'] is False and t['evidence_class']=='OPEN' and t['action'] and t['required_exit_evidence'] for t in review['targets']),'G5_SCOPE:review_status')
        counts=Counter(c['resolution'] for c in review['scores']);open_ids=[c['id'] for c in review['scores'] if c['resolution'] in ('OPEN','INVALID')]
        require(a['open_or_invalid_clause_ids']==open_ids==gap['open_or_invalid_bet_clauses'],'G3_WITNESS:actual_open_clauses')
        require(a['clause_counts']=={k:counts[k] for k in ('SCOPED_EVIDENCE','OPEN','INVALID')} and all(type(v) is int for v in a['clause_counts'].values()),'G1_SCHEMA:clause_counts')
        require(type(a['target_count']) is int and a['target_count']==25 and type(a['source_satisfied_target_count']) is int and a['source_satisfied_target_count']==0,'G3_WITNESS:target_counts')
        require(a['gap_status_annotation']==gap['status'] and a['gap_resolution_annotation']==gap['resolution'] and a['launch_precondition_annotation']==review['launch_preconditions'] and a['review_scope_annotation']==review['supported_scope'] and a['original_scope_evidence_ceiling']=='NOT_DISCHARGED_BY_EXAMINED_RECORDS','G5_SCOPE:scoped_promoted')
        clauses+=len(review['scores']);unpaid+=len(open_ids)
    require(len(all_ids)==len(set(all_ids))==250 and type(d['total_targets']) is int and d['total_targets']==250 and type(d['source_satisfied_targets']) is int and d['source_satisfied_targets']==0 and type(d['total_clauses']) is int and d['total_clauses']==clauses and type(d['open_or_invalid_clauses']) is int and d['open_or_invalid_clauses']==unpaid,'G3_WITNESS:total_counts')
    require(d['evidence_inventory']==p['evidence_inventory'] and type(d['evidence_inventory']) is list,'G5_SCOPE:evidence_inventory_changed')
    for entry in d['evidence_inventory']:
        if entry['available']:snapshot(entry)
        else:require(entry['snapshot'] is None and entry['sha256'] is None,'G5_SCOPE:missing_evidence_fabricated')
    require(d['ledger_status']=='SOURCE_BOUND_SCOPE_MAP_NOT_ORIGINAL_TARGET_DISCHARGE','G5_SCOPE:ledger_promoted')
    return {'blocks':10,'actual_target_records':250,'actual_reviewed_clauses':clauses,'open_or_invalid_clauses':unpaid,'scope':'Source-bound original-contract map only; no original target discharge or replay of every cited campaign computation.'}
if __name__=='__main__':print(json.dumps(check(*sys.argv[1:]),indent=2))
