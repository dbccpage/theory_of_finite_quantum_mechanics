# COMP-COST-MODEL-IMPORT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Complexity is measured after fixing finite input encodings, input length, a uniform machine model and elementary step costs. Computable simulation alone gives no polynomial overhead bound.

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

- finite encoding
- input length
- uniform machine model
- elementary cost

## Bottleneck

Prove overhead bounds for each implementation translation used in a complexity claim. Keep computability and efficient simulation distinct.

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

### Documents and data: `dag/derivations/29_computation/tfq_2602_comp_cost_model_import.md`

- file: [dag/derivations/29_computation/tfq_2602_comp_cost_model_import.md](../../../dag/derivations/29_computation/tfq_2602_comp_cost_model_import.md)
- sha256 (`lf-normalised`): `9fc7f619092f9450f26e576c12d7314a669bc2a148112aedcee5f75fc62b678c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2602
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-COMP-COST-MODEL-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-UTM-CONDITIONAL-ROUTE](COMP-UTM-CONDITIONAL-ROUTE.md) (CONDITIONAL)

Outgoing (3):

- `SCI-R-COMP-NP-VERIFIER-EQUIVALENCE` `DERIVED_PROSE`: [COMP-NP-VERIFIER-EQUIVALENCE](COMP-NP-VERIFIER-EQUIVALENCE.md) (CONDITIONAL)
- `SCI-R-COMP-P-DEFINITION` `DERIVED_PROSE`: [COMP-P-DEFINITION](COMP-P-DEFINITION.md) (DEFINITION)
- `SCI-R-QC-UNIFORM-CIRCUITS-BQP` `DERIVED_PROSE`: [QC-UNIFORM-CIRCUITS-BQP](QC-UNIFORM-CIRCUITS-BQP.md) (DEFINITION)
