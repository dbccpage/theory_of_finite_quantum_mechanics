# COMP-UTM-CONDITIONAL-ROUTE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With separated marks, declared rewriting and unbounded word supply, the existing fixed TM0 machine simulates termination of every encoded partial-recursive program. Its finite mark set is established; output decoding remains a separate open obligation.

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

- admitted separated alphabet
- declared rules
- unbounded word supply
- Mathlib evaluator and compilers

## Bottleneck

Compose the existing forward/backward rewriting simulation with the fixed evaluator compiler chain. This reuses the existing results without a new Lean claim. COMP-C6-TM0-OUTPUT-FORM-OPEN remains open; a halting iff theorem alone is not an output-value theorem.

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

### Documents and data: `dag/derivations/29_computation/tfq_2601_comp_utm_conditional_route.md`

- file: [dag/derivations/29_computation/tfq_2601_comp_utm_conditional_route.md](../../../dag/derivations/29_computation/tfq_2601_comp_utm_conditional_route.md)
- sha256 (`lf-normalised`): `a8959bdca26c7e99c97ff947883005f854555972441c58db2698e43995b39396`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2601
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-COMP-UTM-CONDITIONAL-ROUTE` `CONDITIONAL_ON_IMPORT`: [COMP-C1-CANONICAL-SEPARATED-ALPHABET](COMP-C1-CANONICAL-SEPARATED-ALPHABET.md) (PROVED_LEAN), [COMP-C5-TM0-STEP-SIMULATION](COMP-C5-TM0-STEP-SIMULATION.md) (PROVED_LEAN), [COMP-C6-TM0-HALTING-EQUIVALENCE](COMP-C6-TM0-HALTING-EQUIVALENCE.md) (PROVED_LEAN), [COMP-C6-FINITE-MARKS](COMP-C6-FINITE-MARKS.md) (PROVED_LEAN), [COMP-C4-UNBOUNDED-SUPPLY-IMPORT](COMP-C4-UNBOUNDED-SUPPLY-IMPORT.md) (IMPORTED_ASSUMPTION), [COMP-MARK-ADMISSION-GAP](COMP-MARK-ADMISSION-GAP.md) (OPEN)

Outgoing (1):

- `SCI-R-COMP-COST-MODEL-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-COST-MODEL-IMPORT](COMP-COST-MODEL-IMPORT.md) (IMPORTED_ASSUMPTION)
