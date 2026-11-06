/-
# Continuous frame functions on the complex sphere

Real-to-complex step of the Gleason argument on `ℂ³`.  A frame function is a degree-zero
function on nonzero vectors of `Fin 3 → ℂ` (invariant under all nonzero complex scalars)
whose values on orthonormal triples sum to a fixed weight.  Restricting such a function to
a "fully real" subspace `{x 0 • b₁ + x 1 • b₂ + x 2 • b₃ : x ∈ ℝ³}` of a complex orthonormal
basis gives a continuous real frame function, so `GleasonReal.gleason_real` applies there.
The two-dimensional phase lemma `two_dim` then shows that a maximiser kills every cross term,
and `gleason_complex` assembles a Hermitian form diagonal in an orthonormal basis `(p, q, r)`.
-/
import GleasonRealSphere

namespace GleasonComplex

open Complex ComplexConjugate Filter Topology

/-- Hermitian inner product, conjugate-linear in the first slot. -/
def dotC (u v : Fin 3 → ℂ) : ℂ := conj (u 0) * v 0 + conj (u 1) * v 1 + conj (u 2) * v 2

/-- Squared norm. -/
def nsq (v : Fin 3 → ℂ) : ℝ := normSq (v 0) + normSq (v 1) + normSq (v 2)

/-- The conjugated cross product: orthogonal to both arguments for `dotC`. -/
def ccross (a b : Fin 3 → ℂ) : Fin 3 → ℂ :=
  ![conj (a 1 * b 2 - a 2 * b 1), conj (a 2 * b 0 - a 0 * b 2), conj (a 0 * b 1 - a 1 * b 0)]

/-- A complex frame function of weight `W`. -/
structure IsFrameFunctionC (F : (Fin 3 → ℂ) → ℝ) (W : ℝ) : Prop where
  scale : ∀ v : Fin 3 → ℂ, v ≠ 0 → ∀ c : ℂ, c ≠ 0 → F (c • v) = F v
  frame : ∀ u v w : Fin 3 → ℂ, u ≠ 0 → v ≠ 0 → w ≠ 0 →
    dotC u v = 0 → dotC u w = 0 → dotC v w = 0 → F u + F v + F w = W

/-- Complex orthonormality. -/
structure IsOrthonormalC (p q r : Fin 3 → ℂ) : Prop where
  pp : dotC p p = 1
  qq : dotC q q = 1
  rr : dotC r r = 1
  pq : dotC p q = 0
  pr : dotC p r = 0
  qr : dotC q r = 0

lemma dotC_self_eq_nsq (v : Fin 3 → ℂ) : dotC v v = (nsq v : ℂ) := by
  apply Complex.ext <;> simp [dotC, nsq, normSq_apply]; ring

lemma nsq_nonneg (v : Fin 3 → ℂ) : 0 ≤ nsq v :=
  add_nonneg (add_nonneg (normSq_nonneg _) (normSq_nonneg _)) (normSq_nonneg _)

lemma nsq_eq_zero_iff (v : Fin 3 → ℂ) : nsq v = 0 ↔ v = 0 := by
  constructor
  · intro h
    unfold nsq at h
    have h0 : normSq (v 0) = 0 := by
      linarith [normSq_nonneg (v 0), normSq_nonneg (v 1), normSq_nonneg (v 2)]
    have h1 : normSq (v 1) = 0 := by
      linarith [normSq_nonneg (v 0), normSq_nonneg (v 1), normSq_nonneg (v 2)]
    have h2 : normSq (v 2) = 0 := by
      linarith [normSq_nonneg (v 0), normSq_nonneg (v 1), normSq_nonneg (v 2)]
    ext i; fin_cases i
    · simpa using normSq_eq_zero.mp h0
    · simpa using normSq_eq_zero.mp h1
    · simpa using normSq_eq_zero.mp h2
  · intro h; subst h; simp [nsq]

lemma nsq_pos {v : Fin 3 → ℂ} (hv : v ≠ 0) : 0 < nsq v :=
  lt_of_le_of_ne (nsq_nonneg v) (fun h => hv ((nsq_eq_zero_iff v).mp h.symm))

lemma ne_zero_of_nsq_pos {v : Fin 3 → ℂ} (h : 0 < nsq v) : v ≠ 0 :=
  fun hv => by rw [hv] at h; simp [nsq] at h

lemma nsq_smul (c : ℂ) (v : Fin 3 → ℂ) : nsq (c • v) = normSq c * nsq v := by
  simp [nsq, normSq_mul]; ring

lemma dotC_smul_left (c : ℂ) (u v : Fin 3 → ℂ) : dotC (c • u) v = conj c * dotC u v := by
  simp [dotC]; ring

lemma dotC_smul_right (c : ℂ) (u v : Fin 3 → ℂ) : dotC u (c • v) = c * dotC u v := by
  simp [dotC]; ring

lemma dotC_add_left (u v w : Fin 3 → ℂ) : dotC (u + v) w = dotC u w + dotC v w := by
  simp [dotC]; ring

lemma dotC_add_right (u v w : Fin 3 → ℂ) : dotC u (v + w) = dotC u v + dotC u w := by
  simp [dotC]; ring

lemma dotC_sub_left (u v w : Fin 3 → ℂ) : dotC (u - v) w = dotC u w - dotC v w := by
  simp [dotC]; ring

lemma dotC_sub_right (u v w : Fin 3 → ℂ) : dotC u (v - w) = dotC u v - dotC u w := by
  simp [dotC]; ring

lemma dotC_conj_symm (u v : Fin 3 → ℂ) : dotC v u = conj (dotC u v) := by
  simp [dotC]; ring

lemma dotC_ccross_left (a b : Fin 3 → ℂ) : dotC a (ccross a b) = 0 := by
  simp [dotC, ccross]; ring

lemma dotC_ccross_right (a b : Fin 3 → ℂ) : dotC b (ccross a b) = 0 := by
  simp [dotC, ccross]; ring

lemma nsq_ccross (a b : Fin 3 → ℂ) : nsq (ccross a b) = nsq a * nsq b - normSq (dotC a b) := by
  simp only [nsq, ccross, dotC, normSq_apply]
  simp
  ring

/-- `ℂ`-degree-zero functions are in particular `ℝ`-degree-zero. -/
lemma smul_real_eq (c : ℝ) (v : Fin 3 → ℂ) : (c : ℂ) • v = c • v := by
  ext i; simp [Complex.real_smul]

/-! ### Orthonormal completion over `ℂ` -/

/-- A unit vector orthogonal to a given unit vector. -/
theorem exists_unit_perp (p : Fin 3 → ℂ) :
    ∃ u : Fin 3 → ℂ, nsq u = 1 ∧ dotC p u = 0 := by
  by_cases h12 : normSq (p 1) + normSq (p 2) = 0
  · refine ⟨![0, 1, 0], by simp [nsq], ?_⟩
    have h1 : normSq (p 1) = 0 := by linarith [normSq_nonneg (p 1), normSq_nonneg (p 2)]
    have : p 1 = 0 := normSq_eq_zero.mp h1
    simp [dotC, this]
  · have hpos : 0 < normSq (p 1) + normSq (p 2) :=
      lt_of_le_of_ne (add_nonneg (normSq_nonneg _) (normSq_nonneg _)) (Ne.symm h12)
    let u0 : Fin 3 → ℂ := ![0, -(conj (p 2)), conj (p 1)]
    have hu0 : nsq u0 = normSq (p 1) + normSq (p 2) := by
      simp [nsq, u0, normSq_conj]; ring
    refine ⟨((1 / Real.sqrt (normSq (p 1) + normSq (p 2)) : ℝ) : ℂ) • u0, ?_, ?_⟩
    · rw [nsq_smul, hu0, normSq_ofReal, div_mul_div_comm, one_mul,
        Real.mul_self_sqrt hpos.le]
      exact one_div_mul_cancel hpos.ne'
    · rw [dotC_smul_right]
      have : dotC p u0 = 0 := by simp [dotC, u0]; ring
      rw [this, mul_zero]

/-- An orthonormal pair extends to an orthonormal triple by the conjugated cross product. -/
theorem isOrthonormalC_ccross {p q : Fin 3 → ℂ} (hp : nsq p = 1) (hq : nsq q = 1)
    (hpq : dotC p q = 0) : IsOrthonormalC p q (ccross p q) := by
  refine ⟨?_, ?_, ?_, hpq, dotC_ccross_left p q, dotC_ccross_right p q⟩
  · rw [dotC_self_eq_nsq, hp]; simp
  · rw [dotC_self_eq_nsq, hq]; simp
  · rw [dotC_self_eq_nsq, nsq_ccross, hp, hq, hpq]; simp


/-! ### Completeness over `ℂ` -/

/-- Completeness: `v = ⟨p,v⟩ p + ⟨q,v⟩ q + ⟨r,v⟩ r` for a complex orthonormal triple. -/
theorem completenessC {p q r : Fin 3 → ℂ} (h : IsOrthonormalC p q r) (v : Fin 3 → ℂ) :
    (dotC p v) • p + (dotC q v) • q + (dotC r v) • r = v := by
  -- the matrix with columns `p, q, r` is unitary
  let U : Matrix (Fin 3) (Fin 3) ℂ := Matrix.of fun i l => (![p, q, r] l) i
  have h1 : Matrix.conjTranspose U * U = 1 := by
    have hpp := h.pp; have hqq := h.qq; have hrr := h.rr
    have hpq := h.pq; have hpr := h.pr; have hqr := h.qr
    have hqp : dotC q p = 0 := by rw [dotC_conj_symm, hpq, map_zero]
    have hrp : dotC r p = 0 := by rw [dotC_conj_symm, hpr, map_zero]
    have hrq : dotC r q = 0 := by rw [dotC_conj_symm, hqr, map_zero]
    simp only [dotC] at hpp hqq hrr hpq hpr hqr hqp hrp hrq
    ext a b
    fin_cases a <;> fin_cases b <;>
      simp [U, Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_three] <;>
      first
      | exact hpp | exact hqq | exact hrr | exact hpq | exact hpr | exact hqr
      | exact hqp | exact hrp | exact hrq
  have h2 : U * Matrix.conjTranspose U = 1 := mul_eq_one_comm.1 h1
  have key : ∀ i j : Fin 3, p i * conj (p j) + q i * conj (q j) + r i * conj (r j) =
      if i = j then 1 else 0 := by
    intro i j
    have := congrFun (congrFun h2 i) j
    simpa [U, Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_three,
      Matrix.one_apply] using this
  ext i
  have k0 := key i 0
  have k1 := key i 1
  have k2 := key i 2
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, dotC]
  fin_cases i <;> simp at k0 k1 k2 ⊢ <;>
    linear_combination (v 0) * k0 + (v 1) * k1 + (v 2) * k2

/-! ### Fully real subspaces -/

/-- The real vector `x` placed in the complex frame `(b₁, b₂, b₃)`. -/
def ofFrameC (b₁ b₂ b₃ : Fin 3 → ℂ) (x : Fin 3 → ℝ) : Fin 3 → ℂ :=
  ((x 0 : ℝ) : ℂ) • b₁ + ((x 1 : ℝ) : ℂ) • b₂ + ((x 2 : ℝ) : ℂ) • b₃

lemma ofFrameC_apply (b₁ b₂ b₃ : Fin 3 → ℂ) (x : Fin 3 → ℝ) (i : Fin 3) :
    ofFrameC b₁ b₂ b₃ x i = (x 0 : ℂ) * b₁ i + (x 1 : ℂ) * b₂ i + (x 2 : ℂ) * b₃ i := by
  simp [ofFrameC]

lemma dotC_ofFrameC {b₁ b₂ b₃ : Fin 3 → ℂ} (h : IsOrthonormalC b₁ b₂ b₃) (x y : Fin 3 → ℝ) :
    dotC (ofFrameC b₁ b₂ b₃ x) (ofFrameC b₁ b₂ b₃ y) = (GleasonReal.dot3 x y : ℂ) := by
  have hqp : dotC b₂ b₁ = 0 := by rw [dotC_conj_symm, h.pq, map_zero]
  have hrp : dotC b₃ b₁ = 0 := by rw [dotC_conj_symm, h.pr, map_zero]
  have hrq : dotC b₃ b₂ = 0 := by rw [dotC_conj_symm, h.qr, map_zero]
  simp only [ofFrameC, dotC_add_left, dotC_add_right, dotC_smul_left, dotC_smul_right,
    h.pp, h.qq, h.rr, h.pq, h.pr, h.qr, hqp, hrp, hrq, conj_ofReal, GleasonReal.dot3]
  push_cast; ring

lemma nsq_ofFrameC {b₁ b₂ b₃ : Fin 3 → ℂ} (h : IsOrthonormalC b₁ b₂ b₃) (x : Fin 3 → ℝ) :
    nsq (ofFrameC b₁ b₂ b₃ x) = GleasonReal.dot3 x x := by
  have := dotC_ofFrameC h x x
  rw [dotC_self_eq_nsq] at this
  exact_mod_cast this

lemma ofFrameC_smul (b₁ b₂ b₃ : Fin 3 → ℂ) (c : ℝ) (x : Fin 3 → ℝ) :
    ofFrameC b₁ b₂ b₃ (c • x) = (c : ℂ) • ofFrameC b₁ b₂ b₃ x := by
  ext i; simp [ofFrameC_apply]; ring

lemma ofFrameC_ne_zero {b₁ b₂ b₃ : Fin 3 → ℂ} (h : IsOrthonormalC b₁ b₂ b₃) {x : Fin 3 → ℝ}
    (hx : x ≠ 0) : ofFrameC b₁ b₂ b₃ x ≠ 0 :=
  ne_zero_of_nsq_pos (by rw [nsq_ofFrameC h]; exact GleasonReal.dot3_self_pos hx)

lemma continuous_ofFrameC (b₁ b₂ b₃ : Fin 3 → ℂ) : Continuous (ofFrameC b₁ b₂ b₃) := by
  unfold ofFrameC; fun_prop

lemma ofFrameC_e1 (b₁ b₂ b₃ : Fin 3 → ℂ) : ofFrameC b₁ b₂ b₃ GleasonReal.e1 = b₁ := by
  ext i; simp [ofFrameC_apply, GleasonReal.e1]

lemma ofFrameC_e2 (b₁ b₂ b₃ : Fin 3 → ℂ) : ofFrameC b₁ b₂ b₃ ![0, 1, 0] = b₂ := by
  ext i; simp [ofFrameC_apply]

/-- Restriction of a complex frame function to a fully real subspace. -/
theorem IsFrameFunctionC.pullback {F : (Fin 3 → ℂ) → ℝ} {W : ℝ} (hF : IsFrameFunctionC F W)
    {b₁ b₂ b₃ : Fin 3 → ℂ} (h : IsOrthonormalC b₁ b₂ b₃) :
    GleasonReal.IsFrameFunction (fun x => F (ofFrameC b₁ b₂ b₃ x)) W where
  scale x hx c hc := by
    show F (ofFrameC b₁ b₂ b₃ (c • x)) = F (ofFrameC b₁ b₂ b₃ x)
    rw [ofFrameC_smul, hF.scale _ (ofFrameC_ne_zero h hx) _ (by exact_mod_cast hc)]
  frame u v w hu hv hw huv huw hvw :=
    hF.frame _ _ _ (ofFrameC_ne_zero h hu) (ofFrameC_ne_zero h hv) (ofFrameC_ne_zero h hw)
      (by rw [dotC_ofFrameC h, huv]; simp) (by rw [dotC_ofFrameC h, huw]; simp)
      (by rw [dotC_ofFrameC h, hvw]; simp)

theorem continuousOn_pullback {F : (Fin 3 → ℂ) → ℝ} (hc : ContinuousOn F {v | v ≠ 0})
    {b₁ b₂ b₃ : Fin 3 → ℂ} (h : IsOrthonormalC b₁ b₂ b₃) :
    ContinuousOn (fun x => F (ofFrameC b₁ b₂ b₃ x)) {x | x ≠ 0} :=
  hc.comp (continuous_ofFrameC b₁ b₂ b₃).continuousOn (fun _ hx => ofFrameC_ne_zero h hx)

/-! ### The two-dimensional phase lemma -/

/-- A quadratic `a s² + 2 c s t + b t²` bounded by `a (s² + t²)` has no cross term. -/
lemma cross_term_zero {a b c : ℝ}
    (h : ∀ s t : ℝ, ¬ (s = 0 ∧ t = 0) → a * s ^ 2 + 2 * c * s * t + b * t ^ 2 ≤ a * (s ^ 2 + t ^ 2)) :
    c = 0 := by
  by_contra hc
  have := h ((a - b + 1) / (2 * c)) 1 (by simp)
  have hc2 : (2 * c) ≠ 0 := mul_ne_zero two_ne_zero hc
  have e : 2 * c * ((a - b + 1) / (2 * c)) * 1 = a - b + 1 := by field_simp
  nlinarith [e]

/-- Real version: on the real plane spanned by orthonormal `x, w`, a maximiser `x` kills
the cross term. -/
theorem two_dim_real {F : (Fin 3 → ℂ) → ℝ} {W : ℝ} (hF : IsFrameFunctionC F W)
    (hc : ContinuousOn F {v | v ≠ 0}) {x w : Fin 3 → ℂ} (hx : nsq x = 1) (hw : nsq w = 1)
    (hxw : dotC x w = 0)
    (hmax : ∀ s t : ℝ, (s : ℂ) • x + (t : ℂ) • w ≠ 0 → F ((s : ℂ) • x + (t : ℂ) • w) ≤ F x) :
    ∀ s t : ℝ, (s : ℂ) • x + (t : ℂ) • w ≠ 0 →
      F ((s : ℂ) • x + (t : ℂ) • w) = (F x * s ^ 2 + F w * t ^ 2) / (s ^ 2 + t ^ 2) := by
  set z := ccross x w with hz
  have hfr : IsOrthonormalC x w z := isOrthonormalC_ccross hx hw hxw
  have hG := hF.pullback hfr
  have hcG := continuousOn_pullback hc hfr
  obtain ⟨p, q, r, _, M, α, m, hquad⟩ := GleasonReal.gleason_real hG hcG
  have hplane : ∀ s t : ℝ, ofFrameC x w z (s • GleasonReal.e1 + t • ![0, 1, 0]) =
      (s : ℂ) • x + (t : ℂ) • w := by
    intro s t; ext i; simp [ofFrameC_apply, GleasonReal.e1]
  have hne : ∀ s t : ℝ, (s : ℂ) • x + (t : ℂ) • w ≠ 0 →
      s • GleasonReal.e1 + t • (![0, 1, 0] : Fin 3 → ℝ) ≠ 0 := by
    intro s t hst h0
    apply hst
    rw [← hplane, h0]
    ext i; simp [ofFrameC_apply]
  have hdot : ∀ s t : ℝ, GleasonReal.dot3 (s • GleasonReal.e1 + t • ![0, 1, 0])
      (s • GleasonReal.e1 + t • ![0, 1, 0]) = s ^ 2 + t ^ 2 := by
    intro s t; simp [GleasonReal.dot3, GleasonReal.e1]; ring
  set a := M * p 0 ^ 2 + α * q 0 ^ 2 + m * r 0 ^ 2 with ha
  set b := M * p 1 ^ 2 + α * q 1 ^ 2 + m * r 1 ^ 2 with hb
  set c := M * (p 0 * p 1) + α * (q 0 * q 1) + m * (r 0 * r 1) with hcdef
  have hval : ∀ s t : ℝ, (s : ℂ) • x + (t : ℂ) • w ≠ 0 →
      F ((s : ℂ) • x + (t : ℂ) • w) = (a * s ^ 2 + 2 * c * s * t + b * t ^ 2) / (s ^ 2 + t ^ 2) := by
    intro s t hst
    have := hquad _ (hne s t hst)
    rw [hplane, hdot] at this
    rw [this]
    congr 1
    simp only [ha, hb, hcdef, GleasonReal.dot3, GleasonReal.e1]
    simp
    ring
  have ha' : a = F x := by
    have := hquad GleasonReal.e1 GleasonReal.e1_ne_zero
    rw [ofFrameC_e1] at this
    have hd : GleasonReal.dot3 GleasonReal.e1 GleasonReal.e1 = (1 : ℝ) := by
      simp [GleasonReal.dot3, GleasonReal.e1]
    rw [hd, div_one] at this
    rw [this, ha]
    simp [GleasonReal.dot3, GleasonReal.e1]
  have hb' : b = F w := by
    have h2 : (![0, 1, 0] : Fin 3 → ℝ) ≠ 0 := by
      intro h0; have := congrFun h0 1; simp at this
    have := hquad _ h2
    rw [ofFrameC_e2] at this
    have hd : GleasonReal.dot3 ![0, 1, 0] ![0, 1, 0] = (1 : ℝ) := by simp [GleasonReal.dot3]
    rw [hd, div_one] at this
    rw [this, hb]
    simp [GleasonReal.dot3]
  have hc0 : c = 0 := by
    apply cross_term_zero (a := a) (b := b)
    intro s t hst
    have hst' : (s : ℂ) • x + (t : ℂ) • w ≠ 0 := by
      intro h0
      apply hst
      have h1 : nsq ((s : ℂ) • x + (t : ℂ) • w) = s ^ 2 + t ^ 2 := by
        rw [← hplane, nsq_ofFrameC hfr, hdot]
      rw [h0] at h1
      simp [nsq] at h1
      constructor <;> nlinarith [sq_nonneg s, sq_nonneg t]
    have h1 := hval s t hst'
    have h2 := hmax s t hst'
    rw [h1, ← ha'] at h2
    have hpos : 0 < s ^ 2 + t ^ 2 := by
      rcases not_and_or.mp hst with h | h
      · have := sq_pos_of_ne_zero h; positivity
      · have := sq_pos_of_ne_zero h; positivity
    rwa [div_le_iff₀ hpos] at h2
  intro s t hst
  rw [hval s t hst, hc0, ha', hb']; ring

/-- Complex version (degree-zero form): if the unit vector `x` maximises `F` on the complex
span of `x` and a nonzero `w ⊥ x`, then `F` is a diagonal Hermitian form on that span. -/
theorem two_dim {F : (Fin 3 → ℂ) → ℝ} {W : ℝ} (hF : IsFrameFunctionC F W)
    (hc : ContinuousOn F {v | v ≠ 0}) {x w : Fin 3 → ℂ} (hx : nsq x = 1) (hw : w ≠ 0)
    (hxw : dotC x w = 0)
    (hmax : ∀ α β : ℂ, α • x + β • w ≠ 0 → F (α • x + β • w) ≤ F x) :
    ∀ α β : ℂ, α • x + β • w ≠ 0 →
      F (α • x + β • w) = (F x * normSq α + F w * (normSq β * nsq w)) /
        (normSq α + normSq β * nsq w) := by
  intro α β hαβ
  -- normalise `w`
  set s := Real.sqrt (nsq w) with hs
  have hspos : 0 < s := Real.sqrt_pos.mpr (nsq_pos hw)
  have hs2 : s ^ 2 = nsq w := Real.sq_sqrt (nsq_nonneg w)
  have hsne : s ≠ 0 := hspos.ne'
  have hsC : (s : ℂ) ≠ 0 := by exact_mod_cast hsne
  set w₀ : Fin 3 → ℂ := ((1 / s : ℝ) : ℂ) • w with hw₀
  have hw₀1 : nsq w₀ = 1 := by
    rw [hw₀, nsq_smul, normSq_ofReal, ← hs2]; field_simp
  have hxw₀ : dotC x w₀ = 0 := by rw [hw₀, dotC_smul_right, hxw, mul_zero]
  have hw₀w : w = (s : ℂ) • w₀ := by
    rw [hw₀, smul_smul]; push_cast
    rw [mul_one_div_cancel hsC]; simp
  have hFw₀ : F w₀ = F w := by
    rw [hw₀]; exact hF.scale w hw _ (by exact_mod_cast (one_div_pos.mpr hspos).ne')
  -- reduce to the unit case: `α • x + β • w = α • x + (β s) • w₀`
  have hrw : ∀ α β : ℂ, α • x + β • w = α • x + (β * s) • w₀ := by
    intro α β; rw [hw₀w, smul_smul]
  have hmax₀ : ∀ α β : ℂ, α • x + β • w₀ ≠ 0 → F (α • x + β • w₀) ≤ F x := by
    intro α β h
    have := hmax α (β / s) (by rwa [hrw, div_mul_cancel₀ _ (by exact_mod_cast hspos.ne')])
    rwa [hrw, div_mul_cancel₀ _ (by exact_mod_cast hspos.ne')] at this
  -- the unit case
  have unit_case : ∀ α β : ℂ, α • x + β • w₀ ≠ 0 →
      F (α • x + β • w₀) = (F x * normSq α + F w₀ * normSq β) / (normSq α + normSq β) := by
    intro α β h
    by_cases hα : α = 0
    · subst hα
      have hβ : β ≠ 0 := by rintro rfl; simp at h
      simp only [zero_smul, zero_add]
      rw [hF.scale w₀ (ne_zero_of_nsq_pos (by rw [hw₀1]; exact one_pos)) β hβ]
      have : normSq β ≠ 0 := normSq_pos.mpr hβ |>.ne'
      simp; field_simp
    by_cases hβ : β = 0
    · subst hβ
      simp only [zero_smul, add_zero]
      rw [hF.scale x (ne_zero_of_nsq_pos (by rw [hx]; exact one_pos)) α hα]
      have : normSq α ≠ 0 := normSq_pos.mpr hα |>.ne'
      simp; field_simp
    -- both nonzero: factor out the phase of `α`
    obtain ⟨lam, hlam⟩ : ∃ lam : ℂ, lam = α / (‖α‖ : ℂ) := ⟨_, rfl⟩
    obtain ⟨mu, hmu⟩ : ∃ mu : ℂ, mu = β / (‖β‖ : ℂ) := ⟨_, rfl⟩
    have hαn : (‖α‖ : ℂ) ≠ 0 := by exact_mod_cast (norm_pos_iff.mpr hα).ne'
    have hβn : (‖β‖ : ℂ) ≠ 0 := by exact_mod_cast (norm_pos_iff.mpr hβ).ne'
    have hlam1 : normSq lam = 1 := by
      rw [hlam, normSq_div, normSq_ofReal, normSq_eq_norm_sq]; field_simp
    have hmu1 : normSq mu = 1 := by
      rw [hmu, normSq_div, normSq_ofReal, normSq_eq_norm_sq]; field_simp
    have hlam0 : lam ≠ 0 := fun h0 => by rw [h0, map_zero] at hlam1; exact zero_ne_one hlam1
    have hmu0 : mu ≠ 0 := fun h0 => by rw [h0, map_zero] at hmu1; exact zero_ne_one hmu1
    have hphase : lam * conj lam = 1 := by rw [mul_conj, hlam1]; simp
    obtain ⟨w', hw'⟩ : ∃ w' : Fin 3 → ℂ, w' = (conj lam * mu) • w₀ := ⟨_, rfl⟩
    have hw'1 : nsq w' = 1 := by
      rw [hw', nsq_smul, normSq_mul, normSq_conj, hlam1, hmu1, hw₀1]; ring
    have hxw' : dotC x w' = 0 := by rw [hw', dotC_smul_right, hxw₀, mul_zero]
    have e1 : lam * (‖α‖ : ℂ) = α := by rw [hlam]; field_simp
    have e2 : lam * ((‖β‖ : ℂ) * (conj lam * mu)) = β := by
      have : lam * ((‖β‖ : ℂ) * (conj lam * mu)) = (lam * conj lam) * ((‖β‖ : ℂ) * mu) := by ring
      rw [this, hphase, one_mul, hmu]; field_simp
    have hdecomp : α • x + β • w₀ = lam • (((‖α‖ : ℝ) : ℂ) • x + ((‖β‖ : ℝ) : ℂ) • w') := by
      rw [hw']
      simp only [smul_add, smul_smul]
      rw [e1, e2]
    have hFw' : F w' = F w₀ := by
      rw [hw']
      exact hF.scale w₀ (ne_zero_of_nsq_pos (by rw [hw₀1]; exact one_pos)) _
        (mul_ne_zero ((map_ne_zero _).mpr hlam0) hmu0)
    -- the real lemma on `(x, w')`
    have hmax' : ∀ s t : ℝ, (s : ℂ) • x + (t : ℂ) • w' ≠ 0 →
        F ((s : ℂ) • x + (t : ℂ) • w') ≤ F x := by
      intro s t hst
      have e : (s : ℂ) • x + (t : ℂ) • w' = (s : ℂ) • x + ((t : ℂ) * (conj lam * mu)) • w₀ := by
        rw [hw', smul_smul]
      rw [e] at hst ⊢
      exact hmax₀ _ _ hst
    have hreal := two_dim_real hF hc hx hw'1 hxw' hmax'
    have hne' : ((‖α‖ : ℝ) : ℂ) • x + ((‖β‖ : ℝ) : ℂ) • w' ≠ 0 := by
      intro h0; apply h; rw [hdecomp, h0, smul_zero]
    rw [hdecomp, hF.scale _ hne' lam hlam0, hreal _ _ hne', hFw', normSq_eq_norm_sq,
      normSq_eq_norm_sq]
  -- back to `w`
  have h₀ : α • x + (β * s) • w₀ ≠ 0 := by rwa [← hrw]
  rw [hrw, unit_case _ _ h₀, hFw₀, normSq_mul, normSq_ofReal, ← sq, hs2]


/-! ### Compactness and maximisers on the complex sphere -/

lemma continuous_nsq : Continuous nsq := by
  unfold nsq
  exact ((Complex.continuous_normSq.comp (continuous_apply 0)).add
    (Complex.continuous_normSq.comp (continuous_apply 1))).add
    (Complex.continuous_normSq.comp (continuous_apply 2))

/-- The unit sphere of `ℂ³`. -/
def sphereC : Set (Fin 3 → ℂ) := {v | nsq v = 1}

lemma normSq_le_nsq (v : Fin 3 → ℂ) (i : Fin 3) : normSq (v i) ≤ nsq v := by
  fin_cases i <;> simp [nsq] <;>
    linarith [normSq_nonneg (v 0), normSq_nonneg (v 1), normSq_nonneg (v 2)]

lemma isCompact_sphereC : IsCompact sphereC := by
  apply Metric.isCompact_of_isClosed_isBounded
  · exact isClosed_eq continuous_nsq continuous_const
  · apply (Metric.isBounded_closedBall (x := (0 : Fin 3 → ℂ)) (r := 1)).subset
    intro v hv
    rw [Metric.mem_closedBall, dist_zero_right, pi_norm_le_iff_of_nonneg zero_le_one]
    intro i
    have h1 : normSq (v i) ≤ 1 := by
      have := normSq_le_nsq v i
      rwa [show nsq v = 1 from hv] at this
    rw [← Complex.sq_norm] at h1
    nlinarith [norm_nonneg (v i)]

lemma sphereC_subset : sphereC ⊆ {v : Fin 3 → ℂ | v ≠ 0} := fun v hv =>
  ne_zero_of_nsq_pos (by rw [show nsq v = 1 from hv]; exact one_pos)

lemma e1C_mem_sphereC : (![1, 0, 0] : Fin 3 → ℂ) ∈ sphereC := by
  show nsq _ = 1; simp [nsq]

/-- Normalisation over `ℂ`: a nonzero vector is a positive real multiple of a unit vector. -/
lemma exists_unit_smulC {v : Fin 3 → ℂ} (hv : v ≠ 0) :
    ∃ c : ℂ, c ≠ 0 ∧ c • v ∈ sphereC := by
  have hpos := nsq_pos hv
  refine ⟨((1 / Real.sqrt (nsq v) : ℝ) : ℂ), ?_, ?_⟩
  · exact_mod_cast one_div_ne_zero (Real.sqrt_pos.mpr hpos).ne'
  · show nsq _ = 1
    rw [nsq_smul, normSq_ofReal, div_mul_div_comm, one_mul, Real.mul_self_sqrt hpos.le]
    exact one_div_mul_cancel hpos.ne'

theorem exists_max_unitC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ} (hF : IsFrameFunctionC F W)
    (hc : ContinuousOn F {v | v ≠ 0}) :
    ∃ p : Fin 3 → ℂ, nsq p = 1 ∧ ∀ v : Fin 3 → ℂ, v ≠ 0 → F v ≤ F p := by
  obtain ⟨p, hp, hmax⟩ := isCompact_sphereC.exists_isMaxOn ⟨_, e1C_mem_sphereC⟩
    (hc.mono sphereC_subset)
  refine ⟨p, hp, fun v hv => ?_⟩
  obtain ⟨c, hc0, hcv⟩ := exists_unit_smulC hv
  have : F (c • v) ≤ F p := hmax hcv
  rwa [hF.scale v hv c hc0] at this

/-- A maximiser on the unit sphere of the orthogonal complement of `p`. -/
theorem exists_max_perpC {F : (Fin 3 → ℂ) → ℝ} {W : ℝ} (hF : IsFrameFunctionC F W)
    (hc : ContinuousOn F {v | v ≠ 0}) (p : Fin 3 → ℂ) :
    ∃ q : Fin 3 → ℂ, nsq q = 1 ∧ dotC p q = 0 ∧
      ∀ v : Fin 3 → ℂ, v ≠ 0 → dotC p v = 0 → F v ≤ F q := by
  have hcl : IsClosed {v : Fin 3 → ℂ | dotC p v = 0} := by
    apply isClosed_eq _ continuous_const
    unfold dotC
    exact ((continuous_const.mul (continuous_apply 0)).add
      (continuous_const.mul (continuous_apply 1))).add (continuous_const.mul (continuous_apply 2))
  have hK : IsCompact (sphereC ∩ {v | dotC p v = 0}) := isCompact_sphereC.inter_right hcl
  obtain ⟨u, hu1, hpu⟩ := exists_unit_perp p
  obtain ⟨q, ⟨hq1, hq2⟩, hmax⟩ := hK.exists_isMaxOn ⟨u, hu1, hpu⟩
    (hc.mono (fun v hv => sphereC_subset hv.1))
  refine ⟨q, hq1, hq2, fun v hv hpv => ?_⟩
  obtain ⟨c, hc0, hcv⟩ := exists_unit_smulC hv
  have : F (c • v) ≤ F q := hmax ⟨hcv, by show dotC p (c • v) = 0; rw [dotC_smul_right, hpv, mul_zero]⟩
  rwa [hF.scale v hv c hc0] at this

/-! ### Assembly: Gleason's theorem on `ℂ³` -/

lemma dotC_combo {p q r : Fin 3 → ℂ} (h : IsOrthonormalC p q r) (a b c a' b' c' : ℂ) :
    dotC (a • p + b • q + c • r) (a' • p + b' • q + c' • r) =
      conj a * a' + conj b * b' + conj c * c' := by
  have hqp : dotC q p = 0 := by rw [dotC_conj_symm, h.pq, map_zero]
  have hrp : dotC r p = 0 := by rw [dotC_conj_symm, h.pr, map_zero]
  have hrq : dotC r q = 0 := by rw [dotC_conj_symm, h.qr, map_zero]
  simp only [dotC_add_left, dotC_add_right, dotC_smul_left, dotC_smul_right,
    h.pp, h.qq, h.rr, h.pq, h.pr, h.qr, hqp, hrp, hrq]
  ring

lemma nsq_combo {p q r : Fin 3 → ℂ} (h : IsOrthonormalC p q r) (a b c : ℂ) :
    nsq (a • p + b • q + c • r) = normSq a + normSq b + normSq c := by
  have := dotC_combo h a b c a b c
  rw [dotC_self_eq_nsq] at this
  apply Complex.ofReal_injective
  rw [this]; push_cast
  simp only [Complex.normSq_eq_conj_mul_self]

lemma nsq_combo2 {p q r : Fin 3 → ℂ} (h : IsOrthonormalC p q r) (b c : ℂ) :
    nsq (b • q + c • r) = normSq b + normSq c := by
  have := nsq_combo h 0 b c
  simpa using this

lemma dotC_combo2 {p q r : Fin 3 → ℂ} (h : IsOrthonormalC p q r) (b c : ℂ) :
    dotC p (b • q + c • r) = 0 := by
  simp only [dotC_add_right, dotC_smul_right, h.pq, h.pr]; ring

/-- **Gleason's theorem on `ℂ³` (continuous frame functions).**  A frame function that is
continuous away from the origin is the degree-zero form of a Hermitian form, diagonal in a
suitable orthonormal frame. -/
theorem gleason_complex {F : (Fin 3 → ℂ) → ℝ} {W : ℝ} (hF : IsFrameFunctionC F W)
    (hc : ContinuousOn F {v | v ≠ 0}) :
    ∃ p q r : Fin 3 → ℂ, IsOrthonormalC p q r ∧ ∃ M α m : ℝ,
      ∀ v : Fin 3 → ℂ, v ≠ 0 →
        F v = (M * normSq (dotC p v) + α * normSq (dotC q v) + m * normSq (dotC r v)) / nsq v := by
  obtain ⟨p, hp1, hpmax⟩ := exists_max_unitC hF hc
  obtain ⟨q, hq1, hpq, hqmax⟩ := exists_max_perpC hF hc p
  have hfr : IsOrthonormalC p q (ccross p q) := isOrthonormalC_ccross hp1 hq1 hpq
  set r := ccross p q with hr
  have hr1 : nsq r = 1 := by
    have := hfr.rr; rw [dotC_self_eq_nsq] at this; exact_mod_cast this
  refine ⟨p, q, r, hfr, F p, F q, F r, fun v hv => ?_⟩
  -- coordinates
  set a := dotC p v with ha
  set b := dotC q v with hb
  set c := dotC r v with hcc
  have hv' : v = a • p + b • q + c • r := (completenessC hfr v).symm
  have hnsq : nsq v = normSq a + normSq b + normSq c := by rw [hv', nsq_combo hfr]
  -- the component in `p⊥`
  set u := b • q + c • r with hu
  have hnu : nsq u = normSq b + normSq c := nsq_combo2 hfr b c
  have hpu : dotC p u = 0 := dotC_combo2 hfr b c
  have hvu : v = a • p + u := by rw [hv', add_assoc]
  -- value on `p⊥`
  have hFu : u ≠ 0 → F u * nsq u = F q * normSq b + F r * normSq c := by
    intro hu0
    have hqr : ∀ β γ : ℂ, β • q + γ • r ≠ 0 → F (β • q + γ • r) ≤ F q := by
      intro β γ hβγ
      exact hqmax _ hβγ (dotC_combo2 hfr β γ)
    have := two_dim hF hc hq1 (ne_zero_of_nsq_pos (by rw [hr1]; exact one_pos)) hfr.qr hqr b c
      hu0
    rw [hr1, mul_one] at this
    rw [this, hnu]
    have hpos : 0 < normSq b + normSq c := by rw [← hnu]; exact nsq_pos hu0
    field_simp
  by_cases hu0 : u = 0
  · -- `v` is a multiple of `p`
    have hb0 : normSq b = 0 := by
      have := hnu; rw [hu0, show nsq (0 : Fin 3 → ℂ) = 0 by simp [nsq]] at this
      linarith [normSq_nonneg b, normSq_nonneg c]
    have hc0 : normSq c = 0 := by
      have := hnu; rw [hu0, show nsq (0 : Fin 3 → ℂ) = 0 by simp [nsq]] at this
      linarith [normSq_nonneg b, normSq_nonneg c]
    have ha0 : a ≠ 0 := by
      intro h0
      apply hv
      rw [hvu, hu0, h0, zero_smul, add_zero]
    rw [hvu, hu0, add_zero, hF.scale p (ne_zero_of_nsq_pos (by rw [hp1]; exact one_pos)) a ha0]
    rw [show nsq (a • p) = normSq a by rw [nsq_smul, hp1, mul_one]]
    rw [hb0, hc0]
    have : normSq a ≠ 0 := normSq_pos.mpr ha0 |>.ne'
    field_simp
    ring
  · have hmaxp : ∀ α β : ℂ, α • p + β • u ≠ 0 → F (α • p + β • u) ≤ F p :=
      fun α β h => hpmax _ h
    have h2 := two_dim hF hc hp1 hu0 hpu hmaxp a 1 (by rw [one_smul, ← hvu]; exact hv)
    rw [one_smul, ← hvu] at h2
    rw [h2, normSq_one, one_mul, hnu, hnsq]
    have := hFu hu0
    rw [hnu] at this
    rw [this]; ring
end GleasonComplex
