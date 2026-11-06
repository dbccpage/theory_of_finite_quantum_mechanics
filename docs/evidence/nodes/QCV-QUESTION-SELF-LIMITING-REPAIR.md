# QCV-QUESTION-SELF-LIMITING-REPAIR

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Every step of a noisy quantum computation, syndrome extraction and repair included, adds residual, and repair consumes capacity while adding residual of its own; the question is whether this makes reliable completion a self-referential no-go or a threshold condition that holds only under named resource assumptions (fresh supply, net-efficient repair, bounded overhead growth, physical error below threshold).

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The finite model answers the question as a threshold condition (QCV-Q1 to QCV-Q6); whether any physical system meets the named assumptions is not derived and no verdict on physical viability is given.

## Source status

dag/derivations/29_computation/quantum_computation_self_obstruction.md record QCV-Q0 claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/quantum_computation_self_obstruction.md`

- file: [dag/derivations/29_computation/quantum_computation_self_obstruction.md](../../../dag/derivations/29_computation/quantum_computation_self_obstruction.md)
- sha256 (`lf-normalised`): `303d0562ed0666748c50b6b844ae4c57a8e4bd4bef15f817d7f4622a68783ccd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1314_qcv_question_self_limiting_repair.md`

- file: [dag/derivations/29_computation/tfq_1314_qcv_question_self_limiting_repair.md](../../../dag/derivations/29_computation/tfq_1314_qcv_question_self_limiting_repair.md)
- sha256 (`lf-normalised`): `0d3fbe6912f743ba83a8a8629b38fcb7dc62797af4b6ae27199cc3868c90868b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1314
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-QCV-QUESTION-SELF-LIMITING-REPAIR` `GAP_NO_DERIVATION`: [DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE](DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE.md) (OPEN), [DS-QM102-SYNDROME-CAPACITY-BOUND](DS-QM102-SYNDROME-CAPACITY-BOUND.md) (COMPUTATIONALLY_CHECKED), [DS-QM061-BUILDABILITY-SET-S](DS-QM061-BUILDABILITY-SET-S.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `APP-R-QCV-SELF-OBSTRUCTION-MODEL` `DERIVED_PROSE`: [QCV-SELF-OBSTRUCTION-MODEL](QCV-SELF-OBSTRUCTION-MODEL.md) (DEFINITION)
