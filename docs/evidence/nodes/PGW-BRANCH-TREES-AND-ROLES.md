# PGW-BRANCH-TREES-AND-ROLES

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With the external continuation policy enabled, isomorphism-quotiented branch DAGs were exported for both readings and both measures within the declared bounds. Under mu2 there is no guard cutoff: the quotient tree to the requested 15 transition steps is finite and enumerated in full, 963 nodes for L and 1847 for F, conditional on the orbit policy losing no child classes, and its leaves are round-cut, carrying 10 or 11 separation responses in L and 10, 11 or 12 in F. Under mu1 the 1200-node pre-expansion guard cuts first at depth 6 (L) and 5 (F), leaving exact exported frontiers of 927 and 886 guard-cut nodes. Counted over accepted edges (L mu1, L mu2, F mu1, F mu2), the recurring roles are supply (195/111/233/413), discrimination by one new instance (1047/858/1001/1458), innovation by a fresh form plus instance (8/53/10/83) and double discrimination (6, F mu2 only); the auxiliary-witness shape never appears among accepted minima.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

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

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/role.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/role.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0448_branch_trees_and_roles.md`

- file: [dag/derivations/02_genesis/tfq_0448_branch_trees_and_roles.md](../../../dag/derivations/02_genesis/tfq_0448_branch_trees_and_roles.md)
- sha256 (`lf-normalised`): `a1a5b457e68891591b239ac1b87f64fe2ad810211096a95555903e852f1d0e05`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0448
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::build_tree`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/role.rs::role`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs::depth_fifteen_reading_f_mu2_is_1847_nodes_with_the_sealed_roles`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs::depth_fifteen_reading_l_mu2_is_963_nodes_and_merges_carry_witnesses`

## Absences recorded by the TFQ records

- TFQ-0448 lean4: no Lean statement of the exported trees; they are finite computations

## Routes

Incoming (1):

- `PGW-R-BRANCH-TREES-AND-ROLES` `COMPUTED`: [PGW-PRUNING-LEMMAS-COST-TWO](PGW-PRUNING-LEMMAS-COST-TWO.md) (PROVED_LEAN), [PGW-COUNT-INVARIANCE-TRANSPORT](PGW-COUNT-INVARIANCE-TRANSPORT.md) (PROVED_LEAN)

Outgoing (0):

