"""Complete wire format only: no arithmetic or certificate acceptance."""
def lines(data):
    result=[]
    for a in data['cases']:
        minor=a['separating_minor']
        row=[a['id'],a['left_sum'],a['right_sum']]+a['normalized']+a['normalized_twice']+a['normalized_scaled']+['true' if a['same_weight_ray'] else 'false',a['ray_scale'] or 'none']
        row += [str(minor['indices'][0]),str(minor['indices'][1]),minor['value']] if minor is not None else ['none']*3
        result.append('\t'.join(row))
    a=data['amplitude_control'];result.append('\t'.join(['amplitude_control']+a['left_weights']+a['right_weights']+a['normalized_left']+a['normalized_right']+a['amplitude_minor']))
    return result
