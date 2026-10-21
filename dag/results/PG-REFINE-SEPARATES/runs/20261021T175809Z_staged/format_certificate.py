def lines(data):
    out = []
    for r in data['records']:
        k = r['kind']
        if k == 'graph':
            edges = ','.join('%d-%d' % (e[0], e[1]) for e in r['edges']) or '-'
            out.append('\t'.join(['graph', r['name'], str(r['n']), str(len(r['edges'])), str(r['components']), str(int(r['bipartite'])),
                                  str(r['one_bit_tags']), str(r['chi']), str(r['min_bits']), str(r['odd_girth']), edges]))
        elif k == 'enum':
            out.append('\t'.join(['enum', str(r['n']), str(r['graphs']), str(r['bipartite']), str(r['bipartite_colouring_pairs'])]
                                 + [str(x) for x in r['by_min_bits']]))
        elif k == 'fiber':
            out.append('\t'.join(['fiber', str(r['m']), str(r['min_bits'])] + [str(x) for x in r['injective_tags_by_bits']]))
        elif k == 'fiberbits':
            out.append('\t'.join(['fiberbits', str(r['m']), str(r['min_bits'])]))
        else:
            out.append('\t'.join(['refine', str(r['n']), str(r['o']), str(r['t']), str(r['quadruples']), str(r['iff_failures']),
                                  str(r['separated_by_tag']), str(r['refined_equal']), str(r['old_separation_kept'])]))
    return out
