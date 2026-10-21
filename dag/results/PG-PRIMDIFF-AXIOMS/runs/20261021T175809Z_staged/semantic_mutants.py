"""Semantic near misses for PG-PRIMDIFF-AXIOMS. Each is a well-formed record a reviewer might believe."""


def _rec(data, kind, **match):
    return next(r for r in data['records'] if r['kind'] == kind and all(r.get(k) == v for k, v in match.items()))


def semantic_mutants(data, profile):
    def axiom_list_is_derived(d):
        _rec(d, 'axiom', index=2)['status'] = 'state_predicate'

    def a5_independent_on_two_points(d):
        r = _rec(d, 'models', n=2)
        r['violate_a5_a7_jointly'] = 12

    def a7_independent_of_a5(d):
        r = _rec(d, 'models', n=3)
        r['a5_equals_a7'] = False
        r['violate_only'][4] = 600

    def token_required(d):
        r = _rec(d, 'kernel', n=2)
        r['token_irrelevant'] = False
        r['empty_token_admitted'] = False

    def duplicates_refused(d):
        _rec(d, 'kernel', n=3)['duplicates_stored'] = False

    def reverse_orientation_refused(d):
        _rec(d, 'kernel', n=2)['reverse_orientation_admitted'] = False

    def carrier_checked_before_a1(d):
        r = _rec(d, 'kernel', n=3)
        r['a1_before_carrier'] = False
        r['err_a1'] = r['err_a1'] - 2
        r['err_carrier'] = r['err_carrier'] + 2

    def admission_forced(d):
        r = _rec(d, 'unentailed', n=3)
        r['without_each_offdiag_pair'] = 0
        r['with_each_offdiag_pair'] = r['models']

    def rcl_defined_on_open_cell(d):
        r = _rec(d, 'triad', name='broken_face')
        r['rcl_refusals'] = 0
        r['exact_nonclosed'] = 0
        r['exact'] = 9

    def closed_face_not_exact(d):
        r = _rec(d, 'triad', name='filled_triangle')
        r['closed_nonexact'] = 3
        r['rupture'] = 17

    def gauge_not_invariant(d):
        _rec(d, 'triad', name='open_triangle')['gauge_invariant'] = False

    def preorders_count_off(d):
        _rec(d, 'closure', n=3)['distinct_closures'] = 355

    def floating_face_is_well_formed(d):
        _rec(d, 'models', n=3)['a5_without_well_formed'] = 0

    def a3_violable(d):
        _rec(d, 'models', n=2)['violate_only'][1] = 4

    def a1_needs_two_points(d):
        _rec(d, 'models', n=1)['violate_only'][0] = 0

    def diagonal_admission(d):
        _rec(d, 'unentailed', n=2)['diagonal_pairs_in_a_model'] = 1

    def filled_triangle_refuses(d):
        _rec(d, 'triad', name='filled_triangle')['rcl_refusals'] = 1

    return [
        {'id': 'floating_face_is_well_formed', 'rationale': 'Claim every structure satisfying A5 is a well-formed complex; a face with none of its boundary edges present satisfies d1 o d0 = 0 vacuously.', 'mutate': floating_face_is_well_formed},
        {'id': 'a3_violable', 'rationale': 'Claim the evaluation-relation axiom can fail on a structure; the reflexive-transitive closure is always a preorder containing the relation.', 'mutate': a3_violable},
        {'id': 'a1_needs_two_points', 'rationale': 'Claim the non-identification axiom cannot be violated on a one-point carrier; the single pair (0,0) violates it.', 'mutate': a1_needs_two_points},
        {'id': 'diagonal_admission', 'rationale': 'Claim a model of all the axioms admits a diagonal pair; A1 excludes it.', 'mutate': diagonal_admission},
        {'id': 'filled_triangle_refuses', 'rationale': 'Claim the transcribed R_cl rule refuses on a filled triangle; there d1 o d0 = 0, so the exact-but-not-closed cell is empty.', 'mutate': filled_triangle_refuses},
        {'id': 'axiom_list_is_derived', 'rationale': 'Present A2 (unentailed admission) as a decidable property of finite structures; it is a statement about the status of the admission, not a predicate.', 'mutate': axiom_list_is_derived},
        {'id': 'a5_independent_on_two_points', 'rationale': 'Claim A5 can be violated on a two-point carrier; a face needs three distinct vertices, so A5 is independent only from n = 3.', 'mutate': a5_independent_on_two_points},
        {'id': 'a7_independent_of_a5', 'rationale': 'Count A7 (descent to the quotient) as an independent axiom; it is equivalent to d1 o d0 = 0 on every structure.', 'mutate': a7_independent_of_a5},
        {'id': 'token_required', 'rationale': 'Claim the kernel refuses an admission without a token; admit_difference stores the token and never inspects it.', 'mutate': token_required},
        {'id': 'duplicates_refused', 'rationale': 'Claim a repeated ordered pair is refused; the kernel appends it again.', 'mutate': duplicates_refused},
        {'id': 'reverse_orientation_refused', 'rationale': 'Claim admitting (a,b) forbids (b,a); the kernel enforces only a != b and carrier membership.', 'mutate': reverse_orientation_refused},
        {'id': 'carrier_checked_before_a1', 'rationale': 'Swap the order of the two guards: an identical pair outside the carrier raises the A1 error first.', 'mutate': carrier_checked_before_a1},
        {'id': 'admission_forced', 'rationale': 'Claim the other axioms force every off-diagonal pair into the admitted set; the models with and without each pair are equinumerous.', 'mutate': admission_forced},
        {'id': 'rcl_defined_on_open_cell', 'rationale': 'Claim R_cl is defined for a half-attached face; there exact cochains with nonzero coboundary exist and R_cl refuses.', 'mutate': rcl_defined_on_open_cell},
        {'id': 'closed_face_not_exact', 'rationale': 'Claim a filled triangle has closed non-exact cochains; with the face attached closed means exact there.', 'mutate': closed_face_not_exact},
        {'id': 'gauge_not_invariant', 'rationale': 'Claim the quotient defect is not gauge invariant; shifting by d0(psi) leaves the L1 distance unchanged.', 'mutate': gauge_not_invariant},
        {'id': 'preorders_count_off', 'rationale': 'Quote the number of preorders on four points (355) for three points (29).', 'mutate': preorders_count_off},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
