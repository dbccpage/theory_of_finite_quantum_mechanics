def lines(data):
    out = []
    for r in data['records']:
        fields = ['listed'] + [str(x) for x in r['input']]
        for key in ('lists', 'triples', 'listed_fc', 'recon_correct', 'mismatch', 'complete_triples', 'complete_mismatch',
                    'partial_false_positive', 'unlisted_refused', 'unlisted_correct', 'unlisted_wrong'):
            fields.append(str(r[key]))
        out.append('\t'.join(fields))
    return out
