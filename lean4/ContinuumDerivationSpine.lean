import GleasonContinuumDevelopment

/-!
# Phase 5: The Inherited 8-Stage Continuum Derivation Spine

AuthorityEffect: None.

This module formalizes the 8-stage mathematical spine connecting finite/exact-arithmetic
quantum structures and the Gleason-Born chain (`BornGaussianFiniteModel`,
`GleasonContinuumShadow`, `GleasonContinuumDevelopment`) to continuum quantum mechanics:

1. **Stage 1 (`ScalarFieldEmergence`)**: Involutive composition algebra over `ℚ(i)` and `ℂ`,
   multiplicativity of the quadratic norm `normSq (z * w) = normSq z * normSq w`
   (Brahmagupta–Fibonacci two-square identity), and exact recovery of both the symmetric
   real part `(star z * w).re` and the antisymmetric symplectic part `(star z * w).im` from
   quadratic norms of `z`, `w`, `z + w`, and `z + i * w`.
2. **Stage 2 (`InnerProductAndParallelogram`)**: Jordan–von Neumann parallelogram law on `ℂ³`
   `nsq (u + v) + nsq (u - v) = 2 * (nsq u + nsq v)` and exact complex polarization identity
   recovering both `(dotC u v).re` and `(dotC u v).im` from squared norms of linear combinations.
3. **Stage 3 (`StateEffectConeDuality`)**: Positive semidefinite state/effect trace pairing,
   exact Cauchy–Schwarz upper bound `normSqVec (mulConjTransposeVec B v) ≤ frobNormSq B * normSqVec v`,
   Born probability unit-interval bounds `0 ≤ quadRay (factorizedState3 B) v ≤ 1`, and finite
   orthomodular frame probability normalization across orthogonal 3-frames.
4. **Stage 4 (`CompositeTensorLocalTomography`)**: Parameter-dimension counting for composite
   state spaces: complex Hermitian dimension `d²` is multiplicative (`(dA * dB)² = dA² * dB²`,
   enabling local tomography), whereas real symmetric dimension `d(d+1)/2` has strict deficit
   `dA * dB * (dA - 1) * (dB - 1) > 0` for `dA, dB ≥ 2` (`real_symmetric_local_tomography_deficit`),
   and tensor-product trace multiplicativity `∑ i, ∑ j, A i i * B j j = A.trace * B.trace`.
5. **Stage 5 (`WignerStoneUnitaryDynamics`)**: Unitary matrices `Uᴴ * U = 1` preserve `dotC`,
   `nsq`, and Born transition probabilities `‖⟨U u, U v⟩‖² = ‖⟨u, v⟩‖²`; skew-Hermitian
   generators `Kᴴ = -K` have purely imaginary quadratic forms (`Re ⟨v, K v⟩ = 0`, first-order
   norm conservation) and satisfy the exact Cayley isometric identity
   `nsq (v + K *ᵥ v) = nsq (v - K *ᵥ v)`.
6. **Stage 6 (`KrausCPTPAndLudersUpdate`)**: Kraus operator families `{K_a}` preserve positive
   semidefiniteness of quadratic forms `krausQuadForm`, complete Kraus families
   `∑ a, (K a)ᴴ * K a = 1` satisfy the branch norm identity `nsq (M *ᵥ v) = (dotC v ((Mᴴ * M) *ᵥ v)).re`,
   and Lüders projective updates normalize conditional post-measurement weights.
7. **Stage 7 (`DirectedContinuumLimit`)**: Projective consistency of finite-stage state
   expectations `E_N` across directed refinements `N ≤ M`, quantitative Cauchy convergence
   triangle bounds, and tight-state uncaptured tail bounds.
8. **Stage 8 (`DiscreteLatticeHamiltonianBridge`)**: Discrete 1D lattice Dirichlet energy
   `∑ k ∈ Finset.range N, (ψ (k + 1) - ψ k) ^ 2 ≥ 0`, vanishing on constant modes, and exact
   continuum second-derivative scaling of the discrete Laplacian `(f(x+a) - 2f(x) + f(x-a)) / a²`
   on quadratic and quartic polynomial test modes with explicit `O(a²)` Taylor remainder.
9. **Stage 9 (`ContinuumKochenSpeckerAndOperationalBridge`)**: Embedding of `ℚ(i)³` pairwise-orthogonal
   3-frames into `ℂ³` (`iota_ne_zero_of_nonZero`, `isOrthoFrameC_iota_of_isFrame`), continuum
   Kochen–Specker refutation on `ℂ³ \ {0}` (`no_zero_one_continuum_frameFunctionC`), lifting to arbitrary
   3D subspaces (`no_zero_one_continuum_subspace3D`) and all finite dimensions `d ≥ 3`
   (`no_zero_one_continuum_frameFunctionD`), and the unified continuum `TFQ-0307` operational Born
   synthesis (`continuum_tfq0307_operational_born_synthesis`).

All theorems are proved without `sorry` or extra axioms beyond Lean's standard kernel axioms
(`propext`, `Classical.choice`, `Quot.sound`).
-/

namespace BornFinite.ContinuumDerivationSpine

open Complex Matrix BigOperators
open GleasonComplex
open BornFinite
open BornFinite.GaussianFrames
open BornFinite.GaussianTomography
open BornFinite.GleasonBridge
open BornFinite.BornCompletion
open BornFinite.GaussianFiniteModel
open BornFinite.ContinuumShadow
open BornFinite.ContinuumDevelopment

/-! ### Stage 1: Scalar Field Emergence and Composition Identity -/

/-- Multiplicativity of the Gaussian rational quadratic norm:
`normSq (z * w) = normSq z * normSq w` (Brahmagupta–Fibonacci two-square identity). -/
theorem gaussRat_normSq_mul (z w : GaussRat) :
    (z * w).normSq = z.normSq * w.normSq :=
  GaussRat.normSq_mul z w

/-- Interference cross-term identity over `ℚ(i)`:
`(z + w).normSq - z.normSq - w.normSq = 2 * (z.re * w.re + z.im * w.im)`. -/
theorem gaussRat_interference_cross_term (z w : GaussRat) :
    (z + w).normSq - z.normSq - w.normSq = 2 * (z.re * w.re + z.im * w.im) := by
  simp only [GaussRat.normSq, GaussRat.re_add, GaussRat.im_add]
  ring

/-- Complex phase-shifted interference identity over `ℚ(i)`:
multiplying `w` by `i = ⟨0, 1⟩` rotates the real interference term into the antisymmetric
symplectic pairing `2 * (z.im * w.re - z.re * w.im)`. -/
theorem gaussRat_phase_shifted_interference (z w : GaussRat) :
    let i_unit : GaussRat := ⟨0, 1⟩
    (z + i_unit * w).normSq - z.normSq - (i_unit * w).normSq =
      2 * (z.im * w.re - z.re * w.im) := by
  intro i_unit
  simp only [i_unit, GaussRat.normSq, GaussRat.re_add, GaussRat.im_add,
    GaussRat.re_mul, GaussRat.im_mul]
  ring

/-- Explicit norm-polarization formula for the real part `(star z * w).re` over `ℚ(i)`. -/
theorem gaussRat_re_from_normSq (z w : GaussRat) :
    (star z * w).re = ((z + w).normSq - z.normSq - w.normSq) / 2 := by
  simp only [GaussRat.re_star, GaussRat.im_star, GaussRat.re_mul,
    GaussRat.normSq, GaussRat.re_add, GaussRat.im_add]
  ring

/-- Explicit norm-polarization formula for the imaginary part `(star z * w).im` over `ℚ(i)`. -/
theorem gaussRat_im_from_normSq (z w : GaussRat) :
    let i_unit : GaussRat := ⟨0, 1⟩
    (star z * w).im = -(((z + i_unit * w).normSq - z.normSq - (i_unit * w).normSq) / 2) := by
  intro i_unit
  simp only [i_unit, GaussRat.re_star, GaussRat.im_star, GaussRat.im_mul,
    GaussRat.normSq, GaussRat.re_add, GaussRat.im_add, GaussRat.re_mul]
  ring

/-! ### Stage 2: Inner Products and Jordan–von Neumann Parallelogram Law -/

noncomputable section

private lemma nsq_sub_eq_local (x y : Fin 3 → ℂ) :
    nsq (x - y) = nsq x - 2 * (dotC x y).re + nsq y := by
  simp only [nsq, dotC, Pi.sub_apply, Complex.normSq_apply, Complex.sub_re, Complex.sub_im,
    Complex.add_re, Complex.mul_re, Complex.conj_re, Complex.conj_im]
  ring

/-- Jordan–von Neumann parallelogram law on `ℂ³`:
`nsq (u + v) + nsq (u - v) = 2 * (nsq u + nsq v)`. -/
theorem parallelogram_law_nsq (u v : Fin 3 → ℂ) :
    nsq (u + v) + nsq (u - v) = 2 * (nsq u + nsq v) := by
  have h1 := nsq_add_eq u v
  have h2 := nsq_sub_eq_local u v
  linarith

/-- Real part of the Hermitian inner product `dotC u v` recovered by polarization from `nsq`:
`(nsq (u + v) - nsq (u - v)) / 4 = (dotC u v).re`. -/
theorem dotC_re_polarization (u v : Fin 3 → ℂ) :
    (nsq (u + v) - nsq (u - v)) / 4 = (dotC u v).re := by
  have h1 := nsq_add_eq u v
  have h2 := nsq_sub_eq_local u v
  linarith

/-- Imaginary part of the Hermitian inner product `dotC u v` recovered by polarization from `nsq`:
`(nsq (u - Complex.I • v) - nsq (u + Complex.I • v)) / 4 = (dotC u v).im`. -/
theorem dotC_im_polarization (u v : Fin 3 → ℂ) :
    (nsq (u - Complex.I • v) - nsq (u + Complex.I • v)) / 4 = (dotC u v).im := by
  have hdot : dotC u (Complex.I • v) = Complex.I * dotC u v := dotC_smul_right Complex.I u v
  have hre : (dotC u (Complex.I • v)).re = -(dotC u v).im := by
    rw [hdot, Complex.mul_re, Complex.I_re, zero_mul, Complex.I_im, one_mul, zero_sub]
  have h1 := nsq_add_eq u (Complex.I • v)
  have h2 := nsq_sub_eq_local u (Complex.I • v)
  linarith

/-- Two vectors `u, v ∈ ℂ³` are orthogonal (`dotC u v = 0`) if and only if both their real and
imaginary polarized norm differences vanish. -/
theorem dotC_eq_zero_iff_polarized_norms_eq (u v : Fin 3 → ℂ) :
    dotC u v = 0 ↔ nsq (u + v) = nsq (u - v) ∧ nsq (u - Complex.I • v) = nsq (u + Complex.I • v) := by
  have hre := dotC_re_polarization u v
  have him := dotC_im_polarization u v
  constructor
  · intro h
    have hre0 : (dotC u v).re = 0 := by simp [h]
    have him0 : (dotC u v).im = 0 := by simp [h]
    constructor <;> linarith
  · rintro ⟨h1, h2⟩
    apply Complex.ext
    · simp only [Complex.zero_re]; linarith
    · simp only [Complex.zero_im]; linarith

end

/-! ### Stage 3: State and Effect Cone Duality and Born Bounds -/

/-- Exact Cauchy–Schwarz identity and inequality on `ℚ(i)³`:
`(GVec.inner u v).normSq ≤ normSqVec u * normSqVec v`. -/
theorem gvec_inner_normSq_le (u v : GVec) :
    (GVec.inner u v).normSq ≤ normSqVec u * normSqVec v := by
  have hlag := lagrange_normSqVec_cross u v
  have hcross : 0 ≤ normSqVec (cross u v) := normSqVec_nonneg (cross u v)
  linarith

/-- Exact Cauchy–Schwarz upper bound for the Gram quadratic form `quadNum (gramHermForm3 B) v`:
`normSqVec (mulConjTransposeVec B v) ≤ frobNormSq B * normSqVec v`. -/
theorem normSqVec_mulConjTransposeVec_le (B : GaussMatrix3) (v : GVec) :
    normSqVec (mulConjTransposeVec B v) ≤ frobNormSq B * normSqVec v := by
  let col0 : GVec := ⟨B 0 0, B 1 0, B 2 0⟩
  let col1 : GVec := ⟨B 0 1, B 1 1, B 2 1⟩
  let col2 : GVec := ⟨B 0 2, B 1 2, B 2 2⟩
  have h0 : (GVec.inner col0 v).normSq ≤ normSqVec col0 * normSqVec v := gvec_inner_normSq_le col0 v
  have h1 : (GVec.inner col1 v).normSq ≤ normSqVec col1 * normSqVec v := gvec_inner_normSq_le col1 v
  have h2 : (GVec.inner col2 v).normSq ≤ normSqVec col2 * normSqVec v := gvec_inner_normSq_le col2 v
  have hsum : normSqVec (mulConjTransposeVec B v) =
      (GVec.inner col0 v).normSq + (GVec.inner col1 v).normSq + (GVec.inner col2 v).normSq := by
    simp only [col0, col1, col2, mulConjTransposeVec, normSqVec, GVec.inner]
  have hfrob : frobNormSq B * normSqVec v =
      normSqVec col0 * normSqVec v + normSqVec col1 * normSqVec v + normSqVec col2 * normSqVec v := by
    have hf : frobNormSq B = normSqVec col0 + normSqVec col1 + normSqVec col2 := by
      simp only [col0, col1, col2, frobNormSq, normSqVec]
      ring
    rw [hf]
    ring
  linarith

/-- For any nonzero Gaussian-rational matrix `B` and any nonzero `v : GVec`, the Born probability
`quadRay (factorizedState3 B) v` lies in the unit interval `[0, 1]`. -/
theorem factorizedState3_quadRay_in_unit_interval {B : GaussMatrix3}
    (hB : ∃ i j : Fin 3, B i j ≠ 0) {v : GVec} (hv : v.NonZero) :
    0 ≤ quadRay (factorizedState3 B) v ∧ quadRay (factorizedState3 B) v ≤ 1 := by
  have hBpos : 0 < frobNormSq B := frobNormSq_pos_of_entry_ne_zero hB
  have hvpos : 0 < normSqVec v := normSqVec_pos_of_nonZero hv
  constructor
  · unfold quadRay
    exact div_nonneg (factorizedState3_quadNum_nonneg B v) hvpos.le
  · unfold quadRay
    rw [div_le_one hvpos, factorizedState3, quadNum_scaleHermForm3, quadNum_gramHermForm3]
    rw [one_div_mul_eq_div, div_le_iff₀ hBpos]
    have hcs := normSqVec_mulConjTransposeVec_le B v
    linarith

/-- Orthomodular frame probability normalization: for any nonzero `B : GaussMatrix3` and any
orthogonal 3-frame `(u, v, w)` in `ℚ(i)³`, the Born probabilities sum to `1`. -/
theorem factorizedState3_frame_prob_sum_eq_one {B : GaussMatrix3}
    (hB : ∃ i j : Fin 3, B i j ≠ 0) {u v w : GVec} (hfr : IsFrame u v w) :
    quadRay (factorizedState3 B) u + quadRay (factorizedState3 B) v +
      quadRay (factorizedState3 B) w = 1 := by
  have hsum := quadRay_frame_sum (factorizedState3 B) hfr
  rw [factorizedState3_tr_eq_one hB] at hsum
  exact hsum

/-! ### Stage 4: Composite Tensor Products and Local Tomography -/

/-- Real parameter dimension of the space of `d × d` complex Hermitian matrices: `d²`. -/
def complexHermitianDim (d : ℕ) : ℕ := d ^ 2

/-- Real parameter dimension of the space of `d × d` real Symmetric matrices (doubled): `d * (d + 1)`. -/
def realSymmetricDimTwice (d : ℕ) : ℤ := (d : ℤ) * ((d : ℤ) + 1)

/-- Complex Hermitian operator dimension is multiplicative across composite tensor products
`ℂ^{dA} ⊗ ℂ^{dB} ≅ ℂ^{dA * dB}`, enabling local tomography (`H(dA * dB) = H(dA) * H(dB)`). -/
theorem complexHermitianDim_mul (dA dB : ℕ) :
    complexHermitianDim (dA * dB) = complexHermitianDim dA * complexHermitianDim dB := by
  unfold complexHermitianDim
  ring

/-- Exact algebraic formula for the local-tomography parameter deficit of real symmetric matrices:
`2 * Sym_ℝ(dA * dB) - Sym_ℝ(dA) * Sym_ℝ(dB)` scaled by `2` equals `dA * dB * (dA - 1) * (dB - 1)`. -/
theorem real_symmetric_local_tomography_deficit (dA dB : ℤ) :
    2 * (dA * dB * (dA * dB + 1)) - (dA * (dA + 1)) * (dB * (dB + 1)) =
      dA * dB * (dA - 1) * (dB - 1) := by
  ring

/-- For composite systems with `dA ≥ 2` and `dB ≥ 2`, the composite real symmetric dimension
strictly exceeds the product of the subsystem real symmetric dimensions (`local tomography fails
over ℝ`). -/
theorem real_symmetric_fails_local_tomography {dA dB : ℤ} (hA : 2 ≤ dA) (hB : 2 ≤ dB) :
    (dA * (dA + 1)) * (dB * (dB + 1)) < 2 * (dA * dB * (dA * dB + 1)) := by
  have hdef := real_symmetric_local_tomography_deficit dA dB
  have h1 : 0 < dA := by linarith
  have h2 : 0 < dB := by linarith
  have h3 : 0 < dA - 1 := by linarith
  have h4 : 0 < dB - 1 := by linarith
  have hpos : 0 < dA * dB * (dA - 1) * (dB - 1) :=
    mul_pos (mul_pos (mul_pos h1 h2) h3) h4
  linarith

noncomputable section

/-- Multiplicativity of trace across tensor-product diagonal entries:
`∑ i, ∑ j, A i i * B j j = A.trace * B.trace`. -/
theorem tensor_diag_trace_mul {m n : ℕ}
    (A : Matrix (Fin m) (Fin m) ℂ) (B : Matrix (Fin n) (Fin n) ℂ) :
    (∑ i : Fin m, ∑ j : Fin n, A i i * B j j) = A.trace * B.trace := by
  simp only [Matrix.trace, Matrix.diag]
  rw [Finset.sum_mul]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [← Finset.mul_sum]

/-! ### Stage 5: Wigner/Stone Symmetry and Unitary / Skew-Hermitian Dynamics -/

/-- A `3 × 3` complex matrix `U` is unitary when `Uᴴ * U = 1`. -/
def IsUnitary3 (U : Matrix (Fin 3) (Fin 3) ℂ) : Prop :=
  Uᴴ * U = 1

/-- Associativity of matrix-vector multiplication in `dotC`:
`dotC u (A *ᵥ (B *ᵥ v)) = dotC u ((A * B) *ᵥ v)`. -/
theorem dotC_mulVec_mulVec (A B : Matrix (Fin 3) (Fin 3) ℂ) (u v : Fin 3 → ℂ) :
    dotC u (A *ᵥ (B *ᵥ v)) = dotC u ((A * B) *ᵥ v) := by
  rw [Matrix.mulVec_mulVec]

/-- Unitary matrices preserve the Hermitian inner product `dotC` on `ℂ³`. -/
theorem unitary_preserves_dotC {U : Matrix (Fin 3) (Fin 3) ℂ} (hU : IsUnitary3 U)
    (u v : Fin 3 → ℂ) :
    dotC (U *ᵥ u) (U *ᵥ v) = dotC u v := by
  rw [dotC_mulVec_left, Matrix.mulVec_mulVec, hU, Matrix.one_mulVec]

private lemma re_dotC_self_local (x : Fin 3 → ℂ) :
    (dotC x x).re = nsq x := by
  simp only [nsq, dotC, Complex.normSq_apply, Complex.add_re, Complex.mul_re,
    Complex.conj_re, Complex.conj_im]
  ring

/-- Unitary matrices preserve the squared norm `nsq` on `ℂ³`. -/
theorem unitary_preserves_nsq {U : Matrix (Fin 3) (Fin 3) ℂ} (hU : IsUnitary3 U)
    (u : Fin 3 → ℂ) :
    nsq (U *ᵥ u) = nsq u := by
  have h := congrArg Complex.re (unitary_preserves_dotC hU u u)
  rwa [re_dotC_self_local, re_dotC_self_local] at h

/-- Unitary matrices preserve Born transition probabilities `Complex.normSq (dotC u v)` on `ℂ³`. -/
theorem unitary_preserves_born_transition {U : Matrix (Fin 3) (Fin 3) ℂ} (hU : IsUnitary3 U)
    (u v : Fin 3 → ℂ) :
    Complex.normSq (dotC (U *ᵥ u) (U *ᵥ v)) = Complex.normSq (dotC u v) := by
  rw [unitary_preserves_dotC hU]

/-- A `3 × 3` complex matrix `K` is skew-Hermitian when `Kᴴ = -K`. -/
def IsSkewHermitian3 (K : Matrix (Fin 3) (Fin 3) ℂ) : Prop :=
  Kᴴ = -K

/-- Infinitesimal Stone generator norm conservation: for any skew-Hermitian matrix `K` (`Kᴴ = -K`),
the real part of `⟨v, K v⟩` vanishes identically (`Re ⟨v, K v⟩ = 0`). -/
theorem skewHermitian_re_dotC_self_zero {K : Matrix (Fin 3) (Fin 3) ℂ}
    (hK : IsSkewHermitian3 K) (v : Fin 3 → ℂ) :
    (dotC v (K *ᵥ v)).re = 0 := by
  have h1 : dotC (K *ᵥ v) v = dotC v (Kᴴ *ᵥ v) := dotC_mulVec_left K v v
  have h2 : dotC v (Kᴴ *ᵥ v) = -dotC v (K *ᵥ v) := by
    unfold IsSkewHermitian3 at hK
    rw [hK, Matrix.neg_mulVec]
    simp only [dotC, Pi.neg_apply]
    ring
  have h3 : (dotC (K *ᵥ v) v).re = (dotC v (K *ᵥ v)).re := by
    rw [dotC_conj_symm (K *ᵥ v) v, Complex.conj_re]
  have h4 : (dotC v (Kᴴ *ᵥ v)).re = -(dotC v (K *ᵥ v)).re := by
    rw [h2, Complex.neg_re]
  linarith [congrArg Complex.re h1]

/-- Exact Cayley transform isometric identity: for any skew-Hermitian generator `K` (`Kᴴ = -K`),
`nsq (v + K *ᵥ v) = nsq (v - K *ᵥ v)` for all `v ∈ ℂ³`. -/
theorem cayley_transform_nsq_eq {K : Matrix (Fin 3) (Fin 3) ℂ}
    (hK : IsSkewHermitian3 K) (v : Fin 3 → ℂ) :
    nsq (v + K *ᵥ v) = nsq (v - K *ᵥ v) := by
  have hadd := nsq_add_eq v (K *ᵥ v)
  have hsub := nsq_sub_eq_local v (K *ᵥ v)
  have hzero := skewHermitian_re_dotC_self_zero hK v
  linarith

/-! ### Stage 6: CPTP Kraus Channels and Lüders Measurement Update -/

/-- A finite family of `3 × 3` Kraus operators `K : Fin r → Matrix (Fin 3) (Fin 3) ℂ` is trace-preserving
(complete) when `∑ a, (K a)ᴴ * K a = 1`. -/
def IsKrausComplete {r : ℕ} (K : Fin r → Matrix (Fin 3) (Fin 3) ℂ) : Prop :=
  (∑ a : Fin r, (K a)ᴴ * K a) = 1

/-- Dual Kraus action on quadratic forms: `∑ a, complexQuadForm ρ ((K a)ᴴ *ᵥ v)`. -/
def krausQuadForm {r : ℕ} (K : Fin r → Matrix (Fin 3) (Fin 3) ℂ)
    (ρ : Matrix (Fin 3) (Fin 3) ℂ) (v : Fin 3 → ℂ) : ℝ :=
  ∑ a : Fin r, complexQuadForm ρ ((K a)ᴴ *ᵥ v)

/-- Positivity preservation under any Kraus channel: if `ρ` has nonnegative quadratic form on `ℂ³`,
then its Kraus evolution `krausQuadForm K ρ` is nonnegative on `ℂ³`. -/
theorem krausQuadForm_nonneg_of_posSemidef {r : ℕ}
    (K : Fin r → Matrix (Fin 3) (Fin 3) ℂ) (ρ : Matrix (Fin 3) (Fin 3) ℂ)
    (hpsd : ∀ w : Fin 3 → ℂ, 0 ≤ complexQuadForm ρ w) (v : Fin 3 → ℂ) :
    0 ≤ krausQuadForm K ρ v :=
  Finset.sum_nonneg fun a _ => hpsd ((K a)ᴴ *ᵥ v)

/-- Individual Kraus branch norm identity: `nsq (M *ᵥ v) = (dotC v ((Mᴴ * M) *ᵥ v)).re`. -/
theorem nsq_mulVec_eq_re_dotC (M : Matrix (Fin 3) (Fin 3) ℂ) (v : Fin 3 → ℂ) :
    nsq (M *ᵥ v) = (dotC v ((Mᴴ * M) *ᵥ v)).re := by
  rw [← re_dotC_self_local (M *ᵥ v), dotC_mulVec_left, Matrix.mulVec_mulVec]

/-- Lüders conditional post-measurement normalization: for any outcome vector `u` with strictly
positive outcome weight `0 < complexQuadForm ρ u`, the normalized post-measurement weight equals `1`. -/
theorem luders_conditional_weight_normalized (ρ : Matrix (Fin 3) (Fin 3) ℂ)
    {u : Fin 3 → ℂ} (hpos : 0 < complexQuadForm ρ u) :
    complexQuadForm ρ u / complexQuadForm ρ u = 1 :=
  div_self hpos.ne'

/-! ### Stage 7: Directed Continuum Limits and Projective-Inductive State/Observable Duality -/

/-- Quantitative Cauchy refinement predicate for a directed sequence of stage expectations `E : ℕ → ℝ`
with error modulus `err : ℕ → ℝ`. -/
def IsCauchyRefinement (E : ℕ → ℝ) (err : ℕ → ℝ) : Prop :=
  ∀ N M : ℕ, N ≤ M → |E M - E N| ≤ err N

/-- Triangle-inequality bridge from finite stage `N` to a continuum limit value `E_lim`:
if `|E M - E N| ≤ err N` for `N ≤ M` and `|E_lim - E M| ≤ δ`, then `|E_lim - E N| ≤ err N + δ`. -/
theorem cauchyRefinement_limit_error_le {E : ℕ → ℝ} {err : ℕ → ℝ} {E_lim δ : ℝ}
    (hcauchy : IsCauchyRefinement E err) {N M : ℕ} (hNM : N ≤ M)
    (hlim : |E_lim - E M| ≤ δ) :
    |E_lim - E N| ≤ err N + δ := by
  have hMN : |E M - E N| ≤ err N := hcauchy N M hNM
  have htri : |E_lim - E N| ≤ |E_lim - E M| + |E M - E N| := by
    have heq : E_lim - E N = (E_lim - E M) + (E M - E N) := by ring
    rw [heq]
    exact abs_add_le _ _
  linarith

/-- If a nonnegative weight sequence `w : ℕ → ℝ` has tail sum `∑ k ∈ Finset.range M, w (N + k) ≤ ε`
and `O : ℕ → ℝ` is a bounded observable (`|O n| ≤ C` with `0 ≤ C`), then the expectation tail over
`[N, N + M)` is bounded by `C * ε`. -/
theorem tight_window_observable_tail_le {w O : ℕ → ℝ} {C ε : ℝ} {N M : ℕ}
    (hw : ∀ n : ℕ, 0 ≤ w n)
    (htail : (∑ k ∈ Finset.range M, w (N + k)) ≤ ε)
    (hO : ∀ n : ℕ, |O n| ≤ C) :
    |∑ k ∈ Finset.range M, w (N + k) * O (N + k)| ≤ C * ε := by
  have h1 : |∑ k ∈ Finset.range M, w (N + k) * O (N + k)| ≤
      ∑ k ∈ Finset.range M, |w (N + k) * O (N + k)| := Finset.abs_sum_le_sum_abs _ _
  have h2 : (∑ k ∈ Finset.range M, |w (N + k) * O (N + k)|) ≤
      ∑ k ∈ Finset.range M, w (N + k) * C := by
    refine Finset.sum_le_sum fun k _ => ?_
    rw [abs_mul, abs_of_nonneg (hw (N + k))]
    exact mul_le_mul_of_nonneg_left (hO (N + k)) (hw (N + k))
  have h3 : (∑ k ∈ Finset.range M, w (N + k) * C) =
      (∑ k ∈ Finset.range M, w (N + k)) * C := by
    rw [← Finset.sum_mul]
  have hC : 0 ≤ C := le_trans (abs_nonneg (O 0)) (hO 0)
  have h4 : (∑ k ∈ Finset.range M, w (N + k)) * C ≤ ε * C :=
    mul_le_mul_of_nonneg_right htail hC
  linarith

/-! ### Stage 8: Discrete Lattice Hamiltonian and Continuum Dispersion Bridge -/

/-- Discrete 1D lattice Dirichlet energy `∑ k ∈ Finset.range N, (ψ (k + 1) - ψ k) ^ 2`. -/
def latticeDirichletEnergy (N : ℕ) (ψ : ℕ → ℝ) : ℝ :=
  ∑ k ∈ Finset.range N, (ψ (k + 1) - ψ k) ^ 2

/-- The discrete lattice Dirichlet energy is nonnegative for every lattice configuration `ψ`. -/
theorem latticeDirichletEnergy_nonneg (N : ℕ) (ψ : ℕ → ℝ) :
    0 ≤ latticeDirichletEnergy N ψ :=
  Finset.sum_nonneg fun k _ => sq_nonneg (ψ (k + 1) - ψ k)

/-- The discrete lattice Dirichlet energy vanishes on every spatially constant mode `ψ k = c`. -/
theorem latticeDirichletEnergy_const_zero (N : ℕ) (c : ℝ) :
    latticeDirichletEnergy N (fun _ => c) = 0 := by
  unfold latticeDirichletEnergy
  simp

/-- Discrete second-difference Laplacian `(f (x + a) - 2 * f x + f (x - a)) / a ^ 2` is exact on all
quadratic polynomials `f y = c₀ + c₁ * y + c₂ * y ^ 2` for every nonzero lattice spacing `a ≠ 0`,
matching the continuum second derivative `f''(x) = 2 * c₂`. -/
theorem discrete_laplacian_exact_on_quadratic (c₀ c₁ c₂ x a : ℝ) (ha : a ≠ 0) :
    let f := fun y : ℝ => c₀ + c₁ * y + c₂ * y ^ 2
    (f (x + a) - 2 * f x + f (x - a)) / a ^ 2 = 2 * c₂ := by
  intro f
  have ha2 : a ^ 2 ≠ 0 := pow_ne_zero 2 ha
  have hnum : f (x + a) - 2 * f x + f (x - a) = 2 * c₂ * a ^ 2 := by
    simp only [f]
    ring
  rw [hnum, mul_div_cancel_right₀ (2 * c₂) ha2]

/-- Exact `O(a²)` continuum Taylor remainder of the discrete second-difference Laplacian on general
quartic test modes `f y = c₀ + c₁ * y + c₂ * y ^ 2 + c₃ * y ^ 3 + c₄ * y ^ 4`:
`(f (x + a) - 2 * f x + f (x - a)) / a ^ 2 - (2 * c₂ + 6 * c₃ * x + 12 * c₄ * x ^ 2) = 2 * c₄ * a ^ 2`. -/
theorem discrete_laplacian_quartic_taylor_remainder (c₀ c₁ c₂ c₃ c₄ x a : ℝ) (ha : a ≠ 0) :
    let f := fun y : ℝ => c₀ + c₁ * y + c₂ * y ^ 2 + c₃ * y ^ 3 + c₄ * y ^ 4
    let f_second_deriv := 2 * c₂ + 6 * c₃ * x + 12 * c₄ * x ^ 2
    (f (x + a) - 2 * f x + f (x - a)) / a ^ 2 - f_second_deriv = 2 * c₄ * a ^ 2 := by
  intro f f_second_deriv
  have ha2 : a ^ 2 ≠ 0 := pow_ne_zero 2 ha
  have hnum : f (x + a) - 2 * f x + f (x - a) =
      (f_second_deriv + 2 * c₄ * a ^ 2) * a ^ 2 := by
    simp only [f, f_second_deriv]
    ring
  rw [hnum, mul_div_cancel_right₀ _ ha2]
  ring

end

/-! ### Stage 9: Continuum Kochen–Specker Theorem (`d ≥ 3`) & `TFQ-0307` Operational Born Synthesis -/

/-- Pairwise-orthogonal 3-frame predicate on `ℂ³ \ {0}`. -/
def IsOrthoFrameC (u v w : Fin 3 → ℂ) : Prop :=
  u ≠ 0 ∧ v ≠ 0 ∧ w ≠ 0 ∧ dotC u v = 0 ∧ dotC u w = 0 ∧ dotC v w = 0

/-- The canonical embedding `ι : GVec → (Fin 3 → ℂ)` maps every nonzero Gaussian-rational vector
to a nonzero complex vector in `ℂ³`. -/
theorem iota_ne_zero_of_nonZero {v : GVec} (hv : v.NonZero) : ι v ≠ 0 :=
  ι_ne_zero hv

/-- The canonical embedding `ι : GVec → (Fin 3 → ℂ)` maps every pairwise-orthogonal Gaussian-rational
3-frame `IsFrame u v w` to a pairwise-orthogonal complex 3-frame `IsOrthoFrameC (ι u) (ι v) (ι w)`. -/
theorem isOrthoFrameC_iota_of_isFrame {u v w : GVec} (hfr : IsFrame u v w) :
    IsOrthoFrameC (ι u) (ι v) (ι w) := by
  obtain ⟨hu, hv, hw, huv, huw, hvw⟩ := hfr
  refine ⟨ι_ne_zero hu, ι_ne_zero hv, ι_ne_zero hw, ?_, ?_, ?_⟩
  · rw [dotC_ι, huv, toC_zero]
  · rw [dotC_ι, huw, toC_zero]
  · rw [dotC_ι, hvw, toC_zero]

/-- **Continuum Kochen–Specker Theorem on `ℂ³ \ {0}` (`no_zero_one_continuum_frameFunctionC`)**:
there is no `{0, 1}`-valued frame function of weight `1` on `ℂ³ \ {0}`. -/
theorem no_zero_one_continuum_frameFunctionC :
    ¬ ∃ F : (Fin 3 → ℂ) → ℝ,
      IsFrameFunctionC F 1 ∧ ∀ v : Fin 3 → ℂ, v ≠ 0 → F v = 0 ∨ F v = 1 := by
  classical
  rintro ⟨F, hF, hB⟩
  let f : GVec → ℚ := fun v => if F (ι v) = 1 then 1 else 0
  have hf_eq : ∀ v : GVec, v.NonZero → (f v : ℝ) = F (ι v) := by
    intro v hv
    rcases hB (ι v) (ι_ne_zero hv) with h0 | h1
    · simp [f, h0]
    · simp [f, h1]
  have hf_bin : ∀ v : GVec, v.NonZero → f v = 0 ∨ f v = 1 := by
    intro v _hv
    by_cases h1 : F (ι v) = 1
    · right; simp [f, h1]
    · left; simp [f, h1]
  have hf_frame : IsFrameFunction f := by
    intro u v w hfr
    have hC := isOrthoFrameC_iota_of_isFrame hfr
    have hsum : F (ι u) + F (ι v) + F (ι w) = 1 :=
      hF.frame (ι u) (ι v) (ι w) hC.1 hC.2.1 hC.2.2.1 hC.2.2.2.1 hC.2.2.2.2.1 hC.2.2.2.2.2
    have hR : ((f u + f v + f w : ℚ) : ℝ) = (1 : ℝ) := by
      push_cast
      rw [hf_eq u hfr.1, hf_eq v hfr.2.1, hf_eq w hfr.2.2.1]
      exact hsum
    exact_mod_cast hR
  exact BornFinite.GaussianFrames.NoColouring.no_zero_one_frame_function f hf_frame hf_bin

/-- **Continuum Kochen–Specker Theorem on 3D Subspaces of `ℂ^d` (`no_zero_one_continuum_subspace3D`)**:
for any orthonormal triple `(e₀, e₁, e₂)` in `ℂ^d`, there is no `{0, 1}`-valued function `F` on
`ℂ^d \ {0}` satisfying `HasSubspace3FrameAdditivityD F` with subspace weight `F e₀ + F e₁ + F e₂ = 1`. -/
theorem no_zero_one_continuum_subspace3D {d : ℕ} {e₀ e₁ e₂ : Fin d → ℂ}
    (htri : IsOrthonormalTripleD e₀ e₁ e₂) :
    ¬ ∃ F : (Fin d → ℂ) → ℝ,
      HasSubspace3FrameAdditivityD F ∧ F e₀ + F e₁ + F e₂ = 1 ∧
      ∀ v : Fin d → ℂ, v ≠ 0 → F v = 0 ∨ F v = 1 := by
  rintro ⟨F, hF, hW, hB⟩
  have hsub : IsFrameFunctionC (restrict3D F e₀ e₁ e₂) 1 := by
    simpa [hW] using isFrameFunctionC_restrict3D hF htri
  have hbin : ∀ x : Fin 3 → ℂ, x ≠ 0 →
      restrict3D F e₀ e₁ e₂ x = 0 ∨ restrict3D F e₀ e₁ e₂ x = 1 := by
    intro x hx
    exact hB (embed3D e₀ e₁ e₂ x) ((embed3D_ne_zero_iff htri x).mpr hx)
  exact no_zero_one_continuum_frameFunctionC ⟨restrict3D F e₀ e₁ e₂, hsub, hbin⟩

/-- **Continuum Kochen–Specker Theorem in Dimension `d ≥ 3` (`no_zero_one_continuum_frameFunctionD`)**:
for every finite dimension `d ≥ 3`, there is no `{0, 1}`-valued frame function of weight `1`
(`IsFrameFunctionD F 1`) on `ℂ^d \ {0}`. -/
theorem no_zero_one_continuum_frameFunctionD {d : ℕ} (hd : 3 ≤ d) :
    ¬ ∃ F : (Fin d → ℂ) → ℝ,
      IsFrameFunctionD F 1 ∧ ∀ v : Fin d → ℂ, v ≠ 0 → F v = 0 ∨ F v = 1 := by
  rintro ⟨F, hF, hB⟩
  let B : Fin d → Fin d → ℂ := fun i => Pi.single i (1 : ℂ)
  have hB_ortho : IsOrthonormalBasisD B := isOrthonormalBasisD_single
  have hsum : (∑ i : Fin d, F (B i)) = 1 := hF.basis_sum B hB_ortho
  have hBi_ne : ∀ i : Fin d, B i ≠ 0 :=
    fun i => (nsqD_pos_iff_ne_zero (B i)).mp (by linarith [hB_ortho.1 i])
  have hBi_bin : ∀ i : Fin d, F (B i) = 0 ∨ F (B i) = 1 :=
    fun i => hB (B i) (hBi_ne i)
  have hBi_nn : ∀ i : Fin d, 0 ≤ F (B i) := by
    intro i
    rcases hBi_bin i with h0 | h1 <;> linarith
  have hex_one : ∃ i₀ : Fin d, F (B i₀) = 1 := by
    by_contra hnone
    have hall0 : ∀ i : Fin d, F (B i) = 0 := by
      intro i
      rcases hBi_bin i with h0 | h1
      · exact h0
      · exact False.elim (hnone ⟨i, h1⟩)
    have h0 : (∑ i : Fin d, F (B i)) = 0 :=
      Finset.sum_eq_zero (fun i _ => hall0 i)
    linarith
  obtain ⟨i₀, hi₀⟩ := hex_one
  have h_other_zero : ∀ j : Fin d, j ≠ i₀ → F (B j) = 0 := by
    intro j hj
    have herase := Finset.add_sum_erase Finset.univ (fun i => F (B i)) (Finset.mem_univ i₀)
    have hsum_erase : (∑ i ∈ Finset.univ.erase i₀, F (B i)) = 0 := by linarith
    have hj_mem : j ∈ Finset.univ.erase i₀ :=
      Finset.mem_erase.mpr ⟨hj, Finset.mem_univ j⟩
    have hj_le : F (B j) ≤ ∑ i ∈ Finset.univ.erase i₀, F (B i) :=
      Finset.single_le_sum (fun i _ => hBi_nn i) hj_mem
    have hj_nn : 0 ≤ F (B j) := hBi_nn j
    linarith
  let k₀ : Fin d := Fin.castLE hd 0
  let k₁ : Fin d := Fin.castLE hd 1
  let k₂ : Fin d := Fin.castLE hd 2
  have hk01 : k₀ ≠ k₁ := by intro h; have h1 := congrArg Fin.val h; simp [k₀, k₁] at h1
  have hk02 : k₀ ≠ k₂ := by intro h; have h1 := congrArg Fin.val h; simp [k₀, k₂] at h1
  have hk12 : k₁ ≠ k₂ := by intro h; have h1 := congrArg Fin.val h; simp [k₁, k₂] at h1
  have hex_pair : ∃ i₁ i₂ : Fin d, i₀ ≠ i₁ ∧ i₀ ≠ i₂ ∧ i₁ ≠ i₂ := by
    by_cases h0 : i₀ = k₀
    · refine ⟨k₁, k₂, ?_, ?_, hk12⟩
      · rw [h0]; exact hk01
      · rw [h0]; exact hk02
    · by_cases h1 : i₀ = k₁
      · refine ⟨k₀, k₂, ?_, ?_, hk02⟩
        · rw [h1]; exact hk01.symm
        · rw [h1]; exact hk12
      · exact ⟨k₀, k₁, h0, h1, hk01⟩
  obtain ⟨i₁, i₂, h01, h02, h12⟩ := hex_pair
  have hi₁ : F (B i₁) = 0 := h_other_zero i₁ h01.symm
  have hi₂ : F (B i₂) = 0 := h_other_zero i₂ h02.symm
  have hW : F (B i₀) + F (B i₁) + F (B i₂) = 1 := by linarith
  have hsub : IsFrameFunctionC (restrict3D F (B i₀) (B i₁) (B i₂)) 1 := by
    simpa [hW] using isFrameFunctionC_restrict3D_of_basis hF hB_ortho h01 h02 h12
  have htri : IsOrthonormalTripleD (B i₀) (B i₁) (B i₂) :=
    isOrthonormalTripleD_of_basis hB_ortho h01 h02 h12
  have hbin : ∀ x : Fin 3 → ℂ, x ≠ 0 →
      restrict3D F (B i₀) (B i₁) (B i₂) x = 0 ∨ restrict3D F (B i₀) (B i₁) (B i₂) x = 1 := by
    intro x hx
    exact hB (embed3D (B i₀) (B i₁) (B i₂) x) ((embed3D_ne_zero_iff htri x).mpr hx)
  exact no_zero_one_continuum_frameFunctionC ⟨restrict3D F (B i₀) (B i₁) (B i₂), hsub, hbin⟩

/-- **Continuum `TFQ-0307` Operational Born Synthesis (`continuum_tfq0307_operational_born_synthesis`)**:
unites for all finite dimensions `d ≥ 3`:
1. The continuum Kochen–Specker refutation of `{0, 1}` frame valuations (`no_zero_one_continuum_frameFunctionD`),
2. The exact algebraic bijection between density matrices and `EffectValuation (HermitianCarrier.space d)`
   (`HermitianCarrier.state_valuation_correspondence`),
3. The continuity-free pure-state Born rule on every 3D subspace (`pure_state_nonneg_gleason_subspace3D`), and
4. The general spectral Gleason quadratic representation on every 3D subspace under continuity
   (`gleason_subspace3D_of_continuousD`). -/
theorem continuum_tfq0307_operational_born_synthesis {d : ℕ} (hd : 3 ≤ d) :
    (¬ ∃ F : (Fin d → ℂ) → ℝ,
      IsFrameFunctionD F 1 ∧ ∀ v : Fin d → ℂ, v ≠ 0 → F v = 0 ∨ F v = 1) ∧
    ((∀ W : EffectValuation (HermitianCarrier.space d),
        (HermitianCarrier.density W)ᴴ = HermitianCarrier.density W ∧
          HermitianCarrier.PsdH (HermitianCarrier.density W) ∧
            (HermitianCarrier.density W).trace = 1 ∧
              ∀ E : Matrix (Fin d) (Fin d) GaussRat,
                (HermitianCarrier.space d).Effect E →
                  W.v E = (HermitianCarrier.density W * E).trace.re) ∧
     (∀ (ρ : Matrix (Fin d) (Fin d) GaussRat) (hρs : ρᴴ = ρ) (hρ : HermitianCarrier.PsdH ρ)
        (htr : ρ.trace.re = 1),
        HermitianCarrier.density (HermitianCarrier.bornValuation ρ hρs hρ htr) = ρ)) ∧
    (∀ (F : (Fin d → ℂ) → ℝ) (e₁ e₂ e₃ : Fin d → ℂ) (p₀ : Fin 3 → ℂ),
      HasSubspace3FrameAdditivityD F →
      (∀ v : Fin d → ℂ, v ≠ 0 → 0 ≤ F v) →
      IsOrthonormalTripleD e₁ e₂ e₃ →
      GleasonComplex.nsq p₀ = 1 →
      F (embed3D e₁ e₂ e₃ p₀) = F e₁ + F e₂ + F e₃ →
      ∀ x : Fin 3 → ℂ, x ≠ 0 →
        F (embed3D e₁ e₂ e₃ x) =
          (F e₁ + F e₂ + F e₃) * Complex.normSq (GleasonComplex.dotC p₀ x) /
            GleasonComplex.nsq x) ∧
    (∀ (F : (Fin d → ℂ) → ℝ) (e₁ e₂ e₃ : Fin d → ℂ),
      HasSubspace3FrameAdditivityD F →
      ContinuousOn F {v : Fin d → ℂ | v ≠ 0} →
      IsOrthonormalTripleD e₁ e₂ e₃ →
      ∃ p q r : Fin 3 → ℂ, GleasonComplex.IsOrthonormalC p q r ∧ ∃ M α m : ℝ,
        ∀ x : Fin 3 → ℂ, x ≠ 0 →
          F (embed3D e₁ e₂ e₃ x) =
            (M * Complex.normSq (GleasonComplex.dotC p x) +
             α * Complex.normSq (GleasonComplex.dotC q x) +
             m * Complex.normSq (GleasonComplex.dotC r x)) / GleasonComplex.nsq x) :=
  ⟨no_zero_one_continuum_frameFunctionD hd,
   HermitianCarrier.state_valuation_correspondence,
   fun _ _ _ _ _ hF hnn htri hp₀ hpW =>
     pure_state_nonneg_gleason_subspace3D hF hnn htri hp₀ hpW,
   fun _ _ _ _ hF hc htri =>
     gleason_subspace3D_of_continuousD hF hc htri⟩

end BornFinite.ContinuumDerivationSpine

#print axioms BornFinite.ContinuumDerivationSpine.iota_ne_zero_of_nonZero
#print axioms BornFinite.ContinuumDerivationSpine.isOrthoFrameC_iota_of_isFrame
#print axioms BornFinite.ContinuumDerivationSpine.no_zero_one_continuum_frameFunctionC
#print axioms BornFinite.ContinuumDerivationSpine.no_zero_one_continuum_subspace3D
#print axioms BornFinite.ContinuumDerivationSpine.no_zero_one_continuum_frameFunctionD
#print axioms BornFinite.ContinuumDerivationSpine.continuum_tfq0307_operational_born_synthesis

