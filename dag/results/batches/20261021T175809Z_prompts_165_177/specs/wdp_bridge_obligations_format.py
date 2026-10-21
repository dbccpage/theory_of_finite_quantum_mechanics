def lines(data):
    out = []
    for r in data['records']:
        out.append('\t'.join(['led', ''.join(str(s) for s in r['v']), str(r['n_open']), str(r['n_control']), str(r['n_discharged']),
                              str(int(r['end_to_end'])), str(int(r['controls_run'])), str(int(r['prefix_order'])),
                              str(r['upgrades']), str(r['completing_upgrades']), str(int(r['node_reading']))]))
    return out
