/-
Narrowed boundary for PGW-WDP-BRIDGE-ONGOING-TO-WINDOW.
Carrier {0, 1}. Slots are the loop at 0, the loop at 1, the arc 0→1, and the arc 1→0.
The mark (0, 1, 0) is unbalanced. Its diagnostic is e01 + e10 + e00.
This module does not derive the degree-1 window from Genesis admission.
-/

/-- Coboundary on slots `(e00, e11, e01, e10)`. -/
def cob (g0 g1 : Int) : Int × Int × Int × Int :=
  (0, 0, g0 - g1, g1 - g0)

/-- Diagnostic of the unbalanced mark `(0, 1, 0)`. The loop at 1 is not read. -/
def diag (e00 e01 e10 : Int) : Int :=
  e01 + e10 + e00

theorem cob_slots (g0 g1 : Int) :
    (cob g0 g1).1 = 0 ∧
      (cob g0 g1).2.1 = 0 ∧
        (cob g0 g1).2.2.1 = g0 - g1 ∧
          (cob g0 g1).2.2.2 = g1 - g0 := by
  unfold cob
  repeat (first | constructor | rfl)

theorem diag_on_coboundary (g0 g1 : Int) :
    diag 0 (g0 - g1) (g1 - g0) = 0 := by
  unfold diag
  omega

theorem diag_after_repair (e00 e01 e10 g0 g1 : Int) :
    diag (e00 + 0) (e01 + (g0 - g1)) (e10 + (g1 - g0)) = diag e00 e01 e10 := by
  unfold diag
  omega

theorem denominator_clears
    (b d00 d11 d01 d10 n0 n1 : Int)
    (hb : b ≠ 0)
    (h00 : b * d00 = 0)
    (h11 : b * d11 = 0)
    (h01 : b * d01 = n0 - n1)
    (h10 : b * d10 = n1 - n0) :
    (d00, d11, d01, d10) = cob 0 (-d01) := by
  have hz00 : d00 = 0 :=
    (Int.mul_eq_zero.mp h00).resolve_left hb
  have hz11 : d11 = 0 :=
    (Int.mul_eq_zero.mp h11).resolve_left hb
  have hscaled : b * d10 = b * (-d01) := by
    calc
      b * d10 = n1 - n0 := h10
      _ = -(n0 - n1) := by omega
      _ = -(b * d01) := by rw [← h01]
      _ = b * (-d01) := Int.neg_mul_eq_mul_neg b d01
  have hrev : d10 = -d01 :=
    Int.eq_of_mul_eq_mul_left hb hscaled
  unfold cob
  rw [hz00, hz11, hrev]
  show (0, 0, d01, -d01) = (0, 0, 0 - (-d01), (-d01) - 0)
  have hfwd : 0 - (-d01) = d01 := by omega
  have hback : (-d01) - 0 = -d01 := by omega
  rw [hfwd, hback]

theorem compensated_loop_closed : diag 1 0 (-1) = 0 := by
  decide

theorem compensated_loop_not_coboundary (g0 g1 : Int) :
    (cob g0 g1).1 ≠ 1 := by
  unfold cob
  omega

theorem silent_loop_closed : diag 0 0 0 = 0 := by
  decide

theorem silent_loop_not_coboundary (g0 g1 : Int) :
    (cob g0 g1).2.1 ≠ 1 := by
  have hzero : (cob g0 g1).2.1 = 0 := (cob_slots g0 g1).2.1
  omega

theorem one_arc_diagnostic : diag 0 1 0 = 1 := by
  decide

theorem two_way_sum : (1 : Int) + 1 = 2 := by
  decide

theorem two_way_difference : (1 : Int) - 1 = 0 := by
  decide

#print axioms cob_slots
#print axioms diag_on_coboundary
#print axioms diag_after_repair
#print axioms denominator_clears
#print axioms compensated_loop_closed
#print axioms compensated_loop_not_coboundary
#print axioms silent_loop_closed
#print axioms silent_loop_not_coboundary
#print axioms one_arc_diagnostic
#print axioms two_way_sum
#print axioms two_way_difference
