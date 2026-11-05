import WitnessedDifference.Core

/-!
# Finite multiplicity normalization

Probabilities below are normalized finite multiplicities. Normalization
requires a nonzero denominator and proves no uniqueness principle.
-/

namespace WitnessedDifference.Probability

noncomputable def totalMultiplicity
    {Outcome : Type _} [Fintype Outcome]
    (count : Outcome → Nat) : ℚ :=
  ∑ outcome, (count outcome : ℚ)

noncomputable def normalizedMultiplicity
    {Outcome : Type _} [Fintype Outcome]
    (count : Outcome → Nat) (outcome : Outcome) : ℚ :=
  (count outcome : ℚ) / totalMultiplicity count

theorem normalizedMultiplicity_nonnegative
    {Outcome : Type _} [Fintype Outcome]
    (count : Outcome → Nat) (outcome : Outcome) :
    0 ≤ normalizedMultiplicity count outcome := by
  change 0 ≤ (count outcome : ℚ) / totalMultiplicity count
  unfold totalMultiplicity
  exact count_div_nonneg count outcome

theorem sum_normalizedMultiplicity
    {Outcome : Type _} [Fintype Outcome]
    (count : Outcome → Nat)
    (hnonzero : totalMultiplicity count ≠ 0) :
    (∑ outcome, normalizedMultiplicity count outcome) = 1 := by
  change sumUniv (fun outcome => (count outcome : ℚ) / totalMultiplicity count) = 1
  rw [sumUniv_div]
  change totalMultiplicity count / totalMultiplicity count = 1
  exact div_self (α := Outcome) (totalMultiplicity count) hnonzero

end WitnessedDifference.Probability
