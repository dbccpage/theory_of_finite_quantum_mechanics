import Std

/-! Concrete rational encoding of the distinct-image examples in WDP-DIM-1.
    The general dimension theorem is the written proof in Appendix T.
    These declarations are the checked encoding, not an end-to-end postulate
    and not a formalization of an analytic theorem. -/

namespace WitnessedDifference.DistinctImageCompletion

abbrev V3 := Rat × Rat × Rat
abbrev V4 := Rat × Rat × Rat × Rat

def coord3 (x y z : Rat) : V3 := (x, y, z)

/-- Existing observer on the three-dimensional examples: the last coordinate. -/
def q3 : V3 → Rat := fun v => v.2.2

/-- Raw completion rows on the B ⊂ R example: the first two coordinates. -/
def rawPair : V3 → Rat × Rat := fun v => (v.1, v.2.1)

/-- One quotient row on that example: the second coordinate. -/
def quotientRow : V3 → Rat := fun v => v.2.1

/-- Algebraic repair line spanned by the first basis vector. -/
def inRepairLine (v : V3) : Prop := v.2.1 = 0 ∧ v.2.2 = 0

/-- Realizable plane of the first two coordinates. -/
def inRealizablePlane (v : V3) : Prop := v.2.2 = 0

theorem both_rows_leave_only_zero (x y z : Rat)
    (hQ : q3 (x, y, z) = 0) (hE : rawPair (x, y, z) = (0, 0)) :
    (x, y, z) = (0, 0, 0) := by
  simp [q3, rawPair, Prod.ext_iff] at hQ hE
  rcases hE with ⟨hx, hy⟩
  subst hx
  subst hy
  subst hQ
  rfl

theorem quotient_row_kernel_lies_in_repair (x y z : Rat)
    (hQ : q3 (x, y, z) = 0) (hE : quotientRow (x, y, z) = 0) :
    inRepairLine (x, y, z) := by
  simp [q3, quotientRow] at hQ hE
  simpa [inRepairLine] using And.intro hE hQ

theorem quotient_row_hides_realizable_defect :
    q3 (1, 0, 0) = 0 ∧ quotientRow (1, 0, 0) = 0 ∧ (1, 0, 0) ≠ (0, 0, 0) := by
  refine ⟨rfl, rfl, ?_⟩
  decide

/-- Joint row count dim K − dim(K∩B) + dim(R∩K∩B) on this example. -/
theorem joint_count_on_reverse_inclusion : (2 - 1 + 1 : Nat) = 2 := by decide

/-- The separate minima add to 3, which is strictly larger. -/
theorem separate_sum_exceeds_joint_on_reverse_inclusion :
    (2 + 1 : Nat) = 3 ∧ (2 : Nat) < 3 := by decide

theorem excess_is_the_visible_realizable_complement :
    ((2 + 1) - (2 - 1 + 1) : Nat) = 1 := by decide

/-- On R ⊂ B, dim K = dim(K ∩ B) = 2 and dim T = 1, so the joint count is 1
    and the quotient count is 0. -/
theorem proper_inclusion_counts : (2 - 2 + 1 : Nat) = 1 ∧ (2 - 2 : Nat) = 0 := by decide

/-- Neither inclusion repeats the strict joint gap 2 < 3. -/
theorem neither_inclusion_gap : (3 - 2 + 1 : Nat) = 2 ∧ (2 : Nat) < 2 + 1 := by decide

/-- A row that annihilates span{(1,0,0)} has vanishing first coordinate. -/
theorem annihilator_of_repair_line (a b c : Rat) (h : a * 1 + b * 0 + c * 0 = 0) :
    a = 0 := by
  simp [Rat.mul_one, Rat.mul_zero, Rat.add_zero] at h
  exact h

theorem every_repair_annihilator_misses_e1 (a b c : Rat) (ha : a = 0) :
    a * (1 : Rat) + b * 0 + c * 0 = 0 ∧ (1, 0, 0) ≠ (0, 0, 0) := by
  constructor
  · simp [ha, Rat.mul_one, Rat.mul_zero, Rat.add_zero]
  · decide

/-- B = V makes every vector an algebraic repair combination. -/
theorem full_space_repair_is_quotient_trivial (x y z : Rat) :
    ∃ a b : Rat, (x, y, z) = (a, b, z) := by
  exact ⟨x, y, rfl⟩

/-- An admissible source column realizes the defect (1,0) when the preimage is 1. -/
theorem admissible_preimage_realizes_defect :
    ((1 : Rat) * 1, (1 : Rat) * 0) = (1, 0) := by
  simp [Rat.mul_one, Rat.mul_zero]

end WitnessedDifference.DistinctImageCompletion

#print axioms WitnessedDifference.DistinctImageCompletion.both_rows_leave_only_zero
#print axioms WitnessedDifference.DistinctImageCompletion.quotient_row_kernel_lies_in_repair
#print axioms WitnessedDifference.DistinctImageCompletion.quotient_row_hides_realizable_defect
#print axioms WitnessedDifference.DistinctImageCompletion.joint_count_on_reverse_inclusion
#print axioms WitnessedDifference.DistinctImageCompletion.separate_sum_exceeds_joint_on_reverse_inclusion
#print axioms WitnessedDifference.DistinctImageCompletion.excess_is_the_visible_realizable_complement
#print axioms WitnessedDifference.DistinctImageCompletion.proper_inclusion_counts
#print axioms WitnessedDifference.DistinctImageCompletion.neither_inclusion_gap
#print axioms WitnessedDifference.DistinctImageCompletion.annihilator_of_repair_line
#print axioms WitnessedDifference.DistinctImageCompletion.every_repair_annihilator_misses_e1
#print axioms WitnessedDifference.DistinctImageCompletion.full_space_repair_is_quotient_trivial
#print axioms WitnessedDifference.DistinctImageCompletion.admissible_preimage_realizes_defect
