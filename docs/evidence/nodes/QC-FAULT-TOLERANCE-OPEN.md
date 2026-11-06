# QC-FAULT-TOLERANCE-OPEN

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Connect the circuit family to available gates, preparation, measurement, recovery and a specified noise model with error and resource bounds uniform in computation size.

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

- noise model
- fault-tolerant gadgets
- uniform decoding and scheduling

## Bottleneck

Finite code-distance, queue and recurrence witnesses retain their stated scope. They do not establish a physical threshold without gadget and noise assumptions and a scaling theorem.

## Source status

Editorial reconstruction with explicit premises; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/13_finite_qm_information/QUANTUM_INFORMATION.md`

- file: [dag/derivations/13_finite_qm_information/QUANTUM_INFORMATION.md](../../../dag/derivations/13_finite_qm_information/QUANTUM_INFORMATION.md)
- sha256 (`lf-normalised`): `8ee593efc75d4739338be886916654c69e07b4143c7c622d3924c25f910b32d7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_2616_qc_fault_tolerance_open.md`

- file: [dag/derivations/29_computation/tfq_2616_qc_fault_tolerance_open.md](../../../dag/derivations/29_computation/tfq_2616_qc_fault_tolerance_open.md)
- sha256 (`lf-normalised`): `72bed53b7bbdfbc54d6cc17e67d67a862846b357ccf13162f92fb0eecbff6633`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2616
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-QC-FAULT-TOLERANCE-OPEN` `GAP_NO_DERIVATION`: [QC-UNIFORM-CIRCUITS-BQP](QC-UNIFORM-CIRCUITS-BQP.md) (DEFINITION), [QC-GATE-ERROR-BUDGET](QC-GATE-ERROR-BUDGET.md) (CONDITIONAL), [QI-ENTROPY-CODING-OBLIGATIONS](QI-ENTROPY-CODING-OBLIGATIONS.md) (OPEN)

Outgoing (0):

