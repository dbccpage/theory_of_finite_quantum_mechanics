/-
Narrowed boundary for PGW-WDP-HANDOFF-TO-L1.
One triangle, edges (01, 12, 02), unit weights.
The quotient value is the absolute face evaluation.
The coboundary norm of vertex values (0, 1, 0) is not that quotient value.
This module does not derive the L1 stage.
-/

def iabs (n : Int) : Int :=
  if n < 0 then -n else n

theorem iabs_neg (n : Int) : iabs (-n) = iabs n := by
  unfold iabs
  split
  · next h =>
    split
    · next h2 => omega
    · next h2 => omega
  · next h =>
    split
    · next h2 => omega
    · next h2 => omega

theorem iabs_nonneg (n : Int) : 0 ≤ iabs n := by
  unfold iabs
  split
  · next h => omega
  · next h => omega

theorem iabs_zero (n : Int) : iabs n = 0 ↔ n = 0 := by
  unfold iabs
  constructor
  · intro h
    split at h
    · next hn => omega
    · next hn => omega
  · intro h
    subst h
    split
    · next hn => omega
    · next hn => rfl

theorem iabs_add (a b : Int) : iabs (a + b) ≤ iabs a + iabs b := by
  unfold iabs
  split
  · next h =>
    split
    · next ha =>
      split
      · next hb => omega
      · next hb => omega
    · next ha =>
      split
      · next hb => omega
      · next hb => omega
  · next h =>
    split
    · next ha =>
      split
      · next hb => omega
      · next hb => omega
    · next ha =>
      split
      · next hb => omega
      · next hb => omega

theorem iabs_three (a b c : Int) : iabs (a + b + c) ≤ iabs a + iabs b + iabs c := by
  have h1 : iabs (a + b) ≤ iabs a + iabs b := iabs_add a b
  have h2 : iabs (a + b + c) ≤ iabs (a + b) + iabs c := iabs_add (a + b) c
  omega

def d0 (f0 f1 f2 : Int) : Int × Int × Int :=
  (f1 - f0, f2 - f1, f2 - f0)

theorem d0_components (f0 f1 f2 : Int) :
    (d0 f0 f1 f2).1 = f1 - f0 ∧
      (d0 f0 f1 f2).2.1 = f2 - f1 ∧
        (d0 f0 f1 f2).2.2 = f2 - f0 := by
  unfold d0
  repeat (first | constructor | rfl)

def face (x01 x12 x02 : Int) : Int :=
  x01 + x12 - x02

def l1 (x01 x12 x02 : Int) : Int :=
  iabs x01 + iabs x12 + iabs x02

def leakage (f0 f1 f2 : Int) : Int :=
  l1 (f1 - f0) (f2 - f1) (f2 - f0)

/-- Repair used as the matching certificate. Negative face value sits on edge 02. -/
def repair (h01 h12 h02 : Int) : Int × Int × Int :=
  if face h01 h12 h02 < 0 then (0, h01, h01 + h12)
  else (0, h01 - face h01 h12 h02, h02)

def verdict (phi gamma : Int) : Int :=
  if phi > 0 then 0 else if gamma > 0 then 0 else 1

theorem face_of_coboundary (f0 f1 f2 : Int) :
    face (f1 - f0) (f2 - f1) (f2 - f0) = 0 := by
  unfold face
  omega

theorem l1_ge_face (a b c : Int) : iabs (face a b c) ≤ l1 a b c := by
  have hineq : iabs (a + b + (-c)) ≤ iabs a + iabs b + iabs (-c) :=
    iabs_three a b (-c)
  rw [iabs_neg c] at hineq
  have hface : face a b c = a + b + (-c) := by
    unfold face
    omega
  unfold l1
  rw [hface]
  exact hineq

theorem distance_at_least (h01 h12 h02 f0 f1 f2 : Int) :
    iabs (face h01 h12 h02) ≤
      l1 (h01 - (f1 - f0)) (h12 - (f2 - f1)) (h02 - (f2 - f0)) := by
  have hface : face (h01 - (f1 - f0)) (h12 - (f2 - f1)) (h02 - (f2 - f0))
      = face h01 h12 h02 := by
    unfold face
    omega
  have hineq :=
    l1_ge_face (h01 - (f1 - f0)) (h12 - (f2 - f1)) (h02 - (f2 - f0))
  rw [hface] at hineq
  exact hineq

theorem repair_residual_neg (h01 h12 h02 : Int) :
    h01 - (d0 0 h01 (h01 + h12)).1 = 0 ∧
      h12 - (d0 0 h01 (h01 + h12)).2.1 = 0 ∧
        h02 - (d0 0 h01 (h01 + h12)).2.2 = -(face h01 h12 h02) := by
  have hc := d0_components 0 h01 (h01 + h12)
  rw [hc.1, hc.2.1, hc.2.2]
  unfold face
  omega

theorem repair_residual_nonneg (h01 h12 h02 : Int) :
    h01 - (d0 0 (h01 - face h01 h12 h02) h02).1 = face h01 h12 h02 ∧
      h12 - (d0 0 (h01 - face h01 h12 h02) h02).2.1 = 0 ∧
        h02 - (d0 0 (h01 - face h01 h12 h02) h02).2.2 = 0 := by
  have hc := d0_components 0 (h01 - face h01 h12 h02) h02
  rw [hc.1, hc.2.1, hc.2.2]
  unfold face
  omega

theorem meet_neg (h01 h12 h02 : Int) (_hs : face h01 h12 h02 < 0) :
    l1 0 0 (-(face h01 h12 h02)) = iabs (face h01 h12 h02) := by
  unfold l1
  rw [iabs_neg]
  have z : iabs 0 = 0 := by
    unfold iabs
    decide
  rw [z]
  omega

theorem meet_nonneg (h01 h12 h02 : Int) (hs : ¬ face h01 h12 h02 < 0) :
    l1 (face h01 h12 h02) 0 0 = iabs (face h01 h12 h02) := by
  unfold l1
  have z : iabs 0 = 0 := by
    unfold iabs
    decide
  have hn : iabs (face h01 h12 h02) = face h01 h12 h02 := by
    unfold iabs
    split
    · next h => exact absurd h hs
    · next h => rfl
  rw [z, hn]
  omega

theorem leakage_of_repair_vertex : leakage 0 1 0 = 2 := by
  unfold leakage l1 iabs
  decide

theorem coboundary_of_repair_vertex : d0 0 1 0 = (1, -1, 0) := by
  unfold d0
  decide

theorem quotient_of_that_coboundary : l1 (1 - 1) (-1 - -1) (0 - 0) = 0 := by
  unfold l1 iabs
  decide

theorem leakage_is_not_quotient : leakage 0 1 0 ≠ l1 (1 - 1) (-1 - -1) (0 - 0) := by
  unfold leakage l1 iabs
  decide

theorem face_of_obstruction : face 1 0 0 = 1 := by
  decide

theorem obstructed_verdict : verdict 1 1 = 0 := by
  unfold verdict
  decide

theorem closed_verdict : verdict 0 0 = 1 := by
  unfold verdict
  decide

theorem face_zero_is_coboundary (h01 h12 h02 : Int) (hz : face h01 h12 h02 = 0) :
    h01 = (d0 0 (h01 - face h01 h12 h02) h02).1 ∧
      h12 = (d0 0 (h01 - face h01 h12 h02) h02).2.1 ∧
        h02 = (d0 0 (h01 - face h01 h12 h02) h02).2.2 := by
  have hr := repair_residual_nonneg h01 h12 h02
  have hc := d0_components 0 (h01 - face h01 h12 h02) h02
  rw [hc.1, hc.2.1, hc.2.2]
  unfold face at *
  omega

def fibreConstant (a0 a1 : Int) : Prop :=
  a0 = a1

theorem equal_report_passes : fibreConstant 1 1 := by
  unfold fibreConstant
  rfl

theorem unequal_report_fails : ¬ fibreConstant 0 1 := by
  unfold fibreConstant
  decide

theorem repair_picks_neg (h01 h12 h02 : Int) (hs : face h01 h12 h02 < 0) :
    repair h01 h12 h02 = (0, h01, h01 + h12) := by
  unfold repair
  split
  · rfl
  · next h => exact absurd hs h

theorem repair_picks_nonneg (h01 h12 h02 : Int) (hs : ¬ face h01 h12 h02 < 0) :
    repair h01 h12 h02 = (0, h01 - face h01 h12 h02, h02) := by
  unfold repair
  split
  · next h => exact absurd h hs
  · rfl

#print axioms d0_components
#print axioms face_of_coboundary
#print axioms l1_ge_face
#print axioms distance_at_least
#print axioms repair_residual_neg
#print axioms repair_residual_nonneg
#print axioms meet_neg
#print axioms meet_nonneg
#print axioms leakage_of_repair_vertex
#print axioms coboundary_of_repair_vertex
#print axioms quotient_of_that_coboundary
#print axioms leakage_is_not_quotient
#print axioms face_of_obstruction
#print axioms obstructed_verdict
#print axioms closed_verdict
#print axioms face_zero_is_coboundary
#print axioms equal_report_passes
#print axioms unequal_report_fails
#print axioms repair_picks_neg
#print axioms repair_picks_nonneg
