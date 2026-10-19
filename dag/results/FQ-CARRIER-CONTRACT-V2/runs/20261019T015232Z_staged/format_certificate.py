ARRAYS=('source_coefficients','conjugate_coefficients','norm_coefficients','embedded_coefficients','via_intermediate_coefficients','embedded_norm_coefficients','norm_after_embedding','embedded_sum','sum_after_embedding','embedded_product','product_after_embedding','embedded_conjugate','conjugate_after_embedding')
def lines(data):
    result=['\t'.join(map(str,['inventory',data['label_lcm']]+data['inventory_target_ids']+data['inventory_conductors']+data['distinct_conductors']))]
    for s in data['samples']:
        result.append('\t'.join([s['id'],str(s['source_conductor']),str(s['intermediate_conductor']),str(s['target_conductor'])]+list(map(str,s['source_polynomial']+s['target_polynomial']))+[x for key in ARRAYS for x in s[key]]))
    b=data['declaration_boundary'];result.append('\t'.join(['declaration_boundary','true' if b['colimit_constructed'] else 'false',b['Kronecker_Weber'],'true' if b['field_minimality_proved'] else 'false','true' if b['all_target_amplitudes_verified'] else 'false']))
    return result
