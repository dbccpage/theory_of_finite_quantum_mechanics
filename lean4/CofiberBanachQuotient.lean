
import Mathlib.Analysis.Normed.Group.Quotient
import Mathlib.Topology.Algebra.Module.FiniteDimension
import Mathlib.Analysis.Normed.Module.FiniteDimension

set_option linter.unusedSectionVars false

open Metric Set

namespace QuantumMechanics.BanachQuotient

variable {𝕜 : Type*} [NontriviallyNormedField 𝕜] [CompleteSpace 𝕜]
variable {C0 C1 : Type*} [NormedAddCommGroup C0] [NormedSpace 𝕜 C0]
variable [NormedAddCommGroup C1] [NormedSpace 𝕜 C1]

noncomputable def repairFunctional (d0 : C0 →ₗ[𝕜] C1) (x : C1) : ℝ :=
  Metric.infDist x (LinearMap.range d0 : Set C1)

theorem repair_infDist_closure (d0 : C0 →ₗ[𝕜] C1) (x : C1) :
    Metric.infDist x (closure (LinearMap.range d0 : Set C1)) =
    repairFunctional d0 x := by
  rw [Metric.infDist_closure]
  rfl

theorem phi1_eq_quotient_norm (d0 : C0 →ₗ[𝕜] C1) (x : C1) :
    repairFunctional d0 x =
    ‖(QuotientAddGroup.mk x : C1 ⧸ (LinearMap.range d0).toAddSubgroup)‖ := by
  rw [QuotientAddGroup.norm_mk]
  rfl

theorem phi1_eq_submodule_quotient_norm (d0 : C0 →ₗ[𝕜] C1) (x : C1) :
    repairFunctional d0 x =
    ‖(Submodule.Quotient.mk x : C1 ⧸ LinearMap.range d0)‖ := by
  change repairFunctional d0 x = ‖(QuotientAddGroup.mk x : C1 ⧸ (LinearMap.range d0).toAddSubgroup)‖
  rw [QuotientAddGroup.norm_mk]
  rfl

set_option linter.unusedSectionVars false

theorem quotient_norm_eq_zero_iff_exact_repair (d0 : C0 →ₗ[𝕜] C1)
    [FiniteDimensional 𝕜 (LinearMap.range d0)] (x : C1) :
    ‖(QuotientAddGroup.mk x : C1 ⧸ (LinearMap.range d0).toAddSubgroup)‖ = 0 ↔
    x ∈ LinearMap.range d0 := by
  have hclosed : IsClosed ((LinearMap.range d0).toAddSubgroup : Set C1) :=
    Submodule.closed_of_finiteDimensional (LinearMap.range d0)
  exact QuotientAddGroup.norm_mk_eq_zero (hS := hclosed)

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

private def l5aProvenance : String :=
  "Origin: lean4/CofiberBanachQuotient.lean Claim: repair_infDist_closure AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
