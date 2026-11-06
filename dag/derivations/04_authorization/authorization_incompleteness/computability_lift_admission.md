> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\computability_lift_admission.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](RECOVERY_NOTES.md).

---

# Computability-lift carrier admission

**Goal:** AIT-G5b.

**Status:** open admission gate.

**AuthorityEffect:** None.

## Purpose

Before invoking Rice's theorem, this program must freeze one actual
proposal language and its semantic interface. “Arbitrary program” is not
an input type. It is a claim about a named syntax, encoding, evaluator,
and extensional property.

This sheet is the admission gate between the finite transition/replay
models and the global computability lift. It prevents a future proof from
silently treating a research design, a finite trace language, or a
Boolean function space as though it were a Turing-complete proposal
class.

## Candidate sources and present ceilings

<!-- markdownlint-disable MD013 -->
| Candidate | Useful contribution | Present ceiling |
| --- | --- | --- |
| Direct finite-rule Turing-style seed (DTM0/DTM1) | Formal finite rule syntax, total tape, fuel-bounded evaluator, syntactic halt, and finite token-code parser round trip | No source-byte or input/configuration encoding, trace agreement, universal machine, extensional property, or reduction |
| PO-022 finite presentation calculus | Separates stage, receipt, terminal policy, and bounded Turing simulation | Research draft; its Lean file contains True scaffolds, not a bounded-adapter theorem |
| PO-023 stopping quotient | Identifies the loss from mapping richer dispositions to a stop bit | Research draft; its Lean file contains True scaffolds, not a halting or undecidability theorem |
| Current AIT transition packet | A replayable finite four-state checker with an adequacy boundary | Finite carrier only; it is not a universal machine or program encoding |
<!-- markdownlint-enable MD013 -->

PO-022 and PO-023 are not refused as research. They are retained as
design sources with their current proof ceilings. No result in them is
used as a premise of AIT-G5 until the listed admission requirements
close.

The machine-readable inventory is
computability_carrier_candidates.json. Its validation test rejects an
admitted or selected candidate while the inventory remains open. The
direct seed is partial on syntax, execution semantics, adequacy/policy
separation, and target-local Lean replay only. DTM1 closes a finite
rule-list token-code round trip, but source bytes, input/configuration
encoding, and trace agreement remain open; all global fields remain open.

## Required admission record

One candidate is admitted only with all of the following frozen in a
machine-readable record.

1. **Syntax and encoding.** A finite grammar, program encoding, input
   encoding, and equality relation on programs.
2. **Execution semantics.** A partial or step-indexed evaluator with
   explicit behavior on malformed programs, time/resource bounds, and
   terminal states.
3. **Universality witness.** A theorem or audited imported theorem that
   the carrier realizes a Turing-complete class. A finite collection of
   examples is not enough.
4. **Extensionality boundary.** A semantic property stated over program
   behavior, not merely program text. The exact observational
   equivalence must be named.
5. **Nontriviality witnesses.** One encoded program satisfying the
   property and one encoded program failing it.
6. **Effective reduction.** The map from the source undecidable problem
   into proposal programs, with its computability and preservation
   theorem stated.
7. **Adequacy and authorization split.** The proof must distinguish the
   semantic predicate, reports/checker outputs, and terminal policy.
   Passing a local checker is not the global property.
8. **Replay closure.** Program bytes, evaluator source, toolchain,
   command, and theorem binding are replayable under a named trust
   boundary.

## Admission tests

The gate fails if any of the following occurs.

- A claim about all Boolean-valued functions is substituted for a
  declared computable decision class.
- A finite-horizon simulation is treated as a universal simulation.
- A property of source syntax is substituted for an extensional
  semantic property.
- A halt bit or terminal policy is substituted for the semantic
  predicate.
- A green Lean declaration with statement True is cited as a theorem.
- The reduction depends on a parser, evaluator, or encoding not bound
  into the replay packet.

## Recommended sequence

The first implementation need not formalize Rice's theorem from scratch.
It should first complete a bounded adapter for the chosen carrier and
prove exact trace agreement. Only then should it price the additional
universal-simulation and self-encoding imports needed for the
undecidability transport.

The direct finite-rule route is the cleanest starting point for a global
theorem carrier. Its DTM1 token-code lift now supplies a declared finite
rule grammar and parser round trip. Its next work is a source-byte and
input/configuration encoding plus an exact trace-agreement theorem before
any universality claim. PO-022 can become an alternate carrier only after
its bounded adapter, universal-simulation conditions, and proof obligations
are separately discharged. PO-023 remains a useful P0-shaped terminal
compression countermodel; it is not a substitute for a Rice reduction.

AIT-G5c records the conditional terminal consequence once a real
class-relative no-decider premise has been supplied. It advances none of
the eight admission fields: it neither selects a carrier nor proves its
undecidability, universality, extensionality, or replay closure.

## Exit evidence

- a selected carrier record satisfying all eight admission fields;
- a validated computability_carrier_candidates.json record;
- source and target program fixtures;
- a bounded interpreter or imported evaluator with replay command;
- a theorem-level encoding and reduction plan; and
- an explicit statement of what remains unproved.

**AuthorityEffect:** None.
