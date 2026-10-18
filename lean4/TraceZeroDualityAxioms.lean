
import TraceZeroDuality

open TraceZeroDuality

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

private def l5aProvenance : String :=
  "Origin: lean4/TraceZeroDualityAxioms.lean Claim: split_spectrum_gap_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
