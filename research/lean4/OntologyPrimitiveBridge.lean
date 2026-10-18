/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import OntologyBasic
import PrimitiveTerminalPacket
/-!
Bridge from the PaperFOC000c ontology boundary to the existing primitive FOC spine.

The ontology layer says that a claim earns authority only through descent to
Primitive Difference, Structure, or typed refusal.  The primitive spine already
has terminal packets with classifier status, repair-boundary status, and
certificate readiness.  This file connects those layers without promoting a
representation-only packet.
-/

namespace OmegaCosmology
namespace Ontology
namespace PrimitiveBridge

universe u

open OmegaCore
open OmegaCore.PrimitiveRepairBoundary
open OmegaCore.PrimitiveTerminalPacket

variable {Q : Type u}

/-- Stable cross-domain evidence id for the PaperFOC000c claim-packet boundary. -/
def paper000cClaimPacketEvidenceId : String :=
  "PAPER000C-CLAIM-PACKET-AUTHORITY-BOUNDARY"

theorem paper000cClaimPacketEvidenceId_eq :
    paper000cClaimPacketEvidenceId =
      "PAPER000C-CLAIM-PACKET-AUTHORITY-BOUNDARY" :=
  rfl

/--
Translate a primitive terminal packet into an ontology terminal status.

The mapping is conservative: repair needs a repair boundary and certificate;
refusal/budget/no-rule boundaries remain non-authoritative; a stabilized
survivor becomes a positive stabilized status only when the primitive classifier
has already terminalized it as such.
-/
def statusFromPrimitiveTerminal
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q) : TerminalStatus :=
  match packet.boundary with
  | RepairBoundaryStatus.repaired =>
      if packet.hasCertificate then TerminalStatus.repaired else TerminalStatus.noRule
  | RepairBoundaryStatus.refused => TerminalStatus.refused
  | RepairBoundaryStatus.budgetUnknown => TerminalStatus.budgetUnknown
  | RepairBoundaryStatus.noRule =>
      match packet.status with
      | ObstructionStatus.exactRepair =>
          if packet.hasCertificate then TerminalStatus.certified else TerminalStatus.noRule
      | ObstructionStatus.stabilizedSurvivor =>
          if packet.hasCertificate then TerminalStatus.stabilized else TerminalStatus.noRule
      | ObstructionStatus.openObstruction => TerminalStatus.noRule

/--
A primitive terminal packet becomes a claim packet only after the caller declares
which root descent channels have been witnessed.
-/
def claimPacketFromPrimitiveTerminal
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q)
    (descendsToPrimitiveDifference descendsToStructure : Prop) : ClaimPacket where
  Representation := Unit
  descendsToPrimitiveDifference := descendsToPrimitiveDifference
  descendsToStructure := descendsToStructure
  typedRefusal := (statusFromPrimitiveTerminal packet).TypedRefusal
  terminalStatus := statusFromPrimitiveTerminal packet

theorem primitive_claim_no_authority_without_descent
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q)
    {descendsToPrimitiveDifference descendsToStructure : Prop}
    (hNoPrimitive : ¬ descendsToPrimitiveDifference)
    (hNoStructure : ¬ descendsToStructure) :
    ¬ (claimPacketFromPrimitiveTerminal packet
        descendsToPrimitiveDifference descendsToStructure).HasAuthority := by
  intro hAuthority
  have hDescent := no_authority_without_descent _ hAuthority
  unfold claimPacketFromPrimitiveTerminal ClaimPacket.DescendsToReal0 at hDescent
  cases hDescent with
  | inl hPrimitive => exact hNoPrimitive hPrimitive
  | inr hStructure => exact hNoStructure hStructure

theorem repaired_primitive_packet_claim_has_authority
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q)
    {descendsToPrimitiveDifference descendsToStructure : Prop}
    (hRepaired : PacketRepaired packet)
    (hDescent : descendsToPrimitiveDifference ∨ descendsToStructure) :
    (claimPacketFromPrimitiveTerminal packet
      descendsToPrimitiveDifference descendsToStructure).HasAuthority := by
  constructor
  · exact hDescent
  · unfold claimPacketFromPrimitiveTerminal statusFromPrimitiveTerminal
    rw [hRepaired.1, hRepaired.2]
    simp [TerminalStatus.Authoritative]

theorem refused_primitive_packet_terminalizes_as_typed_refusal
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q)
    {descendsToPrimitiveDifference descendsToStructure : Prop}
    (hBoundary : packet.boundary = RepairBoundaryStatus.refused) :
    (claimPacketFromPrimitiveTerminal packet
      descendsToPrimitiveDifference descendsToStructure).Terminalized := by
  unfold claimPacketFromPrimitiveTerminal ClaimPacket.Terminalized
  right
  unfold statusFromPrimitiveTerminal
  rw [hBoundary]
  simp [TerminalStatus.TypedRefusal]

theorem budget_unknown_primitive_packet_terminalizes_as_typed_refusal
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q)
    {descendsToPrimitiveDifference descendsToStructure : Prop}
    (hBoundary : packet.boundary = RepairBoundaryStatus.budgetUnknown) :
    (claimPacketFromPrimitiveTerminal packet
      descendsToPrimitiveDifference descendsToStructure).Terminalized := by
  unfold claimPacketFromPrimitiveTerminal ClaimPacket.Terminalized
  right
  unfold statusFromPrimitiveTerminal
  rw [hBoundary]
  simp [TerminalStatus.TypedRefusal]

theorem stabilized_survivor_claim_has_authority_of_descent_and_certificate
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q)
    {descendsToPrimitiveDifference descendsToStructure : Prop}
    (hBoundary : packet.boundary = RepairBoundaryStatus.noRule)
    (hStatus : packet.status = ObstructionStatus.stabilizedSurvivor)
    (hCert : packet.hasCertificate = true)
    (hDescent : descendsToPrimitiveDifference ∨ descendsToStructure) :
    (claimPacketFromPrimitiveTerminal packet
      descendsToPrimitiveDifference descendsToStructure).HasAuthority := by
  constructor
  · exact hDescent
  · unfold claimPacketFromPrimitiveTerminal statusFromPrimitiveTerminal
    rw [hBoundary, hStatus, hCert]
    simp [TerminalStatus.Authoritative]

theorem open_no_rule_packet_has_no_authority
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q)
    {descendsToPrimitiveDifference descendsToStructure : Prop}
    (hBoundary : packet.boundary = RepairBoundaryStatus.noRule)
    (hStatus : packet.status = ObstructionStatus.openObstruction) :
    ¬ (claimPacketFromPrimitiveTerminal packet
      descendsToPrimitiveDifference descendsToStructure).HasAuthority := by
  intro hAuthority
  have hStatusAuthority := hAuthority.2
  unfold claimPacketFromPrimitiveTerminal statusFromPrimitiveTerminal at hStatusAuthority
  rw [hBoundary, hStatus] at hStatusAuthority
  simp [TerminalStatus.Authoritative] at hStatusAuthority

end PrimitiveBridge
end Ontology
end OmegaCosmology
