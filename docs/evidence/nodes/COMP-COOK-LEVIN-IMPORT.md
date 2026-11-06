# COMP-COOK-LEVIN-IMPORT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Cook-Levin theorem supplies a polynomial reduction from nondeterministic polynomial-time acceptance to SAT. Applying NP-hardness to a specific rewriting or sign problem needs a further polynomial reduction.

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

- Cook-Levin theorem
- valid tableau encoding
- polynomial reduction cost

## Bottleneck

The tableau constrains initial configuration, local transitions and acceptance with polynomially many Boolean variables and clauses. This is an imported theorem, not a newly checked Lean result.

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

### Documents and data: `dag/derivations/29_computation/tfq_2606_comp_cook_levin_import.md`

- file: [dag/derivations/29_computation/tfq_2606_comp_cook_levin_import.md](../../../dag/derivations/29_computation/tfq_2606_comp_cook_levin_import.md)
- sha256 (`lf-normalised`): `bb4c3a2fec97c974279480cee0314f69d1d47f7d0b5af4b8e54447c5a1d4a02c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2606
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-COMP-COOK-LEVIN-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-NP-VERIFIER-EQUIVALENCE](COMP-NP-VERIFIER-EQUIVALENCE.md) (CONDITIONAL)

Outgoing (1):

- `SCI-R-COMP-P-VS-NP-OPEN` `GAP_NO_DERIVATION`: [COMP-P-VS-NP-OPEN](COMP-P-VS-NP-OPEN.md) (OPEN)
