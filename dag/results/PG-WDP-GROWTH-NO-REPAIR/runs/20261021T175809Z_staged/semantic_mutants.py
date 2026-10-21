"""Semantic near misses for the growth / no-repair certificate (PG-WDP-GROWTH-NO-REPAIR).

Each mutant is a well-formed record a reviewer could believe that breaks one premise of the node.
"""


def _rec(data, ident):
    return next(r for r in data['records'] if r['id'] == ident)


def semantic_mutants(data, profile):
    def rescaled_weights_claimed_monotone(d):
        r = _rec(d, 'parallel_restrict_rescaled_weights')
        r['phi_b'] = '4'
        r['verdict'] = 'sub_phi_le'

    def attachment_lowers_phi1(d):
        r = _rec(d, 'tri_unfilled_attach_face')
        r['phi_b'] = '0'
        r['diag_b'] = 'ExactClass'
        r['verdict'] = 'phi_lower'

    def attachment_keeps_gamma(d):
        r = _rec(d, 'tri_unfilled_attach_face')
        r['gamma_b'] = '0'
        r['diag_b'] = 'ClosedResidual'
        r['verdict'] = 'phi_equal_gamma_same'

    def invalid_row_accepted(d):
        r = _rec(d, 'tri_attach_invalid_row')
        r['complex_b'] = True
        r['diag_b'] = 'ClosedResidual'
        r['verdict'] = 'phi_equal_gamma_same'

    def residual_sum_as_restricted_phi1(d):
        _rec(d, 'k4_restrict_triangle_pendant')['phi_b'] = '3'

    def class_unchanged_after_attachment(d):
        _rec(d, 'square_attach_filling_face')['diag_b'] = 'ClosedResidual'

    def gauge_shift_counted_as_repair(d):
        r = _rec(d, 'tri_edit_h_gauge_shift')
        r['phi_b'] = '1'
        r['verdict'] = 'phi_lower'

    def weight_change_called_invariant(d):
        r = _rec(d, 'tri_edit_w_down')
        r['phi_b'] = '6'
        r['verdict'] = 'phi_same'

    def face_survives_without_its_edges(d):
        _rec(d, 'k4_restrict_to_triangle')['k_b'] = 4

    def gamma2_at_representative_for_nonwindow(d):
        _rec(d, 'tri_attach_invalid_row')['gamma_b'] = '1'

    def lowered_weights_called_raising(d):
        r = _rec(d, 'parallel_restrict_downweighted')
        r['phi_b'] = '6'
        r['verdict'] = 'sub_phi_gt'

    def deletion_called_phi_neutral(d):
        _rec(d, 'k4_restrict_one_edge')['phi_b'] = '3'

    def routing_name_as_class(d):
        _rec(d, 'tri_attach_invalid_row')['diag_b'] = 'NoRule'

    def subset_restriction_raised(d):
        r = _rec(d, 'k4_sub_07')
        r['phi_b'] = '4'
        r['verdict'] = 'sub_phi_gt'

    def primal_witness_not_optimal(d):
        _rec(d, 'k4_sub_63')['witness_a'] = 'x=0,0,0,0|y=0,0,0,0,0,0'

    return [
        {'id': 'rescaled_weights_claimed_monotone', 'rationale': 'Claim restriction never raises Phi1 although the sub-window weights were raised from 2 to 3 (hypothesis "restricted weights" dropped): Phi1 goes from 4 to 6.', 'mutate': rescaled_weights_claimed_monotone},
        {'id': 'attachment_lowers_phi1', 'rationale': 'Claim that filling the triangle with a 2-cell repairs the residual; Phi1 depends only on (C0, C1, d0, J, h) and stays 1.', 'mutate': attachment_lowers_phi1},
        {'id': 'attachment_keeps_gamma', 'rationale': 'Claim attaching a 2-cell cannot change Gamma2; the new face has d1 h = 1, so Gamma2 rises from 0 to 1 and the class moves from ClosedResidual to ActiveClosureFailure.', 'mutate': attachment_keeps_gamma},
        {'id': 'invalid_row_accepted', 'rationale': 'Accept a "face" row (1,0,0) as a 2-cell although d1 d0 != 0; the enlarged data is not a window.', 'mutate': invalid_row_accepted},
        {'id': 'residual_sum_as_restricted_phi1', 'rationale': 'Read the sum of kept edge residuals (the source list sum) as Phi1 of the sub-window; the minimum over potentials is 2.', 'mutate': residual_sum_as_restricted_phi1},
        {'id': 'class_unchanged_after_attachment', 'rationale': 'Say growth does not change the diagnostic class because Phi1 is unchanged; the filled square is ActiveClosureFailure.', 'mutate': class_unchanged_after_attachment},
        {'id': 'gauge_shift_counted_as_repair', 'rationale': 'Count an edit of h by a coboundary as lowering Phi1; Phi1 is a class function and stays 2.', 'mutate': gauge_shift_counted_as_repair},
        {'id': 'weight_change_called_invariant', 'rationale': 'Claim changing the declared weights leaves Phi1 alone; down-weighting from 3 to 1 lowers it from 6 to 2.', 'mutate': weight_change_called_invariant},
        {'id': 'gamma2_at_representative_for_nonwindow', 'rationale': 'Report Gamma2 = 1 for the invalid-row window as if it were the source Gamma2 at the minimal residual; non-closed windows have non-unique minimal residuals and no class value.', 'mutate': gamma2_at_representative_for_nonwindow},
        {'id': 'lowered_weights_called_raising', 'rationale': 'Claim a restriction with lowered weights (2 to 1) raised Phi1 to 6; with weights not raised the monotonicity theorem applies and Phi1 is 2.', 'mutate': lowered_weights_called_raising},
        {'id': 'deletion_called_phi_neutral', 'rationale': 'Claim deleting five of six K4 edges leaves Phi1 = 3; the surviving edge is exact, so Phi1 falls to 0.', 'mutate': deletion_called_phi_neutral},
        {'id': 'routing_name_as_class', 'rationale': 'Put the routing/status name NoRule into the diagnostic-class field; the classes are ExactClass, ClosedResidual, ActiveClosureFailure, and a non-window is marked NotAWindow.', 'mutate': routing_name_as_class},
        {'id': 'subset_restriction_raised', 'rationale': 'Claim a restriction of K4 to three edges raised Phi1 from 3 to 4 although the weights and cochain are the restrictions.', 'mutate': subset_restriction_raised},
        {'id': 'primal_witness_not_optimal', 'rationale': 'Carry the zero potential and zero dual vector as the witness for the whole K4 window; both are feasible but their common value 0 is not Phi1 = 3.', 'mutate': primal_witness_not_optimal},
        {'id': 'face_survives_without_its_edges', 'rationale': 'Keep all four K4 faces after deleting edges; a 2-cell survives restriction only when its whole support does.', 'mutate': face_survives_without_its_edges},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The pairs are a set keyed by id; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
