
import PrimitiveRepairBoundary


namespace OmegaCore
namespace PrimitiveTerminalPacket

universe u

variable {Q : Type u}

open PrimitiveRepairBoundary

structure TerminalPacket (C : ObstructionClassifier Q) (q : Q) where
  status : ObstructionStatus
  status_eq : status = C.terminalize q
  boundary : RepairBoundaryStatus
  hasCertificate : Bool

abbrev PrimitiveTerminalPacket
    {Q : Type u} (C : ObstructionClassifier Q) (q : Q) :=
  TerminalPacket C q

def packetFor
    (C : ObstructionClassifier Q) (q : Q)
    (boundary : RepairBoundaryStatus := RepairBoundaryStatus.noRule)
    (hasCertificate : Bool := false) :
    TerminalPacket C q where
  status := C.terminalize q
  status_eq := rfl
  boundary := boundary
  hasCertificate := hasCertificate

def PacketTerminal
    {C : ObstructionClassifier Q} {q : Q}
    (_packet : TerminalPacket C q) : Prop :=
  True

def PacketRepaired
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q) : Prop :=
  packet.boundary = RepairBoundaryStatus.repaired ∧
    packet.hasCertificate = true

def PacketBlocked
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q) : Prop :=
  packet.boundary ≠ RepairBoundaryStatus.repaired

def PacketReady
    {C : ObstructionClassifier Q} {q : Q}
    (packet : TerminalPacket C q) : Prop :=
  PacketRepaired packet ∨ PacketBlocked packet

theorem packet_status_matches_terminalize
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q) :
    packet.status = C.terminalize q :=
  packet.status_eq

theorem packet_exact_iff
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q) :
    packet.status = ObstructionStatus.exactRepair ↔ C.IsExactRepair q := by
  rw [packet.status_eq]
  exact ObstructionClassifier.terminalize_exactRepair_iff C q

theorem packet_stabilized_iff
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q) :
    packet.status = ObstructionStatus.stabilizedSurvivor ↔
      C.IsStabilizedSurvivor q := by
  rw [packet.status_eq]
  exact ObstructionClassifier.terminalize_stabilizedSurvivor_iff C q

theorem packet_open_iff
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q) :
    packet.status = ObstructionStatus.openObstruction ↔
      C.IsOpenObstruction q := by
  rw [packet.status_eq]
  exact ObstructionClassifier.terminalize_openObstruction_iff C q

theorem packet_classifier_total
    (C : ObstructionClassifier Q) (q : Q)
    (_packet : TerminalPacket C q) :
    C.IsExactRepair q ∨ C.IsStabilizedSurvivor q ∨ C.IsOpenObstruction q :=
  ObstructionClassifier.classifier_total C q

theorem packet_repaired_if_boundary_repaired_and_certificate
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q)
    (hBoundary : packet.boundary = RepairBoundaryStatus.repaired)
    (hCertificate : packet.hasCertificate = true) :
    PacketRepaired packet :=
  ⟨hBoundary, hCertificate⟩

theorem packet_exact_without_certificate_not_repaired
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q)
    (_hExact : C.IsExactRepair q)
    (hCertificate : packet.hasCertificate = false) :
    ¬ PacketRepaired packet := by
  intro hRepaired
  unfold PacketRepaired at hRepaired
  rw [hCertificate] at hRepaired
  cases hRepaired.2

theorem packet_noRule_terminal_not_repaired
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q)
    (_hTerminal : PacketTerminal packet)
    (hBoundary : packet.boundary = RepairBoundaryStatus.noRule) :
    ¬ PacketRepaired packet := by
  intro hRepaired
  exact PrimitiveRepairBoundary.noRule_not_repaired
    (hBoundary.symm.trans hRepaired.1)

theorem packet_budgetUnknown_terminal_not_repaired
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q)
    (_hTerminal : PacketTerminal packet)
    (hBoundary : packet.boundary = RepairBoundaryStatus.budgetUnknown) :
    ¬ PacketRepaired packet := by
  intro hRepaired
  exact PrimitiveRepairBoundary.budgetUnknown_not_repaired
    (hBoundary.symm.trans hRepaired.1)

theorem packet_refused_terminal_not_repaired
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q)
    (_hTerminal : PacketTerminal packet)
    (hBoundary : packet.boundary = RepairBoundaryStatus.refused) :
    ¬ PacketRepaired packet := by
  intro hRepaired
  exact PrimitiveRepairBoundary.refused_not_repaired
    (hBoundary.symm.trans hRepaired.1)

theorem packet_blocked_iff_boundary_not_repaired
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q) :
    PacketBlocked packet ↔
      packet.boundary ≠ RepairBoundaryStatus.repaired :=
  Iff.rfl

theorem packet_ready_iff_blocked_or_repaired
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q) :
    PacketReady packet ↔ PacketBlocked packet ∨ PacketRepaired packet := by
  constructor
  · intro hReady
    cases hReady with
    | inl hRepaired => exact Or.inr hRepaired
    | inr hBlocked => exact Or.inl hBlocked
  · intro h
    cases h with
    | inl hBlocked => exact Or.inr hBlocked
    | inr hRepaired => exact Or.inl hRepaired

theorem packet_not_ready_iff_repaired_boundary_without_certificate
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q) :
    ¬ PacketReady packet ↔
      packet.boundary = RepairBoundaryStatus.repaired ∧
      packet.hasCertificate = false := by
  constructor
  · intro hNotReady
    have hBoundary : packet.boundary = RepairBoundaryStatus.repaired := by
      cases hStatus : packet.boundary
      · rfl
      · exfalso
        exact hNotReady (Or.inr (by
          intro h
          exact PrimitiveRepairBoundary.noRule_not_repaired
            (hStatus.symm.trans h)))
      · exfalso
        exact hNotReady (Or.inr (by
          intro h
          exact PrimitiveRepairBoundary.budgetUnknown_not_repaired
            (hStatus.symm.trans h)))
      · exfalso
        exact hNotReady (Or.inr (by
          intro h
          exact PrimitiveRepairBoundary.refused_not_repaired
            (hStatus.symm.trans h)))
    have hCertificate : packet.hasCertificate = false := by
      cases hCert : packet.hasCertificate
      · rfl
      · exfalso
        exact hNotReady (Or.inl ⟨hBoundary, hCert⟩)
    exact ⟨hBoundary, hCertificate⟩
  · intro h hReady
    cases hReady with
    | inl hRepaired =>
        unfold PacketRepaired at hRepaired
        rw [h.2] at hRepaired
        cases hRepaired.2
    | inr hBlocked =>
        exact hBlocked h.1

theorem packet_repaired_not_blocked
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q) :
    PacketRepaired packet → ¬ PacketBlocked packet := by
  intro hRepaired hBlocked
  exact hBlocked hRepaired.1

theorem packet_blocked_not_repaired
    (C : ObstructionClassifier Q) (q : Q)
    (packet : TerminalPacket C q) :
    PacketBlocked packet → ¬ PacketRepaired packet := by
  intro hBlocked hRepaired
  exact hBlocked hRepaired.1

end PrimitiveTerminalPacket
end OmegaCore

private def l5aProvenance : String :=
  "Origin: lean4/PrimitiveTerminalPacket.lean Claim: packet_status_matches_terminalize AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
