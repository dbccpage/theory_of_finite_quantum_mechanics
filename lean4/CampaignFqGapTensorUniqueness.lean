-- Campaign: FQ-GAP-TENSOR-UNIQUENESS. Not a default target.
-- Integer 2 by 2 outer products. Tensor selection stays outside.

namespace CampaignFqGapTensorUniqueness

def det (m00 m01 m10 m11 : Int) : Int :=
  m00 * m11 - m01 * m10

theorem productsEq (a0 a1 b0 b1 : Int) :
    (a0 * b0) * (a1 * b1) = (a0 * b1) * (a1 * b0) := by
  rw [Int.mul_assoc a0 b0 (a1 * b1)]
  rw [← Int.mul_assoc b0 a1 b1]
  rw [Int.mul_comm b0 a1]
  rw [Int.mul_assoc a1 b0 b1]
  rw [Int.mul_comm b0 b1]
  rw [← Int.mul_assoc a1 b1 b0]
  rw [← Int.mul_assoc a0 (a1 * b1) b0]
  rw [← Int.mul_assoc a0 a1 b1]
  rw [Int.mul_assoc (a0 * a1) b1 b0]
  rw [Int.mul_comm b1 b0]
  rw [← Int.mul_assoc (a0 * a1) b0 b1]
  rw [Int.mul_assoc a0 a1 b0]
  rw [Int.mul_assoc a0 (a1 * b0) b1]
  rw [Int.mul_comm (a1 * b0) b1]
  rw [← Int.mul_assoc a0 b1 (a1 * b0)]

theorem outerDet (a0 a1 b0 b1 : Int) :
    det (a0 * b0) (a0 * b1) (a1 * b0) (a1 * b1) = 0 := by
  unfold det
  rw [productsEq a0 a1 b0 b1]
  exact Int.sub_self ((a0 * b1) * (a1 * b0))

theorem identityDet : det 1 0 0 1 = 1 := by
  unfold det
  rw [Int.mul_one 1, Int.zero_mul 0, Int.sub_zero 1]

theorem identityNotOuter (a0 a1 b0 b1 : Int) :
    ¬ (a0 * b0 = 1 ∧ a0 * b1 = 0 ∧ a1 * b0 = 0 ∧ a1 * b1 = 1) := by
  intro h
  have hdet := outerDet a0 a1 b0 b1
  rw [h.1, h.2.1, h.2.2.1, h.2.2.2] at hdet
  rw [identityDet] at hdet
  exact absurd hdet (by decide)

#print axioms productsEq
#print axioms outerDet
#print axioms identityDet
#print axioms identityNotOuter

end CampaignFqGapTensorUniqueness