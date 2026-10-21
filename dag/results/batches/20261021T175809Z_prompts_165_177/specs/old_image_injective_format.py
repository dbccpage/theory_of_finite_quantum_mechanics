FIELDS = ['pairs_total', 'law', 'law_noninjective', 'law_refusing', 'law_nonrefusing', 'injective_u',
          'obs_total', 'obs_preserved', 'persists', 'cleared']


def lines(data):
    return ['\t'.join(['lift', str(r['input'][0]), str(r['input'][1]), str(r['input'][2])] + [str(r[f]) for f in FIELDS])
            for r in data['records']]
