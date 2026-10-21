def lines(data):
    def b(x):
        return '1' if x else '0'

    out = []
    for r in data['records']:
        i = r['input']
        k = r['kind']
        if k == 'prod':
            out.append('\t'.join(['prod', '%d' % i[1], '%d' % i[2], '%d' % i[3], ','.join(r['RAB']), ','.join(r['RAstar']), ','.join(r['RA_interleaved']),
                                  b(r['interleaved_commutes_block_J']), b(r['mult_ok']), b(r['intertwine_ok']),
                                  b(r['imul_ok']), b(r['star_ok']), b(r['roundtrip_ok']), r['hermitian'], r['symmetric_RA'],
                                  r['trace_real'], r['trace_complex'], r['trace_identity'], r['trace_twice_complex']]))
        elif k == 'img':
            rec = ';'.join(r['recovered']) if r['recovered'] else '-'
            out.append('\t'.join(['img', '%d' % i[1], '%d' % i[2], r['status'], r['commutes'], r['anticommutes'], r['symmetric'], r['hermitian'], rec]))
        elif k == 'psd':
            out.append('\t'.join(['psd', '%d' % i[1], r['hermitian'], r['complex_psd'], r['real_psd'], r['agree']]))
        elif k == 'jstruct':
            out.append('\t'.join(['jstruct', '%d' % i[1], '%d' % i[2], '%d' % i[3], '%d' % i[4], b(r['sq_neg_id']), b(r['pm_J']), b(r['commutes_J'])]))
        else:
            out.append('\t'.join(['jcensus', '%d' % i[1], '%d' % r['total'], '%d' % r['commuting_J'], '%d' % r['pm_J']]))
    return out
