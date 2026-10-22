# AUTHF-TERMINAL-CLOSED-TWO-SIDED

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If a terminalizer never rejects a valid proposal and never returns unresolved, every valid proposal is authorized; with an allowed acceptance bit and no allowed total decider, acceptance-soundness, rejection-soundness and closure cannot all hold.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The result leaves three options (an unsound acceptance, an unsound rejection, or an unresolved case) and does not say any of them must occur for a particular predicate.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record closed_two_sided_terminalization_is_acceptance_complete claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/Terminal.lean`

- file: [lean4/AuthIncompleteness/Terminal.lean](../../../lean4/AuthIncompleteness/Terminal.lean)
- sha256 (`bytes`): `f1e83667ed1ece4713d348bcdf1e3b77f3b9a092b0ac766cbe9204d3cf9e2b99`
- cited in: node.lean, node.source, record TFQ-1350
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/Terminal.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.closed_two_sided_terminalization_is_acceptance_complete` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.closed_two_sided_terminalization_is_acceptance_complete` |
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_closed_two_sided_terminalization` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_closed_two_sided_terminalization` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1350_authf_terminal_closed_two_sided.md`

- file: [dag/derivations/29_computation/tfq_1350_authf_terminal_closed_two_sided.md](../../../dag/derivations/29_computation/tfq_1350_authf_terminal_closed_two_sided.md)
- sha256 (`lf-normalised`): `7b36e67cca0ec9cb1d08bba6b477619edbeb080d1dad0ca26f2ecaa6f82be219`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1350
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-TERMINAL-CLOSED-TWO-SIDED` `DERIVED_LEAN`: [AUTHF-TERMINAL-ACCEPT-BIT](AUTHF-TERMINAL-ACCEPT-BIT.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-AUTHF-TERMINAL-BOOL-FIXTURE` `DERIVED_LEAN`: [AUTHF-TERMINAL-BOOL-FIXTURE](AUTHF-TERMINAL-BOOL-FIXTURE.md) (PROVED_LEAN)
