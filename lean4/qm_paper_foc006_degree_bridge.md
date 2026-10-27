import «degree_separation»
import «admission_firewall_q_admission_firewall»

/-!
QM-facing Paper 012 degree-diagnostic bridge.

A QM residual-density proposal may carry operator and density metadata around
the Paper 012 degree model, but the `Gamma2` readout is still gated by the
declared 2-cell structure and acceptance is still gated by the DSL `eval`
field.  This is an interface firewall only: it does not derive quantum
mechanics, choose a Born rule, license a continuum lift, or mint authority.
-/

namespace QM

namespace PaperFOC006DegreeBridge

universe u v w z

/-- QM-facing proposal wrapper: operator metadata plus density-like source and
target payloads around the Paper 012 degree and DSL states. -/
structure DegreeDiagnosticProposal (Operator : Type u) (DensityState : Type v) where
  operator : Operator
  sourceDensity : DensityState
  targetDensity : DensityState
  degreeModel : PaperFOC006.DegreeModel
  dslState : PaperFOC006.DSLState

/-- The Paper 012 `Gamma2` readout gate, viewed through a QM proposal wrapper. -/
def Gamma2ReadoutAvailable {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState) : Prop :=
  PaperFOC006.HasGamma2Readout proposal.degreeModel

/-- Local diagnostic constructibility, viewed through a QM proposal wrapper. -/
def DiagnosticConstructible {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState) : Bool :=
  PaperFOC006.diagnosticConstructible proposal.dslState

/-- Acceptance authorization, viewed through a QM proposal wrapper. -/
def AcceptanceAuthorized {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState) : Bool :=
  PaperFOC006.acceptanceAuthorized proposal.dslState

/-- The local PaperFOC006 fingerprint exposed through a QM wrapper: `C1` data plus
diagnostic constructibility. -/
def LocalDegreeDiagnosticFingerprint
    {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState) :
    PaperFOC006.C1C3 × Bool :=
  (proposal.degreeModel.c1, DiagnosticConstructible proposal)

/-- The global gated PaperFOC006 readout exposed through a QM wrapper: `Gamma2`
availability/value plus DSL acceptance authorization. -/
def GlobalDegreeDiagnosticGate
    {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState) :
    Option Nat × Bool :=
  (PaperFOC006.gamma2? proposal.degreeModel, AcceptanceAuthorized proposal)

/-- A proposal is accepted only when the Paper 012 DSL state authorizes it. -/
def ProposalAccepted {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState) : Prop :=
  AcceptanceAuthorized proposal = true

/-- Replace only the proposal metadata, preserving the degree and DSL states. -/
def replaceProposalMetadata
    {Operator₁ : Type u} {DensityState₁ : Type v}
    {Operator₂ : Type w} {DensityState₂ : Type z}
    (replacement : Operator₂) (sourceDensity targetDensity : DensityState₂)
    (proposal : DegreeDiagnosticProposal Operator₁ DensityState₁) :
    DegreeDiagnosticProposal Operator₂ DensityState₂ where
  operator := replacement
  sourceDensity := sourceDensity
  targetDensity := targetDensity
  degreeModel := proposal.degreeModel
  dslState := proposal.dslState

/-- QM metadata does not create a `Gamma2` readout.  The readout still requires
the Paper 012 declared 2-cell gate. -/
theorem gamma2_readout_requires_declared_twoCell
    {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState) :
    Gamma2ReadoutAvailable proposal ->
      proposal.degreeModel.hasTwoCell = true :=
  PaperFOC006.gamma2_readout_requires_twoCell proposal.degreeModel

/-- Missing 2-cell structure blocks the QM-facing `Gamma2` readout. -/
theorem missing_twoCell_blocks_gamma2_readout
    {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState)
    (hMissing : proposal.degreeModel.hasTwoCell = false) :
    ¬ Gamma2ReadoutAvailable proposal :=
  PaperFOC006.no_twoCell_blocks_gamma2_readout proposal.degreeModel hMissing

/-- Replacing QM operator/density metadata cannot alter `Gamma2` availability
when the Paper 012 degree model is unchanged. -/
theorem gamma2_readout_ignores_metadata_replacement
    {Operator₁ : Type u} {DensityState₁ : Type v}
    {Operator₂ : Type w} {DensityState₂ : Type z}
    (replacement : Operator₂) (sourceDensity targetDensity : DensityState₂)
    (proposal : DegreeDiagnosticProposal Operator₁ DensityState₁) :
    Gamma2ReadoutAvailable
        (replaceProposalMetadata replacement sourceDensity targetDensity proposal) ↔
      Gamma2ReadoutAvailable proposal :=
  Iff.rfl

/-- Replacing QM metadata cannot change diagnostic constructibility when the
Paper 012 DSL state is unchanged. -/
theorem diagnostic_constructible_ignores_metadata_replacement
    {Operator₁ : Type u} {DensityState₁ : Type v}
    {Operator₂ : Type w} {DensityState₂ : Type z}
    (replacement : Operator₂) (sourceDensity targetDensity : DensityState₂)
    (proposal : DegreeDiagnosticProposal Operator₁ DensityState₁) :
    DiagnosticConstructible
        (replaceProposalMetadata replacement sourceDensity targetDensity proposal) =
      DiagnosticConstructible proposal :=
  rfl

/-- Replacing QM metadata cannot change acceptance authorization when the Paper
012 DSL state is unchanged. -/
theorem acceptance_authority_ignores_metadata_replacement
    {Operator₁ : Type u} {DensityState₁ : Type v}
    {Operator₂ : Type w} {DensityState₂ : Type z}
    (replacement : Operator₂) (sourceDensity targetDensity : DensityState₂)
    (proposal : DegreeDiagnosticProposal Operator₁ DensityState₁) :
    ProposalAccepted
        (replaceProposalMetadata replacement sourceDensity targetDensity proposal) ↔
      ProposalAccepted proposal :=
  Iff.rfl

/-- Replacing QM metadata cannot alter the PaperFOC006 local fingerprint. -/
theorem local_fingerprint_ignores_metadata_replacement
    {Operator₁ : Type u} {DensityState₁ : Type v}
    {Operator₂ : Type w} {DensityState₂ : Type z}
    (replacement : Operator₂) (sourceDensity targetDensity : DensityState₂)
    (proposal : DegreeDiagnosticProposal Operator₁ DensityState₁) :
    LocalDegreeDiagnosticFingerprint
        (replaceProposalMetadata replacement sourceDensity targetDensity proposal) =
      LocalDegreeDiagnosticFingerprint proposal :=
  rfl

/-- Replacing QM metadata cannot alter the PaperFOC006 global gated readout. -/
theorem global_gate_ignores_metadata_replacement
    {Operator₁ : Type u} {DensityState₁ : Type v}
    {Operator₂ : Type w} {DensityState₂ : Type z}
    (replacement : Operator₂) (sourceDensity targetDensity : DensityState₂)
    (proposal : DegreeDiagnosticProposal Operator₁ DensityState₁) :
    GlobalDegreeDiagnosticGate
        (replaceProposalMetadata replacement sourceDensity targetDensity proposal) =
      GlobalDegreeDiagnosticGate proposal :=
  rfl

/-- Without the DSL `eval` gate, a QM-wrapped Paper 012 diagnostic proposal is
not accepted. -/
theorem no_eval_blocks_proposal_acceptance
    {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState)
    (hNoEval : proposal.dslState.hasEval = false) :
    ¬ ProposalAccepted proposal := by
  unfold ProposalAccepted AcceptanceAuthorized
  simp [PaperFOC006.no_eval_no_acceptance proposal.dslState hNoEval]

/-- QHeld admission for a QM degree-diagnostic proposal is exactly the shared Q
admission firewall predicate. -/
def DegreeProposalQHeldAdmissible
    (evidence : Paper_Q.QAdmissionEvidence) : Prop :=
  Paper_Q.QHeldAdmissible evidence

/-- Terminal-within-scope admission for a QM degree-diagnostic proposal is
exactly the shared Q terminal firewall predicate. -/
def DegreeProposalTerminalWithinScopeAdmissible
    (evidence : Paper_Q.QAdmissionEvidence) : Prop :=
  Paper_Q.TerminalWithinScopeAdmissible evidence

/-- Even an available `Gamma2` readout cannot bypass incomplete Q admission
debt. -/
theorem gamma2_readout_admission_gap_blocks_qheld
    {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState)
    (evidence : Paper_Q.QAdmissionEvidence)
    (_hReadout : Gamma2ReadoutAvailable proposal)
    (hGap : Paper_Q.AdmissionDebtGap evidence) :
    ¬ DegreeProposalQHeldAdmissible evidence := by
  exact Paper_Q.admission_debt_gap_blocks_qheld evidence hGap

/-- A `Gamma2` readout cannot produce terminal status without separate witness
support. -/
theorem gamma2_readout_without_witness_blocks_terminal
    {Operator : Type u} {DensityState : Type v}
    (proposal : DegreeDiagnosticProposal Operator DensityState)
    (evidence : Paper_Q.QAdmissionEvidence)
    (_hReadout : Gamma2ReadoutAvailable proposal)
    (hMissingWitness : ¬ evidence.witness_support) :
    ¬ DegreeProposalTerminalWithinScopeAdmissible evidence := by
  exact Paper_Q.terminal_within_scope_without_witness_blocked
    evidence hMissingWitness

/-- Concrete graph-only QM wrapper for the Paper 012 C3 replay. -/
def graphOnlyProposal : DegreeDiagnosticProposal Unit Unit where
  operator := ()
  sourceDensity := ()
  targetDensity := ()
  degreeModel := PaperFOC006.c3GraphOnly
  dslState := PaperFOC006.typedDiagnosticNoEval

/-- Concrete 2-cell QM wrapper for the Paper 012 C3 replay. -/
def withTwoCellProposal : DegreeDiagnosticProposal Unit Unit where
  operator := ()
  sourceDensity := ()
  targetDensity := ()
  degreeModel := PaperFOC006.c3WithTwoCell
  dslState := PaperFOC006.typedDiagnosticWithEval

/-- Graph-only/no-`eval` proposal with arbitrary QM metadata. -/
def graphOnlyProposalWith
    {Operator : Type u} {DensityState : Type v}
    (operator : Operator) (sourceDensity targetDensity : DensityState) :
    DegreeDiagnosticProposal Operator DensityState where
  operator := operator
  sourceDensity := sourceDensity
  targetDensity := targetDensity
  degreeModel := PaperFOC006.c3GraphOnly
  dslState := PaperFOC006.typedDiagnosticNoEval

/-- Declared-2-cell/`eval` proposal with arbitrary QM metadata. -/
def withTwoCellProposalWith
    {Operator : Type u} {DensityState : Type v}
    (operator : Operator) (sourceDensity targetDensity : DensityState) :
    DegreeDiagnosticProposal Operator DensityState where
  operator := operator
  sourceDensity := sourceDensity
  targetDensity := targetDensity
  degreeModel := PaperFOC006.c3WithTwoCell
  dslState := PaperFOC006.typedDiagnosticWithEval

theorem graphOnly_qm_gamma2_unavailable :
    ¬ Gamma2ReadoutAvailable graphOnlyProposal :=
  PaperFOC006.graphOnly_has_no_gamma2_readout

theorem graphOnly_qm_proposal_not_accepted :
    ¬ ProposalAccepted graphOnlyProposal := by
  exact no_eval_blocks_proposal_acceptance graphOnlyProposal rfl

theorem withTwoCell_qm_gamma2_available :
    Gamma2ReadoutAvailable withTwoCellProposal :=
  PaperFOC006.withTwoCell_has_gamma2_readout

/-- The concrete QM wrapper keeps the same local PaperFOC006 fingerprint across
the graph-only/no-`eval` and declared-2-cell/`eval` states. -/
theorem graphOnly_withTwoCell_local_fingerprint_same :
    LocalDegreeDiagnosticFingerprint graphOnlyProposal =
      LocalDegreeDiagnosticFingerprint withTwoCellProposal := by
  rfl

/-- The same concrete QM wrapper changes the global gated readout: `Gamma2`
and acceptance remain separate gates outside the local fingerprint. -/
theorem graphOnly_withTwoCell_global_gate_differs :
    Not (GlobalDegreeDiagnosticGate graphOnlyProposal =
      GlobalDegreeDiagnosticGate withTwoCellProposal) := by
  decide

/-- Arbitrary QM metadata still leaves the graph-only/no-`eval` and
declared-2-cell/`eval` proposals with the same local PaperFOC006 fingerprint. -/
theorem proposalWith_local_fingerprint_same
    {Operator : Type u} {DensityState : Type v}
    (operator₀ operator₁ : Operator)
    (source₀ target₀ source₁ target₁ : DensityState) :
    LocalDegreeDiagnosticFingerprint
        (graphOnlyProposalWith operator₀ source₀ target₀) =
      LocalDegreeDiagnosticFingerprint
        (withTwoCellProposalWith operator₁ source₁ target₁) := by
  rfl

/-- Arbitrary QM metadata cannot erase the global gated-readout difference
between the graph-only/no-`eval` and declared-2-cell/`eval` proposals. -/
theorem proposalWith_global_gate_differs
    {Operator : Type u} {DensityState : Type v}
    (operator₀ operator₁ : Operator)
    (source₀ target₀ source₁ target₁ : DensityState) :
    Not (GlobalDegreeDiagnosticGate
        (graphOnlyProposalWith operator₀ source₀ target₀) =
      GlobalDegreeDiagnosticGate
        (withTwoCellProposalWith operator₁ source₁ target₁)) := by
  exact graphOnly_withTwoCell_global_gate_differs

/-- Local fingerprint equality for QM proposal wrappers with arbitrary
operator/density metadata. -/
def proposalLocalPD (Operator : Type u) (DensityState : Type v) :
    ObstructionCore.PrimitiveDifference
      (DegreeDiagnosticProposal Operator DensityState) Prop where
  δ := fun x y =>
    LocalDegreeDiagnosticFingerprint x = LocalDegreeDiagnosticFingerprint y
  Zero := fun h => h
  zero_refl := by
    intro x
    rfl
  zero_symm := by
    intro _ _ h
    exact h.symm
  zero_trans := by
    intro _ _ _ hxy hyz
    exact hxy.trans hyz

theorem proposal_local_fingerprint_invariant
    (Operator : Type u) (DensityState : Type v) :
    (proposalLocalPD Operator DensityState).InvariantCongruent
      (fun proposal : DegreeDiagnosticProposal Operator DensityState =>
        LocalDegreeDiagnosticFingerprint proposal) := by
  intro _ _ h
  exact h

theorem proposalWith_witness_zero_related
    {Operator : Type u} {DensityState : Type v}
    (operator₀ operator₁ : Operator)
    (source₀ target₀ source₁ target₁ : DensityState) :
    (proposalLocalPD Operator DensityState).ZeroRel
      (graphOnlyProposalWith operator₀ source₀ target₀)
      (withTwoCellProposalWith operator₁ source₁ target₁) := by
  rfl

/-- Arbitrary QM metadata does not repair the composite PaperFOC006 LGGR boundary:
a local fingerprint quotient preserves `C1` plus diagnostic constructibility,
but cannot also carry the global pair consisting of `Gamma2` and acceptance
authorization. -/
theorem proposal_local_green_not_global_gate
    {Operator : Type u} {DensityState : Type v}
    (operator₀ operator₁ : Operator)
    (source₀ target₀ source₁ target₁ : DensityState) :
    (exists F :
      (proposalLocalPD Operator DensityState).ResidualQuotient ->
        PaperFOC006.C1C3 × Bool,
      forall proposal : DegreeDiagnosticProposal Operator DensityState,
        F ((proposalLocalPD Operator DensityState).classOf proposal) =
          LocalDegreeDiagnosticFingerprint proposal) /\
    Not (exists F :
      (proposalLocalPD Operator DensityState).ResidualQuotient ->
        (PaperFOC006.C1C3 × Bool) × (Option Nat × Bool),
      forall proposal : DegreeDiagnosticProposal Operator DensityState,
        F ((proposalLocalPD Operator DensityState).classOf proposal) =
          (LocalDegreeDiagnosticFingerprint proposal,
            GlobalDegreeDiagnosticGate proposal)) := by
  exact
    ObstructionCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction_of_witness
      (proposalLocalPD Operator DensityState)
      (fun proposal : DegreeDiagnosticProposal Operator DensityState =>
        LocalDegreeDiagnosticFingerprint proposal)
      (fun proposal : DegreeDiagnosticProposal Operator DensityState =>
        GlobalDegreeDiagnosticGate proposal)
      (proposal_local_fingerprint_invariant Operator DensityState)
      (proposalWith_witness_zero_related
        operator₀ operator₁ source₀ target₀ source₁ target₁)
      (proposalWith_global_gate_differs
        operator₀ operator₁ source₀ target₀ source₁ target₁)

/-- Local fingerprint equality for unit QM wrappers. -/
def unitProposalLocalPD :
    ObstructionCore.PrimitiveDifference (DegreeDiagnosticProposal Unit Unit) Prop where
  δ := fun x y =>
    LocalDegreeDiagnosticFingerprint x = LocalDegreeDiagnosticFingerprint y
  Zero := fun h => h
  zero_refl := by
    intro x
    rfl
  zero_symm := by
    intro _ _ h
    exact h.symm
  zero_trans := by
    intro _ _ _ hxy hyz
    exact hxy.trans hyz

theorem unitProposal_local_fingerprint_invariant :
    unitProposalLocalPD.InvariantCongruent
      (fun proposal : DegreeDiagnosticProposal Unit Unit =>
        LocalDegreeDiagnosticFingerprint proposal) := by
  intro _ _ h
  exact h

theorem unitProposal_witness_zero_related :
    unitProposalLocalPD.ZeroRel graphOnlyProposal withTwoCellProposal := by
  rfl

/-- QM metadata does not repair the composite PaperFOC006 LGGR boundary: a local
fingerprint quotient preserves `C1` plus diagnostic constructibility, but cannot
also carry the global pair consisting of `Gamma2` and acceptance authorization. -/
theorem unitProposal_local_green_not_global_gate :
    (exists F :
      unitProposalLocalPD.ResidualQuotient -> PaperFOC006.C1C3 × Bool,
      forall proposal : DegreeDiagnosticProposal Unit Unit,
        F (unitProposalLocalPD.classOf proposal) =
          LocalDegreeDiagnosticFingerprint proposal) /\
    Not (exists F :
      unitProposalLocalPD.ResidualQuotient ->
        (PaperFOC006.C1C3 × Bool) × (Option Nat × Bool),
      forall proposal : DegreeDiagnosticProposal Unit Unit,
        F (unitProposalLocalPD.classOf proposal) =
          (LocalDegreeDiagnosticFingerprint proposal,
            GlobalDegreeDiagnosticGate proposal)) := by
  exact
    ObstructionCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction_of_witness
      unitProposalLocalPD
      (fun proposal : DegreeDiagnosticProposal Unit Unit =>
        LocalDegreeDiagnosticFingerprint proposal)
      (fun proposal : DegreeDiagnosticProposal Unit Unit =>
        GlobalDegreeDiagnosticGate proposal)
      unitProposal_local_fingerprint_invariant
      unitProposal_witness_zero_related
      graphOnly_withTwoCell_global_gate_differs

end PaperFOC006DegreeBridge

end QM

#print axioms QM.PaperFOC006DegreeBridge.gamma2_readout_requires_declared_twoCell
#print axioms QM.PaperFOC006DegreeBridge.missing_twoCell_blocks_gamma2_readout
#print axioms QM.PaperFOC006DegreeBridge.gamma2_readout_ignores_metadata_replacement
#print axioms QM.PaperFOC006DegreeBridge.diagnostic_constructible_ignores_metadata_replacement
#print axioms QM.PaperFOC006DegreeBridge.acceptance_authority_ignores_metadata_replacement
#print axioms QM.PaperFOC006DegreeBridge.local_fingerprint_ignores_metadata_replacement
#print axioms QM.PaperFOC006DegreeBridge.global_gate_ignores_metadata_replacement
#print axioms QM.PaperFOC006DegreeBridge.no_eval_blocks_proposal_acceptance
#print axioms QM.PaperFOC006DegreeBridge.gamma2_readout_admission_gap_blocks_qheld
#print axioms QM.PaperFOC006DegreeBridge.gamma2_readout_without_witness_blocks_terminal
#print axioms QM.PaperFOC006DegreeBridge.graphOnly_qm_gamma2_unavailable
#print axioms QM.PaperFOC006DegreeBridge.graphOnly_qm_proposal_not_accepted
#print axioms QM.PaperFOC006DegreeBridge.withTwoCell_qm_gamma2_available
#print axioms QM.PaperFOC006DegreeBridge.graphOnly_withTwoCell_local_fingerprint_same
#print axioms QM.PaperFOC006DegreeBridge.graphOnly_withTwoCell_global_gate_differs
#print axioms QM.PaperFOC006DegreeBridge.proposalWith_local_fingerprint_same
#print axioms QM.PaperFOC006DegreeBridge.proposalWith_global_gate_differs
#print axioms QM.PaperFOC006DegreeBridge.proposal_local_green_not_global_gate
#print axioms QM.PaperFOC006DegreeBridge.unitProposal_local_green_not_global_gate
