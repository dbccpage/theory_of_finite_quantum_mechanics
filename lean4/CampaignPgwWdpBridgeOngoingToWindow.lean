/-
Narrowed boundary for PGW-WDP-BRIDGE-ONGOING-TO-WINDOW.
Three positions labeled 0, 1, 2.
The coboundary on an ordered triple is (g0 - g1, g1 - g2, g2 - g0).
This module does not build a general marked family or a degree-1 window.
-/

/-- Round sum of a coboundary on positions 0, 1, 2. -/
theorem pgwBr_gradient_round (g0 g1 g2 : Int) :
    (g0 - g1) + (g1 - g2) + (g2 - g0) = 0 := by
  omega

/-- Adding a coboundary leaves the oriented diagnostic unchanged. -/
theorem pgwBr_shift_preserves (e01 e12 e20 g0 g1 g2 : Int) :
    (e01 + (g0 - g1)) + (e12 + (g1 - g2)) + (e20 + (g2 - g0))
      = e01 + e12 + e20 := by
  omega

/-- The mark (1, 1, 1) has diagnostic 3, and it stays 3 after the shift from (2, 5, 11). -/
theorem pgwBr_unbalanced :
    ((1 : Int) + 1 + 1 = 3) ∧
      ((1 : Int) + (2 - 5)) + ((1 : Int) + (5 - 11)) + ((1 : Int) + (11 - 2)) = 3 := by
  constructor
  · omega
  · omega

/-- A diagonal coboundary is 0, so the loop value 4 is not one. -/
theorem pgwBr_loop_diag (g : Int) : g - g = 0 := by
  omega

theorem pgwBr_loop_not_coboundary (g : Int) : g - g ≠ 4 := by
  omega

/-- Oriented arcs 0, 0, 0 have diagnostic 0 while the loop value is 4. -/
theorem pgwBr_loop_report :
    ((0 : Int) + 0 + 0 = 0) ∧ (4 ≠ 0) := by
  omega

/-- Forward arc 3 has oriented diagnostic 3. The two-way sum with 5 is 8. -/
theorem pgwBr_two_way :
    ((3 : Int) + 0 + 0 = 3) ∧ (3 + 5 = 8) ∧ (3 ≠ 8) := by
  omega

#print axioms pgwBr_gradient_round
#print axioms pgwBr_shift_preserves
#print axioms pgwBr_unbalanced
#print axioms pgwBr_loop_diag
#print axioms pgwBr_loop_not_coboundary
#print axioms pgwBr_loop_report
#print axioms pgwBr_two_way
