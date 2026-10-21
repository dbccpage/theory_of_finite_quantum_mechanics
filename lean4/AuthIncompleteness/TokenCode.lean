/-
Provenance (recovery, 2026-10-21)
  source    : C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\formal\direct_turing_machine_token_code_models.lean
  recovered : 2026-10-21
  status    : ported to Lean 4.35.0; statements unchanged
  module    : AuthIncompleteness.TokenCode
-/
import AuthIncompleteness.DirectTM

/-!
# Finite token-code grammar for the direct Turing-style machine seed

Paper key: `authorization_an_incompleteness_theory`

This module gives the DTM0 finite-rule `Machine` carrier a declared
finite token-code grammar and a total encoder / partial decoder pair.
One machine code consists of a halt-state token followed by complete
five-token rule frames:

```text
state, scanned-symbol tag, next-state, written-symbol tag, movement tag
```

The decoder consumes the entire finite token list and rejects an empty
header, a truncated frame, and invalid tags. It proves only that decoding
the encoder's finite token code recovers the same DTM0 `Machine` value.

The tokens are natural numbers, not bytes or source text. This module does
not encode configurations or inputs, prove parser-to-execution trace
agreement, supply an unbounded evaluator, establish universality, or make
a halting, Rice, Godel, LLM, replay-custody, or authorization claim.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels

open AuthorizationIncompleteness.DirectTuringMachineModels

/-- Canonical finite tag for a declared tape symbol. -/
def encodeTapeSymbol : TapeSymbol -> Nat
  | .blank => 0
  | .marked => 1

/-- Partial decoder for the two declared tape-symbol tags. -/
def decodeTapeSymbol : Nat -> Option TapeSymbol
  | 0 => some .blank
  | 1 => some .marked
  | _ => none

/-- Canonical finite tag for a declared head movement. -/
def encodeMove : Move -> Nat
  | .left => 0
  | .right => 1
  | .stay => 2

/-- Partial decoder for the three declared movement tags. -/
def decodeMove : Nat -> Option Move
  | 0 => some .left
  | 1 => some .right
  | 2 => some .stay
  | _ => none

/-- One rule is a complete five-token frame. -/
def encodeRule (rule : Rule) : List Nat :=
  [rule.state, encodeTapeSymbol rule.scanned, rule.nextState,
    encodeTapeSymbol rule.write, encodeMove rule.move]

/-- A finite rule-list code is the concatenation of complete rule frames. -/
def encodeRules : List Rule -> List Nat
  | [] => []
  | rule :: rules => encodeRule rule ++ encodeRules rules

/-- Parse complete rule frames only. Any incomplete suffix or invalid tag is
    rejected rather than ignored. -/
def decodeRules : List Nat -> Option (List Rule)
  | [] => some []
  | state :: scannedCode :: nextState :: writtenCode :: moveCode :: rest =>
    match decodeTapeSymbol scannedCode with
    | none => none
    | some scanned =>
      match decodeTapeSymbol writtenCode with
      | none => none
      | some written =>
        match decodeMove moveCode with
        | none => none
        | some move =>
          match decodeRules rest with
          | none => none
          | some rules =>
            some (Rule.mk state scanned nextState written move :: rules)
  | _ => none

/-- One finite machine code is a halt-state token followed by a complete
    rule-list code. -/
def encodeMachine (machine : Machine) : List Nat :=
  machine.haltState :: encodeRules machine.rules

/-- Parse a machine only when its whole remaining code is a complete rule list. -/
def decodeMachine : List Nat -> Option Machine
  | [] => none
  | haltState :: ruleCode =>
    match decodeRules ruleCode with
    | none => none
    | some rules => some { haltState := haltState, rules := rules }

/-- Every declared tape-symbol tag decodes to the originating symbol. -/
theorem decodeTapeSymbol_encodeTapeSymbol (symbol : TapeSymbol) :
    decodeTapeSymbol (encodeTapeSymbol symbol) = some symbol := by
  cases symbol <;> rfl

/-- Every declared movement tag decodes to the originating movement. -/
theorem decodeMove_encodeMove (move : Move) :
    decodeMove (encodeMove move) = some move := by
  cases move <;> rfl

/-- Decoding the token frames emitted for a rule list recovers that list. -/
theorem decodeRules_encodeRules (rules : List Rule) :
    decodeRules (encodeRules rules) = some rules := by
  induction rules with
  | nil => rfl
  | cons rule rules inductionHypothesis =>
    cases rule with
    | mk state scanned nextState written move =>
      simp [encodeRules, encodeRule, decodeRules,
        decodeTapeSymbol_encodeTapeSymbol, decodeMove_encodeMove,
        inductionHypothesis]

/-- Decoding the finite token code emitted for a DTM0 machine recovers the
    same finite rule-list machine. -/
theorem decodeMachine_encodeMachine (machine : Machine) :
    decodeMachine (encodeMachine machine) = some machine := by
  cases machine with
  | mk haltState rules =>
    simp [encodeMachine, decodeMachine, decodeRules_encodeRules]

/-- A machine code needs its halt-state header. -/
theorem empty_machine_code_is_rejected :
    decodeMachine [] = none := by
  rfl

/-- A partial rule frame is rejected rather than silently ignored. -/
theorem truncated_rule_code_is_rejected :
    decodeMachine [0, 0, 0, 1] = none := by
  rfl

/-- A tag outside the declared two-symbol alphabet is rejected. -/
theorem invalid_symbol_tag_is_rejected :
    decodeMachine [0, 0, 2, 1, 0, 0] = none := by
  rfl

/-- A tag outside the declared three-movement alphabet is rejected. -/
theorem invalid_move_tag_is_rejected :
    decodeMachine [0, 0, 0, 1, 0, 3] = none := by
  rfl

end AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels

#print axioms
  AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeTapeSymbol_encodeTapeSymbol
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMove_encodeMove
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeRules_encodeRules
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMachine_encodeMachine
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.empty_machine_code_is_rejected
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.truncated_rule_code_is_rejected
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_symbol_tag_is_rejected
#print axioms
  AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_move_tag_is_rejected
