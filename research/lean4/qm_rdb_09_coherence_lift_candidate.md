import «rdb_06_licensed_coherence»
import «primitive_lift_candidate»
/-!
RDB-09: licensed coherence still needs a primitive lift candidate.

RDB-06 says that off-diagonal/coherence structure requires a coherence license.
This file connects that local QM checklist to the tower-level
`PrimitiveLiftCandidate` gate. The point is a firewall:

* licensed coherence can be present;
* a primitive lift candidate may still be missing source/replay/reduction/closure
  evidence;
* therefore coherence licensing alone does not construct a licensed lift.
-/

namespace QM

namespace RDB09

/-- A plan002 coherence-lift packet carries both a local coherence license and
the independent primitive-lift checklist fields. -/
structure CoherenceLiftPacket where
  coherence : RDB06.CoherenceLicense
  sourceObstructionDeclared : Bool
  newCarrierDeclared : Bool
  replayDeclared : Bool
  residualReductionDeclared : Bool
  closurePreserved : Bool
deriving DecidableEq

def toPrimitiveLiftCandidate
    (packet : CoherenceLiftPacket) :
    OmegaCore.PrimitiveLiftCandidate.LiftCandidate where
  hasSourceObstruction := packet.sourceObstructionDeclared
  hasNewCarrier := packet.newCarrierDeclared
  hasReplay := packet.replayDeclared
  reducesPhi := packet.residualReductionDeclared
  preservesClosure := packet.closurePreserved

def LicensedCoherenceLift (packet : CoherenceLiftPacket) : Prop :=
  RDB06.LicensedCoherence packet.coherence ∧
    OmegaCore.PrimitiveLiftCandidate.IsLicensedLiftCandidate
      (toPrimitiveLiftCandidate packet)

theorem licensedCoherenceLift_iff
    (packet : CoherenceLiftPacket) :
    LicensedCoherenceLift packet ↔
      RDB06.LicensedCoherence packet.coherence ∧
        OmegaCore.PrimitiveLiftCandidate.IsLicensedLiftCandidate
          (toPrimitiveLiftCandidate packet) := by
  rfl

theorem licensedCoherenceLift_implies_local_license
    (packet : CoherenceLiftPacket) :
    LicensedCoherenceLift packet ->
      RDB06.LicensedCoherence packet.coherence := by
  intro h
  exact h.1

theorem licensedCoherenceLift_implies_primitive_lift
    (packet : CoherenceLiftPacket) :
    LicensedCoherenceLift packet ->
      OmegaCore.PrimitiveLiftCandidate.IsLicensedLiftCandidate
        (toPrimitiveLiftCandidate packet) := by
  intro h
  exact h.2

theorem missing_replay_blocks_coherenceLift
    (packet : CoherenceLiftPacket) (hReplay : packet.replayDeclared = false) :
    ¬ LicensedCoherenceLift packet := by
  intro h
  exact
    OmegaCore.PrimitiveLiftCandidate.missing_replay_blocks_lift
      (toPrimitiveLiftCandidate packet) hReplay h.2

theorem missing_residual_reduction_blocks_coherenceLift
    (packet : CoherenceLiftPacket)
    (hReduction : packet.residualReductionDeclared = false) :
    ¬ LicensedCoherenceLift packet := by
  intro h
  exact
    OmegaCore.PrimitiveLiftCandidate.missing_reduction_blocks_lift
      (toPrimitiveLiftCandidate packet) hReduction h.2

theorem licensedCoherence_does_not_construct_primitive_lift :
    ∃ packet : CoherenceLiftPacket,
      RDB06.LicensedCoherence packet.coherence ∧
        ¬ OmegaCore.PrimitiveLiftCandidate.IsLicensedLiftCandidate
          (toPrimitiveLiftCandidate packet) := by
  let coherence : RDB06.CoherenceLicense :=
    ⟨true, true, true, true, true⟩
  let packet : CoherenceLiftPacket :=
    ⟨coherence, true, true, false, true, true⟩
  refine ⟨packet, ?_, ?_⟩
  · exact ⟨rfl, rfl, rfl, rfl, rfl⟩
  · exact
      OmegaCore.PrimitiveLiftCandidate.missing_replay_blocks_lift
        (toPrimitiveLiftCandidate packet) rfl

theorem not_licensedCoherence_implies_primitive_lift :
    ¬ (∀ packet : CoherenceLiftPacket,
      RDB06.LicensedCoherence packet.coherence ->
        OmegaCore.PrimitiveLiftCandidate.IsLicensedLiftCandidate
          (toPrimitiveLiftCandidate packet)) := by
  intro h
  rcases licensedCoherence_does_not_construct_primitive_lift with
    ⟨packet, hCoherence, hNoLift⟩
  exact hNoLift (h packet hCoherence)

end RDB09

end QM

#print axioms QM.RDB09.licensedCoherenceLift_iff
#print axioms QM.RDB09.licensedCoherence_does_not_construct_primitive_lift
#print axioms QM.RDB09.not_licensedCoherence_implies_primitive_lift
