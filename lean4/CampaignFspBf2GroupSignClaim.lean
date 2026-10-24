import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-!
# Campaign: FSP-BF-2GROUP-SIGN-CLAIM (TFQ-1210 / FSP-DERIV-046)

Formalizes the finite cochain, braiding, and cohomology structures underlying 3D/4D BF
and strict 2-group gauge models on finite cell complexes, together with the explicit
scope fences recorded in `GIN-C19` through `GIN-C21` and the `TFQ-1210` witness audit:

1. **Simplicial Cochain Complex Nilpotence on `Δ⁴`**:
   - Exact coboundary identities `d₁ ∘ d₀ = 0`, `d₂ ∘ d₁ = 0`, and `d₃ ∘ d₂ = 0` over any
     commutative additive group `A`, and discrete BF gauge invariance `d₁ (A + d₀ λ) = d₁ A`.
2. **Abelian `ℤ_k` BF Braiding Level-Parity Trichotomy (`GIN-C19`)**:
   - At level `k = 2` (`ℤ₂` BF / 3D toric code), unit Hopf linking (`lk = ±1`) produces sign
     `-1`, which cancels against an equal-weight positive reference partner (`w - w = 0`)
     when `w₊ = w₋`, whereas thermal orientation asymmetry `w₊ ≠ w₋` leaves `w₊ - w₋ ≠ 0`.
   - At level `k = 3` (`ℤ₃` fractional BF), the exact `SL(2, ℤ)` cyclotomic companion matrix
     `omega3Mat` satisfies `omega3Mat ^ 3 = 1`, `omega3Mat ^ 2 ≠ 1` (non-involution), and
     orientation-paired sum `omega3Mat + omega3Mat ^ 2 = -1` (reflecting `2 cos(2π/3) = -1 < 0`).
3. **Non-Abelian Wang-Levin 3-Loop Braiding Commutator (`GIN-C20`)**:
   - In the 2D `SU(2)₂` (Ising) fusion channel, the involutive monodromy generators
     `b1Ising = σ_z` and `b2Ising = σ_x` have group commutator
     `wangLevinCommutator = b1Ising * b2Ising * b1Ising * b2Ising = -1` with negative trace `-2`,
     whereas diagonal abelian monodromy matrices commute (`D₁ D₂ = D₂ D₁`).
4. **Strict 2-Group Crossed Module & Nontrivial Postnikov Class `[a] ∈ H³(Bℤ₂, ℤ₂)` (`GIN-C21`)**:
   - Conjugation crossed module `(G, G, id, conj)` satisfies both the Peiffer identity and
     the second crossed-module identity.
   - The cup-product 3-cochain `postnikovCup3(g₁, g₂, g₃) = g₁ * g₂ * g₃` on `ZMod 2` is a
     3-cocycle (`groupCoboundary3 postnikovCup3 = 0`) and is **not** the coboundary of any
     2-cochain `b : ZMod 2 → ZMod 2 → ZMod 2` (`groupCoboundary2 b ≠ postnikovCup3`),
     witnessed by the invariant 3-cycle functional `c(1,0,0) + c(0,0,1) + c(1,1,1)`.
5. **Model-Change Scope Fences (`GIN-C20` / `GIN-C21`, Manuscript Line 448)**:
   - Replacing a chiral amplitude or trace `Z` by its doubled norm-square `Z * Z` (or
     squaring configuration weights `wᵢ²`) changes the target model: `Z₊ = 2` and `Z₋ = -2`
     become indistinguishable (`Z₊² = Z₋² = 4`), and squaring weights in `(1, -1)` alters
     the partition sum from `1 + (-1) = 0` to `1² + (-1)² = 2 ≠ (1 + (-1))²`.
-/

namespace CampaignFspBf2GroupSignClaim

open Matrix

/-- Simplicial 0-coboundary `(d₀ c₀)(i, j) = c₀(j) - c₀(i)` on `Fin 5`. -/
def d0 {A : Type*} [AddCommGroup A] (c0 : Fin 5 → A) (i j : Fin 5) : A :=
  c0 j - c0 i

/-- Simplicial 1-coboundary `(d₁ c₁)(i, j, k) = c₁(j, k) - c₁(i, k) + c₁(i, j)` on `Fin 5`. -/
def d1 {A : Type*} [AddCommGroup A] (c1 : Fin 5 → Fin 5 → A) (i j k : Fin 5) : A :=
  c1 j k - c1 i k + c1 i j

/-- Simplicial 2-coboundary `(d₂ c₂)(i, j, k, l)` on `Fin 5`. -/
def d2 {A : Type*} [AddCommGroup A] (c2 : Fin 5 → Fin 5 → Fin 5 → A)
    (i j k l : Fin 5) : A :=
  c2 j k l - c2 i k l + c2 i j l - c2 i j k

/-- Simplicial 3-coboundary `(d₃ c₃)(i, j, k, l, m)` on `Fin 5`. -/
def d3 {A : Type*} [AddCommGroup A] (c3 : Fin 5 → Fin 5 → Fin 5 → Fin 5 → A)
    (i j k l m : Fin 5) : A :=
  c3 j k l m - c3 i k l m + c3 i j l m - c3 i j k m + c3 i j k l

/-- Theorem 1 (Simplicial Coboundary Nilpotence on `Δ⁴`):
Over any commutative additive group `A`, the simplicial coboundaries satisfy
`d₁ (d₀ c₀) = 0`, `d₂ (d₁ c₁) = 0`, and `d₃ (d₂ c₂) = 0`. -/
theorem simplicial_coboundary_nilpotence_d1d0_d2d1_d3d2 {A : Type*} [AddCommGroup A]
    (c0 : Fin 5 → A) (c1 : Fin 5 → Fin 5 → A) (c2 : Fin 5 → Fin 5 → Fin 5 → A)
    (i j k l m : Fin 5) :
    d1 (d0 c0) i j k = 0 ∧
    d2 (d1 c1) i j k l = 0 ∧
    d3 (d2 c2) i j k l m = 0 := by
  refine ⟨?_, ?_, ?_⟩
  · dsimp [d1, d0]; abel
  · dsimp [d2, d1]; abel
  · dsimp [d3, d2]; abel

/-- Theorem 2 (Discrete BF 1-Form and 2-Form Gauge Invariance):
Shifting the 1-cochain `A₁` by an exact 0-coboundary `d₀ λ` leaves the curvature
`d₁ (A₁ + d₀ λ) = d₁ A₁` invariant, and shifting the 2-cochain `B₂` by `d₁ η` leaves the
3-curvature `d₂ (B₂ + d₁ η) = d₂ B₂` invariant. -/
theorem bf_cochain_gauge_invariance {A : Type*} [AddCommGroup A]
    (A1 : Fin 5 → Fin 5 → A) (lam : Fin 5 → A)
    (B2 : Fin 5 → Fin 5 → Fin 5 → A) (eta : Fin 5 → Fin 5 → A)
    (i j k l : Fin 5) :
    d1 (fun u v => A1 u v + d0 lam u v) i j k = d1 A1 i j k ∧
    d2 (fun u v w => B2 u v w + d1 eta u v w) i j k l = d2 B2 i j k l := by
  refine ⟨?_, ?_⟩
  · dsimp [d1, d0]; abel
  · dsimp [d2, d1]; abel

/-- Theorem 3 (`ℤ₂` BF Hopf-Link Sign and Orientation Weight Trichotomy, `GIN-C19`):
Under orientation inversion `lk ↦ -lk`, the BF linking product `q * p * (-lk) = -(q * p * lk)`
reverses sign; at `k = 2` with `q = p = lk = 1`, the Hopf-link sign factor is `(-1)^1 = -1`,
symmetric doublet weights `w₊ = w₋` cancel (`w₊ * 1 + w₋ * (-1) = 0`), whereas asymmetric
orientation weights `w₊ ≠ w₋` leave a nonzero residual `w₊ * 1 + w₋ * (-1) ≠ 0`. -/
theorem bf_z2_level_hopf_link_sign_and_weight_trichotomy (q p lk w_pos w_neg : ℤ) :
    q * p * (-lk) = -(q * p * lk) ∧
    (-1 : ℤ) ^ (1 : ℕ) = -1 ∧
    (w_pos = w_neg → w_pos * 1 + w_neg * (-1) = 0) ∧
    (w_pos ≠ w_neg → w_pos * 1 + w_neg * (-1) ≠ 0) := by
  refine ⟨by ring, rfl, ?_, ?_⟩
  · intro h
    omega
  · intro hne heq
    apply hne
    omega

/-- `SL(2, ℤ)` companion matrix of `ω = e^{2πi/3}` on `ℤ[ω] ≅ ℤ²` (`ω² + ω + 1 = 0`). -/
def omega3Mat : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, -1;
     1, -1]

/-- Theorem 4 (`ℤ₃` Fractional BF Non-Involution and Negative Orientation-Paired Sum Fence, `GIN-C19`):
At level `k = 3`, the monodromy generator `omega3Mat` has order 3 (`omega3Mat ^ 3 = 1`), is
not an involution (`omega3Mat ^ 2 ≠ 1`), and its orientation-paired sum with its inverse
`omega3Mat ^ 2` equals `-1 = !![-1, 0; 0, -1]` (recording `ω + ω⁻¹ = 2 cos(2π/3) = -1 < 0`). -/
theorem bf_z3_level_non_involution_and_cos_sum_fence :
    omega3Mat ^ 3 = (1 : Matrix (Fin 2) (Fin 2) ℤ) ∧
    omega3Mat ^ 2 ≠ (1 : Matrix (Fin 2) (Fin 2) ℤ) ∧
    omega3Mat + omega3Mat ^ 2 = -(1 : Matrix (Fin 2) (Fin 2) ℤ) ∧
    Matrix.trace (omega3Mat + omega3Mat ^ 2) = -2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · intro h
    have h00 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℤ => M 0 0) h
    revert h00
    decide
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · decide

/-- `SU(2)₂` (Ising level) 2D fusion-space monodromy generator `B₁ = σ_z`. -/
def b1Ising : Matrix (Fin 2) (Fin 2) ℤ :=
  !![1, 0;
     0, -1]

/-- `SU(2)₂` (Ising level) conjugated monodromy generator `B₂ = σ_x`. -/
def b2Ising : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, 1;
     1, 0]

/-- Wang-Levin 3-loop Borromean braiding commutator `M_WL = B₁ B₂ B₁⁻¹ B₂⁻¹`. -/
def wangLevinCommutator : Matrix (Fin 2) (Fin 2) ℤ :=
  b1Ising * b2Ising * b1Ising * b2Ising

/-- Theorem 5 (Wang-Levin 3-Loop Braiding Negative Trace vs Abelian Commutation, `GIN-C20`):
In the 2D `SU(2)₂` fusion channel, `b1Ising` and `b2Ising` are involutions whose Borromean
commutator `wangLevinCommutator` equals `-I₂` with negative trace `-2`, whereas any two
diagonal (abelian) monodromy matrices commute (`diagonal d₁ * diagonal d₂ = diagonal d₂ * diagonal d₁`). -/
theorem wang_levin_ising_commutator_negative_trace_and_abelian_commutation
    (d1_vec d2_vec : Fin 2 → ℤ) :
    b1Ising * b1Ising = 1 ∧
    b2Ising * b2Ising = 1 ∧
    wangLevinCommutator = -(1 : Matrix (Fin 2) (Fin 2) ℤ) ∧
    Matrix.trace wangLevinCommutator = -2 ∧
    Matrix.diagonal d1_vec * Matrix.diagonal d2_vec =
      Matrix.diagonal d2_vec * Matrix.diagonal d1_vec := by
  refine ⟨?_, ?_, ?_, by decide, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · rw [Matrix.diagonal_mul_diagonal, Matrix.diagonal_mul_diagonal]
    congr 1
    ext i
    exact mul_comm (d1_vec i) (d2_vec i)

/-- Theorem 6 (Strict Crossed Module Peiffer and Conjugation Laws):
For any group `G`, the adjoint action `g ▹ h = g * h * g⁻¹` with boundary map `∂ = id`
satisfies both the Peiffer identity `∂(g ▹ h) = g * ∂(h) * g⁻¹` and the second crossed-module
identity `∂(h₁) ▹ h₂ = h₁ * h₂ * h₁⁻¹`. -/
theorem crossed_module_conjugation_peiffer_and_identity {G : Type*} [Group G]
    (g h h1 h2 : G) :
    (fun x : G => x) (g * h * g⁻¹) = g * (fun x : G => x) h * g⁻¹ ∧
    ((fun x : G => x) h1) * h2 * ((fun x : G => x) h1)⁻¹ = h1 * h2 * h1⁻¹ := by
  exact ⟨rfl, rfl⟩

/-- Cup-product Postnikov 3-cocycle `a(g₁, g₂, g₃) = g₁ * g₂ * g₃` on `G = ZMod 2`. -/
def postnikovCup3 (g1 g2 g3 : ZMod 2) : ZMod 2 :=
  g1 * g2 * g3

/-- Group 3-cochain coboundary `(δ₃ a)(g₁, g₂, g₃, g₄)` on `Bℤ₂`. -/
def groupCoboundary3 (a : ZMod 2 → ZMod 2 → ZMod 2 → ZMod 2)
    (g1 g2 g3 g4 : ZMod 2) : ZMod 2 :=
  a g2 g3 g4 - a (g1 + g2) g3 g4 + a g1 (g2 + g3) g4 - a g1 g2 (g3 + g4) + a g1 g2 g3

/-- Group 2-cochain coboundary `(δ₂ b)(g₁, g₂, g₃)` on `Bℤ₂`. -/
def groupCoboundary2 (b : ZMod 2 → ZMod 2 → ZMod 2)
    (g1 g2 g3 : ZMod 2) : ZMod 2 :=
  b g2 g3 - b (g1 + g2) g3 + b g1 (g2 + g3) - b g1 g2

/-- Theorem 7 (Postnikov Cup-Product 3-Cocycle Identity on `ZMod 2`):
`postnikovCup3` satisfies the 4-simplex group 3-cocycle condition
`groupCoboundary3 postnikovCup3 g₁ g₂ g₃ g₄ = 0` for all `g₁, g₂, g₃, g₄ ∈ ZMod 2`, and
takes the nontrivial value `postnikovCup3 1 1 1 = 1 ≠ 0`. -/
theorem postnikov_cup3_is_3cocycle_on_zmod2 :
    (∀ g1 g2 g3 g4 : ZMod 2, groupCoboundary3 postnikovCup3 g1 g2 g3 g4 = 0) ∧
    postnikovCup3 1 1 1 = 1 ∧
    postnikovCup3 1 1 1 ≠ 0 := by
  refine ⟨by decide, rfl, by decide⟩

/-- Cohomology pairing functional on 3-cochains `c(1,0,0) + c(0,0,1) + c(1,1,1)` over `ZMod 2`. -/
def rp3CyclePairing (c : ZMod 2 → ZMod 2 → ZMod 2 → ZMod 2) : ZMod 2 :=
  c 1 0 0 + c 0 0 1 + c 1 1 1

/-- Theorem 8 (Nontriviality of `[postnikovCup3]` in `H³(Bℤ₂, ℤ₂)`):
Every 2-coboundary `groupCoboundary2 b` vanishes on the 3-cycle pairing
`rp3CyclePairing (groupCoboundary2 b) = 0`, whereas `rp3CyclePairing postnikovCup3 = 1`,
so no 2-cochain `b : ZMod 2 → ZMod 2 → ZMod 2` satisfies `groupCoboundary2 b = postnikovCup3`. -/
theorem postnikov_cup3_not_coboundary_in_H3_zmod2 :
    (∀ b : ZMod 2 → ZMod 2 → ZMod 2, rp3CyclePairing (groupCoboundary2 b) = 0) ∧
    rp3CyclePairing postnikovCup3 = 1 ∧
    (∀ b : ZMod 2 → ZMod 2 → ZMod 2, groupCoboundary2 b ≠ postnikovCup3) := by
  refine ⟨by decide, rfl, ?_⟩
  intro b hb
  have h0 : rp3CyclePairing (groupCoboundary2 b) = 0 := by
     revert b; decide
  rw [hb] at h0
  revert h0
  decide

/-- Theorem 9 (2-Connection 3-Curvature Bianchi Consistency with Flat 1-Gauge Field):
If a flat 1-cochain `g(i, j) = φ(j) - φ(i)` on `Δ⁴` feeds into `postnikovCup3`, the induced
simplicial 3-cochain `C₃(i,j,k,l) = postnikovCup3 (g i j) (g j k) (g k l)` has vanishing
simplicial 3-coboundary `d₃ C₃(i,j,k,l,m) = 0`. -/
theorem two_connection_postnikov_3curvature_bianchi (phi : Fin 5 → ZMod 2)
    (i j k l m : Fin 5) :
    let g := d0 phi
    let C3 (u v w x : Fin 5) : ZMod 2 := postnikovCup3 (g u v) (g v w) (g w x)
    d3 C3 i j k l m = 0 := by
  intro g C3
  have h1 : g i k = g i j + g j k := by dsimp [g, d0]; abel
  have h2 : g j l = g j k + g k l := by dsimp [g, d0]; abel
  have h3 : g k m = g k l + g l m := by dsimp [g, d0]; abel
  have hcocycle := (postnikov_cup3_is_3cocycle_on_zmod2).1 (g i j) (g j k) (g k l) (g l m)
  dsimp [d3, C3]
  rw [h1, h2, h3]
  exact hcocycle

/-- Theorem 10 (1-Form Double Obstruction vs Conjugate 2-Group Postnikov Cancellation):
On `ZMod 2`, pairing `postnikovCup3` with a trivial 2-form sector leaves the class unchanged
(`postnikovCup3 g1 g2 g3 + 0 = postnikovCup3 g1 g2 g3` with value `1` at `(1,1,1)`), whereas
pairing with the conjugate Postnikov class `-postnikovCup3` cancels identically
(`postnikovCup3 g1 g2 g3 - postnikovCup3 g1 g2 g3 = 0`) and squares every `±1` sign factor to `+1`. -/
theorem one_form_double_vs_conjugate_two_group_postnikov_cancellation
    (g1 g2 g3 : ZMod 2) (n : ℕ) :
    postnikovCup3 1 1 1 + 0 = 1 ∧
    postnikovCup3 g1 g2 g3 - postnikovCup3 g1 g2 g3 = 0 ∧
    ((-1 : ℤ) ^ n) * ((-1 : ℤ) ^ n) = 1 := by
  refine ⟨rfl, sub_self _, ?_⟩
  rw [← pow_add, ← two_mul, pow_mul]
  simp

/-- Theorem 11 (Doubled-Trace Model-Change Scope Fence, `GIN-C20`/`GIN-C21` Manuscript Line 448):
Replacing a signed partition sum `Z = w₁ + w₂` by its doubled square `Z²` or by the sum of
squared weights `w₁² + w₂²` changes the target model:
(1) opposite-sign partition functions `Z₊ = 2` and `Z₋ = -2` have `Z₊ ≠ Z₋` but `Z₊² = Z₋² = 4`;
(2) for the canceling doublet `(w₁, w₂) = (1, -1)`, `w₁ + w₂ = 0` and `(w₁ + w₂)² = 0`, whereas
the weight-squared sum is `w₁² + w₂² = 2 ≠ 0` and `(w₁ + w₂)² ≠ w₁² + w₂²`. -/
theorem doubled_partition_function_changes_target_model_fence :
    ((2 : ℤ) ≠ (-2 : ℤ) ∧ (2 : ℤ) ^ 2 = (-2 : ℤ) ^ 2) ∧
    ((1 : ℤ) + (-1 : ℤ) = 0 ∧
     (1 : ℤ) ^ 2 + (-1 : ℤ) ^ 2 = 2 ∧
     ((1 : ℤ) + (-1 : ℤ)) ^ 2 ≠ (1 : ℤ) ^ 2 + (-1 : ℤ) ^ 2) := by
   decide

end CampaignFspBf2GroupSignClaim
