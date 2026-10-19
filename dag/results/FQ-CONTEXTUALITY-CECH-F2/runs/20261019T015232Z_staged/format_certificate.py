def lines(data):
    result=[]
    for c in data['cases']:
        r=[c['id']]+[str(c[k]) for k in ('local_dimension','incidence_rank','incidence_augmented_rank','delta0_rank','delta0_augmented_rank','h1_dimension','obstruction_pairing')]
        for key in ('incidence','overlaps','delta0'):r += [str(x) for row in c[key] for x in row]
        r+=list(map(str,c['discrepancy']))+[str(c['d1']['rows']),str(c['d1']['columns'])]+list(map(str,c['left_character']+c['character_on_columns']))
        r+=['none'] if c['global_section'] is None else ['some']+list(map(str,c['global_section']))
        result.append('\t'.join(r))
    return result
