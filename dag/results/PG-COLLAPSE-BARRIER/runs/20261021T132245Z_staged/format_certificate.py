def lines(data):
    out = []
    for r in data['records']:
        hist = ';'.join('%d:%d' % (e[0], e[1]) for e in r['min_tag_hist']) or '-'
        fields = ['tag', str(r['input'][0]), str(r['input'][1]), str(r['input'][2]), str(r['total']), str(r['fibre_constant']),
                  str(r['collapsed_separated']), str(r['factoring']), str(r['factorizations']), str(r['violations']), hist]
        out.append('\t'.join(fields))
    return out
