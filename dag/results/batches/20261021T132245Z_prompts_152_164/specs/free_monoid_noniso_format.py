ORDER = ('words_n', 'words_m', 'atoms_n', 'atoms_m', 'homs', 'letters_onto', 'injective_bounded', 'bijective_candidates',
         'bijective_not_permutation', 'permutation_homs', 'discrete_equivalences', 'set_bijection', 'homomorphism_violations')


def _cell(value):
    if isinstance(value, list):
        return ':'.join(str(x) for x in value)
    return str(value)


def lines(data):
    out = []
    for r in data['records']:
        fields = ['monoid', str(r['input'][0]), str(r['input'][1]), str(r['input'][2])]
        fields += [_cell(r[key]) for key in ORDER]
        out.append('\t'.join(fields))
    return out
