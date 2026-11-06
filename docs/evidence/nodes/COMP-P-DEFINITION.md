# COMP-P-DEFINITION

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> P is the class of languages decided by one deterministic machine in time bounded by a polynomial in encoded input length.

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

- cost model
- uniform polynomial bound

## Bottleneck

This defines a class of language families over inputs of unbounded length. A finite truth table does not establish membership for an unbounded family.

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

### Documents and data: `dag/derivations/29_computation/tfq_2603_comp_p_definition.md`

- file: [dag/derivations/29_computation/tfq_2603_comp_p_definition.md](../../../dag/derivations/29_computation/tfq_2603_comp_p_definition.md)
- sha256 (`lf-normalised`): `5fcd94eee140bf4c7a92de4db42382257c5335aeb688d49220bb4e04667f07b7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2603
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-COMP-P-DEFINITION` `DERIVED_PROSE`: [COMP-COST-MODEL-IMPORT](COMP-COST-MODEL-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `SCI-R-COMP-NP-VERIFIER-EQUIVALENCE` `DERIVED_PROSE`: [COMP-NP-VERIFIER-EQUIVALENCE](COMP-NP-VERIFIER-EQUIVALENCE.md) (CONDITIONAL)
- `SCI-R-COMP-P-VS-NP-OPEN` `GAP_NO_DERIVATION`: [COMP-P-VS-NP-OPEN](COMP-P-VS-NP-OPEN.md) (OPEN)
