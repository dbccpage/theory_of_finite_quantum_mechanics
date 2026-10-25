/-
Narrowed boundary for PGW-WDP-HANDOFF-TO-L1.
Vertices 0, 1, 2 with values (0, 1, 0).
Slot order is (01, 12, 02). The coboundary is (1, -1, 0).
This module does not certify a weighted quotient or an LGGR adapter.
-/

namespace CampaignPgwWdpHandoffToL1

/-- Coboundary of vertex values (0, 1, 0) in slot order (01, 12, 02). -/
theorem pgwHo_coboundary :
    ((1 : Int) - (0 : Int), (0 : Int) - (1 : Int), (0 : Int) - (0 : Int))
      = ((1 : Int), (-1 : Int), (0 : Int)) := by
  rfl

/-- Leakage L1 of that coboundary is 2. -/
theorem pgwHo_leakage :
    (1 : Int).natAbs + ((-1 : Int).natAbs) + (0 : Int).natAbs = 2 := by
  rfl

/-- Subtracting the same coboundary leaves residual (0, 0, 0). -/
theorem pgwHo_repair :
    (((1 : Int) - ((1 : Int) - (0 : Int))) = (0 : Int)) ∧
      (((-1 : Int) - ((0 : Int) - (1 : Int))) = (0 : Int)) ∧
        (((0 : Int) - ((0 : Int) - (0 : Int))) = (0 : Int)) := by
  constructor
  · rfl
  constructor
  · rfl
  · rfl

/-- Residual L1 is 0. -/
theorem pgwHo_residual_l1 : (0 : Nat) + 0 + 0 = 0 := by
  rfl

/-- Zero is a lower bound for every natural repair cost. -/
theorem pgwHo_zero_le (n : Nat) : 0 ≤ n := Nat.zero_le n

/-- The leakage number 2 is not the residual cost 0. -/
theorem pgwHo_leakage_not_min : (2 : Nat) ≠ 0 := by
  intro h
  cases h

/-- Oriented sum of the coboundary slots is 0. -/
theorem pgwHo_oriented : (1 : Int) + (-1 : Int) - (0 : Int) = (0 : Int) := by
  rfl

end CampaignPgwWdpHandoffToL1

#print axioms CampaignPgwWdpHandoffToL1.pgwHo_coboundary
#print axioms CampaignPgwWdpHandoffToL1.pgwHo_leakage
#print axioms CampaignPgwWdpHandoffToL1.pgwHo_repair
#print axioms CampaignPgwWdpHandoffToL1.pgwHo_residual_l1
#print axioms CampaignPgwWdpHandoffToL1.pgwHo_zero_le
#print axioms CampaignPgwWdpHandoffToL1.pgwHo_leakage_not_min
#print axioms CampaignPgwWdpHandoffToL1.pgwHo_oriented
