"""Semantic near misses for the degree-1 window certificate (PG-WDP-DEGREE1-WINDOW).

Each mutant is a well-formed record a reviewer could believe that breaks one premise of the node.
"""


def _rec(data, ident):
    return next(r for r in data['records'] if r['id'] == ident)


def semantic_mutants(data, profile):
    def violating_window_declared_exact(d):
        r = _rec(d, 'violates_d1d0_edge')
        r['complex'] = True
        r['dim_h1'] = 0
        r['diag'] = 'ExactClass'
        r['kappa_witness'] = None

    def active_read_as_closed(d):
        _rec(d, 'tri_filled_active')['diag'] = 'ClosedResidual'

    def closed_residual_read_as_exact(d):
        _rec(d, 'tri_unfilled_closed')['diag'] = 'ExactClass'
        _rec(d, 'tri_unfilled_closed')['r_cl'] = None

    def unrepaired_sum_as_phi1(d):
        r = _rec(d, 'k4_three_faces')
        r['phi1'] = '5'
        r['r_cl'] = '4/5'

    def weights_ignored(d):
        r = _rec(d, 'tri_heavy_weights')
        r['phi1'] = '2'
        r['r_cl'] = '1'

    def h1_dimension_without_quotient(d):
        _rec(d, 'tri_unfilled_closed')['dim_h1'] = 3

    def ratio_defined_when_phi_zero(d):
        _rec(d, 'tri_filled_exact')['r_cl'] = '0'

    def loop_edge_repaired(d):
        r = _rec(d, 'loop_active')
        r['phi1'] = '0'
        r['diag'] = 'ExactClass'
        r['r_cl'] = None

    def refusal_hidden_by_ratio(d):
        r = _rec(d, 'violates_d1d0_signs')
        r['diag'] = 'ActiveClosureFailure'
        r['r_cl'] = '1'
        r['gamma2'] = '2'
        r['dim_h1'] = 1
        r['complex'] = True
        r['kappa_witness'] = None

    def gauge_shift_changes_phi1(d):
        _rec(d, 'tri_filled_active_shifted')['phi1'] = '4'
        _rec(d, 'tri_filled_active_shifted')['r_cl'] = '1/2'

    def gamma2_with_weights(d):
        r = _rec(d, 'tri_heavy_weights')
        r['gamma2'] = '6'
        r['r_cl'] = '1'

    def dim_q1_uses_rank_d1(d):
        _rec(d, 'tri_filled_active')['dim_q1'] = 2

    def sign_ignored_rank_accepts_row(d):
        r = _rec(d, 'violates_d1d0_signs')
        r['complex'] = True
        r['dim_h1'] = 0
        r['gamma2'] = '2'
        r['r_cl'] = '1'
        r['diag'] = 'ActiveClosureFailure'
        r['kappa_witness'] = None

    def nonwindow_keeps_representative_gamma2(d):
        _rec(d, 'violates_d1d0_edge')['gamma2'] = '2'

    def primal_potential_not_optimal(d):
        _rec(d, 'tri_filled_exact')['witness'] = 'x=0,0,0|y=1,1,-1'

    def dual_vector_exceeds_weights(d):
        _rec(d, 'tri_filled_active')['witness'] = 'x=-2,-1,0|y=2,2,-2'

    return [
        {'id': 'violating_window_declared_exact', 'rationale': 'Treat kappa1 as defined on Q1 for a window with d1 d0 != 0 (the representatives 0 and d0 e_0 of the zero class have different d1 values).', 'mutate': violating_window_declared_exact},
        {'id': 'active_read_as_closed', 'rationale': 'Ignore the closure charge: the filled triangle with Gamma2 = 2 is called a closed residual.', 'mutate': active_read_as_closed},
        {'id': 'closed_residual_read_as_exact', 'rationale': 'Call the unfilled triangle class exact because Gamma2 = 0; its Phi1 is 1, so the class is a nonzero element of H1.', 'mutate': closed_residual_read_as_exact},
        {'id': 'unrepaired_sum_as_phi1', 'rationale': 'Read the sum of edge residuals (the source Lean list sum) as Phi1; the quotient defect is the minimum over potentials and is smaller (3 vs 5 on K4).', 'mutate': unrepaired_sum_as_phi1},
        {'id': 'weights_ignored', 'rationale': 'Compute Phi1 with unit weights for a window whose norm J has weight 3 on every edge.', 'mutate': weights_ignored},
        {'id': 'h1_dimension_without_quotient', 'rationale': 'Take dim H1 = dim ker d1 (cycles) without quotienting by im d0.', 'mutate': h1_dimension_without_quotient},
        {'id': 'ratio_defined_when_phi_zero', 'rationale': 'Report R_cl = 0 for an exact class, as the Rust TriadSignature::r_cl convention does; the node statement defines R_cl = Gamma2/Phi1 only when Phi1 > 0.', 'mutate': ratio_defined_when_phi_zero},
        {'id': 'loop_edge_repaired', 'rationale': 'Claim a potential repairs a loop edge; d0 of a loop is zero so Phi1 = 3 there.', 'mutate': loop_edge_repaired},
        {'id': 'gauge_shift_changes_phi1', 'rationale': 'Report the unrepaired residual sum 4 for h + d0 (0,1,1); Phi1 and R_cl are class functions and stay 2 and 1.', 'mutate': gauge_shift_changes_phi1},
        {'id': 'gamma2_with_weights', 'rationale': 'Weight Gamma2 by J (6 for the weight-3 triangle); Gamma2 is the unweighted L1 norm of d1 h, so R_cl = 1/3 is scale dependent by definition.', 'mutate': gamma2_with_weights},
        {'id': 'dim_q1_uses_rank_d1', 'rationale': 'Swap the quotient: dim Q1 = m - rank d1 (dimension of cycles) instead of m - rank d0.', 'mutate': dim_q1_uses_rank_d1},
        {'id': 'sign_ignored_rank_accepts_row', 'rationale': 'Accept the row (1,1,1) as a 2-cell because its coboundary vanishes mod 2; over Q it gives d1 d0 e_0 = -2.', 'mutate': sign_ignored_rank_accepts_row},
        {'id': 'nonwindow_keeps_representative_gamma2', 'rationale': 'Report Gamma2 = 2 for the window with d1 d0 != 0; there Gamma2 depends on the representative (0 at h = 0, 2 at h = 2), so no class value exists.', 'mutate': nonwindow_keeps_representative_gamma2},
        {'id': 'primal_potential_not_optimal', 'rationale': 'Carry the zero potential as the primal witness of the exact class h = (1,2,3); its cost is 6, not Phi1 = 0.', 'mutate': primal_potential_not_optimal},
        {'id': 'dual_vector_exceeds_weights', 'rationale': 'Carry the dual vector (2,2,-2) for the unit-weight triangle: it annihilates coboundaries and pairs to 4 but violates |y_e| <= w_e, so it is no lower bound.', 'mutate': dual_vector_exceeds_weights},
        {'id': 'refusal_hidden_by_ratio', 'rationale': 'Hide the NoRule refusal of a window with d1 d0 != 0 behind an ActiveClosureFailure line with a finite ratio.', 'mutate': refusal_hidden_by_ratio},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The windows are a set keyed by id; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
