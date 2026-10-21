def _cell(value):
    if value is None:
        return '-'
    if value is True:
        return '1'
    if value is False:
        return '0'
    return str(value)


ORDER = ['complex', 'm', 'rank_d0', 'rank_d1', 'dim_q1', 'dim_h1', 'dim_im', 'exact_dims', 'section_dim', 'canonical_split',
         'class_zero', 'norm_ok', 'phi1', 'gamma2', 'diag', 'classes_hit', 'opnorm', 'bound_holds', 'phi_zero_iff_class_zero', 'witness']


def lines(data):
    return ['\t'.join(['seq', r['id']] + [_cell(r[k]) for k in ORDER]) for r in data['records']]
