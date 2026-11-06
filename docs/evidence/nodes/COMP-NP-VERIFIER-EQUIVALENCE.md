# COMP-NP-VERIFIER-EQUIVALENCE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Under a fixed finite-branching machine model, polynomial-time nondeterministic acceptance is equivalent to existence of polynomial-length witnesses checked by a deterministic polynomial-time verifier; P is contained in NP.

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

- finite branching
- uniform polynomial bounds
- finite input and witness encodings

## Bottleneck

A nondeterministic machine guesses the bounded witness and runs the verifier. Conversely encode the branch choices of an accepting polynomial-time run and replay them deterministically. There are polynomially many choices of constant bit length. For P containment ignore the witness and run the decider. No separation follows. Independent proof review or Lean formalization is still required.

## Source status

Editorial proof sketch awaiting independent replay; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md`

- file: [atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md)
- sha256 (`lf-normalised`): `b6f7b89589ac601c37dda7e659a4b484f37b68b57d1c1227ed3581ebff25137b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_2604_comp_np_verifier_equivalence.md`

- file: [dag/derivations/29_computation/tfq_2604_comp_np_verifier_equivalence.md](../../../dag/derivations/29_computation/tfq_2604_comp_np_verifier_equivalence.md)
- sha256 (`lf-normalised`): `b4d2b46f91408eaed272d0020cc3434759b57f5d51c9d0974e60aff9bbecb93c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2604
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-COMP-NP-VERIFIER-EQUIVALENCE` `DERIVED_PROSE`: [COMP-P-DEFINITION](COMP-P-DEFINITION.md) (DEFINITION), [COMP-COST-MODEL-IMPORT](COMP-COST-MODEL-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (5):

- `SCI-R-COMP-COOK-LEVIN-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-COOK-LEVIN-IMPORT](COMP-COOK-LEVIN-IMPORT.md) (IMPORTED_ASSUMPTION)
- `SCI-R-COMP-P-VS-NP-OPEN` `GAP_NO_DERIVATION`: [COMP-P-VS-NP-OPEN](COMP-P-VS-NP-OPEN.md) (OPEN)
- `SCI-R-COMP-POLYNOMIAL-PRESENTATION-INVARIANCE` `DERIVED_PROSE`: [COMP-POLYNOMIAL-PRESENTATION-INVARIANCE](COMP-POLYNOMIAL-PRESENTATION-INVARIANCE.md) (CONDITIONAL)
- `SCI-R-COMP-UNARY-BOUNDED-REACH-NP` `DERIVED_PROSE`: [COMP-UNARY-BOUNDED-REACH-NP](COMP-UNARY-BOUNDED-REACH-NP.md) (CONDITIONAL)
- `SCI-R-QC-NP-BQP-RELATION-OPEN` `GAP_NO_DERIVATION`: [QC-NP-BQP-RELATION-OPEN](QC-NP-BQP-RELATION-OPEN.md) (OPEN)
