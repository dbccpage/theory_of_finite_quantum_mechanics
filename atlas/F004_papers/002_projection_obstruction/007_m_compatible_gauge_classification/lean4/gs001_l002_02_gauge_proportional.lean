import Mathlib.Analysis.Normed.Module.Basic

/-
Target 2: Proportionality after direction independence
Once unit-sphere constancy is available, proportionality is derived.
-/

variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]

theorem gauge_proportional_tier1
  (ν : V → ℝ)
  (sphere_const : ∀ u v : V, ‖u‖ = 1 → ‖v‖ = 1 → ν u = ν v)
  (nonneg : ∀ x : V, 0 ≤ ν x)
  (homog : ∀ (a : ℝ) (x : V), ν (a • x) = ‖a‖ * ν x)
  (faithful : ∀ x : V, ν x = 0 ↔ x = 0) :
  ∃ c > 0, ∀ x, ν x = c * ‖x‖ := by
  by_cases hV : ∃ x : V, x ≠ 0
  · rcases hV with ⟨x₀, hx₀⟩
    let u₀ := (‖x₀‖⁻¹) • x₀
    have hu₀ : ‖u₀‖ = 1 := by
      rw [norm_smul, norm_inv, norm_norm, inv_mul_cancel₀]
      exact norm_ne_zero_iff.mpr hx₀
    use ν u₀
    have hu₀_ne : u₀ ≠ 0 := by
      exact norm_ne_zero_iff.mp (by rw [hu₀]; exact one_ne_zero)
    have hνu₀_ne : ν u₀ ≠ 0 := by
      intro hzero
      exact hu₀_ne ((faithful u₀).mp hzero)
    have hc : 0 < ν u₀ := lt_of_le_of_ne' (nonneg u₀) hνu₀_ne
    refine ⟨hc, fun x => ?_⟩
    rcases eq_or_ne x 0 with rfl | hx
    · have hν0 : ν (0 : V) = 0 := by
        have h := homog 0 (0 : V)
        simpa using h
      rw [hν0, norm_zero, mul_zero]
    · let u := (‖x‖⁻¹) • x
      have hu : ‖u‖ = 1 := by
        rw [norm_smul, norm_inv, norm_norm, inv_mul_cancel₀]
        exact norm_ne_zero_iff.mpr hx
      have hx_eq : x = ‖x‖ • u := by
        change x = ‖x‖ • (‖x‖⁻¹ • x)
        rw [← mul_smul, mul_inv_cancel₀, one_smul]
        exact norm_ne_zero_iff.mpr hx
      calc
        ν x = ν (‖x‖ • u) := congr_arg ν hx_eq
        _ = ‖x‖ * ν u := by rw [homog, norm_norm]
        _ = ‖x‖ * ν u₀ := by rw [sphere_const u u₀ hu hu₀]
        _ = ν u₀ * ‖x‖ := mul_comm ‖x‖ (ν u₀)
  · use 1
    constructor
    · exact zero_lt_one
    · intro x
      have hx : x = 0 := by
        by_contra hxne
        exact hV ⟨x, hxne⟩
      subst x
      have hν0 : ν (0 : V) = 0 := by
        have h := homog 0 (0 : V)
        simpa using h
      rw [hν0, norm_zero, mul_zero]
