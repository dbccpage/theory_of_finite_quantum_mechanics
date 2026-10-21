def lines(data):
    def ints(xs):
        return ','.join('%d' % x for x in xs)

    out = []
    for r in data['records']:
        i = r['input']
        if r['kind'] == 'residual':
            vecs = ';'.join(ints(v) for v in r['sector_vectors'])
            out.append('\t'.join(['residual', '%d' % i[1], ints(i[2]), ints(i[3]), '%d' % r['holonomy'], '%d' % r['phi1'],
                                  '%d' % r['minimizer_count'], ints(r['lex_min']), ints(r['lex_max']), vecs,
                                  '1' if r['determined'] else '0', '1' if r['unique'] else '0',
                                  '%d/%d' % (r['symmetric'][0], r['symmetric'][1]),
                                  '1' if r['symmetric_integral'] else '0', '%d' % r['sumsq_min'], '%d' % r['sumsq_max'], r['status']]))
        elif r['kind'] == 'weighted':
            vecs = ';'.join(ints(v) for v in r['sector_vectors'])
            out.append('\t'.join(['weighted', '%d' % i[1], ints(i[2]), ints(i[3]), ints(i[4]), '%d' % r['holonomy'], '%d' % r['weighted_phi1'],
                                  '%d' % r['minimizer_count'], ints(r['lex_min']), ints(r['lex_max']), vecs,
                                  '1' if r['determined'] else '0', '1' if r['unique'] else '0', r['status']]))
        else:
            out.append('\t'.join(['twocycle', '%d' % i[1], ints(i[2]), '%d' % i[3], ints(i[4]), ints(r['holonomies']), '%d' % r['phi1'],
                                  '%d' % r['minimizer_count'], '%d' % r['total_holonomy'], '1' if r['total_gives_phi1'] else '0']))
    return out
