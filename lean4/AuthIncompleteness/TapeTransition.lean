/-
Provenance (recovery, 2026-10-21)
  source    : C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\formal\tape_transition_invariant_models.lean
  recovered : 2026-10-21
  status    : ported to Lean 4.35.0; statements unchanged
  module    : AuthIncompleteness.TapeTransition
-/
import AuthIncompleteness.TapeControl

/-!
# Finite transition and invariant models

Paper key: `authorization_an_incompleteness_theory`

This module adds one controlled transition lift to the tape-control seed. A
declared finite transition produces `advance`, `stay`, or `halt` reports and a
next configuration. It proves one supplied Boolean contract is preserved and
exhibits a concrete countertrace for a different supplied contract.

The result is not a definition of the general Turing machine, a theorem about
all semantic invariants, or a claim about P versus NP. The contracts are
declared model inputs. The finite examples show that transition syntax does not
select which contract is intended or establish preservation without a proof.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.TapeTransitionInvariantModels

open AuthorizationIncompleteness.TapeControlModels

/-- The whole finite carrier. Each constructor records one declared phase/cell
    combination without presenting an unbounded tape. -/
inductive Configuration where
  | runningBlank
  | runningMarked
  | haltedBlank
  | haltedMarked
  deriving DecidableEq, Repr

/-- A transition exposes a syntactic control outcome and its next
    configuration. -/
structure TransitionResult where
  outcome : ControlOutcome
  next : Configuration
  deriving DecidableEq, Repr

/-- A finite transition table. It writes the blank cell in every next state;
    this is a declared rule of this model, not an inferred physical law. -/
def transition (configuration : Configuration) : TransitionResult :=
  match configuration with
  | .runningBlank =>
    { outcome := .halt, next := .haltedBlank }
  | .runningMarked =>
    { outcome := .advance, next := .runningBlank }
  | .haltedBlank =>
    { outcome := .stay, next := .haltedBlank }
  | .haltedMarked =>
    { outcome := .stay, next := .haltedBlank }

/-- The next configuration selected by the declared transition table. -/
def nextConfiguration (configuration : Configuration) : Configuration :=
  (transition configuration).next

/-- The control-only report selected by the declared transition table. -/
def transitionControl (configuration : Configuration) : ControlOutcome :=
  (transition configuration).outcome

/-- A supplied Boolean contract on configurations. -/
structure ConfigurationContract where
  accepts : Configuration -> Bool

/-- A report is adequate for a contract when the contract is constant on every
    report fiber. This is the finite report-factorization condition, not a
    claim that every report carries the intended semantics. -/
def AdequateFor {Report : Type} (report : Configuration -> Report)
    (contract : ConfigurationContract) : Prop :=
  ∀ first second, report first = report second ->
    contract.accepts first = contract.accepts second

/-- Preservation is a separately proved property of a named contract and the
    declared transition; it is not a consequence of the word `transition`. -/
def Preserves (contract : ConfigurationContract) : Prop :=
  ∀ configuration, contract.accepts configuration = true ->
    contract.accepts (nextConfiguration configuration) = true

/-- A contract that rejects only the malformed halted/marked configuration. -/
def cleanTerminalContract : ConfigurationContract where
  accepts := fun configuration =>
    match configuration with
    | .runningBlank => true
    | .runningMarked => true
    | .haltedBlank => true
    | .haltedMarked => false

/-- A different supplied contract requiring a marked scanned cell. -/
def markedCellContract : ConfigurationContract where
  accepts := fun configuration =>
    match configuration with
    | .runningBlank => false
    | .runningMarked => true
    | .haltedBlank => false
    | .haltedMarked => true

/-- An identity report retains the whole finite configuration. It is a named
    positive comparison point, not a claim that such a report is available in
    a general computation model. -/
def fullConfigurationReport : Configuration -> Configuration := id

/-- The tiny table realizes each declared control outcome. -/
theorem transition_exposes_advance_stay_and_halt :
    transitionControl .runningMarked = .advance ∧
      transitionControl .haltedBlank = .stay ∧
      transitionControl .runningBlank = .halt := by
  exact ⟨rfl, rfl, rfl⟩

/-- Every output of the declared table satisfies the clean-terminal contract.
    This is a finite result about this table and this supplied contract. -/
theorem transition_output_satisfies_clean_terminal_contract :
    ∀ configuration : Configuration,
      cleanTerminalContract.accepts (nextConfiguration configuration) = true
  | .runningBlank => rfl
  | .runningMarked => rfl
  | .haltedBlank => rfl
  | .haltedMarked => rfl

/-- The preceding output fact yields a genuine preservation theorem for the
    same supplied contract. -/
theorem transition_preserves_clean_terminal_contract :
    Preserves cleanTerminalContract := by
  intro configuration _
  exact transition_output_satisfies_clean_terminal_contract configuration

/-- A concrete countertrace: the marked running configuration initially meets
    the marked-cell contract, but its declared successor does not. -/
theorem marked_contract_countertrace :
    markedCellContract.accepts .runningMarked = true ∧
      markedCellContract.accepts (nextConfiguration .runningMarked) = false := by
  exact ⟨rfl, rfl⟩

/-- The same transition does not preserve every supplied contract. -/
theorem transition_does_not_preserve_marked_cell_contract :
    ¬ Preserves markedCellContract := by
  intro preserves
  have impossible := preserves .runningMarked (by rfl)
  change (false : Bool) = true at impossible
  cases impossible

/-- The control-only report for two terminal configurations can coincide even
    when a supplied contract distinguishes their scanned cells. -/
theorem shared_stay_control_splits_marked_cell_contract :
    transitionControl .haltedBlank = transitionControl .haltedMarked ∧
      markedCellContract.accepts .haltedBlank = false ∧
      markedCellContract.accepts .haltedMarked = true := by
  exact ⟨rfl, rfl, rfl⟩

/-- A control-only reader cannot decide the marked-cell contract for every
    configuration in this finite model. -/
theorem shared_stay_control_blocks_control_only_contract_decider :
    ¬ (∃ decide : ControlOutcome -> Bool,
      ∀ configuration, decide (transitionControl configuration) =
        markedCellContract.accepts configuration) := by
  rintro ⟨decide, h⟩
  have blank : decide ControlOutcome.stay = false := by
    simpa [transitionControl, transition, markedCellContract] using
      h .haltedBlank
  have marked : decide ControlOutcome.stay = true := by
    simpa [transitionControl, transition, markedCellContract] using
      h .haltedMarked
  have impossible : (false : Bool) = true := blank.symm.trans marked
  cases impossible

/-- Retaining the entire configuration is adequate for the marked-cell
    contract in this finite carrier. -/
theorem full_configuration_report_adequate_for_marked_cell_contract :
    AdequateFor fullConfigurationReport markedCellContract := by
  intro first second reportEqual
  change first = second at reportEqual
  cases reportEqual
  rfl

/-- The full report consequently admits a scoped decision for the declared
    marked-cell contract. This is a finite local decision, not authorization
    of an arbitrary proposal. -/
theorem full_configuration_report_admits_marked_cell_decider :
    ∃ decide : Configuration -> Bool,
      ∀ configuration, decide configuration =
        markedCellContract.accepts configuration := by
  exact ⟨markedCellContract.accepts, fun _ => rfl⟩

/-- The control-only report is not adequate for the same contract: the two
    terminal configurations have the same `stay` report and different
    contract values. -/
theorem control_report_not_adequate_for_marked_cell_contract :
    ¬ AdequateFor transitionControl markedCellContract := by
  intro adequate
  have sameReport : transitionControl .haltedBlank =
      transitionControl .haltedMarked := by
    rfl
  have impossible := adequate .haltedBlank .haltedMarked sameReport
  change (false : Bool) = true at impossible
  cases impossible

end AuthorizationIncompleteness.TapeTransitionInvariantModels

#print axioms
  AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_exposes_advance_stay_and_halt
#print axioms
  AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_output_satisfies_clean_terminal_contract
#print axioms
  AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_preserves_clean_terminal_contract
#print axioms
  AuthorizationIncompleteness.TapeTransitionInvariantModels.marked_contract_countertrace
#print axioms
  AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_does_not_preserve_marked_cell_contract
#print axioms
  AuthorizationIncompleteness.TapeTransitionInvariantModels.shared_stay_control_blocks_control_only_contract_decider
#print axioms
  AuthorizationIncompleteness.TapeTransitionInvariantModels.full_configuration_report_adequate_for_marked_cell_contract
#print axioms
  AuthorizationIncompleteness.TapeTransitionInvariantModels.full_configuration_report_admits_marked_cell_decider
#print axioms
  AuthorizationIncompleteness.TapeTransitionInvariantModels.control_report_not_adequate_for_marked_cell_contract
