"""Semantic near misses for the rational unit-circle torsion certificate (L1-U1-SELECTOR-OTHER-SEGMENT).

Each mutant is a well-formed record that a reviewer could believe and each breaks one premise or hides the obstruction.
"""


def _half(data, k):
    return next(r for r in data['records'] if r['kind'] == 'half' and r['input'][1] == k)


def _point(data, m, n):
    return next(r for r in data['records'] if r['kind'] == 'point' and r['input'][1:] == [m, n])


def _census(data, b):
    return next(r for r in data['records'] if r['kind'] == 'census' and r['input'][1] == b)


def _ff(data, p):
    return next(r for r in data['records'] if r['kind'] == 'ffcircle' and r['input'][1] == p)


def semantic_mutants(data, profile):
    def sixth_root_of_unity_in_gaussian_rationals(d):
        r = _half(d, 1)
        r['status'] = 'unit_points'
        r['y_values'] = ['1']
        r['orders'] = [6]

    def pythagorean_point_is_a_quarter_turn(d):
        r = _point(d, 1, 2)
        r['order'] = 4
        r['mu4'] = True

    def valuation_at_the_wrong_prime(d):
        r = _point(d, 1, 2)
        r['prime'] = 3
        r['valuations'] = [0, 0, 0, 0, 0, 0]

    def valuation_exponent_off_by_one(d):
        r = _point(d, 3, 4)
        r['valuations'] = [-1, -2, -3, -4, -5, -6]

    def unit_i_has_infinite_order(d):
        r = _point(d, 1, 1)
        r['order'] = 0
        r['mu4'] = False

    def identity_read_as_minus_one(d):
        _half(d, 2)['orders'] = [2]

    def search_bound_read_as_order(d):
        r = _point(d, 5, 12)
        r['order'] = 12

    def non_unit_point_flagged_as_mu4(d):
        _point(d, 2, 3)['mu4'] = True

    def integral_twice_x_for_a_cayley_point(d):
        r = _point(d, 2, 3)
        r['twice_x_integral'] = True
        r['prime'] = 0
        r['valuations'] = []

    def all_cayley_points_have_infinite_order(d):
        r = _census(d, 3)
        r['other_points'] = r['points']
        r['mu4_points'] = 0

    def cayley_map_misses_minus_one(d):
        _census(d, 6)['reaches_minus_one'] = False

    def finite_field_circle_has_only_mu4(d):
        r = _ff(d, 7)
        r['count'] = 4
        r['max_element_order'] = 4
        r['orders_beyond_four'] = False

    return [
        {'id': 'sixth_root_of_unity_in_gaussian_rationals', 'rationale': 'Take x = 1/2 with y = sqrt(3)/2 as a Gaussian-rational phase of order 6; y^2 = 3/4 has no rational root, so the point does not exist.', 'mutate': sixth_root_of_unity_in_gaussian_rationals},
        {'id': 'pythagorean_point_is_a_quarter_turn', 'rationale': 'Read (3/5, 4/5) as a quarter turn because excluding the sign group is supposed to leave i; it has infinite order.', 'mutate': pythagorean_point_is_a_quarter_turn},
        {'id': 'valuation_at_the_wrong_prime', 'rationale': 'Test the obstruction at the prime 3, which does not divide the denominator 5 of 2x; all valuations vanish and the infinite order is hidden.', 'mutate': valuation_at_the_wrong_prime},
        {'id': 'valuation_exponent_off_by_one', 'rationale': 'For (7/25, 24/25) the denominator of 2x is 25 = 5^2, so the valuation of 2 Re z^k is -2k, not -k.', 'mutate': valuation_exponent_off_by_one},
        {'id': 'unit_i_has_infinite_order', 'rationale': 'Report the point (0,1) = i as non-torsion; it is a fourth root of unity.', 'mutate': unit_i_has_infinite_order},
        {'id': 'identity_read_as_minus_one', 'rationale': 'The point with x = 1 is the identity (order 1); order 2 belongs to x = -1.', 'mutate': identity_read_as_minus_one},
        {'id': 'search_bound_read_as_order', 'rationale': 'The order search stops at 12; a point with no power equal to 1 up to the bound has order recorded as 0, not 12.', 'mutate': search_bound_read_as_order},
        {'id': 'non_unit_point_flagged_as_mu4', 'rationale': 'Flag the point (5/13, 12/13) as one of the four unit points; its order is infinite.', 'mutate': non_unit_point_flagged_as_mu4},
        {'id': 'integral_twice_x_for_a_cayley_point', 'rationale': '2x = 10/13 is not an integer; claiming integrality would put the point in the finite list and erase the p-adic witness.', 'mutate': integral_twice_x_for_a_cayley_point},
        {'id': 'all_cayley_points_have_infinite_order', 'rationale': 'Generalise "(3/5,4/5) has infinite order" to every Cayley point; (0,1), (1,0), (1,1), (-1,1) give (1,0), (-1,0), i and -i, so four Cayley points lie in mu_4.', 'mutate': all_cayley_points_have_infinite_order},
        {'id': 'cayley_map_misses_minus_one', 'rationale': 'Claim the Cayley map misses (-1, 0); n = 0, m != 0 gives (-1, 0), so the map is onto the circle.', 'mutate': cayley_map_misses_minus_one},
        {'id': 'finite_field_circle_has_only_mu4', 'rationale': 'Read the torsion-is-mu_4 result as a statement about every finite carrier; the unit circle over F_7 has 8 points and is cyclic of order 8, so orders beyond 4 occur there.', 'mutate': finite_field_circle_has_only_mu4},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
