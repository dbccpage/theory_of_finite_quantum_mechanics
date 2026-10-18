import PrimitiveAdmissibleRepair
/-!
Primitive repair certificate kernel.

This file packages exact status together with an admissible repair witness.
-/

namespace OmegaCore
namespace PrimitiveRepairCertificate

universe u v

variable {Q : Type u}
variable {α : Type u} {β : Type v}

structure RepairCertificate
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q) where
  exact_status : C.IsExactRepair q
  witness : PrimitiveAdmissibleRepair.AdmissibleRepairWitness S zeroClass q

def HasRepairCertificate
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q) : Prop :=
  Nonempty (RepairCertificate C S zeroClass q)

def CertificateHasAdmissibleRepair
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (cert : RepairCertificate C S zeroClass q) : Prop :=
  PrimitiveAdmissibleRepair.AdmissibleRepair S cert.witness.repair

def CertificateRepairsToZero
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (cert : RepairCertificate C S zeroClass q) : Prop :=
  cert.witness.repair q = zeroClass

def CertificateMatchesClassifier
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (_cert : RepairCertificate C S zeroClass q) : Prop :=
  C.IsExactRepair q

def ExactStatusOnly (C : ObstructionClassifier Q) (q : Q) : Prop :=
  C.IsExactRepair q

def certificateEmptyRepairSystem (Q : Type u) :
    PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q where
  admissible := fun _ => False

theorem certificate_implies_exact
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (cert : RepairCertificate C S zeroClass q) :
    C.IsExactRepair q :=
  cert.exact_status

theorem certificate_implies_admissible_witness
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (cert : RepairCertificate C S zeroClass q) :
    Nonempty (PrimitiveAdmissibleRepair.AdmissibleRepairWitness S zeroClass q) :=
  ⟨cert.witness⟩

theorem certificate_implies_admissible_witnessed_exact
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (cert : RepairCertificate C S zeroClass q) :
    PrimitiveAdmissibleRepair.AdmissibleWitnessedExactRepair
      C S zeroClass q :=
  ⟨cert.exact_status, ⟨cert.witness⟩⟩

theorem certificate_implies_repair_to_zero
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (cert : RepairCertificate C S zeroClass q) :
    cert.witness.repair q = zeroClass :=
  cert.witness.repairs_to_zero

theorem certificate_has_admissible_repair
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (cert : RepairCertificate C S zeroClass q) :
    CertificateHasAdmissibleRepair C S zeroClass q cert :=
  cert.witness.admissible_repair

theorem certificate_repairs_to_zero
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (cert : RepairCertificate C S zeroClass q) :
    CertificateRepairsToZero C S zeroClass q cert :=
  cert.witness.repairs_to_zero

theorem certificate_matches_classifier
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q)
    (cert : RepairCertificate C S zeroClass q) :
    CertificateMatchesClassifier C S zeroClass q cert :=
  cert.exact_status

theorem hasCertificate_implies_exact
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q) :
    HasRepairCertificate C S zeroClass q → C.IsExactRepair q := by
  intro h
  cases h with
  | intro cert =>
      exact cert.exact_status

theorem certificate_implies_ordinary_witnessed_exact
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem
      (PointedResidualQuotient P))
    (q : PointedResidualQuotient P)
    (cert : RepairCertificate C S P.zeroClass q) :
    ∃ r : PrimitiveRepairWitness.RepairMap P,
      PrimitiveRepairWitness.WitnessedExactRepair P C r q :=
  PrimitiveAdmissibleRepair.admissibleWitnessedExactRepair_implies_witnessedExactRepair P C S q
    (certificate_implies_admissible_witnessed_exact C S P.zeroClass q cert)

theorem certificate_from_admissible_witnessed_exact
    (C : ObstructionClassifier Q)
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass : Q) (q : Q) :
    PrimitiveAdmissibleRepair.AdmissibleWitnessedExactRepair C S zeroClass q →
      HasRepairCertificate C S zeroClass q := by
  intro h
  cases h.2 with
  | intro w =>
      exact ⟨{
        exact_status := h.1
        witness := w
      }⟩

theorem no_certificate_under_certificate_empty_system
    (C : ObstructionClassifier Q) (zeroClass : Q) (q : Q) :
    ¬ HasRepairCertificate C (certificateEmptyRepairSystem Q) zeroClass q := by
  intro h
  cases h with
  | intro cert =>
      exact cert.witness.admissible_repair

theorem exact_status_alone_is_not_repairCertificate
    (C : ObstructionClassifier Q) (zeroClass : Q) (q : Q) :
    ExactStatusOnly C q →
      ∃ S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q,
        ExactStatusOnly C q ∧ ¬ HasRepairCertificate C S zeroClass q := by
  intro hExact
  exact ⟨certificateEmptyRepairSystem Q, hExact,
    no_certificate_under_certificate_empty_system C zeroClass q⟩

end PrimitiveRepairCertificate
end OmegaCore
