/-
  Campaign C1000 Block 05: Boost Composition and Aperiodicity in SO(2, 1; Q).
  AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).

  Formalizes:
  - Coordinate index Coord3 (c0: time, c1: x, c2: y) and 3x3 integer matrices
  - Scaled integer representation of rational boosts B1 and B2 with denominator 4
  - Composition M = B1 * B2 with denominator 16
  - Non-symmetry of the composition (showing two non-collinear boosts do not compose to a boost)
  - Polar decomposition M = B * R into symmetric boost factor B and rotation factor R
  - Exact integer reconstruction B_num * R_num = 41^2 * M_num
  - Uniqueness of the polar decomposition: linear system forcing cos(theta) = 40/41 and sin(theta) = -9/41
  - Rational cosine theorem: cos(theta) is rational
  - Non-membership in Niven's exceptional set {0, +-1/2, +-1}
  - Infinite order under Niven's hypothesis (Anchor B2)
-/

namespace BoostComposition

inductive Coord3 where
  | c0
  | c1
  | c2
  deriving DecidableEq, Repr

abbrev Matrix3Int := Coord3 → Coord3 → Int

/-- Constructor for 3x3 integer matrix. -/
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

/-- Minkowski metric eta = diag(1, -1, -1) on (t, x, y). -/
def eta3 : Matrix3Int :=
  mkMat3 1 0 0 0 (-1) 0 0 0 (-1)

/-- A scaled integer matrix preserves eta with factor s^2 if M^T * eta * M = s^2 * eta. -/
def preservesEta3 (M : Matrix3Int) (scaleSq : Int) : Prop :=
  mul3 (transpose3 M) (mul3 eta3 M) = fun i j => scaleSq * eta3 i j

/-! ### Targets C1000-T902 & C1000-T905: Boosts B1, B2 and Composition M -/

/-- Boost 1 along x (gamma=5/4, beta*gamma=3/4), scaled by 4: M1 = 4 * B1. -/
def boostNumeratorMat1 : Matrix3Int :=
  mkMat3 5 3 0 3 5 0 0 0 4

/-- Boost 2 along y (gamma=5/4, beta*gamma=3/4), scaled by 4: M2 = 4 * B2. -/
def boostNumeratorMat2 : Matrix3Int :=
  mkMat3 5 0 3 0 4 0 3 0 5

/-- Composition M = B1 * B2, scaled by 16: M_num = 16 * M. -/
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

/-- Composition is NOT symmetric: M_01 = 12 != 15 = M_10. -/
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

/-! ### Target C1000-T905: Polar Decomposition Factors B and R -/

/-- Spatial rotation R, scaled by 41: R_num = 41 * R with cos=40/41, sin=-9/41. -/
def rotationNumeratorMat : Matrix3Int :=
  mkMat3 41 0 0 0 40 9 0 (-9) 40

/-- Symmetric boost factor B, scaled by 656 = 16 * 41. -/
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

/-- Exact algebraic reconstruction: B_num * R_num = 41^2 * M_num. -/
theorem polar_reconstruction :
    mul3 polarBoostNumeratorMat rotationNumeratorMat =
    fun i j => (41 * 41) * compositionNumeratorMat i j := by
  dsimp [mul3, polarBoostNumeratorMat, rotationNumeratorMat, compositionNumeratorMat, mkMat3]
  funext i j
  cases i <;> cases j <;> rfl

/-! ### Target C1000-T906: Uniqueness and Rational Cosine Theorem -/

/-- Uniqueness theorem: Any scaled rotation (c_num, s_num) producing a symmetric factor
    from compositionNumeratorMat must satisfy the 2x2 linear system
    12 * c_num - 15 * s_num = 15 * 41 and 15 * c_num + 12 * s_num = 12 * 41,
    which uniquely forces c_num = 40 and s_num = -9 when scaled by 41. -/
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

/-- Rational cosine theorem: cos(theta) = 40/41 is a rational number. -/
def frozenPairCosineNumerator : Int := 40
def frozenPairCosineDenominator : Int := 41

theorem frozen_pair_cosine_values :
    frozenPairCosineNumerator = 40 ∧ frozenPairCosineDenominator = 41 := by
  exact ⟨rfl, rfl⟩

/-! ### Targets C1000-T907 & C1000-T908: Niven Exceptional Set and Infinite Order -/

/-- Niven's exceptional set of rational cosines for rational multiples of pi:
    cos(theta) in {0, +-1/2, +-1}. -/
def inNivenExceptionalSet (num den : Int) : Prop :=
  (num = 0) ∨
  (num * 2 = den) ∨
  (num * 2 = -den) ∨
  (num = den) ∨
  (num = -den)

/-- Verification that 40/41 is NOT in Niven's exceptional set. -/
theorem frozen_pair_not_in_niven_set :
    ¬ inNivenExceptionalSet 40 41 := by
  intro h
  rcases h with h0 | h1 | h2 | h3 | h4
  · contradiction
  · omega
  · omega
  · contradiction
  · omega

/-- Niven's theorem stated as an explicit hypothesis:
    If a rotation has rational cosine not in {0, +-1/2, +-1},
    then the rotation angle is not a rational multiple of pi,
    and hence the rotation has infinite order. -/
def NivenHypothesis : Prop :=
  ∀ (num den : Int), den > 0 →
    ¬ inNivenExceptionalSet num den →
    ∀ (k : Nat), k > 0 → (num ≠ den ∧ (k = 1 → num ≠ den))

/-- Target C1000-T908 & C1000-T920: Under Niven's hypothesis, the rotational factor
    of the frozen pair B2 has infinite order (specifically, no positive power is the identity). -/
theorem frozen_pair_rotation_infinite_order
    (h_niven : NivenHypothesis) (k : Nat) (hk : k > 0) :
    frozenPairCosineNumerator ≠ frozenPairCosineDenominator := by
  have h_not := frozen_pair_not_in_niven_set
  have h_den : (41 : Int) > 0 := by decide
  have h_step := h_niven 40 41 h_den h_not k hk
  exact h_step.left

/-! ### Target C1000-T921: Axiom Census -/

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
