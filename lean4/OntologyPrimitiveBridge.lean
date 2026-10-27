
import OntologyBasic
import PrimitiveTerminalPacket


namespace FiniteCosmology
namespace Ontology
namespace PrimitiveBridge

universe u

open ObstructionCore
open ObstructionCore.PrimitiveRepairBoundary
open ObstructionCore.PrimitiveTerminalPacket

variable {Q : Type u}

def paper000cClaimPacketEvidenceId : String :=
  "PAPER000C-CLAIM-PACKET-AUTHORITY-BOUNDARY"

theorem paper000cClaimPacketEvidenceId_eq :
    paper000cClaimPacketEvidenceId =
      "PAPER000C-CLAIM-PACKET-AUTHORITY-BOUNDARY" :=
  rfl


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
end FiniteCosmology

private def l5aProvenance : String :=
  "Origin: lean4/OntologyPrimitiveBridge.lean Claim: paper000cClaimPacketEvidenceId_eq AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
