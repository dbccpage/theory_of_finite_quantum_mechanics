MATRICES=('density','effect','kraus_completeness','channel_density','unitary_star_unitary','evolved_density','tensor_density')
SCALARS=('Born_weight','unit_weight','channel_trace','evolved_trace','tensor_trace','channel_Born_weight')
def lines(data):
    return ['\t'.join([c['id']]+[x for k in MATRICES for row in c['matrices'][k] for x in row]+[c['scalars'][k] for k in SCALARS]+[c['derivation_status']]) for c in data['cases']]
