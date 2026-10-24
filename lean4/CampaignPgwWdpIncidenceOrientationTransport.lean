import Imported.OeWdp.GenesisIncidence
import Imported.WitnessedDifference.WitnessedDifference.Obstruction

open GenesisIncidence WitnessedDifference.Obstruction

/-
Narrowed boundary for PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT.
Vertices 0, 1, 2. Edge slots 01, 02, 12 swap to 01, 12, 02.
Reversing slot 02 toward 20 negates that component.
This module does not transport a general window quantity.
-/

/-- Swap the last two coordinates: slots (01, 02, 12) become (01, 12, 02). -/
def pgwInc_swap23 (a b c : Int) : Int × Int × Int :=
  (a, c, b)

theorem pgwInc_swap_involutive (a b c : Int) :
    (let w := pgwInc_swap23 a b c
     pgwInc_swap23 w.1 w.2.1 w.2.2) = (a, b, c) := by
  rfl

theorem pgwInc_face_swapped :
    pgwInc_swap23 (d2 1).x (d2 1).y (d2 1).z = (1, 1, -1) := by
  simp [pgwInc_swap23, d2]

theorem pgwInc_row :
    triD1Row .e01 = (1 : Rat) ∧ triD1Row .e12 = 1 ∧ triD1Row .e02 = -1 :=
  And.intro rfl (And.intro rfl rfl)

theorem pgwInc_face_is_row :
    ((d2 1).x : Rat) = triD1Row .e01 ∧
      ((d2 1).z : Rat) = triD1Row .e12 ∧
      ((d2 1).y : Rat) = triD1Row .e02 := by
  simp [d2, triD1Row]

/-- Negate the 02 slot, the sign change from edge 02 to edge 20. -/
def pgwInc_reverse02 (a01 a12 a02 : Int) : Int × Int × Int :=
  (a01, a12, -a02)

theorem pgwInc_face_cyclic :
    (let w := pgwInc_swap23 (d2 1).x (d2 1).y (d2 1).z
     pgwInc_reverse02 w.1 w.2.1 w.2.2) = (1, 1, 1) := by
  simp [pgwInc_swap23, pgwInc_reverse02, d2]

/-- Vertex boundary of the swapped face column (1, 1, -1), in slot order (01, 12, 02). -/
theorem pgwInc_transported_cycle :
    match pgwInc_swap23 (d2 1).x (d2 1).y (d2 1).z with
    | (a01, a12, a02) => -a01 - a02 = 0 ∧ a01 - a12 = 0 ∧ a12 + a02 = 0 := by
  simp [pgwInc_swap23, d2]

theorem pgwInc_dot_matches_order (a01 a02 a12 : Int) :
    a01 * 1 + a02 * (-1) + a12 * 1 = a01 + a12 - a02 := by
  omega

theorem pgwInc_swapped_coord_is_tri (a01 a12 a02 : Int) :
    (a01 : Rat) + (a12 : Rat) - (a02 : Rat) =
      triD1 (fun e =>
        match e with
        | .e01 => (a01 : Rat)
        | .e12 => (a12 : Rat)
        | .e02 => (a02 : Rat)) := by
  unfold triD1
  rfl

theorem pgwInc_face_tri :
    triD1 (fun e =>
      match e with
      | .e01 => ((d2 1).x : Rat)
      | .e12 => ((d2 1).z : Rat)
      | .e02 => ((d2 1).y : Rat)) = 3 := by
  simp only [triD1, d2]
  rw [← Rat.intCast_add, ← Rat.intCast_sub]
  have h : (1 + 1 - (-1) : Int) = 3 := by omega
  rw [h]
  rfl

theorem pgwInc_int_d1_d0 (f0 f1 f2 : Int) :
    (f1 - f0) + (f2 - f1) - (f2 - f0) = 0 := by
  omega

theorem pgwInc_rat_telescope (a b c : Rat) :
    (b - a) + (c - b) = c - a := by
  rw [Rat.sub_eq_add_neg, Rat.sub_eq_add_neg, Rat.sub_eq_add_neg]
  rw [Rat.add_assoc]
  rw [Rat.add_left_comm (-a) c]
  rw [← Rat.add_assoc]
  rw [Rat.add_comm b c]
  rw [Rat.add_assoc]
  rw [Rat.add_left_comm b (-a)]
  rw [Rat.add_neg_cancel, Rat.add_zero]

theorem pgwInc_d1_d0 (f0 f1 f2 : Rat) :
    triD1 (triD0 (f0, f1, f2)) = 0 := by
  simp only [triD1, triD0]
  rw [pgwInc_rat_telescope]
  exact Rat.sub_self

#print axioms pgwInc_swap_involutive
#print axioms pgwInc_face_swapped
#print axioms pgwInc_row
#print axioms pgwInc_face_is_row
#print axioms pgwInc_face_cyclic
#print axioms pgwInc_transported_cycle
#print axioms pgwInc_dot_matches_order
#print axioms pgwInc_swapped_coord_is_tri
#print axioms pgwInc_face_tri
#print axioms pgwInc_int_d1_d0
#print axioms pgwInc_rat_telescope
#print axioms pgwInc_d1_d0
