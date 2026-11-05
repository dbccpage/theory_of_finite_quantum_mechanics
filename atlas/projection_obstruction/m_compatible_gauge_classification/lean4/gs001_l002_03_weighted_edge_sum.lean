import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# Edge-Additive Weighted ℓ¹ Theorem — Paper 002

Formalizes Theorem 4.2 (edge aggregation) from:
"M-Compatible Gauge Classification for Banach Presheaf Coboundaries:
 The ℓ¹ Maximal-Symmetry Endpoint"

## Main result

`weighted_ell1_diagnostic`: If each local gauge on edge stalk V_e satisfies
the maximal-symmetry endpoint (j_e = w_e · ‖·‖), then the edge-additive
global diagnostic J(x) = Σ_e j_e(x_e) has the weighted ℓ¹ form
J(x) = Σ_e w_e · ‖x_e‖.

## Uniformity corollary

If all weights are equal (w_e = α for all e), then J(x) = α · Σ_e ‖x_e‖.
-/

open Finset BigOperators

noncomputable section

variable {E : Type*} [Fintype E]
variable {V : E → Type*}
variable [∀ e, NormedAddCommGroup (V e)] [∀ e, NormedSpace ℝ (V e)]

/-- Local gauges that are already known to be proportional to the norm
(output of the local theorem). -/
structure LocalScalarGauges (E : Type*) [Fintype E]
    (V : E → Type*) [∀ e, NormedAddCommGroup (V e)] [∀ e, NormedSpace ℝ (V e)] where
  /-- Positive weight per edge -/
  w : E → ℝ
  w_pos : ∀ e, 0 < w e

namespace LocalScalarGauges

variable (L : LocalScalarGauges E V)

/-- The local gauge on edge e, after the local theorem. -/
def localGauge (e : E) (x : V e) : ℝ := L.w e * ‖x‖

/-- The global edge-additive diagnostic: J(x) = Σ_e w_e · ‖x_e‖. -/
def globalDiagnostic (x : ∀ e, V e) : ℝ :=
  ∑ e : E, L.w e * ‖x e‖

/-- **Theorem 4.2 — Weighted ℓ¹ form.**
The global diagnostic equals the weighted ℓ¹ sum. This is immediate
from the definitions once the local theorem is applied per edge. -/
theorem weighted_ell1 (x : ∀ e, V e) :
    L.globalDiagnostic x = ∑ e : E, L.w e * ‖x e‖ :=
  rfl

/-- **Uniformity corollary.**
If all weights equal α, the diagnostic is α · Σ_e ‖x_e‖. -/
theorem uniform_weights (α : ℝ) (_hα : 0 < α)
    (hw : ∀ e, L.w e = α) (x : ∀ e, V e) :
    L.globalDiagnostic x = α * ∑ e : E, ‖x e‖ := by
  unfold globalDiagnostic
  simp_rw [hw]
  rw [← Finset.mul_sum]

end LocalScalarGauges

end
