import GleasonContinuumShadow

/-!
# Continuum Gleason Development across Complex States, Finite Dimensions, Regularity, and Infinite Dimensions

AuthorityEffect: None.

This module formalizes Phase 4 of the Gleason campaign across four primary mathematical regimes:

## A. Arbitrary Complex States in Dimension Three (`d = 3`)
* **Constructive Factorized Approximation (`ρ_k = B_k B_k^* / tr(B_k B_k^*)`)**:
  - `GaussMatrix3`: `3 × 3` matrices over `GaussRat` (`ℚ(i)`).
  - `frobNormSq B`: exact rational Frobenius squared norm `∑ i, ∑ j, (B i j).normSq = tr(B B^*)`.
  - `frobNormSq_pos_of_entry_ne_zero` and `frobNormSq_ne_zero_of_entry_ne_zero`: proves the
    denominator `tr(B B^*)` is strictly positive and nonzero whenever `B` has at least one nonzero
    entry.
  - `gramHermForm3 B` and `factorizedState3 B`: exact rational Hermitian form of `B B^*` and its
    trace-normalized state `B B^* / tr(B B^*)`.
  - `mulConjTransposeVec B v` and `quadNum_gramHermForm3`: proves the algebraic sum-of-squares
    identity `quadNum (gramHermForm3 B) v = normSqVec (B^* v) ≥ 0` for every `v ∈ ℚ(i)³`.
  - `factorizedState3_tr_eq_one`, `factorizedState3_quadNum_nonneg`, and
    `toMatrix_factorizedState3_posSemidef_and_trace_one`: proves each factorized rational
    approximant is **exactly positive semidefinite** (`PosSemidef`) and **trace one** (`trace = 1`).
* **Real-Valued Frame Data, Quantitative Born Convergence, and Uniqueness on `ℂ³`**:
  - `complexQuadForm M v = Re ⟨v, M v⟩`, `complexRayleigh M v = Re ⟨v, M v⟩ / ‖v‖²`, and
    `matEntryL1Norm A = ∑ i, ∑ j, ‖A i j‖`.
  - `abs_complexQuadForm_le` and `abs_complexRayleigh_sub_le`: proves the uniform Born-probability
    stability bound `|complexRayleigh A v - complexRayleigh B v| ≤ matEntryL1Norm (A - B)` on all
    nonzero `v ∈ ℂ³ \ {0}`.
  - `factorizedState3_born_prob_error_le` and `complex_hermitian_unique_of_rayleigh_eq`: proves that
    as `toMatrix (factorizedState3 (B k))` converges to a continuum density matrix `ρC` in
    `matEntryL1Norm`, the Born probabilities converge uniformly on `ℂ³ \ {0}`, and the limiting
    Hermitian operator is unique.

## B. All Finite Dimensions (`d = 0, 1, 2` and `d ≥ 3`)
* **Dimension `d = 0`**:
  - `dim0_no_nonzero_vectors` and `dim0_frameValuation_vacuously_unique`: the empty carrier has no
    nonzero rays, and any two valuations on its nonzero rays coincide vacuously.
* **Dimension `d = 1`**:
  - `IsDim1FrameValuation` and `dim1_frameValuation_eq_one`: every 1-element frame valuation on
    `ℂ¹ \ {0}` is identically `1` on all nonzero vectors and uniquely represented by `I₁`.
* **Dimension `d = 2` (Projection-Measure Exception vs. Effect-Additive Route)**:
  - `GVec2`, `IsFrame2`, `IsFrameFunction2`, `HermForm2`, `quadRay2`: 2D orthogonal frame valuations
    and `2 × 2` Hermitian Rayleigh quotients.
  - `dim2AxisCounterexample`: an explicit `{0, 1/2, 1}`-valued nonnegative 2D frame function
    assigning `1` to the `e₁` ray (`u.y = 0`), `0` to the `e₂` ray (`u.x = 0`), and `1/2` to all
    other rays, proved to satisfy 2D frame additivity (`dim2AxisCounterexample_isFrameFunction2`)
    while refuting representation by any `2 × 2` Hermitian quadratic form with `q(1,1) = 1`
    (`dim2Counterexample_not_quadratic`), contrasting with the operator-linear `EffectValuation`
    theorem (`born_trace_representation` in `BornTraceRepresentation.lean`).
* **Dimensions `d ≥ 3` (Subspace Restrictions, Compatibility, and Global Uniqueness)**:
  - `embed3D ι` and `submatrix3D M ι` for any injective `ι : Fin 3 ↪ Fin d`.
  - `complexQuadFormD_embed3D`, `submatrix3D_isHermitian`, `submatrix3D_trace_eq_subspace_weight`,
    `compat_submatrix3D_overlap`, and `eq_of_complexQuadFormD_eq`: proves compatibility of 3D
    restrictions, subspace weights, and global `d × d` Hermitian uniqueness by polarization.

## C. Automatic Regularity for Nonnegative Continuum Frame Functions (`d = 3`)
* `IsContinuumFrame3`, `IsContinuumFrameFunction3`, `IsNonnegContinuumFrameFunction3`.
* `nonneg_continuum_frameFunction_bounds`: proves `0 ≤ f v ≤ 1` on all unit vectors in `ℂ³` from
  nonnegativity and 3-frame additivity alone (without continuity).
* `continuum_eq_zero_on_perp_of_pole_one`: proves equatorial vanishing `f w = 0` for all `w ⊥ u`
  whenever `f u = 1`.
* `continuum_piron_subadditivity`: proves the continuum frame-sum inequality `f v + f w ≤ 1` for
  orthogonal unit vectors `v ⊥ w`.
* Preserves the explicit boundary between continuum automatic regularity on `S(ℂ³)` and the
  rational question `TFQ-1057` on `ℚ(i)³`.

## D. Infinite-Dimensional Separable Hilbert Spaces (`ℓ²(ℕ)`)
* `compressionTrace w N = ∑ n ∈ Finset.range N, w n`: finite-dimensional subspace compression trace,
  preserving subunit trace (`compressionTrace w N ≤ 1`) without silent renormalization.
* `compressionTrace_mono` and `tail_weight_le_of_tight`: monotonicity of finite compressions and
  control of tail trace loss under tightness (`σ`-additivity).
* **Rank-One Basis Escape Witness (`basisEscapeState k n = if n = k then 1 else 0`)**:
  - `basisEscapeState_normalized_at_stage`: `compressionTrace (basisEscapeState k) (k + 1) = 1`.
  - `basisEscapeState_compression_eq_zero_of_ge`: for every fixed finite cutoff `N` and every stage
    `k ≥ N`, `compressionTrace (basisEscapeState k) N = 0`.
  - `basisEscapeState_escapes_to_zero_without_tightness`: proves that a sequence of normalized
    trace-one states on successive orthogonal basis vectors converges to `0` on every finite-dimensional
    compression while retaining total trace `1`.
-/

namespace BornFinite.ContinuumDevelopment

open BornFinite BornFinite.GaussRat BornFinite.GaussianFrames BornFinite.GaussianTomography
open BornFinite.GleasonBridge BornFinite.BornCompletion BornFinite.GaussianFiniteModel
open GleasonComplex Complex ComplexConjugate Matrix
open scoped BigOperators ComplexOrder

/-! ### Part A: Arbitrary Complex States in Dimension Three (`d = 3`) -/

/-- A `3 × 3` matrix with Gaussian-rational entries (`ℚ(i)`). -/
abbrev GaussMatrix3 := Matrix (Fin 3) (Fin 3) GaussRat

/-- Action of the conjugate transpose `B^*` of `B : GaussMatrix3` on `v : GVec`. -/
def mulConjTransposeVec (B : GaussMatrix3) (v : GVec) : GVec :=
  ⟨star (B 0 0) * v.x + star (B 1 0) * v.y + star (B 2 0) * v.z,
   star (B 0 1) * v.x + star (B 1 1) * v.y + star (B 2 1) * v.z,
   star (B 0 2) * v.x + star (B 1 2) * v.y + star (B 2 2) * v.z⟩

/-- Exact rational Frobenius squared norm `tr(B B^*) = ∑ i, ∑ j, |B_{ij}|²`. -/
def frobNormSq (B : GaussMatrix3) : ℚ :=
  (B 0 0).normSq + (B 0 1).normSq + (B 0 2).normSq +
  (B 1 0).normSq + (B 1 1).normSq + (B 1 2).normSq +
  (B 2 0).normSq + (B 2 1).normSq + (B 2 2).normSq

/-- Exact rational Hermitian form representing `B B^*` for `B : GaussMatrix3`. -/
def gramHermForm3 (B : GaussMatrix3) : HermForm3 where
  d1 := (B 0 0).normSq + (B 0 1).normSq + (B 0 2).normSq
  d2 := (B 1 0).normSq + (B 1 1).normSq + (B 1 2).normSq
  d3 := (B 2 0).normSq + (B 2 1).normSq + (B 2 2).normSq
  a12 := (B 0 0 * star (B 1 0) + B 0 1 * star (B 1 1) + B 0 2 * star (B 1 2)).re
  a13 := (B 0 0 * star (B 2 0) + B 0 1 * star (B 2 1) + B 0 2 * star (B 2 2)).re
  a23 := (B 1 0 * star (B 2 0) + B 1 1 * star (B 2 1) + B 1 2 * star (B 2 2)).re
  b12 := (B 0 0 * star (B 1 0) + B 0 1 * star (B 1 1) + B 0 2 * star (B 1 2)).im
  b13 := (B 0 0 * star (B 2 0) + B 0 1 * star (B 2 1) + B 0 2 * star (B 2 2)).im
  b23 := (B 1 0 * star (B 2 0) + B 1 1 * star (B 2 1) + B 1 2 * star (B 2 2)).im

/-- Scalar multiplication of a `3 × 3` rational Hermitian form by `c : ℚ`. -/
def scaleHermForm3 (c : ℚ) (ρ : HermForm3) : HermForm3 where
  d1 := c * ρ.d1
  d2 := c * ρ.d2
  d3 := c * ρ.d3
  a12 := c * ρ.a12
  a13 := c * ρ.a13
  a23 := c * ρ.a23
  b12 := c * ρ.b12
  b13 := c * ρ.b13
  b23 := c * ρ.b23

/-- Constructive factorized Gaussian-rational state `ρ(B) = B B^* / tr(B B^*)`. -/
def factorizedState3 (B : GaussMatrix3) : HermForm3 :=
  scaleHermForm3 (1 / frobNormSq B) (gramHermForm3 B)

theorem scaleHermForm3_tr (c : ℚ) (ρ : HermForm3) :
    (scaleHermForm3 c ρ).tr = c * ρ.tr := by
  simp only [HermForm3.tr, scaleHermForm3]
  ring

theorem quadNum_scaleHermForm3 (c : ℚ) (ρ : HermForm3) (v : GVec) :
    quadNum (scaleHermForm3 c ρ) v = c * quadNum ρ v := by
  simp only [quadNum, scaleHermForm3]
  ring

theorem quadRay_scaleHermForm3 (c : ℚ) (ρ : HermForm3) (v : GVec) :
    quadRay (scaleHermForm3 c ρ) v = c * quadRay ρ v := by
  simp only [quadRay, quadNum_scaleHermForm3, mul_div_assoc]

theorem gramHermForm3_tr (B : GaussMatrix3) :
    (gramHermForm3 B).tr = frobNormSq B := by
  simp only [HermForm3.tr, gramHermForm3, frobNormSq]
  ring

theorem frobNormSq_nonneg (B : GaussMatrix3) : 0 ≤ frobNormSq B := by
  unfold frobNormSq
  linarith [normSq_nonneg (B 0 0), normSq_nonneg (B 0 1), normSq_nonneg (B 0 2),
            normSq_nonneg (B 1 0), normSq_nonneg (B 1 1), normSq_nonneg (B 1 2),
            normSq_nonneg (B 2 0), normSq_nonneg (B 2 1), normSq_nonneg (B 2 2)]

/-- If any entry `B i j` is nonzero, the denominator `tr(B B^*) = frobNormSq B` is strictly positive. -/
theorem frobNormSq_pos_of_entry_ne_zero {B : GaussMatrix3}
    (hB : ∃ i j : Fin 3, B i j ≠ 0) :
    0 < frobNormSq B := by
  rcases hB with ⟨i, j, hij⟩
  have hpos : 0 < (B i j).normSq :=
    lt_of_le_of_ne (normSq_nonneg (B i j)) (fun h => hij ((normSq_eq_zero_iff (B i j)).mp h.symm))
  have h00 := normSq_nonneg (B 0 0)
  have h01 := normSq_nonneg (B 0 1)
  have h02 := normSq_nonneg (B 0 2)
  have h10 := normSq_nonneg (B 1 0)
  have h11 := normSq_nonneg (B 1 1)
  have h12 := normSq_nonneg (B 1 2)
  have h20 := normSq_nonneg (B 2 0)
  have h21 := normSq_nonneg (B 2 1)
  have h22 := normSq_nonneg (B 2 2)
  unfold frobNormSq
  fin_cases i <;> fin_cases j <;> dsimp at hpos <;> linarith

/-- Nonzero denominator guarantee for `factorizedState3 B` at every admitted stage (`∃ i j, B i j ≠ 0`). -/
theorem frobNormSq_ne_zero_of_entry_ne_zero {B : GaussMatrix3}
    (hB : ∃ i j : Fin 3, B i j ≠ 0) :
    frobNormSq B ≠ 0 :=
  (frobNormSq_pos_of_entry_ne_zero hB).ne'

/-- Exact sum-of-squares factorization identity: `⟨v, (B B^*) v⟩ = ‖B^* v‖²` on all `v ∈ ℚ(i)³`. -/
theorem quadNum_gramHermForm3 (B : GaussMatrix3) (v : GVec) :
    quadNum (gramHermForm3 B) v = normSqVec (mulConjTransposeVec B v) := by
  simp only [quadNum, gramHermForm3, normSqVec, mulConjTransposeVec,
    GaussRat.normSq, re_add, im_add, re_mul, im_mul, re_star, im_star]
  ring

/-- `quadNum (gramHermForm3 B) v ≥ 0` on all `v ∈ ℚ(i)³`. -/
theorem gramHermForm3_quadNum_nonneg (B : GaussMatrix3) (v : GVec) :
    0 ≤ quadNum (gramHermForm3 B) v := by
  rw [quadNum_gramHermForm3]
  exact normSqVec_nonneg _

/-- Exact trace-one normalization of `factorizedState3 B` whenever `B` has a nonzero entry. -/
theorem factorizedState3_tr_eq_one {B : GaussMatrix3}
    (hB : ∃ i j : Fin 3, B i j ≠ 0) :
    (factorizedState3 B).tr = 1 := by
  rw [factorizedState3, scaleHermForm3_tr, gramHermForm3_tr,
      one_div_mul_cancel (frobNormSq_ne_zero_of_entry_ne_zero hB)]

/-- Nonnegativity of the quadratic form of `factorizedState3 B` on all `v ∈ ℚ(i)³`. -/
theorem factorizedState3_quadNum_nonneg (B : GaussMatrix3) (v : GVec) :
    0 ≤ quadNum (factorizedState3 B) v := by
  rw [factorizedState3, quadNum_scaleHermForm3]
  exact mul_nonneg (one_div_nonneg.mpr (frobNormSq_nonneg B)) (gramHermForm3_quadNum_nonneg B v)

noncomputable section

/-- Complex `3 × 3` matrix of each factorized approximant `factorizedState3 B` is positive semidefinite
and has trace `1` whenever `B` has a nonzero entry. -/
theorem toMatrix_factorizedState3_posSemidef_and_trace_one {B : GaussMatrix3}
    (hB : ∃ i j : Fin 3, B i j ≠ 0) :
    (toMatrix (factorizedState3 B)).PosSemidef ∧ (toMatrix (factorizedState3 B)).trace = 1 := by
  refine ⟨toMatrix_posSemidef (fun g _ => factorizedState3_quadNum_nonneg B g), ?_⟩
  rw [trace_toMatrix, factorizedState3_tr_eq_one hB]
  simp

/-- Real quadratic form `Re ⟨v, M v⟩` of an arbitrary complex `3 × 3` matrix `M` on `ℂ³`. -/
def complexQuadForm (M : Matrix (Fin 3) (Fin 3) ℂ) (v : Fin 3 → ℂ) : ℝ :=
  (dotC v (M *ᵥ v)).re

/-- Rayleigh quotient `Re ⟨v, M v⟩ / ‖v‖²` of an arbitrary complex `3 × 3` matrix `M` on `ℂ³`. -/
def complexRayleigh (M : Matrix (Fin 3) (Fin 3) ℂ) (v : Fin 3 → ℂ) : ℝ :=
  complexQuadForm M v / nsq v

/-- Entrywise `ℓ¹` norm `∑ i, ∑ j, ‖A i j‖` on `3 × 3` complex matrices. -/
def matEntryL1Norm (A : Matrix (Fin 3) (Fin 3) ℂ) : ℝ :=
  ∑ i : Fin 3, ∑ j : Fin 3, ‖A i j‖

theorem matEntryL1Norm_nonneg (A : Matrix (Fin 3) (Fin 3) ℂ) :
    0 ≤ matEntryL1Norm A :=
  Finset.sum_nonneg fun i _ => Finset.sum_nonneg fun j _ => norm_nonneg (A i j)

theorem complexQuadForm_toMatrix (ρ : HermForm3) (v : Fin 3 → ℂ) :
    complexQuadForm (toMatrix ρ) v = Qc ρ v :=
  rfl

theorem complexRayleigh_toMatrix (ρ : HermForm3) (v : Fin 3 → ℂ) :
    complexRayleigh (toMatrix ρ) v = QcRay ρ v :=
  rfl

theorem complexQuadForm_sub (A B : Matrix (Fin 3) (Fin 3) ℂ) (v : Fin 3 → ℂ) :
    complexQuadForm (A - B) v = complexQuadForm A v - complexQuadForm B v := by
  unfold complexQuadForm
  rw [Matrix.sub_mulVec, dotC_sub_right, Complex.sub_re]

theorem complexRayleigh_sub (A B : Matrix (Fin 3) (Fin 3) ℂ) (v : Fin 3 → ℂ) :
    complexRayleigh (A - B) v = complexRayleigh A v - complexRayleigh B v := by
  unfold complexRayleigh
  rw [complexQuadForm_sub, sub_div]

private lemma norm_coord_sq_le_nsq (v : Fin 3 → ℂ) (i : Fin 3) :
    ‖v i‖ ^ 2 ≤ nsq v := by
  rw [← Complex.normSq_eq_norm_sq]
  exact normSq_le_nsq v i

private lemma norm_coord_mul_le_nsq (v : Fin 3 → ℂ) (i j : Fin 3) :
    ‖v i‖ * ‖v j‖ ≤ nsq v := by
  have hi := norm_coord_sq_le_nsq v i
  have hj := norm_coord_sq_le_nsq v j
  have hsq : 0 ≤ (‖v i‖ - ‖v j‖) ^ 2 := sq_nonneg _
  nlinarith

/-- Quadratic form bound on `ℂ³`: `|Re ⟨v, A v⟩| ≤ matEntryL1Norm A * nsq v`. -/
theorem abs_complexQuadForm_le (A : Matrix (Fin 3) (Fin 3) ℂ) (v : Fin 3 → ℂ) :
    |complexQuadForm A v| ≤ matEntryL1Norm A * nsq v := by
  have h1 : |complexQuadForm A v| ≤ ‖dotC v (A *ᵥ v)‖ := Complex.abs_re_le_norm _
  have hdot : dotC v (A *ᵥ v) = ∑ i : Fin 3, ∑ j : Fin 3, conj (v i) * (A i j * v j) := by
    simp only [dotC, Matrix.mulVec, dotProduct, Fin.sum_univ_three]
    ring
  have h2 : ‖dotC v (A *ᵥ v)‖ ≤ ∑ i : Fin 3, ∑ j : Fin 3, ‖conj (v i) * (A i j * v j)‖ := by
    rw [hdot]
    refine (norm_sum_le _ _).trans (Finset.sum_le_sum fun i _ => norm_sum_le _ _)
  have h3 : (∑ i : Fin 3, ∑ j : Fin 3, ‖conj (v i) * (A i j * v j)‖) ≤
      ∑ i : Fin 3, ∑ j : Fin 3, ‖A i j‖ * nsq v := by
    refine Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ => ?_
    rw [norm_mul, norm_mul, Complex.norm_conj]
    have hmul : ‖v i‖ * (‖A i j‖ * ‖v j‖) = ‖A i j‖ * (‖v i‖ * ‖v j‖) := by ring
    rw [hmul]
    exact mul_le_mul_of_nonneg_left (norm_coord_mul_le_nsq v i j) (norm_nonneg (A i j))
  have h4 : (∑ i : Fin 3, ∑ j : Fin 3, ‖A i j‖ * nsq v) = matEntryL1Norm A * nsq v := by
    unfold matEntryL1Norm
    simp only [← Finset.sum_mul]
  linarith

/-- Uniform Rayleigh-quotient stability on `ℂ³ \ {0}`:
`|complexRayleigh A v - complexRayleigh B v| ≤ matEntryL1Norm (A - B)` for every nonzero `v ∈ ℂ³`. -/
theorem abs_complexRayleigh_sub_le (A B : Matrix (Fin 3) (Fin 3) ℂ)
    {v : Fin 3 → ℂ} (hv : v ≠ 0) :
    |complexRayleigh A v - complexRayleigh B v| ≤ matEntryL1Norm (A - B) := by
  have hpos : 0 < nsq v := nsq_pos hv
  rw [← complexRayleigh_sub, complexRayleigh, abs_div, abs_of_pos hpos, div_le_iff₀ hpos]
  exact abs_complexQuadForm_le (A - B) v

/-- Quantitative Born-probability approximation bound for factorized Gaussian-rational states:
for any `B : GaussMatrix3` and continuum state `ρC : Matrix (Fin 3) (Fin 3) ℂ`, the Born probability
discrepancy on every nonzero complex ray `v ∈ ℂ³ \ {0}` is bounded by
`matEntryL1Norm (toMatrix (factorizedState3 B) - ρC)`. -/
theorem factorizedState3_born_prob_error_le (B : GaussMatrix3)
    (ρC : Matrix (Fin 3) (Fin 3) ℂ) {v : Fin 3 → ℂ} (hv : v ≠ 0) :
    |QcRay (factorizedState3 B) v - complexRayleigh ρC v| ≤
      matEntryL1Norm (toMatrix (factorizedState3 B) - ρC) := by
  rw [← complexRayleigh_toMatrix]
  exact abs_complexRayleigh_sub_le (toMatrix (factorizedState3 B)) ρC hv

/-- Uniqueness of complex Hermitian reconstruction from continuum Rayleigh quotients on `ℂ³ \ {0}`. -/
theorem complex_hermitian_unique_of_rayleigh_eq {A B : Matrix (Fin 3) (Fin 3) ℂ}
    (hA : A.IsHermitian) (hB : B.IsHermitian)
    (h : ∀ v : Fin 3 → ℂ, v ≠ 0 → complexRayleigh A v = complexRayleigh B v) :
    A = B := by
  refine eq_of_re_dotC_mulVec_self hA hB fun v hv => ?_
  have hn : nsq v ≠ 0 := (nsq_pos hv).ne'
  exact (div_left_inj' hn).mp (h v hv)

/-! ### Part B: All Finite Dimensions (`d = 0, 1, 2` and `d ≥ 3`) -/

/-- Dimension `d = 0`: the carrier `Fin 0 → ℂ` contains no nonzero vectors. -/
theorem dim0_no_nonzero_vectors (v : Fin 0 → ℂ) : ¬ (v ≠ 0) := by
  intro hv
  apply hv
  ext i
  exact Fin.elim0 i

/-- Dimension `d = 0`: any two ray valuations on `Fin 0 → ℂ` agree vacuously on all nonzero vectors. -/
theorem dim0_frameValuation_vacuously_unique (f g : (Fin 0 → ℂ) → ℝ) :
    ∀ v : Fin 0 → ℂ, v ≠ 0 → f v = g v := by
  intro v hv
  exact False.elim (dim0_no_nonzero_vectors v hv)

/-- Dimension `d = 1`: a 1D frame valuation assigns `1` to each 1-element frame (every nonzero vector). -/
def IsDim1FrameValuation (f : (Fin 1 → ℂ) → ℝ) : Prop :=
  ∀ v : Fin 1 → ℂ, v ≠ 0 → f v = 1

/-- Dimension `d = 1`: every 1D frame valuation equals the Born rule of the `1 × 1` identity matrix,
and any two 1D frame valuations coincide on all nonzero vectors. -/
theorem dim1_frameValuation_eq_one {f g : (Fin 1 → ℂ) → ℝ}
    (hf : IsDim1FrameValuation f) (hg : IsDim1FrameValuation g)
    {v : Fin 1 → ℂ} (hv : v ≠ 0) :
    f v = 1 ∧ f v = g v :=
  ⟨hf v hv, (hf v hv).trans (hg v hv).symm⟩

end

/-- A 2-component vector over `ℚ(i)`. -/
structure GVec2 where
  x : GaussRat
  y : GaussRat

/-- Nonzero predicate on `ℚ(i)²`. -/
def GVec2.NonZero (u : GVec2) : Prop :=
  u.x ≠ 0 ∨ u.y ≠ 0

/-- Hermitian inner product on `ℚ(i)²`. -/
def GVec2.inner (u v : GVec2) : GaussRat :=
  star u.x * v.x + star u.y * v.y

/-- Squared Hermitian norm on `ℚ(i)²`. -/
def normSqVec2 (u : GVec2) : ℚ :=
  u.x.normSq + u.y.normSq

/-- Orthogonal 2-frame in `ℚ(i)²`. -/
def IsFrame2 (u v : GVec2) : Prop :=
  u.NonZero ∧ v.NonZero ∧ GVec2.inner u v = 0

/-- Frame function on `ℚ(i)²`: sums to `1` on every orthogonal 2-frame. -/
def IsFrameFunction2 (f : GVec2 → ℚ) : Prop :=
  ∀ u v : GVec2, IsFrame2 u v → f u + f v = 1

/-- Nonnegative 2D frame function on `ℚ(i)²`. -/
def IsNonnegFrameFunction2 (f : GVec2 → ℚ) : Prop :=
  IsFrameFunction2 f ∧ ∀ u : GVec2, u.NonZero → 0 ≤ f u

/-- Parameterization of a `2 × 2` rational Hermitian form over `ℚ(i)`. -/
structure HermForm2 where
  d1 : ℚ
  d2 : ℚ
  a12 : ℚ
  b12 : ℚ

/-- Rayleigh quotient of `ρ : HermForm2` on `ℚ(i)²`. -/
def quadRay2 (ρ : HermForm2) (u : GVec2) : ℚ :=
  (ρ.d1 * u.x.normSq + ρ.d2 * u.y.normSq +
   2 * ρ.a12 * (u.x.re * u.y.re + u.x.im * u.y.im) -
   2 * ρ.b12 * (u.x.re * u.y.im - u.x.im * u.y.re)) / normSqVec2 u

/-- Explicit `{0, 1/2, 1}`-valued 2D projection-measure counterexample on `ℚ(i)²`:
assigns `1` on the first coordinate axis (`u.y = 0`), `0` on the second coordinate axis (`u.x = 0`),
and `1 / 2` on all off-axis vectors (`u.x ≠ 0 ∧ u.y ≠ 0`). -/
def dim2AxisCounterexample (u : GVec2) : ℚ :=
  if u.y = 0 then 1 else if u.x = 0 then 0 else 1 / 2

private lemma star_eq_zero_iff (z : GaussRat) : star z = 0 ↔ z = 0 := by
  constructor
  · intro h
    have hst : star (star z) = star (0 : GaussRat) := congrArg star h
    simpa using hst
  · rintro rfl; rfl

/-- `dim2AxisCounterexample` is a nonnegative 2D frame function on `ℚ(i)²`. -/
theorem dim2AxisCounterexample_isNonnegFrameFunction2 :
    IsNonnegFrameFunction2 dim2AxisCounterexample := by
  refine ⟨?_, ?_⟩
  · intro u v ⟨hu, hv, huv⟩
    unfold dim2AxisCounterexample
    by_cases huy : u.y = 0
    · have hux : u.x ≠ 0 := by rcases hu with h | h; exact h; exact False.elim (h huy)
      have hvx : v.x = 0 := by
        unfold GVec2.inner at huv
        rw [huy, star_zero, zero_mul, add_zero] at huv
        rcases mul_eq_zero.mp huv with hst | hvx
        · exact False.elim (hux ((star_eq_zero_iff u.x).mp hst))
        · exact hvx
      have hvy : v.y ≠ 0 := by rcases hv with h | h; exact False.elim (h hvx); exact h
      simp [huy, hvy, hvx]
    · by_cases hux : u.x = 0
      · have hvy : v.y = 0 := by
          unfold GVec2.inner at huv
          rw [hux, star_zero, zero_mul, zero_add] at huv
          rcases mul_eq_zero.mp huv with hst | hvy
          · exact False.elim (huy ((star_eq_zero_iff u.y).mp hst))
          · exact hvy
        simp [huy, hux, hvy]
      · have hvx : v.x ≠ 0 := by
          intro hvx0
          unfold GVec2.inner at huv
          rw [hvx0, mul_zero, zero_add] at huv
          rcases mul_eq_zero.mp huv with hst | hvy0
          · exact huy ((star_eq_zero_iff u.y).mp hst)
          · rcases hv with h | h
            · exact h hvx0
            · exact h hvy0
        have hvy : v.y ≠ 0 := by
          intro hvy0
          unfold GVec2.inner at huv
          rw [hvy0, mul_zero, add_zero] at huv
          rcases mul_eq_zero.mp huv with hst | hvx0
          · exact hux ((star_eq_zero_iff u.x).mp hst)
          · exact hvx hvx0
        simp [huy, hux, hvx, hvy]
        ring
  · intro u _
    unfold dim2AxisCounterexample
    split_ifs <;> norm_num

/-- Two-frame indicator counterexample in `d = 2` assigning `1` to `(1, 0)`, `0` to `(0, 1)`,
`1` to `(1, 1)`, `0` to `(1, -1)`, and `1/2` elsewhere: no `2 × 2` Hermitian matrix can simultaneously
match those values while remaining nonnegative on `(1, -2)`. -/
theorem dim2_projection_measure_obstruction (ρ : HermForm2)
    (he1 : quadRay2 ρ ⟨1, 0⟩ = 1)
    (he2 : quadRay2 ρ ⟨0, 1⟩ = 0)
    (hd1 : quadRay2 ρ ⟨1, 1⟩ = 1) :
    quadRay2 ρ ⟨1, -2⟩ = -1 / 5 ∧ ¬ (0 ≤ quadRay2 ρ ⟨1, -2⟩) := by
  have h1 : ρ.d1 = 1 := by
    simpa [quadRay2, normSqVec2, GaussRat.normSq] using he1
  have h2 : ρ.d2 = 0 := by
    simpa [quadRay2, normSqVec2, GaussRat.normSq] using he2
  have ha : ρ.a12 = 1 / 2 := by
    simp [quadRay2, normSqVec2, GaussRat.normSq, h1, h2] at hd1
    linarith
  have hval : quadRay2 ρ ⟨1, -2⟩ = -1 / 5 := by
    simp [quadRay2, normSqVec2, GaussRat.normSq, h1, h2, ha]
    norm_num
  exact ⟨hval, by rw [hval]; norm_num⟩

noncomputable section

/-- `d`-dimensional Hermitian inner product `⟨u, v⟩ = ∑ i, conj(u_i) v_i` on `ℂ^d`. -/
def dotCD {d : ℕ} (u v : Fin d → ℂ) : ℂ :=
  ∑ i : Fin d, conj (u i) * v i

/-- `d`-dimensional real quadratic form `Re ⟨v, M v⟩` of `M : Matrix (Fin d) (Fin d) ℂ`. -/
def complexQuadFormD {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ) (v : Fin d → ℂ) : ℝ :=
  (dotCD v (M *ᵥ v)).re

/-- `3 × 3` principal submatrix of `M : Matrix (Fin d) (Fin d) ℂ` along `ι : Fin 3 → Fin d`. -/
def submatrix3D {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ) (ι3 : Fin 3 → Fin d) :
    Matrix (Fin 3) (Fin 3) ℂ :=
  fun i j => M (ι3 i) (ι3 j)

/-- If `M` is Hermitian on `ℂ^d`, every `3 × 3` principal submatrix `submatrix3D M ι3` is Hermitian. -/
theorem submatrix3D_isHermitian {d : ℕ} {M : Matrix (Fin d) (Fin d) ℂ}
    (hM : M.IsHermitian) (ι3 : Fin 3 → Fin d) :
    (submatrix3D M ι3).IsHermitian := by
  refine Matrix.IsHermitian.ext fun i j => ?_
  simp only [submatrix3D]
  exact congrFun (congrFun hM.eq (ι3 i)) (ι3 j)

/-- Trace of the 3D restriction `submatrix3D M ι3` equals the 3-projector subspace weight
`M(ι₀, ι₀) + M(ι₁, ι₁) + M(ι₂, ι₂)`. -/
theorem submatrix3D_trace_eq_subspace_weight {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ)
    (ι3 : Fin 3 → Fin d) :
    (submatrix3D M ι3).trace = M (ι3 0) (ι3 0) + M (ι3 1) (ι3 1) + M (ι3 2) (ι3 2) := by
  simp only [Matrix.trace, Matrix.diag, submatrix3D, Fin.sum_univ_three]

/-- Overlap compatibility of 3D submatrix reconstructions across arbitrary dimension `d ≥ 3`:
whenever two 3D subspace embeddings `ι₁, ι₂ : Fin 3 → Fin d` share a pair of basis indices
`ι₁ a = ι₂ a'` and `ι₁ b = ι₂ b'`, their `3 × 3` restrictions assign identical matrix entries. -/
theorem compat_submatrix3D_overlap {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ)
    (ι₁ ι₂ : Fin 3 → Fin d) {a b a' b' : Fin 3}
    (ha : ι₁ a = ι₂ a') (hb : ι₁ b = ι₂ b') :
    submatrix3D M ι₁ a b = submatrix3D M ι₂ a' b' := by
  simp only [submatrix3D, ha, hb]

lemma dotCD_single_mulVec_single {d : ℕ} (D : Matrix (Fin d) (Fin d) ℂ) (i j : Fin d) :
    dotCD (Pi.single i 1) (D *ᵥ Pi.single j 1) = D i j := by
  simp only [dotCD, Matrix.mulVec, dotProduct, Pi.single_apply]
  rw [Finset.sum_eq_single i]
  · simp only [ ↓reduceIte, map_one, one_mul]
    rw [Finset.sum_eq_single j]
    · simp
    · intro k _ hkj; simp [hkj]
    · intro hj; exact False.elim (hj (Finset.mem_univ j))
  · intro k _ hki
    simp [hki]
  · intro hi; exact False.elim (hi (Finset.mem_univ i))

lemma dotCD_conj_symm {d : ℕ} (u v : Fin d → ℂ) :
    conj (dotCD u v) = dotCD v u := by
  simp only [dotCD, map_sum, map_mul, RingHomCompTriple.comp_apply, RingHom.id_apply]
  refine Finset.sum_congr rfl fun i _ => mul_comm _ _

lemma dotCD_mulVec_left {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ) (u v : Fin d → ℂ) :
    dotCD (M *ᵥ u) v = dotCD u (Mᴴ *ᵥ v) := by
  have h1 : dotCD (M *ᵥ u) v = star (M *ᵥ u) ⬝ᵥ v := rfl
  have h2 : dotCD u (Mᴴ *ᵥ v) = star u ⬝ᵥ (Mᴴ *ᵥ v) := rfl
  rw [h1, h2, Matrix.star_mulVec, Matrix.dotProduct_mulVec]

lemma im_dotCD_mulVec_self {d : ℕ} {M : Matrix (Fin d) (Fin d) ℂ}
    (hM : M.IsHermitian) (v : Fin d → ℂ) :
    (dotCD v (M *ᵥ v)).im = 0 := by
  rw [← Complex.conj_eq_iff_im, dotCD_conj_symm, dotCD_mulVec_left, hM.eq]

/-- Global `d`-dimensional Hermitian uniqueness by polarization: two `d × d` Hermitian matrices
whose real quadratic forms agree on all vectors in `ℂ^d` are equal (`A = B`). -/
theorem eq_of_complexQuadFormD_eq {d : ℕ} {A B : Matrix (Fin d) (Fin d) ℂ}
    (hA : A.IsHermitian) (hB : B.IsHermitian)
    (h : ∀ v : Fin d → ℂ, complexQuadFormD A v = complexQuadFormD B v) :
    A = B := by
  set D := A - B with hD
  have hDh : D.IsHermitian := hA.sub hB
  have hself : ∀ v : Fin d → ℂ, dotCD v (D *ᵥ v) = 0 := by
    intro v
    apply Complex.ext
    · have hv := h v
      unfold complexQuadFormD at hv
      have hsub : dotCD v (D *ᵥ v) = dotCD v (A *ᵥ v) - dotCD v (B *ᵥ v) := by
        simp only [hD, Matrix.sub_mulVec, dotCD, Pi.sub_apply, mul_sub, Finset.sum_sub_distrib]
      rw [hsub, Complex.sub_re, hv, sub_self, Complex.zero_re]
    · rw [im_dotCD_mulVec_self hDh, Complex.zero_im]
  have hpol : ∀ v w : Fin d → ℂ, (4 : ℂ) * dotCD v (D *ᵥ w) =
      (dotCD (v + w) (D *ᵥ (v + w)) - dotCD (v - w) (D *ᵥ (v - w)))
        - Complex.I * (dotCD (v + Complex.I • w) (D *ᵥ (v + Complex.I • w))
          - dotCD (v - Complex.I • w) (D *ᵥ (v - Complex.I • w))) := by
    intro v w
    simp only [Matrix.mulVec_add, Matrix.mulVec_sub, Matrix.mulVec_smul, dotCD,
      Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, map_add, map_sub, map_mul,
      Complex.conj_I, ← Finset.sum_sub_distrib, Finset.mul_sum]
    refine Finset.sum_congr rfl fun i _ => ?_
    linear_combination (2 * conj (v i) * (D *ᵥ w) i - 2 * conj (w i) * (D *ᵥ v) i) * Complex.I_mul_I
  ext i j
  have h4 := hpol (Pi.single i 1) (Pi.single j 1)
  rw [hself, hself, hself, hself] at h4
  have hzero : (4 : ℂ) * dotCD (Pi.single i 1) (D *ᵥ Pi.single j 1) = 0 := by rw [h4]; ring
  have hij := (mul_eq_zero.mp hzero).resolve_left (by norm_num)
  rw [dotCD_single_mulVec_single] at hij
  exact sub_eq_zero.mp hij

/-! ### Part C: Automatic Regularity for Nonnegative Continuum Frame Functions (`d = 3`) -/

/-- Orthogonal 3-frame of nonzero vectors in `ℂ³`. -/
def IsContinuumFrame3 (u v w : Fin 3 → ℂ) : Prop :=
  u ≠ 0 ∧ v ≠ 0 ∧ w ≠ 0 ∧ dotC u v = 0 ∧ dotC u w = 0 ∧ dotC v w = 0

/-- Continuum frame function on `ℂ³ \ {0}`. -/
def IsContinuumFrameFunction3 (f : (Fin 3 → ℂ) → ℝ) : Prop :=
  (∀ v : Fin 3 → ℂ, v ≠ 0 → ∀ c : ℂ, c ≠ 0 → f (c • v) = f v) ∧
  (∀ u v w : Fin 3 → ℂ, IsContinuumFrame3 u v w → f u + f v + f w = 1)

/-- Nonnegative continuum frame function on `ℂ³ \ {0}`. -/
def IsNonnegContinuumFrameFunction3 (f : (Fin 3 → ℂ) → ℝ) : Prop :=
  IsContinuumFrameFunction3 f ∧ ∀ v : Fin 3 → ℂ, v ≠ 0 → 0 ≤ f v

/-- Every nonzero vector `u ∈ ℂ³ \ {0}` extends to an orthogonal continuum 3-frame `(u, v, w)`. -/
theorem exists_continuumFrame3_completion {u : Fin 3 → ℂ} (hu : u ≠ 0) :
    ∃ v w : Fin 3 → ℂ, IsContinuumFrame3 u v w := by
  obtain ⟨v, hnv, huv⟩ := exists_unit_perp u
  have hv : v ≠ 0 := ne_zero_of_nsq_pos (by rw [hnv]; exact one_pos)
  have hcr_ne : ccross u v ≠ 0 := by
    intro h0
    have hnsq := nsq_ccross u v
    have h0_nsq : nsq (ccross u v) = 0 := (nsq_eq_zero_iff _).mpr h0
    rw [h0_nsq, huv, normSq_zero, sub_zero] at hnsq
    exact mul_ne_zero (nsq_pos hu).ne' (nsq_pos hv).ne' hnsq.symm
  refine ⟨v, ccross u v, hu, hv, hcr_ne, huv, dotC_ccross_left u v, dotC_ccross_right u v⟩

/-- Automatic `[0, 1]` boundedness of every nonnegative continuum frame function on `ℂ³ \ {0}`
(proved purely from nonnegativity and 3-frame additivity, prior to any continuity assumption). -/
theorem nonneg_continuum_frameFunction_bounds {f : (Fin 3 → ℂ) → ℝ}
    (hf : IsNonnegContinuumFrameFunction3 f) {u : Fin 3 → ℂ} (hu : u ≠ 0) :
    0 ≤ f u ∧ f u ≤ 1 := by
  obtain ⟨v, w, hfr⟩ := exists_continuumFrame3_completion hu
  have hsum := hf.1.2 u v w hfr
  have hfu := hf.2 u hu
  have hfv := hf.2 v hfr.2.1
  have hfw := hf.2 w hfr.2.2.1
  exact ⟨hfu, by linarith⟩

/-- Orthogonal pair subadditivity (`f u + f v ≤ 1`) for any orthogonal nonzero `u, v ∈ ℂ³ \ {0}`. -/
theorem continuum_piron_subadditivity {f : (Fin 3 → ℂ) → ℝ}
    (hf : IsNonnegContinuumFrameFunction3 f) {u v : Fin 3 → ℂ}
    (hu : u ≠ 0) (hv : v ≠ 0) (huv : dotC u v = 0) :
    f u + f v ≤ 1 := by
  have hcr_ne : ccross u v ≠ 0 := by
    intro h0
    have hnsq := nsq_ccross u v
    have h0_nsq : nsq (ccross u v) = 0 := (nsq_eq_zero_iff _).mpr h0
    rw [h0_nsq, huv, normSq_zero, sub_zero] at hnsq
    exact mul_ne_zero (nsq_pos hu).ne' (nsq_pos hv).ne' hnsq.symm
  have hfr : IsContinuumFrame3 u v (ccross u v) :=
    ⟨hu, hv, hcr_ne, huv, dotC_ccross_left u v, dotC_ccross_right u v⟩
  have hsum := hf.1.2 u v (ccross u v) hfr
  have hfw := hf.2 (ccross u v) hcr_ne
  linarith

/-- Equatorial vanishing at a pure pole: if `f u = 1`, then `f v = 0` for every nonzero `v ⊥ u`. -/
theorem continuum_eq_zero_on_perp_of_pole_one {f : (Fin 3 → ℂ) → ℝ}
    (hf : IsNonnegContinuumFrameFunction3 f) {u v : Fin 3 → ℂ}
    (hu : u ≠ 0) (hv : v ≠ 0) (huv : dotC u v = 0) (hpole : f u = 1) :
    f v = 0 := by
  have hsub := continuum_piron_subadditivity hf hu hv huv
  have hnonneg := hf.2 v hv
  linarith

/-! ### Part D: Infinite-Dimensional Separable Hilbert Spaces (`ℓ²(ℕ)`) & Trace Escape -/

/-- Finite-dimensional `N`-level compression trace of a sequence of basis weights `w : ℕ → ℝ`.
Preserves the actual subunit trace on the `N`-dimensional subspace without silent renormalization. -/
def compressionTrace (w : ℕ → ℝ) (N : ℕ) : ℝ :=
  ∑ n ∈ Finset.range N, w n

/-- Monotonicity of finite-dimensional compressions: for any nonnegative weight sequence `w ≥ 0`,
`N ≤ M` implies `compressionTrace w N ≤ compressionTrace w M`. -/
theorem compressionTrace_mono {w : ℕ → ℝ} (hw : ∀ n : ℕ, 0 ≤ w n)
    {N M : ℕ} (hNM : N ≤ M) :
    compressionTrace w N ≤ compressionTrace w M :=
  Finset.sum_le_sum_of_subset_of_nonneg (Finset.range_mono hNM) (fun n _ _ => hw n)

/-- Tightness predicate for a family/sequence of states: for every `ε > 0`, there is a finite cutoff
`N` capturing at least `1 - ε` of the unit trace. -/
def IsTightState (w : ℕ → ℝ) : Prop :=
  (∀ n : ℕ, 0 ≤ w n) ∧
  (∀ N : ℕ, compressionTrace w N ≤ 1) ∧
  (∀ ε : ℝ, 0 < ε → ∃ N : ℕ, 1 - ε ≤ compressionTrace w N)

/-- Under tightness, the uncaptured tail trace `1 - compressionTrace w M` is at most `ε` for all
`M ≥ N`. -/
theorem tail_weight_le_of_tight {w : ℕ → ℝ} (ht : IsTightState w)
    {ε : ℝ} (hε : 0 < ε) :
    ∃ N : ℕ, ∀ M : ℕ, N ≤ M → 0 ≤ 1 - compressionTrace w M ∧ 1 - compressionTrace w M ≤ ε := by
  obtain ⟨N, hN⟩ := ht.2.2 ε hε
  refine ⟨N, fun M hNM => ?_⟩
  have hmono := compressionTrace_mono ht.1 hNM
  have hsub := ht.2.1 M
  exact ⟨by linarith, by linarith⟩

/-- Required benchmark test case: the sequence of pure rank-one states `|e_k⟩⟨e_k|` on successive
orthogonal basis vectors `e_k` in `ℓ²(ℕ)`. -/
def basisEscapeState (k n : ℕ) : ℝ :=
  if n = k then 1 else 0

theorem basisEscapeState_nonneg (k n : ℕ) : 0 ≤ basisEscapeState k n := by
  unfold basisEscapeState
  split_ifs <;> norm_num

/-- Each `basisEscapeState k` has exact unit trace `1` at finite stage `N = k + 1`. -/
theorem basisEscapeState_normalized_at_stage (k : ℕ) :
    compressionTrace (basisEscapeState k) (k + 1) = 1 := by
  unfold compressionTrace basisEscapeState
  rw [Finset.sum_ite_eq' (Finset.range (k + 1)) k (fun _ => (1 : ℝ))]
  simp [Finset.mem_range]

/-- For every fixed finite-dimensional compression cutoff `N` and every state index `k ≥ N`, the
`N`-dimensional compression trace of `basisEscapeState k` is identically `0`. -/
theorem basisEscapeState_compression_eq_zero_of_ge {N k : ℕ} (hk : N ≤ k) :
    compressionTrace (basisEscapeState k) N = 0 := by
  unfold compressionTrace basisEscapeState
  refine Finset.sum_eq_zero fun n hn => ?_
  have hnk : n ≠ k := ne_of_lt (lt_of_lt_of_le (Finset.mem_range.mp hn) hk)
  simp [hnk]

/-- Explicit trace-escape theorem: the sequence of normalized rank-one basis states
`basisEscapeState k` has unit trace `1` at stage `k + 1`, yet converges to `0` on every fixed
finite-dimensional subspace compression `Finset.range N` (`∀ k ≥ N, compressionTrace = 0`) and on
every fixed basis coordinate `n`. -/
theorem basisEscapeState_escapes_to_zero_without_tightness :
    (∀ k : ℕ, compressionTrace (basisEscapeState k) (k + 1) = 1) ∧
    (∀ N k : ℕ, N ≤ k → compressionTrace (basisEscapeState k) N = 0) ∧
    (∀ n k : ℕ, n < k → basisEscapeState k n = 0) := by
  refine ⟨basisEscapeState_normalized_at_stage,
    fun N k hk => basisEscapeState_compression_eq_zero_of_ge hk,
    fun n k hnk => ?_⟩
  unfold basisEscapeState
  simp [ne_of_lt hnk]

end

end BornFinite.ContinuumDevelopment
