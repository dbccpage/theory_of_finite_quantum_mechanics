




namespace FableHilbertWalk20260819.H019


abbrev Dim8 := Fin 8

def strictlyUpperPairs8 : List (Dim8 × Dim8) :=
  (List.finRange 8).flatMap (fun i =>
    (List.finRange 8).filterMap (fun j =>
      if i.val < j.val then some (i, j) else none))

theorem so8_dimension_count :
    strictlyUpperPairs8.length = 28 := by
  decide

theorem strictlyUpperPairs8_nodup :
    strictlyUpperPairs8.Nodup := by
  decide

def basisGen8 (i j : Dim8) : Dim8 → Dim8 → Int :=
  fun r c =>
    (if r == i && c == j then (1 : Int) else 0) -
    (if r == j && c == i then (1 : Int) else 0)

theorem basisGen8_is_skew (i j : Dim8) :
    ∀ r c : Dim8, basisGen8 i j c r = - (basisGen8 i j r c) := by
  intro r c
  dsimp [basisGen8]
  have h1 : (c == j && r == i) = (r == i && c == j) := Bool.and_comm _ _
  have h2 : (c == i && r == j) = (r == j && c == i) := Bool.and_comm _ _
  rw [h1, h2]
  cases (r == j && c == i) <;> cases (r == i && c == j) <;> rfl

theorem basisGen8_diag_zero (i j : Dim8) :
    ∀ r : Dim8, basisGen8 i j r r = 0 := by
  intro r
  dsimp [basisGen8]
  have h : (r == j && r == i) = (r == i && r == j) := Bool.and_comm _ _
  rw [h]
  cases (r == i && r == j) <;> rfl

theorem basisGen8_eval_pos (i j : Dim8) (hij : (i == j) = false) (hji : (j == i) = false) :
    basisGen8 i j i j = 1 := by
  dsimp [basisGen8]
  simp [hij, hji]


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

def StarAlgebra.bracket {α : Type} (S : StarAlgebra α) (x y : α) : α :=
  S.sub (S.mul x y) (S.mul y x)

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

theorem cayley_isometry_so8 {α : Type} (S : StarAlgebra α)
    (A B Ainv Binv : α)
    (h_comm : S.mul B A = S.mul A B)
    (h_star_A : S.star A = B)
    (h_star_Binv : S.star Binv = Ainv)
    (h_inv_A_left : S.mul Ainv A = S.one)
    (h_inv_B_right : S.mul B Binv = S.one) :
    S.mul (S.star (S.mul A Binv)) (S.mul A Binv) = S.one := by
  exact cayley_isometry_general S A B Ainv Binv h_comm h_star_A h_star_Binv h_inv_A_left h_inv_B_right


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

def skewGen2Int : Mat2Int := ⟨0, -1, 1, 0⟩

def cayleyMat2 (p q : Int) : Mat2Int :=
  ⟨q * q - p * p, -(2 * p * q), 2 * p * q, q * q - p * p⟩

def cayleyDenom (p q : Int) : Int :=
  p * p + q * q

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

def mul8 (A B : Dim8 → Dim8 → Int) : Dim8 → Dim8 → Int :=
  fun r c =>
    (List.finRange 8).foldl (fun acc k => acc + A r k * B k c) 0

def transpose8 (A : Dim8 → Dim8 → Int) : Dim8 → Dim8 → Int :=
  fun r c => A c r

def smulId8 (s : Int) : Dim8 → Dim8 → Int :=
  fun r c => if r == c then s else 0

theorem cayley_mat8_repeated_index_is_identity (i : Dim8) (p q : Int) (r c : Dim8) :
    cayleyMat8Numerator i i p q r c = smulId8 (p * p + q * q) r c := by
  dsimp [cayleyMat8Numerator, smulId8]
  have hi : (i == i) = true := by revert i; decide
  rw [hi]
  rfl

theorem cayley_mat8_zero_zero_non_singular :
    (∀ r c : Dim8, cayleyMat8Numerator ⟨0, by decide⟩ ⟨0, by decide⟩ 1 1 r c = smulId8 2 r c) ∧
    (∀ r c : Dim8,
      mul8 (transpose8 (cayleyMat8Numerator ⟨0, by decide⟩ ⟨0, by decide⟩ 1 1))
           (cayleyMat8Numerator ⟨0, by decide⟩ ⟨0, by decide⟩ 1 1) r c =
      smulId8 ((cayleyDenom 1 1) * (cayleyDenom 1 1)) r c) := by
  refine ⟨by decide, by decide⟩

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

private def l5aProvenance : String :=
  "Origin: lean4/H019RationalLieSpan.lean Claim: so8_dimension_count AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
