def _items(xs):
    return '+'.join(str(x) for x in xs) or '-'


def _state(st):
    return '|'.join('%s:%s' % (name, _items(v)) for name, v in zip('mSdarO', st))


def lines(data):
    out = []
    for r in data['records']:
        k = r['kind']
        if k == 'trace':
            out.append('\t'.join(['trace', str(r['items']), str(r['max_len']), str(r['init_mask']), str(r['traces']), str(r['changed']),
                                  str(r['with_admit']), str(r['with_new_admit']), str(r['mismatches']), str(r['distinct_final_states'])]))
        elif k == 'footprint':
            out.append('\t'.join(['footprint', r['op'], r['new_item_fields'], r['old_item_fields']]))
        elif k == 'pair':
            out.append('\t'.join(['pair', r['a'], r['b'], str(r['min_len']), str(r['contexts'])]))
        elif k == 'conflation':
            out.append('\t'.join(['conflation', r['name'], str(r['min_len']), str(r['witness_count']), ','.join(r['witness']),
                                  r['differing_fields'], str(int(r['admitted_differs'])), _state(r['six_state']), _state(r['conflated_state'])]))
        else:
            out.append('\t'.join(['reading', str(r['token']), r['conflation'], _items(r['six_L_admitted']), _items(r['six_F_admitted']),
                                  _items(r['conflated_L_admitted']), _items(r['conflated_F_admitted']),
                                  str(int(r['six_separated'])), str(int(r['conflated_separated']))]))
    return out
