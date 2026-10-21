CLASSIFY = ['relations', 'law_bearing', 'cut_relations', 'cut_triples', 'instance_without_law', 'law_without_instance',
            'related_equal', 'related_distinct', 'unrelated_equal', 'unrelated_distinct', 'irreflexive_related_equal']
IDENTIFY = ['rq_pairs', 'rq_with_target', 'rq_identifying', 'rq_overlap', 'cut_q', 'cut_q_with_target',
            'cut_q_identified', 'cut_q_identified_with_target']


def lines(data):
    out = []
    for r in data['records']:
        names = CLASSIFY if r['kind'] == 'classify' else IDENTIFY
        out.append('\t'.join([r['kind'], '%d' % r['n']] + ['%d' % r[k] for k in names]))
    return out
