def lines(data):
    out = []
    for r in data['records']:
        reads = ';'.join('%d:%d' % (o[0], o[1]) for o in r['readouts']) or '-'
        out.append('\t'.join(['fiber', str(r['input'][0]), str(r['input'][1]), str(r['fiber_sizes'][0]), str(r['fiber_sizes'][1]),
                              str(int(r['realizable'])), str(r['distinct_readouts']), str(int(r['total_doubled'])),
                              str(int(r['descends'])), reads]))
    return out
