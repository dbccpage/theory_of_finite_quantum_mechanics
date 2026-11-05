import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Analysis.Normed.Module.Dual
import Mathlib.Topology.Algebra.Module.ContinuousLinearMap.Basic

namespace PaperGS001.NormingAlias

open scoped NNReal
variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]

structure MaximalGauge (V : Type*) [NormedAddCommGroup V] [NormedSpace ℝ V] where
  j : V → ℝ
  j_nonneg : ∀ x : V, 0 ≤ j x
  j_zero_iff : ∀ x : V, j x = 0 ↔ x = 0
  j_smul : ∀ (a : ℝ) (x : V), j (a • x) = |a| * j x
  j_add_le : ∀ x y : V, j (x + y) ≤ j x + j y
  j_compat : ∀ (T : V →L[ℝ] V) (x : V), j (T x) ≤ ‖T‖ * j x

namespace MaximalGauge

variable (G : MaximalGauge V)

lemma j_zero : G.j 0 = 0 := by
  have h := G.j_smul 0 (0 : V)
  simp [abs_zero, zero_mul] at h
  exact h

lemma j_pos {x : V} (hx : x ≠ 0) : 0 < G.j x := by
  rcases lt_or_eq_of_le (G.j_nonneg x) with h | h
  · exact h
  · exfalso; exact hx ((G.j_zero_iff x).mp h.symm)

theorem direction_independence_tier1
    (norming : ∀ u : V, ‖u‖ = 1 → ∃ f : V →L[ℝ] ℝ, ‖f‖ = 1 ∧ f u = 1)
    {u v : V} (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    G.j u = G.j v := by
  have H_le : ∀ u v : V, ‖u‖ = 1 → ‖v‖ = 1 → G.j v ≤ G.j u := by
    intro u v hu hv
    rcases norming u hu with ⟨f, hf_norm, hf_u⟩
    let T : V →L[ℝ] V := f.smulRight v
    have hT_u : T u = v := by
      change f u • v = v
      rw [hf_u, one_smul]
    have hT_norm : ‖T‖ ≤ 1 := by
      have eq1 : ‖T‖ = ‖f‖ * ‖v‖ := ContinuousLinearMap.norm_smulRight_apply f v
      rw [eq1, hf_norm, hv, one_mul]
    have step1 := G.j_compat T u
    rw [hT_u] at step1
    calc
      G.j v ≤ ‖T‖ * G.j u := step1
      _ ≤ 1 * G.j u := mul_le_mul_of_nonneg_right hT_norm (G.j_nonneg u)
      _ = G.j u := one_mul (G.j u)
  exact le_antisymm (H_le v u hv hu) (H_le u v hu hv)

theorem gauge_proportional_tier1
    (norming : ∀ u : V, ‖u‖ = 1 →
      ∃ f : V →L[ℝ] ℝ, ‖f‖ = 1 ∧ f u = 1)
    (hV : ∃ x : V, x ≠ 0) :
    ∃ c : ℝ, 0 < c ∧ ∀ x : V, G.j x = c * ‖x‖ := by
  rcases hV with ⟨x₀, hx₀⟩
  let u₀ := (‖x₀‖⁻¹) • x₀
  have hu₀ : ‖u₀‖ = 1 := by
    rw [norm_smul, norm_inv, norm_norm, inv_mul_cancel₀]
    exact norm_ne_zero_iff.mpr hx₀
  use G.j u₀
  have hc : 0 < G.j u₀ := G.j_pos (norm_ne_zero_iff.mp (by rw [hu₀]; norm_num))
  refine ⟨hc, fun x => ?_⟩
  rcases eq_or_ne x 0 with rfl | hx
  · rw [G.j_zero, norm_zero, mul_zero]
  · let u := (‖x‖⁻¹) • x
    have hu : ‖u‖ = 1 := by
      rw [norm_smul, norm_inv, norm_norm, inv_mul_cancel₀]
      exact norm_ne_zero_iff.mpr hx
    have hx_eq : x = ‖x‖ • u := by
      change x = ‖x‖ • (‖x‖⁻¹ • x)
      rw [← mul_smul, mul_inv_cancel₀, one_smul]
      exact norm_ne_zero_iff.mpr hx
    have h_norm_pos : 0 < ‖x‖ := norm_pos_iff.mpr hx
    calc
      G.j x = G.j (‖x‖ • u) := congr_arg G.j hx_eq
      _ = ‖x‖ * G.j u := by rw [G.j_smul, abs_of_pos h_norm_pos]
      _ = ‖x‖ * G.j u₀ := by rw [direction_independence_tier1 G norming hu hu₀]
      _ = G.j u₀ * ‖x‖ := mul_comm ‖x‖ (G.j u₀)

end MaximalGauge

end PaperGS001.NormingAlias
