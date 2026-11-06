# QI-ENTROPY-CODING-OBLIGATIONS

Stage: [FINITE_QM_INFORMATION](../stages/FINITE_QM_INFORMATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Connect the admitted state and channel models to source coding, channel capacity and error-correction claims with explicit code families, error metrics, asymptotic limits and achievability/converse statements.

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

- specified entropy base
- code and channel families
- error criterion
- asymptotic regime

## Bottleneck

Finite trace or entropy identities do not discharge operational coding theorems. Import a precise external theorem or supply a repository proof with matching hypotheses. Keep natural-log entropy distinct from entropy in bits.

## Source status

Editorial reconstruction with explicit premises; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/13_finite_qm_information/quantum_information.md`

- file: [dag/derivations/13_finite_qm_information/quantum_information.md](../../../dag/derivations/13_finite_qm_information/quantum_information.md)
- sha256 (`lf-normalised`): `8ee593efc75d4739338be886916654c69e07b4143c7c622d3924c25f910b32d7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_2613_qi_entropy_coding_obligations.md`

- file: [dag/derivations/13_finite_qm_information/tfq_2613_qi_entropy_coding_obligations.md](../../../dag/derivations/13_finite_qm_information/tfq_2613_qi_entropy_coding_obligations.md)
- sha256 (`lf-normalised`): `dfac696cf4687018c7b1a3918b582ba8ded2dbfdbe0fd69f5280a8c48ae21625`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2613
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-QI-ENTROPY-CODING-OBLIGATIONS` `GAP_NO_DERIVATION`: [QI-MODEL-ADMISSION](QI-MODEL-ADMISSION.md) (IMPORTED_ASSUMPTION), [FQ-ENTROPY-DICHOTOMY-BAKER](FQ-ENTROPY-DICHOTOMY-BAKER.md) (PROVED_LEAN)

Outgoing (1):

- `SCI-R-QC-FAULT-TOLERANCE-OPEN` `GAP_NO_DERIVATION`: [QC-FAULT-TOLERANCE-OPEN](QC-FAULT-TOLERANCE-OPEN.md) (OPEN)
