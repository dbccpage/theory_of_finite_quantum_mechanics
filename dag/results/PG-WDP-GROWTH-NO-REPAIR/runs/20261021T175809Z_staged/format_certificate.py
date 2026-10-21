def _cell(value):
    return '-' if value is None else str(value)


def lines(data):
    out = []
    for r in data['records']:
        out.append('\t'.join(['pair', r['id'], r['kind'], str(r['m_a']), str(r['m_b']), str(r['k_a']), str(r['k_b']),
                              str(1 if r['complex_a'] else 0), str(1 if r['complex_b'] else 0), r['phi_a'], r['phi_b'],
                              _cell(r['gamma_a']), _cell(r['gamma_b']), r['diag_a'], r['diag_b'], r['verdict'],
                              r['witness_a'], r['witness_b']]))
    return out
