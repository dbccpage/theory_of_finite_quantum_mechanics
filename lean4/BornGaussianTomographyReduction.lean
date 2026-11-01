import BornGaussianFrameRays
import Mathlib.Tactic.LinearCombination

/-!
# Nine-Ray Tomography Reconstruction and Residual Reduction on `ℚ(i)³`

AuthorityEffect: None.

This module formalizes the nine-ray Hermitian tomography reconstruction and the signed
and nonnegative residual-reduction equivalences for rational-valued frame functions on
`ℚ(i)³` (from `dag/derivations/independent/fq-gleason-qi3-rigidity-reduction.md`),
together with the `(1+i)`-adic norm-parity structure of `ℚ(i)³` rays.

## Main Definitions and Results

* `HermForm3`: 9-parameter rational representation of a `3 × 3` Hermitian matrix `ρ` over `ℚ(i)`,
  with diagonal entries `d1, d2, d3 : ℚ` and off-diagonal entries `a_rs + i b_rs` (`r < s`).
* `HermForm3.applyVec`, `inner_applyVec_im_zero`, `inner_applyVec_re_eq_quadNum`: the matrix action
  `ρ v` on `v ∈ ℚ(i)³` has purely rational inner product `⟨v, ρ v⟩ = quadNum ρ v`.
* `quadRay ρ v`: the normalized Rayleigh quotient `⟨v, ρ v⟩ / ⟨v, v⟩`.
* `quadRay_smul`: scale invariance `quadRay ρ (l • v) = quadRay ρ v` for `l ≠ 0`.
* `quadRay_frame_sum`: for any orthogonal triple `(u, v, w)` of nonzero vectors in `ℚ(i)³`
  (without assuming unit-norm representatives),
  `quadRay ρ u + quadRay ρ v + quadRay ρ w = ρ.tr`.
* `quadRay_isFrameFunction`: if `ρ.tr = 1`, then `quadRay ρ` is a frame function on `ℚ(i)³`.
* `tomographyForm f`: the unique `3 × 3` Hermitian form reconstructed from the values of `f` on
  the nine tomography vectors `e_r` (`1 ≤ r ≤ 3`), `e_r + e_s`, and `e_r + i e_s` (`1 ≤ r < s ≤ 3`).
* `tomography_matches_nine_rays`, `tomography_trace_one`, `tomography_unique`: exact reproduction
  of `f` on all nine tomography rays, trace-one normalization when `f` is a frame function, and
  uniqueness of `ρ` from its Rayleigh quotients on the nine rays.
* `signed_rigidity_iff_zero_residual`: every frame function `f : GVec → ℚ` equals `quadRay ρ` for
  a trace-one Hermitian form `ρ` on all nonzero vectors if and only if every zero-weight frame
  function `g` vanishing on the nine tomography rays vanishes on all nonzero vectors.
* `nonneg_rigidity_iff_bounded_zero_residual`: every nonnegative frame function `f` equals
  `quadRay ρ` for a trace-one Hermitian form `ρ` on all nonzero vectors if and only if every
  bounded zero-weight frame function `g` vanishing on the nine tomography rays vanishes on all
  nonzero vectors.
* `normSqVec_zero`, `quadNum_zero`, `quadRay_zero`, `normalizeAtZero`, `eq_quadRay_all_of_zero_at_zero`:
  explicit zero-vector behavior and canonical zero-normalized extension eliminating the junk-value
  caveat at `0`.
* `traceInner`, `traceInner_self_nonneg`, `traceInner_self_eq_zero_iff`, `traceInner_ext`,
  `rayProj`, `traceInner_rayProj`, `rayProj_frame_sum`, `rayProj_nine_rays_span_hermForm3`,
  `rayProj_witness_111_decomp`, `quadRay_witness_111_kernel_relation`,
  `s3_witness_111_kernel_separation`: Section 5 operator-space formulation on `HermForm3`,
  nondegenerate rational Frobenius trace pairing `tr(ρ σ)`, rank-1 ray projector map
  `T(v) = v v* / N(v)` satisfying `tr(ρ T(v)) = quadRay ρ v`, exact frame resolution of the
  identity `T(u) + T(v) + T(w) = I₃` on all orthogonal frames, explicit spanning of `HermForm3`
  by the nine tomography ray projectors, and constructive 7-ray projector kernel decomposition and
  separation without basis extension.
* `gaussian_norm_div_four_witness`, `gaussian_norm_eight_primitive_witness`, and
  `primitive_gaussian_norm_mod_four_iff`: `(1+i)`-primitive vectors in `ℤ[i]³` can have norm
  divisible by `4` or `8`, and `4 ∣ ⟨u, u⟩` on a `(1+i)`-primitive vector iff two coordinates are
  `(1+i)`-odd and one coordinate has `(1+i)`-valuation `1`.
* `v3Rat`, `u3Rat`, `v3Rat_normSq_even`, `detGVec_normSq_of_frame`, `frame_v3Rat_sum_even`,
  `ortho_coord_identity_x`: `3`-adic valuation parity on `ℚ(i)³` rays and orthogonal frames.
* `s3`, `s3_orthogonal_odd_cancel`, `s3_isZeroWeightFrameFunction`, `s3_smul`, `s3_isBoundedOnRays`,
  `s3_vanishes_on_nine_rays`, `witness_111_primitive`, `witness_div_four_shell_primitive`,
  `witness_div_eight_shell_primitive`, `exists_nonzero_bounded_zero_residual`: explicit global
  bounded (`{-1, 0, +1}`-valued) zero-weight residual frame function on `ℚ(i)³` vanishing on all
  nine tomography rays and nonzero across `(1+i)`-primitive rays in distinct `(1+i)`-adic norm
  shells (`witness_111` of norm `3`, `witness_div_four_shell` of norm `12`, and
  `witness_div_eight_shell` of norm `24`).
* `not_signed_quadratic_rigidity`, `not_nonneg_quadratic_rigidity`, `exoticQi3`,
  `exoticQi3_isNonnegFrameFunction`, `exoticQi3_not_quadratic`: negative resolution of both signed
  and nonnegative quadratic frame-function rigidity on `ℚ(i)³`, with `exoticQi3 v = (1 + s3 v) / 3`
  providing an explicit global `{0, 1/3, 2/3}`-valued nonnegative non-quadratic frame function.
* `IsArchimedeanContinuousAt`, `s3_oscillates_near_tomo_e1`, `not_archimedeanContinuousAt_s3_tomo_e1`,
  `not_archimedeanContinuousAt_exoticQi3_tomo_e1`, `s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1`,
  `archimedeanContinuousAt_quadRay_tomo_e1`,
  `quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff`: Section 9A Archimedean continuity
  elimination at `tomo_e1`, proving both that `s3` and `exoticQi3` oscillate discontinuously on rays
  approaching `tomo_e1` and that `quadRay ρ` is Archimedean-continuous at `tomo_e1`, so
  `quadRay ρ + c • s3` is Archimedean-continuous at `tomo_e1` iff `c = 0`.
* `no_unit_norm_smul_witness_111_in_qi3`, `GaussRatSqrt3`, `GVecSqrt3`, `witness_111_unit_sqrt3_normSq`,
  `isFrameSqrt3_witness_111_even_norms`, `zero_on_witness_111_of_sqrt3_even_v3_vanishing`,
  `no_s3_even_v3_extension_to_sqrt3`, `unit_norm_in_sqrtP_of_normSqVec_eq`,
  `fourSquarePartner_ortho_and_normSqRatP`, `isFrameSqrt7_witness_p7_norms`: Section 9B quadratic
  field extension `ℚ(i, √p)³` elimination via universal unit-norm rescaling (`(1/√p) u` has norm `1`)
  and universal four-square SU(2) orthogonal partner completion (shifting partner norms from `m p`
  to `m p²` with even `v_p = 2`), instantiated explicitly for `p = 3` (`(3, 18, 18)`) and `p = 7`
  (`(7, 245, 245)`).
* `FactorsThroughRayProjLinear`, `zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear`,
  `not_factorsThroughRayProjLinear_s3`, `quadratic_rigidity_iff_factorsThroughRayProjLinear`:
  Section 9C operator-space projector-linearity (`T(v) = rayProj v`) characterization of quadratic
  rigidity over `ℚ(i)³`.
-/

namespace BornFinite.GaussianTomography

open BornFinite
open BornFinite.GaussRat
open BornFinite.GaussianFrames

/-! ### 1. Hermitian Forms and Rayleigh Quotients on `ℚ(i)³` -/

/-- A `3 × 3` Hermitian matrix over `ℚ(i)` parameterized by its three rational diagonal entries
`d1, d2, d3` and three Gaussian-rational upper-triangular entries `a12 + i b12`, `a13 + i b13`,
`a23 + i b23`. -/
structure HermForm3 where
  d1 : ℚ
  d2 : ℚ
  d3 : ℚ
  a12 : ℚ
  a13 : ℚ
  a23 : ℚ
  b12 : ℚ
  b13 : ℚ
  b23 : ℚ
  deriving DecidableEq, Repr

@[ext]
theorem HermForm3.ext {ρ σ : HermForm3}
    (hd1 : ρ.d1 = σ.d1) (hd2 : ρ.d2 = σ.d2) (hd3 : ρ.d3 = σ.d3)
    (ha12 : ρ.a12 = σ.a12) (ha13 : ρ.a13 = σ.a13) (ha23 : ρ.a23 = σ.a23)
    (hb12 : ρ.b12 = σ.b12) (hb13 : ρ.b13 = σ.b13) (hb23 : ρ.b23 = σ.b23) :
    ρ = σ := by
  cases ρ; cases σ; simp_all

/-- Trace of the `3 × 3` Hermitian matrix `ρ`. -/
def HermForm3.tr (ρ : HermForm3) : ℚ :=
  ρ.d1 + ρ.d2 + ρ.d3

/-- Absolute-value coefficient norm bounding `|quadRay ρ v|` on all nonzero rays. -/
def HermForm3.coeffNorm (ρ : HermForm3) : ℚ :=
  |ρ.d1| + |ρ.d2| + |ρ.d3| +
  2 * |ρ.a12| + 2 * |ρ.a13| + 2 * |ρ.a23| +
  2 * |ρ.b12| + 2 * |ρ.b13| + 2 * |ρ.b23|

/-- Upper-triangular Gaussian-rational entries of `ρ`. -/
def HermForm3.entry12 (ρ : HermForm3) : GaussRat := ⟨ρ.a12, ρ.b12⟩
def HermForm3.entry13 (ρ : HermForm3) : GaussRat := ⟨ρ.a13, ρ.b13⟩
def HermForm3.entry23 (ρ : HermForm3) : GaussRat := ⟨ρ.a23, ρ.b23⟩

/-- Linear action `v ↦ ρ v` of the `3 × 3` Hermitian matrix `ρ` on `v ∈ ℚ(i)³`. -/
def HermForm3.applyVec (ρ : HermForm3) (v : GVec) : GVec :=
  ⟨⟨ρ.d1, 0⟩ * v.x + ρ.entry12 * v.y + ρ.entry13 * v.z,
   star ρ.entry12 * v.x + ⟨ρ.d2, 0⟩ * v.y + ρ.entry23 * v.z,
   star ρ.entry13 * v.x + star ρ.entry23 * v.y + ⟨ρ.d3, 0⟩ * v.z⟩

/-- Unnormalized Hermitian quadratic form `⟨v, ρ v⟩` evaluated on `v ∈ ℚ(i)³`. -/
def quadNum (ρ : HermForm3) (v : GVec) : ℚ :=
  ρ.d1 * v.x.normSq + ρ.d2 * v.y.normSq + ρ.d3 * v.z.normSq +
  2 * ρ.a12 * (v.x.re * v.y.re + v.x.im * v.y.im) +
  2 * ρ.a13 * (v.x.re * v.z.re + v.x.im * v.z.im) +
  2 * ρ.a23 * (v.y.re * v.z.re + v.y.im * v.z.im) -
  2 * ρ.b12 * (v.x.re * v.y.im - v.x.im * v.y.re) -
  2 * ρ.b13 * (v.x.re * v.z.im - v.x.im * v.z.re) -
  2 * ρ.b23 * (v.y.re * v.z.im - v.y.im * v.z.re)

/-- Squared Hermitian norm `⟨v, v⟩` of `v ∈ ℚ(i)³`. -/
def normSqVec (v : GVec) : ℚ :=
  v.x.normSq + v.y.normSq + v.z.normSq

/-- Normalized Hermitian Rayleigh quotient `⟨v, ρ v⟩ / ⟨v, v⟩`. -/
def quadRay (ρ : HermForm3) (v : GVec) : ℚ :=
  quadNum ρ v / normSqVec v

/-- The Hermitian inner product `⟨v, ρ v⟩` has zero imaginary part. -/
theorem inner_applyVec_im_zero (ρ : HermForm3) (v : GVec) :
    (GVec.inner v (ρ.applyVec v)).im = 0 := by
  simp only [GVec.inner, HermForm3.applyVec, HermForm3.entry12, HermForm3.entry13,
    HermForm3.entry23, re_add, im_add, re_mul, im_mul, re_star, im_star]
  ring

/-- The real part of `⟨v, ρ v⟩` equals `quadNum ρ v`. -/
theorem inner_applyVec_re_eq_quadNum (ρ : HermForm3) (v : GVec) :
    (GVec.inner v (ρ.applyVec v)).re = quadNum ρ v := by
  simp only [GVec.inner, HermForm3.applyVec, HermForm3.entry12, HermForm3.entry13,
    HermForm3.entry23, quadNum, GaussRat.normSq, re_add, im_add, re_mul, im_mul, re_star, im_star]
  ring

theorem inner_self_eq_normSqVec (v : GVec) :
    GVec.inner v v = ⟨normSqVec v, 0⟩ := by
  ext
  · simp only [GVec.inner, normSqVec, GaussRat.normSq, re_add, re_mul, re_star, im_star]
    ring
  · simp only [GVec.inner, im_add, im_mul, re_star, im_star]
    ring

theorem normSqVec_nonneg (v : GVec) : 0 ≤ normSqVec v := by
  unfold normSqVec
  linarith [normSq_nonneg v.x, normSq_nonneg v.y, normSq_nonneg v.z]

theorem normSqVec_pos_of_nonZero {v : GVec} (hv : v.NonZero) : 0 < normSqVec v := by
  rcases hv with hx | hy | hz
  · have h1 : 0 < v.x.normSq :=
      lt_of_le_of_ne (normSq_nonneg v.x) (fun h => hx ((normSq_eq_zero_iff v.x).mp h.symm))
    unfold normSqVec
    linarith [normSq_nonneg v.y, normSq_nonneg v.z]
  · have h1 : 0 < v.y.normSq :=
      lt_of_le_of_ne (normSq_nonneg v.y) (fun h => hy ((normSq_eq_zero_iff v.y).mp h.symm))
    unfold normSqVec
    linarith [normSq_nonneg v.x, normSq_nonneg v.z]
  · have h1 : 0 < v.z.normSq :=
      lt_of_le_of_ne (normSq_nonneg v.z) (fun h => hz ((normSq_eq_zero_iff v.z).mp h.symm))
    unfold normSqVec
    linarith [normSq_nonneg v.x, normSq_nonneg v.y]

theorem normSqVec_ne_zero_of_nonZero {v : GVec} (hv : v.NonZero) : normSqVec v ≠ 0 :=
  ne_of_gt (normSqVec_pos_of_nonZero hv)

theorem quadNum_smul (ρ : HermForm3) (l : GaussRat) (v : GVec) :
    quadNum ρ (GVec.smul l v) = l.normSq * quadNum ρ v := by
  simp only [quadNum, GVec.smul, GaussRat.normSq, re_mul, im_mul]
  ring

theorem normSqVec_smul (l : GaussRat) (v : GVec) :
    normSqVec (GVec.smul l v) = l.normSq * normSqVec v := by
  simp only [normSqVec, GVec.smul, GaussRat.normSq, re_mul, im_mul]
  ring

/-- The Rayleigh quotient `quadRay ρ` is invariant under nonzero Gaussian-rational scaling. -/
theorem quadRay_smul (ρ : HermForm3) {l : GaussRat} (hl : l ≠ 0) (v : GVec) :
    quadRay ρ (GVec.smul l v) = quadRay ρ v := by
  have hln : l.normSq ≠ 0 := fun h0 => hl ((normSq_eq_zero_iff l).mp h0)
  simp only [quadRay, quadNum_smul, normSqVec_smul]
  exact mul_div_mul_left (quadNum ρ v) (normSqVec v) hln

/-! ### 2. Orthogonal Frame Sum via Gram Adjugate Identity -/

/-- Cyclic coordinate rotation `(x, y, z) ↦ (y, z, x)`. -/
def rotVec (v : GVec) : GVec := ⟨v.y, v.z, v.x⟩

/-- Coordinate swap `(x, y, z) ↦ (y, x, z)`. -/
def swapXYVec (v : GVec) : GVec := ⟨v.y, v.x, v.z⟩

theorem inner_rotVec (u v : GVec) : GVec.inner (rotVec u) (rotVec v) = GVec.inner u v := by
  simp only [GVec.inner, rotVec]
  ring

theorem inner_swapXYVec (u v : GVec) : GVec.inner (swapXYVec u) (swapXYVec v) = GVec.inner u v := by
  simp only [GVec.inner, swapXYVec]
  ring

theorem inner_eq_zero_symm {u v : GVec} (h : GVec.inner u v = 0) : GVec.inner v u = 0 := by
  have hstar : star (GVec.inner u v) = GVec.inner v u := by
    simp only [GVec.inner, star_add, star_mul, star_star]
  rw [← hstar, h, star_zero]

theorem u_adjG_ud_diag (u v w : GVec)
    (huv : GVec.inner u v = 0) (huw : GVec.inner u w = 0) (hvw : GVec.inner v w = 0)
    (hvu : GVec.inner v u = 0) (hwu : GVec.inner w u = 0) (hwv : GVec.inner w v = 0) :
    GVec.inner v v * GVec.inner w w * (u.x * star u.x) +
    GVec.inner u u * GVec.inner w w * (v.x * star v.x) +
    GVec.inner u u * GVec.inner v v * (w.x * star w.x) =
    GVec.inner u u * GVec.inner v v * GVec.inner w w := by
  have id_general :
      (GVec.inner v v * GVec.inner w w - GVec.inner v w * GVec.inner w v) * (u.x * star u.x) +
      (GVec.inner u w * GVec.inner w v - GVec.inner u v * GVec.inner w w) * (u.x * star v.x) +
      (GVec.inner u v * GVec.inner v w - GVec.inner u w * GVec.inner v v) * (u.x * star w.x) +
      (GVec.inner v w * GVec.inner w u - GVec.inner v u * GVec.inner w w) * (v.x * star u.x) +
      (GVec.inner u u * GVec.inner w w - GVec.inner u w * GVec.inner w u) * (v.x * star v.x) +
      (GVec.inner u w * GVec.inner v u - GVec.inner u u * GVec.inner v w) * (v.x * star w.x) +
      (GVec.inner v u * GVec.inner w v - GVec.inner v v * GVec.inner w u) * (w.x * star u.x) +
      (GVec.inner u v * GVec.inner w u - GVec.inner u u * GVec.inner w v) * (w.x * star v.x) +
      (GVec.inner u u * GVec.inner v v - GVec.inner u v * GVec.inner v u) * (w.x * star w.x) =
      GVec.inner u u * (GVec.inner v v * GVec.inner w w - GVec.inner v w * GVec.inner w v) -
      GVec.inner u v * (GVec.inner v u * GVec.inner w w - GVec.inner v w * GVec.inner w u) +
      GVec.inner u w * (GVec.inner v u * GVec.inner w v - GVec.inner v v * GVec.inner w u) := by
    simp only [GVec.inner]
    ring
  rw [huv, huw, hvw, hvu, hwu, hwv] at id_general
  linear_combination id_general

theorem u_adjG_ud_offdiag (u v w : GVec)
    (huv : GVec.inner u v = 0) (huw : GVec.inner u w = 0) (hvw : GVec.inner v w = 0)
    (hvu : GVec.inner v u = 0) (hwu : GVec.inner w u = 0) (hwv : GVec.inner w v = 0) :
    GVec.inner v v * GVec.inner w w * (u.x * star u.y) +
    GVec.inner u u * GVec.inner w w * (v.x * star v.y) +
    GVec.inner u u * GVec.inner v v * (w.x * star w.y) = 0 := by
  have id_general :
      (GVec.inner v v * GVec.inner w w - GVec.inner v w * GVec.inner w v) * (u.x * star u.y) +
      (GVec.inner u w * GVec.inner w v - GVec.inner u v * GVec.inner w w) * (u.x * star v.y) +
      (GVec.inner u v * GVec.inner v w - GVec.inner u w * GVec.inner v v) * (u.x * star w.y) +
      (GVec.inner v w * GVec.inner w u - GVec.inner v u * GVec.inner w w) * (v.x * star u.y) +
      (GVec.inner u u * GVec.inner w w - GVec.inner u w * GVec.inner w u) * (v.x * star v.y) +
      (GVec.inner u w * GVec.inner v u - GVec.inner u u * GVec.inner v w) * (v.x * star w.y) +
      (GVec.inner v u * GVec.inner w v - GVec.inner v v * GVec.inner w u) * (w.x * star u.y) +
      (GVec.inner u v * GVec.inner w u - GVec.inner u u * GVec.inner w v) * (w.x * star v.y) +
      (GVec.inner u u * GVec.inner v v - GVec.inner u v * GVec.inner v u) * (w.x * star w.y) = 0 := by
    simp only [GVec.inner]
    ring
  rw [huv, huw, hvw, hvu, hwu, hwv] at id_general
  linear_combination id_general

theorem inner_applyVec_orthogonal_weighted_sum (ρ : HermForm3) {u v w : GVec}
    (huv : GVec.inner u v = 0) (huw : GVec.inner u w = 0) (hvw : GVec.inner v w = 0) :
    GVec.inner v v * GVec.inner w w * GVec.inner u (ρ.applyVec u) +
    GVec.inner u u * GVec.inner w w * GVec.inner v (ρ.applyVec v) +
    GVec.inner u u * GVec.inner v v * GVec.inner w (ρ.applyVec w) =
    GVec.inner u u * GVec.inner v v * GVec.inner w w *
      (⟨ρ.d1, 0⟩ + ⟨ρ.d2, 0⟩ + ⟨ρ.d3, 0⟩) := by
  have hvu := inner_eq_zero_symm huv
  have hwu := inner_eq_zero_symm huw
  have hwv := inner_eq_zero_symm hvw
  have hxx := u_adjG_ud_diag u v w huv huw hvw hvu hwu hwv
  have hyy := u_adjG_ud_diag (rotVec u) (rotVec v) (rotVec w)
    (by rw [inner_rotVec]; exact huv) (by rw [inner_rotVec]; exact huw)
    (by rw [inner_rotVec]; exact hvw) (by rw [inner_rotVec]; exact hvu)
    (by rw [inner_rotVec]; exact hwu) (by rw [inner_rotVec]; exact hwv)
  have hzz := u_adjG_ud_diag (rotVec (rotVec u)) (rotVec (rotVec v)) (rotVec (rotVec w))
    (by rw [inner_rotVec, inner_rotVec]; exact huv) (by rw [inner_rotVec, inner_rotVec]; exact huw)
    (by rw [inner_rotVec, inner_rotVec]; exact hvw) (by rw [inner_rotVec, inner_rotVec]; exact hvu)
    (by rw [inner_rotVec, inner_rotVec]; exact hwu) (by rw [inner_rotVec, inner_rotVec]; exact hwv)
  have hxy := u_adjG_ud_offdiag u v w huv huw hvw hvu hwu hwv
  have hyx := u_adjG_ud_offdiag (swapXYVec u) (swapXYVec v) (swapXYVec w)
    (by rw [inner_swapXYVec]; exact huv) (by rw [inner_swapXYVec]; exact huw)
    (by rw [inner_swapXYVec]; exact hvw) (by rw [inner_swapXYVec]; exact hvu)
    (by rw [inner_swapXYVec]; exact hwu) (by rw [inner_swapXYVec]; exact hwv)
  have hyz := u_adjG_ud_offdiag (rotVec u) (rotVec v) (rotVec w)
    (by rw [inner_rotVec]; exact huv) (by rw [inner_rotVec]; exact huw)
    (by rw [inner_rotVec]; exact hvw) (by rw [inner_rotVec]; exact hvu)
    (by rw [inner_rotVec]; exact hwu) (by rw [inner_rotVec]; exact hwv)
  have hzy := u_adjG_ud_offdiag (swapXYVec (rotVec u)) (swapXYVec (rotVec v)) (swapXYVec (rotVec w))
    (by rw [inner_swapXYVec, inner_rotVec]; exact huv)
    (by rw [inner_swapXYVec, inner_rotVec]; exact huw)
    (by rw [inner_swapXYVec, inner_rotVec]; exact hvw)
    (by rw [inner_swapXYVec, inner_rotVec]; exact hvu)
    (by rw [inner_swapXYVec, inner_rotVec]; exact hwu)
    (by rw [inner_swapXYVec, inner_rotVec]; exact hwv)
  have hzx := u_adjG_ud_offdiag (rotVec (rotVec u)) (rotVec (rotVec v)) (rotVec (rotVec w))
    (by rw [inner_rotVec, inner_rotVec]; exact huv) (by rw [inner_rotVec, inner_rotVec]; exact huw)
    (by rw [inner_rotVec, inner_rotVec]; exact hvw) (by rw [inner_rotVec, inner_rotVec]; exact hvu)
    (by rw [inner_rotVec, inner_rotVec]; exact hwu) (by rw [inner_rotVec, inner_rotVec]; exact hwv)
  have hxz := u_adjG_ud_offdiag (swapXYVec (rotVec (rotVec u)))
    (swapXYVec (rotVec (rotVec v))) (swapXYVec (rotVec (rotVec w)))
    (by rw [inner_swapXYVec, inner_rotVec, inner_rotVec]; exact huv)
    (by rw [inner_swapXYVec, inner_rotVec, inner_rotVec]; exact huw)
    (by rw [inner_swapXYVec, inner_rotVec, inner_rotVec]; exact hvw)
    (by rw [inner_swapXYVec, inner_rotVec, inner_rotVec]; exact hvu)
    (by rw [inner_swapXYVec, inner_rotVec, inner_rotVec]; exact hwu)
    (by rw [inner_swapXYVec, inner_rotVec, inner_rotVec]; exact hwv)
  simp only [inner_rotVec, inner_swapXYVec] at hyy hzz hyx hyz hzy hzx hxz
  simp only [rotVec, swapXYVec] at hyy hzz hyx hyz hzy hzx hxz
  have hexp (q : GVec) :
      GVec.inner q (ρ.applyVec q) =
      ⟨ρ.d1, 0⟩ * (q.x * star q.x) + ⟨ρ.d2, 0⟩ * (q.y * star q.y) + ⟨ρ.d3, 0⟩ * (q.z * star q.z) +
      ρ.entry12 * (q.y * star q.x) + star ρ.entry12 * (q.x * star q.y) +
      ρ.entry13 * (q.z * star q.x) + star ρ.entry13 * (q.x * star q.z) +
      ρ.entry23 * (q.z * star q.y) + star ρ.entry23 * (q.y * star q.z) := by
    simp only [GVec.inner, HermForm3.applyVec]
    ring
  rw [hexp u, hexp v, hexp w]
  linear_combination
    ⟨ρ.d1, 0⟩ * hxx + ⟨ρ.d2, 0⟩ * hyy + ⟨ρ.d3, 0⟩ * hzz +
    ρ.entry12 * hyx + star ρ.entry12 * hxy +
    ρ.entry13 * hzx + star ρ.entry13 * hxz +
    ρ.entry23 * hzy + star ρ.entry23 * hyz

/-- Rational Gram-adjugate identity for orthogonal triples in `ℚ(i)³`. -/
theorem quadNum_orthogonal_weighted_sum (ρ : HermForm3) {u v w : GVec}
    (huv : GVec.inner u v = 0) (huw : GVec.inner u w = 0) (hvw : GVec.inner v w = 0) :
    normSqVec v * normSqVec w * quadNum ρ u +
    normSqVec u * normSqVec w * quadNum ρ v +
    normSqVec u * normSqVec v * quadNum ρ w =
    normSqVec u * normSqVec v * normSqVec w * ρ.tr := by
  have h := congrArg GaussRat.re (inner_applyVec_orthogonal_weighted_sum ρ huv huw hvw)
  simp only [inner_self_eq_normSqVec, re_add, im_add, re_mul, im_mul,
    inner_applyVec_re_eq_quadNum, inner_applyVec_im_zero] at h
  unfold HermForm3.tr
  linarith

/-- On every orthogonal frame `(u, v, w)` in `ℚ(i)³` (without assuming unit-norm representatives),
the Rayleigh quotients of `ρ` sum to `tr(ρ)`. -/
theorem quadRay_frame_sum (ρ : HermForm3) {u v w : GVec} (hfr : IsFrame u v w) :
    quadRay ρ u + quadRay ρ v + quadRay ρ w = ρ.tr := by
  rcases hfr with ⟨hu, hv, hw, huv, huw, hvw⟩
  have hnu := normSqVec_ne_zero_of_nonZero hu
  have hnv := normSqVec_ne_zero_of_nonZero hv
  have hnw := normSqVec_ne_zero_of_nonZero hw
  have hsum := quadNum_orthogonal_weighted_sum ρ huv huw hvw
  unfold quadRay
  rw [div_add_div _ _ hnu hnv, div_add_div _ _ (mul_ne_zero hnu hnv) hnw,
    div_eq_iff (mul_ne_zero (mul_ne_zero hnu hnv) hnw)]
  linarith

/-- Every trace-one `3 × 3` Hermitian form `ρ` defines a frame function `quadRay ρ` on `ℚ(i)³`. -/
theorem quadRay_isFrameFunction (ρ : HermForm3) (htr : ρ.tr = 1) :
    IsFrameFunction (quadRay ρ) := by
  intro u v w hfr
  rw [quadRay_frame_sum ρ hfr, htr]

/-! ### 3. Nine-Ray Tomography Reconstruction and Uniqueness -/

/-- The nine tomography vectors `e₁, e₂, e₃, e₁+e₂, e₁+e₃, e₂+e₃, e₁+ie₂, e₁+ie₃, e₂+ie₃`. -/
def tomo_e1 : GVec := gv 1 0 0 0 0 0
def tomo_e2 : GVec := gv 0 0 1 0 0 0
def tomo_e3 : GVec := gv 0 0 0 0 1 0
def tomo_e12 : GVec := gv 1 0 1 0 0 0
def tomo_e13 : GVec := gv 1 0 0 0 1 0
def tomo_e23 : GVec := gv 0 0 1 0 1 0
def tomo_e12i : GVec := gv 1 0 0 1 0 0
def tomo_e13i : GVec := gv 1 0 0 0 0 1
def tomo_e23i : GVec := gv 0 0 1 0 0 1

theorem frame_tomo_std : IsFrame tomo_e1 tomo_e2 tomo_e3 :=
  ⟨nonZero_of_x (by norm_num [tomo_e1, gv]),
   nonZero_of_y (by norm_num [tomo_e2, gv]),
   nonZero_of_z (by norm_num [tomo_e3, gv]),
   by simp only [tomo_e1, tomo_e2]; gauss_arith,
   by simp only [tomo_e1, tomo_e3]; gauss_arith,
   by simp only [tomo_e2, tomo_e3]; gauss_arith⟩

theorem tomo_e1_nonZero : tomo_e1.NonZero := frame_tomo_std.1
theorem tomo_e2_nonZero : tomo_e2.NonZero := frame_tomo_std.2.1
theorem tomo_e3_nonZero : tomo_e3.NonZero := frame_tomo_std.2.2.1
theorem tomo_e12_nonZero : tomo_e12.NonZero := nonZero_of_x (by norm_num [tomo_e12, gv])
theorem tomo_e13_nonZero : tomo_e13.NonZero := nonZero_of_x (by norm_num [tomo_e13, gv])
theorem tomo_e23_nonZero : tomo_e23.NonZero := nonZero_of_y (by norm_num [tomo_e23, gv])
theorem tomo_e12i_nonZero : tomo_e12i.NonZero := nonZero_of_x (by norm_num [tomo_e12i, gv])
theorem tomo_e13i_nonZero : tomo_e13i.NonZero := nonZero_of_x (by norm_num [tomo_e13i, gv])
theorem tomo_e23i_nonZero : tomo_e23i.NonZero := nonZero_of_y (by norm_num [tomo_e23i, gv])

theorem quadRay_tomo_e1 (ρ : HermForm3) : quadRay ρ tomo_e1 = ρ.d1 := by
  simp [quadRay, quadNum, normSqVec, GaussRat.normSq, tomo_e1, gv]

theorem quadRay_tomo_e2 (ρ : HermForm3) : quadRay ρ tomo_e2 = ρ.d2 := by
  simp [quadRay, quadNum, normSqVec, GaussRat.normSq, tomo_e2, gv]

theorem quadRay_tomo_e3 (ρ : HermForm3) : quadRay ρ tomo_e3 = ρ.d3 := by
  simp [quadRay, quadNum, normSqVec, GaussRat.normSq, tomo_e3, gv]

theorem quadRay_tomo_e12 (ρ : HermForm3) : quadRay ρ tomo_e12 = (ρ.d1 + ρ.d2 + 2 * ρ.a12) / 2 := by
  simp [quadRay, quadNum, normSqVec, GaussRat.normSq, tomo_e12, gv]
  ring

theorem quadRay_tomo_e13 (ρ : HermForm3) : quadRay ρ tomo_e13 = (ρ.d1 + ρ.d3 + 2 * ρ.a13) / 2 := by
  simp [quadRay, quadNum, normSqVec, GaussRat.normSq, tomo_e13, gv]
  ring

theorem quadRay_tomo_e23 (ρ : HermForm3) : quadRay ρ tomo_e23 = (ρ.d2 + ρ.d3 + 2 * ρ.a23) / 2 := by
  simp [quadRay, quadNum, normSqVec, GaussRat.normSq, tomo_e23, gv]
  ring

theorem quadRay_tomo_e12i (ρ : HermForm3) : quadRay ρ tomo_e12i = (ρ.d1 + ρ.d2 - 2 * ρ.b12) / 2 := by
  simp [quadRay, quadNum, normSqVec, GaussRat.normSq, tomo_e12i, gv]
  ring

theorem quadRay_tomo_e13i (ρ : HermForm3) : quadRay ρ tomo_e13i = (ρ.d1 + ρ.d3 - 2 * ρ.b13) / 2 := by
  simp [quadRay, quadNum, normSqVec, GaussRat.normSq, tomo_e13i, gv]
  ring

theorem quadRay_tomo_e23i (ρ : HermForm3) : quadRay ρ tomo_e23i = (ρ.d2 + ρ.d3 - 2 * ρ.b23) / 2 := by
  simp [quadRay, quadNum, normSqVec, GaussRat.normSq, tomo_e23i, gv]
  ring

/-- Reconstruct the unique `3 × 3` Hermitian form matching `f` on the nine tomography rays. -/
def tomographyForm (f : GVec → ℚ) : HermForm3 where
  d1 := f tomo_e1
  d2 := f tomo_e2
  d3 := f tomo_e3
  a12 := f tomo_e12 - (f tomo_e1 + f tomo_e2) / 2
  a13 := f tomo_e13 - (f tomo_e1 + f tomo_e3) / 2
  a23 := f tomo_e23 - (f tomo_e2 + f tomo_e3) / 2
  b12 := (f tomo_e1 + f tomo_e2) / 2 - f tomo_e12i
  b13 := (f tomo_e1 + f tomo_e3) / 2 - f tomo_e13i
  b23 := (f tomo_e2 + f tomo_e3) / 2 - f tomo_e23i

/-- `quadRay (tomographyForm f)` reproduces `f` on all nine tomography rays. -/
theorem tomography_matches_nine_rays (f : GVec → ℚ) :
    quadRay (tomographyForm f) tomo_e1 = f tomo_e1 ∧
    quadRay (tomographyForm f) tomo_e2 = f tomo_e2 ∧
    quadRay (tomographyForm f) tomo_e3 = f tomo_e3 ∧
    quadRay (tomographyForm f) tomo_e12 = f tomo_e12 ∧
    quadRay (tomographyForm f) tomo_e13 = f tomo_e13 ∧
    quadRay (tomographyForm f) tomo_e23 = f tomo_e23 ∧
    quadRay (tomographyForm f) tomo_e12i = f tomo_e12i ∧
    quadRay (tomographyForm f) tomo_e13i = f tomo_e13i ∧
    quadRay (tomographyForm f) tomo_e23i = f tomo_e23i := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [quadRay_tomo_e1]; rfl
  · rw [quadRay_tomo_e2]; rfl
  · rw [quadRay_tomo_e3]; rfl
  · rw [quadRay_tomo_e12]; simp only [tomographyForm]; ring
  · rw [quadRay_tomo_e13]; simp only [tomographyForm]; ring
  · rw [quadRay_tomo_e23]; simp only [tomographyForm]; ring
  · rw [quadRay_tomo_e12i]; simp only [tomographyForm]; ring
  · rw [quadRay_tomo_e13i]; simp only [tomographyForm]; ring
  · rw [quadRay_tomo_e23i]; simp only [tomographyForm]; ring

/-- If `f` is a frame function, its tomography form has trace `1`. -/
theorem tomography_trace_one {f : GVec → ℚ} (hf : IsFrameFunction f) :
    (tomographyForm f).tr = 1 := by
  unfold HermForm3.tr tomographyForm
  exact hf tomo_e1 tomo_e2 tomo_e3 frame_tomo_std

/-- If `f` is a frame function, `quadRay (tomographyForm f)` is itself a frame function. -/
theorem tomography_isFrameFunction {f : GVec → ℚ} (hf : IsFrameFunction f) :
    IsFrameFunction (quadRay (tomographyForm f)) :=
  quadRay_isFrameFunction (tomographyForm f) (tomography_trace_one hf)

/-- A `3 × 3` Hermitian form is uniquely determined by its Rayleigh quotients on the nine rays. -/
theorem tomography_unique (ρ σ : HermForm3)
    (he1 : quadRay ρ tomo_e1 = quadRay σ tomo_e1)
    (he2 : quadRay ρ tomo_e2 = quadRay σ tomo_e2)
    (he3 : quadRay ρ tomo_e3 = quadRay σ tomo_e3)
    (he12 : quadRay ρ tomo_e12 = quadRay σ tomo_e12)
    (he13 : quadRay ρ tomo_e13 = quadRay σ tomo_e13)
    (he23 : quadRay ρ tomo_e23 = quadRay σ tomo_e23)
    (he12i : quadRay ρ tomo_e12i = quadRay σ tomo_e12i)
    (he13i : quadRay ρ tomo_e13i = quadRay σ tomo_e13i)
    (he23i : quadRay ρ tomo_e23i = quadRay σ tomo_e23i) :
    ρ = σ := by
  rw [quadRay_tomo_e1, quadRay_tomo_e1] at he1
  rw [quadRay_tomo_e2, quadRay_tomo_e2] at he2
  rw [quadRay_tomo_e3, quadRay_tomo_e3] at he3
  rw [quadRay_tomo_e12, quadRay_tomo_e12] at he12
  rw [quadRay_tomo_e13, quadRay_tomo_e13] at he13
  rw [quadRay_tomo_e23, quadRay_tomo_e23] at he23
  rw [quadRay_tomo_e12i, quadRay_tomo_e12i] at he12i
  rw [quadRay_tomo_e13i, quadRay_tomo_e13i] at he13i
  rw [quadRay_tomo_e23i, quadRay_tomo_e23i] at he23i
  ext <;> linarith

theorem tomographyForm_quadRay (ρ : HermForm3) :
    tomographyForm (quadRay ρ) = ρ := by
  have hm := tomography_matches_nine_rays (quadRay ρ)
  exact tomography_unique (tomographyForm (quadRay ρ)) ρ
    hm.1 hm.2.1 hm.2.2.1 hm.2.2.2.1 hm.2.2.2.2.1 hm.2.2.2.2.2.1
    hm.2.2.2.2.2.2.1 hm.2.2.2.2.2.2.2.1 hm.2.2.2.2.2.2.2.2

/-! ### 4. Zero-Weight Residual and Signed Rigidity Equivalence -/

/-- A zero-weight frame function sums to `0` on every orthogonal frame in `ℚ(i)³`. -/
def IsZeroWeightFrameFunction (g : GVec → ℚ) : Prop :=
  ∀ u v w : GVec, IsFrame u v w → g u + g v + g w = 0

/-- `g` vanishes on all nine tomography vectors. -/
def VanishesOnNineRays (g : GVec → ℚ) : Prop :=
  g tomo_e1 = 0 ∧ g tomo_e2 = 0 ∧ g tomo_e3 = 0 ∧
  g tomo_e12 = 0 ∧ g tomo_e13 = 0 ∧ g tomo_e23 = 0 ∧
  g tomo_e12i = 0 ∧ g tomo_e13i = 0 ∧ g tomo_e23i = 0

/-- The tomography residual `g = f - quadRay (tomographyForm f)`. -/
def residual (f : GVec → ℚ) (v : GVec) : ℚ :=
  f v - quadRay (tomographyForm f) v

theorem zeroWeight_smul {g : GVec → ℚ} (hg : IsZeroWeightFrameFunction g)
    {v : GVec} (hv : v.NonZero) {l : GaussRat} (hl : l ≠ 0) :
    g (GVec.smul l v) = g v := by
  obtain ⟨w, u, h1, h2⟩ := exists_frame_completion hv
  have e1 := hg _ _ _ h1
  have e2 := hg _ _ _ (h2 l hl)
  linarith

theorem residual_is_zero_weight {f : GVec → ℚ} (hf : IsFrameFunction f) :
    IsZeroWeightFrameFunction (residual f) := by
  intro u v w hfr
  unfold residual
  have h1 := hf u v w hfr
  have h2 := tomography_isFrameFunction hf u v w hfr
  linarith

theorem residual_vanishes_on_nine_rays (f : GVec → ℚ) :
    VanishesOnNineRays (residual f) := by
  have hm := tomography_matches_nine_rays f
  unfold VanishesOnNineRays residual
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> linarith

theorem tomographyForm_eq_zero_of_vanishes {g : GVec → ℚ} (hg : VanishesOnNineRays g) :
    tomographyForm g = ⟨0, 0, 0, 0, 0, 0, 0, 0, 0⟩ := by
  rcases hg with ⟨h1, h2, h3, h12, h13, h23, h12i, h13i, h23i⟩
  ext <;> simp [tomographyForm, h1, h2, h3, h12, h13, h23, h12i, h13i, h23i]

/-- Signed quadratic rigidity on `ℚ(i)³` is equivalent to the vanishing of all zero-weight
frame functions that vanish on the nine tomography rays. -/
theorem signed_rigidity_iff_zero_residual :
    (∀ f : GVec → ℚ, IsFrameFunction f →
      ∃ ρ : HermForm3, ρ.tr = 1 ∧ ∀ v : GVec, v.NonZero → f v = quadRay ρ v) ↔
    (∀ g : GVec → ℚ, IsZeroWeightFrameFunction g → VanishesOnNineRays g →
      ∀ v : GVec, v.NonZero → g v = 0) := by
  constructor
  · intro hrig g hg hvan v hv
    let f : GVec → ℚ := fun x => 1 / 3 + g x
    have hf : IsFrameFunction f := by
      intro x y z hfr
      have hsum := hg x y z hfr
      simp only [f]
      linarith
    obtain ⟨ρ, _, hρ⟩ := hrig f hf
    have hm : tomographyForm f = ρ := by
      apply tomography_unique (tomographyForm f) ρ
      · rw [(tomography_matches_nine_rays f).1, hρ tomo_e1 tomo_e1_nonZero]
      · rw [(tomography_matches_nine_rays f).2.1, hρ tomo_e2 tomo_e2_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.1, hρ tomo_e3 tomo_e3_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.1, hρ tomo_e12 tomo_e12_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.2.1, hρ tomo_e13 tomo_e13_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.2.2.1, hρ tomo_e23 tomo_e23_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.2.2.2.1, hρ tomo_e12i tomo_e12i_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.2.2.2.2.1, hρ tomo_e13i tomo_e13i_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.2.2.2.2.2, hρ tomo_e23i tomo_e23i_nonZero]
    rcases hvan with ⟨h1, h2, h3, h12, h13, h23, h12i, h13i, h23i⟩
    have hρ_id : ρ = ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ := by
      rw [← hm]
      ext <;> simp [tomographyForm, f, h1, h2, h3, h12, h13, h23, h12i, h13i, h23i]
    have hfv := hρ v hv
    rw [hρ_id] at hfv
    have hq_third : quadRay ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ v = 1 / 3 := by
      have hnz := normSqVec_ne_zero_of_nonZero hv
      have hnum : quadNum ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ v = (1 / 3) * normSqVec v := by
        simp only [quadNum, normSqVec]
        ring
      rw [quadRay, hnum, mul_div_cancel_right₀ (1 / 3) hnz]
    simp only [f] at hfv
    linarith
  · intro hzero f hf
    refine ⟨tomographyForm f, tomography_trace_one hf, ?_⟩
    intro v hv
    have hr := hzero (residual f) (residual_is_zero_weight hf) (residual_vanishes_on_nine_rays f) v hv
    unfold residual at hr
    linarith

/-! ### 5. Bounded Residual and Nonnegative Rigidity Equivalence -/

/-- A nonnegative frame function is a frame function taking values `≥ 0` on all nonzero vectors. -/
def IsNonnegFrameFunction (f : GVec → ℚ) : Prop :=
  IsFrameFunction f ∧ ∀ v : GVec, v.NonZero → 0 ≤ f v

/-- `g` is bounded in absolute value on all nonzero vectors in `ℚ(i)³`. -/
def IsBoundedOnRays (g : GVec → ℚ) : Prop :=
  ∃ B : ℚ, 0 ≤ B ∧ ∀ v : GVec, v.NonZero → |g v| ≤ B

/-- Every nonnegative frame function takes values in `[0, 1]` on all nonzero vectors. -/
theorem nonneg_frameFunction_bounds {f : GVec → ℚ} (hf : IsNonnegFrameFunction f)
    {v : GVec} (hv : v.NonZero) : 0 ≤ f v ∧ f v ≤ 1 := by
  obtain ⟨w, u, hfr, _⟩ := exists_frame_completion hv
  have hsum := hf.1 v w u hfr
  have hfv := hf.2 v hv
  have hfw := hf.2 w hfr.2.1
  have hfu := hf.2 u hfr.2.2.1
  exact ⟨hfv, by linarith⟩

theorem abs_two_mul_le_sum_sq (a b : ℚ) : |2 * (a * b)| ≤ a ^ 2 + b ^ 2 := by
  have h1 : 0 ≤ (a - b) ^ 2 := sq_nonneg (a - b)
  have h2 : 0 ≤ (a + b) ^ 2 := sq_nonneg (a + b)
  exact abs_le.mpr ⟨by nlinarith, by nlinarith⟩

theorem abs_two_re_inner_le (x y : GaussRat) :
    |2 * (x.re * y.re + x.im * y.im)| ≤ x.normSq + y.normSq := by
  have h1 := abs_two_mul_le_sum_sq x.re y.re
  have h2 := abs_two_mul_le_sum_sq x.im y.im
  obtain ⟨h1l, h1u⟩ := abs_le.mp h1
  obtain ⟨h2l, h2u⟩ := abs_le.mp h2
  simp only [GaussRat.normSq]
  exact abs_le.mpr ⟨by linarith, by linarith⟩

theorem abs_two_im_inner_le (x y : GaussRat) :
    |2 * (x.re * y.im - x.im * y.re)| ≤ x.normSq + y.normSq := by
  have h1 := abs_two_mul_le_sum_sq x.re y.im
  have h2 := abs_two_mul_le_sum_sq x.im y.re
  obtain ⟨h1l, h1u⟩ := abs_le.mp h1
  obtain ⟨h2l, h2u⟩ := abs_le.mp h2
  simp only [GaussRat.normSq]
  exact abs_le.mpr ⟨by linarith, by linarith⟩

theorem abs_mul_nonneg_le {c x M : ℚ} (hx0 : 0 ≤ x) (hxM : x ≤ M) :
    |c * x| ≤ |c| * M := by
  have hc1 := le_abs_self c
  have hc2 := neg_abs_le c
  have h0 : 0 ≤ |c| := abs_nonneg c
  exact abs_le.mpr ⟨by nlinarith, by nlinarith⟩

theorem abs_two_coeff_mul_le {a t M : ℚ} (ht : |2 * t| ≤ M) (hM : 0 ≤ M) :
    |2 * a * t| ≤ 2 * |a| * M := by
  have ha1 := le_abs_self a
  have ha2 := neg_abs_le a
  have ha0 : 0 ≤ |a| := abs_nonneg a
  obtain ⟨htl, htu⟩ := abs_le.mp ht
  exact abs_le.mpr ⟨by nlinarith, by nlinarith⟩

theorem abs_quadNum_le (ρ : HermForm3) (v : GVec) :
    |quadNum ρ v| ≤ ρ.coeffNorm * normSqVec v := by
  have hx := normSq_nonneg v.x
  have hy := normSq_nonneg v.y
  have hz := normSq_nonneg v.z
  have hN : 0 ≤ normSqVec v := normSqVec_nonneg v
  have hd1 : |ρ.d1 * v.x.normSq| ≤ |ρ.d1| * normSqVec v :=
    abs_mul_nonneg_le hx (by unfold normSqVec; linarith)
  have hd2 : |ρ.d2 * v.y.normSq| ≤ |ρ.d2| * normSqVec v :=
    abs_mul_nonneg_le hy (by unfold normSqVec; linarith)
  have hd3 : |ρ.d3 * v.z.normSq| ≤ |ρ.d3| * normSqVec v :=
    abs_mul_nonneg_le hz (by unfold normSqVec; linarith)
  have ha12 : |2 * ρ.a12 * (v.x.re * v.y.re + v.x.im * v.y.im)| ≤ 2 * |ρ.a12| * normSqVec v :=
    abs_two_coeff_mul_le (by unfold normSqVec; linarith [abs_two_re_inner_le v.x v.y]) hN
  have ha13 : |2 * ρ.a13 * (v.x.re * v.z.re + v.x.im * v.z.im)| ≤ 2 * |ρ.a13| * normSqVec v :=
    abs_two_coeff_mul_le (by unfold normSqVec; linarith [abs_two_re_inner_le v.x v.z]) hN
  have ha23 : |2 * ρ.a23 * (v.y.re * v.z.re + v.y.im * v.z.im)| ≤ 2 * |ρ.a23| * normSqVec v :=
    abs_two_coeff_mul_le (by unfold normSqVec; linarith [abs_two_re_inner_le v.y v.z]) hN
  have hb12 : |-(2 * ρ.b12 * (v.x.re * v.y.im - v.x.im * v.y.re))| ≤ 2 * |ρ.b12| * normSqVec v := by
    rw [abs_neg]
    exact abs_two_coeff_mul_le (by unfold normSqVec; linarith [abs_two_im_inner_le v.x v.y]) hN
  have hb13 : |-(2 * ρ.b13 * (v.x.re * v.z.im - v.x.im * v.z.re))| ≤ 2 * |ρ.b13| * normSqVec v := by
    rw [abs_neg]
    exact abs_two_coeff_mul_le (by unfold normSqVec; linarith [abs_two_im_inner_le v.x v.z]) hN
  have hb23 : |-(2 * ρ.b23 * (v.y.re * v.z.im - v.y.im * v.z.re))| ≤ 2 * |ρ.b23| * normSqVec v := by
    rw [abs_neg]
    exact abs_two_coeff_mul_le (by unfold normSqVec; linarith [abs_two_im_inner_le v.y v.z]) hN
  let t1 := ρ.d1 * v.x.normSq
  let t2 := ρ.d2 * v.y.normSq
  let t3 := ρ.d3 * v.z.normSq
  let t4 := 2 * ρ.a12 * (v.x.re * v.y.re + v.x.im * v.y.im)
  let t5 := 2 * ρ.a13 * (v.x.re * v.z.re + v.x.im * v.z.im)
  let t6 := 2 * ρ.a23 * (v.y.re * v.z.re + v.y.im * v.z.im)
  let t7 := -(2 * ρ.b12 * (v.x.re * v.y.im - v.x.im * v.y.re))
  let t8 := -(2 * ρ.b13 * (v.x.re * v.z.im - v.x.im * v.z.re))
  let t9 := -(2 * ρ.b23 * (v.y.re * v.z.im - v.y.im * v.z.re))
  have hrew : quadNum ρ v = t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 := by
    simp only [quadNum, t1, t2, t3, t4, t5, t6, t7, t8, t9]
    ring
  rw [hrew]
  have s1 := abs_add_le (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8) t9
  have s2 := abs_add_le (t1 + t2 + t3 + t4 + t5 + t6 + t7) t8
  have s3 := abs_add_le (t1 + t2 + t3 + t4 + t5 + t6) t7
  have s4 := abs_add_le (t1 + t2 + t3 + t4 + t5) t6
  have s5 := abs_add_le (t1 + t2 + t3 + t4) t5
  have s6 := abs_add_le (t1 + t2 + t3) t4
  have s7 := abs_add_le (t1 + t2) t3
  have s8 := abs_add_le t1 t2
  unfold HermForm3.coeffNorm
  linarith

/-- On every nonzero vector `v`, `|quadRay ρ v| ≤ ρ.coeffNorm`. -/
theorem abs_quadRay_le (ρ : HermForm3) {v : GVec} (hv : v.NonZero) :
    |quadRay ρ v| ≤ ρ.coeffNorm := by
  have hpos := normSqVec_pos_of_nonZero hv
  have hmul : quadRay ρ v * normSqVec v = quadNum ρ v :=
    div_mul_cancel₀ (quadNum ρ v) (ne_of_gt hpos)
  obtain ⟨hl, hu⟩ := abs_le.mp (abs_quadNum_le ρ v)
  exact abs_le.mpr ⟨by nlinarith, by nlinarith⟩

theorem coeffNorm_nonneg (ρ : HermForm3) : 0 ≤ ρ.coeffNorm := by
  unfold HermForm3.coeffNorm
  linarith [abs_nonneg ρ.d1, abs_nonneg ρ.d2, abs_nonneg ρ.d3,
    abs_nonneg ρ.a12, abs_nonneg ρ.a13, abs_nonneg ρ.a23,
    abs_nonneg ρ.b12, abs_nonneg ρ.b13, abs_nonneg ρ.b23]

/-- If `f` is a nonnegative frame function, its tomography residual `residual f` is bounded on all rays. -/
theorem nonneg_residual_is_bounded {f : GVec → ℚ} (hf : IsNonnegFrameFunction f) :
    IsBoundedOnRays (residual f) := by
  refine ⟨1 + (tomographyForm f).coeffNorm, by linarith [coeffNorm_nonneg (tomographyForm f)], ?_⟩
  intro v hv
  unfold residual
  have hfb := nonneg_frameFunction_bounds hf hv
  have hfv_abs : |f v| ≤ 1 := abs_le.mpr ⟨by linarith [hfb.1], hfb.2⟩
  have hqb := abs_quadRay_le (tomographyForm f) hv
  have htri := abs_sub (f v) (quadRay (tomographyForm f) v)
  linarith

/-- For a zero-weight frame function `g`, a one-sided lower bound `g ≥ -M` on all nonzero vectors
forces the upper bound `g ≤ 2 M` on all nonzero vectors. -/
theorem one_sided_lower_bound_implies_upper_bound {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) {M : ℚ}
    (hlow : ∀ v : GVec, v.NonZero → -M ≤ g v) {v : GVec} (hv : v.NonZero) :
    g v ≤ 2 * M := by
  obtain ⟨w, u, hfr, _⟩ := exists_frame_completion hv
  have hsum := hg v w u hfr
  have hw := hlow w hfr.2.1
  have hu := hlow u hfr.2.2.1
  linarith

/-- Nonnegative quadratic rigidity on `ℚ(i)³` is equivalent to the vanishing of all bounded
zero-weight frame functions that vanish on the nine tomography rays. -/
theorem nonneg_rigidity_iff_bounded_zero_residual :
    (∀ f : GVec → ℚ, IsNonnegFrameFunction f →
      ∃ ρ : HermForm3, ρ.tr = 1 ∧ ∀ v : GVec, v.NonZero → f v = quadRay ρ v) ↔
    (∀ g : GVec → ℚ, IsZeroWeightFrameFunction g → VanishesOnNineRays g → IsBoundedOnRays g →
      ∀ v : GVec, v.NonZero → g v = 0) := by
  constructor
  · intro hrig g hg hvan ⟨B, hB, hbound⟩ v hv
    let c : ℚ := 1 / (3 * (B + 1))
    have hB1 : 0 < B + 1 := by linarith
    have h3B1 : 0 < 3 * (B + 1) := by linarith
    have hc_ne : c ≠ 0 := div_ne_zero one_ne_zero (ne_of_gt h3B1)
    have hc_mul : 3 * (B + 1) * c = 1 := mul_one_div_cancel (ne_of_gt h3B1)
    let f : GVec → ℚ := fun x => 1 / 3 + c * g x
    have hf_frame : IsFrameFunction f := by
      intro x y z hfr
      have hsum := hg x y z hfr
      simp only [f]
      linear_combination c * hsum
    have hf_nonneg : IsNonnegFrameFunction f := by
      refine ⟨hf_frame, ?_⟩
      intro x hx
      have hgx : -B ≤ g x := (abs_le.mp (hbound x hx)).1
      have hprod : 3 * (B + 1) * f x = B + 1 + g x := by
        simp only [f]
        linear_combination g x * hc_mul
      have hprod_nonneg : 0 ≤ 3 * (B + 1) * f x := by linarith
      nlinarith
    obtain ⟨ρ, _, hρ⟩ := hrig f hf_nonneg
    have hm : tomographyForm f = ρ := by
      apply tomography_unique (tomographyForm f) ρ
      · rw [(tomography_matches_nine_rays f).1, hρ tomo_e1 tomo_e1_nonZero]
      · rw [(tomography_matches_nine_rays f).2.1, hρ tomo_e2 tomo_e2_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.1, hρ tomo_e3 tomo_e3_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.1, hρ tomo_e12 tomo_e12_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.2.1, hρ tomo_e13 tomo_e13_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.2.2.1, hρ tomo_e23 tomo_e23_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.2.2.2.1, hρ tomo_e12i tomo_e12i_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.2.2.2.2.1, hρ tomo_e13i tomo_e13i_nonZero]
      · rw [(tomography_matches_nine_rays f).2.2.2.2.2.2.2.2, hρ tomo_e23i tomo_e23i_nonZero]
    rcases hvan with ⟨h1, h2, h3, h12, h13, h23, h12i, h13i, h23i⟩
    have hρ_id : ρ = ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ := by
      rw [← hm]
      ext <;> simp [tomographyForm, f, h1, h2, h3, h12, h13, h23, h12i, h13i, h23i]
    have hfv := hρ v hv
    rw [hρ_id] at hfv
    have hq_third : quadRay ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ v = 1 / 3 := by
      have hnz := normSqVec_ne_zero_of_nonZero hv
      have hnum : quadNum ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ v = (1 / 3) * normSqVec v := by
        simp only [quadNum, normSqVec]
        ring
      rw [quadRay, hnum, mul_div_cancel_right₀ (1 / 3) hnz]
    rw [hq_third] at hfv
    simp only [f] at hfv
    have hcg : c * g v = 0 := by linarith
    exact (mul_eq_zero.mp hcg).resolve_left hc_ne
  · intro hzero f hf
    refine ⟨tomographyForm f, tomography_trace_one hf.1, ?_⟩
    intro v hv
    have hr := hzero (residual f) (residual_is_zero_weight hf.1)
      (residual_vanishes_on_nine_rays f) (nonneg_residual_is_bounded hf) v hv
    unfold residual at hr
    linarith

/-! ### 6. `(1+i)`-Adic Norm-Parity Structure on `ℚ(i)³` -/

/-- A Gaussian-integer vector `(a+bi, c+di, e+gi)` is `(1+i)`-primitive when not all three
coordinates are divisible by `1 + i` (equivalently, not all of `a+b, c+d, e+g` are even). -/
abbrev IsOnePlusIPrimitive (a b c d e g : ℤ) : Prop :=
  ¬ ((a + b) % 2 = 0 ∧ (c + d) % 2 = 0 ∧ (e + g) % 2 = 0)

/-- Unlike primitive integer vectors in `ℤ³` where `a² + b² + c² ≢ 0 (mod 4)`, the
`(1+i)`-primitive vector `(1, 1, 1+i)` in `ℤ[i]³` has Hermitian norm `4`. -/
theorem gaussian_norm_div_four_witness :
    IsOnePlusIPrimitive 1 0 1 0 1 1 ∧ normSqVec (gv 1 0 1 0 1 1) = 4 := by
  refine ⟨by decide, ?_⟩
  simp [normSqVec, GaussRat.normSq, gv]
  norm_num

/-- The `(1+i)`-primitive vector `(1+2i, 1, 1+i)` in `ℤ[i]³` has Hermitian norm `8`,
witnessing `2`-adic isotropy of the 6-variable Gaussian Hermitian norm modulo `8`. -/
theorem gaussian_norm_eight_primitive_witness :
    IsOnePlusIPrimitive 1 2 1 0 1 1 ∧ normSqVec (gv 1 2 1 0 1 1) = 8 := by
  refine ⟨by decide, ?_⟩
  simp [normSqVec, GaussRat.normSq, gv]
  norm_num

theorem sq_emod_four (x : ℤ) : x ^ 2 % 4 = x % 2 := by
  have hxx := Int.mul_emod x x 4
  have hx4 : x % 4 = 0 ∨ x % 4 = 1 ∨ x % 4 = 2 ∨ x % 4 = 3 := by omega
  rcases hx4 with hx4 | hx4 | hx4 | hx4 <;> simp only [sq, hx4] at hxx ⊢ <;> omega

theorem sq_add_sq_emod_four (x y : ℤ) : (x ^ 2 + y ^ 2) % 4 = x % 2 + y % 2 := by
  have hx := sq_emod_four x
  have hy := sq_emod_four y
  have hadd := Int.add_emod (x ^ 2) (y ^ 2) 4
  omega

theorem sq_add_sq_emod_two (x y : ℤ) : (x ^ 2 + y ^ 2) % 2 = (x + y) % 2 := by
  have h4 := sq_add_sq_emod_four x y
  omega

/-- For a Gaussian integer `x + y i`, `(1+i)`-divisibility controls `x² + y² (mod 4)`:
* `(x² + y²) % 4 ∈ {0, 1, 2}` (a sum of two squares is never `3 (mod 4)`);
* `(x + y) % 2 = 0 ↔ (x² + y²) % 2 = 0`;
* `(x² + y²) % 2 = 1 ↔ (x² + y²) % 4 = 1`;
* `x % 2 = 0 ∧ y % 2 = 0 ↔ (x² + y²) % 4 = 0`;
* `x % 2 ≠ 0 ∧ y % 2 ≠ 0 ↔ (x² + y²) % 4 = 2`. -/
theorem gaussian_coord_norm_mod_four (x y : ℤ) :
    ((x ^ 2 + y ^ 2) % 4 = 0 ∨ (x ^ 2 + y ^ 2) % 4 = 1 ∨ (x ^ 2 + y ^ 2) % 4 = 2) ∧
    ((x + y) % 2 = 0 ↔ (x ^ 2 + y ^ 2) % 2 = 0) ∧
    ((x ^ 2 + y ^ 2) % 2 = 1 ↔ (x ^ 2 + y ^ 2) % 4 = 1) ∧
    (x % 2 = 0 ∧ y % 2 = 0 ↔ (x ^ 2 + y ^ 2) % 4 = 0) ∧
    (x % 2 ≠ 0 ∧ y % 2 ≠ 0 ↔ (x ^ 2 + y ^ 2) % 4 = 2) := by
  rw [sq_add_sq_emod_four x y, sq_add_sq_emod_two x y]
  omega

/-- On a `(1+i)`-primitive vector `(a+bi, c+di, e+gi) ∈ ℤ[i]³`, the Hermitian norm
`a² + b² + c² + d² + e² + g²` is divisible by `4` if and only if two coordinates are
`(1+i)`-odd (`norm % 2 = 1`) and the remaining coordinate has `(1+i)`-valuation `1`
(`norm % 4 = 2`). -/
theorem primitive_gaussian_norm_mod_four_iff (a b c d e g : ℤ)
    (hprim : IsOnePlusIPrimitive a b c d e g) :
    (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + e ^ 2 + g ^ 2) % 4 = 0 ↔
      ((a ^ 2 + b ^ 2) % 2 = 1 ∧ (c ^ 2 + d ^ 2) % 2 = 1 ∧ (e ^ 2 + g ^ 2) % 4 = 2) ∨
      ((a ^ 2 + b ^ 2) % 2 = 1 ∧ (c ^ 2 + d ^ 2) % 4 = 2 ∧ (e ^ 2 + g ^ 2) % 2 = 1) ∨
      ((a ^ 2 + b ^ 2) % 4 = 2 ∧ (c ^ 2 + d ^ 2) % 2 = 1 ∧ (e ^ 2 + g ^ 2) % 2 = 1) := by
  have hsum : (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + e ^ 2 + g ^ 2) % 4 =
      ((a ^ 2 + b ^ 2) % 4 + (c ^ 2 + d ^ 2) % 4 + (e ^ 2 + g ^ 2) % 4) % 4 := by
    have h1 : a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + e ^ 2 + g ^ 2 =
        ((a ^ 2 + b ^ 2) + (c ^ 2 + d ^ 2)) + (e ^ 2 + g ^ 2) := by ring
    rw [h1]
    omega
  rw [hsum,
    sq_add_sq_emod_four a b, sq_add_sq_emod_four c d, sq_add_sq_emod_four e g,
    sq_add_sq_emod_two a b, sq_add_sq_emod_two c d, sq_add_sq_emod_two e g]
  unfold IsOnePlusIPrimitive at hprim
  omega

/-! ### 7. Zero-Vector Normalization and Operator-Space Projector Duality (Section 5) -/

theorem normSqVec_zero : normSqVec ⟨0, 0, 0⟩ = 0 := by
  simp [normSqVec, GaussRat.normSq]

theorem quadNum_zero (ρ : HermForm3) : quadNum ρ ⟨0, 0, 0⟩ = 0 := by
  simp [quadNum, GaussRat.normSq]

theorem quadRay_zero (ρ : HermForm3) : quadRay ρ ⟨0, 0, 0⟩ = 0 := by
  simp [quadRay, quadNum_zero, normSqVec_zero]

/-- Canonical zero-normalized extension of `f : GVec → ℚ` taking value `0` at `⟨0, 0, 0⟩`. -/
def normalizeAtZero (f : GVec → ℚ) (v : GVec) : ℚ :=
  if v.x = 0 ∧ v.y = 0 ∧ v.z = 0 then 0 else f v

theorem normalizeAtZero_zero (f : GVec → ℚ) : normalizeAtZero f ⟨0, 0, 0⟩ = 0 := by
  simp [normalizeAtZero]

theorem normalizeAtZero_of_nonZero (f : GVec → ℚ) {v : GVec} (hv : v.NonZero) :
    normalizeAtZero f v = f v := by
  unfold normalizeAtZero
  rw [if_neg]
  rintro ⟨hx, hy, hz⟩
  rcases hv with h | h | h
  · exact h hx
  · exact h hy
  · exact h hz

theorem normalizeAtZero_isFrameFunction {f : GVec → ℚ} (hf : IsFrameFunction f) :
    IsFrameFunction (normalizeAtZero f) := by
  intro u v w hfr
  rw [normalizeAtZero_of_nonZero f hfr.1,
      normalizeAtZero_of_nonZero f hfr.2.1,
      normalizeAtZero_of_nonZero f hfr.2.2.1]
  exact hf u v w hfr

/-- If `f ⟨0, 0, 0⟩ = 0` and `f v = quadRay ρ v` on all nonzero vectors, then `f v = quadRay ρ v`
holds for every `v : GVec` without any `v.NonZero` precondition. -/
theorem eq_quadRay_all_of_zero_at_zero {f : GVec → ℚ} {ρ : HermForm3}
    (hf0 : f ⟨0, 0, 0⟩ = 0)
    (h : ∀ v : GVec, v.NonZero → f v = quadRay ρ v) (v : GVec) :
    f v = quadRay ρ v := by
  by_cases hz : v.x = 0 ∧ v.y = 0 ∧ v.z = 0
  · rcases v with ⟨x, y, z⟩
    rcases hz with ⟨rfl, rfl, rfl⟩
    rw [hf0, quadRay_zero]
  · apply h v
    unfold GVec.NonZero
    tauto

/-- The zero `3 × 3` Hermitian matrix. -/
def HermForm3.zero : HermForm3 := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0⟩

/-- The `3 × 3` identity matrix `I₃` as a Hermitian form. -/
def HermForm3.id : HermForm3 := ⟨1, 1, 1, 0, 0, 0, 0, 0, 0⟩

/-- Addition of `3 × 3` Hermitian matrices. -/
def HermForm3.add (ρ σ : HermForm3) : HermForm3 :=
  ⟨ρ.d1 + σ.d1, ρ.d2 + σ.d2, ρ.d3 + σ.d3,
   ρ.a12 + σ.a12, ρ.a13 + σ.a13, ρ.a23 + σ.a23,
   ρ.b12 + σ.b12, ρ.b13 + σ.b13, ρ.b23 + σ.b23⟩

/-- Subtraction of `3 × 3` Hermitian matrices. -/
def HermForm3.sub (ρ σ : HermForm3) : HermForm3 :=
  ⟨ρ.d1 - σ.d1, ρ.d2 - σ.d2, ρ.d3 - σ.d3,
   ρ.a12 - σ.a12, ρ.a13 - σ.a13, ρ.a23 - σ.a23,
   ρ.b12 - σ.b12, ρ.b13 - σ.b13, ρ.b23 - σ.b23⟩

/-- Rational scalar multiplication on `3 × 3` Hermitian matrices. -/
def HermForm3.smul (c : ℚ) (ρ : HermForm3) : HermForm3 :=
  ⟨c * ρ.d1, c * ρ.d2, c * ρ.d3,
   c * ρ.a12, c * ρ.a13, c * ρ.a23,
   c * ρ.b12, c * ρ.b13, c * ρ.b23⟩

/-- Rational Frobenius / Hilbert-Schmidt trace pairing `tr(ρ σ)` on `HermForm3`. -/
def traceInner (ρ σ : HermForm3) : ℚ :=
  ρ.d1 * σ.d1 + ρ.d2 * σ.d2 + ρ.d3 * σ.d3 +
  2 * (ρ.a12 * σ.a12 + ρ.a13 * σ.a13 + ρ.a23 * σ.a23 +
       ρ.b12 * σ.b12 + ρ.b13 * σ.b13 + ρ.b23 * σ.b23)

theorem traceInner_comm (ρ σ : HermForm3) : traceInner ρ σ = traceInner σ ρ := by
  simp only [traceInner]
  ring

theorem traceInner_add_right (ρ σ τ : HermForm3) :
    traceInner ρ (HermForm3.add σ τ) = traceInner ρ σ + traceInner ρ τ := by
  simp only [traceInner, HermForm3.add]
  ring

theorem traceInner_sub_left (ρ σ τ : HermForm3) :
    traceInner (HermForm3.sub ρ σ) τ = traceInner ρ τ - traceInner σ τ := by
  simp only [traceInner, HermForm3.sub]
  ring

theorem traceInner_smul_right (c : ℚ) (ρ σ : HermForm3) :
    traceInner ρ (HermForm3.smul c σ) = c * traceInner ρ σ := by
  simp only [traceInner, HermForm3.smul]
  ring

theorem traceInner_id_right (ρ : HermForm3) :
    traceInner ρ HermForm3.id = ρ.tr := by
  simp only [traceInner, HermForm3.id, HermForm3.tr]
  ring

theorem traceInner_self_nonneg (ρ : HermForm3) : 0 ≤ traceInner ρ ρ := by
  unfold traceInner
  linarith [sq_nonneg ρ.d1, sq_nonneg ρ.d2, sq_nonneg ρ.d3,
    sq_nonneg ρ.a12, sq_nonneg ρ.a13, sq_nonneg ρ.a23,
    sq_nonneg ρ.b12, sq_nonneg ρ.b13, sq_nonneg ρ.b23]

/-- The Frobenius trace pairing `traceInner` is positive-definite on `HermForm3`. -/
theorem traceInner_self_eq_zero_iff (ρ : HermForm3) :
    traceInner ρ ρ = 0 ↔ ρ = HermForm3.zero := by
  constructor
  · intro h
    unfold traceInner at h
    have hd1 := sq_nonneg ρ.d1
    have hd2 := sq_nonneg ρ.d2
    have hd3 := sq_nonneg ρ.d3
    have ha12 := sq_nonneg ρ.a12
    have ha13 := sq_nonneg ρ.a13
    have ha23 := sq_nonneg ρ.a23
    have hb12 := sq_nonneg ρ.b12
    have hb13 := sq_nonneg ρ.b13
    have hb23 := sq_nonneg ρ.b23
    have ed1 : ρ.d1 * ρ.d1 = 0 := by nlinarith
    have ed2 : ρ.d2 * ρ.d2 = 0 := by nlinarith
    have ed3 : ρ.d3 * ρ.d3 = 0 := by nlinarith
    have ea12 : ρ.a12 * ρ.a12 = 0 := by nlinarith
    have ea13 : ρ.a13 * ρ.a13 = 0 := by nlinarith
    have ea23 : ρ.a23 * ρ.a23 = 0 := by nlinarith
    have eb12 : ρ.b12 * ρ.b12 = 0 := by nlinarith
    have eb13 : ρ.b13 * ρ.b13 = 0 := by nlinarith
    have eb23 : ρ.b23 * ρ.b23 = 0 := by nlinarith
    ext
    · exact mul_self_eq_zero.mp ed1
    · exact mul_self_eq_zero.mp ed2
    · exact mul_self_eq_zero.mp ed3
    · exact mul_self_eq_zero.mp ea12
    · exact mul_self_eq_zero.mp ea13
    · exact mul_self_eq_zero.mp ea23
    · exact mul_self_eq_zero.mp eb12
    · exact mul_self_eq_zero.mp eb13
    · exact mul_self_eq_zero.mp eb23
  · rintro rfl
    simp [traceInner, HermForm3.zero]

/-- Nondegeneracy of the Frobenius trace pairing: if `tr(ρ τ) = tr(σ τ)` for all `τ`, then `ρ = σ`. -/
theorem traceInner_ext {ρ σ : HermForm3}
    (h : ∀ τ : HermForm3, traceInner ρ τ = traceInner σ τ) : ρ = σ := by
  have hsub : traceInner (HermForm3.sub ρ σ) (HermForm3.sub ρ σ) = 0 := by
    rw [traceInner_sub_left, h (HermForm3.sub ρ σ), sub_self]
  have hz := (traceInner_self_eq_zero_iff (HermForm3.sub ρ σ)).mp hsub
  have hd1 := congrArg HermForm3.d1 hz
  have hd2 := congrArg HermForm3.d2 hz
  have hd3 := congrArg HermForm3.d3 hz
  have ha12 := congrArg HermForm3.a12 hz
  have ha13 := congrArg HermForm3.a13 hz
  have ha23 := congrArg HermForm3.a23 hz
  have hb12 := congrArg HermForm3.b12 hz
  have hb13 := congrArg HermForm3.b13 hz
  have hb23 := congrArg HermForm3.b23 hz
  simp only [HermForm3.sub, HermForm3.zero] at hd1 hd2 hd3 ha12 ha13 ha23 hb12 hb13 hb23
  ext <;> linarith

/-- The normalized rank-1 Hermitian ray projector `T(v) = v v* / ⟨v, v⟩ ∈ HermForm3`. -/
def rayProj (v : GVec) : HermForm3 where
  d1 := v.x.normSq / normSqVec v
  d2 := v.y.normSq / normSqVec v
  d3 := v.z.normSq / normSqVec v
  a12 := (v.x.re * v.y.re + v.x.im * v.y.im) / normSqVec v
  a13 := (v.x.re * v.z.re + v.x.im * v.z.im) / normSqVec v
  a23 := (v.y.re * v.z.re + v.y.im * v.z.im) / normSqVec v
  b12 := -(v.x.re * v.y.im - v.x.im * v.y.re) / normSqVec v
  b13 := -(v.x.re * v.z.im - v.x.im * v.z.re) / normSqVec v
  b23 := -(v.y.re * v.z.im - v.y.im * v.z.re) / normSqVec v

/-- Operator-space duality (`Section 5`): `tr(ρ T(v)) = quadRay ρ v` for all `ρ` and `v`. -/
theorem traceInner_rayProj (ρ : HermForm3) (v : GVec) :
    traceInner ρ (rayProj v) = quadRay ρ v := by
  simp only [traceInner, rayProj, quadRay, quadNum]
  ring

/-- The ray projector `rayProj v` is invariant under nonzero Gaussian-rational scaling. -/
theorem rayProj_smul {l : GaussRat} (hl : l ≠ 0) (v : GVec) :
    rayProj (GVec.smul l v) = rayProj v := by
  apply traceInner_ext
  intro τ
  rw [traceInner_comm, traceInner_rayProj, traceInner_comm, traceInner_rayProj,
    quadRay_smul τ hl v]

/-- Every nonzero vector `v` has trace-one projector `tr(T(v)) = 1`. -/
theorem rayProj_tr {v : GVec} (hv : v.NonZero) : (rayProj v).tr = 1 := by
  have hnz := normSqVec_ne_zero_of_nonZero hv
  unfold HermForm3.tr rayProj normSqVec
  dsimp
  rw [← add_div, ← add_div]
  exact div_self hnz

/-- Exact matrix resolution of the identity (`Section 5`): for every orthogonal frame `(u, v, w)`
in `ℚ(i)³` (without assuming unit-norm representatives), `T(u) + T(v) + T(w) = I₃`. -/
theorem rayProj_frame_sum {u v w : GVec} (hfr : IsFrame u v w) :
    HermForm3.add (HermForm3.add (rayProj u) (rayProj v)) (rayProj w) = HermForm3.id := by
  apply traceInner_ext
  intro τ
  rw [traceInner_comm, traceInner_add_right, traceInner_add_right,
    traceInner_rayProj, traceInner_rayProj, traceInner_rayProj,
    quadRay_frame_sum τ hfr, traceInner_comm, traceInner_id_right]

/-- Explicit 9-ray basis expansion (`Section 5`): every `ρ ∈ HermForm3` is a `ℚ`-linear
combination of the nine tomography ray projectors `rayProj tomo_e1`, ..., `rayProj tomo_e23i`,
establishing surjectivity of the projector map `T` onto `HermForm3`. -/
theorem rayProj_nine_rays_span_hermForm3 (ρ : HermForm3) :
    ρ = HermForm3.add
      (HermForm3.add
        (HermForm3.add
          (HermForm3.add
            (HermForm3.add
              (HermForm3.add
                (HermForm3.add
                  (HermForm3.add
                    (HermForm3.smul (ρ.d1 - ρ.a12 - ρ.a13 + ρ.b12 + ρ.b13) (rayProj tomo_e1))
                    (HermForm3.smul (ρ.d2 - ρ.a12 - ρ.a23 + ρ.b12 + ρ.b23) (rayProj tomo_e2)))
                  (HermForm3.smul (ρ.d3 - ρ.a13 - ρ.a23 + ρ.b13 + ρ.b23) (rayProj tomo_e3)))
                (HermForm3.smul (2 * ρ.a12) (rayProj tomo_e12)))
              (HermForm3.smul (2 * ρ.a13) (rayProj tomo_e13)))
            (HermForm3.smul (2 * ρ.a23) (rayProj tomo_e23)))
          (HermForm3.smul (-2 * ρ.b12) (rayProj tomo_e12i)))
        (HermForm3.smul (-2 * ρ.b13) (rayProj tomo_e13i)))
      (HermForm3.smul (-2 * ρ.b23) (rayProj tomo_e23i)) := by
  ext <;>
    simp [HermForm3.add, HermForm3.smul, rayProj, normSqVec, GaussRat.normSq,
      tomo_e1, tomo_e2, tomo_e3, tomo_e12, tomo_e13, tomo_e23,
      tomo_e12i, tomo_e13i, tomo_e23i, gv] <;>
    ring

/-! ### 8. Explicit Global Bounded Residual and Non-Quadratic Frame Function on `ℚ(i)³` -/

/-- Bounded-fuel helper for the `3`-adic valuation of a natural number. -/
def v3NatAux : ℕ → ℕ → ℕ
  | 0, _ => 0
  | fuel + 1, n => if 0 < n ∧ n % 3 = 0 then v3NatAux fuel (n / 3) + 1 else 0

/-- Bounded-fuel helper for the prime-to-`3` part of a natural number. -/
def p3PartNatAux : ℕ → ℕ → ℕ
  | 0, n => n
  | fuel + 1, n => if 0 < n ∧ n % 3 = 0 then p3PartNatAux fuel (n / 3) else n

/-- Number of factors of `3` in a natural number `n` (`0` if `n = 0`). -/
def v3Nat (n : ℕ) : ℕ := v3NatAux n n

/-- Prime-to-`3` part of a natural number `n` (`0` if `n = 0`). -/
def p3PartNat (n : ℕ) : ℕ := p3PartNatAux n n

theorem v3NatAux_spec : ∀ fuel n : ℕ, 3 ^ v3NatAux fuel n * p3PartNatAux fuel n = n
  | 0, n => by simp [v3NatAux, p3PartNatAux]
  | fuel + 1, n => by
      simp only [v3NatAux, p3PartNatAux]
      split_ifs with h
      · have heq := v3NatAux_spec fuel (n / 3)
        have hdiv : 3 * (n / 3) = n := Nat.mul_div_cancel' (Nat.dvd_of_mod_eq_zero h.2)
        calc
          3 ^ (v3NatAux fuel (n / 3) + 1) * p3PartNatAux fuel (n / 3)
              = 3 * (3 ^ v3NatAux fuel (n / 3) * p3PartNatAux fuel (n / 3)) := by ring
          _ = 3 * (n / 3) := by rw [heq]
          _ = n := hdiv
      · ring

theorem v3Nat_spec (n : ℕ) : 3 ^ v3Nat n * p3PartNat n = n :=
  v3NatAux_spec n n

theorem p3PartNatAux_mod_three_ne_zero :
    ∀ fuel n : ℕ, 0 < n → n ≤ fuel → p3PartNatAux fuel n % 3 ≠ 0
  | 0, n, hn, hle => by omega
  | fuel + 1, n, hn, hle => by
      simp only [p3PartNatAux]
      split_ifs with h
      · have hpos : 0 < n / 3 := by omega
        have hle' : n / 3 ≤ fuel := by omega
        exact p3PartNatAux_mod_three_ne_zero fuel (n / 3) hpos hle'
      · omega

theorem p3PartNat_mod_three_ne_zero {n : ℕ} (hn : 0 < n) : p3PartNat n % 3 ≠ 0 :=
  p3PartNatAux_mod_three_ne_zero n n hn (le_refl n)

theorem p3PartNat_pos {n : ℕ} (hn : 0 < n) : 0 < p3PartNat n := by
  have hmod := p3PartNat_mod_three_ne_zero hn
  omega

theorem pow_three_mul_unique :
    ∀ a b m k : ℕ, m % 3 ≠ 0 → k % 3 ≠ 0 → 3 ^ a * m = 3 ^ b * k → a = b ∧ m = k
  | 0, 0, m, k, _, _, heq => by
      simp only [pow_zero, one_mul] at heq
      exact ⟨rfl, heq⟩
  | 0, b + 1, m, k, hm, _, heq => by
      have hm0 : m % 3 = 0 := by
        have h1 : m = 3 ^ b * k * 3 := by
          simp only [pow_zero, one_mul, pow_succ] at heq
          linarith
        omega
      exact False.elim (hm hm0)
  | a + 1, 0, m, k, _, hk, heq => by
      have hk0 : k % 3 = 0 := by
        have h1 : k = 3 ^ a * m * 3 := by
          simp only [pow_zero, one_mul, pow_succ] at heq
          linarith
        omega
      exact False.elim (hk hk0)
  | a + 1, b + 1, m, k, hm, hk, heq => by
      have heq' : 3 ^ a * m = 3 ^ b * k := by
        simp only [pow_succ] at heq
        linarith
      obtain ⟨hab, hmk⟩ := pow_three_mul_unique a b m k hm hk heq'
      exact ⟨congrArg (· + 1) hab, hmk⟩

theorem v3Nat_p3PartNat_eq_of_pow_mul {n a m : ℕ} (hm : m % 3 ≠ 0) (heq : 3 ^ a * m = n) :
    v3Nat n = a ∧ p3PartNat n = m := by
  have hm_pos : 0 < m := by omega
  have hpow_pos : 0 < 3 ^ a := pow_pos (by decide : 0 < 3) a
  have hn : 0 < n := by nlinarith
  exact pow_three_mul_unique (v3Nat n) a (p3PartNat n) m
    (p3PartNat_mod_three_ne_zero hn) hm ((v3Nat_spec n).trans heq.symm)

theorem mul_mod_three_ne_zero {a b : ℕ} (ha : a % 3 ≠ 0) (hb : b % 3 ≠ 0) :
    (a * b) % 3 ≠ 0 := by
  rw [Nat.mul_mod]
  have ha3 : a % 3 = 1 ∨ a % 3 = 2 := by omega
  have hb3 : b % 3 = 1 ∨ b % 3 = 2 := by omega
  rcases ha3 with h1 | h1 <;> rcases hb3 with h2 | h2 <;> simp [h1, h2]

theorem sq_mod_three_eq_one {a : ℕ} (ha : a % 3 ≠ 0) : (a * a) % 3 = 1 := by
  rw [Nat.mul_mod]
  have ha3 : a % 3 = 1 ∨ a % 3 = 2 := by omega
  rcases ha3 with h1 | h1 <;> simp [h1]

theorem mod_three_eq_of_mul_eq {a b c d : ℕ} (hb : b % 3 ≠ 0) (hd : d % 3 ≠ 0)
    (heq : a * b = c * d) : (a * d) % 3 = (c * b) % 3 := by
  have hb3 : b % 3 = 1 ∨ b % 3 = 2 := by omega
  have hd3 : d % 3 = 1 ∨ d % 3 = 2 := by omega
  have ha3 : a % 3 = 0 ∨ a % 3 = 1 ∨ a % 3 = 2 := by omega
  have hc3 : c % 3 = 0 ∨ c % 3 = 1 ∨ c % 3 = 2 := by omega
  have hmod : (a * b) % 3 = (c * d) % 3 := congrArg (· % 3) heq
  rw [Nat.mul_mod a b, Nat.mul_mod c d] at hmod
  rw [Nat.mul_mod a d, Nat.mul_mod c b]
  rcases ha3 with ha | ha | ha <;> rcases hb3 with hb | hb <;>
    rcases hc3 with hc | hc | hc <;> rcases hd3 with hd | hd <;>
    simp [ha, hb, hc, hd] at hmod ⊢

theorem v3Nat_p3PartNat_mul {m k : ℕ} (hm : 0 < m) (hk : 0 < k) :
    v3Nat (m * k) = v3Nat m + v3Nat k ∧
    p3PartNat (m * k) = p3PartNat m * p3PartNat k := by
  apply v3Nat_p3PartNat_eq_of_pow_mul
    (mul_mod_three_ne_zero (p3PartNat_mod_three_ne_zero hm) (p3PartNat_mod_three_ne_zero hk))
  calc
    3 ^ (v3Nat m + v3Nat k) * (p3PartNat m * p3PartNat k)
        = (3 ^ v3Nat m * p3PartNat m) * (3 ^ v3Nat k * p3PartNat k) := by ring
    _ = m * k := by rw [v3Nat_spec m, v3Nat_spec k]

theorem v3Nat_add_of_lt {X Y : ℕ} (hX : 0 < X) (_hY : 0 < Y) (hlt : v3Nat X < v3Nat Y) :
    v3Nat (X + Y) = v3Nat X ∧ p3PartNat (X + Y) % 3 = p3PartNat X % 3 := by
  let d := v3Nat Y - v3Nat X - 1
  have hb : v3Nat Y = v3Nat X + (d + 1) := by omega
  let m := p3PartNat X + 3 ^ (d + 1) * p3PartNat Y
  have hm_mod : m % 3 = p3PartNat X % 3 := by
    have hpow : (3 ^ (d + 1) * p3PartNat Y) % 3 = 0 := by
      have h1 : 3 ^ (d + 1) * p3PartNat Y = 3 * (3 ^ d * p3PartNat Y) := by ring
      rw [h1, Nat.mul_mod_right]
    omega
  have hm_ne : m % 3 ≠ 0 := by
    rw [hm_mod]
    exact p3PartNat_mod_three_ne_zero hX
  have heq : 3 ^ v3Nat X * m = X + Y := by
    calc
      3 ^ v3Nat X * m
          = 3 ^ v3Nat X * p3PartNat X + 3 ^ (v3Nat X + (d + 1)) * p3PartNat Y := by
            simp only [m, pow_add]; ring
      _ = 3 ^ v3Nat X * p3PartNat X + 3 ^ v3Nat Y * p3PartNat Y := by rw [← hb]
      _ = X + Y := by rw [v3Nat_spec X, v3Nat_spec Y]
  obtain ⟨hv, hp⟩ := v3Nat_p3PartNat_eq_of_pow_mul hm_ne heq
  exact ⟨hv, by rw [hp, hm_mod]⟩

theorem v3Nat_add_gt_imp_eq_and_mod_three {X Y : ℕ} (hX : 0 < X) (hY : 0 < Y)
    (hgt : v3Nat X < v3Nat (X + Y)) :
    v3Nat X = v3Nat Y ∧ (p3PartNat X + p3PartNat Y) % 3 = 0 := by
  have heq_v : v3Nat X = v3Nat Y := by
    rcases lt_trichotomy (v3Nat X) (v3Nat Y) with hlt | heq | hlt
    · have h1 := (v3Nat_add_of_lt hX hY hlt).1
      omega
    · exact heq
    · have h1 := (v3Nat_add_of_lt hY hX hlt).1
      rw [Nat.add_comm Y X] at h1
      omega
  refine ⟨heq_v, ?_⟩
  by_contra hmod
  have heq_sum : 3 ^ v3Nat X * (p3PartNat X + p3PartNat Y) = X + Y := by
    calc
      3 ^ v3Nat X * (p3PartNat X + p3PartNat Y)
          = 3 ^ v3Nat X * p3PartNat X + 3 ^ v3Nat Y * p3PartNat Y := by
            rw [← heq_v]; ring
      _ = X + Y := by rw [v3Nat_spec X, v3Nat_spec Y]
  have hv := (v3Nat_p3PartNat_eq_of_pow_mul hmod heq_sum).1
  omega

theorem v3Nat_add_ge_min {X Y : ℕ} (hX : 0 < X) (hY : 0 < Y) :
    min (v3Nat X) (v3Nat Y) ≤ v3Nat (X + Y) := by
  rcases lt_trichotomy (v3Nat X) (v3Nat Y) with hlt | heq | hlt
  · have h1 := (v3Nat_add_of_lt hX hY hlt).1
    omega
  · have hsum_pos : 0 < p3PartNat X + p3PartNat Y := by
      have hpX := p3PartNat_pos hX
      omega
    have hpow_pos : 0 < 3 ^ v3Nat X := pow_pos (by decide : 0 < 3) (v3Nat X)
    have heq_sum : X + Y = 3 ^ v3Nat X * (p3PartNat X + p3PartNat Y) := by
      calc
        X + Y = 3 ^ v3Nat X * p3PartNat X + 3 ^ v3Nat Y * p3PartNat Y := by
          rw [v3Nat_spec X, v3Nat_spec Y]
        _ = 3 ^ v3Nat X * (p3PartNat X + p3PartNat Y) := by
          rw [← heq]; ring
    have hv_pow : v3Nat (3 ^ v3Nat X) = v3Nat X := by
      exact (v3Nat_p3PartNat_eq_of_pow_mul (m := 1) (by decide) (by ring)).1
    have hv_mul := (v3Nat_p3PartNat_mul hpow_pos hsum_pos).1
    rw [heq_sum, hv_mul, hv_pow]
    omega
  · have h1 := (v3Nat_add_of_lt hY hX hlt).1
    rw [Nat.add_comm Y X] at h1
    omega

theorem sq_add_sq_mod_three_eq_zero_iff (x y : ℕ) :
    (x ^ 2 + y ^ 2) % 3 = 0 ↔ x % 3 = 0 ∧ y % 3 = 0 := by
  simp only [sq]
  rw [Nat.add_mod, Nat.mul_mod x x, Nat.mul_mod y y]
  have hx : x % 3 = 0 ∨ x % 3 = 1 ∨ x % 3 = 2 := by omega
  have hy : y % 3 = 0 ∨ y % 3 = 1 ∨ y % 3 = 2 := by omega
  rcases hx with hx | hx | hx <;> rcases hy with hy | hy | hy <;> simp [hx, hy]

theorem v3Nat_sq_add_sq_even (x y : ℕ) : v3Nat (x ^ 2 + y ^ 2) % 2 = 0 := by
  have hmain : ∀ s : ℕ, ∀ a b : ℕ, a + b = s → v3Nat (a ^ 2 + b ^ 2) % 2 = 0 := by
    intro s
    induction s using Nat.strong_induction_on with
    | h s ih =>
      intro a b hab
      by_cases h0 : a = 0 ∧ b = 0
      · rcases h0 with ⟨rfl, rfl⟩
        rfl
      · have hpos : 0 < a ^ 2 + b ^ 2 := by
          rcases not_and_or.mp h0 with ha | hb
          · have : 0 < a := by omega
            nlinarith
          · have : 0 < b := by omega
            nlinarith
        by_cases hmod : (a ^ 2 + b ^ 2) % 3 = 0
        · obtain ⟨ha3, hb3⟩ := (sq_add_sq_mod_three_eq_zero_iff a b).mp hmod
          have ha_eq : a = 3 * (a / 3) := (Nat.mul_div_cancel' (Nat.dvd_of_mod_eq_zero ha3)).symm
          have hb_eq : b = 3 * (b / 3) := (Nat.mul_div_cancel' (Nat.dvd_of_mod_eq_zero hb3)).symm
          have hsub_pos : 0 < (a / 3) ^ 2 + (b / 3) ^ 2 := by nlinarith
          have hsq_eq : a ^ 2 + b ^ 2 = 9 * ((a / 3) ^ 2 + (b / 3) ^ 2) := by
            calc
              a ^ 2 + b ^ 2 = (3 * (a / 3)) ^ 2 + (3 * (b / 3)) ^ 2 := by
                rw [← ha_eq, ← hb_eq]
              _ = 9 * ((a / 3) ^ 2 + (b / 3) ^ 2) := by ring
          have hv9 : v3Nat 9 = 2 := rfl
          have hmul := (v3Nat_p3PartNat_mul (by decide : 0 < 9) hsub_pos).1
          have hlt_s : a / 3 + b / 3 < s := by omega
          have hrec := ih (a / 3 + b / 3) hlt_s (a / 3) (b / 3) rfl
          rw [hsq_eq, hmul, hv9]
          omega
        · have hv0 :=
            (v3Nat_p3PartNat_eq_of_pow_mul (n := a ^ 2 + b ^ 2) (a := 0) (m := a ^ 2 + b ^ 2)
              hmod (by ring)).1
          rw [hv0]
  exact hmain (x + y) x y rfl

/-- `3`-adic valuation of a positive rational `q` (`0` if `q ≤ 0`). -/
def v3Rat (q : ℚ) : ℤ :=
  if 0 < q then (v3Nat q.num.natAbs : ℤ) - (v3Nat q.den : ℤ) else 0

/-- `3`-adic unit residue sign `∈ {-1, 1}` of a positive rational `q` (`0` if `q ≤ 0`). -/
def u3Rat (q : ℚ) : ℚ :=
  if 0 < q then
    if (p3PartNat q.num.natAbs * p3PartNat q.den) % 3 = 1 then 1 else -1
  else 0

theorem rat_pos_eq_natAbs_div_den {q : ℚ} (hq : 0 < q) :
    0 < q.num.natAbs ∧ 0 < q.den ∧ q = (q.num.natAbs : ℚ) / (q.den : ℚ) := by
  have hnum_pos : 0 < q.num := Rat.num_pos.mpr hq
  have hnat_pos : 0 < q.num.natAbs := Int.natAbs_pos.mpr (ne_of_gt hnum_pos)
  have hden_pos : 0 < q.den := q.den_pos
  have hint : (q.num.natAbs : ℤ) = q.num := Int.natAbs_of_nonneg (le_of_lt hnum_pos)
  have hcast : (q.num.natAbs : ℚ) = (q.num : ℚ) := by
    simpa using congrArg (Int.cast : ℤ → ℚ) hint
  refine ⟨hnat_pos, hden_pos, ?_⟩
  rw [hcast, Rat.num_div_den]

theorem v3Rat_u3Rat_of_nat_div {q : ℚ} {n d : ℕ} (hn : 0 < n) (hd : 0 < d)
    (hq : q = (n : ℚ) / (d : ℚ)) :
    0 < q ∧
    v3Rat q = (v3Nat n : ℤ) - (v3Nat d : ℤ) ∧
    u3Rat q = (if (p3PartNat n * p3PartNat d) % 3 = 1 then 1 else -1) := by
  have hn_q : 0 < (n : ℚ) := by exact_mod_cast hn
  have hd_q : 0 < (d : ℚ) := by exact_mod_cast hd
  have hq_pos : 0 < q := by
    rw [hq]
    exact div_pos hn_q hd_q
  obtain ⟨hnum_pos, hden_pos, hq_can⟩ := rat_pos_eq_natAbs_div_den hq_pos
  have hden_q : (q.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hden_pos)
  have hd_ne : (d : ℚ) ≠ 0 := ne_of_gt hd_q
  have hcross_q : (q.num.natAbs : ℚ) * (d : ℚ) = (n : ℚ) * (q.den : ℚ) := by
    have heq_div : (q.num.natAbs : ℚ) / (q.den : ℚ) = (n : ℚ) / (d : ℚ) :=
      hq_can.symm.trans hq
    exact (div_eq_div_iff hden_q hd_ne).mp heq_div
  have hcross : q.num.natAbs * d = n * q.den := by
    exact_mod_cast hcross_q
  obtain ⟨hv1, hp1⟩ := v3Nat_p3PartNat_mul hnum_pos hd
  obtain ⟨hv2, hp2⟩ := v3Nat_p3PartNat_mul hn hden_pos
  have hv_eq : v3Nat q.num.natAbs + v3Nat d = v3Nat n + v3Nat q.den := by
    rw [← hv1, ← hv2, hcross]
  have hp_eq : p3PartNat q.num.natAbs * p3PartNat d = p3PartNat n * p3PartNat q.den := by
    rw [← hp1, ← hp2, hcross]
  have hmod_eq :
      (p3PartNat q.num.natAbs * p3PartNat q.den) % 3 = (p3PartNat n * p3PartNat d) % 3 :=
    mod_three_eq_of_mul_eq (p3PartNat_mod_three_ne_zero hd)
      (p3PartNat_mod_three_ne_zero hden_pos) hp_eq
  refine ⟨hq_pos, ?_, ?_⟩
  · simp only [v3Rat, hq_pos, ↓reduceIte]
    omega
  · simp only [u3Rat, hq_pos, ↓reduceIte, hmod_eq]

theorem v3Rat_natCast {n : ℕ} (hn : 0 < n) : v3Rat (n : ℚ) = (v3Nat n : ℤ) := by
  have h :=
    (v3Rat_u3Rat_of_nat_div (q := (n : ℚ)) (n := n) (d := 1) hn (by decide : 0 < 1) (by simp)).2.1
  have hv1 : v3Nat 1 = 0 := rfl
  omega

theorem u3Rat_natCast {n : ℕ} (hn : 0 < n) :
    u3Rat (n : ℚ) = if p3PartNat n % 3 = 1 then 1 else -1 := by
  have h :=
    (v3Rat_u3Rat_of_nat_div (q := (n : ℚ)) (n := n) (d := 1) hn (by decide : 0 < 1) (by simp)).2.2
  have hp1 : p3PartNat 1 = 1 := rfl
  simp [h, hp1]

theorem u3Rat_values_of_pos {q : ℚ} (hq : 0 < q) : u3Rat q = 1 ∨ u3Rat q = -1 := by
  simp only [u3Rat, hq, ↓reduceIte]
  split_ifs with h
  · exact Or.inl rfl
  · exact Or.inr rfl

theorem u3Rat_sq_of_pos {q : ℚ} (hq : 0 < q) : u3Rat q * u3Rat q = 1 := by
  rcases u3Rat_values_of_pos hq with h | h <;> rw [h] <;> ring

theorem u3Rat_ne_zero_of_pos {q : ℚ} (hq : 0 < q) : u3Rat q ≠ 0 := by
  rcases u3Rat_values_of_pos hq with h | h <;> rw [h] <;> norm_num

theorem v3Rat_mul {p q : ℚ} (hp : 0 < p) (hq : 0 < q) :
    v3Rat (p * q) = v3Rat p + v3Rat q := by
  obtain ⟨hnp, hdp, hp_eq⟩ := rat_pos_eq_natAbs_div_den hp
  obtain ⟨hnq, hdq, hq_eq⟩ := rat_pos_eq_natAbs_div_den hq
  have hmul_eq : p * q = ((p.num.natAbs * q.num.natAbs : ℕ) : ℚ) / ((p.den * q.den : ℕ) : ℚ) := by
    push_cast
    rw [← div_mul_div_comm, ← hp_eq, ← hq_eq]
  have hvpq := (v3Rat_u3Rat_of_nat_div (Nat.mul_pos hnp hnq) (Nat.mul_pos hdp hdq) hmul_eq).2.1
  have hvp := (v3Rat_u3Rat_of_nat_div hnp hdp hp_eq).2.1
  have hvq := (v3Rat_u3Rat_of_nat_div hnq hdq hq_eq).2.1
  have hvn := (v3Nat_p3PartNat_mul hnp hnq).1
  have hvd := (v3Nat_p3PartNat_mul hdp hdq).1
  rw [hvpq, hvp, hvq, hvn, hvd]
  omega

theorem u3Rat_mul {p q : ℚ} (hp : 0 < p) (hq : 0 < q) :
    u3Rat (p * q) = u3Rat p * u3Rat q := by
  obtain ⟨hnp, hdp, hp_eq⟩ := rat_pos_eq_natAbs_div_den hp
  obtain ⟨hnq, hdq, hq_eq⟩ := rat_pos_eq_natAbs_div_den hq
  have hmul_eq : p * q = ((p.num.natAbs * q.num.natAbs : ℕ) : ℚ) / ((p.den * q.den : ℕ) : ℚ) := by
    push_cast
    rw [← div_mul_div_comm, ← hp_eq, ← hq_eq]
  have hupq := (v3Rat_u3Rat_of_nat_div (Nat.mul_pos hnp hnq) (Nat.mul_pos hdp hdq) hmul_eq).2.2
  have hup := (v3Rat_u3Rat_of_nat_div hnp hdp hp_eq).2.2
  have huq := (v3Rat_u3Rat_of_nat_div hnq hdq hq_eq).2.2
  have hpn := (v3Nat_p3PartNat_mul hnp hnq).2
  have hpd := (v3Nat_p3PartNat_mul hdp hdq).2
  rw [hupq, hup, huq, hpn, hpd]
  have hmp_ne : (p3PartNat p.num.natAbs * p3PartNat p.den) % 3 ≠ 0 :=
    mul_mod_three_ne_zero (p3PartNat_mod_three_ne_zero hnp) (p3PartNat_mod_three_ne_zero hdp)
  have hmq_ne : (p3PartNat q.num.natAbs * p3PartNat q.den) % 3 ≠ 0 :=
    mul_mod_three_ne_zero (p3PartNat_mod_three_ne_zero hnq) (p3PartNat_mod_three_ne_zero hdq)
  have hcomm :
      p3PartNat p.num.natAbs * p3PartNat q.num.natAbs * (p3PartNat p.den * p3PartNat q.den) =
      (p3PartNat p.num.natAbs * p3PartNat p.den) * (p3PartNat q.num.natAbs * p3PartNat q.den) := by
    ring
  rw [hcomm, Nat.mul_mod]
  have hmp3 :
      (p3PartNat p.num.natAbs * p3PartNat p.den) % 3 = 1 ∨
      (p3PartNat p.num.natAbs * p3PartNat p.den) % 3 = 2 := by omega
  have hmq3 :
      (p3PartNat q.num.natAbs * p3PartNat q.den) % 3 = 1 ∨
      (p3PartNat q.num.natAbs * p3PartNat q.den) % 3 = 2 := by omega
  rcases hmp3 with h1 | h1 <;> rcases hmq3 with h2 | h2 <;> simp [h1, h2]

theorem v3Rat_add_of_lt {p q : ℚ} (hp : 0 < p) (hq : 0 < q) (hlt : v3Rat p < v3Rat q) :
    v3Rat (p + q) = v3Rat p ∧ u3Rat (p + q) = u3Rat p := by
  obtain ⟨hnp, hdp, hp_eq⟩ := rat_pos_eq_natAbs_div_den hp
  obtain ⟨hnq, hdq, hq_eq⟩ := rat_pos_eq_natAbs_div_den hq
  let X := p.num.natAbs * q.den
  let Y := q.num.natAbs * p.den
  let D := p.den * q.den
  have hX : 0 < X := Nat.mul_pos hnp hdq
  have hY : 0 < Y := Nat.mul_pos hnq hdp
  have hD : 0 < D := Nat.mul_pos hdp hdq
  have hp_D : p = (X : ℚ) / (D : ℚ) := by
    have hdq_ne : (q.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdq)
    simp only [X, D, Nat.cast_mul]
    rw [mul_div_mul_right _ _ hdq_ne, ← hp_eq]
  have hq_D : q = (Y : ℚ) / (D : ℚ) := by
    have hdp_ne : (p.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdp)
    simp only [Y, D, Nat.cast_mul]
    rw [mul_comm (p.den : ℚ) (q.den : ℚ), mul_div_mul_right _ _ hdp_ne, ← hq_eq]
  have hpq_D : p + q = ((X + Y : ℕ) : ℚ) / (D : ℚ) := by
    rw [hp_D, hq_D, Nat.cast_add, add_div]
  obtain ⟨_, hvp, hup⟩ := v3Rat_u3Rat_of_nat_div hX hD hp_D
  obtain ⟨_, hvq, _⟩ := v3Rat_u3Rat_of_nat_div hY hD hq_D
  obtain ⟨_, hvpq, hupq⟩ := v3Rat_u3Rat_of_nat_div (Nat.add_pos_left hX Y) hD hpq_D
  have hlt_nat : v3Nat X < v3Nat Y := by omega
  obtain ⟨hv_add, hp_add⟩ := v3Nat_add_of_lt hX hY hlt_nat
  refine ⟨by omega, ?_⟩
  rw [hupq, hup]
  have hmod_mul : (p3PartNat (X + Y) * p3PartNat D) % 3 = (p3PartNat X * p3PartNat D) % 3 := by
    rw [Nat.mul_mod, hp_add, ← Nat.mul_mod]
  rw [hmod_mul]

theorem v3Rat_add_gt_imp_eq_and_u3Rat_cancel {p q : ℚ} (hp : 0 < p) (hq : 0 < q)
    (hgt : v3Rat p < v3Rat (p + q)) :
    v3Rat p = v3Rat q ∧ u3Rat p + u3Rat q = 0 := by
  obtain ⟨hnp, hdp, hp_eq⟩ := rat_pos_eq_natAbs_div_den hp
  obtain ⟨hnq, hdq, hq_eq⟩ := rat_pos_eq_natAbs_div_den hq
  let X := p.num.natAbs * q.den
  let Y := q.num.natAbs * p.den
  let D := p.den * q.den
  have hX : 0 < X := Nat.mul_pos hnp hdq
  have hY : 0 < Y := Nat.mul_pos hnq hdp
  have hD : 0 < D := Nat.mul_pos hdp hdq
  have hp_D : p = (X : ℚ) / (D : ℚ) := by
    have hdq_ne : (q.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdq)
    simp only [X, D, Nat.cast_mul]
    rw [mul_div_mul_right _ _ hdq_ne, ← hp_eq]
  have hq_D : q = (Y : ℚ) / (D : ℚ) := by
    have hdp_ne : (p.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdp)
    simp only [Y, D, Nat.cast_mul]
    rw [mul_comm (p.den : ℚ) (q.den : ℚ), mul_div_mul_right _ _ hdp_ne, ← hq_eq]
  have hpq_D : p + q = ((X + Y : ℕ) : ℚ) / (D : ℚ) := by
    rw [hp_D, hq_D, Nat.cast_add, add_div]
  obtain ⟨_, hvp, hup⟩ := v3Rat_u3Rat_of_nat_div hX hD hp_D
  obtain ⟨_, hvq, huq⟩ := v3Rat_u3Rat_of_nat_div hY hD hq_D
  obtain ⟨_, hvpq, _⟩ := v3Rat_u3Rat_of_nat_div (Nat.add_pos_left hX Y) hD hpq_D
  have hgt_nat : v3Nat X < v3Nat (X + Y) := by omega
  obtain ⟨hv_eq, hp_sum⟩ := v3Nat_add_gt_imp_eq_and_mod_three hX hY hgt_nat
  refine ⟨by omega, ?_⟩
  rw [hup, huq]
  have hpX_ne := p3PartNat_mod_three_ne_zero hX
  have hpY_ne := p3PartNat_mod_three_ne_zero hY
  have hpD_ne := p3PartNat_mod_three_ne_zero hD
  have hpX3 : p3PartNat X % 3 = 1 ∨ p3PartNat X % 3 = 2 := by omega
  have hpY3 : p3PartNat Y % 3 = 1 ∨ p3PartNat Y % 3 = 2 := by omega
  have hpD3 : p3PartNat D % 3 = 1 ∨ p3PartNat D % 3 = 2 := by omega
  rw [Nat.add_mod] at hp_sum
  rw [Nat.mul_mod (p3PartNat X), Nat.mul_mod (p3PartNat Y)]
  rcases hpX3 with hx | hx <;> rcases hpY3 with hy | hy <;> rcases hpD3 with hd | hd <;>
    simp [hx, hy, hd] at hp_sum ⊢

theorem v3Rat_add_ge_min {p q : ℚ} (hp : 0 < p) (hq : 0 < q) :
    min (v3Rat p) (v3Rat q) ≤ v3Rat (p + q) := by
  obtain ⟨hnp, hdp, hp_eq⟩ := rat_pos_eq_natAbs_div_den hp
  obtain ⟨hnq, hdq, hq_eq⟩ := rat_pos_eq_natAbs_div_den hq
  let X := p.num.natAbs * q.den
  let Y := q.num.natAbs * p.den
  let D := p.den * q.den
  have hX : 0 < X := Nat.mul_pos hnp hdq
  have hY : 0 < Y := Nat.mul_pos hnq hdp
  have hD : 0 < D := Nat.mul_pos hdp hdq
  have hp_D : p = (X : ℚ) / (D : ℚ) := by
    have hdq_ne : (q.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdq)
    simp only [X, D, Nat.cast_mul]
    rw [mul_div_mul_right _ _ hdq_ne, ← hp_eq]
  have hq_D : q = (Y : ℚ) / (D : ℚ) := by
    have hdp_ne : (p.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdp)
    simp only [Y, D, Nat.cast_mul]
    rw [mul_comm (p.den : ℚ) (q.den : ℚ), mul_div_mul_right _ _ hdp_ne, ← hq_eq]
  have hpq_D : p + q = ((X + Y : ℕ) : ℚ) / (D : ℚ) := by
    rw [hp_D, hq_D, Nat.cast_add, add_div]
  obtain ⟨_, hvp, _⟩ := v3Rat_u3Rat_of_nat_div hX hD hp_D
  obtain ⟨_, hvq, _⟩ := v3Rat_u3Rat_of_nat_div hY hD hq_D
  obtain ⟨_, hvpq, _⟩ := v3Rat_u3Rat_of_nat_div (Nat.add_pos_left hX Y) hD hpq_D
  have hmin := v3Nat_add_ge_min hX hY
  omega

theorem rat_sq_eq_natAbs_sq_div_den_sq (r : ℚ) :
    r ^ 2 = ((r.num.natAbs ^ 2 : ℕ) : ℚ) / ((r.den * r.den : ℕ) : ℚ) := by
  have hnum_sq : (r.num.natAbs : ℚ) * (r.num.natAbs : ℚ) = (r.num : ℚ) * (r.num : ℚ) := by
    rcases le_total 0 r.num with h | h
    · have h1 : (r.num.natAbs : ℤ) = r.num := Int.natAbs_of_nonneg h
      have hq : (r.num.natAbs : ℚ) = (r.num : ℚ) := by
        simpa using congrArg (Int.cast : ℤ → ℚ) h1
      rw [hq]
    · have h1 : (r.num.natAbs : ℤ) = -r.num := by omega
      have hq : (r.num.natAbs : ℚ) = -(r.num : ℚ) := by
        simpa using congrArg (Int.cast : ℤ → ℚ) h1
      rw [hq]
      ring
  have hdiv := (Rat.num_div_den r).symm
  push_cast
  rw [sq r, sq (r.num.natAbs : ℚ), hnum_sq, ← div_mul_div_comm, ← hdiv]

theorem v3Rat_normSq_even (z : GaussRat) : v3Rat z.normSq % 2 = 0 := by
  by_cases hpos : 0 < z.normSq
  · let X := z.re.num.natAbs * z.im.den
    let Y := z.im.num.natAbs * z.re.den
    let D := z.re.den * z.im.den
    have hD1 : 0 < D := Nat.mul_pos z.re.den_pos z.im.den_pos
    have hD_pos : 0 < D * D := Nat.mul_pos hD1 hD1
    have hre_den_sq_ne : ((z.re.den * z.re.den : ℕ) : ℚ) ≠ 0 :=
      ne_of_gt (by exact_mod_cast Nat.mul_pos z.re.den_pos z.re.den_pos)
    have him_den_sq_ne : ((z.im.den * z.im.den : ℕ) : ℚ) ≠ 0 :=
      ne_of_gt (by exact_mod_cast Nat.mul_pos z.im.den_pos z.im.den_pos)
    have hnorm_eq : z.normSq = ((X ^ 2 + Y ^ 2 : ℕ) : ℚ) / ((D * D : ℕ) : ℚ) := by
      simp only [GaussRat.normSq]
      rw [rat_sq_eq_natAbs_sq_div_den_sq z.re, rat_sq_eq_natAbs_sq_div_den_sq z.im,
        div_add_div _ _ hre_den_sq_ne him_den_sq_ne]
      simp only [X, Y, D]
      push_cast
      ring
    have hXY_pos : 0 < X ^ 2 + Y ^ 2 := by
      by_contra hle
      have h0 : X ^ 2 + Y ^ 2 = 0 := by omega
      rw [h0] at hnorm_eq
      simp at hnorm_eq
      linarith
    have hv := (v3Rat_u3Rat_of_nat_div hXY_pos hD_pos hnorm_eq).2.1
    have hvD := (v3Nat_p3PartNat_mul hD1 hD1).1
    have heven := v3Nat_sq_add_sq_even X Y
    rw [hv, hvD]
    omega
  · simp only [v3Rat, hpos, ↓reduceIte]
    rfl

theorem four_term_v3Rat_cancel {A B C D : ℚ}
    (hA : 0 < A) (hB_nn : 0 ≤ B) (hC_nn : 0 ≤ C) (_hD : 0 < D)
    (hsum : A + B + C = D)
    (hA_odd : v3Rat A % 2 ≠ 0)
    (hB_odd : 0 < B → v3Rat B % 2 ≠ 0)
    (hC_even : v3Rat C % 2 = 0)
    (hlt_D : v3Rat A < v3Rat D) :
    0 < B ∧ v3Rat A = v3Rat B ∧ u3Rat A + u3Rat B = 0 := by
  have hAB_pos : 0 < A + B := by linarith
  have hAB_gt : v3Rat A < v3Rat (A + B) := by
    by_contra hle
    have hle' : v3Rat (A + B) ≤ v3Rat A := not_lt.mp hle
    have hAB_odd : v3Rat (A + B) % 2 ≠ 0 := by
      rcases eq_or_lt_of_le hB_nn with rfl | hB_pos
      · simp [hA_odd]
      · rcases lt_or_ge (v3Rat B) (v3Rat A) with hlt_BA | hge_BA
        · have hvBA := (v3Rat_add_of_lt hB_pos hA hlt_BA).1
          rw [add_comm] at hvBA
          rw [hvBA]
          exact hB_odd hB_pos
        · have hmin := v3Rat_add_ge_min hA hB_pos
          have heq_AB : v3Rat (A + B) = v3Rat A := by omega
          rw [heq_AB]
          exact hA_odd
    have hAB_lt_D : v3Rat (A + B) < v3Rat (A + B + C) := by
      rw [hsum]
      omega
    rcases eq_or_lt_of_le hC_nn with rfl | hC_pos
    · simp at hAB_lt_D
    · have hv_eq := (v3Rat_add_gt_imp_eq_and_u3Rat_cancel hAB_pos hC_pos hAB_lt_D).1
      omega
  rcases eq_or_lt_of_le hB_nn with rfl | hB_pos
  · simp at hAB_gt
  · obtain ⟨hv_eq, hu_sum⟩ := v3Rat_add_gt_imp_eq_and_u3Rat_cancel hA hB_pos hAB_gt
    exact ⟨hB_pos, hv_eq, hu_sum⟩

/-- Determinant of three vectors in `ℚ(i)³`. -/
def detGVec (u v w : GVec) : GaussRat :=
  u.x * (v.y * w.z - v.z * w.y) -
  u.y * (v.x * w.z - v.z * w.x) +
  u.z * (v.x * w.y - v.y * w.x)

theorem detGVec_normSq_of_frame {u v w : GVec} (hf : IsFrame u v w) :
    (detGVec u v w).normSq = normSqVec u * normSqVec v * normSqVec w := by
  obtain ⟨_, _, _, huv, huw, hvw⟩ := hf
  have hvu := inner_eq_zero_symm huv
  have hwu := inner_eq_zero_symm huw
  have hwv := inner_eq_zero_symm hvw
  have id_det :
      star (detGVec u v w) * detGVec u v w =
      GVec.inner u u * (GVec.inner v v * GVec.inner w w - GVec.inner v w * GVec.inner w v) -
      GVec.inner u v * (GVec.inner v u * GVec.inner w w - GVec.inner v w * GVec.inner w u) +
      GVec.inner u w * (GVec.inner v u * GVec.inner w v - GVec.inner v v * GVec.inner w u) := by
    simp only [detGVec, GVec.inner, star_add, star_sub, star_mul]
    ring
  rw [huv, huw, hvw, hvu, hwu, hwv] at id_det
  have hre := congrArg GaussRat.re id_det
  rw [GaussRat.re_star_mul_self, inner_self_eq_normSqVec u, inner_self_eq_normSqVec v,
    inner_self_eq_normSqVec w] at hre
  simp only [GaussRat.re_add, GaussRat.re_sub, GaussRat.re_mul,
    GaussRat.im_sub, GaussRat.im_mul,
    GaussRat.re_zero, GaussRat.im_zero] at hre
  linarith

theorem frame_v3Rat_sum_even {u v w : GVec} (hf : IsFrame u v w) :
    (v3Rat (normSqVec u) + v3Rat (normSqVec v) + v3Rat (normSqVec w)) % 2 = 0 := by
  have hu := normSqVec_pos_of_nonZero hf.1
  have hv := normSqVec_pos_of_nonZero hf.2.1
  have hw := normSqVec_pos_of_nonZero hf.2.2.1
  have hdet := detGVec_normSq_of_frame hf
  have hmul1 := v3Rat_mul (mul_pos hu hv) hw
  have hmul2 := v3Rat_mul hu hv
  have heven := v3Rat_normSq_even (detGVec u v w)
  rw [hdet, hmul1, hmul2] at heven
  exact heven

theorem ortho_coord_identity_x {u v : GVec} (huv : GVec.inner u v = 0) :
    u.x.normSq * normSqVec v + v.x.normSq * normSqVec u +
      (u.y * v.z - v.y * u.z).normSq = normSqVec u * normSqVec v := by
  have hre : (GVec.inner u v).re = 0 := by rw [huv]; rfl
  have him : (GVec.inner u v).im = 0 := by rw [huv]; rfl
  have hns : (GVec.inner u v).normSq = 0 := by
    rw [huv]
    exact (GaussRat.normSq_eq_zero_iff 0).mpr rfl
  have hid :
      u.x.normSq * normSqVec v + v.x.normSq * normSqVec u +
        (u.y * v.z - v.y * u.z).normSq - normSqVec u * normSqVec v =
      2 * (u.x.re * v.x.re + u.x.im * v.x.im) * (GVec.inner u v).re +
      2 * (u.x.re * v.x.im - u.x.im * v.x.re) * (GVec.inner u v).im -
      (GVec.inner u v).normSq := by
    simp only [GVec.inner, normSqVec, GaussRat.normSq,
      GaussRat.re_add, GaussRat.im_add, GaussRat.re_sub, GaussRat.im_sub,
      GaussRat.re_mul, GaussRat.im_mul, GaussRat.re_star, GaussRat.im_star]
    ring
  rw [hre, him, hns] at hid
  linarith

theorem normSqVec_rotVec (u : GVec) : normSqVec (rotVec u) = normSqVec u := by
  simp only [normSqVec, rotVec]
  ring

/-- Whether a coordinate `z : GaussRat` is `3`-leading in `u : GVec`. -/
def isLead3Coord (z : GaussRat) (u : GVec) : Prop :=
  0 < z.normSq ∧ v3Rat z.normSq < v3Rat (normSqVec u)

instance (z : GaussRat) (u : GVec) : Decidable (isLead3Coord z u) :=
  inferInstanceAs (Decidable (0 < z.normSq ∧ v3Rat z.normSq < v3Rat (normSqVec u)))

/-- The `3`-adic contribution `u3Rat z.normSq * u3Rat (normSqVec u)` of a coordinate `z` in `u`. -/
def coordSign3 (z : GaussRat) (u : GVec) : ℚ :=
  u3Rat z.normSq * u3Rat (normSqVec u)

/-- Explicit global `{-1, 0, 1}`-valued `3`-adic frame residual on `ℚ(i)³`. -/
def s3 (u : GVec) : ℚ :=
  if v3Rat (normSqVec u) % 2 = 0 then 0
  else if isLead3Coord u.x u then coordSign3 u.x u
  else if isLead3Coord u.y u then coordSign3 u.y u
  else coordSign3 u.z u

theorem pos_of_v3Rat_mod_two_ne_zero {q : ℚ} (h : v3Rat q % 2 ≠ 0) : 0 < q := by
  by_contra hle
  simp [v3Rat, hle] at h

theorem v3Rat_add_gt_of_nonneg {a b : ℚ} {V : ℤ}
    (ha_nn : 0 ≤ a) (hb_nn : 0 ≤ b)
    (ha : 0 < a → V < v3Rat a) (hb : 0 < b → V < v3Rat b)
    (hab : 0 < a + b) : V < v3Rat (a + b) := by
  rcases eq_or_lt_of_le ha_nn with rfl | ha_pos
  · simp at hab ⊢
    exact hb hab
  · rcases eq_or_lt_of_le hb_nn with rfl | hb_pos
    · simp at hab ⊢
      exact ha ha_pos
    · have h1 := ha ha_pos
      have h2 := hb hb_pos
      have hmin := v3Rat_add_ge_min ha_pos hb_pos
      omega

theorem exists_lead3Coord_of_odd {u : GVec} (hodd : v3Rat (normSqVec u) % 2 ≠ 0) :
    isLead3Coord u.x u ∨ isLead3Coord u.y u ∨ isLead3Coord u.z u := by
  by_contra hnot
  rcases not_or.mp hnot with ⟨hx_not, hyz_not⟩
  rcases not_or.mp hyz_not with ⟨hy_not, hz_not⟩
  have hpos : 0 < normSqVec u := pos_of_v3Rat_mod_two_ne_zero hodd
  have hx_gt : 0 < u.x.normSq → v3Rat (normSqVec u) < v3Rat u.x.normSq := by
    intro hx_pos
    have hnot_lt : ¬ v3Rat u.x.normSq < v3Rat (normSqVec u) := fun hlt => hx_not ⟨hx_pos, hlt⟩
    have heven := v3Rat_normSq_even u.x
    omega
  have hy_gt : 0 < u.y.normSq → v3Rat (normSqVec u) < v3Rat u.y.normSq := by
    intro hy_pos
    have hnot_lt : ¬ v3Rat u.y.normSq < v3Rat (normSqVec u) := fun hlt => hy_not ⟨hy_pos, hlt⟩
    have heven := v3Rat_normSq_even u.y
    omega
  have hz_gt : 0 < u.z.normSq → v3Rat (normSqVec u) < v3Rat u.z.normSq := by
    intro hz_pos
    have hnot_lt : ¬ v3Rat u.z.normSq < v3Rat (normSqVec u) := fun hlt => hz_not ⟨hz_pos, hlt⟩
    have heven := v3Rat_normSq_even u.z
    omega
  have hxy_gt : 0 < u.x.normSq + u.y.normSq →
      v3Rat (normSqVec u) < v3Rat (u.x.normSq + u.y.normSq) :=
    v3Rat_add_gt_of_nonneg (GaussRat.normSq_nonneg u.x) (GaussRat.normSq_nonneg u.y) hx_gt hy_gt
  have hxyz_gt : v3Rat (normSqVec u) < v3Rat (u.x.normSq + u.y.normSq + u.z.normSq) :=
    v3Rat_add_gt_of_nonneg
      (add_nonneg (GaussRat.normSq_nonneg u.x) (GaussRat.normSq_nonneg u.y))
      (GaussRat.normSq_nonneg u.z) hxy_gt hz_gt hpos
  change v3Rat (normSqVec u) < v3Rat (normSqVec u) at hxyz_gt
  omega

theorem lead3Coord_x_ortho_imp {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v3Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v3Rat (normSqVec v) % 2 ≠ 0)
    (hlead : isLead3Coord u.x u) :
    isLead3Coord v.x v ∧ coordSign3 u.x u + coordSign3 v.x v = 0 := by
  have hu_pos : 0 < normSqVec u := pos_of_v3Rat_mod_two_ne_zero hu_odd
  have hv_pos : 0 < normSqVec v := pos_of_v3Rat_mod_two_ne_zero hv_odd
  let A := u.x.normSq * normSqVec v
  let B := v.x.normSq * normSqVec u
  let C := (u.y * v.z - v.y * u.z).normSq
  let D := normSqVec u * normSqVec v
  have hA : 0 < A := mul_pos hlead.1 hv_pos
  have hB_nn : 0 ≤ B := mul_nonneg (GaussRat.normSq_nonneg v.x) (le_of_lt hu_pos)
  have hC_nn : 0 ≤ C := GaussRat.normSq_nonneg _
  have hD : 0 < D := mul_pos hu_pos hv_pos
  have hsum : A + B + C = D := ortho_coord_identity_x huv
  have hvA : v3Rat A = v3Rat u.x.normSq + v3Rat (normSqVec v) := v3Rat_mul hlead.1 hv_pos
  have hvD : v3Rat D = v3Rat (normSqVec u) + v3Rat (normSqVec v) := v3Rat_mul hu_pos hv_pos
  have hA_odd : v3Rat A % 2 ≠ 0 := by
    have heven := v3Rat_normSq_even u.x
    omega
  have hB_odd : 0 < B → v3Rat B % 2 ≠ 0 := by
    intro hB_pos
    have hvx_pos : 0 < v.x.normSq := by nlinarith
    have hvB : v3Rat B = v3Rat v.x.normSq + v3Rat (normSqVec u) := v3Rat_mul hvx_pos hu_pos
    have heven := v3Rat_normSq_even v.x
    omega
  have hC_even : v3Rat C % 2 = 0 := v3Rat_normSq_even _
  have hlt_D : v3Rat A < v3Rat D := by
    have hlt := hlead.2
    omega
  obtain ⟨hB_pos, hvAB, huAB⟩ :=
    four_term_v3Rat_cancel hA hB_nn hC_nn hD hsum hA_odd hB_odd hC_even hlt_D
  have hvx_pos : 0 < v.x.normSq := by nlinarith
  have hvB : v3Rat B = v3Rat v.x.normSq + v3Rat (normSqVec u) := v3Rat_mul hvx_pos hu_pos
  have hvx_lt : v3Rat v.x.normSq < v3Rat (normSqVec v) := by
    have hlt := hlead.2
    omega
  refine ⟨⟨hvx_pos, hvx_lt⟩, ?_⟩
  have huA : u3Rat A = u3Rat u.x.normSq * u3Rat (normSqVec v) := u3Rat_mul hlead.1 hv_pos
  have huB : u3Rat B = u3Rat v.x.normSq * u3Rat (normSqVec u) := u3Rat_mul hvx_pos hu_pos
  rw [huA, huB] at huAB
  have hsq_u := u3Rat_sq_of_pos hu_pos
  have hsq_v := u3Rat_sq_of_pos hv_pos
  simp only [coordSign3]
  linear_combination
    (u3Rat (normSqVec u) * u3Rat (normSqVec v)) * huAB -
    (u3Rat u.x.normSq * u3Rat (normSqVec u)) * hsq_v -
    (u3Rat v.x.normSq * u3Rat (normSqVec v)) * hsq_u

theorem lead3Coord_x_ortho_iff {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v3Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v3Rat (normSqVec v) % 2 ≠ 0) :
    isLead3Coord u.x u ↔ isLead3Coord v.x v :=
  ⟨fun h => (lead3Coord_x_ortho_imp huv hu_odd hv_odd h).1,
   fun h => (lead3Coord_x_ortho_imp (inner_eq_zero_symm huv) hv_odd hu_odd h).1⟩

theorem isLead3Coord_rotVec_x (u : GVec) :
    isLead3Coord (rotVec u).x (rotVec u) ↔ isLead3Coord u.y u := by
  unfold isLead3Coord
  rw [normSqVec_rotVec]
  rfl

theorem coordSign3_rotVec_x (u : GVec) :
    coordSign3 (rotVec u).x (rotVec u) = coordSign3 u.y u := by
  unfold coordSign3
  rw [normSqVec_rotVec]
  rfl

theorem isLead3Coord_rotVec_y (u : GVec) :
    isLead3Coord (rotVec u).y (rotVec u) ↔ isLead3Coord u.z u := by
  unfold isLead3Coord
  rw [normSqVec_rotVec]
  rfl

theorem coordSign3_rotVec_y (u : GVec) :
    coordSign3 (rotVec u).y (rotVec u) = coordSign3 u.z u := by
  unfold coordSign3
  rw [normSqVec_rotVec]
  rfl

theorem lead3Coord_y_ortho_imp {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v3Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v3Rat (normSqVec v) % 2 ≠ 0)
    (hlead : isLead3Coord u.y u) :
    isLead3Coord v.y v ∧ coordSign3 u.y u + coordSign3 v.y v = 0 := by
  have huv' : GVec.inner (rotVec u) (rotVec v) = 0 := by rw [inner_rotVec]; exact huv
  have hu_odd' : v3Rat (normSqVec (rotVec u)) % 2 ≠ 0 := by rw [normSqVec_rotVec]; exact hu_odd
  have hv_odd' : v3Rat (normSqVec (rotVec v)) % 2 ≠ 0 := by rw [normSqVec_rotVec]; exact hv_odd
  have hlead' : isLead3Coord (rotVec u).x (rotVec u) := (isLead3Coord_rotVec_x u).mpr hlead
  obtain ⟨hv_lead, hsum⟩ := lead3Coord_x_ortho_imp huv' hu_odd' hv_odd' hlead'
  rw [isLead3Coord_rotVec_x] at hv_lead
  rw [coordSign3_rotVec_x, coordSign3_rotVec_x] at hsum
  exact ⟨hv_lead, hsum⟩

theorem lead3Coord_y_ortho_iff {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v3Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v3Rat (normSqVec v) % 2 ≠ 0) :
    isLead3Coord u.y u ↔ isLead3Coord v.y v :=
  ⟨fun h => (lead3Coord_y_ortho_imp huv hu_odd hv_odd h).1,
   fun h => (lead3Coord_y_ortho_imp (inner_eq_zero_symm huv) hv_odd hu_odd h).1⟩

theorem lead3Coord_z_ortho_imp {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v3Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v3Rat (normSqVec v) % 2 ≠ 0)
    (hlead : isLead3Coord u.z u) :
    isLead3Coord v.z v ∧ coordSign3 u.z u + coordSign3 v.z v = 0 := by
  have huv' : GVec.inner (rotVec u) (rotVec v) = 0 := by rw [inner_rotVec]; exact huv
  have hu_odd' : v3Rat (normSqVec (rotVec u)) % 2 ≠ 0 := by rw [normSqVec_rotVec]; exact hu_odd
  have hv_odd' : v3Rat (normSqVec (rotVec v)) % 2 ≠ 0 := by rw [normSqVec_rotVec]; exact hv_odd
  have hlead' : isLead3Coord (rotVec u).y (rotVec u) := (isLead3Coord_rotVec_y u).mpr hlead
  obtain ⟨hv_lead, hsum⟩ := lead3Coord_y_ortho_imp huv' hu_odd' hv_odd' hlead'
  rw [isLead3Coord_rotVec_y] at hv_lead
  rw [coordSign3_rotVec_y, coordSign3_rotVec_y] at hsum
  exact ⟨hv_lead, hsum⟩

theorem s3_orthogonal_odd_cancel {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v3Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v3Rat (normSqVec v) % 2 ≠ 0) :
    s3 u + s3 v = 0 := by
  have hx_iff := lead3Coord_x_ortho_iff huv hu_odd hv_odd
  have hy_iff := lead3Coord_y_ortho_iff huv hu_odd hv_odd
  simp only [s3, hu_odd, hv_odd, ↓reduceIte]
  by_cases hx : isLead3Coord u.x u
  · have hvx : isLead3Coord v.x v := hx_iff.mp hx
    simp only [hx, hvx, ↓reduceIte]
    exact (lead3Coord_x_ortho_imp huv hu_odd hv_odd hx).2
  · have hvx : ¬ isLead3Coord v.x v := fun h => hx (hx_iff.mpr h)
    simp only [hx, hvx, ↓reduceIte]
    by_cases hy : isLead3Coord u.y u
    · have hvy : isLead3Coord v.y v := hy_iff.mp hy
      simp only [hy, hvy, ↓reduceIte]
      exact (lead3Coord_y_ortho_imp huv hu_odd hv_odd hy).2
    · have hvy : ¬ isLead3Coord v.y v := fun h => hy (hy_iff.mpr h)
      simp only [hy, hvy, ↓reduceIte]
      have hz : isLead3Coord u.z u := by
        rcases exists_lead3Coord_of_odd hu_odd with h1 | h2 | h3
        · exact False.elim (hx h1)
        · exact False.elim (hy h2)
        · exact h3
      exact (lead3Coord_z_ortho_imp huv hu_odd hv_odd hz).2

theorem s3_eq_zero_of_even {u : GVec} (heven : v3Rat (normSqVec u) % 2 = 0) : s3 u = 0 := by
  simp [s3, heven]

/-- `s3` is a global zero-weight frame function on all orthogonal frames in `ℚ(i)³`. -/
theorem s3_isZeroWeightFrameFunction : IsZeroWeightFrameFunction s3 := by
  intro u v w hf
  have hsum_even := frame_v3Rat_sum_even hf
  obtain ⟨_, _, _, huv, huw, hvw⟩ := hf
  by_cases hu : v3Rat (normSqVec u) % 2 = 0 <;>
    by_cases hv : v3Rat (normSqVec v) % 2 = 0 <;>
    by_cases hw : v3Rat (normSqVec w) % 2 = 0
  · rw [s3_eq_zero_of_even hu, s3_eq_zero_of_even hv, s3_eq_zero_of_even hw]
    ring
  · omega
  · omega
  · have hvw_sum := s3_orthogonal_odd_cancel hvw hv hw
    rw [s3_eq_zero_of_even hu]
    linarith
  · omega
  · have huw_sum := s3_orthogonal_odd_cancel huw hu hw
    rw [s3_eq_zero_of_even hv]
    linarith
  · have huv_sum := s3_orthogonal_odd_cancel huv hu hv
    rw [s3_eq_zero_of_even hw]
    linarith
  · omega

/-- Every zero-weight frame function on `ℚ(i)³` is constant along rays. -/
theorem zeroWeightFrameFunction_smul {δ : GVec → ℚ} (hZ : IsZeroWeightFrameFunction δ)
    {v : GVec} (hv : v.NonZero) {l : GaussRat} (hl : l ≠ 0) :
    δ (GVec.smul l v) = δ v := by
  obtain ⟨w, u, h1, h2⟩ := exists_frame_completion hv
  have e1 := hZ _ _ _ h1
  have e2 := hZ _ _ _ (h2 l hl)
  linarith

theorem s3_smul {v : GVec} (hv : v.NonZero) {l : GaussRat} (hl : l ≠ 0) :
    s3 (GVec.smul l v) = s3 v :=
  zeroWeightFrameFunction_smul s3_isZeroWeightFrameFunction hv hl

theorem coordSign3_values {z : GaussRat} {u : GVec} (hz : 0 < z.normSq) (hu : 0 < normSqVec u) :
    coordSign3 z u = 1 ∨ coordSign3 z u = -1 := by
  simp only [coordSign3]
  rcases u3Rat_values_of_pos hz with h1 | h1 <;>
    rcases u3Rat_values_of_pos hu with h2 | h2 <;>
    rw [h1, h2] <;> norm_num

theorem s3_values (u : GVec) : s3 u = 0 ∨ s3 u = 1 ∨ s3 u = -1 := by
  by_cases heven : v3Rat (normSqVec u) % 2 = 0
  · exact Or.inl (s3_eq_zero_of_even heven)
  · have hu : 0 < normSqVec u := pos_of_v3Rat_mod_two_ne_zero heven
    simp only [s3, heven, ↓reduceIte]
    by_cases hx : isLead3Coord u.x u
    · simp only [hx, ↓reduceIte]
      exact Or.inr (coordSign3_values hx.1 hu)
    · simp only [hx, ↓reduceIte]
      by_cases hy : isLead3Coord u.y u
      · simp only [hy, ↓reduceIte]
        exact Or.inr (coordSign3_values hy.1 hu)
      · simp only [hy, ↓reduceIte]
        have hz : isLead3Coord u.z u := by
          rcases exists_lead3Coord_of_odd heven with h1 | h2 | h3
          · exact False.elim (hx h1)
          · exact False.elim (hy h2)
          · exact h3
        exact Or.inr (coordSign3_values hz.1 hu)

theorem s3_abs_le_one (u : GVec) : |s3 u| ≤ 1 := by
  rcases s3_values u with h | h | h <;> rw [h] <;> norm_num

theorem s3_isBoundedOnRays : IsBoundedOnRays s3 :=
  ⟨1, by norm_num, fun v _ => s3_abs_le_one v⟩

theorem s3_eq_zero_of_normSqVec_natCast {u : GVec} {n : ℕ}
    (hn : 0 < n) (hnorm : normSqVec u = (n : ℚ)) (heven : (v3Nat n : ℤ) % 2 = 0) :
    s3 u = 0 := by
  apply s3_eq_zero_of_even
  rw [hnorm, v3Rat_natCast hn]
  exact heven

theorem s3_eq_of_lead3Coord_x {u : GVec} {n nx : ℕ}
    (hn : 0 < n) (hnx : 0 < nx)
    (hnorm : normSqVec u = (n : ℚ))
    (hx : u.x.normSq = (nx : ℚ))
    (hodd : (v3Nat n : ℤ) % 2 ≠ 0)
    (hlt : (v3Nat nx : ℤ) < (v3Nat n : ℤ)) :
    s3 u = (if p3PartNat nx % 3 = 1 then 1 else -1) * (if p3PartNat n % 3 = 1 then 1 else -1) := by
  have hvn : v3Rat (normSqVec u) = (v3Nat n : ℤ) := by rw [hnorm, v3Rat_natCast hn]
  have hvx : v3Rat u.x.normSq = (v3Nat nx : ℤ) := by rw [hx, v3Rat_natCast hnx]
  have hun : u3Rat (normSqVec u) = if p3PartNat n % 3 = 1 then 1 else -1 := by
    rw [hnorm, u3Rat_natCast hn]
  have hux : u3Rat u.x.normSq = if p3PartNat nx % 3 = 1 then 1 else -1 := by
    rw [hx, u3Rat_natCast hnx]
  have hx_pos : 0 < u.x.normSq := by rw [hx]; exact_mod_cast hnx
  have hlead : isLead3Coord u.x u := ⟨hx_pos, by omega⟩
  have hodd_u : v3Rat (normSqVec u) % 2 ≠ 0 := by omega
  simp only [s3, hodd_u, hlead, ↓reduceIte, coordSign3, hux, hun]

theorem s3_vanishes_on_nine_rays : VanishesOnNineRays s3 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact s3_eq_zero_of_normSqVec_natCast (n := 1) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e1, gv]) rfl
  · exact s3_eq_zero_of_normSqVec_natCast (n := 1) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e2, gv]) rfl
  · exact s3_eq_zero_of_normSqVec_natCast (n := 1) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e3, gv]) rfl
  · exact s3_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e12, gv]; norm_num) rfl
  · exact s3_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e13, gv]; norm_num) rfl
  · exact s3_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e23, gv]; norm_num) rfl
  · exact s3_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e12i, gv]; norm_num) rfl
  · exact s3_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e13i, gv]; norm_num) rfl
  · exact s3_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e23i, gv]; norm_num) rfl

/-- Norm-`3` witness `(1, 1, 1)` where `s3 = 1`. -/
def witness_111 : GVec := gv 1 0 1 0 1 0

/-- Norm-`12 = 4 * 3` `(1+i)`-primitive witness `(1+2i, 1+2i, 1+i)` where `s3 = -1`. -/
def witness_div_four_shell : GVec := gv 1 2 1 2 1 1

/-- Norm-`24 = 8 * 3` `(1+i)`-primitive witness `(1+4i, 1+2i, 1+i)` where `s3 = 1`. -/
def witness_div_eight_shell : GVec := gv 1 4 1 2 1 1

theorem witness_111_primitive : IsOnePlusIPrimitive 1 0 1 0 1 0 := by decide

theorem witness_111_nonZero : witness_111.NonZero := by
  left
  intro h
  have hre : witness_111.x.re = 0 := by rw [h]; rfl
  revert hre
  decide

theorem witness_111_normSq : normSqVec witness_111 = 3 := by
  simp [normSqVec, GaussRat.normSq, witness_111, gv]
  norm_num

theorem s3_witness_111 : s3 witness_111 = 1 := by
  rw [s3_eq_of_lead3Coord_x (n := 3) (nx := 1) (by decide) (by decide)
    (by simp [normSqVec, GaussRat.normSq, witness_111, gv]; norm_num)
    (by simp [GaussRat.normSq, witness_111, gv])
    (by decide) (by decide)]
  have hp1 : p3PartNat 1 % 3 = 1 := rfl
  have hp3 : p3PartNat 3 % 3 = 1 := rfl
  simp [hp1, hp3]

theorem witness_div_four_shell_primitive : IsOnePlusIPrimitive 1 2 1 2 1 1 := by decide

theorem witness_div_four_shell_nonZero : witness_div_four_shell.NonZero := by
  left
  intro h
  have hre : witness_div_four_shell.x.re = 0 := by rw [h]; rfl
  revert hre
  decide

theorem witness_div_four_shell_normSq : normSqVec witness_div_four_shell = 12 := by
  simp [normSqVec, GaussRat.normSq, witness_div_four_shell, gv]
  norm_num

theorem s3_witness_div_four_shell : s3 witness_div_four_shell = -1 := by
  rw [s3_eq_of_lead3Coord_x (n := 12) (nx := 5) (by decide) (by decide)
    (by simp [normSqVec, GaussRat.normSq, witness_div_four_shell, gv]; norm_num)
    (by simp [GaussRat.normSq, witness_div_four_shell, gv]; norm_num)
    (by decide) (by decide)]
  have hp5 : p3PartNat 5 % 3 = 2 := rfl
  have hp12 : p3PartNat 12 % 3 = 1 := rfl
  simp [hp5, hp12]

theorem witness_div_eight_shell_primitive : IsOnePlusIPrimitive 1 4 1 2 1 1 := by decide

theorem witness_div_eight_shell_nonZero : witness_div_eight_shell.NonZero := by
  left
  intro h
  have hre : witness_div_eight_shell.x.re = 0 := by rw [h]; rfl
  revert hre
  decide

theorem witness_div_eight_shell_normSq : normSqVec witness_div_eight_shell = 24 := by
  simp [normSqVec, GaussRat.normSq, witness_div_eight_shell, gv]
  norm_num

theorem s3_witness_div_eight_shell : s3 witness_div_eight_shell = 1 := by
  rw [s3_eq_of_lead3Coord_x (n := 24) (nx := 17) (by decide) (by decide)
    (by simp [normSqVec, GaussRat.normSq, witness_div_eight_shell, gv]; norm_num)
    (by simp [GaussRat.normSq, witness_div_eight_shell, gv]; norm_num)
    (by decide) (by decide)]
  have hp17 : p3PartNat 17 % 3 = 2 := rfl
  have hp24 : p3PartNat 24 % 3 = 2 := rfl
  simp [hp17, hp24]

/-- There exists an explicit global bounded zero-weight frame function on `ℚ(i)³`
vanishing on all nine tomography rays and nonzero across higher `(1+i)`-adic ray shells
(certified both by norm shells `3, 12, 24` and by `(1+i)`-primitivity `IsOnePlusIPrimitive`). -/
theorem exists_nonzero_bounded_zero_residual :
    ∃ δ : GVec → ℚ,
      IsZeroWeightFrameFunction δ ∧
      VanishesOnNineRays δ ∧
      IsBoundedOnRays δ ∧
      (IsOnePlusIPrimitive 1 0 1 0 1 0 ∧ normSqVec witness_111 = 3 ∧ δ witness_111 = 1) ∧
      (IsOnePlusIPrimitive 1 2 1 2 1 1 ∧ normSqVec witness_div_four_shell = 12 ∧
        δ witness_div_four_shell = -1) ∧
      (IsOnePlusIPrimitive 1 4 1 2 1 1 ∧ normSqVec witness_div_eight_shell = 24 ∧
        δ witness_div_eight_shell = 1) ∧
      ∃ v : GVec, v.NonZero ∧ δ v ≠ 0 := by
  refine ⟨s3, s3_isZeroWeightFrameFunction, s3_vanishes_on_nine_rays, s3_isBoundedOnRays,
    ⟨witness_111_primitive, witness_111_normSq, s3_witness_111⟩,
    ⟨witness_div_four_shell_primitive, witness_div_four_shell_normSq, s3_witness_div_four_shell⟩,
    ⟨witness_div_eight_shell_primitive, witness_div_eight_shell_normSq, s3_witness_div_eight_shell⟩,
    witness_111, witness_111_nonZero, ?_⟩
  rw [s3_witness_111]
  norm_num

/-- Signed quadratic rigidity fails globally on `ℚ(i)³`: not every rational-valued frame
function on `ℚ(i)³` is the normalized Rayleigh quotient `quadRay ρ` of a Hermitian form. -/
theorem not_signed_quadratic_rigidity :
    ¬ (∀ f : GVec → ℚ, IsFrameFunction f →
        ∃ ρ : HermForm3, ρ.tr = 1 ∧ ∀ v : GVec, v.NonZero → f v = quadRay ρ v) := by
  rw [signed_rigidity_iff_zero_residual]
  intro hall
  have h0 := hall s3 s3_isZeroWeightFrameFunction s3_vanishes_on_nine_rays
    witness_111 witness_111_nonZero
  rw [s3_witness_111] at h0
  norm_num at h0

/-- Nonnegative quadratic rigidity also fails globally on `ℚ(i)³`: not every nonnegative
rational-valued frame function on `ℚ(i)³` is the normalized Rayleigh quotient `quadRay ρ`
of a Hermitian form. -/
theorem not_nonneg_quadratic_rigidity :
    ¬ (∀ f : GVec → ℚ, IsNonnegFrameFunction f →
        ∃ ρ : HermForm3, ρ.tr = 1 ∧ ∀ v : GVec, v.NonZero → f v = quadRay ρ v) := by
  rw [nonneg_rigidity_iff_bounded_zero_residual]
  intro hall
  have h0 := hall s3 s3_isZeroWeightFrameFunction s3_vanishes_on_nine_rays s3_isBoundedOnRays
    witness_111 witness_111_nonZero
  rw [s3_witness_111] at h0
  norm_num at h0

/-- Explicit global `{0, 1/3, 2/3}`-valued nonnegative non-quadratic frame function on `ℚ(i)³`. -/
def exoticQi3 (v : GVec) : ℚ := (1 + s3 v) / 3

theorem exoticQi3_values (v : GVec) :
    exoticQi3 v = 1 / 3 ∨ exoticQi3 v = 2 / 3 ∨ exoticQi3 v = 0 := by
  simp only [exoticQi3]
  rcases s3_values v with h | h | h <;> rw [h] <;> norm_num

theorem exoticQi3_bounds (v : GVec) : 0 ≤ exoticQi3 v ∧ exoticQi3 v ≤ 2 / 3 := by
  rcases exoticQi3_values v with h | h | h <;> rw [h] <;> constructor <;> norm_num

theorem exoticQi3_isFrameFunction : IsFrameFunction exoticQi3 := by
  intro u v w hf
  have hsum := s3_isZeroWeightFrameFunction u v w hf
  simp only [exoticQi3]
  linarith

theorem exoticQi3_isNonnegFrameFunction : IsNonnegFrameFunction exoticQi3 :=
  ⟨exoticQi3_isFrameFunction, fun v _ => (exoticQi3_bounds v).1⟩

theorem exoticQi3_not_quadratic :
    ¬ ∃ ρ : HermForm3, ∀ v : GVec, v.NonZero → exoticQi3 v = quadRay ρ v := by
  rintro ⟨ρ, hρ⟩
  obtain ⟨he1_s3, he2_s3, he3_s3, he12_s3, he13_s3, he23_s3, he12i_s3, he13i_s3, he23i_s3⟩ :=
    s3_vanishes_on_nine_rays
  have htomo_id : tomographyForm exoticQi3 = ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ := by
    ext <;>
      simp [tomographyForm, exoticQi3,
        he1_s3, he2_s3, he3_s3, he12_s3, he13_s3, he23_s3, he12i_s3, he13i_s3, he23i_s3]
  have hm := tomography_matches_nine_rays exoticQi3
  have hρ_eq : tomographyForm exoticQi3 = ρ := by
    apply tomography_unique (tomographyForm exoticQi3) ρ
    · rw [hm.1, hρ tomo_e1 tomo_e1_nonZero]
    · rw [hm.2.1, hρ tomo_e2 tomo_e2_nonZero]
    · rw [hm.2.2.1, hρ tomo_e3 tomo_e3_nonZero]
    · rw [hm.2.2.2.1, hρ tomo_e12 tomo_e12_nonZero]
    · rw [hm.2.2.2.2.1, hρ tomo_e13 tomo_e13_nonZero]
    · rw [hm.2.2.2.2.2.1, hρ tomo_e23 tomo_e23_nonZero]
    · rw [hm.2.2.2.2.2.2.1, hρ tomo_e12i tomo_e12i_nonZero]
    · rw [hm.2.2.2.2.2.2.2.1, hρ tomo_e13i tomo_e13i_nonZero]
    · rw [hm.2.2.2.2.2.2.2.2, hρ tomo_e23i tomo_e23i_nonZero]
  have hρ_id : ρ = ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ := hρ_eq.symm.trans htomo_id
  have h111 := hρ witness_111 witness_111_nonZero
  rw [hρ_id] at h111
  have hq : quadRay ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ witness_111 = 1 / 3 := by
    simp [quadRay, quadNum, normSqVec, GaussRat.normSq, witness_111, gv]
    norm_num
  have hex : exoticQi3 witness_111 = 2 / 3 := by
    simp [exoticQi3, s3_witness_111]
    norm_num
  linarith

/-- Explicit operator-space projector relation (`Section 5`): the rank-1 projector of
`witness_111 = (1, 1, 1)` is a rational linear combination of the six real tomography projectors. -/
theorem rayProj_witness_111_decomp :
    rayProj witness_111 =
    HermForm3.add
      (HermForm3.smul (-1 / 3)
        (HermForm3.add (HermForm3.add (rayProj tomo_e1) (rayProj tomo_e2)) (rayProj tomo_e3)))
      (HermForm3.smul (2 / 3)
        (HermForm3.add (HermForm3.add (rayProj tomo_e12) (rayProj tomo_e13)) (rayProj tomo_e23))) := by
  ext <;>
    simp [HermForm3.add, HermForm3.smul, rayProj, normSqVec, GaussRat.normSq,
      witness_111, tomo_e1, tomo_e2, tomo_e3, tomo_e12, tomo_e13, tomo_e23, gv] <;>
    norm_num

/-- Every quadratic Rayleigh function `quadRay ρ` satisfies the 7-ray linear kernel identity
induced by `rayProj_witness_111_decomp`. -/
theorem quadRay_witness_111_kernel_relation (ρ : HermForm3) :
    quadRay ρ witness_111 +
      (1 / 3) * (quadRay ρ tomo_e1 + quadRay ρ tomo_e2 + quadRay ρ tomo_e3) -
      (2 / 3) * (quadRay ρ tomo_e12 + quadRay ρ tomo_e13 + quadRay ρ tomo_e23) = 0 := by
  simp only [← traceInner_rayProj, rayProj_witness_111_decomp,
    traceInner_add_right, traceInner_smul_right]
  ring

/-- Constructive separation of the projector kernel (`Section 5`) without basis extension:
the 7-ray formal combination in `ker(rayProj)` evaluates to `1 ≠ 0` under `s3` (and `1/3 ≠ 0`
under `exoticQi3`). -/
theorem s3_witness_111_kernel_separation :
    s3 witness_111 +
      (1 / 3) * (s3 tomo_e1 + s3 tomo_e2 + s3 tomo_e3) -
      (2 / 3) * (s3 tomo_e12 + s3 tomo_e13 + s3 tomo_e23) = 1 ∧
    exoticQi3 witness_111 +
      (1 / 3) * (exoticQi3 tomo_e1 + exoticQi3 tomo_e2 + exoticQi3 tomo_e3) -
      (2 / 3) * (exoticQi3 tomo_e12 + exoticQi3 tomo_e13 + exoticQi3 tomo_e23) = 1 / 3 := by
  obtain ⟨he1, he2, he3, he12, he13, he23, _, _, _⟩ := s3_vanishes_on_nine_rays
  refine ⟨?_, ?_⟩
  · rw [s3_witness_111, he1, he2, he3, he12, he13, he23]
    norm_num
  · simp only [exoticQi3, s3_witness_111, he1, he2, he3, he12, he13, he23]
    norm_num

/-! ### 9. Regularity, Continuity, and Field-Extension Hypotheses Eliminating `3`-Adic Residuals -/

/-- Squared Euclidean/Hermitian distance `‖u - v‖²` on `ℚ(i)³`. -/
def distSqVec (u v : GVec) : ℚ :=
  normSqVec ⟨u.x - v.x, u.y - v.y, u.z - v.z⟩

/-- Archimedean continuity of a ray function `g : GVec → ℚ` at a nonzero vector `v₀ ∈ ℚ(i)³`. -/
def IsArchimedeanContinuousAt (g : GVec → ℚ) (v₀ : GVec) : Prop :=
  ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
    ∀ v : GVec, v.NonZero → distSqVec v v₀ < δ → |g v - g v₀| < ε

/-- Unscaled positive-sign `3`-adic Gaussian-integer perturbation `(3k, 1, 1 + i)` near `tomo_e1`. -/
def perturbPosInt (k : ℕ) : GVec :=
  gv (3 * (k : ℤ)) 0 1 0 1 1

/-- Unscaled negative-sign `3`-adic Gaussian-integer perturbation `(3k, 1 + i, 1)` near `tomo_e1`. -/
def perturbNegInt (k : ℕ) : GVec :=
  gv (3 * (k : ℤ)) 0 1 1 1 0

/-- Normalized positive-sign perturbation `(1, 1/(3k), (1+i)/(3k))` approaching `tomo_e1`. -/
def perturbPosRay (k : ℕ) : GVec :=
  ⟨⟨1, 0⟩, ⟨1 / (3 * (k : ℚ)), 0⟩, ⟨1 / (3 * (k : ℚ)), 1 / (3 * (k : ℚ))⟩⟩

/-- Normalized negative-sign perturbation `(1, (1+i)/(3k), 1/(3k))` approaching `tomo_e1`. -/
def perturbNegRay (k : ℕ) : GVec :=
  ⟨⟨1, 0⟩, ⟨1 / (3 * (k : ℚ)), 1 / (3 * (k : ℚ))⟩, ⟨1 / (3 * (k : ℚ)), 0⟩⟩

theorem v3Nat_nine_mul_sq_add_three (k : ℕ) :
    v3Nat (9 * k ^ 2 + 3) = 1 ∧ p3PartNat (9 * k ^ 2 + 3) = 3 * k ^ 2 + 1 := by
  apply v3Nat_p3PartNat_eq_of_pow_mul
  · omega
  · ring

theorem v3Nat_nine_mul_sq_ge_two {k : ℕ} (hk : 0 < k) :
    2 ≤ v3Nat (9 * k ^ 2) := by
  have hk2 : 0 < k ^ 2 := pow_pos hk 2
  have hmul := (v3Nat_p3PartNat_mul (by decide : 0 < 9) hk2).1
  have hv9 : v3Nat 9 = 2 := rfl
  omega

theorem s3_eq_of_lead3Coord_y {u : GVec} {n nx ny : ℕ}
    (hn : 0 < n) (hnx : 0 < nx) (hny : 0 < ny)
    (hnorm : normSqVec u = (n : ℚ))
    (hx : u.x.normSq = (nx : ℚ))
    (hy : u.y.normSq = (ny : ℚ))
    (hodd : (v3Nat n : ℤ) % 2 ≠ 0)
    (hge_x : (v3Nat n : ℤ) ≤ (v3Nat nx : ℤ))
    (hlt_y : (v3Nat ny : ℤ) < (v3Nat n : ℤ)) :
    s3 u = (if p3PartNat ny % 3 = 1 then 1 else -1) *
      (if p3PartNat n % 3 = 1 then 1 else -1) := by
  have hvn : v3Rat (normSqVec u) = (v3Nat n : ℤ) := by rw [hnorm, v3Rat_natCast hn]
  have hvx : v3Rat u.x.normSq = (v3Nat nx : ℤ) := by rw [hx, v3Rat_natCast hnx]
  have hvy : v3Rat u.y.normSq = (v3Nat ny : ℤ) := by rw [hy, v3Rat_natCast hny]
  have hun : u3Rat (normSqVec u) = if p3PartNat n % 3 = 1 then 1 else -1 := by
    rw [hnorm, u3Rat_natCast hn]
  have huy : u3Rat u.y.normSq = if p3PartNat ny % 3 = 1 then 1 else -1 := by
    rw [hy, u3Rat_natCast hny]
  have hy_pos : 0 < u.y.normSq := by rw [hy]; exact_mod_cast hny
  have hnot_x : ¬ isLead3Coord u.x u := by
    intro ⟨_, hlt⟩
    omega
  have hlead_y : isLead3Coord u.y u := ⟨hy_pos, by omega⟩
  have hodd_u : v3Rat (normSqVec u) % 2 ≠ 0 := by omega
  simp only [s3, hodd_u, hnot_x, hlead_y, ↓reduceIte, coordSign3, huy, hun]

theorem perturbPosRay_nonZero (k : ℕ) : (perturbPosRay k).NonZero := by
  left
  change (⟨1, 0⟩ : GaussRat) ≠ 0
  decide

theorem perturbNegRay_nonZero (k : ℕ) : (perturbNegRay k).NonZero := by
  left
  change (⟨1, 0⟩ : GaussRat) ≠ 0
  decide

@[ext]
theorem GVec_ext {u v : GVec} (hx : u.x = v.x) (hy : u.y = v.y) (hz : u.z = v.z) : u = v := by
  cases u; cases v; simp_all

theorem three_mul_gaussRat_ne_zero {k : ℕ} (hk : 0 < k) :
    (⟨3 * (k : ℚ), 0⟩ : GaussRat) ≠ 0 := by
  have hk_q : 0 < (k : ℚ) := by exact_mod_cast hk
  intro h
  have hre : (⟨3 * (k : ℚ), 0⟩ : GaussRat).re = 0 := by rw [h]; rfl
  simp only at hre
  linarith

theorem smul_three_mul_perturbPosRay {k : ℕ} (hk : 0 < k) :
    GVec.smul ⟨3 * (k : ℚ), 0⟩ (perturbPosRay k) = perturbPosInt k := by
  have hk_q : 0 < (k : ℚ) := by exact_mod_cast hk
  have hk_ne : (k : ℚ) ≠ 0 := ne_of_gt hk_q
  have hmul : 3 * (k : ℚ) * ((k : ℚ)⁻¹ * 3⁻¹) = 1 := by
    calc 3 * (k : ℚ) * ((k : ℚ)⁻¹ * 3⁻¹)
        = (k : ℚ) * (k : ℚ)⁻¹ := by ring
      _ = 1 := mul_inv_cancel₀ hk_ne
  ext <;> simp [GVec.smul, perturbPosRay, perturbPosInt, gv, hmul]

theorem smul_three_mul_perturbNegRay {k : ℕ} (hk : 0 < k) :
    GVec.smul ⟨3 * (k : ℚ), 0⟩ (perturbNegRay k) = perturbNegInt k := by
  have hk_q : 0 < (k : ℚ) := by exact_mod_cast hk
  have hk_ne : (k : ℚ) ≠ 0 := ne_of_gt hk_q
  have hmul : 3 * (k : ℚ) * ((k : ℚ)⁻¹ * 3⁻¹) = 1 := by
    calc 3 * (k : ℚ) * ((k : ℚ)⁻¹ * 3⁻¹)
        = (k : ℚ) * (k : ℚ)⁻¹ := by ring
      _ = 1 := mul_inv_cancel₀ hk_ne
  ext <;> simp [GVec.smul, perturbNegRay, perturbNegInt, gv, hmul]

theorem s3_perturbPosInt {k : ℕ} (hk : 0 < k) : s3 (perturbPosInt k) = 1 := by
  obtain ⟨hv_n, hp_n⟩ := v3Nat_nine_mul_sq_add_three k
  have hv_x := v3Nat_nine_mul_sq_ge_two hk
  have hv1 : v3Nat 1 = 0 := rfl
  have hp1 : p3PartNat 1 = 1 := rfl
  rw [s3_eq_of_lead3Coord_y (n := 9 * k ^ 2 + 3) (nx := 9 * k ^ 2) (ny := 1)
    (by omega) (by nlinarith) (by decide)
    (by simp [normSqVec, GaussRat.normSq, perturbPosInt, gv]; ring)
    (by simp [GaussRat.normSq, perturbPosInt, gv]; ring)
    (by simp [GaussRat.normSq, perturbPosInt, gv])
    (by omega) (by omega) (by omega)]
  have hmod_n : p3PartNat (9 * k ^ 2 + 3) % 3 = 1 := by rw [hp_n]; omega
  have hmod_y : p3PartNat 1 % 3 = 1 := rfl
  simp [hmod_n, hmod_y]

theorem s3_perturbNegInt {k : ℕ} (hk : 0 < k) : s3 (perturbNegInt k) = -1 := by
  obtain ⟨hv_n, hp_n⟩ := v3Nat_nine_mul_sq_add_three k
  have hv_x := v3Nat_nine_mul_sq_ge_two hk
  have hv2 : v3Nat 2 = 0 := rfl
  have hp2 : p3PartNat 2 = 2 := rfl
  rw [s3_eq_of_lead3Coord_y (n := 9 * k ^ 2 + 3) (nx := 9 * k ^ 2) (ny := 2)
    (by omega) (by nlinarith) (by decide)
    (by simp [normSqVec, GaussRat.normSq, perturbNegInt, gv]; ring)
    (by simp [GaussRat.normSq, perturbNegInt, gv]; ring)
    (by simp [GaussRat.normSq, perturbNegInt, gv]; norm_num)
    (by omega) (by omega) (by omega)]
  have hmod_n : p3PartNat (9 * k ^ 2 + 3) % 3 = 1 := by rw [hp_n]; omega
  have hmod_y : p3PartNat 2 % 3 = 2 := rfl
  simp [hmod_n, hmod_y]

theorem s3_perturbPosRay {k : ℕ} (hk : 0 < k) : s3 (perturbPosRay k) = 1 := by
  rw [← s3_smul (perturbPosRay_nonZero k) (three_mul_gaussRat_ne_zero hk),
    smul_three_mul_perturbPosRay hk]
  exact s3_perturbPosInt hk

theorem s3_perturbNegRay {k : ℕ} (hk : 0 < k) : s3 (perturbNegRay k) = -1 := by
  rw [← s3_smul (perturbNegRay_nonZero k) (three_mul_gaussRat_ne_zero hk),
    smul_three_mul_perturbNegRay hk]
  exact s3_perturbNegInt hk

theorem exoticQi3_perturbPosRay {k : ℕ} (hk : 0 < k) :
    exoticQi3 (perturbPosRay k) = 2 / 3 := by
  simp only [exoticQi3, s3_perturbPosRay hk]
  norm_num

theorem exoticQi3_perturbNegRay {k : ℕ} (hk : 0 < k) :
    exoticQi3 (perturbNegRay k) = 0 := by
  simp only [exoticQi3, s3_perturbNegRay hk]
  norm_num

theorem distSqVec_perturbPosRay_tomo_e1 (k : ℕ) :
    distSqVec (perturbPosRay k) tomo_e1 = 1 / (3 * (k : ℚ) ^ 2) := by
  simp only [distSqVec, perturbPosRay, tomo_e1, gv,
    normSqVec, GaussRat.normSq, GaussRat.re_sub, GaussRat.im_sub]
  ring

theorem distSqVec_perturbNegRay_tomo_e1 (k : ℕ) :
    distSqVec (perturbNegRay k) tomo_e1 = 1 / (3 * (k : ℚ) ^ 2) := by
  simp only [distSqVec, perturbNegRay, tomo_e1, gv,
    normSqVec, GaussRat.normSq, GaussRat.re_sub, GaussRat.im_sub]
  ring

theorem exists_nat_pos_inv_three_sq_lt {δ : ℚ} (hδ : 0 < δ) :
    ∃ k : ℕ, 0 < k ∧ 1 / (3 * (k : ℚ) ^ 2) < δ := by
  let k : ℕ := (1 / δ).num.natAbs + 1
  have hk_pos : 0 < k := Nat.succ_pos _
  refine ⟨k, hk_pos, ?_⟩
  have hk_ge_one : (1 : ℚ) ≤ (k : ℚ) := by exact_mod_cast hk_pos
  have hnum_le : (1 / δ).num ≤ ((1 / δ).num.natAbs : ℤ) := Int.le_natAbs
  have hnum_q : ((1 / δ).num : ℚ) ≤ ((1 / δ).num.natAbs : ℚ) := by
    simpa only [Int.cast_natCast] using (Int.cast_le (R := ℚ)).mpr hnum_le
  have hden_pos : (0 : ℚ) < ((1 / δ).den : ℚ) := by exact_mod_cast (1 / δ).den_pos
  have hden_ge : (1 : ℚ) ≤ ((1 / δ).den : ℚ) := by exact_mod_cast (1 / δ).den_pos
  have hnn : (0 : ℚ) ≤ ((1 / δ).num.natAbs : ℚ) := by positivity
  have hdiv_le : 1 / δ ≤ ((1 / δ).num.natAbs : ℚ) := by
    have hmul : ((1 / δ).num : ℚ) ≤ ((1 / δ).num.natAbs : ℚ) * ((1 / δ).den : ℚ) := by nlinarith
    have hdiv : ((1 / δ).num : ℚ) / ((1 / δ).den : ℚ) ≤ ((1 / δ).num.natAbs : ℚ) :=
      (div_le_iff₀ hden_pos).mpr hmul
    rwa [Rat.num_div_den (1 / δ)] at hdiv
  have hk_gt : 1 / δ < (k : ℚ) := by
    simp only [k, Nat.cast_add, Nat.cast_one]
    linarith
  have h3k2_gt : 1 / δ < 3 * (k : ℚ) ^ 2 := by nlinarith
  have h3k2_pos : 0 < 3 * (k : ℚ) ^ 2 := by positivity
  exact (div_lt_iff₀ h3k2_pos).mpr (by
    have hmul := (div_lt_iff₀ hδ).mp h3k2_gt
    linarith)

/-- In every archimedean neighborhood `distSqVec v tomo_e1 < δ` of `tomo_e1 = (1, 0, 0)`,
there exist nonzero Gaussian-rational vectors `uPos, uNeg ∈ ℚ(i)³` on which `s3` attains `+1` and `-1`
(while `s3 tomo_e1 = 0`), and `exoticQi3` attains `2/3` and `0` (while `exoticQi3 tomo_e1 = 1/3`). -/
theorem s3_oscillates_near_tomo_e1 (δ : ℚ) (hδ : 0 < δ) :
    ∃ uPos uNeg : GVec,
      uPos.NonZero ∧ uNeg.NonZero ∧
      distSqVec uPos tomo_e1 < δ ∧ distSqVec uNeg tomo_e1 < δ ∧
      s3 uPos = 1 ∧ s3 uNeg = -1 ∧
      exoticQi3 uPos = 2 / 3 ∧ exoticQi3 uNeg = 0 := by
  obtain ⟨k, hk, hlt⟩ := exists_nat_pos_inv_three_sq_lt hδ
  refine ⟨perturbPosRay k, perturbNegRay k,
    perturbPosRay_nonZero k, perturbNegRay_nonZero k, ?_, ?_,
    s3_perturbPosRay hk, s3_perturbNegRay hk,
    exoticQi3_perturbPosRay hk, exoticQi3_perturbNegRay hk⟩
  · rw [distSqVec_perturbPosRay_tomo_e1 k]; exact hlt
  · rw [distSqVec_perturbNegRay_tomo_e1 k]; exact hlt

/-- The `3`-adic zero-weight residual `s3` is not archimedean-continuous at `tomo_e1 = (1, 0, 0)`. -/
theorem not_archimedeanContinuousAt_s3_tomo_e1 :
    ¬ IsArchimedeanContinuousAt s3 tomo_e1 := by
  intro hcont
  obtain ⟨δ, hδ, hball⟩ := hcont (1 / 2) (by norm_num)
  obtain ⟨uPos, _, huPos_nz, _, huPos_dist, _, huPos_s3, _, _, _⟩ :=
    s3_oscillates_near_tomo_e1 δ hδ
  have hlt := hball uPos huPos_nz huPos_dist
  have he1 : s3 tomo_e1 = 0 := s3_vanishes_on_nine_rays.1
  rw [huPos_s3, he1] at hlt
  norm_num at hlt

/-- The nonnegative non-quadratic frame function `exoticQi3` is not archimedean-continuous
at `tomo_e1 = (1, 0, 0)`. -/
theorem not_archimedeanContinuousAt_exoticQi3_tomo_e1 :
    ¬ IsArchimedeanContinuousAt exoticQi3 tomo_e1 := by
  intro hcont
  obtain ⟨δ, hδ, hball⟩ := hcont (1 / 6) (by norm_num)
  obtain ⟨uPos, _, huPos_nz, _, huPos_dist, _, _, _, huPos_ex, _⟩ :=
    s3_oscillates_near_tomo_e1 δ hδ
  have hlt := hball uPos huPos_nz huPos_dist
  have he1 : exoticQi3 tomo_e1 = 1 / 3 := by
    simp only [exoticQi3, s3_vanishes_on_nine_rays.1]
    norm_num
  rw [huPos_ex, he1] at hlt
  norm_num at hlt

/-- Any perturbation `f(v) = quadRay ρ v + c * s3 v` cannot be archimedean-continuous at `tomo_e1`
unless the `3`-adic residual coefficient `c` vanishes (`c = 0`), provided `quadRay ρ` is
archimedean-continuous at `tomo_e1`. -/
theorem s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1
    {f : GVec → ℚ} {c : ℚ}
    (hf_cont : IsArchimedeanContinuousAt f tomo_e1)
    (hq_cont : IsArchimedeanContinuousAt (fun v => f v - c * s3 v) tomo_e1) :
    c = 0 := by
  by_contra hc
  have hc_pos : 0 < |c| := abs_pos.mpr hc
  obtain ⟨δ1, hδ1, hb1⟩ := hf_cont (|c| / 3) (by linarith)
  obtain ⟨δ2, hδ2, hb2⟩ := hq_cont (|c| / 3) (by linarith)
  let δ := min δ1 δ2
  have hδ : 0 < δ := lt_min hδ1 hδ2
  obtain ⟨uPos, _, huPos_nz, _, huPos_dist, _, huPos_s3, _, _, _⟩ :=
    s3_oscillates_near_tomo_e1 δ hδ
  have h1 := hb1 uPos huPos_nz (lt_of_lt_of_le huPos_dist (min_le_left δ1 δ2))
  have h2 := hb2 uPos huPos_nz (lt_of_lt_of_le huPos_dist (min_le_right δ1 δ2))
  have he1 : s3 tomo_e1 = 0 := s3_vanishes_on_nine_rays.1
  simp only [huPos_s3, he1, mul_one, mul_zero, sub_zero] at h2
  have htri : |c| ≤ |f uPos - f tomo_e1| + |f uPos - c - f tomo_e1| := by
    calc |c| = |(f uPos - f tomo_e1) - (f uPos - c - f tomo_e1)| := by ring_nf
      _ ≤ |f uPos - f tomo_e1| + |f uPos - c - f tomo_e1| :=
        abs_sub (f uPos - f tomo_e1) (f uPos - c - f tomo_e1)
  linarith

theorem distSqVec_tomo_e1_eq (v : GVec) :
    distSqVec v tomo_e1 = (v.x.re - 1) ^ 2 + v.x.im ^ 2 + v.y.normSq + v.z.normSq := by
  simp only [distSqVec, tomo_e1, gv, normSqVec, GaussRat.normSq,
    GaussRat.re_sub, GaussRat.im_sub, Int.cast_one, Int.cast_zero]
  ring

theorem normSqVec_add_distSqVec_tomo_e1_ge_half (v : GVec) :
    (1 / 2 : ℚ) ≤ normSqVec v + distSqVec v tomo_e1 := by
  have hid : normSqVec v + distSqVec v tomo_e1 =
      2 * (v.x.re - 1 / 2) ^ 2 + 2 * v.x.im ^ 2 + 2 * v.y.normSq + 2 * v.z.normSq + 1 / 2 := by
    rw [distSqVec_tomo_e1_eq]
    simp only [normSqVec, GaussRat.normSq]
    ring
  linarith [sq_nonneg (v.x.re - 1 / 2), sq_nonneg v.x.im,
    GaussRat.normSq_nonneg v.y, GaussRat.normSq_nonneg v.z, hid]

theorem y_z_normSq_le_distSqVec_tomo_e1 (v : GVec) :
    v.y.normSq + v.z.normSq ≤ distSqVec v tomo_e1 := by
  have heq := distSqVec_tomo_e1_eq v
  linarith [sq_nonneg (v.x.re - 1), sq_nonneg v.x.im, heq]

theorem mul_abs_two_mul_le_weighted_sq (θ a b : ℚ) :
    2 * θ * |2 * (a * b)| ≤ 4 * θ ^ 2 * a ^ 2 + b ^ 2 := by
  have h1 : 0 ≤ (2 * θ * a - b) ^ 2 := sq_nonneg (2 * θ * a - b)
  have h2 : 0 ≤ (2 * θ * a + b) ^ 2 := sq_nonneg (2 * θ * a + b)
  rcases le_total 0 (2 * (a * b)) with h | h
  · rw [abs_of_nonneg h]; nlinarith
  · rw [abs_of_nonpos h]; nlinarith

theorem mul_abs_two_re_inner_le_weighted (θ : ℚ) (hθ : 0 ≤ θ) (x y : GaussRat) :
    2 * θ * |2 * (x.re * y.re + x.im * y.im)| ≤ 4 * θ ^ 2 * x.normSq + y.normSq := by
  have h1 := mul_abs_two_mul_le_weighted_sq θ x.re y.re
  have h2 := mul_abs_two_mul_le_weighted_sq θ x.im y.im
  have htri : |2 * (x.re * y.re + x.im * y.im)| ≤ |2 * (x.re * y.re)| + |2 * (x.im * y.im)| := by
    have heq : 2 * (x.re * y.re + x.im * y.im) = 2 * (x.re * y.re) + 2 * (x.im * y.im) := by ring
    rw [heq]
    exact abs_add_le _ _
  simp only [GaussRat.normSq]
  nlinarith

theorem mul_abs_two_im_inner_le_weighted (θ : ℚ) (hθ : 0 ≤ θ) (x y : GaussRat) :
    2 * θ * |2 * (x.re * y.im - x.im * y.re)| ≤ 4 * θ ^ 2 * x.normSq + y.normSq := by
  have h1 := mul_abs_two_mul_le_weighted_sq θ x.re y.im
  have h2 := mul_abs_two_mul_le_weighted_sq θ x.im y.re
  have htri : |2 * (x.re * y.im - x.im * y.re)| ≤ |2 * (x.re * y.im)| + |2 * (x.im * y.re)| := by
    have heq : 2 * (x.re * y.im - x.im * y.re) = 2 * (x.re * y.im) - 2 * (x.im * y.re) := by ring
    rw [heq]
    exact abs_sub _ _
  simp only [GaussRat.normSq]
  nlinarith

theorem abs_quadNum_sub_d1_mul_normSqVec_le (ρ : HermForm3) {v : GVec} {θ : ℚ}
    (hθ_pos : 0 < θ) (hθ_half : θ ≤ 1 / 2)
    (hdist : distSqVec v tomo_e1 < θ ^ 2) :
    1 / 4 < normSqVec v ∧
    |quadNum ρ v - ρ.d1 * normSqVec v| ≤ 8 * ρ.coeffNorm * θ * normSqVec v := by
  have hθ_nn : 0 ≤ θ := le_of_lt hθ_pos
  have hθ_sq_le : θ ^ 2 ≤ 1 / 4 := by nlinarith
  have hN_dist := normSqVec_add_distSqVec_tomo_e1_ge_half v
  have hN_gt : 1 / 4 < normSqVec v := by linarith
  have hyz_le := y_z_normSq_le_distSqVec_tomo_e1 v
  have hx_nn := GaussRat.normSq_nonneg v.x
  have hy_nn := GaussRat.normSq_nonneg v.y
  have hz_nn := GaussRat.normSq_nonneg v.z
  have hx_le_N : v.x.normSq ≤ normSqVec v := by unfold normSqVec; linarith
  have hyz_lt_sq : v.y.normSq + v.z.normSq < 4 * θ ^ 2 * normSqVec v := by nlinarith
  have hyz_le_M : v.y.normSq + v.z.normSq ≤ 4 * θ * normSqVec v := by nlinarith
  have hy_le_M : v.y.normSq ≤ 4 * θ * normSqVec v := by linarith
  have hz_le_M : v.z.normSq ≤ 4 * θ * normSqVec v := by linarith
  let M := 4 * θ * normSqVec v
  have hM_nn : 0 ≤ M := by change 0 ≤ 4 * θ * normSqVec v; positivity
  have h_re_xy : |2 * (v.x.re * v.y.re + v.x.im * v.y.im)| ≤ M := by
    have hw := mul_abs_two_re_inner_le_weighted θ hθ_nn v.x v.y
    change |2 * (v.x.re * v.y.re + v.x.im * v.y.im)| ≤ 4 * θ * normSqVec v
    nlinarith
  have h_re_xz : |2 * (v.x.re * v.z.re + v.x.im * v.z.im)| ≤ M := by
    have hw := mul_abs_two_re_inner_le_weighted θ hθ_nn v.x v.z
    change |2 * (v.x.re * v.z.re + v.x.im * v.z.im)| ≤ 4 * θ * normSqVec v
    nlinarith
  have h_im_xy : |2 * (v.x.re * v.y.im - v.x.im * v.y.re)| ≤ M := by
    have hw := mul_abs_two_im_inner_le_weighted θ hθ_nn v.x v.y
    change |2 * (v.x.re * v.y.im - v.x.im * v.y.re)| ≤ 4 * θ * normSqVec v
    nlinarith
  have h_im_xz : |2 * (v.x.re * v.z.im - v.x.im * v.z.re)| ≤ M := by
    have hw := mul_abs_two_im_inner_le_weighted θ hθ_nn v.x v.z
    change |2 * (v.x.re * v.z.im - v.x.im * v.z.re)| ≤ 4 * θ * normSqVec v
    nlinarith
  have h_re_yz : |2 * (v.y.re * v.z.re + v.y.im * v.z.im)| ≤ M := by
    change |2 * (v.y.re * v.z.re + v.y.im * v.z.im)| ≤ 4 * θ * normSqVec v
    linarith [abs_two_re_inner_le v.y v.z]
  have h_im_yz : |2 * (v.y.re * v.z.im - v.y.im * v.z.re)| ≤ M := by
    change |2 * (v.y.re * v.z.im - v.y.im * v.z.re)| ≤ 4 * θ * normSqVec v
    linarith [abs_two_im_inner_le v.y v.z]
  have hd2 : |(ρ.d2 - ρ.d1) * v.y.normSq| ≤ (|ρ.d2| + |ρ.d1|) * M := by
    have h1 := abs_mul_nonneg_le (c := ρ.d2 - ρ.d1) hy_nn hy_le_M
    have h2 : |ρ.d2 - ρ.d1| * M ≤ (|ρ.d2| + |ρ.d1|) * M :=
      mul_le_mul_of_nonneg_right (abs_sub ρ.d2 ρ.d1) hM_nn
    linarith
  have hd3 : |(ρ.d3 - ρ.d1) * v.z.normSq| ≤ (|ρ.d3| + |ρ.d1|) * M := by
    have h1 := abs_mul_nonneg_le (c := ρ.d3 - ρ.d1) hz_nn hz_le_M
    have h2 : |ρ.d3 - ρ.d1| * M ≤ (|ρ.d3| + |ρ.d1|) * M :=
      mul_le_mul_of_nonneg_right (abs_sub ρ.d3 ρ.d1) hM_nn
    linarith
  have ha12 : |2 * ρ.a12 * (v.x.re * v.y.re + v.x.im * v.y.im)| ≤ 2 * |ρ.a12| * M :=
    abs_two_coeff_mul_le h_re_xy hM_nn
  have ha13 : |2 * ρ.a13 * (v.x.re * v.z.re + v.x.im * v.z.im)| ≤ 2 * |ρ.a13| * M :=
    abs_two_coeff_mul_le h_re_xz hM_nn
  have ha23 : |2 * ρ.a23 * (v.y.re * v.z.re + v.y.im * v.z.im)| ≤ 2 * |ρ.a23| * M :=
    abs_two_coeff_mul_le h_re_yz hM_nn
  have hb12 : |-(2 * ρ.b12 * (v.x.re * v.y.im - v.x.im * v.y.re))| ≤ 2 * |ρ.b12| * M := by
    rw [abs_neg]; exact abs_two_coeff_mul_le h_im_xy hM_nn
  have hb13 : |-(2 * ρ.b13 * (v.x.re * v.z.im - v.x.im * v.z.re))| ≤ 2 * |ρ.b13| * M := by
    rw [abs_neg]; exact abs_two_coeff_mul_le h_im_xz hM_nn
  have hb23 : |-(2 * ρ.b23 * (v.y.re * v.z.im - v.y.im * v.z.re))| ≤ 2 * |ρ.b23| * M := by
    rw [abs_neg]; exact abs_two_coeff_mul_le h_im_yz hM_nn
  let t2 := (ρ.d2 - ρ.d1) * v.y.normSq
  let t3 := (ρ.d3 - ρ.d1) * v.z.normSq
  let t4 := 2 * ρ.a12 * (v.x.re * v.y.re + v.x.im * v.y.im)
  let t5 := 2 * ρ.a13 * (v.x.re * v.z.re + v.x.im * v.z.im)
  let t6 := 2 * ρ.a23 * (v.y.re * v.z.re + v.y.im * v.z.im)
  let t7 := -(2 * ρ.b12 * (v.x.re * v.y.im - v.x.im * v.y.re))
  let t8 := -(2 * ρ.b13 * (v.x.re * v.z.im - v.x.im * v.z.re))
  let t9 := -(2 * ρ.b23 * (v.y.re * v.z.im - v.y.im * v.z.re))
  have hrew : quadNum ρ v - ρ.d1 * normSqVec v = t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 := by
    simp only [quadNum, normSqVec, t2, t3, t4, t5, t6, t7, t8, t9]
    ring
  have s1 := abs_add_le (t2 + t3 + t4 + t5 + t6 + t7 + t8) t9
  have s2 := abs_add_le (t2 + t3 + t4 + t5 + t6 + t7) t8
  have s3 := abs_add_le (t2 + t3 + t4 + t5 + t6) t7
  have s4 := abs_add_le (t2 + t3 + t4 + t5) t6
  have s5 := abs_add_le (t2 + t3 + t4) t5
  have s6 := abs_add_le (t2 + t3) t4
  have s7 := abs_add_le t2 t3
  have hsum_M : |t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9| ≤
      (2 * |ρ.d1| + |ρ.d2| + |ρ.d3| + 2 * |ρ.a12| + 2 * |ρ.a13| + 2 * |ρ.a23| +
        2 * |ρ.b12| + 2 * |ρ.b13| + 2 * |ρ.b23|) * M := by
    linarith [s1, s2, s3, s4, s5, s6, s7, hd2, hd3, ha12, ha13, ha23, hb12, hb13, hb23]
  have hle_coeff :
      (2 * |ρ.d1| + |ρ.d2| + |ρ.d3| + 2 * |ρ.a12| + 2 * |ρ.a13| + 2 * |ρ.a23| +
        2 * |ρ.b12| + 2 * |ρ.b13| + 2 * |ρ.b23|) ≤ 2 * ρ.coeffNorm := by
    unfold HermForm3.coeffNorm
    linarith [abs_nonneg ρ.d2, abs_nonneg ρ.d3,
      abs_nonneg ρ.a12, abs_nonneg ρ.a13, abs_nonneg ρ.a23,
      abs_nonneg ρ.b12, abs_nonneg ρ.b13, abs_nonneg ρ.b23]
  have hmul_coeff := mul_le_mul_of_nonneg_right hle_coeff hM_nn
  have h2M : 2 * ρ.coeffNorm * M = 8 * ρ.coeffNorm * θ * normSqVec v := by
    change 2 * ρ.coeffNorm * (4 * θ * normSqVec v) = 8 * ρ.coeffNorm * θ * normSqVec v
    ring
  refine ⟨hN_gt, ?_⟩
  rw [hrew, ← h2M]
  linarith [hsum_M, hmul_coeff]

/-- Positive control for Suite 9A: every quadratic Born-rule Rayleigh function `quadRay ρ`
is archimedean-continuous at `tomo_e1 = (1, 0, 0)`. -/
theorem archimedeanContinuousAt_quadRay_tomo_e1 (ρ : HermForm3) :
    IsArchimedeanContinuousAt (quadRay ρ) tomo_e1 := by
  intro ε hε
  have hC_nn : 0 ≤ ρ.coeffNorm := coeffNorm_nonneg ρ
  have hdenom_pos : 0 < 8 * ρ.coeffNorm + 1 := by linarith
  let θ := min (1 / 2) (ε / (8 * ρ.coeffNorm + 1))
  have hθ_pos : 0 < θ := lt_min (by norm_num) (div_pos hε hdenom_pos)
  have hθ_half : θ ≤ 1 / 2 := min_le_left _ _
  have hθ_eps : θ ≤ ε / (8 * ρ.coeffNorm + 1) := min_le_right _ _
  refine ⟨θ ^ 2, sq_pos_of_pos hθ_pos, ?_⟩
  intro v _ hdist
  obtain ⟨hN_gt, hnum_le⟩ := abs_quadNum_sub_d1_mul_normSqVec_le ρ hθ_pos hθ_half hdist
  have hN_pos : 0 < normSqVec v := by linarith
  have hN_ne : normSqVec v ≠ 0 := ne_of_gt hN_pos
  have hmul : (quadRay ρ v - quadRay ρ tomo_e1) * normSqVec v =
      quadNum ρ v - ρ.d1 * normSqVec v := by
    rw [quadRay_tomo_e1, quadRay, sub_mul, div_mul_cancel₀ _ hN_ne]
  obtain ⟨hl, hu⟩ := abs_le.mp hnum_le
  rw [← hmul] at hl hu
  have hmul_eps : (8 * ρ.coeffNorm + 1) * θ ≤ ε := by
    have h1 := (le_div_iff₀ hdenom_pos).mp hθ_eps
    linarith
  exact abs_lt.mpr ⟨by nlinarith, by nlinarith⟩

/-- Unconditional Archimedean continuity elimination theorem for `s3`: for any `ρ : HermForm3`
and `c : ℚ`, the perturbed ray function `quadRay ρ + c • s3` is archimedean-continuous at
`tomo_e1 = (1, 0, 0)` if and only if `c = 0`. -/
theorem quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff
    (ρ : HermForm3) (c : ℚ) :
    IsArchimedeanContinuousAt (fun v => quadRay ρ v + c * s3 v) tomo_e1 ↔ c = 0 := by
  constructor
  · intro hf_cont
    apply s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1 hf_cont
    have heq : (fun v => (quadRay ρ v + c * s3 v) - c * s3 v) = quadRay ρ := by
      funext v; ring
    rw [heq]
    exact archimedeanContinuousAt_quadRay_tomo_e1 ρ
  · rintro rfl
    have heq : (fun v => quadRay ρ v + 0 * s3 v) = quadRay ρ := by
      funext v; ring
    rw [heq]
    exact archimedeanContinuousAt_quadRay_tomo_e1 ρ

/-! #### 9B. Quadratic Field Extension `ℚ(i, √3)³` Obstruction Eliminating `s3` -/

/-- Elements `a + b √3` of the biquadratic field `ℚ(i, √3)` with `a, b ∈ ℚ(i)`. -/
@[ext]
structure GaussRatSqrt3 where
  a : GaussRat
  b : GaussRat
  deriving DecidableEq

namespace GaussRatSqrt3

def zero : GaussRatSqrt3 := ⟨0, 0⟩
def one : GaussRatSqrt3 := ⟨1, 0⟩
def invSqrt3 : GaussRatSqrt3 := ⟨0, ⟨1 / 3, 0⟩⟩

def ofGaussRat (z : GaussRat) : GaussRatSqrt3 := ⟨z, 0⟩

def add (z w : GaussRatSqrt3) : GaussRatSqrt3 :=
  ⟨z.a + w.a, z.b + w.b⟩

def mul (z w : GaussRatSqrt3) : GaussRatSqrt3 :=
  ⟨z.a * w.a + ⟨3, 0⟩ * (z.b * w.b), z.a * w.b + z.b * w.a⟩

/-- Complex conjugation on `ℚ(i, √3) ⊂ ℂ` fixes `√3 ∈ ℝ` and conjugates `a, b ∈ ℚ(i)`. -/
def conj (z : GaussRatSqrt3) : GaussRatSqrt3 :=
  ⟨star z.a, star z.b⟩

end GaussRatSqrt3

/-- Three-component vectors over `ℚ(i, √3)`. -/
@[ext]
structure GVecSqrt3 where
  x : GaussRatSqrt3
  y : GaussRatSqrt3
  z : GaussRatSqrt3
  deriving DecidableEq

namespace GVecSqrt3

def ofGVec (v : GVec) : GVecSqrt3 :=
  ⟨GaussRatSqrt3.ofGaussRat v.x, GaussRatSqrt3.ofGaussRat v.y, GaussRatSqrt3.ofGaussRat v.z⟩

def smul (c : GaussRatSqrt3) (v : GVecSqrt3) : GVecSqrt3 :=
  ⟨c.mul v.x, c.mul v.y, c.mul v.z⟩

def inner (u v : GVecSqrt3) : GaussRatSqrt3 :=
  ((u.x.conj.mul v.x).add (u.y.conj.mul v.y)).add (u.z.conj.mul v.z)

def normSqRat (u : GVecSqrt3) : ℚ :=
  (inner u u).a.re

def NonZero (u : GVecSqrt3) : Prop :=
  u.x ≠ GaussRatSqrt3.zero ∨ u.y ≠ GaussRatSqrt3.zero ∨ u.z ≠ GaussRatSqrt3.zero

end GVecSqrt3

/-- Orthogonal frames in `ℚ(i, √3)³`. -/
def IsFrameSqrt3 (u v w : GVecSqrt3) : Prop :=
  u.NonZero ∧ v.NonZero ∧ w.NonZero ∧
  GVecSqrt3.inner u v = GaussRatSqrt3.zero ∧
  GVecSqrt3.inner u w = GaussRatSqrt3.zero ∧
  GVecSqrt3.inner v w = GaussRatSqrt3.zero

/-- Zero-weight frame functions on `ℚ(i, √3)³`. -/
def IsZeroWeightFrameFunctionSqrt3 (G : GVecSqrt3 → ℚ) : Prop :=
  ∀ u v w : GVecSqrt3, IsFrameSqrt3 u v w → G u + G v + G w = 0

/-- Over `ℚ(i)³`, no scalar multiple of `witness_111 = (1, 1, 1)` can have unit squared norm `1`. -/
theorem no_unit_norm_smul_witness_111_in_qi3 (l : GaussRat) :
    normSqVec (GVec.smul l witness_111) ≠ 1 := by
  intro h1
  have hl_pos : 0 < l.normSq := by
    by_contra hle
    have h0 : l.normSq = 0 := le_antisymm (not_lt.mp hle) (GaussRat.normSq_nonneg l)
    rw [normSqVec_smul, h0, zero_mul] at h1
    norm_num at h1
  rw [normSqVec_smul, witness_111_normSq] at h1
  have hv := congrArg v3Rat h1
  rw [v3Rat_mul hl_pos (by norm_num : (0 : ℚ) < 3)] at hv
  have hv1 : v3Rat 1 = 0 := rfl
  have hv3 : v3Rat 3 = 1 := rfl
  have heven := v3Rat_normSq_even l
  omega

/-- Over `ℚ(i, √3)³`, scaling `witness_111 = (1, 1, 1)` by `1 / √3` produces a unit-norm vector
on the same ray whose squared norm `1` has even `3`-adic valuation `v_3(1) = 0`. -/
def witness_111_unit_sqrt3 : GVecSqrt3 :=
  GVecSqrt3.smul GaussRatSqrt3.invSqrt3 (GVecSqrt3.ofGVec witness_111)

theorem witness_111_unit_sqrt3_normSq :
    GVecSqrt3.inner witness_111_unit_sqrt3 witness_111_unit_sqrt3 = GaussRatSqrt3.one ∧
    witness_111_unit_sqrt3.normSqRat = 1 ∧
    v3Rat witness_111_unit_sqrt3.normSqRat % 2 = 0 := by
  refine ⟨?_, ?_, ?_⟩
  · (ext <;>
      simp [witness_111_unit_sqrt3, GVecSqrt3.inner, GVecSqrt3.smul, GVecSqrt3.ofGVec,
        GaussRatSqrt3.invSqrt3, GaussRatSqrt3.ofGaussRat, GaussRatSqrt3.one,
        GaussRatSqrt3.add, GaussRatSqrt3.mul, GaussRatSqrt3.conj, witness_111, gv]);
    norm_num
  · simp [GVecSqrt3.normSqRat, witness_111_unit_sqrt3, GVecSqrt3.inner, GVecSqrt3.smul,
      GVecSqrt3.ofGVec, GaussRatSqrt3.invSqrt3, GaussRatSqrt3.ofGaussRat,
      GaussRatSqrt3.add, GaussRatSqrt3.mul, GaussRatSqrt3.conj, witness_111, gv]
    norm_num
  · have h1 : witness_111_unit_sqrt3.normSqRat = 1 := by
      simp [GVecSqrt3.normSqRat, witness_111_unit_sqrt3, GVecSqrt3.inner, GVecSqrt3.smul,
        GVecSqrt3.ofGVec, GaussRatSqrt3.invSqrt3, GaussRatSqrt3.ofGaussRat,
        GaussRatSqrt3.add, GaussRatSqrt3.mul, GaussRatSqrt3.conj, witness_111, gv]
      norm_num
    rw [h1]
    rfl

/-- Embedded witness `(1, 1, 1)` in `ℚ(i, √3)³`. -/
def witness_111_sqrt3 : GVecSqrt3 := GVecSqrt3.ofGVec witness_111

/-- First orthogonal partner `(1 + i + √3, 1 + i - √3, -2 - 2i)` of `witness_111` in `ℚ(i, √3)³`,
with rational squared norm `18 = 2 × 3²` (`v_3(18) = 2`, even). -/
def frameSqrt3_p : GVecSqrt3 :=
  ⟨⟨⟨1, 1⟩, ⟨1, 0⟩⟩, ⟨⟨1, 1⟩, ⟨-1, 0⟩⟩, ⟨⟨-2, -2⟩, ⟨0, 0⟩⟩⟩

/-- Second orthogonal partner `(-1 + (1 - i)√3, -1 - (1 - i)√3, 2)` of `witness_111` in `ℚ(i, √3)³`,
with rational squared norm `18 = 2 × 3²` (`v_3(18) = 2`, even). -/
def frameSqrt3_q : GVecSqrt3 :=
  ⟨⟨⟨-1, 0⟩, ⟨1, -1⟩⟩, ⟨⟨-1, 0⟩, ⟨-1, 1⟩⟩, ⟨⟨2, 0⟩, ⟨0, 0⟩⟩⟩

theorem isFrameSqrt3_witness_111_even_norms :
    IsFrameSqrt3 witness_111_sqrt3 frameSqrt3_p frameSqrt3_q ∧
    witness_111_sqrt3.normSqRat = 3 ∧
    frameSqrt3_p.normSqRat = 18 ∧
    frameSqrt3_q.normSqRat = 18 ∧
    v3Rat frameSqrt3_p.normSqRat % 2 = 0 ∧
    v3Rat frameSqrt3_q.normSqRat % 2 = 0 ∧
    (v3Rat witness_111_sqrt3.normSqRat +
      v3Rat frameSqrt3_p.normSqRat +
      v3Rat frameSqrt3_q.normSqRat) % 2 ≠ 0 := by
  have hnz_u : witness_111_sqrt3.NonZero := by
    left; decide
  have hnz_p : frameSqrt3_p.NonZero := by
    left; decide
  have hnz_q : frameSqrt3_q.NonZero := by
    left; decide
  have huv : GVecSqrt3.inner witness_111_sqrt3 frameSqrt3_p = GaussRatSqrt3.zero := by
    ext <;>
      simp [witness_111_sqrt3, frameSqrt3_p, GVecSqrt3.ofGVec, GaussRatSqrt3.ofGaussRat,
        GVecSqrt3.inner, GaussRatSqrt3.add, GaussRatSqrt3.mul, GaussRatSqrt3.conj,
        GaussRatSqrt3.zero, witness_111, gv] <;>
      norm_num
  have huw : GVecSqrt3.inner witness_111_sqrt3 frameSqrt3_q = GaussRatSqrt3.zero := by
    (ext <;>
      simp [witness_111_sqrt3, frameSqrt3_q, GVecSqrt3.ofGVec, GaussRatSqrt3.ofGaussRat,
        GVecSqrt3.inner, GaussRatSqrt3.add, GaussRatSqrt3.mul, GaussRatSqrt3.conj,
        GaussRatSqrt3.zero, witness_111, gv]);
    norm_num
  have hvw : GVecSqrt3.inner frameSqrt3_p frameSqrt3_q = GaussRatSqrt3.zero := by
    ext <;>
      simp [frameSqrt3_p, frameSqrt3_q, GVecSqrt3.inner, GaussRatSqrt3.add,
        GaussRatSqrt3.mul, GaussRatSqrt3.conj, GaussRatSqrt3.zero] <;>
      norm_num
  have hnu : witness_111_sqrt3.normSqRat = ((3 : ℕ) : ℚ) := by
    simp [GVecSqrt3.normSqRat, witness_111_sqrt3, GVecSqrt3.ofGVec, GaussRatSqrt3.ofGaussRat,
      GVecSqrt3.inner, GaussRatSqrt3.add, GaussRatSqrt3.mul, GaussRatSqrt3.conj,
      witness_111, gv]
    norm_num
  have hnp : frameSqrt3_p.normSqRat = ((18 : ℕ) : ℚ) := by
    simp [GVecSqrt3.normSqRat, frameSqrt3_p, GVecSqrt3.inner, GaussRatSqrt3.add,
      GaussRatSqrt3.mul, GaussRatSqrt3.conj]
    norm_num
  have hnq : frameSqrt3_q.normSqRat = ((18 : ℕ) : ℚ) := by
    simp [GVecSqrt3.normSqRat, frameSqrt3_q, GVecSqrt3.inner, GaussRatSqrt3.add,
      GaussRatSqrt3.mul, GaussRatSqrt3.conj]
    norm_num
  have hv3 : v3Rat witness_111_sqrt3.normSqRat = 1 := by
    rw [hnu, v3Rat_natCast (by decide : 0 < 3)]
    rfl
  have hv18_p : v3Rat frameSqrt3_p.normSqRat = 2 := by
    rw [hnp, v3Rat_natCast (by decide : 0 < 18)]
    rfl
  have hv18_q : v3Rat frameSqrt3_q.normSqRat = 2 := by
    rw [hnq, v3Rat_natCast (by decide : 0 < 18)]
    rfl
  refine ⟨⟨hnz_u, hnz_p, hnz_q, huv, huw, hvw⟩, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact_mod_cast hnu
  · exact_mod_cast hnp
  · exact_mod_cast hnq
  · rw [hv18_p]; rfl
  · rw [hv18_q]; rfl
  · rw [hv3, hv18_p, hv18_q]; decide

/-- Any zero-weight frame function `G` on `ℚ(i, √3)³` that vanishes on vectors whose rational
squared norm has even `3`-adic valuation must vanish on `witness_111 = (1, 1, 1)`, so `s3`
cannot extend to `ℚ(i, √3)³` under the even-`v_3` vanishing rule. -/
theorem zero_on_witness_111_of_sqrt3_even_v3_vanishing
    {G : GVecSqrt3 → ℚ}
    (hG : IsZeroWeightFrameFunctionSqrt3 G)
    (heven : ∀ u : GVecSqrt3, v3Rat u.normSqRat % 2 = 0 → G u = 0) :
    G witness_111_sqrt3 = 0 := by
  obtain ⟨hfr, _, _, _, hp_even, hq_even, _⟩ := isFrameSqrt3_witness_111_even_norms
  have hsum := hG witness_111_sqrt3 frameSqrt3_p frameSqrt3_q hfr
  have hp0 := heven frameSqrt3_p hp_even
  have hq0 := heven frameSqrt3_q hq_even
  linarith

theorem no_s3_even_v3_extension_to_sqrt3 :
    ¬ ∃ G : GVecSqrt3 → ℚ,
        IsZeroWeightFrameFunctionSqrt3 G ∧
        (∀ u : GVecSqrt3, v3Rat u.normSqRat % 2 = 0 → G u = 0) ∧
        (∀ v : GVec, G (GVecSqrt3.ofGVec v) = s3 v) := by
  rintro ⟨G, hG, heven, hext⟩
  have h0 := zero_on_witness_111_of_sqrt3_even_v3_vanishing hG heven
  have h1 := hext witness_111
  rw [s3_witness_111] at h1
  change G witness_111_sqrt3 = 1 at h1
  linarith

/-- Parameterized biquadratic operations on `ℚ(i, √p)³` for general `p : ℚ` (including all
inert primes `p ≡ 3 (mod 4)` such as `p = 3, 7, 11, 19, ...`). -/
def GaussRatSqrt3.invSqrtP (p : ℚ) : GaussRatSqrt3 := ⟨0, ⟨1 / p, 0⟩⟩

def GaussRatSqrt3.mulP (p : ℚ) (z w : GaussRatSqrt3) : GaussRatSqrt3 :=
  ⟨z.a * w.a + ⟨p, 0⟩ * (z.b * w.b), z.a * w.b + z.b * w.a⟩

def GVecSqrt3.smulP (p : ℚ) (c : GaussRatSqrt3) (v : GVecSqrt3) : GVecSqrt3 :=
  ⟨GaussRatSqrt3.mulP p c v.x, GaussRatSqrt3.mulP p c v.y, GaussRatSqrt3.mulP p c v.z⟩

def GVecSqrt3.innerP (p : ℚ) (u v : GVecSqrt3) : GaussRatSqrt3 :=
  ((GaussRatSqrt3.mulP p u.x.conj v.x).add (GaussRatSqrt3.mulP p u.y.conj v.y)).add
    (GaussRatSqrt3.mulP p u.z.conj v.z)

def GVecSqrt3.normSqRatP (p : ℚ) (u : GVecSqrt3) : ℚ :=
  (GVecSqrt3.innerP p u u).a.re

def IsFrameSqrtP (p : ℚ) (u v w : GVecSqrt3) : Prop :=
  u.NonZero ∧ v.NonZero ∧ w.NonZero ∧
  GVecSqrt3.innerP p u v = GaussRatSqrt3.zero ∧
  GVecSqrt3.innerP p u w = GaussRatSqrt3.zero ∧
  GVecSqrt3.innerP p v w = GaussRatSqrt3.zero

/-- Universal unit-norm rescaling theorem in `ℚ(i, √p)³`: for any `p ≠ 0` and any vector
`u ∈ ℚ(i)³` with `normSqVec u = p`, scaling `u` by `1 / √p` in `ℚ(i, √p)³` produces a vector
with `innerP p = 1` and rational squared norm `normSqRatP p = 1`. -/
theorem unit_norm_in_sqrtP_of_normSqVec_eq {p : ℚ} (hp : p ≠ 0) {u : GVec}
    (hu : normSqVec u = p) :
    GVecSqrt3.innerP p
        (GVecSqrt3.smulP p (GaussRatSqrt3.invSqrtP p) (GVecSqrt3.ofGVec u))
        (GVecSqrt3.smulP p (GaussRatSqrt3.invSqrtP p) (GVecSqrt3.ofGVec u)) =
      GaussRatSqrt3.one ∧
    GVecSqrt3.normSqRatP p
        (GVecSqrt3.smulP p (GaussRatSqrt3.invSqrtP p) (GVecSqrt3.ofGVec u)) = 1 := by
  have hns : u.x.re ^ 2 + u.x.im ^ 2 + u.y.re ^ 2 + u.y.im ^ 2 + u.z.re ^ 2 + u.z.im ^ 2 = p := by
    simpa [normSqVec, GaussRat.normSq, add_assoc] using hu
  have hp_inv : p * p⁻¹ = 1 := mul_inv_cancel₀ hp
  have h1 : GVecSqrt3.innerP p
      (GVecSqrt3.smulP p (GaussRatSqrt3.invSqrtP p) (GVecSqrt3.ofGVec u))
      (GVecSqrt3.smulP p (GaussRatSqrt3.invSqrtP p) (GVecSqrt3.ofGVec u)) =
      GaussRatSqrt3.one := by
    ext
    · simp only [GVecSqrt3.innerP, GVecSqrt3.smulP, GVecSqrt3.ofGVec,
        GaussRatSqrt3.invSqrtP, GaussRatSqrt3.ofGaussRat, GaussRatSqrt3.one,
        GaussRatSqrt3.add, GaussRatSqrt3.mulP, GaussRatSqrt3.conj,
        GaussRat.re_add, GaussRat.im_add, GaussRat.re_mul, GaussRat.im_mul,
        GaussRat.re_star, GaussRat.im_star, GaussRat.re_zero, GaussRat.im_zero,
        GaussRat.re_one]
      linear_combination (p * p⁻¹ ^ 2) * hns + (p * p⁻¹ + 1) * hp_inv
    · simp only [GVecSqrt3.innerP, GVecSqrt3.smulP, GVecSqrt3.ofGVec,
        GaussRatSqrt3.invSqrtP, GaussRatSqrt3.ofGaussRat, GaussRatSqrt3.one,
        GaussRatSqrt3.add, GaussRatSqrt3.mulP, GaussRatSqrt3.conj,
        GaussRat.re_add, GaussRat.im_add, GaussRat.re_mul, GaussRat.im_mul,
        GaussRat.re_star, GaussRat.im_star, GaussRat.re_zero, GaussRat.im_zero,
        GaussRat.im_one]
      ring
    · simp only [GVecSqrt3.innerP, GVecSqrt3.smulP, GVecSqrt3.ofGVec,
        GaussRatSqrt3.invSqrtP, GaussRatSqrt3.ofGaussRat, GaussRatSqrt3.one,
        GaussRatSqrt3.add, GaussRatSqrt3.mulP, GaussRatSqrt3.conj,
        GaussRat.re_add, GaussRat.im_add, GaussRat.re_mul, GaussRat.im_mul,
        GaussRat.re_star, GaussRat.im_star, GaussRat.re_zero, GaussRat.im_zero]
      ring
    · simp only [GVecSqrt3.innerP, GVecSqrt3.smulP, GVecSqrt3.ofGVec,
        GaussRatSqrt3.invSqrtP, GaussRatSqrt3.ofGaussRat, GaussRatSqrt3.one,
        GaussRatSqrt3.add, GaussRatSqrt3.mulP, GaussRatSqrt3.conj,
        GaussRat.re_add, GaussRat.im_add, GaussRat.re_mul, GaussRat.im_mul,
        GaussRat.re_star, GaussRat.im_star, GaussRat.re_zero, GaussRat.im_zero]
      ring
  refine ⟨h1, ?_⟩
  simp only [GVecSqrt3.normSqRatP, h1, GaussRatSqrt3.one]
  rfl

/-- First universal four-square SU(2) partner `α (√p v₀) + β w₀` in `ℚ(i, √p)³`. -/
def fourSquarePartnerP (v₀ w₀ : GVec) (α β : GaussRat) : GVecSqrt3 :=
  ⟨⟨β * w₀.x, α * v₀.x⟩, ⟨β * w₀.y, α * v₀.y⟩, ⟨β * w₀.z, α * v₀.z⟩⟩

/-- Second universal four-square SU(2) partner `(star β) (√p v₀) - (star α) w₀` in `ℚ(i, √p)³`. -/
def fourSquarePartnerQ (v₀ w₀ : GVec) (α β : GaussRat) : GVecSqrt3 :=
  ⟨⟨-(star α * w₀.x), star β * v₀.x⟩,
   ⟨-(star α * w₀.y), star β * v₀.y⟩,
   ⟨-(star α * w₀.z), star β * v₀.z⟩⟩

/-- Universal four-square SU(2) orthogonal partner theorem in `ℚ(i, √p)³`: whenever `(u, v₀, w₀)`
are pairwise orthogonal in `ℚ(i)³` with `normSqVec w₀ = p * normSqVec v₀` and `α, β ∈ ℚ(i)` satisfy
the four-square norm identity `α.normSq + β.normSq = p`, the vectors `fourSquarePartnerP v₀ w₀ α β`
and `fourSquarePartnerQ v₀ w₀ α β` are orthogonal to `u` and to each other in `ℚ(i, √p)³` and both
have rational squared norm `p ^ 2 * normSqVec v₀` (shifting `p`-adic valuation from `1` to `2`). -/
theorem fourSquarePartner_ortho_and_normSqRatP {p : ℚ} {u v₀ w₀ : GVec} {α β : GaussRat}
    (huv : GVec.inner u v₀ = 0)
    (huw : GVec.inner u w₀ = 0)
    (hvw : GVec.inner v₀ w₀ = 0)
    (hnorm_w : normSqVec w₀ = p * normSqVec v₀)
    (hab : α.normSq + β.normSq = p) :
    GVecSqrt3.innerP p (GVecSqrt3.ofGVec u) (fourSquarePartnerP v₀ w₀ α β) = GaussRatSqrt3.zero ∧
    GVecSqrt3.innerP p (GVecSqrt3.ofGVec u) (fourSquarePartnerQ v₀ w₀ α β) = GaussRatSqrt3.zero ∧
    GVecSqrt3.innerP p (fourSquarePartnerP v₀ w₀ α β) (fourSquarePartnerQ v₀ w₀ α β) =
      GaussRatSqrt3.zero ∧
    GVecSqrt3.normSqRatP p (fourSquarePartnerP v₀ w₀ α β) = p ^ 2 * normSqVec v₀ ∧
    GVecSqrt3.normSqRatP p (fourSquarePartnerQ v₀ w₀ α β) = p ^ 2 * normSqVec v₀ := by
  have hwv : GVec.inner w₀ v₀ = 0 := inner_eq_zero_symm hvw
  have h1 : GVecSqrt3.innerP p (GVecSqrt3.ofGVec u) (fourSquarePartnerP v₀ w₀ α β) =
      ⟨β * GVec.inner u w₀, α * GVec.inner u v₀⟩ := by
    ext <;>
      simp only [GVecSqrt3.innerP, GVecSqrt3.ofGVec, fourSquarePartnerP,
        GaussRatSqrt3.ofGaussRat, GaussRatSqrt3.add, GaussRatSqrt3.mulP, GaussRatSqrt3.conj,
        GVec.inner, GaussRat.re_add, GaussRat.im_add, GaussRat.re_mul, GaussRat.im_mul,
        GaussRat.re_star, GaussRat.im_star, GaussRat.re_zero, GaussRat.im_zero] <;>
      ring
  have h2 : GVecSqrt3.innerP p (GVecSqrt3.ofGVec u) (fourSquarePartnerQ v₀ w₀ α β) =
      ⟨-(star α * GVec.inner u w₀), star β * GVec.inner u v₀⟩ := by
    ext <;>
      simp only [GVecSqrt3.innerP, GVecSqrt3.ofGVec, fourSquarePartnerQ,
        GaussRatSqrt3.ofGaussRat, GaussRatSqrt3.add, GaussRatSqrt3.mulP, GaussRatSqrt3.conj,
        GVec.inner, GaussRat.re_add, GaussRat.im_add, GaussRat.re_mul, GaussRat.im_mul,
        GaussRat.re_neg, GaussRat.im_neg, GaussRat.re_star, GaussRat.im_star,
        GaussRat.re_zero, GaussRat.im_zero] <;>
      ring
  have h3 : GVecSqrt3.innerP p (fourSquarePartnerP v₀ w₀ α β) (fourSquarePartnerQ v₀ w₀ α β) =
      ⟨-(star β * star α * GVec.inner w₀ w₀) + ⟨p, 0⟩ * (star α * star β * GVec.inner v₀ v₀),
       star β * star β * GVec.inner w₀ v₀ - star α * star α * GVec.inner v₀ w₀⟩ := by
    ext <;>
      simp only [GVecSqrt3.innerP, fourSquarePartnerP, fourSquarePartnerQ,
        GaussRatSqrt3.add, GaussRatSqrt3.mulP, GaussRatSqrt3.conj,
        GVec.inner, GaussRat.re_add, GaussRat.im_add, GaussRat.re_sub, GaussRat.im_sub,
        GaussRat.re_mul, GaussRat.im_mul, GaussRat.re_neg, GaussRat.im_neg,
        GaussRat.re_star, GaussRat.im_star] <;>
      ring
  have h4 : GVecSqrt3.normSqRatP p (fourSquarePartnerP v₀ w₀ α β) =
      β.normSq * normSqVec w₀ + p * α.normSq * normSqVec v₀ := by
    simp only [GVecSqrt3.normSqRatP, GVecSqrt3.innerP, fourSquarePartnerP,
      GaussRatSqrt3.add, GaussRatSqrt3.mulP, GaussRatSqrt3.conj,
      normSqVec, GaussRat.normSq, GaussRat.re_add, GaussRat.re_mul, GaussRat.im_mul,
      GaussRat.re_star, GaussRat.im_star]
    ring
  have h5 : GVecSqrt3.normSqRatP p (fourSquarePartnerQ v₀ w₀ α β) =
      α.normSq * normSqVec w₀ + p * β.normSq * normSqVec v₀ := by
    simp only [GVecSqrt3.normSqRatP, GVecSqrt3.innerP, fourSquarePartnerQ,
      GaussRatSqrt3.add, GaussRatSqrt3.mulP, GaussRatSqrt3.conj,
      normSqVec, GaussRat.normSq, GaussRat.re_add, GaussRat.re_mul, GaussRat.im_mul,
      GaussRat.re_neg, GaussRat.im_neg, GaussRat.re_star, GaussRat.im_star]
    ring
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · rw [h1, huw, huv, mul_zero, mul_zero]; rfl
  · rw [h2, huw, huv, mul_zero, mul_zero, neg_zero]; rfl
  · rw [h3, hwv, hvw, inner_self_eq_normSqVec w₀, inner_self_eq_normSqVec v₀, hnorm_w]
    ext <;>
      simp only [GaussRatSqrt3.zero, GaussRat.re_add, GaussRat.im_add, GaussRat.re_sub,
        GaussRat.im_sub, GaussRat.re_mul, GaussRat.im_mul, GaussRat.re_neg, GaussRat.im_neg,
        GaussRat.re_star, GaussRat.im_star, GaussRat.re_zero, GaussRat.im_zero] <;>
      ring
  · rw [h4, hnorm_w]
    linear_combination (p * normSqVec v₀) * hab
  · rw [h5, hnorm_w]
    linear_combination (p * normSqVec v₀) * hab

/-- Explicit `p = 7` (`7 ≡ 3 (mod 4)`) witness `(1, 2, 1 + i)` of squared norm `7` in `ℚ(i)³`
and its `ℚ(i, √7)³` four-square SU(2) orthogonal frame completion with rational squared norms
`(7, 245, 245) = (7, 5 × 7², 5 × 7²)`. -/
def witness_p7 : GVec := gv 1 0 2 0 1 1
def witness_p7_v0 : GVec := gv 2 0 (-1) 0 0 0
def witness_p7_w0 : GVec := gv 1 (-1) 2 (-2) (-5) 0
def frameSqrt7_p : GVecSqrt3 := fourSquarePartnerP witness_p7_v0 witness_p7_w0 ⟨1, 1⟩ ⟨2, 1⟩
def frameSqrt7_q : GVecSqrt3 := fourSquarePartnerQ witness_p7_v0 witness_p7_w0 ⟨1, 1⟩ ⟨2, 1⟩

theorem isFrameSqrt7_witness_p7_norms :
    IsFrameSqrtP 7 (GVecSqrt3.ofGVec witness_p7) frameSqrt7_p frameSqrt7_q ∧
    GVecSqrt3.normSqRatP 7 (GVecSqrt3.ofGVec witness_p7) = 7 ∧
    GVecSqrt3.normSqRatP 7 frameSqrt7_p = 245 ∧
    GVecSqrt3.normSqRatP 7 frameSqrt7_q = 245 := by
  have hnz_u : (GVecSqrt3.ofGVec witness_p7).NonZero := by
    left; intro h
    have hre : (GVecSqrt3.ofGVec witness_p7).x.a.re = 0 := by rw [h]; rfl
    revert hre; simp [GVecSqrt3.ofGVec, GaussRatSqrt3.ofGaussRat, witness_p7, gv]
  have hnz_p : frameSqrt7_p.NonZero := by
    left; intro h
    have hre : frameSqrt7_p.x.a.re = 0 := by rw [h]; rfl
    revert hre; simp [frameSqrt7_p, fourSquarePartnerP, witness_p7_w0, gv]; norm_num
  have hnz_q : frameSqrt7_q.NonZero := by
    left; intro h
    have hre : frameSqrt7_q.x.b.re = 0 := by rw [h]; rfl
    revert hre; simp [frameSqrt7_q, fourSquarePartnerQ, witness_p7_v0, gv]
  have huv : GVec.inner witness_p7 witness_p7_v0 = 0 := by
    simp only [witness_p7, witness_p7_v0]; gauss_arith
  have huw : GVec.inner witness_p7 witness_p7_w0 = 0 := by
    simp only [witness_p7, witness_p7_w0]; gauss_arith
  have hvw : GVec.inner witness_p7_v0 witness_p7_w0 = 0 := by
    simp only [witness_p7_v0, witness_p7_w0]; gauss_arith
  have hnv : normSqVec witness_p7_v0 = 5 := by
    simp [normSqVec, GaussRat.normSq, witness_p7_v0, gv]; norm_num
  have hnw : normSqVec witness_p7_w0 = 7 * normSqVec witness_p7_v0 := by
    simp [normSqVec, GaussRat.normSq, witness_p7_v0, witness_p7_w0, gv]; norm_num
  have hab : (⟨1, 1⟩ : GaussRat).normSq + (⟨2, 1⟩ : GaussRat).normSq = 7 := by
    simp [GaussRat.normSq]; norm_num
  obtain ⟨h1, h2, h3, hnp, hnq⟩ :=
    fourSquarePartner_ortho_and_normSqRatP (p := 7) huv huw hvw hnw hab
  have hnu : GVecSqrt3.normSqRatP 7 (GVecSqrt3.ofGVec witness_p7) = 7 := by
    simp [GVecSqrt3.normSqRatP, GVecSqrt3.innerP, GVecSqrt3.ofGVec, GaussRatSqrt3.ofGaussRat,
      GaussRatSqrt3.add, GaussRatSqrt3.mulP, GaussRatSqrt3.conj, witness_p7, gv]
    norm_num
  rw [hnv] at hnp hnq
  norm_num at hnp hnq
  exact ⟨⟨hnz_u, hnz_p, hnz_q, h1, h2, h3⟩, hnu, hnp, hnq⟩

/-! #### 9C. Universal Operator-Space Projector-Linearity Criterion Eliminating All Residuals -/

/-- A functional `L : HermForm3 → ℚ` is `ℚ`-linear on `HermForm3`. -/
def IsLinearOnHermForm3 (L : HermForm3 → ℚ) : Prop :=
  (∀ ρ σ : HermForm3, L (HermForm3.add ρ σ) = L ρ + L σ) ∧
  (∀ (c : ℚ) (ρ : HermForm3), L (HermForm3.smul c ρ) = c * L ρ)

/-- A ray function `f : GVec → ℚ` factors linearly through the rank-1 projector map `rayProj`. -/
def FactorsThroughRayProjLinear (f : GVec → ℚ) : Prop :=
  ∃ L : HermForm3 → ℚ, IsLinearOnHermForm3 L ∧ ∀ v : GVec, v.NonZero → f v = L (rayProj v)

theorem quadRay_factorsThroughRayProjLinear (ρ : HermForm3) :
    FactorsThroughRayProjLinear (quadRay ρ) := by
  refine ⟨traceInner ρ, ⟨traceInner_add_right ρ, fun c σ => traceInner_smul_right c ρ σ⟩, ?_⟩
  intro v _
  exact (traceInner_rayProj ρ v).symm

/-- Every residual that vanishes on the nine tomography rays and factors linearly through `rayProj`
vanishes identically on all nonzero rays in `ℚ(i)³` (eliminating `s_p` for all inert primes `p`). -/
theorem zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear
    {g : GVec → ℚ}
    (hvan : VanishesOnNineRays g)
    (hlin : FactorsThroughRayProjLinear g) :
    ∀ v : GVec, v.NonZero → g v = 0 := by
  obtain ⟨L, ⟨hadd, hsmul⟩, hL⟩ := hlin
  obtain ⟨he1, he2, he3, he12, he13, he23, he12i, he13i, he23i⟩ := hvan
  have hLe1 : L (rayProj tomo_e1) = 0 := by rw [← hL tomo_e1 tomo_e1_nonZero, he1]
  have hLe2 : L (rayProj tomo_e2) = 0 := by rw [← hL tomo_e2 tomo_e2_nonZero, he2]
  have hLe3 : L (rayProj tomo_e3) = 0 := by rw [← hL tomo_e3 tomo_e3_nonZero, he3]
  have hLe12 : L (rayProj tomo_e12) = 0 := by rw [← hL tomo_e12 tomo_e12_nonZero, he12]
  have hLe13 : L (rayProj tomo_e13) = 0 := by rw [← hL tomo_e13 tomo_e13_nonZero, he13]
  have hLe23 : L (rayProj tomo_e23) = 0 := by rw [← hL tomo_e23 tomo_e23_nonZero, he23]
  have hLe12i : L (rayProj tomo_e12i) = 0 := by rw [← hL tomo_e12i tomo_e12i_nonZero, he12i]
  have hLe13i : L (rayProj tomo_e13i) = 0 := by rw [← hL tomo_e13i tomo_e13i_nonZero, he13i]
  have hLe23i : L (rayProj tomo_e23i) = 0 := by rw [← hL tomo_e23i tomo_e23i_nonZero, he23i]
  intro v hv
  rw [hL v hv, rayProj_nine_rays_span_hermForm3 (rayProj v)]
  simp only [hadd, hsmul, hLe1, hLe2, hLe3, hLe12, hLe13, hLe23, hLe12i, hLe13i, hLe23i]
  ring

theorem not_factorsThroughRayProjLinear_s3 : ¬ FactorsThroughRayProjLinear s3 := by
  intro hlin
  have h0 := zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear
    s3_vanishes_on_nine_rays hlin witness_111 witness_111_nonZero
  rw [s3_witness_111] at h0
  norm_num at h0

/-- Exact quadratic rigidity theorem on `ℚ(i)³` under operator-space projector linearity:
a frame function `f` on `ℚ(i)³` is of the Born form `quadRay ρ` (`tr ρ = 1`) if and only if
it factors linearly through `rayProj`. -/
theorem quadratic_rigidity_iff_factorsThroughRayProjLinear (f : GVec → ℚ) :
    (IsFrameFunction f ∧ FactorsThroughRayProjLinear f) ↔
    ∃ ρ : HermForm3, ρ.tr = 1 ∧ ∀ v : GVec, v.NonZero → f v = quadRay ρ v := by
  constructor
  · rintro ⟨hf, L, ⟨hadd, hsmul⟩, hL⟩
    refine ⟨tomographyForm f, tomography_trace_one hf, ?_⟩
    intro v hv
    let ρ := tomographyForm f
    have hres_lin : FactorsThroughRayProjLinear (residual f) := by
      refine ⟨fun σ => L σ - traceInner ρ σ, ⟨?_, ?_⟩, ?_⟩
      · intro σ τ
        simp only [hadd, traceInner_add_right]
        ring
      · intro c σ
        simp only [hsmul, traceInner_smul_right]
        ring
      · intro u hu
        unfold residual
        rw [hL u hu, ← traceInner_rayProj]
    have h0 := zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear
      (residual_vanishes_on_nine_rays f) hres_lin v hv
    unfold residual at h0
    linarith
  · rintro ⟨ρ, htr, hρ⟩
    refine ⟨?_, ?_⟩
    · intro u v w hfr
      rw [hρ u hfr.1, hρ v hfr.2.1, hρ w hfr.2.2.1]
      exact quadRay_isFrameFunction ρ htr u v w hfr
    · refine ⟨traceInner ρ, ⟨traceInner_add_right ρ, fun c σ => traceInner_smul_right c ρ σ⟩, ?_⟩
      intro v hv
      rw [hρ v hv, traceInner_rayProj]

/-! #### 9D. Multi-Prime `7`-Adic Residual `s7`, Linear Independence, and Joint Elimination -/

/-- Bounded-fuel helper for the `7`-adic valuation of a natural number. -/
def v7NatAux : ℕ → ℕ → ℕ
  | 0, _ => 0
  | fuel + 1, n => if 0 < n ∧ n % 7 = 0 then v7NatAux fuel (n / 7) + 1 else 0

/-- Bounded-fuel helper for the prime-to-`7` part of a natural number. -/
def p7PartNatAux : ℕ → ℕ → ℕ
  | 0, n => n
  | fuel + 1, n => if 0 < n ∧ n % 7 = 0 then p7PartNatAux fuel (n / 7) else n

/-- Number of factors of `7` in a natural number `n` (`0` if `n = 0`). -/
def v7Nat (n : ℕ) : ℕ := v7NatAux n n

/-- Prime-to-`7` part of a natural number `n` (`0` if `n = 0`). -/
def p7PartNat (n : ℕ) : ℕ := p7PartNatAux n n

theorem v7NatAux_spec : ∀ fuel n : ℕ, 7 ^ v7NatAux fuel n * p7PartNatAux fuel n = n
  | 0, n => by simp [v7NatAux, p7PartNatAux]
  | fuel + 1, n => by
      simp only [v7NatAux, p7PartNatAux]
      split_ifs with h
      · have heq := v7NatAux_spec fuel (n / 7)
        have hdiv : 7 * (n / 7) = n := Nat.mul_div_cancel' (Nat.dvd_of_mod_eq_zero h.2)
        calc
          7 ^ (v7NatAux fuel (n / 7) + 1) * p7PartNatAux fuel (n / 7)
              = 7 * (7 ^ v7NatAux fuel (n / 7) * p7PartNatAux fuel (n / 7)) := by ring
          _ = 7 * (n / 7) := by rw [heq]
          _ = n := hdiv
      · ring

theorem v7Nat_spec (n : ℕ) : 7 ^ v7Nat n * p7PartNat n = n :=
  v7NatAux_spec n n

theorem p7PartNatAux_mod_seven_ne_zero :
    ∀ fuel n : ℕ, 0 < n → n ≤ fuel → p7PartNatAux fuel n % 7 ≠ 0
  | 0, n, hn, hle => by omega
  | fuel + 1, n, hn, hle => by
      simp only [p7PartNatAux]
      split_ifs with h
      · have hpos : 0 < n / 7 := by omega
        have hle' : n / 7 ≤ fuel := by omega
        exact p7PartNatAux_mod_seven_ne_zero fuel (n / 7) hpos hle'
      · omega

theorem p7PartNat_mod_seven_ne_zero {n : ℕ} (hn : 0 < n) : p7PartNat n % 7 ≠ 0 :=
  p7PartNatAux_mod_seven_ne_zero n n hn (le_refl n)

theorem p7PartNat_pos {n : ℕ} (hn : 0 < n) : 0 < p7PartNat n := by
  have hmod := p7PartNat_mod_seven_ne_zero hn
  omega

theorem pow_seven_mul_unique :
    ∀ a b m k : ℕ, m % 7 ≠ 0 → k % 7 ≠ 0 → 7 ^ a * m = 7 ^ b * k → a = b ∧ m = k
  | 0, 0, m, k, _, _, heq => by
      simp only [pow_zero, one_mul] at heq
      exact ⟨rfl, heq⟩
  | 0, b + 1, m, k, hm, _, heq => by
      have hm0 : m % 7 = 0 := by
        have h1 : m = 7 ^ b * k * 7 := by
          simp only [pow_zero, one_mul, pow_succ] at heq
          linarith
        omega
      exact False.elim (hm hm0)
  | a + 1, 0, m, k, _, hk, heq => by
      have hk0 : k % 7 = 0 := by
        have h1 : k = 7 ^ a * m * 7 := by
          simp only [pow_zero, one_mul, pow_succ] at heq
          linarith
        omega
      exact False.elim (hk hk0)
  | a + 1, b + 1, m, k, hm, hk, heq => by
      have heq' : 7 ^ a * m = 7 ^ b * k := by
        simp only [pow_succ] at heq
        linarith
      obtain ⟨hab, hmk⟩ := pow_seven_mul_unique a b m k hm hk heq'
      exact ⟨congrArg (· + 1) hab, hmk⟩

theorem v7Nat_p7PartNat_eq_of_pow_mul {n a m : ℕ} (hm : m % 7 ≠ 0) (heq : 7 ^ a * m = n) :
    v7Nat n = a ∧ p7PartNat n = m := by
  have hm_pos : 0 < m := by omega
  have hpow_pos : 0 < 7 ^ a := pow_pos (by decide : 0 < 7) a
  have hn : 0 < n := by nlinarith
  exact pow_seven_mul_unique (v7Nat n) a (p7PartNat n) m
    (p7PartNat_mod_seven_ne_zero hn) hm ((v7Nat_spec n).trans heq.symm)

theorem mul_mod_seven_ne_zero {a b : ℕ} (ha : a % 7 ≠ 0) (hb : b % 7 ≠ 0) :
    (a * b) % 7 ≠ 0 := by
  rw [Nat.mul_mod]
  have ha7 : a % 7 = 1 ∨ a % 7 = 2 ∨ a % 7 = 3 ∨ a % 7 = 4 ∨ a % 7 = 5 ∨ a % 7 = 6 := by omega
  have hb7 : b % 7 = 1 ∨ b % 7 = 2 ∨ b % 7 = 3 ∨ b % 7 = 4 ∨ b % 7 = 5 ∨ b % 7 = 6 := by omega
  rcases ha7 with h1 | h1 | h1 | h1 | h1 | h1 <;>
    rcases hb7 with h2 | h2 | h2 | h2 | h2 | h2 <;>
    simp [h1, h2]

/-- Quadratic-residue predicate modulo `7` (`m % 7 ∈ {1, 2, 4}`). -/
def isQrMod7 (m : ℕ) : Prop :=
  m % 7 = 1 ∨ m % 7 = 2 ∨ m % 7 = 4

instance (m : ℕ) : Decidable (isQrMod7 m) :=
  inferInstanceAs (Decidable (m % 7 = 1 ∨ m % 7 = 2 ∨ m % 7 = 4))

/-- Legendre symbol `(m / 7) ∈ {-1, 1}` on `ℕ` (evaluated on `m % 7`). -/
def chi7Nat (m : ℕ) : ℚ :=
  if isQrMod7 m then 1 else -1

theorem chi7Nat_mod_seven (m : ℕ) : chi7Nat (m % 7) = chi7Nat m := by
  have h : isQrMod7 (m % 7) ↔ isQrMod7 m := by simp [isQrMod7]
  simp only [chi7Nat, h]

theorem chi7Nat_values (m : ℕ) : chi7Nat m = 1 ∨ chi7Nat m = -1 := by
  unfold chi7Nat
  split_ifs with h
  · exact Or.inl rfl
  · exact Or.inr rfl

theorem chi7Nat_sq (m : ℕ) : chi7Nat m * chi7Nat m = 1 := by
  rcases chi7Nat_values m with h | h <;> rw [h] <;> ring

theorem chi7Nat_mul {a b : ℕ} (ha : a % 7 ≠ 0) (hb : b % 7 ≠ 0) :
    chi7Nat (a * b) = chi7Nat a * chi7Nat b := by
  rw [← chi7Nat_mod_seven (a * b), Nat.mul_mod, ← chi7Nat_mod_seven a, ← chi7Nat_mod_seven b]
  have ha7 : a % 7 = 1 ∨ a % 7 = 2 ∨ a % 7 = 3 ∨ a % 7 = 4 ∨ a % 7 = 5 ∨ a % 7 = 6 := by omega
  have hb7 : b % 7 = 1 ∨ b % 7 = 2 ∨ b % 7 = 3 ∨ b % 7 = 4 ∨ b % 7 = 5 ∨ b % 7 = 6 := by omega
  rcases ha7 with h1 | h1 | h1 | h1 | h1 | h1 <;>
    rcases hb7 with h2 | h2 | h2 | h2 | h2 | h2 <;>
    simp [h1, h2, chi7Nat, isQrMod7]

theorem chi7Nat_eq_of_mul_eq {a b c d : ℕ}
    (ha : a % 7 ≠ 0) (hb : b % 7 ≠ 0) (hc : c % 7 ≠ 0) (hd : d % 7 ≠ 0)
    (heq : a * b = c * d) :
    chi7Nat (a * d) = chi7Nat (c * b) := by
  have hmul : chi7Nat a * chi7Nat b = chi7Nat c * chi7Nat d := by
    rw [← chi7Nat_mul ha hb, ← chi7Nat_mul hc hd, heq]
  have hsq_b := chi7Nat_sq b
  have hsq_d := chi7Nat_sq d
  rw [chi7Nat_mul ha hd, chi7Nat_mul hc hb]
  linear_combination
    (chi7Nat b * chi7Nat d) * hmul -
    (chi7Nat a * chi7Nat d) * hsq_b +
    (chi7Nat c * chi7Nat b) * hsq_d

theorem chi7Nat_add_cancel {a b : ℕ} (_ha : a % 7 ≠ 0) (_hb : b % 7 ≠ 0)
    (hsum : (a + b) % 7 = 0) :
    chi7Nat a + chi7Nat b = 0 := by
  rw [← chi7Nat_mod_seven a, ← chi7Nat_mod_seven b]
  rw [Nat.add_mod] at hsum
  have ha7 : a % 7 = 1 ∨ a % 7 = 2 ∨ a % 7 = 3 ∨ a % 7 = 4 ∨ a % 7 = 5 ∨ a % 7 = 6 := by omega
  have hb7 : b % 7 = 1 ∨ b % 7 = 2 ∨ b % 7 = 3 ∨ b % 7 = 4 ∨ b % 7 = 5 ∨ b % 7 = 6 := by omega
  rcases ha7 with h1 | h1 | h1 | h1 | h1 | h1 <;>
    rcases hb7 with h2 | h2 | h2 | h2 | h2 | h2 <;>
    simp [h1, h2, chi7Nat, isQrMod7] at hsum ⊢

theorem v7Nat_p7PartNat_mul {m k : ℕ} (hm : 0 < m) (hk : 0 < k) :
    v7Nat (m * k) = v7Nat m + v7Nat k ∧
    p7PartNat (m * k) = p7PartNat m * p7PartNat k := by
  apply v7Nat_p7PartNat_eq_of_pow_mul
    (mul_mod_seven_ne_zero (p7PartNat_mod_seven_ne_zero hm) (p7PartNat_mod_seven_ne_zero hk))
  calc
    7 ^ (v7Nat m + v7Nat k) * (p7PartNat m * p7PartNat k)
        = (7 ^ v7Nat m * p7PartNat m) * (7 ^ v7Nat k * p7PartNat k) := by ring
    _ = m * k := by rw [v7Nat_spec m, v7Nat_spec k]

theorem v7Nat_add_of_lt {X Y : ℕ} (hX : 0 < X) (_hY : 0 < Y) (hlt : v7Nat X < v7Nat Y) :
    v7Nat (X + Y) = v7Nat X ∧ p7PartNat (X + Y) % 7 = p7PartNat X % 7 := by
  let d := v7Nat Y - v7Nat X - 1
  have hb : v7Nat Y = v7Nat X + (d + 1) := by omega
  let m := p7PartNat X + 7 ^ (d + 1) * p7PartNat Y
  have hm_mod : m % 7 = p7PartNat X % 7 := by
    have hpow : (7 ^ (d + 1) * p7PartNat Y) % 7 = 0 := by
      have h1 : 7 ^ (d + 1) * p7PartNat Y = 7 * (7 ^ d * p7PartNat Y) := by ring
      rw [h1, Nat.mul_mod_right]
    omega
  have hm_ne : m % 7 ≠ 0 := by
    rw [hm_mod]
    exact p7PartNat_mod_seven_ne_zero hX
  have heq : 7 ^ v7Nat X * m = X + Y := by
    calc
      7 ^ v7Nat X * m
          = 7 ^ v7Nat X * p7PartNat X + 7 ^ (v7Nat X + (d + 1)) * p7PartNat Y := by
            simp only [m, pow_add]; ring
      _ = 7 ^ v7Nat X * p7PartNat X + 7 ^ v7Nat Y * p7PartNat Y := by rw [← hb]
      _ = X + Y := by rw [v7Nat_spec X, v7Nat_spec Y]
  obtain ⟨hv, hp⟩ := v7Nat_p7PartNat_eq_of_pow_mul hm_ne heq
  exact ⟨hv, by rw [hp, hm_mod]⟩

theorem v7Nat_add_gt_imp_eq_and_mod_seven {X Y : ℕ} (hX : 0 < X) (hY : 0 < Y)
    (hgt : v7Nat X < v7Nat (X + Y)) :
    v7Nat X = v7Nat Y ∧ (p7PartNat X + p7PartNat Y) % 7 = 0 := by
  have heq_v : v7Nat X = v7Nat Y := by
    rcases lt_trichotomy (v7Nat X) (v7Nat Y) with hlt | heq | hlt
    · have h1 := (v7Nat_add_of_lt hX hY hlt).1
      omega
    · exact heq
    · have h1 := (v7Nat_add_of_lt hY hX hlt).1
      rw [Nat.add_comm Y X] at h1
      omega
  refine ⟨heq_v, ?_⟩
  by_contra hmod
  have heq_sum : 7 ^ v7Nat X * (p7PartNat X + p7PartNat Y) = X + Y := by
    calc
      7 ^ v7Nat X * (p7PartNat X + p7PartNat Y)
          = 7 ^ v7Nat X * p7PartNat X + 7 ^ v7Nat Y * p7PartNat Y := by
            rw [← heq_v]; ring
      _ = X + Y := by rw [v7Nat_spec X, v7Nat_spec Y]
  have hv := (v7Nat_p7PartNat_eq_of_pow_mul hmod heq_sum).1
  omega

theorem v7Nat_add_ge_min {X Y : ℕ} (hX : 0 < X) (hY : 0 < Y) :
    min (v7Nat X) (v7Nat Y) ≤ v7Nat (X + Y) := by
  rcases lt_trichotomy (v7Nat X) (v7Nat Y) with hlt | heq | hlt
  · have h1 := (v7Nat_add_of_lt hX hY hlt).1
    omega
  · have hsum_pos : 0 < p7PartNat X + p7PartNat Y := by
      have hpX := p7PartNat_pos hX
      omega
    have hpow_pos : 0 < 7 ^ v7Nat X := pow_pos (by decide : 0 < 7) (v7Nat X)
    have heq_sum : X + Y = 7 ^ v7Nat X * (p7PartNat X + p7PartNat Y) := by
      calc
        X + Y = 7 ^ v7Nat X * p7PartNat X + 7 ^ v7Nat Y * p7PartNat Y := by
          rw [v7Nat_spec X, v7Nat_spec Y]
        _ = 7 ^ v7Nat X * (p7PartNat X + p7PartNat Y) := by
          rw [← heq]; ring
    have hv_pow : v7Nat (7 ^ v7Nat X) = v7Nat X := by
      exact (v7Nat_p7PartNat_eq_of_pow_mul (m := 1) (by decide) (by ring)).1
    have hv_mul := (v7Nat_p7PartNat_mul hpow_pos hsum_pos).1
    rw [heq_sum, hv_mul, hv_pow]
    omega
  · have h1 := (v7Nat_add_of_lt hY hX hlt).1
    rw [Nat.add_comm Y X] at h1
    omega

theorem sq_add_sq_mod_seven_eq_zero_iff (x y : ℕ) :
    (x ^ 2 + y ^ 2) % 7 = 0 ↔ x % 7 = 0 ∧ y % 7 = 0 := by
  simp only [sq]
  rw [Nat.add_mod, Nat.mul_mod x x, Nat.mul_mod y y]
  have hx : x % 7 = 0 ∨ x % 7 = 1 ∨ x % 7 = 2 ∨ x % 7 = 3 ∨
      x % 7 = 4 ∨ x % 7 = 5 ∨ x % 7 = 6 := by omega
  have hy : y % 7 = 0 ∨ y % 7 = 1 ∨ y % 7 = 2 ∨ y % 7 = 3 ∨
      y % 7 = 4 ∨ y % 7 = 5 ∨ y % 7 = 6 := by omega
  rcases hx with hx | hx | hx | hx | hx | hx | hx <;>
    rcases hy with hy | hy | hy | hy | hy | hy | hy <;>
    simp [hx, hy]

theorem v7Nat_sq_add_sq_even (x y : ℕ) : v7Nat (x ^ 2 + y ^ 2) % 2 = 0 := by
  have hmain : ∀ s : ℕ, ∀ a b : ℕ, a + b = s → v7Nat (a ^ 2 + b ^ 2) % 2 = 0 := by
    intro s
    induction s using Nat.strong_induction_on with
    | h s ih =>
      intro a b hab
      by_cases h0 : a = 0 ∧ b = 0
      · rcases h0 with ⟨rfl, rfl⟩
        rfl
      · have hpos : 0 < a ^ 2 + b ^ 2 := by
          rcases not_and_or.mp h0 with ha | hb
          · have : 0 < a := by omega
            nlinarith
          · have : 0 < b := by omega
            nlinarith
        by_cases hmod : (a ^ 2 + b ^ 2) % 7 = 0
        · obtain ⟨ha7, hb7⟩ := (sq_add_sq_mod_seven_eq_zero_iff a b).mp hmod
          have ha_eq : a = 7 * (a / 7) := (Nat.mul_div_cancel' (Nat.dvd_of_mod_eq_zero ha7)).symm
          have hb_eq : b = 7 * (b / 7) := (Nat.mul_div_cancel' (Nat.dvd_of_mod_eq_zero hb7)).symm
          have hsub_pos : 0 < (a / 7) ^ 2 + (b / 7) ^ 2 := by nlinarith
          have hsq_eq : a ^ 2 + b ^ 2 = 49 * ((a / 7) ^ 2 + (b / 7) ^ 2) := by
            calc
              a ^ 2 + b ^ 2 = (7 * (a / 7)) ^ 2 + (7 * (b / 7)) ^ 2 := by
                rw [← ha_eq, ← hb_eq]
              _ = 49 * ((a / 7) ^ 2 + (b / 7) ^ 2) := by ring
          have hv49 : v7Nat 49 = 2 := rfl
          have hmul := (v7Nat_p7PartNat_mul (by decide : 0 < 49) hsub_pos).1
          have hlt_s : a / 7 + b / 7 < s := by omega
          have hrec := ih (a / 7 + b / 7) hlt_s (a / 7) (b / 7) rfl
          rw [hsq_eq, hmul, hv49]
          omega
        · have hv0 :=
            (v7Nat_p7PartNat_eq_of_pow_mul (n := a ^ 2 + b ^ 2) (a := 0) (m := a ^ 2 + b ^ 2)
              hmod (by ring)).1
          rw [hv0]
  exact hmain (x + y) x y rfl

/-- `7`-adic valuation of a positive rational `q` (`0` if `q ≤ 0`). -/
def v7Rat (q : ℚ) : ℤ :=
  if 0 < q then (v7Nat q.num.natAbs : ℤ) - (v7Nat q.den : ℤ) else 0

/-- `7`-adic Legendre unit sign `∈ {-1, 1}` of a positive rational `q` (`0` if `q ≤ 0`). -/
def u7Rat (q : ℚ) : ℚ :=
  if 0 < q then chi7Nat (p7PartNat q.num.natAbs * p7PartNat q.den) else 0

theorem v7Rat_u7Rat_of_nat_div {q : ℚ} {n d : ℕ} (hn : 0 < n) (hd : 0 < d)
    (hq : q = (n : ℚ) / (d : ℚ)) :
    0 < q ∧
    v7Rat q = (v7Nat n : ℤ) - (v7Nat d : ℤ) ∧
    u7Rat q = chi7Nat (p7PartNat n * p7PartNat d) := by
  have hn_q : 0 < (n : ℚ) := by exact_mod_cast hn
  have hd_q : 0 < (d : ℚ) := by exact_mod_cast hd
  have hq_pos : 0 < q := by
    rw [hq]
    exact div_pos hn_q hd_q
  obtain ⟨hnum_pos, hden_pos, hq_can⟩ := rat_pos_eq_natAbs_div_den hq_pos
  have hden_q : (q.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hden_pos)
  have hd_ne : (d : ℚ) ≠ 0 := ne_of_gt hd_q
  have hcross_q : (q.num.natAbs : ℚ) * (d : ℚ) = (n : ℚ) * (q.den : ℚ) := by
    have heq_div : (q.num.natAbs : ℚ) / (q.den : ℚ) = (n : ℚ) / (d : ℚ) :=
      hq_can.symm.trans hq
    exact (div_eq_div_iff hden_q hd_ne).mp heq_div
  have hcross : q.num.natAbs * d = n * q.den := by
    exact_mod_cast hcross_q
  obtain ⟨hv1, hp1⟩ := v7Nat_p7PartNat_mul hnum_pos hd
  obtain ⟨hv2, hp2⟩ := v7Nat_p7PartNat_mul hn hden_pos
  have hv_eq : v7Nat q.num.natAbs + v7Nat d = v7Nat n + v7Nat q.den := by
    rw [← hv1, ← hv2, hcross]
  have hp_eq : p7PartNat q.num.natAbs * p7PartNat d = p7PartNat n * p7PartNat q.den := by
    rw [← hp1, ← hp2, hcross]
  have hchi_eq :
      chi7Nat (p7PartNat q.num.natAbs * p7PartNat q.den) =
      chi7Nat (p7PartNat n * p7PartNat d) :=
    chi7Nat_eq_of_mul_eq
      (p7PartNat_mod_seven_ne_zero hnum_pos)
      (p7PartNat_mod_seven_ne_zero hd)
      (p7PartNat_mod_seven_ne_zero hn)
      (p7PartNat_mod_seven_ne_zero hden_pos)
      hp_eq
  refine ⟨hq_pos, ?_, ?_⟩
  · simp only [v7Rat, hq_pos, ↓reduceIte]
    omega
  · simp only [u7Rat, hq_pos, ↓reduceIte, hchi_eq]

theorem v7Rat_natCast {n : ℕ} (hn : 0 < n) : v7Rat (n : ℚ) = (v7Nat n : ℤ) := by
  have h :=
    (v7Rat_u7Rat_of_nat_div (q := (n : ℚ)) (n := n) (d := 1) hn (by decide : 0 < 1) (by simp)).2.1
  have hv1 : v7Nat 1 = 0 := rfl
  omega

theorem u7Rat_natCast {n : ℕ} (hn : 0 < n) :
    u7Rat (n : ℚ) = chi7Nat (p7PartNat n) := by
  have h :=
    (v7Rat_u7Rat_of_nat_div (q := (n : ℚ)) (n := n) (d := 1) hn (by decide : 0 < 1) (by simp)).2.2
  have hp1 : p7PartNat 1 = 1 := rfl
  simp [h, hp1]

theorem u7Rat_values_of_pos {q : ℚ} (hq : 0 < q) : u7Rat q = 1 ∨ u7Rat q = -1 := by
  simp only [u7Rat, hq, ↓reduceIte]
  exact chi7Nat_values _

theorem u7Rat_sq_of_pos {q : ℚ} (hq : 0 < q) : u7Rat q * u7Rat q = 1 := by
  rcases u7Rat_values_of_pos hq with h | h <;> rw [h] <;> ring

theorem v7Rat_mul {p q : ℚ} (hp : 0 < p) (hq : 0 < q) :
    v7Rat (p * q) = v7Rat p + v7Rat q := by
  obtain ⟨hnp, hdp, hp_eq⟩ := rat_pos_eq_natAbs_div_den hp
  obtain ⟨hnq, hdq, hq_eq⟩ := rat_pos_eq_natAbs_div_den hq
  have hmul_eq : p * q = ((p.num.natAbs * q.num.natAbs : ℕ) : ℚ) / ((p.den * q.den : ℕ) : ℚ) := by
    push_cast
    rw [← div_mul_div_comm, ← hp_eq, ← hq_eq]
  have hvpq := (v7Rat_u7Rat_of_nat_div (Nat.mul_pos hnp hnq) (Nat.mul_pos hdp hdq) hmul_eq).2.1
  have hvp := (v7Rat_u7Rat_of_nat_div hnp hdp hp_eq).2.1
  have hvq := (v7Rat_u7Rat_of_nat_div hnq hdq hq_eq).2.1
  have hvn := (v7Nat_p7PartNat_mul hnp hnq).1
  have hvd := (v7Nat_p7PartNat_mul hdp hdq).1
  rw [hvpq, hvp, hvq, hvn, hvd]
  omega

theorem u7Rat_mul {p q : ℚ} (hp : 0 < p) (hq : 0 < q) :
    u7Rat (p * q) = u7Rat p * u7Rat q := by
  obtain ⟨hnp, hdp, hp_eq⟩ := rat_pos_eq_natAbs_div_den hp
  obtain ⟨hnq, hdq, hq_eq⟩ := rat_pos_eq_natAbs_div_den hq
  have hmul_eq : p * q = ((p.num.natAbs * q.num.natAbs : ℕ) : ℚ) / ((p.den * q.den : ℕ) : ℚ) := by
    push_cast
    rw [← div_mul_div_comm, ← hp_eq, ← hq_eq]
  have hupq := (v7Rat_u7Rat_of_nat_div (Nat.mul_pos hnp hnq) (Nat.mul_pos hdp hdq) hmul_eq).2.2
  have hup := (v7Rat_u7Rat_of_nat_div hnp hdp hp_eq).2.2
  have huq := (v7Rat_u7Rat_of_nat_div hnq hdq hq_eq).2.2
  have hpn := (v7Nat_p7PartNat_mul hnp hnq).2
  have hpd := (v7Nat_p7PartNat_mul hdp hdq).2
  rw [hupq, hup, huq, hpn, hpd]
  have hmp_ne : (p7PartNat p.num.natAbs * p7PartNat p.den) % 7 ≠ 0 :=
    mul_mod_seven_ne_zero (p7PartNat_mod_seven_ne_zero hnp) (p7PartNat_mod_seven_ne_zero hdp)
  have hmq_ne : (p7PartNat q.num.natAbs * p7PartNat q.den) % 7 ≠ 0 :=
    mul_mod_seven_ne_zero (p7PartNat_mod_seven_ne_zero hnq) (p7PartNat_mod_seven_ne_zero hdq)
  have hcomm :
      p7PartNat p.num.natAbs * p7PartNat q.num.natAbs * (p7PartNat p.den * p7PartNat q.den) =
      (p7PartNat p.num.natAbs * p7PartNat p.den) * (p7PartNat q.num.natAbs * p7PartNat q.den) := by
    ring
  rw [hcomm, chi7Nat_mul hmp_ne hmq_ne]

theorem v7Rat_add_of_lt {p q : ℚ} (hp : 0 < p) (hq : 0 < q) (hlt : v7Rat p < v7Rat q) :
    v7Rat (p + q) = v7Rat p ∧ u7Rat (p + q) = u7Rat p := by
  obtain ⟨hnp, hdp, hp_eq⟩ := rat_pos_eq_natAbs_div_den hp
  obtain ⟨hnq, hdq, hq_eq⟩ := rat_pos_eq_natAbs_div_den hq
  let X := p.num.natAbs * q.den
  let Y := q.num.natAbs * p.den
  let D := p.den * q.den
  have hX : 0 < X := Nat.mul_pos hnp hdq
  have hY : 0 < Y := Nat.mul_pos hnq hdp
  have hD : 0 < D := Nat.mul_pos hdp hdq
  have hp_D : p = (X : ℚ) / (D : ℚ) := by
    have hdq_ne : (q.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdq)
    simp only [X, D, Nat.cast_mul]
    rw [mul_div_mul_right _ _ hdq_ne, ← hp_eq]
  have hq_D : q = (Y : ℚ) / (D : ℚ) := by
    have hdp_ne : (p.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdp)
    simp only [Y, D, Nat.cast_mul]
    rw [mul_comm (p.den : ℚ) (q.den : ℚ), mul_div_mul_right _ _ hdp_ne, ← hq_eq]
  have hpq_D : p + q = ((X + Y : ℕ) : ℚ) / (D : ℚ) := by
    rw [hp_D, hq_D, Nat.cast_add, add_div]
  obtain ⟨_, hvp, hup⟩ := v7Rat_u7Rat_of_nat_div hX hD hp_D
  obtain ⟨_, hvq, _⟩ := v7Rat_u7Rat_of_nat_div hY hD hq_D
  obtain ⟨_, hvpq, hupq⟩ := v7Rat_u7Rat_of_nat_div (Nat.add_pos_left hX Y) hD hpq_D
  have hlt_nat : v7Nat X < v7Nat Y := by omega
  obtain ⟨hv_add, hp_add⟩ := v7Nat_add_of_lt hX hY hlt_nat
  refine ⟨by omega, ?_⟩
  rw [hupq, hup, ← chi7Nat_mod_seven (p7PartNat (X + Y) * p7PartNat D),
    ← chi7Nat_mod_seven (p7PartNat X * p7PartNat D)]
  have hmod_mul : (p7PartNat (X + Y) * p7PartNat D) % 7 = (p7PartNat X * p7PartNat D) % 7 := by
    rw [Nat.mul_mod, hp_add, ← Nat.mul_mod]
  rw [hmod_mul]

theorem v7Rat_add_gt_imp_eq_and_u7Rat_cancel {p q : ℚ} (hp : 0 < p) (hq : 0 < q)
    (hgt : v7Rat p < v7Rat (p + q)) :
    v7Rat p = v7Rat q ∧ u7Rat p + u7Rat q = 0 := by
  obtain ⟨hnp, hdp, hp_eq⟩ := rat_pos_eq_natAbs_div_den hp
  obtain ⟨hnq, hdq, hq_eq⟩ := rat_pos_eq_natAbs_div_den hq
  let X := p.num.natAbs * q.den
  let Y := q.num.natAbs * p.den
  let D := p.den * q.den
  have hX : 0 < X := Nat.mul_pos hnp hdq
  have hY : 0 < Y := Nat.mul_pos hnq hdp
  have hD : 0 < D := Nat.mul_pos hdp hdq
  have hp_D : p = (X : ℚ) / (D : ℚ) := by
    have hdq_ne : (q.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdq)
    simp only [X, D, Nat.cast_mul]
    rw [mul_div_mul_right _ _ hdq_ne, ← hp_eq]
  have hq_D : q = (Y : ℚ) / (D : ℚ) := by
    have hdp_ne : (p.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdp)
    simp only [Y, D, Nat.cast_mul]
    rw [mul_comm (p.den : ℚ) (q.den : ℚ), mul_div_mul_right _ _ hdp_ne, ← hq_eq]
  have hpq_D : p + q = ((X + Y : ℕ) : ℚ) / (D : ℚ) := by
    rw [hp_D, hq_D, Nat.cast_add, add_div]
  obtain ⟨_, hvp, hup⟩ := v7Rat_u7Rat_of_nat_div hX hD hp_D
  obtain ⟨_, hvq, huq⟩ := v7Rat_u7Rat_of_nat_div hY hD hq_D
  obtain ⟨_, hvpq, _⟩ := v7Rat_u7Rat_of_nat_div (Nat.add_pos_left hX Y) hD hpq_D
  have hgt_nat : v7Nat X < v7Nat (X + Y) := by omega
  obtain ⟨hv_eq, hp_sum⟩ := v7Nat_add_gt_imp_eq_and_mod_seven hX hY hgt_nat
  refine ⟨by omega, ?_⟩
  rw [hup, huq]
  have hpX_ne := p7PartNat_mod_seven_ne_zero hX
  have hpY_ne := p7PartNat_mod_seven_ne_zero hY
  have hpD_ne := p7PartNat_mod_seven_ne_zero hD
  rw [chi7Nat_mul hpX_ne hpD_ne, chi7Nat_mul hpY_ne hpD_ne]
  have hcancel := chi7Nat_add_cancel hpX_ne hpY_ne hp_sum
  linear_combination chi7Nat (p7PartNat D) * hcancel

theorem v7Rat_add_ge_min {p q : ℚ} (hp : 0 < p) (hq : 0 < q) :
    min (v7Rat p) (v7Rat q) ≤ v7Rat (p + q) := by
  obtain ⟨hnp, hdp, hp_eq⟩ := rat_pos_eq_natAbs_div_den hp
  obtain ⟨hnq, hdq, hq_eq⟩ := rat_pos_eq_natAbs_div_den hq
  let X := p.num.natAbs * q.den
  let Y := q.num.natAbs * p.den
  let D := p.den * q.den
  have hX : 0 < X := Nat.mul_pos hnp hdq
  have hY : 0 < Y := Nat.mul_pos hnq hdp
  have hD : 0 < D := Nat.mul_pos hdp hdq
  have hp_D : p = (X : ℚ) / (D : ℚ) := by
    have hdq_ne : (q.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdq)
    simp only [X, D, Nat.cast_mul]
    rw [mul_div_mul_right _ _ hdq_ne, ← hp_eq]
  have hq_D : q = (Y : ℚ) / (D : ℚ) := by
    have hdp_ne : (p.den : ℚ) ≠ 0 := ne_of_gt (by exact_mod_cast hdp)
    simp only [Y, D, Nat.cast_mul]
    rw [mul_comm (p.den : ℚ) (q.den : ℚ), mul_div_mul_right _ _ hdp_ne, ← hq_eq]
  have hpq_D : p + q = ((X + Y : ℕ) : ℚ) / (D : ℚ) := by
    rw [hp_D, hq_D, Nat.cast_add, add_div]
  obtain ⟨_, hvp, _⟩ := v7Rat_u7Rat_of_nat_div hX hD hp_D
  obtain ⟨_, hvq, _⟩ := v7Rat_u7Rat_of_nat_div hY hD hq_D
  obtain ⟨_, hvpq, _⟩ := v7Rat_u7Rat_of_nat_div (Nat.add_pos_left hX Y) hD hpq_D
  have hmin := v7Nat_add_ge_min hX hY
  omega

/-- Every Gaussian rational `z ∈ ℚ(i)` has even `7`-adic squared-norm valuation `v_7(|z|²)`. -/
theorem v7Rat_normSq_even (z : GaussRat) : v7Rat z.normSq % 2 = 0 := by
  by_cases hpos : 0 < z.normSq
  · let X := z.re.num.natAbs * z.im.den
    let Y := z.im.num.natAbs * z.re.den
    let D := z.re.den * z.im.den
    have hD1 : 0 < D := Nat.mul_pos z.re.den_pos z.im.den_pos
    have hD_pos : 0 < D * D := Nat.mul_pos hD1 hD1
    have hre_den_sq_ne : ((z.re.den * z.re.den : ℕ) : ℚ) ≠ 0 :=
      ne_of_gt (by exact_mod_cast Nat.mul_pos z.re.den_pos z.re.den_pos)
    have him_den_sq_ne : ((z.im.den * z.im.den : ℕ) : ℚ) ≠ 0 :=
      ne_of_gt (by exact_mod_cast Nat.mul_pos z.im.den_pos z.im.den_pos)
    have hnorm_eq : z.normSq = ((X ^ 2 + Y ^ 2 : ℕ) : ℚ) / ((D * D : ℕ) : ℚ) := by
      simp only [GaussRat.normSq]
      rw [rat_sq_eq_natAbs_sq_div_den_sq z.re, rat_sq_eq_natAbs_sq_div_den_sq z.im,
        div_add_div _ _ hre_den_sq_ne him_den_sq_ne]
      simp only [X, Y, D]
      push_cast
      ring
    have hXY_pos : 0 < X ^ 2 + Y ^ 2 := by
      by_contra hle
      have h0 : X ^ 2 + Y ^ 2 = 0 := by omega
      rw [h0] at hnorm_eq
      simp at hnorm_eq
      linarith
    have hv := (v7Rat_u7Rat_of_nat_div hXY_pos hD_pos hnorm_eq).2.1
    have hvD := (v7Nat_p7PartNat_mul hD1 hD1).1
    have heven := v7Nat_sq_add_sq_even X Y
    rw [hv, hvD]
    omega
  · simp only [v7Rat, hpos, ↓reduceIte]
    rfl

theorem four_term_v7Rat_cancel {A B C D : ℚ}
    (hA : 0 < A) (hB_nn : 0 ≤ B) (hC_nn : 0 ≤ C) (_hD : 0 < D)
    (hsum : A + B + C = D)
    (hA_odd : v7Rat A % 2 ≠ 0)
    (hB_odd : 0 < B → v7Rat B % 2 ≠ 0)
    (hC_even : v7Rat C % 2 = 0)
    (hlt_D : v7Rat A < v7Rat D) :
    0 < B ∧ v7Rat A = v7Rat B ∧ u7Rat A + u7Rat B = 0 := by
  have hAB_pos : 0 < A + B := by linarith
  have hAB_gt : v7Rat A < v7Rat (A + B) := by
    by_contra hle
    have hle' : v7Rat (A + B) ≤ v7Rat A := not_lt.mp hle
    have hAB_odd : v7Rat (A + B) % 2 ≠ 0 := by
      rcases eq_or_lt_of_le hB_nn with rfl | hB_pos
      · simp [hA_odd]
      · rcases lt_or_ge (v7Rat B) (v7Rat A) with hlt_BA | hge_BA
        · have hvBA := (v7Rat_add_of_lt hB_pos hA hlt_BA).1
          rw [add_comm] at hvBA
          rw [hvBA]
          exact hB_odd hB_pos
        · have hmin := v7Rat_add_ge_min hA hB_pos
          have heq_AB : v7Rat (A + B) = v7Rat A := by omega
          rw [heq_AB]
          exact hA_odd
    have hAB_lt_D : v7Rat (A + B) < v7Rat (A + B + C) := by
      rw [hsum]
      omega
    rcases eq_or_lt_of_le hC_nn with rfl | hC_pos
    · simp at hAB_lt_D
    · have hv_eq := (v7Rat_add_gt_imp_eq_and_u7Rat_cancel hAB_pos hC_pos hAB_lt_D).1
      omega
  rcases eq_or_lt_of_le hB_nn with rfl | hB_pos
  · simp at hAB_gt
  · obtain ⟨hv_eq, hu_sum⟩ := v7Rat_add_gt_imp_eq_and_u7Rat_cancel hA hB_pos hAB_gt
    exact ⟨hB_pos, hv_eq, hu_sum⟩

/-- On any orthogonal frame `(u, v, w)` in `ℚ(i)³`, the sum of `7`-adic squared-norm
valuations is even. -/
theorem frame_v7Rat_sum_even {u v w : GVec} (hf : IsFrame u v w) :
    (v7Rat (normSqVec u) + v7Rat (normSqVec v) + v7Rat (normSqVec w)) % 2 = 0 := by
  have hu := normSqVec_pos_of_nonZero hf.1
  have hv := normSqVec_pos_of_nonZero hf.2.1
  have hw := normSqVec_pos_of_nonZero hf.2.2.1
  have hdet := detGVec_normSq_of_frame hf
  have hmul1 := v7Rat_mul (mul_pos hu hv) hw
  have hmul2 := v7Rat_mul hu hv
  have heven := v7Rat_normSq_even (detGVec u v w)
  rw [hdet, hmul1, hmul2] at heven
  exact heven

/-- Whether a coordinate `z : GaussRat` is `7`-leading in `u : GVec`. -/
def isLead7Coord (z : GaussRat) (u : GVec) : Prop :=
  0 < z.normSq ∧ v7Rat z.normSq < v7Rat (normSqVec u)

instance (z : GaussRat) (u : GVec) : Decidable (isLead7Coord z u) :=
  inferInstanceAs (Decidable (0 < z.normSq ∧ v7Rat z.normSq < v7Rat (normSqVec u)))

/-- The `7`-adic contribution `u7Rat z.normSq * u7Rat (normSqVec u)` of a coordinate `z` in `u`. -/
def coordSign7 (z : GaussRat) (u : GVec) : ℚ :=
  u7Rat z.normSq * u7Rat (normSqVec u)

/-- Explicit global `{-1, 0, 1}`-valued `7`-adic frame residual on `ℚ(i)³`. -/
def s7 (u : GVec) : ℚ :=
  if v7Rat (normSqVec u) % 2 = 0 then 0
  else if isLead7Coord u.x u then coordSign7 u.x u
  else if isLead7Coord u.y u then coordSign7 u.y u
  else coordSign7 u.z u

theorem pos_of_v7Rat_mod_two_ne_zero {q : ℚ} (h : v7Rat q % 2 ≠ 0) : 0 < q := by
  by_contra hle
  simp [v7Rat, hle] at h

theorem v7Rat_add_gt_of_nonneg {a b : ℚ} {V : ℤ}
    (ha_nn : 0 ≤ a) (hb_nn : 0 ≤ b)
    (ha : 0 < a → V < v7Rat a) (hb : 0 < b → V < v7Rat b)
    (hab : 0 < a + b) : V < v7Rat (a + b) := by
  rcases eq_or_lt_of_le ha_nn with rfl | ha_pos
  · simp at hab ⊢
    exact hb hab
  · rcases eq_or_lt_of_le hb_nn with rfl | hb_pos
    · simp at hab ⊢
      exact ha ha_pos
    · have h1 := ha ha_pos
      have h2 := hb hb_pos
      have hmin := v7Rat_add_ge_min ha_pos hb_pos
      omega

theorem exists_lead7Coord_of_odd {u : GVec} (hodd : v7Rat (normSqVec u) % 2 ≠ 0) :
    isLead7Coord u.x u ∨ isLead7Coord u.y u ∨ isLead7Coord u.z u := by
  by_contra hnot
  rcases not_or.mp hnot with ⟨hx_not, hyz_not⟩
  rcases not_or.mp hyz_not with ⟨hy_not, hz_not⟩
  have hpos : 0 < normSqVec u := pos_of_v7Rat_mod_two_ne_zero hodd
  have hx_gt : 0 < u.x.normSq → v7Rat (normSqVec u) < v7Rat u.x.normSq := by
    intro hx_pos
    have hnot_lt : ¬ v7Rat u.x.normSq < v7Rat (normSqVec u) := fun hlt => hx_not ⟨hx_pos, hlt⟩
    have heven := v7Rat_normSq_even u.x
    omega
  have hy_gt : 0 < u.y.normSq → v7Rat (normSqVec u) < v7Rat u.y.normSq := by
    intro hy_pos
    have hnot_lt : ¬ v7Rat u.y.normSq < v7Rat (normSqVec u) := fun hlt => hy_not ⟨hy_pos, hlt⟩
    have heven := v7Rat_normSq_even u.y
    omega
  have hz_gt : 0 < u.z.normSq → v7Rat (normSqVec u) < v7Rat u.z.normSq := by
    intro hz_pos
    have hnot_lt : ¬ v7Rat u.z.normSq < v7Rat (normSqVec u) := fun hlt => hz_not ⟨hz_pos, hlt⟩
    have heven := v7Rat_normSq_even u.z
    omega
  have hxy_gt : 0 < u.x.normSq + u.y.normSq →
      v7Rat (normSqVec u) < v7Rat (u.x.normSq + u.y.normSq) :=
    v7Rat_add_gt_of_nonneg (GaussRat.normSq_nonneg u.x) (GaussRat.normSq_nonneg u.y) hx_gt hy_gt
  have hxyz_gt : v7Rat (normSqVec u) < v7Rat (u.x.normSq + u.y.normSq + u.z.normSq) :=
    v7Rat_add_gt_of_nonneg
      (add_nonneg (GaussRat.normSq_nonneg u.x) (GaussRat.normSq_nonneg u.y))
      (GaussRat.normSq_nonneg u.z) hxy_gt hz_gt hpos
  change v7Rat (normSqVec u) < v7Rat (normSqVec u) at hxyz_gt
  omega

theorem lead7Coord_x_ortho_imp {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v7Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v7Rat (normSqVec v) % 2 ≠ 0)
    (hlead : isLead7Coord u.x u) :
    isLead7Coord v.x v ∧ coordSign7 u.x u + coordSign7 v.x v = 0 := by
  have hu_pos : 0 < normSqVec u := pos_of_v7Rat_mod_two_ne_zero hu_odd
  have hv_pos : 0 < normSqVec v := pos_of_v7Rat_mod_two_ne_zero hv_odd
  let A := u.x.normSq * normSqVec v
  let B := v.x.normSq * normSqVec u
  let C := (u.y * v.z - v.y * u.z).normSq
  let D := normSqVec u * normSqVec v
  have hA : 0 < A := mul_pos hlead.1 hv_pos
  have hB_nn : 0 ≤ B := mul_nonneg (GaussRat.normSq_nonneg v.x) (le_of_lt hu_pos)
  have hC_nn : 0 ≤ C := GaussRat.normSq_nonneg _
  have hD : 0 < D := mul_pos hu_pos hv_pos
  have hsum : A + B + C = D := ortho_coord_identity_x huv
  have hvA : v7Rat A = v7Rat u.x.normSq + v7Rat (normSqVec v) := v7Rat_mul hlead.1 hv_pos
  have hvD : v7Rat D = v7Rat (normSqVec u) + v7Rat (normSqVec v) := v7Rat_mul hu_pos hv_pos
  have hA_odd : v7Rat A % 2 ≠ 0 := by
    have heven := v7Rat_normSq_even u.x
    omega
  have hB_odd : 0 < B → v7Rat B % 2 ≠ 0 := by
    intro hB_pos
    have hvx_pos : 0 < v.x.normSq := by nlinarith
    have hvB : v7Rat B = v7Rat v.x.normSq + v7Rat (normSqVec u) := v7Rat_mul hvx_pos hu_pos
    have heven := v7Rat_normSq_even v.x
    omega
  have hC_even : v7Rat C % 2 = 0 := v7Rat_normSq_even _
  have hlt_D : v7Rat A < v7Rat D := by
    have hlt := hlead.2
    omega
  obtain ⟨hB_pos, hvAB, huAB⟩ :=
    four_term_v7Rat_cancel hA hB_nn hC_nn hD hsum hA_odd hB_odd hC_even hlt_D
  have hvx_pos : 0 < v.x.normSq := by nlinarith
  have hvB : v7Rat B = v7Rat v.x.normSq + v7Rat (normSqVec u) := v7Rat_mul hvx_pos hu_pos
  have hvx_lt : v7Rat v.x.normSq < v7Rat (normSqVec v) := by
    have hlt := hlead.2
    omega
  refine ⟨⟨hvx_pos, hvx_lt⟩, ?_⟩
  have huA : u7Rat A = u7Rat u.x.normSq * u7Rat (normSqVec v) := u7Rat_mul hlead.1 hv_pos
  have huB : u7Rat B = u7Rat v.x.normSq * u7Rat (normSqVec u) := u7Rat_mul hvx_pos hu_pos
  rw [huA, huB] at huAB
  have hsq_u := u7Rat_sq_of_pos hu_pos
  have hsq_v := u7Rat_sq_of_pos hv_pos
  simp only [coordSign7]
  linear_combination
    (u7Rat (normSqVec u) * u7Rat (normSqVec v)) * huAB -
    (u7Rat u.x.normSq * u7Rat (normSqVec u)) * hsq_v -
    (u7Rat v.x.normSq * u7Rat (normSqVec v)) * hsq_u

theorem lead7Coord_x_ortho_iff {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v7Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v7Rat (normSqVec v) % 2 ≠ 0) :
    isLead7Coord u.x u ↔ isLead7Coord v.x v :=
  ⟨fun h => (lead7Coord_x_ortho_imp huv hu_odd hv_odd h).1,
   fun h => (lead7Coord_x_ortho_imp (inner_eq_zero_symm huv) hv_odd hu_odd h).1⟩

theorem isLead7Coord_rotVec_x (u : GVec) :
    isLead7Coord (rotVec u).x (rotVec u) ↔ isLead7Coord u.y u := by
  unfold isLead7Coord
  rw [normSqVec_rotVec]
  rfl

theorem coordSign7_rotVec_x (u : GVec) :
    coordSign7 (rotVec u).x (rotVec u) = coordSign7 u.y u := by
  unfold coordSign7
  rw [normSqVec_rotVec]
  rfl

theorem isLead7Coord_rotVec_y (u : GVec) :
    isLead7Coord (rotVec u).y (rotVec u) ↔ isLead7Coord u.z u := by
  unfold isLead7Coord
  rw [normSqVec_rotVec]
  rfl

theorem coordSign7_rotVec_y (u : GVec) :
    coordSign7 (rotVec u).y (rotVec u) = coordSign7 u.z u := by
  unfold coordSign7
  rw [normSqVec_rotVec]
  rfl

theorem lead7Coord_y_ortho_imp {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v7Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v7Rat (normSqVec v) % 2 ≠ 0)
    (hlead : isLead7Coord u.y u) :
    isLead7Coord v.y v ∧ coordSign7 u.y u + coordSign7 v.y v = 0 := by
  have huv' : GVec.inner (rotVec u) (rotVec v) = 0 := by rw [inner_rotVec]; exact huv
  have hu_odd' : v7Rat (normSqVec (rotVec u)) % 2 ≠ 0 := by rw [normSqVec_rotVec]; exact hu_odd
  have hv_odd' : v7Rat (normSqVec (rotVec v)) % 2 ≠ 0 := by rw [normSqVec_rotVec]; exact hv_odd
  have hlead' : isLead7Coord (rotVec u).x (rotVec u) := (isLead7Coord_rotVec_x u).mpr hlead
  obtain ⟨hv_lead, hsum⟩ := lead7Coord_x_ortho_imp huv' hu_odd' hv_odd' hlead'
  rw [isLead7Coord_rotVec_x] at hv_lead
  rw [coordSign7_rotVec_x, coordSign7_rotVec_x] at hsum
  exact ⟨hv_lead, hsum⟩

theorem lead7Coord_y_ortho_iff {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v7Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v7Rat (normSqVec v) % 2 ≠ 0) :
    isLead7Coord u.y u ↔ isLead7Coord v.y v :=
  ⟨fun h => (lead7Coord_y_ortho_imp huv hu_odd hv_odd h).1,
   fun h => (lead7Coord_y_ortho_imp (inner_eq_zero_symm huv) hv_odd hu_odd h).1⟩

theorem lead7Coord_z_ortho_imp {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v7Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v7Rat (normSqVec v) % 2 ≠ 0)
    (hlead : isLead7Coord u.z u) :
    isLead7Coord v.z v ∧ coordSign7 u.z u + coordSign7 v.z v = 0 := by
  have huv' : GVec.inner (rotVec u) (rotVec v) = 0 := by rw [inner_rotVec]; exact huv
  have hu_odd' : v7Rat (normSqVec (rotVec u)) % 2 ≠ 0 := by rw [normSqVec_rotVec]; exact hu_odd
  have hv_odd' : v7Rat (normSqVec (rotVec v)) % 2 ≠ 0 := by rw [normSqVec_rotVec]; exact hv_odd
  have hlead' : isLead7Coord (rotVec u).y (rotVec u) := (isLead7Coord_rotVec_y u).mpr hlead
  obtain ⟨hv_lead, hsum⟩ := lead7Coord_y_ortho_imp huv' hu_odd' hv_odd' hlead'
  rw [isLead7Coord_rotVec_y] at hv_lead
  rw [coordSign7_rotVec_y, coordSign7_rotVec_y] at hsum
  exact ⟨hv_lead, hsum⟩

/-- Any two orthogonal vectors in `ℚ(i)³` with odd `7`-adic squared-norm valuation
have opposite `s7` signs (`s7 u + s7 v = 0`). -/
theorem s7_orthogonal_odd_cancel {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v7Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v7Rat (normSqVec v) % 2 ≠ 0) :
    s7 u + s7 v = 0 := by
  have hx_iff := lead7Coord_x_ortho_iff huv hu_odd hv_odd
  have hy_iff := lead7Coord_y_ortho_iff huv hu_odd hv_odd
  simp only [s7, hu_odd, hv_odd, ↓reduceIte]
  by_cases hx : isLead7Coord u.x u
  · have hvx : isLead7Coord v.x v := hx_iff.mp hx
    simp only [hx, hvx, ↓reduceIte]
    exact (lead7Coord_x_ortho_imp huv hu_odd hv_odd hx).2
  · have hvx : ¬ isLead7Coord v.x v := fun h => hx (hx_iff.mpr h)
    simp only [hx, hvx, ↓reduceIte]
    by_cases hy : isLead7Coord u.y u
    · have hvy : isLead7Coord v.y v := hy_iff.mp hy
      simp only [hy, hvy, ↓reduceIte]
      exact (lead7Coord_y_ortho_imp huv hu_odd hv_odd hy).2
    · have hvy : ¬ isLead7Coord v.y v := fun h => hy (hy_iff.mpr h)
      simp only [hy, hvy, ↓reduceIte]
      have hz : isLead7Coord u.z u := by
        rcases exists_lead7Coord_of_odd hu_odd with h1 | h2 | h3
        · exact False.elim (hx h1)
        · exact False.elim (hy h2)
        · exact h3
      exact (lead7Coord_z_ortho_imp huv hu_odd hv_odd hz).2

theorem s7_eq_zero_of_even {u : GVec} (heven : v7Rat (normSqVec u) % 2 = 0) : s7 u = 0 := by
  simp [s7, heven]

/-- `s7` is a global zero-weight frame function on all orthogonal frames in `ℚ(i)³`. -/
theorem s7_isZeroWeightFrameFunction : IsZeroWeightFrameFunction s7 := by
  intro u v w hf
  have hsum_even := frame_v7Rat_sum_even hf
  obtain ⟨_, _, _, huv, huw, hvw⟩ := hf
  by_cases hu : v7Rat (normSqVec u) % 2 = 0 <;>
    by_cases hv : v7Rat (normSqVec v) % 2 = 0 <;>
    by_cases hw : v7Rat (normSqVec w) % 2 = 0
  · rw [s7_eq_zero_of_even hu, s7_eq_zero_of_even hv, s7_eq_zero_of_even hw]
    ring
  · omega
  · omega
  · have hvw_sum := s7_orthogonal_odd_cancel hvw hv hw
    rw [s7_eq_zero_of_even hu]
    linarith
  · omega
  · have huw_sum := s7_orthogonal_odd_cancel huw hu hw
    rw [s7_eq_zero_of_even hv]
    linarith
  · have huv_sum := s7_orthogonal_odd_cancel huv hu hv
    rw [s7_eq_zero_of_even hw]
    linarith
  · omega

theorem s7_smul {v : GVec} (hv : v.NonZero) {l : GaussRat} (hl : l ≠ 0) :
    s7 (GVec.smul l v) = s7 v :=
  zeroWeightFrameFunction_smul s7_isZeroWeightFrameFunction hv hl

theorem coordSign7_values {z : GaussRat} {u : GVec} (hz : 0 < z.normSq) (hu : 0 < normSqVec u) :
    coordSign7 z u = 1 ∨ coordSign7 z u = -1 := by
  simp only [coordSign7]
  rcases u7Rat_values_of_pos hz with h1 | h1 <;>
    rcases u7Rat_values_of_pos hu with h2 | h2 <;>
    rw [h1, h2] <;> norm_num

theorem s7_values (u : GVec) : s7 u = 0 ∨ s7 u = 1 ∨ s7 u = -1 := by
  by_cases heven : v7Rat (normSqVec u) % 2 = 0
  · exact Or.inl (s7_eq_zero_of_even heven)
  · have hu : 0 < normSqVec u := pos_of_v7Rat_mod_two_ne_zero heven
    simp only [s7, heven, ↓reduceIte]
    by_cases hx : isLead7Coord u.x u
    · simp only [hx, ↓reduceIte]
      exact Or.inr (coordSign7_values hx.1 hu)
    · simp only [hx, ↓reduceIte]
      by_cases hy : isLead7Coord u.y u
      · simp only [hy, ↓reduceIte]
        exact Or.inr (coordSign7_values hy.1 hu)
      · simp only [hy, ↓reduceIte]
        have hz : isLead7Coord u.z u := by
          rcases exists_lead7Coord_of_odd heven with h1 | h2 | h3
          · exact False.elim (hx h1)
          · exact False.elim (hy h2)
          · exact h3
        exact Or.inr (coordSign7_values hz.1 hu)

theorem s7_abs_le_one (u : GVec) : |s7 u| ≤ 1 := by
  rcases s7_values u with h | h | h <;> rw [h] <;> norm_num

theorem s7_isBoundedOnRays : IsBoundedOnRays s7 :=
  ⟨1, by norm_num, fun v _ => s7_abs_le_one v⟩

theorem s7_eq_zero_of_normSqVec_natCast {u : GVec} {n : ℕ}
    (hn : 0 < n) (hnorm : normSqVec u = (n : ℚ)) (heven : (v7Nat n : ℤ) % 2 = 0) :
    s7 u = 0 := by
  apply s7_eq_zero_of_even
  rw [hnorm, v7Rat_natCast hn]
  exact heven

theorem s7_eq_of_lead7Coord_x {u : GVec} {n nx : ℕ}
    (hn : 0 < n) (hnx : 0 < nx)
    (hnorm : normSqVec u = (n : ℚ))
    (hx : u.x.normSq = (nx : ℚ))
    (hodd : (v7Nat n : ℤ) % 2 ≠ 0)
    (hlt : (v7Nat nx : ℤ) < (v7Nat n : ℤ)) :
    s7 u = chi7Nat (p7PartNat nx) * chi7Nat (p7PartNat n) := by
  have hvn : v7Rat (normSqVec u) = (v7Nat n : ℤ) := by rw [hnorm, v7Rat_natCast hn]
  have hvx : v7Rat u.x.normSq = (v7Nat nx : ℤ) := by rw [hx, v7Rat_natCast hnx]
  have hun : u7Rat (normSqVec u) = chi7Nat (p7PartNat n) := by rw [hnorm, u7Rat_natCast hn]
  have hux : u7Rat u.x.normSq = chi7Nat (p7PartNat nx) := by rw [hx, u7Rat_natCast hnx]
  have hx_pos : 0 < u.x.normSq := by rw [hx]; exact_mod_cast hnx
  have hlead : isLead7Coord u.x u := ⟨hx_pos, by omega⟩
  have hodd_u : v7Rat (normSqVec u) % 2 ≠ 0 := by omega
  simp only [s7, hodd_u, hlead, ↓reduceIte, coordSign7, hux, hun]

theorem s7_eq_of_lead7Coord_y {u : GVec} {n nx ny : ℕ}
    (hn : 0 < n) (hnx : 0 < nx) (hny : 0 < ny)
    (hnorm : normSqVec u = (n : ℚ))
    (hx : u.x.normSq = (nx : ℚ))
    (hy : u.y.normSq = (ny : ℚ))
    (hodd : (v7Nat n : ℤ) % 2 ≠ 0)
    (hge_x : (v7Nat n : ℤ) ≤ (v7Nat nx : ℤ))
    (hlt_y : (v7Nat ny : ℤ) < (v7Nat n : ℤ)) :
    s7 u = chi7Nat (p7PartNat ny) * chi7Nat (p7PartNat n) := by
  have hvn : v7Rat (normSqVec u) = (v7Nat n : ℤ) := by rw [hnorm, v7Rat_natCast hn]
  have hvx : v7Rat u.x.normSq = (v7Nat nx : ℤ) := by rw [hx, v7Rat_natCast hnx]
  have hvy : v7Rat u.y.normSq = (v7Nat ny : ℤ) := by rw [hy, v7Rat_natCast hny]
  have hun : u7Rat (normSqVec u) = chi7Nat (p7PartNat n) := by rw [hnorm, u7Rat_natCast hn]
  have huy : u7Rat u.y.normSq = chi7Nat (p7PartNat ny) := by rw [hy, u7Rat_natCast hny]
  have hy_pos : 0 < u.y.normSq := by rw [hy]; exact_mod_cast hny
  have hnot_x : ¬ isLead7Coord u.x u := by
    intro ⟨_, hlt⟩
    omega
  have hlead_y : isLead7Coord u.y u := ⟨hy_pos, by omega⟩
  have hodd_u : v7Rat (normSqVec u) % 2 ≠ 0 := by omega
  simp only [s7, hodd_u, hnot_x, hlead_y, ↓reduceIte, coordSign7, huy, hun]

/-- `s7` vanishes on all nine tomography rays (`N ∈ {1, 2}` has `v_7(N) = 0`). -/
theorem s7_vanishes_on_nine_rays : VanishesOnNineRays s7 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact s7_eq_zero_of_normSqVec_natCast (n := 1) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e1, gv]) rfl
  · exact s7_eq_zero_of_normSqVec_natCast (n := 1) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e2, gv]) rfl
  · exact s7_eq_zero_of_normSqVec_natCast (n := 1) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e3, gv]) rfl
  · exact s7_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e12, gv]; norm_num) rfl
  · exact s7_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e13, gv]; norm_num) rfl
  · exact s7_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e23, gv]; norm_num) rfl
  · exact s7_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e12i, gv]; norm_num) rfl
  · exact s7_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e13i, gv]; norm_num) rfl
  · exact s7_eq_zero_of_normSqVec_natCast (n := 2) (by decide)
      (by simp [normSqVec, GaussRat.normSq, tomo_e23i, gv]; norm_num) rfl

theorem witness_p7_primitive : IsOnePlusIPrimitive 1 0 2 0 1 1 := by decide

theorem witness_p7_nonZero : witness_p7.NonZero := by
  left
  intro h
  have hre : witness_p7.x.re = 0 := by rw [h]; rfl
  revert hre
  decide

theorem witness_p7_normSq : normSqVec witness_p7 = 7 := by
  simp [normSqVec, GaussRat.normSq, witness_p7, gv]
  norm_num

theorem s7_witness_111 : s7 witness_111 = 0 :=
  s7_eq_zero_of_normSqVec_natCast (n := 3) (by decide)
    (by simp [normSqVec, GaussRat.normSq, witness_111, gv]; norm_num) rfl

theorem s3_witness_p7 : s3 witness_p7 = 0 :=
  s3_eq_zero_of_normSqVec_natCast (n := 7) (by decide)
    (by simp [normSqVec, GaussRat.normSq, witness_p7, gv]; norm_num) rfl

theorem s7_witness_p7 : s7 witness_p7 = 1 := by
  rw [s7_eq_of_lead7Coord_x (n := 7) (nx := 1) (by decide) (by decide)
    (by simp [normSqVec, GaussRat.normSq, witness_p7, gv]; norm_num)
    (by simp [GaussRat.normSq, witness_p7, gv])
    (by decide) (by decide)]
  have hp1 : p7PartNat 1 = 1 := rfl
  have hp7 : p7PartNat 7 = 1 := rfl
  simp [hp1, hp7, chi7Nat, isQrMod7]

/-- Dual Kronecker-delta evaluation of `(s3, s7)` on `(witness_111, witness_p7)`:
`s3(1,1,1) = 1, s7(1,1,1) = 0` and `s3(1,2,1+i) = 0, s7(1,2,1+i) = 1`. -/
theorem s3_s7_dual_on_witnesses :
    s3 witness_111 = 1 ∧ s7 witness_111 = 0 ∧
    s3 witness_p7 = 0 ∧ s7 witness_p7 = 1 :=
  ⟨s3_witness_111, s7_witness_111, s3_witness_p7, s7_witness_p7⟩

/-- Second explicit `{0, 1/3, 2/3}`-valued nonnegative non-quadratic frame function `(1 + s7 v) / 3`
on `ℚ(i)³` (which agrees with `quadRay (I/3)` on all 9 tomography rays and on `witness_111`,
yet separates `witness_p7`). -/
def exoticQi7 (v : GVec) : ℚ := (1 + s7 v) / 3

theorem exoticQi7_values (v : GVec) :
    exoticQi7 v = 1 / 3 ∨ exoticQi7 v = 2 / 3 ∨ exoticQi7 v = 0 := by
  simp only [exoticQi7]
  rcases s7_values v with h | h | h <;> rw [h] <;> norm_num

theorem exoticQi7_bounds (v : GVec) : 0 ≤ exoticQi7 v ∧ exoticQi7 v ≤ 2 / 3 := by
  rcases exoticQi7_values v with h | h | h <;> rw [h] <;> constructor <;> norm_num

theorem exoticQi7_isFrameFunction : IsFrameFunction exoticQi7 := by
  intro u v w hf
  have hsum := s7_isZeroWeightFrameFunction u v w hf
  simp only [exoticQi7]
  linarith

theorem exoticQi7_isNonnegFrameFunction : IsNonnegFrameFunction exoticQi7 :=
  ⟨exoticQi7_isFrameFunction, fun v _ => (exoticQi7_bounds v).1⟩

theorem exoticQi7_not_quadratic :
    ¬ ∃ ρ : HermForm3, ∀ v : GVec, v.NonZero → exoticQi7 v = quadRay ρ v := by
  rintro ⟨ρ, hρ⟩
  obtain ⟨he1_s7, he2_s7, he3_s7, he12_s7, he13_s7, he23_s7, he12i_s7, he13i_s7, he23i_s7⟩ :=
    s7_vanishes_on_nine_rays
  have htomo_id : tomographyForm exoticQi7 = ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ := by
    ext <;>
      simp [tomographyForm, exoticQi7,
        he1_s7, he2_s7, he3_s7, he12_s7, he13_s7, he23_s7, he12i_s7, he13i_s7, he23i_s7]
  have hm := tomography_matches_nine_rays exoticQi7
  have hρ_eq : tomographyForm exoticQi7 = ρ := by
    apply tomography_unique (tomographyForm exoticQi7) ρ
    · rw [hm.1, hρ tomo_e1 tomo_e1_nonZero]
    · rw [hm.2.1, hρ tomo_e2 tomo_e2_nonZero]
    · rw [hm.2.2.1, hρ tomo_e3 tomo_e3_nonZero]
    · rw [hm.2.2.2.1, hρ tomo_e12 tomo_e12_nonZero]
    · rw [hm.2.2.2.2.1, hρ tomo_e13 tomo_e13_nonZero]
    · rw [hm.2.2.2.2.2.1, hρ tomo_e23 tomo_e23_nonZero]
    · rw [hm.2.2.2.2.2.2.1, hρ tomo_e12i tomo_e12i_nonZero]
    · rw [hm.2.2.2.2.2.2.2.1, hρ tomo_e13i tomo_e13i_nonZero]
    · rw [hm.2.2.2.2.2.2.2.2, hρ tomo_e23i tomo_e23i_nonZero]
  have hρ_id : ρ = ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ := hρ_eq.symm.trans htomo_id
  have hp7 := hρ witness_p7 witness_p7_nonZero
  rw [hρ_id] at hp7
  have hq : quadRay ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ witness_p7 = 1 / 3 := by
    simp [quadRay, quadNum, normSqVec, GaussRat.normSq, witness_p7, gv]
    norm_num
  have hex : exoticQi7 witness_p7 = 2 / 3 := by
    simp [exoticQi7, s7_witness_p7]
    norm_num
  linarith

/-- Two-parameter linear combination `c3 * s3 v + c7 * s7 v` of the `3`-adic and `7`-adic
zero-weight residuals on `ℚ(i)³`. -/
def combResidual37 (c3 c7 : ℚ) (v : GVec) : ℚ :=
  c3 * s3 v + c7 * s7 v

theorem combResidual37_isZeroWeightFrameFunction (c3 c7 : ℚ) :
    IsZeroWeightFrameFunction (combResidual37 c3 c7) := by
  intro u v w hf
  have h3 := s3_isZeroWeightFrameFunction u v w hf
  have h7 := s7_isZeroWeightFrameFunction u v w hf
  simp only [combResidual37]
  linear_combination c3 * h3 + c7 * h7

theorem combResidual37_vanishes_on_nine_rays (c3 c7 : ℚ) :
    VanishesOnNineRays (combResidual37 c3 c7) := by
  obtain ⟨h3_1, h3_2, h3_3, h3_12, h3_13, h3_23, h3_12i, h3_13i, h3_23i⟩ :=
    s3_vanishes_on_nine_rays
  obtain ⟨h7_1, h7_2, h7_3, h7_12, h7_13, h7_23, h7_12i, h7_13i, h7_23i⟩ :=
    s7_vanishes_on_nine_rays
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    simp [combResidual37, h3_1, h3_2, h3_3, h3_12, h3_13, h3_23, h3_12i, h3_13i, h3_23i,
      h7_1, h7_2, h7_3, h7_12, h7_13, h7_23, h7_12i, h7_13i, h7_23i]

theorem combResidual37_isBoundedOnRays (c3 c7 : ℚ) :
    IsBoundedOnRays (combResidual37 c3 c7) := by
  refine ⟨|c3| + |c7|, by linarith [abs_nonneg c3, abs_nonneg c7], ?_⟩
  intro v _
  have hc3 := le_abs_self c3
  have hnc3 := neg_le_abs c3
  have hc7 := le_abs_self c7
  have hnc7 := neg_le_abs c7
  have hnn3 := abs_nonneg c3
  have hnn7 := abs_nonneg c7
  rcases s3_values v with h3 | h3 | h3 <;>
    rcases s7_values v with h7 | h7 | h7 <;>
    simp only [combResidual37, h3, h7] <;>
    rw [abs_le] <;>
    constructor <;>
    linarith

theorem combResidual37_witness_111 (c3 c7 : ℚ) :
    combResidual37 c3 c7 witness_111 = c3 := by
  simp [combResidual37, s3_witness_111, s7_witness_111]

theorem combResidual37_witness_p7 (c3 c7 : ℚ) :
    combResidual37 c3 c7 witness_p7 = c7 := by
  simp [combResidual37, s3_witness_p7, s7_witness_p7]

/-- Linear independence of the `3`-adic and `7`-adic bounded zero-weight residuals `(s3, s7)`
on nonzero rays of `ℚ(i)³`: `c3 * s3 + c7 * s7` vanishes on all nonzero vectors iff `c3 = 0 ∧ c7 = 0`. -/
theorem s3_s7_linearIndependent (c3 c7 : ℚ) :
    (∀ v : GVec, v.NonZero → combResidual37 c3 c7 v = 0) ↔ (c3 = 0 ∧ c7 = 0) := by
  constructor
  · intro hall
    have h1 := hall witness_111 witness_111_nonZero
    have h2 := hall witness_p7 witness_p7_nonZero
    rw [combResidual37_witness_111] at h1
    rw [combResidual37_witness_p7] at h2
    exact ⟨h1, h2⟩
  · rintro ⟨rfl, rfl⟩ v _
    simp [combResidual37]

/-- Unscaled positive-sign `7`-adic Gaussian-integer perturbation `(7k, 1 + i, 2 + i)` near `tomo_e1`. -/
def perturb7PosInt (k : ℕ) : GVec :=
  gv (7 * (k : ℤ)) 0 1 1 2 1

/-- Unscaled negative-sign `7`-adic Gaussian-integer perturbation `(7k, 2 + i, 1 + i)` near `tomo_e1`. -/
def perturb7NegInt (k : ℕ) : GVec :=
  gv (7 * (k : ℤ)) 0 2 1 1 1

/-- Normalized positive-sign `7`-adic perturbation `(1, (1+i)/(7k), (2+i)/(7k))` approaching `tomo_e1`. -/
def perturb7PosRay (k : ℕ) : GVec :=
  ⟨⟨1, 0⟩,
   ⟨1 / (7 * (k : ℚ)), 1 / (7 * (k : ℚ))⟩,
   ⟨2 / (7 * (k : ℚ)), 1 / (7 * (k : ℚ))⟩⟩

/-- Normalized negative-sign `7`-adic perturbation `(1, (2+i)/(7k), (1+i)/(7k))` approaching `tomo_e1`. -/
def perturb7NegRay (k : ℕ) : GVec :=
  ⟨⟨1, 0⟩,
   ⟨2 / (7 * (k : ℚ)), 1 / (7 * (k : ℚ))⟩,
   ⟨1 / (7 * (k : ℚ)), 1 / (7 * (k : ℚ))⟩⟩

theorem perturb7PosRay_nonZero (k : ℕ) : (perturb7PosRay k).NonZero := by
  left
  change (⟨1, 0⟩ : GaussRat) ≠ 0
  decide

theorem perturb7NegRay_nonZero (k : ℕ) : (perturb7NegRay k).NonZero := by
  left
  change (⟨1, 0⟩ : GaussRat) ≠ 0
  decide

theorem seven_mul_gaussRat_ne_zero {k : ℕ} (hk : 0 < k) :
    (⟨7 * (k : ℚ), 0⟩ : GaussRat) ≠ 0 := by
  have hk_q : 0 < (k : ℚ) := by exact_mod_cast hk
  intro h
  have hre : (⟨7 * (k : ℚ), 0⟩ : GaussRat).re = 0 := by rw [h]; rfl
  simp only at hre
  linarith

theorem smul_seven_mul_perturb7PosRay {k : ℕ} (hk : 0 < k) :
    GVec.smul ⟨7 * (k : ℚ), 0⟩ (perturb7PosRay k) = perturb7PosInt k := by
  have hk_q : 0 < (k : ℚ) := by exact_mod_cast hk
  have hk_ne : (k : ℚ) ≠ 0 := ne_of_gt hk_q
  have hmul : 7 * (k : ℚ) * ((k : ℚ)⁻¹ * 7⁻¹) = 1 := by
    calc 7 * (k : ℚ) * ((k : ℚ)⁻¹ * 7⁻¹)
        = (k : ℚ) * (k : ℚ)⁻¹ := by ring
      _ = 1 := mul_inv_cancel₀ hk_ne
  have hmul2 : 7 * (k : ℚ) * (2 / (7 * (k : ℚ))) = 2 := by
    calc 7 * (k : ℚ) * (2 / (7 * (k : ℚ)))
        = 2 * (7 * (k : ℚ) * ((k : ℚ)⁻¹ * 7⁻¹)) := by ring
      _ = 2 * 1 := by rw [hmul]
      _ = 2 := by ring
  ext <;> simp [GVec.smul, perturb7PosRay, perturb7PosInt, gv, hmul, hmul2]

theorem smul_seven_mul_perturb7NegRay {k : ℕ} (hk : 0 < k) :
    GVec.smul ⟨7 * (k : ℚ), 0⟩ (perturb7NegRay k) = perturb7NegInt k := by
  have hk_q : 0 < (k : ℚ) := by exact_mod_cast hk
  have hk_ne : (k : ℚ) ≠ 0 := ne_of_gt hk_q
  have hmul : 7 * (k : ℚ) * ((k : ℚ)⁻¹ * 7⁻¹) = 1 := by
    calc 7 * (k : ℚ) * ((k : ℚ)⁻¹ * 7⁻¹)
        = (k : ℚ) * (k : ℚ)⁻¹ := by ring
      _ = 1 := mul_inv_cancel₀ hk_ne
  have hmul2 : 7 * (k : ℚ) * (2 / (7 * (k : ℚ))) = 2 := by
    calc 7 * (k : ℚ) * (2 / (7 * (k : ℚ)))
        = 2 * (7 * (k : ℚ) * ((k : ℚ)⁻¹ * 7⁻¹)) := by ring
      _ = 2 * 1 := by rw [hmul]
      _ = 2 := by ring
  ext <;> simp [GVec.smul, perturb7NegRay, perturb7NegInt, gv, hmul, hmul2]

theorem v7Nat_forty_nine_mul_sq_add_seven (k : ℕ) :
    v7Nat (49 * k ^ 2 + 7) = 1 ∧ p7PartNat (49 * k ^ 2 + 7) = 7 * k ^ 2 + 1 := by
  apply v7Nat_p7PartNat_eq_of_pow_mul
  · omega
  · ring

theorem v7Nat_forty_nine_mul_sq_ge_two {k : ℕ} (hk : 0 < k) :
    2 ≤ v7Nat (49 * k ^ 2) := by
  have hk2 : 0 < k ^ 2 := pow_pos hk 2
  have hmul := (v7Nat_p7PartNat_mul (by decide : 0 < 49) hk2).1
  have hv49 : v7Nat 49 = 2 := rfl
  omega

theorem s7_perturb7PosInt {k : ℕ} (hk : 0 < k) : s7 (perturb7PosInt k) = 1 := by
  obtain ⟨hv_n, hp_n⟩ := v7Nat_forty_nine_mul_sq_add_seven k
  have hv_x := v7Nat_forty_nine_mul_sq_ge_two hk
  have hv2 : v7Nat 2 = 0 := rfl
  have hp2 : p7PartNat 2 = 2 := rfl
  rw [s7_eq_of_lead7Coord_y (n := 49 * k ^ 2 + 7) (nx := 49 * k ^ 2) (ny := 2)
    (by omega) (by nlinarith) (by decide)
    (by simp [normSqVec, GaussRat.normSq, perturb7PosInt, gv]; ring)
    (by simp [GaussRat.normSq, perturb7PosInt, gv]; ring)
    (by simp [GaussRat.normSq, perturb7PosInt, gv]; norm_num)
    (by omega) (by omega) (by omega)]
  have hchi_n : chi7Nat (p7PartNat (49 * k ^ 2 + 7)) = 1 := by
    rw [hp_n, ← chi7Nat_mod_seven (7 * k ^ 2 + 1)]
    have hmod : (7 * k ^ 2 + 1) % 7 = 1 := by omega
    rw [hmod]
    rfl
  have hchi_y : chi7Nat (p7PartNat 2) = 1 := rfl
  rw [hchi_y, hchi_n]
  ring

theorem s7_perturb7NegInt {k : ℕ} (hk : 0 < k) : s7 (perturb7NegInt k) = -1 := by
  obtain ⟨hv_n, hp_n⟩ := v7Nat_forty_nine_mul_sq_add_seven k
  have hv_x := v7Nat_forty_nine_mul_sq_ge_two hk
  have hv5 : v7Nat 5 = 0 := rfl
  have hp5 : p7PartNat 5 = 5 := rfl
  rw [s7_eq_of_lead7Coord_y (n := 49 * k ^ 2 + 7) (nx := 49 * k ^ 2) (ny := 5)
    (by omega) (by nlinarith) (by decide)
    (by simp [normSqVec, GaussRat.normSq, perturb7NegInt, gv]; ring)
    (by simp [GaussRat.normSq, perturb7NegInt, gv]; ring)
    (by simp [GaussRat.normSq, perturb7NegInt, gv]; norm_num)
    (by omega) (by omega) (by omega)]
  have hchi_n : chi7Nat (p7PartNat (49 * k ^ 2 + 7)) = 1 := by
    rw [hp_n, ← chi7Nat_mod_seven (7 * k ^ 2 + 1)]
    have hmod : (7 * k ^ 2 + 1) % 7 = 1 := by omega
    rw [hmod]
    rfl
  have hchi_y : chi7Nat (p7PartNat 5) = -1 := rfl
  rw [hchi_y, hchi_n]
  ring

theorem s7_perturb7PosRay {k : ℕ} (hk : 0 < k) : s7 (perturb7PosRay k) = 1 := by
  rw [← s7_smul (perturb7PosRay_nonZero k) (seven_mul_gaussRat_ne_zero hk),
    smul_seven_mul_perturb7PosRay hk]
  exact s7_perturb7PosInt hk

theorem s7_perturb7NegRay {k : ℕ} (hk : 0 < k) : s7 (perturb7NegRay k) = -1 := by
  rw [← s7_smul (perturb7NegRay_nonZero k) (seven_mul_gaussRat_ne_zero hk),
    smul_seven_mul_perturb7NegRay hk]
  exact s7_perturb7NegInt hk

theorem forty_nine_mul_sq_add_seven_mod_three_ne_zero (k : ℕ) :
    (49 * k ^ 2 + 7) % 3 ≠ 0 := by
  simp only [sq]
  rw [Nat.add_mod, Nat.mul_mod 49, Nat.mul_mod k k]
  have hk : k % 3 = 0 ∨ k % 3 = 1 ∨ k % 3 = 2 := by omega
  rcases hk with h | h | h <;> simp [h]

theorem v3Nat_forty_nine_mul_sq_add_seven (k : ℕ) :
    v3Nat (49 * k ^ 2 + 7) = 0 :=
  (v3Nat_p3PartNat_eq_of_pow_mul (a := 0) (m := 49 * k ^ 2 + 7)
    (forty_nine_mul_sq_add_seven_mod_three_ne_zero k) (by ring)).1

theorem s3_perturb7PosInt (k : ℕ) : s3 (perturb7PosInt k) = 0 := by
  apply s3_eq_zero_of_normSqVec_natCast (n := 49 * k ^ 2 + 7) (by omega)
  · simp [normSqVec, GaussRat.normSq, perturb7PosInt, gv]; ring
  · rw [v3Nat_forty_nine_mul_sq_add_seven k]; rfl

theorem s3_perturb7NegInt (k : ℕ) : s3 (perturb7NegInt k) = 0 := by
  apply s3_eq_zero_of_normSqVec_natCast (n := 49 * k ^ 2 + 7) (by omega)
  · simp [normSqVec, GaussRat.normSq, perturb7NegInt, gv]; ring
  · rw [v3Nat_forty_nine_mul_sq_add_seven k]; rfl

/-- Selective cross-prime vanishing: `s3` vanishes on the `7`-adic perturbation rays
`perturb7PosRay k` and `perturb7NegRay k` for every `k ≥ 1`. -/
theorem s3_perturb7PosRay {k : ℕ} (hk : 0 < k) : s3 (perturb7PosRay k) = 0 := by
  rw [← s3_smul (perturb7PosRay_nonZero k) (seven_mul_gaussRat_ne_zero hk),
    smul_seven_mul_perturb7PosRay hk]
  exact s3_perturb7PosInt k

theorem s3_perturb7NegRay {k : ℕ} (hk : 0 < k) : s3 (perturb7NegRay k) = 0 := by
  rw [← s3_smul (perturb7NegRay_nonZero k) (seven_mul_gaussRat_ne_zero hk),
    smul_seven_mul_perturb7NegRay hk]
  exact s3_perturb7NegInt k

theorem v7Nat_nine_mul_seven_mul_sq_add_three (k : ℕ) :
    v7Nat (9 * (7 * k) ^ 2 + 3) = 0 :=
  (v7Nat_p7PartNat_eq_of_pow_mul (a := 0) (m := 9 * (7 * k) ^ 2 + 3)
    (by
      have h : 9 * (7 * k) ^ 2 + 3 = 7 * (63 * k ^ 2) + 3 := by ring
      omega)
    (by ring)).1

theorem s7_perturbPosInt_seven_mul (k : ℕ) : s7 (perturbPosInt (7 * k)) = 0 := by
  apply s7_eq_zero_of_normSqVec_natCast (n := 9 * (7 * k) ^ 2 + 3) (by omega)
  · simp [normSqVec, GaussRat.normSq, perturbPosInt, gv]; ring
  · rw [v7Nat_nine_mul_seven_mul_sq_add_three k]; rfl

theorem s7_perturbNegInt_seven_mul (k : ℕ) : s7 (perturbNegInt (7 * k)) = 0 := by
  apply s7_eq_zero_of_normSqVec_natCast (n := 9 * (7 * k) ^ 2 + 3) (by omega)
  · simp [normSqVec, GaussRat.normSq, perturbNegInt, gv]; ring
  · rw [v7Nat_nine_mul_seven_mul_sq_add_three k]; rfl

/-- Selective cross-prime vanishing: `s7` vanishes on the `3`-adic subsequence
`perturbPosRay (7 * k)` and `perturbNegRay (7 * k)` for every `k ≥ 1`. -/
theorem s7_perturbPosRay_seven_mul {k : ℕ} (hk : 0 < k) :
    s7 (perturbPosRay (7 * k)) = 0 := by
  have hk7 : 0 < 7 * k := by omega
  rw [← s7_smul (perturbPosRay_nonZero (7 * k)) (three_mul_gaussRat_ne_zero hk7),
    smul_three_mul_perturbPosRay hk7]
  exact s7_perturbPosInt_seven_mul k

theorem s7_perturbNegRay_seven_mul {k : ℕ} (hk : 0 < k) :
    s7 (perturbNegRay (7 * k)) = 0 := by
  have hk7 : 0 < 7 * k := by omega
  rw [← s7_smul (perturbNegRay_nonZero (7 * k)) (three_mul_gaussRat_ne_zero hk7),
    smul_three_mul_perturbNegRay hk7]
  exact s7_perturbNegInt_seven_mul k

theorem distSqVec_perturb7PosRay_tomo_e1 (k : ℕ) :
    distSqVec (perturb7PosRay k) tomo_e1 = 1 / (7 * (k : ℚ) ^ 2) := by
  simp only [distSqVec, perturb7PosRay, tomo_e1, gv,
    normSqVec, GaussRat.normSq, GaussRat.re_sub, GaussRat.im_sub]
  ring

theorem distSqVec_perturb7NegRay_tomo_e1 (k : ℕ) :
    distSqVec (perturb7NegRay k) tomo_e1 = 1 / (7 * (k : ℚ) ^ 2) := by
  simp only [distSqVec, perturb7NegRay, tomo_e1, gv,
    normSqVec, GaussRat.normSq, GaussRat.re_sub, GaussRat.im_sub]
  ring

/-- In every archimedean neighborhood `distSqVec v tomo_e1 < δ` of `tomo_e1 = (1, 0, 0)`,
there exist four nonzero Gaussian-rational rays `u3Pos, u3Neg, u7Pos, u7Neg ∈ ℚ(i)³`
that selectively oscillate `s3` and `s7` independently:
- `s3 u3Pos = 1, s7 u3Pos = 0` and `s3 u3Neg = -1, s7 u3Neg = 0`,
- `s3 u7Pos = 0, s7 u7Pos = 1` and `s3 u7Neg = 0, s7 u7Neg = -1`. -/
theorem s3_s7_selective_oscillation_near_tomo_e1 (δ : ℚ) (hδ : 0 < δ) :
    ∃ u3Pos u3Neg u7Pos u7Neg : GVec,
      u3Pos.NonZero ∧ u3Neg.NonZero ∧ u7Pos.NonZero ∧ u7Neg.NonZero ∧
      distSqVec u3Pos tomo_e1 < δ ∧ distSqVec u3Neg tomo_e1 < δ ∧
      distSqVec u7Pos tomo_e1 < δ ∧ distSqVec u7Neg tomo_e1 < δ ∧
      s3 u3Pos = 1 ∧ s7 u3Pos = 0 ∧
      s3 u3Neg = -1 ∧ s7 u3Neg = 0 ∧
      s3 u7Pos = 0 ∧ s7 u7Pos = 1 ∧
      s3 u7Neg = 0 ∧ s7 u7Neg = -1 := by
  obtain ⟨k, hk, hlt⟩ := exists_nat_pos_inv_three_sq_lt hδ
  have hk7 : 0 < 7 * k := by omega
  have hk_ge_one : (1 : ℚ) ≤ (k : ℚ) := by exact_mod_cast hk
  have h3k2_pos : 0 < 3 * (k : ℚ) ^ 2 := by nlinarith
  have hpos : 0 < 1 / (3 * (k : ℚ) ^ 2) := div_pos (by norm_num) h3k2_pos
  have h3_eq : 1 / (3 * ((7 * k : ℕ) : ℚ) ^ 2) = (1 / 49) * (1 / (3 * (k : ℚ) ^ 2)) := by
    push_cast; ring
  have h7_eq : 1 / (7 * (k : ℚ) ^ 2) = (3 / 7) * (1 / (3 * (k : ℚ) ^ 2)) := by ring
  have hlt3 : 1 / (3 * ((7 * k : ℕ) : ℚ) ^ 2) < δ := by linarith
  have hlt7 : 1 / (7 * (k : ℚ) ^ 2) < δ := by linarith
  refine ⟨perturbPosRay (7 * k), perturbNegRay (7 * k), perturb7PosRay k, perturb7NegRay k,
    perturbPosRay_nonZero (7 * k), perturbNegRay_nonZero (7 * k),
    perturb7PosRay_nonZero k, perturb7NegRay_nonZero k,
    ?_, ?_, ?_, ?_,
    s3_perturbPosRay hk7, s7_perturbPosRay_seven_mul hk,
    s3_perturbNegRay hk7, s7_perturbNegRay_seven_mul hk,
    s3_perturb7PosRay hk, s7_perturb7PosRay hk,
    s3_perturb7NegRay hk, s7_perturb7NegRay hk⟩
  · rw [distSqVec_perturbPosRay_tomo_e1 (7 * k)]; exact hlt3
  · rw [distSqVec_perturbNegRay_tomo_e1 (7 * k)]; exact hlt3
  · rw [distSqVec_perturb7PosRay_tomo_e1 k]; exact hlt7
  · rw [distSqVec_perturb7NegRay_tomo_e1 k]; exact hlt7

/-- The `7`-adic zero-weight residual `s7` is not archimedean-continuous at `tomo_e1 = (1, 0, 0)`. -/
theorem not_archimedeanContinuousAt_s7_tomo_e1 :
    ¬ IsArchimedeanContinuousAt s7 tomo_e1 := by
  intro hcont
  obtain ⟨δ, hδ, hball⟩ := hcont (1 / 2) (by norm_num)
  obtain ⟨_, _, u7Pos, _, _, _, hu7Pos_nz, _, _, _, hu7Pos_dist, _, _, _, _, _, _, hu7Pos_s7, _, _⟩ :=
    s3_s7_selective_oscillation_near_tomo_e1 δ hδ
  have hlt := hball u7Pos hu7Pos_nz hu7Pos_dist
  have he1 : s7 tomo_e1 = 0 := s7_vanishes_on_nine_rays.1
  rw [hu7Pos_s7, he1] at hlt
  norm_num at hlt

/-- The `7`-adic nonnegative non-quadratic frame function `exoticQi7` is not archimedean-continuous
at `tomo_e1 = (1, 0, 0)`. -/
theorem not_archimedeanContinuousAt_exoticQi7_tomo_e1 :
    ¬ IsArchimedeanContinuousAt exoticQi7 tomo_e1 := by
  intro hcont
  obtain ⟨δ, hδ, hball⟩ := hcont (1 / 6) (by norm_num)
  obtain ⟨_, _, u7Pos, _, _, _, hu7Pos_nz, _, _, _, hu7Pos_dist, _, _, _, _, _, _, hu7Pos_s7, _, _⟩ :=
    s3_s7_selective_oscillation_near_tomo_e1 δ hδ
  have hlt := hball u7Pos hu7Pos_nz hu7Pos_dist
  have he1 : exoticQi7 tomo_e1 = 1 / 3 := by
    simp only [exoticQi7, s7_vanishes_on_nine_rays.1]
    norm_num
  have hu7 : exoticQi7 u7Pos = 2 / 3 := by
    simp only [exoticQi7, hu7Pos_s7]
    norm_num
  rw [hu7, he1] at hlt
  norm_num at hlt

/-- Joint Archimedean continuity elimination of `combResidual37 c3 c7`: if `f` and
`f - combResidual37 c3 c7` are both archimedean-continuous at `tomo_e1 = (1, 0, 0)`, then
both inert-prime residual coefficients vanish (`c3 = 0 ∧ c7 = 0`). -/
theorem combResidual37_coeffs_zero_of_archimedeanContinuousAt_tomo_e1
    {f : GVec → ℚ} {c3 c7 : ℚ}
    (hf_cont : IsArchimedeanContinuousAt f tomo_e1)
    (hq_cont : IsArchimedeanContinuousAt (fun v => f v - combResidual37 c3 c7 v) tomo_e1) :
    c3 = 0 ∧ c7 = 0 := by
  have he1_3 : s3 tomo_e1 = 0 := s3_vanishes_on_nine_rays.1
  have he1_7 : s7 tomo_e1 = 0 := s7_vanishes_on_nine_rays.1
  constructor
  · by_contra hc3
    have hc3_pos : 0 < |c3| := abs_pos.mpr hc3
    obtain ⟨δ1, hδ1, hb1⟩ := hf_cont (|c3| / 3) (by linarith)
    obtain ⟨δ2, hδ2, hb2⟩ := hq_cont (|c3| / 3) (by linarith)
    let δ := min δ1 δ2
    have hδ : 0 < δ := lt_min hδ1 hδ2
    obtain ⟨u3Pos, _, _, _, hu3Pos_nz, _, _, _, hu3Pos_dist, _, _, _,
      hu3Pos_s3, hu3Pos_s7, _, _, _, _, _, _⟩ :=
      s3_s7_selective_oscillation_near_tomo_e1 δ hδ
    have h1 := hb1 u3Pos hu3Pos_nz (lt_of_lt_of_le hu3Pos_dist (min_le_left δ1 δ2))
    have h2 := hb2 u3Pos hu3Pos_nz (lt_of_lt_of_le hu3Pos_dist (min_le_right δ1 δ2))
    simp only [combResidual37, hu3Pos_s3, hu3Pos_s7, he1_3, he1_7,
      mul_one, mul_zero, add_zero, sub_zero] at h2
    have htri : |c3| ≤ |f u3Pos - f tomo_e1| + |f u3Pos - c3 - f tomo_e1| := by
      calc |c3| = |(f u3Pos - f tomo_e1) - (f u3Pos - c3 - f tomo_e1)| := by ring_nf
        _ ≤ |f u3Pos - f tomo_e1| + |f u3Pos - c3 - f tomo_e1| :=
          abs_sub (f u3Pos - f tomo_e1) (f u3Pos - c3 - f tomo_e1)
    linarith
  · by_contra hc7
    have hc7_pos : 0 < |c7| := abs_pos.mpr hc7
    obtain ⟨δ1, hδ1, hb1⟩ := hf_cont (|c7| / 3) (by linarith)
    obtain ⟨δ2, hδ2, hb2⟩ := hq_cont (|c7| / 3) (by linarith)
    let δ := min δ1 δ2
    have hδ : 0 < δ := lt_min hδ1 hδ2
    obtain ⟨_, _, u7Pos, _, _, _, hu7Pos_nz, _, _, _, hu7Pos_dist, _,
      _, _, _, _, hu7Pos_s3, hu7Pos_s7, _, _⟩ :=
      s3_s7_selective_oscillation_near_tomo_e1 δ hδ
    have h1 := hb1 u7Pos hu7Pos_nz (lt_of_lt_of_le hu7Pos_dist (min_le_left δ1 δ2))
    have h2 := hb2 u7Pos hu7Pos_nz (lt_of_lt_of_le hu7Pos_dist (min_le_right δ1 δ2))
    simp only [combResidual37, hu7Pos_s3, hu7Pos_s7, he1_3, he1_7,
      mul_one, mul_zero, zero_add, add_zero, sub_zero] at h2
    have htri : |c7| ≤ |f u7Pos - f tomo_e1| + |f u7Pos - c7 - f tomo_e1| := by
      calc |c7| = |(f u7Pos - f tomo_e1) - (f u7Pos - c7 - f tomo_e1)| := by ring_nf
        _ ≤ |f u7Pos - f tomo_e1| + |f u7Pos - c7 - f tomo_e1| :=
          abs_sub (f u7Pos - f tomo_e1) (f u7Pos - c7 - f tomo_e1)
    linarith

/-- Unconditional joint Archimedean continuity elimination theorem for `(s3, s7)`:
for any `ρ : HermForm3` and `c3, c7 : ℚ`, the perturbed ray function
`quadRay ρ + c3 • s3 + c7 • s7` is archimedean-continuous at `tomo_e1 = (1, 0, 0)`
if and only if `c3 = 0 ∧ c7 = 0`. -/
theorem quadRay_add_combResidual37_archimedeanContinuousAt_tomo_e1_iff
    (ρ : HermForm3) (c3 c7 : ℚ) :
    IsArchimedeanContinuousAt (fun v => quadRay ρ v + combResidual37 c3 c7 v) tomo_e1 ↔
      (c3 = 0 ∧ c7 = 0) := by
  constructor
  · intro hf_cont
    apply combResidual37_coeffs_zero_of_archimedeanContinuousAt_tomo_e1 hf_cont
    have heq : (fun v => (quadRay ρ v + combResidual37 c3 c7 v) - combResidual37 c3 c7 v) =
        quadRay ρ := by
      funext v; ring
    rw [heq]
    exact archimedeanContinuousAt_quadRay_tomo_e1 ρ
  · rintro ⟨rfl, rfl⟩
    have heq : (fun v => quadRay ρ v + combResidual37 0 0 v) = quadRay ρ := by
      funext v; simp [combResidual37]
    rw [heq]
    exact archimedeanContinuousAt_quadRay_tomo_e1 ρ

/-- Over `ℚ(i)³`, no scalar multiple of `witness_p7 = (1, 2, 1 + i)` can have unit squared norm `1`. -/
theorem no_unit_norm_smul_witness_p7_in_qi3 (l : GaussRat) :
    normSqVec (GVec.smul l witness_p7) ≠ 1 := by
  intro h1
  have hl_pos : 0 < l.normSq := by
    by_contra hle
    have h0 : l.normSq = 0 := le_antisymm (not_lt.mp hle) (GaussRat.normSq_nonneg l)
    rw [normSqVec_smul, h0, zero_mul] at h1
    norm_num at h1
  rw [normSqVec_smul, witness_p7_normSq] at h1
  have hv := congrArg v7Rat h1
  rw [v7Rat_mul hl_pos (by norm_num : (0 : ℚ) < 7)] at hv
  have hv1 : v7Rat 1 = 0 := rfl
  have hv7 : v7Rat 7 = 1 := rfl
  have heven := v7Rat_normSq_even l
  omega

/-- Zero-weight frame functions on `ℚ(i, √p)³`. -/
def IsZeroWeightFrameFunctionSqrtP (p : ℚ) (G : GVecSqrt3 → ℚ) : Prop :=
  ∀ u v w : GVecSqrt3, IsFrameSqrtP p u v w → G u + G v + G w = 0

/-- Any zero-weight frame function `G` on `ℚ(i, √7)³` that vanishes on vectors whose rational
squared norm has even `7`-adic valuation must vanish on `witness_p7 = (1, 2, 1 + i)`, so `s7`
cannot extend to `ℚ(i, √7)³` under the even-`v_7` vanishing rule. -/
theorem zero_on_witness_p7_of_sqrt7_even_v7_vanishing
    {G : GVecSqrt3 → ℚ}
    (hG : IsZeroWeightFrameFunctionSqrtP 7 G)
    (heven : ∀ u : GVecSqrt3, v7Rat (GVecSqrt3.normSqRatP 7 u) % 2 = 0 → G u = 0) :
    G (GVecSqrt3.ofGVec witness_p7) = 0 := by
  obtain ⟨hfr, _, hnp, hnq⟩ := isFrameSqrt7_witness_p7_norms
  have hsum := hG (GVecSqrt3.ofGVec witness_p7) frameSqrt7_p frameSqrt7_q hfr
  have hv245 : v7Rat 245 % 2 = 0 := by
    have h245 : (245 : ℚ) = ((245 : ℕ) : ℚ) := by norm_num
    rw [h245, v7Rat_natCast (by decide : 0 < 245)]
    rfl
  have hp_even : v7Rat (GVecSqrt3.normSqRatP 7 frameSqrt7_p) % 2 = 0 := by rw [hnp]; exact hv245
  have hq_even : v7Rat (GVecSqrt3.normSqRatP 7 frameSqrt7_q) % 2 = 0 := by rw [hnq]; exact hv245
  have hp0 := heven frameSqrt7_p hp_even
  have hq0 := heven frameSqrt7_q hq_even
  linarith

theorem no_s7_even_v7_extension_to_sqrt7 :
    ¬ ∃ G : GVecSqrt3 → ℚ,
        IsZeroWeightFrameFunctionSqrtP 7 G ∧
        (∀ u : GVecSqrt3, v7Rat (GVecSqrt3.normSqRatP 7 u) % 2 = 0 → G u = 0) ∧
        (∀ v : GVec, G (GVecSqrt3.ofGVec v) = s7 v) := by
  rintro ⟨G, hG, heven, hext⟩
  have h0 := zero_on_witness_p7_of_sqrt7_even_v7_vanishing hG heven
  have h1 := hext witness_p7
  rw [s7_witness_p7] at h1
  linarith

/-- Joint field-extension elimination of `combResidual37 c3 c7` over `ℚ(i, √3)³` and `ℚ(i, √7)³`:
because the orthogonal partners `frameSqrt3_p, frameSqrt3_q` (norm `18 = 2 × 3²`) and
`frameSqrt7_p, frameSqrt7_q` (norm `245 = 5 × 7²`) have even `3`-adic AND even `7`-adic
valuations simultaneously (`v3Rat 18 = 2, v7Rat 18 = 0` and `v3Rat 245 = 0, v7Rat 245 = 2`),
any linear combination `combResidual37 c3 c7` that extends to zero-weight frame functions on
`ℚ(i, √3)³` and `ℚ(i, √7)³` vanishing on rays with jointly `{3, 7}`-even rational squared norm
must have `c3 = 0 ∧ c7 = 0`. -/
theorem joint_sqrt3_sqrt7_even_valuation_eliminates_combResidual37
    {c3 c7 : ℚ}
    {G3 G7 : GVecSqrt3 → ℚ}
    (hG3 : IsZeroWeightFrameFunctionSqrt3 G3)
    (hG7 : IsZeroWeightFrameFunctionSqrtP 7 G7)
    (heven3 : ∀ u : GVecSqrt3,
      v3Rat u.normSqRat % 2 = 0 ∧ v7Rat u.normSqRat % 2 = 0 → G3 u = 0)
    (heven7 : ∀ u : GVecSqrt3,
      v3Rat (GVecSqrt3.normSqRatP 7 u) % 2 = 0 ∧
      v7Rat (GVecSqrt3.normSqRatP 7 u) % 2 = 0 → G7 u = 0)
    (hext3 : ∀ v : GVec, G3 (GVecSqrt3.ofGVec v) = combResidual37 c3 c7 v)
    (hext7 : ∀ v : GVec, G7 (GVecSqrt3.ofGVec v) = combResidual37 c3 c7 v) :
    c3 = 0 ∧ c7 = 0 := by
  obtain ⟨hfr3, _, hnp3, hnq3, hp3_v3, hq3_v3, _⟩ := isFrameSqrt3_witness_111_even_norms
  obtain ⟨hfr7, _, hnp7, hnq7⟩ := isFrameSqrt7_witness_p7_norms
  have hv7_18 : v7Rat 18 % 2 = 0 := by
    have h18 : (18 : ℚ) = ((18 : ℕ) : ℚ) := by norm_num
    rw [h18, v7Rat_natCast (by decide : 0 < 18)]
    rfl
  have hv3_245 : v3Rat 245 % 2 = 0 := by
    have h245 : (245 : ℚ) = ((245 : ℕ) : ℚ) := by norm_num
    rw [h245, v3Rat_natCast (by decide : 0 < 245)]
    rfl
  have hv7_245 : v7Rat 245 % 2 = 0 := by
    have h245 : (245 : ℚ) = ((245 : ℕ) : ℚ) := by norm_num
    rw [h245, v7Rat_natCast (by decide : 0 < 245)]
    rfl
  have hsum3 := hG3 witness_111_sqrt3 frameSqrt3_p frameSqrt3_q hfr3
  have hp3_0 := heven3 frameSqrt3_p ⟨hp3_v3, by rw [hnp3]; exact hv7_18⟩
  have hq3_0 := heven3 frameSqrt3_q ⟨hq3_v3, by rw [hnq3]; exact hv7_18⟩
  have hw111_0 : G3 (GVecSqrt3.ofGVec witness_111) = 0 := by
    change G3 witness_111_sqrt3 = 0
    linarith
  rw [hext3 witness_111, combResidual37_witness_111] at hw111_0
  have hsum7 := hG7 (GVecSqrt3.ofGVec witness_p7) frameSqrt7_p frameSqrt7_q hfr7
  have hp7_0 := heven7 frameSqrt7_p ⟨by rw [hnp7]; exact hv3_245, by rw [hnp7]; exact hv7_245⟩
  have hq7_0 := heven7 frameSqrt7_q ⟨by rw [hnq7]; exact hv3_245, by rw [hnq7]; exact hv7_245⟩
  have hwp7_0 : G7 (GVecSqrt3.ofGVec witness_p7) = 0 := by linarith
  rw [hext7 witness_p7, combResidual37_witness_p7] at hwp7_0
  exact ⟨hw111_0, hwp7_0⟩

theorem not_factorsThroughRayProjLinear_s7 : ¬ FactorsThroughRayProjLinear s7 := by
  intro hlin
  have h0 := zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear
    s7_vanishes_on_nine_rays hlin witness_p7 witness_p7_nonZero
  rw [s7_witness_p7] at h0
  norm_num at h0

/-- A linear combination `combResidual37 c3 c7` factors linearly through `rayProj`
if and only if `c3 = 0 ∧ c7 = 0`. -/
theorem factorsThroughRayProjLinear_combResidual37_iff (c3 c7 : ℚ) :
    FactorsThroughRayProjLinear (combResidual37 c3 c7) ↔ (c3 = 0 ∧ c7 = 0) := by
  constructor
  · intro hlin
    exact (s3_s7_linearIndependent c3 c7).mp
      (zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear
        (combResidual37_vanishes_on_nine_rays c3 c7) hlin)
  · rintro ⟨rfl, rfl⟩
    refine ⟨fun _ => 0, ⟨by intro _ _; ring, by intro _ _; ring⟩, ?_⟩
    intro v _
    simp [combResidual37]

/-- Explicit operator-space projector relation for `witness_p7 = (1, 2, 1 + i)`:
its rank-1 projector is an exact rational linear combination of the six real tomography
projectors together with the two imaginary tomography projectors `tomo_e13i` and `tomo_e23i`. -/
theorem rayProj_witness_p7_decomp :
    rayProj witness_p7 =
    HermForm3.add
      (HermForm3.add
        (HermForm3.add
          (HermForm3.add
            (HermForm3.add
              (HermForm3.add
                (HermForm3.add
                  (HermForm3.smul (-3 / 7) (rayProj tomo_e1))
                  (HermForm3.smul (-2 / 7) (rayProj tomo_e2)))
                (HermForm3.smul (-4 / 7) (rayProj tomo_e3)))
              (HermForm3.smul (4 / 7) (rayProj tomo_e12)))
            (HermForm3.smul (2 / 7) (rayProj tomo_e13)))
          (HermForm3.smul (4 / 7) (rayProj tomo_e23)))
        (HermForm3.smul (2 / 7) (rayProj tomo_e13i)))
      (HermForm3.smul (4 / 7) (rayProj tomo_e23i)) := by
  ext <;>
    simp [HermForm3.add, HermForm3.smul, rayProj, normSqVec, GaussRat.normSq,
      witness_p7, tomo_e1, tomo_e2, tomo_e3, tomo_e12, tomo_e13, tomo_e23,
      tomo_e13i, tomo_e23i, gv] <;>
    norm_num

/-- Every quadratic Rayleigh function `quadRay ρ` satisfies the 9-ray linear kernel identity
induced by `rayProj_witness_p7_decomp`. -/
theorem quadRay_witness_p7_kernel_relation (ρ : HermForm3) :
    quadRay ρ witness_p7 +
      (3 / 7) * quadRay ρ tomo_e1 + (2 / 7) * quadRay ρ tomo_e2 + (4 / 7) * quadRay ρ tomo_e3 -
      (4 / 7) * quadRay ρ tomo_e12 - (2 / 7) * quadRay ρ tomo_e13 - (4 / 7) * quadRay ρ tomo_e23 -
      (2 / 7) * quadRay ρ tomo_e13i - (4 / 7) * quadRay ρ tomo_e23i = 0 := by
  simp only [← traceInner_rayProj, rayProj_witness_p7_decomp,
    traceInner_add_right, traceInner_smul_right]
  ring

/-- Dual constructive separation of the `witness_p7` projector kernel relation:
the formal combination in `ker(rayProj)` evaluates to `1` under `s7`, `0` under `s3`,
and `c7` under `combResidual37 c3 c7`. -/
theorem s7_witness_p7_kernel_separation (c3 c7 : ℚ) :
    s7 witness_p7 +
      (3 / 7) * s7 tomo_e1 + (2 / 7) * s7 tomo_e2 + (4 / 7) * s7 tomo_e3 -
      (4 / 7) * s7 tomo_e12 - (2 / 7) * s7 tomo_e13 - (4 / 7) * s7 tomo_e23 -
      (2 / 7) * s7 tomo_e13i - (4 / 7) * s7 tomo_e23i = 1 ∧
    s3 witness_p7 +
      (3 / 7) * s3 tomo_e1 + (2 / 7) * s3 tomo_e2 + (4 / 7) * s3 tomo_e3 -
      (4 / 7) * s3 tomo_e12 - (2 / 7) * s3 tomo_e13 - (4 / 7) * s3 tomo_e23 -
      (2 / 7) * s3 tomo_e13i - (4 / 7) * s3 tomo_e23i = 0 ∧
    combResidual37 c3 c7 witness_p7 +
      (3 / 7) * combResidual37 c3 c7 tomo_e1 + (2 / 7) * combResidual37 c3 c7 tomo_e2 +
      (4 / 7) * combResidual37 c3 c7 tomo_e3 -
      (4 / 7) * combResidual37 c3 c7 tomo_e12 - (2 / 7) * combResidual37 c3 c7 tomo_e13 -
      (4 / 7) * combResidual37 c3 c7 tomo_e23 -
      (2 / 7) * combResidual37 c3 c7 tomo_e13i - (4 / 7) * combResidual37 c3 c7 tomo_e23i = c7 := by
  obtain ⟨he1_7, he2_7, he3_7, he12_7, he13_7, he23_7, _, he13i_7, he23i_7⟩ := s7_vanishes_on_nine_rays
  obtain ⟨he1_3, he2_3, he3_3, he12_3, he13_3, he23_3, _, he13i_3, he23i_3⟩ := s3_vanishes_on_nine_rays
  refine ⟨?_, ?_, ?_⟩
  · rw [s7_witness_p7, he1_7, he2_7, he3_7, he12_7, he13_7, he23_7, he13i_7, he23i_7]
    norm_num
  · rw [s3_witness_p7, he1_3, he2_3, he3_3, he12_3, he13_3, he23_3, he13i_3, he23i_3]
    norm_num
  · simp [combResidual37, s3_witness_p7, s7_witness_p7,
      he1_7, he2_7, he3_7, he12_7, he13_7, he23_7, he13i_7, he23i_7,
      he1_3, he2_3, he3_3, he12_3, he13_3, he23_3, he13i_3, he23i_3]

/-- Cross-prime frame norm parity: the `ℚ(i, √3)³` frame `(witness_111, frameSqrt3_p, frameSqrt3_q)`
of norms `(3, 18, 18)` has even `7`-adic valuation (`v7Rat = 0`) on all three vectors, whereas the
`ℚ(i, √7)³` frame `(witness_p7, frameSqrt7_p, frameSqrt7_q)` of norms `(7, 245, 245)` has even
`3`-adic valuation (`v3Rat = 0`) on all three vectors. -/
theorem cross_prime_frame_partner_norm_valuations_even :
    v7Rat witness_111_sqrt3.normSqRat % 2 = 0 ∧
    v7Rat frameSqrt3_p.normSqRat % 2 = 0 ∧
    v7Rat frameSqrt3_q.normSqRat % 2 = 0 ∧
    v3Rat (GVecSqrt3.normSqRatP 7 (GVecSqrt3.ofGVec witness_p7)) % 2 = 0 ∧
    v3Rat (GVecSqrt3.normSqRatP 7 frameSqrt7_p) % 2 = 0 ∧
    v3Rat (GVecSqrt3.normSqRatP 7 frameSqrt7_q) % 2 = 0 := by
  obtain ⟨_, hnw3, hnp3, hnq3, _, _, _⟩ := isFrameSqrt3_witness_111_even_norms
  obtain ⟨_, hnw7, hnp7, hnq7⟩ := isFrameSqrt7_witness_p7_norms
  have hv7_3 : v7Rat 3 % 2 = 0 := by
    have h3 : (3 : ℚ) = ((3 : ℕ) : ℚ) := by norm_num
    rw [h3, v7Rat_natCast (by decide : 0 < 3)]; rfl
  have hv7_18 : v7Rat 18 % 2 = 0 := by
    have h18 : (18 : ℚ) = ((18 : ℕ) : ℚ) := by norm_num
    rw [h18, v7Rat_natCast (by decide : 0 < 18)]; rfl
  have hv3_7 : v3Rat 7 % 2 = 0 := by
    have h7 : (7 : ℚ) = ((7 : ℕ) : ℚ) := by norm_num
    rw [h7, v3Rat_natCast (by decide : 0 < 7)]; rfl
  have hv3_245 : v3Rat 245 % 2 = 0 := by
    have h245 : (245 : ℚ) = ((245 : ℕ) : ℚ) := by norm_num
    rw [h245, v3Rat_natCast (by decide : 0 < 245)]; rfl
  exact ⟨by rw [hnw3]; exact hv7_3,
         by rw [hnp3]; exact hv7_18,
         by rw [hnq3]; exact hv7_18,
         by rw [hnw7]; exact hv3_7,
         by rw [hnp7]; exact hv3_245,
         by rw [hnq7]; exact hv3_245⟩

/-- Two-parameter family `(1 + combResidual37 c3 c7 v) / 3` of frame functions on `ℚ(i)³`
spanning the `ℓ¹` diamond of nonnegative non-quadratic frame functions when `|c3| + |c7| ≤ 1`. -/
def exoticComb37 (c3 c7 : ℚ) (v : GVec) : ℚ :=
  (1 + combResidual37 c3 c7 v) / 3

theorem exoticComb37_isFrameFunction (c3 c7 : ℚ) :
    IsFrameFunction (exoticComb37 c3 c7) := by
  intro u v w hf
  have hsum := combResidual37_isZeroWeightFrameFunction c3 c7 u v w hf
  simp only [exoticComb37]
  linarith

theorem abs_combResidual37_le (c3 c7 : ℚ) (v : GVec) :
    |combResidual37 c3 c7 v| ≤ |c3| + |c7| := by
  have hc3 := le_abs_self c3
  have hnc3 := neg_le_abs c3
  have hc7 := le_abs_self c7
  have hnc7 := neg_le_abs c7
  have hnn3 := abs_nonneg c3
  have hnn7 := abs_nonneg c7
  rcases s3_values v with h3 | h3 | h3 <;>
    rcases s7_values v with h7 | h7 | h7 <;>
    simp only [combResidual37, h3, h7] <;>
    rw [abs_le] <;>
    constructor <;>
    linarith

/-- For every `(c3, c7)` in the rational `ℓ¹` diamond `|c3| + |c7| ≤ 1`,
`exoticComb37 c3 c7` is a nonnegative frame function bounded in `[0, 2/3]`. -/
theorem exoticComb37_isNonnegFrameFunction {c3 c7 : ℚ} (hsum : |c3| + |c7| ≤ 1) :
    IsNonnegFrameFunction (exoticComb37 c3 c7) ∧
    (∀ v : GVec, 0 ≤ exoticComb37 c3 c7 v ∧ exoticComb37 c3 c7 v ≤ 2 / 3) := by
  have hbounds : ∀ v : GVec, 0 ≤ exoticComb37 c3 c7 v ∧ exoticComb37 c3 c7 v ≤ 2 / 3 := by
    intro v
    have habs := abs_combResidual37_le c3 c7 v
    have hle1 : |combResidual37 c3 c7 v| ≤ 1 := le_trans habs hsum
    obtain ⟨hlo, hhi⟩ := abs_le.mp hle1
    simp only [exoticComb37]
    constructor <;> linarith
  exact ⟨⟨exoticComb37_isFrameFunction c3 c7, fun v _ => (hbounds v).1⟩, hbounds⟩

/-- `exoticComb37 c3 c7` is quadratic on nonzero rays of `ℚ(i)³` if and only if `c3 = 0 ∧ c7 = 0`. -/
theorem exoticComb37_quadratic_iff (c3 c7 : ℚ) :
    (∃ ρ : HermForm3, ∀ v : GVec, v.NonZero → exoticComb37 c3 c7 v = quadRay ρ v) ↔
      (c3 = 0 ∧ c7 = 0) := by
  constructor
  · rintro ⟨ρ, hρ⟩
    obtain ⟨h1, h2, h3, h12, h13, h23, h12i, h13i, h23i⟩ :=
      combResidual37_vanishes_on_nine_rays c3 c7
    have htomo_id :
        tomographyForm (exoticComb37 c3 c7) = ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ := by
      ext <;>
        simp [tomographyForm, exoticComb37, h1, h2, h3, h12, h13, h23, h12i, h13i, h23i]
    have hm := tomography_matches_nine_rays (exoticComb37 c3 c7)
    have hρ_eq : tomographyForm (exoticComb37 c3 c7) = ρ := by
      apply tomography_unique (tomographyForm (exoticComb37 c3 c7)) ρ
      · rw [hm.1, hρ tomo_e1 tomo_e1_nonZero]
      · rw [hm.2.1, hρ tomo_e2 tomo_e2_nonZero]
      · rw [hm.2.2.1, hρ tomo_e3 tomo_e3_nonZero]
      · rw [hm.2.2.2.1, hρ tomo_e12 tomo_e12_nonZero]
      · rw [hm.2.2.2.2.1, hρ tomo_e13 tomo_e13_nonZero]
      · rw [hm.2.2.2.2.2.1, hρ tomo_e23 tomo_e23_nonZero]
      · rw [hm.2.2.2.2.2.2.1, hρ tomo_e12i tomo_e12i_nonZero]
      · rw [hm.2.2.2.2.2.2.2.1, hρ tomo_e13i tomo_e13i_nonZero]
      · rw [hm.2.2.2.2.2.2.2.2, hρ tomo_e23i tomo_e23i_nonZero]
    have hρ_id : ρ = ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ := hρ_eq.symm.trans htomo_id
    have hw111 := hρ witness_111 witness_111_nonZero
    have hwp7 := hρ witness_p7 witness_p7_nonZero
    rw [hρ_id] at hw111 hwp7
    have hq111 : quadRay ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ witness_111 = 1 / 3 := by
      simp [quadRay, quadNum, normSqVec, GaussRat.normSq, witness_111, gv]; norm_num
    have hqp7 : quadRay ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ witness_p7 = 1 / 3 := by
      simp [quadRay, quadNum, normSqVec, GaussRat.normSq, witness_p7, gv]; norm_num
    have hex111 : exoticComb37 c3 c7 witness_111 = (1 + c3) / 3 := by
      simp [exoticComb37, combResidual37_witness_111]
    have hexp7 : exoticComb37 c3 c7 witness_p7 = (1 + c7) / 3 := by
      simp [exoticComb37, combResidual37_witness_p7]
    exact ⟨by linarith, by linarith⟩
  · rintro ⟨rfl, rfl⟩
    refine ⟨⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩, ?_⟩
    intro v hv
    have hpos := normSqVec_pos_of_nonZero hv
    have hnz : normSqVec v ≠ 0 := ne_of_gt hpos
    have hnum : quadNum ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ v = (1 / 3) * normSqVec v := by
      simp only [quadNum, normSqVec]
      ring
    simp only [exoticComb37, combResidual37, zero_mul, add_zero, quadRay, hnum,
      mul_div_cancel_right₀ (1 / 3 : ℚ) hnz]

/-- `exoticComb37 c3 c7` is archimedean-continuous at `tomo_e1 = (1, 0, 0)` if and only if
`c3 = 0 ∧ c7 = 0`. -/
theorem exoticComb37_archimedeanContinuousAt_tomo_e1_iff (c3 c7 : ℚ) :
    IsArchimedeanContinuousAt (exoticComb37 c3 c7) tomo_e1 ↔ (c3 = 0 ∧ c7 = 0) := by
  constructor
  · intro hcont
    have hcont3 :
        IsArchimedeanContinuousAt
          (fun v => (1 : ℚ) / 3 + combResidual37 (c3 / 3) (c7 / 3) v) tomo_e1 := by
      have heq :
          (fun v => (1 : ℚ) / 3 + combResidual37 (c3 / 3) (c7 / 3) v) = exoticComb37 c3 c7 := by
        funext v
        simp only [exoticComb37, combResidual37]
        ring
      rw [heq]
      exact hcont
    have hconst_cont : IsArchimedeanContinuousAt (fun _ : GVec => (1 : ℚ) / 3) tomo_e1 := by
      intro ε hε
      refine ⟨1, by norm_num, ?_⟩
      intro v _ _
      simp [hε]
    have hsub_cont :
        IsArchimedeanContinuousAt
          (fun v =>
            ((1 : ℚ) / 3 + combResidual37 (c3 / 3) (c7 / 3) v) -
              combResidual37 (c3 / 3) (c7 / 3) v)
          tomo_e1 := by
      have heq :
          (fun v =>
            ((1 : ℚ) / 3 + combResidual37 (c3 / 3) (c7 / 3) v) -
              combResidual37 (c3 / 3) (c7 / 3) v) =
          (fun _ : GVec => (1 : ℚ) / 3) := by
        funext v; ring
      rw [heq]
      exact hconst_cont
    obtain ⟨hc3, hc7⟩ :=
      combResidual37_coeffs_zero_of_archimedeanContinuousAt_tomo_e1 hcont3 hsub_cont
    exact ⟨by linarith, by linarith⟩
  · rintro ⟨rfl, rfl⟩
    intro ε hε
    refine ⟨1, by norm_num, ?_⟩
    intro v _ _
    simp [exoticComb37, combResidual37, hε]

end BornFinite.GaussianTomography

#print axioms BornFinite.GaussianTomography.inner_applyVec_im_zero
#print axioms BornFinite.GaussianTomography.inner_applyVec_re_eq_quadNum
#print axioms BornFinite.GaussianTomography.quadRay_smul
#print axioms BornFinite.GaussianTomography.quadNum_orthogonal_weighted_sum
#print axioms BornFinite.GaussianTomography.quadRay_frame_sum
#print axioms BornFinite.GaussianTomography.quadRay_isFrameFunction
#print axioms BornFinite.GaussianTomography.tomography_matches_nine_rays
#print axioms BornFinite.GaussianTomography.tomography_trace_one
#print axioms BornFinite.GaussianTomography.tomography_isFrameFunction
#print axioms BornFinite.GaussianTomography.tomography_unique
#print axioms BornFinite.GaussianTomography.tomographyForm_quadRay
#print axioms BornFinite.GaussianTomography.residual_is_zero_weight
#print axioms BornFinite.GaussianTomography.residual_vanishes_on_nine_rays
#print axioms BornFinite.GaussianTomography.signed_rigidity_iff_zero_residual
#print axioms BornFinite.GaussianTomography.nonneg_frameFunction_bounds
#print axioms BornFinite.GaussianTomography.abs_quadRay_le
#print axioms BornFinite.GaussianTomography.nonneg_residual_is_bounded
#print axioms BornFinite.GaussianTomography.one_sided_lower_bound_implies_upper_bound
#print axioms BornFinite.GaussianTomography.nonneg_rigidity_iff_bounded_zero_residual
#print axioms BornFinite.GaussianTomography.gaussian_norm_div_four_witness
#print axioms BornFinite.GaussianTomography.gaussian_norm_eight_primitive_witness
#print axioms BornFinite.GaussianTomography.gaussian_coord_norm_mod_four
#print axioms BornFinite.GaussianTomography.primitive_gaussian_norm_mod_four_iff
#print axioms BornFinite.GaussianTomography.eq_quadRay_all_of_zero_at_zero
#print axioms BornFinite.GaussianTomography.traceInner_self_eq_zero_iff
#print axioms BornFinite.GaussianTomography.traceInner_ext
#print axioms BornFinite.GaussianTomography.traceInner_rayProj
#print axioms BornFinite.GaussianTomography.rayProj_smul
#print axioms BornFinite.GaussianTomography.rayProj_tr
#print axioms BornFinite.GaussianTomography.rayProj_frame_sum
#print axioms BornFinite.GaussianTomography.rayProj_nine_rays_span_hermForm3
#print axioms BornFinite.GaussianTomography.v3Rat_normSq_even
#print axioms BornFinite.GaussianTomography.detGVec_normSq_of_frame
#print axioms BornFinite.GaussianTomography.frame_v3Rat_sum_even
#print axioms BornFinite.GaussianTomography.ortho_coord_identity_x
#print axioms BornFinite.GaussianTomography.s3_orthogonal_odd_cancel
#print axioms BornFinite.GaussianTomography.s3_isZeroWeightFrameFunction
#print axioms BornFinite.GaussianTomography.s3_smul
#print axioms BornFinite.GaussianTomography.s3_isBoundedOnRays
#print axioms BornFinite.GaussianTomography.s3_vanishes_on_nine_rays
#print axioms BornFinite.GaussianTomography.witness_111_primitive
#print axioms BornFinite.GaussianTomography.witness_div_four_shell_primitive
#print axioms BornFinite.GaussianTomography.witness_div_eight_shell_primitive
#print axioms BornFinite.GaussianTomography.exists_nonzero_bounded_zero_residual
#print axioms BornFinite.GaussianTomography.not_signed_quadratic_rigidity
#print axioms BornFinite.GaussianTomography.not_nonneg_quadratic_rigidity
#print axioms BornFinite.GaussianTomography.exoticQi3_isNonnegFrameFunction
#print axioms BornFinite.GaussianTomography.exoticQi3_not_quadratic
#print axioms BornFinite.GaussianTomography.rayProj_witness_111_decomp
#print axioms BornFinite.GaussianTomography.quadRay_witness_111_kernel_relation
#print axioms BornFinite.GaussianTomography.s3_witness_111_kernel_separation
#print axioms BornFinite.GaussianTomography.s3_perturbPosRay
#print axioms BornFinite.GaussianTomography.s3_perturbNegRay
#print axioms BornFinite.GaussianTomography.distSqVec_perturbPosRay_tomo_e1
#print axioms BornFinite.GaussianTomography.distSqVec_perturbNegRay_tomo_e1
#print axioms BornFinite.GaussianTomography.s3_oscillates_near_tomo_e1
#print axioms BornFinite.GaussianTomography.not_archimedeanContinuousAt_s3_tomo_e1
#print axioms BornFinite.GaussianTomography.not_archimedeanContinuousAt_exoticQi3_tomo_e1
#print axioms BornFinite.GaussianTomography.s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1
#print axioms BornFinite.GaussianTomography.archimedeanContinuousAt_quadRay_tomo_e1
#print axioms BornFinite.GaussianTomography.quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff
#print axioms BornFinite.GaussianTomography.no_unit_norm_smul_witness_111_in_qi3
#print axioms BornFinite.GaussianTomography.witness_111_unit_sqrt3_normSq
#print axioms BornFinite.GaussianTomography.isFrameSqrt3_witness_111_even_norms
#print axioms BornFinite.GaussianTomography.zero_on_witness_111_of_sqrt3_even_v3_vanishing
#print axioms BornFinite.GaussianTomography.no_s3_even_v3_extension_to_sqrt3
#print axioms BornFinite.GaussianTomography.unit_norm_in_sqrtP_of_normSqVec_eq
#print axioms BornFinite.GaussianTomography.fourSquarePartner_ortho_and_normSqRatP
#print axioms BornFinite.GaussianTomography.isFrameSqrt7_witness_p7_norms
#print axioms BornFinite.GaussianTomography.zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear
#print axioms BornFinite.GaussianTomography.not_factorsThroughRayProjLinear_s3
#print axioms BornFinite.GaussianTomography.quadratic_rigidity_iff_factorsThroughRayProjLinear
#print axioms BornFinite.GaussianTomography.v7Rat_normSq_even
#print axioms BornFinite.GaussianTomography.frame_v7Rat_sum_even
#print axioms BornFinite.GaussianTomography.s7_orthogonal_odd_cancel
#print axioms BornFinite.GaussianTomography.s7_isZeroWeightFrameFunction
#print axioms BornFinite.GaussianTomography.s7_smul
#print axioms BornFinite.GaussianTomography.s7_isBoundedOnRays
#print axioms BornFinite.GaussianTomography.s7_vanishes_on_nine_rays
#print axioms BornFinite.GaussianTomography.witness_p7_primitive
#print axioms BornFinite.GaussianTomography.s3_s7_dual_on_witnesses
#print axioms BornFinite.GaussianTomography.exoticQi7_isNonnegFrameFunction
#print axioms BornFinite.GaussianTomography.exoticQi7_not_quadratic
#print axioms BornFinite.GaussianTomography.combResidual37_isZeroWeightFrameFunction
#print axioms BornFinite.GaussianTomography.combResidual37_vanishes_on_nine_rays
#print axioms BornFinite.GaussianTomography.combResidual37_isBoundedOnRays
#print axioms BornFinite.GaussianTomography.s3_s7_linearIndependent
#print axioms BornFinite.GaussianTomography.s7_perturb7PosRay
#print axioms BornFinite.GaussianTomography.s7_perturb7NegRay
#print axioms BornFinite.GaussianTomography.s3_perturb7PosRay
#print axioms BornFinite.GaussianTomography.s3_perturb7NegRay
#print axioms BornFinite.GaussianTomography.s7_perturbPosRay_seven_mul
#print axioms BornFinite.GaussianTomography.s7_perturbNegRay_seven_mul
#print axioms BornFinite.GaussianTomography.distSqVec_perturb7PosRay_tomo_e1
#print axioms BornFinite.GaussianTomography.distSqVec_perturb7NegRay_tomo_e1
#print axioms BornFinite.GaussianTomography.s3_s7_selective_oscillation_near_tomo_e1
#print axioms BornFinite.GaussianTomography.not_archimedeanContinuousAt_s7_tomo_e1
#print axioms BornFinite.GaussianTomography.not_archimedeanContinuousAt_exoticQi7_tomo_e1
#print axioms BornFinite.GaussianTomography.combResidual37_coeffs_zero_of_archimedeanContinuousAt_tomo_e1
#print axioms BornFinite.GaussianTomography.quadRay_add_combResidual37_archimedeanContinuousAt_tomo_e1_iff
#print axioms BornFinite.GaussianTomography.no_unit_norm_smul_witness_p7_in_qi3
#print axioms BornFinite.GaussianTomography.zero_on_witness_p7_of_sqrt7_even_v7_vanishing
#print axioms BornFinite.GaussianTomography.no_s7_even_v7_extension_to_sqrt7
#print axioms BornFinite.GaussianTomography.joint_sqrt3_sqrt7_even_valuation_eliminates_combResidual37
#print axioms BornFinite.GaussianTomography.not_factorsThroughRayProjLinear_s7
#print axioms BornFinite.GaussianTomography.factorsThroughRayProjLinear_combResidual37_iff
#print axioms BornFinite.GaussianTomography.rayProj_witness_p7_decomp
#print axioms BornFinite.GaussianTomography.quadRay_witness_p7_kernel_relation
#print axioms BornFinite.GaussianTomography.s7_witness_p7_kernel_separation
#print axioms BornFinite.GaussianTomography.cross_prime_frame_partner_norm_valuations_even
#print axioms BornFinite.GaussianTomography.exoticComb37_isNonnegFrameFunction
#print axioms BornFinite.GaussianTomography.exoticComb37_quadratic_iff
#print axioms BornFinite.GaussianTomography.exoticComb37_archimedeanContinuousAt_tomo_e1_iff

