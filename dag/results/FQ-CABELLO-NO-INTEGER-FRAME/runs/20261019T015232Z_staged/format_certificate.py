def lines(data):
    p=data['parity_main'];c=data['frame_counterexample'];e=data['even_control']
    return ['\t'.join(map(str,['parity_main']+p['multipliers']+p['combined_coefficients']+[p['combined_rhs'],p['divisor'],p['remainder']])),
            '\t'.join(['frame_counterexample',c['denominator']]+[x for row in c['normalized_matrix'] for x in row]+c['weights']+c['frame_sums']+list(map(str,c['negative_vector']))+[c['raw_negative_value'],c['negative_value']]+list(map(str,c['scaled_readout_remainders']))),
            '\t'.join(map(str,['even_control']+e['multipliers']+e['combined_coefficients']+[e['combined_rhs'],e['divisor'],e['remainder']]+e['assignment']+e['context_sums']))]
