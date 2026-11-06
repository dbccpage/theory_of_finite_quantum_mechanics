# Lean finite models

**AuthorityEffect:** None.

The eleven files are intentionally outside the sealed derivation. They are
rooted by the named GenX Lake target `AuthorizationIncompletenessTheory`;
they are not a default target and they make no estate-close claim.

- `authorization_incompleteness_core.lean` is a self-contained
  restatement of PO-000's report-factorization shape, not a replacement
  for PO-000.
- `direct_turing_machine_models.lean` is a direct finite-rule,
  Turing-style operational seed. It defines a total mathematical tape,
  left-biased lookup, fuel-bounded execution, and syntactic terminal
  states. It is not a universal machine or a program-byte encoding.
- `direct_turing_machine_token_code_models.lean` gives the DTM0 finite
  rule-list carrier a complete `List Nat` token grammar and a
  decoder-after-encoder round trip, with empty, truncated, invalid-symbol,
  and invalid-movement rejection fixtures. It is not source bytes, an
  input/configuration encoding, parser-to-execution correspondence, or
  universality.
- `global_computability_lift_models.lean` is an axiom-free,
  class-relative reduction transport. It does not formalize Rice's
  theorem or call arbitrary Boolean functions computable.
- `terminal_authorization_boundary_models.lean` is a conditional
  terminalization bridge. It requires a supplied class-relative
  no-decider premise and allowed acceptance-bit membership; its finite
  Boolean fixture preserves closed local terminalization. It does not
  prove Rice's theorem, model an LLM, or establish physical externality.
- `primitive_difference_authorization_models.lean` is a finite
  non-uniqueness model over a minimal Primitive Difference analogue. It
  is not yet a binding to the full J011 interface.
- `logical_externality_models.lean` is a finite site-label model showing
  that physical separation is neither necessary nor sufficient for a
  bounded authorization result.
- `replay_packet_binding_models.lean` is a finite structural replay
  model. It distinguishes a supplied trust root from a source
  submission, rejects selected substitutions, and keeps terminal policy
  separate from verification. Its equality is not a cryptographic hash.
- `tape_control_authorization_models.lean` is a finite operational
  model separating observation control, read-token interpretation,
  control terminality, content contracts, and policy.
- `tape_transition_invariant_models.lean` is a finite, exhaustive
  transition-table model. It proves preservation for one supplied
  Boolean contract and a named countertrace for another.
- `primitive_difference_p0_bridge.lean` imports J011's actual
  `PrimitiveDifference` quotient interface and specializes the P0
  factorization boundary to `pdProj P`.

Replay the rooted target from the existing GenX Lake environment:

```powershell
Set-Location lean4\genx
lake build AuthorizationIncompletenessTheory
```

The target built successfully on 2026-08-21 (40 jobs). The four theorems in
`authorization_incompleteness_core.lean`, the four printed Primitive
Difference theorems, the four printed logical-externality theorems, and
the six printed tape-control theorems had no axiom dependencies. The two
printed global-transport theorems and the seven printed replay-packet
theorems also had no axiom dependencies. The nine printed transition-model
theorems also had no axiom dependencies.

The direct-machine blank/absence and closed write/reaches-halt fixture
declarations have no axiom dependencies. Its generic syntactic-halt,
bounded-halt, closed stuck/fuel fixtures, closed execution, and
terminal-policy declarations depend on `propext`. This is a recorded
proof ceiling, not an issue hidden by the successful build.

The DTM1 tag round trips print no axioms. Its rule-list and machine parser
round trips plus empty, truncated, invalid-symbol, and invalid-movement
fixtures print `propext`. This records the finite grammar's exact theorem
ceiling; it does not promote it to a source-byte parser or an admitted
program carrier.

The terminalization bridge's
`acceptance_bit_decides_of_sound_complete`,
`no_total_decider_blocks_sound_complete_authorization`,
`no_total_decider_blocks_closed_two_sided_terminalization`, and
`finite_closed_terminalizer_remains_possible` declarations print
`propext`. Its
`closed_two_sided_terminalization_is_acceptance_complete` declaration
prints no axioms. These conditional results do not supply the no-decider
premise, a program carrier, or a Rice theorem.

The bridge proves a nontrivial quotient specialization. Its two negative
theorems and its Boolean collapse instance depend on `propext` and
`Quot.sound`, inherited through J011's `pdProj_eq_iff_zeroRel`. Its
positive quotient-lift theorem has no axiom dependencies. The bridge is
a statement-level correspondence to PO-000 because PO-000 has no Lake
module to import; it does not modify PO-000.

`tape_control_authorization_models.lean` is a second, deliberately
small model: a declared blank cell and a declared halt control outcome
do not select either a semantic contract or a terminal policy. It is a
tape-control analogy, not a formalization of the full standard Turing
machine model. Its `unread` report is deliberately distinct from the
tape alphabet, and its two semantic adapters are supplied alternatives,
not claims about the meaning of a standard Turing-machine symbol.

`tape_transition_invariant_models.lean` is the next controlled lift. Its
four-configuration carrier has a named transition table, not an
unbounded tape. The table realizes `advance`, `stay`, and `halt`; it
preserves the named `cleanTerminalContract` and violates the separately
supplied `markedCellContract` on a concrete countertrace. Its shared
`stay` report also supports a P0-shaped no-control-only-decision result.
It additionally proves that full configuration is adequate for the
marked-cell contract and that the control-only report is not. None of
this chooses the intended contract or proves a claim about all
transition systems.

The files prove finite information statements, finite-rule syntax, and
Bool/Unit models. The direct machine uses an unbounded mathematical tape,
but its evaluator is fuel-bounded and it has no byte encoding or
universality theorem. The files do not formalize Rice's theorem, Goedel's
theorem, an LLM, a physical replay environment, a trusted compiler, or
final authority.
The replay model does not establish cryptographic collision resistance,
verifier soundness, custody, physical independence, or a production
authorization protocol.

The adjacent code/replay_packet directory turns this finite carrier into
a byte-bound executable packet. It replays the finite evaluator and the
target-local two-source Lean closure, but the PowerShell-to-Lean
correspondence remains an explicit open import. A passing packet has
terminal open and AuthorityEffect None.

The `#print axioms` output must be inspected on every claimed replay.
PO-000 remains the formal anchor for report factorization. The formal
set contains a statement mirror, an AIT-PD0 finite countermodel, a
logical-versus-physical externality model, an operational-control finite
model, a transition-invariant finite model, a direct finite-rule
operational seed, a finite token-code syntax lift, a structural
replay-packet model, a class-relative no-decider transport, a conditional
terminalization consequence, and the
current J011 candidate quotient bridge. None proves the later Rice or
Goedel lifts.
