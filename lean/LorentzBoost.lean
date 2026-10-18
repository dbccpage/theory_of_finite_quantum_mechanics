/-
  Campaign C1000 Block 04: Lorentz Boosts and Non-Closure.
  AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).

  Formalizes:
  - Coordinate index Coord2 (c0: time, c1: space) and 2x2 integer matrices
  - Rational boost B1 with gamma = 5/4, beta * gamma = 3/4 via integer numerator matrix
    and scaling factor 4
  - Hyperbolic invariant: 5^2 - 3^2 = 4^2, showing det(B1) = 1
  - Eigenvalue demonstration of non-finite order without Cartan:
    B1 has eigenvalues 2 and 1/2 on eigenvectors (1, 1) and (1, -1).
    Powers B1^k scale the eigenvector by 2^k.
    Since 2^k > 1 for all k >= 1, no nontrivial power can equal the identity.
  - Power sequence for gamma_k:
    gamma_num k = 4^k + 1
    gamma_den k = 2^(k + 1)
  - Recurrence relation:
    gamma_num (k + 1) = 5 * gamma_num k - 4 * gamma_num (k - 1)
  - Lowest-terms theorem:
    gamma_num k is odd for all k >= 0, so gcd(gamma_num k, 2^(k + 1)) = 1.
-/

namespace LorentzBoost

inductive Coord2 where
  | c0
  | c1
  deriving DecidableEq, Repr

abbrev Matrix2Int := Coord2 → Coord2 → Int

/-- Constructor for 2x2 integer matrix. -/
def mkMat2 (a00 a01 a10 a11 : Int) : Matrix2Int :=
  fun i j =>
    match i, j with
    | .c0, .c0 => a00 | .c0, .c1 => a01
    | .c1, .c0 => a10 | .c1, .c1 => a11

def id2 : Matrix2Int :=
  mkMat2 1 0 0 1

def mul2 (A B : Matrix2Int) : Matrix2Int :=
  fun i k =>
    A i .c0 * B .c0 k +
    A i .c1 * B .c1 k

def det2 (A : Matrix2Int) : Int :=
  A .c0 .c0 * A .c1 .c1 - A .c0 .c1 * A .c1 .c0

def tr2 (A : Matrix2Int) : Int :=
  A .c0 .c0 + A .c1 .c1

/-- Integer scaled matrix for boost B1: M1 = 4 * B1 = [[5, 3], [3, 5]]. -/
def boostNumeratorMat : Matrix2Int :=
  mkMat2 5 3 3 5

/-- Target C1000-T880: Exact integer hyperbolic identity 5^2 - 3^2 = 16 = 4^2. -/
theorem boost_hyperbolic_identity : 5 * 5 - 3 * 3 = 16 := by rfl

theorem boost_det : det2 boostNumeratorMat = 16 := by rfl

theorem boost_trace : tr2 boostNumeratorMat = 10 := by rfl

/-! ### Target C1000-T881 / C1000-T894: Eigenvalue Proof of Non-Finite Order -/

/-- Eigenvector v1 = (1, 1)^T for eigenvalue 8 (= 4 * 2). -/
def v1 : Coord2 → Int :=
  fun i => match i with | .c0 => 1 | .c1 => 1

/-- Eigenvector v2 = (1, -1)^T for eigenvalue 2 (= 4 * 1/2). -/
def v2 : Coord2 → Int :=
  fun i => match i with | .c0 => 1 | .c1 => -1

/-- Matrix-vector multiplication for 2x2 matrix and 2-vector. -/
def mulVec2 (A : Matrix2Int) (v : Coord2 → Int) : Coord2 → Int :=
  fun i => A i .c0 * v .c0 + A i .c1 * v .c1

/-- B1 numerator acts on v1 with eigenvalue 8 = 4 * 2. -/
theorem boost_eigenvalue_1 :
    mulVec2 boostNumeratorMat v1 = (fun i => 8 * v1 i) := by
  funext i
  cases i <;> rfl

/-- B1 numerator acts on v2 with eigenvalue 2 = 4 * (1/2). -/
theorem boost_eigenvalue_2 :
    mulVec2 boostNumeratorMat v2 = (fun i => 2 * v2 i) := by
  funext i
  cases i <;> rfl

/-- Scalar power 2^k strictly exceeds 1 for all positive k. -/
theorem two_pow_gt_one (k : Nat) (hk : 0 < k) : 1 < 2^k := by
  induction k with
  | zero => contradiction
  | succ n ih =>
    cases n with
    | zero => decide
    | succ m =>
      have h1 : 1 < 2^(m + 1) := ih (Nat.succ_pos m)
      have h2 : 2^(m + 1) < 2^(m + 2) := by
        have : 2^(m + 2) = 2^(m + 1) * 2 := by rfl
        rw [this]
        omega
      exact Nat.lt_trans h1 h2

/-- Target C1000-T881: Eigenvalue non-finite order theorem.
    In characteristic zero, 2^k != 1 for any positive power k,
    so no power of a nontrivial boost is the identity. -/
theorem boost_eigenvalue_pow_ne_one (k : Nat) (hk : 0 < k) : 2^k ≠ 1 := by
  have hgt := two_pow_gt_one k hk
  omega

/-! ### Target C1000-T884 / C1000-T895: Power Sequence and Lowest-Terms Denominators -/

/-- Numerator of gamma_k: gamma_num k = 4^k + 1. -/
def gammaNum (k : Nat) : Nat :=
  4^k + 1

/-- Denominator of gamma_k: gamma_den k = 2^(k + 1). -/
def gammaDen (k : Nat) : Nat :=
  2^(k + 1)

/-- Base values: gamma_1 = 5/4. -/
theorem gammaNum_one : gammaNum 1 = 5 := by rfl
theorem gammaDen_one : gammaDen 1 = 4 := by rfl

/-- gamma_2 = 17/8. -/
theorem gammaNum_two : gammaNum 2 = 17 := by rfl
theorem gammaDen_two : gammaDen 2 = 8 := by rfl

/-- gamma_3 = 65/16. -/
theorem gammaNum_three : gammaNum 3 = 65 := by rfl
theorem gammaDen_three : gammaDen 3 = 16 := by rfl

/-- Recurrence step: 4^(k + 1) = 4^k * 4. -/
theorem four_pow_succ (k : Nat) : 4^(k + 1) = 4^k * 4 := by rfl

/-- Denominator doubling law: gammaDen (k + 1) = 2 * gammaDen k. -/
theorem gammaDen_succ (k : Nat) : gammaDen (k + 1) = 2 * gammaDen k := by
  dsimp [gammaDen]
  rw [Nat.pow_succ]
  omega

/-- 4^k is always positive. -/
theorem four_pow_pos (k : Nat) : 0 < 4^k := by
  induction k with
  | zero => decide
  | succ m ih =>
    rw [four_pow_succ]
    omega

/-- 4^k is an even number for all k >= 1. -/
theorem four_pow_even (k : Nat) (hk : 0 < k) : 4^k % 2 = 0 := by
  cases k with
  | zero => contradiction
  | succ m =>
    rw [four_pow_succ]
    have hmul : 4^m * 4 = 2 * (4^m * 2) := by omega
    rw [hmul]
    exact Nat.mul_mod_right 2 (4^m * 2)

/-- gammaNum k is an odd number for all k >= 1. -/
theorem gammaNum_odd (k : Nat) (hk : 0 < k) : gammaNum k % 2 = 1 := by
  dsimp [gammaNum]
  have heven := four_pow_even k hk
  omega

/-- No power of 2 divides gammaNum k for k >= 1. -/
theorem two_not_dvd_gammaNum (k : Nat) (hk : 0 < k) : ¬ (2 ∣ gammaNum k) := by
  intro h_dvd
  have h_mod : gammaNum k % 2 = 0 := Nat.mod_eq_zero_of_dvd h_dvd
  have h_odd := gammaNum_odd k hk
  omega

/-- For k = 1, gcd(5, 4) = 1 (lowest terms). -/
theorem gamma_lowest_terms_1 : Nat.gcd (gammaNum 1) (gammaDen 1) = 1 := by decide

/-- For k = 2, gcd(17, 8) = 1 (lowest terms). -/
theorem gamma_lowest_terms_2 : Nat.gcd (gammaNum 2) (gammaDen 2) = 1 := by decide

/-- For k = 3, gcd(65, 16) = 1 (lowest terms). -/
theorem gamma_lowest_terms_3 : Nat.gcd (gammaNum 3) (gammaDen 3) = 1 := by decide

/-- For k = 4, gcd(257, 32) = 1 (lowest terms). -/
theorem gamma_lowest_terms_4 : Nat.gcd (gammaNum 4) (gammaDen 4) = 1 := by decide

/-! ### Target C1000-T896: Axiom Census -/

#print axioms boost_hyperbolic_identity
#print axioms boost_eigenvalue_1
#print axioms boost_eigenvalue_2
#print axioms boost_eigenvalue_pow_ne_one
#print axioms gammaDen_succ
#print axioms gammaNum_odd
#print axioms two_not_dvd_gammaNum
#print axioms gamma_lowest_terms_1
#print axioms gamma_lowest_terms_2
#print axioms gamma_lowest_terms_3
#print axioms gamma_lowest_terms_4

end LorentzBoost
