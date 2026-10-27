
import PrimitiveObstructionPipeline


namespace ObstructionCore
namespace PrimitiveRepairWitness

universe u v

variable {α : Type u} {β : Type v}

abbrev RepairMap (P : PointedPrimitiveDifference α β) :=
  PointedResidualQuotient P → PointedResidualQuotient P

def RepairsToZero
    (P : PointedPrimitiveDifference α β)
    (_C : ObstructionClassifier (PointedResidualQuotient P))
    (r : RepairMap P) (q : PointedResidualQuotient P) : Prop :=
  r q = P.zeroClass

structure RepairWitness
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (r : RepairMap P) (q : PointedResidualQuotient P) where
  repaired : PointedResidualQuotient P
  original_eq : repaired = r q
  repair_eq : repaired = P.zeroClass

def ExactRepairStatusOnly
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (q : PointedResidualQuotient P) : Prop :=
  C.IsExactRepair q

def ExactRepairHasWitness
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (r : RepairMap P) (q : PointedResidualQuotient P) : Prop :=
  Nonempty (RepairWitness P C r q)

def WitnessedExactRepair
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (r : RepairMap P) (q : PointedResidualQuotient P) : Prop :=
  C.IsExactRepair q ∧ ExactRepairHasWitness P C r q

theorem repairWitness_implies_repaired_zero
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (r : RepairMap P) (q : PointedResidualQuotient P)
    (w : RepairWitness P C r q) :
    w.repaired = P.zeroClass :=
  w.repair_eq

theorem witnessedExactRepair_implies_exact
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (r : RepairMap P) (q : PointedResidualQuotient P) :
    WitnessedExactRepair P C r q → C.IsExactRepair q :=
  fun h => h.1

theorem exactRepair_status_without_witness_is_only_classifier
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (q : PointedResidualQuotient P) :
    C.IsExactRepair q → ExactRepairStatusOnly P C q :=
  fun h => h

theorem repairMap_repairs_to_zero_gives_witness
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (r : RepairMap P) (q : PointedResidualQuotient P)
    (hrepair : RepairsToZero P C r q) :
    ExactRepairHasWitness P C r q :=
  ⟨{
    repaired := r q
    original_eq := rfl
    repair_eq := hrepair
  }⟩

def identityRepairMap (P : PointedPrimitiveDifference α β) : RepairMap P :=
  fun q => q

def boolSeparatedPointed : PointedPrimitiveDifference Bool Bool where
  δ := fun x y =>
    match x, y with
    | false, false => false
    | true, true => false
    | _, _ => true
  Zero := fun b => b = false
  zero_refl := by
    intro x
    cases x <;> rfl
  zero_symm := by
    intro x y hxy
    cases x <;> cases y <;> simp at hxy ⊢
  zero_trans := by
    intro x y z hxy hyz
    cases x <;> cases y <;> cases z <;> simp at hxy hyz ⊢
  zero := false

def boolTrueClass : PointedResidualQuotient boolSeparatedPointed :=
  PrimitiveDifference.classOf boolSeparatedPointed.toPrimitiveDifference true

def boolZeroClassifier :
    ObstructionClassifier (PointedResidualQuotient boolSeparatedPointed) where
  Phi := fun _ => 0
  Gamma := fun _ => 0

theorem boolTrueClass_ne_zeroClass :
    boolTrueClass ≠ boolSeparatedPointed.zeroClass := by
  intro hclass
  have hrel :
      boolSeparatedPointed.toPrimitiveDifference.ZeroRel true false :=
    Quotient.exact hclass
  simp [boolSeparatedPointed, PrimitiveDifference.ZeroRel] at hrel

theorem bool_exact_without_identity_repair_witness :
    boolZeroClassifier.IsExactRepair boolTrueClass ∧
      ¬ ExactRepairHasWitness
        boolSeparatedPointed
        boolZeroClassifier
        (identityRepairMap boolSeparatedPointed)
        boolTrueClass := by
  constructor
  · rfl
  · intro h
    cases h with
    | intro w =>
        have hq : boolTrueClass = boolSeparatedPointed.zeroClass :=
          w.original_eq.symm.trans w.repair_eq
        exact boolTrueClass_ne_zeroClass hq

end PrimitiveRepairWitness
end ObstructionCore

private def l5aProvenance : String :=
  "Origin: lean4/PrimitiveRepairWitness.lean Claim: repairWitness_implies_repaired_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
