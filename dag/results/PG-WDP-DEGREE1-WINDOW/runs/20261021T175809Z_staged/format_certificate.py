def lines(data):
    out = []
    for r in data['records']:
        dim_h1 = '-' if r['dim_h1'] is None else str(r['dim_h1'])
        gamma2 = '-' if r['gamma2'] is None else r['gamma2']
        r_cl = '-' if r['r_cl'] is None else r['r_cl']
        wit = '-' if r['kappa_witness'] is None else r['kappa_witness']
        out.append('\t'.join(['window', r['id'], str(r['nv']), str(r['m']), str(r['k']), str(r['rank_d0']), str(r['rank_d1']),
                              str(1 if r['complex'] else 0), str(r['dim_q1']), dim_h1, r['phi1'], gamma2, r_cl, r['diag'], wit, r['witness']]))
    return out
