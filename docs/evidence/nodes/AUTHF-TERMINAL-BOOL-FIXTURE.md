# AUTHF-TERMINAL-BOOL-FIXTURE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On Bool with validity equal to the bit, the terminalizer sending true to authorized and false to rejected is acceptance-sound, acceptance-complete, rejection-sound and closed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A decidable one-bit predicate only; it shows closed terminalization is not forbidden without a no-decider premise.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record finite_closed_terminalizer_remains_possible claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/Terminal.lean`

- file: [lean4/AuthIncompleteness/Terminal.lean](../../../lean4/AuthIncompleteness/Terminal.lean)
- sha256 (`bytes`): `f1e83667ed1ece4713d348bcdf1e3b77f3b9a092b0ac766cbe9204d3cf9e2b99`
- cited in: node.lean, node.source, record TFQ-1351
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.Terminal`): recorded sha256 `f1e83667ed1ece4713d348bcdf1e3b77f3b9a092b0ac766cbe9204d3cf9e2b99` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/Terminal.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.boolTerminalize` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.boolTerminalize` |
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.boolValidity` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.boolValidity` |
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.finite_closed_terminalizer_remains_possible` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.finite_closed_terminalizer_remains_possible` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1351_authf_terminal_bool_fixture.md`

- file: [dag/derivations/29_computation/tfq_1351_authf_terminal_bool_fixture.md](../../../dag/derivations/29_computation/tfq_1351_authf_terminal_bool_fixture.md)
- sha256 (`lf-normalised`): `14b04ed29e274d181c5438e171f858015d39d84cd4f1a54bce8d0ab86c6a6502`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1351
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-TERMINAL-BOOL-FIXTURE` `DERIVED_LEAN`: [AUTHF-TERMINAL-CLOSED-TWO-SIDED](AUTHF-TERMINAL-CLOSED-TWO-SIDED.md) (PROVED_LEAN)

Outgoing (0):

