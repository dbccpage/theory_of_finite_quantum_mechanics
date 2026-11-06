# COMP-REVERSIBLE-BOOLEAN-EMBEDDING

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For any Boolean function f on a fixed finite input domain, (x,y) maps to (x,y XOR f(x)) by an involutive permutation. Its permutation matrix is unitary in the admitted standard complex inner product.

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

- finite Boolean domain
- standard complex basis and inner product

## Bottleneck

Applying the map twice cancels the two XOR copies of f(x). A permutation matrix has orthonormal columns. This is a representation theorem; efficient implementation additionally requires a circuit and resource bound for f, and no physical quantum structure is selected. Independent proof review or Lean formalization is still required.

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

### Documents and data: `dag/derivations/29_computation/tfq_2609_comp_reversible_boolean_embedding.md`

- file: [dag/derivations/29_computation/tfq_2609_comp_reversible_boolean_embedding.md](../../../dag/derivations/29_computation/tfq_2609_comp_reversible_boolean_embedding.md)
- sha256 (`lf-normalised`): `7d7b1634cfd75a182632c1700d23503e2dfe361c34e19f646bdac8699b0f2699`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2609
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-COMP-REVERSIBLE-BOOLEAN-EMBEDDING` `DERIVED_PROSE`: [COMP-C1-CANONICAL-SEPARATED-ALPHABET](COMP-C1-CANONICAL-SEPARATED-ALPHABET.md) (PROVED_LEAN)

Outgoing (1):

- `SCI-R-QC-UNIFORM-CIRCUITS-BQP` `DERIVED_PROSE`: [QC-UNIFORM-CIRCUITS-BQP](QC-UNIFORM-CIRCUITS-BQP.md) (DEFINITION)
