def lines(data):
    out = []
    for r in data['records']:
        k = r['kind']
        if k == 'stat':
            out.append('\t'.join(['stat', str(r['i']), r['name'], r['route'], r['residual'], r['auth'], str(int(r['authterm']))]))
        elif k == 'pfp':
            out.append('\t'.join(['pfp', str(r['i']), r['name'], r['route']]))
        elif k == 'diag':
            out.append('\t'.join(['diag', str(r['i']), r['name'], r['run_tag'], r['route'], str(int(r['cert_eligible']))]))
        elif k == 'rel':
            out.append('\t'.join(['rel', str(int(r['in_profile'])), str(int(r['contradicted'])), str(int(r['supported'])), r['status']]))
        elif k == 'fib':
            out.append('\t'.join(['fib', str(int(r['selected'])), str(r['cand']), str(r['out']), str(int(r['exhaustive'])), r['agreement'],
                                  str(int(r['verifier'])), r['status'], r['route']]))
        else:
            ints = ';'.join(str(x) for x in r['ints']) or '-'
            items = ';'.join(r['items']) or '-'
            out.append('\t'.join(['sum', r['name'], ints, items]))
    return out
