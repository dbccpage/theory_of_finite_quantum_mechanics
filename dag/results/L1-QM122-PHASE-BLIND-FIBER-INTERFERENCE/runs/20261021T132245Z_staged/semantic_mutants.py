"""Semantic near misses for the phase-blind fiber / Hadamard interference certificate.

Each mutant is a well-formed record that a reviewer could believe, and each breaks one premise of the node.
"""


def _record(data, w0, w1):
    return next(r for r in data['records'] if r['input'] == [w0, w1])


def semantic_mutants(data, profile):
    def real_sign_fiber_only(d):
        r = _record(d, 1, 1)
        r['fiber_sizes'] = [2, 2]
        r['readouts'] = [[0, 4], [4, 0]]
        r['distinct_readouts'] = 2

    def unit_orbit_as_fiber(d):
        # the fiber of weight 5 replaced by the unit orbit of 1+2i: 4 of the 8 points, with the readouts that orbit produces
        r = _record(d, 5, 5)
        orbit = [(1, 2), (-2, 1), (-1, -2), (2, -1)]
        outs = sorted({(((a[0] + b[0]) ** 2 + (a[1] + b[1]) ** 2), ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)) for a in orbit for b in orbit})
        r['fiber_sizes'] = [4, 4]
        r['readouts'] = [list(o) for o in outs]
        r['distinct_readouts'] = len(outs)

    def zero_sector_treated_as_generic(d):
        r = _record(d, 0, 5)
        r['descends'] = False
        r['distinct_readouts'] = 2

    def second_sector_zero_treated_as_generic(d):
        r = _record(d, 5, 0)
        r['descends'] = False
        r['distinct_readouts'] = 2

    def unrealizable_weight_accepted(d):
        r = _record(d, 3, 3)
        r['realizable'] = True
        r['fiber_sizes'] = [4, 4]

    def mixing_preserves_total(d):
        _record(d, 2, 5)['total_doubled'] = False

    def equal_weights_imply_equal_readout(d):
        r = _record(d, 4, 9)
        r['readouts'] = r['readouts'][:1]
        r['distinct_readouts'] = 1
        r['descends'] = True

    return [
        {'id': 'real_sign_fiber_only', 'rationale': 'Treat the phase fiber as just the two real signs; still looks non-descending but the fiber is not the Gaussian one.', 'mutate': real_sign_fiber_only},
        {'id': 'unit_orbit_as_fiber', 'rationale': 'Take the orbit of the unit group {1,i,-1,-i} as the whole fiber of weight 5; the fiber also contains 1+2i type points.', 'mutate': unit_orbit_as_fiber},
        {'id': 'zero_sector_treated_as_generic', 'rationale': 'Claim non-descent also when one sector has weight 0, where the fiber is a single point.', 'mutate': zero_sector_treated_as_generic},
        {'id': 'second_sector_zero_treated_as_generic', 'rationale': 'Claim non-descent when the SECOND sector has weight 0, the symmetric boundary the first-slot theorem does not cover by itself.', 'mutate': second_sector_zero_treated_as_generic},
        {'id': 'unrealizable_weight_accepted', 'rationale': 'Treat 3 as a realizable Gaussian weight; it is not a sum of two squares.', 'mutate': unrealizable_weight_accepted},
        {'id': 'mixing_preserves_total', 'rationale': 'Claim the unnormalized mixing readout does not double the total weight.', 'mutate': mixing_preserves_total},
        {'id': 'equal_weights_imply_equal_readout', 'rationale': 'Claim that the weights (4,9) already determine the readout, i.e. interference descends.', 'mutate': equal_weights_imply_equal_readout},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
