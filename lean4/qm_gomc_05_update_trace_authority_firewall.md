/-!
GOMC-05: diagnostic update traces do not close authority.

Channels, branch search, MCTS policies, and other learning/update operators can
preserve diagnostic validity across a finite trace. That trace is still not an
authority terminal unless a separate finite descent gate closes.
-/

namespace QM

namespace GOMC05

/-- One finite diagnostic update step. This is deliberately carrier-agnostic:
it can stand for a density-channel update, a branch-search update, or any other
declared representation-layer transition. -/
structure DiagnosticUpdate where
  inputValid : Bool
  updateAdmissible : Bool
  outputValid : Bool
  authorityEffectNone : Bool
deriving DecidableEq, Repr

def UpdateDiagnostic (u : DiagnosticUpdate) : Prop :=
  u.inputValid = true ∧
    u.updateAdmissible = true ∧
    u.outputValid = true ∧
    u.authorityEffectNone = true

def AllUpdatesDiagnostic : List DiagnosticUpdate -> Prop
  | [] => True
  | u :: rest => UpdateDiagnostic u ∧ AllUpdatesDiagnostic rest

/-- A finite trace of diagnostic updates plus the separate terminal gate. -/
structure UpdateTrace where
  steps : List DiagnosticUpdate
  descentGateClosed : Bool
  authorityTerminal : Bool
deriving DecidableEq, Repr

def TraceDiagnosticOnly (t : UpdateTrace) : Prop :=
  AllUpdatesDiagnostic t.steps ∧ t.descentGateClosed = false

def DescentAuthority (t : UpdateTrace) : Prop :=
  t.descentGateClosed = true ∧ t.authorityTerminal = true

theorem traceDiagnosticOnly_no_descentAuthority
    {t : UpdateTrace} (h : TraceDiagnosticOnly t) :
    ¬ DescentAuthority t := by
  intro hAuth
  exact Bool.noConfusion (h.2.symm.trans hAuth.1)

def cleanDiagnosticStep : DiagnosticUpdate where
  inputValid := true
  updateAdmissible := true
  outputValid := true
  authorityEffectNone := true

def twoStepDiagnosticTrace : UpdateTrace where
  steps := [cleanDiagnosticStep, cleanDiagnosticStep]
  descentGateClosed := false
  authorityTerminal := false

theorem cleanDiagnosticStep_is_diagnostic :
    UpdateDiagnostic cleanDiagnosticStep := by
  exact ⟨rfl, rfl, rfl, rfl⟩

theorem twoStepDiagnosticTrace_is_diagnosticOnly :
    TraceDiagnosticOnly twoStepDiagnosticTrace := by
  constructor
  · exact ⟨cleanDiagnosticStep_is_diagnostic,
      cleanDiagnosticStep_is_diagnostic, True.intro⟩
  · rfl

theorem diagnosticUpdateTrace_without_authority_witness :
    ∃ t : UpdateTrace,
      TraceDiagnosticOnly t ∧ ¬ DescentAuthority t := by
  refine ⟨twoStepDiagnosticTrace, twoStepDiagnosticTrace_is_diagnosticOnly, ?_⟩
  exact traceDiagnosticOnly_no_descentAuthority twoStepDiagnosticTrace_is_diagnosticOnly

theorem not_traceDiagnosticOnly_implies_descentAuthority :
    ¬ (∀ t : UpdateTrace,
      TraceDiagnosticOnly t -> DescentAuthority t) := by
  intro h
  obtain ⟨t, hTrace, hNoAuth⟩ :=
    diagnosticUpdateTrace_without_authority_witness
  exact hNoAuth (h t hTrace)

end GOMC05

end QM

#print axioms QM.GOMC05.traceDiagnosticOnly_no_descentAuthority
#print axioms QM.GOMC05.diagnosticUpdateTrace_without_authority_witness
#print axioms QM.GOMC05.not_traceDiagnosticOnly_implies_descentAuthority
