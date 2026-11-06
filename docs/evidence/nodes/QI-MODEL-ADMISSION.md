# QI-MODEL-ADMISSION

Stage: [FINITE_QM_INFORMATION](../stages/FINITE_QM_INFORMATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Admit finite-dimensional complex Hilbert systems, tensor composition, positive trace-one states, effects, the Born pairing, and an available class of CPTP operations. These premises define the standard operational quantum information setting.

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

- complex Hilbert systems
- tensor composition
- positive state and effect cones
- Born pairing
- CPTP operation availability

## Bottleneck

The earlier finite and conditional reconstruction results inform these premises but do not select all of them from \<\>. State exactly which operational availability assumptions a downstream theorem uses.

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

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_2610_qi_model_admission.md`

- file: [dag/derivations/13_finite_qm_information/tfq_2610_qi_model_admission.md](../../../dag/derivations/13_finite_qm_information/tfq_2610_qi_model_admission.md)
- sha256 (`lf-normalised`): `d23d09ad9936c8d6591a8de00d5fd7d9a514b30c4a3817904c1e83c5cf9fae3b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2610
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-QI-MODEL-ADMISSION` `CONDITIONAL_ON_IMPORT`: [FQ-POSITIVE-WEIGHTS-ADMITTED](FQ-POSITIVE-WEIGHTS-ADMITTED.md) (IMPORTED_ASSUMPTION), [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL), [FQ-GAP-TENSOR-UNIQUENESS](FQ-GAP-TENSOR-UNIQUENESS.md) (CONDITIONAL), [FQ-CPTP-CLASS-DEFINITION](FQ-CPTP-CLASS-DEFINITION.md) (DEFINITION)

Outgoing (4):

- `SCI-R-QC-UNIFORM-CIRCUITS-BQP` `DERIVED_PROSE`: [QC-UNIFORM-CIRCUITS-BQP](QC-UNIFORM-CIRCUITS-BQP.md) (DEFINITION)
- `SCI-R-QI-CLASSICAL-CHANNEL-LIFT` `DERIVED_PROSE`: [QI-CLASSICAL-CHANNEL-LIFT](QI-CLASSICAL-CHANNEL-LIFT.md) (CONDITIONAL)
- `SCI-R-QI-ENTROPY-CODING-OBLIGATIONS` `GAP_NO_DERIVATION`: [QI-ENTROPY-CODING-OBLIGATIONS](QI-ENTROPY-CODING-OBLIGATIONS.md) (OPEN)
- `SCI-R-QI-NO-CLONING-PAIR` `DERIVED_PROSE`: [QI-NO-CLONING-PAIR](QI-NO-CLONING-PAIR.md) (CONDITIONAL)
