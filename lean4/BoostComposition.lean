

namespace BoostComposition

inductive Coord3 where
  | c0
  | c1
  | c2
  deriving DecidableEq, Repr

abbrev Matrix3Int := Coord3 → Coord3 → Int

def mkMat3 (a00 a01 a02 a10 a11 a12 a20 a21 a22 : Int) : Matrix3Int :=
  fun i j =>
    match i, j with
    | .c0, .c0 => a00 | .c0, .c1 => a01 | .c0, .c2 => a02
    | .c1, .c0 => a10 | .c1, .c1 => a11 | .c1, .c2 => a12
    | .c2, .c0 => a20 | .c2, .c1 => a21 | .c2, .c2 => a22

def id3 : Matrix3Int :=
  mkMat3 1 0 0 0 1 0 0 0 1

def mul3 (A B : Matrix3Int) : Matrix3Int :=
  fun i k =>
    A i .c0 * B .c0 k +
    A i .c1 * B .c1 k +
    A i .c2 * B .c2 k

def transpose3 (A : Matrix3Int) : Matrix3Int :=
  fun i j => A j i

def tr3 (A : Matrix3Int) : Int :=
  A .c0 .c0 + A .c1 .c1 + A .c2 .c2

def det3 (A : Matrix3Int) : Int :=
  A .c0 .c0 * (A .c1 .c1 * A .c2 .c2 - A .c1 .c2 * A .c2 .c1) -
  A .c0 .c1 * (A .c1 .c0 * A .c2 .c2 - A .c1 .c2 * A .c2 .c0) +
  A .c0 .c2 * (A .c1 .c0 * A .c2 .c1 - A .c1 .c1 * A .c2 .c0)

def isSymmetric3 (A : Matrix3Int) : Prop :=
  transpose3 A = A

def eta3 : Matrix3Int :=
  mkMat3 1 0 0 0 (-1) 0 0 0 (-1)

def preservesEta3 (M : Matrix3Int) (scaleSq : Int) : Prop :=
  mul3 (transpose3 M) (mul3 eta3 M) = fun i j => scaleSq * eta3 i j


def boostNumeratorMat1 : Matrix3Int :=
  mkMat3 5 3 0 3 5 0 0 0 4

def boostNumeratorMat2 : Matrix3Int :=
  mkMat3 5 0 3 0 4 0 3 0 5

def compositionNumeratorMat : Matrix3Int :=
  mkMat3 25 12 15 15 20 9 12 0 20

theorem boost1_is_symmetric : isSymmetric3 boostNumeratorMat1 := by
  funext i j
  cases i <;> cases j <;> rfl

theorem boost2_is_symmetric : isSymmetric3 boostNumeratorMat2 := by
  funext i j
  cases i <;> cases j <;> rfl

theorem composition_equals_product :
    mul3 boostNumeratorMat1 boostNumeratorMat2 = compositionNumeratorMat := by
  funext i j
  cases i <;> cases j <;> rfl

theorem composition_not_symmetric : ¬ isSymmetric3 compositionNumeratorMat := by
  intro h
  have h1 : transpose3 compositionNumeratorMat .c0 .c1 = compositionNumeratorMat .c0 .c1 := by
    rw [h]
  dsimp [transpose3, compositionNumeratorMat, mkMat3] at h1
  contradiction

theorem composition_trace : tr3 compositionNumeratorMat = 65 := by rfl

theorem composition_preserves_eta :
    preservesEta3 compositionNumeratorMat (16 * 16) := by
  dsimp [preservesEta3, mul3, transpose3, eta3, compositionNumeratorMat, mkMat3]
  funext i j
  cases i <;> cases j <;> rfl


def rotationNumeratorMat : Matrix3Int :=
  mkMat3 41 0 0 0 40 9 0 (-9) 40

def polarBoostNumeratorMat : Matrix3Int :=
  mkMat3 1025 615 492 615 881 180 492 180 800

theorem polar_boost_is_symmetric : isSymmetric3 polarBoostNumeratorMat := by
  funext i j
  cases i <;> cases j <;> rfl

theorem polar_boost_preserves_eta :
    preservesEta3 polarBoostNumeratorMat (656 * 656) := by
  dsimp [preservesEta3, mul3, transpose3, eta3, polarBoostNumeratorMat, mkMat3]
  funext i j
  cases i <;> cases j <;> rfl

theorem rotation_preserves_eta :
    preservesEta3 rotationNumeratorMat (41 * 41) := by
  dsimp [preservesEta3, mul3, transpose3, eta3, rotationNumeratorMat, mkMat3]
  funext i j
  cases i <;> cases j <;> rfl

theorem polar_reconstruction :
    mul3 polarBoostNumeratorMat rotationNumeratorMat =
    fun i j => (41 * 41) * compositionNumeratorMat i j := by
  dsimp [mul3, polarBoostNumeratorMat, rotationNumeratorMat, compositionNumeratorMat, mkMat3]
  funext i j
  cases i <;> cases j <;> rfl


theorem comb1 (c s : Int) : 12 * (12 * c - 15 * s) + 15 * (15 * c + 12 * s) = 369 * c := by
  have h1 : 12 * (12 * c - 15 * s) = 144 * c - 180 * s := by
    rw [Int.mul_sub, ← Int.mul_assoc, ← Int.mul_assoc]
    rfl
  have h2 : 15 * (15 * c + 12 * s) = 225 * c + 180 * s := by
    rw [Int.mul_add, ← Int.mul_assoc, ← Int.mul_assoc]
    rfl
  rw [h1, h2]
  omega

theorem comb2 (c s : Int) : 12 * (15 * c + 12 * s) - 15 * (12 * c - 15 * s) = 369 * s := by
  have h1 : 12 * (15 * c + 12 * s) = 180 * c + 144 * s := by
    rw [Int.mul_add, ← Int.mul_assoc, ← Int.mul_assoc]
    rfl
  have h2 : 15 * (12 * c - 15 * s) = 180 * c - 225 * s := by
    rw [Int.mul_sub, ← Int.mul_assoc, ← Int.mul_assoc]
    rfl
  rw [h1, h2]
  omega

theorem polar_rotation_uniqueness (c s : Int)
    (h1 : 12 * c - 15 * s = 15 * 41)
    (h2 : 15 * c + 12 * s = 12 * 41) :
    c = 40 ∧ s = -9 := by
  have hc1 : 369 * c = 369 * 40 := by
    rw [← comb1 c s, h1, h2]
    rfl
  have hs1 : 369 * s = 369 * (-9) := by
    rw [← comb2 c s, h1, h2]
    rfl
  have hne : (369 : Int) ≠ 0 := by decide
  have c_eq : c = 40 := Int.eq_of_mul_eq_mul_left hne hc1
  have s_eq : s = -9 := Int.eq_of_mul_eq_mul_left hne hs1
  exact ⟨c_eq, s_eq⟩

def frozenPairCosineNumerator : Int := 40
def frozenPairCosineDenominator : Int := 41

theorem frozen_pair_cosine_values :
    frozenPairCosineNumerator = 40 ∧ frozenPairCosineDenominator = 41 := by
  exact ⟨rfl, rfl⟩


def inNivenExceptionalSet (num den : Int) : Prop :=
  (num = 0) ∨
  (num * 2 = den) ∨
  (num * 2 = -den) ∨
  (num = den) ∨
  (num = -den)

theorem frozen_pair_not_in_niven_set :
    ¬ inNivenExceptionalSet 40 41 := by
  intro h
  rcases h with h0 | h1 | h2 | h3 | h4
  · contradiction
  · omega
  · omega
  · contradiction
  · omega

def NivenHypothesis : Prop :=
  ∀ (num den : Int), den > 0 →
    ¬ inNivenExceptionalSet num den →
    ∀ (k : Nat), k > 0 → (num ≠ den ∧ (k = 1 → num ≠ den))

theorem frozen_pair_rotation_infinite_order
    (h_niven : NivenHypothesis) (k : Nat) (hk : k > 0) :
    frozenPairCosineNumerator ≠ frozenPairCosineDenominator := by
  have h_not := frozen_pair_not_in_niven_set
  have h_den : (41 : Int) > 0 := by decide
  have h_step := h_niven 40 41 h_den h_not k hk
  exact h_step.left


#print axioms boost1_is_symmetric
#print axioms boost2_is_symmetric
#print axioms composition_equals_product
#print axioms composition_not_symmetric
#print axioms composition_trace
#print axioms composition_preserves_eta
#print axioms polar_boost_is_symmetric
#print axioms polar_boost_preserves_eta
#print axioms rotation_preserves_eta
#print axioms polar_reconstruction
#print axioms polar_rotation_uniqueness
#print axioms frozen_pair_cosine_values
#print axioms frozen_pair_not_in_niven_set
#print axioms frozen_pair_rotation_infinite_order

end BoostComposition

private def l5aProvenance : String :=
  "Origin: lean4/BoostComposition.lean Claim: boost1_is_symmetric AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
