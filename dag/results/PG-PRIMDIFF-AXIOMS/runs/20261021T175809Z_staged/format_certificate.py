def _text(items):
    return ','.join('-'.join(str(x) for x in it) for it in items) or '-'


def lines(data):
    out = []
    for r in data['records']:
        k = r['kind']
        if k == 'axiom':
            out.append('\t'.join(['axiom', str(r['index']), r['name'], r['status']] + [str(x) for x in r['models_by_n']]))
        elif k == 'models':
            out.append('\t'.join(['models', str(r['n']), str(r['total']), str(r['all_hold'])] + [str(x) for x in r['violate_only']]
                                 + [str(r['violate_a5_a7_jointly']), str(int(r['a5_equals_a7'])), str(r['well_formed_models']),
                                    str(r['a5_without_well_formed']), str(r['distinct_signatures'])]))
        elif k == 'unentailed':
            out.append('\t'.join(['unentailed', str(r['n']), str(r['models']), str(r['offdiag_pairs']), str(r['with_each_offdiag_pair']),
                                  str(r['without_each_offdiag_pair']), str(r['diagonal_pairs_in_a_model']), str(r['models_with_empty_d'])]))
        elif k == 'kernel':
            out.append('\t'.join(['kernel', str(r['n']), str(r['probes']), str(r['ok']), str(r['err_a1']), str(r['err_carrier']),
                                  str(int(r['token_irrelevant'])), str(int(r['empty_token_admitted'])), str(int(r['duplicates_stored'])),
                                  str(int(r['reverse_orientation_admitted'])), str(int(r['a1_before_carrier']))]))
        elif k == 'closure':
            out.append('\t'.join(['closure', str(r['n']), str(r['relations']), str(r['distinct_closures']), str(int(r['all_preorders'])),
                                  str(int(r['contains_relation'])), str(int(r['equals_reachability']))]))
        else:
            out.append('\t'.join(['triad', r['name'], str(r['n']), _text(r['edges']), _text(r['faces']), str(r['cochains']), str(r['exact']),
                                  str(r['closed_nonexact']), str(r['rupture']), str(r['exact_nonclosed']), str(r['rcl_refusals']),
                                  str(r['phi1_sum']), str(r['phi1_max']), str(int(r['gauge_invariant'])), str(int(r['relabel_invariant'])),
                                  str(int(r['nilpotent'])), str(int(r['well_formed']))]))
    return out
