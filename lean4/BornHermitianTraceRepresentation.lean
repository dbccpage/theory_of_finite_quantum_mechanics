import BornLinearExtension
import BornHermitianCarrier
import BornHermitianPsdDecomposition

/-
Born representation of effect valuations on Gaussian-rational matrices.  AuthorityEffect: None.

Every effect-additive, positive, normalised valuation on the n×n matrices over ℚ(i) (effects taken
in the Hermitian-form preorder with unit the identity) is `E ↦ re trace (ρ * E)` for a unique
matrix `ρ`, and that `ρ` is Hermitian, positive semidefinite on Gaussian-rational vectors, and has
trace one.  Conversely every Hermitian rational-PSD trace-one matrix defines such a valuation, and
a concrete valuation exists (the pure state `e₀`).  For a nonzero vector `x` the value on the
rank-one effect `P x = x x* / ⟨x, x⟩` is `⟨x, ρ x⟩ / ⟨x, x⟩`.

Valuations are real-valued and ℚ-linear; no ℚ(i)-linearity is assumed.  Supplied structure: the
Gaussian-rational matrix algebra and its order.  Derived structure: the trace form.  No continuity,
no real or complex numbers, no projection-lattice Gleason theorem.
-/

namespace BornFinite.HermitianCarrier

open Matrix BornFinite

variable {n : ℕ}

theorem space_isOrderUnit : (space n).IsOrderUnit := fun A => order_unit A

/-- The ℚ-linear extension of an effect valuation on Gaussian-rational matrices. -/
noncomputable def ext (W : EffectValuation (space n)) :
    Matrix (Fin n) (Fin n) GaussRat →ₗ[ℚ] ℚ :=
  (space n).extendₗ space_isOrderUnit W

theorem ext_effect (W : EffectValuation (space n)) {E : Matrix (Fin n) (Fin n) GaussRat}
    (hE : (space n).Effect E) : ext W E = W.v E :=
  (space n).extendₗ_effect space_isOrderUnit W hE

theorem ext_one (W : EffectValuation (space n)) : ext W 1 = 1 :=
  (space n).extendₗ_u space_isOrderUnit W

theorem ext_nonneg (W : EffectValuation (space n)) {A : Matrix (Fin n) (Fin n) GaussRat}
    (hA : (space n).le 0 A) : 0 ≤ ext W A :=
  (space n).extendₗ_nonneg space_isOrderUnit W hA

/-- The matrix representing an effect valuation. -/
noncomputable def density (W : EffectValuation (space n)) : Matrix (Fin n) (Fin n) GaussRat :=
  repMatrix (ext W)

theorem ext_eq_re_trace (W : EffectValuation (space n)) (A : Matrix (Fin n) (Fin n) GaussRat) :
    ext W A = (trace (density W * A)).re :=
  trace_rep (ext W) A

theorem density_effect (W : EffectValuation (space n)) {E : Matrix (Fin n) (Fin n) GaussRat}
    (hE : (space n).Effect E) : W.v E = (trace (density W * E)).re := by
  rw [← ext_eq_re_trace, ext_effect W hE]

theorem density_re_trace (W : EffectValuation (space n)) : (trace (density W)).re = 1 := by
  have h := ext_eq_re_trace W 1
  rw [mul_one, ext_one] at h
  exact h.symm

theorem density_psd (W : EffectValuation (space n)) : PsdH (density W) := by
  intro x
  by_cases hx : x = 0
  · subst hx
    simp [hf]
  · have hP := rankOne_effect hx
    have hpos := vnorm_pos hx
    rw [hf_eq_re_trace, ← ext_eq_re_trace]
    have e : vecMulVec x (star x) = (vnorm x) • P x := by
      unfold P
      rw [smul_smul, mul_one_div_cancel hpos.ne', one_smul]
    rw [e, map_smul, smul_eq_mul, ext_effect W hP]
    exact mul_nonneg hpos.le (W.nonneg _ hP)

/-- The extension vanishes on skew-Hermitian matrices: they are both `≤ 0` and `≥ 0`. -/
theorem ext_skew_zero (W : EffectValuation (space n)) {K : Matrix (Fin n) (Fin n) GaussRat}
    (hK : Kᴴ = -K) : ext W K = 0 := by
  obtain ⟨h1, h2⟩ := skew_le_zero_and_ge hK
  have ha : 0 ≤ ext W K := ext_nonneg W h2
  have hb : 0 ≤ ext W (-K) := by
    apply ext_nonneg W
    have := (space n).neg_le_neg h1
    rwa [neg_zero] at this
  rw [map_neg] at hb
  linarith

theorem single_conjTranspose (i j : Fin n) (c : GaussRat) :
    (single i j c)ᴴ = single j i (star c) := by
  apply Matrix.ext
  intro a b
  rw [conjTranspose_apply]
  by_cases h : j = a ∧ i = b
  · obtain ⟨rfl, rfl⟩ := h
    simp [Matrix.single]
  · have h' : ¬ (i = b ∧ j = a) := fun hh => h ⟨hh.2, hh.1⟩
    simp [Matrix.single, h, h']

theorem single_neg_eq (i j : Fin n) (c : GaussRat) :
    single i j (-c) = -(single i j c : Matrix (Fin n) (Fin n) GaussRat) := by
  apply Matrix.ext
  intro a b
  rw [Matrix.neg_apply]
  by_cases h : i = a ∧ j = b
  · obtain ⟨rfl, rfl⟩ := h
    simp [Matrix.single]
  · simp [Matrix.single, h]

theorem skew_single_sub (i j : Fin n) :
    (single j i (1 : GaussRat) - single i j 1)ᴴ = -(single j i (1 : GaussRat) - single i j 1) := by
  rw [conjTranspose_sub, single_conjTranspose, single_conjTranspose, star_one]
  abel

theorem skew_single_I_add (i j : Fin n) :
    (single j i GaussRat.I + single i j GaussRat.I)ᴴ =
      -(single j i GaussRat.I + single i j GaussRat.I) := by
  rw [conjTranspose_add, single_conjTranspose, single_conjTranspose, GaussRat.star_I,
    single_neg_eq, single_neg_eq]
  abel

theorem density_hermitian (W : EffectValuation (space n)) : (density W)ᴴ = density W := by
  apply Matrix.ext
  intro i j
  rw [conjTranspose_apply]
  have h1 := ext_skew_zero W (skew_single_sub i j)
  have h2 := ext_skew_zero W (skew_single_I_add i j)
  rw [map_sub, sub_eq_zero] at h1
  rw [map_add] at h2
  apply GaussRat.ext
  · simp [density, repMatrix_apply, h1]
  · simp [density, repMatrix_apply]
    linarith

theorem density_trace (W : EffectValuation (space n)) : trace (density W) = 1 := by
  apply GaussRat.ext
  · simpa using density_re_trace W
  · rw [GaussRat.im_one, trace, GaussRat.im_sum]
    apply Finset.sum_eq_zero
    intro i _
    simp only [density, repMatrix_apply, Matrix.diag_apply]
    have h := ext_skew_zero W (skew_single_I_add i i)
    rw [map_add] at h
    simp
    linarith

/-- The real-part trace functional `A ↦ re trace (ρ * A)` as a ℚ-linear map. -/
def traceWith (ρ : Matrix (Fin n) (Fin n) GaussRat) : Matrix (Fin n) (Fin n) GaussRat →ₗ[ℚ] ℚ where
  toFun A := (trace (ρ * A)).re
  map_add' A B := by rw [Matrix.mul_add, trace_add, GaussRat.re_add]
  map_smul' c A := by rw [Matrix.mul_smul, trace_smul, GaussRat.re_smul, RingHom.id_apply, smul_eq_mul]

theorem traceWith_apply (ρ A : Matrix (Fin n) (Fin n) GaussRat) :
    traceWith ρ A = (trace (ρ * A)).re := rfl

theorem density_unique (W : EffectValuation (space n)) (ρ : Matrix (Fin n) (Fin n) GaussRat)
    (h : ∀ E, (space n).Effect E → W.v E = (trace (ρ * E)).re) : ρ = density W := by
  have hL : ∀ A, (trace (ρ * A)).re = ext W A := by
    intro A
    have := (space n).extend_unique space_isOrderUnit W (traceWith ρ)
      (fun E hE => (h E hE).symm) A
    rw [← traceWith_apply, this]
    exact ((space n).extendₗ_apply space_isOrderUnit W A).symm
  apply rep_unique
  intro A
  rw [hL A, ext_eq_re_trace]

/-- Born representation over ℚ(i): an effect valuation is the real trace against a unique matrix. -/
theorem born_representation (W : EffectValuation (space n)) :
    ∃! ρ : Matrix (Fin n) (Fin n) GaussRat,
      ∀ E, (space n).Effect E → W.v E = (trace (ρ * E)).re :=
  ⟨density W, fun _ hE => density_effect W hE, fun ρ hρ => density_unique W ρ hρ⟩

/-- The representing matrix is a state: Hermitian, positive semidefinite over ℚ(i), trace one. -/
theorem density_is_state (W : EffectValuation (space n)) :
    (density W)ᴴ = density W ∧ PsdH (density W) ∧ trace (density W) = 1 :=
  ⟨density_hermitian W, density_psd W, density_trace W⟩

/-- The Born rule for rank-one effects: `v (P x) = ⟨x, ρ x⟩ / ⟨x, x⟩`. -/
theorem born_rule (W : EffectValuation (space n)) {x : Fin n → GaussRat} (hx : x ≠ 0) :
    W.v (P x) = hf (density W) x / vnorm x := by
  rw [density_effect W (rankOne_effect hx), hf_eq_re_trace]
  unfold P
  rw [Matrix.mul_smul, trace_smul, GaussRat.re_smul]
  ring

/-- The valuation `E ↦ re trace (ρ * E)` of a matrix positive on effects with real trace one. -/
def ofState (ρ : Matrix (Fin n) (Fin n) GaussRat)
    (hpos : ∀ E, (space n).Effect E → 0 ≤ (trace (ρ * E)).re) (htr : (trace ρ).re = 1) :
    EffectValuation (space n) where
  v E := (trace (ρ * E)).re
  unit := by
    show (trace (ρ * 1)).re = 1
    rw [mul_one, htr]
  nonneg := hpos
  additive := fun a b _ _ _ => by rw [Matrix.mul_add, trace_add, GaussRat.re_add]

theorem ofState_density (ρ : Matrix (Fin n) (Fin n) GaussRat)
    (hpos : ∀ E, (space n).Effect E → 0 ≤ (trace (ρ * E)).re) (htr : (trace ρ).re = 1) :
    density (ofState ρ hpos htr) = ρ :=
  (density_unique _ ρ (fun _ _ => rfl)).symm

/-! ### The converse for every state, via the Hermitian Gram decomposition -/

/-- Real trace positivity of a Hermitian PSD matrix against any effect; the effect need not be
Hermitian, since the real trace against a Hermitian `ρ` only sees its Hermitian part. -/
theorem re_trace_mul_nonneg_of_effect {ρ : Matrix (Fin n) (Fin n) GaussRat} (hρs : ρᴴ = ρ)
    (hρ : PsdH ρ) {E : Matrix (Fin n) (Fin n) GaussRat} (hE : (space n).Effect E) :
    0 ≤ (trace (ρ * E)).re := by
  have hEpsd : PsdH E := ((effect_iff E).mp hE).1
  have hSs : ((1 / 2 : ℚ) • (E + Eᴴ))ᴴ = (1 / 2 : ℚ) • (E + Eᴴ) := by
    rw [conjTranspose_rat_smul, conjTranspose_add, conjTranspose_conjTranspose, add_comm]
  have hSpsd : PsdH ((1 / 2 : ℚ) • (E + Eᴴ)) := by
    intro x
    have h := hEpsd x
    have e : hf ((1 / 2 : ℚ) • (E + Eᴴ)) x = hf E x := by
      rw [hf_smul, hf_add, hf_conjTranspose]
      ring
    rw [e]
    exact h
  have htr : (trace (ρ * E)).re = (trace (ρ * ((1 / 2 : ℚ) • (E + Eᴴ)))).re := by
    rw [Matrix.mul_smul, trace_smul, GaussRat.re_smul, Matrix.mul_add, trace_add, GaussRat.re_add,
      re_trace_mul_conjTranspose hρs]
    ring
  rw [htr]
  exact HermitianPsd.trace_mul_nonneg ρ _ hρ hSpsd hSs

/-- The Born valuation `E ↦ re trace (ρ * E)` of a Hermitian rational-PSD trace-one matrix. -/
def bornValuation (ρ : Matrix (Fin n) (Fin n) GaussRat) (hρs : ρᴴ = ρ) (hρ : PsdH ρ)
    (htr : (trace ρ).re = 1) : EffectValuation (space n) :=
  ofState ρ (fun _ hE => re_trace_mul_nonneg_of_effect hρs hρ hE) htr

theorem bornValuation_apply (ρ : Matrix (Fin n) (Fin n) GaussRat) (hρs : ρᴴ = ρ) (hρ : PsdH ρ)
    (htr : (trace ρ).re = 1) (E : Matrix (Fin n) (Fin n) GaussRat) :
    (bornValuation ρ hρs hρ htr).v E = (trace (ρ * E)).re := rfl

theorem bornValuation_density (ρ : Matrix (Fin n) (Fin n) GaussRat) (hρs : ρᴴ = ρ)
    (hρ : PsdH ρ) (htr : (trace ρ).re = 1) : density (bornValuation ρ hρs hρ htr) = ρ :=
  ofState_density _ _ _

/-- States and effect valuations over ℚ(i) correspond: every valuation is the Born valuation of
its density, and every Hermitian rational-PSD trace-one matrix is the density of its Born
valuation. -/
theorem state_valuation_correspondence :
    (∀ W : EffectValuation (space n),
      (density W)ᴴ = density W ∧ PsdH (density W) ∧ trace (density W) = 1 ∧
        ∀ E, (space n).Effect E → W.v E = (trace (density W * E)).re) ∧
    (∀ (ρ : Matrix (Fin n) (Fin n) GaussRat) (hρs : ρᴴ = ρ) (hρ : PsdH ρ)
        (htr : (trace ρ).re = 1), density (bornValuation ρ hρs hρ htr) = ρ) :=
  ⟨fun W => ⟨density_hermitian W, density_psd W, density_trace W, fun _ hE => density_effect W hE⟩,
    fun ρ hρs hρ htr => bornValuation_density ρ hρs hρ htr⟩

/-- The density of every effect valuation is a nonnegative rational combination of rank-one
Hermitian squares `w w*`. -/
theorem density_hasGram (W : EffectValuation (space n)) :
    HermitianPsd.HasGramH (density W) :=
  HermitianPsd.gram_of_psd (density W) (density_hermitian W) (density_psd W)

/-! ### Nonvacuity: the pure state `e₀` -/

theorem re_trace_single_zero_mul (E : Matrix (Fin (n + 1)) (Fin (n + 1)) GaussRat) :
    (trace (single (0 : Fin (n + 1)) 0 (1 : GaussRat) * E)).re = (E 0 0).re := by
  rw [trace_single_mul, one_smul]

theorem re_apply_zero_zero_eq_hf (E : Matrix (Fin (n + 1)) (Fin (n + 1)) GaussRat) :
    (E 0 0).re = hf E (Pi.single 0 1) := by
  simp [hf, single_dotProduct]

/-- The pure state `e₀` defines an effect valuation, so the hypotheses are satisfiable. -/
def pureZero : EffectValuation (space (n + 1)) :=
  ofState (single 0 0 1)
    (fun E hE => by
      rw [re_trace_single_zero_mul, re_apply_zero_zero_eq_hf E]
      exact ((effect_iff E).mp hE).1 _)
    (by rw [← mul_one (single (0 : Fin (n + 1)) 0 (1 : GaussRat)), re_trace_single_zero_mul,
      Matrix.one_apply_eq, GaussRat.re_one])

theorem pureZero_apply (E : Matrix (Fin (n + 1)) (Fin (n + 1)) GaussRat) :
    pureZero.v E = (E 0 0).re :=
  re_trace_single_zero_mul E

theorem pureZero_density : density (pureZero (n := n)) = single 0 0 1 :=
  ofState_density _ _ _

end BornFinite.HermitianCarrier

#print axioms BornFinite.HermitianCarrier.space_isOrderUnit
#print axioms BornFinite.HermitianCarrier.ext_effect
#print axioms BornFinite.HermitianCarrier.ext_one
#print axioms BornFinite.HermitianCarrier.ext_nonneg
#print axioms BornFinite.HermitianCarrier.ext_eq_re_trace
#print axioms BornFinite.HermitianCarrier.density_effect
#print axioms BornFinite.HermitianCarrier.density_re_trace
#print axioms BornFinite.HermitianCarrier.density_psd
#print axioms BornFinite.HermitianCarrier.ext_skew_zero
#print axioms BornFinite.HermitianCarrier.single_conjTranspose
#print axioms BornFinite.HermitianCarrier.single_neg_eq
#print axioms BornFinite.HermitianCarrier.skew_single_sub
#print axioms BornFinite.HermitianCarrier.skew_single_I_add
#print axioms BornFinite.HermitianCarrier.density_hermitian
#print axioms BornFinite.HermitianCarrier.density_trace
#print axioms BornFinite.HermitianCarrier.traceWith_apply
#print axioms BornFinite.HermitianCarrier.density_unique
#print axioms BornFinite.HermitianCarrier.born_representation
#print axioms BornFinite.HermitianCarrier.density_is_state
#print axioms BornFinite.HermitianCarrier.born_rule
#print axioms BornFinite.HermitianCarrier.ofState_density
#print axioms BornFinite.HermitianCarrier.re_trace_mul_nonneg_of_effect
#print axioms BornFinite.HermitianCarrier.bornValuation_apply
#print axioms BornFinite.HermitianCarrier.bornValuation_density
#print axioms BornFinite.HermitianCarrier.state_valuation_correspondence
#print axioms BornFinite.HermitianCarrier.density_hasGram
#print axioms BornFinite.HermitianCarrier.re_trace_single_zero_mul
#print axioms BornFinite.HermitianCarrier.re_apply_zero_zero_eq_hf
#print axioms BornFinite.HermitianCarrier.pureZero_apply
#print axioms BornFinite.HermitianCarrier.pureZero_density
