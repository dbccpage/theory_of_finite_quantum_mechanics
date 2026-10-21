def lines(data):
    out = []
    for r in data['records']:
        hist = ';'.join('%d:%d' % (p[0], p[1]) for p in r['image_hist']) or '-'
        fields = ['report', str(r['input'][0]), str(r['input'][1]), str(r['input'][2]), str(r['pairs']), str(r['fiber_constant']),
                  str(r['factoring']), str(r['mismatch']), hist, str(r['max_factor_multiplicity']), str(r['extensions_total']),
                  str(r['nonunique_off_image']), str(r['surjective_reports']), str(r['surjective_nonunique'])]
        out.append('\t'.join(fields))
    return out
