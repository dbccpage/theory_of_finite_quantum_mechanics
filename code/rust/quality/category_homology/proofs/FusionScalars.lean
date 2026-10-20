import Mathlib.Data.Int.ModEq
import Mathlib.Combinatorics.Enumerative.Partition.Basic

/-! AuthorityEffect: None. Exact signed modular scaling and its bounded
intermediate. This model does not extract Rust or prove client field laws. -/
namespace TFQM.FusionScalars

def exponent (k n step : Int) : Int := (k % n) * step

theorem scaled_reduction (k n step : Int) (hs : 0 < step) :
    (k * step) % (n * step) = exponent k n step := by
  simpa [exponent, mul_comm] using Int.mul_emod_mul_of_pos k n hs

theorem residue_nonnegative (k n : Int) (hn : 0 < n) : 0 ≤ k % n :=
  Int.emod_nonneg k (ne_of_gt hn)

theorem residue_below_order (k n : Int) (hn : 0 < n) : k % n < n :=
  Int.emod_lt_of_pos k hn

theorem exponent_bounds (k n step : Int) (hn : 0 < n) (hs : 0 < step) :
    0 ≤ exponent k n step ∧ exponent k n step < n * step := by
  constructor
  · exact Int.mul_nonneg (residue_nonnegative k n hn) (le_of_lt hs)
  · exact Int.mul_lt_mul_of_pos_right (residue_below_order k n hn) hs

theorem exponent_fits (k n step : Int) (hn : 0 < n) (hs : 0 < step)
    (hw : n * step ≤ 4096) :
    0 ≤ exponent k n step ∧ exponent k n step < 4096 := by
  have h := exponent_bounds k n step hn hs
  omega

theorem old_maximum_overflows : (9223372036854775807 : Int) * 4 > 9223372036854775807 := by
  decide

theorem maximum_reduced : exponent 9223372036854775807 3 4 = 4 := by decide
theorem minimum_reduced : exponent (-9223372036854775808) 3 4 = 4 := by decide

end TFQM.FusionScalars

#print axioms TFQM.FusionScalars.scaled_reduction
#print axioms TFQM.FusionScalars.residue_nonnegative
#print axioms TFQM.FusionScalars.residue_below_order
#print axioms TFQM.FusionScalars.exponent_bounds
#print axioms TFQM.FusionScalars.exponent_fits
#print axioms TFQM.FusionScalars.old_maximum_overflows
#print axioms TFQM.FusionScalars.maximum_reduced
#print axioms TFQM.FusionScalars.minimum_reduced
