import «rdb_01_normalized_residual_weights»

/-!
RDB-02: diagonal residual-density embedding.

The finite L1 residual distribution embeds into a diagonal density carrier.
This is a finite diagonal model: positivity is diagonal nonnegativity and trace
is the sum of diagonal entries. It is a diagnostic representation, not a
physical-density ontology claim.
-/

open scoped BigOperators

namespace QM

namespace RDB02

noncomputable section

variable {S : Type*} [Fintype S]

/-- Trace of a finite diagonal carrier. -/
def DiagonalTrace (diag : S -> ℚ) : ℚ :=
  ∑ s, diag s

/-- PSD in the finite diagonal sense: all diagonal entries are nonnegative. -/
def DiagonalPSD (diag : S -> ℚ) : Prop :=
  ∀ s, 0 ≤ diag s

/-- The diagonal residual density associated to obstruction masses. -/
abbrev residualDiagonalDensity (mass : S -> ℚ) : S -> ℚ :=
  RDB01.residualWeight mass

/-- Measurement in the residual-sector basis returns the corresponding diagonal
entry, hence the normalized residual weight. -/
def residualSectorMeasurement (diag : S -> ℚ) (s : S) : ℚ :=
  diag s

theorem residualDiagonalDensity_trace_one
    (mass : S -> ℚ) (hTotal : RDB01.residualTotalMass mass ≠ 0) :
    DiagonalTrace (residualDiagonalDensity mass) = 1 := by
  simpa [DiagonalTrace, residualDiagonalDensity, RDB01.residualWeight] using
    RDB01.normalizedResidualWeights_sum_eq_one mass hTotal

theorem residualDiagonalDensity_psd
    (mass : S -> ℚ)
    (hmass : ∀ s, 0 ≤ mass s) (hTotal : 0 < RDB01.residualTotalMass mass) :
    DiagonalPSD (residualDiagonalDensity mass) := by
  intro s
  exact RDB01.normalizedResidualWeights_nonneg mass hmass hTotal s

theorem residualSectorMeasurement_returns_weight
    (mass : S -> ℚ) (s : S) :
    residualSectorMeasurement (residualDiagonalDensity mass) s =
      RDB01.residualWeight mass s := by
  rfl

/-- Residual Density Representation Theorem, diagonal finite slice. -/
theorem residualDensityRepresentation_certificate
    (mass : S -> ℚ)
    (hmass : ∀ s, 0 ≤ mass s) (hTotal : 0 < RDB01.residualTotalMass mass) :
    DiagonalPSD (residualDiagonalDensity mass) ∧
      DiagonalTrace (residualDiagonalDensity mass) = 1 ∧
      ∀ s, residualSectorMeasurement (residualDiagonalDensity mass) s =
        RDB01.residualWeight mass s := by
  exact
    ⟨residualDiagonalDensity_psd mass hmass hTotal,
      residualDiagonalDensity_trace_one mass (ne_of_gt hTotal),
      residualSectorMeasurement_returns_weight mass⟩

end

end RDB02

end QM

#print axioms QM.RDB02.residualDiagonalDensity_trace_one
#print axioms QM.RDB02.residualDensityRepresentation_certificate
