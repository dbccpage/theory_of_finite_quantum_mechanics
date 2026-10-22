# AUTHF-TAPE-CONTROL-REPORTS

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the tape-control model with cells blank and marked and outcomes advance, stay, halt, no function of the control outcome and no function of the always-unread report equals contentContract on every presentation, and the read token blank is given opposite verdicts by the two supplied semantic adapters.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The contract and adapters are supplied examples; the model is not the full Turing-machine model.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record same_halt_control_blocks_control_only_decider claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/TapeControl.lean`

- file: [lean4/AuthIncompleteness/TapeControl.lean](../../../lean4/AuthIncompleteness/TapeControl.lean)
- sha256 (`bytes`): `88462fe7ef09d03d0250de9aaf91c0f43a86a17166a07e0bf3639981f3a584a8`
- cited in: node.lean, node.source, record TFQ-1352
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/TapeControl.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.TapeControlModels.same_halt_control_blocks_control_only_decider` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.TapeControlModels.same_halt_control_blocks_control_only_decider` |
| `AuthorizationIncompleteness.TapeControlModels.same_read_token_allows_distinct_semantic_adapters` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.TapeControlModels.same_read_token_allows_distinct_semantic_adapters` |
| `AuthorizationIncompleteness.TapeControlModels.shared_halt_control_splits_content_contract` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.TapeControlModels.shared_halt_control_splits_content_contract` |
| `AuthorizationIncompleteness.TapeControlModels.unread_report_blocks_content_decider` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.TapeControlModels.unread_report_blocks_content_decider` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1352_authf_tape_control_reports.md`

- file: [dag/derivations/29_computation/tfq_1352_authf_tape_control_reports.md](../../../dag/derivations/29_computation/tfq_1352_authf_tape_control_reports.md)
- sha256 (`lf-normalised`): `b4abac63ecf6e940835ffc96ed612e03bcf45fc0413ecf008c5e3714079e712b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1352
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md](../../../papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md)
- sha256 (`lf-normalised`): `50b2673ad6e6ce3e8f3cba55fbcc848fac64db21600db6e8d1a9e63e96b7f915`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-TAPE-CONTROL-REPORTS` `DERIVED_LEAN`: [AUTHF-DTM0-RULE-MACHINE](AUTHF-DTM0-RULE-MACHINE.md) (DEFINITION)

Outgoing (0):

