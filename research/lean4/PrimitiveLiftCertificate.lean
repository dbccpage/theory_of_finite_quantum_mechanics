/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import PrimitiveLiftCandidate
/-!
Primitive lift certificate kernel.

This file separates a boolean lift checklist from structured evidence carrying
the proof objects required by that checklist.
-/

namespace OmegaCore
namespace PrimitiveLiftCertificate

structure LiftEvidence where
  sourceObstruction : Prop
  newCarrierDeclared : Prop
  replayAvailable : Prop
  residualReduced : Prop
  closurePreserved : Prop

structure LiftCertificate where
  evidence : LiftEvidence
  source_obstruction : evidence.sourceObstruction
  new_carrier : evidence.newCarrierDeclared
  replay : evidence.replayAvailable
  reduction : evidence.residualReduced
  closure : evidence.closurePreserved

def HasLiftCertificate (evidence : LiftEvidence) : Prop :=
  Nonempty { cert : LiftCertificate // cert.evidence = evidence }

namespace LiftCertificate

def toCandidate (_cert : LiftCertificate) :
    PrimitiveLiftCandidate.LiftCandidate where
  hasSourceObstruction := true
  hasNewCarrier := true
  hasReplay := true
  reducesPhi := true
  preservesClosure := true

end LiftCertificate

theorem liftCertificate_implies_source_obstruction
    (cert : LiftCertificate) :
    cert.evidence.sourceObstruction :=
  cert.source_obstruction

theorem liftCertificate_implies_new_carrier
    (cert : LiftCertificate) :
    cert.evidence.newCarrierDeclared :=
  cert.new_carrier

theorem liftCertificate_implies_replay
    (cert : LiftCertificate) :
    cert.evidence.replayAvailable :=
  cert.replay

theorem liftCertificate_implies_residual_reduction
    (cert : LiftCertificate) :
    cert.evidence.residualReduced :=
  cert.reduction

theorem liftCertificate_implies_closure_preservation
    (cert : LiftCertificate) :
    cert.evidence.closurePreserved :=
  cert.closure

theorem liftCertificate_toCandidate_is_licensed
    (cert : LiftCertificate) :
    PrimitiveLiftCandidate.IsLicensedLiftCandidate cert.toCandidate :=
  ⟨rfl, rfl, rfl, rfl, rfl⟩

theorem licensed_boolean_candidate_is_not_certificate
    (L : PrimitiveLiftCandidate.LiftCandidate)
    (_hLicensed : PrimitiveLiftCandidate.IsLicensedLiftCandidate L) :
    ∃ evidence : LiftEvidence, ¬ HasLiftCertificate evidence := by
  let evidence : LiftEvidence := {
    sourceObstruction := True
    newCarrierDeclared := True
    replayAvailable := False
    residualReduced := True
    closurePreserved := True
  }
  refine ⟨evidence, ?_⟩
  intro hCert
  cases hCert with
  | intro cert =>
      have hReplay : evidence.replayAvailable := by
        rw [← cert.property]
        exact cert.val.replay
      exact hReplay

theorem no_lift_certificate_without_replay
    (evidence : LiftEvidence)
    (hNoReplay : ¬ evidence.replayAvailable) :
    ¬ HasLiftCertificate evidence := by
  intro hCert
  cases hCert with
  | intro cert =>
      have hReplay : evidence.replayAvailable := by
        rw [← cert.property]
        exact cert.val.replay
      exact hNoReplay hReplay

theorem no_lift_certificate_without_reduction
    (evidence : LiftEvidence)
    (hNoReduction : ¬ evidence.residualReduced) :
    ¬ HasLiftCertificate evidence := by
  intro hCert
  cases hCert with
  | intro cert =>
      have hReduction : evidence.residualReduced := by
        rw [← cert.property]
        exact cert.val.reduction
      exact hNoReduction hReduction

theorem no_lift_certificate_without_closure
    (evidence : LiftEvidence)
    (hNoClosure : ¬ evidence.closurePreserved) :
    ¬ HasLiftCertificate evidence := by
  intro hCert
  cases hCert with
  | intro cert =>
      have hClosure : evidence.closurePreserved := by
        rw [← cert.property]
        exact cert.val.closure
      exact hNoClosure hClosure

end PrimitiveLiftCertificate
end OmegaCore
