def lines(data):
    result=[]
    for c in data['cases']:
        out=[c['id']]+c['spectrum']+[c['denominator']]+c['integer_weights']+[str(c['terms']),c['purity'],c['purity_deficit']]+c['integer_power_sums']+c['power_traces']
        for b in c['term_bounds']:out +=[b[k] for k in ('mode','t','partial','tail','lower','upper')]
        out +=[c[k] for k in ('entropy_lower','entropy_upper','interval_width','classification','log_base','Baker_status')]
        result.append('\t'.join(out))
    return result
