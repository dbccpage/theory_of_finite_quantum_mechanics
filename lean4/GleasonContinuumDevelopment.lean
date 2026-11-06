import GleasonContinuumShadow

/-!
# Continuum Gleason Development across Complex States, Finite Dimensions, Regularity, and Infinite Dimensions

AuthorityEffect: None.

This module formalizes Phase 4 of the Gleason campaign across four primary mathematical regimes:

## A. Arbitrary Complex States in Dimension Three (`d = 3`)
* **Constructive Factorized Approximation (`ρ_k = B_k B_k^* / tr(B_k B_k^*)`)**:
  - `GaussMatrix3`: `3 × 3` matrices over `GaussRat` (`ℚ(i)`).
  - `frobNormSq B`: exact rational Frobenius squared norm `∑ i, ∑ j, (B i j).normSq = tr(B B^*)`.
  - `frobNormSq_pos_of_entry_ne_zero` and `frobNormSq_ne_zero_of_entry_ne_zero`: establishes that the
    denominator `tr(B B^*)` is strictly positive and nonzero whenever `B` has at least one nonzero
    entry.
  - `gramHermForm3 B` and `factorizedState3 B`: exact rational Hermitian form of `B B^*` and its
    trace-normalized state `B B^* / tr(B B^*)`.
  - `mulConjTransposeVec B v` and `quadNum_gramHermForm3`: establishes the algebraic sum-of-squares
    identity `quadNum (gramHermForm3 B) v = normSqVec (B^* v) ≥ 0` for every `v ∈ ℚ(i)³`.
  - `factorizedState3_tr_eq_one`, `factorizedState3_quadNum_nonneg`, and
    `toMatrix_factorizedState3_posSemidef_and_trace_one`: establishes that each factorized rational
    approximant is **positive semidefinite** (`PosSemidef`) and **trace one** (`trace = 1`).
* **Real-Valued Frame Data, Quantitative Born Convergence, and Uniqueness on `ℂ³`**:
  - `complexQuadForm M v = Re ⟨v, M v⟩`, `complexRayleigh M v = Re ⟨v, M v⟩ / ‖v‖²`, and
    `matEntryL1Norm A = ∑ i, ∑ j, ‖A i j‖`.
  - `abs_complexQuadForm_le` and `abs_complexRayleigh_sub_le`: establishes the uniform Born-probability
    stability bound `|complexRayleigh A v - complexRayleigh B v| ≤ matEntryL1Norm (A - B)` on all
    nonzero `v ∈ ℂ³ \ {0}`.
  - `factorizedState3_born_prob_error_le` and `complex_hermitian_unique_of_rayleigh_eq`: shows in
    this model that as `toMatrix (factorizedState3 (B k))` converges to a continuum density matrix
    `ρC` in `matEntryL1Norm`, the Born probabilities converge uniformly on `ℂ³ \ {0}`, and the
    limiting Hermitian operator is unique.

## B. All Finite Dimensions (`d = 0, 1, 2` and `d ≥ 3`)
* **Dimension `d = 0`**:
  - `dim0_no_nonzero_vectors` and `dim0_frameValuation_vacuously_unique`: the empty carrier has no
    nonzero rays, and any two valuations on its nonzero rays coincide vacuously.
* **Dimension `d = 1`**:
  - `IsDim1FrameValuation` and `dim1_frameValuation_eq_one`: every 1-element frame valuation on
    `ℂ¹ \ {0}` is identically `1` on all nonzero vectors and uniquely represented by `I₁`.
* **Dimension `d = 2` (Projection-Measure Exception vs. Effect-Additive Route)**:
  - `GVec2`, `IsFrame2`, `IsFrameFunction2`, `IsNonnegFrameFunction2`, `HermForm2`, `quadRay2`: 2D
    orthogonal frame valuations and `2 × 2` Hermitian Rayleigh quotients.
  - `dim2AxisCounterexample`: an explicit `{0, 1/2, 1}`-valued nonnegative 2D frame function
    assigning `1` to the `e₁` ray (`u.y = 0`), `0` to the `e₂` ray (`u.x = 0`), and `1/2` to all
    other rays, shown to satisfy 2D frame additivity and nonnegativity
    (`dim2AxisCounterexample_isNonnegFrameFunction2`) while admitting no `2 × 2` Hermitian quadratic
    representation (`dim2AxisCounterexample_not_quadratic`, evaluated at `(2, 1)` where
    `4 / 5 ≠ 1 / 2`), alongside the two-frame `{0, 1}` valuation obstruction at `(1, -2)` where
    `-1 / 5 < 0` (`dim2_projection_measure_obstruction`), contrasting with the operator-linear
    `EffectValuation` route (`born_trace_representation` in `BornHermitianTraceRepresentation.lean`).
* **Dimensions `d ≥ 3` (Subspace Restrictions, Compatibility, and Global Uniqueness)**:
  - `dotCD`, `complexQuadFormD`, and `submatrix3D M ι3` for any `ι3 : Fin 3 → Fin d`.
  - `submatrix3D_isHermitian`, `submatrix3D_trace_eq_subspace_weight`,
    `compat_submatrix3D_overlap`, and `eq_of_complexQuadFormD_eq`: establishes compatibility of 3D
    principal submatrices, subspace weights, and global `d × d` Hermitian uniqueness by polarization.

## C. Automatic Regularity Step for Nonnegative Continuum Frame Functions (`d = 3`)
* `IsContinuumFrame3`, `IsContinuumFrameFunction3`, `IsNonnegContinuumFrameFunction3`.
* `exists_continuumFrame3_completion`: extends any nonzero vector `u ∈ ℂ³ \ {0}` to an orthogonal
  3-frame `(u, v, w)`.
* `nonneg_continuum_frameFunction_bounds`: establishes `0 ≤ f u ≤ 1` on all nonzero vectors in `ℂ³`
  from nonnegativity and 3-frame additivity alone (without continuity).
* `continuum_piron_subadditivity`: establishes the Piron–Soler orthogonal subadditivity inequality
  `f u + f v ≤ 1` for orthogonal nonzero vectors `u ⊥ v`.
* `continuum_eq_zero_on_perp_of_pole_one`: establishes equatorial vanishing `f v = 0` for all
  `v ⊥ u` whenever `f u = 1`.
* Preserves the explicit boundary between continuum automatic regularity on `S(ℂ³)` and the
  rational question `TFQ-1057` on `ℚ(i)³`.

## D. Infinite-Dimensional Separable Hilbert Spaces (`ℓ²(ℕ)`)
* `compressionTrace w N = ∑ n ∈ Finset.range N, w n`: finite-dimensional subspace compression trace,
  preserving subunit trace (`compressionTrace w N ≤ 1`) without silent renormalization.
* `compressionTrace_mono`, `IsTightState`, and `tail_weight_le_of_tight`: monotonicity of finite
  compressions and control of tail trace loss `1 - compressionTrace w M ≤ ε` under tightness.
* **Rank-One Basis Escape Witness (`basisEscapeState k n = if n = k then 1 else 0`)**:
  - `basisEscapeState_normalized_at_stage`: `compressionTrace (basisEscapeState k) (k + 1) = 1`.
  - `basisEscapeState_compression_eq_zero_of_ge`: for every fixed finite cutoff `N` and every stage
    `k ≥ N`, `compressionTrace (basisEscapeState k) N = 0`.
  - `basisEscapeState_escapes_to_zero_without_tightness`: establishes that a sequence of normalized
    trace-one states on successive orthogonal basis vectors vanishes on every fixed finite-dimensional
    compression for `k ≥ N` while retaining total trace `1` at stage `k + 1`.

## E. Compactness, Supremum/Infimum Bounds, Isotropic Deflation & Mixed-State Extremum Reduction (`TFQ-1059`)
* **Unit-Sphere Supremum & Infimum Bounds (`S²` and `S⁵`)**:
  - `nonempty_image_sphere3`, `bddAbove_image_sphere3_of_nonneg`, `bddBelow_image_sphere3_of_nonneg`,
    `le_sSup_sphere3_of_nonneg`, `sInf_sphere3_le_of_nonneg`, `sSup_sphere3_bounds_of_nonneg`,
    `nonempty_image_sphereC`, `bddAbove_image_sphereC_of_nonnegC`, `bddBelow_image_sphereC_of_nonnegC`,
    `le_sSup_sphereC_of_nonnegC`, `sInf_sphereC_le_of_nonnegC`, and `sSup_sphereC_bounds_of_nonnegC`:
    establishes `0 ≤ sInf ≤ W / 3 ≤ sSup ≤ W` for every nonnegative real (`sphere3`) or complex
    (`sphereC`) frame function of weight `W` with zero continuity assumptions.
* **Compactness & Continuity-Free Orthogonal Extrema Reduction (`S²` and `S⁵`)**:
  - `AttainsExtrema`, `attainsExtrema_of_continuousOn_sphere3`, `attainsExtrema_of_continuousOn`,
    `exists_min_on_equator_pole_of_max_and_min`, `exists_min_perp_of_max_and_min`,
    `AttainsExtremaC`, `attainsExtremaC_of_continuousOn_sphereC`, and `attainsExtremaC_of_continuousOn`:
    separates compactness on `sphere3` and `sphereC` from the purely algebraic common-normal
    great-circle identity that produces an orthogonal maximizer-minimizer pair `(p, r)`.
* **Isotropic Minimum Deflation & Continuity-Free Axisymmetric Mixed-State Gleason Theorems (`ℝ³` and `ℂ³`)**:
  - `deflateIso`, `isFrameFunction_deflateIso`, `isNonnegFrameFunction_deflateIso`,
    `axisymmetric_mixed_state_nonneg_gleason_real`, `deflateIsoC`, `isFrameFunctionC_deflateIsoC`,
    `isNonnegFrameFunctionC_deflateIsoC`, and `axisymmetric_mixed_state_nonneg_gleason_complex`:
    establishes the Born quadratic form `F v = m + (F p - m) * |⟨p, v⟩|² / ‖v‖²` for every
    axisymmetric mixed state (`F p + 2 m = W`, `∀ v ≠ 0, m ≤ F v`) with zero continuity assumption.
* **Continuity-Free Zero-Counting, Triaxial Spectral Ordering & Nonnegative PSD Born Form (`ℝ³` and `ℂ³`)**:
  - `eq_zero_of_vanishes_on_six_circles_of_extrema`, `mixed_state_gleason_real_of_extrema`,
    `gleason_real_of_continuousOn_sphere3`, `triaxial_eigenvalues_nonneg_and_ordered`,
    `stdQuad_nonneg_and_le_weight_of_eigenvalues`, `nonneg_gleason_real_of_extrema`,
    `nonneg_gleason_real_of_continuousOn_sphere3`, and `complex_eigenvalues_nonneg_and_ordered`:
    reduces any general triaxial mixed-state frame function with orthogonal extrema `(p, r)` to a
    weight-zero residual `hResidual` that vanishes on all six great circles `x = ±y`, `x = ±z`,
    `y = ±z` without continuity, vanishes identically under `AttainsExtrema hResidual`, and packages
    the ordered nonnegative eigenvalues `0 ≤ λ₃ ≤ λ₂ ≤ λ₁ ≤ W` (`λ₁ + λ₂ + λ₃ = W`) in both `ℝ³` and `ℂ³`.
-/

namespace BornFinite.ContinuumDevelopment

open BornFinite BornFinite.GaussRat BornFinite.GaussianFrames BornFinite.GaussianTomography
open BornFinite.GleasonBridge BornFinite.BornCompletion
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

/-- `dim2AxisCounterexample` cannot be represented as the Rayleigh quotient `quadRay2 ρ` of any
`2 × 2` Hermitian form `ρ : HermForm2` on nonzero vectors in `ℚ(i)²`: matching `⟨1, 0⟩`, `⟨0, 1⟩`,
and `⟨1, 1⟩` forces `quadRay2 ρ ⟨2, 1⟩ = 4 / 5 ≠ 1 / 2 = dim2AxisCounterexample ⟨2, 1⟩`. -/
theorem dim2AxisCounterexample_not_quadratic :
    ¬ ∃ ρ : HermForm2, ∀ u : GVec2, u.NonZero → dim2AxisCounterexample u = quadRay2 ρ u := by
  rintro ⟨ρ, hρ⟩
  have he1 : dim2AxisCounterexample ⟨1, 0⟩ = quadRay2 ρ ⟨1, 0⟩ :=
    hρ ⟨1, 0⟩ (Or.inl one_ne_zero)
  have he2 : dim2AxisCounterexample ⟨0, 1⟩ = quadRay2 ρ ⟨0, 1⟩ :=
    hρ ⟨0, 1⟩ (Or.inr one_ne_zero)
  have hd1 : dim2AxisCounterexample ⟨1, 1⟩ = quadRay2 ρ ⟨1, 1⟩ :=
    hρ ⟨1, 1⟩ (Or.inl one_ne_zero)
  have hw : dim2AxisCounterexample ⟨2, 1⟩ = quadRay2 ρ ⟨2, 1⟩ :=
    hρ ⟨2, 1⟩ (Or.inr one_ne_zero)
  have h1 : ρ.d1 = 1 := by
    simp [dim2AxisCounterexample, quadRay2, normSqVec2, GaussRat.normSq] at he1
    linarith
  have h2 : ρ.d2 = 0 := by
    simp [dim2AxisCounterexample, quadRay2, normSqVec2, GaussRat.normSq] at he2
    linarith
  have ha : ρ.a12 = 0 := by
    simp [dim2AxisCounterexample, quadRay2, normSqVec2, GaussRat.normSq, h1, h2] at hd1
    linarith
  simp [dim2AxisCounterexample, quadRay2, normSqVec2, GaussRat.normSq, h1, h2, ha] at hw
  norm_num at hw

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

namespace GleasonReal

open Real Filter Topology

/-! ### Target 2: Nonnegativity bounds, Piron tangent-step inequalities, and continuity-free reductions -/

/-- A nonnegative frame function of weight `W` on `ℝ³ \ {0}`. -/
structure IsNonnegFrameFunction (f : (Fin 3 → ℝ) → ℝ) (W : ℝ) : Prop extends IsFrameFunction f W where
  nonneg : ∀ v : Fin 3 → ℝ, v ≠ 0 → 0 ≤ f v

/-- Transport of nonnegative frame functions along an orthonormal frame. -/
theorem IsNonnegFrameFunction.comp_ofFrame {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) :
    IsNonnegFrameFunction (fun v => f (ofFrame p q r v)) W where
  toIsFrameFunction := hf.toIsFrameFunction.comp_ofFrame h
  nonneg v hv := hf.nonneg (ofFrame p q r v) (ofFrame_ne_zero h hv)

/-- The weight `W` of a nonnegative frame function on `ℝ³ \ {0}` is nonnegative. -/
theorem weight_nonneg_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) : 0 ≤ W := by
  have he2 : (![0, 1, 0] : Fin 3 → ℝ) ≠ 0 := ne_zero_of_apply_ne (i := 1) (by simp)
  have hsum := hf.frame e1 ![0, 1, 0] e3 e1_ne_zero he2 e3_ne_zero
    (by simp [dot3, e1]) (by simp [dot3, e1, e3]) (by simp [dot3, e3])
  linarith [hf.nonneg e1 e1_ne_zero, hf.nonneg ![0, 1, 0] he2, hf.nonneg e3 e3_ne_zero]

/-- Every value of a nonnegative frame function on `ℝ³ \ {0}` is bounded above by the weight `W`. -/
theorem le_weight_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {v : Fin 3 → ℝ} (hv : v ≠ 0) : f v ≤ W := by
  obtain ⟨c, hc0, hcu⟩ := exists_unit_smul hv
  obtain ⟨q', r', hfr'⟩ := exists_orthonormal_completion hcu
  have hu0 : c • v ≠ 0 :=
    ne_zero_of_dot3_self_pos (by rw [show dot3 (c • v) (c • v) = 1 from hcu]; exact one_pos)
  have hq'0 : q' ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr'.qq]; exact one_pos)
  have hr'0 : r' ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr'.rr]; exact one_pos)
  have hfs := hf.frame _ q' r' hu0 hq'0 hr'0 hfr'.pq hfr'.pr hfr'.qr
  rw [hf.scale v hv c hc0] at hfs
  linarith [hf.nonneg q' hq'0, hf.nonneg r' hr'0]

/-- Automatic `[0, W]` boundedness of a nonnegative frame function on `ℝ³ \ {0}` (without continuity). -/
theorem bounded_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {v : Fin 3 → ℝ} (hv : v ≠ 0) :
    0 ≤ f v ∧ f v ≤ W :=
  ⟨hf.nonneg v hv, le_weight_of_nonneg hf hv⟩

/-- Orthogonal pair subadditivity: `f u + f v ≤ W` for orthogonal nonzero `u, v ∈ ℝ³ \ {0}`. -/
theorem ortho_add_le_weight_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {u v : Fin 3 → ℝ}
    (hu : u ≠ 0) (hv : v ≠ 0) (huv : dot3 u v = 0) :
    f u + f v ≤ W := by
  have hcr : cross3 u v ≠ 0 := by
    apply ne_zero_of_dot3_self_pos
    rw [dot3_cross3_self, huv]
    have hu' := dot3_self_pos hu
    have hv' := dot3_self_pos hv
    nlinarith
  have hsum := hf.frame u v (cross3 u v) hu hv hcr huv (dot3_cross3_left u v) (dot3_cross3_right u v)
  linarith [hf.nonneg (cross3 u v) hcr]

/-- Orthogonal pair bound: `f v ≤ W - f u` for orthogonal nonzero `u, v ∈ ℝ³ \ {0}`. -/
theorem ortho_le_weight_sub_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {u v : Fin 3 → ℝ}
    (hu : u ≠ 0) (hv : v ≠ 0) (huv : dot3 u v = 0) :
    f v ≤ W - f u := by
  linarith [ortho_add_le_weight_of_nonneg hf hu hv huv]

/-- Equatorial vanishing at a pole attaining weight `W`: if `f p = W`, then `f v = 0` for all
nonzero `v ⊥ p`. -/
theorem eq_zero_on_perp_of_pole_eq_weight {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {p : Fin 3 → ℝ} (hp : p ≠ 0) (hpW : f p = W)
    {v : Fin 3 → ℝ} (hv : v ≠ 0) (hvp : dot3 v p = 0) :
    f v = 0 := by
  have hpv : dot3 p v = 0 := by rw [dot3_comm]; exact hvp
  have hle := ortho_add_le_weight_of_nonneg hf hp hv hpv
  have hnn := hf.nonneg v hv
  linarith

/-- General Piron tangent-step inequality for any nonnegative frame function (without assuming
`f` is constant on the equator): `f (tangentStep a t) ≤ f a + f (tangentDir a)`. -/
theorem tangentStep_le_add_equator_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) (a : Fin 3 → ℝ) (hr : a 1 ^ 2 + a 2 ^ 2 ≠ 0) (t : ℝ) :
    f (tangentStep a t) ≤ f a + f (tangentDir a) := by
  have hr' : 0 < a 1 ^ 2 + a 2 ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm hr)
  let u : Fin 3 → ℝ := tangentDir a
  let n : Fin 3 → ℝ := ![a 1 ^ 2 + a 2 ^ 2, -(a 0 * a 1), -(a 0 * a 2)]
  let b : Fin 3 → ℝ := ![a 0, a 1 - t * a 2, a 2 + t * a 1]
  let b₂ : Fin 3 → ℝ := ![-(t * (a 1 ^ 2 + a 2 ^ 2)) * a 0,
    -(a 0 ^ 2 + a 1 ^ 2 + a 2 ^ 2) * a 2 - t * (a 1 ^ 2 + a 2 ^ 2) * a 1,
    (a 0 ^ 2 + a 1 ^ 2 + a 2 ^ 2) * a 1 - t * (a 1 ^ 2 + a 2 ^ 2) * a 2]
  have hb : tangentStep a t = b := by rw [tangentStep_apply]
  have ha0 : a ≠ 0 := ne_zero_of_dot3_self_pos (by unfold dot3; nlinarith [sq_nonneg (a 0)])
  have hu0 : u ≠ 0 := ne_zero_of_dot3_self_pos (by simp only [dot3, u, tangentDir]; simp; nlinarith)
  have hn0 : n ≠ 0 := ne_zero_of_apply_ne (i := 0) (by simpa [n] using hr)
  have hb0 : b ≠ 0 := ne_zero_of_dot3_self_pos (by
    simp only [dot3, b]; simp
    nlinarith [sq_nonneg (a 0), mul_nonneg (sq_nonneg t) hr'.le])
  have hb₂0 : b₂ ≠ 0 := by
    intro h
    have h1 := congrFun h 1
    have h2 := congrFun h 2
    simp [b₂] at h1 h2
    have : (a 0 ^ 2 + a 1 ^ 2 + a 2 ^ 2) * (a 1 ^ 2 + a 2 ^ 2) = 0 := by
      linear_combination (-(a 2)) * h1 + a 1 * h2
    rcases mul_eq_zero.mp this with h3 | h3
    · nlinarith [sq_nonneg (a 0)]
    · exact hr h3
  have key := pair_sum_eq_of_common_normal hf.toIsFrameFunction ha0 hu0 hb0 hb₂0 hn0
    (by simp [dot3, u, tangentDir]; ring) (by simp [dot3, n]; ring)
    (by simp [dot3, u, tangentDir, n]; ring)
    (by simp [dot3, b, b₂]; ring) (by simp [dot3, b, n]; ring) (by simp [dot3, b₂, n]; ring)
  have hb₂_nn : 0 ≤ f b₂ := hf.nonneg b₂ hb₂0
  rw [hb]
  linarith

/-- General Piron tangent-step bound in terms of the pole deficit `W - f e1`: for any nonnegative
frame function, `f (tangentStep a t) - f a ≤ W - f e1`. -/
theorem tangentStep_sub_le_weight_sub_pole_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) (a : Fin 3 → ℝ) (hr : a 1 ^ 2 + a 2 ^ 2 ≠ 0) (t : ℝ) :
    f (tangentStep a t) - f a ≤ W - f e1 := by
  have hstep := tangentStep_le_add_equator_of_nonneg hf a hr t
  have hr' : 0 < a 1 ^ 2 + a 2 ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm hr)
  have hu0 : tangentDir a ≠ 0 :=
    ne_zero_of_dot3_self_pos (by simp only [dot3, tangentDir]; simp; nlinarith)
  have heq : f (tangentDir a) ≤ W - f e1 :=
    ortho_le_weight_sub_of_nonneg hf e1_ne_zero hu0 (by simp [dot3, e1, tangentDir])
  linarith

/-- Continuity-free Lemma 1(iv) at the pole: if `f` has maximum at `e1` and is constant `m` on the
equator `{v 0 = 0}`, then `m ≤ f v` for every nonzero `v` (without assuming `ContinuousOn f`). -/
theorem equator_const_is_min_of_max {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → m ≤ f v := by
  intro v hv
  by_cases hrs : v 1 ^ 2 + v 2 ^ 2 = 0
  · have hv1 : v 1 = 0 := by nlinarith [sq_nonneg (v 1), sq_nonneg (v 2)]
    have hv2 : v 2 = 0 := by nlinarith [sq_nonneg (v 1), sq_nonneg (v 2)]
    have hv0 : v 0 ≠ 0 := by
      intro h0; apply hv; ext i; fin_cases i <;> simp [h0, hv1, hv2]
    have hve : v = (v 0) • e1 := by ext i; fin_cases i <;> simp [e1, hv1, hv2]
    have he2 : (![0, 1, 0] : Fin 3 → ℝ) ≠ 0 := ne_zero_of_apply_ne (i := 1) (by simp)
    have h1 := heq ![0, 1, 0] he2 (by simp)
    have h2 := hmax ![0, 1, 0] he2
    rw [hve, hf.scale e1 e1_ne_zero (v 0) hv0]
    linarith
  · let s' : Fin 3 → ℝ := ![0, v 1, v 2]
    let s'' : Fin 3 → ℝ := ![v 1 ^ 2 + v 2 ^ 2, -(v 0 * v 1), -(v 0 * v 2)]
    let n : Fin 3 → ℝ := ![0, -(v 2), v 1]
    have hs' : s' ≠ 0 := ne_zero_of_transverse_ne (by simpa [s'] using hrs)
    have hs'' : s'' ≠ 0 := ne_zero_of_apply_ne (i := 0) (by simpa [s''] using hrs)
    have hn : n ≠ 0 := ne_zero_of_transverse_ne (by simp [n]; intro h; apply hrs; linarith)
    have key := pair_sum_eq_of_common_normal hf e1_ne_zero hs' hv hs'' hn
      (by simp [dot3, e1, s']) (by simp [dot3, e1, n]) (by simp [dot3, s', n]; ring)
      (by simp [dot3, s'']; ring) (by simp [dot3, n]; ring) (by simp [dot3, s'', n]; ring)
    have h1 := heq s' hs' (by simp [s'])
    have h2 := hmax s'' hs''
    linarith

/-- Shared-normal frame construction for `x, y ≥ 0` with `0 < x + y ≤ 1`: in the plane spanned by
`q = refPt (x + y)` and `r = e3` (orthogonal to `w = ![√(1 - s), -√s, 0]`), the rotated pair
`u = √(x / s) • q + √(y / s) • r` and `v = √(y / s) • q - √(x / s) • r` is orthogonal, shares the
common normal `w` with `(refPt (x + y), e3)`, and has latitudes `lat u = x` and `lat v = y`. -/
theorem exists_common_normal_lat_add {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y)
    (hs0 : 0 < x + y) (hs1 : x + y ≤ 1) :
    ∃ u v w : Fin 3 → ℝ, u ≠ 0 ∧ v ≠ 0 ∧ w ≠ 0 ∧
      dot3 (refPt (x + y)) e3 = 0 ∧ dot3 (refPt (x + y)) w = 0 ∧ dot3 e3 w = 0 ∧
      dot3 u v = 0 ∧ dot3 u w = 0 ∧ dot3 v w = 0 ∧
      lat u = x ∧ lat v = y := by
  set s := x + y with hs
  have hs_nonneg : 0 ≤ s := hs0.le
  have h1s_nonneg : 0 ≤ 1 - s := sub_nonneg.mpr hs1
  set a := Real.sqrt (x / s) with ha
  set b := Real.sqrt (y / s) with hb
  have ha2 : a ^ 2 = x / s := Real.sq_sqrt (div_nonneg hx hs_nonneg)
  have hb2 : b ^ 2 = y / s := Real.sq_sqrt (div_nonneg hy hs_nonneg)
  have hab : a ^ 2 + b ^ 2 = 1 := by
    rw [ha2, hb2, ← add_div, ← hs, div_self hs0.ne']
  let q : Fin 3 → ℝ := refPt s
  let w : Fin 3 → ℝ := ![Real.sqrt (1 - s), -Real.sqrt s, 0]
  let u : Fin 3 → ℝ := a • q + b • e3
  let v : Fin 3 → ℝ := b • q - a • e3
  have hqq : Real.sqrt s * Real.sqrt s + Real.sqrt (1 - s) * Real.sqrt (1 - s) = 1 := by
    have := refPt_dot3 hs_nonneg hs1
    simpa [dot3, refPt] using this
  have hww : dot3 w w = 1 := by
    simp [dot3, w, ← sq, Real.sq_sqrt hs_nonneg, Real.sq_sqrt h1s_nonneg]
  have huu : dot3 u u = 1 := by
    simp [u, q, refPt, e3, dot3]
    linear_combination a ^ 2 * hqq + hab
  have hvv : dot3 v v = 1 := by
    simp [v, q, refPt, e3, dot3]
    linear_combination b ^ 2 * hqq + hab
  have huv : dot3 u v = 0 := by
    simp [u, v, q, refPt, e3, dot3]
    linear_combination (a * b) * hqq
  have huw : dot3 u w = 0 := by
    simp [u, q, refPt, e3, w, dot3]; ring
  have hvw : dot3 v w = 0 := by
    simp [v, q, refPt, e3, w, dot3]; ring
  have hlu : lat u = x := by
    rw [lat, huu, div_one]
    have hu0 : u 0 = a * Real.sqrt s := by simp [u, q, refPt, e3]
    rw [hu0, mul_pow, ha2, Real.sq_sqrt hs_nonneg, div_mul_cancel₀ _ hs0.ne']
  have hlv : lat v = y := by
    rw [lat, hvv, div_one]
    have hv0 : v 0 = b * Real.sqrt s := by simp [v, q, refPt, e3]
    rw [hv0, mul_pow, hb2, Real.sq_sqrt hs_nonneg, div_mul_cancel₀ _ hs0.ne']
  refine ⟨u, v, w,
    ne_zero_of_dot3_self_pos (by rw [huu]; exact one_pos),
    ne_zero_of_dot3_self_pos (by rw [hvv]; exact one_pos),
    ne_zero_of_dot3_self_pos (by rw [hww]; exact one_pos),
    by simp [dot3, refPt, e3],
    by simp [dot3, refPt, w]; ring,
    by simp [dot3, e3, w],
    huv, huw, hvw, hlu, hlv⟩

/-- If `f` is constant `m` on the equator `{v 0 = 0}`, then for any `x, y ≥ 0` with `0 < x + y ≤ 1`
there exist nonzero vectors `u, v` with `lat u = x`, `lat v = y`, and
`(f u - m) + (f v - m) = f (refPt (x + y)) - m`. -/
theorem exists_lat_pair_sum_eq_refPt {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (hs0 : 0 < x + y) (hs1 : x + y ≤ 1) :
    ∃ u v : Fin 3 → ℝ, u ≠ 0 ∧ v ≠ 0 ∧ lat u = x ∧ lat v = y ∧
      (f u - m) + (f v - m) = f (refPt (x + y)) - m := by
  obtain ⟨u, v, w, hu, hv, hw, hqe3, hqw, he3w, huv, huw, hvw, hlu, hlv⟩ :=
    exists_common_normal_lat_add hx hy hs0 hs1
  have hq : refPt (x + y) ≠ 0 := refPt_ne_zero hs0.le hs1
  have hsum := pair_sum_eq_of_common_normal hf hq e3_ne_zero hu hv hw hqe3 hqw he3w huv huw hvw
  have he3m : f e3 = m := heq e3 e3_ne_zero (by simp [e3])
  refine ⟨u, v, hu, hv, hlu, hlv, by linarith⟩

/-- Strict lower-latitude superadditivity of `l ↦ f (refPt l) - m` (without continuity). -/
lemma refPt_sub_add_le_of_lt {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    {x' x y' y : ℝ} (hx' : 0 ≤ x') (hxx : x' < x) (hy' : 0 ≤ y') (hyy : y' < y)
    (hxy : x + y ≤ 1) :
    (f (refPt x') - m) + (f (refPt y') - m) ≤ f (refPt (x + y)) - m := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  obtain ⟨u, v, hu, hv, hlu, hlv, hsum⟩ :=
    exists_lat_pair_sum_eq_refPt hf heq (by linarith) (by linarith) (by linarith) hxy
  have hx1 : x' ≤ 1 := by linarith
  have hy1 : y' ≤ 1 := by linarith
  have hu_le : f (refPt x') ≤ f u :=
    le_of_lat_lt hf hmax heq hmin hu (refPt_ne_zero hx' hx1)
      (by rw [lat_refPt hx' hx1, hlu]; exact hxx)
  have hv_le : f (refPt y') ≤ f v :=
    le_of_lat_lt hf hmax heq hmin hv (refPt_ne_zero hy' hy1)
      (by rw [lat_refPt hy' hy1, hlv]; exact hyy)
  linarith

/-- Strict upper-latitude subadditivity of `l ↦ f (refPt l) - m` (without continuity). -/
lemma refPt_sub_le_add_of_lt {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    {x x'' y y'' : ℝ} (hx : 0 < x) (hxx : x < x'') (hx1 : x'' ≤ 1)
    (hy : 0 < y) (hyy : y < y'') (hy1 : y'' ≤ 1) (hxy : x + y ≤ 1) :
    f (refPt (x + y)) - m ≤ (f (refPt x'') - m) + (f (refPt y'') - m) := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  obtain ⟨u, v, hu, hv, hlu, hlv, hsum⟩ :=
    exists_lat_pair_sum_eq_refPt hf heq hx.le hy.le (by linarith) hxy
  have hx''0 : 0 ≤ x'' := by linarith
  have hy''0 : 0 ≤ y'' := by linarith
  have hu_le : f u ≤ f (refPt x'') :=
    le_of_lat_lt hf hmax heq hmin (refPt_ne_zero hx''0 hx1) hu
      (by rw [lat_refPt hx''0 hx1, hlu]; exact hxx)
  have hv_le : f v ≤ f (refPt y'') :=
    le_of_lat_lt hf hmax heq hmin (refPt_ne_zero hy''0 hy1) hv
      (by rw [lat_refPt hy''0 hy1, hlv]; exact hyy)
  linarith

/-- Iterated lower-latitude bound: for `k ≥ 1` and `0 ≤ a < b` with `k * b ≤ 1`,
`k * (f (refPt a) - m) ≤ f (refPt (k * b)) - m`. -/
lemma nat_mul_refPt_sub_le {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ∀ k : ℕ, 0 < k → ∀ a b : ℝ, 0 ≤ a → a < b → (k : ℝ) * b ≤ 1 →
      (k : ℝ) * (f (refPt a) - m) ≤ f (refPt ((k : ℝ) * b)) - m := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  intro k
  induction k with
  | zero => intro hk; omega
  | succ k ih =>
    intro _ a b ha hab hkb
    by_cases hk0 : k = 0
    · subst hk0
      simp only [zero_add, Nat.cast_one, one_mul] at hkb ⊢
      have hb0 : 0 ≤ b := by linarith
      have ha1 : a ≤ 1 := by linarith
      have hle := le_of_lat_lt hf hmax heq hmin (refPt_ne_zero hb0 hkb) (refPt_ne_zero ha ha1)
        (by rw [lat_refPt ha ha1, lat_refPt hb0 hkb]; exact hab)
      linarith
    · have hkpos : 0 < k := Nat.pos_of_ne_zero hk0
      have hkR : (0 : ℝ) < k := Nat.cast_pos.mpr hkpos
      set b' := (a + b) / 2 with hb'
      have hab' : a < b' := by linarith
      have hb'b : b' < b := by linarith
      have hb'0 : 0 ≤ b' := by linarith
      have hkb_split : (k : ℝ) * b + b = ((k + 1 : ℕ) : ℝ) * b := by push_cast; ring
      have hkb_le : (k : ℝ) * b' ≤ 1 := by
        have : (k : ℝ) * b' < (k : ℝ) * b := mul_lt_mul_of_pos_left hb'b hkR
        have : (k : ℝ) * b + b ≤ 1 := by linarith
        linarith
      have h1 := ih hkpos a b' ha hab' hkb_le
      have h2 := refPt_sub_add_le_of_lt hf hmax heq (mul_nonneg hkR.le hb'0)
        (mul_lt_mul_of_pos_left hb'b hkR) ha hab (by linarith)
      rw [hkb_split] at h2
      have hcast : ((k + 1 : ℕ) : ℝ) * (f (refPt a) - m) =
          (k : ℝ) * (f (refPt a) - m) + (f (refPt a) - m) := by push_cast; ring
      linarith

/-- Iterated upper-latitude bound: for `k ≥ 1` and `0 < a < b ≤ 1` with `k * a ≤ 1`,
`f (refPt (k * a)) - m ≤ k * (f (refPt b) - m)`. -/
lemma refPt_sub_le_nat_mul {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ∀ k : ℕ, 0 < k → ∀ a b : ℝ, 0 < a → a < b → b ≤ 1 → (k : ℝ) * a ≤ 1 →
      f (refPt ((k : ℝ) * a)) - m ≤ (k : ℝ) * (f (refPt b) - m) := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  intro k
  induction k with
  | zero => intro hk; omega
  | succ k ih =>
    intro _ a b ha hab hb1 hka
    by_cases hk0 : k = 0
    · subst hk0
      simp only [zero_add, Nat.cast_one, one_mul] at hka ⊢
      have hb0 : 0 ≤ b := by linarith
      have hle := le_of_lat_lt hf hmax heq hmin (refPt_ne_zero hb0 hb1) (refPt_ne_zero ha.le hka)
        (by rw [lat_refPt ha.le hka, lat_refPt hb0 hb1]; exact hab)
      linarith
    · have hkpos : 0 < k := Nat.pos_of_ne_zero hk0
      have hkR : (0 : ℝ) < k := Nat.cast_pos.mpr hkpos
      have hka_split : (k : ℝ) * a + a = ((k + 1 : ℕ) : ℝ) * a := by push_cast; ring
      have hka_lt1 : (k : ℝ) * a < 1 := by linarith
      have hkab : (k : ℝ) * a < (k : ℝ) * b := mul_lt_mul_of_pos_left hab hkR
      set M := min ((k : ℝ) * b) 1 with hM
      have hkaM : (k : ℝ) * a < M := lt_min hkab hka_lt1
      have hM1 : M ≤ 1 := min_le_right _ _
      have hMb : M ≤ (k : ℝ) * b := min_le_left _ _
      set x'' := ((k : ℝ) * a + M) / 2 with hx''
      have hx''_gt : (k : ℝ) * a < x'' := by linarith
      have hx''_lt : x'' < M := by linarith
      set a' := x'' / k with ha'
      have hka' : (k : ℝ) * a' = x'' := mul_div_cancel₀ x'' hkR.ne'
      have haa' : a < a' := by
        apply lt_of_mul_lt_mul_left _ hkR.le
        rw [hka']
        exact hx''_gt
      have ha'b : a' < b := by
        apply lt_of_mul_lt_mul_left _ hkR.le
        rw [hka']
        exact lt_of_lt_of_le hx''_lt hMb
      have h1 := ih hkpos a' b (by linarith) ha'b hb1 (by linarith)
      have hx''_gt' : (k : ℝ) * a < (k : ℝ) * a' := by rw [hka']; exact hx''_gt
      have hx''_le1 : (k : ℝ) * a' ≤ 1 := by linarith
      have h2 := refPt_sub_le_add_of_lt hf hmax heq (mul_pos hkR ha)
        hx''_gt' hx''_le1 ha hab hb1 (by linarith)
      rw [hka_split] at h2
      have hcast : ((k + 1 : ℕ) : ℝ) * (f (refPt b) - m) =
          (k : ℝ) * (f (refPt b) - m) + (f (refPt b) - m) := by push_cast; ring
      linarith

/-- Rational lower and upper bounds at any nonzero vector `w`: for `1 ≤ k ≤ n`,
if `k / n < lat w` then `(k / n) * (f e1 - m) ≤ f w - m`, and if `lat w < k / n` then
`f w - m ≤ (k / n) * (f e1 - m)` (without assuming `ContinuousOn f`). -/
lemma rat_mul_pole_sub_bounds_of_lat {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    {n k : ℕ} (hn : 0 < n) (hk : 0 < k) (hkn : k ≤ n) {w : Fin 3 → ℝ} (hw : w ≠ 0) :
    ((k : ℝ) / n < lat w → (k : ℝ) / n * (f e1 - m) ≤ f w - m) ∧
    (lat w < (k : ℝ) / n → f w - m ≤ (k : ℝ) / n * (f e1 - m)) := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  have hnR : (0 : ℝ) < n := Nat.cast_pos.mpr hn
  have hkR : (0 : ℝ) < k := Nat.cast_pos.mpr hk
  have hknR : (k : ℝ) / n ≤ 1 := (div_le_one hnR).mpr (by exact_mod_cast hkn)
  have hxw0 : 0 ≤ lat w := lat_nonneg w
  have hxw1 : lat w ≤ 1 := lat_le_one hw
  constructor
  · intro hlt
    set b := ((k : ℝ) / n + lat w) / 2 with hb
    have hkb : (k : ℝ) / n < b := by linarith
    have hbw : b < lat w := by linarith
    have hb1 : b ≤ 1 := by linarith
    have hb_div : 1 / (n : ℝ) < b / k := by
      rw [div_lt_div_iff₀ hnR hkR]
      have : (k : ℝ) < b * n := (div_lt_iff₀ hnR).mp hkb
      linarith
    set a := (1 / (n : ℝ) + b / k) / 2 with ha
    have h1a : 1 / (n : ℝ) < a := by linarith
    have habk : a < b / k := by linarith
    have ha1 : a ≤ 1 := by
      have : b / k ≤ 1 := by
        rw [div_le_one hkR]
        have : (1 : ℝ) ≤ k := by exact_mod_cast hk
        linarith
      linarith
    have hlow1 : f e1 - m ≤ (n : ℝ) * (f (refPt a) - m) := by
      have := refPt_sub_le_nat_mul hf hmax heq n hn (1 / (n : ℝ)) a
        (div_pos one_pos hnR) h1a ha1 (by rw [mul_one_div_cancel hnR.ne'])
      rwa [mul_one_div_cancel hnR.ne', refPt_one] at this
    have hlow2 : (k : ℝ) * (f (refPt a) - m) ≤ f (refPt b) - m := by
      have := nat_mul_refPt_sub_le hf hmax heq k hk a (b / k) (by positivity) habk
        (by rw [mul_div_cancel₀ b hkR.ne']; exact hb1)
      rwa [mul_div_cancel₀ b hkR.ne'] at this
    have hlow3 : f (refPt b) ≤ f w :=
      le_of_lat_lt hf hmax heq hmin hw (refPt_ne_zero (by positivity) hb1)
        (by rw [lat_refPt (by positivity) hb1]; exact hbw)
    have hlow1' : (f e1 - m) / n ≤ f (refPt a) - m := (div_le_iff₀ hnR).mpr (by linarith)
    have hlow2' : (k : ℝ) * ((f e1 - m) / n) ≤ (k : ℝ) * (f (refPt a) - m) :=
      mul_le_mul_of_nonneg_left hlow1' hkR.le
    have h_eq : (k : ℝ) / n * (f e1 - m) = (k : ℝ) * ((f e1 - m) / n) := by ring
    linarith
  · intro hlt
    set a := (lat w + (k : ℝ) / n) / 2 with ha
    have hwa : lat w < a := by linarith
    have hak : a < (k : ℝ) / n := by linarith
    have ha0 : 0 < a := by positivity
    have ha1 : a ≤ 1 := by linarith
    have ha_div : a / k < 1 / (n : ℝ) := by
      rw [div_lt_div_iff₀ hkR hnR]
      have : a * n < (k : ℝ) := (lt_div_iff₀ hnR).mp hak
      linarith
    set b := (a / k + 1 / (n : ℝ)) / 2 with hb
    have hab : a / k < b := by linarith
    have hb1n : b < 1 / (n : ℝ) := by linarith
    have hb1 : b ≤ 1 := by
      have : 1 / (n : ℝ) ≤ 1 := div_le_one_of_le₀ (by exact_mod_cast hn) hnR.le
      linarith
    have hup1 : f w ≤ f (refPt a) :=
      le_of_lat_lt hf hmax heq hmin (refPt_ne_zero ha0.le ha1) hw
        (by rw [lat_refPt ha0.le ha1]; exact hwa)
    have hup2 : f (refPt a) - m ≤ (k : ℝ) * (f (refPt b) - m) := by
      have := refPt_sub_le_nat_mul hf hmax heq k hk (a / k) b (div_pos ha0 hkR) hab hb1
        (by rw [mul_div_cancel₀ a hkR.ne']; exact ha1)
      rwa [mul_div_cancel₀ a hkR.ne'] at this
    have hup3 : (n : ℝ) * (f (refPt b) - m) ≤ f e1 - m := by
      have := nat_mul_refPt_sub_le hf hmax heq n hn b (1 / (n : ℝ)) (by positivity) hb1n
        (by rw [mul_one_div_cancel hnR.ne'])
      rwa [mul_one_div_cancel hnR.ne', refPt_one] at this
    have hup3' : f (refPt b) - m ≤ (f e1 - m) / n := (le_div_iff₀ hnR).mpr (by linarith)
    have hup2' : (k : ℝ) * (f (refPt b) - m) ≤ (k : ℝ) * ((f e1 - m) / n) :=
      mul_le_mul_of_nonneg_left hup3' hkR.le
    have h_eq : (k : ℝ) / n * (f e1 - m) = (k : ℝ) * ((f e1 - m) / n) := by ring
    linarith

/-- **Continuity-free Proposition 1 at the pole.**  Every frame function on `ℝ³ \ {0}` with its
maximum at `e1` and constant `m` on the equator `{v 0 = 0}` equals `m + (f e1 - m) * lat v` on
all nonzero vectors, with zero continuity assumption on `f`. -/
theorem prop1_pole_of_max {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → f v = m + (f e1 - m) * lat v := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  have hM : 0 ≤ f e1 - m := by linarith [hmin e1 e1_ne_zero]
  intro v hv
  by_cases hv0 : v 0 = 0
  · have hlat0 : lat v = 0 := by simp [lat, hv0]
    rw [heq v hv hv0, hlat0]; ring
  by_cases hrv : v 1 ^ 2 + v 2 ^ 2 = 0
  · have hv1 : v 1 = 0 := by nlinarith [sq_nonneg (v 1), sq_nonneg (v 2)]
    have hv2 : v 2 = 0 := by nlinarith [sq_nonneg (v 1), sq_nonneg (v 2)]
    have hve : v = (v 0) • e1 := by ext i; fin_cases i <;> simp [e1, hv1, hv2]
    rw [hve, hf.scale e1 e1_ne_zero (v 0) hv0, lat_smul e1 hv0, lat_e1]; ring
  -- Generic case: `0 < lat v < 1`, sandwiched by rationals `(k ± 1) / n`
  set x := lat v with hx
  have hx0 : 0 < x := div_pos (sq_pos_of_ne_zero hv0) (dot3_self_pos hv)
  have hx1 : x < 1 := by
    rw [hx, lat, div_lt_one (dot3_self_pos hv)]
    unfold dot3
    have : 0 < v 1 ^ 2 + v 2 ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm hrv)
    nlinarith
  have hbound : ∀ n : ℕ, 0 < n → |(f v - m) - x * (f e1 - m)| ≤ 2 * (f e1 - m) / n := by
    intro n hn
    have hnR : (0 : ℝ) < n := Nat.cast_pos.mpr hn
    set k := ⌊(n : ℝ) * x⌋₊ with hk
    have hk0 : (k : ℝ) ≤ (n : ℝ) * x := Nat.floor_le (by positivity)
    have hk1 : (n : ℝ) * x < (k : ℝ) + 1 := Nat.lt_floor_add_one _
    have hlow : x * (f e1 - m) - (f v - m) ≤ 2 * (f e1 - m) / n := by
      by_cases hk_pos : 0 < k
      · by_cases hk1_pos : 0 < k - 1
        · have hkn1 : k - 1 ≤ n := by
            have : (k : ℝ) ≤ n := le_trans hk0 (by nlinarith)
            have hk_le : k ≤ n := by exact_mod_cast this
            omega
          have hk_sub : ((k - 1 : ℕ) : ℝ) + 1 = (k : ℝ) := by
            exact_mod_cast Nat.sub_add_cancel hk_pos
          have hlt : ((k - 1 : ℕ) : ℝ) / n < x := by
            rw [div_lt_iff₀ hnR]
            linarith
          have hb := (rat_mul_pole_sub_bounds_of_lat hf hmax heq hn hk1_pos hkn1 hv).1 hlt
          have hsub : x - ((k - 1 : ℕ) : ℝ) / n ≤ 2 / n := by
            have heq_sub : x - ((k - 1 : ℕ) : ℝ) / n = (x * n - ((k - 1 : ℕ) : ℝ)) / n := by
              field_simp
            rw [heq_sub, div_le_div_iff_of_pos_right hnR]
            linarith
          have hmul : (x - ((k - 1 : ℕ) : ℝ) / n) * (f e1 - m) ≤ (2 / n) * (f e1 - m) :=
            mul_le_mul_of_nonneg_right hsub hM
          have heq_rhs : (2 / (n : ℝ)) * (f e1 - m) = 2 * (f e1 - m) / n := by ring
          linarith
        · have hk_le1 : k ≤ 1 := by omega
          have hnx : (n : ℝ) * x < 2 := by
            have : (k : ℝ) ≤ 1 := by exact_mod_cast hk_le1
            linarith
          have hx_le : x ≤ 2 / n := (le_div_iff₀ hnR).mpr (by linarith)
          have hmul : x * (f e1 - m) ≤ (2 / n) * (f e1 - m) :=
            mul_le_mul_of_nonneg_right hx_le hM
          have heq_rhs : (2 / (n : ℝ)) * (f e1 - m) = 2 * (f e1 - m) / n := by ring
          have hfv : 0 ≤ f v - m := by linarith [hmin v hv]
          linarith
      · have hk_eq0 : k = 0 := by omega
        have hnx : (n : ℝ) * x < 1 := by rw [hk_eq0] at hk1; simpa using hk1
        have hx_le : x ≤ 2 / n := (le_div_iff₀ hnR).mpr (by linarith)
        have hmul : x * (f e1 - m) ≤ (2 / n) * (f e1 - m) :=
          mul_le_mul_of_nonneg_right hx_le hM
        have heq_rhs : (2 / (n : ℝ)) * (f e1 - m) = 2 * (f e1 - m) / n := by ring
        have hfv : 0 ≤ f v - m := by linarith [hmin v hv]
        linarith
    have hup : (f v - m) - x * (f e1 - m) ≤ 2 * (f e1 - m) / n := by
      by_cases hkn2 : k + 2 ≤ n
      · have hk_add : ((k + 2 : ℕ) : ℝ) = (k : ℝ) + 2 := by push_cast; ring
        have hlt : x < ((k + 2 : ℕ) : ℝ) / n := by
          rw [lt_div_iff₀ hnR]
          linarith
        have hb := (rat_mul_pole_sub_bounds_of_lat hf hmax heq hn (by omega) hkn2 hv).2 hlt
        have hsub : ((k + 2 : ℕ) : ℝ) / n - x ≤ 2 / n := by
          have heq_sub : ((k + 2 : ℕ) : ℝ) / n - x = (((k + 2 : ℕ) : ℝ) - x * n) / n := by
            field_simp
          rw [heq_sub, div_le_div_iff_of_pos_right hnR]
          linarith
        have hmul : (((k + 2 : ℕ) : ℝ) / n - x) * (f e1 - m) ≤ (2 / n) * (f e1 - m) :=
          mul_le_mul_of_nonneg_right hsub hM
        have heq_rhs : (2 / (n : ℝ)) * (f e1 - m) = 2 * (f e1 - m) / n := by ring
        linarith
      · have hn_le : n ≤ k + 1 := by omega
        have hnR_le : (n : ℝ) ≤ (k : ℝ) + 1 := by exact_mod_cast hn_le
        have h1x : 1 - x ≤ 2 / n := by
          rw [le_div_iff₀ hnR]
          linarith
        have hmul : (1 - x) * (f e1 - m) ≤ (2 / n) * (f e1 - m) :=
          mul_le_mul_of_nonneg_right h1x hM
        have heq_rhs : (2 / (n : ℝ)) * (f e1 - m) = 2 * (f e1 - m) / n := by ring
        have hfv : f v ≤ f e1 := hmax v hv
        linarith
    rw [abs_le]
    exact ⟨by linarith, hup⟩
  suffices h0 : (f v - m) - x * (f e1 - m) = 0 by linarith
  by_contra hne
  have hpos : 0 < |(f v - m) - x * (f e1 - m)| := abs_pos.mpr hne
  obtain ⟨n, hn⟩ := exists_nat_gt (2 * (f e1 - m) / |(f v - m) - x * (f e1 - m)|)
  have hn0 : 0 < n := by
    have : (0 : ℝ) ≤ 2 * (f e1 - m) / |(f v - m) - x * (f e1 - m)| :=
      div_nonneg (by linarith) hpos.le
    exact_mod_cast lt_of_le_of_lt this hn
  have hn' : (0 : ℝ) < n := Nat.cast_pos.mpr hn0
  have h1 := hbound n hn0
  rw [div_lt_iff₀ hpos] at hn
  rw [le_div_iff₀ hn'] at h1
  linarith

/-- Automatic continuity of any frame function on `ℝ³ \ {0}` that has its maximum at `e1` and is
constant on the equator `{v 0 = 0}`. -/
theorem continuousOn_of_max_and_equator_const {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ}
    (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ContinuousOn f {v | v ≠ 0} := by
  refine (continuousOn_stdQuad (f e1) m m).congr fun v hv => ?_
  have hp := prop1_pole_of_max hf hmax heq v hv
  have hD : dot3 v v ≠ 0 := (dot3_self_pos hv).ne'
  rw [hp, stdQuad, lat]
  field_simp [hD]
  unfold dot3
  ring

/-- **Continuity-free Proposition 1 at an arbitrary unit pole `p`.**  Every frame function on
`ℝ³ \ {0}` with its maximum at a unit vector `p` and constant `m` on `p⊥` is
`m + (f p - m) * (⟨v, p⟩² / ⟨v, v⟩)`, without assuming continuity of `f`. -/
theorem prop1_of_max {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    {p : Fin 3 → ℝ} (hp : dot3 p p = 1)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → dot3 v p = 0 → f v = m) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → f v = m + (f p - m) * (dot3 v p ^ 2 / dot3 v v) := by
  obtain ⟨q, r, h⟩ := exists_orthonormal_completion hp
  have hF := hf.comp_ofFrame h
  have hmaxF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f (ofFrame p q r v)) v ≤ (fun v => f (ofFrame p q r v)) e1 := by
    intro v hv
    simp only [ofFrame_e1]
    exact hmax _ (ofFrame_ne_zero h hv)
  have heqF : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → (fun v => f (ofFrame p q r v)) v = m := by
    intro v hv hv0
    exact heq _ (ofFrame_ne_zero h hv) (by rw [(dot3_ofFrame_left h v).1]; exact hv0)
  have key := prop1_pole_of_max hF hmaxF heqF
  intro w hw
  have := key (toFrame p q r w) (toFrame_ne_zero h hw)
  simp only [ofFrame_e1, ofFrame_toFrame h] at this
  rw [this, lat, dot3_toFrame_self h]
  simp [toFrame]

/-- Continuity-free (4.5): with the maximum at `e1`, `f + f ∘ phat` is an explicit function of
`lat v` without assuming continuity of `f`. -/
theorem sum_phat_of_max {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 →
      f v + f (phat v) = (W - f e1) + (3 * f e1 - W) * lat v := by
  have hF : IsFrameFunction (fun v => f v + f (phat v)) (W + W) := hf.add hf.comp_phat
  have hmaxF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f v + f (phat v)) v ≤ (fun v => f v + f (phat v)) e1 := by
    intro v hv; simp only [phat_e1]
    linarith [hmax v hv, hmax (phat v) (phat_ne_zero hv)]
  have heqF : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 →
      (fun v => f v + f (phat v)) v = W - f e1 := by
    intro v hv hv0
    have := hf.frame e1 v (phat v) e1_ne_zero hv (phat_ne_zero hv)
      (by simp [dot3, e1, hv0]) (by simp [dot3, e1, phat, hv0]) (by simp [dot3, phat, hv0]; ring)
    show f v + f (phat v) = W - f e1
    linarith
  have key := prop1_pole_of_max hF hmaxF heqF
  intro v hv
  have := key v hv
  simp only [phat_e1] at this
  rw [this]; ring

/-- Continuity-free (4.6): with the minimum at `e3`, `f + f ∘ rhat` is an explicit function of
`v 2 ^ 2 / ⟨v, v⟩` without assuming continuity of `f`. -/
theorem sum_rhat_of_min {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → f e3 ≤ f v) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 →
      f v + f (rhat v) = (W - f e3) + (3 * f e3 - W) * (v 2 ^ 2 / dot3 v v) := by
  have hG : IsFrameFunction (fun v => -(f v + f (rhat v))) (-(W + W)) := (hf.add hf.comp_rhat).neg
  have hmaxG : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => -(f v + f (rhat v))) v ≤ (fun v => -(f v + f (rhat v))) e3 := by
    intro v hv; simp only [rhat_e3]
    linarith [hmin v hv, hmin (rhat v) (rhat_ne_zero hv)]
  have heqG : ∀ v : Fin 3 → ℝ, v ≠ 0 → dot3 v e3 = 0 →
      (fun v => -(f v + f (rhat v))) v = -(W - f e3) := by
    intro v hv hv2
    have hv2' : v 2 = 0 := by simpa [dot3, e3] using hv2
    have := hf.frame e3 v (rhat v) e3_ne_zero hv (rhat_ne_zero hv)
      (by simp [dot3, e3, hv2']) (by simp [dot3, e3, rhat, hv2']) (by simp [dot3, rhat, hv2']; ring)
    show -(f v + f (rhat v)) = -(W - f e3)
    linarith
  have key := prop1_of_max hG dot3_e3_self hmaxG heqG
  intro v hv
  have := key v hv
  simp only [rhat_e3] at this
  have e : dot3 v e3 = v 2 := by simp [dot3, e3]
  rw [e] at this
  linarith

/-- Continuity-free Lemma 8 (standard position): with the maximum at `e1` and the minimum at `e3`,
`f` agrees with `stdQuad (f e1) (W - f e1 - f e3) (f e3)` on the six great circles
`x = ±y`, `x = ±z`, `y = ±z` without assuming continuity of `f`. -/
theorem eq_stdQuad_on_six_circles_of_extrema {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → f e3 ≤ f v) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (v 0 = v 1 ∨ v 0 = -v 1 ∨ v 0 = v 2 ∨ v 0 = -v 2 ∨ v 1 = v 2 ∨ v 1 = -v 2) →
      f v = stdQuad (f e1) (W - f e1 - f e3) (f e3) v := by
  set M := f e1 with hM
  set m := f e3 with hm
  set α := W - M - m with hα
  set g := stdQuad M α m with hg
  set h : (Fin 3 → ℝ) → ℝ := fun v => f v - g v with hh
  have hhf : IsFrameFunction h 0 := by
    have := hf.sub (isFrameFunction_stdQuad M α m)
    rwa [show W - (M + α + m) = 0 by rw [hα]; ring] at this
  have hp : ∀ v : Fin 3 → ℝ, v ≠ 0 → h (phat v) = -h v := by
    intro v hv
    have h1 := sum_phat_of_max hf hmax v hv
    have h2 := stdQuad_add_phat M α m hv
    simp only [hh, hg]
    rw [← hM] at h1
    linarith
  have hr : ∀ v : Fin 3 → ℝ, v ≠ 0 → h (rhat v) = -h v := by
    intro v hv
    have h1 := sum_rhat_of_min hf hmin v hv
    have h2 := stdQuad_add_rhat M α m hv
    simp only [hh, hg]
    rw [← hm] at h1
    linarith
  have hneg : ∀ v : Fin 3 → ℝ, v ≠ 0 → h ((-1 : ℝ) • v) = h v :=
    fun v hv => hhf.scale v hv (-1) (by norm_num)
  intro v hv hcirc
  suffices hz : h v = 0 by simp only [hh, hg] at hz; linarith
  rcases hcirc with h01 | h01 | h02 | h02 | h12 | h12
  · have e : phat (phat (rhat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h01]
    have := hp _ (phat_ne_zero (rhat_ne_zero hv))
    rw [e, hneg v hv, hp _ (rhat_ne_zero hv), hr v hv] at this
    linarith
  · have e : rhat (phat (phat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h01]
    have := hr _ (phat_ne_zero (phat_ne_zero hv))
    rw [e, hneg v hv, hp _ (phat_ne_zero hv), hp v hv] at this
    linarith
  · have e : rhat (phat (phat (phat (rhat v)))) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h02]
    have := hr _ (phat_ne_zero (phat_ne_zero (phat_ne_zero (rhat_ne_zero hv))))
    rw [e, hneg v hv, hp _ (phat_ne_zero (phat_ne_zero (rhat_ne_zero hv))),
      hp _ (phat_ne_zero (rhat_ne_zero hv)), hp _ (rhat_ne_zero hv), hr v hv] at this
    linarith
  · have e : phat (rhat (phat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h02]
    have := hp _ (rhat_ne_zero (phat_ne_zero hv))
    rw [e, hneg v hv, hr _ (phat_ne_zero hv), hp v hv] at this
    linarith
  · have e : phat (rhat (rhat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h12]
    have := hp _ (rhat_ne_zero (rhat_ne_zero hv))
    rw [e, hneg v hv, hr _ (rhat_ne_zero hv), hr v hv] at this
    linarith
  · have e : rhat (rhat (phat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h12]
    have := hr _ (rhat_ne_zero (phat_ne_zero hv))
    rw [e, hneg v hv, hr _ (phat_ne_zero hv), hp v hv] at this
    linarith

/-- **Pure-state continuity-free Gleason theorem on `ℝ³`.**  If a nonnegative frame function `f`
of weight `W` attains `W` at a unit vector `p`, then `f v = W * (⟨v, p⟩² / ⟨v, v⟩)` for every
nonzero `v ∈ ℝ³ \ {0}`, without assuming continuity of `f`. -/
theorem pure_state_nonneg_gleason_real {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {p : Fin 3 → ℝ} (hp : dot3 p p = 1) (hpW : f p = W) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → f v = W * (dot3 v p ^ 2 / dot3 v v) := by
  have hp0 : p ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hp]; exact one_pos)
  have hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p := by
    intro v hv
    rw [hpW]
    exact le_weight_of_nonneg hf hv
  have heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → dot3 v p = 0 → f v = 0 :=
    fun v hv hvp => eq_zero_on_perp_of_pole_eq_weight hf hp0 hpW hv hvp
  intro v hv
  have := prop1_of_max hf.toIsFrameFunction hp hmax heq v hv
  rw [this, hpW]
  ring

/-! ### Target 3 (`TFQ-1059`): Supremum/infimum bounds on `S²`, compactness, isotropic deflation, and mixed-state extremum reduction -/

/-- The image `f '' sphere3` of the unit sphere `S²` under any `f` is nonempty (witnessed by `e1`). -/
theorem nonempty_image_sphere3 (f : (Fin 3 → ℝ) → ℝ) :
    (f '' sphere3).Nonempty :=
  ⟨f e1, e1, e1_mem_sphere3, rfl⟩

/-- For any nonnegative frame function `f` of weight `W`, the image `f '' sphere3` is bounded above
by `W` (`W ∈ upperBounds (f '' sphere3)`). -/
theorem bddAbove_image_sphere3_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) :
    BddAbove (f '' sphere3) := by
  refine ⟨W, ?_⟩
  rintro _ ⟨v, hv, rfl⟩
  exact le_weight_of_nonneg hf (sphere3_subset hv)

/-- For any nonnegative frame function `f` of weight `W`, the image `f '' sphere3` is bounded below
by `0` (`0 ∈ lowerBounds (f '' sphere3)`). -/
theorem bddBelow_image_sphere3_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) :
    BddBelow (f '' sphere3) := by
  refine ⟨0, ?_⟩
  rintro _ ⟨v, hv, rfl⟩
  exact hf.nonneg v (sphere3_subset hv)

/-- By scale invariance, every value `f v` (`v ≠ 0`) of a nonnegative frame function is bounded above
by the unit-sphere supremum `sSup (f '' sphere3)`. -/
theorem le_sSup_sphere3_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {v : Fin 3 → ℝ} (hv : v ≠ 0) :
    f v ≤ sSup (f '' sphere3) := by
  obtain ⟨c, hc0, hcv⟩ := exists_unit_smul hv
  rw [← hf.scale v hv c hc0]
  exact le_csSup (bddAbove_image_sphere3_of_nonneg hf) ⟨c • v, hcv, rfl⟩

/-- By scale invariance, every value `f v` (`v ≠ 0`) of a nonnegative frame function is bounded below
by the unit-sphere infimum `sInf (f '' sphere3)`. -/
theorem sInf_sphere3_le_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {v : Fin 3 → ℝ} (hv : v ≠ 0) :
    sInf (f '' sphere3) ≤ f v := by
  obtain ⟨c, hc0, hcv⟩ := exists_unit_smul hv
  rw [← hf.scale v hv c hc0]
  exact csInf_le (bddBelow_image_sphere3_of_nonneg hf) ⟨c • v, hcv, rfl⟩

/-- Continuity-free trace-sandwich bounds for the unit-sphere infimum and supremum of any nonnegative
frame function of weight `W`:
`0 ≤ sInf (f '' sphere3) ≤ W / 3 ≤ sSup (f '' sphere3) ≤ W`. -/
theorem sSup_sphere3_bounds_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) :
    0 ≤ sInf (f '' sphere3) ∧
    sInf (f '' sphere3) ≤ W / 3 ∧
    W / 3 ≤ sSup (f '' sphere3) ∧
    sSup (f '' sphere3) ≤ W := by
  have he2 : (![0, 1, 0] : Fin 3 → ℝ) ≠ 0 := ne_zero_of_apply_ne (i := 1) (by simp)
  have hsum := hf.frame e1 ![0, 1, 0] e3 e1_ne_zero he2 e3_ne_zero
    (by simp [dot3, e1]) (by simp [dot3, e1, e3]) (by simp [dot3, e3])
  have hinf_nonneg : 0 ≤ sInf (f '' sphere3) := by
    refine le_csInf (nonempty_image_sphere3 f) ?_
    rintro _ ⟨v, hv, rfl⟩
    exact hf.nonneg v (sphere3_subset hv)
  have hsup_le_W : sSup (f '' sphere3) ≤ W := by
    refine csSup_le (nonempty_image_sphere3 f) ?_
    rintro _ ⟨v, hv, rfl⟩
    exact le_weight_of_nonneg hf (sphere3_subset hv)
  have h1_inf := sInf_sphere3_le_of_nonneg hf e1_ne_zero
  have h2_inf := sInf_sphere3_le_of_nonneg hf he2
  have h3_inf := sInf_sphere3_le_of_nonneg hf e3_ne_zero
  have h1_sup := le_sSup_sphere3_of_nonneg hf e1_ne_zero
  have h2_sup := le_sSup_sphere3_of_nonneg hf he2
  have h3_sup := le_sSup_sphere3_of_nonneg hf e3_ne_zero
  refine ⟨hinf_nonneg, by linarith, by linarith, hsup_le_W⟩

/-- Extrema-attainment hypothesis on `ℝ³ \ {0}`: `f` attains its global maximum at a unit vector `p`
and attains its global minimum at a nonzero vector `s`. -/
def AttainsExtrema (f : (Fin 3 → ℝ) → ℝ) : Prop :=
  (∃ p : Fin 3 → ℝ, dot3 p p = 1 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p) ∧
  (∃ s : Fin 3 → ℝ, s ≠ 0 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f s ≤ f v)

/-- Continuity on the compact unit sphere `sphere3` alone implies `AttainsExtrema f` for any frame
function `f`. -/
theorem attainsExtrema_of_continuousOn_sphere3 {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsFrameFunction f W) (hc : ContinuousOn f sphere3) :
    AttainsExtrema f := by
  constructor
  · obtain ⟨p, hp, hmax⟩ := isCompact_sphere3.exists_isMaxOn ⟨e1, e1_mem_sphere3⟩ hc
    refine ⟨p, hp, fun v hv => ?_⟩
    obtain ⟨c, hc0, hcv⟩ := exists_unit_smul hv
    have : f (c • v) ≤ f p := hmax hcv
    rwa [hf.scale v hv c hc0] at this
  · obtain ⟨s, hs, hmin⟩ := isCompact_sphere3.exists_isMinOn ⟨e1, e1_mem_sphere3⟩ hc
    refine ⟨s, sphere3_subset hs, fun v hv => ?_⟩
    obtain ⟨c, hc0, hcv⟩ := exists_unit_smul hv
    have : f s ≤ f (c • v) := hmin hcv
    rwa [hf.scale v hv c hc0] at this

/-- Continuity on `ℝ³ \ {0}` implies `AttainsExtrema f` for any frame function `f`. -/
theorem attainsExtrema_of_continuousOn {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsFrameFunction f W) (hc : ContinuousOn f {v | v ≠ 0}) :
    AttainsExtrema f :=
  attainsExtrema_of_continuousOn_sphere3 hf (hc.mono sphere3_subset)

/-- Continuity-free Lemma 1(iv) at the pole `e1`: if `f` has a global maximum at `e1` and attains its
global minimum at some nonzero vector `s`, then `f` also attains its global minimum at a nonzero
vector `r` on the equator `{v 0 = 0}` (with zero continuity assumption on `f`). -/
theorem exists_min_on_equator_pole_of_max_and_min {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (hmin_ex : ∃ s : Fin 3 → ℝ, s ≠ 0 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f s ≤ f v) :
    ∃ r : Fin 3 → ℝ, r ≠ 0 ∧ r 0 = 0 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f r ≤ f v := by
  obtain ⟨s, hs, hmin⟩ := hmin_ex
  by_cases hrs : s 1 ^ 2 + s 2 ^ 2 = 0
  · have hs1 : s 1 = 0 := by nlinarith [sq_nonneg (s 1), sq_nonneg (s 2)]
    have hs2 : s 2 = 0 := by nlinarith [sq_nonneg (s 1), sq_nonneg (s 2)]
    have hs0 : s 0 ≠ 0 := by
      intro h0; apply hs; ext i; fin_cases i <;> simp [h0, hs1, hs2]
    have hse : s = (s 0) • e1 := by ext i; fin_cases i <;> simp [e1, hs1, hs2]
    have he2 : (![0, 1, 0] : Fin 3 → ℝ) ≠ 0 := ne_zero_of_apply_ne (i := 1) (by simp)
    refine ⟨![0, 1, 0], he2, by simp, fun v hv => ?_⟩
    have h1 := hmax ![0, 1, 0] he2
    have h2 := hmin v hv
    rw [hse, hf.scale e1 e1_ne_zero (s 0) hs0] at h2
    have h3 := hmax v hv
    linarith
  · let s' : Fin 3 → ℝ := ![0, s 1, s 2]
    let s'' : Fin 3 → ℝ := ![s 1 ^ 2 + s 2 ^ 2, -(s 0 * s 1), -(s 0 * s 2)]
    let n : Fin 3 → ℝ := ![0, -(s 2), s 1]
    have hs' : s' ≠ 0 := ne_zero_of_transverse_ne (by simpa [s'] using hrs)
    have hs'' : s'' ≠ 0 := ne_zero_of_apply_ne (i := 0) (by simpa [s''] using hrs)
    have hn : n ≠ 0 := ne_zero_of_transverse_ne (by simp [n]; intro h; apply hrs; linarith)
    have key := pair_sum_eq_of_common_normal hf e1_ne_zero hs' hs hs'' hn
      (by simp [dot3, e1, s']) (by simp [dot3, e1, n]) (by simp [dot3, s', n]; ring)
      (by simp [dot3, s'']; ring) (by simp [dot3, n]; ring) (by simp [dot3, s'', n]; ring)
    have h2 := hmax s'' hs''
    refine ⟨s', hs', by simp [s'], fun v hv => ?_⟩
    have := hmin v hv
    linarith

/-- Continuity-free Lemma 1(iv) at an arbitrary unit pole `p`: if `f` has a global maximum at `p`
and attains its global minimum at some nonzero vector `s`, then `f` attains its global minimum at a
unit vector `r` orthogonal to `p` (`dot3 r r = 1 ∧ dot3 p r = 0`), with zero continuity assumption. -/
theorem exists_min_perp_of_max_and_min {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsFrameFunction f W) {p : Fin 3 → ℝ} (hp : dot3 p p = 1)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p)
    (hmin_ex : ∃ s : Fin 3 → ℝ, s ≠ 0 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f s ≤ f v) :
    ∃ r : Fin 3 → ℝ, dot3 r r = 1 ∧ dot3 p r = 0 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f r ≤ f v := by
  obtain ⟨q, r, h⟩ := exists_orthonormal_completion hp
  have hF := hf.comp_ofFrame h
  have hmaxF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f (ofFrame p q r v)) v ≤ (fun v => f (ofFrame p q r v)) e1 := by
    intro v hv
    simp only [ofFrame_e1]
    exact hmax _ (ofFrame_ne_zero h hv)
  have hminF_ex : ∃ s₀ : Fin 3 → ℝ, s₀ ≠ 0 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f (ofFrame p q r v)) s₀ ≤ (fun v => f (ofFrame p q r v)) v := by
    obtain ⟨s, hs, hmin⟩ := hmin_ex
    refine ⟨toFrame p q r s, toFrame_ne_zero h hs, fun v hv => ?_⟩
    simp only [ofFrame_toFrame h]
    exact hmin _ (ofFrame_ne_zero h hv)
  obtain ⟨r₀, hr₀, hr₀0, hminF⟩ := exists_min_on_equator_pole_of_max_and_min hF hmaxF hminF_ex
  have hw : ofFrame p q r r₀ ≠ 0 := ofFrame_ne_zero h hr₀
  obtain ⟨c, hc0, hcu⟩ := exists_unit_smul hw
  refine ⟨c • ofFrame p q r r₀, hcu, ?_, fun v hv => ?_⟩
  · rw [dot3_smul_right, dot3_comm, (dot3_ofFrame_left h r₀).1, hr₀0, mul_zero]
  · rw [hf.scale _ hw c hc0]
    have := hminF (toFrame p q r v) (toFrame_ne_zero h hv)
    simpa only [ofFrame_toFrame h] using this

/-- Isotropic shift (deflation) of a real frame function by a constant `c`:
`deflateIso f c v = f v - c`. -/
def deflateIso (f : (Fin 3 → ℝ) → ℝ) (c : ℝ) (v : Fin 3 → ℝ) : ℝ :=
  f v - c

/-- Subtracting an isotropic constant `c` from a frame function of weight `W` produces a frame
function of weight `W - 3 * c`. -/
theorem isFrameFunction_deflateIso {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsFrameFunction f W) (c : ℝ) :
    IsFrameFunction (deflateIso f c) (W - 3 * c) where
  scale v hv a ha := by
    simp only [deflateIso, hf.scale v hv a ha]
  frame u v w hu hv hw huv huw hvw := by
    have := hf.frame u v w hu hv hw huv huw hvw
    simp only [deflateIso]
    linarith

/-- Subtracting any global lower bound `m` (`∀ v ≠ 0, m ≤ f v`) from a frame function `f` of weight
`W` produces a nonnegative frame function of weight `W - 3 * m`. -/
theorem isNonnegFrameFunction_deflateIso {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ}
    (hf : IsFrameFunction f W) (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → m ≤ f v) :
    IsNonnegFrameFunction (deflateIso f m) (W - 3 * m) where
  toIsFrameFunction := isFrameFunction_deflateIso hf m
  nonneg v hv := sub_nonneg.mpr (hmin v hv)

/-- **Continuity-free axisymmetric mixed-state Gleason theorem on `ℝ³`.**
If `f` is a frame function of weight `W` bounded below by `m` (`∀ v ≠ 0, m ≤ f v`) and `p` is a unit
vector such that `f p + 2 * m = W` (which holds for every axisymmetric / degenerate-spectrum mixed
state `ρ = (M - m)|p⟩⟨p| + m I₃`), then `f v = m + (f p - m) * (⟨v, p⟩² / ⟨v, v⟩)` for every
`v ≠ 0`, with zero continuity assumption on `f`. -/
theorem axisymmetric_mixed_state_nonneg_gleason_real {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ}
    (hf : IsFrameFunction f W) (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → m ≤ f v)
    {p : Fin 3 → ℝ} (hp : dot3 p p = 1) (hpW : f p + 2 * m = W) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 →
      f v = m + (f p - m) * (dot3 v p ^ 2 / dot3 v v) := by
  have hdef : IsNonnegFrameFunction (deflateIso f m) (W - 3 * m) :=
    isNonnegFrameFunction_deflateIso hf hmin
  have hp_def : deflateIso f m p = W - 3 * m := by
    unfold deflateIso; linarith
  intro v hv
  have h := pure_state_nonneg_gleason_real hdef hp hp_def v hv
  unfold deflateIso at h
  have hW : W - 3 * m = f p - m := by linarith
  rw [hW] at h
  linarith

/-- **Continuity-free zero counting on `S²`.**  A weight-zero frame function `h` that satisfies
`AttainsExtrema h` and vanishes on the six great circles `x = ±y`, `x = ±z`, `y = ±z` vanishes
identically on `ℝ³ \ {0}`, with zero continuity assumption on `h`. -/
theorem eq_zero_of_vanishes_on_six_circles_of_extrema {h : (Fin 3 → ℝ) → ℝ}
    (hh : IsFrameFunction h 0) (hext : AttainsExtrema h)
    (h6 : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (v 0 = v 1 ∨ v 0 = -v 1 ∨ v 0 = v 2 ∨ v 0 = -v 2 ∨ v 1 = v 2 ∨ v 1 = -v 2) → h v = 0) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → h v = 0 := by
  obtain ⟨p, hp, hmax⟩ := hext.1
  obtain ⟨r, hr, hpr, hmin⟩ := exists_min_perp_of_max_and_min hh hp hmax hext.2
  set q := cross3 p r with hq
  have hfr : IsOrthonormal p q r := isOrthonormal_cross hp hr hpr
  have hp0 : p ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hp]; exact one_pos)
  have hq0 : q ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr.qq]; exact one_pos)
  have hr0 : r ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hr]; exact one_pos)
  have hsum : h p + h q + h r = 0 := hh.frame p q r hp0 hq0 hr0 hfr.pq hfr.pr hfr.qr
  have hH := hh.comp_ofFrame hfr
  have hmaxH : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => h (ofFrame p q r v)) v ≤ (fun v => h (ofFrame p q r v)) e1 := by
    intro v hv; simp only [ofFrame_e1]; exact hmax _ (ofFrame_ne_zero hfr hv)
  have hminH : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => h (ofFrame p q r v)) e3 ≤ (fun v => h (ofFrame p q r v)) v := by
    intro v hv; simp only [ofFrame_e3]; exact hmin _ (ofFrame_ne_zero hfr hv)
  have hL8 := eq_stdQuad_on_six_circles_of_extrema hH hmaxH hminH
  simp only [ofFrame_e1, ofFrame_e3] at hL8
  have hEp : ∀ e : Fin 3 → ℝ, e ≠ 0 → dot3 e p = 0 → h e ≤ h q := by
    intro e he hep
    have he' : cross3 p e ≠ 0 := ne_zero_of_dot3_self_pos (by
      rw [dot3_cross3_self, hp, dot3_comm p e, hep, one_mul]; simpa using dot3_self_pos he)
    have h1 := hh.frame p e (cross3 p e) hp0 he he' (by rw [dot3_comm]; exact hep)
      (dot3_cross3_left p e) (dot3_cross3_right p e)
    have h2 := hmin _ he'
    linarith
  have hEr : ∀ e : Fin 3 → ℝ, e ≠ 0 → dot3 e r = 0 → h q ≤ h e := by
    intro e he her
    have he' : cross3 r e ≠ 0 := ne_zero_of_dot3_self_pos (by
      rw [dot3_cross3_self, hr, dot3_comm r e, her, one_mul]; simpa using dot3_self_pos he)
    have h1 := hh.frame r e (cross3 r e) hr0 he he' (by rw [dot3_comm]; exact her)
      (dot3_cross3_left r e) (dot3_cross3_right r e)
    have h2 := hmax _ he'
    linarith
  have hzero_perp : ∀ s : Fin 3 → ℝ, ∃ e : Fin 3 → ℝ, e ≠ 0 ∧ dot3 e s = 0 ∧ h e = 0 := by
    intro s
    by_cases hcr : cross3 s ![1, -1, 0] = 0
    · have hs2 : s 2 = 0 := by have := congrFun hcr 0; simpa [cross3] using this
      exact ⟨e3, e3_ne_zero, by simp [dot3, e3, hs2], h6 e3 e3_ne_zero (Or.inl (by simp [e3]))⟩
    · refine ⟨cross3 s ![1, -1, 0], hcr, by rw [dot3_comm]; exact dot3_cross3_left _ _,
        h6 _ hcr (Or.inl ?_)⟩
      simp [cross3]
  obtain ⟨ep, hep0, hep, hepz⟩ := hzero_perp p
  obtain ⟨er, her0, her, herz⟩ := hzero_perp r
  have hα0 : h q = 0 :=
    le_antisymm (by have := hEr er her0 her; linarith) (by have := hEp ep hep0 hep; linarith)
  have hm0 : h r = -h p := by linarith
  set a := p + q with ha
  have hap : dot3 a p = 1 := by rw [ha, dot3_add_left, hp, dot3_comm q p, hfr.pq]; ring
  have haq : dot3 a q = 1 := by rw [ha, dot3_add_left, hfr.pq, hfr.qq]; ring
  have har : dot3 a r = 0 := by rw [ha, dot3_add_left, hfr.pr, hfr.qr]; ring
  have haa : dot3 a a = 2 := by
    rw [ha, dot3_add_left, dot3_comm p, dot3_comm q, dot3_add_left, dot3_add_left, hp, hfr.qq,
      hfr.pq, dot3_comm q p, hfr.pq]; ring
  have key : ∀ n : Fin 3 → ℝ, (∀ v : Fin 3 → ℝ, v ≠ 0 → dot3 v n = 0 → h v = 0) →
      h p * (dot3 r n ^ 2 - dot3 a n ^ 2) = 0 := by
    intro n hn
    set β := dot3 r n with hβ
    set γ := dot3 a n with hγ
    set vi := β • a - γ • r with hvi
    have hvin : dot3 vi n = 0 := by
      rw [hvi, dot3_sub_left, dot3_smul_left, dot3_smul_left, ← hβ, ← hγ]; ring
    have hvp : dot3 vi p = β := by
      rw [hvi, dot3_sub_left, dot3_smul_left, dot3_smul_left, hap, dot3_comm r p, hpr]; ring
    have hvq : dot3 vi q = β := by
      rw [hvi, dot3_sub_left, dot3_smul_left, dot3_smul_left, haq, dot3_comm r q, hfr.qr]; ring
    have hvr : dot3 vi r = -γ := by
      rw [hvi, dot3_sub_left, dot3_smul_left, dot3_smul_left, har, hr]; ring
    by_cases hv0 : vi = 0
    · have hβ0 : β = 0 := by rw [← hvp, hv0]; simp [dot3]
      have hγ0 : γ = 0 := by
        have := hvr; rw [hv0] at this; simp [dot3] at this; linarith
      rw [hβ0, hγ0]; ring
    · have h1 : h vi = 0 := hn vi hv0 hvin
      have htf : toFrame p q r vi = ![β, β, -γ] := by
        simp [toFrame, hvp, hvq, hvr]
      have h2 := hL8 (toFrame p q r vi) (toFrame_ne_zero hfr hv0)
        (Or.inl (by rw [htf]; simp))
      rw [ofFrame_toFrame hfr, h1, htf] at h2
      have hD : (β ^ 2 + β ^ 2 + γ ^ 2) ≠ 0 := by
        have := dot3_self_pos (toFrame_ne_zero hfr hv0)
        rw [htf] at this; simp [dot3] at this; nlinarith
      simp only [stdQuad, dot3] at h2
      simp at h2
      rw [eq_comm, div_eq_zero_iff] at h2
      rcases h2 with h2 | h2
      · rw [hm0] at h2; linear_combination h2
      · exfalso; apply hD; linarith
  have k1 := key ![1, -1, 0] (fun v hv hvn => h6 v hv (Or.inl (by simp [dot3] at hvn; linarith)))
  have k2 := key ![1, 1, 0] (fun v hv hvn => h6 v hv (Or.inr (Or.inl (by simp [dot3] at hvn; linarith))))
  have k3 := key ![1, 0, -1] (fun v hv hvn => h6 v hv (Or.inr (Or.inr (Or.inl (by simp [dot3] at hvn; linarith)))))
  have k4 := key ![1, 0, 1] (fun v hv hvn => h6 v hv (Or.inr (Or.inr (Or.inr (Or.inl (by simp [dot3] at hvn; linarith))))))
  have k5 := key ![0, 1, -1] (fun v hv hvn => h6 v hv (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (by simp [dot3] at hvn; linarith)))))))
  have k6 := key ![0, 1, 1] (fun v hv hvn => h6 v hv (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (by simp [dot3] at hvn; linarith)))))))
  have htr := six_normals_tight r
  have hta := six_normals_tight a
  have hM0 : h p = 0 := by
    have : h p * (4 * dot3 r r - 4 * dot3 a a) = 0 := by
      linear_combination k1 + k2 + k3 + k4 + k5 + k6 - h p * htr + h p * hta
    rw [hr, haa] at this
    linarith
  intro v hv
  obtain ⟨c, hc0, hcu⟩ := exists_unit_smul hv
  obtain ⟨q', r', hfr'⟩ := exists_orthonormal_completion hcu
  have hu0 : c • v ≠ 0 :=
    ne_zero_of_dot3_self_pos (by rw [show dot3 (c • v) (c • v) = 1 from hcu]; exact one_pos)
  have hq'0 : q' ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr'.qq]; exact one_pos)
  have hr'0 : r' ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr'.rr]; exact one_pos)
  have hfs := hh.frame _ q' r' hu0 hq'0 hr'0 hfr'.pq hfr'.pr hfr'.qr
  have h1 := hmax _ hu0
  have h2 := hmax _ hq'0
  have h3 := hmax _ hr'0
  rw [← hh.scale v hv c hc0]
  linarith

/-- **General triaxial mixed-state reduction to the continuity-free Piron chain.**
For any frame function `f` of weight `W` and orthonormal frame `(p, q, r)` where `p` maximizes `f`
and `r` minimizes `f`, the residual `hResidual v = f (ofFrame p q r v) - stdQuad (f p) (W - f p - f r) (f r) v`
is a weight-zero frame function that automatically vanishes on all six great circles `x = ±y`,
`x = ±z`, `y = ±z` (with zero continuity assumption on `f`), and if `AttainsExtrema hResidual` holds
then `f` equals the triaxial Born quadratic form on all `w ≠ 0`. -/
theorem mixed_state_gleason_real_of_extrema {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsFrameFunction f W) {p q r : Fin 3 → ℝ} (hfr : IsOrthonormal p q r)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → f r ≤ f v) :
    let hResidual : (Fin 3 → ℝ) → ℝ :=
      fun v => f (ofFrame p q r v) - stdQuad (f p) (W - f p - f r) (f r) v
    IsFrameFunction hResidual 0 ∧
    (∀ v : Fin 3 → ℝ, v ≠ 0 →
      (v 0 = v 1 ∨ v 0 = -v 1 ∨ v 0 = v 2 ∨ v 0 = -v 2 ∨ v 1 = v 2 ∨ v 1 = -v 2) →
      hResidual v = 0) ∧
    (AttainsExtrema hResidual → ∀ w : Fin 3 → ℝ, w ≠ 0 →
      f w = (f p * dot3 w p ^ 2 + (W - f p - f r) * dot3 w q ^ 2 + f r * dot3 w r ^ 2) / dot3 w w) := by
  dsimp only
  have hF := hf.comp_ofFrame hfr
  have hmaxF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f (ofFrame p q r v)) v ≤ (fun v => f (ofFrame p q r v)) e1 := by
    intro v hv; simp only [ofFrame_e1]; exact hmax _ (ofFrame_ne_zero hfr hv)
  have hminF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f (ofFrame p q r v)) e3 ≤ (fun v => f (ofFrame p q r v)) v := by
    intro v hv; simp only [ofFrame_e3]; exact hmin _ (ofFrame_ne_zero hfr hv)
  have hg := isFrameFunction_stdQuad (f p) (W - f p - f r) (f r)
  have hhf : IsFrameFunction
      (fun v => (fun v => f (ofFrame p q r v)) v - stdQuad (f p) (W - f p - f r) (f r) v) 0 := by
    have := hF.sub hg
    rwa [show W - (f p + (W - f p - f r) + f r) = 0 by ring] at this
  have h6 : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (v 0 = v 1 ∨ v 0 = -v 1 ∨ v 0 = v 2 ∨ v 0 = -v 2 ∨ v 1 = v 2 ∨ v 1 = -v 2) →
      f (ofFrame p q r v) - stdQuad (f p) (W - f p - f r) (f r) v = 0 := by
    intro v hv hcirc
    have := eq_stdQuad_on_six_circles_of_extrema hF hmaxF hminF v hv hcirc
    simp only [ofFrame_e1, ofFrame_e3] at this
    rw [this, sub_self]
  refine ⟨hhf, h6, fun hext w hw => ?_⟩
  have hz := eq_zero_of_vanishes_on_six_circles_of_extrema hhf hext h6
    (toFrame p q r w) (toFrame_ne_zero hfr hw)
  simp only [ofFrame_toFrame hfr] at hz
  rw [sub_eq_zero] at hz
  rw [hz, stdQuad, dot3_toFrame_self hfr]
  simp [toFrame]

/-- **Real Gleason theorem from continuity on the compact unit sphere `sphere3` alone.**
Every frame function on `ℝ³ \ {0}` whose restriction to `sphere3` is continuous is a triaxial
quadratic form divided by `⟨v, v⟩`, proved via `attainsExtrema_of_continuousOn_sphere3`,
`exists_min_perp_of_max_and_min`, and `mixed_state_gleason_real_of_extrema`. -/
theorem gleason_real_of_continuousOn_sphere3 {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsFrameFunction f W) (hc : ContinuousOn f sphere3) :
    ∃ p q r : Fin 3 → ℝ, IsOrthonormal p q r ∧ ∃ M α m : ℝ, ∀ v : Fin 3 → ℝ, v ≠ 0 →
      f v = (M * dot3 v p ^ 2 + α * dot3 v q ^ 2 + m * dot3 v r ^ 2) / dot3 v v := by
  have hext := attainsExtrema_of_continuousOn_sphere3 hf hc
  obtain ⟨p, hp, hmax⟩ := hext.1
  obtain ⟨r, hr, hpr, hmin⟩ := exists_min_perp_of_max_and_min hf hp hmax hext.2
  set q := cross3 p r with hq
  have hfr : IsOrthonormal p q r := isOrthonormal_cross hp hr hpr
  have hred := mixed_state_gleason_real_of_extrema hf hfr hmax hmin
  rcases hred with ⟨hhf, _, hgleason⟩
  have hc_ofFrame : ContinuousOn (fun v => f (ofFrame p q r v)) sphere3 :=
    hc.comp (continuous_ofFrame p q r).continuousOn (fun v hv => by
      show dot3 (ofFrame p q r v) (ofFrame p q r v) = 1
      rw [dot3_ofFrame hfr]
      exact hv)
  have hc_res : ContinuousOn
      (fun v => f (ofFrame p q r v) - stdQuad (f p) (W - f p - f r) (f r) v) sphere3 :=
    hc_ofFrame.sub ((continuousOn_stdQuad (f p) (W - f p - f r) (f r)).mono sphere3_subset)
  exact ⟨p, q, r, hfr, f p, W - f p - f r, f r,
    hgleason (attainsExtrema_of_continuousOn_sphere3 hhf hc_res)⟩

/-- **Triaxial spectral positivity and eigenvalue ordering (`ℝ³`).**
For any nonnegative frame function `f` of weight `W` and any orthonormal frame `(p, q, r)` where
`p` maximizes `f` and `r` minimizes `f`, the three principal values `λ₁ = f p`,
`λ₂ = f q = W - f p - f r`, and `λ₃ = f r` satisfy `0 ≤ f r ≤ W - f p - f r ≤ f p ≤ W` and sum to `W`. -/
theorem triaxial_eigenvalues_nonneg_and_ordered {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {p q r : Fin 3 → ℝ} (hfr : IsOrthonormal p q r)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → f r ≤ f v) :
    f q = W - f p - f r ∧
    0 ≤ f r ∧
    f r ≤ W - f p - f r ∧
    W - f p - f r ≤ f p ∧
    f p ≤ W ∧
    f p + (W - f p - f r) + f r = W := by
  have hp0 : p ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr.pp]; exact one_pos)
  have hq0 : q ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr.qq]; exact one_pos)
  have hr0 : r ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr.rr]; exact one_pos)
  have hsum := hf.frame p q r hp0 hq0 hr0 hfr.pq hfr.pr hfr.qr
  have hr_nn := hf.nonneg r hr0
  have hr_le_q := hmin q hq0
  have hq_le_p := hmax q hq0
  have hp_le_W := le_weight_of_nonneg hf hp0
  refine ⟨by linarith, hr_nn, by linarith, by linarith, hp_le_W, by ring⟩

/-- **Rayleigh-Ritz spectral sandwich and PSD bounds for `stdQuad` (`ℝ³`).**
For any ordered nonnegative eigenvalues `0 ≤ lam₃ ≤ lam₂ ≤ lam₁` summing to `W` (`lam₁ + lam₂ + lam₃ = W`)
and any nonzero vector `v ≠ 0`, `stdQuad lam₁ lam₂ lam₃ v` lies in `[lam₃, lam₁] ⊆ [0, W]`. -/
theorem stdQuad_nonneg_and_le_weight_of_eigenvalues {lam₁ lam₂ lam₃ W : ℝ}
    (h0 : 0 ≤ lam₃) (h32 : lam₃ ≤ lam₂) (h21 : lam₂ ≤ lam₁) (hW : lam₁ + lam₂ + lam₃ = W)
    {v : Fin 3 → ℝ} (hv : v ≠ 0) :
    lam₃ ≤ stdQuad lam₁ lam₂ lam₃ v ∧
    stdQuad lam₁ lam₂ lam₃ v ≤ lam₁ ∧
    0 ≤ stdQuad lam₁ lam₂ lam₃ v ∧
    stdQuad lam₁ lam₂ lam₃ v ≤ W := by
  have hpos : 0 < dot3 v v := dot3_self_pos hv
  have hlow : lam₃ ≤ stdQuad lam₁ lam₂ lam₃ v := by
    rw [stdQuad, le_div_iff₀ hpos]
    unfold dot3
    nlinarith [sq_nonneg (v 0), sq_nonneg (v 1), sq_nonneg (v 2)]
  have hhigh : stdQuad lam₁ lam₂ lam₃ v ≤ lam₁ := by
    rw [stdQuad, div_le_iff₀ hpos]
    unfold dot3
    nlinarith [sq_nonneg (v 0), sq_nonneg (v 1), sq_nonneg (v 2)]
  refine ⟨hlow, hhigh, by linarith, by linarith⟩

/-- **Nonnegative mixed-state Gleason theorem on `ℝ³ \ {0}` from extrema attainment alone.**
If a nonnegative frame function `f` of weight `W` satisfies `AttainsExtrema f` and its triaxial
residual satisfies `AttainsExtrema`, then there exist an orthonormal frame `(p, q, r)` and ordered
nonnegative eigenvalues `0 ≤ lam₃ ≤ lam₂ ≤ lam₁ ≤ W` (`lam₁ = f p`, `lam₂ = f q`, `lam₃ = f r`,
`lam₁ + lam₂ + lam₃ = W`) representing `f` as a positive-semidefinite Born quadratic form on `ℝ³ \ {0}`. -/
theorem nonneg_gleason_real_of_extrema {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) (hext : AttainsExtrema f)
    (hext_res : ∀ p q r : Fin 3 → ℝ, IsOrthonormal p q r →
      (∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p) →
      (∀ v : Fin 3 → ℝ, v ≠ 0 → f r ≤ f v) →
      AttainsExtrema (fun v => f (ofFrame p q r v) - stdQuad (f p) (W - f p - f r) (f r) v)) :
    ∃ p q r : Fin 3 → ℝ, IsOrthonormal p q r ∧
      ∃ lam₁ lam₂ lam₃ : ℝ,
        lam₁ = f p ∧ lam₂ = f q ∧ lam₃ = f r ∧
        0 ≤ lam₃ ∧ lam₃ ≤ lam₂ ∧ lam₂ ≤ lam₁ ∧ lam₁ ≤ W ∧
        lam₁ + lam₂ + lam₃ = W ∧
        ∀ w : Fin 3 → ℝ, w ≠ 0 →
          f w = (lam₁ * dot3 w p ^ 2 + lam₂ * dot3 w q ^ 2 + lam₃ * dot3 w r ^ 2) / dot3 w w := by
  obtain ⟨p, hp, hmax⟩ := hext.1
  obtain ⟨r, hr, hpr, hmin⟩ := exists_min_perp_of_max_and_min hf.toIsFrameFunction hp hmax hext.2
  set q := cross3 p r with hq
  have hfr : IsOrthonormal p q r := isOrthonormal_cross hp hr hpr
  rcases triaxial_eigenvalues_nonneg_and_ordered hf hfr hmax hmin with
    ⟨hfq, hr0, hrq, hqp, hpW, hsum⟩
  have hgleason := (mixed_state_gleason_real_of_extrema hf.toIsFrameFunction hfr hmax hmin).2.2
    (hext_res p q r hfr hmax hmin)
  refine ⟨p, q, r, hfr, f p, f q, f r, rfl, rfl, rfl, hr0, by linarith, by linarith, hpW,
    by linarith, fun w hw => ?_⟩
  rw [hfq, hgleason w hw]

/-- **Complete nonnegative mixed-state Gleason theorem on `ℝ³ \ {0}` from continuity on `sphere3`.**
Every nonnegative frame function `f` of weight `W` whose restriction to `sphere3` is continuous
admits an orthonormal eigenframe `(p, q, r)` and ordered nonnegative eigenvalues
`0 ≤ lam₃ ≤ lam₂ ≤ lam₁ ≤ W` (`lam₁ = f p`, `lam₂ = f q`, `lam₃ = f r`, `lam₁ + lam₂ + lam₃ = W`) such that
`f w = (lam₁ ⟨w, p⟩² + lam₂ ⟨w, q⟩² + lam₃ ⟨w, r⟩²) / ⟨w, w⟩` for every `w ≠ 0`. -/
theorem nonneg_gleason_real_of_continuousOn_sphere3 {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) (hc : ContinuousOn f sphere3) :
    ∃ p q r : Fin 3 → ℝ, IsOrthonormal p q r ∧
      ∃ lam₁ lam₂ lam₃ : ℝ,
        lam₁ = f p ∧ lam₂ = f q ∧ lam₃ = f r ∧
        0 ≤ lam₃ ∧ lam₃ ≤ lam₂ ∧ lam₂ ≤ lam₁ ∧ lam₁ ≤ W ∧
        lam₁ + lam₂ + lam₃ = W ∧
        ∀ w : Fin 3 → ℝ, w ≠ 0 →
          f w = (lam₁ * dot3 w p ^ 2 + lam₂ * dot3 w q ^ 2 + lam₃ * dot3 w r ^ 2) / dot3 w w := by
  refine nonneg_gleason_real_of_extrema hf
    (attainsExtrema_of_continuousOn_sphere3 hf.toIsFrameFunction hc)
    (fun p q r hfr hmax hmin => ?_)
  have hhf := (mixed_state_gleason_real_of_extrema hf.toIsFrameFunction hfr hmax hmin).1
  have hc_ofFrame : ContinuousOn (fun v => f (ofFrame p q r v)) sphere3 :=
    hc.comp (continuous_ofFrame p q r).continuousOn (fun v hv => by
      show dot3 (ofFrame p q r v) (ofFrame p q r v) = 1
      rw [dot3_ofFrame hfr]
      exact hv)
  have hc_res : ContinuousOn
      (fun v => f (ofFrame p q r v) - stdQuad (f p) (W - f p - f r) (f r) v) sphere3 :=
    hc_ofFrame.sub ((continuousOn_stdQuad (f p) (W - f p - f r) (f r)).mono sphere3_subset)
  exact attainsExtrema_of_continuousOn_sphere3 hhf hc_res

end GleasonReal

namespace GleasonComplex

open Complex ComplexConjugate Filter Topology

/-! ### Target 2: Complex nonnegativity bounds and continuity-free pure-state reduction -/

/-- A nonnegative complex frame function of weight `W` on `ℂ³`. -/
structure IsNonnegFrameFunctionC (F : (Fin 3 → ℂ) → ℝ) (W : ℝ) : Prop
    extends IsFrameFunctionC F W where
  nonneg : ∀ v : Fin 3 → ℂ, v ≠ 0 → 0 ≤ F v

/-- Pulling back a nonnegative complex frame function along a complex orthonormal triple
yields a nonnegative real frame function on `ℝ³`. -/
theorem IsNonnegFrameFunctionC.pullback {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) {p q r : Fin 3 → ℂ} (h : IsOrthonormalC p q r) :
    GleasonReal.IsNonnegFrameFunction (fun v => F (ofFrameC p q r v)) W where
  toIsFrameFunction := hF.toIsFrameFunctionC.pullback h
  nonneg v hv := hF.nonneg (ofFrameC p q r v) (ofFrameC_ne_zero h hv)

/-- The weight `W` of a nonnegative complex frame function is nonnegative. -/
theorem weight_nonneg_of_nonnegC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) : 0 ≤ W := by
  have hp : (![1, 0, 0] : Fin 3 → ℂ) ≠ 0 := ne_zero_of_nsq_pos (by simp [nsq])
  have hq : (![0, 1, 0] : Fin 3 → ℂ) ≠ 0 := ne_zero_of_nsq_pos (by simp [nsq])
  have hr : (![0, 0, 1] : Fin 3 → ℂ) ≠ 0 := ne_zero_of_nsq_pos (by simp [nsq])
  have hfr := hF.frame ![1, 0, 0] ![0, 1, 0] ![0, 0, 1] hp hq hr
    (by simp [dotC]) (by simp [dotC]) (by simp [dotC])
  linarith [hF.nonneg _ hp, hF.nonneg _ hq, hF.nonneg _ hr, hfr]

/-- Every value of a nonnegative complex frame function of weight `W` is at most `W`. -/
theorem le_weight_of_nonnegC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) {v : Fin 3 → ℂ} (hv : v ≠ 0) :
    F v ≤ W := by
  obtain ⟨c, hc0, hcv⟩ := exists_unit_smulC hv
  set p := c • v with hp_def
  have hp1 : nsq p = 1 := hcv
  obtain ⟨q, hq1, hpq⟩ := exists_unit_perp p
  have hfr : IsOrthonormalC p q (ccross p q) := isOrthonormalC_ccross hp1 hq1 hpq
  have hp0 : p ≠ 0 := ne_zero_of_nsq_pos (by rw [hp1]; exact one_pos)
  have hq0 : q ≠ 0 := ne_zero_of_nsq_pos (by rw [hq1]; exact one_pos)
  have hr1 : nsq (ccross p q) = 1 := by
    have := hfr.rr; rw [dotC_self_eq_nsq] at this; exact_mod_cast this
  have hr0 : ccross p q ≠ 0 := ne_zero_of_nsq_pos (by rw [hr1]; exact one_pos)
  have hsum := hF.frame p q (ccross p q) hp0 hq0 hr0 hfr.pq hfr.pr hfr.qr
  have hFp : F p = F v := hF.scale v hv c hc0
  linarith [hF.nonneg q hq0, hF.nonneg (ccross p q) hr0, hsum, hFp]

/-- A nonnegative complex frame function of weight `W` takes values in `[0, W]`. -/
theorem bounded_of_nonnegC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) {v : Fin 3 → ℂ} (hv : v ≠ 0) :
    0 ≤ F v ∧ F v ≤ W :=
  ⟨hF.nonneg v hv, le_weight_of_nonnegC hF hv⟩

/-- For any two orthogonal nonzero vectors `u, v ∈ ℂ³`, `F u + F v ≤ W`. -/
theorem ortho_add_le_weight_of_nonnegC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) {u v : Fin 3 → ℂ}
    (hu : u ≠ 0) (hv : v ≠ 0) (huv : dotC u v = 0) :
    F u + F v ≤ W := by
  have hw : ccross u v ≠ 0 := ne_zero_of_nsq_pos (by
    rw [nsq_ccross, huv, map_zero, sub_zero]
    exact mul_pos (nsq_pos hu) (nsq_pos hv))
  have hsum := hF.frame u v (ccross u v) hu hv hw huv
    (dotC_ccross_left u v) (dotC_ccross_right u v)
  linarith [hF.nonneg (ccross u v) hw, hsum]

/-- For any two orthogonal nonzero vectors `u, v ∈ ℂ³`, `F v ≤ W - F u`. -/
theorem ortho_le_weight_sub_of_nonnegC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) {u v : Fin 3 → ℂ}
    (hu : u ≠ 0) (hv : v ≠ 0) (huv : dotC u v = 0) :
    F v ≤ W - F u := by
  linarith [ortho_add_le_weight_of_nonnegC hF hu hv huv]

/-- If a nonnegative complex frame function attains the full weight `W` at a pole `p ≠ 0`,
then it vanishes on the orthogonal complement `dotC p v = 0`. -/
theorem eq_zero_on_perp_of_pole_eq_weightC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) {p v : Fin 3 → ℂ}
    (hp : p ≠ 0) (hpW : F p = W) (hv : v ≠ 0) (hpv : dotC p v = 0) :
    F v = 0 := by
  have hle := ortho_le_weight_sub_of_nonnegC hF hp hv hpv
  have hge := hF.nonneg v hv
  linarith

/-- Continuity-free Proposition 1 at an arbitrary unit pole `p ∈ ℂ³`: if `F` is maximized
at `p` and equals `m` on the orthogonal complement `dotC p v = 0`, then
`F v = m + (F p - m) * (normSq (dotC p v) / nsq v)` for all `v ≠ 0`, without any
continuity assumption on `F`. -/
theorem prop1_of_maxC {F : (Fin 3 → ℂ) → ℝ} {W m : ℝ}
    (hF : IsFrameFunctionC F W) {p : Fin 3 → ℂ} (hp : nsq p = 1)
    (hmax : ∀ v : Fin 3 → ℂ, v ≠ 0 → F v ≤ F p)
    (heq : ∀ v : Fin 3 → ℂ, v ≠ 0 → dotC p v = 0 → F v = m) :
    ∀ v : Fin 3 → ℂ, v ≠ 0 →
      F v = m + (F p - m) * (normSq (dotC p v) / nsq v) := by
  intro v hv
  obtain ⟨q, hq1, hpq⟩ := exists_unit_perp p
  have hfr : IsOrthonormalC p q (ccross p q) := isOrthonormalC_ccross hp hq1 hpq
  set r := ccross p q with hr
  set a := dotC p v with ha
  set b := dotC q v with hb
  set c := dotC r v with hc
  have hv' : v = a • p + b • q + c • r := (completenessC hfr v).symm
  have hnsq : nsq v = normSq a + normSq b + normSq c := by rw [hv', nsq_combo hfr]
  set u := b • q + c • r with hu
  have hnu : nsq u = normSq b + normSq c := nsq_combo2 hfr b c
  have hpu : dotC p u = 0 := dotC_combo2 hfr b c
  have hvu : v = a • p + u := by rw [hv', add_assoc]
  have hnsq_u : nsq v = normSq a + nsq u := by linarith [hnsq, hnu]
  have hp0 : p ≠ 0 := ne_zero_of_nsq_pos (by rw [hp]; exact one_pos)
  by_cases hu0 : u = 0
  · have hnu0 : nsq u = 0 := (nsq_eq_zero_iff u).mpr hu0
    have ha0 : a ≠ 0 := by
      intro h0
      apply hv
      rw [hvu, hu0, h0, zero_smul, add_zero]
    have hFv : F v = F p := by
      rw [hvu, hu0, add_zero, hF.scale p hp0 a ha0]
    have hna_pos : 0 < normSq a := normSq_pos.mpr ha0
    rw [hFv, hnsq_u, hnu0, add_zero, div_self hna_pos.ne']
    ring
  · by_cases ha0 : a = 0
    · have hvu' : v = u := by rw [hvu, ha0, zero_smul, zero_add]
      have hpv : dotC p v = 0 := by rw [hvu', hpu]
      rw [heq v hv hpv, ha0, map_zero, zero_div, mul_zero, add_zero]
    · set s := Real.sqrt (nsq u) with hs
      have hs_pos : 0 < s := Real.sqrt_pos.mpr (nsq_pos hu0)
      have hs2 : s ^ 2 = nsq u := Real.sq_sqrt (nsq_nonneg u)
      have hs_ne : s ≠ 0 := hs_pos.ne'
      have hsC : (s : ℂ) ≠ 0 := by exact_mod_cast hs_ne
      set lam : ℂ := a / (‖a‖ : ℂ) with hlam
      have han_pos : 0 < ‖a‖ := norm_pos_iff.mpr ha0
      have hanC : (‖a‖ : ℂ) ≠ 0 := by exact_mod_cast han_pos.ne'
      have hlam1 : normSq lam = 1 := by
        rw [hlam, normSq_div, normSq_ofReal, normSq_eq_norm_sq]; field_simp
      have hlam0 : lam ≠ 0 := fun h0 => by
        rw [h0, map_zero] at hlam1; exact zero_ne_one hlam1
      have hphase : lam * conj lam = 1 := by rw [mul_conj, hlam1]; simp
      have e1_lam : lam * (‖a‖ : ℂ) = a := by rw [hlam]; field_simp
      set q' : Fin 3 → ℂ := (((1 / s : ℝ) : ℂ) * conj lam) • u with hq'
      have hq'1 : nsq q' = 1 := by
        rw [hq', nsq_smul, normSq_mul, normSq_ofReal, normSq_conj, hlam1, mul_one, ← hs2]
        field_simp
      have hpq' : dotC p q' = 0 := by rw [hq', dotC_smul_right, hpu, mul_zero]
      set r' := ccross p q' with hr'
      have hfr' : IsOrthonormalC p q' r' := isOrthonormalC_ccross hp hq'1 hpq'
      let G : (Fin 3 → ℝ) → ℝ := fun x => F (ofFrameC p q' r' x)
      have hG : GleasonReal.IsFrameFunction G W := hF.pullback hfr'
      have hGe1 : G GleasonReal.e1 = F p := by
        show F (ofFrameC p q' r' GleasonReal.e1) = F p
        rw [ofFrameC_e1]
      have hGmax : ∀ x : Fin 3 → ℝ, x ≠ 0 → G x ≤ G GleasonReal.e1 := by
        intro x hx
        rw [hGe1]
        exact hmax _ (ofFrameC_ne_zero hfr' hx)
      have hGeq : ∀ x : Fin 3 → ℝ, x ≠ 0 → x 0 = 0 → G x = m := by
        intro x hx hx0
        apply heq _ (ofFrameC_ne_zero hfr' hx)
        have hd := dotC_ofFrameC hfr' GleasonReal.e1 x
        rw [ofFrameC_e1] at hd
        have hd3 : GleasonReal.dot3 GleasonReal.e1 x = 0 := by
          simp [GleasonReal.dot3, GleasonReal.e1, hx0]
        rw [hd, hd3, Complex.ofReal_zero]
      let x0 : Fin 3 → ℝ := ![‖a‖, s, 0]
      have hx0_ne : x0 ≠ 0 := by
        intro h0
        have := congrFun h0 0
        simp [x0] at this
        exact ha0 this
      have hprop := GleasonReal.prop1_pole_of_max hG hGmax hGeq x0 hx0_ne
      have hof_x0 : lam • ofFrameC p q' r' x0 = v := by
        have h1 : ofFrameC p q' r' x0 = (‖a‖ : ℂ) • p + (s : ℂ) • q' := by
          ext i; simp [ofFrameC_apply, x0]
        have h2 : lam • ((s : ℂ) • q') = u := by
          rw [hq', smul_smul, smul_smul]
          have hcoef : lam * (s : ℂ) * (((1 / s : ℝ) : ℂ) * conj lam) = 1 := by
            push_cast
            have : lam * (s : ℂ) * (1 / (s : ℂ) * conj lam) =
                (lam * conj lam) * ((s : ℂ) * (1 / (s : ℂ))) := by ring
            rw [this, hphase, one_mul, mul_one_div_cancel hsC]
          rw [hcoef, one_smul]
        rw [h1, smul_add, smul_smul, e1_lam, h2, ← hvu]
      have hFv_eq : F v = G x0 := by
        rw [← hof_x0, hF.scale _ (ofFrameC_ne_zero hfr' hx0_ne) lam hlam0]
      have hlat_x0 : GleasonReal.lat x0 = normSq a / nsq v := by
        simp [GleasonReal.lat, GleasonReal.dot3, x0, ← sq ‖a‖, ← sq s,
          Complex.sq_norm, hs2, ← hnsq_u]
      rw [hFv_eq, hprop, hGe1, hlat_x0]

/-- Continuity-free pure-state Born rule on `ℂ³`: if a nonnegative complex frame function `F`
of weight `W` attains `W` at a unit vector `p`, then `F v = W * normSq (dotC p v) / nsq v`
for every `v ≠ 0`, with zero continuity assumption on `F`. -/
theorem pure_state_nonneg_gleason_complex {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) {p : Fin 3 → ℂ}
    (hp : nsq p = 1) (hpW : F p = W) :
    ∀ v : Fin 3 → ℂ, v ≠ 0 →
      F v = W * normSq (dotC p v) / nsq v := by
  intro v hv
  have hp0 : p ≠ 0 := ne_zero_of_nsq_pos (by rw [hp]; exact one_pos)
  have hmax : ∀ u : Fin 3 → ℂ, u ≠ 0 → F u ≤ F p := by
    intro u hu
    rw [hpW]
    exact le_weight_of_nonnegC hF hu
  have heq : ∀ u : Fin 3 → ℂ, u ≠ 0 → dotC p u = 0 → F u = 0 :=
    fun u hu hpu => eq_zero_on_perp_of_pole_eq_weightC hF hp0 hpW hu hpu
  have hprop := prop1_of_maxC hF.toIsFrameFunctionC hp hmax heq v hv
  rw [hprop, hpW]
  ring

/-! ### Target 3 (`TFQ-1059`): Complex isotropic deflation and continuity-free axisymmetric mixed-state Gleason theorem on `ℂ³` -/

/-- Isotropic shift (deflation) of a complex frame function on `ℂ³` by a real constant `c`:
`deflateIsoC F c v = F v - c`. -/
def deflateIsoC (F : (Fin 3 → ℂ) → ℝ) (c : ℝ) (v : Fin 3 → ℂ) : ℝ :=
  F v - c

/-- Subtracting an isotropic constant `c` from a complex frame function of weight `W` produces a
complex frame function of weight `W - 3 * c`. -/
theorem isFrameFunctionC_deflateIsoC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsFrameFunctionC F W) (c : ℝ) :
    IsFrameFunctionC (deflateIsoC F c) (W - 3 * c) where
  scale v hv a ha := by
    simp only [deflateIsoC, hF.scale v hv a ha]
  frame u v w hu hv hw huv huw hvw := by
    have := hF.frame u v w hu hv hw huv huw hvw
    simp only [deflateIsoC]
    linarith

/-- Subtracting any global lower bound `m` (`∀ v ≠ 0, m ≤ F v`) from a complex frame function `F`
of weight `W` produces a nonnegative complex frame function of weight `W - 3 * m`. -/
theorem isNonnegFrameFunctionC_deflateIsoC {F : (Fin 3 → ℂ) → ℝ} {W m : ℝ}
    (hF : IsFrameFunctionC F W) (hmin : ∀ v : Fin 3 → ℂ, v ≠ 0 → m ≤ F v) :
    IsNonnegFrameFunctionC (deflateIsoC F m) (W - 3 * m) where
  toIsFrameFunctionC := isFrameFunctionC_deflateIsoC hF m
  nonneg v hv := sub_nonneg.mpr (hmin v hv)

/-- **Continuity-free axisymmetric mixed-state Gleason theorem on `ℂ³`.**
If `F` is a complex frame function of weight `W` bounded below by `m` (`∀ v ≠ 0, m ≤ F v`) and `p`
is a unit vector (`nsq p = 1`) such that `F p + 2 * m = W` (which holds for every axisymmetric /
degenerate-spectrum mixed state `ρ = (M - m)|p⟩⟨p| + m I₃` on `ℂ³`), then
`F v = m + (F p - m) * (normSq (dotC p v) / nsq v)` for every `v ≠ 0`, with zero continuity
assumption on `F`. -/
theorem axisymmetric_mixed_state_nonneg_gleason_complex {F : (Fin 3 → ℂ) → ℝ} {W m : ℝ}
    (hF : IsFrameFunctionC F W) (hmin : ∀ v : Fin 3 → ℂ, v ≠ 0 → m ≤ F v)
    {p : Fin 3 → ℂ} (hp : nsq p = 1) (hpW : F p + 2 * m = W) :
    ∀ v : Fin 3 → ℂ, v ≠ 0 →
      F v = m + (F p - m) * (normSq (dotC p v) / nsq v) := by
  have hdef : IsNonnegFrameFunctionC (deflateIsoC F m) (W - 3 * m) :=
    isNonnegFrameFunctionC_deflateIsoC hF hmin
  have hp_def : deflateIsoC F m p = W - 3 * m := by
    unfold deflateIsoC; linarith
  intro v hv
  have h := pure_state_nonneg_gleason_complex hdef hp hp_def v hv
  unfold deflateIsoC at h
  have hW : W - 3 * m = F p - m := by linarith
  rw [hW, mul_div_assoc] at h
  linarith

/-- The image `F '' sphereC` of the complex unit sphere `S⁵ ⊂ ℂ³` under any `F` is nonempty
(witnessed by `![1, 0, 0] ∈ sphereC`). -/
theorem nonempty_image_sphereC (F : (Fin 3 → ℂ) → ℝ) :
    (F '' sphereC).Nonempty :=
  ⟨F ![1, 0, 0], ![1, 0, 0], e1C_mem_sphereC, rfl⟩

/-- For any nonnegative complex frame function `F` of weight `W`, the image `F '' sphereC` is
bounded above by `W` (`W ∈ upperBounds (F '' sphereC)`). -/
theorem bddAbove_image_sphereC_of_nonnegC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) :
    BddAbove (F '' sphereC) := by
  refine ⟨W, ?_⟩
  rintro _ ⟨v, hv, rfl⟩
  exact le_weight_of_nonnegC hF (sphereC_subset hv)

/-- For any nonnegative complex frame function `F` of weight `W`, the image `F '' sphereC` is
bounded below by `0` (`0 ∈ lowerBounds (F '' sphereC)`). -/
theorem bddBelow_image_sphereC_of_nonnegC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) :
    BddBelow (F '' sphereC) := by
  refine ⟨0, ?_⟩
  rintro _ ⟨v, hv, rfl⟩
  exact hF.nonneg v (sphereC_subset hv)

/-- By complex scale invariance, every value `F v` (`v ≠ 0`) of a nonnegative complex frame
function is bounded above by the unit-sphere supremum `sSup (F '' sphereC)`. -/
theorem le_sSup_sphereC_of_nonnegC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) {v : Fin 3 → ℂ} (hv : v ≠ 0) :
    F v ≤ sSup (F '' sphereC) := by
  obtain ⟨c, hc0, hcv⟩ := exists_unit_smulC hv
  rw [← hF.scale v hv c hc0]
  exact le_csSup (bddAbove_image_sphereC_of_nonnegC hF) ⟨c • v, hcv, rfl⟩

/-- By complex scale invariance, every value `F v` (`v ≠ 0`) of a nonnegative complex frame
function is bounded below by the unit-sphere infimum `sInf (F '' sphereC)`. -/
theorem sInf_sphereC_le_of_nonnegC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) {v : Fin 3 → ℂ} (hv : v ≠ 0) :
    sInf (F '' sphereC) ≤ F v := by
  obtain ⟨c, hc0, hcv⟩ := exists_unit_smulC hv
  rw [← hF.scale v hv c hc0]
  exact csInf_le (bddBelow_image_sphereC_of_nonnegC hF) ⟨c • v, hcv, rfl⟩

/-- Continuity-free trace-sandwich bounds for the unit-sphere infimum and supremum of any
nonnegative complex frame function of weight `W` on `S⁵ ⊂ ℂ³`:
`0 ≤ sInf (F '' sphereC) ≤ W / 3 ≤ sSup (F '' sphereC) ≤ W`. -/
theorem sSup_sphereC_bounds_of_nonnegC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) :
    0 ≤ sInf (F '' sphereC) ∧
    sInf (F '' sphereC) ≤ W / 3 ∧
    W / 3 ≤ sSup (F '' sphereC) ∧
    sSup (F '' sphereC) ≤ W := by
  have hp : (![1, 0, 0] : Fin 3 → ℂ) ≠ 0 := ne_zero_of_nsq_pos (by simp [nsq])
  have hq : (![0, 1, 0] : Fin 3 → ℂ) ≠ 0 := ne_zero_of_nsq_pos (by simp [nsq])
  have hr : (![0, 0, 1] : Fin 3 → ℂ) ≠ 0 := ne_zero_of_nsq_pos (by simp [nsq])
  have hsum := hF.frame ![1, 0, 0] ![0, 1, 0] ![0, 0, 1] hp hq hr
    (by simp [dotC]) (by simp [dotC]) (by simp [dotC])
  have hinf_nonneg : 0 ≤ sInf (F '' sphereC) := by
    refine le_csInf (nonempty_image_sphereC F) ?_
    rintro _ ⟨v, hv, rfl⟩
    exact hF.nonneg v (sphereC_subset hv)
  have hsup_le_W : sSup (F '' sphereC) ≤ W := by
    refine csSup_le (nonempty_image_sphereC F) ?_
    rintro _ ⟨v, hv, rfl⟩
    exact le_weight_of_nonnegC hF (sphereC_subset hv)
  have h1_inf := sInf_sphereC_le_of_nonnegC hF hp
  have h2_inf := sInf_sphereC_le_of_nonnegC hF hq
  have h3_inf := sInf_sphereC_le_of_nonnegC hF hr
  have h1_sup := le_sSup_sphereC_of_nonnegC hF hp
  have h2_sup := le_sSup_sphereC_of_nonnegC hF hq
  have h3_sup := le_sSup_sphereC_of_nonnegC hF hr
  refine ⟨hinf_nonneg, by linarith, by linarith, hsup_le_W⟩

/-- Extrema-attainment hypothesis on `ℂ³ \ {0}`: `F` attains its global maximum at a unit vector `p`
and attains its global minimum at a unit vector `s` on `sphereC`. -/
def AttainsExtremaC (F : (Fin 3 → ℂ) → ℝ) : Prop :=
  (∃ p : Fin 3 → ℂ, nsq p = 1 ∧ ∀ v : Fin 3 → ℂ, v ≠ 0 → F v ≤ F p) ∧
  (∃ s : Fin 3 → ℂ, nsq s = 1 ∧ ∀ v : Fin 3 → ℂ, v ≠ 0 → F s ≤ F v)

/-- Continuity on the compact complex unit sphere `sphereC` (`S⁵ ⊂ ℂ³`) alone implies
`AttainsExtremaC F` for any complex frame function `F`. -/
theorem attainsExtremaC_of_continuousOn_sphereC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsFrameFunctionC F W) (hc : ContinuousOn F sphereC) :
    AttainsExtremaC F := by
  constructor
  · obtain ⟨p, hp, hmax⟩ := isCompact_sphereC.exists_isMaxOn ⟨_, e1C_mem_sphereC⟩ hc
    refine ⟨p, hp, fun v hv => ?_⟩
    obtain ⟨c, hc0, hcv⟩ := exists_unit_smulC hv
    have : F (c • v) ≤ F p := hmax hcv
    rwa [hF.scale v hv c hc0] at this
  · obtain ⟨s, hs, hmin⟩ := isCompact_sphereC.exists_isMinOn ⟨_, e1C_mem_sphereC⟩ hc
    refine ⟨s, hs, fun v hv => ?_⟩
    obtain ⟨c, hc0, hcv⟩ := exists_unit_smulC hv
    have : F s ≤ F (c • v) := hmin hcv
    rwa [hF.scale v hv c hc0] at this

/-- Continuity on `ℂ³ \ {0}` implies `AttainsExtremaC F` for any complex frame function `F`. -/
theorem attainsExtremaC_of_continuousOn {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsFrameFunctionC F W) (hc : ContinuousOn F {v | v ≠ 0}) :
    AttainsExtremaC F :=
  attainsExtremaC_of_continuousOn_sphereC hF (hc.mono sphereC_subset)

/-- **Complex spectral positivity and eigenvalue ordering (`ℂ³`).**
For any nonnegative complex frame function `F` of weight `W` and any complex orthonormal frame
`(p, q, r)` where `p` maximizes `F` and `r` minimizes `F`, the three principal values `F p`,
`F q = W - F p - F r`, and `F r` satisfy `0 ≤ F r ≤ W - F p - F r ≤ F p ≤ W`. -/
theorem complex_eigenvalues_nonneg_and_ordered {F : (Fin 3 → ℂ) → ℝ} {W : ℝ}
    (hF : IsNonnegFrameFunctionC F W) {p q r : Fin 3 → ℂ} (hfr : IsOrthonormalC p q r)
    (hmax : ∀ v : Fin 3 → ℂ, v ≠ 0 → F v ≤ F p)
    (hmin : ∀ v : Fin 3 → ℂ, v ≠ 0 → F r ≤ F v) :
    F q = W - F p - F r ∧
    0 ≤ F r ∧
    F r ≤ W - F p - F r ∧
    W - F p - F r ≤ F p ∧
    F p ≤ W := by
  have hp1 : nsq p = 1 := by
    have := hfr.pp; rw [dotC_self_eq_nsq] at this; exact_mod_cast this
  have hq1 : nsq q = 1 := by
    have := hfr.qq; rw [dotC_self_eq_nsq] at this; exact_mod_cast this
  have hr1 : nsq r = 1 := by
    have := hfr.rr; rw [dotC_self_eq_nsq] at this; exact_mod_cast this
  have hp0 : p ≠ 0 := ne_zero_of_nsq_pos (by rw [hp1]; exact one_pos)
  have hq0 : q ≠ 0 := ne_zero_of_nsq_pos (by rw [hq1]; exact one_pos)
  have hr0 : r ≠ 0 := ne_zero_of_nsq_pos (by rw [hr1]; exact one_pos)
  have hsum := hF.frame p q r hp0 hq0 hr0 hfr.pq hfr.pr hfr.qr
  have hr_nn := hF.nonneg r hr0
  have hr_le_q := hmin q hq0
  have hq_le_p := hmax q hq0
  have hp_le_W := le_weight_of_nonnegC hF hp0
  refine ⟨by linarith, hr_nn, by linarith, by linarith, hp_le_W⟩

end GleasonComplex

namespace BornFinite.ContinuumDevelopment

open GleasonComplex Complex ComplexConjugate Matrix Filter Topology
open scoped BigOperators

noncomputable section

/-! ### Part E: Dimension `d = 3` to General Finite Dimension `d ≥ 3` Subspace Restriction Bridge -/

/-- `d`-dimensional squared norm `‖v‖² = ∑ i, |v_i|²` on `ℂ^d`. -/
def nsqD {d : ℕ} (v : Fin d → ℂ) : ℝ :=
  ∑ i : Fin d, Complex.normSq (v i)

lemma dotCD_add_left {d : ℕ} (u v w : Fin d → ℂ) :
    dotCD (u + v) w = dotCD u w + dotCD v w := by
  simp only [dotCD, Pi.add_apply, map_add, add_mul, Finset.sum_add_distrib]

lemma dotCD_add_right {d : ℕ} (u v w : Fin d → ℂ) :
    dotCD u (v + w) = dotCD u v + dotCD u w := by
  simp only [dotCD, Pi.add_apply, mul_add, Finset.sum_add_distrib]

lemma dotCD_sub_left {d : ℕ} (u v w : Fin d → ℂ) :
    dotCD (u - v) w = dotCD u w - dotCD v w := by
  simp only [dotCD, Pi.sub_apply, map_sub, sub_mul, Finset.sum_sub_distrib]

lemma dotCD_sub_right {d : ℕ} (u v w : Fin d → ℂ) :
    dotCD u (v - w) = dotCD u v - dotCD u w := by
  simp only [dotCD, Pi.sub_apply, mul_sub, Finset.sum_sub_distrib]

lemma dotCD_smul_left {d : ℕ} (c : ℂ) (u v : Fin d → ℂ) :
    dotCD (c • u) v = conj c * dotCD u v := by
  simp only [dotCD, Pi.smul_apply, smul_eq_mul, map_mul, mul_assoc, ← Finset.mul_sum]

lemma dotCD_smul_right {d : ℕ} (c : ℂ) (u v : Fin d → ℂ) :
    dotCD u (c • v) = c * dotCD u v := by
  simp only [dotCD, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => by ring

lemma dotCD_zero_left {d : ℕ} (v : Fin d → ℂ) :
    dotCD 0 v = 0 := by
  simp [dotCD]

lemma dotCD_zero_right {d : ℕ} (u : Fin d → ℂ) :
    dotCD u 0 = 0 := by
  simp [dotCD]

lemma dotCD_self_eq_nsqD {d : ℕ} (v : Fin d → ℂ) :
    dotCD v v = (nsqD v : ℂ) := by
  simp only [dotCD, nsqD, Complex.ofReal_sum, Complex.normSq_eq_conj_mul_self]

lemma nsqD_nonneg {d : ℕ} (v : Fin d → ℂ) :
    0 ≤ nsqD v :=
  Finset.sum_nonneg fun i _ => Complex.normSq_nonneg (v i)

lemma nsqD_eq_zero_iff {d : ℕ} (v : Fin d → ℂ) :
    nsqD v = 0 ↔ v = 0 := by
  unfold nsqD
  rw [Finset.sum_eq_zero_iff_of_nonneg (fun i _ => Complex.normSq_nonneg (v i))]
  constructor
  · intro h
    ext i
    exact Complex.normSq_eq_zero.mp (h i (Finset.mem_univ i))
  · rintro rfl i _
    simp

lemma nsqD_pos_iff_ne_zero {d : ℕ} (v : Fin d → ℂ) :
    0 < nsqD v ↔ v ≠ 0 := by
  constructor
  · intro h hv
    rw [hv, (nsqD_eq_zero_iff 0).mpr rfl] at h
    exact lt_irrefl 0 h
  · intro hv
    exact lt_of_le_of_ne (nsqD_nonneg v) (fun h => hv ((nsqD_eq_zero_iff v).mp h.symm))

lemma nsqD_smul {d : ℕ} (c : ℂ) (v : Fin d → ℂ) :
    nsqD (c • v) = Complex.normSq c * nsqD v := by
  simp only [nsqD, Pi.smul_apply, smul_eq_mul, map_mul, ← Finset.mul_sum]

lemma nsqD_single {d : ℕ} (i : Fin d) (c : ℂ) :
    nsqD (Pi.single i c) = Complex.normSq c := by
  unfold nsqD
  rw [Finset.sum_eq_single i]
  · simp
  · intro j _ hji
    simp [Pi.single_eq_of_ne hji]
  · intro hi
    exact False.elim (hi (Finset.mem_univ i))

lemma dotCD_single_single {d : ℕ} (i j : Fin d) (a b : ℂ) :
    dotCD (Pi.single i a) (Pi.single j b) = if i = j then conj a * b else 0 := by
  unfold dotCD
  rw [Finset.sum_eq_single i]
  · by_cases hij : i = j
    · subst hij; simp
    · simp [hij]
  · intro k _ hki
    simp [Pi.single_eq_of_ne hki]
  · intro hi
    exact False.elim (hi (Finset.mem_univ i))

/-- Orthonormal triple of vectors `(e₁, e₂, e₃)` in `ℂ^d`. -/
def IsOrthonormalTripleD {d : ℕ} (e₁ e₂ e₃ : Fin d → ℂ) : Prop :=
  nsqD e₁ = 1 ∧ nsqD e₂ = 1 ∧ nsqD e₃ = 1 ∧
  dotCD e₁ e₂ = 0 ∧ dotCD e₁ e₃ = 0 ∧ dotCD e₂ e₃ = 0

/-- Any three distinct standard coordinate basis vectors in `ℂ^d` form an orthonormal triple. -/
theorem isOrthonormalTripleD_single {d : ℕ} {i₀ i₁ i₂ : Fin d}
    (h01 : i₀ ≠ i₁) (h02 : i₀ ≠ i₂) (h12 : i₁ ≠ i₂) :
    IsOrthonormalTripleD (Pi.single i₀ 1) (Pi.single i₁ 1) (Pi.single i₂ 1) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp [nsqD_single]
  · simp [nsqD_single]
  · simp [nsqD_single]
  · simp [dotCD_single_single, h01]
  · simp [dotCD_single_single, h02]
  · simp [dotCD_single_single, h12]

/-- Isometric linear embedding `ℂ³ → ℂ^d` spanned by `(e₁, e₂, e₃)`. -/
def embed3D {d : ℕ} (e₁ e₂ e₃ : Fin d → ℂ) (x : Fin 3 → ℂ) : Fin d → ℂ :=
  x 0 • e₁ + x 1 • e₂ + x 2 • e₃

lemma embed3D_add {d : ℕ} (e₁ e₂ e₃ : Fin d → ℂ) (x y : Fin 3 → ℂ) :
    embed3D e₁ e₂ e₃ (x + y) = embed3D e₁ e₂ e₃ x + embed3D e₁ e₂ e₃ y := by
  ext i; simp [embed3D]; ring

lemma embed3D_sub {d : ℕ} (e₁ e₂ e₃ : Fin d → ℂ) (x y : Fin 3 → ℂ) :
    embed3D e₁ e₂ e₃ (x - y) = embed3D e₁ e₂ e₃ x - embed3D e₁ e₂ e₃ y := by
  ext i; simp [embed3D]; ring

lemma embed3D_smul {d : ℕ} (e₁ e₂ e₃ : Fin d → ℂ) (c : ℂ) (x : Fin 3 → ℂ) :
    embed3D e₁ e₂ e₃ (c • x) = c • embed3D e₁ e₂ e₃ x := by
  ext i; simp [embed3D]; ring

lemma embed3D_zero {d : ℕ} (e₁ e₂ e₃ : Fin d → ℂ) :
    embed3D e₁ e₂ e₃ 0 = 0 := by
  ext i; simp [embed3D]

lemma embed3D_e0 {d : ℕ} (e₁ e₂ e₃ : Fin d → ℂ) :
    embed3D e₁ e₂ e₃ ![1, 0, 0] = e₁ := by
  ext i; simp [embed3D]

lemma embed3D_e1 {d : ℕ} (e₁ e₂ e₃ : Fin d → ℂ) :
    embed3D e₁ e₂ e₃ ![0, 1, 0] = e₂ := by
  ext i; simp [embed3D]

lemma embed3D_e2 {d : ℕ} (e₁ e₂ e₃ : Fin d → ℂ) :
    embed3D e₁ e₂ e₃ ![0, 0, 1] = e₃ := by
  ext i; simp [embed3D]

/-- `embed3D` preserves the Hermitian inner product when `(e₁, e₂, e₃)` is an orthonormal triple in `ℂ^d`. -/
theorem dotCD_embed3D {d : ℕ} {e₁ e₂ e₃ : Fin d → ℂ}
    (h : IsOrthonormalTripleD e₁ e₂ e₃) (x y : Fin 3 → ℂ) :
    dotCD (embed3D e₁ e₂ e₃ x) (embed3D e₁ e₂ e₃ y) = GleasonComplex.dotC x y := by
  rcases h with ⟨h1, h2, h3, h12, h13, h23⟩
  have h11 : dotCD e₁ e₁ = 1 := by rw [dotCD_self_eq_nsqD, h1]; simp
  have h22 : dotCD e₂ e₂ = 1 := by rw [dotCD_self_eq_nsqD, h2]; simp
  have h33 : dotCD e₃ e₃ = 1 := by rw [dotCD_self_eq_nsqD, h3]; simp
  have h21 : dotCD e₂ e₁ = 0 := by rw [← dotCD_conj_symm, h12, map_zero]
  have h31 : dotCD e₃ e₁ = 0 := by rw [← dotCD_conj_symm, h13, map_zero]
  have h32 : dotCD e₃ e₂ = 0 := by rw [← dotCD_conj_symm, h23, map_zero]
  simp only [embed3D, dotCD_add_left, dotCD_add_right, dotCD_smul_left, dotCD_smul_right,
    h11, h22, h33, h12, h13, h23, h21, h31, h32, GleasonComplex.dotC]
  ring

/-- `embed3D` is an isometry (`nsqD (embed3D e₁ e₂ e₃ x) = nsq x`) when `(e₁, e₂, e₃)` is orthonormal. -/
theorem nsqD_embed3D {d : ℕ} {e₁ e₂ e₃ : Fin d → ℂ}
    (h : IsOrthonormalTripleD e₁ e₂ e₃) (x : Fin 3 → ℂ) :
    nsqD (embed3D e₁ e₂ e₃ x) = GleasonComplex.nsq x := by
  have hd := dotCD_embed3D h x x
  rw [dotCD_self_eq_nsqD, GleasonComplex.dotC_self_eq_nsq] at hd
  exact_mod_cast hd

/-- `embed3D e₁ e₂ e₃ x` is nonzero if and only if `x` is nonzero. -/
theorem embed3D_ne_zero_iff {d : ℕ} {e₁ e₂ e₃ : Fin d → ℂ}
    (h : IsOrthonormalTripleD e₁ e₂ e₃) (x : Fin 3 → ℂ) :
    embed3D e₁ e₂ e₃ x ≠ 0 ↔ x ≠ 0 := by
  refine not_congr ?_
  rw [← nsqD_eq_zero_iff, nsqD_embed3D h, GleasonComplex.nsq_eq_zero_iff]

/-- Continuity of `embed3D e₁ e₂ e₃ : (Fin 3 → ℂ) → (Fin d → ℂ)`. -/
theorem continuous_embed3D {d : ℕ} (e₁ e₂ e₃ : Fin d → ℂ) :
    Continuous (embed3D e₁ e₂ e₃) := by
  unfold embed3D
  fun_prop

/-- Orthonormal basis of `ℂ^d`. -/
def IsOrthonormalBasisD {d : ℕ} (B : Fin d → Fin d → ℂ) : Prop :=
  (∀ i : Fin d, nsqD (B i) = 1) ∧ (∀ i j : Fin d, i ≠ j → dotCD (B i) (B j) = 0)

/-- The standard coordinate basis `i ↦ Pi.single i 1` is an orthonormal basis of `ℂ^d`. -/
theorem isOrthonormalBasisD_single {d : ℕ} :
    IsOrthonormalBasisD (fun i : Fin d => Pi.single i (1 : ℂ)) :=
  ⟨fun i => by simp [nsqD_single], fun i j hij => by simp [dotCD_single_single, hij]⟩

/-- Any three pairwise distinct vectors of an orthonormal basis of `ℂ^d` form an orthonormal triple. -/
theorem isOrthonormalTripleD_of_basis {d : ℕ} {B : Fin d → Fin d → ℂ}
    (hB : IsOrthonormalBasisD B) {i₀ i₁ i₂ : Fin d}
    (h01 : i₀ ≠ i₁) (h02 : i₀ ≠ i₂) (h12 : i₁ ≠ i₂) :
    IsOrthonormalTripleD (B i₀) (B i₁) (B i₂) :=
  ⟨hB.1 i₀, hB.1 i₁, hB.1 i₂, hB.2 i₀ i₁ h01, hB.2 i₀ i₂ h02, hB.2 i₁ i₂ h12⟩

/-- Replace the three slots `(i₀, i₁, i₂)` of a `d`-element family `B` by `(u₀, u₁, u₂)`. -/
def replaceBasis3D {d : ℕ} (B : Fin d → Fin d → ℂ) (i₀ i₁ i₂ : Fin d)
    (u₀ u₁ u₂ : Fin d → ℂ) (i : Fin d) : Fin d → ℂ :=
  if i = i₀ then u₀ else if i = i₁ then u₁ else if i = i₂ then u₂ else B i

private lemma dotCD_embed3D_basis_other {d : ℕ} {B : Fin d → Fin d → ℂ}
    (hB : IsOrthonormalBasisD B) {i₀ i₁ i₂ j : Fin d}
    (hj0 : j ≠ i₀) (hj1 : j ≠ i₁) (hj2 : j ≠ i₂) (x : Fin 3 → ℂ) :
    dotCD (embed3D (B i₀) (B i₁) (B i₂) x) (B j) = 0 ∧
    dotCD (B j) (embed3D (B i₀) (B i₁) (B i₂) x) = 0 := by
  have h0j : dotCD (B i₀) (B j) = 0 := hB.2 i₀ j hj0.symm
  have h1j : dotCD (B i₁) (B j) = 0 := hB.2 i₁ j hj1.symm
  have h2j : dotCD (B i₂) (B j) = 0 := hB.2 i₂ j hj2.symm
  have hj0' : dotCD (B j) (B i₀) = 0 := hB.2 j i₀ hj0
  have hj1' : dotCD (B j) (B i₁) = 0 := hB.2 j i₁ hj1
  have hj2' : dotCD (B j) (B i₂) = 0 := hB.2 j i₂ hj2
  constructor
  · simp [embed3D, dotCD_add_left, dotCD_smul_left, h0j, h1j, h2j]
  · simp [embed3D, dotCD_add_right, dotCD_smul_right, hj0', hj1', hj2']

private lemma replaceBasis3D_eq {d : ℕ} (B : Fin d → Fin d → ℂ) {i₀ i₁ i₂ : Fin d}
    (h01 : i₀ ≠ i₁) (h02 : i₀ ≠ i₂) (h12 : i₁ ≠ i₂) (u₀ u₁ u₂ : Fin d → ℂ) :
    replaceBasis3D B i₀ i₁ i₂ u₀ u₁ u₂ i₀ = u₀ ∧
    replaceBasis3D B i₀ i₁ i₂ u₀ u₁ u₂ i₁ = u₁ ∧
    replaceBasis3D B i₀ i₁ i₂ u₀ u₁ u₂ i₂ = u₂ ∧
    (∀ k : Fin d, k ≠ i₀ → k ≠ i₁ → k ≠ i₂ → replaceBasis3D B i₀ i₁ i₂ u₀ u₁ u₂ k = B k) := by
  refine ⟨by simp [replaceBasis3D], by simp [replaceBasis3D, h01.symm],
    by simp [replaceBasis3D, h02.symm, h12.symm],
    fun k hk0 hk1 hk2 => by simp [replaceBasis3D, hk0, hk1, hk2]⟩

/-- Rotating three distinct slots `(i₀, i₁, i₂)` of an orthonormal basis `B` of `ℂ^d` by any
orthonormal triple `(x, y, z)` in `ℂ³` produces another orthonormal basis of `ℂ^d`. -/
theorem isOrthonormalBasisD_replaceBasis3D {d : ℕ} {B : Fin d → Fin d → ℂ}
    (hB : IsOrthonormalBasisD B) {i₀ i₁ i₂ : Fin d}
    (h01 : i₀ ≠ i₁) (h02 : i₀ ≠ i₂) (h12 : i₁ ≠ i₂)
    {x y z : Fin 3 → ℂ} (hxyz : GleasonComplex.IsOrthonormalC x y z) :
    IsOrthonormalBasisD
      (replaceBasis3D B i₀ i₁ i₂
        (embed3D (B i₀) (B i₁) (B i₂) x)
        (embed3D (B i₀) (B i₁) (B i₂) y)
        (embed3D (B i₀) (B i₁) (B i₂) z)) := by
  have htr : IsOrthonormalTripleD (B i₀) (B i₁) (B i₂) :=
    isOrthonormalTripleD_of_basis hB h01 h02 h12
  have hx1 : GleasonComplex.nsq x = 1 := by
    have := hxyz.pp; rw [GleasonComplex.dotC_self_eq_nsq] at this; exact_mod_cast this
  have hy1 : GleasonComplex.nsq y = 1 := by
    have := hxyz.qq; rw [GleasonComplex.dotC_self_eq_nsq] at this; exact_mod_cast this
  have hz1 : GleasonComplex.nsq z = 1 := by
    have := hxyz.rr; rw [GleasonComplex.dotC_self_eq_nsq] at this; exact_mod_cast this
  have hyx : GleasonComplex.dotC y x = 0 := by
    rw [GleasonComplex.dotC_conj_symm, hxyz.pq, map_zero]
  have hzx : GleasonComplex.dotC z x = 0 := by
    rw [GleasonComplex.dotC_conj_symm, hxyz.pr, map_zero]
  have hzy : GleasonComplex.dotC z y = 0 := by
    rw [GleasonComplex.dotC_conj_symm, hxyz.qr, map_zero]
  rcases replaceBasis3D_eq B h01 h02 h12
    (embed3D (B i₀) (B i₁) (B i₂) x)
    (embed3D (B i₀) (B i₁) (B i₂) y)
    (embed3D (B i₀) (B i₁) (B i₂) z) with ⟨hr0, hr1, hr2, hro⟩
  refine ⟨?_, ?_⟩
  · intro i
    unfold replaceBasis3D
    split_ifs
    · rw [nsqD_embed3D htr, hx1]
    · rw [nsqD_embed3D htr, hy1]
    · rw [nsqD_embed3D htr, hz1]
    · exact hB.1 i
  · intro i j hij
    by_cases hi0 : i = i₀
    · rw [hi0, hr0]
      by_cases hj0 : j = i₀
      · exact False.elim (hij (hi0.trans hj0.symm))
      · by_cases hj1 : j = i₁
        · rw [hj1, hr1, dotCD_embed3D htr]; exact hxyz.pq
        · by_cases hj2 : j = i₂
          · rw [hj2, hr2, dotCD_embed3D htr]; exact hxyz.pr
          · rw [hro j hj0 hj1 hj2]; exact (dotCD_embed3D_basis_other hB hj0 hj1 hj2 x).1
    · by_cases hi1 : i = i₁
      · rw [hi1, hr1]
        by_cases hj0 : j = i₀
        · rw [hj0, hr0, dotCD_embed3D htr]; exact hyx
        · by_cases hj1 : j = i₁
          · exact False.elim (hij (hi1.trans hj1.symm))
          · by_cases hj2 : j = i₂
            · rw [hj2, hr2, dotCD_embed3D htr]; exact hxyz.qr
            · rw [hro j hj0 hj1 hj2]; exact (dotCD_embed3D_basis_other hB hj0 hj1 hj2 y).1
      · by_cases hi2 : i = i₂
        · rw [hi2, hr2]
          by_cases hj0 : j = i₀
          · rw [hj0, hr0, dotCD_embed3D htr]; exact hzx
          · by_cases hj1 : j = i₁
            · rw [hj1, hr1, dotCD_embed3D htr]; exact hzy
            · by_cases hj2 : j = i₂
              · exact False.elim (hij (hi2.trans hj2.symm))
              · rw [hro j hj0 hj1 hj2]; exact (dotCD_embed3D_basis_other hB hj0 hj1 hj2 z).1
        · rw [hro i hi0 hi1 hi2]
          by_cases hj0 : j = i₀
          · rw [hj0, hr0]; exact (dotCD_embed3D_basis_other hB hi0 hi1 hi2 x).2
          · by_cases hj1 : j = i₁
            · rw [hj1, hr1]; exact (dotCD_embed3D_basis_other hB hi0 hi1 hi2 y).2
            · by_cases hj2 : j = i₂
              · rw [hj2, hr2]; exact (dotCD_embed3D_basis_other hB hi0 hi1 hi2 z).2
              · rw [hro j hj0 hj1 hj2]; exact hB.2 i j hij

/-- Exact telescoping identity for 3-slot basis replacement: replacing `(B i₀, B i₁, B i₂)` by
`(u₀, u₁, u₂)` changes the basis sum of `F` by `(F u₀ + F u₁ + F u₂) - (F (B i₀) + F (B i₁) + F (B i₂))`. -/
theorem sum_replaceBasis3D_sub {d : ℕ} (F : (Fin d → ℂ) → ℝ)
    (B : Fin d → Fin d → ℂ) {i₀ i₁ i₂ : Fin d}
    (h01 : i₀ ≠ i₁) (h02 : i₀ ≠ i₂) (h12 : i₁ ≠ i₂)
    (u₀ u₁ u₂ : Fin d → ℂ) :
    (∑ i : Fin d, F (replaceBasis3D B i₀ i₁ i₂ u₀ u₁ u₂ i)) - (∑ i : Fin d, F (B i)) =
      (F u₀ + F u₁ + F u₂) - (F (B i₀) + F (B i₁) + F (B i₂)) := by
  rw [← Finset.sum_sub_distrib]
  have hterm : ∀ i : Fin d,
      F (replaceBasis3D B i₀ i₁ i₂ u₀ u₁ u₂ i) - F (B i) =
        (if i = i₀ then F u₀ - F (B i₀) else 0) +
        (if i = i₁ then F u₁ - F (B i₁) else 0) +
        (if i = i₂ then F u₂ - F (B i₂) else 0) := by
    intro i
    unfold replaceBasis3D
    by_cases hi0 : i = i₀
    · subst hi0; simp [h01, h02]
    · by_cases hi1 : i = i₁
      · subst hi1; simp [hi0, h12]
      · by_cases hi2 : i = i₂
        · subst hi2; simp [hi0, hi1]
        · simp [hi0, hi1, hi2]
  simp_rw [hterm]
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, ↓reduceIte]
  ring

/-- A `d`-dimensional frame function of weight `W` on `ℂ^d`: scale-invariant on nonzero vectors
and summing to `W` on every orthonormal basis of `ℂ^d`. -/
structure IsFrameFunctionD {d : ℕ} (F : (Fin d → ℂ) → ℝ) (W : ℝ) : Prop where
  scale : ∀ v : Fin d → ℂ, v ≠ 0 → ∀ c : ℂ, c ≠ 0 → F (c • v) = F v
  basis_sum : ∀ B : Fin d → Fin d → ℂ, IsOrthonormalBasisD B → (∑ i : Fin d, F (B i)) = W

/-- Subspace 3-frame additivity on `ℂ^d`: scale-invariance on nonzero vectors together with
3-frame weight conservation `F(embed3D x) + F(embed3D y) + F(embed3D z) = F e₁ + F e₂ + F e₃`
on every 3D subspace spanned by an orthonormal triple `(e₁, e₂, e₃)` in `ℂ^d`. -/
structure HasSubspace3FrameAdditivityD {d : ℕ} (F : (Fin d → ℂ) → ℝ) : Prop where
  scale : ∀ v : Fin d → ℂ, v ≠ 0 → ∀ c : ℂ, c ≠ 0 → F (c • v) = F v
  subspace_frame : ∀ {e₁ e₂ e₃ : Fin d → ℂ}, IsOrthonormalTripleD e₁ e₂ e₃ →
    ∀ x y z : Fin 3 → ℂ, x ≠ 0 → y ≠ 0 → z ≠ 0 →
      GleasonComplex.dotC x y = 0 → GleasonComplex.dotC x z = 0 → GleasonComplex.dotC y z = 0 →
      F (embed3D e₁ e₂ e₃ x) + F (embed3D e₁ e₂ e₃ y) + F (embed3D e₁ e₂ e₃ z) =
        F e₁ + F e₂ + F e₃

/-- Restriction of `F : (Fin d → ℂ) → ℝ` to the 3D subspace spanned by `(e₁, e₂, e₃)`. -/
def restrict3D {d : ℕ} (F : (Fin d → ℂ) → ℝ) (e₁ e₂ e₃ : Fin d → ℂ) (x : Fin 3 → ℂ) : ℝ :=
  F (embed3D e₁ e₂ e₃ x)

/-- Restricting any `d`-dimensional frame function `F` (`IsFrameFunctionD F W`) to the 3D subspace
spanned by three distinct basis vectors `(B i₀, B i₁, B i₂)` of an orthonormal basis `B` yields a
`ℂ³` frame function `IsFrameFunctionC` of weight `F (B i₀) + F (B i₁) + F (B i₂)`. -/
theorem isFrameFunctionC_restrict3D_of_basis {d : ℕ} {F : (Fin d → ℂ) → ℝ} {W : ℝ}
    (hF : IsFrameFunctionD F W) {B : Fin d → Fin d → ℂ} (hB : IsOrthonormalBasisD B)
    {i₀ i₁ i₂ : Fin d} (h01 : i₀ ≠ i₁) (h02 : i₀ ≠ i₂) (h12 : i₁ ≠ i₂) :
    GleasonComplex.IsFrameFunctionC (restrict3D F (B i₀) (B i₁) (B i₂))
      (F (B i₀) + F (B i₁) + F (B i₂)) where
  scale v hv c hc := by
    have htr := isOrthonormalTripleD_of_basis hB h01 h02 h12
    show F (embed3D (B i₀) (B i₁) (B i₂) (c • v)) = F (embed3D (B i₀) (B i₁) (B i₂) v)
    rw [embed3D_smul, hF.scale _ ((embed3D_ne_zero_iff htr v).mpr hv) c hc]
  frame u v w hu hv hw huv huw hvw := by
    have htr := isOrthonormalTripleD_of_basis hB h01 h02 h12
    obtain ⟨cu, hcu0, hcu1⟩ := GleasonComplex.exists_unit_smulC hu
    obtain ⟨cv, hcv0, hcv1⟩ := GleasonComplex.exists_unit_smulC hv
    obtain ⟨cw, hcw0, hcw1⟩ := GleasonComplex.exists_unit_smulC hw
    set x := cu • u
    set y := cv • v
    set z := cw • w
    have hxyz : GleasonComplex.IsOrthonormalC x y z := by
      refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
      · rw [GleasonComplex.dotC_self_eq_nsq, show GleasonComplex.nsq x = 1 from hcu1]; simp
      · rw [GleasonComplex.dotC_self_eq_nsq, show GleasonComplex.nsq y = 1 from hcv1]; simp
      · rw [GleasonComplex.dotC_self_eq_nsq, show GleasonComplex.nsq z = 1 from hcw1]; simp
      · simp [x, y, GleasonComplex.dotC_smul_left, GleasonComplex.dotC_smul_right, huv]
      · simp [x, z, GleasonComplex.dotC_smul_left, GleasonComplex.dotC_smul_right, huw]
      · simp [y, z, GleasonComplex.dotC_smul_left, GleasonComplex.dotC_smul_right, hvw]
    have hB' := isOrthonormalBasisD_replaceBasis3D hB h01 h02 h12 hxyz
    have hsum' := hF.basis_sum _ hB'
    have hsumB := hF.basis_sum B hB
    have hdiff := sum_replaceBasis3D_sub F B h01 h02 h12
      (embed3D (B i₀) (B i₁) (B i₂) x)
      (embed3D (B i₀) (B i₁) (B i₂) y)
      (embed3D (B i₀) (B i₁) (B i₂) z)
    rw [hsum', hsumB, sub_self] at hdiff
    have hx_eq : F (embed3D (B i₀) (B i₁) (B i₂) x) = F (embed3D (B i₀) (B i₁) (B i₂) u) := by
      rw [show x = cu • u from rfl, embed3D_smul,
        hF.scale _ ((embed3D_ne_zero_iff htr u).mpr hu) cu hcu0]
    have hy_eq : F (embed3D (B i₀) (B i₁) (B i₂) y) = F (embed3D (B i₀) (B i₁) (B i₂) v) := by
      rw [show y = cv • v from rfl, embed3D_smul,
        hF.scale _ ((embed3D_ne_zero_iff htr v).mpr hv) cv hcv0]
    have hz_eq : F (embed3D (B i₀) (B i₁) (B i₂) z) = F (embed3D (B i₀) (B i₁) (B i₂) w) := by
      rw [show z = cw • w from rfl, embed3D_smul,
        hF.scale _ ((embed3D_ne_zero_iff htr w).mpr hw) cw hcw0]
    unfold restrict3D
    linarith

/-- Restricting any `F` satisfying `HasSubspace3FrameAdditivityD F` to the 3D subspace spanned by
an orthonormal triple `(e₁, e₂, e₃)` yields a `ℂ³` frame function of weight `F e₁ + F e₂ + F e₃`. -/
theorem isFrameFunctionC_restrict3D {d : ℕ} {F : (Fin d → ℂ) → ℝ}
    (hF : HasSubspace3FrameAdditivityD F)
    {e₁ e₂ e₃ : Fin d → ℂ} (h : IsOrthonormalTripleD e₁ e₂ e₃) :
    GleasonComplex.IsFrameFunctionC (restrict3D F e₁ e₂ e₃) (F e₁ + F e₂ + F e₃) where
  scale v hv c hc := by
    show F (embed3D e₁ e₂ e₃ (c • v)) = F (embed3D e₁ e₂ e₃ v)
    rw [embed3D_smul, hF.scale _ ((embed3D_ne_zero_iff h v).mpr hv) c hc]
  frame u v w hu hv hw huv huw hvw :=
    hF.subspace_frame h u v w hu hv hw huv huw hvw

/-- Nonnegativity and 3-frame additivity lift to `IsNonnegFrameFunctionC` on every 3D subspace. -/
theorem isNonnegFrameFunctionC_restrict3D {d : ℕ} {F : (Fin d → ℂ) → ℝ}
    (hF : HasSubspace3FrameAdditivityD F)
    (hnonneg : ∀ v : Fin d → ℂ, v ≠ 0 → 0 ≤ F v)
    {e₁ e₂ e₃ : Fin d → ℂ} (h : IsOrthonormalTripleD e₁ e₂ e₃) :
    GleasonComplex.IsNonnegFrameFunctionC (restrict3D F e₁ e₂ e₃) (F e₁ + F e₂ + F e₃) where
  toIsFrameFunctionC := isFrameFunctionC_restrict3D hF h
  nonneg x hx := hnonneg (embed3D e₁ e₂ e₃ x) ((embed3D_ne_zero_iff h x).mpr hx)

/-- Nonnegativity and `IsFrameFunctionD` lift to `IsNonnegFrameFunctionC` on any 3 basis vectors. -/
theorem isNonnegFrameFunctionC_restrict3D_of_basis {d : ℕ} {F : (Fin d → ℂ) → ℝ} {W : ℝ}
    (hF : IsFrameFunctionD F W)
    (hnonneg : ∀ v : Fin d → ℂ, v ≠ 0 → 0 ≤ F v)
    {B : Fin d → Fin d → ℂ} (hB : IsOrthonormalBasisD B)
    {i₀ i₁ i₂ : Fin d} (h01 : i₀ ≠ i₁) (h02 : i₀ ≠ i₂) (h12 : i₁ ≠ i₂) :
    GleasonComplex.IsNonnegFrameFunctionC (restrict3D F (B i₀) (B i₁) (B i₂))
      (F (B i₀) + F (B i₁) + F (B i₂)) where
  toIsFrameFunctionC := isFrameFunctionC_restrict3D_of_basis hF hB h01 h02 h12
  nonneg x hx :=
    hnonneg _ ((embed3D_ne_zero_iff (isOrthonormalTripleD_of_basis hB h01 h02 h12) x).mpr hx)

/-- Continuity of `F` on `ℂ^d \ {0}` implies continuity of `restrict3D F e₁ e₂ e₃` on `ℂ³ \ {0}`. -/
theorem continuousOn_restrict3D {d : ℕ} {F : (Fin d → ℂ) → ℝ}
    (hc : ContinuousOn F {v : Fin d → ℂ | v ≠ 0})
    {e₁ e₂ e₃ : Fin d → ℂ} (h : IsOrthonormalTripleD e₁ e₂ e₃) :
    ContinuousOn (restrict3D F e₁ e₂ e₃) {x : Fin 3 → ℂ | x ≠ 0} :=
  hc.comp (continuous_embed3D e₁ e₂ e₃).continuousOn
    (fun x hx => (embed3D_ne_zero_iff h x).mpr hx)

/-- **3D Subspace Gleason Representation in `ℂ^d`.**  For any continuous `F` on `ℂ^d \ {0}`
satisfying `HasSubspace3FrameAdditivityD F` and any orthonormal triple `(e₁, e₂, e₃)` in `ℂ^d`,
the restriction `restrict3D F e₁ e₂ e₃` has the spectral quadratic representation of
`GleasonComplex.gleason_complex`. -/
theorem gleason_subspace3D_of_continuousD {d : ℕ} {F : (Fin d → ℂ) → ℝ}
    (hF : HasSubspace3FrameAdditivityD F)
    (hc : ContinuousOn F {v : Fin d → ℂ | v ≠ 0})
    {e₁ e₂ e₃ : Fin d → ℂ} (h : IsOrthonormalTripleD e₁ e₂ e₃) :
    ∃ p q r : Fin 3 → ℂ, GleasonComplex.IsOrthonormalC p q r ∧ ∃ M α m : ℝ,
      ∀ x : Fin 3 → ℂ, x ≠ 0 →
        F (embed3D e₁ e₂ e₃ x) =
          (M * Complex.normSq (GleasonComplex.dotC p x) +
           α * Complex.normSq (GleasonComplex.dotC q x) +
           m * Complex.normSq (GleasonComplex.dotC r x)) / GleasonComplex.nsq x :=
  GleasonComplex.gleason_complex (isFrameFunctionC_restrict3D hF h) (continuousOn_restrict3D hc h)

/-- **3D Basis-Subspace Gleason Representation in `ℂ^d`.**  For any continuous `d`-dimensional
frame function `F` (`IsFrameFunctionD F W`) on `ℂ^d \ {0}` and any three pairwise distinct basis
indices `i₀, i₁, i₂ : Fin d` of an orthonormal basis `B` (`IsOrthonormalBasisD B`), the 3D
restriction `restrict3D F (B i₀) (B i₁) (B i₂)` has the spectral quadratic representation of
`GleasonComplex.gleason_complex`. -/
theorem gleason_basis3D_of_continuousD {d : ℕ} {F : (Fin d → ℂ) → ℝ} {W : ℝ}
    (hF : IsFrameFunctionD F W)
    (hc : ContinuousOn F {v : Fin d → ℂ | v ≠ 0})
    {B : Fin d → Fin d → ℂ} (hB : IsOrthonormalBasisD B)
    {i₀ i₁ i₂ : Fin d} (h01 : i₀ ≠ i₁) (h02 : i₀ ≠ i₂) (h12 : i₁ ≠ i₂) :
    ∃ p q r : Fin 3 → ℂ, GleasonComplex.IsOrthonormalC p q r ∧ ∃ M α m : ℝ,
      ∀ x : Fin 3 → ℂ, x ≠ 0 →
        F (embed3D (B i₀) (B i₁) (B i₂) x) =
          (M * Complex.normSq (GleasonComplex.dotC p x) +
           α * Complex.normSq (GleasonComplex.dotC q x) +
           m * Complex.normSq (GleasonComplex.dotC r x)) / GleasonComplex.nsq x :=
  GleasonComplex.gleason_complex
    (isFrameFunctionC_restrict3D_of_basis hF hB h01 h02 h12)
    (continuousOn_restrict3D hc (isOrthonormalTripleD_of_basis hB h01 h02 h12))

/-- **Continuity-Free Pure-State Gleason Theorem on 3D Subspaces of `ℂ^d`.**  For any nonnegative
`F` on `ℂ^d \ {0}` satisfying `HasSubspace3FrameAdditivityD F` and any orthonormal triple
`(e₁, e₂, e₃)`, if `F` attains the full 3D subspace weight `F e₁ + F e₂ + F e₃` at a unit vector
`embed3D e₁ e₂ e₃ p₀` (`nsq p₀ = 1`), then `F (embed3D e₁ e₂ e₃ x) = (F e₁ + F e₂ + F e₃) * |⟨p₀, x⟩|² / ‖x‖²`
for all `x ≠ 0`, with zero continuity assumption on `F`. -/
theorem pure_state_nonneg_gleason_subspace3D {d : ℕ} {F : (Fin d → ℂ) → ℝ}
    (hF : HasSubspace3FrameAdditivityD F)
    (hnonneg : ∀ v : Fin d → ℂ, v ≠ 0 → 0 ≤ F v)
    {e₁ e₂ e₃ : Fin d → ℂ} (h : IsOrthonormalTripleD e₁ e₂ e₃)
    {p₀ : Fin 3 → ℂ} (hp₀ : GleasonComplex.nsq p₀ = 1)
    (hpW : F (embed3D e₁ e₂ e₃ p₀) = F e₁ + F e₂ + F e₃) :
    ∀ x : Fin 3 → ℂ, x ≠ 0 →
      F (embed3D e₁ e₂ e₃ x) =
        (F e₁ + F e₂ + F e₃) * Complex.normSq (GleasonComplex.dotC p₀ x) / GleasonComplex.nsq x :=
  GleasonComplex.pure_state_nonneg_gleason_complex
    (isNonnegFrameFunctionC_restrict3D hF hnonneg h) hp₀ hpW

/-- **Continuity-Free Pure-State Gleason Theorem on Basis 3-Subspaces of `ℂ^d`.**  Directly from
`IsFrameFunctionD F W` and `IsOrthonormalBasisD B` for pairwise distinct `i₀, i₁, i₂ : Fin d`,
without assuming continuity of `F`. -/
theorem pure_state_nonneg_gleason_basis3D {d : ℕ} {F : (Fin d → ℂ) → ℝ} {W : ℝ}
    (hF : IsFrameFunctionD F W)
    (hnonneg : ∀ v : Fin d → ℂ, v ≠ 0 → 0 ≤ F v)
    {B : Fin d → Fin d → ℂ} (hB : IsOrthonormalBasisD B)
    {i₀ i₁ i₂ : Fin d} (h01 : i₀ ≠ i₁) (h02 : i₀ ≠ i₂) (h12 : i₁ ≠ i₂)
    {p₀ : Fin 3 → ℂ} (hp₀ : GleasonComplex.nsq p₀ = 1)
    (hpW : F (embed3D (B i₀) (B i₁) (B i₂) p₀) = F (B i₀) + F (B i₁) + F (B i₂)) :
    ∀ x : Fin 3 → ℂ, x ≠ 0 →
      F (embed3D (B i₀) (B i₁) (B i₂) x) =
        (F (B i₀) + F (B i₁) + F (B i₂)) *
          Complex.normSq (GleasonComplex.dotC p₀ x) / GleasonComplex.nsq x :=
  GleasonComplex.pure_state_nonneg_gleason_complex
    (isNonnegFrameFunctionC_restrict3D_of_basis hF hnonneg hB h01 h02 h12) hp₀ hpW

/-- `d`-dimensional Rayleigh quotient `Re ⟨v, M v⟩ / ‖v‖²` of `M : Matrix (Fin d) (Fin d) ℂ`. -/
def complexRayleighD {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ) (v : Fin d → ℂ) : ℝ :=
  complexQuadFormD M v / nsqD v

lemma complexQuadFormD_smul {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ) (c : ℂ) (v : Fin d → ℂ) :
    complexQuadFormD M (c • v) = Complex.normSq c * complexQuadFormD M v := by
  unfold complexQuadFormD
  rw [Matrix.mulVec_smul, dotCD_smul_left, dotCD_smul_right, ← mul_assoc,
    ← Complex.normSq_eq_conj_mul_self, Complex.re_ofReal_mul]

lemma complexRayleighD_smul {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ)
    {v : Fin d → ℂ} (_hv : v ≠ 0) {c : ℂ} (hc : c ≠ 0) :
    complexRayleighD M (c • v) = complexRayleighD M v := by
  unfold complexRayleighD
  rw [complexQuadFormD_smul, nsqD_smul,
    mul_div_mul_left _ _ (Complex.normSq_pos.mpr hc).ne']

/-- `d`-dimensional parallelogram law for the quadratic form `complexQuadFormD M`:
`Q(u + v) + Q(u - v) = 2 Q(u) + 2 Q(v)`. -/
theorem complexQuadFormD_parallelogram {d : ℕ} {M : Matrix (Fin d) (Fin d) ℂ}
    (_hM : M.IsHermitian) (u v : Fin d → ℂ) :
    complexQuadFormD M (u + v) + complexQuadFormD M (u - v) =
      2 * complexQuadFormD M u + 2 * complexQuadFormD M v := by
  unfold complexQuadFormD
  simp only [Matrix.mulVec_add, Matrix.mulVec_sub, dotCD_add_left, dotCD_add_right,
    dotCD_sub_left, dotCD_sub_right, Complex.add_re, Complex.sub_re]
  ring

/-- Alias `complexQuadForm3` for `complexQuadForm` on `3 × 3` complex matrices. -/
abbrev complexQuadForm3 := complexQuadForm

private lemma vec3_two {α : Type*} (a b c : α) : (![a, b, c] : Fin 3 → α) 2 = c := rfl

/-- Evaluating `complexQuadFormD M` on a coordinate 3D subspace `embed3D (e_{i₀}) (e_{i₁}) (e_{i₂})`
coincides with the `3 × 3` principal submatrix quadratic form `complexQuadForm3 (submatrix3D M ![i₀, i₁, i₂])`. -/
theorem complexQuadFormD_embed3D_single_eq_submatrix3D {d : ℕ}
    (M : Matrix (Fin d) (Fin d) ℂ) (i₀ i₁ i₂ : Fin d) (x : Fin 3 → ℂ) :
    complexQuadFormD M (embed3D (Pi.single i₀ 1) (Pi.single i₁ 1) (Pi.single i₂ 1) x) =
      complexQuadForm3 (submatrix3D M ![i₀, i₁, i₂]) x := by
  unfold complexQuadFormD complexQuadForm3 complexQuadForm embed3D
  congr 1
  simp only [Matrix.mulVec_add, Matrix.mulVec_smul, dotCD_add_left, dotCD_add_right,
    dotCD_smul_left, dotCD_smul_right, dotCD_single_mulVec_single,
    GleasonComplex.dotC, Matrix.mulVec, dotProduct, Fin.sum_univ_three, submatrix3D,
    Matrix.cons_val_zero, Matrix.cons_val_one, vec3_two]
  ring

/-- On any three pairwise distinct coordinate axes `(i₀, i₁, i₂)`, restricting the `d`-dimensional
Rayleigh quotient `complexRayleighD M` via `embed3D` equals the `3 × 3` principal submatrix
Rayleigh quotient `complexRayleigh (submatrix3D M ![i₀, i₁, i₂])`. -/
theorem complexRayleighD_embed3D_single_eq_submatrix3D {d : ℕ}
    (M : Matrix (Fin d) (Fin d) ℂ) {i₀ i₁ i₂ : Fin d}
    (h01 : i₀ ≠ i₁) (h02 : i₀ ≠ i₂) (h12 : i₁ ≠ i₂) (x : Fin 3 → ℂ) :
    complexRayleighD M (embed3D (Pi.single i₀ 1) (Pi.single i₁ 1) (Pi.single i₂ 1) x) =
      complexRayleigh (submatrix3D M ![i₀, i₁, i₂]) x := by
  unfold complexRayleighD complexRayleigh
  rw [complexQuadFormD_embed3D_single_eq_submatrix3D,
    nsqD_embed3D (isOrthonormalTripleD_single h01 h02 h12)]

/-- `3 × 3` compressed matrix of `M : Matrix (Fin d) (Fin d) ℂ` on the 3-tuple `(e₁, e₂, e₃)`. -/
def subspaceMatrix3D {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ)
    (e₁ e₂ e₃ : Fin d → ℂ) : Matrix (Fin 3) (Fin 3) ℂ :=
  fun a b => dotCD (![e₁, e₂, e₃] a) (M *ᵥ (![e₁, e₂, e₃] b))

/-- If `M` is Hermitian on `ℂ^d`, its `3 × 3` compression `subspaceMatrix3D M e₁ e₂ e₃` onto any
triple `(e₁, e₂, e₃)` is Hermitian. -/
theorem subspaceMatrix3D_isHermitian {d : ℕ} {M : Matrix (Fin d) (Fin d) ℂ}
    (hM : M.IsHermitian) (e₁ e₂ e₃ : Fin d → ℂ) :
    (subspaceMatrix3D M e₁ e₂ e₃).IsHermitian := by
  refine Matrix.IsHermitian.ext fun a b => ?_
  simp only [subspaceMatrix3D, Complex.star_def]
  rw [dotCD_conj_symm, dotCD_mulVec_left, hM.eq]

/-- On standard coordinate basis vectors `(Pi.single i₀ 1, Pi.single i₁ 1, Pi.single i₂ 1)`,
`subspaceMatrix3D M` coincides with the principal `3 × 3` submatrix `submatrix3D M ![i₀, i₁, i₂]`. -/
theorem subspaceMatrix3D_single_eq_submatrix3D {d : ℕ}
    (M : Matrix (Fin d) (Fin d) ℂ) (i₀ i₁ i₂ : Fin d) :
    subspaceMatrix3D M (Pi.single i₀ 1) (Pi.single i₁ 1) (Pi.single i₂ 1) =
      submatrix3D M ![i₀, i₁, i₂] := by
  have hv : ∀ a : Fin 3,
      (![Pi.single i₀ (1 : ℂ), Pi.single i₁ 1, Pi.single i₂ 1] : Fin 3 → Fin d → ℂ) a =
        Pi.single ((![i₀, i₁, i₂] : Fin 3 → Fin d) a) (1 : ℂ) := by
    intro a; fin_cases a <;> rfl
  ext a b
  simp only [subspaceMatrix3D, submatrix3D, hv, dotCD_single_mulVec_single]

lemma dotCD_embed3D_mulVec_embed3D {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ)
    (e₁ e₂ e₃ : Fin d → ℂ) (x : Fin 3 → ℂ) :
    dotCD (embed3D e₁ e₂ e₃ x) (M *ᵥ embed3D e₁ e₂ e₃ x) =
      GleasonComplex.dotC x (subspaceMatrix3D M e₁ e₂ e₃ *ᵥ x) := by
  simp only [embed3D, subspaceMatrix3D, Matrix.mulVec_add, Matrix.mulVec_smul,
    dotCD_add_left, dotCD_add_right, dotCD_smul_left, dotCD_smul_right,
    GleasonComplex.dotC, Matrix.mulVec, dotProduct, Fin.sum_univ_three,
    Matrix.cons_val_zero, Matrix.cons_val_one, vec3_two]
  ring

/-- Evaluating `complexQuadFormD M` along `embed3D e₁ e₂ e₃` equals the `3 × 3` quadratic form
of `subspaceMatrix3D M e₁ e₂ e₃`. -/
theorem complexQuadFormD_embed3D_eq_subspaceMatrix3D {d : ℕ}
    (M : Matrix (Fin d) (Fin d) ℂ) (e₁ e₂ e₃ : Fin d → ℂ) (x : Fin 3 → ℂ) :
    complexQuadFormD M (embed3D e₁ e₂ e₃ x) =
      complexQuadForm3 (subspaceMatrix3D M e₁ e₂ e₃) x := by
  unfold complexQuadFormD complexQuadForm3 complexQuadForm
  rw [dotCD_embed3D_mulVec_embed3D]

/-- For any orthonormal triple `(e₁, e₂, e₃)` in `ℂ^d`, restricting `complexRayleighD M` via
`embed3D e₁ e₂ e₃` equals the `3 × 3` Rayleigh quotient `complexRayleigh (subspaceMatrix3D M e₁ e₂ e₃)`. -/
theorem complexRayleighD_embed3D_eq_subspaceMatrix3D {d : ℕ}
    (M : Matrix (Fin d) (Fin d) ℂ) {e₁ e₂ e₃ : Fin d → ℂ}
    (h : IsOrthonormalTripleD e₁ e₂ e₃) (x : Fin 3 → ℂ) :
    complexRayleighD M (embed3D e₁ e₂ e₃ x) =
      complexRayleigh (subspaceMatrix3D M e₁ e₂ e₃) x := by
  unfold complexRayleighD complexRayleigh
  rw [complexQuadFormD_embed3D_eq_subspaceMatrix3D, nsqD_embed3D h]

private lemma orthonormalC_outer_sum {p q r : Fin 3 → ℂ}
    (h : GleasonComplex.IsOrthonormalC p q r) (i j : Fin 3) :
    p i * conj (p j) + q i * conj (q j) + r i * conj (r j) =
      if i = j then 1 else 0 := by
  let U : Matrix (Fin 3) (Fin 3) ℂ := Matrix.of fun a l => (![p, q, r] l) a
  have h1 : Matrix.conjTranspose U * U = 1 := by
    have hpp := h.pp; have hqq := h.qq; have hrr := h.rr
    have hpq := h.pq; have hpr := h.pr; have hqr := h.qr
    have hqp : GleasonComplex.dotC q p = 0 := by rw [GleasonComplex.dotC_conj_symm, hpq, map_zero]
    have hrp : GleasonComplex.dotC r p = 0 := by rw [GleasonComplex.dotC_conj_symm, hpr, map_zero]
    have hrq : GleasonComplex.dotC r q = 0 := by rw [GleasonComplex.dotC_conj_symm, hqr, map_zero]
    simp only [GleasonComplex.dotC] at hpp hqq hrr hpq hpr hqr hqp hrp hrq
    ext a b
    fin_cases a <;> fin_cases b <;>
      simp [U, Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_three] <;>
      first
      | exact hpp | exact hqq | exact hrr | exact hpq | exact hpr | exact hqr
      | exact hqp | exact hrp | exact hrq
  have h2 : U * Matrix.conjTranspose U = 1 := mul_eq_one_comm.1 h1
  have := congrFun (congrFun h2 i) j
  simpa [U, Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_three,
    Matrix.one_apply] using this

private lemma dotC_mulVec_sum_of_isOrthonormalC {p q r : Fin 3 → ℂ}
    (h : GleasonComplex.IsOrthonormalC p q r) (N : Matrix (Fin 3) (Fin 3) ℂ) :
    GleasonComplex.dotC p (N *ᵥ p) + GleasonComplex.dotC q (N *ᵥ q) +
      GleasonComplex.dotC r (N *ᵥ r) = N 0 0 + N 1 1 + N 2 2 := by
  have k00 := orthonormalC_outer_sum h 0 0
  have k01 := orthonormalC_outer_sum h 0 1
  have k02 := orthonormalC_outer_sum h 0 2
  have k10 := orthonormalC_outer_sum h 1 0
  have k11 := orthonormalC_outer_sum h 1 1
  have k12 := orthonormalC_outer_sum h 1 2
  have k20 := orthonormalC_outer_sum h 2 0
  have k21 := orthonormalC_outer_sum h 2 1
  have k22 := orthonormalC_outer_sum h 2 2
  simp at k00 k01 k02 k10 k11 k12 k20 k21 k22
  simp only [GleasonComplex.dotC, Matrix.mulVec, dotProduct, Fin.sum_univ_three]
  linear_combination
    N 0 0 * k00 + N 0 1 * k10 + N 0 2 * k20 +
    N 1 0 * k01 + N 1 1 * k11 + N 1 2 * k21 +
    N 2 0 * k02 + N 2 1 * k12 + N 2 2 * k22

/-- For every Hermitian `d × d` matrix `M`, its Rayleigh quotient `complexRayleighD M` satisfies
3-frame additivity on every 3D subspace of `ℂ^d`. -/
theorem hasSubspace3FrameAdditivityD_complexRayleighD {d : ℕ}
    {M : Matrix (Fin d) (Fin d) ℂ} (_hM : M.IsHermitian) :
    HasSubspace3FrameAdditivityD (complexRayleighD M) where
  scale v hv c hc := complexRayleighD_smul M hv hc
  subspace_frame {e₁ e₂ e₃} h x y z hx hy hz hxy hxz hyz := by
    obtain ⟨cx, hcx0, hcx1⟩ := GleasonComplex.exists_unit_smulC hx
    obtain ⟨cy, hcy0, hcy1⟩ := GleasonComplex.exists_unit_smulC hy
    obtain ⟨cz, hcz0, hcz1⟩ := GleasonComplex.exists_unit_smulC hz
    set p := cx • x
    set q := cy • y
    set r := cz • z
    have hp1 : GleasonComplex.nsq p = 1 := hcx1
    have hq1 : GleasonComplex.nsq q = 1 := hcy1
    have hr1 : GleasonComplex.nsq r = 1 := hcz1
    have hpqr : GleasonComplex.IsOrthonormalC p q r := by
      refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
      · rw [GleasonComplex.dotC_self_eq_nsq, hp1]; simp
      · rw [GleasonComplex.dotC_self_eq_nsq, hq1]; simp
      · rw [GleasonComplex.dotC_self_eq_nsq, hr1]; simp
      · simp [p, q, GleasonComplex.dotC_smul_left, GleasonComplex.dotC_smul_right, hxy]
      · simp [p, r, GleasonComplex.dotC_smul_left, GleasonComplex.dotC_smul_right, hxz]
      · simp [q, r, GleasonComplex.dotC_smul_left, GleasonComplex.dotC_smul_right, hyz]
    have htr := dotC_mulVec_sum_of_isOrthonormalC hpqr (subspaceMatrix3D M e₁ e₂ e₃)
    have hre := congrArg Complex.re htr
    simp only [Complex.add_re, ← dotCD_embed3D_mulVec_embed3D] at hre
    have hp_ray : complexRayleighD M (embed3D e₁ e₂ e₃ x) =
        (dotCD (embed3D e₁ e₂ e₃ p) (M *ᵥ embed3D e₁ e₂ e₃ p)).re := by
      have hsc : complexRayleighD M (embed3D e₁ e₂ e₃ p) = complexRayleighD M (embed3D e₁ e₂ e₃ x) := by
        rw [show p = cx • x from rfl, embed3D_smul,
          complexRayleighD_smul M ((embed3D_ne_zero_iff h x).mpr hx) hcx0]
      rw [← hsc, complexRayleighD, nsqD_embed3D h, hp1, div_one]; rfl
    have hq_ray : complexRayleighD M (embed3D e₁ e₂ e₃ y) =
        (dotCD (embed3D e₁ e₂ e₃ q) (M *ᵥ embed3D e₁ e₂ e₃ q)).re := by
      have hsc : complexRayleighD M (embed3D e₁ e₂ e₃ q) = complexRayleighD M (embed3D e₁ e₂ e₃ y) := by
        rw [show q = cy • y from rfl, embed3D_smul,
          complexRayleighD_smul M ((embed3D_ne_zero_iff h y).mpr hy) hcy0]
      rw [← hsc, complexRayleighD, nsqD_embed3D h, hq1, div_one]; rfl
    have hr_ray : complexRayleighD M (embed3D e₁ e₂ e₃ z) =
        (dotCD (embed3D e₁ e₂ e₃ r) (M *ᵥ embed3D e₁ e₂ e₃ r)).re := by
      have hsc : complexRayleighD M (embed3D e₁ e₂ e₃ r) = complexRayleighD M (embed3D e₁ e₂ e₃ z) := by
        rw [show r = cz • z from rfl, embed3D_smul,
          complexRayleighD_smul M ((embed3D_ne_zero_iff h z).mpr hz) hcz0]
      rw [← hsc, complexRayleighD, nsqD_embed3D h, hr1, div_one]; rfl
    have he1_ray : complexRayleighD M e₁ = (subspaceMatrix3D M e₁ e₂ e₃ 0 0).re := by
      rw [complexRayleighD, h.1, div_one]; rfl
    have he2_ray : complexRayleighD M e₂ = (subspaceMatrix3D M e₁ e₂ e₃ 1 1).re := by
      rw [complexRayleighD, h.2.1, div_one]; rfl
    have he3_ray : complexRayleighD M e₃ = (subspaceMatrix3D M e₁ e₂ e₃ 2 2).re := by
      rw [complexRayleighD, h.2.2.1, div_one]; rfl
    rw [hp_ray, hq_ray, hr_ray, he1_ray, he2_ray, he3_ray, hre]

/-- Uniqueness of `d × d` Hermitian matrices from their Rayleigh quotients `complexRayleighD` on
all nonzero vectors `v ∈ ℂ^d \ {0}`. -/
theorem eq_of_complexRayleighD_eq {d : ℕ} {A B : Matrix (Fin d) (Fin d) ℂ}
    (hA : A.IsHermitian) (hB : B.IsHermitian)
    (h : ∀ v : Fin d → ℂ, v ≠ 0 → complexRayleighD A v = complexRayleighD B v) :
    A = B := by
  refine eq_of_complexQuadFormD_eq hA hB fun v => ?_
  by_cases hv : v = 0
  · subst hv
    simp [complexQuadFormD, dotCD]
  · have hn : nsqD v ≠ 0 := ((nsqD_pos_iff_ne_zero v).mpr hv).ne'
    exact (div_left_inj' hn).mp (h v hv)

/-- Parseval outer-product completeness for any `d`-dimensional orthonormal basis `B`:
`∑ i : Fin d, conj (B i r) * B i s = δ_{r, s}`. -/
theorem sum_conj_mul_of_isOrthonormalBasisD {d : ℕ} {B : Fin d → Fin d → ℂ}
    (hB : IsOrthonormalBasisD B) (r s : Fin d) :
    (∑ i : Fin d, conj (B i r) * B i s) = if r = s then 1 else 0 := by
  let U : Matrix (Fin d) (Fin d) ℂ := Matrix.of fun i r => B i r
  have h1 : U * Uᴴ = 1 := by
    ext i j
    simp only [U, Matrix.mul_apply, Matrix.of_apply, Matrix.conjTranspose_apply,
      Matrix.one_apply, Complex.star_def]
    have hdot : (∑ k : Fin d, B i k * conj (B j k)) = dotCD (B j) (B i) :=
      Finset.sum_congr rfl fun k _ => mul_comm _ _
    rw [hdot]
    split_ifs with hij
    · subst hij; rw [dotCD_self_eq_nsqD, hB.1 i, Complex.ofReal_one]
    · exact hB.2 j i (Ne.symm hij)
  have h2 : Uᴴ * U = 1 := mul_eq_one_comm.mp h1
  have h3 := congrFun (congrFun h2 r) s
  simpa [U, Matrix.mul_apply, Matrix.conjTranspose_apply, Matrix.one_apply, Complex.star_def] using h3

/-- Basis-independent trace identity on `ℂ^d`: for any `M : Matrix (Fin d) (Fin d) ℂ` and any
orthonormal basis `B` of `ℂ^d`, `∑ i : Fin d, ⟨B i, M (B i)⟩ = M.trace`. -/
theorem sum_dotCD_mulVec_of_isOrthonormalBasisD {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ)
    {B : Fin d → Fin d → ℂ} (hB : IsOrthonormalBasisD B) :
    (∑ i : Fin d, dotCD (B i) (M *ᵥ B i)) = M.trace := by
  have hexp : ∀ i : Fin d, dotCD (B i) (M *ᵥ B i) =
      ∑ r : Fin d, ∑ s : Fin d, M r s * (conj (B i r) * B i s) := by
    intro i
    simp only [dotCD, Matrix.mulVec, dotProduct, Finset.mul_sum]
    refine Finset.sum_congr rfl fun r _ => Finset.sum_congr rfl fun s _ => by ring
  simp_rw [hexp]
  rw [Finset.sum_comm]
  have hswap : ∀ r : Fin d,
      (∑ i : Fin d, ∑ s : Fin d, M r s * (conj (B i r) * B i s)) =
      ∑ s : Fin d, M r s * (∑ i : Fin d, conj (B i r) * B i s) := by
    intro r
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun s _ => (Finset.mul_sum _ _ _).symm
  simp_rw [hswap, sum_conj_mul_of_isOrthonormalBasisD hB]
  simp [Matrix.trace, Matrix.diag]

/-- For any `M : Matrix (Fin d) (Fin d) ℂ` and any orthonormal basis `B` of `ℂ^d`, the Rayleigh
quotients `complexRayleighD M (B i)` sum to `(M.trace).re`. -/
theorem sum_complexRayleighD_of_isOrthonormalBasisD {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ)
    {B : Fin d → Fin d → ℂ} (hB : IsOrthonormalBasisD B) :
    (∑ i : Fin d, complexRayleighD M (B i)) = (M.trace).re := by
  have hterm : ∀ i : Fin d, complexRayleighD M (B i) = (dotCD (B i) (M *ᵥ B i)).re := by
    intro i
    rw [complexRayleighD, complexQuadFormD, hB.1 i, div_one]
  simp_rw [hterm, ← Complex.re_sum, sum_dotCD_mulVec_of_isOrthonormalBasisD M hB]

/-- Every `d × d` complex matrix `M` induces a `d`-dimensional frame function `complexRayleighD M`
of weight `(M.trace).re` across all orthonormal bases of `ℂ^d`. -/
theorem isFrameFunctionD_complexRayleighD {d : ℕ} (M : Matrix (Fin d) (Fin d) ℂ) :
    IsFrameFunctionD (complexRayleighD M) (M.trace).re where
  scale _ hv _ hc := complexRayleighD_smul M hv hc
  basis_sum _ hB := sum_complexRayleighD_of_isOrthonormalBasisD M hB

end

end BornFinite.ContinuumDevelopment

#print axioms GleasonReal.triaxial_eigenvalues_nonneg_and_ordered
#print axioms GleasonReal.stdQuad_nonneg_and_le_weight_of_eigenvalues
#print axioms GleasonReal.nonneg_gleason_real_of_extrema
#print axioms GleasonReal.nonneg_gleason_real_of_continuousOn_sphere3
#print axioms GleasonComplex.nonempty_image_sphereC
#print axioms GleasonComplex.bddAbove_image_sphereC_of_nonnegC
#print axioms GleasonComplex.bddBelow_image_sphereC_of_nonnegC
#print axioms GleasonComplex.le_sSup_sphereC_of_nonnegC
#print axioms GleasonComplex.sInf_sphereC_le_of_nonnegC
#print axioms GleasonComplex.sSup_sphereC_bounds_of_nonnegC
#print axioms GleasonComplex.AttainsExtremaC
#print axioms GleasonComplex.attainsExtremaC_of_continuousOn_sphereC
#print axioms GleasonComplex.attainsExtremaC_of_continuousOn
#print axioms GleasonComplex.complex_eigenvalues_nonneg_and_ordered
