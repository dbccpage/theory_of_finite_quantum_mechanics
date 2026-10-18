import «rdb_03_amplitude_phase_non_unique»

/-!
RDB-13: diagnostic nonfaithfulness.

The diagonal residual-density bridge records residual mass, not signed
orientation. This file isolates the finite witness: two distinct signed
residual pairs can have the same orientation-blind residual weights.
-/

namespace QM

namespace RDB13

def orientationBlindResidualWeights (p : ℚ × ℚ) : ℚ × ℚ :=
  (abs p.1, abs p.2)

def positiveOrientationWitness : ℚ × ℚ :=
  ((2 : ℚ), (-3 : ℚ))

def reversedOrientationWitness : ℚ × ℚ :=
  ((-2 : ℚ), (3 : ℚ))

theorem orientationBlindResidualWeights_alias :
    orientationBlindResidualWeights positiveOrientationWitness =
      orientationBlindResidualWeights reversedOrientationWitness := by
  rfl

theorem orientationWitnesses_distinct :
    positiveOrientationWitness ≠ reversedOrientationWitness := by
  intro h
  have hfst := congrArg Prod.fst h
  norm_num [positiveOrientationWitness, reversedOrientationWitness] at hfst

theorem orientationBlindResidualDensity_nonfaithful :
    orientationBlindResidualWeights positiveOrientationWitness =
        orientationBlindResidualWeights reversedOrientationWitness ∧
      positiveOrientationWitness ≠ reversedOrientationWitness := by
  exact ⟨orientationBlindResidualWeights_alias, orientationWitnesses_distinct⟩

theorem not_orientationBlindResidualWeights_injective :
    ¬ Function.Injective orientationBlindResidualWeights := by
  intro h
  exact orientationWitnesses_distinct
    (h orientationBlindResidualWeights_alias)

end RDB13

end QM

#print axioms QM.RDB13.orientationBlindResidualDensity_nonfaithful
#print axioms QM.RDB13.not_orientationBlindResidualWeights_injective
