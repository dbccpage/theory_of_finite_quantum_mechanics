"""Source-bound original-target ledger; source status is not a discharge proof."""
import copy

def _mapping(value, fields, role):
    if type(value) is not dict or not fields <= value.keys():
        raise ValueError(f'{role}: mapping with required fields expected')
    return value

def _records(value, fields, role):
    if type(value) not in (list, tuple):
        raise ValueError(f'{role}: record sequence required')
    for row in value:
        _mapping(row, fields, role)
        if type(row['id']) is not str or not row['id']:
            raise ValueError(f'{role}: nonempty text id required')
    return value

def summarize(block):
    block=_mapping(block,{'review','gap'},'block')
    review=_mapping(block['review'],{'targets','scores','block','launch_preconditions','supported_scope'},'review')
    gap=_mapping(block['gap'],{'open_or_invalid_bet_clauses','unresolved_targets','status','resolution'},'gap')
    targets=_records(review['targets'],{'id','plan_target_satisfied','action','required_exit_evidence'},'targets')
    scores=_records(review['scores'],{'id','resolution'},'scores')
    if not targets or len({t['id'] for t in targets})!=len(targets):raise ValueError('distinct target records required')
    if len({c['id'] for c in scores})!=len(scores) or any(c['resolution'] not in ('SCOPED_EVIDENCE','OPEN','INVALID') for c in scores):raise ValueError('actual distinct reviewed clauses required')
    if any(type(t['plan_target_satisfied']) is not bool or not t['action'] or not t['required_exit_evidence'] for t in targets):raise ValueError('typed original target contract required')
    clauses=[c['id'] for c in scores if c['resolution'] in ('OPEN','INVALID')]
    if clauses!=gap['open_or_invalid_bet_clauses'] or [t['id'] for t in targets]!=gap['unresolved_targets']:raise ValueError('source gap/review identity mismatch')
    satisfied=sum(t['plan_target_satisfied'] for t in targets)
    return {'block':review['block'],'gap_status_annotation':gap['status'],'gap_resolution_annotation':gap['resolution'],'launch_precondition_annotation':review['launch_preconditions'],'review_scope_annotation':review['supported_scope'],'original_targets':copy.deepcopy(targets),'clauses':copy.deepcopy(scores),'open_or_invalid_clause_ids':clauses,'target_count':len(targets),'source_satisfied_target_count':satisfied,'clause_counts':{k:sum(c['resolution']==k for c in scores) for k in ('SCOPED_EVIDENCE','OPEN','INVALID')},'original_scope_evidence_ceiling':'NOT_DISCHARGED_BY_EXAMINED_RECORDS' if satisfied==0 else 'SOURCE_LABEL_REQUIRES_INDEPENDENT_PROOF'}
def certify(blocks,evidence_inventory):
    rows=[summarize(b) for b in blocks];ids=[t['id'] for r in rows for t in r['original_targets']]
    if len(ids)!=len(set(ids)):raise ValueError('duplicate target across blocks')
    return {'blocks':rows,'total_targets':len(ids),'source_satisfied_targets':sum(r['source_satisfied_target_count'] for r in rows),'total_clauses':sum(sum(r['clause_counts'].values()) for r in rows),'open_or_invalid_clauses':sum(r['clause_counts']['OPEN']+r['clause_counts']['INVALID'] for r in rows),'evidence_inventory':copy.deepcopy(evidence_inventory),'ledger_status':'SOURCE_BOUND_SCOPE_MAP_NOT_ORIGINAL_TARGET_DISCHARGE'}
