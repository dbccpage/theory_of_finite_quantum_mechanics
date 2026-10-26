-- Campaign: L1-WDP-CH08-C01-REPLICA-L1. Not a default target.
-- Nat scaling of a coordinate sum and of a sum of squares.
-- A derivation that l1 appears from replica extensivity, and any reading
-- that l2 is excluded, stay outside this module.
-- AuthorityEffect: None.

namespace CampaignL1ReplicaScale

theorem scaleSum (c a b : Nat) : c * a + c * b = c * (a + b) :=
  (Nat.mul_add c a b).symm

private theorem scaleOne (c a : Nat) : (c * a) * (c * a) = (c * c) * (a * a) := by
  calc
    (c * a) * (c * a) = c * (a * (c * a)) := Nat.mul_assoc c a (c * a)
    _ = c * (c * (a * a)) := by rw [Nat.mul_left_comm a c a]
    _ = (c * c) * (a * a) := by rw [Nat.mul_assoc]

theorem scaleSquares (c a b : Nat) :
    (c * a) * (c * a) + (c * b) * (c * b) = (c * c) * (a * a + b * b) := by
  rw [scaleOne c a, scaleOne c b, ← Nat.mul_add]

theorem sampleSum : (3 + 4 : Nat) = 7 := by
  decide

theorem sampleSquares : (3 * 3 + 4 * 4 : Nat) = 25 := by
  decide

theorem sampleFive : (5 * 5 : Nat) = 25 := by
  decide

theorem sampleSumSquare : ((3 + 4) * (3 + 4) : Nat) = 49 := by
  decide

theorem sampleSquaresNeSumSquare : (25 : Nat) ≠ 49 := by
  decide

theorem sampleScaledSum : (2 * (3 + 4) : Nat) = 14 := by
  decide

theorem sampleScaledSquares : ((2 * 3) * (2 * 3) + (2 * 4) * (2 * 4) : Nat) = 100 := by
  decide

theorem sampleLinearScale : (2 * (3 * 3 + 4 * 4) : Nat) = 50 := by
  decide

theorem sampleScaledNeLinear : (100 : Nat) ≠ 50 := by
  decide

#print axioms scaleSum
#print axioms scaleSquares
#print axioms sampleSum
#print axioms sampleSquares
#print axioms sampleFive
#print axioms sampleSumSquare
#print axioms sampleSquaresNeSumSquare
#print axioms sampleScaledSum
#print axioms sampleScaledSquares
#print axioms sampleLinearScale
#print axioms sampleScaledNeLinear

end CampaignL1ReplicaScale
