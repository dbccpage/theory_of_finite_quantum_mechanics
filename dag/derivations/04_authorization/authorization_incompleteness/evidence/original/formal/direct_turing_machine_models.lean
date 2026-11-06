/-!
# Direct finite-rule Turing-style syntax and bounded operational semantics

Paper key: `authorization_an_incompleteness_theory`

This is a direct finite-rule operational seed, not a universal-machine
proof. A machine has a finite rule list, an unbounded total tape, a
designated halt state, and a left-biased rule lookup. The evaluator is
fuel-bounded. It therefore makes the syntactic meaning of a declared
halt precise: the current configuration is in the machine's designated
halt state.

It does not prove that this syntax is Turing complete, encode a universal
machine, solve the halting problem, formalize Rice's theorem, or say
anything about P versus NP. A halt result is deliberately distinct from
a supplied terminal policy.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.DirectTuringMachineModels

/-- A finite tape alphabet with an explicit blank symbol. -/
inductive TapeSymbol where
  | blank
  | marked
  deriving DecidableEq, Repr

/-- A finite transition may move the head left, right, or not at all. -/
inductive Move where
  | left
  | right
  | stay
  deriving DecidableEq, Repr

/-- One finite transition-table row. -/
structure Rule where
  state : Nat
  scanned : TapeSymbol
  nextState : Nat
  write : TapeSymbol
  move : Move
  deriving DecidableEq, Repr

/-- A total tape has a declared symbol at every integer position. Meta-level
    absence is not represented by this carrier. -/
abbrev Tape := Int -> TapeSymbol

/-- A machine configuration carries control, head position, and total tape. -/
structure Configuration where
  state : Nat
  head : Int
  tape : Tape

/-- A finite machine code is a designated halt state plus a finite rule list.
    The rule-list order is part of the declared operational semantics. -/
structure Machine where
  haltState : Nat
  rules : List Rule

/-- The evaluator distinguishes a syntactic halt, a missing rule, and a fuel
    boundary. None is an authorization outcome. -/
inductive StepResult where
  | next (configuration : Configuration)
  | halted
  | stuck
  | fuelExhausted (configuration : Configuration)

/-- Equality test for the finite tape alphabet. -/
def tapeSymbolEq (left right : TapeSymbol) : Bool :=
  match left, right with
  | .blank, .blank => true
  | .marked, .marked => true
  | _, _ => false

/-- A rule matches the currently declared state and scanned symbol. -/
def Rule.matches (rule : Rule) (configuration : Configuration) : Bool :=
  (rule.state == configuration.state) &&
    tapeSymbolEq rule.scanned (configuration.tape configuration.head)

/-- Lookup is left-biased, so even malformed duplicate rule lists have a
    deterministic operational reading. A later universality theorem must
    state whatever well-formedness discipline it needs separately. -/
def lookup (machine : Machine) (configuration : Configuration) : Option Rule :=
  machine.rules.find? (fun rule => rule.matches configuration)

/-- Write one declared tape position while retaining all other positions. -/
def writeAt (tape : Tape) (position : Int) (symbol : TapeSymbol) : Tape :=
  fun index => if index = position then symbol else tape index

/-- Apply one syntactic head movement. -/
def applyMove (move : Move) (head : Int) : Int :=
  match move with
  | .left => head - 1
  | .right => head + 1
  | .stay => head

/-- Apply a matched transition row to a configuration. -/
def applyRule (rule : Rule) (configuration : Configuration) : Configuration where
  state := rule.nextState
  head := applyMove rule.move configuration.head
  tape := writeAt configuration.tape configuration.head rule.write

/-- The Boolean operational halt test. -/
def isDeclaredHalt (machine : Machine) (configuration : Configuration) : Bool :=
  configuration.state == machine.haltState

/-- This proposition is the whole syntactic meaning of a declared halt. -/
def DeclaredHalt (machine : Machine) (configuration : Configuration) : Prop :=
  isDeclaredHalt machine configuration = true

/-- Take one declared operational step. -/
def step (machine : Machine) (configuration : Configuration) : StepResult :=
  match isDeclaredHalt machine configuration with
  | true => .halted
  | false =>
    match lookup machine configuration with
    | none => .stuck
    | some rule => .next (applyRule rule configuration)

/-- Evaluate for at most the stated number of transitions. Fuel exhaustion
    is not non-halting; it is a bounded-evaluator result. -/
def execute (machine : Machine) : Nat -> Configuration -> StepResult
  | 0, configuration =>
    match isDeclaredHalt machine configuration with
    | true => .halted
    | false => .fuelExhausted configuration
  | fuel + 1, configuration =>
    match step machine configuration with
    | .next nextConfiguration => execute machine fuel nextConfiguration
    | .halted => .halted
    | .stuck => .stuck
    | .fuelExhausted boundedConfiguration => .fuelExhausted boundedConfiguration

/-- A terminal policy is extra supplied structure over an operational result. -/
structure TerminalPolicy where
  decide : StepResult -> Bool

/-- One possible policy licenses the declared halt result. -/
def acceptHalted : TerminalPolicy where
  decide := fun result =>
    match result with
    | .halted => true
    | _ => false

/-- Another possible policy leaves every operational result unlicensed. -/
def leaveAllOpen : TerminalPolicy where
  decide := fun _ => false

/-- A total all-blank tape. -/
def blankTape : Tape := fun _ => .blank

/-- The initial configuration for the one-rule demonstration machine. -/
def initialConfiguration : Configuration where
  state := 0
  head := 0
  tape := blankTape

/-- The one rule writes a mark and enters the designated halt state. -/
def writeAndHaltRule : Rule where
  state := 0
  scanned := .blank
  nextState := 1
  write := .marked
  move := .stay

/-- A finite direct machine used only as a closed operational fixture. -/
def writeAndHaltMachine : Machine where
  haltState := 1
  rules := [writeAndHaltRule]

/-- A finite machine with no matching transition and no declared halt. -/
def stuckMachine : Machine where
  haltState := 1
  rules := []

/-- One transition that deliberately returns to the same non-halt state. -/
def loopingRule : Rule where
  state := 0
  scanned := .blank
  nextState := 0
  write := .blank
  move := .stay

/-- A finite fixture whose bounded evaluation can exhaust its fuel. -/
def loopingMachine : Machine where
  haltState := 1
  rules := [loopingRule]

/-- A tape blank is a declared symbol, while an unread/absent observation
    would require a separately typed report carrier. -/
theorem blank_symbol_is_not_option_absence :
    (some TapeSymbol.blank : Option TapeSymbol) ≠ none := by
  intro impossible
  cases impossible

/-- The declared halt state is exactly what makes one step syntactically
    terminal. This does not assign a semantic or policy meaning to it. -/
theorem step_halted_iff_declared_halt
    (machine : Machine) (configuration : Configuration) :
    step machine configuration = .halted ↔ DeclaredHalt machine configuration := by
  cases halted : isDeclaredHalt machine configuration with
  | false =>
    cases hlookup : lookup machine configuration <;>
      simp [step, DeclaredHalt, halted, hlookup]
  | true =>
    simp [step, DeclaredHalt, halted]

/-- A bounded evaluator reports a declared halt immediately at any fuel
    budget. -/
theorem execute_halted_of_declared_halt
    (machine : Machine) (fuel : Nat) (configuration : Configuration)
    (halted : DeclaredHalt machine configuration) :
    execute machine fuel configuration = .halted := by
  unfold DeclaredHalt at halted
  cases hhalt : isDeclaredHalt machine configuration with
  | false =>
    simp [hhalt] at halted
  | true =>
    cases fuel <;> simp [execute, step, hhalt]

/-- The fixture's declared transition writes the marked symbol at the head. -/
theorem write_and_halt_transition_writes_mark :
    (applyRule writeAndHaltRule initialConfiguration).tape 0 =
      TapeSymbol.marked := by
  rfl

/-- The fixture reaches its designated halt state after its one transition. -/
theorem write_and_halt_transition_reaches_declared_halt :
    DeclaredHalt writeAndHaltMachine
      (applyRule writeAndHaltRule initialConfiguration) := by
  rfl

/-- A missing matching row is a syntactic stuck result, not a semantic
    rejection. -/
theorem empty_rule_fixture_is_stuck :
    step stuckMachine initialConfiguration = .stuck := by
  rfl

/-- Following one non-halt transition with a zero remaining budget yields
    fuel exhaustion. It is not a proof that the machine never halts. -/
theorem looping_fixture_exhausts_bounded_fuel :
    execute loopingMachine 1 initialConfiguration =
      .fuelExhausted (applyRule loopingRule initialConfiguration) := by
  rfl

/-- A one-transition bounded execution of the fixture returns the syntactic
    halt result, rather than an authorization result. -/
theorem write_and_halt_executes_to_syntactic_halt :
    execute writeAndHaltMachine 1 initialConfiguration = .halted := by
  rfl

/-- The same syntactic halt result admits distinct supplied terminal policies. -/
theorem syntactic_halt_does_not_select_direct_machine_policy :
    acceptHalted.decide StepResult.halted = true ∧
      leaveAllOpen.decide StepResult.halted = false := by
  exact ⟨rfl, rfl⟩

end AuthorizationIncompleteness.DirectTuringMachineModels

#print axioms
  AuthorizationIncompleteness.DirectTuringMachineModels.blank_symbol_is_not_option_absence
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineModels.step_halted_iff_declared_halt
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineModels.execute_halted_of_declared_halt
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_transition_writes_mark
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_transition_reaches_declared_halt
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineModels.empty_rule_fixture_is_stuck
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineModels.looping_fixture_exhausts_bounded_fuel
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_executes_to_syntactic_halt
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineModels.syntactic_halt_does_not_select_direct_machine_policy
