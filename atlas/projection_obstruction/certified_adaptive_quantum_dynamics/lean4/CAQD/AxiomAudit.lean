import CAQD.ShortTimeRate

-- Core Duhamel bounds
#print axioms CAQD.abs_stepPairing_le_sumAbs
#print axioms CAQD.single_step_holder_bound
#print axioms CAQD.sumAbsPairing_le_bound
#print axioms CAQD.duhamel_observable_bound

-- Local edge decomposition and margin honesty
#print axioms CAQD.trajectory_residual_le_edge_sum
#print axioms CAQD.certificate_honesty
#print axioms CAQD.margin_nonnegative

-- Tolerance satisfaction and refinement monotonicity
#print axioms CAQD.certified_tolerance_satisfaction
#print axioms CAQD.refinement_monotonicity

-- Short-time rate consistency
#print axioms CAQD.single_step_rate
#print axioms CAQD.leading_linear_rate_matches_defect_sum
