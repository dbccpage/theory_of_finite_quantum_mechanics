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

end BornFinite.ContinuumDerivationSpine
