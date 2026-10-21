import global_computability_lift_models

/-!
# Terminalization consequence of a class-relative no-decider boundary

Paper key: `authorization_an_incompleteness_theory`

This module is an abstract adapter, not Rice's theorem. Given a declared
decision class and an explicit premise that no total decider for a validity
predicate belongs to that class, it proves two narrow consequences:

1. a terminalizer whose `authorized` bit is allowed, acceptance-sound, and
   acceptance-complete would yield the prohibited Boolean decider; and
2. a terminalizer that is also rejection-sound and never returns `open` is
   acceptance-complete, so it is likewise prohibited.

The second result does not say that every terminalizer must return `open`.
It says that, under the named no-decider premise and allowed-class closure,
a closed terminalizer must fail one of the two semantic soundness conditions.
A finite Boolean fixture shows that bounded decidable terminalization remains
possible when the no-decider premise does not hold.

This module has no program encoding, universal-machine result, Rice proof,
Goedel proof, LLM model, physical-placement model, custody claim, or replay
protocol theorem.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.TerminalAuthorizationBoundary

open AuthorizationIncompleteness.GlobalComputabilityLift

/-- The semantic terminal vocabulary separates a positive authorization,
    a semantically supported rejection, and an unresolved result. -/
inductive AuthorizationTerminal where
  | authorized
  | rejected
  | unresolved
  deriving DecidableEq, Repr

/-- The Boolean decision extracted from a terminalizer: only `authorized`
    counts as true. A later computability lift must separately show that this
    extraction belongs to its declared computable decision class. -/
def acceptanceBit {Proposal : Type}
    (terminalize : Proposal -> AuthorizationTerminal) : Proposal -> Bool :=
  fun proposal => terminalize proposal == .authorized

/-- No invalid proposal is given the positive authorization terminal. -/
def AcceptanceSound {Proposal : Type} (valid : Proposal -> Prop)
    (terminalize : Proposal -> AuthorizationTerminal) : Prop :=
  ∀ proposal, terminalize proposal = .authorized -> valid proposal

/-- Every valid proposal receives the positive authorization terminal. -/
def AcceptanceComplete {Proposal : Type} (valid : Proposal -> Prop)
    (terminalize : Proposal -> AuthorizationTerminal) : Prop :=
  ∀ proposal, valid proposal -> terminalize proposal = .authorized

/-- No valid proposal is given the rejection terminal. This is distinct from
    acceptance soundness and is needed for the closed-terminal consequence. -/
def RejectionSound {Proposal : Type} (valid : Proposal -> Prop)
    (terminalize : Proposal -> AuthorizationTerminal) : Prop :=
  ∀ proposal, terminalize proposal = .rejected -> ¬ valid proposal

/-- A closed terminalizer has no unresolved `open` result on its stated
    carrier. This definition says nothing about physical or organizational
    placement. -/
def TerminalClosed {Proposal : Type}
    (terminalize : Proposal -> AuthorizationTerminal) : Prop :=
  ∀ proposal, terminalize proposal ≠ .unresolved

/-- The extracted Boolean bit is true exactly at positive authorization. -/
theorem acceptance_bit_true_iff {Proposal : Type}
    (terminalize : Proposal -> AuthorizationTerminal) (proposal : Proposal) :
    acceptanceBit terminalize proposal = true ↔
      terminalize proposal = .authorized := by
  cases terminal : terminalize proposal <;> simp [acceptanceBit, terminal]

/-- Acceptance soundness and acceptance completeness make the extracted
    terminal bit a total decider for the supplied validity predicate. -/
theorem acceptance_bit_decides_of_sound_complete {Proposal : Type}
    {valid : Proposal -> Prop}
    (terminalize : Proposal -> AuthorizationTerminal)
    (sound : AcceptanceSound valid terminalize)
    (complete : AcceptanceComplete valid terminalize) :
    Decides valid (acceptanceBit terminalize) := by
  intro proposal
  constructor
  · intro accepted
    exact sound proposal
      ((acceptance_bit_true_iff terminalize proposal).mp accepted)
  · intro validProposal
    exact (acceptance_bit_true_iff terminalize proposal).mpr
      (complete proposal validProposal)

/-- Under an explicit class-relative no-decider premise, an allowed terminal
    acceptance bit cannot be both sound and complete for the semantic
    predicate. This is not a Rice theorem; the no-decider premise is supplied. -/
theorem no_total_decider_blocks_sound_complete_authorization
    {Proposal : Type} {valid : Proposal -> Prop}
    {allowed : (Proposal -> Bool) -> Prop}
    (terminalize : Proposal -> AuthorizationTerminal)
    (noTotalDecider : NoTotalDecider allowed valid)
    (allowedAcceptanceBit : allowed (acceptanceBit terminalize))
    (sound : AcceptanceSound valid terminalize)
    (complete : AcceptanceComplete valid terminalize) : False := by
  apply noTotalDecider
  exact ⟨acceptanceBit terminalize, allowedAcceptanceBit,
    acceptance_bit_decides_of_sound_complete terminalize sound complete⟩

/-- If rejection is semantically sound and no case is left open, every valid
    proposal must be authorized. This bridge contains no no-decider premise. -/
theorem closed_two_sided_terminalization_is_acceptance_complete
    {Proposal : Type} {valid : Proposal -> Prop}
    (terminalize : Proposal -> AuthorizationTerminal)
    (rejectionSound : RejectionSound valid terminalize)
    (closed : TerminalClosed terminalize) :
    AcceptanceComplete valid terminalize := by
  intro proposal validProposal
  cases terminal : terminalize proposal with
  | authorized => rfl
  | rejected =>
    exact False.elim ((rejectionSound proposal terminal) validProposal)
  | unresolved =>
    exact False.elim ((closed proposal) terminal)

/-- The precise terminal consequence of a class-relative no-decider boundary.
    If the terminalizer's acceptance bit belongs to the allowed class, it cannot
    jointly be acceptance-sound, rejection-sound, and closed. Therefore the
    theorem leaves three explicit possibilities: an unsound positive result, an
    unsound rejection, or an unresolved case. -/
theorem no_total_decider_blocks_closed_two_sided_terminalization
    {Proposal : Type} {valid : Proposal -> Prop}
    {allowed : (Proposal -> Bool) -> Prop}
    (terminalize : Proposal -> AuthorizationTerminal)
    (noTotalDecider : NoTotalDecider allowed valid)
    (allowedAcceptanceBit : allowed (acceptanceBit terminalize))
    (acceptanceSound : AcceptanceSound valid terminalize)
    (rejectionSound : RejectionSound valid terminalize)
    (closed : TerminalClosed terminalize) : False := by
  exact no_total_decider_blocks_sound_complete_authorization terminalize
    noTotalDecider allowedAcceptanceBit acceptanceSound
    (closed_two_sided_terminalization_is_acceptance_complete terminalize
      rejectionSound closed)

/-- A finite decidable validity predicate used to fence the global conclusion.
    It is intentionally a local Boolean contract. -/
def boolValidity (proposal : Bool) : Prop := proposal = true

/-- A finite closed terminalizer can authorize a true Boolean and reject a
    false Boolean. Its existence shows that no-open behavior is not forbidden
    without a no-decider premise. -/
def boolTerminalize : Bool -> AuthorizationTerminal
  | true => .authorized
  | false => .rejected

theorem bool_terminalization_acceptance_sound :
    AcceptanceSound boolValidity boolTerminalize := by
  intro proposal authorized
  cases proposal <;> simp [boolValidity, boolTerminalize] at authorized ⊢

theorem bool_terminalization_acceptance_complete :
    AcceptanceComplete boolValidity boolTerminalize := by
  intro proposal validProposal
  cases proposal <;> simp [boolValidity, boolTerminalize] at validProposal ⊢

theorem bool_terminalization_rejection_sound :
    RejectionSound boolValidity boolTerminalize := by
  intro proposal rejected validProposal
  cases proposal <;> simp [boolValidity, boolTerminalize] at rejected validProposal

theorem bool_terminalization_closed :
    TerminalClosed boolTerminalize := by
  intro proposal opened
  cases proposal <;> simp [boolTerminalize] at opened

/-- The finite Boolean fixture is a closed two-sided sound terminalizer. It is
    compatible with the global theorem because its validity predicate has an
    ordinary total Boolean decider. -/
theorem finite_closed_terminalizer_remains_possible :
    AcceptanceSound boolValidity boolTerminalize ∧
      AcceptanceComplete boolValidity boolTerminalize ∧
      RejectionSound boolValidity boolTerminalize ∧
      TerminalClosed boolTerminalize := by
  exact ⟨bool_terminalization_acceptance_sound,
    bool_terminalization_acceptance_complete,
    bool_terminalization_rejection_sound,
    bool_terminalization_closed⟩

end AuthorizationIncompleteness.TerminalAuthorizationBoundary

#print axioms
  AuthorizationIncompleteness.TerminalAuthorizationBoundary.acceptance_bit_decides_of_sound_complete
#print axioms
  AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_sound_complete_authorization
#print axioms
  AuthorizationIncompleteness.TerminalAuthorizationBoundary.closed_two_sided_terminalization_is_acceptance_complete
#print axioms
  AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_closed_two_sided_terminalization
#print axioms
  AuthorizationIncompleteness.TerminalAuthorizationBoundary.finite_closed_terminalizer_remains_possible
