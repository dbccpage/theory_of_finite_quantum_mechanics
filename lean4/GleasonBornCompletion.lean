import GleasonGaussianBridge
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Topology.Instances.Matrix

/-!
# Density-matrix completion of the Gleason hinge on `ℚ(i)³`

AuthorityEffect: None.

`GleasonGaussianBridge` shows that a frame function `f : ℚ(i)³ → ℚ` that is uniformly continuous
on rays (`IsUniformlyRayContinuous`, a declared input) equals the Rayleigh quotient of the rational
Hermitian form `tomographyForm f`, and extends to a continuous frame function `F f` on `ℂ³ \ {0}`.
This module packages that result in the vocabulary of density matrices and closes the converse:

* `toMatrix ρ`: the complex `3 × 3` matrix of a rational Hermitian form `ρ : HermForm3`; it is
  Hermitian (`toMatrix_isHermitian`), has trace `ρ.tr` (`trace_toMatrix`) and acts on `ι g` as
  `ρ.applyVec g` (`mulVec_ι`).
* `born_density_matrix_of_uniformlyRayContinuous`: for a nonnegative frame function `f` that is
  uniformly continuous on rays there is a positive semidefinite, trace-one `ρC` with
  `F f v = Re ⟨v, ρC v⟩ / ⟨v, v⟩` on every nonzero `v ∈ ℂ³` and `f g = Re ⟨g, ρC g⟩ / ⟨g, g⟩` on every
  nonzero `g ∈ ℚ(i)³`; `ρC` is the only Hermitian matrix with this property.  Positivity is used
  only for positive semidefiniteness: the signed statement is `F_eq_QcRay`.
* `eq_of_re_dotC_mulVec_self`: two Hermitian `3 × 3` matrices with the same real quadratic form on
  `ℂ³ \ {0}` are equal (polarization).
* `isUniformlyRayContinuous_quadRay`: the Rayleigh quotient of **every** rational Hermitian form is
  uniformly continuous on rays, by compactness of the unit sphere of `ℂ³`.  Together with
  `quadRay_isFrameFunction` this gives the characterization
  `uniformlyRayContinuous_frameFunction_iff`: the frame functions on `ℚ(i)³` that are uniformly
  continuous on rays are exactly the Rayleigh quotients `v ↦ ⟨v, ρ v⟩ / ⟨v, v⟩` of trace-one rational
  Hermitian forms.  In particular the declared input class is not empty, and uniform continuity is
  the exact hypothesis for this description, not merely a sufficient one.

Everything here is a consequence of the kernel-checked modules it imports; the pointwise-to-uniform
question (`FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM`) is untouched.
-/

namespace BornFinite.BornCompletion

open BornFinite BornFinite.GaussRat BornFinite.GaussianFrames BornFinite.GaussianTomography
open BornFinite.GleasonBridge GleasonComplex Complex ComplexConjugate Matrix
open scoped ComplexOrder

noncomputable section

/-! ### The complex matrix of a rational Hermitian form -/

/-- The complex `3 × 3` matrix of `ρ : HermForm3`: diagonal `d₁, d₂, d₃`, upper entries
`entry12, entry13, entry23`, lower entries their conjugates. -/
def toMatrix (ρ : HermForm3) : Matrix (Fin 3) (Fin 3) ℂ :=
  !![toC ⟨ρ.d1, 0⟩, toC ρ.entry12, toC ρ.entry13;
     conj (toC ρ.entry12), toC ⟨ρ.d2, 0⟩, toC ρ.entry23;
     conj (toC ρ.entry13), conj (toC ρ.entry23), toC ⟨ρ.d3, 0⟩]

lemma toMatrix_isHermitian (ρ : HermForm3) : (toMatrix ρ).IsHermitian := by
  refine Matrix.IsHermitian.ext fun i j => ?_
  fin_cases i <;> fin_cases j <;> simp [toMatrix] <;> (apply Complex.ext <;> simp [toC])

lemma trace_toMatrix (ρ : HermForm3) : (toMatrix ρ).trace = ((ρ.tr : ℝ) : ℂ) := by
  unfold toMatrix
  rw [Matrix.trace_fin_three_of]
  apply Complex.ext <;> simp [toC, HermForm3.tr]

/-- `toMatrix ρ` acts on the image of `ℚ(i)³` as `ρ.applyVec`. -/
lemma mulVec_ι (ρ : HermForm3) (g : GVec) : toMatrix ρ *ᵥ ι g = ι (ρ.applyVec g) := by
  ext i
  fin_cases i <;>
    simp [toMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_three, ι, HermForm3.applyVec,
      toC_add, toC_mul, toC_star]

lemma dotC_eq_dotProduct (v w : Fin 3 → ℂ) : dotC v w = star v ⬝ᵥ w := by
  simp [dotC, dotProduct, Fin.sum_univ_three]

lemma dotC_mulVec_left (M : Matrix (Fin 3) (Fin 3) ℂ) (u v : Fin 3 → ℂ) :
    dotC (M *ᵥ u) v = dotC u (Mᴴ *ᵥ v) := by
  rw [dotC_eq_dotProduct, dotC_eq_dotProduct, Matrix.star_mulVec, Matrix.dotProduct_mulVec]

/-- For a Hermitian matrix the form `⟨v, M v⟩` is real. -/
lemma im_dotC_mulVec_self {M : Matrix (Fin 3) (Fin 3) ℂ} (hM : M.IsHermitian) (v : Fin 3 → ℂ) :
    (dotC v (M *ᵥ v)).im = 0 := by
  rw [← Complex.conj_eq_iff_im, ← dotC_conj_symm, dotC_mulVec_left, hM.eq]

/-! ### The quadratic form of `toMatrix ρ` on `ℂ³` -/

/-- `Qc ρ v = Re ⟨v, ρ v⟩` on `ℂ³`. -/
def Qc (ρ : HermForm3) (v : Fin 3 → ℂ) : ℝ := (dotC v (toMatrix ρ *ᵥ v)).re

/-- `QcRay ρ v = Re ⟨v, ρ v⟩ / ⟨v, v⟩`, the Rayleigh quotient on `ℂ³`. -/
def QcRay (ρ : HermForm3) (v : Fin 3 → ℂ) : ℝ := Qc ρ v / nsq v

lemma Qc_ι (ρ : HermForm3) (g : GVec) : Qc ρ (ι g) = (quadNum ρ g : ℝ) := by
  rw [Qc, mulVec_ι, dotC_ι, toC_re, inner_applyVec_re_eq_quadNum]

lemma Qc_smul (ρ : HermForm3) (c : ℂ) (v : Fin 3 → ℂ) : Qc ρ (c • v) = normSq c * Qc ρ v := by
  rw [Qc, Qc, Matrix.mulVec_smul, dotC_smul_left, dotC_smul_right, ← mul_assoc,
    ← Complex.normSq_eq_conj_mul_self, Complex.re_ofReal_mul]

lemma continuous_mulVec (ρ : HermForm3) : Continuous (fun v : Fin 3 → ℂ => toMatrix ρ *ᵥ v) :=
  Continuous.matrix_mulVec continuous_const continuous_id

lemma continuous_Qc (ρ : HermForm3) : Continuous (Qc ρ) :=
  Complex.continuous_re.comp (continuous_dotC_pair.comp (continuous_id.prodMk (continuous_mulVec ρ)))

lemma QcRay_ι (ρ : HermForm3) (g : GVec) : QcRay ρ (ι g) = (quadRay ρ g : ℝ) := by
  rw [QcRay, Qc_ι, nsq_ι, quadRay]
  push_cast
  rfl

lemma QcRay_smul (ρ : HermForm3) (v : Fin 3 → ℂ) {c : ℂ} (hc : c ≠ 0) :
    QcRay ρ (c • v) = QcRay ρ v := by
  rw [QcRay, QcRay, Qc_smul, nsq_smul]
  exact mul_div_mul_left _ _ (Complex.normSq_pos.mpr hc).ne'

lemma continuousOn_QcRay (ρ : HermForm3) : ContinuousOn (QcRay ρ) {v | v ≠ 0} :=
  (continuous_Qc ρ).continuousOn.div continuous_nsq.continuousOn fun _ hv => (nsq_pos hv).ne'

/-! ### Uniqueness of continuous scale-invariant extensions -/

lemma denseRange_ι : DenseRange ι := by
  rw [Metric.denseRange_iff]
  intro v r hr
  obtain ⟨g, hg⟩ := exists_ι_near v hr
  exact ⟨g, by rwa [dist_comm]⟩

/-- Two functions on `ℂ³ \ {0}` that are continuous there, scale invariant, and agree on the image
of the nonzero vectors of `ℚ(i)³`, agree everywhere on `ℂ³ \ {0}`. -/
theorem eq_on_nonzero_of_eq_on_ι {G H : (Fin 3 → ℂ) → ℝ}
    (hG : ContinuousOn G {v | v ≠ 0}) (hH : ContinuousOn H {v | v ≠ 0})
    (hGs : ∀ v : Fin 3 → ℂ, v ≠ 0 → ∀ c : ℂ, c ≠ 0 → G (c • v) = G v)
    (hHs : ∀ v : Fin 3 → ℂ, v ≠ 0 → ∀ c : ℂ, c ≠ 0 → H (c • v) = H v)
    (h : ∀ g : GVec, g.NonZero → G (ι g) = H (ι g)) :
    ∀ v : Fin 3 → ℂ, v ≠ 0 → G v = H v := by
  have hGS : Continuous (fun s : S => G s.1) :=
    hG.comp_continuous continuous_subtype_val fun s => S_ne_zero s.2
  have hHS : Continuous (fun s : S => H s.1) :=
    hH.comp_continuous continuous_subtype_val fun s => S_ne_zero s.2
  have hS : (fun s : S => G s.1) = (fun s : S => H s.1) := by
    refine Continuous.ext_on dense_D hGS hHS ?_
    rintro ⟨s, hs⟩ ⟨g, hg⟩
    have hg0 : g.NonZero := nonZero_of_ι_ne_zero (hg ▸ S_ne_zero hs)
    have hgs : ι g = s := hg
    show G s = H s
    rw [← hgs]
    exact h g hg0
  intro v hv
  have hc : ((Real.sqrt (nsq v) : ℝ) : ℂ) ≠ 0 := by
    exact_mod_cast (Real.sqrt_pos.mpr (nsq_pos hv)).ne'
  have hn : normalize v ≠ 0 := S_ne_zero (normalize_mem_S hv)
  rw [← sqrt_smul_normalize hv, hGs _ hn _ hc, hHs _ hn _ hc]
  exact congrFun hS ⟨normalize v, normalize_mem_S hv⟩

/-- The extension `F f` of the bridge is the Rayleigh quotient of `tomographyForm f` on all of
`ℂ³ \ {0}` (signed frame functions; no positivity assumed). -/
theorem F_eq_QcRay {f : GVec → ℚ} (hf : IsFrameFunction f) (hu : IsUniformlyRayContinuous f) :
    ∀ v : Fin 3 → ℂ, v ≠ 0 → F f v = QcRay (tomographyForm f) v :=
  eq_on_nonzero_of_eq_on_ι (continuousOn_F hu) (continuousOn_QcRay _)
    (fun v hv c hc => F_smul hf hu hv hc) (fun v _ c hc => QcRay_smul _ v hc)
    (fun g hg => by
      rw [F_ι hf hu hg, QcRay_ι _ g, born_of_uniformlyRayContinuous hf hu g hg])

/-! ### Positivity by density -/

theorem Qc_nonneg {ρ : HermForm3} (h : ∀ g : GVec, g.NonZero → 0 ≤ quadNum ρ g) (v : Fin 3 → ℂ) :
    0 ≤ Qc ρ v := by
  refine isClosed_property denseRange_ι (isClosed_le continuous_const (continuous_Qc ρ))
    (fun g => ?_) v
  rw [Qc_ι]
  by_cases hg : g.NonZero
  · exact_mod_cast h g hg
  · rw [eq_zero_of_not_nonZero hg]
    show (0 : ℝ) ≤ ((quadNum ρ ⟨0, 0, 0⟩ : ℚ) : ℝ)
    rw [quadNum_zero]
    simp

lemma quadNum_nonneg_of_quadRay_nonneg {ρ : HermForm3} {g : GVec} (hg : g.NonZero)
    (h : 0 ≤ quadRay ρ g) : 0 ≤ quadNum ρ g := by
  have hb := normSqVec_pos_of_nonZero hg
  have : quadNum ρ g = quadRay ρ g * normSqVec g := (div_mul_cancel₀ _ hb.ne').symm
  rw [this]
  exact mul_nonneg h hb.le

theorem toMatrix_posSemidef {ρ : HermForm3} (h : ∀ g : GVec, g.NonZero → 0 ≤ quadNum ρ g) :
    (toMatrix ρ).PosSemidef := by
  rw [Matrix.posSemidef_iff_dotProduct_mulVec]
  refine ⟨toMatrix_isHermitian ρ, fun v => ?_⟩
  rw [← dotC_eq_dotProduct, Complex.nonneg_iff]
  exact ⟨Qc_nonneg h v, (im_dotC_mulVec_self (toMatrix_isHermitian ρ) v).symm⟩

/-! ### Hermitian matrices are determined by their real quadratic form -/

lemma dotC_single_mulVec_single (D : Matrix (Fin 3) (Fin 3) ℂ) (i j : Fin 3) :
    dotC (Pi.single i 1) (D *ᵥ Pi.single j 1) = D i j := by
  fin_cases i <;> fin_cases j <;> simp [dotC, Matrix.mulVec, dotProduct, Fin.sum_univ_three]

/-- Polarization: a Hermitian `3 × 3` matrix whose real quadratic form vanishes on `ℂ³ \ {0}` is
zero; hence two Hermitian matrices with the same real quadratic form are equal. -/
theorem eq_of_re_dotC_mulVec_self {A B : Matrix (Fin 3) (Fin 3) ℂ}
    (hA : A.IsHermitian) (hB : B.IsHermitian)
    (h : ∀ v : Fin 3 → ℂ, v ≠ 0 → (dotC v (A *ᵥ v)).re = (dotC v (B *ᵥ v)).re) : A = B := by
  set D := A - B with hD
  have hDh : D.IsHermitian := hA.sub hB
  have hself : ∀ v : Fin 3 → ℂ, dotC v (D *ᵥ v) = 0 := by
    intro v
    by_cases hv : v = 0
    · subst hv; simp [dotC]
    · apply Complex.ext
      · rw [hD, Matrix.sub_mulVec, dotC_sub_right, Complex.sub_re, h v hv, sub_self, Complex.zero_re]
      · rw [im_dotC_mulVec_self hDh, Complex.zero_im]
  have hpol : ∀ v w : Fin 3 → ℂ, (4 : ℂ) * dotC v (D *ᵥ w) =
      (dotC (v + w) (D *ᵥ (v + w)) - dotC (v - w) (D *ᵥ (v - w)))
        - Complex.I * (dotC (v + Complex.I • w) (D *ᵥ (v + Complex.I • w))
          - dotC (v - Complex.I • w) (D *ᵥ (v - Complex.I • w))) := by
    intro v w
    simp only [Matrix.mulVec_add, Matrix.mulVec_sub, Matrix.mulVec_smul, dotC_add_left,
      dotC_add_right, dotC_sub_left, dotC_sub_right, dotC_smul_left, dotC_smul_right, Complex.conj_I]
    linear_combination (2 * dotC v (D *ᵥ w) - 2 * dotC w (D *ᵥ v)) * Complex.I_mul_I
  have hzero : ∀ v w : Fin 3 → ℂ, dotC v (D *ᵥ w) = 0 := by
    intro v w
    have h4 := hpol v w
    rw [hself, hself, hself, hself] at h4
    have : (4 : ℂ) * dotC v (D *ᵥ w) = 0 := by rw [h4]; ring
    exact (mul_eq_zero.mp this).resolve_left (by norm_num)
  have hD0 : D = 0 := by
    ext i j
    have hij := dotC_single_mulVec_single D i j
    rw [hzero] at hij
    rw [Matrix.zero_apply]
    exact hij.symm
  exact sub_eq_zero.mp hD0

/-! ### The density-matrix statement -/

/-- **Density-matrix completion.** A nonnegative frame function on `ℚ(i)³` that is uniformly
continuous on rays is the Born rule of a unique positive semidefinite, trace-one matrix: there is
`ρC` with `F f v = Re ⟨v, ρC v⟩ / ⟨v, v⟩` for every nonzero `v ∈ ℂ³` and
`f g = Re ⟨g, ρC g⟩ / ⟨g, g⟩` for every nonzero `g ∈ ℚ(i)³`, and any Hermitian matrix with the
first property is `ρC`.  (`⟨v, w⟩ = star v ⬝ᵥ w`.) -/
theorem born_density_matrix_of_uniformlyRayContinuous {f : GVec → ℚ}
    (hf : IsNonnegFrameFunction f) (hu : IsUniformlyRayContinuous f) :
    ∃ ρC : Matrix (Fin 3) (Fin 3) ℂ, ρC.PosSemidef ∧ ρC.trace = 1 ∧
      (∀ v : Fin 3 → ℂ, v ≠ 0 → F f v = (star v ⬝ᵥ (ρC *ᵥ v)).re / nsq v) ∧
      (∀ g : GVec, g.NonZero → (f g : ℝ) = (star (ι g) ⬝ᵥ (ρC *ᵥ ι g)).re / nsq (ι g)) ∧
      (∀ σC : Matrix (Fin 3) (Fin 3) ℂ, σC.IsHermitian →
        (∀ v : Fin 3 → ℂ, v ≠ 0 → F f v = (star v ⬝ᵥ (σC *ᵥ v)).re / nsq v) → σC = ρC) := by
  have hF : ∀ v : Fin 3 → ℂ, v ≠ 0 →
      F f v = (star v ⬝ᵥ (toMatrix (tomographyForm f) *ᵥ v)).re / nsq v := by
    intro v hv
    rw [F_eq_QcRay hf.1 hu v hv, QcRay, Qc, dotC_eq_dotProduct]
  refine ⟨toMatrix (tomographyForm f), ?_, ?_, hF, ?_, ?_⟩
  · refine toMatrix_posSemidef fun g hg => quadNum_nonneg_of_quadRay_nonneg hg ?_
    rw [← born_of_uniformlyRayContinuous hf.1 hu g hg]
    exact hf.2 g hg
  · rw [trace_toMatrix, tomography_trace_one hf.1]
    simp
  · intro g hg
    rw [← hF (ι g) (ι_ne_zero hg), F_ι hf.1 hu hg]
  · intro σC hσ hσF
    refine eq_of_re_dotC_mulVec_self hσ (toMatrix_isHermitian _) fun v hv => ?_
    have hn : nsq v ≠ 0 := (nsq_pos hv).ne'
    have := (hσF v hv).symm.trans (hF v hv)
    rw [dotC_eq_dotProduct, dotC_eq_dotProduct]
    exact (div_left_inj' hn).mp this

/-! ### Uniform ray continuity of every rational Hermitian Rayleigh quotient -/

lemma exists_phase (z : ℂ) : ∃ c : ℂ, normSq c = 1 ∧ c * z = (‖z‖ : ℂ) := by
  by_cases hz : z = 0
  · exact ⟨1, by simp, by simp [hz]⟩
  · have hn : ‖z‖ ≠ 0 := norm_ne_zero_iff.mpr hz
    have hnC : (‖z‖ : ℂ) ≠ 0 := by exact_mod_cast hn
    refine ⟨conj z / ‖z‖, ?_, ?_⟩
    · rw [Complex.normSq_div, Complex.normSq_conj, Complex.normSq_ofReal,
        Complex.normSq_eq_norm_sq, sq]
      exact div_self (mul_self_ne_zero.mpr hn)
    · rw [div_mul_eq_mul_div, ← Complex.normSq_eq_conj_mul_self, Complex.normSq_eq_norm_sq]
      push_cast
      rw [sq, mul_div_assoc, div_self hnC, mul_one]

lemma normSq_dotC_normalize {x y : Fin 3 → ℂ} (hx : x ≠ 0) (hy : y ≠ 0) :
    normSq (dotC (normalize x) (normalize y)) = normSq (dotC x y) / (nsq x * nsq y) := by
  have hpx := nsq_pos hx
  have hpy := nsq_pos hy
  rw [GleasonBridge.normalize, GleasonBridge.normalize, dotC_smul_left, dotC_smul_right,
    Complex.normSq_mul, Complex.normSq_mul, Complex.normSq_conj, Complex.normSq_ofReal,
    Complex.normSq_ofReal, div_mul_div_comm, one_mul, Real.mul_self_sqrt hpx.le,
    div_mul_div_comm, one_mul, Real.mul_self_sqrt hpy.le]
  field_simp

lemma nsq_sub_eq (x y : Fin 3 → ℂ) : nsq (x - y) = nsq x - 2 * (dotC x y).re + nsq y := by
  simp only [nsq, dotC, Pi.sub_apply, Complex.normSq_apply, Complex.sub_re, Complex.sub_im,
    Complex.add_re, Complex.mul_re, Complex.conj_re, Complex.conj_im]
  ring

/-- The Rayleigh quotient of every rational Hermitian form is uniformly continuous on rays: the
declared input of the bridge is satisfied by every Born rule. -/
theorem isUniformlyRayContinuous_quadRay (ρ : HermForm3) : IsUniformlyRayContinuous (quadRay ρ) := by
  intro ε hε
  have hεR : (0 : ℝ) < ε := by exact_mod_cast hε
  have huc : UniformContinuousOn (QcRay ρ) sphereC :=
    isCompact_sphereC.uniformContinuousOn_of_continuous ((continuousOn_QcRay ρ).mono sphereC_subset)
  obtain ⟨δ', hδ', hδ⟩ := Metric.uniformContinuousOn_iff.mp huc ε hεR
  obtain ⟨δ, hδ0, hδlt⟩ := exists_rat_btwn (show (0 : ℝ) < δ' ^ 2 / 2 by positivity)
  refine ⟨δ, by exact_mod_cast hδ0, ?_⟩
  intro u v hu hv huv
  have hx : ι u ≠ 0 := ι_ne_zero hu
  have hy : ι v ≠ 0 := ι_ne_zero hv
  set z := dotC (normalize (ι u)) (normalize (ι v)) with hzdef
  obtain ⟨c, hc1, hcz⟩ := exists_phase z
  have hc0 : c ≠ 0 := Complex.normSq_pos.mp (by rw [hc1]; exact one_pos)
  have hû : normalize (ι u) ∈ sphereC := nsq_normalize hx
  have hw' : nsq (c • normalize (ι v)) = 1 := by rw [nsq_smul, hc1, nsq_normalize hy, mul_one]
  have hw : c • normalize (ι v) ∈ sphereC := hw'
  -- `|z|² = 1 - raySinSq u v ≤ 1`
  have hz : normSq z = 1 - (raySinSq u v : ℝ) := by
    rw [hzdef, normSq_dotC_normalize hx hy, raySinSq_cast]; ring
  have hz1 : normSq z ≤ 1 := by
    have h := nsq_nonneg (ccross (normalize (ι u)) (normalize (ι v)))
    rw [nsq_ccross, nsq_normalize hx, nsq_normalize hy] at h
    linarith
  have hzn := Complex.normSq_eq_norm_sq z
  have hnorm : ‖z‖ ≤ 1 := by nlinarith [norm_nonneg z]
  -- after the phase alignment the unit representatives are close
  have hnsq : nsq (normalize (ι u) - c • normalize (ι v)) = 2 - 2 * ‖z‖ := by
    rw [nsq_sub_eq, dotC_smul_right, ← hzdef, hcz, Complex.ofReal_re, nsq_normalize hx, hw']
    ring
  have hray : (raySinSq u v : ℝ) < δ := by exact_mod_cast huv
  have hsq : nsq (normalize (ι u) - c • normalize (ι v)) < δ' ^ 2 := by
    rw [hnsq]
    nlinarith [mul_nonneg (norm_nonneg z) (sub_nonneg.mpr hnorm)]
  have hle : dist (normalize (ι u)) (c • normalize (ι v)) ≤
      Real.sqrt (nsq (normalize (ι u) - c • normalize (ι v))) := by
    rw [dist_pi_le_iff (Real.sqrt_nonneg _)]
    intro i
    rw [Complex.dist_eq, Real.le_sqrt (norm_nonneg _) (nsq_nonneg _), Complex.sq_norm]
    exact normSq_le_nsq (normalize (ι u) - c • normalize (ι v)) i
  have hdist : dist (normalize (ι u)) (c • normalize (ι v)) < δ' :=
    calc dist (normalize (ι u)) (c • normalize (ι v))
        ≤ Real.sqrt (nsq (normalize (ι u) - c • normalize (ι v))) := hle
      _ < Real.sqrt (δ' ^ 2) := Real.sqrt_lt_sqrt (nsq_nonneg _) hsq
      _ = δ' := Real.sqrt_sq hδ'.le
  have hval := hδ _ hû _ hw hdist
  rw [Real.dist_eq] at hval
  -- identify the two values with the rational Rayleigh quotients
  have ha : ((1 / Real.sqrt (nsq (ι u)) : ℝ) : ℂ) ≠ 0 := by
    exact_mod_cast (one_div_pos.mpr (Real.sqrt_pos.mpr (nsq_pos hx))).ne'
  have hb : ((1 / Real.sqrt (nsq (ι v)) : ℝ) : ℂ) ≠ 0 := by
    exact_mod_cast (one_div_pos.mpr (Real.sqrt_pos.mpr (nsq_pos hy))).ne'
  have e1 : QcRay ρ (normalize (ι u)) = (quadRay ρ u : ℝ) := by
    rw [GleasonBridge.normalize, QcRay_smul ρ _ ha, QcRay_ι ρ u]
  have e2 : QcRay ρ (c • normalize (ι v)) = (quadRay ρ v : ℝ) := by
    rw [QcRay_smul ρ _ hc0, GleasonBridge.normalize, QcRay_smul ρ _ hb, QcRay_ι ρ v]
  rw [e1, e2] at hval
  exact_mod_cast hval

/-- **Characterization.** The frame functions on `ℚ(i)³` that are uniformly continuous on rays are
exactly the Rayleigh quotients of trace-one rational Hermitian forms (on nonzero vectors). -/
theorem uniformlyRayContinuous_frameFunction_iff (f : GVec → ℚ) :
    (IsFrameFunction f ∧ IsUniformlyRayContinuous f) ↔
      ∃ ρ : HermForm3, ρ.tr = 1 ∧ ∀ v : GVec, v.NonZero → f v = quadRay ρ v := by
  constructor
  · rintro ⟨hf, hu⟩
    exact ⟨tomographyForm f, tomography_trace_one hf, born_of_uniformlyRayContinuous hf hu⟩
  · rintro ⟨ρ, htr, hρ⟩
    refine ⟨?_, ?_⟩
    · intro u v w hfr
      rw [hρ u hfr.1, hρ v hfr.2.1, hρ w hfr.2.2.1]
      exact quadRay_isFrameFunction ρ htr u v w hfr
    · intro ε hε
      obtain ⟨δ, hδ, h⟩ := isUniformlyRayContinuous_quadRay ρ ε hε
      refine ⟨δ, hδ, fun u v hu hv huv => ?_⟩
      rw [hρ u hu, hρ v hv]
      exact h u v hu hv huv

end

#print axioms BornFinite.BornCompletion.born_density_matrix_of_uniformlyRayContinuous
#print axioms BornFinite.BornCompletion.eq_of_re_dotC_mulVec_self
#print axioms BornFinite.BornCompletion.isUniformlyRayContinuous_quadRay
#print axioms BornFinite.BornCompletion.uniformlyRayContinuous_frameFunction_iff

end BornFinite.BornCompletion
