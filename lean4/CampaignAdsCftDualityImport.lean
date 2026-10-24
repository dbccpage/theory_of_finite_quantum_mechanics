import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.DotProduct
import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

/-!
# Campaign: ADS-CFT-DUALITY-IMPORT (TFQ-2202)

AuthorityEffect: None.

This module formalizes exact rational and finite-matrix algebraic shadows of the
imported AdS/CFT dictionary (Maldacena 1997, Gubser-Klebanov-Polyakov 1998,
Witten 1998):

1. **GKPW Scalar Mass-Dimension Relation and Breitenlohner-Freedman (BF) Bound**:
   For boundary dimension `d` and conformal dimension `Δ` over `ℚ`, the mass-squared
   expression `gkpwMassSq d Δ = Δ * (Δ - d)` is invariant under the shadow involution
   `shadowDimension d Δ = d - Δ`, satisfies Vieta's sum `Δ + (d - Δ) = d` and product
   `Δ * (d - Δ) = -gkpwMassSq d Δ`, completes the square as
   `(2 * Δ - d)^2 = d^2 + 4 * gkpwMassSq d Δ`, and satisfies the Breitenlohner-Freedman
   lower bound `-(d^2) / 4 ≤ gkpwMassSq d Δ` with double root `Δ = d / 2` at saturation.
   For any `mSq < -(d^2) / 4`, no rational `Δ` solves `Δ * (Δ - d) = mSq`.

2. **'t Hooft Large-N Ribbon-Graph Genus Scaling and U(N)/SU(N) Dimension Split**:
   With `'t Hooft coupling` `λ = gYM_sq * N` and ribbon Euler characteristic
   `χ(V, E, F) = V - E + F = 2 - 2g`, the double-line weight `gYM_sq^(E - V) * N^F`
   satisfies `ribbonDoubleLineWeight gYM_sq N V E F * N^(E - V) = λ^(E - V) * N^F`,
   suppressing the genus-1 torus contraction `(V=2, E=3, F=1)` relative to the
   genus-0 planar dipole `(V=2, E=3, F=3)` by the exact factor `N^2`.

3. **Finite Isometric Bulk-to-Boundary Pullback/Pushforward Dictionary and Fence**:
   For an isometric encoding `V : Matrix B b ℚ` (`V^T * V = 1`), the pushforward
   `ι_V(O_bulk) = V * O_bulk * V^T` and pullback `π_V(O_bdry) = V^T * O_bdry * V`
   satisfy `π_V(ι_V(O_bulk)) = O_bulk`, `ι_V(A) * ι_V(B) = ι_V(A * B)`, and exact
   quadratic expectation matching `<V ψ, O_bdry (V ψ)> = <ψ, π_V(O_bdry) ψ>`.
   However, for `b = 1 < B = 2`, `V * V^T ≠ 1`, a nonzero boundary operator
   `boundaryAnnihilator12` pulls back to `0`, and `bulkPushforward` is not surjective.

This module does NOT construct continuum quantum field theory, continuum gravity on
asymptotically anti-de Sitter space, or the large-N limit. The node status stays
`IMPORTED_ASSUMPTION`.
-/

namespace CampaignAdsCftDualityImport

open Matrix

/-! ## 1. GKPW Scalar Mass-Dimension Relation and Breitenlohner-Freedman Bound -/

/-- The GKPW scalar mass-squared expression `(m R)^2 = Δ (Δ - d)` over `ℚ`. -/
def gkpwMassSq (d Δ : ℚ) : ℚ :=
  Δ * (Δ - d)

/-- The shadow conformal dimension `d - Δ` paired with `Δ` by the GKPW quadratic. -/
def shadowDimension (d Δ : ℚ) : ℚ :=
  d - Δ

/-- The discriminant `d^2 + 4 * mSq` of the GKPW quadratic `Δ^2 - d Δ - mSq = 0`. -/
def gkpwDiscriminant (d mSq : ℚ) : ℚ :=
  d ^ 2 + 4 * mSq

/-- The Breitenlohner-Freedman stability lower bound `-(d^2) / 4` on `(m R)^2`. -/
def bfBound (d : ℚ) : ℚ :=
  -(d ^ 2) / 4

/-- The upper root `Δ_+ = (d + s) / 2` when `s^2 = d^2 + 4 * mSq`. -/
def gkpwRootPlus (d s : ℚ) : ℚ :=
  (d + s) / 2

/-- The lower root `Δ_- = (d - s) / 2` when `s^2 = d^2 + 4 * mSq`. -/
def gkpwRootMinus (d s : ℚ) : ℚ :=
  (d - s) / 2

/-- The shadow-dimension map `Δ ↦ d - Δ` is an involution. -/
theorem shadowDimension_involutive (d Δ : ℚ) :
    shadowDimension d (shadowDimension d Δ) = Δ := by
  dsimp [shadowDimension]
  ring

/-- A conformal dimension and its shadow sum to the boundary dimension `d`. -/
theorem shadowDimension_sum (d Δ : ℚ) :
    Δ + shadowDimension d Δ = d := by
  dsimp [shadowDimension]
  ring

/-- A conformal dimension `Δ` and its shadow `d - Δ` have identical GKPW `(m R)^2`. -/
theorem gkpwMassSq_shadow_eq (d Δ : ℚ) :
    gkpwMassSq d (shadowDimension d Δ) = gkpwMassSq d Δ := by
  dsimp [gkpwMassSq, shadowDimension]
  ring

/-- Vieta's product relation: `Δ * (d - Δ) = - Δ (Δ - d)`. -/
theorem gkpw_vieta_product (d Δ : ℚ) :
    Δ * shadowDimension d Δ = -gkpwMassSq d Δ := by
  dsimp [gkpwMassSq, shadowDimension]
  ring

/-- Completing the square in the GKPW mass-dimension relation:
`(2 Δ - d)^2 = d^2 + 4 Δ (Δ - d)`. -/
theorem gkpw_completed_square (d Δ : ℚ) :
    (2 * Δ - d) ^ 2 = gkpwDiscriminant d (gkpwMassSq d Δ) := by
  dsimp [gkpwDiscriminant, gkpwMassSq]
  ring

/-- Whenever `s^2 = d^2 + 4 mSq`, both `gkpwRootPlus d s` and `gkpwRootMinus d s`
solve `gkpwMassSq d Δ = mSq`, sum to `d`, and differ by `s`. -/
theorem gkpw_roots_from_square_discriminant (d mSq s : ℚ)
    (hs : s ^ 2 = gkpwDiscriminant d mSq) :
    gkpwMassSq d (gkpwRootPlus d s) = mSq ∧
      gkpwMassSq d (gkpwRootMinus d s) = mSq ∧
      gkpwRootPlus d s + gkpwRootMinus d s = d ∧
      gkpwRootPlus d s - gkpwRootMinus d s = s := by
  dsimp [gkpwMassSq, gkpwRootPlus, gkpwRootMinus, gkpwDiscriminant] at *
  refine ⟨?_, ?_, by ring, by ring⟩
  · calc
      (d + s) / 2 * ((d + s) / 2 - d) = (s ^ 2 - d ^ 2) / 4 := by ring
      _ = (d ^ 2 + 4 * mSq - d ^ 2) / 4 := by rw [hs]
      _ = mSq := by ring
  · calc
      (d - s) / 2 * ((d - s) / 2 - d) = (s ^ 2 - d ^ 2) / 4 := by ring
      _ = (d ^ 2 + 4 * mSq - d ^ 2) / 4 := by rw [hs]
      _ = mSq := by ring

/-- The Breitenlohner-Freedman bound `-(d^2)/4 ≤ mSq` holds if and only if
the GKPW discriminant `d^2 + 4 mSq` is nonnegative. -/
theorem bf_bound_iff_discriminant_nonneg (d mSq : ℚ) :
    bfBound d ≤ mSq ↔ 0 ≤ gkpwDiscriminant d mSq := by
  dsimp [bfBound, gkpwDiscriminant]
  constructor <;> intro h <;> linarith

/-- At the Breitenlohner-Freedman bound `mSq = -(d^2)/4`, the discriminant vanishes
and the two roots coalesce at `Δ_+ = Δ_- = d / 2`. -/
theorem bf_saturation_double_root (d : ℚ) :
    gkpwDiscriminant d (bfBound d) = 0 ∧
      gkpwRootPlus d 0 = d / 2 ∧
      gkpwRootMinus d 0 = d / 2 ∧
      gkpwMassSq d (d / 2) = bfBound d := by
  dsimp [gkpwDiscriminant, bfBound, gkpwRootPlus, gkpwRootMinus, gkpwMassSq]
  refine ⟨by ring, by ring, by ring, by ring⟩

/-- Every rational dimension `Δ` satisfies the Breitenlohner-Freedman bound
`-(d^2)/4 ≤ Δ (Δ - d)`. -/
theorem gkpwMassSq_ge_bfBound (d Δ : ℚ) :
    bfBound d ≤ gkpwMassSq d Δ := by
  have hsq : 0 ≤ (Δ - d / 2) ^ 2 := sq_nonneg (Δ - d / 2)
  have hid : gkpwMassSq d Δ - bfBound d = (Δ - d / 2) ^ 2 := by
    dsimp [gkpwMassSq, bfBound]
    ring
  linarith

/-- Strictly below the Breitenlohner-Freedman bound (`mSq < -(d^2)/4`), no rational
dimension `Δ` solves `Δ (Δ - d) = mSq`. -/
theorem no_rational_root_below_bf_bound (d mSq Δ : ℚ) (h : mSq < bfBound d) :
    gkpwMassSq d Δ ≠ mSq := by
  have hge := gkpwMassSq_ge_bfBound d Δ
  linarith

/-- Concrete GKPW mass-dimension points in `d = 4` (`AdS_5/CFT_4`) and `d = 2` (`AdS_3/CFT_2`),
together with the non-square discriminant `D = 20` at `(d = 4, mSq = 1)`. -/
theorem recorded_ads5_and_ads3_gkpw_points :
    -- d = 4, mSq = 0 (massless scalar / marginal operator Δ_+ = 4, Δ_- = 0)
    gkpwDiscriminant 4 0 = 16 ∧
      gkpwRootPlus 4 4 = 4 ∧ gkpwRootMinus 4 4 = 0 ∧
      gkpwMassSq 4 4 = 0 ∧ gkpwMassSq 4 0 = 0 ∧
      -- d = 4, mSq = -4 (BF saturation: Δ_+ = Δ_- = 2)
      bfBound 4 = -4 ∧ gkpwDiscriminant 4 (-4) = 0 ∧ gkpwMassSq 4 2 = -4 ∧
      -- d = 4, mSq = -3 (conformal scalar on AdS_5: Δ_+ = 3, Δ_- = 1)
      gkpwDiscriminant 4 (-3) = 4 ∧
      gkpwRootPlus 4 2 = 3 ∧ gkpwRootMinus 4 2 = 1 ∧
      gkpwMassSq 4 3 = -3 ∧ gkpwMassSq 4 1 = -3 ∧
      -- d = 4, mSq = 5 (Δ_+ = 5, Δ_- = -1)
      gkpwDiscriminant 4 5 = 36 ∧
      gkpwRootPlus 4 6 = 5 ∧ gkpwRootMinus 4 6 = -1 ∧
      gkpwMassSq 4 5 = 5 ∧ gkpwMassSq 4 (-1) = 5 ∧
      -- d = 2, mSq = -1 (AdS_3 BF saturation: Δ_+ = Δ_- = 1)
      bfBound 2 = -1 ∧ gkpwDiscriminant 2 (-1) = 0 ∧ gkpwMassSq 2 1 = -1 ∧
      -- d = 4, mSq = 1 (discriminant 20 lies strictly between 4^2 and 5^2)
      gkpwDiscriminant 4 1 = 20 ∧ (4 : ℚ) ^ 2 < gkpwDiscriminant 4 1 ∧
      gkpwDiscriminant 4 1 < (5 : ℚ) ^ 2 := by
  dsimp [gkpwDiscriminant, gkpwRootPlus, gkpwRootMinus, gkpwMassSq, bfBound]
  norm_num

/-! ## 2. 't Hooft Large-N Ribbon-Graph Genus Scaling and U(N)/SU(N) Split -/

/-- The 't Hooft coupling `λ = g_YM^2 * N`. -/
def tHooftCoupling (gYM_sq N : ℚ) : ℚ :=
  gYM_sq * N

/-- The Euler characteristic `χ = V - E + F` of a ribbon graph with `V` vertices,
`E` propagators, and `F` index loops. -/
def ribbonEulerChar (V E F : ℤ) : ℤ :=
  V - E + F

/-- The Euler characteristic `2 - 2g` of a closed oriented surface of genus `g`. -/
def closedSurfaceEulerChar (g : ℤ) : ℤ :=
  2 - 2 * g

/-- The unnormalized double-line ribbon weight `(g_YM^2)^(E - V) * N^F` for `V ≤ E`. -/
def ribbonDoubleLineWeight (gYM_sq N : ℚ) (V E F : ℕ) : ℚ :=
  gYM_sq ^ (E - V) * N ^ F

/-- Exact polynomial form of the 't Hooft large-N factorization:
`(g_YM^2)^(E - V) * N^F * N^(E - V) = (g_YM^2 * N)^(E - V) * N^F`. -/
theorem thooft_factorization (gYM_sq N : ℚ) (V E F : ℕ) :
    ribbonDoubleLineWeight gYM_sq N V E F * N ^ (E - V) =
      (tHooftCoupling gYM_sq N) ^ (E - V) * N ^ F := by
  dsimp [ribbonDoubleLineWeight, tHooftCoupling]
  rw [mul_pow]
  ring

/-- Planar (`g = 0`, `V = 2, E = 3, F = 3`) versus genus-1 torus (`g = 1`, `V = 2, E = 3, F = 1`)
vacuum ribbon graphs: both have excess `E - V = 1`, Euler characteristics `2` and `0`,
and the planar weight exceeds the torus weight by the exact factor `N^2`. -/
theorem thooft_planar_vs_torus_suppression (gYM_sq N : ℚ) :
    ribbonEulerChar 2 3 3 = closedSurfaceEulerChar 0 ∧
      ribbonEulerChar 2 3 1 = closedSurfaceEulerChar 1 ∧
      ribbonDoubleLineWeight gYM_sq N 2 3 3 = (tHooftCoupling gYM_sq N) * N ^ 2 ∧
      ribbonDoubleLineWeight gYM_sq N 2 3 1 * N ^ 2 =
        ribbonDoubleLineWeight gYM_sq N 2 3 3 := by
  dsimp [ribbonEulerChar, closedSurfaceEulerChar, ribbonDoubleLineWeight, tHooftCoupling]
  refine ⟨by norm_num, by norm_num, by ring, by ring⟩

/-- Adjoint dimension split `N^2 = (N^2 - 1) + 1` between `U(N)` and `SU(N) ⊕ u(1)`,
together with concrete values at `N = 3` (`g_YM^2 = 1/3, λ = 1`) and `N = 4`. -/
theorem recorded_thooft_and_gauge_counts (N : ℚ) :
    N ^ 2 = (N ^ 2 - 1) + 1 ∧
      tHooftCoupling (1 / 3) 3 = 1 ∧
      ribbonDoubleLineWeight (1 / 3) 3 2 3 3 = 9 ∧
      ribbonDoubleLineWeight (1 / 3) 3 2 3 1 = 1 ∧
      ((3 : ℚ) ^ 2 - 1 = 8) ∧ ((4 : ℚ) ^ 2 - 1 = 15) := by
  dsimp [tHooftCoupling, ribbonDoubleLineWeight]
  refine ⟨by ring, by norm_num, by norm_num, by norm_num, by norm_num, by norm_num⟩

/-! ## 3. Finite Isometric Bulk-to-Boundary Dictionary and Non-Surjectivity Fence -/

/-- Pushforward `ι_V(O_bulk) = V O_bulk V^T` of a bulk operator to the boundary. -/
def bulkPushforward {b B : Type*} [Fintype b] [Fintype B] (V : Matrix B b ℚ)
    (O_bulk : Matrix b b ℚ) : Matrix B B ℚ :=
  V * O_bulk * V.transpose

/-- Pullback `π_V(O_bdry) = V^T O_bdry V` of a boundary operator to the bulk code space. -/
def boundaryPullback {b B : Type*} [Fintype b] [Fintype B] (V : Matrix B b ℚ)
    (O_bdry : Matrix B B ℚ) : Matrix b b ℚ :=
  V.transpose * O_bdry * V

/-- Quadratic expectation value `<ψ, O ψ>` of a rational matrix `O` in state vector `ψ`. -/
def quadExpectation {n : Type*} [Fintype n] (O : Matrix n n ℚ) (ψ : n → ℚ) : ℚ :=
  dotProduct ψ (O.mulVec ψ)

/-- For any bulk-to-boundary isometry `V` (`V^T V = 1`), pulling back the pushed-forward
bulk operator recovers `O_bulk` identically (`π_V(ι_V(O_bulk)) = O_bulk`). -/
theorem pullback_pushforward_id {b B : Type*} [Fintype b] [Fintype B] [DecidableEq b]
    (V : Matrix B b ℚ) (hV : V.transpose * V = 1) (O_bulk : Matrix b b ℚ) :
    boundaryPullback V (bulkPushforward V O_bulk) = O_bulk := by
  dsimp [boundaryPullback, bulkPushforward]
  calc
    V.transpose * (V * O_bulk * V.transpose) * V
        = (V.transpose * V) * O_bulk * (V.transpose * V) := by
          simp only [Matrix.mul_assoc]
    _ = 1 * O_bulk * 1 := by rw [hV]
    _ = O_bulk := by simp

/-- For any bulk-to-boundary isometry `V` (`V^T V = 1`), `bulkPushforward V` is a
multiplicative homomorphism on bulk operators (`ι_V(A) * ι_V(B) = ι_V(A * B)`). -/
theorem pushforward_mul_of_isometry {b B : Type*} [Fintype b] [Fintype B] [DecidableEq b]
    (V : Matrix B b ℚ) (hV : V.transpose * V = 1) (A C : Matrix b b ℚ) :
    bulkPushforward V A * bulkPushforward V C = bulkPushforward V (A * C) := by
  dsimp [bulkPushforward]
  calc
    (V * A * V.transpose) * (V * C * V.transpose)
        = V * A * (V.transpose * V) * (C * V.transpose) := by
          simp only [Matrix.mul_assoc]
    _ = V * A * (1 : Matrix b b ℚ) * (C * V.transpose) := by rw [hV]
    _ = V * (A * C) * V.transpose := by simp [Matrix.mul_assoc]

/-- Exact correlator dictionary on encoded states: for any encoding matrix `V`,
boundary operator `O_bdry`, and bulk vector `ψ`, the boundary expectation in `V ψ`
equals the bulk expectation of the pullback `π_V(O_bdry)` in `ψ`. -/
theorem correlator_dictionary_pullback {b B : Type*} [Fintype b] [Fintype B]
    (V : Matrix B b ℚ) (O_bdry : Matrix B B ℚ) (ψ : b → ℚ) :
    quadExpectation O_bdry (V.mulVec ψ) =
      quadExpectation (boundaryPullback V O_bdry) ψ := by
  dsimp [quadExpectation, boundaryPullback]
  symm
  calc
    dotProduct ψ ((V.transpose * O_bdry * V).mulVec ψ)
        = dotProduct ψ (V.transpose.mulVec (O_bdry.mulVec (V.mulVec ψ))) := by
          rw [← mulVec_mulVec, ← mulVec_mulVec]
    _ = dotProduct (vecMul ψ V.transpose) (O_bdry.mulVec (V.mulVec ψ)) := by
          rw [dotProduct_mulVec]
    _ = dotProduct (V.mulVec ψ) (O_bdry.mulVec (V.mulVec ψ)) := by
          rw [vecMul_transpose]

/-- Combining `correlator_dictionary_pullback` with `pullback_pushforward_id`: when
`V^T V = 1`, the boundary expectation of `ι_V(O_bulk)` in `V ψ` equals `<ψ, O_bulk ψ>`. -/
theorem correlator_dictionary_match {b B : Type*} [Fintype b] [Fintype B] [DecidableEq b]
    (V : Matrix B b ℚ) (hV : V.transpose * V = 1) (O_bulk : Matrix b b ℚ) (ψ : b → ℚ) :
    quadExpectation (bulkPushforward V O_bulk) (V.mulVec ψ) =
      quadExpectation O_bulk ψ := by
  rw [correlator_dictionary_pullback, pullback_pushforward_id V hV O_bulk]

/-- Explicit 1-to-2 isometric code embedding `V = [[1], [0]] : ℚ^1 → ℚ^2`. -/
def codeIsometry12 : Matrix (Fin 2) (Fin 1) ℚ :=
  fun i _ => if i = 0 then 1 else 0

/-- Nonzero boundary operator `O_perp = [[0, 0], [0, 1]]` supported on the orthogonal
complement of the image of `codeIsometry12`. -/
def boundaryAnnihilator12 : Matrix (Fin 2) (Fin 2) ℚ :=
  fun i j => if i = 1 ∧ j = 1 then 1 else 0

/-- `codeIsometry12` is an exact isometry (`V^T V = 1`). -/
theorem codeIsometry12_is_isometry :
    codeIsometry12.transpose * codeIsometry12 = 1 := by
  ext i j
  fin_cases i
  fin_cases j
  simp [codeIsometry12, Matrix.mul_apply]

/-- The code-subspace projector `V V^T = [[1, 0], [0, 0]]` is not the 2×2 identity. -/
theorem codeIsometry12_projector_ne_one :
    codeIsometry12 * codeIsometry12.transpose ≠ 1 := by
  intro h
  have h11 : (codeIsometry12 * codeIsometry12.transpose) 1 1 = (1 : Matrix (Fin 2) (Fin 2) ℚ) 1 1 :=
    congrFun (congrFun h 1) 1
  revert h11
  simp [codeIsometry12, Matrix.mul_apply]

/-- Non-equivalence fence: `boundaryAnnihilator12` is a nonzero boundary observable whose
bulk pullback vanishes (`π_V(O_perp) = 0`), and `bulkPushforward codeIsometry12` is not
surjective onto `Matrix (Fin 2) (Fin 2) ℚ`. -/
theorem boundary_annihilator_obstruction :
    boundaryAnnihilator12 ≠ 0 ∧
      boundaryPullback codeIsometry12 boundaryAnnihilator12 = 0 ∧
      ¬ Function.Surjective (bulkPushforward codeIsometry12) := by
  refine ⟨?_, ?_, ?_⟩
  · intro h0
    have h11 : boundaryAnnihilator12 1 1 = (0 : Matrix (Fin 2) (Fin 2) ℚ) 1 1 :=
      congrFun (congrFun h0 1) 1
    revert h11
    simp [boundaryAnnihilator12]
  · ext i j
    fin_cases i
    fin_cases j
    simp [boundaryPullback, codeIsometry12, boundaryAnnihilator12, Matrix.mul_apply]
  · intro hsurj
    rcases hsurj boundaryAnnihilator12 with ⟨O_bulk, hO⟩
    have h11 : (bulkPushforward codeIsometry12 O_bulk) 1 1 = boundaryAnnihilator12 1 1 :=
      congrFun (congrFun hO 1) 1
    revert h11
    simp [bulkPushforward, codeIsometry12, boundaryAnnihilator12, Matrix.mul_apply]

#print axioms shadowDimension_involutive
#print axioms shadowDimension_sum
#print axioms gkpwMassSq_shadow_eq
#print axioms gkpw_vieta_product
#print axioms gkpw_completed_square
#print axioms gkpw_roots_from_square_discriminant
#print axioms bf_bound_iff_discriminant_nonneg
#print axioms bf_saturation_double_root
#print axioms gkpwMassSq_ge_bfBound
#print axioms no_rational_root_below_bf_bound
#print axioms recorded_ads5_and_ads3_gkpw_points
#print axioms thooft_factorization
#print axioms thooft_planar_vs_torus_suppression
#print axioms recorded_thooft_and_gauge_counts
#print axioms pullback_pushforward_id
#print axioms pushforward_mul_of_isometry
#print axioms correlator_dictionary_pullback
#print axioms correlator_dictionary_match
#print axioms codeIsometry12_is_isometry
#print axioms codeIsometry12_projector_ne_one
#print axioms boundary_annihilator_obstruction

end CampaignAdsCftDualityImport
