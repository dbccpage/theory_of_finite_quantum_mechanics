> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\proof_program.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](RECOVERY_NOTES.md).

---

# Sequential proof program

**Status:** active research program.

**AuthorityEffect:** None.

The goals are deliberately linear. A later goal cannot be closed by a
plausible essay, a green unrelated build, or a copied result. It needs
the listed predecessor artifacts and its own replay evidence. The
proposed future sealed runs are detailed in `seal_derivation_series.md`.

## AIT-PD0: Bind the Primitive Difference starting interface

**Depends on:** none.

**Status:** finite non-uniqueness model closed; J011 quotient/P0 bridge
now closed; full semantic and replay interface open.

Start from the J011-style Primitive Difference trunk, not from an
already interpreted LLM or a Turing machine. Define the minimal input:
a carrier, two unequal marks, a zero relation, the derived quotient, and
the distinction between derived quotient data and supplied reports.

**Proof needed:** Construct two model extensions with the same
Primitive Difference interface but different validity predicates or
terminal policies. This will prove that neither a contract predicate nor
an authorization act is selected by raw difference alone.

**Current evidence:**

- `formal/primitive_difference_authorization_models.lean` supplies two
  same-primitive extensions with different validity and terminal-policy
  values;
- its exact ceiling is a minimal Bool analogue, not full J011.

**Remaining exit evidence:** extend the bridge beyond the quotient to
the replay and terminal-policy carriers, add explicit positive and
negative models, and name every introduced structure. The result must
not claim that a raw mark derives computation, authorization, or physics.

## AIT-PD1: Specialize P0 to the J011 quotient

**Depends on:** AIT-PD0.

**Status:** closed rooted candidate; `lake build
AuthorizationIncompletenessTheory` succeeded on 2026-08-20.

Import the current J011 candidate's `PrimitiveDifference P`, `pdSetoid P`, and
`pdProj P`. The bridge must keep the following separation explicit:

```text
J011 supplies P, ZeroRel P, and the quotient report pdProj P.
The authorization program supplies valid : α -> Bool.
```

**Proof closed:** the bridge proves that a supplied validity predicate
splitting a `ZeroRel P` class cannot factor through `pdProj P`; it also
constructs a quotient decision under an explicitly supplied ZeroRel
constancy hypothesis.

**Axiom ceiling:** the negative quotient theorem depends on `propext`
and `Quot.sound` through J011's quotient equality theorem. The positive
quotient-lift theorem prints no axioms.

**Remaining exit evidence:** direct P0 module binding or a stable common
interface, a replay-packet carrier, and a terminal-policy carrier. The
current result is a statement-level P0 specialization, not an edit to
or import of P0.

## AIT-P0: Fix the Projection Obstruction anchor

**Depends on:** AIT-PD1.

**Status:** established for the report/validity factorization theorem in
PO-000; successor bindings open.

Use the unchanged PO-000 factorization theorem as the gate for every
subsequent lift. Do not assume that a proposal, evaluation, replay
status, or authorization can inhabit the report carrier merely because
it is named there.

**Proof needed:** for each proposed map, prove fiber constancy or show a
split-fiber countermodel and record the added report/refinement needed.

**Exit evidence:** a per-lift descent ledger whose claim IDs point to P0
or an independently replayed successor theorem. No P0 edit is allowed.

## AIT-G0: Freeze the contract vocabulary

**Depends on:** AIT-P0.

**Status:** draft vocabulary complete; theorem binding open.

Define, without metaphors:

- proposal source;
- proposal bytes and semantic interpretation;
- source-controlled report;
- local validity predicate;
- replay checker and receipt;
- terminal policy;
- soundness, completeness, local certainty, and global semantic
  certainty.

**Exit evidence:** Paper §2 and §5 plus ledger AIT-0 / AIT-3 have no
undefined conversion from a test result to semantic truth.

## AIT-G1: Prove the finite report-factorization theorem

**Depends on:** AIT-G0.

**Status:** closed finite seed; direct Lean replay on 2026-08-20 printed
no axioms for the four declarations in the file.

Prove that a validity predicate that splits a report fiber cannot factor
through the report. The proof must be polymorphic in proposal and report
types and must not assume an LLM or finite enumeration.

**Exit evidence:**

- `formal/authorization_incompleteness_core.lean`;
- theorem `split_fiber_blocks_total_authorization`;
- direct Lean replay with axiom disclosure;
- a negative and a positive finite model.

## AIT-G2: Prove the self-attestation instance

**Depends on:** AIT-G1.

**Status:** closed finite seed; direct Lean replay on 2026-08-20 printed
no axioms for the four declarations in the file.

Instantiate the theorem with a receipt that discards the contract bit.
Also exhibit a complete report that retains it. This prevents the later
paper from confusing “self-generated” with “necessarily inadequate.”

**Exit evidence:**

- `self_receipt_blocks_authorization`;
- `complete_receipt_decides_toy_contract`;
- exact statement-to-prose check in the claim ledger.

## AIT-E0: Separate logical from physical externality

**Depends on:** AIT-G1.

**Status:** closed finite model; `lake build
AuthorizationIncompletenessTheory` succeeded on 2026-08-20.

The word "external" is split into two non-equivalent claims.

```text
physical externality: source and evaluator have distinct site labels;
logical externality: the report, contract, checker, and policy are not
silently selected by the submitted proposal.
```

**Proof closed:** a complete Boolean report can be decided at the same
finite site label; a collapsed Boolean report cannot be decided at a
different site label. Thus physical separation is neither necessary nor
sufficient in this toy model. Report adequacy is the necessary theorem
condition for a total report-only decision.

**Exit evidence:**

- `formal/logical_externality_models.lean`;
- `can_authorize_requires_adequacy`;
- `physical_separation_neither_needed_nor_sufficient_for_toy_authorization`;
- explicit nonclaim that `Site` proves security, custody, or semantic
  truth.

## AIT-TC0: Separate tape control from contract and terminal policy

**Depends on:** AIT-PD0.

**Status:** closed finite model; direct Lean replay on 2026-08-20 printed
no axioms for the six printed declarations in the file.

The tiny operational model has a declared blank cell, a marked cell, and
declared `advance`, `stay`, and `halt` control outcomes. It also gives
`unread` its own observation-report type rather than treating it as a
tape symbol. It proves four strictly finite facts: an `unread` report can
hide a contract-relevant cell, the same read token admits distinct
supplied semantic adapters, a control-only `halt` report can identify two
presentations for which a supplied content contract differs, and the same
syntactic halt can feed opposite terminal policies.

This is not a new definition of a general Turing machine and does not
settle any question about P versus NP. It is the first controlled
negative example for the interpretation "halt equals authorization."

**Exit evidence:**

- `formal/tape_control_authorization_models.lean`;
- `same_read_token_allows_distinct_semantic_adapters`;
- `unread_report_blocks_content_decider`;
- `same_halt_control_blocks_control_only_decider`;
- `syntactic_halt_does_not_select_terminal_policy`;
- `controlled_turing_derivation_series.md` for the next lifts.

## AIT-TC1: Freeze the controlled Turing derivation protocol

**Depends on:** AIT-TC0 and AIT-G2.

**Status:** design.

Before asking an agent to derive a broader computation theory, freeze a
single-prompt, literature-blind experiment in a new repository. The
sealed artifact must include the prompt, model/tool configuration,
minimal interface, command environment, claim ledger, positive witness,
negative control, tests, and axiom report. Only after sealing may an
external source audit compare it with known literature.

The blind run is evidence about provenance and unpriced imported
structure. It is not evidence of mathematical novelty, independence from
training, or correctness beyond its replayed theorem. The full protocol
is in `controlled_turing_derivation_series.md`.

## AIT-TC2: Prove one controlled transition invariant and countertrace

**Depends on:** AIT-TC0.

**Status:** closed finite model; direct Lean replay on 2026-08-20 printed
no axioms for its six listed declarations.

The finite carrier has four explicitly named configurations. Its declared
table realizes `advance`, `stay`, and `halt`, preserves the supplied
`cleanTerminalContract`, and violates the separately supplied
`markedCellContract` on the named `runningMarked` countertrace. Two
terminal configurations share a `stay` control report while the latter
contract distinguishes them.

This is the desired SEAL-TC-02 shape: transition preservation is a
theorem about a named table and named contract, while non-preservation
is a named countertrace. It is neither a universal theory of transition
systems nor a general Turing-machine result.

**Exit evidence:**

- `formal/tape_transition_invariant_models.lean`;
- `transition_exposes_advance_stay_and_halt`;
- `transition_preserves_clean_terminal_contract`;
- `marked_contract_countertrace`;
- `transition_does_not_preserve_marked_cell_contract`;
- `shared_stay_control_blocks_control_only_contract_decider`.

## AIT-G3a: Finite replay-packet binding model

**Depends on:** AIT-G2 and AIT-E0.

**Status:** closed finite model; it is not a production packet.

The rooted Lean model supplies a trust root outside the source submission,
structurally binds a receipt to the exact submission, recomputes the
verification outcome on replay, and keeps terminal policy separate from
verification. It demonstrates four attacks in its finite carrier:

- an invalid payload paired with a source-controlled `selfPass` flag is
  contract-rejected;
- checker, schema-version, and contract-version substitutions are
  binding-rejected; and
- a payload substituted after receipt issuance is binding-rejected.

Its equality check is structural equality, not a hash. It makes no claim
about collision resistance, verifier soundness, custody, physical
independence, or deployment security.

**Exit evidence:**

- `formal/replay_packet_binding_models.lean`;
- `self_pass_cannot_authorize_invalid_content`;
- `checker_substitution_is_binding_rejected`;
- `replayed_status_requires_bound_submission`;
- `terminal_policy_is_not_selected_by_verification`.

## AIT-G3: Bind a real replay packet

**Depends on:** AIT-G3a.

**Status:** closed bounded replay packet on 2026-08-20.

The concrete packet at
`code/replay_packet/packet_manifest.json` binds immutable
SHA-256 digests for proposal, contract, terminal policy, evaluator,
entrypoint, Lean model, its direct formal dependency, and Lean toolchain.
It names PowerShell JSON parsing, the Lean toolchain, the replay command,
and its trusted-computing-base assumptions. The evaluator ignores the
source-provided pass Boolean. Its twenty-one mutation cases reject altered
bytes, path escape, every bound artifact role, schema and parser
substitution, declared-outcome substitution, terminal-policy
substitution, and command substitution. The integration test compiles the
target-local two-source Lean closure after packet verification succeeds.

The result is bounded by its stated trust root. The manifest is an input
that must be fixed outside proposal-controlled bytes; it does not
authenticate itself. SHA-256 collision resistance, evaluator-to-Lean
correspondence, runtime integrity, and custody remain explicit
assumptions rather than consequences of a passing replay.

**Exit evidence:** `code/replay_packet/`; its unit and integration
tests; and the packet README. The bounded packet is not a production
security or independent-custody protocol.

## AIT-G4: Formalize report adequacy for an executable contract

**Depends on:** AIT-G3.

**Status:** closed finite executable adequacy model on 2026-08-20.

For the finite marked-cell contract,
`AdequateFor fullConfigurationReport markedCellContract` is
proved in Lean, while
`control_report_not_adequate_for_marked_cell_contract`
exhibits the shared stay-report fiber that splits the contract. The
same model supplies a scoped full-configuration decision and a named
countertrace. The byte-bound evaluator recomputes those facts and emits
`open_due_to_inadequate_report` for the control-only route.
Its terminal policy remains `open`; it does not convert a finite
local check into authority.

This closes one finite contract/report pair only. The contract semantics,
the PowerShell evaluator's correspondence to Lean, and every wider
semantic interpretation remain explicit inputs or open obligations.

**Exit evidence:** `formal/tape_transition_invariant_models.lean`,
the bounded packet, its positive replay, and its negative mutation
corpus.

## AIT-G5a: Transport a class-relative no-decider boundary

**Depends on:** no earlier AIT claim.

**Status:** closed abstract transport; it is not a Rice theorem.

The rooted Lean file defines a decision class explicitly rather than
using every Boolean-valued function as if it were computable. It proves:

```text
source no total allowed decider
  + validity-preserving reduction into proposals
  + closure of allowed proposal authorizers under reduction
  -> no total allowed proposal authorizer.
```

The theorem has no axiom dependencies, but its three nontrivial inputs
remain inputs. In particular, no source undecidability theorem, program
syntax, universal evaluator, or computable-function class has yet been
instantiated.

**Exit evidence:**

- `formal/global_computability_lift_models.lean`;
- `no_source_decider_blocks_total_authorizer`;
- explicit statement that the decision classes, reduction, and source
  no-decider premise remain to be realized by AIT-G5.

## AIT-G5c: Derive the terminalization consequence

**Depends on:** AIT-G5a.

**Status:** closed abstract terminalization consequence; it is not a
Rice theorem.

The rooted Lean file shows that an allowed `authorized` bit becomes a
Boolean decider when it is acceptance-sound and acceptance-complete. It
then combines that fact with the supplied class-relative no-decider
premise. Separately, rejection soundness plus the absence of an
`unresolved` result entails acceptance completeness. Therefore, under
the named no-decider and allowed-membership premises, a terminalizer
cannot jointly be acceptance-sound, rejection-sound, and closed.

The same module proves a finite Boolean fixture that is closed and
two-sided sound. This fences the result: an unresolved result is not
universally required; it is the remaining sound route only under an
actual no-decider boundary. Four listed bridge theorems print `propext`,
and the two-sided-closure theorem prints no axioms.

**Nonclaim:** this does not instantiate a program carrier, prove a
source undecidability theorem or Rice's theorem, model an LLM, or infer
a physical/custodial externality boundary.

**Exit evidence:**

- `formal/terminal_authorization_boundary_models.lean`;
- `acceptance_bit_decides_of_sound_complete`;
- `no_total_decider_blocks_closed_two_sided_terminalization`;
- `finite_closed_terminalizer_remains_possible`; and
- the named Lake build with its printed axiom report.

## AIT-DTM0: Direct finite-rule operational seed

**Depends on:** AIT-TC2.

**Status:** closed finite-rule operational seed on 2026-08-20.

The rooted Lean module defines a finite rule-list machine with an
unbounded total tape, left-biased lookup, a fuel-bounded evaluator, a
designated halt state, and distinct halted, stuck, and fuel-exhausted
results. It proves the exact syntactic terminal condition and a
one-transition write-and-halt fixture. It also proves that the halt
result does not choose a supplied terminal policy.

The source has no sorry or admit marker. Its blank/absence and
write/reaches-halt fixture declarations print no axioms; the generic
terminal and policy declarations plus the closed stuck/fuel fixtures
print propext. This is recorded rather than treated as an axiom-free or
universal result.

**Nonclaim:** the module has no byte parser, universal machine,
Turing-completeness theorem, extensional property, reduction, or
halting-problem result.

**Exit evidence:** formal/direct_turing_machine_models.lean,
computability_carrier_candidates.json, its mutation test, and the
named Lake build.

## AIT-DTM1: Finite token-code grammar for the direct machine

**Depends on:** AIT-DTM0.

**Status:** closed finite token-code syntax lift; `lake build
AuthorizationIncompletenessTheory` succeeded on 2026-08-21.

The finite DTM0 rule-list carrier now has a declared `List Nat` grammar:
one halt-state token followed by complete five-token rule frames for the
state, scanned symbol, next state, written symbol, and movement. The
decoder consumes the whole list and rejects an empty header, a truncated
frame, an invalid symbol tag, or an invalid movement tag.

**Proof closed:** `decodeMachine_encodeMachine` proves that decoding the
emitted finite token code recovers the same DTM0 `Machine`. The tag
round-trip theorems print no axioms; the rule-list/machine round trips and
the four malformed-code fixtures print `propext`.

**Nonclaim:** the code is a finite natural-number token grammar, not a
byte format, source-file parser, configuration/input encoding,
parser-to-execution agreement theorem, universal machine, or reduction.

**Next exit evidence:** a separately typed configuration/input grammar
and a bounded trace-agreement theorem. Those remain needed before the
syntax-and-encoding admission field can close.

## AIT-G5b: Admit a computability carrier

**Depends on:** AIT-G4, AIT-TC1, AIT-TC2, AIT-DTM0, and AIT-DTM1.

**Status:** open admission gate.

Before invoking Rice's theorem, freeze one actual proposal language and
semantic interface. An arbitrary-program claim needs named syntax and
encodings, execution semantics, a universality witness, an extensional
property, nontrivial witnesses, an effective reduction, the
report/authorization split, and replay closure. A finite transition
table, a research draft, or a blind derivation run is a candidate source
for this work; none is an arbitrary-program class merely by being
suggestive.

The required record is maintained in computability_lift_admission.md and
computability_carrier_candidates.json. It retains the direct finite-rule
seed and its finite token-code successor, PO-022, PO-023, and the present
finite packet with their distinct proof ceilings. The candidate test rejects
a selected or admitted record while any field remains open or partial. No
candidate has been selected or promoted by this goal.

**Exit evidence:** a selected, machine-readable carrier record with all
eight admission fields, an explicit statement of the remaining unproved
imports, and a replayable validation of that record.

## AIT-G5: Establish the global computability lift

**Depends on:** AIT-G5a, AIT-G5b, AIT-G4, AIT-TC1, and AIT-TC2.

**Status:** open.

Choose an explicit Turing-complete proposal language and a nontrivial
extensional property. Prove that a total sound-and-complete authorizer
for that property would decide the corresponding semantic property.
Discharge the contradiction by a formalized Rice theorem or a fully
audited reduction to a mechanized computability library.

**Proof needed:** all of the following are mandatory:

- computable proposal encoding;
- exact extensional semantic predicate;
- positive and negative witnesses for nontriviality;
- totality, soundness, and completeness definitions;
- reduction and theorem citation / formal binding.

**Exit evidence:** a theorem whose quantifiers are visible in Lean and
whose paper sentence says “arbitrary programs in this language,” not
“all conceivable claims.”

**Complexity fence:** this lift neither defines nor resolves P versus NP.
SEAL-TC-05 studies a fixed verifier and supplied witness; any complexity
claim would additionally require a uniform encoding, resource model,
and reduction at its own claim ID.

## AIT-G6: Establish the self-soundness lift

**Depends on:** AIT-G5.

**Status:** open.

Model a recursively axiomatized authorization theory `T`, define the
relevant consistency or reflection sentence, and prove the exact
second-incompleteness boundary under named derivability assumptions.

**Proof needed:** an explicit formal-system encoding or a verified
bridge to an established proof assistant library. Do not use “Goedel” as
a slogan for a statement not covered by its hypotheses.

**Exit evidence:** theorem, hypothesis audit, and an example that shows
why an external meta-theory moves rather than removes the trust boundary.

## AIT-G7: Bind the LLM corollary

**Depends on:** AIT-G3, AIT-G5, and AIT-G5c.

**Status:** open.

Define an LLM deployment as a computable or seed-indexed proposal
source with explicit tool boundaries. Prove the dichotomy:

```text
LLM-only total semantic authorization
  -> violates AIT-G5,
or
authorization consumes an independent oracle/checker/policy input
  -> the LLM is not the sole authorization source.
```

**Exit evidence:** model definition, reduction, and a corpus of
counterexamples showing that local proof checking remains allowed.

AIT-G6 is a separate metatheoretic reinforcement. It is required before
the paper claims the stronger self-soundness conclusion, but it is not a
hidden premise of the Rice-based global semantic boundary in this
section.

## AIT-G8: Build and attack an authorization protocol

**Depends on:** AIT-G3 and AIT-G7.

**Status:** open.

Implement a small proposal -> checker -> receipt -> terminal-policy
pipeline. Run producer-controlled parser, checker, schema, version, and
hash substitution attacks. Include the policy path for `authorized`,
`rejected`, and `open` outcomes.

**Exit evidence:** all attacks are replayed and rejected or routed to
`open`; an independent reviewer can reproduce the receipt from frozen
inputs; the claim ledger assigns every final decision a scope.

## Stopping condition

The paper may state the global LLM conclusion as a proved in-tree result
only after AIT-PD0, AIT-PD1, AIT-P0, AIT-E0, AIT-TC0, AIT-TC1, AIT-TC2,
AIT-DTM0, AIT-DTM1, and AIT-G0 through AIT-G5, including AIT-G3a, AIT-G5a,
AIT-G5b, and AIT-G5c, plus AIT-G7,
have all closed under their stated evidence. AIT-G6 must also close
before the paper claims its separate self-soundness conclusion; it is
not smuggled in as a premise of the Rice-based LLM result. AIT-G8 is the
additional deployment-protocol branch. Until the relevant goals close,
the finite theorems are proved, the global theorem is a standard cited
result with a planned local formalization, and the LLM corollary remains
conditional on its explicit model.

**AuthorityEffect:** None.
