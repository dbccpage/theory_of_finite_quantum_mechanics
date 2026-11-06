# COMP-POLYNOMIAL-PRESENTATION-INVARIANCE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For two encodings with polynomial-time faithful translations in both directions, polynomial length bounds and polynomial valid-encoding recognition, language membership in P and NP is preserved.

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

- faithful translations in both directions
- polynomial time and size
- decidable validity within polynomial time

## Bottleneck

Translate the input and compose with the target decider. For NP translate the input and use its target verifier; the polynomial target input size gives a polynomial witness-size bound in the source input size. Apply the reverse translation for the converse. Reject invalid encodings before translation. Independent proof review or Lean formalization is still required.

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

### Documents and data: `dag/derivations/29_computation/tfq_2608_comp_polynomial_presentation_invariance.md`

- file: [dag/derivations/29_computation/tfq_2608_comp_polynomial_presentation_invariance.md](../../../dag/derivations/29_computation/tfq_2608_comp_polynomial_presentation_invariance.md)
- sha256 (`lf-normalised`): `1276235090f77833dd10f0a89b45d5892713a43f66b23309f4a05a25cbe45851`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2608
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-COMP-POLYNOMIAL-PRESENTATION-INVARIANCE` `DERIVED_PROSE`: [COMP-NP-VERIFIER-EQUIVALENCE](COMP-NP-VERIFIER-EQUIVALENCE.md) (CONDITIONAL)

Outgoing (0):

