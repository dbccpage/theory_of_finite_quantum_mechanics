# QC-GATE-ERROR-BUDGET

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For two L-gate unitary circuits whose corresponding gates differ in operator norm by at most epsilon/L, with L positive, their products differ by at most epsilon.

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

- unitary gates
- operator norm
- positive gate count
- nonnegative error budget

## Bottleneck

Subtract the two products by replacing one factor at a time. Each term is a gate difference multiplied on either side by unitaries, so its norm is at most epsilon/L. Triangle inequality sums L terms. Efficient synthesis to this precision requires a separate theorem for the chosen gate set. Independent proof review or Lean formalization is still required.

## Source status

Editorial proof sketch awaiting independent replay; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md`

- file: [atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md)
- sha256 (`lf-normalised`): `b3aff2eb94aa10a76984e739451717a682e120ab83741ab0f902ca75069cae47`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_2615_qc_gate_error_budget.md`

- file: [dag/derivations/29_computation/tfq_2615_qc_gate_error_budget.md](../../../dag/derivations/29_computation/tfq_2615_qc_gate_error_budget.md)
- sha256 (`lf-normalised`): `35f9156db3b93c40afb6c1af37d6e3482a7024e3b73a8e4c37610c585de7e71b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2615
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-QC-GATE-ERROR-BUDGET` `DERIVED_PROSE`: [QC-UNIFORM-CIRCUITS-BQP](QC-UNIFORM-CIRCUITS-BQP.md) (DEFINITION)

Outgoing (1):

- `SCI-R-QC-FAULT-TOLERANCE-OPEN` `GAP_NO_DERIVATION`: [QC-FAULT-TOLERANCE-OPEN](QC-FAULT-TOLERANCE-OPEN.md) (OPEN)
