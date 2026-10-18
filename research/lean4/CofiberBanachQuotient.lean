/-
  CofiberBanachQuotient.lean
  Mechanization in Lean 4 of the analytic identity Φ₁([x]) = ‖[x]‖_quot
  using Mathlib's normed group quotient infrastructure (Mathlib.Analysis.Normed.Group.Quotient)
  and finite-dimensional subspace closedness (Submodule.closed_of_finiteDimensional).

  AuthorityEffect: None.
  Replaces the store/read definition (QM-002 / O022a / ENC-1077 / PL-QM007-2).
-/
import Mathlib.Analysis.Normed.Group.Quotient
import Mathlib.Topology.Algebra.Module.FiniteDimension
import Mathlib.Analysis.Normed.Module.FiniteDimension

set_option linter.unusedSectionVars false

open Metric Set

namespace QuantumMechanics.BanachQuotient

variable {𝕜 : Type*} [NontriviallyNormedField 𝕜] [CompleteSpace 𝕜]
variable {C0 C1 : Type*} [NormedAddCommGroup C0] [NormedSpace 𝕜 C0]
variable [NormedAddCommGroup C1] [NormedSpace 𝕜 C1]

/-- The repair functional Φ₁(x): the infimum distance from a 1-cochain x ∈ C₁
    to the boundary subspace im(d₀) ⊆ C₁. -/
noncomputable def repairFunctional (d0 : C0 →ₗ[𝕜] C1) (x : C1) : ℝ :=
  Metric.infDist x (LinearMap.range d0 : Set C1)

/-- 1. Topological closure invariance: the infimum distance to a subspace
    equals the infimum distance to its topological closure. -/
theorem repair_infDist_closure (d0 : C0 →ₗ[𝕜] C1) (x : C1) :
    Metric.infDist x (closure (LinearMap.range d0 : Set C1)) =
    repairFunctional d0 x := by
  rw [Metric.infDist_closure]
  rfl

/-- 2. Analytic quotient norm identity: the repair functional Φ₁([x])
    equals the Mathlib normed quotient norm ‖[x]‖_quot
    on C₁ ⧸ im(d₀). -/
theorem phi1_eq_quotient_norm (d0 : C0 →ₗ[𝕜] C1) (x : C1) :
    repairFunctional d0 x =
    ‖(QuotientAddGroup.mk x : C1 ⧸ (LinearMap.range d0).toAddSubgroup)‖ := by
  rw [QuotientAddGroup.norm_mk]
  rfl

/-- 2b. Formulated on Submodule.Quotient: the repair functional Φ₁([x])
    equals the norm of the canonical submodule projection Submodule.Quotient.mk x. -/
theorem phi1_eq_submodule_quotient_norm (d0 : C0 →ₗ[𝕜] C1) (x : C1) :
    repairFunctional d0 x =
    ‖(Submodule.Quotient.mk x : C1 ⧸ LinearMap.range d0)‖ := by
  change repairFunctional d0 x = ‖(QuotientAddGroup.mk x : C1 ⧸ (LinearMap.range d0).toAddSubgroup)‖
  rw [QuotientAddGroup.norm_mk]
  rfl

set_option linter.unusedSectionVars false

/-- 3. Exact separation / solvability in finite dimension:
    a 1-cochain has zero quotient norm if and only if it is an exact boundary (x ∈ im(d₀)).
    This uses topological closedness of finite-dimensional subspaces (`Submodule.closed_of_finiteDimensional`). -/
theorem quotient_norm_eq_zero_iff_exact_repair (d0 : C0 →ₗ[𝕜] C1)
    [FiniteDimensional 𝕜 (LinearMap.range d0)] (x : C1) :
    ‖(QuotientAddGroup.mk x : C1 ⧸ (LinearMap.range d0).toAddSubgroup)‖ = 0 ↔
    x ∈ LinearMap.range d0 := by
  have hclosed : IsClosed ((LinearMap.range d0).toAddSubgroup : Set C1) :=
    Submodule.closed_of_finiteDimensional (LinearMap.range d0)
  exact QuotientAddGroup.norm_mk_eq_zero (hS := hclosed)

/-- 3b. Exact separation on Submodule.Quotient. -/
theorem submodule_quotient_norm_eq_zero_iff_exact_repair (d0 : C0 →ₗ[𝕜] C1)
    [FiniteDimensional 𝕜 (LinearMap.range d0)] (x : C1) :
    ‖(Submodule.Quotient.mk x : C1 ⧸ LinearMap.range d0)‖ = 0 ↔
    x ∈ LinearMap.range d0 := by
  exact quotient_norm_eq_zero_iff_exact_repair d0 x

#print axioms repair_infDist_closure
#print axioms phi1_eq_quotient_norm
#print axioms phi1_eq_submodule_quotient_norm
#print axioms quotient_norm_eq_zero_iff_exact_repair
#print axioms submodule_quotient_norm_eq_zero_iff_exact_repair

end QuantumMechanics.BanachQuotient
