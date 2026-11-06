> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\controlled_turing_derivation_series.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](RECOVERY_NOTES.md).

---

# Controlled Turing Derivation Series

**Status:** research design. No mathematical conclusion is sealed by
this document.

**AuthorityEffect:** None.

## Purpose

This is the controlled branch proposed for the question: what does a
tape, read, transition, movement, and halt actually establish before a
semantic contract and an authorization policy are introduced?

It does not say that Turing's account of effective procedure is wrong.
It says that a model of syntactic procedure does not, merely by being a
model of procedure, select the intended semantics of a proposal or the
policy effect of a terminal state. The series should make that difference
visible one lift at a time.

The working interpretation is deliberately split: a tape configuration
may serve as a proposal/presentation; a head, read rule, and transition
table may serve as a **syntactic** evaluator of the declared transition
rule; and advance, stay, or halt may serve as a control report. None is a
semantic evaluator or authorizer until a semantic contract and terminal
policy are separately supplied and bound.

The branch feeds `SEAL-AIT-06`; it does not replace the finite
report-factorization theorem or Paper 0. A halt is a terminal condition
of a declared transition system. It becomes an authorization only after
an explicit policy maps that condition, under an explicit contract, to a
licensed effect.

## Non-negotiable boundary

In a standard Turing-machine presentation, a blank is a declared tape
alphabet symbol. Meta-level absence is not automatically a tape symbol.
If an experiment needs an "absent" case, it must model that state
explicitly, for example with `Option Symbol` or a tagged alphabet. This
prevents the primitive distinction "present / absent" from entering the
formal object as an untyped metaphor.

Likewise, a standard machine transition can prescribe an updated state,
written symbol, and direction. It does not, by itself, prove that the
transition has the intended worldly, mathematical, or policy meaning.

## Controlled proposal-generation experiments

An isolated prompt can be useful for discovery, but it is not a derivation
and not evidence that a result is novel. Treat every generated artifact as a
proposal until it passes the same formal and replay checks as any other
proposal.

For each experiment, freeze the exact prompt, model and tool configuration,
initial repository revision, declared available context (including an explicit
"no external literature supplied" condition when applicable), output bytes,
and evaluation results. Change one experimental variable at a time. The
independent evaluators remain the parser, Lean checker, replay packet, and
human claim audit; the model's self-description is never its own
authorization.

The useful outcome is a controlled comparison of proposed structures or
invariants. A successful run does not establish priority, semantic truth,
independent custody, or a global authorization theorem.

## Controlled vocabulary

<!-- markdownlint-disable MD013 -->
| Operational object | Legitimate role in this branch | Not licensed by itself |
| --- | --- | --- |
| Tape/configuration | A finite presentation or proposal state | The semantic content of the state |
| Blank or marked cell | A declared syntactic distinction | Meta-level absence, unless modeled explicitly |
| Head/read rule | A syntactic selection of a declared cell | Evaluation of the cell's intended meaning |
| Transition table | A declared syntactic update rule | Correctness of the rule's external interpretation |
| Advance/stay | A declared control outcome | Evidence that a contract was met |
| Halt | A declared terminal control outcome | Authorization, acceptance, publication, or truth |
| Output decoder | A separately declared semantic adapter | A consequence of tape syntax alone |
| Terminal policy | A separately declared licensing rule | A consequence of halting alone |
<!-- markdownlint-enable MD013 -->

The finite Lean file
`formal/tape_control_authorization_models.lean` establishes the smallest
instance: two presentations can share the same `halt` report while a
supplied content contract distinguishes them, and two terminal policies
can map that same `halt` outcome differently. It now also distinguishes
`unread` from the declared tape alphabet and exhibits two supplied
semantic adapters that disagree on the same read token. These are finite
countermodels of unforced interpretation, not a formalization of the
full standard Turing-machine model.

## The derivation ladder

Each item is a separate proposed derivation or controlled experiment.
The word "derive" below means prove the stated invariant from the
frozen inputs; it does not mean an LLM has narrated a plausible route.

### SEAL-TC-00: Inscription and Primitive Difference

**Frozen input:** a finite alphabet with at least two declared marks,
one of which may be named `blank`.

**Lift:** form finite configurations containing a scanned cell and a
head location.

**Invariant:** a difference of cell inscriptions gives a syntactic
distinction only. It does not select a semantic predicate.

**Required negative control:** two semantic contracts over the same
configuration interface that disagree on one marked configuration.

**Typing fence:** `blank` is an alphabet member. “No symbol was
observed” is an observation outcome such as `ReadReport.unread`, while a
genuine absent cell must be a separately declared carrier extension.
Neither is silently identified with the other merely because each can
be encoded by a mark.

**Open import after the lift:** an observer/read operation.

### SEAL-TC-01: Read is syntactic selection

**Frozen input:** SEAL-TC-00 plus a declared head and read function.

**Lift:** expose the scanned cell as a report.

**Invariant:** a read returns a declared symbol from a declared
configuration. It does not authorize an interpretation of that symbol.

**Required negative control:** two semantic adapters that accept the
same read trace but assign different contract values to a configuration.

**Current finite seed:** `read_is_syntactic_selection` proves only that
the read map returns the scanned declared cell;
`same_read_token_allows_distinct_semantic_adapters` exhibits two supplied
interpretations of that same token; and
`unread_report_blocks_content_decider` gives the P0 split-fiber form when
the observation policy withholds the cell. None says that a standard
Turing head is incapable of participating in a semantic system.

**P0 question:** does the proposed contract descend through the read
report? If it does not, retain the missing configuration distinction or
return `open`.

### SEAL-TC-02: Transition and motion

**Frozen input:** SEAL-TC-01 plus a finite transition table.

**Lift:** compute a next configuration and explicitly distinguish
advance, stay, and terminal outcomes.

**Invariant:** the table defines a syntactic evolution relative to its
encoding. It does not establish that the evolution preserves an
independently stated semantic contract.

**Required positive witness:** a small invariant that does descend and
is preserved by the declared transition table.

**Required negative control:** a contract that is not preserved, with a
concrete countertrace.

**Current finite seed:**
`formal/tape_transition_invariant_models.lean` has an exhaustive
four-configuration carrier. Its declared table realizes `advance`,
`stay`, and `halt`; `transition_preserves_clean_terminal_contract`
proves preservation of one supplied Boolean contract; and
`marked_contract_countertrace` together with
`transition_does_not_preserve_marked_cell_contract` proves failure for a
different supplied Boolean contract. The theorem
`shared_stay_control_blocks_control_only_contract_decider` additionally
replays the P0 pattern: two configurations can share a `stay` report
while the contract distinguishes them.

This is a closed finite witness of the ladder's form, not a result about
all Turing-machine transition tables or the intended meaning of either
contract. A future sealed experiment must replace this carrier with its
own frozen interface, witnesses, countertrace, and source audit.

The same finite carrier now makes the positive adequacy condition
explicit. A report that retains the whole configuration is adequate for
the marked-cell contract; the transition-control report is not, because
the two terminal configurations share stay while the contract separates
them. This is the exact finite P0 question: retain the distinction or
route the report-only result to open.

### SEAL-TC-02b: Direct finite-rule operational semantics

**Frozen input:** a finite rule list, a designated halt state, a total
tape carrier, and a declared bounded evaluator.

**Lift:** execute a direct Turing-style rule table and distinguish a
declared halt, a missing rule, and fuel exhaustion.

**Invariant:** a declared halt is exactly membership in the designated
control state. Fuel exhaustion is a result of the bounded evaluator, not
a proof of non-halting. Neither result supplies an intended semantic
property or a terminal policy.

**Formal seed:** AIT-DTM0 in
formal/direct_turing_machine_models.lean. It has finite structured Lean
syntax, closed fixtures for halted/stuck/fuel-exhausted outcomes, and no
universal-machine or byte-parser theorem.

**Required negative control:** assign two supplied terminal policies to
the same halted result and show that their effects differ.

### SEAL-TC-02c: Finite token grammar and parser

**Frozen input:** SEAL-TC-02b's finite rule-list `Machine` carrier.

**Lift:** encode the declared halt state and each complete rule as a
finite natural-number token list, then parse the whole list back into the
same carrier.

**Invariant:** decoding the finite token code emitted for a DTM0 machine
recovers that machine. A parser is not permitted to ignore an empty
header, a truncated suffix, or an invalid alphabet/movement tag.

**Required positive witness:**
`decodeMachine_encodeMachine` in
`formal/direct_turing_machine_token_code_models.lean`.

**Required negative controls:** the empty code, a partial rule frame, an
invalid symbol tag, and an invalid movement tag are rejected by the declared
decoder.

**Current finite seed:** symbol/movement tag round trips print no axioms;
the rule-list/machine round trips and malformed-code fixtures print
`propext`. The code is `List Nat`, not bytes or source text.

**Open import after the lift:** a configuration/input grammar and a proof
that parsed source, execution, trace, and report agree. The token grammar
does not select a semantic contract, establish P0 descent, bind replay
custody, or give a universal-machine result.

### SEAL-TC-03: Halt is terminality, not authorization

**Frozen input:** SEAL-TC-02 plus a declared halting condition.

**Lift:** label terminal configurations.

**Invariant:** `halt` says that the declared transition relation has no
next step of the specified kind. It says neither that the output meets a
semantic specification nor what a recipient is licensed to do.

**Required negative controls:**

- identical terminal control reports with a content contract that
  differs on a forgotten tape distinction;
- accepting and rejecting policies over the same terminal report.

**Formal seed:** `AIT-TC0` and
`same_halt_control_blocks_control_only_decider`.

### SEAL-TC-04: Trace, receipt, and replay

**Frozen input:** SEAL-TC-03 plus a trace format, parser, checker,
environment record, and hash rules.

**Lift:** make the syntactic run replayable as an artifact.

**Invariant:** replay establishes only the result of the fixed
interpreter/checker on the frozen bytes in the declared environment.

**Required attacks:** substitute the transition table, parser, decoder,
checker, schema version, environment, and policy binding. The replay
must reject the substitution or state exactly what changed.

**Current bounded packet:** the AIT-G3 packet binds a finite transition
proposal, its separately supplied contract and terminal policy, the
PowerShell evaluator and entrypoint, the Lean model and its direct formal
dependency, and the Lean toolchain. Its mutation corpus rejects byte,
path, schema, parser-profile, command-profile, evaluator, and policy
substitutions. It recomputes the contract and returns an open route for
the inadequate control-only report.

This is only a finite replay packet. It does not provide a generic trace
decoder, independent environment custody, collision-resistance proof,
or a proof that the PowerShell evaluator has the same meaning as the
Lean model. Those remain explicit imports for a later sealed
experiment.

**Remaining import after the lift:** an independently controlled
semantic contract and a policy owner.

### SEAL-TC-05: Certificate verification and the P/NP boundary

**Frozen input:** a fixed encoding of instances, witnesses, and a
polynomial-time verifier for one named decision problem.

**Lift:** check a concrete witness under the declared verifier.

**Invariant:** a passing witness establishes the verifier's declared
relation for that fixed instance and encoding. It is a constructive,
bounded authorization route.

**Nonclaim:** this experiment does not decide P versus NP, prove that a
verifier's intended natural-language specification is complete, or make
the verifier self-authorizing. It tests exactly how much a fixed
certificate relation can license.

**Complexity fence:** the experiment concerns verification of a supplied
witness under one declared cost model. P versus NP additionally asks for
uniform polynomial-time decision or search across an encoded problem
family. No conclusion about that equality is licensed until the encoding,
machine model, reductions, and quantifiers are formalized separately.

**Required negative control:** retain a semantic property that the
certificate/report does not encode and show the P0 split-fiber residual.

### Admission gate before SEAL-TC-06

The arbitrary-program lift cannot begin from a suggestive tape trace,
finite transition table, or a function space that was never shown to be
computable. It first needs one frozen proposal carrier with named syntax,
input encoding, evaluator, observational equivalence, universality
witness, nontrivial property witnesses, reduction plan, and replay
boundary. The admission record is
[computability_lift_admission.md](computability_lift_admission.md).

A single-prompt, isolated, no-literature run is useful here as a
provenance and countermodel-discovery experiment. It may suggest a
candidate invariant or reveal an unpriced import. It does not establish
that the candidate is universal, novel, semantically adequate, or a
Rice-style reduction. Those claims require the frozen carrier record
and independently replayed proof evidence.

### SEAL-TC-06: Arbitrary-program semantic boundary

**Frozen input:** an admitted Turing-complete proposal language, its
extensional semantics, and explicit nontrivial positive and negative
witnesses.

**Lift:** attempt a total authorizer for that named semantic property.

**Invariant:** no total computable sound-and-complete decider exists for
the nontrivial extensional property over arbitrary proposals in the
chosen language, by a fully stated Rice reduction.

**Nonclaim:** the result does not rule out restricted languages,
bounded runs, proof checkers, semi-decision procedures, or `open`.

### SEAL-TC-07: Self-description and formal soundness

**Frozen input:** SEAL-TC-06 plus a recursively axiomatized formal
system representing the authorization procedure.

**Lift:** state the internal consistency/reflection claim precisely.

**Invariant:** the specified second-incompleteness hypotheses locate a
new metatheoretic trust boundary. They do not turn every local proof
check into an impossibility.

**Required evidence:** exact provability predicate, representability
conditions, theorem statement, and a named external meta-theory.

### SEAL-TC-08: LLM corollary

**Frozen input:** an LLM execution model with weights, prompt, sampling
state, tools, and finite output trace explicitly represented.

**Lift:** classify its final decision path.

**Invariant:** an LLM-only route is a computable proposal/decision path;
an independent checker, semantic oracle, or policy owner is a separate
authorization input. Neither fluent output nor a halt-like terminal
token erases that distinction.

**Required result:** a conditional reduction to SEAL-TC-06, plus a
separate constructive example of bounded external checking.

## Blind derivation protocol

The proposed isolated-repository experiments are useful if their goal is
provenance and countermodel discovery, not proof by isolation. Each run
must use a new repository and must never import the sealed derivation or
its files into CODA.

1. Freeze one task prompt, tool policy, model identity, deterministic
   settings when available, repository state, and command environment.
2. Give the run no literature, CODA source, or prior derivation text
   beyond the deliberately minimal formal interface for that experiment.
3. Require a claim ledger that labels every introduced notion as input,
   definition, proved theorem, example, or open assumption.
4. Require at least one positive witness and one countermodel or failed
   descent witness for every proposed lift.
5. Seal the bytes, commands, outputs, tests, and axiom report before any
   external literature comparison.
6. After sealing, perform source classification and compare the result
   with Turing, Rice, Goedel, and relevant literature. Record any
   rediscovery, hidden assumption, or mismatch without altering the
   sealed object.
7. In CODA, cite the sealed tag only for the replay receipt; do not use
   the blind run as proof of novelty, semantic correctness, or an
   impossibility theorem it did not formally establish.

Blindness can reveal which structure a generator introduces without a
given reference. It cannot establish that the result is original,
independent of all training influence, mathematically valid, or stronger
than the actual checked theorem. The post-seal audit is therefore part
of the method, not an optional afterthought.

The desired “single-prompt, no-literature” experiment is therefore a
provenance probe: it can reveal whether a proposed lift was smuggled in
by the prompt or appears as an unstated addition. It is never evidence
that the prompt has rediscovered a theorem, avoided all prior influence,
or supplied the external semantic authorization that the experiment is
meant to study.

## Controlled experiment matrix

<!-- markdownlint-disable MD013 -->
| Experiment | Hold fixed | Vary deliberately | Allowed conclusion |
| --- | --- | --- | --- |
| Inscription | Carrier and tape alphabet | Semantic contract | Syntax alone does not choose contract |
| Read | Configuration and read trace | Semantic adapter | Read output alone may be inadequate evidence |
| Motion | Transition encoding | Invariant/contract | A transition preserves only a proved invariant |
| Halt | Terminal state | Terminal policy | Halt alone is not authorization |
| Replay | Bytes and command | Parser/checker/environment binding | Byte binding is replayable; custody remains a declared import |
| Certificate | Instance and verifier | Witness and unencoded semantics | A verifier licenses only its declared relation |
| Global property | Proposal language | Semantic property | Rice boundary is about the named arbitrary-program class |
<!-- markdownlint-enable MD013 -->

## Exit condition for this branch

The branch is ready to support the main AIT paper only when each lift
has a frozen interface, explicit theorem statement, replay receipt,
positive witness, negative control, P0 descent audit, and nonclaim.
Until then, this is a disciplined research route, not a new theory of
computation and not a solution of P versus NP.

**AuthorityEffect:** None.
