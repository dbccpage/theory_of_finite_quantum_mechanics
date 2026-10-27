
import PrimitiveRepairWitness


namespace ObstructionCore
namespace PrimitiveAdmissibleRepair

universe u v

variable {Q : Type u}
variable {α : Type u} {β : Type v}

structure AdmissibleRepairSystem (Q : Type u) where
  admissible : (Q → Q) → Prop

def AdmissibleRepair (S : AdmissibleRepairSystem Q) (r : Q → Q) : Prop :=
  S.admissible r

structure AdmissibleRepairWitness
    (S : AdmissibleRepairSystem Q) (zeroClass : Q) (q : Q) where
  repair : Q → Q
  admissible_repair : AdmissibleRepair S repair
  repairs_to_zero : repair q = zeroClass

def AdmissibleWitnessedExactRepair
    (C : ObstructionClassifier Q)
    (S : AdmissibleRepairSystem Q) (zeroClass : Q) (q : Q) : Prop :=
  C.IsExactRepair q ∧ Nonempty (AdmissibleRepairWitness S zeroClass q)

def constantZeroRepair (zeroClass : Q) : Q → Q :=
  fun _ => zeroClass

def NoTrivialRepairCollapse
    (S : AdmissibleRepairSystem Q) (zeroClass : Q) : Prop :=
  ¬ AdmissibleRepair S (constantZeroRepair zeroClass)

def RepairCost (Q : Type u) :=
  (Q → Q) → Nat

def BudgetAdmissible
    (S : AdmissibleRepairSystem Q) (cost : RepairCost Q)
    (budget : Nat) (repair : Q → Q) : Prop :=
  AdmissibleRepair S repair ∧ cost repair ≤ budget

theorem budgetAdmissible_implies_admissible
    (S : AdmissibleRepairSystem Q) (cost : RepairCost Q)
    (budget : Nat) (repair : Q → Q) :
    BudgetAdmissible S cost budget repair → AdmissibleRepair S repair :=
  fun h => h.1

theorem admissibleRepairWitness_implies_repairWitness
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (S : AdmissibleRepairSystem (PointedResidualQuotient P))
    (q : PointedResidualQuotient P)
    (w : AdmissibleRepairWitness S P.zeroClass q) :
    PrimitiveRepairWitness.ExactRepairHasWitness P C w.repair q :=
  ⟨{
    repaired := w.repair q
    original_eq := rfl
    repair_eq := w.repairs_to_zero
  }⟩

theorem admissibleWitnessedExactRepair_implies_witnessedExactRepair
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (S : AdmissibleRepairSystem (PointedResidualQuotient P))
    (q : PointedResidualQuotient P) :
    AdmissibleWitnessedExactRepair C S P.zeroClass q →
      ∃ r : PrimitiveRepairWitness.RepairMap P,
        PrimitiveRepairWitness.WitnessedExactRepair P C r q := by
  intro h
  cases h.2 with
  | intro w =>
      exact ⟨w.repair, ⟨h.1,
        admissibleRepairWitness_implies_repairWitness P C S q w⟩⟩

theorem admissibleWitnessedExactRepair_implies_exact
    (C : ObstructionClassifier Q)
    (S : AdmissibleRepairSystem Q) (zeroClass : Q) (q : Q) :
    AdmissibleWitnessedExactRepair C S zeroClass q → C.IsExactRepair q :=
  fun h => h.1

theorem constantZeroRepair_inadmissible_blocks_constant_zero_witness
    (S : AdmissibleRepairSystem Q) (zeroClass : Q) (q : Q)
    (hnot : ¬ AdmissibleRepair S (constantZeroRepair zeroClass)) :
    ¬ (∃ w : AdmissibleRepairWitness S zeroClass q,
        w.repair = constantZeroRepair zeroClass) := by
  intro h
  rcases h with ⟨w, hw⟩
  exact hnot (hw ▸ w.admissible_repair)

theorem noTrivialRepairCollapse_blocks_constant_zero_witness
    (S : AdmissibleRepairSystem Q) (zeroClass : Q) (q : Q) :
    NoTrivialRepairCollapse S zeroClass →
      ¬ (∃ w : AdmissibleRepairWitness S zeroClass q,
          w.repair = constantZeroRepair zeroClass) :=
  constantZeroRepair_inadmissible_blocks_constant_zero_witness S zeroClass q

end PrimitiveAdmissibleRepair
end ObstructionCore

private def l5aProvenance : String :=
  "Origin: lean4/PrimitiveAdmissibleRepair.lean Claim: budgetAdmissible_implies_admissible AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
