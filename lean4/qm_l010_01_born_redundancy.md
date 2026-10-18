import Mathlib.Tactic
import primitive_difference

/-!
Paper 010 / PL-010-1 kernels.

These lemmas mechanize the finite algebra used by the paper's redundancy
claims. They do not derive the Born rule, Hilbert space, unitary dynamics, or
measurement ontology. ENC-0317 remains conditional on imported representation
assumptions.
-/

open scoped BigOperators

namespace PaperQF002

noncomputable section

variable {Γ : Type*} [Fintype Γ]

def totalWeight (w : Γ → ℚ) : ℚ :=
  ∑ γ, w γ

def directProb (w : Γ → ℚ) (γ : Γ) : ℚ :=
  w γ / totalWeight w

theorem directProb_nonneg
    (w : Γ → ℚ) (hw : ∀ γ, 0 ≤ w γ) (hW : 0 < totalWeight w) (γ : Γ) :
    0 ≤ directProb w γ := by
  exact div_nonneg (hw γ) (le_of_lt hW)

theorem directProb_sum_eq_one
    (w : Γ → ℚ) (hW : totalWeight w ≠ 0) :
    ∑ γ, directProb w γ = 1 := by
  have hsum : (∑ γ, w γ) ≠ 0 := by
    simpa [totalWeight] using hW
  unfold directProb totalWeight
  rw [← Finset.sum_div]
  exact div_self hsum

theorem directProb_totalWeight_eq_one
    (w : Γ → ℚ) (hW : totalWeight w ≠ 0) :
    totalWeight (directProb w) = 1 := by
  simpa [totalWeight] using directProb_sum_eq_one w hW

theorem directProb_idempotent
    (w : Γ → ℚ) (hW : totalWeight w ≠ 0) (γ : Γ) :
    directProb (directProb w) γ = directProb w γ := by
  calc
    directProb (directProb w) γ =
        directProb w γ / totalWeight (directProb w) := rfl
    _ = directProb w γ / 1 := by
      rw [directProb_totalWeight_eq_one w hW]
    _ = directProb w γ := by ring

theorem totalWeight_const_mul (a : ℚ) (w : Γ → ℚ) :
    totalWeight (fun γ => a * w γ) = a * totalWeight w := by
  unfold totalWeight
  rw [Finset.mul_sum]

theorem directProb_scale_invariant
    {a : ℚ} (ha : a ≠ 0) (w : Γ → ℚ) (γ : Γ) :
    directProb (fun η => a * w η) γ = directProb w γ := by
  unfold directProb totalWeight
  change (a * w γ) / (∑ η, a * w η) = w γ / (∑ η, w η)
  rw [← Finset.mul_sum]
  field_simp [ha]

def scalarRayDifference (w v : Γ → ℚ) : (Γ → ℚ) × (Γ → ℚ) :=
  (w, v)

def scalarRayZero (p : (Γ → ℚ) × (Γ → ℚ)) : Prop :=
  ∃ a : ℚ, a ≠ 0 ∧ ∀ γ, p.2 γ = a * p.1 γ

def scalarRayPrimitiveDifference :
    OmegaCore.PrimitiveDifference (Γ → ℚ) ((Γ → ℚ) × (Γ → ℚ)) where
  δ := scalarRayDifference
  Zero := scalarRayZero
  zero_refl := by
    intro w
    exact ⟨1, one_ne_zero, by simp [scalarRayDifference]⟩
  zero_symm := by
    intro w v hwv
    rcases hwv with ⟨a, ha, hv⟩
    dsimp [scalarRayDifference] at hv
    refine ⟨a⁻¹, inv_ne_zero ha, ?_⟩
    intro γ
    calc
      w γ = a⁻¹ * (a * w γ) := by field_simp [ha]
      _ = a⁻¹ * v γ := by rw [hv γ]
  zero_trans := by
    intro u v w huv hvw
    rcases huv with ⟨a, ha, hv⟩
    rcases hvw with ⟨b, hb, hw⟩
    dsimp [scalarRayDifference] at hv hw
    refine ⟨b * a, mul_ne_zero hb ha, ?_⟩
    intro γ
    calc
      w γ = b * v γ := hw γ
      _ = b * (a * u γ) := by rw [hv γ]
      _ = (b * a) * u γ := by ring

theorem directProb_invariantCongruent_scalarRay :
    scalarRayPrimitiveDifference.InvariantCongruent
      (fun w : Γ → ℚ => directProb w) := by
  intro w v hwv
  rcases hwv with ⟨a, ha, hv⟩
  funext γ
  have hvfun : v = fun η => a * w η := by
    funext η
    exact hv η
  calc
    directProb w γ = directProb (fun η => a * w η) γ :=
      (directProb_scale_invariant (Γ := Γ) (a := a) ha w γ).symm
    _ = directProb v γ := by rw [hvfun]

theorem directProb_factor_exists_through_scalarRayQuotient :
    ∃ F : scalarRayPrimitiveDifference.ResidualQuotient → (Γ → ℚ),
      ∀ w : Γ → ℚ,
        F (scalarRayPrimitiveDifference.classOf w) = directProb w := by
  exact
    (OmegaCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      scalarRayPrimitiveDifference (fun w : Γ → ℚ => directProb w)).mpr
      directProb_invariantCongruent_scalarRay

theorem directProb_eq_iff_scalarRay_of_nonzero_total
    (w v : Γ → ℚ) (hW : totalWeight w ≠ 0) (hV : totalWeight v ≠ 0) :
    directProb w = directProb v ↔
      scalarRayPrimitiveDifference.ZeroRel w v := by
  constructor
  · intro h
    refine ⟨totalWeight v / totalWeight w, div_ne_zero hV hW, ?_⟩
    intro γ
    have hγ := congrFun h γ
    unfold directProb at hγ
    calc
      v γ = (v γ / totalWeight v) * totalWeight v := by
        field_simp [hV]
      _ = (w γ / totalWeight w) * totalWeight v := by
        rw [← hγ]
      _ = (totalWeight v / totalWeight w) * w γ := by
        field_simp [hW]
  · intro hrel
    exact directProb_invariantCongruent_scalarRay w v hrel

theorem directProb_eq_zero_iff
    (w : Γ → ℚ) (hW : totalWeight w ≠ 0) (γ : Γ) :
    directProb w γ = 0 ↔ w γ = 0 := by
  unfold directProb
  constructor
  · intro h
    field_simp [hW] at h
    simpa using h
  · intro h
    simp [h]

theorem directProb_pos_iff
    (w : Γ → ℚ) (hW : 0 < totalWeight w) (γ : Γ) :
    0 < directProb w γ ↔ 0 < w γ := by
  unfold directProb
  constructor
  · intro h
    have hmul : 0 < (w γ / totalWeight w) * totalWeight w := mul_pos h hW
    have hcancel : (w γ / totalWeight w) * totalWeight w = w γ := by
      field_simp [ne_of_gt hW]
    rwa [hcancel] at hmul
  · intro hw
    exact div_pos hw hW

theorem weight_le_totalWeight
    (w : Γ → ℚ) (hw : ∀ γ, 0 ≤ w γ) (γ : Γ) :
    w γ ≤ totalWeight w := by
  unfold totalWeight
  exact Finset.single_le_sum (fun η _hη => hw η) (Fintype.complete γ)

theorem directProb_le_one
    (w : Γ → ℚ) (hw : ∀ γ, 0 ≤ w γ) (hW : 0 < totalWeight w) (γ : Γ) :
    directProb w γ ≤ 1 := by
  unfold directProb
  have hle : w γ ≤ totalWeight w := weight_le_totalWeight w hw γ
  have hdiv :
      w γ / totalWeight w ≤ totalWeight w / totalWeight w :=
    div_le_div_of_nonneg_right hle (le_of_lt hW)
  simpa [div_self (ne_of_gt hW)] using hdiv

theorem directProb_le_iff
    (w : Γ → ℚ) (hW : 0 < totalWeight w) (γ η : Γ) :
    directProb w γ ≤ directProb w η ↔ w γ ≤ w η := by
  unfold directProb
  constructor
  · intro h
    calc
      w γ = (w γ / totalWeight w) * totalWeight w := by
        field_simp [ne_of_gt hW]
      _ ≤ (w η / totalWeight w) * totalWeight w :=
        mul_le_mul_of_nonneg_right h (le_of_lt hW)
      _ = w η := by
        field_simp [ne_of_gt hW]
  · intro h
    exact div_le_div_of_nonneg_right h (le_of_lt hW)

theorem directProb_lt_iff
    (w : Γ → ℚ) (hW : 0 < totalWeight w) (γ η : Γ) :
    directProb w γ < directProb w η ↔ w γ < w η := by
  unfold directProb
  constructor
  · intro h
    calc
      w γ = (w γ / totalWeight w) * totalWeight w := by
        field_simp [ne_of_gt hW]
      _ < (w η / totalWeight w) * totalWeight w :=
        mul_lt_mul_of_pos_right h hW
      _ = w η := by
        field_simp [ne_of_gt hW]
  · intro h
    exact div_lt_div_of_pos_right h hW

theorem directProb_eq_iff
    (w : Γ → ℚ) (hW : 0 < totalWeight w) (γ η : Γ) :
    directProb w γ = directProb w η ↔ w γ = w η := by
  constructor
  · intro h
    have hle : w γ ≤ w η :=
      (directProb_le_iff w hW γ η).mp (le_of_eq h)
    have hge : w η ≤ w γ :=
      (directProb_le_iff w hW η γ).mp (le_of_eq h.symm)
    exact le_antisymm hle hge
  · intro h
    simp [directProb, h]

theorem directNormalization_certificate
    (w : Γ → ℚ) (hw : ∀ γ, 0 ≤ w γ) (hW : 0 < totalWeight w) :
    (∀ γ, 0 ≤ directProb w γ) ∧ ∑ γ, directProb w γ = 1 := by
  exact ⟨directProb_nonneg w hw hW, directProb_sum_eq_one w (ne_of_gt hW)⟩

theorem directNormalization_unit_interval_certificate
    (w : Γ → ℚ) (hw : ∀ γ, 0 ≤ w γ) (hW : 0 < totalWeight w) :
    (∀ γ, 0 ≤ directProb w γ ∧ directProb w γ ≤ 1) ∧
      ∑ γ, directProb w γ = 1 := by
  exact ⟨fun γ => ⟨directProb_nonneg w hw hW γ,
      directProb_le_one w hw hW γ⟩,
    directProb_sum_eq_one w (ne_of_gt hW)⟩

def bornProbFromNormSq (normSq : Γ → ℚ) (γ : Γ) : ℚ :=
  normSq γ / ∑ η, normSq η

theorem bornProbFromNormSq_eq_directProb (normSq : Γ → ℚ) (γ : Γ) :
    bornProbFromNormSq normSq γ = directProb normSq γ := by
  simp [bornProbFromNormSq, directProb, totalWeight]

theorem bornProbFromNormSq_nonneg
    (normSq : Γ → ℚ) (hnormSq : ∀ γ, 0 ≤ normSq γ)
    (hT : 0 < totalWeight normSq) (γ : Γ) :
    0 ≤ bornProbFromNormSq normSq γ := by
  rw [bornProbFromNormSq_eq_directProb]
  exact directProb_nonneg normSq hnormSq hT γ

theorem bornProbFromNormSq_sum_eq_one
    (normSq : Γ → ℚ) (hT : totalWeight normSq ≠ 0) :
    ∑ γ, bornProbFromNormSq normSq γ = 1 := by
  simpa [bornProbFromNormSq_eq_directProb] using directProb_sum_eq_one normSq hT

theorem bornProbFromNormSq_totalWeight_eq_one
    (normSq : Γ → ℚ) (hT : totalWeight normSq ≠ 0) :
    totalWeight (bornProbFromNormSq normSq) = 1 := by
  simpa [totalWeight] using bornProbFromNormSq_sum_eq_one normSq hT

theorem bornProbFromNormSq_idempotent
    (normSq : Γ → ℚ) (hT : totalWeight normSq ≠ 0) (γ : Γ) :
    bornProbFromNormSq (bornProbFromNormSq normSq) γ =
      bornProbFromNormSq normSq γ := by
  calc
    bornProbFromNormSq (bornProbFromNormSq normSq) γ =
        directProb (bornProbFromNormSq normSq) γ := by
          rw [bornProbFromNormSq_eq_directProb]
    _ = directProb (directProb normSq) γ := by
      have hfun : bornProbFromNormSq normSq = directProb normSq := by
        funext η
        exact bornProbFromNormSq_eq_directProb normSq η
      rw [hfun]
    _ = directProb normSq γ := directProb_idempotent normSq hT γ
    _ = bornProbFromNormSq normSq γ :=
      (bornProbFromNormSq_eq_directProb normSq γ).symm

theorem bornProbFromNormSq_eq_zero_iff
    (normSq : Γ → ℚ) (hT : totalWeight normSq ≠ 0) (γ : Γ) :
    bornProbFromNormSq normSq γ = 0 ↔ normSq γ = 0 := by
  rw [bornProbFromNormSq_eq_directProb]
  exact directProb_eq_zero_iff normSq hT γ

theorem bornProbFromNormSq_pos_iff
    (normSq : Γ → ℚ) (hT : 0 < totalWeight normSq) (γ : Γ) :
    0 < bornProbFromNormSq normSq γ ↔ 0 < normSq γ := by
  rw [bornProbFromNormSq_eq_directProb]
  exact directProb_pos_iff normSq hT γ

theorem bornProbFromNormSq_le_one
    (normSq : Γ → ℚ) (hnormSq : ∀ γ, 0 ≤ normSq γ)
    (hT : 0 < totalWeight normSq) (γ : Γ) :
    bornProbFromNormSq normSq γ ≤ 1 := by
  rw [bornProbFromNormSq_eq_directProb]
  exact directProb_le_one normSq hnormSq hT γ

theorem bornProbFromNormSq_le_iff
    (normSq : Γ → ℚ) (hT : 0 < totalWeight normSq) (γ η : Γ) :
    bornProbFromNormSq normSq γ ≤ bornProbFromNormSq normSq η ↔
      normSq γ ≤ normSq η := by
  rw [bornProbFromNormSq_eq_directProb, bornProbFromNormSq_eq_directProb]
  exact directProb_le_iff normSq hT γ η

theorem bornProbFromNormSq_lt_iff
    (normSq : Γ → ℚ) (hT : 0 < totalWeight normSq) (γ η : Γ) :
    bornProbFromNormSq normSq γ < bornProbFromNormSq normSq η ↔
      normSq γ < normSq η := by
  rw [bornProbFromNormSq_eq_directProb, bornProbFromNormSq_eq_directProb]
  exact directProb_lt_iff normSq hT γ η

theorem bornProbFromNormSq_eq_iff
    (normSq : Γ → ℚ) (hT : 0 < totalWeight normSq) (γ η : Γ) :
    bornProbFromNormSq normSq γ = bornProbFromNormSq normSq η ↔
      normSq γ = normSq η := by
  rw [bornProbFromNormSq_eq_directProb, bornProbFromNormSq_eq_directProb]
  exact directProb_eq_iff normSq hT γ η

theorem bornProbFromNormSq_probability_certificate
    (normSq : Γ → ℚ) (hnormSq : ∀ γ, 0 ≤ normSq γ)
    (hT : 0 < totalWeight normSq) :
    (∀ γ, 0 ≤ bornProbFromNormSq normSq γ) ∧
      ∑ γ, bornProbFromNormSq normSq γ = 1 := by
  exact ⟨bornProbFromNormSq_nonneg normSq hnormSq hT,
    bornProbFromNormSq_sum_eq_one normSq (ne_of_gt hT)⟩

theorem bornProbFromNormSq_unit_interval_certificate
    (normSq : Γ → ℚ) (hnormSq : ∀ γ, 0 ≤ normSq γ)
    (hT : 0 < totalWeight normSq) :
    (∀ γ, 0 ≤ bornProbFromNormSq normSq γ ∧
      bornProbFromNormSq normSq γ ≤ 1) ∧
      ∑ γ, bornProbFromNormSq normSq γ = 1 := by
  exact ⟨fun γ => ⟨bornProbFromNormSq_nonneg normSq hnormSq hT γ,
      bornProbFromNormSq_le_one normSq hnormSq hT γ⟩,
    bornProbFromNormSq_sum_eq_one normSq (ne_of_gt hT)⟩

theorem bornProbFromNormSq_pos_scale_invariant
    {a : ℚ} (ha : 0 < a) (normSq : Γ → ℚ) (γ : Γ) :
    bornProbFromNormSq (fun η => a * normSq η) γ =
      bornProbFromNormSq normSq γ := by
  unfold bornProbFromNormSq
  change (a * normSq γ) / (∑ η, a * normSq η) =
    normSq γ / (∑ η, normSq η)
  rw [← Finset.mul_sum]
  field_simp [ne_of_gt ha]

theorem bornProbFromNormSq_invariantCongruent_scalarRay :
    scalarRayPrimitiveDifference.InvariantCongruent
      (fun normSq : Γ → ℚ => bornProbFromNormSq normSq) := by
  intro normSq normSq' hrel
  have hdirect := directProb_invariantCongruent_scalarRay normSq normSq' hrel
  funext γ
  calc
    bornProbFromNormSq normSq γ = directProb normSq γ :=
      bornProbFromNormSq_eq_directProb normSq γ
    _ = directProb normSq' γ := congrFun hdirect γ
    _ = bornProbFromNormSq normSq' γ :=
      (bornProbFromNormSq_eq_directProb normSq' γ).symm

theorem bornProbFromNormSq_factor_exists_through_scalarRayQuotient :
    ∃ F : scalarRayPrimitiveDifference.ResidualQuotient → (Γ → ℚ),
      ∀ normSq : Γ → ℚ,
        F (scalarRayPrimitiveDifference.classOf normSq) =
          bornProbFromNormSq normSq := by
  exact
    (OmegaCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      scalarRayPrimitiveDifference
      (fun normSq : Γ → ℚ => bornProbFromNormSq normSq)).mpr
      bornProbFromNormSq_invariantCongruent_scalarRay

theorem bornProbFromNormSq_eq_iff_scalarRay_of_nonzero_total
    (normSq normSq' : Γ → ℚ)
    (hT : totalWeight normSq ≠ 0) (hT' : totalWeight normSq' ≠ 0) :
    bornProbFromNormSq normSq = bornProbFromNormSq normSq' ↔
      scalarRayPrimitiveDifference.ZeroRel normSq normSq' := by
  constructor
  · intro h
    have hdirect : directProb normSq = directProb normSq' := by
      funext γ
      calc
        directProb normSq γ = bornProbFromNormSq normSq γ :=
          (bornProbFromNormSq_eq_directProb normSq γ).symm
        _ = bornProbFromNormSq normSq' γ := congrFun h γ
        _ = directProb normSq' γ :=
          bornProbFromNormSq_eq_directProb normSq' γ
    exact
      (directProb_eq_iff_scalarRay_of_nonzero_total normSq normSq' hT hT').mp
        hdirect
  · intro hrel
    exact bornProbFromNormSq_invariantCongruent_scalarRay normSq normSq' hrel

theorem bornNormalization_redundant_of_normSq_eq_weight
    (w normSq : Γ → ℚ) (h : ∀ γ, normSq γ = w γ) (γ : Γ) :
    bornProbFromNormSq normSq γ = directProb w γ := by
  simp [bornProbFromNormSq, directProb, totalWeight, h]

theorem bornNormalization_redundant_certificate
    (w normSq : Γ → ℚ) (h : ∀ γ, normSq γ = w γ)
    (hw : ∀ γ, 0 ≤ w γ) (hW : 0 < totalWeight w) :
    (∀ γ, 0 ≤ bornProbFromNormSq normSq γ) ∧
      (∑ γ, bornProbFromNormSq normSq γ = 1) ∧
        (∀ γ, bornProbFromNormSq normSq γ = directProb w γ) := by
  have heq : ∀ γ, bornProbFromNormSq normSq γ = directProb w γ :=
    bornNormalization_redundant_of_normSq_eq_weight w normSq h
  refine ⟨?_, ?_, heq⟩
  · intro γ
    rw [heq γ]
    exact directProb_nonneg w hw hW γ
  · calc
      ∑ γ, bornProbFromNormSq normSq γ = ∑ γ, directProb w γ := by
        apply Finset.sum_congr rfl
        intro γ _hγ
        exact heq γ
      _ = 1 := directProb_sum_eq_one w (ne_of_gt hW)

theorem bornNormalization_redundant_support_certificate
    (w normSq : Γ → ℚ) (h : ∀ γ, normSq γ = w γ)
    (hW : 0 < totalWeight w) (γ : Γ) :
    (bornProbFromNormSq normSq γ = 0 ↔ w γ = 0) ∧
      (0 < bornProbFromNormSq normSq γ ↔ 0 < w γ) := by
  rw [bornNormalization_redundant_of_normSq_eq_weight w normSq h]
  exact ⟨directProb_eq_zero_iff w (ne_of_gt hW) γ,
    directProb_pos_iff w hW γ⟩

theorem bornNormalization_redundant_order_certificate
    (w normSq : Γ → ℚ) (h : ∀ γ, normSq γ = w γ)
    (hW : 0 < totalWeight w) (γ η : Γ) :
    (bornProbFromNormSq normSq γ ≤ bornProbFromNormSq normSq η ↔
        w γ ≤ w η) ∧
      (bornProbFromNormSq normSq γ < bornProbFromNormSq normSq η ↔
        w γ < w η) ∧
        (bornProbFromNormSq normSq γ = bornProbFromNormSq normSq η ↔
          w γ = w η) := by
  rw [bornNormalization_redundant_of_normSq_eq_weight w normSq h γ,
    bornNormalization_redundant_of_normSq_eq_weight w normSq h η]
  exact ⟨directProb_le_iff w hW γ η,
    directProb_lt_iff w hW γ η,
    directProb_eq_iff w hW γ η⟩

def l1Norm (x : Γ → ℚ) : ℚ :=
  ∑ γ, |x γ|

theorem l1Norm_nonneg (x : Γ → ℚ) :
    0 ≤ l1Norm x := by
  unfold l1Norm
  exact Finset.sum_nonneg (fun γ _hγ => abs_nonneg (x γ))

theorem l1Norm_eq_zero_iff (x : Γ → ℚ) :
    l1Norm x = 0 ↔ ∀ γ, x γ = 0 := by
  unfold l1Norm
  constructor
  · intro h γ
    have habs : |x γ| = 0 :=
      (Finset.sum_eq_zero_iff_of_nonneg
        (fun η _hη => abs_nonneg (x η))).mp h γ (Fintype.complete γ)
    exact abs_eq_zero.mp habs
  · intro h
    simp [h]

theorem l1Norm_pos_iff_exists_ne_zero (x : Γ → ℚ) :
    0 < l1Norm x ↔ ∃ γ, x γ ≠ 0 := by
  constructor
  · intro h
    by_contra hnone
    push Not at hnone
    have hzero : l1Norm x = 0 := (l1Norm_eq_zero_iff x).mpr hnone
    linarith
  · intro h
    rcases h with ⟨γ, hγ⟩
    by_contra hnotpos
    have hle : l1Norm x ≤ 0 := le_of_not_gt hnotpos
    have hzero : l1Norm x = 0 := le_antisymm hle (l1Norm_nonneg x)
    exact hγ ((l1Norm_eq_zero_iff x).mp hzero γ)

theorem l1Norm_triangle (x y : Γ → ℚ) :
    l1Norm (fun γ => x γ + y γ) ≤ l1Norm x + l1Norm y := by
  unfold l1Norm
  calc
    (∑ γ, |x γ + y γ|) ≤ ∑ γ, (|x γ| + |y γ|) := by
      exact Finset.sum_le_sum (fun γ _hγ => abs_add_le (x γ) (y γ))
    _ = (∑ γ, |x γ|) + (∑ γ, |y γ|) := by
      rw [Finset.sum_add_distrib]

def l1AdditivityDefect (x y : Γ → ℚ) : ℚ :=
  l1Norm x + l1Norm y - l1Norm (fun γ => x γ + y γ)

def l1CoordinateAdditivityDefect (x y : Γ → ℚ) (γ : Γ) : ℚ :=
  |x γ| + |y γ| - |x γ + y γ|

omit [Fintype Γ] in
theorem l1CoordinateAdditivityDefect_nonneg
    (x y : Γ → ℚ) (γ : Γ) :
    0 ≤ l1CoordinateAdditivityDefect x y γ := by
  unfold l1CoordinateAdditivityDefect
  have htri : |x γ + y γ| ≤ |x γ| + |y γ| := abs_add_le (x γ) (y γ)
  linarith

omit [Fintype Γ] in
theorem l1CoordinateAdditivityDefect_eq_zero_iff_mul_nonneg
    (x y : Γ → ℚ) (γ : Γ) :
    l1CoordinateAdditivityDefect x y γ = 0 ↔ 0 ≤ x γ * y γ := by
  let a : ℚ := x γ
  let b : ℚ := y γ
  change |a| + |b| - |a + b| = 0 ↔ 0 ≤ a * b
  constructor
  · intro h
    have habs : |a + b| = |a| + |b| := by linarith
    by_contra hnot
    have hprod : a * b < 0 := lt_of_not_ge hnot
    by_cases ha : 0 ≤ a
    · have hbneg : b < 0 := by
        by_contra hbnot
        have hb : 0 ≤ b := le_of_not_gt hbnot
        have hnonneg : 0 ≤ a * b := mul_nonneg ha hb
        linarith
      have hapos : 0 < a := by
        by_contra hanot
        have haz : a = 0 := le_antisymm (le_of_not_gt hanot) ha
        rw [haz] at hprod
        norm_num at hprod
      by_cases hsum : 0 ≤ a + b
      · have hsum_abs : |a + b| = a + b := abs_of_nonneg hsum
        have ha_abs : |a| = a := abs_of_nonneg ha
        have hb_abs : |b| = -b := abs_of_nonpos (le_of_lt hbneg)
        rw [hsum_abs, ha_abs, hb_abs] at habs
        linarith
      · have hsum_nonpos : a + b ≤ 0 := le_of_not_ge hsum
        have hsum_abs : |a + b| = -(a + b) := abs_of_nonpos hsum_nonpos
        have ha_abs : |a| = a := abs_of_nonneg ha
        have hb_abs : |b| = -b := abs_of_nonpos (le_of_lt hbneg)
        rw [hsum_abs, ha_abs, hb_abs] at habs
        linarith
    · have haneg : a < 0 := lt_of_not_ge ha
      have hbpos : 0 < b := by
        by_contra hbnot
        have hb : b ≤ 0 := le_of_not_gt hbnot
        have hnonneg : 0 ≤ a * b :=
          mul_nonneg_of_nonpos_of_nonpos (le_of_lt haneg) hb
        linarith
      by_cases hsum : 0 ≤ a + b
      · have hsum_abs : |a + b| = a + b := abs_of_nonneg hsum
        have ha_abs : |a| = -a := abs_of_nonpos (le_of_lt haneg)
        have hb_abs : |b| = b := abs_of_nonneg (le_of_lt hbpos)
        rw [hsum_abs, ha_abs, hb_abs] at habs
        linarith
      · have hsum_nonpos : a + b ≤ 0 := le_of_not_ge hsum
        have hsum_abs : |a + b| = -(a + b) := abs_of_nonpos hsum_nonpos
        have ha_abs : |a| = -a := abs_of_nonpos (le_of_lt haneg)
        have hb_abs : |b| = b := abs_of_nonneg (le_of_lt hbpos)
        rw [hsum_abs, ha_abs, hb_abs] at habs
        linarith
  · intro hprod
    have hcases := (mul_nonneg_iff.mp hprod)
    rcases hcases with ⟨ha, hb⟩ | ⟨ha, hb⟩
    · have hsum : 0 ≤ a + b := add_nonneg ha hb
      rw [abs_of_nonneg ha, abs_of_nonneg hb, abs_of_nonneg hsum]
      ring
    · have hsum : a + b ≤ 0 := add_nonpos ha hb
      rw [abs_of_nonpos ha, abs_of_nonpos hb, abs_of_nonpos hsum]
      ring

theorem l1AdditivityDefect_eq_sum_coordinateDefects
    (x y : Γ → ℚ) :
    l1AdditivityDefect x y =
      ∑ γ, l1CoordinateAdditivityDefect x y γ := by
  unfold l1AdditivityDefect l1CoordinateAdditivityDefect l1Norm
  rw [Finset.sum_sub_distrib, Finset.sum_add_distrib]

theorem l1AdditivityDefect_nonneg (x y : Γ → ℚ) :
    0 ≤ l1AdditivityDefect x y := by
  rw [l1AdditivityDefect_eq_sum_coordinateDefects]
  exact Finset.sum_nonneg
    (fun γ _hγ => l1CoordinateAdditivityDefect_nonneg x y γ)

theorem l1AdditivityDefect_eq_zero_iff_additive (x y : Γ → ℚ) :
    l1AdditivityDefect x y = 0 ↔
      l1Norm (fun γ => x γ + y γ) = l1Norm x + l1Norm y := by
  unfold l1AdditivityDefect
  constructor <;> intro h <;> linarith

theorem l1AdditivityDefect_eq_zero_iff_all_coordinateDefects_zero
    (x y : Γ → ℚ) :
    l1AdditivityDefect x y = 0 ↔
      ∀ γ, l1CoordinateAdditivityDefect x y γ = 0 := by
  rw [l1AdditivityDefect_eq_sum_coordinateDefects]
  constructor
  · intro h γ
    have hall :=
      (Finset.sum_eq_zero_iff_of_nonneg
        (s := Finset.univ)
        (f := fun γ => l1CoordinateAdditivityDefect x y γ)
        (fun γ _hγ => l1CoordinateAdditivityDefect_nonneg x y γ)).mp h
    exact hall γ (Fintype.complete γ)
  · intro h
    exact Finset.sum_eq_zero (fun γ _hγ => h γ)

theorem l1AdditivityDefect_eq_zero_iff_pointwise_mul_nonneg
    (x y : Γ → ℚ) :
    l1AdditivityDefect x y = 0 ↔ ∀ γ, 0 ≤ x γ * y γ := by
  rw [l1AdditivityDefect_eq_zero_iff_all_coordinateDefects_zero]
  constructor
  · intro h γ
    exact (l1CoordinateAdditivityDefect_eq_zero_iff_mul_nonneg x y γ).mp (h γ)
  · intro h γ
    exact (l1CoordinateAdditivityDefect_eq_zero_iff_mul_nonneg x y γ).mpr (h γ)

theorem l1Norm_add_iff_pointwise_mul_nonneg
    (x y : Γ → ℚ) :
    l1Norm (fun γ => x γ + y γ) = l1Norm x + l1Norm y ↔
      ∀ γ, 0 ≤ x γ * y γ := by
  constructor
  · intro hadd
    exact (l1AdditivityDefect_eq_zero_iff_pointwise_mul_nonneg x y).mp
      ((l1AdditivityDefect_eq_zero_iff_additive x y).mpr hadd)
  · intro hcompat
    exact (l1AdditivityDefect_eq_zero_iff_additive x y).mp
      ((l1AdditivityDefect_eq_zero_iff_pointwise_mul_nonneg x y).mpr hcompat)

omit [Fintype Γ] in
theorem l1CoordinateAdditivityDefect_pos_iff_mul_neg
    (x y : Γ → ℚ) (γ : Γ) :
    0 < l1CoordinateAdditivityDefect x y γ ↔ x γ * y γ < 0 := by
  constructor
  · intro hpos
    by_contra hnot
    have hnonneg : 0 ≤ x γ * y γ := le_of_not_gt hnot
    have hzero :
        l1CoordinateAdditivityDefect x y γ = 0 :=
      (l1CoordinateAdditivityDefect_eq_zero_iff_mul_nonneg x y γ).mpr hnonneg
    exact (ne_of_gt hpos) hzero
  · intro hneg
    have hnonneg : 0 ≤ l1CoordinateAdditivityDefect x y γ :=
      l1CoordinateAdditivityDefect_nonneg x y γ
    by_contra hnot
    have hle : l1CoordinateAdditivityDefect x y γ ≤ 0 := le_of_not_gt hnot
    have hzero : l1CoordinateAdditivityDefect x y γ = 0 :=
      le_antisymm hle hnonneg
    have hprod_nonneg : 0 ≤ x γ * y γ :=
      (l1CoordinateAdditivityDefect_eq_zero_iff_mul_nonneg x y γ).mp hzero
    linarith

theorem l1AdditivityDefect_pos_iff_exists_mul_neg
    (x y : Γ → ℚ) :
    0 < l1AdditivityDefect x y ↔ ∃ γ, x γ * y γ < 0 := by
  constructor
  · intro hpos
    by_contra hnone
    push Not at hnone
    have hcompat : ∀ γ, 0 ≤ x γ * y γ := by
      intro γ
      exact hnone γ
    have hzero : l1AdditivityDefect x y = 0 :=
      (l1AdditivityDefect_eq_zero_iff_pointwise_mul_nonneg x y).mpr hcompat
    exact (ne_of_gt hpos) hzero
  · intro h
    rcases h with ⟨γ, hγ⟩
    have hnonneg : 0 ≤ l1AdditivityDefect x y :=
      l1AdditivityDefect_nonneg x y
    have hne : l1AdditivityDefect x y ≠ 0 := by
      intro hzero
      have hcompat : ∀ η, 0 ≤ x η * y η :=
        (l1AdditivityDefect_eq_zero_iff_pointwise_mul_nonneg x y).mp hzero
      linarith [hcompat γ]
    exact lt_of_le_of_ne hnonneg (Ne.symm hne)

def disjointSupport (x y : Γ → ℚ) : Prop :=
  ∀ γ, x γ = 0 ∨ y γ = 0

def lpPowerSum (p : ℕ) (x : Γ → ℚ) : ℚ :=
  ∑ γ, |x γ| ^ p

theorem lpPowerSum_nonneg (p : ℕ) (x : Γ → ℚ) :
    0 ≤ lpPowerSum p x := by
  unfold lpPowerSum
  exact Finset.sum_nonneg (fun γ _hγ => pow_nonneg (abs_nonneg (x γ)) p)

theorem lpPowerSum_pos_of_exists_ne_zero
    (p : ℕ) (x : Γ → ℚ) (h : ∃ γ, x γ ≠ 0) :
    0 < lpPowerSum p x := by
  rcases h with ⟨γ, hγ⟩
  unfold lpPowerSum
  have hterm : 0 < |x γ| ^ p := pow_pos (abs_pos.mpr hγ) p
  have hle : |x γ| ^ p ≤ ∑ η, |x η| ^ p := by
    exact Finset.single_le_sum
      (fun η _hη => pow_nonneg (abs_nonneg (x η)) p)
      (Fintype.complete γ)
  exact lt_of_lt_of_le hterm hle

theorem lpPowerSum_eq_zero_iff
    {p : ℕ} (hp : p ≠ 0) (x : Γ → ℚ) :
    lpPowerSum p x = 0 ↔ ∀ γ, x γ = 0 := by
  unfold lpPowerSum
  constructor
  · intro h γ
    have hterm : |x γ| ^ p = 0 :=
      (Finset.sum_eq_zero_iff_of_nonneg
        (fun η _hη => pow_nonneg (abs_nonneg (x η)) p)).mp h γ
        (Fintype.complete γ)
    by_contra hγ
    have hpos : 0 < |x γ| ^ p := pow_pos (abs_pos.mpr hγ) p
    linarith
  · intro h
    simp [h, hp]

theorem lpPowerSum_pos_iff_exists_ne_zero
    {p : ℕ} (hp : p ≠ 0) (x : Γ → ℚ) :
    0 < lpPowerSum p x ↔ ∃ γ, x γ ≠ 0 := by
  constructor
  · intro h
    by_contra hnone
    push Not at hnone
    have hzero : lpPowerSum p x = 0 :=
      (lpPowerSum_eq_zero_iff hp x).mpr hnone
    linarith
  · intro h
    exact lpPowerSum_pos_of_exists_ne_zero p x h

theorem l1Norm_add_of_disjointSupport
    (x y : Γ → ℚ) (hdisj : disjointSupport x y) :
    l1Norm (fun γ => x γ + y γ) = l1Norm x + l1Norm y := by
  unfold l1Norm
  calc
    (∑ γ, |x γ + y γ|) = ∑ γ, (|x γ| + |y γ|) := by
      apply Finset.sum_congr rfl
      intro γ _hγ
      rcases hdisj γ with hx | hy
      · simp [hx]
      · simp [hy]
    _ = (∑ γ, |x γ|) + (∑ γ, |y γ|) := by
      rw [Finset.sum_add_distrib]

theorem l1AdditivityDefect_eq_zero_of_disjointSupport
    (x y : Γ → ℚ) (hdisj : disjointSupport x y) :
    l1AdditivityDefect x y = 0 := by
  exact (l1AdditivityDefect_eq_zero_iff_additive x y).mpr
    (l1Norm_add_of_disjointSupport x y hdisj)

omit [Fintype Γ] in
theorem disjointSupport_mul_eq_zero
    (x y : Γ → ℚ) (hdisj : disjointSupport x y) :
    ∀ γ, x γ * y γ = 0 := by
  intro γ
  rcases hdisj γ with hx | hy
  · simp [hx]
  · simp [hy]

theorem l1LocalGreenCertificate_of_disjointSupport
    (x y : Γ → ℚ) (hdisj : disjointSupport x y) :
    l1Norm (fun γ => x γ + y γ) = l1Norm x + l1Norm y ∧
      l1AdditivityDefect x y = 0 ∧
      (∀ γ, l1CoordinateAdditivityDefect x y γ = 0) ∧
      (∀ γ, x γ * y γ = 0) := by
  have hadd : l1Norm (fun γ => x γ + y γ) = l1Norm x + l1Norm y :=
    l1Norm_add_of_disjointSupport x y hdisj
  have hdefect : l1AdditivityDefect x y = 0 :=
    l1AdditivityDefect_eq_zero_of_disjointSupport x y hdisj
  have hlocal : ∀ γ, l1CoordinateAdditivityDefect x y γ = 0 :=
    (l1AdditivityDefect_eq_zero_iff_all_coordinateDefects_zero x y).mp hdefect
  have hproduct : ∀ γ, x γ * y γ = 0 :=
    disjointSupport_mul_eq_zero x y hdisj
  exact ⟨hadd, hdefect, hlocal, hproduct⟩

theorem lpPowerSum_add_of_disjointSupport
    {p : ℕ} (hp : p ≠ 0) (x y : Γ → ℚ) (hdisj : disjointSupport x y) :
    lpPowerSum p (fun γ => x γ + y γ) = lpPowerSum p x + lpPowerSum p y := by
  unfold lpPowerSum
  calc
    (∑ γ, |x γ + y γ| ^ p) = ∑ γ, (|x γ| ^ p + |y γ| ^ p) := by
      apply Finset.sum_congr rfl
      intro γ _hγ
      rcases hdisj γ with hx | hy
      · simp [hx, hp]
      · simp [hy, hp]
    _ = (∑ γ, |x γ| ^ p) + (∑ γ, |y γ| ^ p) := by
      rw [Finset.sum_add_distrib]

theorem l1_disjoint_additivity_two_blocks (a b : ℚ) :
    a + b = a + b := by
  rfl

theorem l2_squared_strict_subadditivity_two_positive_blocks
    {a b : ℚ} (ha : 0 < a) (hb : 0 < b) :
    a ^ 2 + b ^ 2 < (a + b) ^ 2 := by
  nlinarith [mul_pos ha hb]

theorem lp_nat_power_strict_subadditivity_two_positive_blocks
    {a b : ℚ} {p : ℕ} (ha : 0 < a) (hb : 0 < b) (hp : 2 ≤ p) :
    a ^ p + b ^ p < (a + b) ^ p := by
  let q : ℕ := p - 2
  have hp_eq : p = q + 2 := by
    dsimp [q]
    omega
  have h2q : 2 + q = p := by
    dsimp [q]
    omega
  have hab_pos : 0 < a + b := add_pos ha hb
  have hq_pos : 0 < (a + b) ^ q := pow_pos hab_pos q
  have ha_le : a ≤ a + b := by linarith
  have hb_le : b ≤ a + b := by linarith
  have hqa : a ^ q ≤ (a + b) ^ q :=
    pow_le_pow_left₀ (le_of_lt ha) ha_le q
  have hqb : b ^ q ≤ (a + b) ^ q :=
    pow_le_pow_left₀ (le_of_lt hb) hb_le q
  have ha_bound : a ^ p ≤ a ^ 2 * (a + b) ^ q := by
    calc
      a ^ p = a ^ 2 * a ^ q := by
        rw [hp_eq, pow_add]
        ring
      _ ≤ a ^ 2 * (a + b) ^ q :=
        mul_le_mul_of_nonneg_left hqa (sq_nonneg a)
  have hb_bound : b ^ p ≤ b ^ 2 * (a + b) ^ q := by
    calc
      b ^ p = b ^ 2 * b ^ q := by
        rw [hp_eq, pow_add]
        ring
      _ ≤ b ^ 2 * (a + b) ^ q :=
        mul_le_mul_of_nonneg_left hqb (sq_nonneg b)
  have hsum_bound :
      a ^ p + b ^ p ≤ (a ^ 2 + b ^ 2) * (a + b) ^ q := by
    calc
      a ^ p + b ^ p ≤
          a ^ 2 * (a + b) ^ q + b ^ 2 * (a + b) ^ q :=
        add_le_add ha_bound hb_bound
      _ = (a ^ 2 + b ^ 2) * (a + b) ^ q := by ring
  have h2_strict : a ^ 2 + b ^ 2 < (a + b) ^ 2 :=
    l2_squared_strict_subadditivity_two_positive_blocks ha hb
  calc
    a ^ p + b ^ p ≤ (a ^ 2 + b ^ 2) * (a + b) ^ q := hsum_bound
    _ < (a + b) ^ 2 * (a + b) ^ q :=
      mul_lt_mul_of_pos_right h2_strict hq_pos
    _ = (a + b) ^ p := by
      rw [← pow_add, h2q]

theorem lpPowerSum_disjoint_strict_below_sum_witness_power
    {p : ℕ} (hp : 2 ≤ p) (x y : Γ → ℚ) (hdisj : disjointSupport x y)
    {a b : ℚ} (ha : 0 < a) (hb : 0 < b)
    (ha_power : a ^ p = lpPowerSum p x)
    (hb_power : b ^ p = lpPowerSum p y) :
    lpPowerSum p (fun γ => x γ + y γ) < (a + b) ^ p := by
  have hp_ne : p ≠ 0 := by omega
  calc
    lpPowerSum p (fun γ => x γ + y γ) =
        lpPowerSum p x + lpPowerSum p y :=
      lpPowerSum_add_of_disjointSupport hp_ne x y hdisj
    _ = a ^ p + b ^ p := by rw [← ha_power, ← hb_power]
    _ < (a + b) ^ p :=
      lp_nat_power_strict_subadditivity_two_positive_blocks ha hb hp

def twoInputRow (a b x y : ℚ) : ℚ :=
  a * x + b * y

def phaseBlind₂ (x y x' y' : ℚ) : Prop :=
  x ^ 2 = x' ^ 2 ∧ y ^ 2 = y' ^ 2

def rowDescentCompatible₂ (a b : ℚ) : Prop :=
  ∀ x y x' y',
    phaseBlind₂ x y x' y' →
      (twoInputRow a b x y) ^ 2 = (twoInputRow a b x' y') ^ 2

theorem sign_phase_cross_term_varies
    {a b : ℚ} (hab : a * b ≠ 0) :
    (a + b) ^ 2 ≠ (a - b) ^ 2 := by
  intro h
  have hzero : a * b = 0 := by
    nlinarith
  exact hab hzero

theorem rowDescentCompatible₂_forces_zero_product
    {a b : ℚ} (h : rowDescentCompatible₂ a b) :
    a * b = 0 := by
  by_contra hab
  have hsame : phaseBlind₂ (1 : ℚ) 1 1 (-1) := by
    constructor <;> norm_num
  have hsq := h 1 1 1 (-1) hsame
  have hbad : (a + b) ^ 2 = (a - b) ^ 2 := by
    simpa [twoInputRow, sub_eq_add_neg] using hsq
  exact sign_phase_cross_term_varies hab hbad

theorem rowDescentCompatible₂_forces_row_sparse
    {a b : ℚ} (h : rowDescentCompatible₂ a b) :
    a = 0 ∨ b = 0 := by
  exact mul_eq_zero.mp (rowDescentCompatible₂_forces_zero_product h)

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def finiteRowEval (a x : ι → ℚ) : ℚ :=
  ∑ k, a k * x k

def finitePhaseBlind (x y : ι → ℚ) : Prop :=
  ∀ k, x k ^ 2 = y k ^ 2

def squaredWeightDifference (x y : ι → ℚ) : ι → ℚ :=
  fun k => x k ^ 2 - y k ^ 2

def squaredWeightZero (d : ι → ℚ) : Prop :=
  ∀ k, d k = 0

def phaseBlindPrimitiveDifference :
    OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ) where
  δ := squaredWeightDifference
  Zero := squaredWeightZero
  zero_refl := by
    intro x k
    dsimp [squaredWeightDifference]
    ring
  zero_symm := by
    intro x y hxy k
    have hk : x k ^ 2 = y k ^ 2 := by
      have := hxy k
      dsimp [squaredWeightDifference] at this
      linarith
    dsimp [squaredWeightDifference]
    linarith
  zero_trans := by
    intro x y z hxy hyz k
    have hxyk : x k ^ 2 = y k ^ 2 := by
      have := hxy k
      dsimp [squaredWeightDifference] at this
      linarith
    have hyzk : y k ^ 2 = z k ^ 2 := by
      have := hyz k
      dsimp [squaredWeightDifference] at this
      linarith
    dsimp [squaredWeightDifference]
    linarith

omit [Fintype ι] [DecidableEq ι] in
theorem finitePhaseBlind_iff_primitiveDifference_zeroRel
    (x y : ι → ℚ) :
    finitePhaseBlind x y ↔
      (phaseBlindPrimitiveDifference :
        OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).ZeroRel x y := by
  constructor
  · intro h k
    dsimp [OmegaCore.PrimitiveDifference.ZeroRel, phaseBlindPrimitiveDifference,
      squaredWeightDifference, squaredWeightZero]
    exact sub_eq_zero.mpr (h k)
  · intro h k
    have hk := h k
    dsimp [OmegaCore.PrimitiveDifference.ZeroRel, phaseBlindPrimitiveDifference,
      squaredWeightDifference, squaredWeightZero] at hk
    exact sub_eq_zero.mp hk

def finiteRowDescentCompatible (a : ι → ℚ) : Prop :=
  ∀ x y : ι → ℚ,
    finitePhaseBlind x y →
      (finiteRowEval a x) ^ 2 = (finiteRowEval a y) ^ 2

def rowSupportSubsingleton (a : ι → ℚ) : Prop :=
  ∀ {i j : ι}, a i ≠ 0 → a j ≠ 0 → i = j

theorem finiteRowDescentCompatible_forces_pairwise_zero_product
    {a : ι → ℚ} (h : finiteRowDescentCompatible a) {i j : ι} (hij : i ≠ j) :
    a i * a j = 0 := by
  classical
  let x : ι → ℚ := fun k => if k = i then 1 else if k = j then 1 else 0
  let y : ι → ℚ := fun k => if k = i then 1 else if k = j then -1 else 0
  have hpb : finitePhaseBlind x y := by
    intro k
    by_cases hki : k = i
    · simp [x, y, hki]
    · by_cases hkj : k = j
      · simp [x, y, hkj]
      · simp [x, y, hki, hkj]
  have hsq := h x y hpb
  have hx_sum :
      (∑ k, if k = i then a k else if k = j then a k else 0) = a i + a j := by
    have hpoint : ∀ k,
        (if k = i then a k else if k = j then a k else 0) =
          (if k = i then a k else 0) + (if k = j then a k else 0) := by
      intro k
      by_cases hki : k = i
      · subst k
        simp [hij]
      · simp [hki]
    calc
      (∑ k, if k = i then a k else if k = j then a k else 0)
          = ∑ k, ((if k = i then a k else 0) + (if k = j then a k else 0)) := by
            apply Finset.sum_congr rfl
            intro k _hk
            exact hpoint k
      _ = (∑ k, if k = i then a k else 0) + (∑ k, if k = j then a k else 0) := by
            rw [Finset.sum_add_distrib]
      _ = a i + a j := by simp
  have hy_sum :
      (∑ k, if k = i then a k else if k = j then -a k else 0) = a i - a j := by
    have hpoint : ∀ k,
        (if k = i then a k else if k = j then -a k else 0) =
          (if k = i then a k else 0) + (if k = j then -a k else 0) := by
      intro k
      by_cases hki : k = i
      · subst k
        simp [hij]
      · simp [hki]
    calc
      (∑ k, if k = i then a k else if k = j then -a k else 0)
          = ∑ k, ((if k = i then a k else 0) + (if k = j then -a k else 0)) := by
            apply Finset.sum_congr rfl
            intro k _hk
            exact hpoint k
      _ = (∑ k, if k = i then a k else 0) + (∑ k, if k = j then -a k else 0) := by
            rw [Finset.sum_add_distrib]
      _ = a i - a j := by
            simp
            ring
  have hx : finiteRowEval a x = a i + a j := by
    simpa [finiteRowEval, x] using hx_sum
  have hy : finiteRowEval a y = a i - a j := by
    simpa [finiteRowEval, y] using hy_sum
  have heq : (a i + a j) ^ 2 = (a i - a j) ^ 2 := by
    simpa [hx, hy] using hsq
  nlinarith

theorem finiteRowDescentCompatible_forces_pairwise_row_sparse
    {a : ι → ℚ} (h : finiteRowDescentCompatible a) {i j : ι} (hij : i ≠ j) :
    a i = 0 ∨ a j = 0 := by
  exact mul_eq_zero.mp
    (finiteRowDescentCompatible_forces_pairwise_zero_product h hij)

theorem finiteRowDescentCompatible_forces_support_subsingleton
    {a : ι → ℚ} (h : finiteRowDescentCompatible a) {i j : ι}
    (hi : a i ≠ 0) (hj : a j ≠ 0) :
    i = j := by
  by_contra hij
  exact (finiteRowDescentCompatible_forces_pairwise_row_sparse h hij).elim hi hj

theorem finiteRowDescentCompatible_forces_rowSupportSubsingleton
    {a : ι → ℚ} (h : finiteRowDescentCompatible a) :
    rowSupportSubsingleton a := by
  intro i j hi hj
  exact finiteRowDescentCompatible_forces_support_subsingleton h hi hj

omit [DecidableEq ι] in
theorem finiteRowEval_eq_zero_of_zero_row
    {a x : ι → ℚ} (hzero : ∀ k, a k = 0) :
    finiteRowEval a x = 0 := by
  unfold finiteRowEval
  exact Finset.sum_eq_zero (fun k _hk => by simp [hzero k])

omit [DecidableEq ι] in
theorem finiteRowDescentCompatible_of_zero_row
    {a : ι → ℚ} (hzero : ∀ k, a k = 0) :
    finiteRowDescentCompatible a := by
  intro x y _hxy
  simp [finiteRowEval_eq_zero_of_zero_row (a := a) (x := x) hzero,
    finiteRowEval_eq_zero_of_zero_row (a := a) (x := y) hzero]

omit [DecidableEq ι] in
theorem finiteRowEval_eq_single_of_supportedAt
    {a x : ι → ℚ} {i : ι} (hsupp : ∀ k, k ≠ i → a k = 0) :
    finiteRowEval a x = a i * x i := by
  unfold finiteRowEval
  exact Finset.sum_eq_single i
    (fun k _hk hki => by simp [hsupp k hki])
    (fun hi => False.elim (hi (Fintype.complete i)))

omit [DecidableEq ι] in
theorem finiteRowDescentCompatible_of_supportedAt
    {a : ι → ℚ} {i : ι} (hsupp : ∀ k, k ≠ i → a k = 0) :
    finiteRowDescentCompatible a := by
  intro x y hxy
  rw [finiteRowEval_eq_single_of_supportedAt (a := a) (x := x) hsupp,
    finiteRowEval_eq_single_of_supportedAt (a := a) (x := y) hsupp]
  calc
    (a i * x i) ^ 2 = (a i) ^ 2 * (x i) ^ 2 := by ring
    _ = (a i) ^ 2 * (y i) ^ 2 := by rw [hxy i]
    _ = (a i * y i) ^ 2 := by ring

omit [DecidableEq ι] in
theorem finiteRowDescentCompatible_of_rowSupportSubsingleton
    {a : ι → ℚ} (hs : rowSupportSubsingleton a) :
    finiteRowDescentCompatible a := by
  classical
  by_cases hzero : ∀ k, a k = 0
  · exact finiteRowDescentCompatible_of_zero_row hzero
  · push Not at hzero
    rcases hzero with ⟨i, hi⟩
    have hsupp : ∀ k, k ≠ i → a k = 0 := by
      intro k hki
      by_contra hk
      exact hki ((hs hi hk).symm)
    exact finiteRowDescentCompatible_of_supportedAt hsupp

theorem finiteRowDescentCompatible_iff_rowSupportSubsingleton
    (a : ι → ℚ) :
    finiteRowDescentCompatible a ↔ rowSupportSubsingleton a := by
  constructor
  · exact finiteRowDescentCompatible_forces_rowSupportSubsingleton
  · exact finiteRowDescentCompatible_of_rowSupportSubsingleton

def finiteRowSquaredEval (a x : ι → ℚ) : ℚ :=
  (finiteRowEval a x) ^ 2

omit [DecidableEq ι] in
theorem finiteRowDescentCompatible_iff_invariantCongruent
    (a : ι → ℚ) :
    finiteRowDescentCompatible a ↔
      (phaseBlindPrimitiveDifference :
        OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).InvariantCongruent
        (finiteRowSquaredEval a) := by
  constructor
  · intro h x y hxy
    have hpb : finitePhaseBlind x y :=
      (finitePhaseBlind_iff_primitiveDifference_zeroRel x y).mpr hxy
    simpa [finiteRowSquaredEval] using h x y hpb
  · intro h x y hxy
    have hzero :
        (phaseBlindPrimitiveDifference :
          OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).ZeroRel x y :=
      (finitePhaseBlind_iff_primitiveDifference_zeroRel x y).mp hxy
    simpa [finiteRowSquaredEval] using h x y hzero

theorem finiteRowSquaredEval_invariantCongruent_iff_rowSupportSubsingleton
    (a : ι → ℚ) :
    (phaseBlindPrimitiveDifference :
      OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).InvariantCongruent
        (finiteRowSquaredEval a) ↔ rowSupportSubsingleton a :=
  (finiteRowDescentCompatible_iff_invariantCongruent a).symm.trans
    (finiteRowDescentCompatible_iff_rowSupportSubsingleton a)

theorem finiteRowSquaredEval_factor_exists_iff_rowSupportSubsingleton
    (a : ι → ℚ) :
    (∃ F :
        (phaseBlindPrimitiveDifference :
          OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).ResidualQuotient → ℚ,
        ∀ x : ι → ℚ,
          F ((phaseBlindPrimitiveDifference :
            OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).classOf x) =
            finiteRowSquaredEval a x) ↔
      rowSupportSubsingleton a := by
  have hfactor :
      (∃ F :
          (phaseBlindPrimitiveDifference :
            OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).ResidualQuotient → ℚ,
          ∀ x : ι → ℚ,
            F ((phaseBlindPrimitiveDifference :
              OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).classOf x) =
              finiteRowSquaredEval a x) ↔
        (phaseBlindPrimitiveDifference :
          OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).InvariantCongruent
          (finiteRowSquaredEval a) :=
    OmegaCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      (phaseBlindPrimitiveDifference :
        OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ))
      (finiteRowSquaredEval a)
  exact hfactor.trans
    (finiteRowSquaredEval_invariantCongruent_iff_rowSupportSubsingleton a)

variable {κ : Type*} [Fintype κ] [DecidableEq κ]

def finiteMatrixEval (M : κ → ι → ℚ) (x : ι → ℚ) : κ → ℚ :=
  fun j => finiteRowEval (M j) x

def finiteMatrixSquaredEval (M : κ → ι → ℚ) (x : ι → ℚ) : κ → ℚ :=
  fun j => finiteRowSquaredEval (M j) x

def finiteMatrixDescentCompatible (M : κ → ι → ℚ) : Prop :=
  ∀ x y : ι → ℚ,
    finitePhaseBlind x y →
      finitePhaseBlind (finiteMatrixEval M x) (finiteMatrixEval M y)

omit [DecidableEq ι] [Fintype κ] [DecidableEq κ] in
theorem finiteMatrixDescentCompatible_iff_all_rows_compatible
    (M : κ → ι → ℚ) :
    finiteMatrixDescentCompatible M ↔
      ∀ j : κ, finiteRowDescentCompatible (M j) := by
  constructor
  · intro h j x y hxy
    exact h x y hxy j
  · intro h x y hxy j
    exact h j x y hxy

omit [Fintype κ] [DecidableEq κ] in
theorem finiteMatrixDescentCompatible_iff_all_rows_rowSupportSubsingleton
    (M : κ → ι → ℚ) :
    finiteMatrixDescentCompatible M ↔
      ∀ j : κ, rowSupportSubsingleton (M j) := by
  rw [finiteMatrixDescentCompatible_iff_all_rows_compatible]
  constructor
  · intro h j
    exact (finiteRowDescentCompatible_iff_rowSupportSubsingleton (M j)).mp (h j)
  · intro h j
    exact (finiteRowDescentCompatible_iff_rowSupportSubsingleton (M j)).mpr (h j)

omit [DecidableEq ι] [Fintype κ] [DecidableEq κ] in
theorem finiteMatrixDescentCompatible_iff_invariantCongruent
    (M : κ → ι → ℚ) :
    finiteMatrixDescentCompatible M ↔
      (phaseBlindPrimitiveDifference :
        OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).InvariantCongruent
        (finiteMatrixSquaredEval M) := by
  constructor
  · intro h x y hxy
    have hpb : finitePhaseBlind x y :=
      (finitePhaseBlind_iff_primitiveDifference_zeroRel x y).mpr hxy
    funext j
    simpa [finiteMatrixSquaredEval, finiteMatrixEval, finiteRowSquaredEval]
      using h x y hpb j
  · intro h x y hxy j
    have hzero :
        (phaseBlindPrimitiveDifference :
          OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).ZeroRel x y :=
      (finitePhaseBlind_iff_primitiveDifference_zeroRel x y).mp hxy
    have heq := congrFun (h x y hzero) j
    simpa [finiteMatrixSquaredEval, finiteMatrixEval, finiteRowSquaredEval]
      using heq

omit [Fintype κ] [DecidableEq κ] in
theorem finiteMatrixSquaredEval_invariantCongruent_iff_all_rows_rowSupportSubsingleton
    (M : κ → ι → ℚ) :
    (phaseBlindPrimitiveDifference :
      OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).InvariantCongruent
        (finiteMatrixSquaredEval M) ↔
      ∀ j : κ, rowSupportSubsingleton (M j) :=
  (finiteMatrixDescentCompatible_iff_invariantCongruent M).symm.trans
    (finiteMatrixDescentCompatible_iff_all_rows_rowSupportSubsingleton M)

omit [Fintype κ] [DecidableEq κ] in
theorem finiteMatrixSquaredEval_factor_exists_iff_all_rows_rowSupportSubsingleton
    (M : κ → ι → ℚ) :
    (∃ F :
        (phaseBlindPrimitiveDifference :
          OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).ResidualQuotient →
            (κ → ℚ),
        ∀ x : ι → ℚ,
          F ((phaseBlindPrimitiveDifference :
            OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).classOf x) =
            finiteMatrixSquaredEval M x) ↔
      ∀ j : κ, rowSupportSubsingleton (M j) := by
  have hfactor :
      (∃ F :
          (phaseBlindPrimitiveDifference :
            OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).ResidualQuotient →
              (κ → ℚ),
          ∀ x : ι → ℚ,
            F ((phaseBlindPrimitiveDifference :
              OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).classOf x) =
              finiteMatrixSquaredEval M x) ↔
        (phaseBlindPrimitiveDifference :
          OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).InvariantCongruent
          (finiteMatrixSquaredEval M) :=
    OmegaCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      (phaseBlindPrimitiveDifference :
        OmegaCore.PrimitiveDifference (ι → ℚ) (ι → ℚ))
      (finiteMatrixSquaredEval M)
  exact hfactor.trans
    (finiteMatrixSquaredEval_invariantCongruent_iff_all_rows_rowSupportSubsingleton M)

def twoRowMixWeights (x y : ℚ) : ℚ × ℚ :=
  ((x + y) ^ 2, (x - y) ^ 2)

def pairSquaredWeights (p : ℚ × ℚ) : ℚ × ℚ :=
  (p.1 ^ 2, p.2 ^ 2)

def pairSquaredWeightDifference (p q : ℚ × ℚ) : ℚ × ℚ :=
  (p.1 ^ 2 - q.1 ^ 2, p.2 ^ 2 - q.2 ^ 2)

def pairSquaredWeightZero (d : ℚ × ℚ) : Prop :=
  d.1 = 0 ∧ d.2 = 0

def pairPhaseBlindPrimitiveDifference :
    OmegaCore.PrimitiveDifference (ℚ × ℚ) (ℚ × ℚ) where
  δ := pairSquaredWeightDifference
  Zero := pairSquaredWeightZero
  zero_refl := by
    intro p
    constructor <;> dsimp [pairSquaredWeightDifference, pairSquaredWeightZero] <;> ring
  zero_symm := by
    intro p q hpq
    rcases p with ⟨x, y⟩
    rcases q with ⟨x', y'⟩
    rcases hpq with ⟨hx, hy⟩
    constructor <;>
      dsimp [pairSquaredWeightDifference, pairSquaredWeightZero] at hx hy ⊢ <;>
      linarith
  zero_trans := by
    intro p q r hpq hqr
    rcases p with ⟨x, y⟩
    rcases q with ⟨x', y'⟩
    rcases r with ⟨x'', y''⟩
    rcases hpq with ⟨hx, hy⟩
    rcases hqr with ⟨hx', hy'⟩
    constructor <;>
      dsimp [pairSquaredWeightDifference, pairSquaredWeightZero] at hx hy hx' hy' ⊢ <;>
      linarith

omit [Fintype ι] [DecidableEq ι] in
theorem pairPhaseBlind_iff_primitiveDifference_zeroRel
    (x y x' y' : ℚ) :
    phaseBlind₂ x y x' y' ↔
      pairPhaseBlindPrimitiveDifference.ZeroRel (x, y) (x', y') := by
  constructor
  · intro h
    rcases h with ⟨hx, hy⟩
    constructor <;>
      dsimp [OmegaCore.PrimitiveDifference.ZeroRel,
        pairPhaseBlindPrimitiveDifference, pairSquaredWeightDifference,
        pairSquaredWeightZero] <;>
      linarith
  · intro h
    rcases h with ⟨hx, hy⟩
    constructor <;>
      dsimp [OmegaCore.PrimitiveDifference.ZeroRel,
        pairPhaseBlindPrimitiveDifference, pairSquaredWeightDifference,
        pairSquaredWeightZero] at hx hy <;>
      linarith

omit [Fintype ι] [DecidableEq ι] in
theorem pairSquaredWeights_invariantCongruent :
    pairPhaseBlindPrimitiveDifference.InvariantCongruent pairSquaredWeights := by
  intro p q hpq
  rcases p with ⟨x, y⟩
  rcases q with ⟨x', y'⟩
  rcases hpq with ⟨hx, hy⟩
  ext <;>
    dsimp [OmegaCore.PrimitiveDifference.ZeroRel,
      pairPhaseBlindPrimitiveDifference, pairSquaredWeights,
      pairSquaredWeightDifference, pairSquaredWeightZero] at hx hy ⊢ <;>
    linarith

omit [Fintype ι] [DecidableEq ι] in
theorem pairSquaredWeights_factor_exists :
    ∃ F : pairPhaseBlindPrimitiveDifference.ResidualQuotient → ℚ × ℚ,
      ∀ p : ℚ × ℚ,
        F (pairPhaseBlindPrimitiveDifference.classOf p) = pairSquaredWeights p := by
  exact
    (OmegaCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      pairPhaseBlindPrimitiveDifference pairSquaredWeights).mpr
      pairSquaredWeights_invariantCongruent

omit [Fintype ι] [DecidableEq ι] in
theorem twoRowMixWeights_not_invariantCongruent :
    ¬ pairPhaseBlindPrimitiveDifference.InvariantCongruent
        (fun p : ℚ × ℚ => twoRowMixWeights p.1 p.2) := by
  intro hcongr
  have hzero :
      pairPhaseBlindPrimitiveDifference.ZeroRel ((1, 1) : ℚ × ℚ) (1, -1) :=
    (pairPhaseBlind_iff_primitiveDifference_zeroRel 1 1 1 (-1)).mp
      (by constructor <;> norm_num)
  have hmix := hcongr ((1, 1) : ℚ × ℚ) (1, -1) hzero
  have hfst := congrArg Prod.fst hmix
  norm_num [twoRowMixWeights] at hfst

omit [Fintype ι] [DecidableEq ι] in
theorem twoRowMixWeights_no_factor_through_phaseBlindQuotient :
    ¬ (∃ F : pairPhaseBlindPrimitiveDifference.ResidualQuotient → ℚ × ℚ,
        ∀ p : ℚ × ℚ,
          F (pairPhaseBlindPrimitiveDifference.classOf p) =
            twoRowMixWeights p.1 p.2) := by
  exact
    OmegaCore.PrimitiveDifference.invariantFactor_no_factor_of_not_invariant
      pairPhaseBlindPrimitiveDifference
      (fun p : ℚ × ℚ => twoRowMixWeights p.1 p.2)
      twoRowMixWeights_not_invariantCongruent

def pairTotal (p : ℚ × ℚ) : ℚ :=
  p.1 + p.2

def pairSwap (p : ℚ × ℚ) : ℚ × ℚ :=
  (p.2, p.1)

def pairImbalance (p : ℚ × ℚ) : ℚ :=
  p.1 - p.2

def pairSquaredDistance (p q : ℚ × ℚ) : ℚ :=
  (p.1 - q.1) ^ 2 + (p.2 - q.2) ^ 2

theorem pairSquaredDistance_nonneg (p q : ℚ × ℚ) :
    0 ≤ pairSquaredDistance p q := by
  unfold pairSquaredDistance
  exact add_nonneg (sq_nonneg (p.1 - q.1)) (sq_nonneg (p.2 - q.2))

theorem pairSquaredDistance_pos_of_ne {p q : ℚ × ℚ} (h : p ≠ q) :
    0 < pairSquaredDistance p q := by
  rcases p with ⟨a, b⟩
  rcases q with ⟨c, d⟩
  unfold pairSquaredDistance
  by_cases hfst : a = c
  · have hsnd : b ≠ d := by
      intro hbd
      exact h (by ext <;> assumption)
    have hsndpos : 0 < (b - d) ^ 2 :=
      sq_pos_of_ne_zero (sub_ne_zero.mpr hsnd)
    have hfstzero : (a - c) ^ 2 = 0 := by simp [hfst]
    nlinarith
  · have hfstpos : 0 < (a - c) ^ 2 :=
      sq_pos_of_ne_zero (sub_ne_zero.mpr hfst)
    have hsndnonneg : 0 ≤ (b - d) ^ 2 := sq_nonneg (b - d)
    nlinarith

theorem pairSquaredDistance_eq_zero_iff (p q : ℚ × ℚ) :
    pairSquaredDistance p q = 0 ↔ p = q := by
  constructor
  · intro hzero
    by_contra hne
    have hpos : 0 < pairSquaredDistance p q := pairSquaredDistance_pos_of_ne hne
    linarith
  · intro hpq
    rw [hpq]
    unfold pairSquaredDistance
    ring

theorem pairSquaredDistance_swap (p : ℚ × ℚ) :
    pairSquaredDistance p (pairSwap p) = 2 * pairImbalance p ^ 2 := by
  rcases p with ⟨a, b⟩
  unfold pairSquaredDistance pairSwap pairImbalance
  ring

theorem pairSquaredDistance_add_swap_left_of_total_one
    {p q : ℚ × ℚ} (hp : pairTotal p = 1) (hq : pairTotal q = 1) :
    pairSquaredDistance p q + pairSquaredDistance (pairSwap p) q =
      pairImbalance p ^ 2 + pairImbalance q ^ 2 := by
  rcases p with ⟨a, b⟩
  rcases q with ⟨c, d⟩
  dsimp [pairTotal] at hp hq
  unfold pairSquaredDistance pairSwap pairImbalance
  nlinarith

def pairDirectNormalize (p : ℚ × ℚ) : ℚ × ℚ :=
  (p.1 / pairTotal p, p.2 / pairTotal p)

theorem pairDirectNormalize_sum_eq_one
    {p : ℚ × ℚ} (h : pairTotal p ≠ 0) :
    (pairDirectNormalize p).1 + (pairDirectNormalize p).2 = 1 := by
  rcases p with ⟨a, b⟩
  dsimp [pairDirectNormalize, pairTotal] at h ⊢
  field_simp [h]

theorem pairDirectNormalize_fst_nonneg
    {p : ℚ × ℚ} (hfst : 0 ≤ p.1) (htotal : 0 < pairTotal p) :
    0 ≤ (pairDirectNormalize p).1 := by
  exact div_nonneg hfst (le_of_lt htotal)

theorem pairDirectNormalize_snd_nonneg
    {p : ℚ × ℚ} (hsnd : 0 ≤ p.2) (htotal : 0 < pairTotal p) :
    0 ≤ (pairDirectNormalize p).2 := by
  exact div_nonneg hsnd (le_of_lt htotal)

def pairSquaredDirectProb (p : ℚ × ℚ) : ℚ × ℚ :=
  pairDirectNormalize (pairSquaredWeights p)

theorem pairSquaredDirectProb_sign_flip (x y : ℚ) :
    pairSquaredDirectProb (x, y) = pairSquaredDirectProb (x, -y) := by
  simp [pairSquaredDirectProb, pairDirectNormalize, pairSquaredWeights, pairTotal]

theorem pairSquaredWeights_pairTotal_pos_of_nonzero
    {p : ℚ × ℚ} (h : p.1 ≠ 0 ∨ p.2 ≠ 0) :
    0 < pairTotal (pairSquaredWeights p) := by
  rcases p with ⟨x, y⟩
  rcases h with hx | hy
  · have hxpos : 0 < x ^ 2 := sq_pos_of_ne_zero hx
    have hynonneg : 0 ≤ y ^ 2 := sq_nonneg y
    unfold pairTotal pairSquaredWeights
    nlinarith
  · have hxnonneg : 0 ≤ x ^ 2 := sq_nonneg x
    have hypos : 0 < y ^ 2 := sq_pos_of_ne_zero hy
    unfold pairTotal pairSquaredWeights
    nlinarith

theorem pairSquaredDirectProb_probability_certificate
    {p : ℚ × ℚ} (h : p.1 ≠ 0 ∨ p.2 ≠ 0) :
    0 ≤ (pairSquaredDirectProb p).1 ∧
      0 ≤ (pairSquaredDirectProb p).2 ∧
      (pairSquaredDirectProb p).1 + (pairSquaredDirectProb p).2 = 1 := by
  have htotal_pos : 0 < pairTotal (pairSquaredWeights p) :=
    pairSquaredWeights_pairTotal_pos_of_nonzero h
  have htotal_ne : pairTotal (pairSquaredWeights p) ≠ 0 := ne_of_gt htotal_pos
  constructor
  · exact pairDirectNormalize_fst_nonneg (sq_nonneg p.1) htotal_pos
  constructor
  · exact pairDirectNormalize_snd_nonneg (sq_nonneg p.2) htotal_pos
  · exact pairDirectNormalize_sum_eq_one htotal_ne

theorem pairSquaredDirectProb_imbalance_formula (p : ℚ × ℚ) :
    pairImbalance (pairSquaredDirectProb p) =
      (p.1 ^ 2 - p.2 ^ 2) / (p.1 ^ 2 + p.2 ^ 2) := by
  rcases p with ⟨x, y⟩
  unfold pairImbalance pairSquaredDirectProb pairDirectNormalize
    pairSquaredWeights pairTotal
  ring_nf

theorem pairSquaredDirectProb_imbalance_sign_flip (x y : ℚ) :
    pairImbalance (pairSquaredDirectProb (x, -y)) =
      pairImbalance (pairSquaredDirectProb (x, y)) := by
  exact congrArg pairImbalance (pairSquaredDirectProb_sign_flip x y).symm

theorem pairSquaredDirectProb_sign_flip_squaredDistance_eq_zero (x y : ℚ) :
    pairSquaredDistance (pairSquaredDirectProb (x, y))
      (pairSquaredDirectProb (x, -y)) = 0 := by
  rw [pairSquaredDirectProb_sign_flip x y]
  unfold pairSquaredDistance
  ring

omit [Fintype ι] [DecidableEq ι] in
theorem pairSquaredDirectProb_invariantCongruent :
    pairPhaseBlindPrimitiveDifference.InvariantCongruent pairSquaredDirectProb := by
  intro p q hpq
  have hsq := pairSquaredWeights_invariantCongruent p q hpq
  exact congrArg pairDirectNormalize hsq

omit [Fintype ι] [DecidableEq ι] in
theorem pairSquaredDirectProb_factor_exists :
    ∃ F : pairPhaseBlindPrimitiveDifference.ResidualQuotient → ℚ × ℚ,
      ∀ p : ℚ × ℚ,
        F (pairPhaseBlindPrimitiveDifference.classOf p) = pairSquaredDirectProb p := by
  exact
    (OmegaCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      pairPhaseBlindPrimitiveDifference pairSquaredDirectProb).mpr
      pairSquaredDirectProb_invariantCongruent

theorem twoRowMixWeights_pairTotal (x y : ℚ) :
    pairTotal (twoRowMixWeights x y) = 2 * (x ^ 2 + y ^ 2) := by
  unfold pairTotal twoRowMixWeights
  ring

theorem twoRowMixWeights_pairTotal_sign_flip (x y : ℚ) :
    pairTotal (twoRowMixWeights x (-y)) = pairTotal (twoRowMixWeights x y) := by
  unfold pairTotal twoRowMixWeights
  ring

theorem twoRowMixWeights_pairTotal_ne_zero_of_mul_ne_zero
    {x y : ℚ} (hxy : x * y ≠ 0) :
    pairTotal (twoRowMixWeights x y) ≠ 0 := by
  have hx : x ≠ 0 := by
    intro hx
    exact hxy (by simp [hx])
  have hy : y ≠ 0 := by
    intro hy
    exact hxy (by simp [hy])
  have hxpos : 0 < x ^ 2 := sq_pos_of_ne_zero hx
  have hypos : 0 < y ^ 2 := sq_pos_of_ne_zero hy
  rw [twoRowMixWeights_pairTotal]
  nlinarith

theorem twoRowMixWeights_pairTotal_pos_of_mul_ne_zero
    {x y : ℚ} (hxy : x * y ≠ 0) :
    0 < pairTotal (twoRowMixWeights x y) := by
  have hx : x ≠ 0 := by
    intro hx
    exact hxy (by simp [hx])
  have hy : y ≠ 0 := by
    intro hy
    exact hxy (by simp [hy])
  have hxpos : 0 < x ^ 2 := sq_pos_of_ne_zero hx
  have hypos : 0 < y ^ 2 := sq_pos_of_ne_zero hy
  rw [twoRowMixWeights_pairTotal]
  nlinarith

theorem twoRowMixWeights_normalized_probability_certificate
    {x y : ℚ} (hxy : x * y ≠ 0) :
    0 ≤ (pairDirectNormalize (twoRowMixWeights x y)).1 ∧
      0 ≤ (pairDirectNormalize (twoRowMixWeights x y)).2 ∧
      (pairDirectNormalize (twoRowMixWeights x y)).1 +
        (pairDirectNormalize (twoRowMixWeights x y)).2 = 1 := by
  have htotal_pos : 0 < pairTotal (twoRowMixWeights x y) :=
    twoRowMixWeights_pairTotal_pos_of_mul_ne_zero hxy
  have htotal_ne : pairTotal (twoRowMixWeights x y) ≠ 0 := ne_of_gt htotal_pos
  constructor
  · exact pairDirectNormalize_fst_nonneg (sq_nonneg (x + y)) htotal_pos
  constructor
  · exact pairDirectNormalize_snd_nonneg (sq_nonneg (x - y)) htotal_pos
  · exact pairDirectNormalize_sum_eq_one htotal_ne

theorem twoRowMixWeights_imbalance (x y : ℚ) :
    pairImbalance (twoRowMixWeights x y) = 4 * x * y := by
  unfold pairImbalance twoRowMixWeights
  ring

theorem twoRowMixWeights_normalized_imbalance_total_formula (x y : ℚ) :
    pairImbalance (pairDirectNormalize (twoRowMixWeights x y)) =
      (4 * x * y) / pairTotal (twoRowMixWeights x y) := by
  unfold pairImbalance pairDirectNormalize pairTotal twoRowMixWeights
  ring_nf

theorem twoRowMixWeights_normalized_imbalance_formula
    {x y : ℚ} (hxy : x * y ≠ 0) :
    pairImbalance (pairDirectNormalize (twoRowMixWeights x y)) =
      (2 * x * y) / (x ^ 2 + y ^ 2) := by
  have hx : x ≠ 0 := by
    intro hx
    exact hxy (by simp [hx])
  have hy : y ≠ 0 := by
    intro hy
    exact hxy (by simp [hy])
  have hxpos : 0 < x ^ 2 := sq_pos_of_ne_zero hx
  have hypos : 0 < y ^ 2 := sq_pos_of_ne_zero hy
  have hsum : x ^ 2 + y ^ 2 ≠ 0 := by
    nlinarith
  rw [twoRowMixWeights_normalized_imbalance_total_formula]
  rw [twoRowMixWeights_pairTotal]
  field_simp [hsum]
  ring

theorem twoRowMixWeights_normalized_imbalance_sign_flip (x y : ℚ) :
    pairImbalance (pairDirectNormalize (twoRowMixWeights x (-y))) =
      - pairImbalance (pairDirectNormalize (twoRowMixWeights x y)) := by
  unfold pairImbalance pairDirectNormalize pairTotal twoRowMixWeights
  ring_nf

theorem twoRowMixWeights_sign_flip_swap (x y : ℚ) :
    twoRowMixWeights x (-y) = pairSwap (twoRowMixWeights x y) := by
  ext <;> unfold pairSwap twoRowMixWeights <;> ring

theorem twoRowMixWeights_normalized_sign_flip_swap (x y : ℚ) :
    pairDirectNormalize (twoRowMixWeights x (-y)) =
      pairSwap (pairDirectNormalize (twoRowMixWeights x y)) := by
  ext <;> unfold pairSwap pairDirectNormalize pairTotal twoRowMixWeights <;> ring

theorem twoRowMixWeights_normalized_sign_flip_differs
    {x y : ℚ} (hxy : x * y ≠ 0) :
    pairDirectNormalize (twoRowMixWeights x y) ≠
      pairDirectNormalize (twoRowMixWeights x (-y)) := by
  intro h
  have hfst := congrArg Prod.fst h
  have hden : pairTotal (twoRowMixWeights x y) ≠ 0 :=
    twoRowMixWeights_pairTotal_ne_zero_of_mul_ne_zero hxy
  have hfst' :
      (x + y) ^ 2 / pairTotal (twoRowMixWeights x y) =
        (x - y) ^ 2 / pairTotal (twoRowMixWeights x y) := by
    simpa [pairDirectNormalize, twoRowMixWeights, pairTotal, sub_eq_add_neg,
      add_comm, add_left_comm, add_assoc] using hfst
  have hbad : (x + y) ^ 2 = (x - y) ^ 2 := by
    field_simp [hden] at hfst'
    exact hfst'
  exact sign_phase_cross_term_varies hxy hbad

theorem twoRowMixWeights_squaredDistance_normalized_sign_flip_pos
    {x y : ℚ} (hxy : x * y ≠ 0) :
    0 < pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
      (pairDirectNormalize (twoRowMixWeights x (-y))) := by
  exact pairSquaredDistance_pos_of_ne
    (twoRowMixWeights_normalized_sign_flip_differs hxy)

theorem twoRowMixDistance_normalized_sign_flip_formula
    {x y : ℚ} (hxy : x * y ≠ 0) :
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
      (pairDirectNormalize (twoRowMixWeights x (-y))) =
        8 * x ^ 2 * y ^ 2 / (x ^ 2 + y ^ 2) ^ 2 := by
  have hx : x ≠ 0 := by
    intro hx
    exact hxy (by simp [hx])
  have hy : y ≠ 0 := by
    intro hy
    exact hxy (by simp [hy])
  have hxpos : 0 < x ^ 2 := sq_pos_of_ne_zero hx
  have hypos : 0 < y ^ 2 := sq_pos_of_ne_zero hy
  have hsum : x ^ 2 + y ^ 2 ≠ 0 := by
    nlinarith
  rw [twoRowMixWeights_normalized_sign_flip_swap]
  rw [pairSquaredDistance_swap]
  rw [twoRowMixWeights_normalized_imbalance_formula hxy]
  field_simp [hsum]
  ring

theorem twoRowMixWeights_normalized_sign_flip_eq_iff_mul_eq_zero (x y : ℚ) :
    pairDirectNormalize (twoRowMixWeights x y) =
      pairDirectNormalize (twoRowMixWeights x (-y)) ↔ x * y = 0 := by
  constructor
  · intro h
    by_contra hxy
    exact twoRowMixWeights_normalized_sign_flip_differs hxy h
  · intro hxy
    rcases mul_eq_zero.mp hxy with hx | hy
    · ext <;> simp [pairDirectNormalize, pairTotal, twoRowMixWeights, hx]
    · ext <;> simp [pairDirectNormalize, pairTotal, twoRowMixWeights, hy]

theorem twoRowMixDistance_zero_iff_crossTerm_zero (x y : ℚ) :
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
      (pairDirectNormalize (twoRowMixWeights x (-y))) = 0 ↔ x * y = 0 := by
  rw [pairSquaredDistance_eq_zero_iff]
  exact twoRowMixWeights_normalized_sign_flip_eq_iff_mul_eq_zero x y

theorem twoRowMixLocalEq_iff_crossTermBalance
    {x y : ℚ} (hsum : x ^ 2 + y ^ 2 ≠ 0) :
    pairDirectNormalize (twoRowMixWeights x y) =
        pairSquaredDirectProb (x, y) ↔
      2 * x * y = x ^ 2 - y ^ 2 := by
  have hsum_nonneg : 0 ≤ x ^ 2 + y ^ 2 := by
    nlinarith [sq_nonneg x, sq_nonneg y]
  have hsum_pos : 0 < x ^ 2 + y ^ 2 := lt_of_le_of_ne' hsum_nonneg hsum
  have hden : (x + y) ^ 2 + (x - y) ^ 2 ≠ 0 := by
    have hden_eq : (x + y) ^ 2 + (x - y) ^ 2 = 2 * (x ^ 2 + y ^ 2) := by
      ring
    rw [hden_eq]
    nlinarith
  constructor
  · intro h
    have hfst :
        (x + y) ^ 2 / ((x + y) ^ 2 + (x - y) ^ 2) =
          x ^ 2 / (x ^ 2 + y ^ 2) := by
      simpa [pairDirectNormalize, pairTotal, twoRowMixWeights,
        pairSquaredDirectProb, pairSquaredWeights] using congrArg Prod.fst h
    field_simp [hden, hsum] at hfst
    nlinarith
  · intro hbalance
    ext <;>
      simp [pairDirectNormalize, pairTotal, twoRowMixWeights,
        pairSquaredDirectProb, pairSquaredWeights]
    · field_simp [hden, hsum]
      nlinarith
    · field_simp [hden, hsum]
      nlinarith

theorem twoRowMixLocalFlipEq_iff_crossTermBalance
    {x y : ℚ} (hsum : x ^ 2 + y ^ 2 ≠ 0) :
    pairDirectNormalize (twoRowMixWeights x (-y)) =
        pairSquaredDirectProb (x, -y) ↔
      -(2 * x * y) = x ^ 2 - y ^ 2 := by
  rw [twoRowMixLocalEq_iff_crossTermBalance
    (x := x) (y := -y)]
  · ring_nf
  · simpa using hsum

theorem twoRowMixLocalDistance_formula
    {x y : ℚ} (hsum : x ^ 2 + y ^ 2 ≠ 0) :
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
        (pairSquaredDirectProb (x, y)) =
      (x ^ 2 - y ^ 2 - 2 * x * y) ^ 2 /
        (2 * (x ^ 2 + y ^ 2) ^ 2) := by
  have hsum_nonneg : 0 ≤ x ^ 2 + y ^ 2 := by
    nlinarith [sq_nonneg x, sq_nonneg y]
  have hsum_pos : 0 < x ^ 2 + y ^ 2 := lt_of_le_of_ne' hsum_nonneg hsum
  have hden : (x + y) ^ 2 + (x - y) ^ 2 ≠ 0 := by
    have hden_eq : (x + y) ^ 2 + (x - y) ^ 2 = 2 * (x ^ 2 + y ^ 2) := by
      ring
    rw [hden_eq]
    nlinarith
  simp [pairSquaredDistance, pairDirectNormalize, twoRowMixWeights,
    pairSquaredDirectProb, pairSquaredWeights, pairTotal]
  field_simp [hden, hsum]
  ring_nf

theorem twoRowMixLocalFlipDistance_formula
    {x y : ℚ} (hsum : x ^ 2 + y ^ 2 ≠ 0) :
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x (-y)))
        (pairSquaredDirectProb (x, -y)) =
      (x ^ 2 - y ^ 2 + 2 * x * y) ^ 2 /
        (2 * (x ^ 2 + y ^ 2) ^ 2) := by
  have h :=
    twoRowMixLocalDistance_formula (x := x) (y := -y) (by simpa using hsum)
  simpa using h

theorem twoRowMixLocalDistance_zero_iff
    {x y : ℚ} (hsum : x ^ 2 + y ^ 2 ≠ 0) :
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
        (pairSquaredDirectProb (x, y)) = 0 ↔
      2 * x * y = x ^ 2 - y ^ 2 := by
  rw [pairSquaredDistance_eq_zero_iff]
  exact twoRowMixLocalEq_iff_crossTermBalance hsum

theorem twoRowMixLocalFlipDistance_zero_iff
    {x y : ℚ} (hsum : x ^ 2 + y ^ 2 ≠ 0) :
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x (-y)))
        (pairSquaredDirectProb (x, -y)) = 0 ↔
      -(2 * x * y) = x ^ 2 - y ^ 2 := by
  rw [pairSquaredDistance_eq_zero_iff]
  exact twoRowMixLocalFlipEq_iff_crossTermBalance hsum

theorem twoRowMixLocalBoth_ne_of_nonzero
    {x y : ℚ} (hnz : x ≠ 0 ∨ y ≠ 0) :
    ¬ (pairDirectNormalize (twoRowMixWeights x y) = pairSquaredDirectProb (x, y) ∧
        pairDirectNormalize (twoRowMixWeights x (-y)) = pairSquaredDirectProb (x, -y)) := by
  have hsum : x ^ 2 + y ^ 2 ≠ 0 := by
    rcases hnz with hx | hy
    · have hxpos : 0 < x ^ 2 := sq_pos_of_ne_zero hx
      have hynonneg : 0 ≤ y ^ 2 := sq_nonneg y
      nlinarith
    · have hxnonneg : 0 ≤ x ^ 2 := sq_nonneg x
      have hypos : 0 < y ^ 2 := sq_pos_of_ne_zero hy
      nlinarith
  intro hlocal
  have hplus :
      2 * x * y = x ^ 2 - y ^ 2 :=
    (twoRowMixLocalEq_iff_crossTermBalance hsum).mp hlocal.1
  have hminus :
      -(2 * x * y) = x ^ 2 - y ^ 2 :=
    (twoRowMixLocalFlipEq_iff_crossTermBalance hsum).mp
      hlocal.2
  have hxy : x * y = 0 := by
    nlinarith
  have hdiff : x ^ 2 - y ^ 2 = 0 := by
    nlinarith
  rcases mul_eq_zero.mp hxy with hx | hy
  · subst x
    have hy2 : y ^ 2 = 0 := by
      nlinarith
    exact hsum (by simp [hy2])
  · subst y
    have hx2 : x ^ 2 = 0 := by
      nlinarith
    exact hsum (by simp [hx2])

theorem twoRowMixWeights_normalized_not_local_on_sign_flip_pair
    {x y : ℚ} (hxy : x * y ≠ 0) :
    ¬ (pairDirectNormalize (twoRowMixWeights x y) = pairSquaredDirectProb (x, y) ∧
        pairDirectNormalize (twoRowMixWeights x (-y)) = pairSquaredDirectProb (x, -y)) := by
  have hx : x ≠ 0 := by
    intro hx
    exact hxy (by simp [hx])
  exact twoRowMixLocalBoth_ne_of_nonzero
    (Or.inl hx)

theorem twoRowMixWeights_normalized_exists_local_mismatch_of_mul_ne_zero
    {x y : ℚ} (hxy : x * y ≠ 0) :
    pairDirectNormalize (twoRowMixWeights x y) ≠ pairSquaredDirectProb (x, y) ∨
      pairDirectNormalize (twoRowMixWeights x (-y)) ≠
        pairSquaredDirectProb (x, -y) := by
  by_cases hlocal :
      pairDirectNormalize (twoRowMixWeights x y) = pairSquaredDirectProb (x, y)
  · right
    intro hlocalFlip
    exact twoRowMixWeights_normalized_not_local_on_sign_flip_pair hxy
      ⟨hlocal, hlocalFlip⟩
  · exact Or.inl hlocal

theorem twoRowMixLocalDistSum_one_nonzero
    {x y : ℚ} (hsum : x ^ 2 + y ^ 2 ≠ 0) :
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
        (pairSquaredDirectProb (x, y)) +
      pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x (-y)))
        (pairSquaredDirectProb (x, -y)) = 1 := by
  rw [twoRowMixLocalDistance_formula hsum,
    twoRowMixLocalFlipDistance_formula hsum]
  field_simp [hsum]
  ring

theorem twoRowMixLocalOneDist_ge_half
    {x y : ℚ} (hsum : x ^ 2 + y ^ 2 ≠ 0) :
    (1 / 2 : ℚ) ≤
        pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
          (pairSquaredDirectProb (x, y)) ∨
      (1 / 2 : ℚ) ≤
        pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x (-y)))
          (pairSquaredDirectProb (x, -y)) := by
  let a :=
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
      (pairSquaredDirectProb (x, y))
  let b :=
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x (-y)))
      (pairSquaredDirectProb (x, -y))
  have hsum1 : a + b = 1 := by
    dsimp [a, b]
    exact twoRowMixLocalDistSum_one_nonzero hsum
  by_cases ha : (1 / 2 : ℚ) ≤ a
  · exact Or.inl ha
  · right
    have hlt : a < (1 / 2 : ℚ) := lt_of_not_ge ha
    change (1 / 2 : ℚ) ≤ b
    nlinarith

theorem twoRowMixLocalDistance_eq_one_iff_flipCrossTermBalance
    {x y : ℚ} (hsum : x ^ 2 + y ^ 2 ≠ 0) :
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
        (pairSquaredDirectProb (x, y)) = 1 ↔
      -(2 * x * y) = x ^ 2 - y ^ 2 := by
  let a :=
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
      (pairSquaredDirectProb (x, y))
  let b :=
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x (-y)))
      (pairSquaredDirectProb (x, -y))
  have hsum1 : a + b = 1 := by
    dsimp [a, b]
    exact twoRowMixLocalDistSum_one_nonzero hsum
  constructor
  · intro ha
    have hb : b = 0 := by
      nlinarith
    exact (twoRowMixLocalFlipDistance_zero_iff hsum).mp hb
  · intro hbalance
    have hb : b = 0 :=
      (twoRowMixLocalFlipDistance_zero_iff hsum).mpr hbalance
    change a = 1
    nlinarith

theorem twoRowMixLocalFlipDistance_eq_one_iff_crossTermBalance
    {x y : ℚ} (hsum : x ^ 2 + y ^ 2 ≠ 0) :
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x (-y)))
        (pairSquaredDirectProb (x, -y)) = 1 ↔
      2 * x * y = x ^ 2 - y ^ 2 := by
  let a :=
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
      (pairSquaredDirectProb (x, y))
  let b :=
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x (-y)))
      (pairSquaredDirectProb (x, -y))
  have hsum1 : a + b = 1 := by
    dsimp [a, b]
    exact twoRowMixLocalDistSum_one_nonzero hsum
  constructor
  · intro hb
    have ha : a = 0 := by
      nlinarith
    exact (twoRowMixLocalDistance_zero_iff hsum).mp ha
  · intro hbalance
    have ha : a = 0 :=
      (twoRowMixLocalDistance_zero_iff hsum).mpr hbalance
    change b = 1
    nlinarith

theorem twoRowMixLocalDistances_sum_eq_one
    {x y : ℚ} (hxy : x * y ≠ 0) :
    pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x y))
        (pairSquaredDirectProb (x, y)) +
      pairSquaredDistance (pairDirectNormalize (twoRowMixWeights x (-y)))
        (pairSquaredDirectProb (x, -y)) = 1 := by
  have hx : x ≠ 0 := by
    intro hx
    exact hxy (by simp [hx])
  have hxpos : 0 < x ^ 2 := sq_pos_of_ne_zero hx
  have hynonneg : 0 ≤ y ^ 2 := sq_nonneg y
  have hsum : x ^ 2 + y ^ 2 ≠ 0 := by
    nlinarith
  exact twoRowMixLocalDistSum_one_nonzero hsum

theorem pairSquaredDirectProb_unit_sign_pair :
    pairSquaredDirectProb (1, 1) = ((1 / 2 : ℚ), (1 / 2 : ℚ)) ∧
      pairSquaredDirectProb (1, -1) = ((1 / 2 : ℚ), (1 / 2 : ℚ)) := by
  constructor <;>
    norm_num [pairSquaredDirectProb, pairDirectNormalize, pairSquaredWeights,
      pairTotal]

theorem twoRowMixWeights_normalized_unit_sign_pair :
    pairDirectNormalize (twoRowMixWeights 1 1) = ((1 : ℚ), 0) ∧
      pairDirectNormalize (twoRowMixWeights 1 (-1)) = (0, (1 : ℚ)) := by
  constructor <;>
    norm_num [pairDirectNormalize, pairTotal, twoRowMixWeights]

theorem normalized_unit_lggr_witness :
    pairSquaredDirectProb (1, 1) = pairSquaredDirectProb (1, -1) ∧
      pairDirectNormalize (twoRowMixWeights 1 1) = ((1 : ℚ), 0) ∧
      pairDirectNormalize (twoRowMixWeights 1 (-1)) = (0, (1 : ℚ)) := by
  exact ⟨pairSquaredDirectProb_sign_flip 1 1,
    twoRowMixWeights_normalized_unit_sign_pair⟩

omit [Fintype ι] [DecidableEq ι] in
theorem twoRowMixWeights_normalized_not_invariantCongruent :
    ¬ pairPhaseBlindPrimitiveDifference.InvariantCongruent
        (fun p : ℚ × ℚ => pairDirectNormalize (twoRowMixWeights p.1 p.2)) := by
  intro hcongr
  have hzero :
      pairPhaseBlindPrimitiveDifference.ZeroRel ((1, 1) : ℚ × ℚ) (1, -1) :=
    (pairPhaseBlind_iff_primitiveDifference_zeroRel 1 1 1 (-1)).mp
      (by constructor <;> norm_num)
  have hmix := hcongr ((1, 1) : ℚ × ℚ) (1, -1) hzero
  have hfst := congrArg Prod.fst hmix
  norm_num [pairDirectNormalize, pairTotal, twoRowMixWeights] at hfst

omit [Fintype ι] [DecidableEq ι] in
theorem twoRowMixWeights_normalized_no_factor_through_phaseBlindQuotient :
    ¬ (∃ F : pairPhaseBlindPrimitiveDifference.ResidualQuotient → ℚ × ℚ,
        ∀ p : ℚ × ℚ,
          F (pairPhaseBlindPrimitiveDifference.classOf p) =
            pairDirectNormalize (twoRowMixWeights p.1 p.2)) := by
  exact
    OmegaCore.PrimitiveDifference.invariantFactor_no_factor_of_not_invariant
      pairPhaseBlindPrimitiveDifference
      (fun p : ℚ × ℚ => pairDirectNormalize (twoRowMixWeights p.1 p.2))
      twoRowMixWeights_normalized_not_invariantCongruent

def pairLocalGlobalDiagnostic (p : ℚ × ℚ) : (ℚ × ℚ) × (ℚ × ℚ) :=
  (pairSquaredDirectProb p, pairDirectNormalize (twoRowMixWeights p.1 p.2))

omit [Fintype ι] [DecidableEq ι] in
theorem pairLocalGlobalDiagnostic_local_projection_factor_exists :
    ∃ F : pairPhaseBlindPrimitiveDifference.ResidualQuotient → ℚ × ℚ,
      ∀ p : ℚ × ℚ,
        F (pairPhaseBlindPrimitiveDifference.classOf p) =
          (pairLocalGlobalDiagnostic p).1 := by
  exact pairSquaredDirectProb_factor_exists

omit [Fintype ι] [DecidableEq ι] in
theorem pairLocalGlobalDiagnostic_factor_exists_iff_components_invariant :
    (∃ F :
          pairPhaseBlindPrimitiveDifference.ResidualQuotient →
            (ℚ × ℚ) × (ℚ × ℚ),
        ∀ p : ℚ × ℚ,
          F (pairPhaseBlindPrimitiveDifference.classOf p) =
            pairLocalGlobalDiagnostic p) ↔
      pairPhaseBlindPrimitiveDifference.InvariantCongruent pairSquaredDirectProb ∧
        pairPhaseBlindPrimitiveDifference.InvariantCongruent
          (fun p : ℚ × ℚ =>
            pairDirectNormalize (twoRowMixWeights p.1 p.2)) := by
  simpa [pairLocalGlobalDiagnostic] using
    (OmegaCore.PrimitiveDifference.invariantFactor_pair_exists_iff
      pairPhaseBlindPrimitiveDifference
      pairSquaredDirectProb
      (fun p : ℚ × ℚ =>
        pairDirectNormalize (twoRowMixWeights p.1 p.2)))

omit [Fintype ι] [DecidableEq ι] in
theorem pairLocalGlobalDiagnostic_no_factor_through_phaseBlindQuotient :
    ¬ (∃ F :
          pairPhaseBlindPrimitiveDifference.ResidualQuotient →
            (ℚ × ℚ) × (ℚ × ℚ),
        ∀ p : ℚ × ℚ,
          F (pairPhaseBlindPrimitiveDifference.classOf p) =
            pairLocalGlobalDiagnostic p) := by
  intro h
  exact twoRowMixWeights_normalized_not_invariantCongruent
    ((pairLocalGlobalDiagnostic_factor_exists_iff_components_invariant).mp h).2

omit [Fintype ι] [DecidableEq ι] in
theorem pairLocalGlobalDiagnostic_lggr_quotient_obstruction :
    (∃ F : pairPhaseBlindPrimitiveDifference.ResidualQuotient → ℚ × ℚ,
        ∀ p : ℚ × ℚ,
          F (pairPhaseBlindPrimitiveDifference.classOf p) =
            (pairLocalGlobalDiagnostic p).1) ∧
      ¬ (∃ F :
            pairPhaseBlindPrimitiveDifference.ResidualQuotient →
              (ℚ × ℚ) × (ℚ × ℚ),
          ∀ p : ℚ × ℚ,
            F (pairPhaseBlindPrimitiveDifference.classOf p) =
              pairLocalGlobalDiagnostic p) := by
  simpa [pairLocalGlobalDiagnostic] using
    (OmegaCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction
      pairPhaseBlindPrimitiveDifference
      pairSquaredDirectProb
      (fun p : ℚ × ℚ =>
        pairDirectNormalize (twoRowMixWeights p.1 p.2))
      pairSquaredDirectProb_invariantCongruent
      twoRowMixWeights_normalized_not_invariantCongruent)

omit [Fintype ι] [DecidableEq ι] in
theorem pairPhaseBlind_sign_flip_zeroRel (x y : ℚ) :
    pairPhaseBlindPrimitiveDifference.ZeroRel (x, y) (x, -y) := by
  exact
    (pairPhaseBlind_iff_primitiveDifference_zeroRel x y x (-y)).mp
      (by constructor <;> ring)

omit [Fintype ι] [DecidableEq ι] in
theorem pairLocalGlobalDiagnostic_sign_flip_lggr_of_mul_ne_zero
    {x y : ℚ} (hxy : x * y ≠ 0) :
    pairPhaseBlindPrimitiveDifference.ZeroRel (x, y) (x, -y) ∧
      (pairLocalGlobalDiagnostic (x, y)).1 =
        (pairLocalGlobalDiagnostic (x, -y)).1 ∧
      pairLocalGlobalDiagnostic (x, y) ≠
        pairLocalGlobalDiagnostic (x, -y) := by
  refine ⟨pairPhaseBlind_sign_flip_zeroRel x y, ?_, ?_⟩
  · simpa [pairLocalGlobalDiagnostic] using pairSquaredDirectProb_sign_flip x y
  · intro hdiag
    have hsnd := congrArg Prod.snd hdiag
    exact twoRowMixWeights_normalized_sign_flip_differs hxy
      (by simpa [pairLocalGlobalDiagnostic] using hsnd)

omit [Fintype ι] [DecidableEq ι] in
theorem pairLocalGlobalDiagnostic_sign_flip_witness_and_quotient_obstruction
    {x y : ℚ} (hxy : x * y ≠ 0) :
    (pairLocalGlobalDiagnostic (x, y)).1 =
        (pairLocalGlobalDiagnostic (x, -y)).1 ∧
      pairLocalGlobalDiagnostic (x, y) ≠
        pairLocalGlobalDiagnostic (x, -y) ∧
      (∃ F : pairPhaseBlindPrimitiveDifference.ResidualQuotient → ℚ × ℚ,
        ∀ p : ℚ × ℚ,
          F (pairPhaseBlindPrimitiveDifference.classOf p) =
            (pairLocalGlobalDiagnostic p).1) ∧
      ¬ (∃ F :
            pairPhaseBlindPrimitiveDifference.ResidualQuotient →
              (ℚ × ℚ) × (ℚ × ℚ),
          ∀ p : ℚ × ℚ,
            F (pairPhaseBlindPrimitiveDifference.classOf p) =
              pairLocalGlobalDiagnostic p) := by
  have hred :
      pairDirectNormalize (twoRowMixWeights x y) ≠
        pairDirectNormalize (twoRowMixWeights x (-y)) :=
    twoRowMixWeights_normalized_sign_flip_differs hxy
  simpa [pairLocalGlobalDiagnostic] using
    (OmegaCore.PrimitiveDifference.localGreenGlobalRed_pair_witness_and_obstruction
      pairPhaseBlindPrimitiveDifference
      pairSquaredDirectProb
      (fun p : ℚ × ℚ =>
        pairDirectNormalize (twoRowMixWeights p.1 p.2))
      pairSquaredDirectProb_invariantCongruent
      (pairPhaseBlind_sign_flip_zeroRel x y)
      hred)

omit [Fintype ι] [DecidableEq ι] in
theorem twoRowMixWeights_sign_flip_differs
    {x y : ℚ} (hxy : x * y ≠ 0) :
    twoRowMixWeights x y ≠ twoRowMixWeights x (-y) := by
  intro h
  have hfst := congrArg Prod.fst h
  have hbad : (x + y) ^ 2 = (x - y) ^ 2 := by
    simpa [twoRowMixWeights, sub_eq_add_neg] using hfst
  exact sign_phase_cross_term_varies hxy hbad

theorem sign_phase_same_weights_but_mixing_changes_descended_weights_of_mul_ne_zero
    {x y : ℚ} (hxy : x * y ≠ 0) :
    phaseBlind₂ x y x (-y) ∧
      twoRowMixWeights x y ≠ twoRowMixWeights x (-y) := by
  exact ⟨by constructor <;> ring, twoRowMixWeights_sign_flip_differs hxy⟩

theorem sign_phase_same_weights_but_mixing_changes_descended_weights :
    phaseBlind₂ (1 : ℚ) 1 1 (-1) ∧
      twoRowMixWeights 1 1 ≠ twoRowMixWeights 1 (-1) := by
  constructor
  · constructor <;> norm_num
  · intro h
    have hfst := congrArg Prod.fst h
    norm_num [twoRowMixWeights] at hfst

theorem sign_phase_mixing_redistributes_weights :
    twoRowMixWeights 1 1 = (4, 0) ∧
      twoRowMixWeights 1 (-1) = (0, 4) := by
  constructor <;> norm_num [twoRowMixWeights]

def finiteSignedSums : List ℚ → List ℚ
  | [] => [0]
  | a :: xs =>
      (finiteSignedSums xs).map (fun s => a + s) ++
        (finiteSignedSums xs).map (fun s => -a + s)

def listSquareSum (xs : List ℚ) : ℚ :=
  (xs.map (fun x => x ^ 2)).sum

theorem finiteSignedSums_length (xs : List ℚ) :
    (finiteSignedSums xs).length = 2 ^ xs.length := by
  induction xs with
  | nil => simp [finiteSignedSums]
  | cons _ xs ih =>
      simp [finiteSignedSums, ih, Nat.pow_succ]
      omega

theorem list_sum_map_const_rational (xs : List ℚ) (c : ℚ) :
    (xs.map (fun _ => c)).sum = (xs.length : ℚ) * c := by
  induction xs with
  | nil => simp
  | cons _ xs ih =>
      simp only [List.map_cons, List.sum_cons, List.length_cons, ih,
        Nat.cast_add, Nat.cast_one]
      ring

theorem finite_signed_pair_square_cancel (a : ℚ) (xs : List ℚ) :
    (xs.map (fun s => (a + s) ^ 2)).sum +
      (xs.map (fun s => (-a + s) ^ 2)).sum =
      (xs.map (fun s => 2 * a ^ 2 + 2 * s ^ 2)).sum := by
  induction xs with
  | nil => simp
  | cons s xs ih =>
      simp only [List.map_cons, List.sum_cons]
      calc
        (a + s) ^ 2 + (List.map (fun s => (a + s) ^ 2) xs).sum +
            ((-a + s) ^ 2 + (List.map (fun s => (-a + s) ^ 2) xs).sum)
            = ((a + s) ^ 2 + (-a + s) ^ 2) +
                ((List.map (fun s => (a + s) ^ 2) xs).sum +
                  (List.map (fun s => (-a + s) ^ 2) xs).sum) := by ring
        _ = (2 * a ^ 2 + 2 * s ^ 2) +
                (List.map (fun s => 2 * a ^ 2 + 2 * s ^ 2) xs).sum := by
              rw [ih]
              ring

theorem finite_signed_pair_square_cancel_listSquareSum
    (a : ℚ) (xs : List ℚ) :
    (xs.map (fun s => (a + s) ^ 2)).sum +
      (xs.map (fun s => (-a + s) ^ 2)).sum =
      (xs.length : ℚ) * (2 * a ^ 2) + 2 * listSquareSum xs := by
  rw [finite_signed_pair_square_cancel]
  calc
    (xs.map (fun s => 2 * a ^ 2 + 2 * s ^ 2)).sum =
        (xs.map (fun _ => 2 * a ^ 2)).sum +
          (xs.map (fun s => 2 * s ^ 2)).sum := by
          rw [List.sum_map_add]
    _ = (xs.length : ℚ) * (2 * a ^ 2) + 2 * listSquareSum xs := by
          rw [list_sum_map_const_rational]
          simp only [listSquareSum]
          rw [List.sum_map_mul_left]

theorem finiteSignedSums_sumSquares (xs : List ℚ) :
    listSquareSum (finiteSignedSums xs) =
      (2 : ℚ) ^ xs.length * listSquareSum xs := by
  induction xs with
  | nil => simp [finiteSignedSums, listSquareSum]
  | cons a xs ih =>
      calc
        listSquareSum (finiteSignedSums (a :: xs)) =
            (List.map (fun s => (a + s) ^ 2) (finiteSignedSums xs)).sum +
              (List.map (fun s => (-a + s) ^ 2) (finiteSignedSums xs)).sum := by
                simp [finiteSignedSums, listSquareSum, List.map_map,
                  Function.comp_def, List.sum_append]
        _ = ((finiteSignedSums xs).length : ℚ) *
              (2 * a ^ 2) + 2 * listSquareSum (finiteSignedSums xs) :=
              finite_signed_pair_square_cancel_listSquareSum a
                (finiteSignedSums xs)
        _ = (2 : ℚ) ^ (a :: xs).length * listSquareSum (a :: xs) := by
              rw [finiteSignedSums_length xs, ih]
              simp [listSquareSum]
              ring

theorem finite_rademacher_sign_average_square_identity (xs : List ℚ) :
    listSquareSum (finiteSignedSums xs) / (2 : ℚ) ^ xs.length =
      listSquareSum xs := by
  rw [finiteSignedSums_sumSquares]
  have hpow : (2 : ℚ) ^ xs.length ≠ 0 := by
    exact pow_ne_zero _ (by norm_num)
  field_simp [hpow]

theorem two_sign_phase_average_cross_terms_cancel (A B : ℚ) :
    ((A + B) ^ 2 + (A - B) ^ 2) / 2 = A ^ 2 + B ^ 2 := by
  ring

theorem independent_two_sign_phase_average_cross_terms_cancel (A B : ℚ) :
    ((A + B) ^ 2 + (A - B) ^ 2 +
      ((-A) + B) ^ 2 + ((-A) - B) ^ 2) / 4 =
      A ^ 2 + B ^ 2 := by
  ring

end

end PaperQF002
