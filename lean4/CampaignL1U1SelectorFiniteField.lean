/-
Narrowed finite-field table for L1-U1-SELECTOR-OTHER-SEGMENT.
Z/5Z pairs of norm 1, the order of (0, 1), one off-circle pair,
and one nonzero norm-zero pair. This module does not select C or U(1).
-/

def mul5 (a b c d : Fin 5) : Fin 5 × Fin 5 :=
  (a * c + (4 : Fin 5) * (b * d), a * d + b * c)

def circleCount : Nat :=
  (List.range 5).foldl (fun acc x =>
    (List.range 5).foldl (fun acc2 y =>
      if (x * x + y * y) % 5 = 1 then acc2 + 1 else acc2) acc) 0

theorem circle_iff (x y : Fin 5) :
    x * x + y * y = 1 ↔
      (x = 0 ∧ y = 1) ∨ (x = 0 ∧ y = 4) ∨ (x = 1 ∧ y = 0) ∨ (x = 4 ∧ y = 0) := by
  revert x y
  decide

theorem circle_count : circleCount = 4 := rfl

theorem four_eq_pred_five : 4 = 5 - 1 := rfl

theorem six_eq_succ_five : 5 + 1 = 6 := rfl

theorem four_ne_six : 4 ≠ 6 := by
  decide

theorem four_plus_one_eq_zero : (4 : Fin 5) + 1 = 0 := by
  decide

theorem gen_square : mul5 0 1 0 1 = (4, 0) := by
  decide

theorem gen_square_ne_one : ((4 : Fin 5), 0) ≠ (1, 0) := by
  decide

theorem gen_cube : mul5 4 0 0 1 = (0, 4) := by
  decide

theorem gen_fourth : mul5 0 4 0 1 = (1, 0) := by
  decide

theorem off_circle_one_one : (1 : Fin 5) * 1 + 1 * 1 ≠ 1 := by
  decide

theorem one_one_norm : (1 : Fin 5) * 1 + 1 * 1 = 2 := by
  decide

theorem two_ne_one : 2 ≠ 1 := by
  decide

theorem isotropic_nonzero : ((2 : Fin 5), 1) ≠ (0, 0) := by
  decide

theorem isotropic_norm_zero : (2 : Fin 5) * 2 + 1 * 1 = 0 := by
  decide

#print axioms circle_iff
#print axioms circle_count
#print axioms four_eq_pred_five
#print axioms six_eq_succ_five
#print axioms four_ne_six
#print axioms four_plus_one_eq_zero
#print axioms gen_square
#print axioms gen_square_ne_one
#print axioms gen_cube
#print axioms gen_fourth
#print axioms off_circle_one_one
#print axioms one_one_norm
#print axioms two_ne_one
#print axioms isotropic_nonzero
#print axioms isotropic_norm_zero
