# QC-UNIFORM-CIRCUITS-BQP

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With the admitted quantum model and an efficiently specified finite gate set, BQP consists of languages decided by polynomial-time uniform polynomial-size circuit families with acceptance at least 2/3 for yes instances and at most 1/3 for no instances.

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

- uniform classical circuit generator
- polynomial gate count
- ancilla preparation
- finite gate specification
- Born measurement

## Bottleneck

Uniformity, input encoding, gate resources and bounded error are part of the definition. Classical control and quantum model admission are both prerequisites; the P versus NP open node is not a prerequisite.

## Source status

Editorial reconstruction with explicit premises; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md`

- file: [atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md)
- sha256 (`lf-normalised`): `b6f7b89589ac601c37dda7e659a4b484f37b68b57d1c1227ed3581ebff25137b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_2614_qc_uniform_circuits_bqp.md`

- file: [dag/derivations/29_computation/tfq_2614_qc_uniform_circuits_bqp.md](../../../dag/derivations/29_computation/tfq_2614_qc_uniform_circuits_bqp.md)
- sha256 (`lf-normalised`): `6b3564b7bff4f07fd17c40e0031400f48d8fb4a2be09636b1d012ea9dc2e13ea`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2614
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-QC-UNIFORM-CIRCUITS-BQP` `DERIVED_PROSE`: [QI-MODEL-ADMISSION](QI-MODEL-ADMISSION.md) (IMPORTED_ASSUMPTION), [COMP-COST-MODEL-IMPORT](COMP-COST-MODEL-IMPORT.md) (IMPORTED_ASSUMPTION), [COMP-REVERSIBLE-BOOLEAN-EMBEDDING](COMP-REVERSIBLE-BOOLEAN-EMBEDDING.md) (CONDITIONAL)

Outgoing (3):

- `SCI-R-QC-FAULT-TOLERANCE-OPEN` `GAP_NO_DERIVATION`: [QC-FAULT-TOLERANCE-OPEN](QC-FAULT-TOLERANCE-OPEN.md) (OPEN)
- `SCI-R-QC-GATE-ERROR-BUDGET` `DERIVED_PROSE`: [QC-GATE-ERROR-BUDGET](QC-GATE-ERROR-BUDGET.md) (CONDITIONAL)
- `SCI-R-QC-NP-BQP-RELATION-OPEN` `GAP_NO_DERIVATION`: [QC-NP-BQP-RELATION-OPEN](QC-NP-BQP-RELATION-OPEN.md) (OPEN)
