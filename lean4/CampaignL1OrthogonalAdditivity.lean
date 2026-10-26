-- Campaign: L1-IMP-ORTHOGONAL-ADDITIVITY. Not a default target.
-- One 2 by 2 integer Gram matrix. Arbitrary orthogonal frames stay outside.

namespace CampaignL1OrthogonalAdditivity

def qf (g00 g01 g10 g11 a b : Int) : Int :=
  g00 * a * a + g01 * a * b + g10 * b * a + g11 * b * b

theorem pairSum : ((1 : Int) + (-1)) = 0 := by
  decide

theorem entriesNotZero : (1 : Int) ≠ 0 ∧ ((-1 : Int) ≠ 0) := by
  decide

theorem negCross (a b : Int) : (-1 : Int) * b * a = -(a * b) := by
  calc
    (-1 : Int) * b * a = (-1) * (b * a) := by rw [Int.mul_assoc]
    _ = (-1) * (a * b) := by rw [Int.mul_comm b a]
    _ = -(a * b) := by rw [Int.neg_one_mul]

theorem readout (a b : Int) : qf 1 1 (-1) 1 a b = a * a + b * b := by
  unfold qf
  repeat rw [Int.one_mul]
  rw [negCross a b]
  rw [Int.add_assoc (a * a) (a * b) (-(a * b))]
  rw [Int.add_right_neg (a * b)]
  rw [Int.add_zero (a * a)]

theorem axisSum (a b : Int) :
    qf 1 1 (-1) 1 a 0 + qf 1 1 (-1) 1 0 b = qf 1 1 (-1) 1 a b := by
  rw [readout a 0, readout 0 b, readout a b]
  rw [Int.zero_mul 0]
  rw [Int.add_zero (a * a), Int.zero_add (b * b)]

#print axioms pairSum
#print axioms entriesNotZero
#print axioms readout
#print axioms axisSum

end CampaignL1OrthogonalAdditivity
