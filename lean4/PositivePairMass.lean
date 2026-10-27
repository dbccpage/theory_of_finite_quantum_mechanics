-- TFQ-0171. Not a default target.
-- Positive natural masses on two coordinates are not a unit sum.
-- A general Boolean valuation and the Rust modules stay outside.

import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp

namespace PositivePairMass

theorem positivePairMassNotOne (a b : Nat) (ha : 1 ≤ a) (hb : 1 ≤ b) : a + b ≠ 1 := by
  intro h
  have hle : 1 + 1 ≤ a + b := Nat.add_le_add ha hb
  rw [h] at hle
  exact Nat.not_succ_le_self 1 hle

theorem oneOneMass : (1 : Nat) + 1 = 2 := by
  decide

theorem twoNotOne : (2 : Nat) ≠ 1 := by
  decide

theorem emptyMassNotOne : (0 : Nat) ≠ 1 := by
  decide

theorem halfPairSumsToOne : ((1 : Rat) / 2) + ((1 : Rat) / 2) = 1 := by
  norm_num

theorem oneOneNotUnit : ((1 : Rat) + 1) ≠ 1 := by
  norm_num

theorem unnormalizedPairDiffers :
    ((1 : Rat), (1 : Rat)) ≠ ((1 : Rat) / 2, (1 : Rat) / 2) := by
  intro h
  have h1 : (1 : Rat) = (1 : Rat) / 2 := congrArg Prod.fst h
  norm_num at h1

theorem normalizeByTotal (a b : Nat) (h : 0 < a + b) :
    (a : Rat) / ((a + b : Nat) : Rat) + (b : Rat) / ((a + b : Nat) : Rat) = 1 := by
  have hne : ((a + b : Nat) : Rat) ≠ 0 := by
    exact_mod_cast Nat.ne_of_gt h
  field_simp [hne]
  norm_cast

#print axioms positivePairMassNotOne
#print axioms oneOneMass
#print axioms twoNotOne
#print axioms emptyMassNotOne
#print axioms halfPairSumsToOne
#print axioms oneOneNotUnit
#print axioms unnormalizedPairDiffers
#print axioms normalizeByTotal

end PositivePairMass
