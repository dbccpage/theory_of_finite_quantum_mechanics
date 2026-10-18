import «pl010_aggregator»

/-!
RDB-01: normalized residual weights.

This file gives a plan002-facing name to the finite L1 normalization already
proved in PaperQF002. The weights are obstruction/residual-sector weights. The
theorems do not claim physical probability or authority.
-/

open scoped BigOperators

namespace QM

namespace RDB01

noncomputable section

variable {S : Type*} [Fintype S]

/-- Total residual obstruction mass. -/
abbrev residualTotalMass (mass : S -> ℚ) : ℚ :=
  PaperQF002.totalWeight mass

/-- Normalized residual-sector weight. -/
abbrev residualWeight (mass : S -> ℚ) (s : S) : ℚ :=
  PaperQF002.directProb mass s

/-- Finite nonnegative residual masses with positive total normalize to a
probability distribution over residual sectors. -/
theorem normalizedResidualWeights_probability
    (mass : S -> ℚ)
    (hmass : ∀ s, 0 ≤ mass s) (hTotal : 0 < residualTotalMass mass) :
    (∀ s, 0 ≤ residualWeight mass s ∧ residualWeight mass s ≤ 1) ∧
      ∑ s, residualWeight mass s = 1 := by
  simpa [residualWeight, residualTotalMass] using
    PaperQF002.PL010_1_Theorem1_direct_normalization mass hmass hTotal

theorem normalizedResidualWeights_nonneg
    (mass : S -> ℚ)
    (hmass : ∀ s, 0 ≤ mass s) (hTotal : 0 < residualTotalMass mass)
    (s : S) :
    0 ≤ residualWeight mass s := by
  exact ((normalizedResidualWeights_probability mass hmass hTotal).1 s).1

theorem normalizedResidualWeights_le_one
    (mass : S -> ℚ)
    (hmass : ∀ s, 0 ≤ mass s) (hTotal : 0 < residualTotalMass mass)
    (s : S) :
    residualWeight mass s ≤ 1 := by
  exact ((normalizedResidualWeights_probability mass hmass hTotal).1 s).2

theorem normalizedResidualWeights_sum_eq_one
    (mass : S -> ℚ)
    (hTotal : residualTotalMass mass ≠ 0) :
    ∑ s, residualWeight mass s = 1 := by
  simpa [residualWeight, residualTotalMass] using
    PaperQF002.directProb_sum_eq_one mass hTotal

end

end RDB01

end QM

#print axioms QM.RDB01.normalizedResidualWeights_probability
#print axioms QM.RDB01.normalizedResidualWeights_sum_eq_one
