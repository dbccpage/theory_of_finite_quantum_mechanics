import WitnessedDifference.Core
import WitnessedDifference.Difference

/-!
# Finite algebraic witnesses for the quantum-import discussion

These theorems are the small witnesses identified in the manuscript. Their
conjunction is not an independence theorem for eight quantum axioms and does
not characterize continuous quantum mechanics.

1. No integer solves x*x + 1 = 0; this does not analyze Cauchy completion.
2. Integer signs exhibit cancellation without continuous phases.
3. Two integer matrices fail to commute, whereas diagonal matrices commute.
   This is not a spectral decomposition theorem or its negation.
4. The quartic function is nonnegative and differs from the square at 2.
   No normalized frame-additive valuation on all projections is constructed.
5. Functions on a disjoint sum split into, and reassemble from, two components.
   No uniqueness or classification theorem for physical composites follows.
6. A map preserving every pairwise inner product cannot identify two
   orthogonal basis vectors. Norm preservation alone is insufficient; no
   Stinespring dilation is constructed.
7. The Boolean toggle has no square root among endomaps of Bool.
8. Two natural counts summing to one are (1,0) or (0,1). This is not a
   convex-closure or dual-cone completion result.

The historical declaration names are retained for source compatibility.
-/

namespace WitnessedDifference

open WitnessedDifference

/-! ## Discrete Permutation-Isometry Envelope -/

def Q2 := Bool

def Vec2 := Q2 → Int

def dot2 (u v : Vec2) : Int :=
  u false * v false + u true * v true

def l1Norm2 (v : Vec2) : Nat :=
  (v false).natAbs + (v true).natAbs

def permAct (σ : Equiv Q2 Q2) (v : Vec2) : Vec2 :=
  fun q => v (σ.invFun q)

theorem discrete_difference_supports_integer_permutation_isometry :
    ∀ (σ : Equiv Q2 Q2) (u v : Vec2),
      dot2 (permAct σ u) (permAct σ v) = dot2 u v ∧
      l1Norm2 (permAct σ u) = l1Norm2 u := by
  intro σ u v
  by_cases hf : σ.invFun false = false
  · have ht : σ.invFun true = true := by
      by_cases ht' : σ.invFun true = false
      · have h_contra : false = true := by
          have h1 : σ.toFun (σ.invFun false) = σ.toFun (σ.invFun true) := by
            rw [hf, ht']
          rw [σ.right_inv false, σ.right_inv true] at h1
          exact h1
        cases h_contra
      · cases h_bool : σ.invFun true with
        | false => contradiction
        | true => rfl
    constructor
    · show (u (σ.invFun false) * v (σ.invFun false) + u (σ.invFun true) * v (σ.invFun true)) = u false * v false + u true * v true
      rw [hf, ht]
    · show (u (σ.invFun false)).natAbs + (u (σ.invFun true)).natAbs = (u false).natAbs + (u true).natAbs
      rw [hf, ht]
  · have hf_true : σ.invFun false = true := by
      cases h_bool : σ.invFun false with
      | false => contradiction
      | true => rfl
    have ht : σ.invFun true = false := by
      by_cases ht' : σ.invFun true = true
      · have h_contra : false = true := by
          have h1 : σ.toFun (σ.invFun false) = σ.toFun (σ.invFun true) := by
            rw [hf_true, ht']
          rw [σ.right_inv false, σ.right_inv true] at h1
          exact h1
        cases h_contra
      · cases h_bool : σ.invFun true with
        | false => rfl
        | true => contradiction
    constructor
    · show (u (σ.invFun false) * v (σ.invFun false) + u (σ.invFun true) * v (σ.invFun true)) = u false * v false + u true * v true
      rw [hf_true, ht]
      exact Int.add_comm (u true * v true) (u false * v false)
    · show (u (σ.invFun false)).natAbs + (u (σ.invFun true)).natAbs = (u false).natAbs + (u true).natAbs
      rw [hf_true, ht]
      exact Nat.add_comm (u true).natAbs (u false).natAbs

/-! ## Import 1: Continuous Field ℂ (Unforced) -/

theorem import1_unforced : ¬ ∃ x : Int, x * x + 1 = 0 := by
  intro ⟨x, hx⟩
  cases x with
  | ofNat n =>
    have h1 : (Int.ofNat n) * (Int.ofNat n) + 1 = Int.ofNat (n * n + 1) := rfl
    rw [h1] at hx
    cases hx
  | negSucc n =>
    have h1 : (Int.negSucc n) * (Int.negSucc n) + 1 = Int.ofNat ((n + 1) * (n + 1) + 1) := rfl
    rw [h1] at hx
    cases hx

/-! ## Import 2: Continuous Circle Group U(1) (Unforced) -/

theorem import2_unforced :
    ∃ s₁ s₂ : Int, (s₁ = 1 ∨ s₁ = -1) ∧ (s₂ = 1 ∨ s₂ = -1) ∧ s₁ + s₂ = 0 ∧ s₁ + s₁ ≠ 0 := by
  refine ⟨1, -1, Or.inl rfl, Or.inr rfl, rfl, ?_⟩
  intro h
  cases h

/-! ## Import 3: Spectral Theorem for Self-Adjoint Operators (Unforced) -/

def Mat : Type := Bool → Bool → Int

def mmul (A B : Mat) : Mat :=
  fun i j => A i false * B false j + A i true * B true j

/-- Elementary matrix unit E_{01} -/
def matE01 : Mat := fun i j => if (!i && j) then 1 else 0

/-- Elementary matrix unit E_{10} -/
def matE10 : Mat := fun i j => if (i && !j) then 1 else 0

def nMat : Mat := matE01
def nMat' : Mat := matE10

def diag (d : Bool → Int) : Mat :=
  fun i j => if i == j then d i else 0

theorem noncomm_witness :
    ¬(∀ i j : Bool, mmul matE01 matE10 i j = mmul matE10 matE01 i j) := by
  intro h
  have h1 := h false false
  revert h1
  decide

theorem diagonal_commutes (d e : Bool → Int) :
    ∀ i j : Bool, mmul (diag d) (diag e) i j = mmul (diag e) (diag d) i j := by
  intro i j
  cases i <;> cases j <;> simp [mmul, diag, Int.mul_comm]

theorem import3_unforced :
    ¬(∀ i j : Bool, mmul matE01 matE10 i j = mmul matE10 matE01 i j) ∧
      (∀ (d e : Bool → Int) (i j : Bool),
        mmul (diag d) (diag e) i j = mmul (diag e) (diag d) i j) :=
  ⟨noncomm_witness, fun d e i j => diagonal_commutes d e i j⟩

/-! ## Import 4: Gleason Frame Continuity (Unforced) -/

def quarticVal (x : Int) : Int := x * x * x * x

theorem quarticVal_nonneg (x : Int) : 0 ≤ quarticVal x := by
  cases x with
  | ofNat n =>
    change (0 : Int) ≤ Int.ofNat (n * n * n * n)
    exact Int.natCast_nonneg (n * n * n * n)
  | negSucc n =>
    change (0 : Int) ≤ Int.ofNat ((n + 1) * (n + 1) * (n + 1) * (n + 1))
    exact Int.natCast_nonneg ((n + 1) * (n + 1) * (n + 1) * (n + 1))

theorem import4_unforced :
    quarticVal 0 = 0 ∧
    quarticVal 1 = 1 ∧
    quarticVal 2 ≠ 2 * 2 ∧
    (∀ x : Int, 0 ≤ quarticVal x) :=
  ⟨rfl, rfl, by decide, quarticVal_nonneg⟩

/-! ## Import 5: Unique Tensor Product (Unforced) -/

def sumSplit (w : Sum Bool Bool → Int) : (Bool → Int) × (Bool → Int) :=
  (fun b => w (Sum.inl b), fun b => w (Sum.inr b))

def sumJoin (p : (Bool → Int) × (Bool → Int)) : Sum Bool Bool → Int
  | Sum.inl b => p.1 b
  | Sum.inr b => p.2 b

theorem import5_unforced :
    ∀ w : Sum Bool Bool → Int, sumJoin (sumSplit w) = w := by
  intro w
  funext s
  cases s with
  | inl b => rfl
  | inr b => rfl

/-! ## Import 6: CPTP Channels & Stinespring Dilation (Unforced) -/

def basis0 : Vec2
  | false => 1
  | true  => 0

def basis1 : Vec2
  | false => 0
  | true  => 1

theorem import6_unforced :
    ¬ ∃ U : Vec2 → Vec2,
      (∀ u v : Vec2, dot2 (U u) (U v) = dot2 u v) ∧
      U basis0 = basis0 ∧
      U basis1 = basis0 := by
  intro ⟨U, h_iso, h_b0, h_b1⟩
  have h_dot_orig : dot2 basis0 basis1 = 0 := rfl
  have h_dot_mapped : dot2 (U basis0) (U basis1) = 1 := by
    rw [h_b0, h_b1]
    rfl
  have h_dot_eq := h_iso basis0 basis1
  rw [h_dot_mapped] at h_dot_eq
  rw [h_dot_orig] at h_dot_eq
  cases h_dot_eq

/-! ## Import 7: Continuous 1-Parameter Unitary Dynamics (Unforced) -/

def toggleOp (q : Bool) : Bool := !q

theorem import7_unforced :
    ¬ ∃ σ : Bool → Bool, ∀ q : Bool, σ (σ q) = toggleOp q := by
  intro ⟨σ, hσ⟩
  cases hff : σ false with
  | false =>
    have h1 := hσ false
    dsimp [toggleOp] at h1
    rw [hff, hff] at h1
    cases h1
  | true =>
    cases htf : σ true with
    | false =>
      have h1 := hσ false
      dsimp [toggleOp] at h1
      rw [hff, htf] at h1
      cases h1
    | true =>
      have h2 := hσ true
      dsimp [toggleOp] at h2
      rw [htf, htf] at h2
      cases h2

/-! ## Import 8: Continuous Dual Cone Completion (Unforced) -/

def IsExtremalCount (c : Bool → Nat) : Prop :=
  c false + c true = 1

theorem import8_unforced (c : Bool → Nat) (h : IsExtremalCount c) :
    (c false = 1 ∧ c true = 0) ∨ (c false = 0 ∧ c true = 1) := by
  dsimp [IsExtremalCount] at h
  omega

/-! ## Conjunction of the finite witnesses -/

theorem quantum_reconstruction_boundary :
    (∀ (σ : Equiv Q2 Q2) (u v : Vec2),
      dot2 (permAct σ u) (permAct σ v) = dot2 u v ∧
      l1Norm2 (permAct σ u) = l1Norm2 u) ∧
    (¬ ∃ x : Int, x * x + 1 = 0) ∧
    (∃ s₁ s₂ : Int, (s₁ = 1 ∨ s₁ = -1) ∧ (s₂ = 1 ∨ s₂ = -1) ∧ s₁ + s₂ = 0 ∧ s₁ + s₁ ≠ 0) ∧
    (¬(∀ i j : Bool, mmul nMat nMat' i j = mmul nMat' nMat i j) ∧
      (∀ (d e : Bool → Int) (i j : Bool),
        mmul (diag d) (diag e) i j = mmul (diag e) (diag d) i j)) ∧
    (quarticVal 0 = 0 ∧
     quarticVal 1 = 1 ∧
     quarticVal 2 ≠ 2 * 2 ∧
     (∀ x : Int, 0 ≤ quarticVal x)) ∧
    (∀ w : Sum Bool Bool → Int, sumJoin (sumSplit w) = w) ∧
    (¬ ∃ U : Vec2 → Vec2,
      (∀ u v : Vec2, dot2 (U u) (U v) = dot2 u v) ∧
      U basis0 = basis0 ∧
      U basis1 = basis0) ∧
    (¬ ∃ σ : Bool → Bool, ∀ q : Bool, σ (σ q) = toggleOp q) ∧
    (∀ (c : Bool → Nat), IsExtremalCount c →
      (c false = 1 ∧ c true = 0) ∨ (c false = 0 ∧ c true = 1)) :=
  ⟨discrete_difference_supports_integer_permutation_isometry,
   import1_unforced,
   import2_unforced,
   import3_unforced,
   import4_unforced,
   import5_unforced,
   import6_unforced,
   import7_unforced,
   import8_unforced⟩

end WitnessedDifference
