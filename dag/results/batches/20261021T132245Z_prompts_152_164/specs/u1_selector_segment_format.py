def lines(data):
    out = []
    for r in data['records']:
        i = r['input']
        if r['kind'] == 'census':
            out.append('\t'.join(['census', '%d' % i[1], '%d' % r['points'], '%d' % r['mu4_points'], '%d' % r['other_points'],
                                  '1' if r['reaches_minus_one'] else '0', '1' if r['other_points_have_nonintegral_2x'] else '0']))
        elif r['kind'] == 'ffcircle':
            out.append('\t'.join(['ffcircle', '%d' % i[1], '%d' % r['count'], '%d' % r['max_element_order'], '1' if r['cyclic'] else '0',
                                  '1' if r['divisible_by_four'] else '0', '1' if r['orders_beyond_four'] else '0']))
        elif r['kind'] == 'half':
            ys = ','.join(r['y_values']) if r['y_values'] else '-'
            orders = ','.join('%d' % o for o in r['orders']) if r['orders'] else '-'
            out.append('\t'.join(['half', '%d' % i[1], r['x'], r['y_squared'], ys, orders, r['status']]))
        else:
            vals = ','.join('%d' % v for v in r['valuations']) if r['valuations'] else '-'
            out.append('\t'.join(['point', '%d' % i[1], '%d' % i[2], r['x'], r['y'], '1' if r['twice_x_integral'] else '0', '%d' % r['prime'],
                                  vals, '%d' % r['order'], '1' if r['mu4'] else '0']))
    return out
