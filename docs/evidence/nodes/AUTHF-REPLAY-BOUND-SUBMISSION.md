# AUTHF-REPLAY-BOUND-SUBMISSION

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the finite structural replay model, if replay of a receipt on an observed submission returns replayed with some outcome, then the observed submission equals the submission bound in the receipt.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Equality is structural equality of a finite record, not a digest; verifier soundness and custody are not modelled.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record replayed_status_requires_bound_submission claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/Replay.lean`

- file: [lean4/AuthIncompleteness/Replay.lean](../../../lean4/AuthIncompleteness/Replay.lean)
- sha256 (`bytes`): `5d1411fd9a1b692f18bbe037dc42532911d7468415ea5ae0bcd91d64f7463362`
- cited in: node.lean, node.source, record TFQ-1356
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/Replay.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.ReplayPacketBindingModels.issueReceipt` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.issueReceipt` |
| `AuthorizationIncompleteness.ReplayPacketBindingModels.replay` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.replay` |
| `AuthorizationIncompleteness.ReplayPacketBindingModels.replayed_status_requires_bound_submission` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.replayed_status_requires_bound_submission` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1356_authf_replay_bound_submission.md`

- file: [dag/derivations/29_computation/tfq_1356_authf_replay_bound_submission.md](../../../dag/derivations/29_computation/tfq_1356_authf_replay_bound_submission.md)
- sha256 (`lf-normalised`): `51aec62f42754c0b8e2dc916e0f8d4961fd6fc98d8a488532c76c4438bbf05fa`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1356
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md](../../../papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md)
- sha256 (`lf-normalised`): `50b2673ad6e6ce3e8f3cba55fbcc848fac64db21600db6e8d1a9e63e96b7f915`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-REPLAY-BOUND-SUBMISSION` `DERIVED_LEAN`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (1):

- `APP-R-AUTHF-REPLAY-SUBSTITUTIONS` `COMPUTED`: [AUTHF-REPLAY-SUBSTITUTIONS](AUTHF-REPLAY-SUBSTITUTIONS.md) (COMPUTATIONALLY_CHECKED)
