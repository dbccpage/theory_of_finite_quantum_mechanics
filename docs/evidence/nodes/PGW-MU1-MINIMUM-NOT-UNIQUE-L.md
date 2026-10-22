# PGW-MU1-MINIMUM-NOT-UNIQUE-L

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Under mu1 in reading L the minimum corrective augmentation is not unique. The unary mark deltaU0 and the binary link deltaBL are both valid two-item responses to Challenge 3 on R2L, no response of at most one item is valid, and their results U0 and BL are non-isomorphic because form arity is an isomorphism invariant (mu1_minimum_not_unique, U0_not_iso_BL). The theorem is stated over R2L only.

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

- `proved_lean_below_e3`: grade E0; 2 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 2 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

- Declared item grammar, measure mu1 and the implemented isomorphism relation (assumption)

## Bottleneck

Reading L only: reading-F non-uniqueness is the bounded engine enumeration of five classes (TFQ-0442), and under mu2 the minimum is unique up to isomorphism (TFQ-0382).

## Source status

genesis_source.txt section 7.3 \[theorem, reading L\]; Minimality.lean mu1_minimum_not_unique

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0440_mu1_minimum_not_unique_l.md`

- file: [dag/derivations/02_genesis/tfq_0440_mu1_minimum_not_unique_l.md](../../../dag/derivations/02_genesis/tfq_0440_mu1_minimum_not_unique_l.md)
- sha256 (`lf-normalised`): `0545d5224baeeb6c3728d8ef06f7d927342bac2fd43e2555ce0a5debaaa61c32`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0440
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::min_responses`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs::nothing_below_two_items_separates_the_target`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean::U0_not_iso_BL`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean::mu1_minimum_not_unique`

## Routes

Incoming (1):

- `PGW-R-MU1-MINIMUM-NOT-UNIQUE-L` `DERIVED_LEAN`: [PGW-CHALLENGE3-CURRENT-REGIME-FAILS](PGW-CHALLENGE3-CURRENT-REGIME-FAILS.md) (PROVED_LEAN), [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) (COMPUTATIONALLY_CHECKED)

Outgoing (2):

- `PGW-R-BOUNDED-TIE-CENSUS` `COMPUTED`: [PGW-BOUNDED-TIE-CENSUS](PGW-BOUNDED-TIE-CENSUS.md) (COMPUTATIONALLY_CHECKED)
- `PGW-R-MU1-ARITY-INDEXED-TIE-FAMILY` `DERIVED_LEAN`: [PGW-MU1-ARITY-INDEXED-TIE-FAMILY](PGW-MU1-ARITY-INDEXED-TIE-FAMILY.md) (PROVED_LEAN)
