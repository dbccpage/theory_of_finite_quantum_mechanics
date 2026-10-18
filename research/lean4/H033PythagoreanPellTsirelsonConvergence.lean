/-
  H033PythagoreanPellTsirelsonConvergence.lean
  AuthorityEffect: None.

  Shows in this model under exact integer arithmetic that:
  1. The Pell-convergent triple (119, 120, 169) is a primitive Pythagorean triple:
     119^2 + 120^2 = 169^2 = 28561.
  2. The measurement vectors at scale 169 are strictly orthonormal:
     b1 = (-119, 120) and b2 = (120, 119) have norm squared 28561 and dot product 0.
  3. The discrete Bell-CHSH sum at scale 169 evaluates to 478.
  4. It strictly violates the classical local realism bound (2 * 169 = 338) with quantum surplus 140.
  5. It strictly obeys the Tsirelson bound 2*sqrt(2):
     478^2 = 228484 < 228488 = 8 * 169^2, with exact integer deficit 228488 - 228484 = 4.
-/

namespace FableHilbertWalk20260819.H033

/-- Theorem: (119, 120, 169) is an exact Pythagorean triple. -/
theorem pell_triple_pythagorean :
    (119 : Int) ^ 2 + 120 ^ 2 = 169 ^ 2 := by decide

/-- Scale factor squared: 169^2 = 28561. -/
theorem scale_squared_eval : (169 : Int) ^ 2 = 28561 := by decide

/-- Orthogonality of Bob's measurement basis vectors:
    <(-119, 120), (120, 119)> = -119*120 + 120*119 = 0. -/
theorem pell_basis_orthogonality :
    (-119 : Int) * 120 + 120 * 119 = 0 := by decide

/-- Discrete Bell sum at scale 169: 120 + 119 + 119 + 120 = 478. -/
theorem pell_bell_sum_eval :
    (120 : Int) + 119 + 119 + 120 = 478 := by decide

/-- Classical local realism bound at scale 169: 2 * 169 = 338. -/
def classical_bound_169 : Int := 2 * 169

/-- Theorem: Strict violation of the classical local realism bound:
    478 > 338, with exact surplus 478 - 338 = 140. -/
theorem pell_bell_violates_classical :
    (478 : Int) > classical_bound_169 ∧ (478 : Int) - classical_bound_169 = 140 := by decide

/-- Scaled squared Tsirelson bound: 8 * 169^2 = 228488. -/
def tsirelson_bound_sq_169 : Int := 8 * (169 ^ 2)

theorem tsirelson_bound_sq_eval : tsirelson_bound_sq_169 = 228488 := by decide

/-- Theorem: Discrete Bell value strictly respects the continuous Tsirelson bound:
    478^2 = 228484 < 228488 = 8 * 169^2.
    The exact integer deficit is 228488 - 228484 = 4. -/
theorem pell_strictly_below_tsirelson :
    (478 : Int) ^ 2 < tsirelson_bound_sq_169 ∧
    tsirelson_bound_sq_169 - (478 : Int) ^ 2 = 4 := by decide

#print axioms pell_triple_pythagorean
#print axioms scale_squared_eval
#print axioms pell_basis_orthogonality
#print axioms pell_bell_sum_eval
#print axioms pell_bell_violates_classical
#print axioms tsirelson_bound_sq_eval
#print axioms pell_strictly_below_tsirelson

end FableHilbertWalk20260819.H033
