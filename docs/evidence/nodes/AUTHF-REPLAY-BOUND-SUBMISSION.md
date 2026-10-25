# AUTHF-REPLAY-BOUND-SUBMISSION

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the finite structural replay model, if replay of a receipt on an observed submission returns replayed with some outcome, then the observed submission equals the submission bound in the receipt.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
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
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.Replay`): recorded sha256 `5d1411fd9a1b692f18bbe037dc42532911d7468415ea5ae0bcd91d64f7463362` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/Replay.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.ReplayPacketBindingModels.issueReceipt` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.issueReceipt` |
| `AuthorizationIncompleteness.ReplayPacketBindingModels.replay` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.replay` |
| `AuthorizationIncompleteness.ReplayPacketBindingModels.replayed_status_requires_bound_submission` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.replayed_status_requires_bound_submission` |

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
