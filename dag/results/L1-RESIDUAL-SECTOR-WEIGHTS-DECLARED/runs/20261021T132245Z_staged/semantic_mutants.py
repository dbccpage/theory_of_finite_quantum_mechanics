"""Semantic near misses for the residual sector-weight certificate (L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED).

Each mutant is a well-formed record that a reviewer could believe and each breaks one premise or reads a fixed
instance as the general statement.
"""


def _rec(data, n, c):
    return next(r for r in data['records'] if r['kind'] == 'residual' and r['input'][1] == n and r['input'][2] == list(c))


def _weighted(data, masses):
    return next(r for r in data['records'] if r['kind'] == 'weighted' and r['input'][4] == list(masses))


def semantic_mutants(data, profile):
    def unique_minimizer_from_one_witness(d):
        r = _rec(d, 4, (1, 0, 1, 0))
        r['minimizer_count'] = 1
        r['unique'] = True
        r['lex_min'] = r['lex_max'] = [2, 0, 0, 0]
        r['sector_vectors'] = [[2, 0]]
        r['determined'] = True

    def orbit_sum_as_symmetric_point(d):
        r = _rec(d, 4, (1, 0, 1, 0))
        r['symmetric'] = [1, 1]

    def rounded_symmetric_point_integral(d):
        r = _rec(d, 6, (1, 0, 0, 0, 0, 0))
        r['symmetric'] = [0, 1]
        r['symmetric_integral'] = True

    def zero_mass_accepted(d):
        _rec(d, 4, (1, -1, 0, 0))['status'] = 'ok'

    def one_edge_still_nonunique(d):
        r = _rec(d, 1, (5,))
        r['minimizer_count'] = 2
        r['unique'] = False

    def single_sector_weight_varies(d):
        r = _rec(d, 4, (1, 1, 0, 0))
        r['sector_vectors'] = [[0], [2]]
        r['determined'] = False

    def raw_l1_read_as_phi1(d):
        _rec(d, 4, (3, -1, -1, 0))['phi1'] = 5

    def negative_class_with_positive_minimizers(d):
        r = _rec(d, 4, (-2, 0, -1, 0))
        r['lex_min'], r['lex_max'] = [0, 0, 0, 3], [3, 0, 0, 0]

    def holonomy_as_absolute_value(d):
        _rec(d, 3, (2, -3, 0))['holonomy'] = 1

    def minimizers_counted_by_sector_vectors(d):
        _rec(d, 4, (1, 0, 1, 0))['minimizer_count'] = 3

    def weighted_l1_treated_as_unweighted(d):
        # unequal masses (1,2,3,4): the unique minimizer sits on the minimal-mass edge, but the unweighted table is read instead
        r = _weighted(d, (1, 2, 3, 4))
        r['minimizer_count'] = 10
        r['unique'] = False
        r['lex_min'], r['lex_max'] = [0, 0, 0, 2], [2, 0, 0, 0]
        r['sector_vectors'] = [[0, 2], [1, 1], [2, 0]]
        r['determined'] = False

    def gamma2_as_sum_of_squares_constant_on_minimizers(d):
        r = _rec(d, 4, (1, 0, 1, 0))
        r['sumsq_min'] = r['sumsq_max'] = 4

    def cycle_rank_two_single_holonomy(d):
        r = next(x for x in d['records'] if x['kind'] == 'twocycle' and x['input'][2] == [2, 0, 0])
        r['phi1'] = 1
        r['total_gives_phi1'] = True

    def determined_but_not_unique_read_as_free(d):
        r = _weighted(d, (2, 2, 1, 1))
        r['sector_vectors'] = [[0, 3], [1, 2]]
        r['determined'] = False

    return [
        {'id': 'unique_minimizer_from_one_witness', 'rationale': 'Read the single C4 witness (1,0,1,0)->(2,0,0,0) as "the" minimizer; the minimizer set is a simplex with 10 points.', 'mutate': unique_minimizer_from_one_witness},
        {'id': 'orbit_sum_as_symmetric_point', 'rationale': 'The source orbit SUM (1,1,1,1) has total 4 while Phi1 = 2; the canonical symmetric point is the orbit average (1/2 each).', 'mutate': orbit_sum_as_symmetric_point},
        {'id': 'rounded_symmetric_point_integral', 'rationale': 'Round the symmetric selector 1/6 to an integer cochain; the cyclically invariant minimizer is integral only when n divides the holonomy.', 'mutate': rounded_symmetric_point_integral},
        {'id': 'zero_mass_accepted', 'rationale': 'Accept holonomy 0 as a valid weight vector; the minimizer is the zero residual and the declared total M = 0 is refused.', 'mutate': zero_mass_accepted},
        {'id': 'one_edge_still_nonunique', 'rationale': 'Claim non-uniqueness for a 1-cycle; the class has a single point there, so the hypothesis n >= 2 cannot be dropped.', 'mutate': one_edge_still_nonunique},
        {'id': 'single_sector_weight_varies', 'rationale': 'Claim the weight of a single sector (all edges) varies; it equals Phi1 for every minimizer, so only a split into two or more sectors is undetermined.', 'mutate': single_sector_weight_varies},
        {'id': 'raw_l1_read_as_phi1', 'rationale': 'Phi1 is the minimum of the L1 form over the class c - d0 h, not the raw L1 form of the representative c (off by the gauge).', 'mutate': raw_l1_read_as_phi1},
        {'id': 'negative_class_with_positive_minimizers', 'rationale': 'For holonomy -3 the minimizers are the nonpositive cochains; sign convention swapped.', 'mutate': negative_class_with_positive_minimizers},
        {'id': 'holonomy_as_absolute_value', 'rationale': 'Gamma2 is the signed holonomy; replacing it by |S| loses the orientation of the class.', 'mutate': holonomy_as_absolute_value},
        {'id': 'minimizers_counted_by_sector_vectors', 'rationale': 'Count minimizers by their distinct sector-weight vectors (3) instead of by residual cochains (10).', 'mutate': minimizers_counted_by_sector_vectors},
        {'id': 'weighted_l1_treated_as_unweighted', 'rationale': 'With unequal declared edge masses (1,2,3,4) the minimizer is the single point (2,0,0,0) on the minimal-mass edge; the equal-mass non-uniqueness table does not carry over.', 'mutate': weighted_l1_treated_as_unweighted},
        {'id': 'gamma2_as_sum_of_squares_constant_on_minimizers', 'rationale': 'If Gamma2 were the sum of squares of the weights it is 2 for (1,1,0,0) but 4 for (2,0,0,0): the minimizers do not share it, so the two readings of Gamma2 give different fibers.', 'mutate': gamma2_as_sum_of_squares_constant_on_minimizers},
        {'id': 'cycle_rank_two_single_holonomy', 'rationale': 'For two disjoint cycles with holonomies 2 and -1 the total holonomy is 1 but Phi1 = 3; one holonomy no longer determines the class or Phi1.', 'mutate': cycle_rank_two_single_holonomy},
        {'id': 'determined_but_not_unique_read_as_free', 'rationale': 'With masses (2,2,1,1) both minimal edges lie in the second sector, so the sector weights (0,3) are determined although the minimizer is not unique.', 'mutate': determined_but_not_unique_read_as_free},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
