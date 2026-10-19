def lines(data):
    out=[]
    for c in data['weak_contracts']:out.append('\t'.join(['weak',c['id']]+c['normalized_weights']+[c[k] for k in ('Born','swapped','unit_total_Born','unit_total_swapped','difference')]))
    for c in data['dimensions']:out.append('\t'.join(['dimension',c['id'],str(c['listed_count']),str(c['distinct_count']),str(c['dimension_three_guard']).lower()]))
    for c in data['frames']:
        row=['frame',c['id'],str(c['dimension'])]+[x for g in c['gram_matrices'] for r in g for x in r]+c['determinants']+[x for key in ('quadratic_values','quartic_values') for r in c[key] for x in r]+c['quadratic_sums']+c['quartic_sums']+[c['quartic_deficit']];out.append('\t'.join(row))
    return out+['uniqueness_status\t'+data['uniqueness_status']]
