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
#print axioms BornFinite.GaussianTomography.exists_nonzero_bounded_zero_residual
#print axioms BornFinite.GaussianTomography.not_signed_quadratic_rigidity
#print axioms BornFinite.GaussianTomography.not_nonneg_quadratic_rigidity
#print axioms BornFinite.GaussianTomography.exoticQi3_isNonnegFrameFunction
#print axioms BornFinite.GaussianTomography.exoticQi3_not_quadratic
#print axioms BornFinite.GaussianTomography.rayProj_witness_111_decomp
#print axioms BornFinite.GaussianTomography.quadRay_witness_111_kernel_relation
#print axioms BornFinite.GaussianTomography.s3_witness_111_kernel_separation

