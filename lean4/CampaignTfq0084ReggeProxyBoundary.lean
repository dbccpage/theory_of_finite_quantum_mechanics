/-
Narrowed boundary for TFQ-0084.
The integers are the squared-area weighting on two declared pairs
and the two recorded defect-bound comparisons.
This module does not read the Rust file and does not derive an Einstein equation.
-/

theorem tfq0084_proxy_sum : (1 : Int) * 2 + 4 * 5 = 22 := by
  decide

theorem tfq0084_defect_sum : (2 : Int) + 5 = 7 := by
  decide

theorem tfq0084_proxy_ne_defects : (1 : Int) * 2 + 4 * 5 ≠ (2 : Int) + 5 := by
  decide

theorem tfq0084_proxy_ne_zero : (1 : Int) * 2 + 4 * 5 ≠ (0 : Int) := by
  decide

theorem tfq0084_fraction_difference : (1 : Int) * 4 - 1 * 3 = 1 ∧ (3 : Int) * 4 = 12 := by
  decide

theorem tfq0084_gap_square : (12 : Int) * 12 = 144 := by
  decide

theorem tfq0084_allowance_reduced : (2 : Int) * 8 = (1 : Int) * 16 := by
  decide

theorem tfq0084_allowance_square : (8 : Int) * 8 = 64 := by
  decide

theorem tfq0084_bound_strict : (1 : Int) * 64 < 1 * 144 := by
  decide

theorem tfq0084_second_gap : (1 : Int) * 16 > (1 : Int) * 1 := by
  decide

theorem tfq0084_negative_guard : (-1 : Int) < 0 := by
  decide

#print axioms tfq0084_proxy_sum
#print axioms tfq0084_defect_sum
#print axioms tfq0084_proxy_ne_defects
#print axioms tfq0084_proxy_ne_zero
#print axioms tfq0084_fraction_difference
#print axioms tfq0084_gap_square
#print axioms tfq0084_allowance_reduced
#print axioms tfq0084_allowance_square
#print axioms tfq0084_bound_strict
#print axioms tfq0084_second_gap
#print axioms tfq0084_negative_guard
