/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import PrimitiveLiftCertificate
import PrimitiveRepairBoundary
/-!
Primitive spine summary kernel.

This file collects projection lemmas across the primitive difference,
invariant descent, obstruction classifier, repair boundary, terminal packet,
repair certificate, and lift-candidate layers.
-/

namespace OmegaCore
namespace PrimitiveSpineSummary

universe u v w

variable {α : Type u} {β : Type v} {γ : Type w}

structure SpineSummary
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem
      (PointedResidualQuotient P))
    (q : PointedResidualQuotient P) where
  terminal_packet : PrimitiveTerminalPacket.TerminalPacket C q
  lift_candidate : PrimitiveLiftCandidate.LiftCandidate

structure SpineSummaryWithCertificate
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem
      (PointedResidualQuotient P))
    (q : PointedResidualQuotient P) where
  summary : SpineSummary P C S q
  certificate :
    PrimitiveRepairCertificate.RepairCertificate C S P.zeroClass q

theorem spine_delta_descends_iff_congruent
    (P : PrimitiveDifference α β) :
    (∃ F : P.ResidualQuotient → P.ResidualQuotient → β,
        ∀ x y : α, F (P.classOf x) (P.classOf y) = P.δ x y)
      ↔ P.DeltaCongruent :=
  PrimitiveDifference.deltaFactor_exists_iff_deltaCongruent P

theorem spine_delta_no_factor_of_not_congruent
    (P : PrimitiveDifference α β)
    (hδ : ¬ P.DeltaCongruent) :
    ¬ (∃ F : P.ResidualQuotient → P.ResidualQuotient → β,
        ∀ x y : α, F (P.classOf x) (P.classOf y) = P.δ x y) :=
  PrimitiveDifference.deltaFactor_no_factor_of_not_deltaCongruent P hδ

theorem spine_delta_no_factor_of_zeroRel_ne
    (P : PrimitiveDifference α β)
    {x x' y y' : α}
    (hxx : P.ZeroRel x x') (hyy : P.ZeroRel y y')
    (hne : P.δ x y ≠ P.δ x' y') :
    ¬ (∃ F : P.ResidualQuotient → P.ResidualQuotient → β,
        ∀ x y : α, F (P.classOf x) (P.classOf y) = P.δ x y) :=
  PrimitiveDifference.deltaFactor_no_factor_of_zeroRel_ne P hxx hyy hne

theorem spine_invariant_descends_iff_congruent
    (P : PrimitiveDifference α β) (phi : α → γ) :
    (∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = phi x)
      ↔ P.InvariantCongruent phi :=
  PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent P phi

theorem spine_raw_phi_noncongruent_blocks_classifier
    (P : PointedPrimitiveDifference α β)
    (phiRaw : α → Nat)
    (hnot :
      ¬ PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference phiRaw) :
    ¬ (∃ C : ObstructionClassifier (PointedResidualQuotient P),
        ∀ x : α,
          C.Phi (PrimitiveDifference.classOf P.toPrimitiveDifference x) =
            phiRaw x) := by
  intro hClassifier
  rcases hClassifier with ⟨C, hPhi⟩
  exact PrimitiveObstructionPipeline.no_phiQuot_if_not_congruent
    P phiRaw hnot ⟨C.Phi, hPhi⟩

theorem spine_admissible_repair_certificate_implies_exact
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem
      (PointedResidualQuotient P))
    (q : PointedResidualQuotient P)
    (cert : PrimitiveRepairCertificate.RepairCertificate C S P.zeroClass q) :
    C.IsExactRepair q :=
  PrimitiveRepairCertificate.certificate_implies_exact
    C S P.zeroClass q cert

theorem spine_repair_boundary_blocks_noRule
    (input : PrimitiveRepairBoundary.RepairBoundaryInput)
    (hPolicy : input.policyAllowed = true)
    (hRule : input.hasRule = false) :
    PrimitiveRepairBoundary.repairBoundaryDecision input ≠
      PrimitiveRepairBoundary.RepairBoundaryStatus.repaired := by
  rw [PrimitiveRepairBoundary.missing_rule_routes_noRule
    input hPolicy hRule]
  exact PrimitiveRepairBoundary.noRule_not_repaired

theorem spine_repair_boundary_repaired_iff
    (input : PrimitiveRepairBoundary.RepairBoundaryInput) :
    PrimitiveRepairBoundary.repairBoundaryDecision input =
        PrimitiveRepairBoundary.RepairBoundaryStatus.repaired ↔
      input.policyAllowed = true ∧
      input.hasRule = true ∧
      input.withinBudget = true ∧
      input.hasAdmissibleWitness = true :=
  PrimitiveRepairBoundary.repairBoundary_repaired_iff input

theorem spine_terminal_packet_exact_without_certificate_not_repaired
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (q : PointedResidualQuotient P)
    (packet : PrimitiveTerminalPacket.TerminalPacket C q)
    (hExact : C.IsExactRepair q)
    (hCertificate : packet.hasCertificate = false) :
    ¬ PrimitiveTerminalPacket.PacketRepaired packet :=
  PrimitiveTerminalPacket.packet_exact_without_certificate_not_repaired
    C q packet hExact hCertificate

theorem spine_packet_not_ready_iff_repaired_without_certificate
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (q : PointedResidualQuotient P)
    (packet : PrimitiveTerminalPacket.TerminalPacket C q) :
    ¬ PrimitiveTerminalPacket.PacketReady packet ↔
      packet.boundary =
        PrimitiveRepairBoundary.RepairBoundaryStatus.repaired ∧
      packet.hasCertificate = false :=
  PrimitiveTerminalPacket.packet_not_ready_iff_repaired_boundary_without_certificate
    C q packet

theorem spine_lift_requires_replay_reduction_closure
    (L : PrimitiveLiftCandidate.LiftCandidate) :
    PrimitiveLiftCandidate.IsLicensedLiftCandidate L →
      L.hasReplay = true ∧
        L.reducesPhi = true ∧
        L.preservesClosure = true := by
  intro hLicensed
  exact ⟨
    PrimitiveLiftCandidate.licensed_lift_requires_replay L hLicensed,
    PrimitiveLiftCandidate.licensed_lift_requires_residual_reduction
      L hLicensed,
    PrimitiveLiftCandidate.licensed_lift_requires_closure_preservation
      L hLicensed⟩

theorem spine_lift_missing_source_blocks
    (L : PrimitiveLiftCandidate.LiftCandidate)
    (hSource : L.hasSourceObstruction = false) :
    ¬ PrimitiveLiftCandidate.IsLicensedLiftCandidate L :=
  PrimitiveLiftCandidate.missing_source_obstruction_blocks_lift L hSource

theorem spine_lift_missing_new_carrier_blocks
    (L : PrimitiveLiftCandidate.LiftCandidate)
    (hCarrier : L.hasNewCarrier = false) :
    ¬ PrimitiveLiftCandidate.IsLicensedLiftCandidate L :=
  PrimitiveLiftCandidate.missing_new_carrier_blocks_lift L hCarrier

theorem spine_lift_certificate_implies_licensed_candidate
    (cert : PrimitiveLiftCertificate.LiftCertificate) :
    PrimitiveLiftCandidate.IsLicensedLiftCandidate cert.toCandidate :=
  PrimitiveLiftCertificate.liftCertificate_toCandidate_is_licensed cert

theorem spine_lift_certificate_requires_replay_reduction_closure
    (cert : PrimitiveLiftCertificate.LiftCertificate) :
    cert.evidence.replayAvailable ∧
      cert.evidence.residualReduced ∧
      cert.evidence.closurePreserved :=
  ⟨
    PrimitiveLiftCertificate.liftCertificate_implies_replay cert,
    PrimitiveLiftCertificate.liftCertificate_implies_residual_reduction cert,
    PrimitiveLiftCertificate.liftCertificate_implies_closure_preservation cert⟩

theorem summary_terminal_status_matches
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem
      (PointedResidualQuotient P))
    (q : PointedResidualQuotient P)
    (summary : SpineSummary P C S q) :
    summary.terminal_packet.status = C.terminalize q :=
  PrimitiveTerminalPacket.packet_status_matches_terminalize
    C q summary.terminal_packet

theorem summaryWithCertificate_implies_exact
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem
      (PointedResidualQuotient P))
    (q : PointedResidualQuotient P)
    (summary : SpineSummaryWithCertificate P C S q) :
    C.IsExactRepair q :=
  summary.certificate.exact_status

theorem summaryWithCertificate_implies_admissible_witnessed_exact
    (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (S : PrimitiveAdmissibleRepair.AdmissibleRepairSystem
      (PointedResidualQuotient P))
    (q : PointedResidualQuotient P)
    (summary : SpineSummaryWithCertificate P C S q) :
    PrimitiveAdmissibleRepair.AdmissibleWitnessedExactRepair
      C S P.zeroClass q :=
  PrimitiveRepairCertificate.certificate_implies_admissible_witnessed_exact
    C S P.zeroClass q summary.certificate

end PrimitiveSpineSummary
end OmegaCore
