/-
Narrowed boundary for PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT.
One triangle. Incidence order (01, 02, 12) reorders to (01, 12, 02).
The coboundary matches the transposed incidence boundary.
The face column (1, -1, 1) becomes (1, 1, -1).
Edge 20 is stored as the negation of edge 02.
This module does not derive the WDP window from Genesis admission.
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

theorem iabs_two : iabs 2 = 2 := by
  decide

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

/-- Incidence boundary on the edge order `(01, 02, 12)`. -/
def incBoundary (x01 x02 x12 : Int) : Int × Int × Int :=
  (-x01 - x02, x01 - x12, x02 + x12)

/-- Reorder `(01, 02, 12)` to `(01, 12, 02)`. -/
def reorderToWdp (a01 a02 a12 : Int) : Int × Int × Int :=
  (a01, a12, a02)

def dot3 (u v : Int × Int × Int) : Int :=
  u.1 * v.1 + u.2.1 * v.2.1 + u.2.2 * v.2.2

/-- WDP coboundary on the edge order `(01, 12, 02)`. -/
def wdpD0 (f0 f1 f2 : Int) : Int × Int × Int :=
  (f1 - f0, f2 - f1, f2 - f0)

/-- WDP face evaluation `x01 + x12 - x02`. -/
def wdpD1 (x01 x12 x02 : Int) : Int :=
  x01 + x12 - x02

theorem column_01 : incBoundary 1 0 0 = (-1, 1, 0) := by
  decide

theorem column_02 : incBoundary 0 1 0 = (-1, 0, 1) := by
  decide

theorem column_12 : incBoundary 0 0 1 = (0, -1, 1) := by
  decide

theorem transport_matches_transpose (f0 f1 f2 : Int) :
    (dot3 (incBoundary 1 0 0) (f0, f1, f2),
      dot3 (incBoundary 0 0 1) (f0, f1, f2),
      dot3 (incBoundary 0 1 0) (f0, f1, f2))
      = wdpD0 f0 f1 f2 := by
  have h01 : dot3 (incBoundary 1 0 0) (f0, f1, f2) = f1 - f0 := by
    rw [column_01]
    show (-1) * f0 + 1 * f1 + 0 * f2 = f1 - f0
    omega
  have h12 : dot3 (incBoundary 0 0 1) (f0, f1, f2) = f2 - f1 := by
    rw [column_12]
    show 0 * f0 + (-1) * f1 + 1 * f2 = f2 - f1
    omega
  have h02 : dot3 (incBoundary 0 1 0) (f0, f1, f2) = f2 - f0 := by
    rw [column_02]
    show (-1) * f0 + 0 * f1 + 1 * f2 = f2 - f0
    omega
  unfold wdpD0
  rw [h01, h12, h02]

theorem face_reorders :
    reorderToWdp 1 (-1) 1 = (1, 1, -1) := by
  decide

theorem incidence_face_boundary_zero :
    incBoundary 1 (-1) 1 = (0, 0, 0) := by
  decide

theorem wdp_d1_d0 (f0 f1 f2 : Int) :
    wdpD1 (f1 - f0) (f2 - f1) (f2 - f0) = 0 := by
  unfold wdpD1
  omega

theorem reverse_edge_20 (x01 x12 x02 : Int) :
    x01 + x12 + (-x02) = wdpD1 x01 x12 x02 := by
  unfold wdpD1
  omega

theorem defect_charge : wdpD1 1 1 0 = 2 := by
  decide

def residual (f0 f1 f2 : Int) : Int :=
  iabs (1 - (f1 - f0)) + iabs (1 - (f2 - f1)) + iabs (0 - (f2 - f0))

theorem pairing_is_two (f0 f1 f2 : Int) :
    (1 - (f1 - f0)) + (1 - (f2 - f1)) - (0 - (f2 - f0)) = 2 := by
  omega

theorem residual_at_repair : residual 0 1 0 = 2 := by
  unfold residual iabs
  decide

theorem residual_at_least_two (f0 f1 f2 : Int) : 2 ≤ residual f0 f1 f2 := by
  let a := 1 - (f1 - f0)
  let b := 1 - (f2 - f1)
  let c := 0 - (f2 - f0)
  have hpair : a + b + (-c) = 2 := by
    dsimp [a, b, c]
    omega
  have hineq : iabs (a + b + (-c)) ≤ iabs a + iabs b + iabs (-c) :=
    iabs_three a b (-c)
  rw [hpair, iabs_two, iabs_neg c] at hineq
  simpa [residual, a, b, c] using hineq

#print axioms column_01
#print axioms column_02
#print axioms column_12
#print axioms transport_matches_transpose
#print axioms face_reorders
#print axioms incidence_face_boundary_zero
#print axioms wdp_d1_d0
#print axioms reverse_edge_20
#print axioms defect_charge
#print axioms pairing_is_two
#print axioms residual_at_repair
#print axioms residual_at_least_two
