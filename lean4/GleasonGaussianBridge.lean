import GleasonComplexSphere
import BornGaussianParallelogramRigidity

/-!
# The Gleason hinge on `ℚ(i)³` under uniform ray continuity

AuthorityEffect: None.

This module connects the two halves of the Gleason hinge for frame functions on `ℚ(i)³`.

* Input (declared): a frame function `f : GVec → ℚ` (`IsFrameFunction`, sums to `1` on every
  orthogonal frame) that is **uniformly continuous on rays**: for every rational `ε > 0` there is a
  rational `δ > 0` such that `|f u - f v| < ε` whenever the rays of `u` and `v` are `δ`-close in the
  phase-invariant ray metric `raySinSq u v = 1 - |⟨u,v⟩|² / (⟨u,u⟩⟨v,v⟩)` (the squared sine of the
  angle between the rays).
* Method: `f` is pushed forward along `ι : ℚ(i)³ → ℂ³` and extended by uniform continuity to a
  frame function `F` on `ℂ³ \ {0}` that is continuous away from the origin; `GleasonComplexSphere`
  gives `F` as the degree-zero form of a Hermitian form; pulled back to `ℚ(i)³` the residual
  `f - quadRay (tomographyForm f)` therefore satisfies the orthogonal parallelogram law, and the
  algebraic half `BornGaussianParallelogramRigidity` concludes `f = quadRay (tomographyForm f)` on
  every nonzero vector.

The real and complex numbers appear only inside the proof; the statement is about rational data.
-/

namespace BornFinite.GleasonBridge

open BornFinite BornFinite.GaussRat BornFinite.GaussianFrames BornFinite.GaussianTomography
open GleasonComplex Complex ComplexConjugate Filter Topology

/-! ### The embedding `ℚ(i) → ℂ` and `ℚ(i)³ → ℂ³` -/

/-- `a + b i ↦ (a : ℝ) + (b : ℝ) i`. -/
def toC (z : GaussRat) : ℂ := ⟨(z.re : ℝ), (z.im : ℝ)⟩

@[simp] lemma toC_re (z : GaussRat) : (toC z).re = z.re := rfl
@[simp] lemma toC_im (z : GaussRat) : (toC z).im = z.im := rfl

lemma toC_add (z w : GaussRat) : toC (z + w) = toC z + toC w := by
  apply Complex.ext <;> simp [toC]
lemma toC_sub (z w : GaussRat) : toC (z - w) = toC z - toC w := by
  apply Complex.ext <;> simp [toC]
lemma toC_neg (z : GaussRat) : toC (-z) = -toC z := by
  apply Complex.ext <;> simp [toC]
lemma toC_mul (z w : GaussRat) : toC (z * w) = toC z * toC w := by
  apply Complex.ext <;> simp [toC]
lemma toC_star (z : GaussRat) : toC (star z) = conj (toC z) := by
  apply Complex.ext <;> simp [toC]
@[simp] lemma toC_zero : toC 0 = 0 := by apply Complex.ext <;> simp [toC]
@[simp] lemma toC_one : toC 1 = 1 := by apply Complex.ext <;> simp [toC]
lemma toC_ratCast (q : ℚ) : toC (q : GaussRat) = (q : ℂ) := by
  apply Complex.ext <;> simp [toC]
lemma toC_natCast (n : ℕ) : toC (n : GaussRat) = (n : ℂ) := by
  apply Complex.ext <;> simp [toC]

lemma toC_injective : Function.Injective toC := by
  intro z w h
  have h1 := congrArg Complex.re h
  have h2 := congrArg Complex.im h
  simp only [toC_re, toC_im, Rat.cast_inj] at h1 h2
  exact GaussRat.ext h1 h2

lemma toC_eq_zero_iff (z : GaussRat) : toC z = 0 ↔ z = 0 := by
  constructor
  · intro h; exact toC_injective (by rw [h, toC_zero])
  · rintro rfl; exact toC_zero

lemma normSq_toC (z : GaussRat) : normSq (toC z) = (z.normSq : ℝ) := by
  simp only [normSq_apply, toC_re, toC_im, GaussRat.normSq]; push_cast; ring

/-- The embedding `ℚ(i)³ → ℂ³`. -/
def ι (v : GVec) : Fin 3 → ℂ := ![toC v.x, toC v.y, toC v.z]

@[simp] lemma ι_apply_zero (v : GVec) : ι v 0 = toC v.x := rfl
@[simp] lemma ι_apply_one (v : GVec) : ι v 1 = toC v.y := rfl
@[simp] lemma ι_apply_two (v : GVec) : ι v 2 = toC v.z := rfl

lemma ι_injective : Function.Injective ι := by
  intro u v h
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  have h2 := congrFun h 2
  simp only [ι_apply_zero, ι_apply_one, ι_apply_two] at h0 h1 h2
  cases u; cases v
  simp only at h0 h1 h2
  rw [toC_injective h0, toC_injective h1, toC_injective h2]

lemma ι_ne_zero {v : GVec} (hv : v.NonZero) : ι v ≠ 0 := by
  intro h
  rcases hv with hx | hy | hz
  · exact hx ((toC_eq_zero_iff _).1 (by simpa using congrFun h 0))
  · exact hy ((toC_eq_zero_iff _).1 (by simpa using congrFun h 1))
  · exact hz ((toC_eq_zero_iff _).1 (by simpa using congrFun h 2))

lemma nonZero_of_ι_ne_zero {v : GVec} (hv : ι v ≠ 0) : v.NonZero := by
  by_contra h
  apply hv
  simp only [GVec.NonZero, not_or, not_not] at h
  obtain ⟨hx, hy, hz⟩ := h
  ext i; fin_cases i <;> simp [ι, hx, hy, hz]

lemma dotC_ι (u v : GVec) : dotC (ι u) (ι v) = toC (GVec.inner u v) := by
  simp only [dotC, ι, GVec.inner, toC_add, toC_mul, toC_star]
  simp

lemma nsq_ι (v : GVec) : nsq (ι v) = (normSqVec v : ℝ) := by
  simp only [nsq, ι, normSqVec]
  simp [normSq_toC]

lemma ι_smul (l : GaussRat) (v : GVec) : ι (GVec.smul l v) = toC l • ι v := by
  ext i; fin_cases i <;> simp [ι, GVec.smul, toC_mul]

lemma ι_add (u v : GVec) : ι (GVec.add u v) = ι u + ι v := by
  ext i; fin_cases i <;> simp [ι, GVec.add, toC_add]

lemma ι_sub (u v : GVec) : ι (GVec.sub u v) = ι u - ι v := by
  ext i; fin_cases i <;> simp [ι, GVec.sub, toC_sub]

/-- The conjugated cross product on `ℚ(i)³`, matching `GleasonComplex.ccross`. -/
def cross (u v : GVec) : GVec :=
  ⟨star (u.y * v.z - u.z * v.y), star (u.z * v.x - u.x * v.z), star (u.x * v.y - u.y * v.x)⟩

lemma ι_cross (u v : GVec) : ι (cross u v) = ccross (ι u) (ι v) := by
  ext i; fin_cases i <;> simp [ι, cross, ccross, toC_star, toC_sub, toC_mul]

lemma inner_cross_left (u v : GVec) : GVec.inner u (cross u v) = 0 := by
  apply toC_injective
  rw [← dotC_ι, ι_cross, dotC_ccross_left, toC_zero]

lemma inner_cross_right (u v : GVec) : GVec.inner v (cross u v) = 0 := by
  apply toC_injective
  rw [← dotC_ι, ι_cross, dotC_ccross_right, toC_zero]

lemma normSqVec_cross (u v : GVec) :
    normSqVec (cross u v) = normSqVec u * normSqVec v - (GVec.inner u v).normSq := by
  have := nsq_ccross (ι u) (ι v)
  rw [← ι_cross, nsq_ι, nsq_ι, nsq_ι, dotC_ι, normSq_toC] at this
  exact_mod_cast this

/-! ### The ray metric and uniform ray continuity -/

/-- The squared sine of the angle between the rays of `u` and `v`; phase- and
scale-invariant, rational-valued. -/
def raySinSq (u v : GVec) : ℚ :=
  1 - (GVec.inner u v).normSq / (normSqVec u * normSqVec v)

/-- **Declared input.**  Uniform continuity of `f` on rays: a rational `ε`-`δ` statement in the ray
metric `raySinSq`. -/
def IsUniformlyRayContinuous (f : GVec → ℚ) : Prop :=
  ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
    ∀ u v : GVec, u.NonZero → v.NonZero → raySinSq u v < δ → |f u - f v| < ε

lemma raySinSq_cast (u v : GVec) :
    (raySinSq u v : ℝ) = 1 - normSq (dotC (ι u) (ι v)) / (nsq (ι u) * nsq (ι v)) := by
  rw [dotC_ι, normSq_toC, nsq_ι, nsq_ι, raySinSq]; push_cast; ring

/-! ### Estimates on `ℂ³` -/

lemma ccross_self (u : Fin 3 → ℂ) : ccross u u = 0 := by
  ext i; fin_cases i <;> simp [ccross] <;> ring

lemma ccross_sub_right (u v w : Fin 3 → ℂ) : ccross u (v - w) = ccross u v - ccross u w := by
  ext i; fin_cases i <;> simp [ccross] <;> ring

/-- The ray distance is controlled by the vector distance: `sin²∠(u,w) ≤ |u - w|² / |w|²`. -/
lemma raySinSq_le_nsq_sub {u w : Fin 3 → ℂ} (hu : u ≠ 0) (hw : w ≠ 0) :
    1 - normSq (dotC u w) / (nsq u * nsq w) ≤ nsq (u - w) / nsq w := by
  have hpu := nsq_pos hu
  have hpw := nsq_pos hw
  have h1 := nsq_ccross u w
  have h2 : ccross u w = ccross u (w - u) := by
    rw [ccross_sub_right, ccross_self, sub_zero]
  have h3 := nsq_ccross u (w - u)
  have key : nsq u * nsq w - normSq (dotC u w) ≤ nsq u * nsq (w - u) := by
    rw [← h1, h2, h3]; linarith [normSq_nonneg (dotC u (w - u))]
  have hsub : nsq (u - w) = nsq (w - u) := by
    simp only [nsq, Pi.sub_apply]; rw [← normSq_neg, neg_sub, ← normSq_neg (u 1 - w 1), neg_sub,
      ← normSq_neg (u 2 - w 2), neg_sub]
  rw [hsub]
  have e : 1 - normSq (dotC u w) / (nsq u * nsq w) =
      (nsq u * nsq w - normSq (dotC u w)) / (nsq u * nsq w) := by
    field_simp
  rw [e, div_le_div_iff₀ (by positivity) hpw]
  calc (nsq u * nsq w - normSq (dotC u w)) * nsq w
      ≤ (nsq u * nsq (w - u)) * nsq w := mul_le_mul_of_nonneg_right key hpw.le
    _ = nsq (w - u) * (nsq u * nsq w) := by ring

/-- `|u - w|² ≤ 3 · dist(u,w)²` in the sup metric on `Fin 3 → ℂ`. -/
lemma nsq_sub_le_dist (u w : Fin 3 → ℂ) : nsq (u - w) ≤ 3 * dist u w ^ 2 := by
  have h : ∀ i : Fin 3, normSq (u i - w i) ≤ dist u w ^ 2 := by
    intro i
    rw [← Complex.sq_norm, ← Complex.dist_eq]
    exact pow_le_pow_left₀ dist_nonneg (dist_le_pi_dist u w i) 2
  simp only [nsq, Pi.sub_apply]
  linarith [h 0, h 1, h 2]

/-! ### Rational approximation -/

lemma exists_toC_near (z : ℂ) {ε : ℝ} (hε : 0 < ε) : ∃ q : GaussRat, dist (toC q) z < ε := by
  obtain ⟨a, ha⟩ := exists_rat_near z.re (half_pos hε)
  obtain ⟨b, hb⟩ := exists_rat_near z.im (half_pos hε)
  refine ⟨⟨a, b⟩, ?_⟩
  rw [Complex.dist_eq]
  calc ‖toC ⟨a, b⟩ - z‖ ≤ |(toC ⟨a, b⟩ - z).re| + |(toC ⟨a, b⟩ - z).im| :=
        Complex.norm_le_abs_re_add_abs_im _
    _ < ε / 2 + ε / 2 := by
        apply add_lt_add
        · simpa [toC, abs_sub_comm] using ha
        · simpa [toC, abs_sub_comm] using hb
    _ = ε := add_halves ε

lemma exists_ι_near (v : Fin 3 → ℂ) {ε : ℝ} (hε : 0 < ε) : ∃ g : GVec, dist (ι g) v < ε := by
  obtain ⟨a, ha⟩ := exists_toC_near (v 0) hε
  obtain ⟨b, hb⟩ := exists_toC_near (v 1) hε
  obtain ⟨c, hc⟩ := exists_toC_near (v 2) hε
  refine ⟨⟨a, b, c⟩, ?_⟩
  rw [dist_pi_lt_iff hε]
  intro i; fin_cases i <;> simpa [ι]

/-! ### The ambient space `S = {|v|² ≥ 1}` and its rational points -/

/-- Vectors of squared norm at least `1`. -/
def S : Set (Fin 3 → ℂ) := {v | 1 ≤ nsq v}

lemma S_ne_zero {v : Fin 3 → ℂ} (hv : v ∈ S) : v ≠ 0 :=
  ne_zero_of_nsq_pos (lt_of_lt_of_le one_pos hv)

lemma smul_mem_S {c : ℂ} (hc : 1 ≤ ‖c‖) {v : Fin 3 → ℂ} (hv : v ∈ S) : c • v ∈ S := by
  show 1 ≤ nsq (c • v)
  rw [nsq_smul, ← Complex.sq_norm]
  have : 1 ≤ ‖c‖ ^ 2 := by nlinarith
  calc (1 : ℝ) = 1 * 1 := (one_mul 1).symm
    _ ≤ ‖c‖ ^ 2 * nsq v := mul_le_mul this hv zero_le_one (by positivity)

/-- The rational points of `S`. -/
def D : Set S := {s | ∃ g : GVec, ι g = s.1}

lemma isOpen_gt_one : IsOpen {v : Fin 3 → ℂ | 1 < nsq v} :=
  isOpen_lt continuous_const continuous_nsq

lemma dense_D : Dense D := by
  rw [Metric.dense_iff]
  rintro ⟨v, hv⟩ r hr
  have hv' : 1 ≤ nsq v := hv
  -- push `v` slightly outwards so that nearby rational points stay in `S`
  set η : ℝ := r / (2 * (‖v‖ + 1)) with hη
  have hηpos : 0 < η := by positivity
  set t : Fin 3 → ℂ := ((1 + η : ℝ) : ℂ) • v with ht
  have htU : t ∈ {w : Fin 3 → ℂ | 1 < nsq w} := by
    show 1 < nsq t
    rw [ht, nsq_smul, normSq_ofReal]
    have : 1 < (1 + η) * (1 + η) := by nlinarith
    calc (1 : ℝ) = 1 * 1 := (one_mul 1).symm
      _ < (1 + η) * (1 + η) * nsq v := by nlinarith
  obtain ⟨ρ, hρ, hball⟩ := Metric.isOpen_iff.1 isOpen_gt_one t htU
  obtain ⟨g, hg⟩ := exists_ι_near t (lt_min hρ (half_pos hr))
  have hgS : ι g ∈ S := by
    have : ι g ∈ {w : Fin 3 → ℂ | 1 < nsq w} := hball (lt_of_lt_of_le hg (min_le_left _ _))
    exact le_of_lt (show 1 < nsq (ι g) from this)
  refine ⟨⟨ι g, hgS⟩, ?_, ⟨g, rfl⟩⟩
  rw [Metric.mem_ball, Subtype.dist_eq]
  have htv : dist t v = η * ‖v‖ := by
    have e : ((1 + η : ℝ) : ℂ) • v - v = ((η : ℝ) : ℂ) • v := by
      ext i; simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul]; push_cast; ring
    rw [dist_eq_norm, ht, e, norm_smul, Complex.norm_real, Real.norm_of_nonneg hηpos.le]
  have hηv : η * ‖v‖ < r / 2 := by
    rw [hη]
    have hvpos : 0 < ‖v‖ + 1 := by positivity
    rw [div_mul_eq_mul_div, div_lt_iff₀ (by positivity)]
    nlinarith [norm_nonneg v]
  calc dist (ι g) v ≤ dist (ι g) t + dist t v := dist_triangle _ _ _
    _ < r / 2 + r / 2 := add_lt_add (lt_of_lt_of_le hg (min_le_right _ _)) (htv ▸ hηv)
    _ = r := add_halves r

/-! ### The extension by uniform continuity -/

/-- `f` read on the rational points of `S`. -/
noncomputable def f₀ (f : GVec → ℚ) (d : D) : ℝ := (f (Classical.choose d.2) : ℝ)

lemma f₀_eq (f : GVec → ℚ) (d : D) {g : GVec} (hg : ι g = d.1.1) : f₀ f d = f g := by
  unfold f₀
  rw [ι_injective ((Classical.choose_spec d.2).trans hg.symm)]

theorem uniformContinuous_f₀ {f : GVec → ℚ} (hu : IsUniformlyRayContinuous f) :
    UniformContinuous (f₀ f) := by
  rw [Metric.uniformContinuous_iff]
  intro ε hε
  obtain ⟨ε', hε'0, hε'⟩ := exists_rat_btwn hε
  obtain ⟨δ, hδ, hf⟩ := hu ε' (by exact_mod_cast hε'0)
  have hδ' : (0 : ℝ) < δ := by exact_mod_cast hδ
  refine ⟨min 1 ((δ : ℝ) / 3), by positivity, ?_⟩
  rintro ⟨⟨a, ha⟩, g, hg⟩ ⟨⟨b, hb⟩, g', hg'⟩ hdd'
  simp only at hg hg'
  subst hg; subst hg'
  rw [f₀_eq f _ rfl, f₀_eq f _ rfl, Real.dist_eq]
  have hg0 : g.NonZero := nonZero_of_ι_ne_zero (S_ne_zero ha)
  have hg'0 : g'.NonZero := nonZero_of_ι_ne_zero (S_ne_zero hb)
  rw [Subtype.dist_eq, Subtype.dist_eq] at hdd'
  simp only at hdd'
  have hd1 : dist (ι g) (ι g') < 1 := lt_of_lt_of_le hdd' (min_le_left _ _)
  have hd2 : dist (ι g) (ι g') < δ / 3 := lt_of_lt_of_le hdd' (min_le_right _ _)
  have hsq : dist (ι g) (ι g') ^ 2 ≤ dist (ι g) (ι g') := by
    nlinarith [dist_nonneg (x := ι g) (y := ι g')]
  have key : raySinSq g g' < δ := by
    have h1 := raySinSq_le_nsq_sub (ι_ne_zero hg0) (ι_ne_zero hg'0)
    rw [← raySinSq_cast] at h1
    have h2 := nsq_sub_le_dist (ι g) (ι g')
    have hb' : 1 ≤ nsq (ι g') := hb
    have h3 : nsq (ι g - ι g') / nsq (ι g') ≤ nsq (ι g - ι g') := by
      rw [div_le_iff₀ (lt_of_lt_of_le one_pos hb')]
      exact le_mul_of_one_le_right (nsq_nonneg _) hb'
    have : (raySinSq g g' : ℝ) < δ := by linarith
    exact_mod_cast this
  have := hf g g' hg0 hg'0 key
  calc |(f g : ℝ) - f g'| = ((|f g - f g'| : ℚ) : ℝ) := by push_cast; rfl
    _ < ε' := by exact_mod_cast this
    _ < ε := hε'

lemma h_e : IsUniformInducing (Subtype.val : D → S) :=
  isUniformEmbedding_subtype_val.isUniformInducing

lemma h_dense : DenseRange (Subtype.val : D → S) := dense_D.denseRange_val

/-- The uniformly continuous extension of `f` to `S`. -/
noncomputable def ext (f : GVec → ℚ) : S → ℝ :=
  (h_e.isDenseInducing h_dense).extend (f₀ f)

theorem uniformContinuous_ext {f : GVec → ℚ} (hu : IsUniformlyRayContinuous f) :
    UniformContinuous (ext f) :=
  uniformContinuous_uniformly_extend h_e h_dense (uniformContinuous_f₀ hu)

theorem continuous_ext {f : GVec → ℚ} (hu : IsUniformlyRayContinuous f) :
    Continuous (ext f) :=
  (uniformContinuous_ext hu).continuous

theorem ext_eq_of_eq_ι {f : GVec → ℚ} (hu : IsUniformlyRayContinuous f) {g : GVec}
    (s : S) (hs : s.1 = ι g) : ext f s = f g := by
  have hmem : ι g ∈ S := hs ▸ s.2
  have hd : (⟨ι g, hmem⟩ : S) ∈ D := ⟨g, rfl⟩
  have e : s = (⟨ι g, hmem⟩ : S) := Subtype.ext hs
  rw [e]
  have := uniformly_extend_of_ind h_e h_dense (uniformContinuous_f₀ hu) ⟨⟨ι g, hmem⟩, hd⟩
  rw [f₀_eq f _ rfl] at this
  exact this

/-! ### Scale invariance of the extension -/

/-- Scalars of modulus at least one. -/
def C₁ : Set ℂ := {c | 1 ≤ ‖c‖}

/-- Rational scalars of modulus at least one. -/
def R₁ : Set C₁ := {c | ∃ l : GaussRat, toC l = c.1}

lemma dense_R₁ : Dense R₁ := by
  rw [Metric.dense_iff]
  rintro ⟨c, hc⟩ r hr
  have hc' : 1 ≤ ‖c‖ := hc
  set η : ℝ := r / (2 * (‖c‖ + 1)) with hη
  have hηpos : 0 < η := by positivity
  set t : ℂ := ((1 + η : ℝ) : ℂ) * c with ht
  have htn : ‖t‖ = (1 + η) * ‖c‖ := by
    rw [ht, norm_mul, Complex.norm_real, Real.norm_of_nonneg (by linarith)]
  obtain ⟨l, hl⟩ := exists_toC_near t (lt_min hηpos (half_pos hr))
  have hl1 : 1 ≤ ‖toC l‖ := by
    have h1 : dist (toC l) t < η := lt_of_lt_of_le hl (min_le_left _ _)
    have h2 : ‖t‖ ≤ ‖toC l‖ + dist (toC l) t := by
      rw [dist_comm, dist_eq_norm]
      calc ‖t‖ = ‖toC l + (t - toC l)‖ := by ring_nf
        _ ≤ ‖toC l‖ + ‖t - toC l‖ := norm_add_le _ _
    have : 1 + η ≤ ‖t‖ := by rw [htn]; nlinarith
    linarith
  refine ⟨⟨toC l, hl1⟩, ?_, ⟨l, rfl⟩⟩
  rw [Metric.mem_ball, Subtype.dist_eq]
  have htc : dist t c = η * ‖c‖ := by
    rw [dist_eq_norm, ht, show ((1 + η : ℝ) : ℂ) * c - c = ((η : ℝ) : ℂ) * c by push_cast; ring,
      norm_mul, Complex.norm_real, Real.norm_of_nonneg hηpos.le]
  have hηc : η * ‖c‖ < r / 2 := by
    rw [hη]
    have hcpos : 0 < ‖c‖ + 1 := by positivity
    rw [div_mul_eq_mul_div, div_lt_iff₀ (by positivity)]
    nlinarith [norm_nonneg c]
  calc dist (toC l) c ≤ dist (toC l) t + dist t c := dist_triangle _ _ _
    _ < r / 2 + r / 2 := add_lt_add (lt_of_lt_of_le hl (min_le_right _ _)) (htc ▸ hηc)
    _ = r := add_halves r

/-- `ext f (c • s) = ext f s` for a rational scalar `c` of modulus at least one. -/
theorem ext_smul_rat {f : GVec → ℚ} (hf : IsFrameFunction f) (hu : IsUniformlyRayContinuous f)
    {l : GaussRat} (hl : 1 ≤ ‖toC l‖) (s : S) :
    ext f ⟨toC l • s.1, smul_mem_S hl s.2⟩ = ext f s := by
  have hl0 : l ≠ 0 := by
    intro h0; rw [h0, toC_zero, norm_zero] at hl; linarith
  have key : (fun s : S => ext f ⟨toC l • s.1, smul_mem_S hl s.2⟩) = ext f := by
    apply Continuous.ext_on dense_D
    · exact (continuous_ext hu).comp
        (Continuous.subtype_mk (by fun_prop : Continuous fun s : S => toC l • s.1) _)
    · exact continuous_ext hu
    · rintro ⟨v, hv⟩ ⟨g, hg⟩
      simp only at hg
      subst hg
      have hg0 : g.NonZero := nonZero_of_ι_ne_zero (S_ne_zero hv)
      show ext f ⟨toC l • ι g, _⟩ = ext f ⟨ι g, hv⟩
      rw [ext_eq_of_eq_ι hu _ (ι_smul l g).symm, ext_eq_of_eq_ι hu _ rfl,
        GaussianTomography.frameFunction_smul hf hg0 hl0]
  exact congrFun key s

/-- `ext f (c • s) = ext f s` for every complex scalar `c` of modulus at least one. -/
theorem ext_smul {f : GVec → ℚ} (hf : IsFrameFunction f) (hu : IsUniformlyRayContinuous f)
    {c : ℂ} (hc : 1 ≤ ‖c‖) (s : S) :
    ext f ⟨c • s.1, smul_mem_S hc s.2⟩ = ext f s := by
  have key : (fun c : C₁ => ext f ⟨c.1 • s.1, smul_mem_S c.2 s.2⟩) = fun _ => ext f s := by
    apply Continuous.ext_on dense_R₁
    · exact (continuous_ext hu).comp
        (Continuous.subtype_mk (by fun_prop : Continuous fun c : C₁ => c.1 • s.1) _)
    · exact continuous_const
    · rintro ⟨c, hc⟩ ⟨l, hl⟩
      simp only at hl
      subst hl
      exact ext_smul_rat hf hu hc s
  exact congrFun key ⟨c, hc⟩

/-! ### The frame function on `ℂ³` -/

/-- Normalisation to the unit sphere. -/
noncomputable def normalize (v : Fin 3 → ℂ) : Fin 3 → ℂ :=
  ((1 / Real.sqrt (nsq v) : ℝ) : ℂ) • v

lemma nsq_normalize {v : Fin 3 → ℂ} (hv : v ≠ 0) : nsq (normalize v) = 1 := by
  have hpos := nsq_pos hv
  rw [normalize, nsq_smul, normSq_ofReal, div_mul_div_comm, one_mul,
    Real.mul_self_sqrt hpos.le]
  exact one_div_mul_cancel hpos.ne'

lemma normalize_mem_S {v : Fin 3 → ℂ} (hv : v ≠ 0) : normalize v ∈ S :=
  le_of_eq (nsq_normalize hv).symm

lemma sqrt_smul_normalize {v : Fin 3 → ℂ} (hv : v ≠ 0) :
    ((Real.sqrt (nsq v) : ℝ) : ℂ) • normalize v = v := by
  have hpos : 0 < Real.sqrt (nsq v) := Real.sqrt_pos.mpr (nsq_pos hv)
  rw [normalize, smul_smul, ← Complex.ofReal_mul, mul_one_div_cancel hpos.ne']
  simp

/-- The extension of `f` to all of `ℂ³` (value `0` at the origin, never used). -/
noncomputable def F (f : GVec → ℚ) (v : Fin 3 → ℂ) : ℝ :=
  if hv : v ≠ 0 then ext f ⟨normalize v, normalize_mem_S hv⟩ else 0

lemma F_eq {f : GVec → ℚ} {v : Fin 3 → ℂ} (hv : v ≠ 0) :
    F f v = ext f ⟨normalize v, normalize_mem_S hv⟩ := dif_pos hv

/-- On `S`, `F` is the extension. -/
theorem F_eq_ext {f : GVec → ℚ} (hf : IsFrameFunction f) (hu : IsUniformlyRayContinuous f)
    (s : S) : F f s.1 = ext f s := by
  have hv := S_ne_zero s.2
  rw [F_eq hv]
  have hc : 1 ≤ ‖((Real.sqrt (nsq s.1) : ℝ) : ℂ)‖ := by
    rw [Complex.norm_real, Real.norm_of_nonneg (Real.sqrt_nonneg _)]
    exact Real.one_le_sqrt.mpr s.2
  have := ext_smul hf hu hc ⟨normalize s.1, normalize_mem_S hv⟩
  rw [← this]
  congr 1
  exact Subtype.ext (sqrt_smul_normalize hv)

/-- `F` restricts to `f` on `ℚ(i)³`. -/
theorem F_ι {f : GVec → ℚ} (hf : IsFrameFunction f) (hu : IsUniformlyRayContinuous f)
    {g : GVec} (hg : g.NonZero) : F f (ι g) = f g := by
  have hv : ι g ≠ 0 := ι_ne_zero hg
  have hpos : 0 < Real.sqrt (nsq (ι g)) := Real.sqrt_pos.mpr (nsq_pos hv)
  -- a natural number `N ≥ 1 / √|g|²`
  set N : ℕ := ⌈1 / Real.sqrt (nsq (ι g))⌉₊ with hN
  have hN1 : 1 / Real.sqrt (nsq (ι g)) ≤ N := Nat.le_ceil _
  have hNpos : (0 : ℝ) < N := lt_of_lt_of_le (by positivity) hN1
  have hNnat : N ≠ 0 := Nat.pos_iff_ne_zero.mp (by exact_mod_cast hNpos)
  have hN0 : (N : GaussRat) ≠ 0 := by
    intro h; apply hNnat; have := congrArg GaussRat.re h; simpa using this
  set c : ℂ := ((N * Real.sqrt (nsq (ι g)) : ℝ) : ℂ) with hc
  have hc1 : 1 ≤ ‖c‖ := by
    rw [hc, Complex.norm_real, Real.norm_of_nonneg (by positivity)]
    rwa [div_le_iff₀ hpos] at hN1
  rw [F_eq hv, ← ext_smul hf hu hc1 ⟨normalize (ι g), normalize_mem_S hv⟩]
  rw [ext_eq_of_eq_ι hu (g := GVec.smul (N : GaussRat) g) _ ?_,
    GaussianTomography.frameFunction_smul hf hg hN0]
  show c • normalize (ι g) = ι (GVec.smul (N : GaussRat) g)
  rw [ι_smul, toC_natCast, hc, normalize, smul_smul]
  congr 1
  have hsC : ((Real.sqrt (nsq (ι g)) : ℝ) : ℂ) ≠ 0 := by exact_mod_cast hpos.ne'
  push_cast
  field_simp

/-- `F` is scale invariant on nonzero vectors. -/
theorem F_smul {f : GVec → ℚ} (hf : IsFrameFunction f) (hu : IsUniformlyRayContinuous f)
    {v : Fin 3 → ℂ} (hv : v ≠ 0) {c : ℂ} (hc : c ≠ 0) : F f (c • v) = F f v := by
  have hcv : c • v ≠ 0 := smul_ne_zero hc hv
  have hcn : 0 < ‖c‖ := norm_pos_iff.mpr hc
  have hn : normalize (c • v) = (c / (‖c‖ : ℂ)) • normalize v := by
    rw [normalize, normalize, nsq_smul, ← Complex.sq_norm, Real.sqrt_mul (sq_nonneg _),
      Real.sqrt_sq hcn.le, smul_smul, smul_smul]
    congr 1
    push_cast
    field_simp
  have hphase : 1 ≤ ‖c / (‖c‖ : ℂ)‖ := by
    rw [norm_div, Complex.norm_real, Real.norm_of_nonneg hcn.le, div_self hcn.ne']
  rw [F_eq hcv, F_eq hv, ← ext_smul hf hu hphase ⟨normalize v, normalize_mem_S hv⟩]
  congr 1
  exact Subtype.ext hn

lemma continuous_normalize_restrict :
    Continuous (fun v : {v : Fin 3 → ℂ // v ≠ 0} => normalize v.1) := by
  have h1 : Continuous (fun v : {v : Fin 3 → ℂ // v ≠ 0} => (1 : ℝ) / Real.sqrt (nsq v.1)) :=
    Continuous.div₀ continuous_const
      (Real.continuous_sqrt.comp (continuous_nsq.comp continuous_subtype_val))
      (fun v => (Real.sqrt_pos.mpr (nsq_pos v.2)).ne')
  have h2 : Continuous (fun v : {v : Fin 3 → ℂ // v ≠ 0} =>
      ((1 / Real.sqrt (nsq v.1) : ℝ) : ℂ)) := Complex.continuous_ofReal.comp h1
  show Continuous (fun v : {v : Fin 3 → ℂ // v ≠ 0} => ((1 / Real.sqrt (nsq v.1) : ℝ) : ℂ) • v.1)
  exact h2.smul continuous_subtype_val

theorem continuousOn_F {f : GVec → ℚ} (hu : IsUniformlyRayContinuous f) :
    ContinuousOn (F f) {v | v ≠ 0} := by
  rw [continuousOn_iff_continuous_domRestrict]
  have : Set.domRestrict {v : Fin 3 → ℂ | v ≠ 0} (F f) =
      (ext f) ∘ (fun v : {v : Fin 3 → ℂ // v ≠ 0} => ⟨normalize v.1, normalize_mem_S v.2⟩) := by
    funext v
    exact F_eq v.2
  rw [this]
  exact (continuous_ext hu).comp (Continuous.subtype_mk continuous_normalize_restrict _)

/-! ### The frame property of `F` -/

lemma ccross_smul_right (u : Fin 3 → ℂ) (c : ℂ) (v : Fin 3 → ℂ) :
    ccross u (c • v) = conj c • ccross u v := by
  ext i; fin_cases i <;> simp [ccross] <;> ring

lemma ccross_smul_left (c : ℂ) (u v : Fin 3 → ℂ) :
    ccross (c • u) v = conj c • ccross u v := by
  ext i; fin_cases i <;> simp [ccross] <;> ring

lemma ccross_zero_right (u : Fin 3 → ℂ) : ccross u 0 = 0 := by
  ext i; fin_cases i <;> simp [ccross]

lemma continuous_ccross_pair :
    Continuous (fun p : (Fin 3 → ℂ) × (Fin 3 → ℂ) => ccross p.1 p.2) := by
  apply continuous_pi
  intro i
  fin_cases i <;> simp only [ccross] <;> simp <;> fun_prop

lemma continuous_dotC_pair :
    Continuous (fun p : (Fin 3 → ℂ) × (Fin 3 → ℂ) => dotC p.1 p.2) := by
  unfold dotC; fun_prop

/-- Projection of `h` onto the orthogonal complement of `u`. -/
noncomputable def proj (u h : Fin 3 → ℂ) : Fin 3 → ℂ :=
  h - (dotC u h / (nsq u : ℂ)) • u

lemma dotC_proj {u : Fin 3 → ℂ} (hu : u ≠ 0) (h : Fin 3 → ℂ) : dotC u (proj u h) = 0 := by
  have hn : (nsq u : ℂ) ≠ 0 := by exact_mod_cast (nsq_pos hu).ne'
  rw [proj, dotC_sub_right, dotC_smul_right, dotC_self_eq_nsq]
  field_simp
  ring

lemma ccross_proj (u h : Fin 3 → ℂ) : ccross u (proj u h) = ccross u h := by
  rw [proj, ccross_sub_right, ccross_smul_right, ccross_self, smul_zero, sub_zero]

lemma proj_of_dotC_zero {u h : Fin 3 → ℂ} (huh : dotC u h = 0) : proj u h = h := by
  rw [proj, huh, zero_div, zero_smul, sub_zero]

lemma continuous_proj_pair :
    Continuous (fun p : {p : (Fin 3 → ℂ) × (Fin 3 → ℂ) // p.1 ≠ 0} => proj p.1.1 p.1.2) := by
  have h1 : Continuous (fun p : {p : (Fin 3 → ℂ) × (Fin 3 → ℂ) // p.1 ≠ 0} =>
      dotC p.1.1 p.1.2 / (nsq p.1.1 : ℂ)) := by
    apply Continuous.div₀ (continuous_dotC_pair.comp continuous_subtype_val)
      (Complex.continuous_ofReal.comp
        (continuous_nsq.comp (continuous_fst.comp continuous_subtype_val)))
    intro p
    show (nsq p.1.1 : ℂ) ≠ 0
    exact_mod_cast (nsq_pos p.2).ne'
  show Continuous (fun p : {p : (Fin 3 → ℂ) × (Fin 3 → ℂ) // p.1 ≠ 0} =>
    p.1.2 - (dotC p.1.1 p.1.2 / (nsq p.1.1 : ℂ)) • p.1.1)
  exact (continuous_snd.comp continuous_subtype_val).sub
    (h1.smul (continuous_fst.comp continuous_subtype_val))

/-- Pairs `(u, h)` with `u ≠ 0` and `u × h ≠ 0`. -/
def T : Set ((Fin 3 → ℂ) × (Fin 3 → ℂ)) := {p | p.1 ≠ 0 ∧ ccross p.1 p.2 ≠ 0}

lemma isOpen_T : IsOpen T :=
  (isOpen_ne_fun continuous_fst continuous_const).inter
    (isOpen_ne_fun continuous_ccross_pair continuous_const)

/-- Rational pairs in `T`. -/
def RT : Set T := {p | ∃ g h : GVec, ι g = p.1.1 ∧ ι h = p.1.2}

lemma dense_RT : Dense RT := by
  rw [Metric.dense_iff]
  rintro ⟨⟨u, h⟩, hp⟩ r hr
  obtain ⟨ρ, hρ, hball⟩ := Metric.isOpen_iff.1 isOpen_T _ hp
  obtain ⟨g, hg⟩ := exists_ι_near u (lt_min hρ hr)
  obtain ⟨k, hk⟩ := exists_ι_near h (lt_min hρ hr)
  have hmem : ((ι g, ι k) : (Fin 3 → ℂ) × (Fin 3 → ℂ)) ∈ T := by
    apply hball
    rw [Metric.mem_ball, Prod.dist_eq]
    exact max_lt (lt_of_lt_of_le hg (min_le_left _ _)) (lt_of_lt_of_le hk (min_le_left _ _))
  refine ⟨⟨(ι g, ι k), hmem⟩, ?_, ⟨g, k, rfl, rfl⟩⟩
  rw [Metric.mem_ball, Subtype.dist_eq, Prod.dist_eq]
  exact max_lt (lt_of_lt_of_le hg (min_le_right _ _)) (lt_of_lt_of_le hk (min_le_right _ _))

lemma inner_smul_right (l : GaussRat) (u v : GVec) :
    GVec.inner u (GVec.smul l v) = l * GVec.inner u v := by
  apply toC_injective
  rw [← dotC_ι, ι_smul, dotC_smul_right, toC_mul, dotC_ι]

lemma inner_sub_right (u v w : GVec) :
    GVec.inner u (GVec.sub v w) = GVec.inner u v - GVec.inner u w := by
  apply toC_injective
  rw [← dotC_ι, ι_sub, dotC_sub_right, toC_sub, dotC_ι, dotC_ι]

/-- On `T`, `F u + F (proj u h) + F (u × h) = 1`. -/
theorem F_frame_proj {f : GVec → ℚ} (hf : IsFrameFunction f) (hu : IsUniformlyRayContinuous f)
    (p : T) : F f p.1.1 + F f (proj p.1.1 p.1.2) + F f (ccross p.1.1 p.1.2) = 1 := by
  have hproj0 : ∀ p : T, proj p.1.1 p.1.2 ≠ 0 := by
    intro p h0
    have := ccross_proj p.1.1 p.1.2
    rw [h0, ccross_zero_right] at this
    exact p.2.2 this.symm
  have key : (fun p : T => F f p.1.1 + F f (proj p.1.1 p.1.2) + F f (ccross p.1.1 p.1.2)) =
      fun _ => 1 := by
    apply Continuous.ext_on dense_RT
    · have hF := continuousOn_F hu
      refine ((hF.comp_continuous (continuous_fst.comp continuous_subtype_val)
        (fun p => p.2.1)).add (hF.comp_continuous ?_ hproj0)).add
        (hF.comp_continuous (continuous_ccross_pair.comp continuous_subtype_val) (fun p => p.2.2))
      exact continuous_proj_pair.comp (Continuous.subtype_mk continuous_subtype_val (fun p => p.2.1))
    · exact continuous_const
    · rintro ⟨⟨u, h⟩, hp⟩ ⟨g, k, hg, hk⟩
      simp only at hg hk
      subst hg; subst hk
      have hg0 : g.NonZero := nonZero_of_ι_ne_zero hp.1
      have hn : (nsq (ι g) : ℂ) ≠ 0 := by exact_mod_cast (nsq_pos hp.1).ne'
      have hp0 : proj (ι g) (ι k) ≠ 0 := hproj0 ⟨(ι g, ι k), hp⟩
      -- the rational frame `(g, k', g × k)` with `k' = ⟨g,g⟩ k - ⟨g,k⟩ g`
      set k' : GVec := GVec.sub (GVec.smul (GVec.inner g g) k) (GVec.smul (GVec.inner g k) g)
        with hk'
      have hιk' : ι k' = (nsq (ι g) : ℂ) • proj (ι g) (ι k) := by
        rw [hk', ι_sub, ι_smul, ι_smul, proj, smul_sub, smul_smul, ← dotC_ι, ← dotC_ι,
          dotC_self_eq_nsq, mul_div_cancel₀ _ hn]
      have hk'0 : k'.NonZero :=
        nonZero_of_ι_ne_zero (by rw [hιk']; exact smul_ne_zero hn hp0)
      have hcross0 : (cross g k).NonZero :=
        nonZero_of_ι_ne_zero (by rw [ι_cross]; exact hp.2)
      have h1 : GVec.inner g k' = 0 := by
        apply toC_injective
        rw [← dotC_ι, hιk', dotC_smul_right, dotC_proj hp.1, mul_zero, toC_zero]
      have h2 : GVec.inner k' (cross g k) = 0 := by
        apply toC_injective
        rw [← dotC_ι, hιk', ι_cross, dotC_smul_left, proj, dotC_sub_left, dotC_smul_left,
          dotC_ccross_right, dotC_ccross_left, mul_zero, sub_zero, mul_zero, toC_zero]
      have hframe : IsFrame g k' (cross g k) :=
        ⟨hg0, hk'0, hcross0, h1, inner_cross_left g k, h2⟩
      have hsum := hf g k' (cross g k) hframe
      show F f (ι g) + F f (proj (ι g) (ι k)) + F f (ccross (ι g) (ι k)) = 1
      have e2 : F f (proj (ι g) (ι k)) = f k' := by
        rw [← F_ι hf hu hk'0, hιk', F_smul hf hu hp0 hn]
      rw [F_ι hf hu hg0, e2, ← ι_cross, F_ι hf hu hcross0]
      exact_mod_cast hsum
  exact congrFun key p

theorem F_frame_cross {f : GVec → ℚ} (hf : IsFrameFunction f) (hu : IsUniformlyRayContinuous f)
    {u v : Fin 3 → ℂ} (hu0 : u ≠ 0) (hv0 : v ≠ 0) (huv : dotC u v = 0) :
    F f u + F f v + F f (ccross u v) = 1 := by
  have hc : ccross u v ≠ 0 := by
    apply ne_zero_of_nsq_pos
    rw [nsq_ccross, huv, map_zero, sub_zero]
    exact mul_pos (nsq_pos hu0) (nsq_pos hv0)
  have := F_frame_proj hf hu ⟨(u, v), hu0, hc⟩
  simp only at this
  rwa [proj_of_dotC_zero huv] at this

/-- A third vector orthogonal to `u` and `v` is a multiple of `u × v`. -/
lemma eq_smul_ccross {u v w : Fin 3 → ℂ} (hu0 : u ≠ 0) (hv0 : v ≠ 0) (hw0 : w ≠ 0)
    (huv : dotC u v = 0) (huw : dotC u w = 0) (hvw : dotC v w = 0) :
    ∃ μ : ℂ, μ ≠ 0 ∧ w = μ • ccross u v := by
  set p := normalize u with hp
  set q := normalize v with hq
  have hp1 : nsq p = 1 := nsq_normalize hu0
  have hq1 : nsq q = 1 := nsq_normalize hv0
  have hpq : dotC p q = 0 := by
    rw [hp, hq, normalize, normalize, dotC_smul_left, dotC_smul_right, huv]; ring
  have hfr := isOrthonormalC_ccross hp1 hq1 hpq
  have hpw : dotC p w = 0 := by rw [hp, normalize, dotC_smul_left, huw, mul_zero]
  have hqw : dotC q w = 0 := by rw [hq, normalize, dotC_smul_left, hvw, mul_zero]
  have hcomp := completenessC hfr w
  rw [hpw, hqw, zero_smul, zero_smul, zero_add, zero_add] at hcomp
  -- `u × v = (√|u|² √|v|²) • (p × q)`
  set a : ℝ := Real.sqrt (nsq u) with ha
  set b : ℝ := Real.sqrt (nsq v) with hb
  have hapos : 0 < a := Real.sqrt_pos.mpr (nsq_pos hu0)
  have hbpos : 0 < b := Real.sqrt_pos.mpr (nsq_pos hv0)
  have hu' : u = (a : ℂ) • p := (sqrt_smul_normalize hu0).symm
  have hv' : v = (b : ℂ) • q := (sqrt_smul_normalize hv0).symm
  have hcross : ccross u v = ((a * b : ℝ) : ℂ) • ccross p q := by
    rw [hu', hv', ccross_smul_left, ccross_smul_right, smul_smul, Complex.conj_ofReal,
      Complex.conj_ofReal]; push_cast; ring_nf
  have hr0 : dotC (ccross p q) w ≠ 0 := by
    intro h0; apply hw0; rw [← hcomp, h0, zero_smul]
  have hab : ((a * b : ℝ) : ℂ) ≠ 0 := by exact_mod_cast (mul_pos hapos hbpos).ne'
  refine ⟨dotC (ccross p q) w / ((a * b : ℝ) : ℂ), div_ne_zero hr0 hab, ?_⟩
  rw [hcross, smul_smul, div_mul_cancel₀ _ hab]
  exact hcomp.symm

/-- `F` is a frame function on `ℂ³` of weight `1`. -/
theorem isFrameFunctionC_F {f : GVec → ℚ} (hf : IsFrameFunction f)
    (hu : IsUniformlyRayContinuous f) : IsFrameFunctionC (F f) 1 where
  scale v hv c hc := F_smul hf hu hv hc
  frame u v w hu0 hv0 hw0 huv huw hvw := by
    obtain ⟨μ, hμ, hw⟩ := eq_smul_ccross hu0 hv0 hw0 huv huw hvw
    have hc : ccross u v ≠ 0 := by
      intro h0; apply hw0; rw [hw, h0, smul_zero]
    rw [hw, F_smul hf hu hc hμ]
    exact F_frame_cross hf hu hu0 hv0 huv

/-! ### Back on `ℚ(i)³`: the residual satisfies the orthogonal parallelogram law -/

/-- The Hermitian numerator produced by `gleason_complex`. -/
noncomputable def hermNum (p q r : Fin 3 → ℂ) (M α m : ℝ) (v : Fin 3 → ℂ) : ℝ :=
  M * normSq (dotC p v) + α * normSq (dotC q v) + m * normSq (dotC r v)

lemma hermNum_parallelogram (p q r : Fin 3 → ℂ) (M α m : ℝ) (u v : Fin 3 → ℂ) :
    hermNum p q r M α m (u + v) + hermNum p q r M α m (u - v) =
      2 * hermNum p q r M α m u + 2 * hermNum p q r M α m v := by
  simp only [hermNum, dotC_add_right, dotC_sub_right, normSq_add, normSq_sub]; ring

theorem exists_hermitian {f : GVec → ℚ} (hf : IsFrameFunction f)
    (hu : IsUniformlyRayContinuous f) :
    ∃ p q r : Fin 3 → ℂ, ∃ M α m : ℝ, ∀ g : GVec, g.NonZero →
      (f g : ℝ) = hermNum p q r M α m (ι g) / normSqVec g := by
  obtain ⟨p, q, r, _, M, α, m, h⟩ := gleason_complex (isFrameFunctionC_F hf hu) (continuousOn_F hu)
  refine ⟨p, q, r, M, α, m, fun g hg => ?_⟩
  rw [← F_ι hf hu hg, h _ (ι_ne_zero hg), nsq_ι]
  rfl

lemma quadNum_add_sub (ρ : HermForm3) (u v : GVec) :
    quadNum ρ (GVec.add u v) + quadNum ρ (GVec.sub u v) = 2 * quadNum ρ u + 2 * quadNum ρ v := by
  simp only [quadNum, GVec.add, GVec.sub, GaussRat.normSq, re_add, im_add, re_sub, im_sub]; ring

lemma normSqVec_add_of_inner_zero {u v : GVec} (h : GVec.inner u v = 0) :
    normSqVec (GVec.add u v) = normSqVec u + normSqVec v := by
  have hre := congrArg GaussRat.re h
  simp only [GVec.inner, re_add, re_mul, re_star, im_star, re_zero] at hre
  simp only [normSqVec, GVec.add, GaussRat.normSq, re_add, im_add]
  linear_combination 2 * hre

lemma normSqVec_sub_of_inner_zero {u v : GVec} (h : GVec.inner u v = 0) :
    normSqVec (GVec.sub u v) = normSqVec u + normSqVec v := by
  have hre := congrArg GaussRat.re h
  simp only [GVec.inner, re_add, re_mul, re_star, im_star, re_zero] at hre
  simp only [normSqVec, GVec.sub, GaussRat.normSq, re_sub, im_sub]
  linear_combination (-2) * hre

lemma eq_zero_of_not_nonZero {v : GVec} (h : ¬ v.NonZero) : v = 0 := by
  simp only [GVec.NonZero, not_or, not_not] at h
  obtain ⟨hx, hy, hz⟩ := h
  cases v; simp only at hx hy hz; subst hx; subst hy; subst hz; rfl

lemma add_zero' (u : GVec) : GVec.add u 0 = u := by cases u; simp [GVec.add]
lemma sub_zero' (u : GVec) : GVec.sub u 0 = u := by cases u; simp [GVec.sub]
lemma zero_add' (v : GVec) : GVec.add 0 v = v := by cases v; simp [GVec.add]
lemma zero_sub' (v : GVec) : GVec.sub 0 v = GVec.smul (-1) v := by
  cases v; simp only [GVec.sub, GVec.smul]; congr 1 <;> apply GaussRat.ext <;> simp

lemma residual_neg {f : GVec → ℚ} (hf : IsFrameFunction f) {v : GVec} (hv : v.NonZero) :
    GaussianTomography.residual f (GVec.smul (-1) v) = GaussianTomography.residual f v := by
  have h1 : (-1 : GaussRat) ≠ 0 := by
    intro h; have := congrArg GaussRat.re h; simp at this
  rw [GaussianTomography.residual, GaussianTomography.residual,
    GaussianTomography.frameFunction_smul hf hv h1, quadRay_smul _ h1]

theorem residual_orthoParallelogram {f : GVec → ℚ} (hf : IsFrameFunction f)
    (hu : IsUniformlyRayContinuous f) :
    SatisfiesOrthoParallelogramZero (GaussianTomography.residual f) := by
  obtain ⟨p, q, r, M, α, m, hH⟩ := exists_hermitian hf hu
  intro u v huv hgu hgv
  set ρ := tomographyForm f with hρ
  have hres : ∀ x : GVec, x.NonZero →
      (GaussianTomography.residual f x : ℝ) =
        (hermNum p q r M α m (ι x) - quadNum ρ x) / normSqVec x := by
    intro x hx
    rw [GaussianTomography.residual, quadRay]; push_cast
    rw [hH x hx, sub_div]
  by_cases hu0 : u.NonZero
  · by_cases hv0 : v.NonZero
    · have hn : normSqVec (GVec.add u v) = normSqVec u + normSqVec v :=
        normSqVec_add_of_inner_zero huv
      have hn' : normSqVec (GVec.sub u v) = normSqVec u + normSqVec v :=
        normSqVec_sub_of_inner_zero huv
      have hpos : 0 < normSqVec u + normSqVec v :=
        add_pos (normSqVec_pos_of_nonZero hu0) (normSqVec_pos_of_nonZero hv0)
      have hadd0 : (GVec.add u v).NonZero := nonZero_of_normSqVec_pos (by rw [hn]; exact hpos)
      have hsub0 : (GVec.sub u v).NonZero := nonZero_of_normSqVec_pos (by rw [hn']; exact hpos)
      have hNu : hermNum p q r M α m (ι u) - quadNum ρ u = 0 := by
        have h := hres u hu0
        rw [hgu] at h; push_cast at h
        have hn0 : (normSqVec u : ℝ) ≠ 0 := by exact_mod_cast (normSqVec_pos_of_nonZero hu0).ne'
        rcases (div_eq_zero_iff.mp h.symm) with h' | h'
        · exact h'
        · exact absurd h' hn0
      have hNv : hermNum p q r M α m (ι v) - quadNum ρ v = 0 := by
        have h := hres v hv0
        rw [hgv] at h; push_cast at h
        have hn0 : (normSqVec v : ℝ) ≠ 0 := by exact_mod_cast (normSqVec_pos_of_nonZero hv0).ne'
        rcases (div_eq_zero_iff.mp h.symm) with h' | h'
        · exact h'
        · exact absurd h' hn0
      have hpar := hermNum_parallelogram p q r M α m (ι u) (ι v)
      have hq : (quadNum ρ (GVec.add u v) : ℝ) + quadNum ρ (GVec.sub u v) =
          2 * quadNum ρ u + 2 * quadNum ρ v := by exact_mod_cast quadNum_add_sub ρ u v
      have hcast : ((GaussianTomography.residual f (GVec.add u v) +
          GaussianTomography.residual f (GVec.sub u v) : ℚ) : ℝ) = 0 := by
        push_cast
        rw [hres _ hadd0, hres _ hsub0, ι_add, ι_sub, hn, hn', ← add_div]
        push_cast
        rw [div_eq_zero_iff]; left; linarith
      exact_mod_cast hcast
    · have hv' : v = 0 := eq_zero_of_not_nonZero hv0
      subst hv'
      rw [add_zero', sub_zero', hgu]; ring
  · have hu' : u = 0 := eq_zero_of_not_nonZero hu0
    subst hu'
    rw [zero_add', zero_sub', hgv]
    by_cases hv0 : v.NonZero
    · rw [residual_neg hf hv0, hgv]; ring
    · have hv' : v = 0 := eq_zero_of_not_nonZero hv0
      subst hv'
      have : GVec.smul (-1) (0 : GVec) = 0 := by
        apply GVec_ext <;> simp [GVec.smul] <;> rfl
      rw [this, hgv]; ring

/-- **Main theorem.**  A frame function on `ℚ(i)³` that is uniformly continuous on rays is the
Born quadratic form of its nine-ray tomography reconstruction, on every nonzero vector. -/
theorem born_of_uniformlyRayContinuous {f : GVec → ℚ} (hf : IsFrameFunction f)
    (hu : IsUniformlyRayContinuous f) :
    ∀ v : GVec, v.NonZero → f v = quadRay (tomographyForm f) v :=
  signed_rigidity_of_orthoParallelogramZero_residual hf (residual_orthoParallelogram hf hu)

end BornFinite.GleasonBridge
