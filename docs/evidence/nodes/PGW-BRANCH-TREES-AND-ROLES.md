# PGW-BRANCH-TREES-AND-ROLES

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With the external continuation policy enabled, isomorphism-quotiented branch DAGs were exported for both readings and both measures within the declared bounds. Under mu2 there is no guard cutoff: the quotient tree to the requested 15 transition steps is finite and enumerated in full, 963 nodes for L and 1847 for F, conditional on the orbit policy losing no child classes, and its leaves are round-cut, carrying 10 or 11 separation responses in L and 10, 11 or 12 in F. Under mu1 the 1200-node pre-expansion guard cuts first at depth 6 (L) and 5 (F), leaving exact exported frontiers of 927 and 886 guard-cut nodes. Counted over accepted edges (L mu1, L mu2, F mu1, F mu2), the recurring roles are supply (195/111/233/413), discrimination by one new instance (1047/858/1001/1458), innovation by a fresh form plus instance (8/53/10/83) and double discrimination (6, F mu2 only); the auxiliary-witness shape never appears among accepted minima.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared resource bounds: at most 2 items, concrete arity at most 2, 15 transition steps, pre-expansion node guards 1200 (mu1) and 3000 (mu2) (assumption)

## Bottleneck

Reaching the requested depth is not unboundedness and no unboundedness claim is made; mu2 completeness is conditional on CL-TREE-MU2-COMPLETE, the mu1 trees are guard-bounded, and behaviour past the exported depths is unresolved.

## Source status

genesis_source.txt section 8.4 \[finite computation\] (CL-BRANCH-REPORTS, CL-TREE-MU2-COMPLETE)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/role.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/role.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/role.rs)
- sha256 (`bytes`): `76b089e5c804fb5477b44614daef467f8592fa4a536ef764a41778e9e221e0b1`
- cited in: node.rust, record TFQ-0448

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `role` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/tree.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/tree.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/tree.rs)
- sha256 (`bytes`): `9099aba7ae1495a15c2291865db9bdd38d8a1779158d4900dacb827e72111f97`
- cited in: node.rust, record TFQ-0448

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `depth_fifteen_reading_f_mu2_is_1847_nodes_with_the_sealed_roles` (rust_test) | yes | yes | yes | - | - |
| `depth_fifteen_reading_l_mu2_is_963_nodes_and_merges_carry_witnesses` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py)
- sha256 (`bytes`): `23803a3dcce2adf0dee623caba33791d41a25d2da3fdfd226da3cad2ee140b5e`
- cited in: record TFQ-0448

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `build_tree` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0448_branch_trees_and_roles.md`

- file: [dag/derivations/02_genesis/tfq_0448_branch_trees_and_roles.md](../../../dag/derivations/02_genesis/tfq_0448_branch_trees_and_roles.md)
- sha256 (`lf-normalised`): `3214d21e6f2a974577f4d7cbba8c84a8fdb783816e3a0369d410ff4bd9a89609`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0448
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0448 lean4: no Lean statement of the exported trees; they are finite computations

## Routes

Incoming (1):

- `PGW-R-BRANCH-TREES-AND-ROLES` `COMPUTED`: [PGW-PRUNING-LEMMAS-COST-TWO](PGW-PRUNING-LEMMAS-COST-TWO.md) (PROVED_LEAN), [PGW-COUNT-INVARIANCE-TRANSPORT](PGW-COUNT-INVARIANCE-TRANSPORT.md) (PROVED_LEAN)

Outgoing (0):

