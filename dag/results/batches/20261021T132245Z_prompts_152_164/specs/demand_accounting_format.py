LISTREG_FIELDS = ['total', 'identity_holds', 'nodup_inputs', 'disjoint_inputs', 'nodup_when_disjoint', 'nodup_when_overlap']


def lines(data):
    out = []
    for r in data['records']:
        if r['kind'] == 'demand':
            out.append('\t'.join(['demand', str(r['u']), str(r['total'])] + ['%d:%d:%d' % (c[0], c[1], c[2]) for c in r['classes']]))
        elif r['kind'] == 'sequence':
            out.append('\t'.join(['sequence', ','.join(str(x) for x in r['seq']), ','.join(str(x) for x in r['decompositions']),
                                  str(int(r['underdetermined']))]))
        else:
            out.append('\t'.join(['listreg'] + [str(x) for x in r['input']] + [str(r[k]) for k in LISTREG_FIELDS]))
    return out
