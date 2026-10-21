def lines(data):
    out = []
    for r in data['records']:
        front = ';'.join(str(m) for m in r['frontier']) or '-'
        table = ';'.join('%d:%d:%d:%d' % (t[0], t[1], int(t[2]), int(t[3])) for t in r['table'])
        out.append('\t'.join(['sel', str(r['n']), str(r['selecting_count']), str(r['frontier_size']), '-' if r['min_price'] is None else str(r['min_price']), front, table]))
    return out
