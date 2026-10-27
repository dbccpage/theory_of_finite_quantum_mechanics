import BornLinearExtension
import BornMatrixCarrier
import BornPsdDecomposition
import Mathlib.LinearAlgebra.Matrix.Symmetric

/-
Born representation of effect valuations on rational matrices.  AuthorityEffect: None.

Every effect-additive, positive, normalised valuation on the rational n×n matrices (effects taken
in the quadratic-form preorder with unit the identity) is `E ↦ trace (ρ * E)` for a unique matrix
`ρ`, and that `ρ` is symmetric, positive semidefinite on rational vectors, and has trace one.
Conversely any matrix positive on effects with trace one defines a valuation, and a concrete
valuation exists (the pure state `e₀`).  For a nonzero rational vector `x` the value on the
rank-one effect `P x` is `⟨x, ρ x⟩ / ⟨x, x⟩`.

Supplied structure: the rational matrix algebra and its order.  Derived structure: the trace
form of the valuation.  No continuity, no real scalars, no projection-lattice Gleason theorem;
the hypotheses are additivity on effects (not only on projections), positivity and normalisation.
-/

namespace BornFinite.MatrixCarrier

open Matrix

variable {n : ℕ}

theorem space_isOrderUnit : (space n).IsOrderUnit := fun A => order_unit A

/-- The ℚ-linear extension of an effect valuation on rational matrices. -/
noncomputable def ext (W : EffectValuation (space n)) : Matrix (Fin n) (Fin n) ℚ →ₗ[ℚ] ℚ :=
  (space n).extendₗ space_isOrderUnit W

theorem ext_effect (W : EffectValuation (space n)) {E : Matrix (Fin n) (Fin n) ℚ}
    (hE : (space n).Effect E) : ext W E = W.v E :=
  (space n).extendₗ_effect space_isOrderUnit W hE

theorem ext_one (W : EffectValuation (space n)) : ext W 1 = 1 :=
  (space n).extendₗ_u space_isOrderUnit W

theorem ext_nonneg (W : EffectValuation (space n)) {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : (space n).le 0 A) : 0 ≤ ext W A :=
  (space n).extendₗ_nonneg space_isOrderUnit W hA

/-- The matrix representing an effect valuation: `density W i j = ext W (single j i 1)`. -/
noncomputable def density (W : EffectValuation (space n)) : Matrix (Fin n) (Fin n) ℚ :=
  repMatrix (ext W)

theorem ext_eq_trace (W : EffectValuation (space n)) (A : Matrix (Fin n) (Fin n) ℚ) :
    ext W A = trace (density W * A) :=
  trace_rep (ext W) A

theorem density_effect (W : EffectValuation (space n)) {E : Matrix (Fin n) (Fin n) ℚ}
    (hE : (space n).Effect E) : W.v E = trace (density W * E) := by
  rw [← ext_eq_trace, ext_effect W hE]

theorem density_trace (W : EffectValuation (space n)) : trace (density W) = 1 := by
  have h := ext_eq_trace W 1
  rw [mul_one, ext_one] at h
  exact h.symm

theorem density_psd (W : EffectValuation (space n)) : PsdQ (density W) := by
  intro x
  by_cases hx : x = 0
  · subst hx
    simp [qf]
  · have hP := rankOne_effect hx
    have hpos := dot_self_pos hx
    rw [qf_eq_trace', ← ext_eq_trace]
    have e : vecMulVec x x = (x ⬝ᵥ x) • P x := by
      unfold P
      rw [smul_smul, mul_one_div_cancel hpos.ne', one_smul]
    rw [e, map_smul, smul_eq_mul, ext_effect W hP]
    exact mul_nonneg hpos.le (W.nonneg _ hP)

theorem single_transpose_eq (i j : Fin n) : (single i j (1 : ℚ))ᵀ = single j i 1 := by
  ext a b
  simp [Matrix.single, and_comm]

/-- The extension vanishes on skew matrices: they are both `≤ 0` and `≥ 0` in the preorder. -/
theorem ext_skew_zero (W : EffectValuation (space n)) {K : Matrix (Fin n) (Fin n) ℚ}
    (hK : Kᵀ = -K) : ext W K = 0 := by
  obtain ⟨h1, h2⟩ := skew_le_zero_and_ge hK
  have ha : 0 ≤ ext W K := ext_nonneg W h2
  have hb : 0 ≤ ext W (-K) := by
    apply ext_nonneg W
    have := (space n).neg_le_neg h1
    rwa [neg_zero] at this
  rw [map_neg] at hb
  linarith

theorem density_symm (W : EffectValuation (space n)) : (density W).IsSymm := by
  apply IsSymm.ext
  intro i j
  simp only [density, repMatrix_apply]
  have hK : (single i j (1 : ℚ) - single j i 1)ᵀ = -(single i j (1 : ℚ) - single j i 1) := by
    rw [transpose_sub, single_transpose_eq, single_transpose_eq]
    abel
  have := ext_skew_zero W hK
  rw [map_sub, sub_eq_zero] at this
  exact this

/-- The trace functional `A ↦ trace (ρ * A)` as a ℚ-linear map. -/
def traceWith (ρ : Matrix (Fin n) (Fin n) ℚ) : Matrix (Fin n) (Fin n) ℚ →ₗ[ℚ] ℚ where
  toFun A := trace (ρ * A)
  map_add' A B := by rw [Matrix.mul_add, trace_add]
  map_smul' c A := by rw [Matrix.mul_smul, trace_smul, RingHom.id_apply]

theorem traceWith_apply (ρ A : Matrix (Fin n) (Fin n) ℚ) : traceWith ρ A = trace (ρ * A) := rfl

theorem density_unique (W : EffectValuation (space n)) (ρ : Matrix (Fin n) (Fin n) ℚ)
    (h : ∀ E, (space n).Effect E → W.v E = trace (ρ * E)) : ρ = density W := by
  have hL : ∀ A, trace (ρ * A) = ext W A := by
    intro A
    have := (space n).extend_unique space_isOrderUnit W (traceWith ρ)
      (fun E hE => (h E hE).symm) A
    rw [← traceWith_apply, this]
    exact ((space n).extendₗ_apply space_isOrderUnit W A).symm
  apply rep_unique
  intro A
  rw [hL A, ext_eq_trace]

/-- Born representation: an effect valuation is the trace against a unique matrix. -/
theorem born_representation (W : EffectValuation (space n)) :
    ∃! ρ : Matrix (Fin n) (Fin n) ℚ, ∀ E, (space n).Effect E → W.v E = trace (ρ * E) :=
  ⟨density W, fun _ hE => density_effect W hE, fun ρ hρ => density_unique W ρ hρ⟩

/-- The representing matrix is a state: symmetric, positive semidefinite over ℚ, trace one. -/
theorem density_is_state (W : EffectValuation (space n)) :
    (density W).IsSymm ∧ PsdQ (density W) ∧ trace (density W) = 1 :=
  ⟨density_symm W, density_psd W, density_trace W⟩

/-- The Born rule for rank-one effects: `v (P x) = ⟨x, ρ x⟩ / ⟨x, x⟩`. -/
theorem born_rule (W : EffectValuation (space n)) {x : Fin n → ℚ} (hx : x ≠ 0) :
    W.v (P x) = qf (density W) x / (x ⬝ᵥ x) := by
  rw [density_effect W (rankOne_effect hx), qf_eq_trace']
  unfold P
  rw [Matrix.mul_smul, trace_smul, smul_eq_mul]
  ring

/-- The valuation `E ↦ trace (ρ * E)` of a matrix positive on effects with trace one. -/
def ofState (ρ : Matrix (Fin n) (Fin n) ℚ)
    (hpos : ∀ E, (space n).Effect E → 0 ≤ trace (ρ * E)) (htr : trace ρ = 1) :
    EffectValuation (space n) where
  v E := trace (ρ * E)
  unit := by
    show trace (ρ * 1) = 1
    rw [mul_one, htr]
  nonneg := hpos
  additive := fun a b _ _ _ => by rw [Matrix.mul_add, trace_add]

theorem ofState_density (ρ : Matrix (Fin n) (Fin n) ℚ)
    (hpos : ∀ E, (space n).Effect E → 0 ≤ trace (ρ * E)) (htr : trace ρ = 1) :
    density (ofState ρ hpos htr) = ρ :=
  (density_unique _ ρ (fun _ _ => rfl)).symm

theorem trace_single_zero_mul (E : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    trace (single (0 : Fin (n + 1)) 0 (1 : ℚ) * E) = E 0 0 := by
  rw [trace_single_mul, one_smul]

theorem apply_zero_zero_eq_qf (E : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    E 0 0 = qf E (Pi.single 0 1) := by
  simp [qf, single_dotProduct]

/-- The pure state `e₀` defines an effect valuation, so the hypotheses are satisfiable. -/
def pureZero : EffectValuation (space (n + 1)) :=
  ofState (single 0 0 1)
    (fun E hE => by
      rw [trace_single_zero_mul, apply_zero_zero_eq_qf E]
      exact ((effect_iff E).mp hE).1 _)
    (by rw [← mul_one (single (0 : Fin (n + 1)) 0 (1 : ℚ)), trace_single_zero_mul,
      Matrix.one_apply_eq])

theorem pureZero_apply (E : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) : pureZero.v E = E 0 0 :=
  trace_single_zero_mul E

theorem pureZero_density : density (pureZero (n := n)) = single 0 0 1 :=
  ofState_density _ _ _

/-! ### The converse for every state, via the rational Gram decomposition -/

theorem qf_transpose (E : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) : qf Eᵀ x = qf E x := by
  unfold qf
  rw [mulVec_transpose, dotProduct_comm, ← dotProduct_mulVec]

theorem trace_mul_transpose_of_symm {ρ : Matrix (Fin n) (Fin n) ℚ} (hρs : ρᵀ = ρ)
    (E : Matrix (Fin n) (Fin n) ℚ) : trace (ρ * Eᵀ) = trace (ρ * E) := by
  rw [← trace_transpose, transpose_mul, transpose_transpose, hρs, trace_mul_comm]

/-- Trace positivity of a symmetric rational-PSD matrix against any effect; the effect need not
be symmetric, since the trace against a symmetric `ρ` only sees its symmetric part. -/
theorem trace_mul_nonneg_of_effect {ρ : Matrix (Fin n) (Fin n) ℚ} (hρs : ρᵀ = ρ) (hρ : PsdQ ρ)
    {E : Matrix (Fin n) (Fin n) ℚ} (hE : (space n).Effect E) : 0 ≤ trace (ρ * E) := by
  have hEpsd : PsdQ E := ((effect_iff E).mp hE).1
  have hSs : ((1 / 2 : ℚ) • (E + Eᵀ))ᵀ = (1 / 2 : ℚ) • (E + Eᵀ) := by
    rw [transpose_smul, transpose_add, transpose_transpose, add_comm]
  have hSpsd : ∀ x, 0 ≤ x ⬝ᵥ (((1 / 2 : ℚ) • (E + Eᵀ)) *ᵥ x) := by
    intro x
    have h := hEpsd x
    have e : x ⬝ᵥ (((1 / 2 : ℚ) • (E + Eᵀ)) *ᵥ x) = qf E x := by
      rw [← qf, qf_smul, qf_add, qf_transpose]
      ring
    rw [e]
    exact h
  have htr : trace (ρ * E) = trace (ρ * ((1 / 2 : ℚ) • (E + Eᵀ))) := by
    rw [Matrix.mul_smul, trace_smul, Matrix.mul_add, trace_add, trace_mul_transpose_of_symm hρs,
      smul_eq_mul]
    ring
  rw [htr]
  exact PsdDecomposition.trace_mul_nonneg ρ _ hρ hSpsd hSs

/-- The Born valuation `E ↦ trace (ρ * E)` of a symmetric rational-PSD trace-one matrix. -/
def bornValuation (ρ : Matrix (Fin n) (Fin n) ℚ) (hρs : ρᵀ = ρ) (hρ : PsdQ ρ)
    (htr : trace ρ = 1) : EffectValuation (space n) :=
  ofState ρ (fun _ hE => trace_mul_nonneg_of_effect hρs hρ hE) htr

theorem bornValuation_apply (ρ : Matrix (Fin n) (Fin n) ℚ) (hρs : ρᵀ = ρ) (hρ : PsdQ ρ)
    (htr : trace ρ = 1) (E : Matrix (Fin n) (Fin n) ℚ) :
    (bornValuation ρ hρs hρ htr).v E = trace (ρ * E) := rfl

theorem bornValuation_density (ρ : Matrix (Fin n) (Fin n) ℚ) (hρs : ρᵀ = ρ) (hρ : PsdQ ρ)
    (htr : trace ρ = 1) : density (bornValuation ρ hρs hρ htr) = ρ :=
  ofState_density _ _ _

/-- States and effect valuations correspond: every valuation is the Born valuation of its density,
and every symmetric rational-PSD trace-one matrix is the density of its Born valuation. -/
theorem state_valuation_correspondence :
    (∀ W : EffectValuation (space n),
      (density W)ᵀ = density W ∧ PsdQ (density W) ∧ trace (density W) = 1 ∧
        ∀ E, (space n).Effect E → W.v E = trace (density W * E)) ∧
    (∀ (ρ : Matrix (Fin n) (Fin n) ℚ) (hρs : ρᵀ = ρ) (hρ : PsdQ ρ) (htr : trace ρ = 1),
      density (bornValuation ρ hρs hρ htr) = ρ) :=
  ⟨fun W => ⟨density_symm W, density_psd W, density_trace W, fun _ hE => density_effect W hE⟩,
    fun ρ hρs hρ htr => bornValuation_density ρ hρs hρ htr⟩

/-- The density of every effect valuation is a nonnegative rational combination of rank-one
squares `w wᵀ` (rational Gram form). -/
theorem density_hasGram (W : EffectValuation (space n)) :
    PsdDecomposition.HasGram (density W) :=
  PsdDecomposition.gram_of_psd (density W) (density_symm W) (density_psd W)

end BornFinite.MatrixCarrier

#print axioms BornFinite.MatrixCarrier.space_isOrderUnit
#print axioms BornFinite.MatrixCarrier.ext_effect
#print axioms BornFinite.MatrixCarrier.ext_one
#print axioms BornFinite.MatrixCarrier.ext_nonneg
#print axioms BornFinite.MatrixCarrier.ext_eq_trace
#print axioms BornFinite.MatrixCarrier.density_effect
#print axioms BornFinite.MatrixCarrier.density_trace
#print axioms BornFinite.MatrixCarrier.density_psd
#print axioms BornFinite.MatrixCarrier.single_transpose_eq
#print axioms BornFinite.MatrixCarrier.ext_skew_zero
#print axioms BornFinite.MatrixCarrier.density_symm
#print axioms BornFinite.MatrixCarrier.traceWith_apply
#print axioms BornFinite.MatrixCarrier.density_unique
#print axioms BornFinite.MatrixCarrier.born_representation
#print axioms BornFinite.MatrixCarrier.density_is_state
#print axioms BornFinite.MatrixCarrier.born_rule
#print axioms BornFinite.MatrixCarrier.ofState_density
#print axioms BornFinite.MatrixCarrier.trace_single_zero_mul
#print axioms BornFinite.MatrixCarrier.apply_zero_zero_eq_qf
#print axioms BornFinite.MatrixCarrier.pureZero_apply
#print axioms BornFinite.MatrixCarrier.pureZero_density
#print axioms BornFinite.MatrixCarrier.qf_transpose
#print axioms BornFinite.MatrixCarrier.trace_mul_transpose_of_symm
#print axioms BornFinite.MatrixCarrier.trace_mul_nonneg_of_effect
#print axioms BornFinite.MatrixCarrier.bornValuation_apply
#print axioms BornFinite.MatrixCarrier.bornValuation_density
#print axioms BornFinite.MatrixCarrier.state_valuation_correspondence
#print axioms BornFinite.MatrixCarrier.density_hasGram
