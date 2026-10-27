





namespace FiniteCosmology
namespace Ontology

universe u v

structure PrimitiveDifference where
  Source : Sort u
  Target : Sort v
  delta : Source → Source → Target



structure Structure where
  Carrier : Sort u
  persists : Prop
  composes : Prop
  stabilizes : Prop
  records : Prop
  resultsFromObstruction : Prop

inductive Real0 where
  | primitiveDifference : PrimitiveDifference → Real0
  | structure : Structure → Real0

inductive TerminalStatus where
  | certified
  | repaired
  | lifted
  | stabilized
  | refused
  | noRule
  | budgetUnknown
deriving DecidableEq

def TerminalStatus.Authoritative : TerminalStatus → Prop
  | .certified => True
  | .repaired => True
  | .lifted => True
  | .stabilized => True
  | .refused => False
  | .noRule => False
  | .budgetUnknown => False

def TerminalStatus.TypedRefusal : TerminalStatus → Prop
  | .refused => True
  | .noRule => True
  | .budgetUnknown => True
  | .certified => False
  | .repaired => False
  | .lifted => False
  | .stabilized => False


structure ClaimPacket where
  Representation : Sort u
  descendsToPrimitiveDifference : Prop
  descendsToStructure : Prop
  typedRefusal : Prop
  terminalStatus : TerminalStatus

def ClaimPacket.DescendsToReal0 (packet : ClaimPacket) : Prop :=
  packet.descendsToPrimitiveDifference ∨ packet.descendsToStructure

def ClaimPacket.Terminalized (packet : ClaimPacket) : Prop :=
  packet.DescendsToReal0 ∨ packet.typedRefusal

def ClaimPacket.HasAuthority (packet : ClaimPacket) : Prop :=
  packet.DescendsToReal0 ∧ packet.terminalStatus.Authoritative

structure ValidatedClaimPacket extends ClaimPacket.{u} where
  terminalized : toClaimPacket.Terminalized
  authority_descent : toClaimPacket.terminalStatus.Authoritative → toClaimPacket.DescendsToReal0

structure TruthPacket extends ClaimPacket where
  witnessConditions : Prop
  terminalizedStructure : descendsToStructure
  witnessed : witnessConditions
  authority : toClaimPacket.HasAuthority

def TruthPacket.toValidatedClaimPacket (truth : TruthPacket.{u}) : ValidatedClaimPacket.{u} where
  toClaimPacket := truth.toClaimPacket
  terminalized := Or.inl (Or.inr truth.terminalizedStructure)
  authority_descent := fun _ => Or.inr truth.terminalizedStructure

structure OntologyAxiomSet where
  primitiveDifferenceIsReal :
    ∀ _D : PrimitiveDifference.{0, 0}, Real0
  structureIsReal :
    ∀ _S : Structure.{0}, Real0
  claimsDescendOrRefuse :
    ∀ packet : ValidatedClaimPacket.{u}, packet.toClaimPacket.Terminalized
  noRepresentationAuthorityByDefault :
    ∀ packet : ValidatedClaimPacket.{u},
      packet.toClaimPacket.terminalStatus.Authoritative → packet.toClaimPacket.DescendsToReal0
  truthIsTerminalizedStructure :
    ∀ truth : TruthPacket.{u}, truth.toClaimPacket.HasAuthority

def primitiveDifferenceReal (D : PrimitiveDifference) : Real0 :=
  Real0.primitiveDifference D

def structureReal (S : Structure) : Real0 :=
  Real0.structure S

def defaultOntologyAxioms : OntologyAxiomSet.{u} where
  primitiveDifferenceIsReal := fun D => Real0.primitiveDifference D
  structureIsReal := fun S => Real0.structure S
  claimsDescendOrRefuse := fun p => p.terminalized
  noRepresentationAuthorityByDefault := fun p => p.authority_descent
  truthIsTerminalizedStructure := fun t => t.authority

def ValidatedClaimPacket.ofRefusal (Representation : Sort u) : ValidatedClaimPacket.{u} where
  Representation := Representation
  descendsToPrimitiveDifference := False
  descendsToStructure := False
  typedRefusal := True
  terminalStatus := TerminalStatus.refused
  terminalized := Or.inr True.intro
  authority_descent := by
    intro hAuth
    cases hAuth

def ValidatedClaimPacket.ofPrimitiveDifference (Representation : Sort u) : ValidatedClaimPacket.{u} where
  Representation := Representation
  descendsToPrimitiveDifference := True
  descendsToStructure := False
  typedRefusal := False
  terminalStatus := TerminalStatus.certified
  terminalized := Or.inl (Or.inl True.intro)
  authority_descent := fun _ => Or.inl True.intro

def ValidatedClaimPacket.ofStructure (Representation : Sort u) : ValidatedClaimPacket.{u} where
  Representation := Representation
  descendsToPrimitiveDifference := False
  descendsToStructure := True
  typedRefusal := False
  terminalStatus := TerminalStatus.certified
  terminalized := Or.inl (Or.inr True.intro)
  authority_descent := fun _ => Or.inr True.intro

theorem no_authority_without_descent
    (packet : ClaimPacket)
    (h : packet.HasAuthority) :
    packet.DescendsToReal0 :=
  h.1

theorem authoritative_status_is_not_enough
    (A : OntologyAxiomSet.{u})
    (packet : ValidatedClaimPacket.{u})
    (hStatus : packet.toClaimPacket.terminalStatus.Authoritative) :
    packet.toClaimPacket.DescendsToReal0 :=
  A.noRepresentationAuthorityByDefault packet hStatus

theorem terminalized_without_descent_is_refusal
    (packet : ClaimPacket)
    (hTerminal : packet.Terminalized)
    (hNoDescent : ¬ packet.DescendsToReal0) :
    packet.typedRefusal := by
  cases hTerminal with
  | inl hDescent => exact False.elim (hNoDescent hDescent)
  | inr hRefusal => exact hRefusal

theorem truth_packet_has_authority
    (truth : TruthPacket) :
    truth.toClaimPacket.HasAuthority :=
  truth.authority

theorem truth_packet_descends_to_structure
    (truth : TruthPacket) :
    truth.toClaimPacket.descendsToStructure :=
  truth.terminalizedStructure

theorem truth_packet_descends_to_real0
    (truth : TruthPacket) :
    truth.toClaimPacket.DescendsToReal0 :=
  Or.inr truth.terminalizedStructure

theorem typed_refusal_is_terminalized
    (packet : ClaimPacket)
    (hRefusal : packet.typedRefusal) :
    packet.Terminalized :=
  Or.inr hRefusal

theorem primitive_difference_descent_terminalized
    (packet : ClaimPacket)
    (hPD : packet.descendsToPrimitiveDifference) :
    packet.Terminalized :=
  Or.inl (Or.inl hPD)

theorem structure_descent_terminalized
    (packet : ClaimPacket)
    (hStructure : packet.descendsToStructure) :
    packet.Terminalized :=
  Or.inl (Or.inr hStructure)

end Ontology
end FiniteCosmology

private def l5aProvenance : String :=
  "Origin: lean4/OntologyBasic.lean Claim: no_authority_without_descent AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
