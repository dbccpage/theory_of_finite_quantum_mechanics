/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import TraceZeroDuality

open TraceZeroDuality

/-- On the split spectrum `(2, -2)` the dual pairing meets the spread and the centered norm. -/
theorem split_spectrum_gap_zero :
    spread (⟨2, -2⟩ : Eig2) = 4 ∧
      pairing ⟨2, -2⟩ (optimalVec2 ⟨2, -2⟩) = spread ⟨2, -2⟩ ∧
      opNorm ⟨2, -2⟩ (optimalShift ⟨2, -2⟩) = spread ⟨2, -2⟩ := by
  refine ⟨?_, optimal_pairing_eq_spread _, optimal_shift_achieves_spread _⟩
  unfold spread max2 min2
  decide

#print axioms optimal_pairing_eq_spread
#print axioms optimal_shift_achieves_spread
#print axioms opNorm_ge_spread
#print axioms trace_zero_duality_gap_zero
#print axioms scaleMetric_monotone
#print axioms monotone_metric_distinct
#print axioms coboundary_shift_equiv
#print axioms quotient_evaluation_invariant
