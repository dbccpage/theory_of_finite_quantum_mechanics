import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Analysis.Normed.Operator.Basic

/-
Target 1: Direction independence under norming functional
This remains the primary Paper 002 Lean target.
-/

variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]

theorem direction_independence_tier1
  (ν : V → ℝ)
  (norming : ∀ u, ‖u‖ = 1 → ∃ f : V →L[ℝ] ℝ, ‖f‖ ≤ 1 ∧ f u = 1)
  (compat : ∀ (T : V →L[ℝ] V) (x : V), ν (T x) ≤ ‖T‖ * ν x)
  (nonneg : ∀ x : V, 0 ≤ ν x)
  (_homog : ∀ (a : ℝ) (x : V), ν (a • x) = ‖a‖ * ν x)
  {u v : V}
  (hu : ‖u‖ = 1)
  (hv : ‖v‖ = 1) :
  ν u = ν v := by
  have H_le : ∀ u v : V, ‖u‖ = 1 → ‖v‖ = 1 → ν v ≤ ν u := by
    intro u v hu hv
    rcases norming u hu with ⟨f, hf_norm_le, hf_u⟩
    let T : V →L[ℝ] V := f.smulRight v
    have hT_u : T u = v := by
      change f u • v = v
      rw [hf_u, one_smul]
    have hT_norm : ‖T‖ ≤ 1 := by
      refine ContinuousLinearMap.opNorm_le_bound T zero_le_one ?_
      intro x
      change ‖f x • v‖ ≤ 1 * ‖x‖
      rw [norm_smul, hv, mul_one, one_mul]
      simpa [one_mul] using
        (f.le_opNorm x).trans
          (mul_le_mul_of_nonneg_right hf_norm_le (norm_nonneg x))
    have step := compat T u
    rw [hT_u] at step
    calc
      ν v ≤ ‖T‖ * ν u := step
      _ ≤ 1 * ν u := mul_le_mul_of_nonneg_right hT_norm (nonneg u)
      _ = ν u := one_mul (ν u)
  exact le_antisymm (H_le v u hv hu) (H_le u v hu hv)
