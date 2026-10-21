def lines(data):
    out = []
    for r in data['records']:
        k = r['kind']
        if k == 'maps':
            out.append('\t'.join(['maps', str(r['a']), str(r['b']), str(r['c']), str(r['total_maps']), str(r['left_maps']), str(r['right_maps']),
                                  str(int(r['product_matches'])), str(r['unique_copairs']), str(int(r['inl_injective'])),
                                  str(int(r['inr_injective'])), str(int(r['disjoint'])), str(int(r['covering']))]))
        elif k == 'reduction':
            out.append('\t'.join(['reduction', str(r['a']), str(r['b']), str(r['maps_b_to_a']), str(r['maps_a_to_b']), str(r['retractions_to_pd']),
                                  str(r['retractions_to_s']), str(int(r['exists_to_pd'])), str(int(r['exists_to_s']))]))
        else:
            out.append('\t'.join(['posit', str(r['a']), str(r['b']), str(int(r['nonempty_pd'])), str(int(r['nonempty_s'])), str(r['coproduct_size']),
                                  str(int(r['nonempty_real0'])), str(int(r['real0_nonempty_iff_a_channel_is']))]))
    return out
