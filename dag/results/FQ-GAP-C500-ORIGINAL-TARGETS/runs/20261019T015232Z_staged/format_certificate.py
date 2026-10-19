def lines(data):
    return ['\t'.join([b['block'],str(b['target_count']),str(b['source_satisfied_target_count'])]+[str(b['clause_counts'][k]) for k in ('SCOPED_EVIDENCE','OPEN','INVALID')]+[t['id'].removeprefix('C500-T') for t in b['original_targets']]+b['open_or_invalid_clause_ids']) for b in data['blocks']]+['ledger_status\t'+data['ledger_status']]
