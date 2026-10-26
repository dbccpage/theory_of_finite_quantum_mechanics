/-
Paper 002, Tier 8: weighted-to-unweighted transition.

Once the maximal-symmetry endpoint has produced a positive scalar weight per
edge, the unweighted global l1 diagnostic is licensed only when those weights
are constant, or when a single edge orbit plus invariance forces constancy.
-/

import «gs001_l002_03_weighted_edge_sum»
import «gs001_l002_04_uniform_weights»

namespace PaperGS001

open Finset BigOperators

noncomputable section

variable {E : Type*} [Fintype E]
variable {V : E → Type*}
variable [∀ e, NormedAddCommGroup (V e)] [∀ e, NormedSpace ℝ (V e)]

theorem weighted_sum_eq_scalar_l1_of_uniform_weights
    (L : LocalScalarGauges E V)
    (α : ℝ)
    (hw : ∀ e, L.w e = α)
    (x : ∀ e, V e) :
    L.globalDiagnostic x = α * ∑ e : E, ‖x e‖ := by
  unfold LocalScalarGauges.globalDiagnostic
  simp_rw [hw]
  rw [← Finset.mul_sum]

theorem weighted_sum_eq_scalar_l1_of_single_orbit_weights
    (L : LocalScalarGauges E V)
    (SameOrbit : E → E → Prop)
    (orbit : ∀ e₁ e₂, SameOrbit e₁ e₂)
    (invariance : ∀ e₁ e₂, SameOrbit e₁ e₂ → L.w e₁ = L.w e₂) :
    ∃ α : ℝ, ∀ x : ∀ e, V e,
      L.globalDiagnostic x = α * ∑ e : E, ‖x e‖ := by
  rcases uniform_weights_on_single_orbit SameOrbit L.w orbit invariance with
    ⟨α, hw⟩
  exact
    ⟨α, fun x =>
      weighted_sum_eq_scalar_l1_of_uniform_weights L α hw x⟩

#print axioms PaperGS001.weighted_sum_eq_scalar_l1_of_uniform_weights
#print axioms PaperGS001.weighted_sum_eq_scalar_l1_of_single_orbit_weights

end

end PaperGS001
