# QCV-IMPORT-NOISY-REVERSIBLE-LIMITS

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Aharonov, Ben-Or, Impagliazzo and Nisan (1996) show that noisy reversible or quantum computation with no supply of fresh low-entropy bits cannot preserve its input beyond a short depth; the result is cited, not re-proved or imported as a proof here.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- ABIN 1996 limitation theorem for noisy reversible computation

## Bottleneck

The exact statement and its noise model are in the cited paper; QCV-Q4 establishes a finite exact analogue for global depolarizing noise only.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-IMP-ABIN claims IMPORTED_ASSUMPTION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/tfq_1321_qcv_import_noisy_reversible_limits.md`

- file: [dag/derivations/29_computation/tfq_1321_qcv_import_noisy_reversible_limits.md](../../../dag/derivations/29_computation/tfq_1321_qcv_import_noisy_reversible_limits.md)
- sha256 (`lf-normalised`): `214c92352394f02f001e8041289c11b37418dd47639692203d72801ace45c522`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1321
- counts toward the grade: no

### Documents and data: `dag/research/quantum_computation_self_obstruction.md`

- file: [dag/research/quantum_computation_self_obstruction.md](../../../dag/research/quantum_computation_self_obstruction.md)
- sha256 (`lf-normalised`): `8ae1b2ae291ee74f773da07740ebd0c1f98842bc01d7ec6a4d3c267e0077d178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-QCV-IMPORT-NOISY-REVERSIBLE-LIMITS` `CONDITIONAL_ON_IMPORT`: [DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE](DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY` `DERIVED_LEAN`: [QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY](QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY.md) (PROVED_LEAN)
