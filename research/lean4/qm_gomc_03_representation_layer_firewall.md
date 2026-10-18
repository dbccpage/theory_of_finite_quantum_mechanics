/-!
GOMC-03: representation-layer firewall.

The General Obstruction Management Calculus (GOMC) treats QM-like density,
channel, and search structure as a diagnostic representation layer for finite
obstruction accounting. This file records the first finite firewall: the native
obstruction core plus a representation layer does not construct a closed
descent authority terminal.
-/

namespace QM

namespace GOMC03

/-- A finite bookkeeping situation at the L1-to-L2 boundary. -/
structure ObstructionSituation where
  primitiveDifference : Bool
  quotientResidual : Bool
  residualMass : Bool
  representationCarrier : Bool
  observerLoss : Bool
  channelOrSearch : Bool
  finiteDescentClosed : Bool
  authorityTerminal : Bool
deriving DecidableEq, Repr

def NativeObstructionCore (s : ObstructionSituation) : Prop :=
  s.primitiveDifference = true ∧
    s.quotientResidual = true ∧
    s.residualMass = true

def RepresentationLayer (s : ObstructionSituation) : Prop :=
  s.representationCarrier = true ∧
    s.observerLoss = true ∧
    s.channelOrSearch = true

def GOMCDiagnostic (s : ObstructionSituation) : Prop :=
  NativeObstructionCore s ∧ RepresentationLayer s

def DescentAuthority (s : ObstructionSituation) : Prop :=
  s.finiteDescentClosed = true ∧ s.authorityTerminal = true

/-- A report emitted by the representation layer. Its authority effect is fixed
to `None` by construction. -/
structure RepresentationLayerReport where
  nativeObstructionCore : Bool
  representationCarrier : Bool
  observerLoss : Bool
  channelOrSearch : Bool
  authorityEffectNone : Bool
deriving DecidableEq, Repr

def reportFromSituation (s : ObstructionSituation) : RepresentationLayerReport where
  nativeObstructionCore :=
    s.primitiveDifference && s.quotientResidual && s.residualMass
  representationCarrier := s.representationCarrier
  observerLoss := s.observerLoss
  channelOrSearch := s.channelOrSearch
  authorityEffectNone := true

def ReportAuthorityPromoted (r : RepresentationLayerReport) : Prop :=
  r.authorityEffectNone = false

def diagnosticNoAuthorityWitness : ObstructionSituation where
  primitiveDifference := true
  quotientResidual := true
  residualMass := true
  representationCarrier := true
  observerLoss := true
  channelOrSearch := true
  finiteDescentClosed := false
  authorityTerminal := false

theorem reportFromSituation_authorityEffectNone
    (s : ObstructionSituation) :
    (reportFromSituation s).authorityEffectNone = true := by
  rfl

theorem representationLayerReport_no_authority_promotion
    (s : ObstructionSituation) :
    ¬ ReportAuthorityPromoted (reportFromSituation s) := by
  intro h
  exact Bool.noConfusion h

theorem gomcDiagnostic_without_descentAuthority_witness :
    ∃ s : ObstructionSituation,
      GOMCDiagnostic s ∧ ¬ DescentAuthority s := by
  refine ⟨diagnosticNoAuthorityWitness, ?_, ?_⟩
  · exact ⟨⟨rfl, rfl, rfl⟩, ⟨rfl, rfl, rfl⟩⟩
  · intro h
    exact Bool.noConfusion h.2

theorem not_gomcDiagnostic_implies_descentAuthority :
    ¬ (∀ s : ObstructionSituation,
      GOMCDiagnostic s -> DescentAuthority s) := by
  intro h
  obtain ⟨s, hDiag, hNoAuth⟩ :=
    gomcDiagnostic_without_descentAuthority_witness
  exact hNoAuth (h s hDiag)

end GOMC03

end QM

#print axioms QM.GOMC03.reportFromSituation_authorityEffectNone
#print axioms QM.GOMC03.representationLayerReport_no_authority_promotion
#print axioms QM.GOMC03.not_gomcDiagnostic_implies_descentAuthority
