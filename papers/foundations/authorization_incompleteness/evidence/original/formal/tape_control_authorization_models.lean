/-!
# Tape control to authorization: finite operational models

Paper key: `authorization_an_incompleteness_theory`

This is a deliberately small tape-control presentation. It models a
declared blank cell and declared control outcomes (`advance`, `stay`, or
`halt`). It proves that a shared syntactic halt outcome neither decides a
content contract nor selects a terminal policy. It also distinguishes a
declared tape symbol from an `unread` observation report, and shows that
the same read token can be given different supplied semantic adapters.

It is not a formalization of the full standard Turing-machine model,
Rice's theorem, or P versus NP. In particular, `blank` is a declared
alphabet member in this model; it is not a claim about meta-level
absence.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.TapeControlModels

/-- A finite tape alphabet with a declared blank symbol. -/
inductive TapeCell where
  | blank
  | marked
  deriving DecidableEq, Repr

/-- The syntactic control outcome of one declared transition. -/
inductive ControlOutcome where
  | advance
  | stay
  | halt
  deriving DecidableEq, Repr

/-- The observable part of a tiny tape-control configuration. -/
structure TapeControlPresentation where
  scanned : TapeCell
  outcome : ControlOutcome

/-- A blank-cell configuration that reaches the declared halt outcome. -/
def haltingBlankPresentation : TapeControlPresentation where
  scanned := .blank
  outcome := .halt

/-- A marked-cell configuration that reaches the same halt outcome. -/
def haltingMarkedPresentation : TapeControlPresentation where
  scanned := .marked
  outcome := .halt

/-- A control-only report deliberately forgets the scanned cell. -/
def controlReport (presentation : TapeControlPresentation) : ControlOutcome :=
  presentation.outcome

/-- Whether the small observer exposes the scanned tape cell. This is a
    control choice, not a member of the tape alphabet. -/
inductive ReadControl where
  | read
  | unread
  deriving DecidableEq, Repr

/-- A report emitted by the controlled observation. `unread` is not another
    tape symbol: it records that this observer did not expose a cell. -/
inductive ReadReport where
  | unread
  | observed (cell : TapeCell)
  deriving DecidableEq, Repr

/-- Read is syntactic selection from the declared presentation. -/
def readCell (presentation : TapeControlPresentation) : TapeCell :=
  presentation.scanned

/-- A controlled observer either exposes the selected symbol or reports that
    it did not expose one. -/
def readReport (control : ReadControl)
    (presentation : TapeControlPresentation) : ReadReport :=
  match control with
  | .read => .observed (readCell presentation)
  | .unread => .unread

/-- A semantic adapter is additional supplied structure over a read token. -/
structure SemanticAdapter where
  decide : TapeCell -> Bool

/-- One declared interpretation of the blank mark. -/
def blankAcceptingAdapter : SemanticAdapter where
  decide := fun cell =>
    match cell with
    | .blank => true
    | .marked => false

/-- Another declared interpretation of the same marks. -/
def blankRejectingAdapter : SemanticAdapter where
  decide := fun _ => false

/-- A content contract that distinguishes the two halting presentations.
    The contract is supplied structure, not a consequence of control. -/
def contentContract (presentation : TapeControlPresentation) : Bool :=
  match presentation.scanned with
  | .blank =>
    match presentation.outcome with
    | .advance => false
    | .stay => false
    | .halt => true
  | .marked => false

/-- The terminal action licensed by an organization or protocol after a
    control outcome. It is additional to the transition rule. -/
structure TerminalPolicy where
  decide : ControlOutcome -> Bool

/-- One possible policy accepts the syntactic halt outcome. -/
def acceptHalt : TerminalPolicy where
  decide := fun outcome =>
    match outcome with
    | .advance => false
    | .stay => false
    | .halt => true

/-- Another possible policy rejects every control outcome. -/
def rejectAll : TerminalPolicy where
  decide := fun _ => false

theorem blank_is_a_declared_tape_cell :
    haltingBlankPresentation.scanned = TapeCell.blank := by
  rfl

theorem halting_presentations_share_control_report :
    controlReport haltingBlankPresentation =
      controlReport haltingMarkedPresentation := by
  rfl

theorem read_is_syntactic_selection :
    readCell haltingBlankPresentation = TapeCell.blank := by
  rfl

theorem unread_report_forgets_scanned_cell :
    readReport ReadControl.unread haltingBlankPresentation =
      readReport ReadControl.unread haltingMarkedPresentation := by
  rfl

theorem same_read_token_allows_distinct_semantic_adapters :
    blankAcceptingAdapter.decide (readCell haltingBlankPresentation) = true /\
      blankRejectingAdapter.decide (readCell haltingBlankPresentation) = false := by
  exact ⟨rfl, rfl⟩

theorem shared_halt_control_splits_content_contract :
    contentContract haltingBlankPresentation = true /\
      contentContract haltingMarkedPresentation = false := by
  exact ⟨rfl, rfl⟩

theorem syntactic_halt_does_not_select_terminal_policy :
    acceptHalt.decide ControlOutcome.halt = true /\
      rejectAll.decide ControlOutcome.halt = false := by
  exact ⟨rfl, rfl⟩

/-- A control-only decision cannot decide the supplied contract for all
    presentations because the two examples share a halt report. -/
theorem same_halt_control_blocks_control_only_decider :
    ¬ (∃ decide : ControlOutcome -> Bool,
      ∀ presentation, decide (controlReport presentation) =
        contentContract presentation) := by
  rintro ⟨decide, h⟩
  have blank : decide ControlOutcome.halt = true := by
    simpa [controlReport, contentContract, haltingBlankPresentation] using
      h haltingBlankPresentation
  have marked : decide ControlOutcome.halt = false := by
    simpa [controlReport, contentContract, haltingMarkedPresentation] using
      h haltingMarkedPresentation
  have impossible : (true : Bool) = false := blank.symm.trans marked
  cases impossible

/-- An observer which reports only `unread` cannot decide a contract that
    distinguishes the hidden cell. -/
theorem unread_report_blocks_content_decider :
    ¬ (∃ decide : ReadReport -> Bool,
      ∀ presentation, decide (readReport ReadControl.unread presentation) =
        contentContract presentation) := by
  rintro ⟨decide, h⟩
  have blank : decide ReadReport.unread = true := by
    simpa [readReport, contentContract, haltingBlankPresentation] using
      h haltingBlankPresentation
  have marked : decide ReadReport.unread = false := by
    simpa [readReport, contentContract, haltingMarkedPresentation] using
      h haltingMarkedPresentation
  have impossible : (true : Bool) = false := blank.symm.trans marked
  cases impossible

end AuthorizationIncompleteness.TapeControlModels

#print axioms AuthorizationIncompleteness.TapeControlModels.blank_is_a_declared_tape_cell
#print axioms AuthorizationIncompleteness.TapeControlModels.shared_halt_control_splits_content_contract
#print axioms AuthorizationIncompleteness.TapeControlModels.same_read_token_allows_distinct_semantic_adapters
#print axioms AuthorizationIncompleteness.TapeControlModels.syntactic_halt_does_not_select_terminal_policy
#print axioms AuthorizationIncompleteness.TapeControlModels.same_halt_control_blocks_control_only_decider
#print axioms AuthorizationIncompleteness.TapeControlModels.unread_report_blocks_content_decider
