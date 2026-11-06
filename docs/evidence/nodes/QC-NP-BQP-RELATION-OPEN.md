# QC-NP-BQP-RELATION-OPEN

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Determine whether NP is contained in BQP under the standard uniform bounded-error circuit model. Factoring algorithms and finite quantum examples do not resolve this question or P versus NP.

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

Supply a polynomial-time bounded-error algorithm for an NP-complete language to establish containment, or an appropriate separation theorem to refute it. No such result is supplied here.

## Source status

Editorial reconstruction with explicit premises; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md`

- file: [atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md)
- sha256 (`lf-normalised`): `9716b40a77fdcd19feedfec7f0780c2eb16128958609f1fe73e906afe324dee7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_2617_qc_np_bqp_relation_open.md`

- file: [dag/derivations/29_computation/tfq_2617_qc_np_bqp_relation_open.md](../../../dag/derivations/29_computation/tfq_2617_qc_np_bqp_relation_open.md)
- sha256 (`lf-normalised`): `cfedd40160d2cbc489c7c24052845aa408c01af23d0b1148e815379ad4d39526`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2617
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-QC-NP-BQP-RELATION-OPEN` `GAP_NO_DERIVATION`: [COMP-NP-VERIFIER-EQUIVALENCE](COMP-NP-VERIFIER-EQUIVALENCE.md) (CONDITIONAL), [QC-UNIFORM-CIRCUITS-BQP](QC-UNIFORM-CIRCUITS-BQP.md) (DEFINITION)

Outgoing (0):

