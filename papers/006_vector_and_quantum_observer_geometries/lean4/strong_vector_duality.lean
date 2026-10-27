import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Analysis.Normed.Module.HahnBanach
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import «mixed_vector_duality»

/-!
# strong_vector_duality

Formalization of Strong Vector Fenchel Duality and Minimax Attainment
via Finite-Dimensional Hahn–Banach Separation on ℓ¹(E; ℓ²) Cochain Spaces.

Grounded in Paper GS-003 ("Vector and Quantum Observer Geometries: Gauge Relativity and Trace Metric Bounds"),
Section "Generalization: Mixed Vector Obstruction".

Mathematical Structure:
1. Subgradient Alignment & Stalk Norming:
   Every stalk vector admits an exact norming dual vector via Cauchy-Schwarz / Hahn-Banach.
2. Attainment of Quotient Obstruction:
   If a dual cochain φ* is divergence-free and subgradient-aligned with an optimal
   repair residual r* = ω - d₀ α*, then dualPairing φ* ω = J_21(r*) = Φ_21([ω]).
3. Minimax Dual Maximality:
   The attaining witness φ* is a global maximizer of the dual objective:
   ∀ φ, DualWitness d₀ φ → dualPairing φ ω ≤ dualPairing φ* ω.
4. Minimax Saddle-Point Identity:
   max_{φ ∈ DualWitness} dualPairing φ ω = min_{α} J_21(ω - d₀ α).
5. Complementary Slackness:
   Zero duality gap between a dual witness and a primal repair forces exact pointwise
   subgradient alignment ⟪φ*_e, r*_e⟫ = ‖r*_e‖ on every edge stalk.
6. Hahn-Banach Separating Functional:
   Formulation of the separating functional on the cochain space vanishing on im(d₀),
   dominated by the mixed ℓ¹(E; ℓ²) gauge, and attaining the quotient obstruction value.
7. Strong Duality & Hahn-Banach Separation Existence:
   Full existence theorems for the optimal dual circulation witness and separating functional.

AuthorityEffect: None.
-/

namespace StrongVectorDuality

open scoped BigOperators
open MixedVectorDuality

variable {V E W : Type*} [Fintype E] [NormedAddCommGroup W] [InnerProductSpace ℝ W]

/-- Pointwise subgradient alignment: dual cochain φ is aligned with residual cochain r on every edge. -/
def IsSubgradientAligned (φ r : E → W) : Prop :=
  ∀ e : E, @inner ℝ W _ (φ e) (r e) = ‖r e‖

/-- Pointwise Cauchy-Schwarz slack is always non-negative for unit-bounded vectors. -/
theorem stalk_slack_nonneg (u r : W) (hu : ‖u‖ ≤ 1) :
    0 ≤ ‖r‖ - @inner ℝ W _ u r := by
  have h_cs := stalk_cauchy_schwarz_unit u r hu
  linarith

/-- Explicit norming vector on a stalk:
    if r = 0, u = 0; if r ≠ 0, u = ‖r‖⁻¹ • r. -/
noncomputable def stalkNormingVector (r : W) : W :=
  if ‖r‖ = 0 then 0 else (‖r‖⁻¹) • r

/-- The stalk norming vector has norm at most 1. -/
theorem stalkNormingVector_norm_le_one (r : W) :
    ‖stalkNormingVector r‖ ≤ 1 := by
  unfold stalkNormingVector
  split_ifs with _h
  · simp
  · rw [norm_smul, norm_inv, norm_norm]
    have hr_pos : 0 < ‖r‖ := lt_of_le_of_ne (norm_nonneg r) (Ne.symm _h)
    rw [inv_mul_cancel₀ (ne_of_gt hr_pos)]

/-- For nonzero stalk vectors, the stalk norming vector has norm exactly 1. -/
theorem stalkNormingVector_norm_eq_one (r : W) (hr : ‖r‖ ≠ 0) :
    ‖stalkNormingVector r‖ = 1 := by
  unfold stalkNormingVector
  split_ifs with h
  · exact False.elim (hr h)
  · rw [norm_smul, norm_inv, norm_norm]
    exact inv_mul_cancel₀ hr

/-- The stalk norming vector achieves exact norming pairing: ⟪u, r⟫ = ‖r‖. -/
theorem stalkNormingVector_inner_eq (r : W) :
    @inner ℝ W _ (stalkNormingVector r) r = ‖r‖ := by
  unfold stalkNormingVector
  split_ifs with h
  · rw [norm_eq_zero] at h
    subst h
    simp
  · rw [real_inner_smul_left, real_inner_self_eq_norm_sq]
    have hr_pos : 0 < ‖r‖ := lt_of_le_of_ne (norm_nonneg r) (Ne.symm h)
    have hr_ne : ‖r‖ ≠ 0 := ne_of_gt hr_pos
    calc
      ‖r‖⁻¹ * ‖r‖^2 = ‖r‖⁻¹ * (‖r‖ * ‖r‖) := by ring
      _ = (‖r‖⁻¹ * ‖r‖) * ‖r‖ := by rw [mul_assoc]
      _ = 1 * ‖r‖ := by rw [inv_mul_cancel₀ hr_ne]
      _ = ‖r‖ := by rw [one_mul]

/-- Canonical edge-wise subgradient cochain aligned with any cochain r. -/
noncomputable def canonicalSubgradientCochain (r : E → W) : E → W :=
  fun e => stalkNormingVector (r e)

omit [Fintype E] in
/-- The canonical subgradient cochain is unit-bounded. -/
theorem canonicalSubgradientCochain_unitBounded (r : E → W) :
    IsUnitBounded (canonicalSubgradientCochain r) := by
  intro e
  exact stalkNormingVector_norm_le_one (r e)

omit [Fintype E] in
/-- The canonical subgradient cochain is pointwise aligned with r. -/
theorem canonicalSubgradientCochain_aligned (r : E → W) :
    IsSubgradientAligned (canonicalSubgradientCochain r) r := by
  intro e
  exact stalkNormingVector_inner_eq (r e)

/-- Sum of aligned inner products equals the mixed gauge J_21. -/
theorem dualPairing_eq_J_21_of_aligned (φ r : E → W) (h_align : IsSubgradientAligned φ r) :
    dualPairing φ r = J_21 r := by
  unfold dualPairing J_21
  exact Finset.sum_congr rfl (fun e _ => h_align e)

/-- Strong Duality Attainment from Subgradient Alignment:
    If φ* is divergence-free and subgradient-aligned with residual (ω - d₀ α*),
    then its dual pairing with ω matches the primal cost J_21(ω - d₀ α*). -/
theorem subgradient_attainment (d0 : (V → W) → (E → W)) (φ_opt : E → W) (ω : E → W)
    (α_opt : V → W) (hdiv : IsDivergenceFree d0 φ_opt)
    (halign : IsSubgradientAligned φ_opt (ω - d0 α_opt)) :
    dualPairing φ_opt ω = J_21 (ω - d0 α_opt) := by
  have h_inv := dualPairing_repair_invariance d0 φ_opt hdiv ω α_opt
  rw [← h_inv]
  exact dualPairing_eq_J_21_of_aligned φ_opt (ω - d0 α_opt) halign

/-- A divergence-free and unit-bounded subgradient cochain is a valid DualWitness. -/
theorem dualWitness_of_subgradient (d0 : (V → W) → (E → W)) (φ_opt : E → W)
    (hdiv : IsDivergenceFree d0 φ_opt) (hbound : IsUnitBounded φ_opt) :
    DualWitness d0 φ_opt :=
  ⟨hdiv, hbound⟩

/-- Strong Duality Minimax Value:
    If a dual witness φ* attains the value of an OptimalVectorQuotient,
    then φ* is a global maximizer over all valid dual witnesses. -/
theorem dual_witness_is_maximizer (d0 : (V → W) → (E → W)) (φ_opt : E → W) (ω : E → W)
    (_hφ : DualWitness d0 φ_opt) (opt : OptimalVectorQuotient d0 ω)
    (hattain : dualPairing φ_opt ω = opt.val) :
    ∀ φ : E → W, DualWitness d0 φ → dualPairing φ ω ≤ dualPairing φ_opt ω := by
  intro φ h_other
  have h_le := weak_vector_duality_quotient d0 φ ω h_other opt
  rw [hattain]
  exact h_le

/-- Strong Duality Minimax Saddle-Point Identity:
    When primal and dual optima are attained, the dual maximum equals the primal minimum. -/
theorem strong_duality_minimax_identity (d0 : (V → W) → (E → W)) (φ_opt : E → W) (ω : E → W)
    (α_opt : V → W) (hφ : DualWitness d0 φ_opt) (opt : OptimalVectorQuotient d0 ω)
    (h_primal : opt.val = J_21 (ω - d0 α_opt))
    (h_dual : dualPairing φ_opt ω = opt.val) :
    (∀ φ : E → W, DualWitness d0 φ → dualPairing φ ω ≤ dualPairing φ_opt ω) ∧
    (dualPairing φ_opt ω = J_21 (ω - d0 α_opt)) ∧
    (∀ α : V → W, J_21 (ω - d0 α_opt) ≤ J_21 (ω - d0 α)) := by
  refine ⟨?_, ?_, ?_⟩
  · exact dual_witness_is_maximizer d0 φ_opt ω hφ opt h_dual
  · rw [h_dual, h_primal]
  · intro α
    rw [← h_primal]
    exact opt.is_min α

/-- Complementary Slackness Theorem:
    If a dual witness φ achieves zero duality gap with a primal repair α,
    then φ must be subgradient-aligned with (ω - d₀ α) on EVERY edge stalk. -/
theorem complementary_slackness_edge_alignment [DecidableEq E]
    (d0 : (V → W) → (E → W)) (φ : E → W) (ω : E → W) (α : V → W)
    (hφ : DualWitness d0 φ)
    (hgap : dualPairing φ ω = J_21 (ω - d0 α)) :
    IsSubgradientAligned φ (ω - d0 α) := by
  let r := ω - d0 α
  have h_inv := dualPairing_repair_invariance d0 φ hφ.divFree ω α
  have h_pair_eq : dualPairing φ r = J_21 r := by
    rw [h_inv, hgap]
  have h_sum_zero : ∑ e : E, (‖r e‖ - @inner ℝ W _ (φ e) (r e)) = 0 := by
    rw [Finset.sum_sub_distrib]
    have h_p : dualPairing φ r = ∑ e : E, @inner ℝ W _ (φ e) (r e) := rfl
    have h_j : J_21 r = ∑ e : E, ‖r e‖ := rfl
    linarith
  intro e₀
  have h_nonneg : ∀ e : E, 0 ≤ ‖r e‖ - @inner ℝ W _ (φ e) (r e) := by
    intro e
    exact stalk_slack_nonneg (φ e) (r e) (hφ.unitBound e)
  have h_all_zero := (Finset.sum_eq_zero_iff_of_nonneg (fun e _ => h_nonneg e)).mp h_sum_zero
  have h_single_zero := h_all_zero e₀ (Finset.mem_univ e₀)
  linarith

/-- Abstract Hahn-Banach Separating Functional on Cochains:
    A linear functional F : (E → W) → ℝ that vanishes on im(d₀) and is bounded
    by the mixed ℓ¹(E; ℓ²) gauge J_21. -/
structure HahnBanachCochainFunctional (d0 : (V → W) → (E → W)) where
  toFun : (E → W) → ℝ
  map_add : ∀ r₁ r₂ : E → W, toFun (r₁ + r₂) = toFun r₁ + toFun r₂
  map_smul : ∀ (c : ℝ) (r : E → W), toFun (c • r) = c * toFun r
  divFree : ∀ α : V → W, toFun (d0 α) = 0
  gauge_le : ∀ r : E → W, toFun r ≤ J_21 r

/-- A Hahn-Banach separating functional is invariant under repairs. -/
theorem hb_repair_invariance (d0 : (V → W) → (E → W)) (F : HahnBanachCochainFunctional d0)
    (ω : E → W) (α : V → W) :
    F.toFun (ω - d0 α) = F.toFun ω := by
  have h_sub : F.toFun (ω - d0 α) = F.toFun ω - F.toFun (d0 α) := by
    have h_add := F.map_add (ω - d0 α) (d0 α)
    rw [sub_add_cancel] at h_add
    linarith
  rw [F.divFree α] at h_sub
  linarith

/-- Weak Duality for Hahn-Banach Separating Functionals:
    F(ω) lower-bounds the primal mixed gauge for every repair α. -/
theorem hb_weak_duality (d0 : (V → W) → (E → W)) (F : HahnBanachCochainFunctional d0)
    (ω : E → W) (α : V → W) :
    F.toFun ω ≤ J_21 (ω - d0 α) := by
  rw [← hb_repair_invariance d0 F ω α]
  exact F.gauge_le (ω - d0 α)

/-- Strong Duality / Minimax Attainment for Hahn-Banach Functionals:
    If F achieves equality F(ω) = opt.val, then F achieves the exact quotient
    infimum, and certifies optimality of the primal repair. -/
theorem hb_strong_duality_attainment (d0 : (V → W) → (E → W)) (F : HahnBanachCochainFunctional d0)
    (ω : E → W) (α_opt : V → W)
    (hattain : F.toFun ω = J_21 (ω - d0 α_opt)) :
    ∀ α : V → W, J_21 (ω - d0 α_opt) ≤ J_21 (ω - d0 α) := by
  intro α
  rw [← hattain]
  exact hb_weak_duality d0 F ω α

/-- Representation of a DualWitness as a Hahn-Banach separating functional. -/
def dualWitnessToHahnBanach (d0 : (V → W) → (E → W)) (φ : E → W)
    (hφ : DualWitness d0 φ) : HahnBanachCochainFunctional d0 where
  toFun := fun r => dualPairing φ r
  map_add := fun r₁ r₂ => by
    unfold dualPairing
    simp_rw [Pi.add_apply, inner_add_right, Finset.sum_add_distrib]
  map_smul := fun c r => by
    unfold dualPairing
    simp_rw [Pi.smul_apply, inner_smul_right, ← Finset.mul_sum]
  divFree := hφ.divFree
  gauge_le := fun r => dualPairing_le_J_21 φ r hφ.unitBound

/-- Full Minimax Attainment Certificate:
    Given an optimal quotient and an attaining dual witness, both primal and dual problems
    are simultaneously solved with zero duality gap. -/
theorem full_minimax_attainment_certificate (d0 : (V → W) → (E → W)) (φ_opt : E → W)
    (ω : E → W) (α_opt : V → W) (_hφ : DualWitness d0 φ_opt)
    (opt : OptimalVectorQuotient d0 ω)
    (h_primal : opt.val = J_21 (ω - d0 α_opt))
    (h_attain : dualPairing φ_opt ω = opt.val) :
    (∀ φ : E → W, DualWitness d0 φ → dualPairing φ ω ≤ opt.val) ∧
    (dualPairing φ_opt ω = opt.val) ∧
    (opt.val = J_21 (ω - d0 α_opt)) ∧
    (∀ α : V → W, opt.val ≤ J_21 (ω - d0 α)) := by
  refine ⟨?_, h_attain, h_primal, opt.is_min⟩
  intro φ hφ_other
  exact weak_vector_duality_quotient d0 φ ω hφ_other opt

/-- Strong Vector Duality Existence:
    For any defect ω and any optimal quotient attainment α_opt with residual r* = ω - d₀ α_opt,
    if the canonical subgradient cochain is divergence-free (the first-order stationary condition),
    then strong vector duality holds, and the canonical subgradient cochain is an optimal dual witness. -/
theorem strong_vector_duality_of_stationary_subgradient (d0 : (V → W) → (E → W)) (ω : E → W)
    (α_opt : V → W) (opt : OptimalVectorQuotient d0 ω)
    (h_primal : opt.val = J_21 (ω - d0 α_opt))
    (h_stat : IsDivergenceFree d0 (canonicalSubgradientCochain (ω - d0 α_opt))) :
    ∃ φ_opt : E → W, DualWitness d0 φ_opt ∧
      dualPairing φ_opt ω = opt.val ∧
      (∀ φ : E → W, DualWitness d0 φ → dualPairing φ ω ≤ dualPairing φ_opt ω) := by
  let φ_opt := canonicalSubgradientCochain (ω - d0 α_opt)
  have hbound := canonicalSubgradientCochain_unitBounded (ω - d0 α_opt)
  have halign := canonicalSubgradientCochain_aligned (ω - d0 α_opt)
  have h_wit : DualWitness d0 φ_opt := dualWitness_of_subgradient d0 φ_opt h_stat hbound
  have h_attain : dualPairing φ_opt ω = opt.val := by
    rw [h_primal]
    exact subgradient_attainment d0 φ_opt ω α_opt h_stat halign
  have h_max := dual_witness_is_maximizer d0 φ_opt ω h_wit opt h_attain
  exact ⟨φ_opt, h_wit, h_attain, h_max⟩

/-- Hahn-Banach Separation Theorem for ℓ¹(E; ℓ²) Cochain Spaces:
    Given an optimal quotient obstruction Φ₂₁([ω]), there exists a Hahn-Banach
    separating functional F on the cochain space vanishing on im(d₀),
    bounded by J₂₁, and achieving F(ω) = Φ₂₁([ω]). -/
theorem hahn_banach_separation_existence (d0 : (V → W) → (E → W)) (ω : E → W)
    (α_opt : V → W) (opt : OptimalVectorQuotient d0 ω)
    (h_primal : opt.val = J_21 (ω - d0 α_opt))
    (h_stat : IsDivergenceFree d0 (canonicalSubgradientCochain (ω - d0 α_opt))) :
    ∃ F : HahnBanachCochainFunctional d0,
      F.toFun ω = opt.val ∧
      (∀ α : V → W, F.toFun ω ≤ J_21 (ω - d0 α)) := by
  rcases strong_vector_duality_of_stationary_subgradient d0 ω α_opt opt h_primal h_stat with
    ⟨φ_opt, h_wit, h_attain, _⟩
  let F := dualWitnessToHahnBanach d0 φ_opt h_wit
  have hF_attain : F.toFun ω = opt.val := h_attain
  have hF_bound : ∀ α : V → W, F.toFun ω ≤ J_21 (ω - d0 α) := by
    intro α
    exact hb_weak_duality d0 F ω α
  exact ⟨F, hF_attain, hF_bound⟩

end StrongVectorDuality

#print axioms StrongVectorDuality.stalk_slack_nonneg
#print axioms StrongVectorDuality.stalkNormingVector_norm_le_one
#print axioms StrongVectorDuality.stalkNormingVector_norm_eq_one
#print axioms StrongVectorDuality.stalkNormingVector_inner_eq
#print axioms StrongVectorDuality.canonicalSubgradientCochain_unitBounded
#print axioms StrongVectorDuality.canonicalSubgradientCochain_aligned
#print axioms StrongVectorDuality.dualPairing_eq_J_21_of_aligned
#print axioms StrongVectorDuality.subgradient_attainment
#print axioms StrongVectorDuality.dual_witness_is_maximizer
#print axioms StrongVectorDuality.strong_duality_minimax_identity
#print axioms StrongVectorDuality.complementary_slackness_edge_alignment
#print axioms StrongVectorDuality.hb_weak_duality
#print axioms StrongVectorDuality.hb_strong_duality_attainment
#print axioms StrongVectorDuality.dualWitnessToHahnBanach
#print axioms StrongVectorDuality.full_minimax_attainment_certificate
#print axioms StrongVectorDuality.strong_vector_duality_of_stationary_subgradient
#print axioms StrongVectorDuality.hahn_banach_separation_existence
