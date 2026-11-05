import Mathlib.Data.Real.Basic

/-
Target 4: Uniform weights under single orbit
Formalizes the finite orbit statement.
-/

variable {Edge : Type*}
variable (SameOrbit : Edge → Edge → Prop)
variable (w : Edge → ℝ)

theorem uniform_weights_on_single_orbit
  (orbit : ∀ e₁ e₂, SameOrbit e₁ e₂)
  (invariance : ∀ e₁ e₂, SameOrbit e₁ e₂ → w e₁ = w e₂) :
  ∃ α, ∀ e, w e = α := by
  by_cases h : Nonempty Edge
  · rcases h with ⟨e₀⟩
    exact ⟨w e₀, fun e => invariance e e₀ (orbit e e₀)⟩
  · exact ⟨0, fun e => False.elim (h ⟨e⟩)⟩
