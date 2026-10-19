"""Complete TSV formatting; no arithmetic or predicate acceptance."""
def lines(data):
    result=['\t'.join(map(str,['census',data['basis_supports_examined'],data['incidence_rank'],data['projector_span_rank'],data['vertex_count'],data['spectral_counts']['at_minus_half'],data['spectral_counts']['above_minus_quarter']]))]
    for i,v in enumerate(data['vertices']):
        fields=['vertex_'+str(i)]+v['weights']+[x for row in v['representative'] for x in row]+list(map(str,v['negative_vector']))+[v['quadratic_value'],v['spectral_class'],v['half_shift_determinant']]+v['quarter_shift_leading_minors']+[str(v['denominator'])]+list(map(str,v['matrix_numerators']+v['weights_twice']+[v['negative_value_numerator']]))
        result.append('\t'.join(fields))
    return result
