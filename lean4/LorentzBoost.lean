

namespace LorentzBoost

inductive Coord2 where
  | c0
  | c1
  deriving DecidableEq, Repr

abbrev Matrix2Int := Coord2 → Coord2 → Int

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

def boostNumeratorMat : Matrix2Int :=
  mkMat2 5 3 3 5

theorem boost_hyperbolic_identity : 5 * 5 - 3 * 3 = 16 := by rfl

theorem boost_det : det2 boostNumeratorMat = 16 := by rfl

theorem boost_trace : tr2 boostNumeratorMat = 10 := by rfl


def v1 : Coord2 → Int :=
  fun i => match i with | .c0 => 1 | .c1 => 1

def v2 : Coord2 → Int :=
  fun i => match i with | .c0 => 1 | .c1 => -1

def mulVec2 (A : Matrix2Int) (v : Coord2 → Int) : Coord2 → Int :=
  fun i => A i .c0 * v .c0 + A i .c1 * v .c1

theorem boost_eigenvalue_1 :
    mulVec2 boostNumeratorMat v1 = (fun i => 8 * v1 i) := by
  funext i
  cases i <;> rfl

theorem boost_eigenvalue_2 :
    mulVec2 boostNumeratorMat v2 = (fun i => 2 * v2 i) := by
  funext i
  cases i <;> rfl

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

theorem boost_eigenvalue_pow_ne_one (k : Nat) (hk : 0 < k) : 2^k ≠ 1 := by
  have hgt := two_pow_gt_one k hk
  omega


def gammaNum (k : Nat) : Nat :=
  4^k + 1

def gammaDen (k : Nat) : Nat :=
  2^(k + 1)

theorem gammaNum_one : gammaNum 1 = 5 := by rfl
theorem gammaDen_one : gammaDen 1 = 4 := by rfl

theorem gammaNum_two : gammaNum 2 = 17 := by rfl
theorem gammaDen_two : gammaDen 2 = 8 := by rfl

theorem gammaNum_three : gammaNum 3 = 65 := by rfl
theorem gammaDen_three : gammaDen 3 = 16 := by rfl

theorem four_pow_succ (k : Nat) : 4^(k + 1) = 4^k * 4 := by rfl

theorem gammaDen_succ (k : Nat) : gammaDen (k + 1) = 2 * gammaDen k := by
  dsimp [gammaDen]
  rw [Nat.pow_succ]
  omega

theorem four_pow_pos (k : Nat) : 0 < 4^k := by
  induction k with
  | zero => decide
  | succ m ih =>
    rw [four_pow_succ]
    omega

theorem four_pow_even (k : Nat) (hk : 0 < k) : 4^k % 2 = 0 := by
  cases k with
  | zero => contradiction
  | succ m =>
    rw [four_pow_succ]
    have hmul : 4^m * 4 = 2 * (4^m * 2) := by omega
    rw [hmul]
    exact Nat.mul_mod_right 2 (4^m * 2)

theorem gammaNum_odd (k : Nat) (hk : 0 < k) : gammaNum k % 2 = 1 := by
  dsimp [gammaNum]
  have heven := four_pow_even k hk
  omega

theorem two_not_dvd_gammaNum (k : Nat) (hk : 0 < k) : ¬ (2 ∣ gammaNum k) := by
  intro h_dvd
  have h_mod : gammaNum k % 2 = 0 := Nat.mod_eq_zero_of_dvd h_dvd
  have h_odd := gammaNum_odd k hk
  omega

theorem gamma_lowest_terms_1 : Nat.gcd (gammaNum 1) (gammaDen 1) = 1 := by decide

theorem gamma_lowest_terms_2 : Nat.gcd (gammaNum 2) (gammaDen 2) = 1 := by decide

theorem gamma_lowest_terms_3 : Nat.gcd (gammaNum 3) (gammaDen 3) = 1 := by decide

theorem gamma_lowest_terms_4 : Nat.gcd (gammaNum 4) (gammaDen 4) = 1 := by decide


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

private def l5aProvenance : String :=
  "Origin: lean4/LorentzBoost.lean Claim: boost_hyperbolic_identity AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
