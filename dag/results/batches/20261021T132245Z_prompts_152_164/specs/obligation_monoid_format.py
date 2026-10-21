ORDER = {
    'laws': ['elements', 'triples', 'assoc_failures', 'comm_failures', 'unit_failures', 'cancel_failures', 'invertible_nonzero'],
    'bounded': ['elements', 'pairs', 'defined_pairs', 'overflow_pairs', 'triples', 'defined_triples', 'definedness_mismatch', 'value_mismatch'],
    'saturating': ['elements', 'triples', 'assoc_failures', 'comm_failures', 'unit_failures', 'cancel_failures'],
    'events': ['terms', 'assertions', 'destructive', 'cost', 'length', 'valid_fresh', 'declare_then_assert', 'perm_count',
               'perm_trace_failures', 'split_failures'],
    'ledger': ['status', 'fail_index', 'generated', 'discharged', 'outstanding', 'settled'],
}


def _cell(value):
    if value is True:
        return '1'
    if value is False:
        return '0'
    if isinstance(value, list):
        return ','.join('%d' % x for x in value)
    return str(value)


def lines(data):
    out = []
    for r in data['records']:
        cells = [r['kind']] + [str(a) for a in r['args']] + [_cell(r[f]) for f in ORDER[r['kind']]]
        out.append('\t'.join(cells))
    return out
