# QCV-IMPORT-THRESHOLD-THEOREM

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The fault-tolerance threshold theorems (Shor 1996; Aharonov and Ben-Or 1997; Kitaev 1997; Knill, Laflamme and Zurek 1998; Aliferis, Gottesman and Preskill 2006) are cited under each theorem's own noise, locality and overhead hypotheses; they are not re-proved.

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

- threshold theorems for concatenated codes under their stated noise models

## Bottleneck

Exact constants and noise hypotheses of each theorem are not reproduced; the finite recurrence in QCV-Q2 is the only part checked.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-IMP-THRESHOLD claims IMPORTED_ASSUMPTION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/tfq_1318_qcv_import_threshold_theorem.md`

- file: [dag/derivations/29_computation/tfq_1318_qcv_import_threshold_theorem.md](../../../dag/derivations/29_computation/tfq_1318_qcv_import_threshold_theorem.md)
- sha256 (`lf-normalised`): `cf8990b4134fb6ad97ce1fe7c7729fb396fece7854248748994a2d32a7156d82`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1318
- counts toward the grade: no

### Documents and data: `dag/research/quantum_computation_self_obstruction.md`

- file: [dag/research/quantum_computation_self_obstruction.md](../../../dag/research/quantum_computation_self_obstruction.md)
- sha256 (`lf-normalised`): `8ae1b2ae291ee74f773da07740ebd0c1f98842bc01d7ec6a4d3c267e0077d178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-QCV-IMPORT-THRESHOLD-THEOREM` `CONDITIONAL_ON_IMPORT`: [DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE](DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-QCV-CONCATENATION-THRESHOLD-DICHOTOMY` `DERIVED_LEAN`: [QCV-CONCATENATION-THRESHOLD-DICHOTOMY](QCV-CONCATENATION-THRESHOLD-DICHOTOMY.md) (PROVED_LEAN)
