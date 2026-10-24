/-
Narrowed boundary for TFQ-0177.
The integers are the Segre pieces at the point (1, 1, 1, 1)
and the cleared collar comparison for -1/1000.
This module does not read the deposit files and does not decide
whether seven mutually unbiased bases exist in dimension 6.
-/

theorem tfq0177_point_quadric :
    ((1 : Int) - 1) * ((1 : Int) - 1) - ((1 : Int) - 1) * ((1 : Int) - 1) = 0 := by
  decide

theorem tfq0177_point_squares :
    ((1 : Int) * 1 - 1) + (1 * 1 - 1) + (1 * 1 - 1) + (1 * 1 - 1) = 0 := by
  decide

theorem tfq0177_guard_cleared : (0 : Int) * 1000 - 1 = -1 := by
  decide

theorem tfq0177_collar_sign : (-1 : Int) < 0 ∧ (0 : Int) < 1000 := by
  decide

#print axioms tfq0177_point_quadric
#print axioms tfq0177_point_squares
#print axioms tfq0177_guard_cleared
#print axioms tfq0177_collar_sign
