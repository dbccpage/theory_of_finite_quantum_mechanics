-- Campaign: DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY. Not a default target.
-- Integer slice of the PromptBoundaries anchors: pair sum, one (3, 4) split
-- between linear, quadratic and quartic products, and the rotation identity.
-- Gleason uniqueness and L^p measure pairings stay outside this module.

namespace CampaignDsQm204BornUniqueness

theorem sqPair (x y : Int) : (x * y) * (x * y) = (x * x) * (y * y) := by
  rw [Int.mul_assoc x y (x * y)]
  rw [← Int.mul_assoc y x y]
  rw [Int.mul_comm y x]
  rw [Int.mul_assoc x y y]
  rw [← Int.mul_assoc x x (y * y)]

theorem cross (r a s b : Int) : (r * a) * (s * b) = (r * s) * (a * b) := by
  rw [Int.mul_assoc r a (s * b)]
  rw [← Int.mul_assoc a s b]
  rw [Int.mul_comm a s]
  rw [Int.mul_assoc s a b]
  rw [← Int.mul_assoc r s (a * b)]

theorem addSq (x y : Int) : (x + y) * (x + y) = x * x + x * y + y * x + y * y := by
  calc
    (x + y) * (x + y) = x * (x + y) + y * (x + y) := by rw [Int.add_mul]
    _ = (x * x + x * y) + (y * x + y * y) := by rw [Int.mul_add, Int.mul_add]
    _ = x * x + x * y + y * x + y * y := by
      rw [← Int.add_assoc (x * x + x * y) (y * x) (y * y)]

theorem subSq (x y : Int) : (x - y) * (x - y) = x * x - x * y - y * x + y * y := by
  calc
    (x - y) * (x - y) = x * (x - y) - y * (x - y) := by rw [Int.sub_mul]
    _ = (x * x - x * y) - (y * x - y * y) := by rw [Int.mul_sub, Int.mul_sub]
    _ = x * x - x * y - y * x + y * y := by omega

theorem expandRight (r s a b : Int) :
    (r * r + s * s) * (a * a + b * b)
      = (r * r) * (a * a) + (r * r) * (b * b) + (s * s) * (a * a) + (s * s) * (b * b) := by
  rw [Int.add_mul (r * r) (s * s) (a * a + b * b)]
  rw [Int.mul_add (r * r) (a * a) (b * b), Int.mul_add (s * s) (a * a) (b * b)]
  rw [← Int.add_assoc ((r * r) * (a * a) + (r * r) * (b * b)) ((s * s) * (a * a)) ((s * s) * (b * b))]

theorem rot (a b r s : Int) :
    (r * a - s * b) * (r * a - s * b) + (s * a + r * b) * (s * a + r * b)
      = (r * r + s * s) * (a * a + b * b) := by
  rw [subSq (r * a) (s * b), addSq (s * a) (r * b)]
  rw [sqPair r a, sqPair s b, sqPair s a, sqPair r b]
  rw [cross r a s b, cross s b r a, cross s a r b, cross r b s a]
  rw [Int.mul_comm s r]
  rw [Int.mul_comm b a]
  rw [expandRight r s a b]
  omega

theorem pairNorm (A B : Int) : A + B = (A + B) * 1 := by
  rw [Int.mul_one]

theorem denom34 : (3 : Int) + 4 = 7 ∧ (7 : Int) ≠ 0 := by decide

theorem squares34 : (3 : Int) * 3 + 4 * 4 = 25 ∧ (5 : Int) * 5 = 25 := by decide

theorem fourths34 : (3 : Int) * 3 * 3 * 3 + 4 * 4 * 4 * 4 = 337 := by decide

theorem quarticSeparates :
    (3 : Int) * 3 * (3 * 3 * 3 * 3 + 4 * 4 * 4 * 4) ≠ 3 * 3 * 3 * 3 * (5 * 5) := by decide

theorem linearSeparates : (3 : Int) * (3 * 3 + 4 * 4) ≠ 3 * 3 * (3 + 4) := by decide

theorem rotWitness :
    ((3 : Int) * 3 - 4 * 4) * (3 * 3 - 4 * 4) + (4 * 3 + 3 * 4) * (4 * 3 + 3 * 4) = 625 ∧
      (3 * 3 + 4 * 4) * (3 * 3 + 4 * 4) = 625 := by decide

#print axioms sqPair
#print axioms cross
#print axioms addSq
#print axioms subSq
#print axioms expandRight
#print axioms rot
#print axioms pairNorm
#print axioms denom34
#print axioms squares34
#print axioms fourths34
#print axioms quarticSeparates
#print axioms linearSeparates
#print axioms rotWitness

end CampaignDsQm204BornUniqueness
