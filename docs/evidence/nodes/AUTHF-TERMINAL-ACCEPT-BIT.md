# AUTHF-TERMINAL-ACCEPT-BIT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a terminalizer into authorized, rejected, unresolved that is acceptance-sound and acceptance-complete for a validity predicate, the Boolean that is true exactly on authorized decides the predicate; if that Boolean lies in an allowed class with no total decider, the terminalizer cannot be both.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The no-total-decider premise and the membership of the acceptance bit in the allowed class are hypotheses; neither is discharged.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record acceptance_bit_decides_of_sound_complete claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/Terminal.lean`

- file: [lean4/AuthIncompleteness/Terminal.lean](../../../lean4/AuthIncompleteness/Terminal.lean)
- sha256 (`bytes`): `f1e83667ed1ece4713d348bcdf1e3b77f3b9a092b0ac766cbe9204d3cf9e2b99`
- cited in: node.lean, node.source, record TFQ-1349
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.Terminal`): recorded sha256 `f1e83667ed1ece4713d348bcdf1e3b77f3b9a092b0ac766cbe9204d3cf9e2b99` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/Terminal.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.acceptance_bit_decides_of_sound_complete` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.acceptance_bit_decides_of_sound_complete` |
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.acceptance_bit_true_iff` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.acceptance_bit_true_iff` |
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_sound_complete_authorization` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_sound_complete_authorization` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1349_authf_terminal_accept_bit.md`

- file: [dag/derivations/29_computation/tfq_1349_authf_terminal_accept_bit.md](../../../dag/derivations/29_computation/tfq_1349_authf_terminal_accept_bit.md)
- sha256 (`lf-normalised`): `e2578e2e894563a396d10a9cfb786cf5f99f9f013a12b22c9255df5a074c482a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1349
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-TERMINAL-ACCEPT-BIT` `DERIVED_LEAN`: [AUTHF-CLASS-RELATIVE-TRANSPORT](AUTHF-CLASS-RELATIVE-TRANSPORT.md) (PROVED_LEAN), [TFQ-0330](TFQ-0330.md) (OPEN)

Outgoing (1):

- `APP-R-AUTHF-TERMINAL-CLOSED-TWO-SIDED` `DERIVED_LEAN`: [AUTHF-TERMINAL-CLOSED-TWO-SIDED](AUTHF-TERMINAL-CLOSED-TWO-SIDED.md) (PROVED_LEAN)
