"""Semantic near misses for the symmetry-price / minimal-input frontier certificate.

Each mutant is a well-formed record a reviewer could believe; each breaks one premise or states the unpaid bridge
(a general result read off a fixed instance, or the hypothesis `at least two points` dropped).
"""


def _rec(data, n):
    return next(r for r in data['records'] if r['n'] == n)


def _set_entry(r, mask, inv, sel, minimal):
    r['table'][mask] = [mask, inv, sel, minimal]


def semantic_mutants(data, profile):
    def empty_declaration_selects(d):
        # n=3: "the empty declaration already selects point 0" - contradicts no_fully_invariant_point.
        r = _rec(d, 3)
        _set_entry(r, 0, 1, True, False)
        r['selecting_count'] += 1
        r['min_price'] = 0

    def complement_singleton_ignored(d):
        # n=2, S={0}: only the declared point is invariant; the one-point complement {1} is also invariant.
        r = _rec(d, 2)
        _set_entry(r, 1, 1, True, True)

    def rigidification_price(d):
        # n=4: confuse "select a point" with "kill the whole stabiliser": frontier = the 3-point declarations.
        r = _rec(d, 4)
        threes = [m for m in range(16) if bin(m).count('1') == 3]
        for mask in range(16):
            t = r['table'][mask]
            t[3] = mask in threes
        r['frontier'] = threes
        r['frontier_size'] = 4
        r['min_price'] = 3

    def non_minimal_marked_minimal(d):
        # n=3: a two-point declaration flagged as inclusion-minimal although each point already selects.
        r = _rec(d, 3)
        r['table'][3][3] = True
        r['frontier'] = sorted(r['frontier'] + [3])
        r['frontier_size'] += 1

    def one_point_pays_a_declaration(d):
        # n=1: apply the >=2-point theorem to a one-point carrier: claim the empty declaration does not select.
        r = _rec(d, 1)
        r['table'][0] = [0, 0, False, False]
        r['selecting_count'] = 1
        r['frontier'] = [1]
        r['frontier_size'] = 1

    def empty_carrier_selects(d):
        # n=0: a "distinguished point" on the empty carrier.
        r = _rec(d, 0)
        r['table'][0] = [0, 1, True, True]
        r['selecting_count'] = 1
        r['frontier'] = [0]
        r['frontier_size'] = 1
        r['min_price'] = 0

    def price_is_zero_for_five_points(d):
        # n=5: claim selection is free (min price 0) because 'some point is always special in a finite set'.
        _rec(d, 5)['min_price'] = 0


    def setwise_stabiliser_table(d):
        # n=3: read 'declared' as 'fixed as a set' (setwise stabiliser): invariant points of S are then only the points outside S
        # when S is a proper subset with a single outside point, and nothing when S is everything; the table differs from the pointwise one.
        r = _rec(d, 3)
        setwise = {0: 0, 1: 1, 2: 2, 3: 4, 4: 4, 5: 2, 6: 1, 7: 0}
        for mask, inv in setwise.items():
            _set_entry(r, mask, inv, inv != 0, r['table'][mask][3])
        r['selecting_count'] = sum(1 for t in r['table'] if t[2])

    def rigid_carrier_price_zero(d):
        # n=3 read as a RIGID carrier (trivial symmetry group): every point is invariant at once, price 0, frontier = {empty set}.
        r = _rec(d, 3)
        for mask in range(8):
            _set_entry(r, mask, 7, True, mask == 0)
        r['selecting_count'] = 8
        r['frontier'] = [0]
        r['frontier_size'] = 1
        r['min_price'] = 0

    return [
        {'id': 'empty_declaration_selects', 'rationale': 'Claims the empty declaration selects a point on a 3-point set, the exact statement no_fully_invariant_point refutes.', 'mutate': empty_declaration_selects},
        {'id': 'complement_singleton_ignored', 'rationale': 'On two points the complement of a declared point is a single point and is invariant too; dropping it reads the n>=3 pattern into n=2.', 'mutate': complement_singleton_ignored},
        {'id': 'rigidification_price', 'rationale': 'Confuses the price of selecting one point (one declared point) with the price of trivialising the symmetry group (n-1 declared points).', 'mutate': rigidification_price},
        {'id': 'non_minimal_marked_minimal', 'rationale': 'Marks a two-point declaration as inclusion-minimal although each of its singletons already selects.', 'mutate': non_minimal_marked_minimal},
        {'id': 'one_point_pays_a_declaration', 'rationale': 'Applies the at-least-two-points theorem at n=1, where the empty declaration selects the only point for free.', 'mutate': one_point_pays_a_declaration},
        {'id': 'empty_carrier_selects', 'rationale': 'Claims a selected point on an empty carrier; the vacuous-universal reading of invariance is not a point.', 'mutate': empty_carrier_selects},
        {'id': 'price_is_zero_for_five_points', 'rationale': 'Reads selection as free on five points, contradicting the nonexistence of a fully invariant point and the not-free reading of CH03-N01.', 'mutate': price_is_zero_for_five_points},
        {'id': 'setwise_stabiliser_table', 'rationale': 'Reads a declared set as fixed only as a set (setwise stabiliser) instead of pointwise: the table changes (declared points are no longer invariant) although the singleton frontier survives, so this tests the modelling choice.', 'mutate': setwise_stabiliser_table},
        {'id': 'rigid_carrier_price_zero', 'rationale': 'Reads the 3-point carrier as rigid (trivial symmetry group): every point is invariant at price 0, which is the structured-carrier case the bare-set frontier does not cover.', 'mutate': rigid_carrier_price_zero},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The carrier sizes are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
