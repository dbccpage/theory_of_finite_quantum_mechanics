import PrimitiveRepairCertificate
/-!
Primitive repair boundary kernel.

This file records the distinction between exact classifier status and the
presence of a repair certificate.
-/

namespace OmegaCore
namespace PrimitiveRepairBoundary

universe u

variable {Q : Type u}

inductive RepairBoundaryStatus where
  | repaired
  | noRule
  | budgetUnknown
  | refused
  deriving DecidableEq, Repr

structure RepairBoundaryInput where
  hasRule : Bool
  withinBudget : Bool
  policyAllowed : Bool
  hasAdmissibleWitness : Bool

def repairBoundaryDecision :
    RepairBoundaryInput → RepairBoundaryStatus :=
  fun input =>
    if input.policyAllowed = false then
      RepairBoundaryStatus.refused
    else if input.hasRule = false then
      RepairBoundaryStatus.noRule
    else if input.withinBudget = false then
      RepairBoundaryStatus.budgetUnknown
    else if input.hasAdmissibleWitness = true then
      RepairBoundaryStatus.repaired
    else
      RepairBoundaryStatus.noRule

theorem policy_failure_routes_refused
    (input : RepairBoundaryInput)
    (hPolicy : input.policyAllowed = false) :
    repairBoundaryDecision input = RepairBoundaryStatus.refused := by
  cases input with
  | mk hasRule withinBudget policyAllowed hasAdmissibleWitness =>
      cases policyAllowed
      · rfl
      · cases hPolicy

theorem missing_rule_routes_noRule
    (input : RepairBoundaryInput)
    (hPolicy : input.policyAllowed = true)
    (hRule : input.hasRule = false) :
    repairBoundaryDecision input = RepairBoundaryStatus.noRule := by
  cases input with
  | mk hasRule withinBudget policyAllowed hasAdmissibleWitness =>
      cases policyAllowed
      · cases hPolicy
      · cases hasRule
        · rfl
        · cases hRule

theorem budget_failure_routes_budgetUnknown
    (input : RepairBoundaryInput)
    (hPolicy : input.policyAllowed = true)
    (hRule : input.hasRule = true)
    (hBudget : input.withinBudget = false) :
    repairBoundaryDecision input = RepairBoundaryStatus.budgetUnknown := by
  cases input with
  | mk hasRule withinBudget policyAllowed hasAdmissibleWitness =>
      cases policyAllowed
      · cases hPolicy
      · cases hasRule
        · cases hRule
        · cases withinBudget
          · rfl
          · cases hBudget

theorem admissible_witness_routes_repaired
    (input : RepairBoundaryInput)
    (hPolicy : input.policyAllowed = true)
    (hRule : input.hasRule = true)
    (hBudget : input.withinBudget = true)
    (hWitness : input.hasAdmissibleWitness = true) :
    repairBoundaryDecision input = RepairBoundaryStatus.repaired := by
  cases input with
  | mk hasRule withinBudget policyAllowed hasAdmissibleWitness =>
      cases policyAllowed
      · cases hPolicy
      · cases hasRule
        · cases hRule
        · cases withinBudget
          · cases hBudget
          · cases hasAdmissibleWitness
            · cases hWitness
            · rfl

theorem repaired_requires_policy_rule_budget_and_witness
    (input : RepairBoundaryInput)
    (hRepaired :
      repairBoundaryDecision input = RepairBoundaryStatus.repaired) :
    input.policyAllowed = true ∧
      input.hasRule = true ∧
      input.withinBudget = true ∧
      input.hasAdmissibleWitness = true := by
  cases input with
  | mk hasRule withinBudget policyAllowed hasAdmissibleWitness =>
      cases policyAllowed
      · cases hRepaired
      · cases hasRule
        · cases hRepaired
        · cases withinBudget
          · cases hRepaired
          · cases hasAdmissibleWitness
            · cases hRepaired
            · exact ⟨rfl, rfl, rfl, rfl⟩

theorem repairBoundary_repaired_iff
    (input : RepairBoundaryInput) :
    repairBoundaryDecision input = RepairBoundaryStatus.repaired ↔
      input.policyAllowed = true ∧
      input.hasRule = true ∧
      input.withinBudget = true ∧
      input.hasAdmissibleWitness = true := by
  constructor
  · exact repaired_requires_policy_rule_budget_and_witness input
  · intro h
    exact admissible_witness_routes_repaired
      input h.1 h.2.1 h.2.2.1 h.2.2.2

theorem repairBoundary_refused_iff
    (input : RepairBoundaryInput) :
    repairBoundaryDecision input = RepairBoundaryStatus.refused ↔
      input.policyAllowed = false := by
  cases input with
  | mk hasRule withinBudget policyAllowed hasAdmissibleWitness =>
      cases policyAllowed <;>
        cases hasRule <;>
        cases withinBudget <;>
        cases hasAdmissibleWitness <;>
        decide

theorem repairBoundary_budgetUnknown_iff
    (input : RepairBoundaryInput) :
    repairBoundaryDecision input = RepairBoundaryStatus.budgetUnknown ↔
      input.policyAllowed = true ∧
      input.hasRule = true ∧
      input.withinBudget = false := by
  cases input with
  | mk hasRule withinBudget policyAllowed hasAdmissibleWitness =>
      cases policyAllowed <;>
        cases hasRule <;>
        cases withinBudget <;>
        cases hasAdmissibleWitness <;>
        decide

theorem repairBoundary_noRule_iff
    (input : RepairBoundaryInput) :
    repairBoundaryDecision input = RepairBoundaryStatus.noRule ↔
      (input.policyAllowed = true ∧ input.hasRule = false) ∨
      (input.policyAllowed = true ∧
        input.hasRule = true ∧
        input.withinBudget = true ∧
        input.hasAdmissibleWitness = false) := by
  cases input with
  | mk hasRule withinBudget policyAllowed hasAdmissibleWitness =>
      cases policyAllowed <;>
        cases hasRule <;>
        cases withinBudget <;>
        cases hasAdmissibleWitness <;>
        decide

theorem refused_not_repaired :
    RepairBoundaryStatus.refused ≠ RepairBoundaryStatus.repaired := by
  decide

theorem noRule_not_repaired :
    RepairBoundaryStatus.noRule ≠ RepairBoundaryStatus.repaired := by
  decide

theorem budgetUnknown_not_repaired :
    RepairBoundaryStatus.budgetUnknown ≠ RepairBoundaryStatus.repaired := by
  decide

def ExactStatusNoCertificate
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q) : Prop :=
  C.IsExactRepair q ∧
    ¬ PrimitiveRepairCertificate.HasRepairCertificate C S zeroClass q

theorem exactStatusNoCertificate_implies_exact
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q) :
    ExactStatusNoCertificate C S zeroClass q → C.IsExactRepair q :=
  fun h => h.1

theorem exactStatusNoCertificate_implies_no_certificate
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q) :
    ExactStatusNoCertificate C S zeroClass q →
      ¬ PrimitiveRepairCertificate.HasRepairCertificate C S zeroClass q :=
  fun h => h.2

theorem certificate_excludes_exactStatusNoCertificate
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (cert : PrimitiveRepairCertificate.RepairCertificate C S zeroClass q) :
    ¬ ExactStatusNoCertificate C S zeroClass q := by
  intro h
  exact h.2 ⟨cert⟩

def emptyRepairSystem (Q : Type u) :
    PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q where
  admissible := fun _ => False

theorem no_certificate_under_empty_system
    (C : ObstructionClassifier Q) (zeroClass : Q) (q : Q) :
    ¬ PrimitiveRepairCertificate.HasRepairCertificate
      C (emptyRepairSystem Q) zeroClass q := by
  intro h
  cases h with
  | intro cert =>
      exact cert.witness.admissible_repair

theorem exact_status_without_certificate_under_empty_system
    (C : ObstructionClassifier Q) (zeroClass : Q) (q : Q)
    (hExact : C.IsExactRepair q) :
    ExactStatusNoCertificate C (emptyRepairSystem Q) zeroClass q :=
  ⟨hExact, no_certificate_under_empty_system C zeroClass q⟩

end PrimitiveRepairBoundary
end OmegaCore
