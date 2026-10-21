def _cell(value):
    if value is True:
        return '1'
    if value is False:
        return '0'
    if isinstance(value, list):
        return ','.join('%d' % x for x in value) or '-'
    return str(value)


ORDER = ['is_subcomplex', 'dims_D', 'dims_C', 'betti_C', 'betti_D', 'rank_hi', 'killed', 'h_injective', 'retraction_exists',
         'system_rank', 'augmented_rank']


def lines(data):
    return ['\t'.join(['chain', r['name']] + [_cell(r[f]) for f in ORDER]) for r in data['records']]
