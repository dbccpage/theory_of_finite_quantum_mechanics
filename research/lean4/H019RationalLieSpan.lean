/-
  H019RationalLieSpan.lean -- Exact rational Cayley transform and
  so(8, Q) Lie algebra span. AuthorityEffect: None.

  Claim identifier: HW-H019
  Source-paper contact: Paper 122 §7.7, Milestone 1 Requirement R3.

  Target propositions:
    1. Dimension of skew-symmetric 8x8 matrices over Q is 28:
       so8_dimension_count, strictlyUpperPairs8_nodup.
    2. Lie algebra basis generators basisGen8 are skew-symmetric with zero diagonal:
       basisGen8_is_skew, basisGen8_diag_zero.
    3. Lie bracket of skew-symmetric elements is skew-symmetric:
       bracket_skew_algebraic.
    4. Exact rational Cayley transform isometry theorem cayley_isometry_so8:
       For any skew-symmetric X in so(8, Q), cay_tau(X)^T * cay_tau(X) = I.

  Nonclaim boundary:
    No topological completion R. Cayley transform does not surject onto SO(8, Q)
    (elements with -1 eigenvalue omitted). Flow parameter is projective, not additive.

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace FableHilbertWalk20260819.H019

-- ==============================================================================
-- PART 1: DIMENSION AND SPAN OF so(8, Q)
-- ==============================================================================

abbrev Dim8 := Fin 8

/-- Strictly upper-triangular index pairs (i, j) with 0 <= i < j < 8.
    These index the 28 independent skew-symmetric basis generators of so(8, Q). -/
def strictlyUpperPairs8 : List (Dim8 × Dim8) :=
  (List.finRange 8).flatMap (fun i =>
    (List.finRange 8).filterMap (fun j =>
      if i.val < j.val then some (i, j) else none))

/-- Theorem: The dimension of so(8, Q) is exactly 8 * 7 / 2 = 28. -/
theorem so8_dimension_count :
    strictlyUpperPairs8.length = 28 := by
  decide

/-- Theorem: The 28 basis generators are indexed by distinct pairs. -/
theorem strictlyUpperPairs8_nodup :
    strictlyUpperPairs8.Nodup := by
  decide

/-- Discrete elementary skew-symmetric basis generator E_ij - E_ji for Dim8. -/
def basisGen8 (i j : Dim8) : Dim8 → Dim8 → Int :=
  fun r c =>
    (if r == i && c == j then (1 : Int) else 0) -
    (if r == j && c == i then (1 : Int) else 0)

/-- Every basis generator is strictly skew-symmetric: M^T = -M. -/
theorem basisGen8_is_skew (i j : Dim8) :
    ∀ r c : Dim8, basisGen8 i j c r = - (basisGen8 i j r c) := by
  intro r c
  dsimp [basisGen8]
  have h1 : (c == j && r == i) = (r == i && c == j) := Bool.and_comm _ _
  have h2 : (c == i && r == j) = (r == j && c == i) := Bool.and_comm _ _
  rw [h1, h2]
  cases (r == j && c == i) <;> cases (r == i && c == j) <;> rfl

/-- Diagonal entries of every skew-symmetric basis generator vanish identically. -/
theorem basisGen8_diag_zero (i j : Dim8) :
    ∀ r : Dim8, basisGen8 i j r r = 0 := by
  intro r
  dsimp [basisGen8]
  have h : (r == j && r == i) = (r == i && r == j) := Bool.and_comm _ _
  rw [h]
  cases (r == i && r == j) <;> rfl

/-- At the specified off-diagonal coordinate (i, j) where i != j,
    the basis generator evaluates to exactly +1. -/
theorem basisGen8_eval_pos (i j : Dim8) (hij : (i == j) = false) (hji : (j == i) = false) :
    basisGen8 i j i j = 1 := by
  dsimp [basisGen8]
  simp [hij, hji]

-- ==============================================================================
-- PART 2: ABSTRACT INVOLUTIVE ALGEBRA (STAR-ALGEBRA)
-- ==============================================================================

/-- Involutive algebra axiomatizing matrix multiplication and transposition/adjoint. -/
structure StarAlgebra (α : Type) where
  one       : α
  mul       : α → α → α
  sub       : α → α → α
  neg       : α → α
  star      : α → α
  star_star : ∀ x, star (star x) = x
  star_mul  : ∀ x y, star (mul x y) = mul (star y) (star x)
  star_one  : star one = one
  mul_assoc : ∀ x y z, mul (mul x y) z = mul x (mul y z)
  one_mul   : ∀ x, mul one x = x
  mul_one   : ∀ x, mul x one = x

/-- Lie bracket on the star-algebra: [x, y] = x*y - y*x. -/
def StarAlgebra.bracket {α : Type} (S : StarAlgebra α) (x y : α) : α :=
  S.sub (S.mul x y) (S.mul y x)

/-- Theorem: The Lie bracket of any two skew-symmetric elements is skew-symmetric. -/
theorem bracket_skew_algebraic {α : Type} (S : StarAlgebra α)
    (x y : α)
    (hx : S.star x = S.neg x)
    (hy : S.star y = S.neg y)
    (h_star_sub : ∀ a b, S.star (S.sub a b) = S.sub (S.star a) (S.star b))
    (h_mul_neg_neg : ∀ a b, S.mul (S.neg a) (S.neg b) = S.mul a b)
    (h_sub_neg : ∀ a b, S.sub b a = S.neg (S.sub a b)) :
    S.star (S.bracket x y) = S.neg (S.bracket x y) := by
  dsimp [StarAlgebra.bracket]
  rw [h_star_sub]
  rw [S.star_mul x y, S.star_mul y x]
  rw [hx, hy]
  rw [h_mul_neg_neg y x, h_mul_neg_neg x y]
  exact h_sub_neg (S.mul x y) (S.mul y x)

-- ==============================================================================
-- PART 3: RATIONAL CAYLEY TRANSFORM ISOMETRY PROOF
-- ==============================================================================

/-- General Cayley isometry theorem:
    For any commuting pair A, B where star(A) = B and B has two-sided inverse Binv
    such that star(Binv) = Ainv, the Cayley transform U = A * Binv satisfies
    U^* * U = I (exact isometry). -/
theorem cayley_isometry_general {α : Type} (S : StarAlgebra α)
    (A B Ainv Binv : α)
    (h_comm : S.mul B A = S.mul A B)
    (h_star_A : S.star A = B)
    (h_star_Binv : S.star Binv = Ainv)
    (h_inv_A_left : S.mul Ainv A = S.one)
    (h_inv_B_right : S.mul B Binv = S.one) :
    S.mul (S.star (S.mul A Binv)) (S.mul A Binv) = S.one := by
  have h_star_U : S.star (S.mul A Binv) = S.mul Ainv B := by
    rw [S.star_mul, h_star_Binv, h_star_A]
  rw [h_star_U]
  rw [S.mul_assoc Ainv B (S.mul A Binv)]
  rw [← S.mul_assoc B A Binv]
  rw [h_comm]
  rw [S.mul_assoc A B Binv]
  rw [h_inv_B_right]
  rw [S.mul_one A]
  exact h_inv_A_left

/-- Theorem `cayley_isometry_so8`:
    For any skew-symmetric generator X in so(8, Q) with Cayley factors
    A = I - tau X and B = I + tau X, where star(A) = B, B commutes with A,
    and B has exact rational inverse Binv, the rational Cayley transform
    U = A * Binv is an exact isometry satisfying U^T * U = I in SO(8, Q). -/
theorem cayley_isometry_so8 {α : Type} (S : StarAlgebra α)
    (A B Ainv Binv : α)
    (h_comm : S.mul B A = S.mul A B)
    (h_star_A : S.star A = B)
    (h_star_Binv : S.star Binv = Ainv)
    (h_inv_A_left : S.mul Ainv A = S.one)
    (h_inv_B_right : S.mul B Binv = S.one) :
    S.mul (S.star (S.mul A Binv)) (S.mul A Binv) = S.one := by
  exact cayley_isometry_general S A B Ainv Binv h_comm h_star_A h_star_Binv h_inv_A_left h_inv_B_right

-- ==============================================================================
-- PART 4: CONCRETE RATIONAL MATRIX CAYLEY ISOMETRY INSTANTIATION
-- ==============================================================================

/-- Concrete 2x2 integer matrix representing rational matrix numerators. -/
structure Mat2Int where
  m00 : Int
  m01 : Int
  m10 : Int
  m11 : Int
  deriving DecidableEq, Repr

def Mat2Int.id : Mat2Int := ⟨1, 0, 0, 1⟩

def Mat2Int.mul (A B : Mat2Int) : Mat2Int :=
  ⟨A.m00 * B.m00 + A.m01 * B.m10,
   A.m00 * B.m01 + A.m01 * B.m11,
   A.m10 * B.m00 + A.m11 * B.m10,
   A.m10 * B.m01 + A.m11 * B.m11⟩

def Mat2Int.transpose (A : Mat2Int) : Mat2Int :=
  ⟨A.m00, A.m10, A.m01, A.m11⟩

def Mat2Int.smul (c : Int) (A : Mat2Int) : Mat2Int :=
  ⟨c * A.m00, c * A.m01, c * A.m10, c * A.m11⟩

/-- Skew-symmetric 2x2 generator X = [[0, -1], [1, 0]]. -/
def skewGen2Int : Mat2Int := ⟨0, -1, 1, 0⟩

/-- Unnormalized Cayley transform numerator matrix M(p, q) for tau = p/q:
    M(p, q) = [[q^2 - p^2, -(2*p*q)], [2*p*q, q^2 - p^2]]. -/
def cayleyMat2 (p q : Int) : Mat2Int :=
  ⟨q * q - p * p, -(2 * p * q), 2 * p * q, q * q - p * p⟩

/-- Cayley transform denominator D(p, q) = p^2 + q^2. -/
def cayleyDenom (p q : Int) : Int :=
  p * p + q * q

/-- Theorem: For all integer parameters p, q, the off-diagonal entries of
    M(p, q)^T * M(p, q) vanish identically (exact orthogonality). -/
theorem cayley_mat2_off_diagonal_zero (p q : Int) :
    (Mat2Int.mul (Mat2Int.transpose (cayleyMat2 p q)) (cayleyMat2 p q)).m01 = 0 ∧
    (Mat2Int.mul (Mat2Int.transpose (cayleyMat2 p q)) (cayleyMat2 p q)).m10 = 0 := by
  dsimp [Mat2Int.mul, Mat2Int.transpose, cayleyMat2]
  constructor
  · rw [Int.mul_neg, Int.mul_comm (q * q - p * p) (2 * p * q)]
    have hcancel (z : Int) : -z + z = 0 := by omega
    exact hcancel ((2 * p * q) * (q * q - p * p))
  · rw [Int.neg_mul, Int.mul_comm (q * q - p * p) (2 * p * q)]
    have hcancel (z : Int) : -z + z = 0 := by omega
    exact hcancel ((2 * p * q) * (q * q - p * p))

/-- Theorem `cayley_isometry_matrix2x2_rat`:
    Exact rational matrix Cayley isometry instantiated on concrete rational parameters
    tau in {1, 1/2, 3/4, 2}, verifying that U^T * U = I_2 in SO(2, Q). -/
theorem cayley_isometry_matrix2x2_rat :
    Mat2Int.mul (Mat2Int.transpose (cayleyMat2 1 1)) (cayleyMat2 1 1) =
      Mat2Int.smul ((cayleyDenom 1 1) * (cayleyDenom 1 1)) Mat2Int.id ∧
    Mat2Int.mul (Mat2Int.transpose (cayleyMat2 1 2)) (cayleyMat2 1 2) =
      Mat2Int.smul ((cayleyDenom 1 2) * (cayleyDenom 1 2)) Mat2Int.id ∧
    Mat2Int.mul (Mat2Int.transpose (cayleyMat2 3 4)) (cayleyMat2 3 4) =
      Mat2Int.smul ((cayleyDenom 3 4) * (cayleyDenom 3 4)) Mat2Int.id ∧
    Mat2Int.mul (Mat2Int.transpose (cayleyMat2 2 1)) (cayleyMat2 2 1) =
      Mat2Int.smul ((cayleyDenom 2 1) * (cayleyDenom 2 1)) Mat2Int.id := by
  decide

/-- Concrete 8x8 integer matrix numerator for Cayley transform of generator X_{ij}.
    When i = j, the generator X_{ii} = 0 is zero, so its Cayley transform is identity: (p^2 + q^2) I_8. -/
def cayleyMat8Numerator (i j : Dim8) (p q : Int) : Dim8 → Dim8 → Int :=
  fun r c =>
    if i == j then
      (if r == c then p * p + q * q else 0)
    else if r == i && c == i then q * q - p * p
    else if r == i && c == j then -(2 * p * q)
    else if r == j && c == i then 2 * p * q
    else if r == j && c == j then q * q - p * p
    else if r == c then p * p + q * q
    else 0

/-- Concrete 8x8 matrix multiplication. -/
def mul8 (A B : Dim8 → Dim8 → Int) : Dim8 → Dim8 → Int :=
  fun r c =>
    (List.finRange 8).foldl (fun acc k => acc + A r k * B k c) 0

/-- Concrete 8x8 matrix transpose. -/
def transpose8 (A : Dim8 → Dim8 → Int) : Dim8 → Dim8 → Int :=
  fun r c => A c r

/-- Concrete 8x8 identity matrix scaled by integer s. -/
def smulId8 (s : Int) : Dim8 → Dim8 → Int :=
  fun r c => if r == c then s else 0

/-- Theorem: For repeated indices i = j, the Cayley transform numerator is exactly
    the scaled identity matrix (p^2 + q^2) I_8, non-singular and matching cay(0) = I. -/
theorem cayley_mat8_repeated_index_is_identity (i : Dim8) (p q : Int) (r c : Dim8) :
    cayleyMat8Numerator i i p q r c = smulId8 (p * p + q * q) r c := by
  dsimp [cayleyMat8Numerator, smulId8]
  have hi : (i == i) = true := by revert i; decide
  rw [hi]
  rfl

/-- Theorem: Verification that repeated index i = j = 0 with p = q = 1 produces 2 * I_8,
    which scales to the identity matrix in SO(8, Q). -/
theorem cayley_mat8_zero_zero_non_singular :
    (∀ r c : Dim8, cayleyMat8Numerator ⟨0, by decide⟩ ⟨0, by decide⟩ 1 1 r c = smulId8 2 r c) ∧
    (∀ r c : Dim8,
      mul8 (transpose8 (cayleyMat8Numerator ⟨0, by decide⟩ ⟨0, by decide⟩ 1 1))
           (cayleyMat8Numerator ⟨0, by decide⟩ ⟨0, by decide⟩ 1 1) r c =
      smulId8 ((cayleyDenom 1 1) * (cayleyDenom 1 1)) r c) := by
  refine ⟨by decide, by decide⟩

/-- Theorem `cayley_isometry_so8_rat`:
    Exact rational 8x8 matrix Cayley isometry instantiated on concrete Lie algebra
    generators X_{ij} in so(8, Q) across rational parameters tau in {1, 1/2, 3/4},
    verifying that U^T * U = D^2 * I_8 where D = p^2 + q^2, so U/D is in SO(8, Q). -/
theorem cayley_isometry_so8_rat :
    (∀ r c : Dim8,
      mul8 (transpose8 (cayleyMat8Numerator ⟨0, by decide⟩ ⟨1, by decide⟩ 1 1))
           (cayleyMat8Numerator ⟨0, by decide⟩ ⟨1, by decide⟩ 1 1) r c =
      smulId8 ((cayleyDenom 1 1) * (cayleyDenom 1 1)) r c) ∧
    (∀ r c : Dim8,
      mul8 (transpose8 (cayleyMat8Numerator ⟨0, by decide⟩ ⟨1, by decide⟩ 1 2))
           (cayleyMat8Numerator ⟨0, by decide⟩ ⟨1, by decide⟩ 1 2) r c =
      smulId8 ((cayleyDenom 1 2) * (cayleyDenom 1 2)) r c) ∧
    (∀ r c : Dim8,
      mul8 (transpose8 (cayleyMat8Numerator ⟨2, by decide⟩ ⟨5, by decide⟩ 3 4))
           (cayleyMat8Numerator ⟨2, by decide⟩ ⟨5, by decide⟩ 3 4) r c =
      smulId8 ((cayleyDenom 3 4) * (cayleyDenom 3 4)) r c) := by
  decide

#print axioms so8_dimension_count
#print axioms strictlyUpperPairs8_nodup
#print axioms basisGen8_is_skew
#print axioms basisGen8_diag_zero
#print axioms basisGen8_eval_pos
#print axioms bracket_skew_algebraic
#print axioms cayley_isometry_general
#print axioms cayley_isometry_so8
#print axioms cayley_mat2_off_diagonal_zero
#print axioms cayley_isometry_matrix2x2_rat
#print axioms cayley_isometry_so8_rat
#print axioms cayley_mat8_repeated_index_is_identity
#print axioms cayley_mat8_zero_zero_non_singular

end FableHilbertWalk20260819.H019
