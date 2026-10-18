/-!
RDB-07: channel diagnostics do not mint authority.

An admissible channel update can preserve diagnostic density validity, but that
validity is not an authority terminal. The result is a finite typed
non-implication, matching the governance rule for plan002.
-/

namespace QM

namespace RDB07

/-- A finite bookkeeping situation for a residual-density channel update. -/
structure ChannelSituation where
  inputDensityValid : Bool
  channelValid : Bool
  outputDensityValid : Bool
  authorityTerminal : Bool
deriving DecidableEq

def ChannelDiagnosticValid (s : ChannelSituation) : Prop :=
  s.inputDensityValid = true ∧
    s.channelValid = true ∧
    s.outputDensityValid = true

def ChannelAuthorityTerminal (s : ChannelSituation) : Prop :=
  s.authorityTerminal = true

/-- A diagnostic report produced by a channel path carries no authority effect by
construction. -/
structure ChannelDiagnosticReport where
  inputDensityValid : Bool
  channelValid : Bool
  outputDensityValid : Bool
  authorityEffectNone : Bool
deriving DecidableEq

def reportFromChannelSituation (s : ChannelSituation) : ChannelDiagnosticReport where
  inputDensityValid := s.inputDensityValid
  channelValid := s.channelValid
  outputDensityValid := s.outputDensityValid
  authorityEffectNone := true

theorem report_authorityEffectNone
    (s : ChannelSituation) :
    (reportFromChannelSituation s).authorityEffectNone = true := by
  rfl

/-- Valid channel diagnostics can exist with no authority terminal. -/
theorem channelDiagnosticValid_not_authority_witness :
    ∃ s : ChannelSituation,
      ChannelDiagnosticValid s ∧ ¬ ChannelAuthorityTerminal s := by
  refine ⟨⟨true, true, true, false⟩, ?_, ?_⟩
  · exact ⟨rfl, rfl, rfl⟩
  · show ¬ (false = true)
    decide

theorem not_channelDiagnosticValid_implies_authority :
    ¬ (∀ s : ChannelSituation,
      ChannelDiagnosticValid s -> ChannelAuthorityTerminal s) := by
  intro h
  rcases channelDiagnosticValid_not_authority_witness with ⟨s, hValid, hNoAuth⟩
  exact hNoAuth (h s hValid)

end RDB07

end QM

#print axioms QM.RDB07.report_authorityEffectNone
#print axioms QM.RDB07.not_channelDiagnosticValid_implies_authority
