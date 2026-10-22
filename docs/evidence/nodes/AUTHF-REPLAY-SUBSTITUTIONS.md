# AUTHF-REPLAY-SUBSTITUTIONS

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Under authorizeTrueRoot, verify returns contractRejected for the invalid submission that sets selfPass, returns bindingRejected for the checker, contract-version and schema-version substitutions, issues a receipt that replays the valid submission as verified, and rejects the invalid payload as a substitution.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Six rfl facts on five named submissions; the model does not prove that every substitution is caught.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record self_pass_cannot_authorize_invalid_content claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/Replay.lean`

- file: [lean4/AuthIncompleteness/Replay.lean](../../../lean4/AuthIncompleteness/Replay.lean)
- sha256 (`bytes`): `5d1411fd9a1b692f18bbe037dc42532911d7468415ea5ae0bcd91d64f7463362`
- cited in: node.lean, node.source, record TFQ-1357
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/Replay.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.ReplayPacketBindingModels.checker_substitution_is_binding_rejected` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.checker_substitution_is_binding_rejected` |
| `AuthorizationIncompleteness.ReplayPacketBindingModels.contract_version_substitution_is_binding_rejected` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.contract_version_substitution_is_binding_rejected` |
| `AuthorizationIncompleteness.ReplayPacketBindingModels.issued_receipt_replays_exact_submission` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.issued_receipt_replays_exact_submission` |
| `AuthorizationIncompleteness.ReplayPacketBindingModels.replay_rejects_payload_substitution` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.replay_rejects_payload_substitution` |
| `AuthorizationIncompleteness.ReplayPacketBindingModels.schema_version_substitution_is_binding_rejected` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.schema_version_substitution_is_binding_rejected` |
| `AuthorizationIncompleteness.ReplayPacketBindingModels.self_pass_cannot_authorize_invalid_content` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.self_pass_cannot_authorize_invalid_content` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1357_authf_replay_substitutions.md`

- file: [dag/derivations/29_computation/tfq_1357_authf_replay_substitutions.md](../../../dag/derivations/29_computation/tfq_1357_authf_replay_substitutions.md)
- sha256 (`lf-normalised`): `39f72e86f4e7a4962bd09dd34d4bf5d6f3fd49cee462ee64d4f1c95c03c50ece`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1357
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-REPLAY-SUBSTITUTIONS` `COMPUTED`: [AUTHF-REPLAY-BOUND-SUBMISSION](AUTHF-REPLAY-BOUND-SUBMISSION.md) (PROVED_LEAN)

Outgoing (0):

