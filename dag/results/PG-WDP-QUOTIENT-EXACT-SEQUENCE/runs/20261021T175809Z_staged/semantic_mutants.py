"""Semantic near misses for the exact-sequence certificate (PG-WDP-QUOTIENT-EXACT-SEQUENCE).

Each mutant is a well-formed record a reviewer could believe that breaks one premise of the node.
"""


def _rec(data, ident):
    return next(r for r in data['records'] if r['id'] == ident)


def semantic_mutants(data, profile):
    def canonical_splitting_claimed(d):
        r = _rec(d, 'two_triangles_mixed')
        r['section_dim'] = 0
        r['canonical_split'] = True

    def splitting_denied_when_h1_zero(d):
        r = _rec(d, 'k4_all_faces')
        r['section_dim'] = 3
        r['canonical_split'] = False

    def exactness_without_complex(d):
        r = _rec(d, 'violates_d1d0_edge')
        r['complex'] = True
        r['dim_h1'] = 0
        r['exact_dims'] = True
        r['section_dim'] = 0
        r['canonical_split'] = True
        r['diag'] = 'ExactClass'
        r['gamma2'] = '2'
        r['classes_hit'] = 1

    def opnorm_largest_entry(d):
        r = _rec(d, 'loop_three_faces')
        r['opnorm'] = '1'
        r['bound_holds'] = False

    def nonwindow_representative_gamma2_reported(d):
        r = _rec(d, 'violates_d1d0_edge')
        r['gamma2'] = '2'
        r['bound_holds'] = False

    def nonwindow_minimal_residual_gamma2_reported(d):
        r = _rec(d, 'violates_d1d0_edge')
        r['gamma2'] = '0'
        r['bound_holds'] = True

    def no_splitting_claimed_for_zero_d1(d):
        r = _rec(d, 'tri_unfilled_closed')
        r['section_dim'] = 1
        r['canonical_split'] = False

    def seminorm_filled_relabelled(d):
        _rec(d, 'seminorm_zero_weight_filled')['diag'] = 'ActiveClosureFailure'

    def kernel_witness_not_optimal(d):
        _rec(d, 'tri_filled_active')['witness'] = 'x=0,0,0|y=1,1,-1'.replace('x=0,0,0', 'x=0,0,2')

    def seminorm_phi_zero_means_zero_class(d):
        _rec(d, 'seminorm_zero_weight_unfilled')['phi_zero_iff_class_zero'] = True

    def two_classes_at_once(d):
        _rec(d, 'tri_filled_active')['classes_hit'] = 2

    def h1_dimension_without_quotient(d):
        r = _rec(d, 'tri_unfilled_closed')
        r['dim_h1'] = 3
        r['exact_dims'] = False
        r['section_dim'] = 0

    def opnorm_ignores_weights(d):
        _rec(d, 'tri_heavy_weights')['opnorm'] = '1'

    def nonzero_class_called_zero(d):
        _rec(d, 'seminorm_zero_weight_unfilled')['class_zero'] = True
        _rec(d, 'seminorm_zero_weight_unfilled')['phi_zero_iff_class_zero'] = True

    return [
        {'id': 'canonical_splitting_claimed', 'rationale': 'Claim a canonical section for a window with dim H1 = dim im d1 = 1; the sections form a 1-parameter affine family moved by the automorphisms 1 + i f p.', 'mutate': canonical_splitting_claimed},
        {'id': 'splitting_denied_when_h1_zero', 'rationale': 'Claim "no canonical splitting" for K4 with all faces where H1 = 0; then the section is unique and canonical, so the source clause needs dim H1 > 0 and im d1 != 0.', 'mutate': splitting_denied_when_h1_zero},
        {'id': 'exactness_without_complex', 'rationale': 'Report the exact sequence for a window with d1 d0 != 0, where kappa1 is not defined on Q1.', 'mutate': exactness_without_complex},
        {'id': 'opnorm_largest_entry', 'rationale': 'Use the largest entry of d1 as ||d1|| and report the inequality failing; the J-to-L1 operator norm is the largest column sum (3), and the inequality holds with equality.', 'mutate': opnorm_largest_entry},
        {'id': 'nonwindow_representative_gamma2_reported', 'rationale': 'Report Gamma2 = 2 and a failing inequality for the window with d1 d0 != 0; that is the norm at the representative h, which is not a class function there (it is 0 at h = 0), so it is not reported.', 'mutate': nonwindow_representative_gamma2_reported},
        {'id': 'nonwindow_minimal_residual_gamma2_reported', 'rationale': 'Report Gamma2 = 0 and a holding inequality for the window with d1 d0 != 0, i.e. the source reading at the minimal residual h* = 0; the certificate withholds Gamma2 for non-windows because minimal residuals are not unique in general and the representative norm is not a class function.', 'mutate': nonwindow_minimal_residual_gamma2_reported},
        {'id': 'no_splitting_claimed_for_zero_d1', 'rationale': 'Claim a non-canonical splitting (one free parameter) for the unfilled triangle where d1 = 0: H1 is 1-dimensional but im d1 = 0, so the section is unique.', 'mutate': no_splitting_claimed_for_zero_d1},
        {'id': 'seminorm_filled_relabelled', 'rationale': 'Relabel the zero-weight filled triangle ActiveClosureFailure because Gamma2 = 1; the label follows the source if-chain (Phi1 = 0 gives ExactClass), which for a seminorm no longer means an exact coboundary.', 'mutate': seminorm_filled_relabelled},
        {'id': 'primal_potential_not_optimal', 'rationale': 'Carry the potential (0,0,2) for the filled triangle with h = (1,1,0): its cost is 4, not Phi1 = 2.', 'mutate': kernel_witness_not_optimal},
        {'id': 'seminorm_phi_zero_means_zero_class', 'rationale': 'Claim Phi1 = 0 iff the class vanishes for a seminorm with a weight-0 edge; Phi1 = 0 there but the class is nonzero.', 'mutate': seminorm_phi_zero_means_zero_class},
        {'id': 'two_classes_at_once', 'rationale': 'Count both ClosedResidual and ActiveClosureFailure for one class; exactly one predicate holds.', 'mutate': two_classes_at_once},
        {'id': 'h1_dimension_without_quotient', 'rationale': 'Take dim H1 = dim ker d1 without quotienting by im d0 and report the dimension count as failing.', 'mutate': h1_dimension_without_quotient},
        {'id': 'opnorm_ignores_weights', 'rationale': 'Take ||d1|| = 1 for the window with weights 3 on every edge; the norm J rescales it to 1/3.', 'mutate': opnorm_ignores_weights},
        {'id': 'nonzero_class_called_zero', 'rationale': 'Call the class zero because Phi1 = 0 under a seminorm; h is not in im d0.', 'mutate': nonzero_class_called_zero},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The windows are a set keyed by id; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
